"""Versioned single-item writes and the JSONL log that makes them reversible."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lib.sources import zotero_write


class Server:
    """A fake of Zotero's ``/items`` endpoint: PATCH semantics, version checks, write tokens."""

    def __init__(self, items: dict[str, dict]):
        self.items, self.version, self.posts = items, 10, []

    def __call__(self, objects):
        self.posts.append(objects)
        out = {"successful": {}, "unchanged": {}, "failed": {}}
        for i, obj in enumerate(objects):
            key = obj.get("key")
            if key is None:
                self.version += 1
                new = f"NEW{len(self.items) + 1}"
                self.items[new] = {"version": self.version, "data": dict(obj)}
                out["successful"][str(i)] = {"key": new, "version": self.version}
                continue
            item = self.items[key]
            if obj["version"] != item["version"]:
                out["failed"][str(i)] = {"code": 412, "message": "Item has been modified since specified version"}
                continue
            fields = {k: v for k, v in obj.items() if k not in ("key", "version")}
            if all(item["data"].get(k) == v for k, v in fields.items()):
                out["unchanged"][str(i)] = key
                continue
            item["data"].update(fields)
            self.version += 1
            item["version"] = self.version
            out["successful"][str(i)] = {"key": key, "version": self.version}
        return out


def item(key="K1", version=5, **data):
    return {"key": key, "version": version, "data": {"title": "Old", "extra": "", **data}}


def test_entry_sends_only_changed_fields_and_remembers_previous_values():
    e = zotero_write.entry(item(), {"title": "New", "extra": ""})
    assert e == {"item": "K1", "version": 5, "fields": {"title": "New"}, "restore": {"title": "Old"}}
    assert zotero_write.entry(item(), {"title": "Old"}) is None


def test_entry_restores_a_missing_field_to_empty():
    url_entry = zotero_write.entry(item(), {"url": "https://x.org"})
    tag_entry = zotero_write.entry(item(), {"tags": [{"tag": "processed"}]})
    assert url_entry is not None and url_entry["restore"] == {"url": ""}
    assert tag_entry is not None and tag_entry["restore"] == {"tags": []}


def test_patch_returns_the_new_version_and_logs(tmp_path):
    server = Server({"K1": item()})
    log = tmp_path / "w.jsonl"
    version = zotero_write.patch_item(server.items["K1"] | {"key": "K1"}, {"title": "New"}, post=server, path_log=log)
    assert version == 11 and server.items["K1"]["data"]["title"] == "New"
    entry = json.loads(log.read_text().splitlines()[0])
    assert entry["status"] == "successful" and entry["version_before"] == 5 and entry["version_after"] == 11
    assert entry["restore"] == {"title": "Old"}


def test_unchanged_item_makes_no_request(tmp_path):
    server = Server({"K1": item()})
    assert (
        zotero_write.patch_item(
            {"key": "K1", **server.items["K1"]}, {"title": "Old"}, post=server, path_log=tmp_path / "w.jsonl"
        )
        == 5
    )
    assert server.posts == []


def test_a_stale_version_is_rejected_with_code_412(tmp_path):
    server = Server({"K1": item(version=9)})
    stale = {"key": "K1", "version": 5, "data": {"title": "Old", "extra": ""}}
    with pytest.raises(zotero_write.WriteError) as e:
        zotero_write.patch_item(stale, {"title": "Mine"}, post=server, path_log=tmp_path / "w.jsonl")
    assert e.value.code == 412
    assert server.items["K1"]["data"]["title"] == "Old"  # the other edit was not overwritten


def test_create_returns_the_key_and_logs_a_creation(tmp_path):
    server = Server({})
    key = zotero_write.create_item({"itemType": "document", "title": "T"}, post=server, path_log=tmp_path / "w.jsonl")
    assert key == "NEW1"
    assert json.loads((tmp_path / "w.jsonl").read_text())["detail"] == "created"


def test_create_failure_raises(tmp_path):
    with pytest.raises(zotero_write.WriteError, match="rejected the new item"):
        zotero_write.create_item(
            {"itemType": "nope"},
            post=lambda objs: {"failed": {"0": {"code": 400, "message": "bad"}}},
            path_log=tmp_path / "w.jsonl",
        )


def test_log_can_be_reversed(tmp_path):
    server = Server({"K1": item()})
    log = tmp_path / "w.jsonl"
    current = {"key": "K1", **server.items["K1"]}
    zotero_write.patch_item(current, {"title": "Second"}, post=server, path_log=log)
    current = {"key": "K1", **server.items["K1"]}
    zotero_write.patch_item(current, {"title": "Third"}, post=server, path_log=log)
    undo = zotero_write.entries_to_undo(log)
    assert (
        len(undo) == 1
        and undo[0]["fields"] == {"title": "Second"}
        and undo[0]["version"] == server.items["K1"]["version"]
    )


def test_log_event_is_appended(tmp_path):
    log = tmp_path / "w.jsonl"
    zotero_write.log_event("collection_created", {"name": "nj_hp_rates", "key": "C1"}, path_log=log)
    line = json.loads(log.read_text())
    assert line["event"] == "collection_created" and line["name"] == "nj_hp_rates"


def test_done_items_skip_only_written_ones(tmp_path):
    log = Path(tmp_path / "w.jsonl")
    log.write_text(
        json.dumps({"item": "A", "status": "successful"}) + "\n" + json.dumps({"item": "B", "status": "failed"}) + "\n"
    )
    assert zotero_write.done_items(log) == {"A"}
