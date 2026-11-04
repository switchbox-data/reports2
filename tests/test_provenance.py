"""Tests for lib.provenance (testimony provenance documents)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from lib.provenance import links
from lib.provenance.align import Occurrence, align_stream
from lib.provenance.build import check_cache
from lib.provenance.config import Hardcoded, KnownDifference, Link, ProvenanceConfig
from lib.provenance.document import write_markdown
from lib.provenance.extract_check import check_against_extract
from lib.provenance.pdf_index import PdfIndex, PdfToken, classify_page, filed_testimony_pages, index_pdf
from lib.provenance.qmd import QmdDoc, QToken, parse_qmd, strip_html_comments
from lib.provenance.resolve import Notebook, filed_constant_resolver, find_var_line, resolve_expr
from lib.provenance.rows import (
    Row,
    _hardcoded_rows,
    _known_difference,
    _locate_table,
    _rescue_known_difference,
    format_locations,
    quote_for,
)
from lib.provenance.runs import _cairo_rates, _iter_mc_records, _urdb_rates
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
    # The number moved to another sentence after rendering; the value search still finds it.
    q = _qtoks("we simulated bills for each of the", "4,897", "buildings in the territory under both rates")
    p = _ptoks(
        "we simulated bills for each of the homes in the territory under both rates. "
        "In all, 4,897 buildings in the sample"
    )
    occ = align_stream(q, p)[0]
    assert occ.confidence == "fallback"
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
    assert link.url.endswith("/blob/t/reports/x/notebooks/rep.qmd#L3-L9")
    assert link.notebook == "rep"
    assert cfg.notebook_link("expert_testimony", 1, 2).url.endswith("/blob/t/reports/x/expert_testimony.qmd#L1-L2")


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


def test_caption_on_numbered_lines_stays_body_and_is_recorded():
    page = PdfPage(
        8,
        [
            PdfLine(76, "the same homes before and after (Table 1).", 2, 72),
            PdfLine(104, "Table 1: Annual change for the average home that switches to a", 3, 72),
            PdfLine(118, "heat pump, measured two ways.", 4, 72),
            PdfLine(140, "Added electricity use 4,801 kWh", None, 72),
            PdfLine(400, "Next body line", 5, 72),
        ],
        "6",
    )
    idx = index_pdf(Path("unused.pdf"), pages=[page])
    assert idx.captions == [
        {
            "type": "Table",
            "number": 1,
            "text": "Annual change for the average home that switches to a heat pump, measured two ways.",
            "page": 6,
        }
    ]
    assert [t.line for t in idx.body if t.text == "Table"] == [3]
    assert "4,801" not in [t.text for t in idx.body]


def test_numbered_caption_without_period_ends_at_unnumbered_line():
    page = PdfPage(
        8,
        [
            PdfLine(104, "Table 1: Annual change for the average home", 3, 72),
            PdfLine(124, "Added electricity use 4,801 kWh", None, 72),  # table row, close and not indented
            PdfLine(400, "Next body line", 4, 72),
        ],
        "6",
    )
    idx = index_pdf(Path("unused.pdf"), pages=[page])
    assert [c["text"] for c in idx.captions] == ["Annual change for the average home"]


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
    elsewhere = _ptoks("The average home pays $1,040 more per year on delivery.", page=8, line=5)
    moved = Occurrence(0, elsewhere[value - 1 : value + 1], elsewhere, value - 1, value + 1, "exact")
    review.clear()
    check_against_extract([Row("Number", [], "", "", None, [moved])], extract, review)
    assert review[0]["check"] == "extract_location"


def test_includes_code_by_namespace_and_exclude_list():
    cfg = _cfg(
        namespaces={"d": "direct", "s": "rerun"},
        include_namespaces=frozenset({"s"}),
        exclude_codes=frozenset({"dollar(min(d.x, s.x))"}),
    )
    assert cfg.includes_code("dollar(mc_delta(s))")  # bare namespace argument
    assert cfg.includes_code("dollar(max(d.x, s.x))")
    assert not cfg.includes_code("dollar(min(d.x, s.x))")
    assert not cfg.includes_code("pct(-d.rhp_pct_change_dist)")
    assert cfg.includes_notebook("rerun") and not cfg.includes_notebook("direct")
    assert _cfg().includes_code("pct(-d.x)")


def test_check_links_tries_refs_with_slashes(monkeypatch):
    exists = {
        "repos/org/r2/contents/reports/x/notebooks/a.qmd?ref=tag1",
        "repos/org/rdp/contents/rate_design/hp_rates?ref=tag2",
        "repos/org/rdp/contents/utils/mc.py?ref=mc/abc123",
    }
    calls: list[str] = []

    def fake_run(cmd: list[str], **_kw: object) -> subprocess.CompletedProcess[str]:
        calls.append(cmd[2])
        return subprocess.CompletedProcess(cmd, 0 if cmd[2] in exists else 1)

    monkeypatch.setattr(links.subprocess, "run", fake_run)
    md = (
        "[a](https://github.com/org/r2/blob/tag1/reports/x/notebooks/a.qmd#L3-L9) "
        "[a again](https://github.com/org/r2/blob/tag1/reports/x/notebooks/a.qmd#L20-L30) "
        "[folder](https://github.com/org/rdp/tree/tag2/rate_design/hp_rates/) "
        "[slash tag](https://github.com/org/rdp/blob/mc/abc123/utils/mc.py)"
    )
    review: list[dict[str, str]] = []
    links.check_links([*links.find_urls(md), "https://github.com/org/r2/blob/tag1/missing.qmd"], review)
    assert exists <= set(calls)
    assert review == [
        {"check": "link_missing", "item": "org/r2", "detail": "tag1/missing.qmd not found on GitHub"},
        {"check": "links_checked", "item": "4", "detail": "files and folders linked; 1 not found"},
    ]


def test_resolve_expr_prefers_the_included_namespace():
    notebooks = {
        "direct": Notebook("direct", ['report_vars["o"] = 1'], [(1, 1)]),
        "rerun": Notebook("rerun", ["```{python}", 'report_vars["o"] = 2', "```"], [(1, 3)]),
    }
    testimony = Notebook("expert_testimony", [], [])
    code = "dollar(max(d.o, s.o))"
    cfg = _cfg(namespaces={"d": "direct", "s": "rerun"})
    res = resolve_expr(cfg, code, notebooks, testimony)
    assert res.link is not None and res.link.notebook == "direct"
    cfg = _cfg(namespaces={"d": "direct", "s": "rerun"}, include_namespaces=frozenset({"s"}))
    res = resolve_expr(cfg, code, notebooks, testimony)
    assert res.link is not None and res.link.url.endswith("/notebooks/rerun.qmd#L1-L3")
    assert res.other_cells == ("o at direct.qmd_1-1",)


def test_filed_constant_resolver_links_setup_constants():
    testimony = Notebook("expert_testimony", ["import x", "FILED_TX = 1.0", "FILED_DX = 2.0", "y = 3"], [])
    resolve = filed_constant_resolver()
    link = resolve("dollar(FILED_TX + FILED_DX)", testimony, _cfg())
    assert link is not None and link.url.endswith("/reports/x/expert_testimony.qmd#L2-L3")
    assert resolve("dollar(r.x)", testimony, _cfg()) is None


def test_hardcoded_rows_locate_the_number_by_its_context():
    link = Link("src", "https://example.com/src")
    idx = PdfIndex(body=_ptoks("In 2024 BGE served 1,234 customers, and in 2025 it served 1,234 more.", page=4, line=7))
    cfg = _cfg(hardcoded=[Hardcoded("1,234", "it served 1,234 more", link)])
    review: list[dict[str, str]] = []
    rows = _hardcoded_rows(cfg, idx, review)
    assert len(rows) == 1 and rows[0].link == link
    [occ] = rows[0].occurrences
    assert occ.start == [t.text for t in idx.body].index("more.") - 1  # the second 1,234
    assert review == []
    assert _hardcoded_rows(_cfg(hardcoded=[Hardcoded("9", "nine 9 homes", link)]), idx, review) == []
    assert review[0]["check"] == "hardcoded_missing"
    with pytest.raises(ValueError):
        _hardcoded_rows(_cfg(hardcoded=[Hardcoded("1,234", "served customers", link)]), idx, review)


def test_write_markdown_leaves_out_empty_sections(tmp_path: Path):
    cfg = _cfg(notebook_blurbs={"rep": ("Typical home", "The average home.")})
    link = cfg.notebook_link("rep", 1, 2)
    path_md = tmp_path / "p.md"
    write_markdown(cfg, [Row("Number", [(5, 3, "line")], "**\\$1**", "[$1]", link)], path_md)
    md = path_md.read_text()
    assert "## Numbers" in md and "| p. 5, line 3 |" in md
    assert "## Figures" not in md and "## Tables" not in md
    assert "**Typical home**" in md


def _git_repo(path: Path) -> None:
    def run(*args: str) -> None:
        subprocess.run(["git", "-C", str(path), "-c", "user.name=t", "-c", "user.email=t@t", *args], check=True)

    path.mkdir()
    run("init", "-q")
    (path / "f.txt").write_text("x")
    run("add", "f.txt")
    run("commit", "-q", "-m", "c", "--date=2020-01-01T00:00:00Z")
    run("tag", "-a", "t", "-m", "t")


def test_check_cache_flags_files_written_after_the_tag_elsewhere(tmp_path: Path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setenv("GIT_COMMITTER_DATE", "2020-01-01T00:00:00Z")
    _git_repo(repo)
    cfg = _cfg(path_repo=repo)
    doc = QmdDoc(lines=[], setup_code='pickle.loads(Path("cache/v.pkl").read_bytes())')
    for exec_dir in (tmp_path / "elsewhere", repo):
        (exec_dir / "cache").mkdir(parents=True)
        (exec_dir / "cache/v.pkl").write_bytes(b"v")  # written now, after the 2020 tag commit
    review: list[dict[str, str]] = []
    check_cache(cfg, doc, tmp_path / "elsewhere", review)
    assert [r["check"] for r in review] == ["cache_file", "cache_not_from_tag"]
    review.clear()
    check_cache(cfg, doc, repo, review)  # the checkout at the tag: its cache is the tag's
    assert [r["check"] for r in review] == ["cache_file"]


def test_runs_tariff_and_marginal_cost_records():
    urdb = {
        "items": [
            {"fixedchargefirstmeter": 10, "energyratestructure": [[{"rate": 0.1, "adj": 0.01}], [{"rate": 0.05}]]}
        ]
    }
    assert _urdb_rates(urdb) == (10.0, [0.05, 0.11])
    cairo = {"ur_monthly_fixed_charge": 10, "ur_ec_tou_mat": [[1, 1, 1e38, 0, 0.11, 0], [2, 1, 1e38, 0, 0.05, 0]]}
    assert _cairo_rates(cairo) == _urdb_rates(urdb)
    used = {
        "dist_and_sub_tx": {"path": "s3://b/dist.parquet", "sha256": "a"},
        "delivery": {"bulk_tx": [{"path": "s3://b/bulk.parquet", "sha256": "b"}]},
        "supply": {"path": "s3://b/supply.parquet", "sha256": "c"},
        "local": {"bulk_tx": {"path": "/tmp/bulk.parquet", "sha256": "d"}},
    }
    records = _iter_mc_records(used, {"dist_and_sub_tx", "bulk_tx"})
    assert [(t, r["sha256"]) for t, r in records] == [("dist_and_sub_tx", "a"), ("bulk_tx", "b")]
