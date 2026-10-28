"""Ingest is rerunnable at every failure point: the second run finishes the job and duplicates nothing."""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.sources import extra, frontmatter, ingest, metadata, shortlinks, zotero
from tests.sources.conftest import World, make_card, remote_commits, remote_links, use_repo_env


@pytest.fixture(autouse=True)
def _repo_env(monkeypatch: pytest.MonkeyPatch, repo: Path) -> None:
    use_repo_env(monkeypatch, repo)


def run(world: World, repo: Path, card: metadata.SourceMetadata, pdf: Path | None, **kw) -> ingest.IngestReport:
    return ingest.ingest(card, source=pdf, repo_root=repo, **kw)


def statuses(report: ingest.IngestReport) -> dict[str, str]:
    return {s.name: s.status for s in report.steps}


def only_item(world: World) -> dict:
    assert len(world.items) == 1, f"expected one Zotero item, found {len(world.items)}"
    return next(iter(world.items.values()))


def test_full_ingest(world, repo, pdf_file, extract_file, pub_remote, tmp_path):
    card = make_card()
    report = run(world, repo, card, pdf_file)
    assert report.ok, report.to_dict()
    assert report.processed
    item = only_item(world)
    data = item["data"]
    assert extra.get(data["extra"], extra.CITATION_KEY) == card.citekey
    assert extra.get(data["extra"], extra.SHORTAUTHOR) == "MA DPU"
    assert data["url"] == f"https://pub.switch.box/{card.citekey}"
    assert data["collections"] == ["COL_MA"]
    assert data["tags"] == [{"tag": "processed"}]
    kinds = {c["title"]: c["linkMode"] for c in world.attachments_of(item["key"])}
    assert kinds["order.pdf"] == "imported_file"
    assert kinds[ingest.ORIGINAL_TITLE] == "linked_url"
    assert kinds[ingest.DOCUMENTCLOUD_TITLE] == "linked_url"
    assert extra.get(data["extra"], zotero.DOCUMENTCLOUD_ID) == "101"
    # The short link forwards to the DocumentCloud copy and is on the remote.
    assert remote_links(pub_remote, tmp_path)[card.citekey].startswith("https://www.documentcloud.org/documents/101-")
    assert report.short_url == f"https://pub.switch.box/{card.citekey}"
    # Front matter: legacy fields converted, ids written, comments kept.
    text = extract_file.read_text(encoding="utf-8")
    fm = frontmatter.parse(text)
    assert fm["citekey"] == card.citekey and fm["zotero_item"] == item["key"]
    assert fm["source_file"] == "order.pdf" and "source" not in fm and "original_pdf_path" not in fm
    assert fm["validated"] == "2026-10-28" and fm["pages_total"] == 12
    assert "# as printed on every page" in text
    # Index row added to the global README.
    assert "| ma_hp_rates/madpu_25-55_order.md |" in (repo / "context" / "README.md").read_text(encoding="utf-8")


def test_rerun_after_success_changes_nothing(world, repo, pdf_file, extract_file, pub_remote):
    card = make_card()
    assert run(world, repo, card, pdf_file).ok
    commits = remote_commits(pub_remote)
    readme = (repo / "context" / "README.md").read_text(encoding="utf-8")
    extract = extract_file.read_text(encoding="utf-8")
    world.calls.clear()
    report = run(world, repo, make_card(), pdf_file)
    assert report.ok
    assert world.calls["create_item"] == 0 and world.calls["dc_start_upload"] == 0
    assert len(only_item(world)["data"]["tags"]) == 1
    assert remote_commits(pub_remote) == commits
    assert (repo / "context" / "README.md").read_text(encoding="utf-8") == readme
    assert extract_file.read_text(encoding="utf-8") == extract
    assert len(world.attachments_of(only_item(world)["key"])) == 3


@pytest.mark.parametrize(
    "failing",
    ["create_item", "attach_file", "dc_start_upload", "dc_wait", "set_extra_fields", "attach_link", "mark_processed"],
)
def test_failure_at_each_step_then_rerun_completes(world, repo, pdf_file, extract_file, pub_remote, failing):
    card = make_card()
    world.fail_next(failing)
    first = run(world, repo, card, pdf_file)
    assert not first.ok or not first.processed
    second = run(world, repo, make_card(), pdf_file)
    assert second.ok, second.to_dict()
    assert second.processed
    item = only_item(world)
    assert len([d for d in world.dc.values() if d["citekey"] == card.citekey]) == 1
    stored = [c for c in world.attachments_of(item["key"]) if c["linkMode"] == "imported_file"]
    assert len(stored) == 1
    links = [c["url"] for c in world.attachments_of(item["key"]) if c["linkMode"] == "linked_url"]
    assert len(links) == len(set(links))
    assert item["data"]["tags"] == [{"tag": "processed"}]


def test_item_created_but_nothing_else_resumes_from_the_item(world, repo, pdf_file, extract_file):
    """A run that dies right after creating the item must not create a second one."""
    world.fail_next("attach_file")
    run(world, repo, make_card(), pdf_file)
    assert world.calls["create_item"] == 1
    run(world, repo, make_card(), pdf_file)
    assert world.calls["create_item"] == 1
    assert len(world.items) == 1


def test_documentcloud_id_never_recorded_is_found_by_citekey(world, repo, pdf_file, extract_file):
    card = make_card()
    world.fail_next("set_extra_fields")  # upload started, the ID never reached Zotero
    first = run(world, repo, card, pdf_file)
    assert "documentcloud_start" in {s.name for s in first.failed}
    second = run(world, repo, make_card(), pdf_file)
    assert second.ok
    assert world.calls["dc_start_upload"] == 1
    assert extra.get(only_item(world)["data"]["extra"], zotero.DOCUMENTCLOUD_ID) == "101"


def test_documentcloud_processing_error_reuploads_once(world, repo, pdf_file, extract_file):
    from lib.sources import documentcloud

    world.fail_next("dc_wait", documentcloud.UploadError("processing failed"))
    report = run(world, repo, make_card(), pdf_file)
    assert report.ok, report.to_dict()
    assert world.calls["dc_start_upload"] == 2
    assert len(world.dc) == 1  # the failed upload was deleted


def test_publish_failure_is_finished_by_rerun(world, repo, pdf_file, extract_file, pub_remote, tmp_path, monkeypatch):
    card = make_card()
    real = shortlinks._git

    def broken_push(repo_path, *args, **kwargs):
        if args[:1] == ("push",):
            raise RuntimeError("network down")
        return real(repo_path, *args, **kwargs)

    monkeypatch.setattr(shortlinks, "_git", broken_push)
    first = run(world, repo, card, pdf_file)
    assert not first.processed and any(s.name == "short_links_publish" for s in first.failed)
    monkeypatch.setattr(shortlinks, "_git", real)
    second = run(world, repo, make_card(), pdf_file)
    assert second.ok and second.processed
    assert card.citekey in remote_links(pub_remote, tmp_path)


def test_missing_extract_leaves_item_pending(world, repo, pdf_file):
    report = run(world, repo, make_card(), pdf_file)
    assert statuses(report)["front_matter"] == "pending"
    assert not report.processed and not report.ok
    assert only_item(world)["data"]["tags"] == []


def test_duplicate_by_md5_is_refused(world, repo, pdf_file, extract_file):
    existing = world.add_item({"itemType": "document", "title": "Something else entirely"})
    zotero.attach_file(existing, pdf_file)
    report = run(world, repo, make_card(), pdf_file)
    assert statuses(report)["zotero_item"] == "failed"
    assert "possible duplicates" in report.steps[-1].detail
    assert world.calls["create_item"] == 0


def test_force_creates_despite_duplicates(world, repo, pdf_file, extract_file):
    existing = world.add_item({"itemType": "document", "title": "Something else entirely"})
    zotero.attach_file(existing, pdf_file)
    report = run(world, repo, make_card(), pdf_file, force=True)
    assert statuses(report)["zotero_item"] == "done"


def test_key_collision_is_refused(world, repo, pdf_file, extract_file):
    card = make_card()
    world.add_item({"itemType": "document", "title": "Other", "extra": f"Citation Key: {card.citekey}"})
    report = run(world, repo, card, pdf_file)
    assert statuses(report)["validate"] == "failed"
    assert "already used" in report.steps[0].detail
    assert world.calls["create_item"] == 0


def test_adopting_an_inbox_item(world, repo, pdf_file, extract_file):
    key = world.add_item(
        {
            "itemType": "webpage",
            "title": "docket order",
            "collections": ["COL_INBOX"],
            "url": "https://example.org/files/order.pdf",
        }
    )
    report = run(world, repo, make_card(), pdf_file, zotero_item=key)
    assert report.ok, report.to_dict()
    data = world.items[key]["data"]
    assert data["itemType"] == "document" and data["collections"] == ["COL_MA"]
    assert world.calls["create_item"] == 0
    assert extra.get(data["extra"], extra.CITATION_KEY) == make_card().citekey


def add_raw_file(world: World, pdf: Path, **data) -> str:
    key = world.add_item(
        {
            "itemType": "attachment",
            "linkMode": "imported_file",
            "title": pdf.name,
            "filename": pdf.name,
            "md5": zotero.file_md5(pdf),
            "contentType": "application/pdf",
            "collections": ["COL_INBOX"],
            **data,
        }
    )
    world.files[key] = pdf.read_bytes()
    return key


def test_adopting_a_raw_file_creates_the_item_and_moves_the_file_under_it(world, repo, pdf_file, extract_file):
    raw = add_raw_file(world, pdf_file)
    report = run(world, repo, make_card(), None, zotero_item=raw)
    assert report.ok, report.to_dict()
    item = only_item(world)
    assert item["data"]["itemType"] == "document" and item["data"]["collections"] == ["COL_MA"]
    assert [c["key"] for c in world.children[item["key"]] if c["linkMode"] == "imported_file"] == [raw]
    assert "moved file" in next(s.detail for s in report.steps if s.name == "zotero_item")

    again = run(world, repo, make_card(), None, zotero_item=raw)
    assert again.ok, again.to_dict()
    assert world.calls["create_item"] == 1 and world.calls["adopt_raw_file"] == 1


def test_raw_file_adoption_resumes_after_a_failed_move(world, repo, pdf_file, extract_file):
    raw = add_raw_file(world, pdf_file)
    world.fail_next("adopt_raw_file")
    first = run(world, repo, make_card(), None, zotero_item=raw)
    assert statuses(first)["zotero_item"] == "failed"
    report = run(world, repo, make_card(), None, zotero_item=raw)
    assert report.ok, report.to_dict()
    assert world.calls["create_item"] == 1
    assert raw in {c["key"] for c in world.children[only_item(world)["key"]]}


def test_no_public_copy_and_no_source_url_fails_the_short_link(world, repo, pdf_file, extract_file):
    card = make_card(upload_documentcloud=False, source_url=None)
    report = run(world, repo, card, pdf_file)
    assert statuses(report)["short_link"] == "failed"
    assert "nothing for the short link" in next(s.detail for s in report.steps if s.name == "short_link")
    assert not report.processed


def test_a_linked_attachment_cannot_be_adopted(world, repo, extract_file):
    link = world.add_item({"itemType": "attachment", "linkMode": "linked_url", "url": "https://example.org/x"})
    report = run(world, repo, make_card(), None, zotero_item=link)
    assert statuses(report)["validate"] == "failed"
    assert "not a stored file" in report.steps[0].detail


def test_doi_item_has_no_short_link_and_no_documentcloud(world, repo, pdf_file, extract_file, pub_remote, tmp_path):
    card = make_card(
        item_type="journalArticle",
        title="Heat pump rates and cross-subsidies",
        creators=[{"first_name": "Ana", "last_name": "Lopez"}],
        abbreviation=None,
        docket=None,
        doi="10.1234/abcd.5678",
        extract_path="context/sources/ma_hp_rates/lopez_cross_subsidies.md",
    )
    path = repo / "context" / "sources" / "ma_hp_rates" / "lopez_cross_subsidies.md"
    path.write_text("---\nsource: paper.pdf\n---\n\nText\n", encoding="utf-8")
    report = run(world, repo, card, pdf_file)
    assert report.ok, report.to_dict()
    assert world.calls["dc_start_upload"] == 0
    assert only_item(world)["data"]["url"] == "https://doi.org/10.1234/abcd.5678"
    assert card.citekey not in remote_links(pub_remote, tmp_path)
    assert report.short_url is None
    assert frontmatter.parse(path.read_text(encoding="utf-8")).get("short_url") is None


def test_workbook_gets_drive_copy_and_stub(world, repo, tmp_path):
    book = tmp_path / "model.xlsx"
    book.write_bytes(b"PK\x03\x04 pretend workbook")
    card = make_card(
        item_type="dataset",
        title="Docket 25-55: Heat Pump Rate Design Model",
        source_file="model.xlsx",
        source_url="https://example.org/files/model.xlsx",
        extract_path="context/sources/ma_hp_rates/madpu_25-55_model.md",
    )
    report = run(world, repo, card, book)
    assert report.ok, report.to_dict()
    assert world.calls["dc_start_upload"] == 0 and world.calls["drive_upload"] == 1
    stub = repo / "context" / "sources" / "ma_hp_rates" / "madpu_25-55_model.md"
    fm = frontmatter.parse(stub.read_text(encoding="utf-8"))
    assert fm["repo_file"] == "madpu_25-55_model.xlsx"
    assert (stub.with_suffix(".xlsx")).read_bytes() == book.read_bytes()
    assert fm["public_url"].startswith("https://drive.google.com/file/d/")
    assert extra.get(only_item(world)["data"]["extra"], zotero.DRIVE_ID) == "DRV1"


def test_large_workbook_needs_a_decision(world, repo, tmp_path):
    book = tmp_path / "big.xlsx"
    book.write_bytes(b"x" * (601 * 1024))
    card = make_card(item_type="dataset", source_file="big.xlsx", extract_path="context/sources/ma_hp_rates/big.md")
    report = run(world, repo, card, book)
    assert statuses(report)["validate"] == "failed"
    assert "workbook_in_repo" in report.steps[0].detail
    assert not world.items


def test_large_workbook_zotero_only(world, repo, tmp_path):
    book = tmp_path / "big.xlsx"
    book.write_bytes(b"x" * (601 * 1024))
    card = make_card(
        item_type="dataset",
        source_file="big.xlsx",
        workbook_in_repo=False,
        extract_path="context/sources/ma_hp_rates/big.md",
    )
    report = run(world, repo, card, book)
    assert report.ok, report.to_dict()
    stub = repo / "context" / "sources" / "ma_hp_rates" / "big.md"
    assert frontmatter.parse(stub.read_text(encoding="utf-8"))["repo_file"] == "not in repo: fetch from Zotero"
    assert not stub.with_suffix(".xlsx").exists()
    assert any("fetch-source" in n for n in report.notes)


def test_web_page_is_captured_archived_and_extracted(world, repo, pub_remote, tmp_path):
    card = make_card(
        item_type="webpage",
        title="Heat pump rates explained",
        creators=[{"name": "Example Energy Institute"}],
        abbreviation=None,
        docket=None,
        date="2026-05-01",
        source_file=None,
        source_url="https://example.org/heat-pump-rates",
        access_date="2026-10-28",
        extract_path="context/sources/ma_hp_rates/example_heat_pump_rates.md",
    )
    report = run(world, repo, card, None)
    assert report.ok, report.to_dict()
    item = only_item(world)
    assert world.calls["dc_start_upload"] == 0
    titles = {c["title"] for c in world.attachments_of(item["key"])}
    assert {ingest.CAPTURE_TITLE, ingest.WAYBACK_TITLE, ingest.ORIGINAL_TITLE} <= titles
    assert str(extra.get(item["data"]["extra"], zotero.WAYBACK_URL)).startswith("https://web.archive.org/")
    extract = repo / "context" / "sources" / "ma_hp_rates" / "example_heat_pump_rates.md"
    text = extract.read_text(encoding="utf-8")
    assert "Hello world." in text and "menu" not in text
    assert remote_links(pub_remote, tmp_path)[card.citekey] == "https://example.org/heat-pump-rates"


def test_wayback_blocked_is_noted_not_failed(world, repo, tmp_path):
    world.wayback_blocked = True
    card = make_card(
        item_type="webpage",
        title="Blocked page",
        creators=[{"name": "Example Energy Institute"}],
        abbreviation=None,
        docket=None,
        source_file=None,
        source_url="https://example.org/blocked",
        extract_path="context/sources/ma_hp_rates/blocked.md",
    )
    report = run(world, repo, card, None)
    assert report.ok, report.to_dict()
    assert any("blocked" in n.lower() for n in report.notes)


def test_batch_makes_one_short_link_commit_and_survives_one_failure(
    world, repo, pdf_file, extract_file, pub_remote, tmp_path
):
    a = make_card()
    other = repo / "context" / "sources" / "ma_hp_rates" / "madpu_25-55_second.md"
    other.write_text("---\nsource: second.pdf\n---\n\nText\n", encoding="utf-8")
    second_pdf = tmp_path / "second.pdf"
    second_pdf.write_bytes(b"%PDF-1.4 second\n")
    b = make_card(
        title="Docket 25-55: Second Order",
        source_file="second.pdf",
        source_url="https://example.org/files/second.pdf",
        extract_path="context/sources/ma_hp_rates/madpu_25-55_second.md",
    )
    bad = make_card(
        title="Docket 25-55: Third Order", extract_path="context/sources/ma_hp_rates/third.md", index_row=None
    )
    before = remote_commits(pub_remote)
    reports = ingest.ingest_batch(
        [(a, pdf_file, None, None), (b, second_pdf, None, None), (bad, pdf_file, None, None)], repo_root=repo
    )
    assert [r.ok for r in reports] == [True, True, False]
    assert remote_commits(pub_remote) == before + 1
    links = remote_links(pub_remote, tmp_path)
    assert a.citekey in links and b.citekey in links


def test_unknown_project_needs_new_project(world, repo, pdf_file, extract_file):
    report = run(world, repo, make_card(projects=["nj_hp_rates"]), pdf_file)
    assert statuses(report)["validate"] == "failed"
    assert "new_project" in report.steps[0].detail


def test_write_token_is_stable():
    assert ingest.write_token("abc") == ingest.write_token("abc") != ingest.write_token("abd")
    assert len(ingest.write_token("abc")) == 32
