"""Parse and edit Zotero's Extra field as ordered ``Name: value`` lines.

Zotero stores free-form metadata in Extra, one entry per line. Two lines matter here:

- ``Citation Key: <key>`` pins an item's citation key.
- ``tex.shortauthor: <short form>`` holds an organization's abbreviation.

The public-copy lines (``DocumentCloud ID``, ``Google Drive ID``, ``Wayback URL``) are written by ingest.

Every other line (and any free text) is preserved verbatim and in order.
"""

from __future__ import annotations

import re

CITATION_KEY = "Citation Key"
SHORTAUTHOR = "tex.shortauthor"
# Lines ingest writes to record where an item's public copies live; they never belong in the bibliography.
DOCUMENTCLOUD_ID = "DocumentCloud ID"
DRIVE_ID = "Google Drive ID"
WAYBACK_URL = "Wayback URL"
MANAGED = (CITATION_KEY, SHORTAUTHOR, DOCUMENTCLOUD_ID, DRIVE_ID, WAYBACK_URL)

_FIELD_RE = re.compile(r"^\s*([^:\n]+?)\s*:\s?(.*)$")


class ExtraError(ValueError):
    """Raised when Extra holds the same managed field more than once."""


def _matches(line: str, name: str) -> bool:
    m = _FIELD_RE.match(line)
    return bool(m) and m.group(1).casefold() == name.casefold()


def get(extra: str | None, name: str) -> str | None:
    """Return the value of field ``name`` (case-insensitive), or None if absent.

    >>> get("Citation Key: madpu_Docket23150Order_2024", "citation key")
    'madpu_Docket23150Order_2024'
    """
    values = []
    for line in (extra or "").splitlines():
        m = _FIELD_RE.match(line)
        if m and m.group(1).casefold() == name.casefold():
            values.append(m.group(2).strip())
    if len(values) > 1:
        raise ExtraError(f"Extra has {len(values)} '{name}' lines: {values}")
    return values[0] if values else None


def set_field(extra: str | None, name: str, value: str | None) -> str:
    """Set (or, with ``value=None``, remove) field ``name``, keeping other lines in order.

    An existing line is replaced in place; a new one is appended.

    >>> set_field("arXiv: 1234\\ntex.shortauthor: DPU", "tex.shortauthor", "MA DPU")
    'arXiv: 1234\\ntex.shortauthor: MA DPU'
    """
    get(extra, name)  # raises on duplicated lines
    lines = (extra or "").splitlines()
    out: list[str] = []
    replaced = False
    for line in lines:
        if _matches(line, name):
            if value is not None:
                out.append(f"{name}: {value}")
            replaced = True
        else:
            out.append(line)
    if not replaced and value is not None:
        out.append(f"{name}: {value}")
    return "\n".join(out)


def remove_fields(text: str | None, names: tuple[str, ...]) -> str:
    """Drop every line holding one of ``names`` (used to clean CSL ``note``)."""
    return "\n".join(line for line in (text or "").splitlines() if not any(_matches(line, n) for n in names)).strip()
