"""DOI finding: front matter and running headers count, the reference list never does; Crossref confirms."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from lib.sources import doi
from tests.sources.pdfs import make_pdf

TITLE = "Heat Pump Rates and Cross-Subsidies in New England"
OWN = "10.1016/j.enpol.2024.114321"
CITED = "10.1000/cited.reference.77"


class Crossref:
    """A fake of ``requests.get`` for Crossref and landing pages."""

    def __init__(self, titles: dict[str, str], search: list[dict] | None = None, pages: dict[str, str] | None = None):
        self.titles, self.search, self.pages, self.requested = titles, search or [], pages or {}, []

    def __call__(self, url: str, params=None, headers=None, timeout=None, **_):
        self.requested.append(url)
        if url.startswith(doi.CROSSREF + "/"):
            d = url[len(doi.CROSSREF) + 1 :]
            if d in self.titles:
                return SimpleNamespace(status_code=200, json=lambda: {"message": {"title": [self.titles[d]]}})
            return SimpleNamespace(status_code=404, json=lambda: {})
        if url == doi.CROSSREF:
            return SimpleNamespace(status_code=200, json=lambda: {"message": {"items": self.search}})
        if url in self.pages:
            return SimpleNamespace(status_code=200, text=self.pages[url], headers={"content-type": "text/html"})
        return SimpleNamespace(status_code=404, text="", headers={})


@pytest.fixture
def paper(tmp_path: Path) -> Path:
    pages = [
        [TITLE, "Ana Lopez", f"https://doi.org/{OWN}", "Abstract. We study rates."],
        ["Introduction", "Body text."],
        ["Body text continues."],
        ["References", "Smith, J. (2020). Another paper.", f"https://doi.org/{CITED}"],
    ]
    return make_pdf(pages, tmp_path / "paper.pdf")


def test_clean_strips_wrappers_and_punctuation():
    assert doi.clean("https://doi.org/10.1234/ABC.def).") == "10.1234/ABC.def"
    assert doi.clean("doi: 10.1234/x;") == "10.1234/x"
    assert doi.dois_in("see (10.1234/abc), and 10.5555/z.1.") == ["10.1234/abc", "10.5555/z.1"]


def test_front_page_doi_is_found_and_reference_list_doi_is_ignored(paper):
    found = doi.from_front_pages(paper)
    assert OWN in found
    assert CITED not in found  # page 4 is the reference list: only the first two pages count


def test_running_header_doi_counts_when_repeated_on_three_pages(tmp_path):
    pages = [
        ["Journal of Rates  " + OWN, "Body"] + ["text"] * 3,
        ["Journal of Rates  " + OWN, "more"],
        ["Journal of Rates  " + OWN, "more"],
        ["Journal of Rates  " + OWN, "end"],
    ]
    path = make_pdf(pages, tmp_path / "running.pdf")
    assert doi.from_front_pages(path) == [OWN]


def test_a_doi_in_one_late_footer_is_not_a_running_footer(tmp_path):
    pages = [["No identifier here"], ["Body"], ["Body"], ["Body"], ["Smith (2020).", f"doi {CITED}"]]
    assert doi.from_front_pages(make_pdf(pages, tmp_path / "late.pdf")) == []


def test_info_dictionary_doi(tmp_path):
    path = make_pdf([["Hello"]], tmp_path / "info.pdf", info={"doi": OWN})
    assert doi.from_xmp(path) == [OWN]


def test_find_doi_verifies_against_crossref_title(paper):
    fetch = Crossref({OWN: TITLE})
    result = doi.find_doi(TITLE, pdf=paper, fetch=fetch)
    assert result == doi.DoiResult(OWN, "front_pages", True)
    assert result is not None and result.url == f"https://doi.org/{OWN}"
    assert f"{doi.CROSSREF}/{CITED}" not in fetch.requested


def test_candidate_resolving_to_another_title_is_discarded(paper):
    fetch = Crossref({OWN: "A Completely Different Paper About Something Else Entirely"})
    assert doi.find_doi(TITLE, pdf=paper, fetch=fetch) is None


def test_zotero_doi_is_tried_first(paper):
    fetch = Crossref({OWN: TITLE, "10.9999/zot": TITLE})
    result = doi.find_doi(TITLE, pdf=paper, zotero_doi="https://doi.org/10.9999/zot", fetch=fetch)
    assert result and result.source == "zotero" and result.doi == "10.9999/zot"


def test_doi_in_the_url_and_on_the_landing_page():
    fetch = Crossref(
        {OWN: TITLE},
        pages={"https://journal.example.org/article/1": f'<html><meta name="citation_doi" content="{OWN}"></html>'},
    )
    by_url = doi.find_doi(TITLE, source_url=f"https://doi.org/{OWN}", fetch=fetch)
    by_page = doi.find_doi(TITLE, source_url="https://journal.example.org/article/1", fetch=fetch)
    assert by_url is not None and by_url.source == "url"
    assert by_page is not None and by_page.source == "landing_page"
    assert doi.from_url("https://example.org/files/report.pdf", fetch=fetch) == []


def test_crossref_search_needs_a_near_exact_title():
    close = {"DOI": OWN, "title": [TITLE]}
    other = {"DOI": CITED, "title": ["Heat pump rates in the Midwest"]}
    assert doi.find_doi(TITLE, fetch=Crossref({}, search=[other, close])) == doi.DoiResult(OWN, "crossref_search", True)
    assert doi.find_doi(TITLE, fetch=Crossref({}, search=[other])) is None


def test_without_a_title_the_candidate_is_returned_unverified(paper):
    result = doi.find_doi(None, pdf=paper, fetch=Crossref({}))
    assert result == doi.DoiResult(OWN, "front_pages", False)


def test_open_access_copy_via_unpaywall(monkeypatch):
    monkeypatch.setenv("SOURCES_CONTACT_EMAIL", "team@example.org")

    def fetch(url, params=None, **_):
        assert url == f"{doi.UNPAYWALL}/{OWN}" and params == {"email": "team@example.org"}
        return SimpleNamespace(
            status_code=200, json=lambda: {"best_oa_location": {"url_for_pdf": "https://oa.example.org/p.pdf"}}
        )

    assert doi.open_access_pdf(OWN, fetch) == "https://oa.example.org/p.pdf"
    monkeypatch.delenv("SOURCES_CONTACT_EMAIL")
    monkeypatch.setattr(doi.env, "load_env", lambda: None)
    assert doi.open_access_pdf(OWN, fetch) is None


def test_open_access_falls_back_to_other_locations(monkeypatch):
    monkeypatch.setenv("SOURCES_CONTACT_EMAIL", "team@example.org")
    body = {
        "best_oa_location": {"url_for_pdf": None, "version": "publishedVersion"},
        "oa_locations": [
            {"url_for_pdf": None, "version": "publishedVersion"},
            {"url_for_pdf": "https://repo.example.org/preprint.pdf", "version": "submittedVersion"},
            {"url_for_pdf": "https://repo.example.org/published.pdf", "version": "publishedVersion"},
        ],
    }
    fetch = lambda url, params=None, **_: SimpleNamespace(status_code=200, json=lambda: body)  # noqa: E731
    assert doi.open_access_pdf(OWN, fetch) == "https://repo.example.org/published.pdf"
    body["oa_locations"] = body["oa_locations"][:1]
    assert doi.open_access_pdf(OWN, fetch) is None
