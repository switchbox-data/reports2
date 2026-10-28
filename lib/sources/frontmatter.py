"""Read and edit the flat YAML front matter of extracted-source markdown files.

Existing extracts carry hand-written front matter with inline comments, so edits are line-based: only the
fields being changed are touched, every other line (comments included) and the body stay byte-for-byte as
they were. New identifying fields are inserted in canonical order.

Flat schema: ``source_file``, ``citekey``, ``zotero_item``, ``public_url``, ``short_url``, ``source_url``,
``md5``, ``validated`` come first, then the descriptive fields (``docket``, ``utility``, ``filing_date``,
``filer``, ``document_type``, ``pages_total``, ``extraction_scope``, ``why_here``). ``original_pdf_path`` is
dropped and the legacy ``source`` is renamed ``source_file``.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from lib.sources import env

ID_FIELDS = ("source_file", "citekey", "zotero_item", "public_url", "short_url", "source_url", "md5", "validated")
DESCRIPTIVE_FIELDS = (
    "docket",
    "utility",
    "rate",
    "filing_date",
    "filer",
    "document_type",
    "pages_total",
    "extraction_scope",
    "why_here",
)
LEGACY_RENAMES = {"source": "source_file"}
LEGACY_REMOVED = ("original_pdf_path",)

_KEY_LINE = re.compile(r"^([A-Za-z_][\w.-]*):(?:\s|$)")
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DELIM = "---"
_QUOTED = frozenset({"md5", "zotero_item"})  # hex or short keys that a YAML 1.2 reader could take for numbers


@dataclass
class _Block:
    key: str | None  # None for lines before the first field (comments)
    lines: list[str]


def split(text: str) -> tuple[list[str] | None, str]:
    """``(front matter lines, rest)``; ``rest`` starts at the closing ``---``. ``(None, text)`` without a block."""
    lines = text.split("\n")
    if lines[0].rstrip() != _DELIM:
        return None, text
    for i in range(1, len(lines)):
        if lines[i].rstrip() == _DELIM:
            return lines[1:i], "\n".join(lines[i:])
    return None, text


def _join(front: list[str], rest: str) -> str:
    return "\n".join([_DELIM, *front]) + "\n" + rest


def _blocks(front: list[str]) -> list[_Block]:
    blocks: list[_Block] = []
    for line in front:
        m = _KEY_LINE.match(line)
        if m:
            blocks.append(_Block(m.group(1), [line]))
        elif blocks:
            blocks[-1].lines.append(line)
        else:
            blocks.append(_Block(None, [line]))
    return blocks


def _plain(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value


def parse(text: str) -> dict[str, Any]:
    """Front matter as a dict (dates as ISO strings); ``{}`` when absent or unparseable."""
    front, _ = split(text)
    if front is None:
        return {}
    try:
        data = yaml.safe_load("\n".join(front)) or {}
    except yaml.YAMLError:
        return {}
    return {k: _plain(v) for k, v in data.items()} if isinstance(data, dict) else {}


def read(path: Path) -> dict[str, Any]:
    """Front matter of the file at ``path`` (only the leading block is read)."""
    with Path(path).open(encoding="utf-8", errors="replace") as f:
        head: list[str] = []
        for i, line in enumerate(f):
            head.append(line)
            if i > 0 and line.rstrip() == _DELIM:
                break
            if i > 200:
                return {}
    return parse("".join(head))


def _render(key: str, value: Any) -> list[str]:
    """Lines for ``key: value``; ISO dates stay unquoted, everything else follows PyYAML's quoting rules."""
    if isinstance(value, date | datetime):
        return [f"{key}: {_plain(value)}"]
    if key in _QUOTED and isinstance(value, str):
        return [f"{key}: {json.dumps(value)}"]
    if isinstance(value, str) and _ISO_DATE.match(value):
        return [f"{key}: {value}"]
    dumped = yaml.safe_dump({key: value}, default_flow_style=False, allow_unicode=True, width=10**6, sort_keys=False)
    return dumped.rstrip("\n").split("\n")


def _insert_at(blocks: list[_Block], key: str) -> int:
    """Index at which a new ``key`` goes: after the nearest preceding canonical field present, else the top."""
    if key in ID_FIELDS:
        rank = ID_FIELDS.index(key)
        for i in range(len(blocks) - 1, -1, -1):
            k = blocks[i].key
            if k in ID_FIELDS and ID_FIELDS.index(k) < rank:
                return i + 1
        first = next((i for i, b in enumerate(blocks) if b.key is not None), len(blocks))
        return first
    return len(blocks)


def edit(
    text: str,
    set_fields: Mapping[str, Any] | None = None,
    remove: Iterable[str] = (),
    rename: Mapping[str, str] | None = None,
) -> str:
    """``text`` with the given fields set, removed or renamed; unchanged when nothing needs to change."""
    front, rest = split(text)
    if front is None:
        raise ValueError("no front matter block")
    blocks = _blocks(front)
    for old, new in (rename or {}).items():
        for b in blocks:
            if b.key == old and not any(o.key == new for o in blocks):
                b.lines[0] = new + b.lines[0][len(old) :]
                b.key = new
    removed = set(remove)
    blocks = [b for b in blocks if b.key not in removed]
    for key, value in (set_fields or {}).items():
        new_lines = _render(key, value)
        existing = next((b for b in blocks if b.key == key), None)
        if existing is None:
            blocks.insert(_insert_at(blocks, key), _Block(key, new_lines))
            continue
        if parse_block_value(existing) == _plain(value):
            continue
        comment = _trailing_comment(existing.lines[0]) if len(new_lines) == 1 else ""
        existing.lines = [new_lines[0] + comment, *new_lines[1:]]
    out = [line for b in blocks for line in b.lines]
    return _join(out, rest)


def parse_block_value(block: _Block) -> Any:
    try:
        data = yaml.safe_load("\n".join(block.lines))
    except yaml.YAMLError:
        return object()
    return _plain(data.get(block.key)) if isinstance(data, dict) else object()


def _trailing_comment(line: str) -> str:
    """The ``  # comment`` at the end of a one-line field, so a changed value keeps the author's note."""
    m = re.search(r"\s+#\s.*$", line)
    return m.group(0) if m and not re.search(r"""['"].*#""", line) else ""


def update(
    path: Path,
    set_fields: Mapping[str, Any] | None = None,
    remove: Iterable[str] = (),
    rename: Mapping[str, str] | None = None,
) -> bool:
    """Edit the front matter of ``path`` in place; True when the file changed."""
    path = Path(path)
    old = path.read_text(encoding="utf-8")
    new = edit(old, set_fields, remove, rename)
    if new == old:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def write(path: Path, fields: Mapping[str, Any], body: str) -> None:
    """Create a markdown file with canonical-order front matter followed by ``body``."""
    ordered = [k for k in (*ID_FIELDS, *DESCRIPTIVE_FIELDS) if k in fields]
    ordered += [k for k in fields if k not in ordered]
    lines = [line for k in ordered for line in _render(k, fields[k])]
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join([_DELIM, *lines, _DELIM]) + "\n\n" + body.lstrip("\n"), encoding="utf-8")


def to_flat(text: str, set_fields: Mapping[str, Any] | None = None) -> str:
    """Convert legacy front matter: ``source`` -> ``source_file``, drop ``original_pdf_path``, add new fields."""
    return edit(text, set_fields, remove=LEGACY_REMOVED, rename=LEGACY_RENAMES)


def iter_extracts(root: Path | None = None) -> Iterator[Path]:
    """Every markdown file under ``context/sources`` (nested folders included), skipping index files."""
    base = Path(root) if root else env.SOURCES_DIR
    for p in sorted(base.rglob("*.md")):
        if p.name.lower() != "readme.md":
            yield p


def find_by(field: str, value: str, root: Path | None = None) -> list[Path]:
    """Extracts whose front matter ``field`` equals ``value``."""
    return [p for p in iter_extracts(root) if str(read(p).get(field, "")) == value]


def find_by_citekey(citekey: str, root: Path | None = None) -> Path | None:
    """The extract carrying ``citekey`` (preferring a path whose file name matches the key)."""
    hits = find_by("citekey", citekey, root)
    return hits[0] if hits else None
