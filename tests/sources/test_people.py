"""Person lookup against a fixture references.yaml and Zotero items."""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.sources import checks, people

REFERENCES = """references:
  - author:
      - family: Walsh
        given: Michael J.
    id: walsh_Paper_2024
    title: Paper
    type: article-journal
  - author:
      - family: Walsh
        given: Michael
      - family: Pérez-Arriaga
        given: José Ignacio
    id: walsh_Other_2023
    title: Other
    type: article-journal
  - author:
      - family: Walsh
        given: Jane
    id: walsh_Different_2022
    title: Different
    type: report
  - author:
      - family: Massachusetts Department of Public Utilities
    id: madpu_Order_2024
    title: Order
    type: document
"""


@pytest.fixture
def refs(tmp_path: Path) -> Path:
    p = tmp_path / "references.yaml"
    p.write_text(REFERENCES, encoding="utf-8")
    return p


def test_finds_compatible_spellings_but_not_other_people_with_the_family_name(refs):
    matches = people.find_person("Walsh, Michael", references=refs)
    assert [m.display() for m in matches] == ["Walsh, Michael", "Walsh, Michael J."]
    assert matches[0].exact and not matches[1].exact


def test_an_initial_matches_and_given_family_order_works(refs):
    assert [m.display() for m in people.find_person("M. Walsh", references=refs)] == [
        "Walsh, Michael",
        "Walsh, Michael J.",
    ]


def test_accents_and_hyphens_do_not_hide_a_match(refs):
    assert [m.display() for m in people.find_person("Perez Arriaga, Jose", references=refs)] == [
        "Pérez-Arriaga, José Ignacio"
    ]


def test_zotero_items_not_yet_in_references_are_searched(refs):
    items = [
        {
            "key": "Z1",
            "data": {
                "itemType": "report",
                "extra": "",
                "creators": [{"creatorType": "author", "firstName": "M.", "lastName": "Walsh"}],
            },
        }
    ]
    matches = people.find_person("Walsh, Michael", references=refs, items=items)
    assert "Walsh, M." in [m.display() for m in matches]


def test_no_match_says_new_person(refs):
    assert "new person" in people.describe("Lopez, Ana", people.find_person("Lopez, Ana", references=refs))


def test_variants_are_flagged_as_a_warning_and_different_people_are_not():
    def item(first, last):
        return {"itemType": "report", "creators": [{"creatorType": "author", "firstName": first, "lastName": last}]}

    entries = [
        ("walsh_A_2024", item("Michael J.", "Walsh")),
        ("walsh_B_2023", item("Michael", "Walsh")),
        ("walsh_C_2022", item("Jane", "Walsh")),
    ]
    found = [f for f in checks.run_checks(entries) if f.code == "SIMILAR_PERSON_NAMES"]
    assert len(found) == 1
    assert found[0].level == "warning"
    assert "'Walsh, Michael'" in found[0].message and "'Walsh, Michael J.'" in found[0].message
