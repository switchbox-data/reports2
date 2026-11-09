"""Pull verbatim testimony excerpts into interrogatory-response question blocks.

CIEC questions cite Velez Direct by printed page and line (or footnote). The
``insert-refs`` materializes ``page:line<TAB>text`` paragraphs from the extract
into each ``referenced-testimony`` div; ``interrogatory.lua`` styles them for Word.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from lib.sources.pagelines import parse_extract

_PAGE_LINES = re.compile(r"page (\d+), lines (\d+)-(\d+)(?:\s+and\s+footnote (\d+))?", re.IGNORECASE)
_PAGE_FOOTNOTE = re.compile(r"page (\d+), footnote (\d+)", re.IGNORECASE)
_PAGE_FN_PAIR = re.compile(
    r"page (\d+), lines (\d+)-(\d+), and footnotes (\d+) and (\d+)",
    re.IGNORECASE,
)
_TESTIMONY_CALL = re.compile(r'testimony\(\s*["\']([^"\']+)["\']\s*\)')
_DIV_OPEN = re.compile(r"^:{3,}\s*(?:\{\s*\.(?P<braced>[\w-]+)[^}]*\}|\{\s*custom-style=[^}]*\}|[\w-]+)\s*$")
_VELEZ_LINE = re.compile(r"^\d+:\d+\t")
_VELEZ_FN_LINE = re.compile(r"^\d+ n\.\d+\t")
_PASSAGE_TITLE = re.compile(r"^\*\*Velez Direct, printed")
_DIV_CLOSE = re.compile(r"^:{3,}\s*$")
_REFERENCED_BLOCK = re.compile(
    r"::: \{\.referenced-testimony\}\s*\n(.*?):::",
    re.DOTALL,
)


@dataclass(frozen=True)
class PassageLine:
    label: str
    text: str


class TestimonyExcerptError(ValueError):
    pass


def _refer_tail_from_line(line: str) -> str | None:
    prefix = "Please refer to Velez Direct Testimony at "
    if not line.strip().lower().startswith(prefix.lower()):
        return None
    return line.strip()[len(prefix) :].rstrip(".").strip()


def parse_velez_references(refer_tail: str) -> list[str]:
    """Return ``testimony()`` ref keys in the order CIEC cites them."""
    events: list[tuple[int, str]] = []

    for m in _PAGE_FN_PAIR.finditer(refer_tail):
        pg, lo, hi, f1, f2 = m.groups()
        pos = m.start()
        events.extend(
            [
                (pos, f"{pg}:{lo}-{hi}"),
                (pos, f"{pg}:n{f1}"),
                (pos, f"{pg}:n{f2}"),
            ]
        )

    fn_pair_spans = [(m.start(), m.end()) for m in _PAGE_FN_PAIR.finditer(refer_tail)]

    for m in _PAGE_LINES.finditer(refer_tail):
        if any(s <= m.start() and m.end() <= e for s, e in fn_pair_spans):
            continue
        pg, lo, hi, fn = m.group(1), m.group(2), m.group(3), m.group(4)
        pos = m.start()
        events.append((pos, f"{pg}:{lo}-{hi}"))
        if fn:
            events.append((pos, f"{pg}:n{fn}"))

    for m in _PAGE_FOOTNOTE.finditer(refer_tail):
        events.append((m.start(), f"{m.group(1)}:n{m.group(2)}"))

    events.sort(key=lambda item: item[0])
    refs: list[str] = []
    seen: set[str] = set()
    for _, ref in events:
        if ref in seen:
            continue
        seen.add(ref)
        refs.append(ref)

    if not refs:
        raise TestimonyExcerptError(f"could not parse Velez references in: {refer_tail!r}")
    return refs


def parse_ref(ref: str) -> tuple[int, int | None, int | None, int | None]:
    """Parse ``95:1-16`` or ``83:n75`` into printed page and line or footnote."""
    ref = ref.strip()
    m = re.fullmatch(r"(\d+):n(\d+)", ref)
    if m:
        return int(m.group(1)), None, None, int(m.group(2))
    m = re.fullmatch(r"(\d+):(\d+)-(\d+)", ref)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), None
    m = re.fullmatch(r"(\d+):(\d+)", ref)
    if m:
        n = int(m.group(2))
        return int(m.group(1)), n, n, None
    raise TestimonyExcerptError(f"bad testimony ref {ref!r}; use PAGE:LINE-LINE or PAGE:nFOOTNOTE")


def _printed_int(printed: str | None) -> int | None:
    if not printed or not printed.isdigit():
        return None
    return int(printed)


@dataclass
class _Index:
    by_page_line: dict[tuple[int, int], str]
    footnotes: dict[tuple[int, int], str]  # (printed_page, num) -> text


def _build_index(text: str) -> _Index:
    ex = parse_extract(text)
    by_page_line: dict[tuple[int, int], str] = {}
    footnotes: dict[tuple[int, int], str] = {}
    for ln in ex.lines:
        page = _printed_int(ln.printed)
        if page is None:
            continue
        if ln.footnote is not None and ln.start is None:
            num_m = re.fullmatch(r"(\d+)", ln.footnote)
            if num_m:
                footnotes[(page, int(num_m.group(1)))] = ln.text.strip()
            continue
        if ln.start is None or ln.end is None:
            continue
        for n in range(ln.start, ln.end + 1):
            by_page_line[(page, n)] = ln.text.strip()
    return _Index(by_page_line, footnotes)


def _slice(index: _Index, ref: str) -> list[PassageLine]:
    page, lo, hi, foot = parse_ref(ref)
    if foot is not None:
        try:
            text = index.footnotes[(page, foot)]
        except KeyError as exc:
            raise TestimonyExcerptError(f"footnote {foot} not found on printed p. {page}") from exc
        return [PassageLine(f"{page} n.{foot}", text)]
    assert lo is not None and hi is not None
    lines: list[PassageLine] = []
    missing: list[int] = []
    for n in range(lo, hi + 1):
        key = (page, n)
        if key not in index.by_page_line:
            missing.append(n)
            continue
        lines.append(PassageLine(f"{page}:{n}", index.by_page_line[key]))
    if missing:
        raise TestimonyExcerptError(f"printed p. {page} missing line(s) {missing} (ref {ref})")
    if not lines:
        raise TestimonyExcerptError(f"no lines for ref {ref}")
    return lines


@lru_cache(maxsize=4)
def _load_index(path: Path) -> _Index:
    return _build_index(path.read_text(encoding="utf-8"))


def format_passage_markdown(lines: list[PassageLine]) -> str:
    """Plain paragraphs for Quarto ``results: asis``; styled in Word by ``interrogatory.lua``."""
    parts: list[str] = []
    for row in lines:
        text = row.text.replace("\n", " ").strip()
        parts.append(f"{row.label}\t{text}")
    return "\n\n".join(parts) + ("\n\n" if parts else "")


def bind_testimony(extract_path: Path) -> Callable[[str], str]:
    """Return ``testimony(ref)`` bound to one extract file."""
    extract_path = extract_path.resolve()
    if not extract_path.is_file():
        raise FileNotFoundError(extract_path)

    def testimony(ref: str) -> str:
        return format_passage_markdown(_slice(_load_index(extract_path), ref))

    return testimony


def _strip_div_blocks(question: str, *, open_line: str) -> str:
    """Remove one fenced-div region that starts with ``open_line`` (nest-balanced)."""
    lines = question.splitlines()
    out: list[str] = []
    in_div = False
    nest = 0
    for line in lines:
        opened = _DIV_OPEN.match(line)
        if not in_div and line.strip() == open_line:
            in_div = True
            nest = 1
            continue
        if in_div:
            if opened:
                nest += 1
                continue
            if _DIV_CLOSE.match(line):
                nest -= 1
                if nest == 0:
                    in_div = False
                continue
            continue
        out.append(line)
    return "\n".join(out)


def _strip_referenced_testimony(question: str) -> str:
    """Remove the nested ``referenced-testimony`` block (all passage divs inside it)."""
    return _strip_div_blocks(question, open_line="::: {.referenced-testimony}")


def _scrub_legacy_testimony_markup(question: str) -> str:
    """Remove referenced excerpts and any legacy nested passage divs."""
    question = _strip_referenced_testimony(question)
    while "testimony-passage" in question:
        before = question
        question = _strip_div_blocks(question, open_line="::: {.testimony-passage}")
        # Broken inserts sometimes dropped the leading colons.
        question = _strip_div_blocks(question, open_line=" {.testimony-passage}")
        if question == before:
            break
    while "IR Testimony Passage" in question:
        before = question
        question = _strip_div_blocks(question, open_line='::: {custom-style="IR Testimony Passage"}')
        if question == before:
            break
    kept: list[str] = []
    for line in question.splitlines():
        if _VELEZ_LINE.match(line) or _VELEZ_FN_LINE.match(line):
            continue
        if _PASSAGE_TITLE.match(line.strip()):
            continue
        kept.append(line)
    return "\n".join(kept)


def question_lines_for_extract_check(question: str) -> str:
    """Drop ``referenced-testimony`` blocks so only CIEC's words are checked."""
    return _strip_referenced_testimony(question)


def testimony_calls_in_question(question: str) -> list[str]:
    return expected_refs_from_question(question)


def expected_refs_from_question(question: str) -> list[str]:
    for raw in question.splitlines():
        tail = _refer_tail_from_line(raw.strip())
        if tail is not None:
            return parse_velez_references(tail)
    raise TestimonyExcerptError("no 'Please refer to Velez Direct Testimony' line in question")


def verify_referenced_testimony(question: str, extract_path: Path, label: str) -> list[str]:
    """Confirm inline ``testimony()`` calls match the question's cite line."""
    problems: list[str] = []
    try:
        expected = expected_refs_from_question(question)
    except TestimonyExcerptError as exc:
        return [f"{label}: {exc}"]
    if not _REFERENCED_BLOCK.search(question):
        problems.append(f"{label}: question cites Velez Direct but has no `referenced-testimony` block")
        return problems
    found = testimony_calls_in_question(question)
    if found != expected:
        problems.append(f"{label}: testimony refs {found!r} do not match the cite line {expected!r}")
    for ref in found:
        try:
            _slice(_load_index(extract_path.resolve()), ref)
        except (TestimonyExcerptError, FileNotFoundError) as exc:
            problems.append(f"{label}: testimony({ref!r}): {exc}")
    return problems


def ref_caption(ref: str) -> str:
    """Human-readable label for one CIEC cite key (``6:11-23``, ``83:n75``, …)."""
    page, lo, hi, foot = parse_ref(ref)
    if foot is not None:
        return f"Velez Direct, printed p. {page}, footnote {foot}"
    assert lo is not None and hi is not None
    if lo == hi:
        return f"Velez Direct, printed p. {page}, line {lo}"
    return f"Velez Direct, printed p. {page}, lines {lo}–{hi}"  # noqa: RUF001


def _referenced_testimony_inner(extract_path: Path, refs: list[str]) -> str:
    """Machine-generated block: one div, bold passage titles, ``page:line<TAB>text`` lines."""
    index = _load_index(extract_path.resolve())
    parts: list[str] = ["::: {.referenced-testimony}", ""]
    for ref in refs:
        parts.append(f"**{ref_caption(ref)}**")
        parts.append("")
        line_paras: list[str] = []
        for row in _slice(index, ref):
            text = row.text.replace("\n", " ").strip()
            line_paras.append(f"{row.label}\t{text}")
        parts.append("\n\n".join(line_paras))
        parts.append("")
    parts.append(":::")
    return "\n".join(parts)


def insert_referenced_testimony_block(question: str, extract_path: Path) -> str:
    """Insert or refresh a ``referenced-testimony`` block after the Please refer line."""
    question = _scrub_legacy_testimony_markup(question)
    question = re.sub(r"\n{3,}", "\n\n", question).strip()
    lines = question.splitlines()
    out: list[str] = []
    inserted = False
    for line in lines:
        out.append(line)
        tail = _refer_tail_from_line(line.strip())
        if tail is not None and not inserted:
            refs = parse_velez_references(tail)
            out.append("")
            out.append(_referenced_testimony_inner(extract_path, refs))
            out.append("")
            inserted = True
    if not inserted:
        raise TestimonyExcerptError("no Please refer line found")
    return "\n".join(out).strip()
