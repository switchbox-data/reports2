#!/usr/bin/env python3
"""Find and fetch NJ Board of Public Utilities (NJBPU) docket filings and board orders.

Standard library only (plus contextlib). The NJ BPU Public Document Search site
(publicaccess.bpu.state.nj.us) uses an Incapsula/Imperva WAF that
requires a browser-like User-Agent and cookie-warming handshake.
Board orders on nj.gov and tariffs on nj.pseg.com have no WAF.

Subcommands
-----------
case      ER23120924                     -> list documents in a docket
fetch     1359943 [-o DIR]               -> download one document by ID
search    "PUBLIC SERVICE" --type party   -> search by docket or party name
order     2024-10-09 "2A ORDER PS 23 BRC" [-o DIR]
                                         -> download a board order PDF

Examples
--------
  S=.cursor/skills/njbpu-documents/scripts/fetch_njbpu.py
  uv run python $S case ER23120924
  uv run python $S fetch 1359943 -o /tmp/nj
  uv run python $S search ER23120924 --type docket
  uv run python $S search "PUBLIC SERVICE ELECTRIC" --type party
  uv run python $S order 2024-10-09 "2A ORDER PS 23 BRC" -o /tmp/nj
"""

from __future__ import annotations

import argparse
import contextlib
import html as html_mod
import http.cookiejar
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path

BASE = "https://publicaccess.bpu.state.nj.us"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# HTTP helpers with Incapsula cookie-warming
# ---------------------------------------------------------------------------

_opener: urllib.request.OpenerDirector | None = None


def _get_opener() -> urllib.request.OpenerDirector:
    """Build a urllib opener with a persistent cookie jar.

    The Incapsula WAF sets visid_incap_*, nlbi_*, incap_ses_*, and
    ASP.NET_SessionId cookies across a 3-request warm-up. We keep
    the cookie jar alive for the session.
    """
    global _opener
    if _opener is None:
        cj = http.cookiejar.CookieJar()
        _opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj),
            urllib.request.HTTPRedirectHandler(),
        )
    return _opener


def _warm_cookies(url: str) -> None:
    """Two throwaway GETs to populate the Incapsula cookies."""
    opener = _get_opener()
    for _ in range(2):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with contextlib.suppress(urllib.error.HTTPError):
            opener.open(req, timeout=30)


_warmed = False


def bpu_get(url: str, timeout: int = 120) -> bytes:
    """GET a BPU page, handling Incapsula warm-up on first call."""
    global _warmed
    if not _warmed:
        _warm_cookies(url)
        _warmed = True
    opener = _get_opener()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=timeout) as resp:
        return resp.read()


def bpu_text(url: str) -> str:
    return bpu_get(url).decode("utf-8", errors="replace")


def plain_get(url: str, timeout: int = 120) -> tuple[bytes, str, str]:
    """GET without Incapsula (nj.gov, nj.pseg.com). Returns (body, ctype, final_url)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers.get("Content-Type", ""), resp.geturl()


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------


def _clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html_mod.unescape(s).replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", s)).strip()


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Document:
    document_id: str
    docket: str
    title: str
    folder: str
    uploaded_by: str
    description: str
    posted_date: str
    url: str


@dataclass
class SearchResult:
    docket: str
    case_id: str
    case_type: str
    open_date: str
    caption: str
    party_name: str
    status: str


# ---------------------------------------------------------------------------
# case: list documents in a docket
# ---------------------------------------------------------------------------


def parse_case_summary(page_html: str) -> list[Document]:
    """Parse the gvDocuments grid from CaseSummary.aspx."""
    docs: list[Document] = []
    # Each document row has a link to DocumentHandler.ashx?document_id=...
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", page_html, flags=re.S | re.I)
    for row in rows:
        m = re.search(r"DocumentHandler\.ashx\?document_id=(\d+)", row)
        if not m:
            continue
        doc_id = m.group(1)
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S | re.I)
        if len(tds) < 7:
            continue
        # Columns: checkbox, docket, title, folder, uploaded_by, description, posted_date
        docket = _clean(tds[1])
        title = _clean(tds[2])
        folder = _clean(tds[3])
        uploaded_by = _clean(tds[4])
        description = _clean(tds[5])
        posted_date = _clean(tds[6])
        url = f"{BASE}/DocumentHandler.ashx?document_id={doc_id}"
        docs.append(
            Document(
                document_id=doc_id,
                docket=docket,
                title=title,
                folder=folder,
                uploaded_by=uploaded_by,
                description=description,
                posted_date=posted_date,
                url=url,
            )
        )
    return docs


def find_case_id(docket: str, page_html: str) -> str | None:
    """Extract case_id from a redirect or the page content."""
    m = re.search(r"case_id=(\d+)", page_html)
    return m.group(1) if m else None


def cmd_case(args: argparse.Namespace) -> None:
    docket = args.docket.strip().upper()
    # Search by docket number to find the case_id
    search_url = f"{BASE}/SearchResults.aspx?SearchType=CaseNumber&SearchText={urllib.parse.quote(docket)}"
    page = bpu_text(search_url)

    # If single result, we may land on CaseSummary directly
    case_id = find_case_id(docket, page)

    if case_id:
        # We either got redirected or the case_id is on the page
        case_url = f"{BASE}/CaseSummary.aspx?case_id={case_id}"
        page = bpu_text(case_url)
    else:
        # Multiple results — look for the matching docket link
        m = re.search(rf"CaseSummary\.aspx\?case_id=(\d+).*?{re.escape(docket)}", page, re.S | re.I)
        if not m:
            raise SystemExit(f"Could not find case for docket {docket}")
        case_id = m.group(1)
        case_url = f"{BASE}/CaseSummary.aspx?case_id={case_id}"
        page = bpu_text(case_url)

    docs = parse_case_summary(page)

    if args.json:
        print(json.dumps([asdict(d) for d in docs], indent=2))
        return

    print(f"# Docket {docket} (case_id={case_id}): {len(docs)} documents")
    print()
    for d in docs:
        print(f"  {d.document_id:<10} {d.folder:<35} {d.posted_date:<12} {d.title[:120]}")
    print()
    print("# Fetch a document: uv run python <script> fetch <document_id> -o <dir>")


# ---------------------------------------------------------------------------
# fetch: download one document by document_id
# ---------------------------------------------------------------------------


def is_pdf(body: bytes) -> bool:
    return body[:5] == b"%PDF-" and len(body) > 1024


def save(body: bytes, dest_dir: Path, name: str) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / name
    path.write_bytes(body)
    kind = "PDF" if is_pdf(body) else f"unknown ({len(body)} bytes)"
    print(f"saved {path} ({len(body):,} bytes, {kind})")
    return path


def cmd_fetch(args: argparse.Namespace) -> None:
    doc_id = args.document_id.strip()
    if not doc_id.isdigit():
        raise SystemExit(f"document_id must be an integer, got {doc_id!r}")
    url = f"{BASE}/DocumentHandler.ashx?document_id={doc_id}"
    body = bpu_get(url)

    if not is_pdf(body):
        # Check if we got an HTML page (WAF challenge or error)
        text = body[:500].decode("utf-8", errors="replace")
        if "<html" in text.lower():
            raise SystemExit(f"Got HTML instead of PDF for document_id={doc_id}. The WAF may have blocked the request.")
        raise SystemExit(f"Response does not look like a PDF ({len(body)} bytes)")

    # Try to get the original filename from Content-Disposition
    # Since we can't get headers from the opener easily, use the doc_id
    name = args.name or f"njbpu_{doc_id}.pdf"
    if not name.endswith(".pdf"):
        name += ".pdf"
    save(body, Path(args.output_dir), name)


# ---------------------------------------------------------------------------
# search: query the portal by docket number or party name
# ---------------------------------------------------------------------------


def parse_search_results(page_html: str) -> list[SearchResult]:
    """Parse the search results grid."""
    results: list[SearchResult] = []
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", page_html, flags=re.S | re.I)
    for row in rows:
        m = re.search(r"CaseSummary\.aspx\?case_id=(\d+)", row)
        if not m:
            continue
        case_id = m.group(1)
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S | re.I)
        if len(tds) < 6:
            continue
        results.append(
            SearchResult(
                docket=_clean(tds[0]),
                case_id=case_id,
                case_type=_clean(tds[1]),
                open_date=_clean(tds[2]),
                caption=_clean(tds[3]),
                party_name=_clean(tds[4]),
                status=_clean(tds[5]) if len(tds) > 5 else "",
            )
        )
    return results


def cmd_search(args: argparse.Namespace) -> None:
    query = args.query.strip()
    search_type = "CaseNumber" if args.type == "docket" else "PartyName"
    url = f"{BASE}/SearchResults.aspx?SearchType={search_type}&SearchText={urllib.parse.quote(query)}"
    page = bpu_text(url)

    # Check if we got redirected to a case summary (single result)
    if "CaseSummary.aspx" in page and "gvDocuments" in page:
        case_id = find_case_id(query, page)
        print(f"# Single result: case_id={case_id}")
        print(f"  {BASE}/CaseSummary.aspx?case_id={case_id}")
        return

    results = parse_search_results(page)

    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2))
        return

    print(f"# Search '{query}' (type={search_type}): {len(results)} results")
    print()
    for r in results:
        print(f"  {r.docket:<20} {r.open_date:<12} {r.status:<10} case_id={r.case_id}")
        print(f"    {r.caption[:120]}")
    if not results:
        print("  (no results)")


# ---------------------------------------------------------------------------
# order: download a board order from nj.gov
# ---------------------------------------------------------------------------


def cmd_order(args: argparse.Namespace) -> None:
    """Download a board order PDF from nj.gov.

    Board orders live at:
    https://www.nj.gov/bpu/pdf/boardorders/{YYYY}/{YYYYMMDD}/{name}.pdf
    The name uses the agenda item number with spaces.
    """
    date = args.date.strip()
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", date)
    if not m:
        raise SystemExit("Date must be YYYY-MM-DD")
    yyyy, mm, dd = m.groups()
    yyyymmdd = f"{yyyy}{mm}{dd}"

    name = args.name.strip()
    # URL-encode spaces in the filename
    encoded_name = urllib.parse.quote(name)
    if not encoded_name.lower().endswith(".pdf"):
        encoded_name += ".pdf"

    url = f"https://www.nj.gov/bpu/pdf/boardorders/{yyyy}/{yyyymmdd}/{encoded_name}"
    print(f"# Fetching: {url}", file=sys.stderr)

    try:
        body, ctype, _final = plain_get(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # Try the meeting orders page to list available orders
            listing = f"https://www.nj.gov/bpu/agenda/{yyyy}calendar/approved/{yyyymmdd}.html"
            print("# 404: order not found at that path.", file=sys.stderr)
            print(f"# Try browsing the meeting page: {listing}", file=sys.stderr)
            raise SystemExit(f"Order not found: {url}") from e
        raise

    if not is_pdf(body):
        raise SystemExit(f"Response does not look like a PDF ({ctype}, {len(body)} bytes)")

    # Use the order name as filename
    safe_name = re.sub(r"[^\w\-. ]", "_", name)
    save(body, Path(args.output_dir), f"{safe_name}.pdf")
    print(f"source: {url}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    # case
    p = sub.add_parser("case", help="list documents in a docket")
    p.add_argument("docket", help="e.g. ER23120924")
    p.add_argument("--json", action="store_true", help="output as JSON")
    p.set_defaults(fn=cmd_case)

    # fetch
    p = sub.add_parser("fetch", help="download one document by document_id")
    p.add_argument("document_id", help="e.g. 1359943")
    p.add_argument("-o", "--output-dir", default=".", help="directory to save the PDF")
    p.add_argument("-n", "--name", default=None, help="override the output filename")
    p.set_defaults(fn=cmd_fetch)

    # search
    p = sub.add_parser("search", help="search by docket number or party name")
    p.add_argument("query", help="search text")
    p.add_argument(
        "--type",
        choices=["docket", "party"],
        default="docket",
        help="search type (default: docket)",
    )
    p.add_argument("--json", action="store_true", help="output as JSON")
    p.set_defaults(fn=cmd_search)

    # order
    p = sub.add_parser("order", help="download a board order by date and name")
    p.add_argument("date", help="meeting date YYYY-MM-DD")
    p.add_argument("name", help="order filename, e.g. '2A ORDER PS 23 BRC'")
    p.add_argument("-o", "--output-dir", default=".", help="directory to save the PDF")
    p.set_defaults(fn=cmd_order)

    args = ap.parse_args()
    try:
        args.fn(args)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} for {e.url}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error: {e.reason}") from e


if __name__ == "__main__":
    main()
