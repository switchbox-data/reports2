"""Tests for inline Velez testimony excerpts in interrogatory questions."""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.just import interrogatory as ir
from lib.just.interrogatory_reftext import (
    insert_referenced_testimony_block,
    parse_velez_references,
    question_lines_for_extract_check,
    ref_caption,
    verify_referenced_testimony,
)

REPO = Path(__file__).resolve().parents[2]
VELEZ = REPO / "context/sources/ct_hp_rates/pura_260510_direct_testimony_clf_velez.md"


def test_ref_caption() -> None:
    assert ref_caption("6:11-23") == "Velez Direct, printed p. 6, lines 11–23"  # noqa: RUF001
    assert ref_caption("83:n75") == "Velez Direct, printed p. 83, footnote 75"


def test_parse_velez_preserves_order_and_footnotes_on_same_page() -> None:
    assert parse_velez_references("page 83, footnote 75, and page 101, lines 5-17") == [
        "83:n75",
        "101:5-17",
    ]
    assert parse_velez_references("page 84, lines 1-12 and footnote 76") == ["84:1-12", "84:n76"]
    assert parse_velez_references("page 8, lines 1-2 and footnote 1, and page 10, lines 4-7") == [
        "8:1-2",
        "8:n1",
        "10:4-7",
    ]
    assert parse_velez_references("page 58, lines 11-19, and footnotes 60 and 61, which describe") == [
        "58:11-19",
        "58:n60",
        "58:n61",
    ]


def test_insert_referenced_testimony_block() -> None:
    question = """Please refer to Velez Direct Testimony at page 27, lines 3-8.

a. Confirm something."""
    out = insert_referenced_testimony_block(question, VELEZ)
    assert "::: {.referenced-testimony}" in out
    assert "**Velez Direct, printed p. 27, lines 3–8**" in out  # noqa: RUF001
    assert "testimony-passage" not in out
    assert "custom-style" not in out
    assert "27:3\u2003\u2003" in out


def test_nested_referenced_testimony_inside_question() -> None:
    body = """
## CIEC-1

::: {.question}
Please refer to Velez Direct Testimony at page 27, lines 3-8.

::: {.referenced-testimony}
27:3\tThe implication is clear:
:::


a. Confirm something.
:::

::: {.response}
Done.
:::
"""
    responses, problems = ir.parse_body(f"---\ntitle: x\n---\n{body}")
    assert problems == []
    assert "27:3\t" in responses[0].question
    assert "Confirm something" in question_lines_for_extract_check(responses[0].question)


@pytest.mark.skipif(not VELEZ.is_file(), reason="Velez extract not in workspace")
def test_verify_referenced_testimony_against_velez() -> None:
    question = """Please refer to Velez Direct Testimony at page 27, lines 3-8.

::: {.referenced-testimony}
27:3\tThe implication is clear:
:::


a. Confirm something."""
    assert verify_referenced_testimony(question, VELEZ, "CIEC-6") == []


def test_numbered_list_markers_and_indent_are_kept() -> None:
    """The recommendations list (6:13-7:12) keeps its numbers and hanging indent, across the page break."""
    out = insert_referenced_testimony_block(
        "Please refer to Velez Direct Testimony at page 6, lines 13-23; page 7, lines 1-8.", VELEZ
    ).replace("\u2007", "")  # figure spaces only pad the line references to a common width
    gap, nb = "\u2003\u2003", "\u00a0"
    # The marker is indented; runon lines of the item are indented further.
    assert f"6:13{gap}{nb * 2}1. Create a new residential rate schedule" in out
    assert f"6:14{gap}{nb * 6}a heat pump for heating." in out
    assert f"6:20{gap}{nb * 2}3. Set a lower Transmission Service Rate" in out
    # The extract drops the list prefix at the page break; the item still continues.
    assert f"7:1{gap}{nb * 6}Transmission Service Rate should be 75% lower" in out
    assert f"7:3{gap}{nb * 2}4. Auto-enroll all electric customers" in out


def test_passage_lines_are_one_single_spaced_paragraph() -> None:
    """Lines inside a passage are joined by hard breaks (a trailing backslash), not blank lines."""
    out = insert_referenced_testimony_block("Please refer to Velez Direct Testimony at page 6, lines 11-14.", VELEZ)
    lines = [ln for ln in out.splitlines() if ln.startswith("6:1")]
    assert [ln.endswith("\\") for ln in lines] == [True, True, True, False]
    assert "" not in out.splitlines()[out.splitlines().index(lines[0]) : out.splitlines().index(lines[-1])]
