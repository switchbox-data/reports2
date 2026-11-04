"""Parse a testimony qmd into body/footnote token streams, inline expressions, embeds and tables."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lib.provenance.text import split_word

INLINE_RE = re.compile(r"(?<!`)`\{python\}\s*(.*?)`(?!`)")
EMBED_RE = re.compile(r"\{\{<\s*embed\s+notebooks/(\w+)\.qmd#([\w-]+)\s*>\}\}")
FOOTDEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s?(.*)$")
TABLE_CAP_RE = re.compile(r"^:\s*(.*?)\s*\{#(tbl-[\w-]+)\}\s*$")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


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


def strip_html_comments(text: str) -> str:
    """Blank out ``<!-- -->`` blocks, keeping line numbers stable for permalinks."""
    return HTML_COMMENT_RE.sub(lambda m: "\n" * m.group().count("\n"), text)


def _table_header(row: str) -> list[str]:
    cells = [clean_markdown(INLINE_RE.sub(" ", c)).strip() for c in row.strip().strip("|").split("|")]
    return [c for c in cells if c and not re.fullmatch(r"[-:\s]+", c)]


def parse_qmd(text: str) -> QmdDoc:
    lines = strip_html_comments(text).splitlines()
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
            tbl = {
                "qmd_line": start,
                "end_line": start + len(plines) - 1,
                "label": label,
                "title": title,
                "header": _table_header(first),
            }
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


def evaluate_exprs(doc: QmdDoc, path_exec_dir: Path, qmd_name: str) -> dict[str, Any]:
    """Evaluate every inline expression and splice its value into the token streams.

    Runs the qmd's setup cell (which loads the cached report variables) with the working directory
    temporarily set to ``path_exec_dir``, so its relative ``cache/`` paths resolve, and returns the
    setup cell's namespace. An expression that fails to evaluate gets ``<error: ...>`` as its value.
    """
    ns: dict[str, Any] = {}
    cwd = Path.cwd()
    os.chdir(path_exec_dir)
    try:
        exec(compile(doc.setup_code, qmd_name, "exec"), ns)
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
