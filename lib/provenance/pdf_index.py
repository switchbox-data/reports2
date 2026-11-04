"""Index a filed testimony PDF by printed page, margin line number, footnote and caption.

Page and line numbers come from ``lib.sources.pagelines.read_pdf``, the same reader that places and checks
the page and line markers in source extracts. On top of it, this module classifies the unnumbered lines of
each testimony page as figure/table captions or footnotes, and tokenizes the text for alignment.

The testimony is the run of pages whose printed page numbers increase; it ends at the first page whose
number does not (the attachments restart at 1). Pages without a printed number (cover letter, cover) are
skipped.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lib.provenance.text import split_word
from lib.sources.pagelines import PdfLine, PdfPage, read_pdf

CAPTION_RE = re.compile(r"^(Figure|Table)\s+(\d+):\s*(.*)$")
FOOTNOTE_RE = re.compile(r"^(\d{1,3})\s+(\S.*)$")
WRAP_GAP = 30.0
"""Most points between the tops of two lines of one wrapped caption or footnote (double-spaced is ~28pt)."""
WRAP_INDENT = 40.0
"""Most points a wrapped caption or footnote line starts right of the body text's left margin (hanging
indents are 36pt); table rows under a caption start further right, so they end the caption."""


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


def filed_testimony_pages(pages: list[PdfPage]) -> list[tuple[int, PdfPage]]:
    """``(printed page, page)`` for the testimony: printed numbers that increase, stopping when they don't."""
    out: list[tuple[int, PdfPage]] = []
    for page in pages:
        label = page.printed_label
        if label is None or not label.isdigit():
            continue
        if out and int(label) <= out[-1][0]:
            break
        out.append((int(label), page))
    return out


def classify_page(page: PdfPage, printed: int, next_fn: int) -> tuple[list[dict[str, Any]], int]:
    """The page's lines as body (numbered), caption, footnote or other; returns the next footnote number.

    A footnote starts with the next footnote number below the page's last numbered line; captions and
    footnotes continue onto following unnumbered lines within ``WRAP_GAP`` below the previous line and
    within ``WRAP_INDENT`` of the body text's left margin.

    A caption printed on numbered lines stays body text and is also recorded as a ``numbered_caption``.
    It continues onto the following numbered lines within ``WRAP_GAP`` until it ends with a period, and
    ends at any unnumbered line, so the rows of a table under it are never appended.
    """
    lines: list[PdfLine] = [
        ln for ln in page.lines if ln.text.strip() and not (ln.number is None and ln.text.strip() == str(printed))
    ]
    numbered = [ln for ln in lines if ln.number is not None]
    last_body_top = max((ln.top for ln in numbered), default=-1.0)
    left = min((ln.x0 for ln in numbered), default=min((ln.x0 for ln in lines), default=0.0))
    out: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    prev_top = 0.0
    for ln in lines:
        text = ln.text.strip()
        if ln.number is not None:
            if current is not None and current["kind"] == "numbered_caption" and ln.top - prev_top <= WRAP_GAP:
                current["text"] += " " + normalize_pdf_text(text)
            elif m := CAPTION_RE.match(text):
                current = {
                    "kind": "numbered_caption",
                    "caption_type": m.group(1),
                    "number": int(m.group(2)),
                    "text": normalize_pdf_text(m.group(3)),
                    "line": ln.number,
                }
                out.append(current)
            else:
                current = None
            if current is not None and current["text"].endswith("."):
                current = None
            out.append({"kind": "body", "line": ln.number, "text": normalize_pdf_text(text)})
        else:
            if current is not None and current["kind"] == "numbered_caption":
                current = None
            if m := CAPTION_RE.match(text):
                current = {
                    "kind": "caption",
                    "caption_type": m.group(1),
                    "number": int(m.group(2)),
                    "text": normalize_pdf_text(m.group(3)),
                }
                out.append(current)
            elif (m := FOOTNOTE_RE.match(text)) and int(m.group(1)) == next_fn and ln.top > last_body_top:
                current = {"kind": "footnote", "number": next_fn, "text": normalize_pdf_text(m.group(2))}
                out.append(current)
                next_fn += 1
            elif current is not None and ln.top - prev_top <= WRAP_GAP and ln.x0 <= left + WRAP_INDENT:
                current["text"] += " " + normalize_pdf_text(text)
            else:
                current = None
                out.append({"kind": "other", "text": normalize_pdf_text(text)})
        prev_top = ln.top
    for pl in out:
        if pl["kind"] in ("caption", "numbered_caption", "footnote"):
            pl["text"] = normalize_pdf_text(re.sub(r"(?<=[A-Za-z])\s*-\s+(?=[a-z])", "-", pl["text"]))
        pl["page"] = printed
        pl["pdf_page"] = page.index
    return out, next_fn


def index_pdf(path_pdf: Path, pages: list[PdfPage] | None = None) -> PdfIndex:
    """Index the testimony; pass ``pages`` (from ``read_pdf``) to reuse a reading of the PDF."""
    idx = PdfIndex()
    next_fn = 1
    for printed, page in filed_testimony_pages(pages if pages is not None else read_pdf(path_pdf)):
        page_lines, next_fn = classify_page(page, printed, next_fn)
        page_fns = {pl["number"] for pl in page_lines if pl["kind"] == "footnote"}
        for pl in page_lines:
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
            elif pl["kind"] in ("caption", "numbered_caption"):
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
