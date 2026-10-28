"""Versioned writes to the Zotero group library, with a log that makes them resumable and reversible.

Every object sent carries the item's ``version`` as read, so Zotero rejects (412) any item edited
since then instead of overwriting the edit. Batch ``POST`` has ``PATCH`` semantics: only the fields
sent change. Each item's outcome goes to a JSONL log as soon as its batch returns, with the fields
written and their previous values, so a rollback (:func:`entries_to_undo`) puts back exactly what
was changed.

Ingest calls this one item at a time (:func:`patch_item`, :func:`create_item`); bulk edits can build
:func:`entry` objects and call :func:`write`, which skips items the log already records as written.
"""

from __future__ import annotations

import json
import time
import uuid
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from lib.sources import env

API = "https://api.zotero.org"
BATCH = 50  # the API's maximum objects per write request

Post = Callable[[list[dict[str, Any]]], dict[str, Any]]


class WriteError(RuntimeError):
    """Zotero rejected a write; ``code`` is the per-object HTTP status when the API gave one."""

    def __init__(self, message: str, code: int | None = None):
        super().__init__(message)
        self.code = code


def log_path() -> Path:
    """The default write log (``SOURCES_CACHE_DIR/logs/zotero_writes.jsonl``)."""
    return env.cache_dir() / "logs" / "zotero_writes.jsonl"


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


def web_post(write_token: str | None = None) -> Post:
    """A poster for the group library's ``/items`` endpoint.

    Retries 429 and 5xx responses after the server's ``Retry-After``. ``write_token`` makes a
    retried create idempotent: Zotero ignores a second request with the same token.
    """
    env.require(*env.VARIABLES["zotero"])
    url = f"{API}/groups/{env.get('ZOTERO_GROUP_ID')}/items"
    headers = {
        "Zotero-API-Key": env.get("ZOTERO_API_KEY") or "",
        "Zotero-API-Version": "3",
        "Content-Type": "application/json",
    }
    if write_token:
        headers["Zotero-Write-Token"] = write_token

    def post(objects: list[dict[str, Any]]) -> dict[str, Any]:
        r = None
        for attempt in range(5):
            r = requests.post(url, headers=headers, data=json.dumps(objects), timeout=60)
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(int(r.headers.get("Retry-After", 5 * (attempt + 1))))
                continue
            if wait := r.headers.get("Backoff"):
                time.sleep(int(wait))
            if r.status_code == 412 and write_token:
                raise WriteError("Zotero already accepted a create with this write token; look the item up", 412)
            r.raise_for_status()
            return r.json()
        raise WriteError(f"Zotero kept refusing the write ({r.status_code if r is not None else '?'})")

    return post


def mismatches(entries: Sequence[Mapping[str, Any]]) -> list[tuple[str, str]]:
    """(item, field) pairs where the server's data differs from what ``entries`` wrote."""
    from lib.sources import zotero as zotero_client  # zotero imports this module

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


def _record(log: Any, e: Mapping[str, Any], status: str, detail: str, version_after: int | None) -> None:
    log.write(
        json.dumps(
            {
                "at": datetime.now(UTC).isoformat(timespec="seconds"),
                "item": e["item"],
                "status": status,
                "detail": detail,
                "version_before": e["version"],
                "version_after": version_after,
                "fields": e["fields"],
                "restore": e["restore"],
            },
            ensure_ascii=False,
        )
        + "\n"
    )


def write(
    entries: Sequence[Mapping[str, Any]],
    path_log: Path,
    post: Post,
    on_batch: Callable[[int, Counter], None] | None = None,
    resume: bool = True,
) -> dict[str, int]:
    """Send ``entries`` (``item``, ``version``, ``fields``, ``restore``) in batches and log each outcome.

    Returns counts by status. With ``resume`` (bulk edits), items already in the log as written
    are skipped; ingest passes ``resume=False`` because it edits one item several times.
    """
    skip = done_items(path_log) if resume else set()
    todo = [e for e in entries if e["item"] not in skip]
    counts: Counter = Counter(skipped=len(entries) - len(todo))
    path_log.parent.mkdir(parents=True, exist_ok=True)
    with path_log.open("a", encoding="utf-8") as log:
        for start in range(0, len(todo), BATCH):
            batch = todo[start : start + BATCH]
            result = post([{"key": e["item"], "version": e["version"], **e["fields"]} for e in batch])
            for i, e in enumerate(batch):
                status, detail = _outcome(result, i)
                new_version = (result["successful"][str(i)] or {}).get("version") if status == "successful" else None
                counts[status] += 1
                _record(log, e, status, detail, new_version)
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


def patch_item(
    item: Mapping[str, Any],
    after: Mapping[str, Any],
    post: Post | None = None,
    path_log: Path | None = None,
) -> int:
    """Write ``after``'s changed fields to one item (as just read) and return its new version.

    Returns the item's current version when nothing changes. Raises :class:`WriteError` on a
    rejected write, with ``code`` 412 when the item was edited since it was read.
    """
    e = entry(item, after)
    if e is None:
        return int(item["version"])
    post = post or web_post()
    path_log = path_log or log_path()
    path_log.parent.mkdir(parents=True, exist_ok=True)
    result = post([{"key": e["item"], "version": e["version"], **e["fields"]}])
    status, detail = _outcome(result, 0)
    with path_log.open("a", encoding="utf-8") as log:
        _record(log, e, status, detail, (result.get("successful", {}).get("0") or {}).get("version"))
    if status == "failed":
        code = (result.get("failed", {}).get("0") or {}).get("code")
        raise WriteError(f"Zotero rejected the write to {e['item']}: {detail}", code)
    if status == "unchanged":
        return int(e["version"])
    return int(result["successful"]["0"]["version"])


def create_item(
    data: Mapping[str, Any],
    post: Post | None = None,
    path_log: Path | None = None,
    write_token: str | None = None,
) -> str:
    """Create one item from ``data`` (Zotero JSON without ``key``/``version``) and return its key."""
    post = post or web_post(write_token or uuid.uuid4().hex)
    path_log = path_log or log_path()
    path_log.parent.mkdir(parents=True, exist_ok=True)
    result = post([dict(data)])
    status, detail = _outcome(result, 0)
    if status != "successful":
        raise WriteError(
            f"Zotero rejected the new item: {detail}", (result.get("failed", {}).get("0") or {}).get("code")
        )
    created = result["successful"]["0"]
    key = created["key"]
    log_created(key, created.get("version"), path_log=path_log)
    return key


def log_created(key: str, version: int | None, detail: str = "created", path_log: Path | None = None) -> None:
    """Record a new item (one made here or by a file upload) so a rollback trashes it."""
    path_log = path_log or log_path()
    path_log.parent.mkdir(parents=True, exist_ok=True)
    with path_log.open("a", encoding="utf-8") as log:
        _record(
            log,
            {"item": key, "version": 0, "fields": {"created": True}, "restore": {"deleted": 1}},
            "successful",
            detail,
            version,
        )


def log_event(kind: str, detail: Mapping[str, Any], path_log: Path | None = None) -> None:
    """Append a non-item write (a collection created, say) to the log."""
    path_log = path_log or log_path()
    path_log.parent.mkdir(parents=True, exist_ok=True)
    line = {"at": datetime.now(UTC).isoformat(timespec="seconds"), "event": kind, "status": "event", **detail}
    with path_log.open("a", encoding="utf-8") as log:
        log.write(json.dumps(line, ensure_ascii=False) + "\n")
