"""Organization lookup against a fixture references.yaml and conventions table."""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.sources import organizations

REFERENCES = """references:
  - author:
      - family: Massachusetts Department of Public Utilities
    author-short: MA DPU
    id: madpu_Order_2024
    title: Order
    type: document
  - author:
      - family: Massachusetts Department of Public Utilities
    author-short: MA DPU
    id: madpu_Other_2025
    title: Other
    type: document
  - author:
      - family: Mass. DPU
    id: madpu_Variant_2023
    title: Variant
    type: document
  - author:
      - family: Lopez
        given: Ana
    id: lopez_Paper_2024
    title: Paper
    type: article-journal
  - author:
      - literal: Narragansett Electric Company
    author-short: RI Energy
    id: nec_Tariff_2024
    title: Tariff
    type: document
"""

CONVENTIONS = """# Conventions

### Subsidiaries

| legal company | parent | full name | short form | key part |
| --- | --- | --- | --- | --- |
| Massachusetts Electric Company | National Grid | National Grid Massachusetts Electric | MECo | meco |
| NSTAR Electric Company | Eversource | Eversource Massachusetts | | |

### Other
"""


@pytest.fixture
def refs(tmp_path: Path) -> tuple[Path, Path]:
    r, c = tmp_path / "references.yaml", tmp_path / "conventions.md"
    r.write_text(REFERENCES, encoding="utf-8")
    c.write_text(CONVENTIONS, encoding="utf-8")
    return r, c


def test_persons_are_not_organizations(refs):
    names = [n for n, _, _ in organizations.references_organizations(refs[0])]
    assert "Lopez" not in names and "Narragansett Electric Company" in names


def test_exact_match_reuses_full_name_and_short_form(refs):
    matches = organizations.find_organization(
        "Massachusetts Department of Public Utilities", refs[0], conventions=refs[1]
    )
    best = matches[0]
    assert best.full_name == "Massachusetts Department of Public Utilities"
    assert best.short_form == "MA DPU" and best.count == 2 and best.score == 100


def test_short_form_finds_the_organization(refs):
    matches = organizations.find_organization("MA DPU", refs[0], conventions=refs[1])
    assert matches and matches[0].full_name == "Massachusetts Department of Public Utilities"


def test_two_spellings_are_flagged(refs):
    matches = organizations.find_organization("Mass. DPU", refs[0], conventions=refs[1])
    assert {m.full_name for m in matches} >= {"Mass. DPU"}
    text = organizations.describe(organizations.find_organization("Massachusetts DPU", refs[0], conventions=refs[1]))
    assert "Massachusetts Department of Public Utilities" in text


def test_subsidiary_table_is_searched(refs):
    matches = organizations.find_organization("Massachusetts Electric Company", refs[0], conventions=refs[1])
    assert any(
        m.full_name == "National Grid Massachusetts Electric" and m.legal_name == "Massachusetts Electric Company"
        for m in matches
    )


def test_legal_suffixes_and_the_are_ignored():
    assert organizations.normalize("The Narragansett Electric Company, Inc.") == organizations.normalize(
        "Narragansett Electric Company"
    )


def test_no_match_says_new_organization(refs):
    text = organizations.describe(
        organizations.find_organization("Zebra Widgets Collective", refs[0], conventions=refs[1])
    )
    assert "NEW ORGANIZATION" in text


def test_zotero_items_not_yet_in_references_are_searched(refs):
    items = [
        {
            "key": "ABC",
            "data": {
                "itemType": "document",
                "creators": [{"creatorType": "author", "name": "Vermont Public Service Board"}],
                "extra": "Citation Key: vtpsb_X_2024\ntex.shortauthor: VT PSB",
            },
        }
    ]
    matches = organizations.find_organization("Vermont Public Service Board", refs[0], items=items, conventions=refs[1])
    assert matches[0].short_form == "VT PSB" and "zotero" in matches[0].sources
