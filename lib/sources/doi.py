"""Find a document's DOI, and check it, so Zotero's ``url`` can be a ``doi.org`` link.

Order, stopping at the first candidate that Crossref confirms is *this* document:

1. the DOI Zotero already has;
2. the PDF's XMP metadata;
3. the first two pages, and running headers/footers (a DOI repeated in the top or bottom lines of at least
   three pages) -- never the body or the reference list, whose DOIs belong to other papers;
4. the download URL, or ``citation_doi`` on its landing page;
5. a Crossref bibliographic search that matches the title almost exactly.

Every candidate is resolved at Crossref and its title compared with the document's; mismatches are discarded.
``open_access_pdf`` asks Unpaywall for a free copy of a DOI. Both services want a contact e-mail
(``SOURCES_CONTACT_EMAIL``) so requests land in their polite pools.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit

import requests
from rapidfuzz import fuzz

from lib.sources import env

CROSSREF = "https://api.crossref.org/works"
UNPAYWALL = "https://api.unpaywall.org/v2"
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>]+)", re.IGNORECASE)
TITLE_MATCH = 90
SEARCH_MATCH = 97
FRONT_PAGES = 2
RUNNING_LINES = 2
RUNNING_PAGES = 3
TIMEOUT = 30

Fetch = Callable[..., Any]


@dataclass(frozen=True)
class DoiResult:
    doi: str
    source: str  # which step found it: zotero, xmp, front_pages, url, landing_page, crossref_search
    verified: bool  # Crossref resolved it and the title matched (False only when no title was available)

    @property
    def url(self) -> str:
        return f"https://doi.org/{self.doi}"


def clean(doi: str) -> str:
    """A DOI without the punctuation and ``doi:`` / ``https://doi.org/`` wrappers that surround it in text."""
    doi = re.sub(r"^(?:doi:\s*|https?://(?:dx\.)?doi\.org/)", "", doi.strip(), flags=re.IGNORECASE)
    return doi.rstrip(".,;:)]}>'\"")


def dois_in(text: str) -> list[str]:
    return [clean(m) for m in DOI_RE.findall(text)]


def _title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", title.lower()).strip()


def _headers() -> dict[str, str]:
    mail = env.get("SOURCES_CONTACT_EMAIL")
    return {"User-Agent": f"switchbox-sources/1.0 (mailto:{mail})" if mail else "switchbox-sources/1.0"}


def _get_json(url: str, params: Mapping[str, Any] | None = None, fetch: Fetch | None = None) -> dict[str, Any] | None:
    resp = (fetch or requests.get)(url, params=dict(params or {}), headers=_headers(), timeout=TIMEOUT)
    if resp.status_code != 200:
        return None
    return resp.json()


def crossref_title(doi: str, fetch: Fetch | None = None) -> str | None:
    """The Crossref title for ``doi``; ``None`` when Crossref does not know the DOI."""
    data = _get_json(f"{CROSSREF}/{quote(doi, safe='/')}", fetch=fetch)
    titles = ((data or {}).get("message") or {}).get("title") or []
    return titles[0] if titles else None


def verify(doi: str, title: str, fetch: Fetch | None = None) -> bool:
    """Whether ``doi`` resolves at Crossref to a title that matches ``title``."""
    found = crossref_title(doi, fetch)
    return found is not None and fuzz.ratio(_title_key(found), _title_key(title)) >= TITLE_MATCH


def from_xmp(pdf: Path) -> list[str]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf))
    found: list[str] = []
    xmp = reader.xmp_metadata
    if xmp is not None:
        for ident in getattr(xmp, "dc_identifier", None) or []:
            found += dois_in(str(ident))
        found += dois_in(
            " ".join(str(v) for v in (getattr(xmp, "prism_doi", None), getattr(xmp, "pdfx_doi", None)) if v)
        )
    info = reader.metadata
    if info is not None:
        found += dois_in(" ".join(str(v) for v in (info.get("/doi"), info.get("/DOI"), info.get("/Subject")) if v))
    return list(dict.fromkeys(found))


def from_front_pages(pdf: Path) -> list[str]:
    """DOIs on the first two pages, plus DOIs repeated in the top/bottom lines of three or more pages."""
    from pypdf import PdfReader

    pages = PdfReader(str(pdf)).pages
    found = dois_in("\n".join((p.extract_text() or "") for p in pages[:FRONT_PAGES]))
    running: Counter[str] = Counter()
    for page in pages:
        lines = [ln for ln in (page.extract_text() or "").splitlines() if ln.strip()]
        edge = lines[:RUNNING_LINES] + lines[-RUNNING_LINES:]
        running.update({d for ln in edge for d in dois_in(ln)})
    found += [d for d, n in running.items() if n >= RUNNING_PAGES]
    return list(dict.fromkeys(found))


def from_url(url: str, fetch: Fetch | None = None) -> list[tuple[str, str]]:
    """``(doi, step)`` pairs from the URL itself, or from ``citation_doi`` / ``dc.identifier`` on its landing page."""
    found: list[tuple[str, str]] = [(d, "url") for d in dois_in(url)]
    if found or urlsplit(url).path.lower().endswith(".pdf"):
        return found
    try:
        resp = (fetch or requests.get)(url, headers=_headers(), timeout=TIMEOUT)
    except requests.RequestException:
        return found
    if resp.status_code != 200 or "html" not in resp.headers.get("content-type", "html"):
        return found
    for m in re.finditer(
        r"""<meta[^>]+name=["'](?:citation_doi|dc\.identifier|prism\.doi)["'][^>]*>""", resp.text, re.I
    ):
        content = re.search(r"""content=["']([^"']+)["']""", m.group(0))
        if content:
            found += [(d, "landing_page") for d in dois_in(content.group(1))]
    return found


def search_crossref(title: str, author: str | None = None, fetch: Fetch | None = None) -> str | None:
    """A DOI whose Crossref title matches ``title`` almost exactly, from a bibliographic search."""
    params: dict[str, Any] = {"query.bibliographic": title, "rows": 3}
    if author:
        params["query.author"] = author
    items = ((_get_json(CROSSREF, params, fetch) or {}).get("message") or {}).get("items") or []
    for item in items:
        found = (item.get("title") or [""])[0]
        if found and fuzz.ratio(_title_key(found), _title_key(title)) >= SEARCH_MATCH:
            return clean(item["DOI"])
    return None


def find_doi(
    title: str | None = None,
    pdf: Path | None = None,
    source_url: str | None = None,
    zotero_doi: str | None = None,
    author: str | None = None,
    fetch: Fetch | None = None,
) -> DoiResult | None:
    """The first DOI for the document that Crossref confirms; ``None`` when there is none."""
    candidates: list[tuple[str, str]] = []
    if zotero_doi:
        candidates.append((clean(zotero_doi), "zotero"))
    if pdf is not None and Path(pdf).suffix.lower() == ".pdf":
        candidates += [(d, "xmp") for d in from_xmp(pdf)]
        candidates += [(d, "front_pages") for d in from_front_pages(pdf)]
    if source_url:
        candidates += from_url(source_url, fetch)
    seen: set[str] = set()
    for doi, step in candidates:
        if doi.lower() in seen:
            continue
        seen.add(doi.lower())
        if title is None:
            return DoiResult(doi, step, verified=False)
        if verify(doi, title, fetch):
            return DoiResult(doi, step, verified=True)
    if title:
        doi = search_crossref(title, author, fetch)
        if doi:
            return DoiResult(doi, "crossref_search", verified=True)
    return None


def open_access_pdf(doi: str, fetch: Fetch | None = None) -> str | None:
    """URL of a free PDF for ``doi`` from Unpaywall, if one exists.

    Unpaywall's best location is often a landing page with no PDF link; then the other locations are tried,
    published versions first.
    """
    mail = env.get("SOURCES_CONTACT_EMAIL")
    if not mail:
        return None
    data = _get_json(f"{UNPAYWALL}/{quote(doi, safe='/')}", {"email": mail}, fetch) or {}
    best = data.get("best_oa_location") or {}
    if best.get("url_for_pdf"):
        return best["url_for_pdf"]
    others = sorted(data.get("oa_locations") or [], key=lambda loc: loc.get("version") != "publishedVersion")
    return next((loc["url_for_pdf"] for loc in others if loc.get("url_for_pdf")), None)
