"""Format library catalog text (Context / Contents / Why here) for Zotero's ``abstractNote`` field.

Ingest and ``just sources-backfill-catalog`` write this shape; pre-existing publisher abstracts are
preserved under an ``Abstract:`` tail. See ``context/code/source_metadata_conventions.md``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lib.sources.metadata import SourceMetadata

PENDING_CATALOG = "(pending catalog description)"

_LABEL_CONTEXT = "Context:"
_LABEL_CONTENTS = "Contents:"
_LABEL_WHY = "Why here:"
_PUBLISHER_PREFIX = "\n\nAbstract:"


def format_zotero_abstract(context: str, contents: str, why_here: str) -> str:
    """The catalog block only (no publisher tail). Blank lines separate sections for readability in Zotero."""
    return f"{_LABEL_CONTEXT} {context}\n\n{_LABEL_CONTENTS} {contents}\n\n{_LABEL_WHY} {why_here}"


def has_switchbox_layout(text: str) -> bool:
    """Whether ``text`` already uses the Context / Contents / Why here layout."""
    return text.strip().startswith(_LABEL_CONTEXT)


def publisher_tail(existing: str | None) -> str | None:
    """Publisher text to keep when replacing the catalog block.

    If ``existing`` is not our layout, the whole field is treated as publisher text. If it is our layout
    and has an ``Abstract:`` section, that section is returned; otherwise ``None``.
    """
    if not existing or not existing.strip():
        return None
    s = existing.strip()
    if not has_switchbox_layout(s):
        return s
    for sep in (_PUBLISHER_PREFIX, "\nAbstract:"):
        if sep in s:
            return s.split(sep, 1)[1].strip() or None
    return None


def merge_with_existing(existing: str | None, catalog_block: str) -> str:
    """Combine a new catalog block with any publisher tail from ``existing``."""
    publisher = publisher_tail(existing)
    if publisher:
        return f"{catalog_block}{_PUBLISHER_PREFIX} {publisher}"
    return catalog_block


def triple_for_card(meta: SourceMetadata) -> tuple[str, str, str]:
    """Catalog triple from the card's extract front matter, or the pending sentinel."""
    fm = meta.front_matter
    c, co, w = fm.get("context"), fm.get("contents"), fm.get("why_here")

    def one(value: object | None) -> str:
        if value is None or (isinstance(value, str) and not value.strip()):
            return PENDING_CATALOG
        return str(value).strip()

    if c or co or w:
        return one(c), one(co), one(w)
    return PENDING_CATALOG, PENDING_CATALOG, PENDING_CATALOG


def build_from_card(meta: SourceMetadata) -> str:
    """Zotero ``abstractNote`` for a details card (catalog block only)."""
    return format_zotero_abstract(*triple_for_card(meta))
