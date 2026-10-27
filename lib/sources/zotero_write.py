"""Versioned batch writes to the Zotero group library, with a log that makes them resumable and reversible.

For bulk edits (a cleanup pass, creating items in bulk): take a ``snapshot`` first, build one
:func:`entry` per item, preview, then :func:`write`. ``just zotero-rollback`` undoes a log.

Every object sent carries the item's ``version`` as read, so Zotero rejects (412) any
item edited since then instead of overwriting the edit. Batch ``POST`` has ``PATCH`` semantics:
only the fields sent change. Each item's outcome goes to a JSONL log as soon as its batch
returns, with the fields written and their previous values, so a rerun skips finished items and
a rollback puts back exactly what was changed.
"""

from __future__ import annotations

import json
import os
import time
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from lib.sources import zotero as zotero_client

API = "https://api.zotero.org"
BATCH = 50  # the API's maximum objects per write request

Post = Callable[[list[dict[str, Any]]], dict[str, Any]]


def entry(item: Mapping[str, Any], after: Mapping[str, Any] | None) -> dict[str, Any] | None:
    """One write for ``item`` (as read from Zotero or a snapshot): its new ``data``, or ``None`` to trash it.

    Only changed fields are sent. Returns ``None`` when nothing changes.
    """
    before = item["data"]
    if after is None:
        fields: dict[str, Any] = {"deleted": 1}
    else:
        fields = {f: v for f, v in after.items() if f not in ("key", "version") and before.get(f) != v}
    if not fields:
        return None
    return {"item": item["key"], "version": item["version"], "fields": fields, "restore": restore(fields, before)}


def restore(fields: Mapping[str, Any], before: Mapping[str, Any]) -> dict[str, Any]:
    """The previous values of ``fields``, to undo a write."""
    out: dict[str, Any] = {}
    for f, v in fields.items():
        if f == "deleted":
            out[f] = 1 if before.get("deleted") else 0
        elif f in before:
            out[f] = before[f]
        else:
            out[f] = [] if isinstance(v, list) else ""
    return out


def web_post() -> Post:
    """A poster for the group library's ``/items`` endpoint."""
    zotero_client.client()  # loads .env and checks the credentials are set
    url = f"{API}/groups/{os.environ['ZOTERO_GROUP_ID']}/items"
    headers = {
        "Zotero-API-Key": os.environ["ZOTERO_API_KEY"],
        "Zotero-API-Version": "3",
        "Content-Type": "application/json",
    }

    def post(objects: list[dict[str, Any]]) -> dict[str, Any]:
        for attempt in range(5):
            r = requests.post(url, headers=headers, data=json.dumps(objects), timeout=60)
            if r.status_code in (429, 503) or r.status_code >= 500:
                time.sleep(int(r.headers.get("Retry-After", 5 * (attempt + 1))))
                continue
            if wait := r.headers.get("Backoff"):
                time.sleep(int(wait))
            r.raise_for_status()
            return r.json()
        raise RuntimeError(f"Zotero kept refusing the write ({r.status_code})")

    return post


def current_versions(keys: Sequence[str]) -> dict[str, int]:
    """Each item's version on the server now."""
    z = zotero_client.client()
    out: dict[str, int] = {}
    for start in range(0, len(keys), BATCH):
        out |= z.items(itemKey=",".join(keys[start : start + BATCH]), format="versions", includeTrashed=1)
    return out


def mismatches(entries: Sequence[Mapping[str, Any]]) -> list[tuple[str, str]]:
    """(item, field) pairs where the server's data differs from what ``entries`` wrote."""
    z = zotero_client.client()
    keys = [e["item"] for e in entries]
    server: dict[str, dict[str, Any]] = {}
    for start in range(0, len(keys), BATCH):
        for it in z.items(itemKey=",".join(keys[start : start + BATCH]), includeTrashed=1):
            server[it["key"]] = it["data"]
    out = []
    for e in entries:
        data = server.get(e["item"])
        if data is None:
            out.append((e["item"], "(missing)"))
            continue
        for f, v in e["fields"].items():
            got = bool(data.get("deleted")) if f == "deleted" else data.get(f, [] if isinstance(v, list) else "")
            if (bool(v) if f == "deleted" else v) != got:
                out.append((e["item"], f))
    return out


def done_items(path_log: Path) -> set[str]:
    """Items the log records as written (or unchanged), so a rerun skips them."""
    if not path_log.exists():
        return set()
    with path_log.open(encoding="utf-8") as f:
        return {e["item"] for line in f if (e := json.loads(line))["status"] in ("successful", "unchanged")}


def write(
    entries: Sequence[Mapping[str, Any]],
    path_log: Path,
    post: Post,
    on_batch: Callable[[int, Counter], None] | None = None,
) -> dict[str, int]:
    """Send ``entries`` (``item``, ``version``, ``fields``, ``restore``) in batches and log each outcome.

    Returns counts by status. Items already in the log as written are skipped.
    """
    skip = done_items(path_log)
    todo = [e for e in entries if e["item"] not in skip]
    counts: Counter = Counter(skipped=len(entries) - len(todo))
    path_log.parent.mkdir(parents=True, exist_ok=True)
    with path_log.open("a", encoding="utf-8") as log:
        for start in range(0, len(todo), BATCH):
            batch = todo[start : start + BATCH]
            result = post([{"key": e["item"], "version": e["version"], **e["fields"]} for e in batch])
            new_version = None
            for i, e in enumerate(batch):
                status, detail = _outcome(result, i)
                if status == "successful":
                    new_version = (result["successful"][str(i)] or {}).get("version")
                counts[status] += 1
                log.write(
                    json.dumps(
                        {
                            "at": datetime.now(UTC).isoformat(timespec="seconds"),
                            "item": e["item"],
                            "status": status,
                            "detail": detail,
                            "version_before": e["version"],
                            "version_after": new_version if status == "successful" else None,
                            "fields": e["fields"],
                            "restore": e["restore"],
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
            log.flush()
            if on_batch:
                on_batch(start + len(batch), counts)
    return dict(counts)


def _outcome(result: Mapping[str, Any], i: int) -> tuple[str, str]:
    for status in ("successful", "unchanged", "failed"):
        if str(i) in result.get(status, {}):
            v = result[status][str(i)]
            return status, json.dumps(v)[:300] if status == "failed" else ""
    return "failed", "not in the response"


def entries_to_undo(path_log: Path) -> list[dict[str, Any]]:
    """Rollback writes for every item the log records as written, at its post-write version."""
    latest: dict[str, dict[str, Any]] = {}
    with path_log.open(encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            if e["status"] == "successful":
                latest[e["item"]] = e
    return [
        {"item": e["item"], "version": e["version_after"], "fields": e["restore"], "restore": e["fields"]}
        for e in latest.values()
    ]
