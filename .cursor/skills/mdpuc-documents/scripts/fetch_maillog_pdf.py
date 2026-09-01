#!/usr/bin/env python3
"""Download a Maryland PSC DMS document by MailLog number.

The DMS MailLog search resolves the real pdfview path. Direct filing URLs
often return 0 bytes — do not bypass this two-step lookup.

Usage:
    uv run python scripts/fetch_maillog_pdf.py 218934 -o /tmp/ml218934.pdf
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests

BASE = "https://webpscxb.pscmaryland.com"
MAILLOG_SEARCH = f"{BASE}/DMS/maillogsearch"
SESSION_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (compatible; Switchbox-reports2/1.0; +https://switch.box/)"),
}


def _extract_hidden_fields(html: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for name in ("__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"):
        match = re.search(
            rf'name="{name}"[^>]*value="([^"]*)"',
            html,
            re.IGNORECASE,
        )
        if match:
            fields[name] = match.group(1)
    return fields


def _first_data_pdf(html: str) -> str | None:
    for pattern in (
        r'data-pdf="([^"]+)"',
        r"data-pdf='([^']+)'",
    ):
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    return None


def _first_maillog_viewer_path(html: str, maillog: str) -> str | None:
    match = re.search(
        rf"/DMS/maillogpdfview/MailLog/0/0/{re.escape(maillog)}/\d+",
        html,
    )
    return match.group(0) if match else None


def resolve_maillog_pdf_url(session: requests.Session, maillog: str) -> str:
    """Return absolute pdfview URL for a MailLog number."""
    search_page = session.get(MAILLOG_SEARCH, timeout=60)
    search_page.raise_for_status()

    payload = {
        **_extract_hidden_fields(search_page.text),
        "ctl00$ContentPlaceHolder1$txtSearch": maillog,
        "ctl00$ContentPlaceHolder1$btnSearch": "Search",
    }
    if "__VIEWSTATE" not in payload:
        msg = "Could not parse ASP.NET form fields from maillogsearch page"
        raise RuntimeError(msg)

    results = session.post(MAILLOG_SEARCH, data=payload, timeout=60)
    results.raise_for_status()

    viewer_path = _first_data_pdf(results.text) or _first_maillog_viewer_path(results.text, maillog)
    if not viewer_path:
        msg = f"No data-pdf found in MailLog search results for ML {maillog}"
        raise RuntimeError(msg)

    viewer_url = urljoin(BASE, viewer_path)
    viewer_page = session.get(viewer_url, timeout=60)
    viewer_page.raise_for_status()

    pdf_path = _first_data_pdf(viewer_page.text)
    if not pdf_path:
        msg = f"No data-pdf found on MailLog viewer page for ML {maillog}"
        raise RuntimeError(msg)

    return urljoin(BASE, pdf_path)


def download_maillog_pdf(maillog: str, output_path: Path) -> Path:
    with requests.Session() as session:
        session.headers.update(SESSION_HEADERS)
        pdf_url = resolve_maillog_pdf_url(session, maillog)
        response = session.get(pdf_url, timeout=120)
        response.raise_for_status()

        if len(response.content) < 1000:
            msg = (
                f"Downloaded only {len(response.content)} bytes from {pdf_url}. "
                "Expected a PDF — direct DMS paths often fail; MailLog lookup may "
                "have resolved incorrectly."
            )
            raise RuntimeError(msg)

        if not response.content.startswith(b"%PDF"):
            msg = f"Response from {pdf_url} does not look like a PDF"
            raise RuntimeError(msg)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(response.content)
        return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("maillog", help="MailLog number (e.g. 218934)")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="Output PDF path",
    )
    args = parser.parse_args()

    try:
        path = download_maillog_pdf(args.maillog.strip(), args.output)
    except (RuntimeError, requests.RequestException) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"saved {path} ({path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
