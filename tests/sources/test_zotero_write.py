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


def _plan(action: str = "update", **after: Any) -> dict[str, Any]:
    return {"item": "AAAA1111", "action": action, "key": "org_NewTitle_2020", "after": {**BEFORE, **after}}


def test_changes_sends_only_changed_fields_and_pins_the_key() -> None:
    got = zotero_write.changes(_plan(title="New Title"), BEFORE)
    assert got == {"title": "New Title", "extra": "Citation Key: org_NewTitle_2020", "citationKey": ""}


def test_changes_trashes_duplicates() -> None:
    assert zotero_write.changes(_plan("duplicate"), BEFORE) == {"deleted": 1}


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


def test_entries_from_plan_skips_no_ops_and_trashes_last() -> None:
    snap = {
        "items": [
            {"key": "AAAA1111", "version": 7, "data": BEFORE},
            {"key": "BBBB2222", "version": 3, "data": {**BEFORE, "key": "BBBB2222"}},
        ]
    }
    plans = [
        {**_plan("duplicate"), "item": "AAAA1111"},
        {**_plan(), "item": "BBBB2222", "key": "", "after": {**BEFORE, "key": "BBBB2222", "citationKey": ""}},
    ]
    got = zotero_write.entries_from_plan(plans, snap)
    assert [e["item"] for e in got] == ["BBBB2222", "AAAA1111"]
    assert got[1]["fields"] == {"deleted": 1} and got[1]["version"] == 7
