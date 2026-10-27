import json
from pathlib import Path
from typing import Any

from lib.sources import zotero_write

BEFORE = {
    "key": "AAAA1111",
    "version": 7,
    "itemType": "report",
    "title": "OLD TITLE",
    "extra": "",
    "citationKey": "old_Key_2020",
    "creators": [{"creatorType": "author", "name": "Org"}],
}


ITEM = {"key": "AAAA1111", "version": 7, "data": BEFORE}


def test_entry_sends_only_changed_fields() -> None:
    got = zotero_write.entry(ITEM, {**BEFORE, "title": "New Title", "citationKey": ""})
    assert got == {
        "item": "AAAA1111",
        "version": 7,
        "fields": {"title": "New Title", "citationKey": ""},
        "restore": {"title": "OLD TITLE", "citationKey": "old_Key_2020"},
    }


def test_entry_trashes_on_none_and_skips_no_ops() -> None:
    trash = zotero_write.entry(ITEM, None)
    assert trash is not None and trash["fields"] == {"deleted": 1}
    assert zotero_write.entry(ITEM, dict(BEFORE)) is None


def test_restore_gives_snapshot_values() -> None:
    fields = {"title": "New Title", "deleted": 1, "publisher": "X"}
    assert zotero_write.restore(fields, BEFORE) == {"title": "OLD TITLE", "deleted": 0, "publisher": ""}


def _fake_post(fail: set[str], sent: list[list[dict[str, Any]]]) -> zotero_write.Post:
    def post(objects: list[dict[str, Any]]) -> dict[str, Any]:
        sent.append(objects)
        out: dict[str, Any] = {"successful": {}, "unchanged": {}, "failed": {}}
        for i, o in enumerate(objects):
            if o["key"] in fail:
                out["failed"][str(i)] = {"key": o["key"], "code": 412, "message": "Item has been modified"}
            else:
                out["successful"][str(i)] = {"key": o["key"], "version": o["version"] + 1}
        return out

    return post


def test_write_logs_outcomes_resumes_and_rolls_back(tmp_path: Path) -> None:
    entries = [
        {"item": f"K{i:07d}", "version": 10, "fields": {"title": f"T{i}"}, "restore": {"title": "old"}}
        for i in range(60)
    ]
    log = tmp_path / "log.jsonl"
    sent: list[list[dict[str, Any]]] = []
    counts = zotero_write.write(entries, log, _fake_post({"K0000003"}, sent))
    assert counts == {"skipped": 0, "successful": 59, "failed": 1}
    assert [len(b) for b in sent] == [50, 10]
    assert sent[0][0] == {"key": "K0000000", "version": 10, "title": "T0"}

    sent.clear()
    again = zotero_write.write(entries, log, _fake_post(set(), sent))
    assert again == {"skipped": 59, "successful": 1}
    assert [o["key"] for b in sent for o in b] == ["K0000003"]

    undo = zotero_write.entries_to_undo(log)
    assert len(undo) == 60
    assert undo[0] == {"item": "K0000000", "version": 11, "fields": {"title": "old"}, "restore": {"title": "T0"}}
    assert all(json.loads(line)["restore"] == {"title": "old"} for line in log.open())
