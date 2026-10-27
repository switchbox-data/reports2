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


def test_scope_and_key_sources() -> None:
    snap = _snap(
        [
            _item("A", ["RP"], citationKey="org_ATitle_2024"),
            _item("B", ["I"], extra="Citation Key: org_Pinned_2024", citationKey="org_Pinned_2024"),
            _item("C", ["O"], citationKey="org_Elsewhere_2024"),
            _item("D", ["RP", "I"]),
            _item("E", ["RP"], itemType="attachment"),
            _item("F", ["RP"], deleted=1, citationKey="org_Trash_2024"),
        ]
    )
    s = snapshot.summarize(snap)
    assert s.bibliographic == 4 and s.children == 1 and s.trashed == 1
    assert s.scope_counts == {"reports": 1, "inbox": 1, "neither": 1, "both": 1}
    assert s.key_sources == {"native": 1, "extra": 1, "none": 1}


def test_duplicates_pin_differs_and_empty() -> None:
    snap = _snap(
        [
            _item("A", ["RP"], citationKey="dup_X_2025a"),
            _item("B", ["RP"], citationKey="dup_X_2025a"),
            _item("C", ["O"], citationKey="dup_X_2025a"),
            _item("D", ["RP"], extra="Citation Key: eia_P_2025", citationKey="eia_P_2024"),
            _item("E", ["RP"], title="", creators=[], date="", citationKey="__c"),
        ]
    )
    s = snapshot.summarize(snap)
    assert s.duplicate_keys == {"dup_X_2025a": ["A", "B"]}
    assert s.pin_differs == [("D", "eia_P_2025", "eia_P_2024")]
    assert [r.item for r in s.empty] == ["E"]


def test_key_map_records_both_names_and_citations() -> None:
    snap = _snap(
        [
            _item("D", ["RP"], extra="Citation Key: eia_P_2025", citationKey="eia_P_2024"),
            _item("C", ["O"], citationKey="other_X_2024"),
        ]
    )
    rows = snapshot.key_map(snapshot.summarize(snap), cited={"eia_P_2024", "other_X_2024"})
    assert rows == [
        {
            "item": "D",
            "key": "eia_P_2025",
            "source": "extra",
            "old_keys": ["eia_P_2024", "eia_P_2025"],
            "scope": "reports",
            "cited": ["eia_P_2024"],
        }
    ]


def test_write_load_round_trip(tmp_path) -> None:
    snap = _snap([_item("A", ["RP"], title="Pérez \u2013 test")])
    path = snapshot.write(snap, tmp_path)
    assert path.name == "snapshot_v7.json"
    assert snapshot.load(path) == snap
    assert snapshot.s3_uri(snap) == "s3://data.sb/switchbox/zotero/snapshots/snapshot_v7_20261027.json"
