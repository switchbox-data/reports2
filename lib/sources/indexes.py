"""Index rows for ingested sources: the global ``context/README.md`` table and a folder ``README.md`` table.

Rows are keyed by file path, so rerunning an ingest replaces its row rather than adding a second one. An existing
row is found anywhere in the README (any section or table), and a workbook stub ``x.md`` also matches an older
row naming ``x.xlsx``; only a file with no row gets a new one, in the sources section or first file table. A
folder that already has a one-row directory entry in the global table (``` `general_reference/bonbright_1960/` (directory) ```)
is covered by it and gets no per-file row; the folder's own README table, when it has one, still does.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from lib.sources import env

GLOBAL_README = env.REPO_ROOT / "context" / "README.md"
SECTION = "## sources/"

_DIR_SUFFIX = re.compile(r"\s*\(directory\)\s*$")


WORKBOOK_SUFFIXES = (".xlsx", ".xlsm", ".xls")


def _cell_key(cell: str) -> str:
    return _DIR_SUFFIX.sub("", cell.strip()).strip("` ").strip()


def _names(key: str) -> set[str]:
    """``key`` and, for a workbook stub ``x.md``, the workbook ``x.xlsx`` an older row may name instead."""
    if not key.endswith(".md"):
        return {key}
    return {key} | {key[: -len(".md")] + s for s in WORKBOOK_SUFFIXES}


def _find_row(lines: Sequence[str], key: str, start: int = 0, end: int | None = None) -> int | None:
    names = _names(key)
    for i in range(start, len(lines) if end is None else end):
        if _is_row(lines[i]) and not _is_separator(lines[i]) and _cell_key(_split_row(lines[i])[0]) in names:
            return i
    return None


def _split_row(line: str) -> list[str]:
    inner = line.strip()[1:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", inner)]


def _is_row(line: str) -> bool:
    return line.lstrip().startswith("|") and line.rstrip().endswith("|")


def _is_separator(line: str) -> bool:
    return _is_row(line) and set(line.replace("|", "").replace(" ", "")) <= set("-:")


def _escape(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def _row(cells: Sequence[str]) -> str:
    return "| " + " | ".join(_escape(c) for c in cells) + " |"


def _upsert(lines: list[str], start: int, end: int, key: str, row: str) -> bool:
    """Replace the row for ``key`` anywhere in ``lines``, or add it after the last row in ``lines[start:end]``."""
    found = _find_row(lines, key)
    if found is not None:
        if lines[found] == row:
            return False
        lines[found] = row
        return True
    last_row = next(
        (i for i in range(end - 1, start - 1, -1) if _is_row(lines[i]) and not _is_separator(lines[i])), None
    )
    if last_row is None:
        raise ValueError("no table found in the index section")
    lines.insert(last_row + 1, row)
    return True


def _section_bounds(lines: list[str], heading: str) -> tuple[int, int]:
    start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, end


def covered_by_directory_row(rel_path: str, text: str) -> str | None:
    """The global directory row (``folder/ (directory)``) that already covers ``rel_path``, if any."""
    folder = rel_path.split("/", 1)[0] + "/" if "/" in rel_path else None
    if folder is None:
        return None
    start, end = _section_bounds(text.split("\n"), SECTION)
    for line in text.split("\n")[start:end]:
        if _is_row(line) and "(directory)" in line and _cell_key(_split_row(line)[0]) == folder:
            return folder
    return None


def has_global_row(rel_path: str, path: Path | None = None) -> bool:
    """Whether ``rel_path`` has a row in the global index, or a directory row covers it."""
    text = Path(path or GLOBAL_README).read_text(encoding="utf-8")
    return _find_row(text.split("\n"), rel_path) is not None or covered_by_directory_row(rel_path, text) is not None


def upsert_global_row(rel_path: str, description: str, path: Path | None = None) -> str:
    """Add or update the row for ``rel_path`` (relative to ``context/sources/``) in the global index.

    Returns ``"added"``, ``"updated"``, ``"unchanged"`` or ``"covered"`` (a directory row already covers it).
    """
    readme = Path(path) if path else GLOBAL_README
    text = readme.read_text(encoding="utf-8")
    if covered_by_directory_row(rel_path, text):
        return "covered"
    lines = text.split("\n")
    start, end = _section_bounds(lines, SECTION)
    existed = _find_row(lines, rel_path) is not None
    changed = _upsert(lines, start, end, rel_path, _row([rel_path, description]))
    if changed:
        readme.write_text("\n".join(lines), encoding="utf-8")
    return "unchanged" if not changed else ("updated" if existed else "added")


def upsert_folder_row(readme: Path, filename: str, cells: Sequence[str]) -> str:
    """Add or update the row for ``filename`` in a folder README's file table (the table headed ``File``).

    ``cells`` are the columns after the file name, in the table's own order; extra cells are folded into the last
    column and missing ones left empty.
    """
    readme = Path(readme)
    lines = readme.read_text(encoding="utf-8").split("\n")
    header = next(
        (i for i, line in enumerate(lines) if _is_row(line) and _cell_key(_split_row(line)[0]) == "File"), None
    )
    if header is None:
        raise ValueError(f"{readme} has no file table (a table whose first column is 'File')")
    width = len(_split_row(lines[header]))
    end = header + 1
    while end < len(lines) and _is_row(lines[end]):
        end += 1
    rest = list(cells)[: width - 1]
    if len(cells) > width - 1 and width > 1:
        rest[-1] = " ".join([rest[-1], *cells[width - 1 :]])
    rest += [""] * (width - 1 - len(rest))
    existed = _find_row(lines, filename) is not None
    changed = _upsert(lines, header, end, filename, _row([f"`{filename}`", *rest]))
    if changed:
        readme.write_text("\n".join(lines), encoding="utf-8")
    return "unchanged" if not changed else ("updated" if existed else "added")
