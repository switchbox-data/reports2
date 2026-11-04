import pytest

from lib.sources import extra


def test_get_is_case_insensitive_and_strips():
    assert extra.get("arXiv: 1\ncitation key:  madpu_X_2024 ", extra.CITATION_KEY) == "madpu_X_2024"
    assert extra.get("", extra.CITATION_KEY) is None
    assert extra.get(None, extra.SHORTAUTHOR) is None


def test_duplicate_line_is_an_error():
    with pytest.raises(extra.ExtraError):
        extra.get("Citation Key: a\nCitation Key: b", extra.CITATION_KEY)


def test_set_replaces_in_place_and_preserves_other_lines():
    text = "Free text first\ntex.shortauthor: DPU\nPage Version ID: 12"
    assert (
        extra.set_field(text, extra.SHORTAUTHOR, "MA DPU")
        == "Free text first\ntex.shortauthor: MA DPU\nPage Version ID: 12"
    )


def test_set_appends_and_removes():
    assert extra.set_field("arXiv: 1", extra.CITATION_KEY, "k_T_2024") == "arXiv: 1\nCitation Key: k_T_2024"
    assert extra.set_field("arXiv: 1\nCitation Key: k", extra.CITATION_KEY, None) == "arXiv: 1"
    assert extra.set_field(None, extra.CITATION_KEY, "k") == "Citation Key: k"


def test_remove_fields():
    note = "Citation Key: k\ntex.shortauthor: NiMo\n_eprint: 2410"
    assert extra.remove_fields(note, (extra.CITATION_KEY, extra.SHORTAUTHOR)) == "_eprint: 2410"
