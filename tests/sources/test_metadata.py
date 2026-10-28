"""The details card enforces the conventions in code."""

from __future__ import annotations

import pytest
import yaml

from lib.sources import citekeys, metadata
from tests.sources.conftest import make_card


def problems(card: metadata.SourceMetadata, taken: set[str] | None = None) -> list[str]:
    return card.problems(taken)


def test_valid_card_has_no_problems():
    assert problems(make_card()) == []


def test_citekey_must_be_the_rules_key():
    card = make_card().model_copy(update={"citekey": "madpu_Wrong_2025"})
    assert any("is not the rule's key" in p for p in problems(card))


def test_collision_suffix_is_accepted_when_free_and_proposed_when_taken():
    base = make_card().citekey
    taken = {base}
    assert any("already used" in p and f"{base}a" in p for p in problems(make_card(), taken))
    suffixed = make_card().model_copy(update={"citekey": f"{base}a"})
    assert problems(suffixed, taken) == []
    assert any("already used" in p for p in problems(suffixed, {base, f"{base}a"}))


def test_key_would_be_read_as_markdown_emphasis():
    card = make_card(creators=[{"name": "Dept. of Public Utilities"}], abbreviation=None)
    card = card.model_copy(update={"citekey": "_oops_"})
    assert any("emphasis" in p for p in problems(card))


def test_abbreviation_needs_an_organization_author():
    card = make_card(creators=[{"first_name": "Ana", "last_name": "Lopez"}])
    assert any("belongs on an organization" in p for p in problems(card))


def test_new_organization_needs_the_short_form_source():
    assert any("abbreviation_source" in p for p in problems(make_card(new_organization=True)))
    assert not any(
        "abbreviation_source" in p for p in problems(make_card(new_organization=True, abbreviation_source="p. 1"))
    )


@pytest.mark.parametrize("short", ["DPU", "psc", "PUC", "DEC", "DPS"])
def test_bare_agency_abbreviations_are_rejected(short):
    assert any("never valid" in p for p in problems(make_card(abbreviation=short)))


def test_all_caps_title_is_rejected():
    assert any("ALL CAPS" in p for p in problems(make_card(title="DOCKET 25-55: ORDER ON SEASONAL HEAT PUMP RATES")))


def test_docket_titles_follow_the_rule():
    assert any("Docket 25-55:" in p for p in problems(make_card(title="Order on Seasonal Heat Pump Rates")))


def test_publisher_must_not_repeat_the_author():
    assert any("repeats the author" in p for p in problems(make_card(publisher="MA DPU")))
    assert not any("repeats the author" in p for p in problems(make_card(publisher="Commonwealth of Massachusetts")))


def test_projects_are_snake_case_and_required():
    assert any("snake_case" in p for p in problems(make_card(projects=["MA HP Rates"])))
    assert any("every source belongs to a project" in p for p in problems(make_card(projects=[])))
    assert not any("belongs to a project" in p for p in problems(make_card(projects=["general_reference"])))


def test_dates_and_dois_are_checked():
    assert any("date" in p for p in problems(make_card(date="June 2025")))
    assert any("doi" in p for p in problems(make_card(doi="https://doi.org/10.1/x")))


def test_workbook_types_and_web_page_url():
    assert any(
        "workbook" in p
        for p in problems(make_card(source_file="m.xlsx", item_type="webpage", source_url="https://x.org"))
    )
    assert any("web page needs source_url" in p for p in problems(make_card(item_type="webpage", source_url=None)))
    assert any(
        "DocumentCloud cannot host workbooks" in p
        for p in problems(make_card(source_file="m.xlsx", item_type="dataset", upload_documentcloud=True))
    )


def test_unknown_fields_are_rejected():
    with pytest.raises(ValueError):
        metadata.SourceMetadata.model_validate({**make_card().model_dump(), "extractpath": "x"})


def test_creator_must_be_an_organization_or_a_person():
    with pytest.raises(ValueError):
        metadata.Creator(name="Org", first_name="A", last_name="B")
    with pytest.raises(ValueError):
        metadata.Creator(first_name="A")


def test_check_raises_with_every_problem():
    with pytest.raises(metadata.MetadataError) as e:
        make_card(projects=[], date="soon").check()
    assert len(e.value.problems) == 2


def test_citation_url_is_the_doi_link_or_the_short_link():
    card = make_card()
    assert card.citation_url == f"https://pub.switch.box/{card.citekey}"
    assert card.short_link_target == card.source_url
    with_doi = make_card(doi="10.1234/abc")
    assert with_doi.citation_url == "https://doi.org/10.1234/abc"
    assert with_doi.short_link_target is None
    assert not with_doi.should_upload_documentcloud
    assert make_card(doi="10.1234/abc", upload_documentcloud=True).should_upload_documentcloud


def test_pdf_host_picks_documentcloud_or_drive(monkeypatch):
    monkeypatch.delenv("SOURCES_PDF_HOST")
    assert metadata.PDF_HOST == "gdrive"
    card = make_card()
    assert card.should_upload_drive and not card.should_upload_documentcloud
    assert not make_card(doi="10.1234/abc").should_upload_drive
    monkeypatch.setenv("SOURCES_PDF_HOST", "documentcloud")
    assert card.should_upload_documentcloud and not card.should_upload_drive
    monkeypatch.setenv("SOURCES_PDF_HOST", "dropbox")
    with pytest.raises(ValueError, match="SOURCES_PDF_HOST"):
        _ = card.should_upload_drive


def test_public_url_prefers_documentcloud_then_drive():
    card = make_card()
    assert card.public_url == card.source_url
    card.drive_url = "https://drive.google.com/file/d/1/view"
    assert card.public_url == card.drive_url
    card.documentcloud_url = "https://www.documentcloud.org/documents/1-x"
    assert card.public_url == card.documentcloud_url


def test_zotero_data_maps_item_type_fields():
    report = make_card(item_type="report", publisher="Commonwealth of Massachusetts")
    data = report.zotero_data(["COL1"])
    assert data["institution"] == "Commonwealth of Massachusetts" and "reportNumber" not in data
    assert "Docket: 25-55" in data["extra"]
    assert data["collections"] == ["COL1"] and "Citation Key: " + report.citekey in data["extra"]
    assert "tex.shortauthor: MA DPU" in data["extra"]
    page = make_card(
        item_type="webpage", container="Example Blog", access_date="2026-10-28", source_url="https://x.org/a"
    )
    d = page.zotero_data()
    assert d["websiteTitle"] == "Example Blog" and d["accessDate"] == "2026-10-28"


def test_card_round_trips_through_yaml(tmp_path):
    card = make_card()
    path = tmp_path / "card.yaml"
    metadata.dump(card, path)
    assert metadata.load(path) == card
    assert "documentcloud_url" not in yaml.safe_load(path.read_text())


def test_key_rule_matches_citekeys_module():
    card = make_card()
    assert card.citekey == citekeys.propose_key(card.zotero_data(), set())
