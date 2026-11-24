"""Unit tests for Zotero catalog abstracts."""

from __future__ import annotations

from lib.sources import catalog
from tests.sources.conftest import make_card


def test_format_zotero_abstract():
    block = catalog.format_zotero_abstract("ctx", "cont", "why")
    assert block == "Context: ctx\nContents: cont\nWhy here: why"


def test_merge_keeps_publisher_tail_when_not_switchbox_layout():
    existing = "Publisher summary from a journal."
    block = catalog.format_zotero_abstract("c", "o", "w")
    merged = catalog.merge_with_existing(existing, block)
    assert merged.endswith("Abstract: Publisher summary from a journal.")
    assert merged.startswith("Context: c")


def test_merge_preserves_abstract_tail_on_rerun():
    existing = "Context: old\nContents: old\nWhy here: old\n\nAbstract: pub"
    block = catalog.format_zotero_abstract("new", "new", "new")
    merged = catalog.merge_with_existing(existing, block)
    assert "Context: new" in merged
    assert merged.endswith("Abstract: pub")


def test_build_from_card_uses_front_matter():
    card = make_card(
        front_matter={
            "context": "Commission filing",
            "contents": "Order sections 1-3",
            "why_here": "Approved seasonal rates",
            "docket": "25-55",
        }
    )
    assert catalog.build_from_card(card) == catalog.format_zotero_abstract(
        "Commission filing", "Order sections 1-3", "Approved seasonal rates"
    )


def test_zotero_data_includes_abstract():
    card = make_card(front_matter={"context": "a", "contents": "b", "why_here": "c", "docket": "25-55"})
    assert "abstract" in card.zotero_data()
    assert card.zotero_data()["abstract"].startswith("Context:")
