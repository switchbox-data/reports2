#!/usr/bin/env python3
"""Find and fetch Oregon PUC (OPUC) eDocket filings and orders.

Standard library only. The OPUC site (apps.puc.state.or.us, edocs.puc.state.or.us)
needs no login and no browser; it only wants a browser-like User-Agent.

Subcommands
-----------
docket-id  "UM 2377"                    -> internal DocketID (e.g. 24470)
docket     "UM 2377" [--match TEXT] [--action TYPE] [--since YYYY-MM-DD] [--json]
                                        -> every action in the docket, with
                                           direct PDF URLs (or order numbers)
dockets    [--category UE] [--company NAME] [--open] [--since D] [--match RE]
                                        -> docket search by type/company/date
tariffs    --company NAME [--pending] [--since D] [--until D] [--match RE]
                                        -> advice (tariff) filings: advice no.,
                                           ADV docket, status, effective date
company    "portland general"           -> company id(s) for --company
order      26-154 [-o DIR]              -> download an order (PDF or .htm)
fetch      <FileName|URL> [-o DIR]      -> download one eDocket filing, e.g.
                                           um2377htb342431028.pdf

Examples
--------
  S=.cursor/skills/orpuc-documents/scripts/fetch_orpuc.py
  uv run python $S docket-id "UM 2377"
  uv run python $S docket "UM 2377" --match "Surrebuttal" --action "TESTIMONY"
  uv run python $S tariffs --company "portland general" --since 2026-01-01 --match "SCHEDULE 7"
  uv run python $S dockets --category UE --company "portland general" --open
  uv run python $S order 26-154 -o /tmp/or
  uv run python $S fetch um2377htb342431028.pdf -o /tmp/or
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path

APPS = "https://apps.puc.state.or.us"
EDOCKETS = f"{APPS}/edockets"
EFDOCS = "https://edocs.puc.state.or.us/efdocs"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"


def http_get(url: str, timeout: int = 120) -> tuple[bytes, str, str]:
    """GET following redirects; returns (body, content_type, final_url)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers.get("Content-Type", ""), resp.geturl()


def get_text(url: str) -> str:
    body, _, _ = http_get(url)
    return body.decode("cp1252", errors="replace")


def split_docket(label: str) -> tuple[str, str]:
    """'UM 2377' / 'um2377' / 'UE-457' -> ('UM', '2377')."""
    m = re.fullmatch(r"\s*([A-Za-z]{2,3})[\s\-_]*(\d{1,6})\s*", label)
    if not m:
        raise SystemExit(f"Cannot parse docket number {label!r}; use e.g. 'UM 2377'")
    return m.group(1).upper(), m.group(2)


def find_docket_ids(label: str) -> list[str]:
    """Look a docket number up through the site's own search form.

    The Prefix option values are four characters wide ('UM  ', 'UE  ', 'LC  '),
    so the prefix must be space-padded.
    """
    prefix, number = split_docket(label)
    qs = urllib.parse.urlencode({"Prefix": prefix.ljust(4), "DocketNumber": number, "submit1": "GO"})
    page = get_text(f"{EDOCKETS}/srchlist.asp?{qs}")
    ids = re.findall(r"DocketID=(\d+)", page, flags=re.I)
    return list(dict.fromkeys(ids))


def resolve_docket_id(arg: str) -> str:
    if arg.isdigit() and int(arg) > 9999:  # already an internal DocketID
        return arg
    ids = find_docket_ids(arg)
    if not ids:
        raise SystemExit(f"No eDocket found for {arg!r}")
    if len(ids) > 1:
        print(f"warning: {arg!r} matched DocketIDs {ids}; using {ids[0]}", file=sys.stderr)
    return ids[0]


@dataclass
class Action:
    date: str  # M/D/YYYY as printed
    iso_date: str
    action: str  # e.g. TESTIMONY & EXHIBITS, ORDER, OTHER FILING/PLEADING
    description: str
    order_no: str | None = None
    file_type: str | None = None  # HTB, HBC, ...
    file_name: str | None = None
    url: str | None = None  # direct PDF URL (filings) or order redirect URL
    extra_files: list[str] = field(default_factory=list)


def _iso(date: str) -> str:
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", date.strip())
    return f"{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}" if m else date


def _clean(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s).replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", s)).strip()


def parse_actions(page: str) -> list[Action]:
    """Parse the ACTIONS table of docket.asp.

    Each action is a block starting at '<b>Date:' with: the date cell, the
    action-type cell, a cell holding the document link, optionally an
    'Order No:' row, and a 'Description' row. The link sits in the *date* row
    above its description, so split on the date marker, not on <tr>.
    """
    blocks = re.split(r"<b>Date:", page)[1:]
    actions: list[Action] = []
    for blk in blocks:
        date_m = re.search(r"</b>\s*(\d{1,2}/\d{1,2}/\d{4})", blk)
        act_m = re.search(r"Action:\s*(?:&nbsp;)?\s*</b>\s*(.*?)(?:&nbsp;)?\s*</td>", blk, re.S)
        if not (date_m and act_m):
            continue
        desc_m = re.search(r"Description</b>\s*<br>(.*?)</td>", blk, re.S)
        order_m = re.search(r"Order No:\s*(?:&nbsp;)?\s*</b>\s*([\d\-]+)", blk)
        files = re.findall(r'href="edocs\.asp\?FileType=([A-Z]+)&amp;FileName=([^&"]+)', blk)
        order_link = re.search(r'href="orders\.asp\?OrderNumber=([\d\-]+)"', blk)
        a = Action(
            date=date_m.group(1),
            iso_date=_iso(date_m.group(1)),
            action=_clean(act_m.group(1)),
            description=_clean(desc_m.group(1)) if desc_m else "",
            order_no=order_m.group(1) if order_m else (order_link.group(1) if order_link else None),
        )
        if files:
            a.file_type, a.file_name = files[0]
            a.url = f"{EFDOCS}/{a.file_type}/{a.file_name}"
            a.extra_files = [f"{EFDOCS}/{t}/{n}" for t, n in files[1:]]
        elif order_link:
            a.url = f"{EDOCKETS}/orders.asp?OrderNumber={order_link.group(1)}"
        actions.append(a)
    return actions


def get_docket(arg: str) -> tuple[str, list[Action], str]:
    did = resolve_docket_id(arg)
    page = get_text(f"{EDOCKETS}/docket.asp?DocketID={did}")
    name = re.search(r"Docket Name:</b>(.*?)</td>", page, re.S)
    title = _clean(name.group(1)) if name else ""
    return did, parse_actions(page), title


@dataclass
class Row:
    """One row of a srchlist.asp result table (dockets or tariffs)."""

    label: str  # 'UE 475' (dockets) or '26-43 / ADV 1911' (tariffs)
    docket: str | None
    docket_id: str | None
    advice_no: str | None
    title: str
    filed: str
    status: str | None
    effective: str | None  # tariffs: effective date; dockets: final order date
    file_type: str | None
    file_name: str | None
    url: str | None


_search_page: str | None = None


def search_page() -> str:
    global _search_page
    if _search_page is None:
        _search_page = get_text(f"{EDOCKETS}/search.asp")
    return _search_page


def find_companies(name: str) -> list[tuple[str, str]]:
    """Match a company by id or name substring against the search form's list."""
    opts = re.findall(
        r"<option value='(\d+)'>([^<]*)</option>",
        search_page()[search_page().find('name="Company"') :],
    )
    opts = [(i, html.unescape(n).strip()) for i, n in opts]
    if name.isdigit():
        return [o for o in opts if o[0] == name]
    pat = re.compile(re.escape(name), re.I)
    return [o for o in opts if pat.search(o[1])]


def resolve_company(name: str) -> str:
    hits = find_companies(name)
    if not hits:
        raise SystemExit(f"No company matches {name!r}; try `company <part of name>`")
    exact = [h for h in hits if h[1].lower() == name.lower()]
    if len(hits) > 1 and not exact:
        listing = "; ".join(f"{i} {n}" for i, n in hits[:10])
        raise SystemExit(f"{name!r} is ambiguous: {listing}")
    return (exact or hits)[0][0]


def _date_params(since: str | None, until: str | None) -> dict[str, str]:
    if not (since or until):
        return {}
    y0, m0, d0 = (since or "1990-01-01").split("-")
    y1, m1, d1 = (until or "2099-12-31").split("-")
    if until is None:
        import datetime as _dt

        t = _dt.date.today()
        y1, m1, d1 = str(t.year), str(t.month), str(t.day)
    return {
        "DateRange": "usedate",
        "StartMonth": str(int(m0)),
        "StartDay": str(int(d0)),
        "StartYear": y0,
        "EndMonth": str(int(m1)),
        "EndDay": str(int(d1)),
        "EndYear": y1,
    }


def parse_rows(page: str, tariff: bool) -> list[Row]:
    rows: list[Row] = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", page, flags=re.S):
        dm = re.search(r'href="docket\.asp\?DocketID=(\d+)">(.*?)</a>', tr, re.S)
        if not dm:
            continue
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, flags=re.S)
        first = re.split(r"<br>", re.sub(r"<a .*", "", tds[0], flags=re.S), flags=re.I)
        parts = [_clean(x) for x in first if _clean(x)]
        fm = re.search(r"edocs\.asp\?FileType=([A-Z]+)&amp;FileName=([^&\"\s>]+)", tr)
        filed = next(
            (_clean(t) for t in tds if re.fullmatch(r"\s*\d{1,2}/\d{1,2}/\d{4}\s*(&nbsp;)?\s*", t)),
            "",
        )
        tail = [_clean(t) for t in tds[-2:]] if len(tds) >= 5 else ["", ""]
        r = Row(
            label=" / ".join(parts),
            docket=next((p for p in parts if re.match(r"[A-Z]{2,3}\s*\d+$", p)), None),
            docket_id=dm.group(1),
            advice_no=parts[0] if tariff and parts else None,
            title=_clean(dm.group(2)),
            filed=filed,
            status=tail[0] or None,
            effective=tail[1] or None,
            file_type=fm.group(1) if fm else None,
            file_name=fm.group(2) if fm else None,
            url=f"{EFDOCS}/{fm.group(1)}/{fm.group(2)}" if fm else None,
        )
        rows.append(r)
    return rows


def _in_range(filed: str, since: str | None, until: str | None) -> bool:
    iso = _iso(filed)
    return (not since or iso >= since) and (not until or iso <= until)


def _print_rows(rows: list[Row], as_json: bool, tariff: bool) -> None:
    if as_json:
        print(json.dumps([asdict(r) for r in rows], indent=2))
        return
    print(f"# {len(rows)} results")
    for r in rows:
        status = (r.status or "").replace("[PDF]", "").strip()
        if tariff:
            extra = f"  {status} {('eff ' + r.effective) if r.effective else ''}"
        else:  # dockets: final order number and date, when there is one
            extra = f"  final order {status} {r.effective or ''}" if status else ""
        extra = extra.rstrip()
        print(f"{_iso(r.filed)}  {r.label:<22} DocketID {r.docket_id}{extra}")
        print(f"    {r.title[:180]}")
        if r.url:
            print(f"    {r.url}")


def cmd_company(args: argparse.Namespace) -> None:
    hits = find_companies(args.name)
    if not hits:
        raise SystemExit(f"No company matches {args.name!r}")
    for i, n in hits:
        print(f"{i}\t{n}")


def _criteria_search(args: argparse.Namespace, search_type: str) -> list[Row]:
    params: dict[str, str] = {"SearchType": search_type, "Category": getattr(args, "category", "") or ""}
    cat = params["Category"]
    if cat:
        params["Category"] = cat.upper().ljust(4)  # option values are 4 chars wide
    params["Company"] = resolve_company(args.company) if args.company else ""
    if getattr(args, "open", False):
        params["chkOpen"] = "open"
    if getattr(args, "pending", False):
        params["chkPending"] = "pending"
    params.update(_date_params(args.since, args.until))
    params["submit3"] = "Submit"
    page = get_text(f"{EDOCKETS}/srchlist.asp?{urllib.parse.urlencode(params)}")
    rows = parse_rows(page, tariff=(search_type == "Tariff"))
    if args.match:
        pat = re.compile(args.match, re.I)
        rows = [r for r in rows if pat.search(r.title) or pat.search(r.label)]
    return [r for r in rows if _in_range(r.filed, args.since, args.until)] if args.since or args.until else rows


def cmd_dockets(args: argparse.Namespace) -> None:
    if not (args.category or args.company):
        raise SystemExit("Give --category and/or --company (searching everything returns thousands)")
    _print_rows(_criteria_search(args, "Docket"), args.json, tariff=False)


def cmd_tariffs(args: argparse.Namespace) -> None:
    if not args.company:
        raise SystemExit("--company is required (use `company <name>` to find it)")
    _print_rows(_criteria_search(args, "Tariff"), args.json, tariff=True)


def cmd_docket_id(args: argparse.Namespace) -> None:
    ids = find_docket_ids(args.docket)
    if not ids:
        raise SystemExit(f"No eDocket found for {args.docket!r}")
    print("\n".join(ids))


def cmd_docket(args: argparse.Namespace) -> None:
    did, actions, title = get_docket(args.docket)
    rows = actions
    if args.match:
        pat = re.compile(args.match, re.I)
        rows = [a for a in rows if pat.search(a.description) or pat.search(a.order_no or "")]
    if args.action:
        pat = re.compile(args.action, re.I)
        rows = [a for a in rows if pat.search(a.action)]
    if args.since:
        rows = [a for a in rows if a.iso_date >= args.since]
    if args.json:
        print(json.dumps([asdict(a) for a in rows], indent=2))
        return
    print(f"# DocketID {did}: {title} ({len(rows)} of {len(actions)} actions)")
    for a in rows:
        label = (a.order_no and f"Order {a.order_no}") or (a.file_name or "-")
        print(f"{a.iso_date}  {a.action:<28} {label}")
        if a.description:
            print("    " + a.description.splitlines()[0][:200])
        if a.url:
            print(f"    {a.url}")


def is_pdf(body: bytes) -> bool:
    return body[:5] == b"%PDF-" and len(body) > 1024


def save(body: bytes, ctype: str, dest_dir: Path, name: str) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / name
    path.write_bytes(body)
    kind = "PDF" if is_pdf(body) else ctype or "unknown type"
    print(f"saved {path} ({len(body):,} bytes, {kind})")
    return path


def cmd_order(args: argparse.Namespace) -> None:
    """orders.asp 302-redirects to the real file (PDF since ~2000, .htm for old ones)."""
    num = args.order_number
    if not re.fullmatch(r"\d{2}-\d{1,4}", num):
        raise SystemExit("Order number looks like 26-154")
    body, ctype, final = http_get(f"{EDOCKETS}/orders.asp?OrderNumber={num}")
    name = Path(urllib.parse.urlparse(final).path).name or f"{num}.pdf"
    if name.lower() == "orders.asp":
        raise SystemExit(f"Order {num} not found (no redirect to a file)")
    save(body, ctype, Path(args.output_dir), name)
    print(f"source: {final}")


def cmd_fetch(args: argparse.Namespace) -> None:
    target = args.file
    if target.startswith("http"):
        url = target
    else:
        # FileName = [<docket>]<FileType><digits>.pdf, e.g. um2377 + htb + 342431028
        # (advice filings omit the docket: uaa350016029.pdf)
        m = re.match(r"(?i)^(?:[a-z]{2,3}\d+)?([a-z]{3})\d+\.pdf$", target)
        if not m:
            raise SystemExit("Give a FileName like um2377htb342431028.pdf or a full URL")
        url = f"{EFDOCS}/{m.group(1).upper()}/{target}"
    body, ctype, final = http_get(url)
    if not is_pdf(body):
        raise SystemExit(f"{final} did not return a PDF ({ctype}, {len(body)} bytes)")
    save(body, ctype, Path(args.output_dir), Path(urllib.parse.urlparse(final).path).name)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("docket-id", help="docket number -> internal DocketID")
    p.add_argument("docket", help="e.g. 'UM 2377'")
    p.set_defaults(fn=cmd_docket_id)

    p = sub.add_parser("docket", help="list a docket's actions with direct file URLs")
    p.add_argument("docket", help="'UM 2377' or an internal DocketID like 24470")
    p.add_argument("--match", help="regex on description / order number")
    p.add_argument("--action", help="regex on action type, e.g. 'TESTIMONY|BRIEF|ORDER'")
    p.add_argument("--since", help="only actions on/after YYYY-MM-DD")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_docket)

    p = sub.add_parser("company", help="find a company id by name")
    p.add_argument("name", help="part of the name, e.g. 'portland general'")
    p.set_defaults(fn=cmd_company)

    def add_search_args(p: argparse.ArgumentParser) -> None:
        p.add_argument("--company", help="company id or part of the name")
        p.add_argument("--since", help="YYYY-MM-DD, filed on/after")
        p.add_argument("--until", help="YYYY-MM-DD, filed on/before")
        p.add_argument("--match", help="regex on title / advice number / docket")
        p.add_argument("--json", action="store_true")

    p = sub.add_parser("dockets", help="search dockets by category, company and date")
    p.add_argument("--category", help="docket prefix: UE, UG, UM, LC, ADV, ...")
    p.add_argument("--open", action="store_true", help="only open dockets")
    add_search_args(p)
    p.set_defaults(fn=cmd_dockets)

    p = sub.add_parser("tariffs", help="search advice (tariff) filings by company and date")
    p.add_argument("--pending", action="store_true", help="only pending advice filings")
    add_search_args(p)
    p.set_defaults(fn=cmd_tariffs)

    p = sub.add_parser("order", help="download an order by number, e.g. 26-154")
    p.add_argument("order_number")
    p.add_argument("-o", "--output-dir", default=".")
    p.set_defaults(fn=cmd_order)

    p = sub.add_parser("fetch", help="download one eDocket filing by FileName or URL")
    p.add_argument("file")
    p.add_argument("-o", "--output-dir", default=".")
    p.set_defaults(fn=cmd_fetch)

    args = ap.parse_args()
    try:
        args.fn(args)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} for {e.url}") from e
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error: {e.reason}") from e


if __name__ == "__main__":
    main()
