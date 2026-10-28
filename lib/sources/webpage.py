"""Web pages as sources: URL normalization, a headless-Chromium capture, an HTML-to-markdown extract and a
Wayback Machine capture (Internet Archive Save Page Now 2).

Playwright is imported only where a capture runs, so the rest of the tooling works without a browser
(``just install`` installs Chromium). Pages behind a login or paywall need the Zotero browser button.
"""

from __future__ import annotations

import hashlib
import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

from lib.sources import env

SPN_SAVE = "https://web.archive.org/save"
SPN_STATUS = "https://web.archive.org/save/status/{job_id}"
USER_AGENT = "Switchbox-sources/1.0 (+https://switch.box)"
_TRACKING = re.compile(
    r"^(utm_.*|fbclid|gclid|dclid|mc_cid|mc_eid|igshid|ref|ref_src|cmpid|_hsenc|_hsmi|mkt_tok)$", re.I
)
_FURNITURE = ("script", "style", "noscript", "nav", "header", "footer", "aside", "form", "iframe", "svg", "button")
_FURNITURE_ROLES = ("navigation", "banner", "contentinfo", "complementary", "search")


def normalize_url(url: str) -> str:
    """Lowercase host, https, no fragment, no tracking parameters, sorted query, no trailing slash.

    >>> normalize_url("HTTP://Www.Example.com/a/b/?utm_source=x&b=2&a=1#top")
    'https://www.example.com/a/b?a=1&b=2'
    """
    parts = urlsplit(url.strip())
    query = sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not _TRACKING.match(k))
    path = parts.path.rstrip("/") if parts.path != "/" else ""
    return urlunsplit(("https", parts.netloc.lower(), path, urlencode(query), ""))


def md5_of(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


@dataclass(frozen=True)
class Capture:
    """What a browser capture of a page produced."""

    url: str
    final_url: str
    title: str
    captured_at: str  # ISO date
    pdf_path: Path
    html_path: Path
    pdf_md5: str


def capture(url: str, out_dir: Path, stem: str, timeout_ms: int = 60_000) -> Capture:
    """Render ``url`` in headless Chromium and save ``<stem>.pdf`` and ``<stem>.html`` in ``out_dir``."""
    from playwright.sync_api import sync_playwright

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path, html_path = out_dir / f"{stem}.pdf", out_dir / f"{stem}.html"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(user_agent=USER_AGENT)
            page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            html_path.write_text(page.content(), encoding="utf-8")
            title, final_url = page.title(), page.url
            page.pdf(path=str(pdf_path), format="Letter", print_background=True)
        finally:
            browser.close()
    return Capture(
        url, final_url, title, datetime.now(UTC).date().isoformat(), pdf_path, html_path, md5_of(pdf_path.read_bytes())
    )


def page_metadata(html: str) -> dict[str, Any]:
    """Title, authors, date, site name and DOI from a page's ``<meta>`` tags (empty keys when absent)."""
    soup = BeautifulSoup(html, "html.parser")

    def meta(*names: str) -> list[str]:
        out = []
        for n in names:
            for tag in soup.find_all("meta", attrs={"name": n}) + soup.find_all("meta", attrs={"property": n}):
                if (c := str(tag.get("content") or "").strip()) and c not in out:
                    out.append(c)
        return out

    title = (meta("citation_title", "og:title") or [soup.title.get_text(strip=True) if soup.title else ""])[0]
    return {
        "title": title,
        "authors": meta("citation_author", "author", "article:author"),
        "date": next(iter(meta("citation_publication_date", "citation_date", "article:published_time", "date")), ""),
        "site_name": next(iter(meta("og:site_name", "citation_journal_title")), ""),
        "doi": next(iter(meta("citation_doi", "dc.identifier", "DC.identifier")), ""),
    }


def html_to_markdown(html: str) -> str:
    """The page's main content as markdown, without navigation, headers, footers, forms or scripts."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(_FURNITURE):
        tag.decompose()
    for tag in soup.find_all(attrs={"role": list(_FURNITURE_ROLES)}):
        tag.decompose()
    root = soup.find("main") or soup.find("article") or soup.body or soup
    text = markdownify(str(root), heading_style="ATX", strip=["img"])
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


# --- Wayback Machine ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WaybackResult:
    """Outcome of a Save Page Now request."""

    ok: bool
    url: str | None  # https://web.archive.org/web/<timestamp>/<original>
    blocked: bool
    message: str


def _spn_headers() -> dict[str, str]:
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    access, secret = env.get("IA_ACCESS_KEY"), env.get("IA_SECRET_KEY")
    if access and secret:
        headers["Authorization"] = f"LOW {access}:{secret}"
    return headers


def wayback_save(
    url: str,
    session: requests.Session | None = None,
    poll_seconds: float = 5.0,
    timeout_seconds: float = 300.0,
    sleep: Callable[[float], None] = time.sleep,
) -> WaybackResult:
    """Request a capture and wait for it. Anonymous requests work but are rate-limited harder.

    Blocked sites (``robots``/``blocked`` status extensions) return ``blocked=True`` so the card can say so.
    """
    http = session or requests
    r = http.post(
        SPN_SAVE,
        headers=_spn_headers(),
        data={"url": url, "capture_all": "1", "if_not_archived_within": "1d"},
        timeout=60,
    )
    if r.status_code in (401, 403, 429):
        return WaybackResult(False, None, False, f"Wayback refused the request ({r.status_code})")
    r.raise_for_status()
    body = r.json()
    job_id = body.get("job_id")
    if not job_id:
        return WaybackResult(False, None, False, body.get("message") or "no job id in the Wayback response")
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        status = http.get(SPN_STATUS.format(job_id=job_id), headers=_spn_headers(), timeout=60).json()
        if status.get("status") == "success":
            original = status.get("original_url") or url
            return WaybackResult(True, f"https://web.archive.org/web/{status['timestamp']}/{original}", False, "")
        if status.get("status") == "error":
            ext = status.get("status_ext") or ""
            message = status.get("message") or ext or "capture failed"
            return WaybackResult(
                False, None, bool(re.search(r"blocked|robots|forbidden", ext + message, re.I)), message
            )
        sleep(poll_seconds)
    return WaybackResult(False, None, False, f"capture still pending after {timeout_seconds:.0f}s (job {job_id})")
