"""Tests for the expert-testimony Word output (``just testimony``).

Two layers:

* Fast unit tests for the ``testimony:`` frontmatter fields (validation,
  header text, scaffold).
* Integration tests that run the real pipeline (Quarto + Pandoc + the Lua
  filter) on a small testimony and inspect the resulting ``.docx`` XML:
  fonts, spacing, headings, line numbering, header/footer, cover page.
  They are skipped when Quarto is not installed.
"""

from __future__ import annotations

import os
import re
import shutil
import xml.etree.ElementTree as ET
import zipfile
from datetime import date
from pathlib import Path

import pytest
import yaml

from lib.just import draft as draft_module
from lib.just import testimony as tm
from lib.just.templates import build_expert_testimony as builder

VALID_BLOCK = """\
testimony:
  commission: Maryland Public Service Commission
  commission_short: Maryland PSC
  case_number: "Case No. 9888"
  caption:
    - IN THE MATTER OF THE APPLICATION OF
    - BALTIMORE GAS & ELECTRIC COMPANY
    - FOR ADJUSTMENTS TO ITS ELECTRIC BASE RATES
  type: surrebuttal
  and_exhibits: true
  witness: Juan-Pablo Velez
  witness_title: Executive Director, Switchbox
  on_behalf_of: Chesapeake Climate Action Network
  date: 2026-11-02
"""

BODY = """
## I. Introduction

**Q.** Please state your name, business address, and occupation.

**A.** My name is Juan-Pablo Velez.[^1]

A second paragraph of the same answer.

<br>

**Q.** How is your testimony organized?

**A.** Sections:

- **Section I** introduces my qualifications.
- **Section II** summarizes findings.

### A. A subheading

#### 1) A sub-subheading

| Col A | Col B |
|-------|-------|
| 1     | 2     |

## II. Summary and Recommendations

**Q.** Summary?

**A.** Yes.

[^1]: A footnote.
"""


def _qmd(block: str = VALID_BLOCK, body: str = BODY) -> str:
    return f"---\ntitle: ignored\n{block}---\n{body}"


def _meta(text: str) -> dict:
    """Parse a .qmd string's frontmatter the same way the tool does."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match
    return yaml.safe_load(match.group(1))


# ---------------------------------------------------------------------------
# Frontmatter fields
# ---------------------------------------------------------------------------


def test_valid_block_parses_and_derives_header_and_date() -> None:
    t = tm.parse(_meta(_qmd()))
    assert t.type == "Surrebuttal"  # case-insensitive input is normalized
    assert t.and_exhibits is True
    assert t.date == date(2026, 11, 2)
    assert t.date_long == "November 2, 2026"  # no zero-padded day
    assert t.header_lines == (
        "Surrebuttal Testimony of Juan-Pablo Velez",
        "Chesapeake Climate Action Network",
        "Maryland PSC Case No. 9888",
    )


def test_missing_block_lists_every_required_field() -> None:
    with pytest.raises(tm.TestimonyError) as exc:
        tm.parse({"title": "x"})
    text = "\n".join(exc.value.problems)
    assert "no `testimony:` block" in text
    for name in tm.REQUIRED_FIELDS:
        assert name in text
    assert "just new-testimony" in text


def test_all_problems_are_reported_at_once() -> None:
    block = VALID_BLOCK.replace('case_number: "Case No. 9888"', 'case_no: "Case No. 9888"')
    block = block.replace("type: surrebuttal", "type: bogus").replace("date: 2026-11-02", "date: someday")
    with pytest.raises(tm.TestimonyError) as exc:
        tm.parse(_meta(_qmd(block)))
    text = "\n".join(exc.value.problems)
    assert "Unknown field `testimony.case_no`. Did you mean `case_number`?" in text
    assert "Missing `testimony.case_number`" in text
    assert "`testimony.type` is `bogus`" in text
    assert "`testimony.date` is `someday`" in text


def test_placeholders_are_rejected() -> None:
    block = VALID_BLOCK.replace("witness: Juan-Pablo Velez", 'witness: "[WITNESS NAME]"')
    block = block.replace("    - BALTIMORE GAS & ELECTRIC COMPANY", '    - "[APPLICANT NAME]"')
    with pytest.raises(tm.TestimonyError) as exc:
        tm.parse(_meta(_qmd(block)))
    text = "\n".join(exc.value.problems)
    assert "`testimony.witness` is still a placeholder" in text
    assert "`testimony.caption` still has placeholder lines" in text


def test_empty_and_wrong_shape_fields() -> None:
    block = VALID_BLOCK.replace("witness: Juan-Pablo Velez", "witness:").replace(
        "and_exhibits: true", "and_exhibits: maybe"
    )
    with pytest.raises(tm.TestimonyError) as exc:
        tm.parse(_meta(_qmd(block)))
    text = "\n".join(exc.value.problems)
    assert "Missing `testimony.witness`" in text
    assert "`testimony.and_exhibits` must be true or false" in text


def test_optional_fields_may_be_omitted() -> None:
    block = VALID_BLOCK.replace("  witness_title: Executive Director, Switchbox\n", "").replace(
        "  and_exhibits: true\n", ""
    )
    t = tm.parse(_meta(_qmd(block)))
    assert t.witness_title is None
    assert t.and_exhibits is False


def test_scaffold_is_complete_but_refuses_to_render(tmp_path: Path) -> None:
    path = tm.write_scaffold(tmp_path / "new" / "expert_testimony.qmd")
    meta = tm.read_frontmatter(path)
    # Every field is present in the scaffold ...
    for name in tm.REQUIRED_FIELDS:
        assert name in meta["testimony"]
    # ... but each is still a placeholder, so rendering stops.
    with pytest.raises(tm.TestimonyError) as exc:
        tm.parse(meta)
    assert len(exc.value.problems) >= len(tm.REQUIRED_FIELDS) - 1
    with pytest.raises(FileExistsError):
        tm.write_scaffold(path)


# ---------------------------------------------------------------------------
# Model file and header substitution
# ---------------------------------------------------------------------------


def test_header_fill_escapes_xml() -> None:
    header = builder.HEADER_XML
    filled = draft_module._fill_header(header, ("A & B", "<party>", "Case 1"))
    assert "A &amp; B" in filled and "&lt;party&gt;" in filled
    # Idempotent over the baked-in defaults too.
    default = header
    for i, d in enumerate(builder.DEFAULT_HEADER_LINES, start=1):
        default = default.replace(f"{{{{HEADER_LINE_{i}}}}}", d)
    assert "A &amp; B" in draft_module._fill_header(default, ("A & B", "P", "C"))


@pytest.mark.skipif(
    not (shutil.which("pandoc") or shutil.which("quarto")), reason="needs Pandoc (or Quarto) to rebuild"
)
def test_committed_template_matches_builder(tmp_path: Path) -> None:
    """Editing the builder without rebuilding the committed .docx fails here."""
    rebuilt = builder.build(tmp_path / "rebuilt.docx")
    parts = [
        "word/styles.xml",
        "word/document.xml",
        "word/header1.xml",
        "word/header2.xml",
        "word/footer1.xml",
        "word/footer2.xml",
    ]
    with zipfile.ZipFile(builder.OUTPUT) as committed, zipfile.ZipFile(rebuilt) as fresh:
        for part in parts:
            assert committed.read(part) == fresh.read(part), (
                f"{part} is stale; run: uv run python -m lib.just.templates.build_expert_testimony"
            )


# ---------------------------------------------------------------------------
# End to end: render and inspect the Word file
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def rendered(tmp_path_factory: pytest.TempPathFactory) -> zipfile.ZipFile:
    if not shutil.which("quarto"):
        pytest.skip("Quarto is not installed")
    work = tmp_path_factory.mktemp("testimony")
    (work / "t.qmd").write_text(_qmd(), encoding="utf-8")
    cwd = Path.cwd()
    os.chdir(work)
    try:
        draft_module.draft(Path("t.qmd"), testimony=True)
    finally:
        os.chdir(cwd)
    out = next(work.glob("t_*.docx"))
    return zipfile.ZipFile(out)


def _doc(z: zipfile.ZipFile) -> str:
    return z.read("word/document.xml").decode("utf-8")


def _paragraphs(z: zipfile.ZipFile) -> list[tuple[str, str, str]]:
    """(style, plain text with tabs as \\t, raw xml) per paragraph in the body."""
    body = _doc(z)
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", body, re.S):
        style = (re.findall(r'<w:pStyle w:val="([^"]+)"', p) or [""])[0]
        text = re.sub(r"<[^>]+>", "", p.replace("<w:tab/>", "\t"))
        out.append((style, text, p))
    return out


W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _style(z: zipfile.ZipFile, style_id: str) -> ET.Element:
    """One <w:style>, parsed (Pandoc re-serializes styles.xml, so don't match on strings)."""
    root = ET.fromstring(z.read("word/styles.xml"))
    for el in root.iter(f"{W}style"):
        if el.get(f"{W}styleId") == style_id:
            return el
    raise AssertionError(f"style {style_id} missing")


def _has(el: ET.Element, tag: str) -> bool:
    """Does the element contain ``<w:tag>`` that is switched on (not val=0/false)?"""
    return any(found.get(f"{W}val") not in {"0", "false", "none"} for found in el.iter(f"{W}{tag}"))


def _attr(el: ET.Element, tag: str, name: str) -> str | None:
    found = el.find(f".//{W}{tag}")
    return None if found is None else found.get(f"{W}{name}")


def test_cover_page_is_generated_from_the_fields(rendered: zipfile.ZipFile) -> None:
    texts = [t for _s, t, _x in _paragraphs(rendered)]
    joined = "\n".join(texts)
    assert "BEFORE THE" in joined
    assert "MARYLAND PUBLIC SERVICE COMMISSION" in joined
    assert "BALTIMORE GAS &amp; ELECTRIC COMPANY" in joined or "BALTIMORE GAS & ELECTRIC COMPANY" in joined
    assert "Case No. 9888" in joined
    assert "SURREBUTTAL TESTIMONY AND EXHIBITS OF" in joined
    assert "CHESAPEAKE CLIMATE ACTION NETWORK" in joined
    assert "November 2, 2026" in joined
    # the caption has one ")" per caption line
    assert joined.count(")") >= 3


def test_cover_and_body_are_separate_sections(rendered: zipfile.ZipFile) -> None:
    sections = re.findall(r"<w:sectPr.*?</w:sectPr>", _doc(rendered), re.S)
    assert len(sections) == 2
    cover, body = sections
    assert "rIdTestimonyHeaderBlank" in cover and "rIdTestimonyFooterBlank" in cover
    assert "lnNumType" not in cover  # no line numbers on the cover
    # Body: line numbers restart on every page, 0.25" from the text; page 1 is the first body page.
    assert re.search(r'<w:lnNumType[^>]*w:restart="newPage"', body)
    assert re.search(r'<w:lnNumType[^>]*w:distance="360"', body)
    assert re.search(r'<w:pgNumType[^>]*w:start="1"', body)
    assert 'w:left="1440"' in body and 'w:right="1440"' in body and 'w:top="1440"' in body and 'w:bottom="1440"' in body


def test_running_header_and_footer(rendered: zipfile.ZipFile) -> None:
    header = re.sub(r"<[^>]+>", "|", rendered.read("word/header1.xml").decode())
    lines = [x for x in header.split("|") if x.strip()]
    assert lines == [
        "Surrebuttal Testimony of Juan-Pablo Velez",
        "Chesapeake Climate Action Network",
        "Maryland PSC Case No. 9888",
    ]
    assert _attr(_style(rendered, "Header"), "jc", "val") == "right"
    footer = rendered.read("word/footer1.xml").decode()
    assert "PAGE" in footer  # live page number
    assert _attr(_style(rendered, "Footer"), "jc", "val") == "center"
    # The cover shows neither.
    assert "PAGE" not in rendered.read("word/footer2.xml").decode()
    assert "<w:t" not in rendered.read("word/header2.xml").decode()


def test_headings_underline_the_words_not_the_numeral(rendered: zipfile.ZipFile) -> None:
    headings = [(s, t, x) for s, t, x in _paragraphs(rendered) if s == "Heading1"]
    assert [t for _s, t, _x in headings] == ["\tI.\tIntroduction", "\tII.\tSummary and Recommendations"]
    for _s, _t, xml in headings:
        runs = re.findall(r"<w:r>.*?</w:r>|<w:r [^>]*>.*?</w:r>", xml, re.S)
        underlined = [re.sub(r"<[^>]+>", "", r) for r in runs if "<w:u " in r]
        assert underlined and not any(re.fullmatch(r"[IVX]+\.", u.strip()) for u in underlined)
        assert not any(u.strip() in {"", "I.", "II."} for u in underlined)
    # The style itself carries no underline (otherwise Word would underline the numeral).
    assert not _has(_style(rendered, "Heading1"), "u")
    assert _has(_style(rendered, "Heading1"), "b")
    # Deeper levels: italic, typed label then a tab.
    by_style = {s: t for s, t, _x in _paragraphs(rendered)}
    assert by_style["Heading2"] == "A.\tA subheading"
    assert by_style["Heading3"] == "1)\tA sub-subheading"
    assert _has(_style(rendered, "Heading2"), "i")


def test_question_answer_format(rendered: zipfile.ZipFile) -> None:
    paras = _paragraphs(rendered)
    styles = [s for s, _t, _x in paras]
    assert styles.count("Question") == 3
    q = next(t for s, t, _x in paras if s == "Question")
    assert q == "Q.\tPlease state your name, business address, and occupation."  # not upper-cased
    # The second paragraph of an answer is a continuation, and the <br> separator is gone.
    assert "AnswerContinuation" in styles
    assert not any(s == "AnswerContinuation" and not t.strip() for s, t, _x in paras)
    # Q bold, A regular; both hang at 0.5" with a tab stop.
    question, answer = _style(rendered, "Question"), _style(rendered, "Answer")
    assert _has(question, "b") and not _has(answer, "b")
    for el in (question, answer):
        assert (_attr(el, "ind", "left"), _attr(el, "ind", "hanging")) == ("720", "720")
        assert (_attr(el, "tab", "val"), _attr(el, "tab", "pos")) == ("left", "720")
    # Follow-on paragraphs: 0.5" with no first-line indent.
    cont = _style(rendered, "AnswerContinuation")
    assert _attr(cont, "ind", "left") == "720"
    assert _attr(cont, "ind", "firstLine") is None and _attr(cont, "ind", "hanging") is None


def test_fonts_spacing_and_alignment(rendered: zipfile.ZipFile) -> None:
    root = ET.fromstring(rendered.read("word/styles.xml"))
    defaults = root.find(f"{W}docDefaults")
    assert defaults is not None
    assert _attr(defaults, "rFonts", "ascii") == "Times New Roman" and _attr(defaults, "sz", "val") == "24"
    # Double-spaced body text, a 9 pt gap after every paragraph, left-aligned (not justified).
    for sid in ("BodyText", "Question", "Answer", "AnswerContinuation"):
        el = _style(rendered, sid)
        spacing = (_attr(el, "spacing", "line"), _attr(el, "spacing", "after"), _attr(el, "spacing", "before"))
        assert spacing == ("480", "180", "0"), sid
        assert _attr(el, "jc", "val") == "left", sid
    assert not any(el.get(f"{W}val") == "both" for el in root.iter(f"{W}jc"))  # nothing is justified
    # Section headings: 9 pt above and below.
    h1 = _style(rendered, "Heading1")
    assert (_attr(h1, "spacing", "before"), _attr(h1, "spacing", "after")) == ("180", "180")
    # Captions: italic, single-spaced, indented 0.5"; footnotes 11 pt, no line numbers.
    cap = _style(rendered, "Caption")
    assert _has(cap, "i") and _attr(cap, "spacing", "line") == "240" and _attr(cap, "ind", "left") == "720"
    foot = _style(rendered, "FootnoteText")
    assert _attr(foot, "sz", "val") == "22" and foot.find(f".//{W}suppressLineNumbers") is not None


def test_bullets_and_tables(rendered: zipfile.ZipFile) -> None:
    paras = _paragraphs(rendered)
    assert [s for s, t, _x in paras if t.startswith("Section ")] == ["Compact", "Compact"]
    # Bullet at 0.25", text at 0.5".
    numbering = rendered.read("word/numbering.xml").decode()
    first_level_match = re.search(r'<w:lvl w:ilvl="0".*?</w:lvl>', numbering, re.S)
    assert first_level_match
    first_level = first_level_match.group(0)
    assert re.search(r'w:left="720"\s+w:hanging="360"', first_level)
    # Data-table cells are single-spaced "Table Text", not the double-spaced list style.
    tables = re.findall(r"<w:tbl>.*?</w:tbl>", _doc(rendered), re.S)
    assert len(tables) == 2  # the cover caption and the data table
    assert set(re.findall(r'<w:pStyle w:val="([^"]+)"', tables[1])) == {"TableText"}


def test_illinois_only_features_are_gone(rendered: zipfile.ZipFile) -> None:
    text = "\n".join(t for _s, t, _x in _paragraphs(rendered))
    assert "JPV-" not in text
    assert "Table of Contents" not in text
    assert "updateFields" not in rendered.read("word/settings.xml").decode()


def test_missing_fields_stop_the_render_before_quarto_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "t.qmd").write_text("---\ntitle: x\n---\n\n## I. Intro\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as exc:
        draft_module.draft(Path("t.qmd"), testimony=True)
    assert exc.value.code == 2
    assert "no `testimony:` block" in capsys.readouterr().err


def test_render_subcommand_reports_missing_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """`just testimony` runs `testimony render`; a bad path fails cleanly, before Quarto."""
    with pytest.raises(SystemExit) as exc:
        tm.main(["render", str(tmp_path / "nope.qmd")])
    assert exc.value.code == 1
    assert "File not found" in capsys.readouterr().err
