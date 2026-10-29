"""Build the CIEC-1 provenance table for the CT Eversource testimony.

For every figure, table and computed number in the submitted testimony PDF,
records its page/line in the PDF and a GitHub permalink (at the
``ct_eversource_submission`` tag) to the notebook cell that generates it.

Outputs (in this directory):

- ``pdf_lines.json``: the PDF indexed by printed page, margin line, footnote and caption
- ``provenance.csv``: one row per artifact (type, location, what it is, link)
- ``provenance_review.csv``: internal checks (never shown in the Word document)
- ``provenance.md`` / ``ciec_1_provenance.docx``: the document sent to CIEC
"""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import os
import re
import subprocess
import zipfile
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import boto3
from pypdf import PdfReader
from rapidfuzz import fuzz

TAG = "ct_eversource_submission"
RDP_PIN = "e97a3ca"
MC_TAGS = {
    "dist_and_sub_tx": ("mc/92366c905831", "utils/data_prep/marginal_costs/generate_utility_tx_dx_mc.py"),
    "bulk_tx": ("mc/1b1b329be68f", "utils/data_prep/marginal_costs/bulk_tx/generate_bulk_tx_mc.py"),
}
# The MC methodology docs at TAG misstate the bulk-tx dollar year; this commit on RDP main corrects them.
RDP_MC_DOCS_REF = "979af55635436ed27b829457fcced7c9ad43d34e"
BATCH_PREFIX = "switchbox/cairo/outputs/hp_rates/ct/ct_eversource/ct_20261015_a/"
S3_BUCKET = "data.sb"

PATH_HERE = Path(__file__).resolve().parent
PATH_REPORT = PATH_HERE.parent
PATH_REPO = PATH_REPORT.parents[1]
PATH_RDP = Path(os.environ.get("PATH_RDP", PATH_REPO.parent / "rate-design-platform"))
REPORT_REL = "reports/ct_hp_rates"
QMD_NAME = "expert_testimony.qmd"
PATH_PDF = PATH_REPO / "context/sources/ct_hp_rates/Direct Testimony of Juan-Pablo Velez - Docket No. 26-05-10.pdf"

REPORTS2_BLOB = f"https://github.com/switchbox-data/reports2/blob/{TAG}/{REPORT_REL}"
RDP_BLOB = "https://github.com/switchbox-data/rate-design-platform/blob"
RDP_TREE = "https://github.com/switchbox-data/rate-design-platform/tree"

NAMESPACES = {
    "r": "representative_home",
    "m": "delivery_mc",
    "mc": "marginal_costs",
    "a": "analysis",
    "fc": "incremental_fair_default",
    "op": "overpayment",
    "th": "rate6_threshold",
    "fh": "feeder_headroom",
}

NOTEBOOK_BLURBS = {
    "representative_home": (
        "Typical home's usage and bills",
        "Monthly electricity use, bills and grid costs for the average fossil-fuel-heated home, "
        "before and after it installs a heat pump.",
    ),
    "delivery_mc": (
        "When the grid is under strain",
        "Which hours of the year drive new grid costs, and how large those costs are.",
    ),
    "marginal_costs": (
        "Cost of new grid capacity",
        "The cost of adding distribution and transmission capacity, drawn from the Company's filings.",
    ),
    "feeder_headroom": (
        "Spare grid capacity",
        "Each distribution feeder's peak demand compared with its capacity.",
    ),
    "overpayment": (
        "Overpayment across all homes",
        "How much each home that installs a heat pump would overpay for delivery under each rate.",
    ),
    "analysis": (
        "Bill changes by heating fuel",
        "How many homes would see their bills rise or fall under each rate.",
    ),
    "rate6_threshold": (
        "Rate 6's 700 kWh threshold",
        "How the 700 kWh winter threshold sorts each home's usage into discounted and undiscounted blocks.",
    ),
    "incremental_fair_default": (
        "Fixed charge alternative",
        "The fixed charge that would remove the overpayment if the volumetric rate were lowered instead.",
    ),
    "expert_testimony": (
        "The testimony itself",
        "The text of the testimony, including its tables and the filed Rate 1 charges it quotes.",
    ),
}


def git_show(rev: str, path: str, repo: Path = PATH_REPO) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "show", f"{rev}:{path}"], check=True, capture_output=True, text=True
    ).stdout


# ---------------------------------------------------------------------------
# PDF index
# ---------------------------------------------------------------------------

BODY_RE = re.compile(r"^\s{0,3}(\d{1,2})\s{2,}(\S.*)$")
CAPTION_RE = re.compile(r"^\s*(Figure|Table)\s+(\d+):\s*(.*)$")
FOOTNOTE_RE = re.compile(r"^\s{4,}(\d{1,3})\s+(\S.*)$")


def normalize_pdf_text(s: str) -> str:
    s = re.sub(r"(?<=[A-Za-z])\s+-(?=[A-Za-z])", "-", s)  # "fuel  -heated", "Juan -Pablo"
    s = re.sub(r"(?<=\w)-\s+(?=\w)", "-", s)  # "26-     05-10", "non-       bypassable"
    s = re.sub(r"(?<=[\s$])-\s+(?=\d)", "-", s)  # "- 0.911", "$- 1"
    s = re.sub(r"(?<=\S)\s+—", " —", s)
    s = re.sub(r"(?<=[A-Za-z])\s+-\s+(?=[a-z])", "-", s)  # "fuel - heated"
    for glued in (r"(?<=\d%)(?=[A-Za-z])", r"(?<=\bvs\.)(?=[\dA-Z])", r"(?<=Figure \d)(?=[a-z])",
                  r"(?<=Figure \d\d)(?=[a-z])", r"(?<=Table \d)(?=[a-z])"):  # fmt: skip
        s = re.sub(glued, " ", s)
    return re.sub(r"\s+", " ", s).strip()


@dataclass
class PdfToken:
    text: str
    page: int
    line: int | None
    footnote: int | None = None
    space: bool = True


SUBTOKEN_RE = re.compile(r"\$?[-\u2212]?\d[\d,]*(?:\.\d+)?%?|[A-Za-z][\w'\u2019]*|\S")


def split_word(word: str) -> list[tuple[str, bool]]:
    """Split a whitespace word into number/word pieces, flagging which follow a space.

    Punctuation-only pieces stay glued to a neighbor so quotes keep their punctuation.
    """
    pieces: list[list[Any]] = []
    pending = ""
    for k, p in enumerate(SUBTOKEN_RE.findall(word)):
        if norm_tok(p):
            pieces.append([pending + p, k == 0 or (bool(pending) and len(pieces) == 0)])
            pending = ""
        elif pieces:
            pieces[-1][0] += p
        else:
            pending += p
    if pending:
        pieces.append([pending, True])
    if pieces:
        pieces[0][1] = True
    return [(p, s) for p, s in pieces]


def join_tokens(tokens: list[Any]) -> str:
    return "".join((" " if t.space and k else "") + t.text for k, t in enumerate(tokens))


@dataclass
class PdfIndex:
    lines: list[dict[str, Any]] = field(default_factory=list)
    body: list[PdfToken] = field(default_factory=list)
    footnotes: dict[int, list[PdfToken]] = field(default_factory=dict)
    footnote_pages: dict[int, int] = field(default_factory=dict)
    captions: list[dict[str, Any]] = field(default_factory=list)


def _strip_footnote_marker(tok: str, page_footnotes: set[int]) -> str:
    m = re.match(r"^(.*?[^\d\s])(\d{1,3})$", tok)
    if m and int(m.group(2)) in page_footnotes and re.search(r"[.,;:)\u201d\"\u2019%a-zA-Z]$", m.group(1)):
        return m.group(1)
    return tok


def index_pdf(path_pdf: Path) -> PdfIndex:
    reader = PdfReader(str(path_pdf))
    idx = PdfIndex()
    next_fn = 1
    for page_i, page in enumerate(reader.pages):
        raw = [ln for ln in page.extract_text(extraction_mode="layout").splitlines() if ln.strip()]
        if not raw:
            continue
        printed: int | None = int(raw[-1].strip()) if raw[-1].strip().isdigit() else None
        if printed is None:
            continue
        raw = raw[:-1]
        page_lines: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        for ln in raw:
            if m := BODY_RE.match(ln):
                page_lines.append({"kind": "body", "line": int(m.group(1)), "text": normalize_pdf_text(m.group(2))})
                current = None
            elif m := CAPTION_RE.match(ln):
                current = {
                    "kind": "caption",
                    "caption_type": m.group(1),
                    "number": int(m.group(2)),
                    "text": normalize_pdf_text(m.group(3)),
                }
                page_lines.append(current)
            elif (m := FOOTNOTE_RE.match(ln)) and int(m.group(1)) == next_fn:
                current = {"kind": "footnote", "number": next_fn, "text": normalize_pdf_text(m.group(2))}
                page_lines.append(current)
                next_fn += 1
            else:
                indent = len(ln) - len(ln.lstrip())
                if (current is not None and current["kind"] == "caption" and indent <= 10) or (
                    current is not None and current["kind"] == "footnote" and indent >= 4
                ):
                    current["text"] += " " + normalize_pdf_text(ln)
                else:
                    current = None
                    page_lines.append({"kind": "other", "text": normalize_pdf_text(ln)})
        page_fns = {pl["number"] for pl in page_lines if pl["kind"] == "footnote"}
        for pl in page_lines:
            if pl["kind"] in ("caption", "footnote"):
                pl["text"] = normalize_pdf_text(re.sub(r"(?<=[A-Za-z])\s*-\s+(?=[a-z])", "-", pl["text"]))
            pl["page"] = printed
            pl["pdf_page"] = page_i + 1
            idx.lines.append(pl)
            if pl["kind"] == "body":
                for tok in pl["text"].split(" "):
                    prev = idx.body[-1].text if idx.body else ""
                    if tok.isdigit() and int(tok) in page_fns and re.search(r"[.,;:)”]$", prev):
                        continue  # superscript footnote marker extracted as its own word
                    idx.body.append(PdfToken(_strip_footnote_marker(tok, page_fns), printed, pl["line"]))
            elif pl["kind"] == "footnote":
                n = pl["number"]
                idx.footnote_pages[n] = printed
                idx.footnotes[n] = [PdfToken(t, printed, None, n) for t in pl["text"].split(" ")]
            elif pl["kind"] == "caption":
                idx.captions.append(
                    {"type": pl["caption_type"], "number": pl["number"], "text": pl["text"], "page": printed}
                )
    _merge_hyphen_breaks(idx.body)
    idx.body = _split_tokens(idx.body)
    idx.footnotes = {n: _split_tokens(toks) for n, toks in idx.footnotes.items()}
    return idx


def _split_tokens(tokens: list[PdfToken]) -> list[PdfToken]:
    return [PdfToken(p, t.page, t.line, t.footnote, space) for t in tokens for p, space in split_word(t.text)]


def _merge_hyphen_breaks(tokens: list[PdfToken]) -> None:
    i = 0
    while i < len(tokens) - 1:
        a, b = tokens[i], tokens[i + 1]
        if a.text == "-" and i > 0 and tokens[i - 1].line == a.line:
            tokens[i - 1].text += "-"
            del tokens[i]
            i -= 1
            continue
        if a.text.endswith("-") and len(a.text) > 1 and (a.line != b.line or a.page != b.page):
            a.text += b.text
            del tokens[i + 1]
        else:
            i += 1


# ---------------------------------------------------------------------------
# qmd parsing
# ---------------------------------------------------------------------------

INLINE_RE = re.compile(r"(?<!`)`\{python\}\s*(.*?)`(?!`)")
EMBED_RE = re.compile(r"\{\{<\s*embed\s+notebooks/(\w+)\.qmd#([\w-]+)\s*>\}\}")
FOOTDEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s?(.*)$")
TABLE_CAP_RE = re.compile(r"^:\s*(.*?)\s*\{#(tbl-[\w-]+)\}\s*$")


@dataclass
class QToken:
    text: str
    expr_id: int | None = None


@dataclass
class Expr:
    id: int
    code: str
    qmd_line: int
    value: str
    in_table: str | None = None


@dataclass
class QmdDoc:
    lines: list[str]
    body: list[QToken] = field(default_factory=list)
    footnotes: dict[str, list[QToken]] = field(default_factory=dict)
    exprs: list[Expr] = field(default_factory=list)
    embeds: list[dict[str, Any]] = field(default_factory=list)
    tables: list[dict[str, Any]] = field(default_factory=list)
    setup_code: str = ""
    setup_start: int = 0


def clean_markdown(s: str) -> str:
    s = re.sub(r"\[\^[^\]]+\]", " ", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[(-?@[^\]]*)\]", " ", s)
    s = re.sub(r"@fig-[\w-]+", "Figure", s)
    s = re.sub(r"@tbl-[\w-]+", "Table", s)
    s = re.sub(r"-?@[\w:.-]*\w", " ", s)
    s = re.sub(r"\{[.#][^}]*\}", " ", s)
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"\*+", "", s)
    s = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", s)
    s = re.sub(r"\\(.)", r"\1", s)
    s = re.sub(r"^\s*#+\s*", "", s)
    s = re.sub(r"^\s*[-*]\s+", "", s)
    return s


def _tokens(s: str, expr_id: int | None = None) -> list[QToken]:
    return [QToken(p, expr_id) for w in s.split() for p, _ in split_word(w)]


def parse_qmd(text: str) -> QmdDoc:
    lines = text.splitlines()
    doc = QmdDoc(lines=lines)
    n = len(lines)
    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while lines[i].strip() != "---":
            i += 1
        i += 1
    paragraphs: list[tuple[int, list[str]]] = []
    buf: list[str] = []
    buf_start = 0
    while i < n:
        ln = lines[i]
        if ln.startswith("```"):
            if buf:
                paragraphs.append((buf_start, buf))
                buf = []
            start = i
            i += 1
            while i < n and not lines[i].startswith("```"):
                i += 1
            if not doc.setup_code and lines[start].startswith("```{python"):
                doc.setup_code = "\n".join(lines[start + 1 : i])
                doc.setup_start = start + 1
            i += 1
            continue
        if not ln.strip() or ln.strip().startswith(":::"):
            if buf:
                paragraphs.append((buf_start, buf))
                buf = []
            i += 1
            continue
        if not buf:
            buf_start = i + 1
        buf.append(ln)
        i += 1
    if buf:
        paragraphs.append((buf_start, buf))

    for start, plines in paragraphs:
        first = plines[0]
        if m := EMBED_RE.search(first):
            doc.embeds.append({"qmd_line": start, "notebook": m.group(1), "label": m.group(2)})
            continue
        if first.lstrip().startswith("|"):
            cap_i = next((k for k, pl in enumerate(plines) if TABLE_CAP_RE.match(pl)), None)
            label, title = None, ""
            if cap_i is not None:
                cm = TABLE_CAP_RE.match(plines[cap_i])
                assert cm
                title, label = cm.group(1), cm.group(2)
            tbl = {"qmd_line": start, "end_line": start + len(plines) - 1, "label": label, "title": title}
            doc.tables.append(tbl)
            for k, pl in enumerate(plines):
                for em in INLINE_RE.finditer(pl):
                    doc.exprs.append(Expr(len(doc.exprs), em.group(1).strip(), start + k, "", label or "table"))
            continue
        if (cm := TABLE_CAP_RE.match(first)) and doc.tables and doc.tables[-1]["label"] is None:
            doc.tables[-1].update(label=cm.group(2), title=cm.group(1), end_line=start)
            continue
        if m := FOOTDEF_RE.match(first):
            label = m.group(1)
            toks = doc.footnotes.setdefault(label, [])
            toks.extend(_render_lines(doc, start, [m.group(2), *plines[1:]]))
            continue
        doc.body.extend(_render_lines(doc, start, plines))
    return doc


def _render_lines(doc: QmdDoc, start: int, plines: list[str]) -> list[QToken]:
    out: list[QToken] = []
    for k, pl in enumerate(plines):
        pos = 0
        for em in INLINE_RE.finditer(pl):
            out.extend(_tokens(clean_markdown(pl[pos : em.start()])))
            expr = Expr(len(doc.exprs), em.group(1).strip(), start + k, "")
            doc.exprs.append(expr)
            out.append(QToken("\0", expr.id))  # placeholder, filled after evaluation
            pos = em.end()
        out.extend(_tokens(clean_markdown(pl[pos:])))
    return out


def evaluate_exprs(doc: QmdDoc) -> dict[str, Any]:
    ns: dict[str, Any] = {}
    cwd = Path.cwd()
    os.chdir(PATH_REPORT)
    try:
        exec(compile(doc.setup_code, QMD_NAME, "exec"), ns)
        for e in doc.exprs:
            try:
                e.value = str(eval(e.code, ns))
            except Exception as exc:
                e.value = f"<error: {exc}>"
    finally:
        os.chdir(cwd)

    def expand(tokens: list[QToken]) -> list[QToken]:
        out: list[QToken] = []
        for t in tokens:
            if t.text == "\0" and t.expr_id is not None:
                out.extend(_tokens(clean_markdown(doc.exprs[t.expr_id].value) or "?", t.expr_id))
            else:
                out.append(t)
        return out

    doc.body = expand(doc.body)
    doc.footnotes = {k: expand(v) for k, v in doc.footnotes.items()}
    return ns


# ---------------------------------------------------------------------------
# Aligning qmd text to the PDF
# ---------------------------------------------------------------------------


def norm_tok(t: str) -> str:
    t = t.lower().replace("\u2019", "'").replace("\u2018", "'").replace("“", '"').replace("”", '"')
    t = t.replace("\u2212", "-").replace("\u2013", "-")
    return t.strip(".,;:()[]\"'!?*")


@dataclass
class Occurrence:
    expr_id: int
    tokens: list[PdfToken]
    stream: list[PdfToken]
    start: int
    end: int
    confidence: str


def align_stream(q_tokens: list[QToken], p_tokens: list[PdfToken]) -> list[Occurrence]:
    qn = [norm_tok(t.text) for t in q_tokens]
    pn = [norm_tok(t.text) for t in p_tokens]
    sm = difflib.SequenceMatcher(None, qn, pn, autojunk=False)
    q2p: list[int | None] = [None] * len(qn)
    exact = [False] * len(qn)
    block_of: list[tuple[int, int, int, int] | None] = [None] * len(qn)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                q2p[i1 + k] = j1 + k
                exact[i1 + k] = True
        elif tag == "replace":
            for k in range(i2 - i1):
                q2p[i1 + k] = j1 + min(int(k * (j2 - j1) / (i2 - i1)), j2 - j1 - 1)
                block_of[i1 + k] = (i1, i2, j1, j2)

    out: list[Occurrence] = []
    i = 0
    while i < len(q_tokens):
        eid = q_tokens[i].expr_id
        if eid is None:
            i += 1
            continue
        s = i
        while i < len(q_tokens) and q_tokens[i].expr_id == eid:
            i += 1
        e = i
        mapped = [q2p[k] for k in range(s, e) if q2p[k] is not None]
        before_ok = s == 0 or exact[s - 1]
        after_ok = e >= len(qn) or exact[e]
        if all(exact[s:e]):
            js, je, conf = q2p[s], q2p[e - 1], "exact"
        elif mapped and before_ok and after_ok:
            blk = block_of[s]
            if blk and blk[0] == s and blk[1] == e:
                js, je = blk[2], blk[3] - 1
            else:
                js, je = min(mapped), max(mapped)
            conf = "anchored"
        elif mapped:
            js, je, conf = min(mapped), max(mapped), "low"
        else:
            out.append(Occurrence(eid, [], p_tokens, -1, -1, "missing"))
            continue
        assert js is not None and je is not None
        out.append(Occurrence(eid, p_tokens[js : je + 1], p_tokens, js, je + 1, conf))
    return out


def match_footnotes(doc: QmdDoc, idx: PdfIndex) -> dict[str, list[tuple[int, float]]]:
    """Map each qmd footnote label to the PDF footnote number(s) carrying its text."""
    p_text = {n: " ".join(norm_tok(t.text) for t in toks) for n, toks in idx.footnotes.items()}
    out: dict[str, list[tuple[int, float]]] = {}
    for label, toks in doc.footnotes.items():
        q = " ".join(norm_tok(t.text) for t in toks)
        scores = sorted(((fuzz.ratio(q, p), n) for n, p in p_text.items()), reverse=True)
        best = scores[0][0]
        out[label] = [(n, s) for s, n in scores if s >= max(85.0, best - 2.0)] or [(scores[0][1], best)]
    return out


# ---------------------------------------------------------------------------
# Resolving artifacts to notebook cells
# ---------------------------------------------------------------------------


@dataclass
class Notebook:
    name: str
    lines: list[str]
    cells: list[tuple[int, int]]


def load_notebook(name: str) -> Notebook:
    rel = f"{REPORT_REL}/{QMD_NAME}" if name == "expert_testimony" else f"{REPORT_REL}/notebooks/{name}.qmd"
    lines = git_show(TAG, rel).splitlines()
    cells: list[tuple[int, int]] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("```{"):
            start = i
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                i += 1
            cells.append((start + 1, i + 1))
        i += 1
    return Notebook(name, lines, cells)


def cell_for_line(nb: Notebook, line: int) -> tuple[int, int]:
    for s, e in nb.cells:
        if s <= line <= e:
            return s, e
    return line, line


def _template_regex(template: str) -> tuple[re.Pattern[str], int]:
    parts = re.split(r"\{[^}]*\}", template)
    literal = sum(len(p) for p in parts)
    return re.compile("[A-Za-z0-9_]+".join(re.escape(p) for p in parts)), literal


def find_var_line(nb: Notebook, var: str) -> int | None:
    literal_re = re.compile(
        r"""(?:\w+_vars\[\s*["']"""
        + re.escape(var)
        + r"""["']\s*\]\s*=(?!=))|(?:^\s*["']"""
        + re.escape(var)
        + r"""["']\s*:)"""
    )
    hits = [k + 1 for k, ln in enumerate(nb.lines) if literal_re.search(ln)]
    if hits:
        return hits[-1]
    best: tuple[int, int] | None = None
    tmpl_re = re.compile(r"""\w+_vars\[\s*f["']([^"']+)["']\s*\]\s*=(?!=)""")
    for k, ln in enumerate(nb.lines):
        for m in tmpl_re.finditer(ln):
            rx, literal = _template_regex(m.group(1))
            if rx.fullmatch(var) and (best is None or literal >= best[0]):
                best = (literal, k + 1)
    return best[1] if best else None


def find_label_line(nb: Notebook, label: str) -> int | None:
    rx = re.compile(r"^#\|\s*label:\s*" + re.escape(label) + r"\s*$")
    return next((k + 1 for k, ln in enumerate(nb.lines) if rx.match(ln)), None)


def fig_caption(nb: Notebook, label_line: int) -> str:
    s, e = cell_for_line(nb, label_line)
    for ln in nb.lines[s - 1 : e]:
        if m := re.match(r'^#\|\s*fig-cap:\s*"?(.*?)"?\s*$', ln):
            return m.group(1)
    return ""


@dataclass
class Link:
    notebook: str
    start: int
    end: int

    @property
    def text(self) -> str:
        return f"{self.notebook}.qmd_{self.start}-{self.end}"

    @property
    def url(self) -> str:
        path = QMD_NAME if self.notebook == "expert_testimony" else f"notebooks/{self.notebook}.qmd"
        return f"{REPORTS2_BLOB}/{path}#L{self.start}-L{self.end}"


VAR_RE = re.compile(r"\b(" + "|".join(list(NAMESPACES)) + r")\.(\w+)")


def resolve_expr(code: str, notebooks: dict[str, Notebook], testimony: Notebook) -> tuple[Link | None, str]:
    for prefix, var in VAR_RE.findall(code):
        nb = notebooks[NAMESPACES[prefix]]
        line = find_var_line(nb, var)
        if line is not None:
            s, e = cell_for_line(nb, line)
            return Link(nb.name, s, e), ""
        return None, f"no assignment of {var!r} in {nb.name}.qmd"
    consts = re.findall(r"\b(FILED_[A-Z_]+)\b", code)
    if consts:
        lines = [k + 1 for k, ln in enumerate(testimony.lines) for c in consts if re.match(rf"^{c}\s*=", ln)]
        if lines:
            return Link("expert_testimony", min(lines), max(lines)), ""
    return None, "no report variable or constant in expression"


# ---------------------------------------------------------------------------
# Building rows
# ---------------------------------------------------------------------------


@dataclass
class Row:
    type: str
    locations: list[tuple[int, int, str]]  # (page, sort_key, label)
    what: str  # markdown
    what_plain: str
    link: Link | None


def md_escape(s: str) -> str:
    return re.sub(r"([\\*_$\[\]<>|#`])", r"\\\1", s)


def format_locations(locs: list[tuple[int, int, str]]) -> str:
    by_page: dict[int, dict[str, list[int]]] = defaultdict(lambda: {"line": [], "footnote": [], "page": []})
    order: list[int] = []
    for page, key, kind in sorted(set(locs)):
        if page not in by_page:
            order.append(page)
        by_page[page][kind].append(key)

    def join(items: list[int]) -> str:
        items = sorted(set(items))
        if len(items) == 1:
            return str(items[0])
        if len(items) == 2:
            return f"{items[0]} and {items[1]}"
        return ", ".join(map(str, items[:-1])) + f", and {items[-1]}"

    parts = []
    for page in order:
        d = by_page[page]
        sub = []
        if d["line"]:
            sub.append(("line " if len(set(d["line"])) == 1 else "lines ") + join(d["line"]))
        if d["footnote"]:
            sub.append(("footnote " if len(set(d["footnote"])) == 1 else "footnotes ") + join(d["footnote"]))
        parts.append(f"p. {page}" + (", " + " and ".join(sub) if sub else ""))
    return "; ".join(parts)


ABBREVIATIONS = {"no.", "vs.", "e.g.", "i.e.", "etc.", "st.", "dr.", "mr.", "ms.", "approx.", "u.s.", "fig.", "p."}


def _ends_sentence(tok: PdfToken) -> bool:
    t = tok.text
    if t in {"•", "Q.", "A."}:
        return True
    return bool(re.search(r"[.?!:]”?$", t)) and t.lower() not in ABBREVIATIONS


def quote_for(occ: Occurrence) -> tuple[str, str]:
    stream, s, e = occ.stream, occ.start, occ.end
    lo = max(0, s - 12)
    while 0 < lo < s and not stream[lo].space:
        lo += 1
    before = stream[lo:s]
    lead = "" if lo == 0 else "…"
    for k in range(len(before) - 1, -1, -1):
        if _ends_sentence(before[k]):
            before, lead = before[k + 1 :], ""
            break
    hi = min(len(stream), e + 10)
    while e < hi < len(stream) and not stream[hi].space:
        hi -= 1
    after = stream[e:hi]
    trail = "" if e + len(after) >= len(stream) else "…"
    if _ends_sentence(occ.tokens[-1]):
        after, trail = [], ""
    for k, t in enumerate(after):
        if t.text in {"•", "Q.", "A."}:
            after, trail = after[:k], ""
            break
        if _ends_sentence(t):
            after, trail = after[: k + 1], ""
            break
    b, v, a = join_tokens(before), join_tokens(occ.tokens), join_tokens(after)
    m = re.match(r"^([(\[“\"]*)(.*?)([).,;:”\"\]]*)$", v)
    assert m
    vpre, vcore, vpost = m.groups()
    sp1 = " " if before and occ.tokens[0].space else ""
    sp2 = " " if after and after[0].space else ""
    md = (
        f"{lead}{md_escape(b)}{sp1}{md_escape(vpre)}**{md_escape(vcore)}**{md_escape(vpost)}{sp2}{md_escape(a)}{trail}"
    ).strip()
    plain = f"{lead}{b}{sp1}{vpre}[{vcore}]{vpost}{sp2}{a}{trail}".strip()
    return md, plain


def location_of(occ: Occurrence) -> tuple[int, int, str]:
    t = occ.tokens[0]
    if t.footnote is not None:
        return (t.page, t.footnote, "footnote")
    assert t.line is not None
    return (t.page, t.line, "line")


def build_rows(doc: QmdDoc, idx: PdfIndex, review: list[dict[str, str]]) -> tuple[list[Row], set[str]]:
    notebooks = {name: load_notebook(name) for name in NAMESPACES.values()}
    testimony = load_notebook("expert_testimony")
    used: set[str] = set()
    rows: list[Row] = []

    # Numbers in body text and footnotes
    occs = align_stream(doc.body, idx.body)
    fn_map = match_footnotes(doc, idx)
    for label, matches in fn_map.items():
        if not any(t.expr_id is not None for t in doc.footnotes[label]):
            continue
        if matches[0][1] < 80:
            review.append({"check": "footnote_match", "item": label, "detail": f"best score {matches[0][1]:.0f}"})
        for n, _ in matches:
            occs.extend(align_stream(doc.footnotes[label], idx.footnotes[n]))

    by_code: dict[str, list[Occurrence]] = defaultdict(list)
    for occ in occs:
        by_code[doc.exprs[occ.expr_id].code].append(occ)
    for code, group in by_code.items():
        found = [o for o in group if o.tokens]
        for o in group:
            expr = doc.exprs[o.expr_id]
            if o.confidence in ("missing", "low"):
                review.append(
                    {
                        "check": f"match_{o.confidence}",
                        "item": code,
                        "detail": f"qmd line {expr.qmd_line}; value {expr.value!r}"
                        + (f"; pdf {join_tokens(o.tokens)!r}" if o.tokens else ""),
                    }
                )
            elif norm_tok(join_tokens(o.tokens)) != norm_tok(clean_markdown(expr.value)):
                review.append(
                    {
                        "check": "pdf_vs_cache",
                        "item": code,
                        "detail": f"{format_locations([location_of(o)])}: pdf "
                        f"{join_tokens(o.tokens)!r} vs cache {expr.value!r}",
                    }
                )
        if not found:
            continue
        link, why = resolve_expr(code, notebooks, testimony)
        if link is None:
            review.append({"check": "unresolved", "item": code, "detail": why})
        else:
            used.add(link.notebook)
        first = min(found, key=lambda o: location_of(o)[:2])
        md, plain = quote_for(first)
        rows.append(Row("Number", [location_of(o) for o in found], md, plain, link))

    # Figures, mapped by embed order
    fig_caps = sorted((c for c in idx.captions if c["type"] == "Figure"), key=lambda c: c["number"])
    if len(fig_caps) != len(doc.embeds):
        review.append(
            {"check": "figure_count", "item": "", "detail": f"{len(doc.embeds)} embeds vs {len(fig_caps)} PDF figures"}
        )
    fig_rows: dict[str, Row] = {}
    for emb, cap in zip(doc.embeds, fig_caps, strict=False):
        nb = notebooks.get(emb["notebook"]) or load_notebook(emb["notebook"])
        label_line = find_label_line(nb, emb["label"])
        link = None
        if label_line is None:
            review.append({"check": "unresolved", "item": emb["label"], "detail": f"label not in {nb.name}.qmd"})
        else:
            link = Link(nb.name, *cell_for_line(nb, label_line))
            used.add(nb.name)
            nb_cap = clean_markdown(fig_caption(nb, label_line))
            score = fuzz.partial_ratio(norm_tok(nb_cap.lower()), norm_tok(cap["text"].lower()))
            if score < 80:
                review.append(
                    {
                        "check": "caption_mismatch",
                        "item": f"Figure {cap['number']} ({emb['label']})",
                        "detail": f"score {score:.0f}: notebook {nb_cap!r} vs pdf {cap['text']!r}",
                    }
                )
        loc = (cap["page"], 0, "page")
        title = f"Figure {cap['number']}: {cap['text']}"
        if emb["label"] in fig_rows:
            row = fig_rows[emb["label"]]
            row.locations.append(loc)
            row.what += f" (also shown as Figure {cap['number']})"
            row.what_plain += f" (also shown as Figure {cap['number']})"
        else:
            fig_rows[emb["label"]] = row = Row("Figure", [loc], md_escape(title), title, link)
            rows.append(row)

    # Tables, mapped by order; they link to their lines in the testimony
    tbl_caps = sorted((c for c in idx.captions if c["type"] == "Table"), key=lambda c: c["number"])
    if len(tbl_caps) != len(doc.tables):
        review.append(
            {"check": "table_count", "item": "", "detail": f"{len(doc.tables)} qmd tables vs {len(tbl_caps)} PDF"}
        )
    for tbl, cap in zip(doc.tables, tbl_caps, strict=False):
        title = f"Table {cap['number']}: {cap['text']}"
        link = Link("expert_testimony", tbl["qmd_line"], tbl["end_line"])
        used.add("expert_testimony")
        rows.append(Row("Table", [(cap["page"], 0, "page")], md_escape(title), title, link))

    kind_order = {"page": 0, "line": 1, "footnote": 2}
    rows.sort(key=lambda r: min((p, kind_order[k], s) for p, s, k in r.locations))
    return rows, used


# ---------------------------------------------------------------------------
# Internal checks against the simulation runs (review CSV only)
# ---------------------------------------------------------------------------


def _s3_json(s3: Any, key: str) -> Any:
    try:
        return json.loads(s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read())
    except s3.exceptions.NoSuchKey:
        return None


def _urdb_rates(urdb: dict[str, Any]) -> tuple[float, list[float]]:
    item = urdb["items"][0]
    rates = sorted(
        round(t.get("rate", 0.0) + t.get("adj", 0.0), 8) for period in item["energyratestructure"] for t in period
    )
    return float(item.get("fixedchargefirstmeter", 0.0)), rates


def _cairo_rates(cfg: dict[str, Any]) -> tuple[float, list[float]]:
    return float(cfg["ur_monthly_fixed_charge"]), sorted(round(row[4], 8) for row in cfg["ur_ec_tou_mat"])


def check_runs(review: list[dict[str, str]]) -> None:
    s3 = boto3.client("s3")
    pages = s3.get_paginator("list_objects_v2").paginate(Bucket=S3_BUCKET, Prefix=BATCH_PREFIX, Delimiter="/")
    runs = [
        p["Prefix"]
        for page in pages
        for p in page.get("CommonPrefixes", [])
        if re.search(r"/\d{8}_\d{6}_[^/]+/$", p["Prefix"])
    ]
    n_tariffs = 0
    mc_seen: dict[str, set[str]] = defaultdict(set)
    mc_paths: dict[str, str] = {}
    for run in runs:
        run_name = run.rstrip("/").rsplit("/", 1)[-1]
        settings = _s3_json(s3, run + "scenario_settings.json")
        used = _s3_json(s3, run + "marginal_costs_used.json")
        if settings is None or used is None:
            review.append({"check": "run_record_missing", "item": run_name, "detail": "no settings or MC record"})
            continue
        for mc_type, rec in _iter_mc_records(used):
            mc_seen[mc_type].add(rec["sha256"])
            mc_paths[mc_type] = rec["path"]
        for path_key in ("path_tariff_maps_electric", "path_tariff_maps_gas"):
            rel = _rdp_rel(settings.get(path_key))
            if rel and not _rdp_exists(rel):
                review.append({"check": "run_file_missing", "item": run_name, "detail": f"{rel} not at {RDP_PIN}"})
        if "_precalc_" not in run_name or "uncalibrated" not in run_name:
            continue
        final = _s3_json(s3, run + "tariff_final_config.json") or {}
        for key, local_path in settings.get("path_tariffs_electric", {}).items():
            rel = _rdp_rel(local_path)
            if not rel or not _rdp_exists(rel):
                review.append({"check": "run_file_missing", "item": run_name, "detail": f"{rel} not at {RDP_PIN}"})
                continue
            if key not in final:
                continue
            pinned = _urdb_rates(json.loads(git_show(RDP_PIN, rel, PATH_RDP)))
            ran = _cairo_rates(final[key])
            n_tariffs += 1
            if abs(pinned[0] - ran[0]) > 1e-6 or pinned[1] != ran[1]:
                review.append(
                    {
                        "check": "run_tariff_vs_pin",
                        "item": run_name,
                        "detail": f"{rel}: pinned fixed/rates {pinned} vs run {ran}",
                    }
                )
    for mc_type, hashes in mc_seen.items():
        if len(hashes) != 1:
            review.append({"check": "mc_hash", "item": mc_type, "detail": f"runs used {len(hashes)} different files"})
            continue
        path = mc_paths[mc_type]
        bucket, key = path.removeprefix("s3://").split("/", 1)
        live = hashlib.sha256(s3.get_object(Bucket=bucket, Key=key)["Body"].read()).hexdigest()
        if live != next(iter(hashes)):
            review.append({"check": "mc_hash", "item": mc_type, "detail": f"live {live} vs run {next(iter(hashes))}"})
    review.append(
        {
            "check": "runs_checked",
            "item": str(len(runs)),
            "detail": f"run directories; {n_tariffs} precalc tariffs compared to {RDP_PIN}; "
            f"MC files hashed: {sorted(mc_seen)}",
        }
    )


def _iter_mc_records(used: Any) -> list[tuple[str, dict[str, Any]]]:
    out: list[tuple[str, dict[str, Any]]] = []

    def walk(node: Any, mc_type: str | None) -> None:
        if isinstance(node, dict):
            if "sha256" in node and "path" in node and str(node["path"]).startswith("s3://"):
                out.append((mc_type or "?", node))
                return
            for k, v in node.items():
                walk(v, mc_type or (k if k in MC_TAGS else None))
        elif isinstance(node, list):
            for v in node:
                walk(v, mc_type)

    walk(used, None)
    return [(t, r) for t, r in out if t in MC_TAGS]


def _rdp_rel(local_path: str | None) -> str | None:
    if not local_path:
        return None
    m = re.search(r"rate-design-platform/(.+)$", local_path)
    return m.group(1) if m else None


def _rdp_exists(rel: str) -> bool:
    r = subprocess.run(["git", "-C", str(PATH_RDP), "cat-file", "-e", f"{RDP_PIN}:{rel}"], capture_output=True)
    return r.returncode == 0


# ---------------------------------------------------------------------------
# Writing the document
# ---------------------------------------------------------------------------

INTRO = f"""\
This document lists every figure, table and calculated number in the Direct Testimony of
Juan-Pablo Velez (Docket No. 26-05-10), and links each one to the code that produced it.
Figures, tables and numbers each have their own table, in the order they appear in the testimony.

- **Location** gives the page and line number in the testimony as filed. Items that appear
  more than once are listed once, with every place they appear.
- The second column gives the figure or table title, or for numbers, a short quote with the
  number in bold.
- **Where it's generated** links to the block of code that produces the item. Our analysis is
  written as notebooks: documents that explain each step in plain language next to the code
  that carries it out. Each link opens the exact lines on GitHub, frozen at the version used for
  the testimony (labeled `{TAG}`), so the links will keep pointing to the same code.
"""


def rdp_links() -> list[str]:
    def blob(ref: str, path: str) -> str:
        return f"{RDP_BLOB}/{ref}/{path}"

    dist_tag, dist_path = MC_TAGS["dist_and_sub_tx"]
    bulk_tag, bulk_path = MC_TAGS["bulk_tx"]
    return [
        "**Hourly cost of new distribution capacity**: "
        f"[explanation]({blob(RDP_MC_DOCS_REF, 'context/methods/marginal_costs/ct_eversource_dist_mc_methodology.md')}), "
        f"[code]({blob(dist_tag, dist_path)}).",
        "**Hourly cost of new bulk transmission capacity**: "
        f"[explanation]({blob(RDP_MC_DOCS_REF, 'context/methods/marginal_costs/ct_bulk_transmission_marginal_cost.md')}), "
        f"[code]({blob(bulk_tag, bulk_path)}).",
        f"**Bill simulation for every modeled home**: [code]({blob(TAG, 'rate_design/hp_rates/run_scenario.py')}).",
        "**The rates we simulated** (Rate 1, Rate 6 and Rate HP): "
        f"[rate definitions]({RDP_TREE}/{TAG}/rate_design/hp_rates/ct/config/tariffs/electric).",
        "**How we derived Rate HP**: "
        f"[explanation]({blob(TAG, 'context/methods/tou_and_rates/icos_tariff_derivation.md')}), "
        f"[code]({blob(TAG, 'utils/mid/derive_icos_tariff.py')}).",
    ]


def write_markdown(rows: list[Row], used: set[str], path_md: Path) -> None:
    out = [
        "---",
        'title: "CIEC-1: Where the testimony\'s figures, tables and numbers come from"',
        'subtitle: "Direct Testimony of Juan-Pablo Velez, Docket No. 26-05-10"',
        "---",
        "",
        INTRO,
        "## Where the work happens",
        "",
        "The table links to these notebooks:",
        "",
    ]
    for name in [*NAMESPACES.values(), "expert_testimony"]:
        if name not in used:
            continue
        title, blurb = NOTEBOOK_BLURBS[name]
        path = QMD_NAME if name == "expert_testimony" else f"notebooks/{name}.qmd"
        out.append(f"- **{title}** ([{name}.qmd]({REPORTS2_BLOB}/{path})): {blurb}")
    out += [
        "",
        "The notebooks read results from Switchbox's rate simulation platform, which models each home's "
        "hourly electricity use, its bills under each rate, and the cost of serving it:",
        "",
        *[f"- {s}" for s in rdp_links()],
        "",
    ]
    for heading, row_type, what in (
        ("Figures", "Figure", "Figure"),
        ("Tables", "Table", "Table"),
        ("Numbers", "Number", "Quote (number in bold)"),
    ):
        out += [
            f"## {heading}",
            "",
            f"| Location | {what} | Where it's generated |",
            "|------------------|--------------------------------------------------|------------------------------|",
        ]
        for r in rows:
            if r.type != row_type:
                continue
            link = f"[{md_escape(r.link.text)}]({r.link.url})" if r.link else ""
            out.append(f"| {format_locations(r.locations)} | {r.what} | {link} |")
        out.append("")
    path_md.write_text("\n".join(out))


def landscape_reference(path_ref: Path) -> Path:
    data = subprocess.run(
        ["quarto", "pandoc", "--print-default-data-file", "reference.docx"], check=True, capture_output=True
    ).stdout
    path_ref.write_bytes(data)
    tmp = path_ref.with_suffix(".tmp.docx")
    with zipfile.ZipFile(path_ref) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            buf = zin.read(item.filename)
            if item.filename == "word/document.xml":
                page = (
                    '<w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/>'
                    '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" '
                    'w:header="720" w:footer="720" w:gutter="0"/>'
                )
                buf = buf.decode().replace("<w:sectPr>", "<w:sectPr>" + page, 1).encode()
            elif item.filename == "word/styles.xml":
                xml = buf.decode()
                compact = xml.find('w:styleId="Compact"')
                end = xml.find("</w:style>", compact)
                xml = xml[:end] + '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>' + xml[end:]
                buf = xml.encode()
            zout.writestr(item, buf)
    tmp.replace(path_ref)
    return path_ref


def write_docx(path_md: Path, path_docx: Path) -> None:
    ref = landscape_reference(PATH_HERE / ".reference_landscape.docx")
    subprocess.run(
        ["quarto", "pandoc", str(path_md), "-o", str(path_docx), f"--reference-doc={ref}", "--columns=200"],
        check=True,
    )
    ref.unlink()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build the CIEC-1 provenance table for the CT testimony.")
    ap.add_argument("--path-output-dir", type=Path, default=PATH_HERE)
    ap.add_argument("--skip-s3", action="store_true", help="skip the checks against the simulation runs on S3")
    args = ap.parse_args()
    out_dir: Path = args.path_output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    idx = index_pdf(PATH_PDF)
    (out_dir / "pdf_lines.json").write_text(json.dumps(idx.lines, indent=1, ensure_ascii=False))
    doc = parse_qmd(git_show(TAG, f"{REPORT_REL}/{QMD_NAME}"))
    evaluate_exprs(doc)

    review: list[dict[str, str]] = []
    rows, used = build_rows(doc, idx, review)
    if not args.skip_s3:
        check_runs(review)

    write_csv(
        out_dir / "provenance.csv",
        [
            {
                "type": r.type,
                "location": format_locations(r.locations),
                "what_it_is": r.what_plain,
                "link_text": r.link.text if r.link else "",
                "url": r.link.url if r.link else "",
            }
            for r in rows
        ],
    )
    write_csv(out_dir / "provenance_review.csv", review)
    path_md = out_dir / "provenance.md"
    write_markdown(rows, used, path_md)
    write_docx(path_md, out_dir / "ciec_1_provenance.docx")
    counts = defaultdict(int)
    for r in rows:
        counts[r.type] += 1
    print(f"{len(rows)} rows ({dict(counts)}); {len(review)} review items -> {out_dir}")


if __name__ == "__main__":
    main()
