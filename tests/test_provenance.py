"""Tests for lib.provenance (testimony provenance documents)."""

from __future__ import annotations

from pathlib import Path

from lib.provenance.align import Occurrence, align_stream
from lib.provenance.config import KnownDifference, Link, ProvenanceConfig
from lib.provenance.extract_check import check_against_extract
from lib.provenance.pdf_index import PdfIndex, PdfToken, classify_page, filed_testimony_pages
from lib.provenance.qmd import QToken, parse_qmd, strip_html_comments
from lib.provenance.resolve import Notebook, find_var_line
from lib.provenance.rows import (
    Row,
    _known_difference,
    _locate_table,
    _rescue_known_difference,
    format_locations,
    quote_for,
)
from lib.provenance.text import split_word
from lib.sources.pagelines import PdfLine, PdfPage


def _cfg(**kw: object) -> ProvenanceConfig:
    base: dict = {
        "tag": "t",
        "path_repo": Path("."),
        "report_rel": "reports/x",
        "path_pdf": Path("x.pdf"),
        "namespaces": {"r": "rep"},
        "notebook_blurbs": {},
        "title": "T",
        "subtitle": "S",
        "intro": "",
        "docx_name": "x.docx",
    }
    base.update(kw)
    return ProvenanceConfig(**base)


def _ptoks(text: str, page: int = 1, line: int = 1) -> list[PdfToken]:
    return [PdfToken(p, page, line, None, s) for w in text.split() for p, s in split_word(w)]


def _qtoks(before: str, value: str, after: str) -> list[QToken]:
    def toks(s: str, eid: int | None = None) -> list[QToken]:
        return [QToken(p, eid) for w in s.split() for p, _ in split_word(w)]

    return toks(before) + toks(value, 0) + toks(after)


def test_strip_html_comments_keeps_line_numbers():
    text = "a\n<!-- one\ntwo\nthree -->\nb\n"
    out = strip_html_comments(text)
    assert out.splitlines()[4] == "b"
    assert "two" not in out


def test_parse_qmd_ignores_commented_embeds_and_reads_table_header():
    qmd = "\n".join(
        [
            "---",
            "title: x",
            "---",
            "<!--",
            "{{< embed notebooks/a.qmd#fig-old >}}",
            "-->",
            "",
            "| Service | Current Charge |",
            "|---|---|",
            "| Distribution | `{python} r.x` |",
            "",
            "{{< embed notebooks/a.qmd#fig-new >}}",
        ]
    )
    doc = parse_qmd(qmd)
    assert [e["label"] for e in doc.embeds] == ["fig-new"]
    assert doc.embeds[0]["qmd_line"] == 12
    assert doc.tables[0]["header"] == ["Service", "Current Charge"]
    assert doc.tables[0]["label"] is None
    assert doc.exprs[0].code == "r.x"


def test_align_exact_and_fallback():
    q = _qtoks("homes from the territory", "4,897", "buildings representing customers")
    exact = align_stream(q, _ptoks("homes from the territory 4,897 buildings representing customers"))
    assert exact[0].confidence == "exact"
    # Reworded text around the number throws alignment off; the value search recovers it.
    q = _qtoks("bills for each of the", "4,897", "BGE-territory buildings under both their baseline")
    p = _ptoks(
        "lots of unrelated words here and there that do not match at all "
        "energy bills for each of the 4,897 BGE-territory buildings, under both their baseline"
    )
    occ = align_stream(q, p)[0]
    assert occ.confidence in ("exact", "anchored", "fallback")
    assert [t.text for t in occ.tokens] == ["4,897"]


def test_format_locations():
    locs = [(5, 17, "line"), (25, 4, "line"), (25, 7, "line"), (41, 3, "footnote"), (12, 0, "page")]
    assert format_locations(locs) == "p. 5, line 17; p. 12; p. 25, lines 4 and 7; p. 41, footnote 3"


def test_quote_stops_at_math_glyphs_and_unbolds_open_paren():
    stream = _ptoks("\U0001d43f\U0001d43f\U0001d458\U0001d458 Multiplying the $57.74/kW-year figure by each hour")
    k = next(i for i, t in enumerate(stream) if t.text.startswith("$57.74"))
    md, plain = quote_for(Occurrence(0, stream[k : k + 1], stream, k, k + 1, "exact"))
    assert plain.startswith("Multiplying the [$57.74]")
    stream = _ptoks("could save $256( nearly 9%) per year.")
    k = next(i for i, t in enumerate(stream) if t.text.startswith("$256"))
    md, _ = quote_for(Occurrence(0, stream[k : k + 1], stream, k, k + 1, "exact"))
    assert "**\\$256**(" in md


def test_find_var_line_literal_and_template():
    nb = Notebook(
        "rep",
        [
            'report_vars["a_total"] = 1',
            "for k in keys:",
            '    report_vars[f"{k}_delta"] = 2',
            "report_vars.update({",
            '    "b_total": 3,',
            "})",
        ],
        [],
    )
    assert find_var_line(nb, "a_total") == 1
    assert find_var_line(nb, "natgas_delta") == 3
    assert find_var_line(nb, "b_total") == 5
    assert find_var_line(nb, "missing") is None


def test_known_difference_matching_and_rescue():
    cfg = _cfg(known_differences=[KnownDifference("$256", "$257", "edited in Word")])
    assert _known_difference(cfg, "$256(", "$257") == "edited in Word"
    assert _known_difference(cfg, "$256", "$300") is None
    stream = _ptoks("could save $256( nearly 9%) per year")
    weak = Occurrence(0, stream[1:4], stream, 1, 4, "low")
    fixed = _rescue_known_difference(cfg, weak, "$257")
    assert fixed is not None and fixed.confidence == "exact"
    assert [t.text for t in fixed.tokens] == ["$256("]


def test_locate_table_with_wrapped_header():
    idx = PdfIndex(
        lines=[
            {"kind": "other", "page": 37, "text": "Service Current Charge Schedule R rate"},
            {"kind": "body", "page": 38, "text": "The following table contains the proposed rates."},
            {"kind": "other", "page": 39, "text": "Schedule R Schedule R-"},
            {"kind": "other", "page": 39, "text": "Service Charge rate HP rate Change"},
        ]
    )
    first = _locate_table(["Service", "Current Charge", "Schedule R rate"], idx, 0)
    assert first == (37, 0)
    second = _locate_table(["Service", "Charge", "Schedule R rate", "Schedule R-HP rate", "Change"], idx, 1)
    assert second is not None and second[0] == 39


def test_notebook_link():
    cfg = _cfg()
    link = cfg.notebook_link("rep", 3, 9)
    assert link == Link(
        "rep.qmd_3-9", "https://github.com/switchbox-data/reports2/blob/t/reports/x/notebooks/rep.qmd#L3-L9", "rep"
    )
    assert cfg.notebook_link("expert_testimony", 1, 2).url.endswith("/reports/x/expert_testimony.qmd#L1-L2")


def test_testimony_pages_stop_where_attachment_numbering_restarts():
    pages = [PdfPage(1, []), PdfPage(2, [], "1"), PdfPage(3, [], "2"), PdfPage(4, [], "1"), PdfPage(5, [], "3")]
    assert [(n, p.index) for n, p in filed_testimony_pages(pages)] == [(1, 2), (2, 3)]


def test_classify_page_wraps_captions_and_footnotes_but_not_table_rows():
    page = PdfPage(
        9,
        [
            PdfLine(76, "the Company proposed Rate 6.12", 1, 72),
            PdfLine(104, "Table 1: Rate 1 vs. Rate 6", None, 72),
            PdfLine(131, "Block 1 Block 2", None, 300),  # table header row, set far right
            PdfLine(200, "Figure 3: Average monthly electricity", None, 72),
            PdfLine(228, "before and after installation.", None, 108),  # double-spaced wrap, hanging indent
            PdfLine(256, "Next body line", 2, 72),
            PdfLine(680, "12 See supra n.10.", None, 72),
            PdfLine(694, "And more of footnote 12.", None, 72),
            PdfLine(726, "8", None, 300),
        ],
        "8",
    )
    lines, next_fn = classify_page(page, 8, 12)
    assert next_fn == 13
    kinds = [(pl["kind"], pl["text"]) for pl in lines]
    assert kinds == [
        ("body", "the Company proposed Rate 6.12"),
        ("caption", "Rate 1 vs. Rate 6"),
        ("other", "Block 1 Block 2"),
        ("caption", "Average monthly electricity before and after installation."),
        ("body", "Next body line"),
        ("footnote", "See supra n.10. And more of footnote 12."),
    ]


def test_extract_cross_check_reads_page_and_line_from_markers(tmp_path: Path):
    extract = tmp_path / "x.md"
    extract.write_text(
        "---\ncitation_scheme: page_line\n---\n[PDF p. 10 | printed p. 8]\n"
        "{1} The average home pays \\$1,040 more\n{2} per year on delivery.\n"
    )
    stream = _ptoks("The average home pays $1,040 more per year on delivery.", page=8, line=1)
    value = next(i for i, t in enumerate(stream) if t.text == "$1,040")
    occ = Occurrence(0, stream[value - 1 : value + 1], stream, value - 1, value + 1, "exact")
    review: list[dict[str, str]] = []
    check_against_extract([Row("Number", [], "", "", None, [occ])], extract, review)
    assert [r["check"] for r in review] == ["extract_checked"]
    assert "1 agree" in review[0]["detail"]
    moved = Occurrence(0, occ.tokens, occ.stream, occ.start, occ.end, "exact")
    for t in moved.stream:
        t.line = 5
    review.clear()
    check_against_extract([Row("Number", [], "", "", None, [moved])], extract, review)
    assert review[0]["check"] == "extract_location"
