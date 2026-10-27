"""Whole-library Zotero snapshot: the backup to take before any bulk write.

A snapshot holds every item in the group library (top-level items, attachments and notes, with
``data`` and ``csljson``), the collection tree and the library version it was read at. ``just
zotero-snapshot`` writes it locally and copies it to S3; build bulk-write entries from it so each
write carries the version it was planned against.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from lib.sources import zotero

S3_PREFIX = "s3://data.sb/switchbox/zotero/snapshots/"
MAX_ATTEMPTS = 3

Snapshot = dict[str, Any]


class LibraryChangedError(RuntimeError):
    """The library changed while the snapshot was being read."""


def default_dir() -> Path:
    return Path.home() / ".cache" / "switchbox_sources" / "zotero_snapshots"


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
