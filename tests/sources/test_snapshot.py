from __future__ import annotations

from typing import Any

from lib.sources import snapshot


def _col(key: str, name: str, parent: str | bool = False) -> dict[str, Any]:
    return {"key": key, "data": {"name": name, "parentCollection": parent}}


def _item(key: str, cols: list[str], **data: Any) -> dict[str, Any]:
    base = {"itemType": "report", "title": "A Title", "creators": [{"name": "Org"}], "date": "2024"}
    return {"key": key, "data": {**base, "collections": cols, **data}}


COLLECTIONS = [_col("R", "Reports"), _col("RP", "ct_hp_rates", "R"), _col("I", "Inbox"), _col("O", "Other")]


def _snap(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {"library_version": 7, "taken_at": "2026-10-27T17:00:00+00:00", "collections": COLLECTIONS, "items": items}


def test_write_load_round_trip(tmp_path) -> None:
    snap = _snap([_item("A", ["RP"], title="Pérez \u2013 test")])
    path = snapshot.write(snap, tmp_path)
    assert path.name == "snapshot_v7.json"
    assert snapshot.load(path) == snap
    assert snapshot.s3_uri(snap) == "s3://data.sb/switchbox/zotero/snapshots/snapshot_v7_20261027.json"
