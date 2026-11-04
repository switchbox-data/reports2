"""Page markers and margin line numbers: read from the PDF, checked in the extract, used to cite quotes."""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.sources import pagelines
from tests.sources.pdfs import make_footnoted_pdf, make_numbered_pdf, make_pdf

PAGE_1 = [
    "Q. Please state your name and business address.",
    "A. My name is Jane Witness, and my business address is 1 Main Street.",
    "Q. What is the purpose of your testimony?",
    "A. To show that the default rate overcharges heat pump customers for",
]
PAGE_2 = [
    "delivery service relative to the costs they cause on the system.",
    "Q. What do you recommend?",
    "A. A lower winter distribution charge for heat pump customers.",
]


@pytest.fixture
def testimony(tmp_path: Path) -> list[pagelines.PdfPage]:
    pdf = make_numbered_pdf([PAGE_1, PAGE_2], tmp_path / "t.pdf", footer=["Page 1 of 2", "Page 2 of 2"])
    return pagelines.read_pdf(pdf)


def _extract(body: str, scheme: str = "page_line") -> str:
    return f"---\nsource_file: t.pdf\ncitation_scheme: {scheme}\n---\n\n# Direct Testimony\n\n{body}"


GOOD = """[PDF p. 1 | printed p. 1]

{1} **Q.** Please state your name and business address.
{2} **A.** My name is Jane Witness, and my business address is 1 Main Street.
{3} **Q.** What is the purpose of your testimony?
{4} **A.** To show that the default rate overcharges heat pump customers for

[PDF p. 2 | printed p. 2]

{1} delivery service relative to the costs they cause on the system.
{2} **Q.** What do you recommend?
{3} **A.** A lower winter distribution charge for heat pump customers.
"""


def test_read_pdf_finds_margin_numbers_and_printed_labels(testimony: list[pagelines.PdfPage]) -> None:
    assert [p.printed_label for p in testimony] == ["1", "2"]
    assert testimony[0].numbered[2].startswith("A. My name is Jane Witness")
    assert sorted(testimony[1].numbered) == [1, 2, 3]
    assert pagelines.has_line_numbers(testimony)


def test_footnote_numbers_are_not_margin_line_numbers(tmp_path: Path) -> None:
    pdf = make_footnoted_pdf(
        ["The Commission accepts the tariffs.", "The pilots are denied as filed."],
        ["Maillog No. 320089.", "Id. at 3.", "PUA 7-1001(d).", "See Order No. 91218 at 2."],
        tmp_path / "order.pdf",
    )
    pages = pagelines.read_pdf(pdf)
    assert not pages[0].numbered
    assert not pagelines.has_line_numbers(pages)


def test_skeleton_is_a_valid_extract(testimony: list[pagelines.PdfPage]) -> None:
    sk = pagelines.skeleton(testimony)
    assert "[PDF p. 2 | printed p. 2]" in sk
    assert "{3} A. A lower winter distribution charge" in sk
    errors, _ = pagelines.check(_extract(sk), testimony)
    assert errors == []


def test_faithful_extract_passes(testimony: list[pagelines.PdfPage]) -> None:
    assert pagelines.check(_extract(GOOD), testimony) == ([], [])


def test_list_items_and_indented_continuations_pass(testimony: list[pagelines.PdfPage]) -> None:
    # dprint indents a list item's continuation lines, so the prefix can be bare whitespace
    body = GOOD.replace("{3} **Q.**", "- {3} **Q.**").replace("{4} **A.**", "  {4} **A.**")
    assert pagelines.check(_extract(body), testimony) == ([], [])


def test_dropped_and_misnumbered_lines_fail(testimony: list[pagelines.PdfPage]) -> None:
    body = GOOD.replace("{2} **Q.** What do you recommend?\n", "").replace("{3} **A.** A lower", "{4} **A.** A lower")
    errors, _ = pagelines.check(_extract(body), testimony)
    assert any("has no line 4" in e for e in errors)
    assert any("numbered line(s) 2-3 missing" in e for e in errors)


def test_text_on_the_wrong_line_fails(testimony: list[pagelines.PdfPage]) -> None:
    body = GOOD.replace("{1} **Q.** Please state", "{1} **Q.** What do you recommend? Please")
    body = body.replace("{3} **Q.** What is the purpose of your testimony?", "{3} **Q.** Something else entirely.")
    errors, _ = pagelines.check(_extract(body), testimony)
    assert any("{3} on PDF p. 1 does not match" in e for e in errors)


def test_missing_and_out_of_order_page_markers_fail(testimony: list[pagelines.PdfPage]) -> None:
    errors, _ = pagelines.check(_extract(GOOD.replace("[PDF p. 2 | printed p. 2]", "")), testimony)
    assert any("no page marker for PDF page(s) 2" in e for e in errors)
    swapped = GOOD.replace("[PDF p. 1 | printed p. 1]", "[PDF p. 2 | printed p. 2]", 1)
    errors, _ = pagelines.check(_extract(swapped), testimony)
    assert any("page markers must increase" in e for e in errors)


def test_scheme_must_match_the_pdf(testimony: list[pagelines.PdfPage]) -> None:
    errors, _ = pagelines.check(_extract(GOOD, scheme="page"), testimony)
    assert any("set citation_scheme: page_line" in e for e in errors)
    errors, _ = pagelines.check(GOOD, testimony)
    assert any("citation_scheme must be one of" in e for e in errors)


def test_unresolved_printed_label_fails(testimony: list[pagelines.PdfPage]) -> None:
    errors, _ = pagelines.check(_extract(GOOD.replace("printed p. 2]", "printed p. ?]")), testimony)
    assert any("unresolved printed page label" in e for e in errors)


def test_not_transcribed_pages_count_as_marked(tmp_path: Path) -> None:
    pages = pagelines.read_pdf(make_pdf([["Cover page text"], ["Exhibit one"], ["Exhibit two"]], tmp_path / "x.pdf"))
    body = "[PDF p. 1]\n\nCover page text\n\n[PDF pp. 2-3 not transcribed: Exhibits 1 and 2, data tables]\n"
    assert pagelines.check(_extract(body, scheme="page"), pages) == ([], [])


def test_cite_spans_lines_and_page_breaks() -> None:
    md = _extract(GOOD)
    assert [str(c) for c in pagelines.cite(md, "my business address is 1 Main Street")] == ["1:2 (PDF p. 1)"]
    assert [str(c) for c in pagelines.cite(md, "Q. What is the purpose of your testimony? A. To show")] == [
        "1:3-4 (PDF p. 1)"
    ]
    assert [str(c) for c in pagelines.cite(md, "overcharges heat pump customers for delivery service")] == [
        "1:4-2:1 (PDF pp. 1-2)"
    ]


def test_cite_footnote_and_inline_page_break() -> None:
    body = (
        "[PDF p. 1 | printed p. 7]\n\nThe rate recovers fixed costs through volumetric charges [PDF p. 2 | printed p. 8] "
        "that rise with usage.[^3]\n\n[^3]: Response to DR 1-4, Attachment 1.\n"
    )
    md = _extract(body, scheme="page")
    assert [str(c) for c in pagelines.cite(md, "fixed costs through volumetric")] == ["p. 7 (PDF p. 1)"]
    assert [str(c) for c in pagelines.cite(md, "volumetric charges that rise")] == ["pp. 7-8 (PDF pp. 1-2)"]
    assert [str(c) for c in pagelines.cite(md, "DR 1-4, Attachment 1")] == ["p. 8 n. 3 (PDF p. 2)"]
    assert [str(c) for c in pagelines.cite(_extract("[PDF p. 4]\n\nNo printed number here.\n", "page"), "printed")] == [
        "PDF p. 4"
    ]


def test_cli_cite_points_an_unmarked_extract_at_the_repair_steps(tmp_path: Path, capsys) -> None:
    from lib.sources import cli

    old = tmp_path / "old.md"
    old.write_text("---\ncitekey: karas_Docket9888Prepared_2026\n---\n\n# Old extract\n\nSome quoted words.\n")
    assert cli.main(["cite", str(old), "quoted words"]) == 2
    err = capsys.readouterr().err
    assert "just fetch-source karas_Docket9888Prepared_2026" in err
    assert "Adding markers to an older extract" in err
