"""Tests for interrogatory-response Word output (``just interrogatories``).

Fast unit tests cover the frontmatter fields, the structure of the file, and
the check that every question line appears in the source extract. The
integration test runs the real pipeline (Quarto + Pandoc + the Lua filter) on a
two-response file and inspects the ``.docx`` XML. It is skipped when Quarto is
not installed.
"""

from __future__ import annotations

import re
import shutil
import xml.dom.minidom
import zipfile
from datetime import date
from pathlib import Path

import pytest
import yaml

from lib.just import interrogatory as ir

BLOCK = """\
interrogatory_responses:
  docket: PURA Docket No. 26-05-10
  responding_party: Conservation Law Foundation and Sierra Club
  requesting_party: Connecticut Industrial Energy Consumers
  set: Set CIEC-02
  date_issued: 2026-10-29
  date_filed: 2026-11-12
  witness: Juan-Pablo Velez
  file_prefix: CT 26-05-10
  expected_responses: 2
"""

BODY = """
## CIEC-1

::: {.question}
Please refer to Velez Direct Testimony at page 6.

a. Please provide the estimate.
b. Please explain _why_ not.
:::

::: {.response}
The estimate is in Exhibit JPV-3.[^1]

[^1]: A footnote.

b. Because it was not prepared.
:::

## CIEC-2 {witness="Someone Else"}

::: {.question}
Please confirm that Rate HP is not revenue neutral.
:::

::: {.response}
:::
"""

EXTRACT = """
**CIEC-1.** Please refer to Velez Direct Testimony at page 6.

- a. Please provide the estimate.
- b. Please explain _why_ not.

[PDF p. 4 | printed p. 4]

**CIEC-2.** Please confirm that Rate HP is not
revenue neutral.
"""


def _qmd(block: str = BLOCK, body: str = BODY) -> str:
    return f"---\ntitle: ignored\n{block}---\n{body}"


def _meta(text: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match
    return yaml.safe_load(match.group(1))


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------


def test_valid_block_parses() -> None:
    f = ir.parse_fields(_meta(_qmd()))
    assert f.set_label == "Set CIEC-02"
    assert f.date_issued == date(2026, 10, 29)
    assert f.draft is True  # default
    assert f.expected_responses == 2
    assert ir.split_file_name(f, "CIEC-7") == "CT 26-05-10_CIEC-7 Response.docx"


def test_missing_block_lists_required_fields() -> None:
    with pytest.raises(ir.InterrogatoryError) as exc:
        ir.parse_fields({"title": "x"})
    text = "\n".join(exc.value.problems)
    assert "no `interrogatory_responses:` block" in text
    for name in ir.REQUIRED_FIELDS:
        assert name in text


def test_problems_are_reported_together() -> None:
    block = BLOCK.replace("set: Set CIEC-02", 'set: "[Set XXXX-01]"').replace(
        "date_filed: 2026-11-12", "date_filed: soon"
    )
    block = block.replace("witness: Juan-Pablo Velez", "wittness: Juan-Pablo Velez")
    with pytest.raises(ir.InterrogatoryError) as exc:
        ir.parse_fields(_meta(_qmd(block)))
    text = "\n".join(exc.value.problems)
    assert "Unknown field `interrogatory_responses.wittness`" in text
    assert "Missing `interrogatory_responses.witness`" in text
    assert "`interrogatory_responses.set` is still a placeholder" in text
    assert "`interrogatory_responses.date_filed` is `soon`" in text


# ---------------------------------------------------------------------------
# Structure
# ---------------------------------------------------------------------------


def test_body_splits_into_responses() -> None:
    responses, problems = ir.parse_body(_qmd())
    assert problems == []
    assert [r.label for r in responses] == ["CIEC-1", "CIEC-2"]
    assert responses[1].witness == "Someone Else"
    assert responses[0].answered and not responses[1].answered
    assert "a. Please provide the estimate." in responses[0].question


def test_structure_problems() -> None:
    body = "\nStray text.\n\n## CIEC-1\n\n::: {.question}\nQ\n:::\n\n## CIEC-1\n\n::: {.response}\n:::\n"
    _, problems = ir.parse_body(_qmd(body=body))
    text = "\n".join(problems)
    assert "Text outside a question/response block" in text
    assert "CIEC-1: this response label appears twice." in text
    assert "no `response` block" in text
    assert "no question text" in text


# ---------------------------------------------------------------------------
# Questions versus the extract
# ---------------------------------------------------------------------------


def test_questions_match_extract_despite_markdown_and_page_breaks() -> None:
    responses, _ = ir.parse_body(_qmd())
    assert ir.verify_questions(responses, EXTRACT) == []


def test_reworded_question_is_reported_with_the_point_of_divergence() -> None:
    body = BODY.replace("Please provide the estimate.", "Please give the estimate.")
    responses, _ = ir.parse_body(_qmd(body=body))
    problems = ir.verify_questions(responses, EXTRACT)
    assert len(problems) == 1
    assert "CIEC-1" in problems[0] and "give the estimate" in problems[0] and "provide the estimate" in problems[0]


def test_question_parts_as_divs_still_match_extract() -> None:
    # Question parts are wrapped in part divs; the fence lines are markup, not request text.
    body = BODY.replace(
        "a. Please provide the estimate.\nb. Please explain _why_ not.",
        ':::: {.part label="a."}\nPlease provide the estimate.\n::::\n\n'
        ':::: {.part label="b."}\nPlease explain _why_ not.\n::::',
    )
    responses, problems = ir.parse_body(_qmd(body=body))
    assert problems == []
    assert ir.verify_questions(responses, EXTRACT) == []


# ---------------------------------------------------------------------------
# Citations in the responses
# ---------------------------------------------------------------------------


def _response(text: str) -> str:
    return _qmd(body=f"\n## CIEC-1\n\n::: {{.question}}\nQ\n:::\n\n::: {{.response}}\n{text}\n:::\n")


def test_well_formed_citations_pass() -> None:
    assert ir.check_citations(_qmd()) == []
    text = (
        "a. Rate HP is calibrated on average.[^a]\n\n"
        "   [^a]: [Velez Direct](https://pub.switch.box/x) at 85:2\u20137 [@velez_Docket260510Direct_2026].\n\n"
        "   - The Company computed none.[^b] **[TK: confirm (PDF p. 12)]**\n\n"
        "     [^b]: CL&P Response to CLF-SC-026, at 1 **[NOT INGESTED: inbox `x.pdf`, p. 3]**.\n\n"
        "> **[DISCUSSION FOR JPV]** See Velez Direct at 85:14\u201319 and `madpu_Docket2508Order_2026`, p. 21.\n\n"
        "```{python}\n# Exhibit CLP-MCOS-1 (Velez Direct p. 14 n. 8).\nx = 1\n```\n"
    )
    assert ir.check_citations(_response(text)) == []


@pytest.mark.parametrize(
    "line",
    [
        "a. Rate HP is calibrated on average (Velez Direct at 85:2\u20137).",
        "a. The Company computed none (CL&P Response to CLF-SC-026 at 1).",
        "a. The discount is anchored to marginal cost (id. at 28:5\u20136).",
        "a. It covers new load (Exhibit CLP-RATES-1 at 24:19\u201325:1).",
    ],
)
def test_inline_citation_is_reported(line: str) -> None:
    problems = ir.check_citations(_response(line))
    assert len(problems) == 1 and "move it to a footnote" in problems[0]


def test_citation_key_and_page_abbreviation_are_reported_in_footnotes_too() -> None:
    text = "a. The DPU directed it.[^a]\n\n   [^a]: `madpu_Docket2508Order_2026`, p. 21.\n"
    problems = ir.check_citations(_response(text))
    assert any("citation key used as a citation" in p for p in problems)
    assert any("never p., pp. or PDF p." in p for p in problems)


def test_citation_check_keeps_reading_after_a_nested_part() -> None:
    # A response's parts are nested divs. Closing the first part must not end the
    # response for the citation check, or everything after it goes unchecked.
    text = (
        "::: {.response}\n\n"
        ':::: {.part label="a."}\nFirst part, cleanly written.\n::::\n\n'
        ':::: {.part label="b."}\nSecond part cites Velez Direct at 14:5 inline.\n::::\n'
        ":::\n"
    )
    problems = ir.check_citations(_qmd(body=f"\n## CIEC-1\n\n{text}"))
    assert any("move it to a footnote" in p and "CIEC-1" in p for p in problems)


def test_footnote_problems_are_reported() -> None:
    text = (
        "a. First.[^a] Again.[^a] Missing.[^c]\n\n"
        "   [^a]: Note.\n"
        "   A paragraph that Pandoc would fold into the note.\n\n"
        "   [^b]: Unused.\n"
    )
    problems = "\n".join(ir.check_citations(_response(text)))
    assert "add a blank line after footnote [^a]" in problems
    assert "[^a] is referenced 2 times" in problems
    assert "[^c] is used but never defined" in problems
    assert "[^b] is defined but never used" in problems


def test_check_file_uses_source_extract(tmp_path: Path) -> None:
    extract = tmp_path / "extract.md"
    extract.write_text(EXTRACT, encoding="utf-8")
    block = BLOCK + f"  source_extract: {extract}\n"
    qmd = tmp_path / "r.qmd"
    qmd.write_text(_qmd(block), encoding="utf-8")
    report = ir.check_file(qmd)
    assert report.errors == []
    assert any("1 of 2 responses are not written yet" in n for n in report.notes)

    qmd.write_text(_qmd(block, BODY.replace("revenue neutral", "revenue-neutral")), encoding="utf-8")
    assert any("CIEC-2" in e for e in ir.check_file(qmd).errors)

    qmd.write_text(_qmd(BLOCK.replace("expected_responses: 2", "expected_responses: 19")), encoding="utf-8")
    assert any("19 responses but the file has 2" in e for e in ir.check_file(qmd).errors)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------


def test_header_has_label_and_section_page_count() -> None:
    f = ir.parse_fields(_meta(_qmd()))
    xml_text = ir.header_xml(f, "CIEC-7")
    xml.dom.minidom.parseString(xml_text)  # well-formed
    plain = re.sub(r"<[^>]+>", "|", xml_text)
    assert "DRAFT" not in plain  # the DRAFT mark is a watermark shape, not header text
    assert 'string="DRAFT"' in xml_text
    assert "rotation:315" in xml_text and "mso-position-horizontal-relative:margin" in xml_text
    for expected in (
        "Conservation Law Foundation and Sierra Club",
        "PURA Docket No. 26-05-10",
        "CIEC-7",
    ):
        assert expected in plain
    assert "Date Issued" not in plain  # date issued is in the caption block, not the header
    assert "Set CIEC-02" not in plain  # the set label is not printed in the header
    assert " PAGE " in xml_text and " SECTIONPAGES " in xml_text
    final = ir.parse_fields(
        {**_meta(_qmd()), "interrogatory_responses": {**_meta(_qmd())["interrogatory_responses"], "draft": False}}
    )
    assert "DRAFT" not in ir.header_xml(final, "CIEC-7")


# ---------------------------------------------------------------------------
# Real render
# ---------------------------------------------------------------------------

needs_quarto = pytest.mark.skipif(shutil.which("quarto") is None, reason="Quarto is not installed")


def _document(path: Path) -> tuple[str, dict[str, str]]:
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name.endswith((".xml", ".rels")):
                xml.dom.minidom.parseString(z.read(name))
        headers = {n: z.read(n).decode() for n in z.namelist() if n.startswith("word/headerIR")}
        return z.read("word/document.xml").decode(), headers


@needs_quarto
def test_render_combined_and_split(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    qmd = tmp_path / "responses.qmd"
    qmd.write_text(_qmd(), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    combined = ir.render(qmd)[0]
    document, headers = _document(combined)
    assert len(re.findall(r"<w:sectPr\b", document)) == 2  # one section per response
    assert 'r:id="rIdIRHeader1"' in document and 'r:id="rIdIRHeader2"' in document
    assert "CIEC-1" in re.sub(r"<[^>]+>", "", headers["word/headerIR1.xml"])
    assert "CIEC-2" in re.sub(r"<[^>]+>", "", headers["word/headerIR2.xml"])
    text = re.sub(r"<[^>]+>", " ", document)
    assert "Someone Else" in text and "Juan-Pablo Velez" in text
    assert "Date Issued:" in text and "October 29, 2026" in text
    assert "Date Filed:" in text and "November 12, 2026" in text
    assert "Question CIEC-1:" in text and "Question CIEC-2:" in text

    files = ir.render(qmd, split=True)
    assert [p.name for p in files] == ["CT 26-05-10_CIEC-1 Response.docx", "CT 26-05-10_CIEC-2 Response.docx"]
    for path, label in zip(files, ("CIEC-1", "CIEC-2"), strict=True):
        document, headers = _document(path)
        assert len(re.findall(r"<w:sectPr\b", document)) == 1
        assert label in re.sub(r"<[^>]+>", "", headers["word/headerIR1.xml"])
        assert "rIdIRHeader1" in document
    only_second = re.sub(r"<[^>]+>", " ", _document(files[1])[0])
    assert "Someone Else" in only_second and "Exhibit JPV-3" not in only_second


def test_select_responses_matches_labels_case_insensitively() -> None:
    responses, _ = ir.parse_body(_qmd())
    assert [r.label for r in ir.select_responses(responses, ["ciec-2"])] == ["CIEC-2"]
    with pytest.raises(ir.InterrogatoryError) as exc:
        ir.select_responses(responses, ["CIEC-9"])
    assert "CIEC-9" in "\n".join(exc.value.problems) and "CIEC-1, CIEC-2" in "\n".join(exc.value.problems)


def test_open_markers_only_look_at_the_given_responses() -> None:
    body = (
        "\n## CIEC-1\n\n::: {.question}\nQ\n:::\n\n::: {.response}\nDone.\n\n"
        '```{python}\ndef est(key):\n    return "[EST]"\n```\n:::\n'
        "\n## CIEC-2\n\n::: {.question}\nQ\n:::\n\n::: {.response}\nNeeds work **[TK: check]** and `{python} est('x')`.\n:::\n"
    )
    first, second = ir.parse_body(_qmd(body=body))[0]
    assert ir.open_markers([first]) == []
    found = ir.open_markers([second])
    assert any("[TK: check]" in item for item in found) and any("est()" in item for item in found)


@needs_quarto
def test_render_only_and_final(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    qmd = tmp_path / "responses.qmd"
    qmd.write_text(_qmd(), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    files = ir.render(qmd, only=["CIEC-1"], final=True)
    assert [p.name for p in files] == ["CT 26-05-10_CIEC-1 Response.docx"]
    _, headers = _document(files[0])
    assert "PowerPlusWaterMarkObject" not in headers["word/headerIR1.xml"]  # --final drops the watermark
    drafted = ir.render(qmd, only=["CIEC-1"])
    assert "PowerPlusWaterMarkObject" in _document(drafted[0])[1]["word/headerIR1.xml"]
