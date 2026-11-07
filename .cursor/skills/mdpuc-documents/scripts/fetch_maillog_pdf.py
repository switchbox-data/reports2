#!/usr/bin/env python3
"""Download a Maryland PSC DMS document by MailLog number.

The DMS MailLog search resolves the real pdfview path. Direct filing URLs
often return 0 bytes — do not bypass this two-step lookup.

Cloudflare challenges every https request, and the maillogpdfview viewer page
over http too, from datacenter IPs (EC2). Over http with a browser User-Agent,
the search page and the final pdfview download still pass. If the viewer step
is challenged, open the viewer URL in a real browser (e.g. the Cursor IDE
browser), copy the `data-pdf` of the `btnOpenPdfFile` button, and pass it as
--pdf-path.

Usage:
    uv run python scripts/fetch_maillog_pdf.py 218934 -o /tmp/ml218934.pdf
    uv run python scripts/fetch_maillog_pdf.py 321573 -o /tmp/ml321573.pdf \
        --pdf-path '/DMS/pdfview/%60%60wportal%60Documents%60DMS%6032%601573%60/...~pdf'
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests

BASE = "http://webpscxb.pscmaryland.com"
MAILLOG_SEARCH = f"{BASE}/DMS/maillogsearch"
SESSION_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    ),
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
    if viewer_page.status_code == 403 and viewer_page.headers.get("cf-mitigated"):
        msg = (
            f"Cloudflare challenged the MailLog viewer for ML {maillog}. Open "
            f"{viewer_url.replace('http://', 'https://')} in a real browser, copy the "
            "data-pdf of the btnOpenPdfFile button, and rerun with --pdf-path."
        )
        raise RuntimeError(msg)
    viewer_page.raise_for_status()

    pdf_path = _first_data_pdf(viewer_page.text)
    if not pdf_path:
        msg = f"No data-pdf found on MailLog viewer page for ML {maillog}"
        raise RuntimeError(msg)

    return urljoin(BASE, pdf_path)


def download_maillog_pdf(maillog: str, output_path: Path, pdf_path: str | None = None) -> Path:
    with requests.Session() as session:
        session.headers.update(SESSION_HEADERS)
        if pdf_path:
            pdf_url = urljoin(BASE, re.sub(r"^https?://[^/]+", "", pdf_path))
        else:
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
    parser.add_argument(
        "--pdf-path",
        help="data-pdf of the viewer's btnOpenPdfFile button (skips the MailLog lookup)",
    )
    args = parser.parse_args()

    try:
        path = download_maillog_pdf(args.maillog.strip(), args.output, args.pdf_path)
    except (RuntimeError, requests.RequestException) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"saved {path} ({path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
