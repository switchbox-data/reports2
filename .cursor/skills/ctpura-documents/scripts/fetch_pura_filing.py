#!/usr/bin/env python3
"""Fetch Connecticut PURA filings from the Lotus Domino docket database.

Two subcommands:

    filing  Parse one filing page (metadata + attachment list) to JSON, and
            optionally download its PDFs (and merge them into one file).
    docket  List the filings in one docket from the Electric docket view,
            optionally expanding interrogatory rows to show their responses.

Usage:
    uv run python scripts/fetch_pura_filing.py filing '<filing URL>'
    uv run python scripts/fetch_pura_filing.py filing '<filing URL>' -o /tmp/set3 \\
        --merge /tmp/set3/pura_260510_eversource_resp_clf_sc_set3.pdf
    uv run python scripts/fetch_pura_filing.py docket 26-05-10 --match CLF --expand

Single-quote every PURA URL: they contain `$FILE`, which the shell (and `just`)
would otherwise expand to an empty string.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urljoin

BASE = "https://www.dpuc.state.ct.us"
ELECTRIC_VIEW = "/DOCKCURR.NSF/$FormDocketElectricRevView"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; Switchbox-reports2/1.0; +https://switch.box/)"}
FIELDS = {
    "docket_number": "Docket Number",
    "official_filer": "Official Filer(s) Name",
    "filing_firm": "Filing Firm's Name",
    "company": "Company Name",
    "date_filed": "Date Filed",
    "interrogatories_answered": "Interrogatories answered",
    "comment": "Comment",
    "supplemental_or_revision": "Supplemental or Revision",
    "docket_title": "Docket Title",
    "directed_from": "Directed from",
    "directed_to": "Directed to",
    "first_interrogatory": "Beginning Interrogatory Number",
    "last_interrogatory": "Ending Interrogatory Number",
    "date_issued": "Date Issued",
    "date_due": "Indicated Date Due",
}


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def page_text(raw: str) -> list[str]:
    text = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", raw)
    text = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|td|h\d|li)>", "\n", text)
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_filing(url: str, raw: str) -> dict:
    lines = page_text(raw)
    record: dict = {"url": url, "heading": lines[0] if lines else ""}
    # Response pages put "Label: value" on one line; interrogatory pages put the
    # value on the next line, sometimes after a parenthetical hint.
    for key, label in FIELDS.items():
        pattern = re.compile(rf"^{re.escape(label)}(?:\s*\[[^\]]*\])?:\s*(.*)$")
        for i, line in enumerate(lines):
            match = pattern.match(line)
            if not match:
                continue
            value = match.group(1)
            following = (n for n in lines[i + 1 :] if not n.startswith("("))
            if not value.strip():
                value = next(following, "")
            record[key] = re.sub(r"\s+", " ", value).strip()
            break
    attachments = []
    for href in dict.fromkeys(re.findall(r'href="([^"]*/\$FILE/[^"]+)"', raw, re.IGNORECASE)):
        absolute = urljoin(BASE, html.unescape(href))
        attachments.append({"name": unquote(absolute.rsplit("/", 1)[-1]), "url": absolute})
    record["attachments"] = attachments
    return record


def download(attachments: list[dict], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for attachment in attachments:
        data = get(attachment["url"])
        if not data.startswith(b"%PDF") or len(data) < 1024:
            sys.exit(f"Not a PDF (or under 1 KB): {attachment['url']}")
        path = out_dir / attachment["name"]
        path.write_bytes(data)
        print(f"{path} ({len(data):,} bytes)", file=sys.stderr)
        paths.append(path)
    return paths


def merge(paths: list[Path], out: Path) -> None:
    from pypdf import PdfWriter

    writer = PdfWriter()
    for path in paths:
        writer.append(str(path))
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as handle:
        writer.write(handle)
    print(f"merged {len(paths)} files into {out}", file=sys.stderr)


def view_rows(expand: str | None) -> list[str]:
    query = "?OpenForm&Start=1&Count=1000" + (f"&Expand={expand}&Seq=1" if expand else "&CollapseView")
    raw = get(BASE + ELECTRIC_VIEW + query).decode("latin-1")
    return re.findall(r"<tr[^>]*>(.*?)</tr>", raw, re.DOTALL)


def row_text(row: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", row))).strip()


def row_link(row: str) -> str | None:
    match = re.search(r'href="([^"]*\?OpenDocument)"', row)
    return urljoin(BASE, html.unescape(match.group(1))) if match else None


def row_expand(row: str) -> str | None:
    match = re.search(r"Expand=([0-9.]+)", row)
    return match.group(1) if match else None


def list_docket(docket: str, match: str | None, expand_children: bool) -> list[dict]:
    year = "20" + docket[:2]
    year_row = next((r for r in view_rows(None) if row_text(r).startswith(year)), None)
    if year_row is None or row_expand(year_row) is None:
        sys.exit(f"No {year} category in the Electric docket view")
    docket_row = next((r for r in view_rows(row_expand(year_row)) if f"[{docket}]" in row_text(r)), None)
    if docket_row is None:
        sys.exit(f"Docket {docket} not found in the Electric view's {year} dockets")
    docket_index = row_expand(docket_row)
    rows = view_rows(docket_index)
    start = next(i for i, r in enumerate(rows) if f"[{docket}]" in row_text(r))
    filings = []
    for row in rows[start + 1 :]:
        text = row_text(row)
        if re.search(r"\[\d\d-\d\d-\d\d", text):
            break
        if match and match.lower() not in text.lower():
            continue
        entry: dict = {"title": text, "url": row_link(row)}
        child_index = row_expand(row)
        if expand_children and child_index and text.startswith("Interrogs"):
            child_rows = view_rows(child_index)
            at = next(i for i, r in enumerate(child_rows) if row_text(r) == text)
            entry["responses"] = []
            for r in child_rows[at + 1 :]:
                if not row_text(r).startswith("Question(s) Answered"):
                    break
                entry["responses"].append({"title": row_text(r), "url": row_link(r)})
        filings.append(entry)
    return filings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    filing = sub.add_parser("filing", help="Parse a filing page; optionally download its PDFs")
    filing.add_argument("url", help="Filing page URL (…?OpenDocument); single-quote it")
    filing.add_argument("-o", "--output-dir", type=Path, help="Download the attachments here")
    filing.add_argument("--merge", type=Path, help="Also merge the downloaded PDFs into this file")
    docket = sub.add_parser("docket", help="List a docket's filings (Electric view)")
    docket.add_argument("docket", help="Docket number, e.g. 26-05-10")
    docket.add_argument("--match", help="Only rows whose title contains this text (case-insensitive)")
    docket.add_argument("--expand", action="store_true", help="List the responses under each interrogatory row")
    args = parser.parse_args()

    if args.command == "filing":
        record = parse_filing(args.url, get(args.url).decode("latin-1"))
        if args.merge and not args.output_dir:
            parser.error("--merge needs --output-dir")
        if args.output_dir:
            paths = download(record["attachments"], args.output_dir)
            if args.merge:
                merge(paths, args.merge)
        print(json.dumps(record, indent=2))
    else:
        print(json.dumps(list_docket(args.docket, args.match, args.expand), indent=2))


if __name__ == "__main__":
    main()
