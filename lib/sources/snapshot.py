"""Whole-library Zotero snapshot: the backup taken before any cleanup write, and the current-key map.

A snapshot holds every item in the group library (top-level items, attachments and notes, with
``data`` and ``csljson``), the collection tree and the library version it was read at. It is what
``orgs-rollback`` restores from, so it is taken before anything else in the cleanup and copied to S3.
"""

from __future__ import annotations

import datetime as dt
import json
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lib.sources import bib, citekeys, zotero

S3_PREFIX = "s3://data.sb/switchbox/zotero/snapshots/"
REPORTS = "Reports"
INBOX = "Inbox"
MAX_ATTEMPTS = 3

Snapshot = dict[str, Any]


class LibraryChangedError(RuntimeError):
    """The library changed while the snapshot was being read."""


def default_work_dir(today: dt.date | None = None) -> Path:
    return Path.home() / ".cache" / "switchbox_sources" / "org_cleanup" / (today or dt.date.today()).strftime("%Y%m%d")


def fetch() -> Snapshot:
    """Read the whole library, retrying if someone edits it mid-read."""
    z = zotero.client()
    for _ in range(MAX_ATTEMPTS):
        version = zotero.library_version()
        cols = zotero.collections()
        items = z.everything(z.items(include="data,csljson"))
        if zotero.library_version() == version:
            return {
                "group_id": z.library_id,
                "library_version": version,
                "taken_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
                "collections": sorted(cols, key=lambda c: c["key"]),
                "items": sorted(items, key=lambda it: it["key"]),
            }
    raise LibraryChangedError(f"The library kept changing during {MAX_ATTEMPTS} attempts; ask for an edit freeze.")


def _tree(name: str, cols: list[dict[str, Any]]) -> set[str]:
    try:
        return set(zotero.collection_tree(name, cols))
    except RuntimeError:
        return set()


def current_key(data: Mapping[str, Any]) -> tuple[str | None, str]:
    """The key an item is cited by today, and where it lives: ``extra``, ``native`` or ``none``."""
    if pinned := bib.pinned_key(data):
        return pinned, "extra"
    if native := (data.get("citationKey") or "").strip():
        return native, "native"
    return None, "none"


def is_empty(data: Mapping[str, Any]) -> bool:
    """No title, creator or date: nothing a citation could be built from."""
    return not citekeys.item_title(data) and not data.get("creators") and not citekeys.item_date(data)


@dataclass
class KeyRow:
    item: str
    key: str | None
    source: str
    native: str | None
    scope: str
    item_type: str
    title: str | None


@dataclass
class Summary:
    library_version: int
    bibliographic: int
    children: int
    trashed: int
    scope_counts: Counter[str]
    key_sources: Counter[str]
    duplicate_keys: dict[str, list[str]]
    pin_differs: list[tuple[str, str, str]]
    empty: list[KeyRow]
    rows: list[KeyRow] = field(repr=False)


def summarize(snap: Snapshot) -> Summary:
    """Classify every bibliographic item by scope (Reports, Inbox, both, neither) and current key."""
    cols = snap["collections"]
    reports, inbox = _tree(REPORTS, cols), _tree(INBOX, cols)
    rows: list[KeyRow] = []
    empty: list[KeyRow] = []
    children = trashed = 0
    pin_differs: list[tuple[str, str, str]] = []
    for it in snap["items"]:
        data = it["data"]
        if data.get("deleted"):
            trashed += 1
            continue
        if data["itemType"] in zotero.NON_BIB_TYPES:
            children += 1
            continue
        in_cols = set(data.get("collections", []))
        in_reports, in_inbox = bool(in_cols & reports), bool(in_cols & inbox)
        scope = "both" if in_reports and in_inbox else "reports" if in_reports else "inbox" if in_inbox else "neither"
        key, source = current_key(data)
        native = (data.get("citationKey") or "").strip()
        if source == "extra" and native and native != key:
            pin_differs.append((it["key"], key or "", native))
        row = KeyRow(it["key"], key, source, native or None, scope, data["itemType"], citekeys.item_title(data))
        rows.append(row)
        if scope != "neither" and is_empty(data):
            empty.append(row)
    by_key: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        if r.key and r.scope != "neither":
            by_key[r.key].append(r.item)
    return Summary(
        library_version=snap["library_version"],
        bibliographic=len(rows),
        children=children,
        trashed=trashed,
        scope_counts=Counter(r.scope for r in rows),
        key_sources=Counter(r.source for r in rows if r.scope != "neither"),
        duplicate_keys={k: v for k, v in sorted(by_key.items()) if len(v) > 1},
        pin_differs=pin_differs,
        empty=empty,
        rows=rows,
    )


def key_map(summary: Summary, cited: Iterable[str]) -> list[dict[str, Any]]:
    """Today's key for every item in Reports or Inbox, plus any other name reports may cite it by.

    ``old_keys`` holds both the Extra pin and the native key when they differ, so the rename map
    covers citations of either.
    """
    cited_set = set(cited)
    rows = []
    for r in summary.rows:
        if r.scope == "neither":
            continue
        old = sorted({k for k in (r.key, r.native) if k})
        rows.append(
            {
                "item": r.item,
                "key": r.key,
                "source": r.source,
                "old_keys": old,
                "scope": r.scope,
                "cited": [k for k in old if k in cited_set],
            }
        )
    return rows


def write(snap: Snapshot, work_dir: Path) -> Path:
    work_dir.mkdir(parents=True, exist_ok=True)
    path = work_dir / f"snapshot_v{snap['library_version']}.json"
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(snap, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
    tmp.replace(path)
    return path


def s3_uri(snap: Snapshot) -> str:
    stamp = snap["taken_at"][:10].replace("-", "")
    return f"{S3_PREFIX}snapshot_v{snap['library_version']}_{stamp}.json"


def upload(path: Path, uri: str) -> None:
    import boto3

    bucket, key = uri.removeprefix("s3://").split("/", 1)
    boto3.client("s3").upload_file(str(path), bucket, key)


def load(path: Path) -> Snapshot:
    return json.loads(path.read_text(encoding="utf-8"))
