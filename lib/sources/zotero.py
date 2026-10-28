"""Thin pyzotero wrapper for the Switchbox Zotero group library.

Credentials come from ``ZOTERO_API_KEY`` and ``ZOTERO_GROUP_ID`` in the repo's ``.env``
(or the environment). The key is never printed.

Reads (collections, items, bibliographic export) are at the top. Ingest's writes follow: they
create items and attachments, set the citation URL, pin public IDs in Extra, and move items into
project collections. Patches go through :mod:`lib.sources.zotero_write` (versioned, logged); every
write checks the library first, so re-running a step never duplicates an item or attachment.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import date
from functools import cache
from pathlib import Path
from typing import Any

from pyzotero import zotero
from rapidfuzz import fuzz

from lib.sources import env, extra, zotero_write

NON_BIB_TYPES = frozenset({"attachment", "note", "annotation"})
REPORTS = "Reports"
INBOX = "Inbox"
PROCESSED_TAG = "processed"
# Items added before this date are not "pending" until the backfill tags them (see sources_architecture.md).
PENDING_SINCE = "2026-10-28"
RAW_FILE_REASON = "file with no item"
# Extra lines that record where the public copies of an item live; ``bib`` keeps them out of the bibliography.
DOCUMENTCLOUD_ID = extra.DOCUMENTCLOUD_ID
DRIVE_ID = extra.DRIVE_ID
WAYBACK_URL = extra.WAYBACK_URL


@cache
def client() -> zotero.Zotero:
    """Zotero client for the group library, loading ``.env`` from the repo root."""
    env.require(*env.VARIABLES["zotero"])
    return zotero.Zotero(os.environ["ZOTERO_GROUP_ID"], "group", os.environ["ZOTERO_API_KEY"])


def library_version() -> int:
    """Current library version (``Last-Modified-Version``)."""
    return client().last_modified_version()


def collections() -> list[dict[str, Any]]:
    """Every collection in the library."""
    z = client()
    return z.everything(z.collections())


def collection_tree(name: str, all_collections: list[dict[str, Any]] | None = None) -> list[str]:
    """Keys of the top-level collection ``name`` and all its subcollections, recursively."""
    cols = all_collections if all_collections is not None else collections()
    roots = [c["key"] for c in cols if c["data"]["name"] == name and not c["data"]["parentCollection"]]
    if len(roots) != 1:
        raise RuntimeError(f"Expected one top-level collection named {name!r}, found {len(roots)}")
    children: dict[str, list[str]] = defaultdict(list)
    for c in cols:
        if c["data"]["parentCollection"]:
            children[c["data"]["parentCollection"]].append(c["key"])
    tree, stack = [], [roots[0]]
    while stack:
        key = stack.pop()
        tree.append(key)
        stack.extend(children.get(key, []))
    return tree


def items_in_collections(collection_keys: Iterable[str], include: str = "data,csljson") -> list[dict[str, Any]]:
    """Top-level items in the given collections, de-duplicated by item key, trash excluded."""
    z = client()
    items: dict[str, dict[str, Any]] = {}
    for key in collection_keys:
        for item in z.everything(z.collection_items_top(key, include=include)):
            if not item["data"].get("deleted"):
                items[item["key"]] = item
    return sorted(items.values(), key=lambda it: it["key"])


def bibliographic(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop standalone attachments and notes, which are not bibliography entries."""
    return [it for it in items if it["data"]["itemType"] not in NON_BIB_TYPES]


# --- the whole library, cached on disk ---------------------------------------------------------
# Dedupe, key-collision checks and organization lookup read every item. A cold fetch takes minutes,
# so the library is cached under SOURCES_CACHE_DIR and refreshed incrementally from its version.

_MEMORY: dict[str, dict[str, Any]] = {}


def _cache_file() -> Path:
    return env.cache_dir() / "zotero_items.json"


def invalidate() -> None:
    """Forget the in-memory library (call after any write)."""
    _MEMORY.clear()


def all_items(refresh: bool = False) -> list[dict[str, Any]]:
    """Every item (attachments and notes included, trash excluded), as ``data`` + metadata."""
    if refresh:
        invalidate()
    if "items" not in _MEMORY:
        path = _cache_file()
        cached = json.loads(path.read_text(encoding="utf-8")) if path.exists() and not refresh else None
        z = client()
        version = z.last_modified_version()
        if cached and cached["version"] == version:
            items = cached["items"]
        else:
            items = dict(cached["items"]) if cached else {}
            since = {"since": cached["version"]} if cached else {}
            for it in z.everything(z.items(include="data", **since)):
                items[it["key"]] = it
            if cached:
                for gone in z.deleted(since=cached["version"]).get("items", []):
                    items.pop(gone, None)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"version": version, "items": items}), encoding="utf-8")
        _MEMORY["items"] = {"items": items}
    return [it for it in _MEMORY["items"]["items"].values() if not it["data"].get("deleted")]


def bib_items() -> list[dict[str, Any]]:
    """All top-level bibliographic items in the library (not just Reports)."""
    return [it for it in all_items() if it["data"]["itemType"] not in NON_BIB_TYPES]


def get_item(item_key: str) -> dict[str, Any]:
    """One item, read fresh from the server (its ``version`` is what versioned writes check)."""
    return client().item(item_key)


def pinned_keys() -> dict[str, str]:
    """Every pinned citation key in the whole library -> Zotero item key (for collision checks)."""
    out: dict[str, str] = {}
    for it in bib_items():
        try:
            key = extra.get(it["data"].get("extra"), extra.CITATION_KEY)
        except extra.ExtraError:
            continue
        if key:
            out[key] = it["key"]
    return out


def find_by_pinned_key(citekey: str) -> dict[str, Any] | None:
    """The item whose ``Citation Key:`` line is ``citekey``, if any."""
    if item_key := pinned_keys().get(citekey):
        return get_item(item_key)
    return None


def children(item_key: str) -> list[dict[str, Any]]:
    """An item's child attachments and notes, read fresh."""
    return client().everything(client().children(item_key))


STORED_LINK_MODES = ("imported_file", "imported_url")


def is_raw_file(data: Mapping[str, Any]) -> bool:
    """Whether ``data`` is a stored file with no parent item (a PDF dragged into Zotero that got no item)."""
    return (
        data.get("itemType") == "attachment"
        and not data.get("parentItem")
        and data.get("linkMode") in STORED_LINK_MODES
        and not data.get("deleted")
    )


def adopt_raw_file(attachment_key: str, parent_key: str) -> None:
    """Move a raw file under ``parent_key``. Child items cannot be in collections, so its collections are cleared."""
    _patch(attachment_key, lambda _: {"parentItem": parent_key, "collections": []})


def _norm_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()


def _norm_doi(doi: str) -> str:
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", doi.strip(), flags=re.IGNORECASE).casefold()


@dataclass(frozen=True)
class Duplicate:
    """An existing Zotero item that may be the same source."""

    kind: str  # "md5", "url", "doi" or "title"
    item_key: str
    citekey: str | None
    title: str
    detail: str


def find_duplicates(
    md5: str | None = None,
    url: str | None = None,
    doi: str | None = None,
    title: str | None = None,
    items: list[dict[str, Any]] | None = None,
) -> list[Duplicate]:
    """Items that match by attachment md5, normalized URL, DOI or near-identical title.

    ``items`` defaults to the cached library; tests pass fixtures.
    """
    from lib.sources.webpage import normalize_url

    items = items if items is not None else all_items()
    by_key = {it["key"]: it for it in items}
    found: dict[tuple[str, str], Duplicate] = {}

    def add(kind: str, item: Mapping[str, Any], detail: str) -> None:
        top = by_key.get(item["data"].get("parentItem") or "", item)
        data = top["data"]
        if data["itemType"] in NON_BIB_TYPES:
            return
        found[(kind, top["key"])] = Duplicate(
            kind, top["key"], extra.get(data.get("extra"), extra.CITATION_KEY), data.get("title", ""), detail
        )

    want_url = normalize_url(url) if url else None
    want_title = _norm_title(title) if title else None
    for it in items:
        d = it["data"]
        if md5 and d["itemType"] == "attachment" and d.get("md5") == md5:
            add("md5", it, f"attachment {it['key']} has the same md5")
        if want_url and d.get("url") and normalize_url(d["url"]) == want_url:
            add("url", it, d["url"])
        if doi and d.get("DOI") and _norm_doi(d["DOI"]) == _norm_doi(doi):
            add("doi", it, d["DOI"])
        if (
            want_title
            and d["itemType"] not in NON_BIB_TYPES
            and d.get("title")
            and fuzz.ratio(_norm_title(d["title"]), want_title) >= 95
        ):
            add("title", it, d["title"])
    return sorted(found.values(), key=lambda m: (m.kind, m.item_key))


def web_link(item: Mapping[str, Any]) -> str:
    """The item's page in the Zotero web library."""
    href = (item.get("links") or {}).get("alternate", {}).get("href")
    return href or f"https://www.zotero.org/groups/{env.get('ZOTERO_GROUP_ID')}/items/{item['key']}"


def desktop_link(item_key: str) -> str:
    """A ``zotero://`` link that opens the item in the Zotero app."""
    return f"zotero://select/groups/{env.get('ZOTERO_GROUP_ID')}/items/{item_key}"


# --- writes -------------------------------------------------------------------------------------


def _patch(item_key: str, change: Callable[[Mapping[str, Any]], dict[str, Any]], retries: int = 1) -> dict[str, Any]:
    """Apply ``change(data) -> fields`` to a fresh read of the item; retry once on a 412 (edited since read)."""
    for attempt in range(retries + 1):
        item = get_item(item_key)
        fields = change(item["data"])
        try:
            zotero_write.patch_item(item, fields)
        except zotero_write.WriteError as e:
            if e.code == 412 and attempt < retries:
                continue
            raise
        invalidate()
        return get_item(item_key)
    raise AssertionError("unreachable")


def create_item(data: Mapping[str, Any], write_token: str | None = None) -> str:
    """Create a library item from Zotero-shaped ``data`` (with ``collections`` and Extra already set)."""
    key = zotero_write.create_item(data, write_token=write_token)
    invalidate()
    return key


def _file_md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def file_md5(path: Path) -> str:
    """md5 of a file, the hash Zotero keeps on stored attachments."""
    return _file_md5(Path(path))


def stored_attachments(item_key: str) -> list[dict[str, Any]]:
    """Child attachments whose file is stored in Zotero (the original document, and any snapshot)."""
    return [
        c
        for c in children(item_key)
        if c["data"]["itemType"] == "attachment" and c["data"].get("linkMode") in STORED_LINK_MODES
    ]


def attach_file(item_key: str, path: Path, title: str | None = None) -> str:
    """Upload ``path`` as a stored attachment of the item, unless one with the same md5 exists. Returns its key."""
    path = Path(path)
    want = _file_md5(path)
    for c in stored_attachments(item_key):
        if c["data"].get("md5") == want:
            return c["key"]
    result = client().attachment_both([(title or path.name, str(path))], parentid=item_key)
    invalidate()
    for bucket in ("success", "unchanged"):  # "unchanged": the file was already on the server, the item is new
        if result.get(bucket):
            made = result[bucket][0]
            version = made.get("version") or get_item(made["key"])["version"]
            zotero_write.log_created(made["key"], version, f"uploaded {path.name}")
            return made["key"]
    raise zotero_write.WriteError(f"Zotero did not accept the upload of {path.name}: {result.get('failure')}")


def attach_link(item_key: str, url: str, title: str) -> str:
    """Add a link attachment (public copy, Wayback capture) unless the item already has one for ``url``."""
    for c in children(item_key):
        if (
            c["data"]["itemType"] == "attachment"
            and c["data"].get("linkMode") == "linked_url"
            and c["data"].get("url") == url
        ):
            return c["key"]
    data = {
        "itemType": "attachment",
        "parentItem": item_key,
        "linkMode": "linked_url",
        "title": title,
        "url": url,
        "contentType": "",
        "tags": [],
        "relations": {},
    }
    key = zotero_write.create_item(data)
    invalidate()
    return key


def set_url(item_key: str, url: str) -> None:
    """Set the item's ``url`` field (a no-op when it already holds ``url``)."""
    _patch(item_key, lambda _data: {"url": url})


def set_extra_fields(item_key: str, fields: Mapping[str, str | None]) -> None:
    """Set (or, with ``None``, remove) lines in the item's Extra, keeping every other line."""

    def change(data: Mapping[str, Any]) -> dict[str, Any]:
        text = data.get("extra") or ""
        for name, value in fields.items():
            text = extra.set_field(text, name, value)
        return {"extra": text}

    _patch(item_key, change)


def mark_processed(item_key: str) -> None:
    """Tag the item ``processed`` (only after every ingest step is verified)."""

    def change(data: Mapping[str, Any]) -> dict[str, Any]:
        tags = list(data.get("tags") or [])
        if not any(t["tag"] == PROCESSED_TAG for t in tags):
            tags.append({"tag": PROCESSED_TAG})
        return {"tags": tags}

    _patch(item_key, change)


def is_processed(data: Mapping[str, Any]) -> bool:
    """Whether the item carries the ``processed`` tag."""
    return any(t["tag"] == PROCESSED_TAG for t in data.get("tags") or [])


def project_collections(cols: list[dict[str, Any]] | None = None) -> dict[str, str]:
    """Project name -> collection key, for the subcollections directly under Reports."""
    cols = cols if cols is not None else collections()
    roots = [c["key"] for c in cols if c["data"]["name"] == REPORTS and not c["data"]["parentCollection"]]
    if len(roots) != 1:
        raise RuntimeError(f"Expected one top-level {REPORTS!r} collection, found {len(roots)}")
    return {
        c["data"]["name"]: c["key"]
        for c in cols
        if c["data"]["parentCollection"] == roots[0] and c["data"]["name"] != INBOX
    }


def inbox_key(cols: list[dict[str, Any]] | None = None) -> str | None:
    """Key of the top-level Inbox collection, or ``None`` when it does not exist."""
    cols = cols if cols is not None else collections()
    keys = [c["key"] for c in cols if c["data"]["name"] == INBOX and not c["data"]["parentCollection"]]
    return keys[0] if keys else None


def add_to_projects(item_key: str, projects: Iterable[str]) -> None:
    """Put the item in each project subcollection of Reports, and take it out of the Inbox."""
    cols = collections()
    known = project_collections(cols)
    unknown = [p for p in projects if p not in known]
    if unknown:
        raise RuntimeError(f"No Reports subcollection named {', '.join(unknown)}; create it with ensure_project first")
    inbox = inbox_key(cols)

    def change(data: Mapping[str, Any]) -> dict[str, Any]:
        current = [c for c in data.get("collections") or [] if c != inbox]
        return {"collections": sorted({*current, *(known[p] for p in projects)})}

    _patch(item_key, change)


def update_from_card(item_key: str, data: Mapping[str, Any], project_keys: Iterable[str]) -> None:
    """Make an existing item (say, one added by hand to the Inbox) match the card's ``zotero_data``.

    Sets the card's fields, merges its ``Citation Key`` / ``tex.shortauthor`` lines into the item's Extra
    without touching other lines, and moves the item from the Inbox into the project subcollections.
    """
    inbox = inbox_key()
    card_extra = data.get("extra") or ""

    def change(current: Mapping[str, Any]) -> dict[str, Any]:
        fields = {k: v for k, v in data.items() if k not in ("extra", "collections", "tags", "relations")}
        text = current.get("extra") or ""
        for name in (extra.CITATION_KEY, extra.SHORTAUTHOR, extra.DOCKET):
            if value := extra.get(card_extra, name):
                text = extra.set_field(text, name, value)
        fields["extra"] = text
        kept = [c for c in current.get("collections") or [] if c != inbox]
        fields["collections"] = sorted({*kept, *project_keys})
        return fields

    _patch(item_key, change)


def create_project_collection(name: str) -> str:
    """Create ``Reports > <name>`` (or return the existing one's key)."""
    cols = collections()
    known = project_collections(cols)
    if name in known:
        return known[name]
    root = next(c["key"] for c in cols if c["data"]["name"] == REPORTS and not c["data"]["parentCollection"])
    result = client().create_collections([{"name": name, "parentCollection": root}])
    key = result["success"]["0"]
    zotero_write.log_event("collection_created", {"name": name, "key": key, "parent": root})
    return key


def download_attachment(item_key: str, dest_dir: Path) -> Path:
    """Download the item's original stored file (not a web snapshot) into ``dest_dir``; return its path.

    ``item_key`` may also be a stored file itself (such as a raw file with no item), which is then downloaded.
    """
    candidates = stored_attachments(item_key)
    if not candidates:
        own = get_item(item_key)
        stored = own["data"]["itemType"] == "attachment" and own["data"].get("linkMode") in STORED_LINK_MODES
        candidates = [own] if stored else []
    if not candidates:
        raise FileNotFoundError(f"Zotero item {item_key} has no stored file; attach the PDF in Zotero")

    def rank(c: Mapping[str, Any]) -> tuple[int, int]:
        d = c["data"]
        return (d.get("linkMode") != "imported_file", d.get("contentType") == "text/html")

    best = min(candidates, key=rank)
    name = best["data"].get("filename") or f"{item_key}.pdf"
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / name
    path.write_bytes(client().file(best["key"]))
    return path


@dataclass(frozen=True)
class PendingItem:
    """An item that still needs ingest: no pinned key, no ``processed`` tag, in the Inbox, or in no project."""

    key: str
    title: str
    author: str
    year: str
    reason: str
    projects: tuple[str, ...]

    def label(self) -> str:
        where = ", ".join(self.projects) or "no project"
        return f"{' '.join(filter(None, (self.author, self.year)))} ({where})"


def _first_author(data: Mapping[str, Any]) -> str:
    for c in data.get("creators") or []:
        return c.get("name") or c.get("lastName") or "Unknown"
    return "Unknown"


def _waits_for_ingest(data: Mapping[str, Any]) -> bool:
    """A top-level library entry that could need ingest: a bibliographic item, or a raw file with no item."""
    if data.get("deleted"):
        return False
    return data["itemType"] not in NON_BIB_TYPES or is_raw_file(data)


def _recent_items(z: zotero.Zotero, since: str, page: int = 25, max_pages: int = 8) -> list[dict[str, Any]]:
    """Bibliographic items and raw files added on or after ``since``, newest first, fetched a page at a time.

    One large page is much slower than several small ones, and most sessions need only the first.
    """
    out: list[dict[str, Any]] = []
    for n in range(max_pages):
        batch = z.top(limit=page, start=n * page, sort="dateAdded", direction="desc", include="data")
        out += [it for it in batch if _waits_for_ingest(it["data"]) and it["data"]["dateAdded"][:10] >= since]
        if len(batch) < page or batch[-1]["data"]["dateAdded"][:10] < since:
            break
    return out


def pending_items(since: str | None = None) -> list[PendingItem]:
    """Items waiting for ingest, found with a few API calls (fast enough for a session-start hook).

    1. Items under Reports added on or after ``since`` with no pinned key or no ``processed`` tag.
    2. Everything in the top-level Inbox.
    3. Recently added items that are in no Reports subcollection.

    Raw files (a PDF dragged in without an item) count wherever they are; ingest adopts them with ``--zotero-item``.
    """
    since = since or os.environ.get("SOURCES_PENDING_SINCE") or PENDING_SINCE
    z = client()
    cols = collections()
    projects = project_collections(cols)
    tree = set(collection_tree(REPORTS, cols))
    names = {key: name for name, key in projects.items()}
    inbox = inbox_key(cols)
    recent = _recent_items(z, since)
    pending: dict[str, PendingItem] = {}

    def add(it: Mapping[str, Any], reason: str) -> None:
        d = it["data"]
        raw = is_raw_file(d)
        pending.setdefault(
            it["key"],
            PendingItem(
                it["key"],
                d.get("title", ""),
                (d.get("filename") or d.get("title") or "file") if raw else _first_author(d),
                "" if raw else (d.get("date") or "")[:4] or "n.d.",
                RAW_FILE_REASON if raw else reason,
                tuple(sorted(names[c] for c in d.get("collections", []) if c in names)),
            ),
        )

    for it in recent:
        d = it["data"]
        if d["dateAdded"][:10] < since:
            continue
        cols_of = set(d.get("collections") or [])
        if inbox and inbox in cols_of:
            continue  # reported below
        if is_raw_file(d):
            add(it, RAW_FILE_REASON)
        elif cols_of & tree:
            pinned = extra.get(d.get("extra"), extra.CITATION_KEY)
            if not pinned:
                add(it, "no citation key")
            elif not is_processed(d):
                add(it, "not marked processed")
        else:
            add(it, "not in any project")
    if inbox:
        for it in z.everything(z.collection_items_top(inbox, include="data")):
            if _waits_for_ingest(it["data"]):
                add(it, "in Inbox")
    return sorted(pending.values(), key=lambda p: p.key)


def today() -> str:
    """Today's date (ISO), used for ``validated`` and ``accessDate``."""
    return date.today().isoformat()
