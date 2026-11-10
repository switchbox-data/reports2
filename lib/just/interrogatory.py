#!/usr/bin/env python3
"""Interrogatory responses: one .qmd in, Word out.

Written for discovery responses in utility rate cases (first used for CLF and
Sierra Club's responses to CIEC in Connecticut PURA Docket 26-05-10). The
whole set of responses lives in one ``.qmd``. Docket details go in an
``interrogatory_responses:`` block in the frontmatter; each response is a
level-2 heading (the response label) followed by a ``question`` block and a
``response`` block::

    interrogatory_responses:
      docket: PURA Docket No. 26-05-10
      responding_party: Conservation Law Foundation and Sierra Club
      requesting_party: Connecticut Industrial Energy Consumers
      set: Set CIEC-02
      date_issued: 2026-10-29
      date_filed: 2026-11-12
      witness: Juan-Pablo Velez
      source_extract: context/sources/ct_hp_rates/pura_260510_ciec_ir1_to_clf_sc.md

    ## CIEC-1 {witness="Someone Else"}    <- witness override is optional

    ::: {.question}
    Please refer to ...
    :::

    ::: {.response}
    ...
    :::

Two renderings of the same file:

* ``render`` makes one combined Word file for review. Every response starts a
  new Word section with the filed header: party, docket, set, date issued,
  the response label, and "Page n of N" counted within that response.
* ``render --split`` makes one Word file per response, each with the same
  header, ready to save as PDF and file.

``check`` validates the frontmatter and the structure, and (when
``source_extract`` is set) confirms every line of every question appears in
the extract, so a question is never silently reworded.

Usage::

    uv run python -m lib.just.interrogatory new reports/xx/responses.qmd
    uv run python -m lib.just.interrogatory check responses.qmd
    uv run python -m lib.just.interrogatory render responses.qmd
    uv run python -m lib.just.interrogatory render responses.qmd --split
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from lib.just.quarto_env import quarto_env
from lib.just.testimony import _is_placeholder, _parse_date, long_date, read_frontmatter

HERE = Path(__file__).parent
TEMPLATE = HERE / "templates" / "interrogatory_response.docx"
LUA_FILTER = HERE / "templates" / "filters" / "interrogatory.lua"

BLOCK = "interrogatory_responses"

# ---------------------------------------------------------------------------
# Frontmatter fields
# ---------------------------------------------------------------------------

REQUIRED_FIELDS: tuple[str, ...] = (
    "docket",
    "responding_party",
    "requesting_party",
    "set",
    "date_issued",
    "date_filed",
    "witness",
)
OPTIONAL_FIELDS: tuple[str, ...] = (
    "file_prefix",
    "source_extract",
    "testimony_extract",
    "expected_responses",
    "draft",
)
ALL_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS

FIELD_HELP: dict[str, str] = {
    "docket": 'docket as it prints in the header, e.g. "PURA Docket No. 26-05-10"',
    "responding_party": 'who is answering, e.g. "Conservation Law Foundation and Sierra Club"',
    "requesting_party": "who asked the questions (prints as 'Request from')",
    "set": 'the set label as it prints in the header, e.g. "Set CIEC-02"',
    "date_issued": "date the requests were issued, e.g. 2026-10-29",
    "date_filed": "filing date, e.g. 2026-11-12 (use the due date until you know)",
    "witness": "default witness for every response (override per response with {witness=...})",
    "file_prefix": 'start of each split file name, e.g. "CT 26-05-10" gives "CT 26-05-10_CIEC-1 Response.docx" (optional)',
    "source_extract": "path to the extract of the requests; every question line is checked against it (optional)",
    "testimony_extract": "path to the Velez Direct extract; inlines ``testimony()`` refs in question blocks (optional)",
    "expected_responses": "how many responses the set has; checked against the file (optional)",
    "draft": "true (default) prints DRAFT FOR COUNSEL REVIEW at the top of every page; set false for the filing copy",
}


class InterrogatoryError(ValueError):
    """Raised when the frontmatter or the structure of the file is wrong."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = problems
        super().__init__("\n".join(problems))


@dataclass(frozen=True)
class Fields:
    """Validated ``interrogatory_responses:`` fields."""

    docket: str
    responding_party: str
    requesting_party: str
    set_label: str
    date_issued: date
    date_filed: date
    witness: str
    file_prefix: str | None = None
    source_extract: str | None = None
    testimony_extract: str | None = None
    expected_responses: int | None = None
    draft: bool = True


def parse_fields(meta: Mapping[str, Any]) -> Fields:
    """Validate the frontmatter, listing every problem at once."""
    block = meta.get(BLOCK)
    if not isinstance(block, Mapping):
        raise InterrogatoryError(
            [
                f"The frontmatter has no `{BLOCK}:` block. Fill in these fields:",
                *[f"  {name}: {FIELD_HELP[name]}" for name in REQUIRED_FIELDS],
                "Tip: `just new-interrogatory-responses <path>` writes a new file with the block in place.",
            ]
        )

    problems: list[str] = []
    for key in block:
        if key not in ALL_FIELDS:
            problems.append(f"Unknown field `{BLOCK}.{key}`. Known fields: {', '.join(ALL_FIELDS)}.")

    values: dict[str, Any] = {}
    for name in REQUIRED_FIELDS:
        raw = block.get(name)
        text = None if raw is None else str(raw).strip()
        if not text:
            problems.append(f"Missing `{BLOCK}.{name}`: {FIELD_HELP[name]}.")
        elif _is_placeholder(text):
            problems.append(f"`{BLOCK}.{name}` is still a placeholder ({text}): {FIELD_HELP[name]}.")
        elif name in ("date_issued", "date_filed"):
            parsed = _parse_date(raw)
            if parsed is None:
                problems.append(f"`{BLOCK}.{name}` is `{raw}`; write it like 2026-11-12.")
            else:
                values[name] = parsed
        else:
            values["set_label" if name == "set" else name] = text

    for name in ("file_prefix", "source_extract", "testimony_extract"):
        raw = block.get(name)
        if raw is not None and str(raw).strip():
            values[name] = str(raw).strip()

    if block.get("expected_responses") is not None:
        raw = block["expected_responses"]
        if isinstance(raw, int) and not isinstance(raw, bool) and raw > 0:
            values["expected_responses"] = raw
        else:
            problems.append(f"`{BLOCK}.expected_responses` must be a whole number, not `{raw}`.")

    if block.get("draft") is not None:
        raw = block["draft"]
        if isinstance(raw, bool):
            values["draft"] = raw
        else:
            problems.append(f"`{BLOCK}.draft` must be true or false, not `{raw}`.")

    if problems:
        raise InterrogatoryError(problems)
    return Fields(**values)


# ---------------------------------------------------------------------------
# Reading the body: one Response per level-2 heading
# ---------------------------------------------------------------------------

_FRONTMATTER = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_HEADING = re.compile(r"^#{1,6}\s+(?P<label>.*?)\s*(?:\{(?P<attrs>[^}]*)\})?\s*$")
_DIV_OPEN = re.compile(r"^:{3,}\s*(?:\{\s*\.(?P<braced>[\w-]+)[^}]*\}|\{\s*custom-style=[^}]*\}|(?P<bare>[\w-]+))\s*$")
_DIV_CLOSE = re.compile(r"^:{3,}\s*$")
_WITNESS_ATTR = re.compile(r'witness\s*=\s*"([^"]*)"')


@dataclass
class Response:
    label: str
    witness: str | None = None
    question: str = ""
    response: str = ""
    has_question: bool = False
    has_response: bool = False

    @property
    def answered(self) -> bool:
        text = self.response.strip()
        return bool(text) and not text.upper().startswith("TODO") and not _is_placeholder(text)


_PREAMBLE_CHUNK = re.compile(r"^(`{3,}\{python\}.*?`{3,}\s*)$", re.DOTALL)


def _strip_body_preamble(body: str) -> tuple[str, list[str]]:
    """Drop a leading setup chunk (e.g. ``bind_testimony``) before the first heading."""
    match = re.search(r"^#{1,6}\s+", body, re.MULTILINE)
    if match is None:
        return body, []
    preamble = body[: match.start()]
    if not preamble.strip():
        return body[match.start() :], []
    if _PREAMBLE_CHUNK.fullmatch(preamble.strip() + "\n") or _PREAMBLE_CHUNK.fullmatch(preamble.strip()):
        return body[match.start() :], []
    return body, ["Text appears before the first response heading; move it below the first `##` or into a setup chunk."]


def parse_body(text: str) -> tuple[list[Response], list[str]]:
    """Split the body into responses; return them with any structural problems."""
    body = _COMMENT.sub("", _FRONTMATTER.sub("", text, count=1))
    body, preamble_problems = _strip_body_preamble(body)
    responses: list[Response] = []
    problems: list[str] = list(preamble_problems)
    current: Response | None = None
    div: str | None = None
    nest = 0
    buf: list[str] = []

    def close_div() -> None:
        nonlocal div, nest, buf
        if current is not None and div in ("question", "response"):
            setattr(current, div, "\n".join(buf).strip())
        div, nest, buf = None, 0, []

    for line in body.splitlines():
        heading = _HEADING.match(line)
        if heading and div is None:
            attrs = heading.group("attrs") or ""
            witness = _WITNESS_ATTR.search(attrs)
            current = Response(label=heading.group("label").strip(), witness=witness.group(1) if witness else None)
            responses.append(current)
            continue
        opened = _DIV_OPEN.match(line)
        if opened and div is None:
            name = opened.group("braced") or opened.group("bare")
            if current is None:
                problems.append(f"A `{name}` block appears before the first response heading.")
            elif name not in ("question", "response"):
                problems.append(f"{current.label}: unknown block `{name}`; use `question` or `response`.")
            elif getattr(current, f"has_{name}"):
                problems.append(f"{current.label}: more than one `{name}` block.")
            else:
                setattr(current, f"has_{name}", True)
            div = name
            continue
        if opened and div in ("question", "response"):
            nest += 1
            buf.append(line)
            continue
        if _DIV_CLOSE.match(line) and div is not None:
            if nest > 0:
                nest -= 1
                buf.append(line)
                continue
            close_div()
            continue
        if div is not None:
            buf.append(line)
        elif line.strip():
            where = current.label if current else "before the first response heading"
            problems.append(f"Text outside a question/response block ({where}): “{line.strip()[:50]}”.")
    if div is not None:
        problems.append("A block was never closed with `:::`.")

    seen: set[str] = set()
    for r in responses:
        if r.label in seen:
            problems.append(f"{r.label}: this response label appears twice.")
        seen.add(r.label)
        if not r.has_question or not r.question:
            problems.append(f"{r.label}: no question text.")
        if not r.has_response:
            problems.append(f"{r.label}: no `response` block (leave it empty until you write it).")
    if not responses:
        problems.append("No responses found: add a `## <label>` heading for each one.")
    return responses, problems


# ---------------------------------------------------------------------------
# Checking questions against the extract
# ---------------------------------------------------------------------------

_PAGE_MARKER = re.compile(r"\[PDF p\. \d+(?: \| printed p\. \w+)?\]")
_LIST_MARKER = re.compile(r"^\s*[-*+]\s+")


def _squash(text: str) -> str:
    """Drop markdown emphasis and escapes, collapse whitespace."""
    text = re.sub(r"[*_`\\]", "", text.replace("\u00a0", " "))
    return " ".join(text.split())


def _prefix_len(line: str, hay: str) -> int:
    """Length of the longest prefix of ``line`` that occurs in ``hay``."""
    lo, hi = 0, len(line)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if line[:mid] in hay:
            lo = mid
        else:
            hi = mid - 1
    return lo


def verify_questions(responses: list[Response], extract_text: str) -> list[str]:
    """Return one message per question line that is not in the extract."""
    from lib.just.interrogatory_reftext import question_lines_for_extract_check

    hay = _squash(_PAGE_MARKER.sub(" ", extract_text))
    problems: list[str] = []
    for r in responses:
        question = question_lines_for_extract_check(r.question)
        for raw in question.splitlines():
            line = _squash(_LIST_MARKER.sub("", raw))
            if not line or line in hay:
                continue
            n = _prefix_len(line, hay)
            msg = f"{r.label}: a question line is not in the extract"
            if n == 0:
                msg += f"; it starts “{line[:50]}”."
            else:
                at = hay.find(line[:n])
                msg += (
                    f"; it matches up to “…{line[max(0, n - 25) : n]}” and then diverges. "
                    f"Yours: “{line[n : n + 40]}”. Extract: “{hay[at + n : at + n + 40]}”."
                )
            problems.append(msg)
    return problems


# ---------------------------------------------------------------------------
# Checking citations in the responses
# ---------------------------------------------------------------------------

_FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
_FOOTNOTE_DEF = re.compile(r"^\s*\[\^(?P<label>[^\]]+)\]:")
_FOOTNOTE_REF = re.compile(r"\[\^(?P<label>[^\]]+)\](?!:)")
_DRAFT_NOTE = re.compile(
    r"\[(?:TK|NOT INGESTED|NOT EXTRACTED|COUNSEL|RESEARCH|ANALYSIS|UNVERIFIED IDEA|EST|DISCUSSION FOR JPV)\b[^\]]*\]"
)
_INLINE_CITE = re.compile(
    r"\((?:see |_?id\._? )?(?:\w[\w.-]* )?Direct\b|"
    r"\b(?:Direct|Exhibit [\w.-]+|Response to [A-Z][\w-]*\d[\w()]*),? at \d|"
    r"\(_?[Ii]d\._?,? at \d"
)
_BACKTICK_KEY = re.compile(r"`[a-z][a-z0-9]*_[A-Z]\w*_\d{4}[a-z]?`")
_PAGE_ABBREV = re.compile(r"\b(?:PDF )?pp?\. \d")


def check_citations(text: str) -> list[str]:
    """Return one message per citation-style problem in the response blocks.

    Citations go in footnotes written out as in the testimony (see the
    ``expert-testimony`` skill's ``citations.md``), drafts included. Skipped:
    question blocks, fenced code, ``>`` discussion blocks and bracketed draft
    markers such as ``[TK: …]``.
    """
    body = _COMMENT.sub("", _FRONTMATTER.sub("", text, count=1))
    problems: list[str] = []
    label = "before the first response heading"
    div: str | None = None
    fence: str | None = None
    defs: dict[str, int] = {}
    refs: dict[str, int] = {}
    lines = body.splitlines()
    for i, line in enumerate(lines):
        fenced = _FENCE.match(line)
        if fence is not None:
            if fenced and fenced.group(1)[0] == fence[0] and len(fenced.group(1)) >= len(fence):
                fence = None
            continue
        if div is None:
            heading = _HEADING.match(line)
            if heading:
                label = heading.group("label").strip()
                continue
            opened = _DIV_OPEN.match(line)
            if opened:
                div = opened.group("braced") or opened.group("bare")
            continue
        if _DIV_CLOSE.match(line):
            div = None
            continue
        if div != "response":
            continue
        if fenced:
            fence = fenced.group(1)
            continue
        if line.lstrip().startswith(">"):
            continue
        prose = _DRAFT_NOTE.sub("", line)
        footnote = _FOOTNOTE_DEF.match(line)
        for ref in _FOOTNOTE_REF.finditer(prose[footnote.end() :] if footnote else prose):
            refs[ref.group("label")] = refs.get(ref.group("label"), 0) + 1
        if footnote:
            name = footnote.group("label")
            defs[name] = defs.get(name, 0) + 1
            if i + 1 < len(lines) and lines[i + 1].strip():
                problems.append(
                    f"{label}: add a blank line after footnote [^{name}]; without one, Pandoc folds a following "
                    "paragraph into the note."
                )
        elif _INLINE_CITE.search(prose):
            problems.append(
                f"{label}: a citation in the response text (“{line.strip()[:60]}”); move it to a footnote written "
                "out as in the testimony."
            )
        if key := _BACKTICK_KEY.search(prose):
            problems.append(
                f"{label}: a citation key used as a citation (“{key.group(0)}”); write the source out in a "
                "footnote, with `[@key]` after it."
            )
        if page := _PAGE_ABBREV.search(prose):
            problems.append(
                f"{label}: “{page.group(0)}”; pinpoints are written `at 14` or `at 14:5\u20137`, never p., pp. or PDF p."
            )
    for name, n in defs.items():
        if n > 1:
            problems.append(f"Footnote [^{name}] is defined {n} times.")
        if name not in refs:
            problems.append(f"Footnote [^{name}] is defined but never used.")
    for name, n in refs.items():
        if n > 1:
            problems.append(
                f"Footnote [^{name}] is referenced {n} times; Pandoc repeats the note. Give each use its own."
            )
        if name not in defs:
            problems.append(f"Footnote [^{name}] is used but never defined.")
    return problems


def _find_extract(qmd_path: Path, name: str) -> Path | None:
    """Resolve ``source_extract`` against the repo root, then the .qmd folder."""
    candidates = [qmd_path.resolve().parent / name]
    for root in qmd_path.resolve().parents:
        if (root / "pyproject.toml").is_file():
            candidates.insert(0, root / name)
            break
    return next((c for c in candidates if c.is_file()), None)


@dataclass
class Report:
    fields: Fields | None
    responses: list[Response] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def check_file(qmd_path: Path) -> Report:
    """Validate everything about a responses .qmd without rendering."""
    errors: list[str] = []
    fields: Fields | None = None
    try:
        fields = parse_fields(read_frontmatter(qmd_path))
    except InterrogatoryError as err:
        errors.extend(err.problems)

    text = qmd_path.read_text(encoding="utf-8")
    responses, problems = parse_body(text)
    errors.extend(problems)
    errors.extend(check_citations(text))
    report = Report(fields=fields, responses=responses, errors=errors)

    if fields is not None:
        if fields.expected_responses is not None and fields.expected_responses != len(responses):
            errors.append(f"The set has {fields.expected_responses} responses but the file has {len(responses)}.")
        if fields.source_extract:
            extract = _find_extract(qmd_path, fields.source_extract)
            if extract is None:
                errors.append(f"`source_extract` not found: {fields.source_extract}")
            else:
                errors.extend(verify_questions(responses, extract.read_text(encoding="utf-8")))
        else:
            report.notes.append("No `source_extract` set, so the questions were not checked against the requests.")
        if fields.testimony_extract:
            testimony_path = _find_extract(qmd_path, fields.testimony_extract)
            if testimony_path is None:
                errors.append(f"`testimony_extract` not found: {fields.testimony_extract}")
            else:
                from lib.just.interrogatory_reftext import verify_referenced_testimony

                for r in responses:
                    if "Please refer to Velez Direct Testimony" in r.question:
                        errors.extend(verify_referenced_testimony(r.question, testimony_path, r.label))

    open_count = sum(1 for r in responses if not r.answered)
    if responses and open_count:
        report.notes.append(f"{open_count} of {len(responses)} responses are not written yet.")
    return report


def print_report(report: Report, qmd_path: Path) -> None:
    if report.errors:
        print(f"💥 {qmd_path}: needs attention:", file=sys.stderr)
        for line in report.errors:
            print(f"   {line}", file=sys.stderr)
    for note in report.notes:
        print(f"📝 {note}")


# ---------------------------------------------------------------------------
# Per-response header, patched into the rendered .docx
# ---------------------------------------------------------------------------

_NS = (
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
)


def _line(text: str, *, bold: bool = False) -> str:
    rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
    return f'<w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr><w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def _field(instruction: str) -> str:
    return (
        '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        f'<w:r><w:instrText xml:space="preserve"> {instruction} </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        "<w:r><w:rPr><w:noProof/></w:rPr><w:t>1</w:t></w:r>"
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    )


def header_xml(fields: Fields, label: str, pages_field: str = "SECTIONPAGES") -> str:
    """The running header for one response: its own label and its own page count.

    In the combined file every response is its own Word section that restarts
    page numbering at 1, and ``SECTIONPAGES`` counts that section's pages, so
    each response reads "Page 1 of N" for its own N. Word computes it; LibreOffice
    does not support it. A split file holds one response, so ``NUMPAGES`` gives
    the same count and works in LibreOffice and Google Docs too.
    """
    paragraphs = []
    if fields.draft:
        paragraphs.append(_line("DRAFT FOR COUNSEL REVIEW", bold=True))
    paragraphs += [
        _line(fields.responding_party),
        _line(fields.docket),
        _line(fields.set_label),
        _line(f"Date Issued: {long_date(fields.date_issued)}"),
        _line(label),
        (
            '<w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr><w:r><w:t xml:space="preserve">Page </w:t></w:r>'
            f'{_field("PAGE")}<w:r><w:t xml:space="preserve"> of </w:t></w:r>{_field(pages_field)}</w:p>'
        ),
        '<w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr></w:p>',
    ]
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:hdr {_NS}>{"".join(paragraphs)}</w:hdr>\n'


_SECT_PR = re.compile(r"<w:sectPr\b[^>]*?/>|<w:sectPr\b[^>]*>.*?</w:sectPr>", re.DOTALL)
_HEADER_REF = re.compile(r"<w:headerReference\b[^>]*/>")


def patch_headers(docx_path: Path, fields: Fields, labels: list[str], pages_field: str = "SECTIONPAGES") -> None:
    """Give section *i* of the rendered file the header for ``labels[i]``.

    The Lua filter ends every response with a section break, and the last
    response uses the model file's closing section, so the file has exactly one
    ``<w:sectPr>`` per response, in order.
    """
    with zipfile.ZipFile(docx_path) as src:
        parts = {name: src.read(name) for name in src.namelist()}
        infos = {i.filename: i for i in src.infolist()}

    document = parts["word/document.xml"].decode("utf-8")
    sections = list(_SECT_PR.finditer(document))
    if len(sections) != len(labels):
        raise RuntimeError(f"Expected {len(labels)} sections (one per response) but the Word file has {len(sections)}.")

    rels = parts["word/_rels/document.xml.rels"].decode("utf-8")
    content_types = parts["[Content_Types].xml"].decode("utf-8")
    rel_add, type_add = "", ""
    pieces: list[str] = []
    cursor = 0
    for i, (match, label) in enumerate(zip(sections, labels, strict=True), start=1):
        rid, part = f"rIdIRHeader{i}", f"headerIR{i}.xml"
        sect = _HEADER_REF.sub("", match.group(0))
        if sect.endswith("/>") and "</w:sectPr>" not in sect:
            sect = sect[:-2] + f'><w:headerReference w:type="default" r:id="{rid}"/></w:sectPr>'
        else:
            sect = re.sub(
                r"(<w:sectPr\b[^>]*>)", rf'\1<w:headerReference w:type="default" r:id="{rid}"/>', sect, count=1
            )
        pieces += [document[cursor : match.start()], sect]
        cursor = match.end()
        parts[f"word/{part}"] = header_xml(fields, label, pages_field).encode("utf-8")
        rel_add += (
            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
            f'relationships/header" Target="{part}"/>'
        )
        type_add += (
            f'<Override PartName="/word/{part}" ContentType="application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.header+xml"/>'
        )
    pieces.append(document[cursor:])
    document = "".join(pieces)
    if "xmlns:r=" not in document.split(">", 2)[1]:
        document = document.replace(
            "<w:document ",
            '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ',
            1,
        )

    parts["word/document.xml"] = document.encode("utf-8")
    parts["word/_rels/document.xml.rels"] = rels.replace("</Relationships>", rel_add + "</Relationships>").encode(
        "utf-8"
    )
    parts["[Content_Types].xml"] = content_types.replace("</Types>", type_add + "</Types>").encode("utf-8")

    tmp = docx_path.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for name, data in parts.items():
            dst.writestr(infos.get(name, name), data)
    tmp.replace(docx_path)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _render_one(qmd_path: Path, fields: Fields, labels: list[str], output_name: str, only: str | None) -> Path:
    """Run Quarto once, then patch the per-response headers into the result."""
    cmd = [
        "quarto",
        "render",
        qmd_path.name,
        "--to",
        "docx",
        "--output",
        output_name,
        "--reference-doc",
        str(TEMPLATE.resolve()),
        "--lua-filter",
        str(LUA_FILTER.resolve()),
        "-M",
        f"ir-date-filed-long:{long_date(fields.date_filed)}",
    ]
    if only is not None:
        cmd += ["-M", f"ir-only:{only}"]
    result = subprocess.run(cmd, env=quarto_env(), cwd=qmd_path.resolve().parent)
    if result.returncode != 0:
        print("💥 Quarto render failed!", file=sys.stderr)
        sys.exit(1)
    out = qmd_path.resolve().parent / output_name
    patch_headers(out, fields, labels, "NUMPAGES" if only is not None else "SECTIONPAGES")
    return out


def split_file_name(fields: Fields, label: str) -> str:
    name = f"{label} Response.docx"
    return f"{fields.file_prefix}_{name}" if fields.file_prefix else name


def render(qmd_path: Path, *, split: bool = False) -> list[Path]:
    """Check, then render the combined review file or one file per response."""
    from lib.just.draft import _hide_quarto_yml  # draft.py already imports testimony.py

    report = check_file(qmd_path)
    print_report(report, qmd_path)
    if report.errors or report.fields is None:
        sys.exit(2)
    fields, labels = report.fields, [r.label for r in report.responses]

    outputs: list[Path] = []
    with _hide_quarto_yml():
        if not split:
            name = f"{qmd_path.stem}_{date.today():%Y%m%d}.docx"
            outputs.append(_render_one(qmd_path, fields, labels, name, None))
        else:
            out_dir = qmd_path.resolve().parent / "filing"
            out_dir.mkdir(exist_ok=True)
            for label in labels:
                tmp_name = f"_split_{re.sub(r'[^A-Za-z0-9]+', '_', label)}.docx"
                made = _render_one(qmd_path, fields, [label], tmp_name, label)
                target = out_dir / split_file_name(fields, label)
                shutil.move(made, target)
                outputs.append(target)
    for path in outputs:
        print(f"✅ {path}")
    return outputs


# ---------------------------------------------------------------------------
# Scaffold
# ---------------------------------------------------------------------------

SCAFFOLD = """---
title: "Interrogatory Responses"
execute:
  echo: false
format:
  html:
    include-in-header: ../.style/interrogatory-preview.html   # sets quoted testimony apart in the HTML preview
    reference-location: margin   # footnotes beside the paragraph that cites them, not at the end

# Fill in every field below. They become the header printed at the top of every
# page of every response. `just interrogatories` stops and lists anything still
# missing or still in [BRACKETS].
interrogatory_responses:
  docket: "[PURA Docket No. 00-00-00]"
  responding_party: "[Responding party]"
  requesting_party: "[Party that asked the questions]"
  set: "[Set XXXX-01]"
  date_issued: "[YYYY-MM-DD]"
  date_filed: "[YYYY-MM-DD]"
  witness: "[WITNESS NAME]"
  # file_prefix: "CT 00-00-00"   # start of each split file name
  # source_extract: context/sources/...md   # every question line is checked against it
  # testimony_extract: context/sources/...md   # Velez Direct, for inline testimony() quotes
  # expected_responses: 19
  # draft: false   # drop the DRAFT line for the filing copy
---

## XXXX-1

::: {.question}
Paste the question here exactly as the requesting party wrote it.
:::

::: {.response}
:::
"""


def insert_testimony_refs(qmd_path: Path) -> int:
    """Add ``referenced-testimony`` blocks to every question that cites Velez Direct."""
    from lib.just.interrogatory_reftext import insert_referenced_testimony_block

    fields = parse_fields(read_frontmatter(qmd_path))
    if not fields.testimony_extract:
        raise InterrogatoryError(["Set `testimony_extract` in the frontmatter before insert-refs."])
    extract = _find_extract(qmd_path, fields.testimony_extract)
    if extract is None:
        raise InterrogatoryError([f"`testimony_extract` not found: {fields.testimony_extract}"])

    text = qmd_path.read_text(encoding="utf-8")
    body = _COMMENT.sub("", _FRONTMATTER.sub("", text, count=1))
    lines = body.splitlines()
    out_front = text[: len(text) - len(body)]
    out: list[str] = []
    div: str | None = None
    nest = 0
    buf: list[str] = []
    updated = 0

    def flush_question() -> None:
        nonlocal updated
        question = "\n".join(buf).strip()
        patched = insert_referenced_testimony_block(question, extract)
        if patched != question:
            updated += 1
        out.extend(patched.splitlines())
        buf.clear()

    for line in lines:
        opened = _DIV_OPEN.match(line)
        if opened and div is None:
            name = opened.group("braced") or opened.group("bare")
            if name == "question":
                div = name
                out.append(line)
                continue
        if opened and div == "question":
            nest += 1
            buf.append(line)
            continue
        if _DIV_CLOSE.match(line) and div == "question":
            if nest > 0:
                nest -= 1
                buf.append(line)
                continue
            flush_question()
            div = None
            nest = 0
            out.append(line)
            continue
        if div == "question":
            buf.append(line)
            continue
        out.append(line)

    qmd_path.write_text(out_front + "\n".join(out) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    return updated


def write_scaffold(path: Path) -> Path:
    if path.exists():
        raise FileExistsError(f"{path} already exists; not overwriting it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SCAFFOLD, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Create, check or render interrogatory responses.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("new", help="Write a new responses .qmd with the frontmatter block in place.").add_argument(
        "path_qmd"
    )
    sub.add_parser("check", help="Validate fields, structure and questions without rendering.").add_argument("path_qmd")
    sub.add_parser(
        "insert-refs",
        help="Insert referenced-testimony blocks after each Velez Direct cite line.",
    ).add_argument("path_qmd")
    p_render = sub.add_parser("render", help="Render the combined review file, or one file per response.")
    p_render.add_argument("path_qmd")
    p_render.add_argument("--split", action="store_true", help="One Word file per response, in ./filing/.")
    args = parser.parse_args(argv)
    path = Path(args.path_qmd)

    if args.command == "new":
        try:
            created = write_scaffold(path)
        except FileExistsError as exc:
            print(f"💥 {exc}", file=sys.stderr)
            sys.exit(1)
        print(f"✅ Created {created}. Fill in the `{BLOCK}:` fields, then add one section per question.")
        return

    if not path.exists():
        print(f"💥 File not found: {path}", file=sys.stderr)
        sys.exit(1)

    if args.command == "render":
        render(path, split=args.split)
        return

    if args.command == "insert-refs":
        n = insert_testimony_refs(path)
        print(f"✅ {path}: inserted or refreshed referenced-testimony blocks in {n} question(s).")
        return

    report = check_file(path)
    print_report(report, path)
    if report.errors:
        sys.exit(2)
    print(f"✅ {path}: {len(report.responses)} responses OK.")


if __name__ == "__main__":
    main()
