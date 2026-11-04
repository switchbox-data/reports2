"""Page and line citations for extracts: read them from the PDF, check them in the markdown, cite from them.

Extracts are cited in testimony by page and, for documents with numbered lines, by page and line, so every
extract carries the PDF's own pagination and line numbering as markers (see
``.cursor/commands/extract-pdf-to-markdown.md``):

- ``[PDF p. 17 | printed p. 14]`` where each PDF page begins (``[PDF p. 1]`` when no number is printed), and
  ``[PDF pp. 91-300 not transcribed: <what>]`` for a run of pages left out of a partial extract.
- ``{5}`` at the start of every source line on a page with line numbers in the margin (after any markdown
  prefix such as ``## `` or ``- ``), one source line per markdown line; ``{12-18}`` before a table or figure
  that occupies those lines.

The facts come from the PDF's text layer, never from an agent's reading: ``read_pdf`` finds each page's lines
and margin numbers, ``skeleton`` emits them as a scaffold to transcribe into, ``check`` compares an extract's
markers with the PDF, and ``cite`` turns a quote into ``14:5-7 (PDF p. 17)`` (printed page 14, lines 5-7).
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

from lib.sources import frontmatter

SCHEMES = ("page", "page_line")

PAGE_MARKER = re.compile(r"\[PDF p\. (\d+)(?: \| printed p\. ([^\]]+))?\]")
OMITTED_MARKER = re.compile(r"\[PDF pp?\. (\d+)(?:\s*[-\u2013]\s*(\d+))? not transcribed(?::[^\]]*)?\]")
_ANY_MARKER = re.compile(rf"{PAGE_MARKER.pattern}|{OMITTED_MARKER.pattern}")
_BLOCK_PREFIX = r"\s*(?:(?:#{1,6}\s+|>\s?|[-*+]\s+|\d+[.)]\s+|\|\s*)\s*)*"
LINE_PREFIX = re.compile(rf"^({_BLOCK_PREFIX})\{{(\d+)(?:\s*[-\u2013]\s*(\d+))?\}}\s?(.*)$")
_FOOTNOTE_DEF = re.compile(r"^\[\^([^\]]+)\]:\s?(.*)$")
_PRINTED_OF = re.compile(r"\bpage\s+(\S+)\s+of\s+\d+\b", re.IGNORECASE)
_BARE_LABEL = re.compile(r"^(?:-\s*)?([0-9]{1,4}|[ivxlcdm]{1,7})(?:\s*-)?$", re.IGNORECASE)

_MARGIN_FRACTION = 0.16  # line numbers sit in the outer 16% of the page width
_SAME_LINE_TOL = 3.0  # points between word tops on one printed line
_MIN_NUMBER_SIZE = 0.7  # margin line numbers are set near body size; footnote superscripts are far smaller
_LINE_SIMILARITY = 0.6  # below this, an extract line probably does not match the PDF line it is numbered as
_PAGE_OVERLAP = 0.6  # share of an extract page's words that must appear on that PDF page


@dataclass
class PdfLine:
    top: float
    text: str
    number: int | None = None


@dataclass
class PdfPage:
    index: int  # 1-based PDF page number
    lines: list[PdfLine]
    printed_label: str | None = None

    @property
    def numbered(self) -> dict[int, str]:
        return {ln.number: ln.text for ln in self.lines if ln.number is not None}

    @property
    def text(self) -> str:
        return " ".join(ln.text for ln in self.lines)


def _group_lines(words: list[dict]) -> list[list[dict]]:
    rows: list[list[dict]] = []
    for w in sorted(words, key=lambda w: (round(w["top"], 1), w["x0"])):
        if rows and abs(rows[-1][0]["top"] - w["top"]) <= _SAME_LINE_TOL:
            rows[-1].append(w)
        else:
            rows.append([w])
    return [sorted(r, key=lambda w: w["x0"]) for r in rows]


def _word_size(word: dict, chars: list[dict]) -> float:
    sizes = [
        float(c["size"])
        for c in chars
        if c["x0"] >= word["x0"] - 0.5 and c["x1"] <= word["x1"] + 0.5 and abs(c["top"] - word["top"]) <= _SAME_LINE_TOL
    ]
    return max(sizes, default=0.0)


def _margin_numbers(words: list[dict], width: float, chars: list[dict] | None = None) -> set[int]:
    """Ids of the words that are margin line numbers: one column of integers counting up by one, top to bottom.

    Footnote numbers at the left edge of a footnote block also count up by one, but they are superscripts, so
    integers set much smaller than the page's body text are not line numbers.
    """
    candidates = [
        w
        for w in words
        if w["text"].isdigit() and (w["x1"] < width * _MARGIN_FRACTION or w["x0"] > width * (1 - _MARGIN_FRACTION))
    ]
    if chars:
        sizes = sorted(float(c["size"]) for c in chars if c["text"].strip())
        body_size = sizes[len(sizes) // 2]
        candidates = [w for w in candidates if _word_size(w, chars) >= body_size * _MIN_NUMBER_SIZE]
    columns: dict[int, list[dict]] = {}
    for w in candidates:
        columns.setdefault(round(w["x1"] / 3), []).append(w)
    best: list[dict] = []
    for col in columns.values():
        col = sorted(col, key=lambda w: w["top"])
        run: list[dict] = []
        for w in col:
            if run and int(w["text"]) == int(run[-1]["text"]) + 1:
                run.append(w)
            elif len(run) < 3:
                run = [w]
        if len(run) > len(best):
            best = run
    return {id(w) for w in best} if len(best) >= 3 else set()


def _printed_label(lines: list[PdfLine], height_tops: tuple[float, float]) -> str | None:
    """The page number printed in the header or footer: "Page N of M" first, then a bare number or numeral."""
    for ln in lines:
        m = _PRINTED_OF.search(ln.text)
        if m:
            return m.group(1)
    top_band, bottom_band = height_tops
    edge = [ln for ln in lines if ln.number is None and (ln.top < top_band or ln.top > bottom_band)]
    for ln in reversed(edge):
        m = _BARE_LABEL.match(ln.text.strip())
        if m:
            return m.group(1)
    return None


def read_pdf(path: Path) -> list[PdfPage]:
    """Every page's text lines (top to bottom), each with its margin line number when it has one."""
    import pdfplumber

    pages: list[PdfPage] = []
    with pdfplumber.open(str(path)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(keep_blank_chars=False, use_text_flow=False)
            margin = _margin_numbers(words, float(page.width), page.chars)
            lines: list[PdfLine] = []
            numbers = {id(w): int(w["text"]) for w in words if id(w) in margin}
            for row in _group_lines(words):
                num = next((numbers[id(w)] for w in row if id(w) in numbers), None)
                text = " ".join(w["text"] for w in row if id(w) not in numbers).strip()
                if text or num is not None:
                    lines.append(PdfLine(top=float(row[0]["top"]), text=text, number=num))
            height = float(page.height)
            label = _printed_label(lines, (height * 0.1, height * 0.88))
            pages.append(PdfPage(index=i, lines=lines, printed_label=label))
    return pages


def has_line_numbers(pages: Iterable[PdfPage], min_share: float = 0.2) -> bool:
    pages = list(pages)
    with_numbers = sum(1 for p in pages if p.numbered)
    return bool(pages) and with_numbers / len(pages) >= min_share


def skeleton(pages: Iterable[PdfPage]) -> str:
    """The PDF's text as a transcription scaffold: page markers, and ``{n}`` on every numbered line."""
    out: list[str] = []
    for p in pages:
        label = f" | printed p. {p.printed_label}" if p.printed_label else ""
        out += ["", f"[PDF p. {p.index}{label}]", ""]
        for ln in p.lines:
            out.append(f"{{{ln.number}}} {ln.text}".rstrip() if ln.number is not None else ln.text)
    return "\n".join(out).lstrip("\n") + "\n"


def normalize(text: str) -> str:
    """Lowercase words only: markdown, footnote marks, link targets, quotes and punctuation removed."""
    text = re.sub(r"\[\^[^\]]+\]", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[\u2018\u2019\u201c\u201d]", "'", text)
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return " ".join(text.split())


@dataclass
class ExtractLine:
    """One unit of an extract body: a numbered line, an unnumbered line, or a footnote definition."""

    pdf_page: int | None
    printed: str | None
    text: str
    start: int | None = None  # source line number, or first of a ``{12-18}`` range
    end: int | None = None
    footnote: str | None = None
    lineno: int = 0  # line in the markdown file


@dataclass
class Marker:
    first: int  # PDF page (first of the run for a not-transcribed marker)
    last: int
    printed: str | None
    lineno: int
    omitted: bool = False


@dataclass
class ExtractPages:
    scheme: str | None
    lines: list[ExtractLine] = field(default_factory=list)
    markers: list[Marker] = field(default_factory=list)

    @property
    def marked(self) -> set[int]:
        return {m.first for m in self.markers if not m.omitted}

    @property
    def omitted(self) -> set[int]:
        return {p for m in self.markers if m.omitted for p in range(m.first, m.last + 1)}


def _unit(text: str, page: int | None, printed: str | None, lineno: int, first_piece: bool) -> ExtractLine:
    fn = _FOOTNOTE_DEF.match(text.strip()) if first_piece else None
    if fn:
        return ExtractLine(page, printed, fn.group(2), footnote=fn.group(1), lineno=lineno)
    lm = LINE_PREFIX.match(text) if first_piece else None
    if lm:
        start = int(lm.group(2))
        end = int(lm.group(3)) if lm.group(3) else start
        return ExtractLine(page, printed, lm.group(4), start=start, end=end, lineno=lineno)
    return ExtractLine(page, printed, text, lineno=lineno)


def parse_extract(text: str) -> ExtractPages:
    """The page markers, line prefixes and footnote definitions of an extract's body.

    A page marker in the middle of a line splits it: the words before the marker stay on the previous page.
    """
    fm = frontmatter.parse(text)
    _, body = frontmatter.split(text)
    offset = text[: len(text) - len(body)].count("\n")
    out = ExtractPages(scheme=fm.get("citation_scheme"))
    page: int | None = None
    printed: str | None = None
    for i, raw in enumerate(body.split("\n"), start=offset + 1):
        pos = 0
        first_piece = True
        footnote: str | None = None
        for m in [*_ANY_MARKER.finditer(raw), None]:
            piece = raw[pos : m.start() if m else len(raw)]
            if piece.strip():
                unit = _unit(piece, page, printed, i, first_piece)
                if footnote is not None:
                    unit.footnote = footnote  # a footnote that runs onto the next page
                footnote = unit.footnote
                out.lines.append(unit)
                first_piece = False
            if m is None:
                break
            pos = m.end()
            if m.group(1):
                page, printed = int(m.group(1)), (m.group(2) or "").strip() or None
                out.markers.append(Marker(page, page, printed, i))
            else:
                lo = int(m.group(3))
                hi = int(m.group(4) or lo)
                out.markers.append(Marker(lo, hi, None, i, omitted=True))
                page, printed = None, None
    return out


def _page_words(text: str) -> set[str]:
    return {w for w in normalize(text).split() if len(w) >= 4}


def check(md_text: str, pages: list[PdfPage]) -> tuple[list[str], list[str]]:
    """``(errors, warnings)`` comparing an extract's page and line markers with the PDF."""
    ex = parse_extract(md_text)
    errors: list[str] = []
    warnings: list[str] = []
    n = len(pages)
    numbered_pdf = has_line_numbers(pages)

    if ex.scheme not in SCHEMES:
        errors.append(f"front matter citation_scheme must be one of {', '.join(SCHEMES)} (got {ex.scheme!r})")
    elif ex.scheme == "page" and numbered_pdf:
        errors.append("the PDF has margin line numbers; set citation_scheme: page_line and mark every line")
    elif ex.scheme == "page_line" and not numbered_pdf:
        warnings.append("citation_scheme is page_line but the PDF shows no margin line numbers")

    last = 0
    for m in ex.markers:
        label = f"PDF p{'p' if m.last > m.first else ''}. {m.first}{f'-{m.last}' if m.last > m.first else ''}"
        if m.first < 1 or m.last > n:
            errors.append(f"line {m.lineno}: {label} is outside the PDF (1-{n})")
        if m.first <= last:
            errors.append(f"line {m.lineno}: {label} comes after PDF p. {last}; page markers must increase")
        if m.printed and "?" in m.printed:
            errors.append(f"line {m.lineno}: {label} has an unresolved printed page label ({m.printed!r})")
        last = max(last, m.last)
    missing = [p for p in range(1, n + 1) if p not in ex.marked and p not in ex.omitted]
    if missing:
        errors.append(f"no page marker for PDF page(s) {page_ranges(missing)}")
    for ln in ex.lines:
        if ln.pdf_page is None and (ln.start is not None or ln.footnote is not None):
            errors.append(f"line {ln.lineno}: numbered line or footnote outside a transcribed page")

    by_page: dict[int, list[ExtractLine]] = {}
    for ln in ex.lines:
        if ln.pdf_page is not None:
            by_page.setdefault(ln.pdf_page, []).append(ln)

    for pdf_page in pages:
        if pdf_page.index in ex.omitted:
            continue
        units = by_page.get(pdf_page.index, [])
        if not pdf_page.text.strip():
            continue  # no text layer (scanned or image-only); nothing to compare
        if ex.scheme == "page_line" and pdf_page.numbered:
            errors += _check_lines(pdf_page, units)
        overlap = _overlap([u for u in units if u.footnote is None], pdf_page)
        if overlap is not None and overlap < _PAGE_OVERLAP:
            warnings.append(
                f"PDF p. {pdf_page.index}: only {overlap:.0%} of the extract's words for this page appear on it; "
                "check the page marker position"
            )
        for u in units:
            if u.footnote is None:
                continue
            fo = _overlap([u], pdf_page)
            if fo is not None and fo < _PAGE_OVERLAP:
                warnings.append(
                    f"line {u.lineno}: footnote [^{u.footnote}] is not printed on PDF p. {pdf_page.index}; "
                    "place each footnote definition on the page it is printed on"
                )
    return errors, warnings


def _overlap(units: list[ExtractLine], page: PdfPage) -> float | None:
    words = _page_words(" ".join(u.text for u in units))
    if len(words) < 8:
        return None
    return len(words & _page_words(page.text)) / len(words)


def _check_lines(page: PdfPage, units: list[ExtractLine]) -> list[str]:
    errors: list[str] = []
    pdf_lines = page.numbered
    covered: set[int] = set()
    last = 0
    for u in units:
        if u.start is None or u.end is None:
            continue
        if u.start < last:
            errors.append(f"line {u.lineno}: {{{u.start}}} follows {{{last}}} on PDF p. {page.index}")
        last = u.end
        span = set(range(u.start, u.end + 1))
        extra = sorted(span - set(pdf_lines))
        if extra:
            errors.append(f"line {u.lineno}: PDF p. {page.index} has no line {page_ranges(extra)}")
        covered |= span
        if u.start == u.end and u.start in pdf_lines:
            want, got = normalize(pdf_lines[u.start]), normalize(u.text)
            if want and SequenceMatcher(None, want, got).ratio() < _LINE_SIMILARITY:
                errors.append(
                    f"line {u.lineno}: {{{u.start}}} on PDF p. {page.index} does not match the PDF line "
                    f"({pdf_lines[u.start][:60]!r})"
                )
    missing = sorted(k for k, text in pdf_lines.items() if text.strip() and k not in covered)
    if missing:
        errors.append(f"PDF p. {page.index}: numbered line(s) {page_ranges(missing)} missing from the extract")
    return errors


def page_ranges(nums: Iterable[int]) -> str:
    nums = sorted(set(nums))
    out: list[str] = []
    start = prev = nums[0]
    for x in nums[1:]:
        if x == prev + 1:
            prev = x
            continue
        out.append(f"{start}-{prev}" if prev > start else str(start))
        start = prev = x
    out.append(f"{start}-{prev}" if prev > start else str(start))
    return ", ".join(out)


@dataclass
class Location:
    pdf_page: int | None
    printed: str | None
    line: int | None


@dataclass
class Citation:
    """Where a quote sits: testimony-style ``page:line`` on the printed page, with the PDF page alongside.

    ``14:5-7 (PDF p. 17)``, ``14:22-15:3 (PDF pp. 17-18)``, ``p. 14 n. 3 (PDF p. 17)``, ``pp. 3-4 (PDF pp. 5-6)``.
    A page with no printed number is given by its PDF page (``PDF p. 2``).
    """

    start: Location
    end: Location
    footnote: str | None = None

    def __str__(self) -> str:
        s, e = self.start, self.end
        one_page = s.pdf_page == e.pdf_page
        pdf = f"PDF p. {s.pdf_page}" if one_page else f"PDF pp. {s.pdf_page}-{e.pdf_page}"
        if not (s.printed and e.printed):
            if self.footnote:
                return f"{pdf} n. {self.footnote}"
            if s.line is not None and e.line is not None:
                return (
                    f"{pdf}, lines {s.line}-{e.line}" if (s.line != e.line or not one_page) else f"{pdf}, line {s.line}"
                )
            return pdf
        if self.footnote:
            return f"p. {s.printed} n. {self.footnote} ({pdf})"
        if s.line is not None and e.line is not None:
            if one_page:
                where = f"{s.printed}:{s.line}" + (f"-{e.line}" if e.line != s.line else "")
            else:
                where = f"{s.printed}:{s.line}-{e.printed}:{e.line}"
        else:
            where = f"p. {s.printed}" if one_page else f"pp. {s.printed}-{e.printed}"
        return f"{where} ({pdf})"


def cite(md_text: str, quote: str) -> list[Citation]:
    """Every place ``quote`` occurs in the extract, as PDF page, printed page and line (or footnote)."""
    ex = parse_extract(md_text)
    target = normalize(quote)
    if not target:
        return []
    results: list[Citation] = []
    streams: dict[str | None, list[ExtractLine]] = {}  # the body reads through footnotes; each footnote alone
    for ln in ex.lines:
        streams.setdefault(ln.footnote, []).append(ln)
    for units in streams.values():
        joined = ""
        spans: list[tuple[int, int, ExtractLine]] = []
        for u in units:
            t = normalize(u.text)
            if not t:
                continue
            if joined:
                joined += " "
            spans.append((len(joined), len(joined) + len(t), u))
            joined += t
        start = joined.find(target)
        while start != -1:
            end = start + len(target)
            hit = [u for s, e, u in spans if s < end and e > start]
            results.append(_citation(hit))
            start = joined.find(target, start + 1)
    return results


def _citation(units: list[ExtractLine]) -> Citation:
    paged = [u for u in units if u.pdf_page is not None] or units
    first, last = paged[0], paged[-1]
    numbered = [u for u in paged if u.start is not None]
    lo = numbered[0].start if numbered else None
    hi = numbered[-1].end if numbered else None
    return Citation(
        Location(first.pdf_page, first.printed, lo),
        Location(last.pdf_page, last.printed, hi),
        first.footnote,
    )
