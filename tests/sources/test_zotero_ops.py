"""zotero.py's write helpers against a fake client: retries, idempotent attachments, collections, pending items."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from lib.sources import extra, zotero, zotero_write
from tests.sources.test_zotero_write import Server


class FakeClient:
    """Just enough of pyzotero for ``zotero.py``: items, children, uploads, collections."""

    def __init__(self, server: Server, children=None, collections=None, top=None, inbox_items=None):
        self.server, self._children = server, children or {}
        self._collections, self._top, self._inbox_items = collections or [], top or [], inbox_items or []
        self.uploaded, self.created_collections = [], []

    def item(self, key):
        it = self.server.items[key]
        return {"key": key, "version": it["version"], "data": it["data"]}

    def children(self, key):
        return self._children.get(key, [])

    def everything(self, result):
        return result

    def attachment_both(self, files, parentid=None):
        self.uploaded.append((files, parentid))
        return {"success": [{"key": "ATT_NEW", "version": 7}], "unchanged": [], "failure": []}

    def collections(self):
        return self._collections

    def create_collections(self, payload):
        self.created_collections.append(payload)
        return {"success": {"0": "COL_NEW"}}

    def top(self, **kw):
        start = kw.get("start", 0)
        return self._top[start : start + kw.get("limit", 100)]

    def collection_items_top(self, key, **kw):
        return self._inbox_items

    def last_modified_version(self):
        return 99


@pytest.fixture
def fake(monkeypatch, tmp_path):
    monkeypatch.setenv("SOURCES_CACHE_DIR", str(tmp_path / "cache"))
    server = Server(
        {
            "K1": {
                "version": 5,
                "data": {"title": "T", "extra": "", "tags": [], "collections": ["INBOX"], "itemType": "document"},
            }
        }
    )
    client = FakeClient(server)
    monkeypatch.setattr(zotero, "client", lambda: client)
    monkeypatch.setattr(zotero_write, "web_post", lambda write_token=None: server)
    monkeypatch.setattr(zotero_write, "log_path", lambda: tmp_path / "w.jsonl")
    return SimpleNamespace(server=server, client=client)


def test_patch_retries_once_after_a_412(fake):
    attempts = []
    real_item = fake.client.item

    def item_then_bump(key):
        got = real_item(key)
        if not attempts:  # someone edits the item between our read and our write
            fake.server.items[key]["version"] += 3
        attempts.append(1)
        return got

    fake.client.item = item_then_bump
    zotero.set_url("K1", "https://pub.switch.box/k")
    assert len(attempts) >= 2 and fake.server.items["K1"]["data"]["url"] == "https://pub.switch.box/k"


def test_set_extra_fields_preserves_other_lines(fake):
    fake.server.items["K1"]["data"]["extra"] = "Citation Key: k_A_2025\nfree text\ntex.shortauthor: MA DPU"
    zotero.set_extra_fields("K1", {zotero.DOCUMENTCLOUD_ID: "42"})
    text = fake.server.items["K1"]["data"]["extra"]
    assert text.splitlines() == [
        "Citation Key: k_A_2025",
        "free text",
        "tex.shortauthor: MA DPU",
        "DocumentCloud ID: 42",
    ]
    zotero.set_extra_fields("K1", {zotero.DOCUMENTCLOUD_ID: None})
    assert "DocumentCloud" not in fake.server.items["K1"]["data"]["extra"]


def test_mark_processed_is_idempotent(fake):
    zotero.mark_processed("K1")
    zotero.mark_processed("K1")
    assert fake.server.items["K1"]["data"]["tags"] == [{"tag": "processed"}] and len(fake.server.posts) == 1
    assert zotero.is_processed(fake.server.items["K1"]["data"])


def test_attach_file_skips_when_the_same_md5_is_already_stored(fake, tmp_path):
    pdf = tmp_path / "a.pdf"
    pdf.write_bytes(b"%PDF one")
    md5 = zotero.file_md5(pdf)
    fake.client._children["K1"] = [
        {"key": "ATT1", "data": {"itemType": "attachment", "linkMode": "imported_file", "md5": md5}}
    ]
    assert zotero.attach_file("K1", pdf) == "ATT1" and fake.client.uploaded == []
    other = tmp_path / "b.pdf"
    other.write_bytes(b"%PDF two")
    assert zotero.attach_file("K1", other) == "ATT_NEW" and fake.client.uploaded[0][1] == "K1"


def test_an_uploaded_attachment_is_logged_so_rollback_trashes_it(fake, tmp_path):
    pdf = tmp_path / "a.pdf"
    pdf.write_bytes(b"%PDF one")
    zotero.attach_file("K1", pdf)
    undo = zotero_write.entries_to_undo(tmp_path / "w.jsonl")
    assert undo == [{"item": "ATT_NEW", "version": 7, "fields": {"deleted": 1}, "restore": {"created": True}}]


def test_attach_link_skips_an_existing_url(fake):
    fake.client._children["K1"] = [
        {"key": "L1", "data": {"itemType": "attachment", "linkMode": "linked_url", "url": "https://x.org/a"}}
    ]
    assert zotero.attach_link("K1", "https://x.org/a", "Title") == "L1"
    assert fake.server.posts == []
    assert zotero.attach_link("K1", "https://x.org/b", "Title").startswith("NEW")
    created = fake.server.posts[-1][0]
    assert created["parentItem"] == "K1" and created["linkMode"] == "linked_url"


def collections_fixture(with_inbox=True):
    cols = [
        {"key": "REP", "data": {"name": "Reports", "parentCollection": False}},
        {"key": "MA", "data": {"name": "ma_hp_rates", "parentCollection": "REP"}},
        {"key": "GEN", "data": {"name": "Heat pumps", "parentCollection": False}},
    ]
    if with_inbox:
        cols.append({"key": "INBOX", "data": {"name": "Inbox", "parentCollection": False}})
    return cols


def test_add_to_projects_moves_the_item_out_of_the_inbox(fake):
    fake.client._collections = collections_fixture()
    zotero.add_to_projects("K1", ["ma_hp_rates"])
    assert fake.server.items["K1"]["data"]["collections"] == ["MA"]
    with pytest.raises(RuntimeError, match="No Reports subcollection"):
        zotero.add_to_projects("K1", ["nj_hp_rates"])


def test_update_from_card_merges_extra_and_moves_collections(fake):
    fake.client._collections = collections_fixture()
    fake.server.items["K1"]["data"]["extra"] = "free text"
    zotero.update_from_card(
        "K1",
        {"title": "Docket 1: T", "extra": "Citation Key: k_A_2025\ntex.shortauthor: MA DPU", "itemType": "document"},
        ["MA"],
    )
    data = fake.server.items["K1"]["data"]
    assert data["title"] == "Docket 1: T" and data["collections"] == ["MA"]
    assert extra.get(data["extra"], extra.CITATION_KEY) == "k_A_2025" and "free text" in data["extra"]


def test_missing_inbox_is_none_not_an_error(fake):
    fake.client._collections = collections_fixture(with_inbox=False)
    assert zotero.inbox_key() is None
    assert set(zotero.project_collections()) == {"ma_hp_rates"}


def test_inbox_under_reports_is_not_a_project(fake):
    cols = [
        *collections_fixture(with_inbox=False),
        {"key": "INB2", "data": {"name": "Inbox", "parentCollection": "REP"}},
    ]
    fake.client._collections = cols
    assert set(zotero.project_collections()) == {"ma_hp_rates"}


def test_create_project_collection_is_idempotent_and_logged(fake, tmp_path):
    fake.client._collections = collections_fixture()
    assert zotero.create_project_collection("ma_hp_rates") == "MA"
    assert fake.client.created_collections == []
    assert zotero.create_project_collection("nj_hp_rates") == "COL_NEW"
    assert fake.client.created_collections == [[{"name": "nj_hp_rates", "parentCollection": "REP"}]]
    assert "collection_created" in (tmp_path / "w.jsonl").read_text()


def top_item(key, added, **data):
    return {
        "key": key,
        "data": {
            "itemType": "document",
            "title": key,
            "dateAdded": added,
            "extra": "",
            "tags": [],
            "collections": [],
            "creators": [{"name": "Org"}],
            **data,
        },
    }


def test_pending_items_reports_each_reason_and_ignores_old_items(fake):
    fake.client._collections = collections_fixture()
    fake.client._top = [
        top_item("NOKEY", "2026-10-28T09:00:00Z", collections=["MA"]),
        top_item("UNTAGGED", "2026-10-28T08:00:00Z", collections=["MA"], extra="Citation Key: k_A_2025"),
        top_item(
            "DONE",
            "2026-10-28T07:00:00Z",
            collections=["MA"],
            extra="Citation Key: k_B_2025",
            tags=[{"tag": "processed"}],
        ),
        top_item("UNFILED", "2026-10-28T06:00:00Z", collections=[]),
        top_item("GENERAL", "2026-10-28T05:00:00Z", collections=["GEN"]),
        top_item("OLD", "2026-09-01T00:00:00Z", collections=["MA"]),
    ]
    fake.client._inbox_items = [top_item("INBOXED", "2026-08-01T00:00:00Z", collections=["INBOX"])]
    pending = {p.key: p.reason for p in zotero.pending_items(since="2026-10-28")}
    assert pending == {
        "NOKEY": "no citation key",
        "UNTAGGED": "not marked processed",
        "INBOXED": "in Inbox",
    }


def raw_file(key, added, **data):
    return {
        "key": key,
        "data": {
            "itemType": "attachment",
            "linkMode": "imported_file",
            "title": f"{key}.pdf",
            "filename": f"{key}.pdf",
            "dateAdded": added,
            "tags": [],
            "collections": [],
            **data,
        },
    }


def test_pending_items_include_raw_files_in_reports_and_the_inbox_only(fake):
    fake.client._collections = collections_fixture()
    fake.client._top = [
        raw_file("RAW_PROJECT", "2026-10-28T09:00:00Z", collections=["MA"]),
        raw_file("RAW_UNFILED", "2026-10-28T08:00:00Z"),
        raw_file("RAW_GENERAL", "2026-10-28T08:00:00Z", collections=["GEN"]),
        raw_file("LINK", "2026-10-28T07:00:00Z", linkMode="linked_url", collections=["MA"]),
        top_item("NOTE", "2026-10-28T06:00:00Z", itemType="note", collections=["MA"]),
    ]
    fake.client._inbox_items = [raw_file("RAW_INBOX", "2026-08-01T00:00:00Z", collections=["INBOX"])]
    pending = {p.key: p for p in zotero.pending_items(since="2026-10-28")}
    assert {k: p.reason for k, p in pending.items()} == {
        "RAW_PROJECT": "file with no item",
        "RAW_INBOX": "file with no item",
    }
    assert pending["RAW_PROJECT"].author == "RAW_PROJECT.pdf"
    assert pending["RAW_PROJECT"].projects == ("ma_hp_rates",)


def test_pending_items_without_an_inbox_does_not_crash(fake):
    fake.client._collections = collections_fixture(with_inbox=False)
    fake.client._top = []
    assert zotero.pending_items(since="2026-10-28") == []


def test_recent_items_fetch_in_small_pages_and_stop_early(fake):
    fake.client._top = [top_item(f"I{i}", f"2026-10-{28 - i // 10:02d}T00:00:00Z") for i in range(60)]
    items = zotero._recent_items(fake.client, "2026-10-28", page=25)
    assert {i["key"] for i in items} == {f"I{i}" for i in range(10)}


def test_download_prefers_the_original_over_a_snapshot(fake, tmp_path):
    fake.client._children["K1"] = [
        {
            "key": "SNAP",
            "data": {
                "itemType": "attachment",
                "linkMode": "imported_url",
                "contentType": "text/html",
                "filename": "page.html",
            },
        },
        {
            "key": "PDF",
            "data": {
                "itemType": "attachment",
                "linkMode": "imported_file",
                "contentType": "application/pdf",
                "filename": "order.pdf",
            },
        },
    ]
    fake.client.file = lambda key: b"%PDF original" if key == "PDF" else b"<html>"
    path = zotero.download_attachment("K1", tmp_path / "out")
    assert path.name == "order.pdf" and path.read_bytes() == b"%PDF original"


def test_download_without_a_stored_file_explains(fake, tmp_path):
    with pytest.raises(FileNotFoundError, match="attach the PDF in Zotero"):
        zotero.download_attachment("K1", tmp_path)


def test_duplicates_find_attachment_md5_url_and_title():
    items = [
        {
            "key": "P",
            "data": {
                "itemType": "document",
                "title": "Order on Rates",
                "url": "https://x.org/o.pdf",
                "extra": "Citation Key: k_A_2025",
            },
        },
        {"key": "A", "data": {"itemType": "attachment", "parentItem": "P", "md5": "abc"}},
    ]
    assert [(d.kind, d.item_key) for d in zotero.find_duplicates(md5="abc", items=items)] == [("md5", "P")]
    assert [d.kind for d in zotero.find_duplicates(url="http://X.org/o.pdf/", items=items)] == ["url"]
    assert [d.kind for d in zotero.find_duplicates(title="Order on rates", items=items)] == ["title"]
    assert zotero.find_duplicates(md5="nope", items=items) == []
