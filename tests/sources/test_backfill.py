"""Backfill of doi.org urls and short links for items that predate ingest."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from lib.sources import backfill, extra
from lib.sources.ingest import DOCUMENTCLOUD_TITLE, ORIGINAL_TITLE

from .conftest import World, remote_commits, remote_links

DC_PAGE = "https://www.documentcloud.org/documents/111-ma-order"
WRITES = ("set_url", "attach_link", "set_extra_fields")


def add(world: World, citekey: str, **fields: Any) -> str:
    data = {
        "itemType": "report",
        "title": f"Title of {citekey}",
        "collections": ["COL_MA"],
        "extra": f"Citation Key: {citekey}",
        **fields,
    }
    return world.add_item(data)


def link(world: World, item: str, url: str, mode: str = "linked_url", title: str = "") -> None:
    world.children[item].append(
        {"key": world._new_key(), "itemType": "attachment", "linkMode": mode, "url": url, "title": title}
    )


def attachments(world: World, item: str) -> list[tuple[str, str]]:
    return [(c["url"], c["title"]) for c in world.children[item] if c["linkMode"] in ("linked_url", "imported_url")]


def data(world: World, item: str) -> dict[str, Any]:
    return world.items[item]["data"]


@pytest.mark.parametrize(
    "url, doc_id, canonical",
    [
        (DC_PAGE + "/", "111", DC_PAGE),
        (DC_PAGE + "/#document/p4/a12", "111", DC_PAGE),
        (DC_PAGE + "/?mode=annotating", "111", DC_PAGE),
        (DC_PAGE + "/p4/a12", "111", DC_PAGE),
        (
            "https://s3.documentcloud.org/documents/111/ma-order.pdf?X-Amz-Signature=abc",
            "111",
            DC_PAGE,
        ),
        ("https://www.documentcloud.org/documents/111", "111", "https://www.documentcloud.org/documents/111"),
    ],
)
def test_documentcloud_urls_reduce_to_the_document_page(url: str, doc_id: str, canonical: str) -> None:
    ref = backfill.parse_documentcloud(url)
    assert ref is not None
    assert (ref.doc_id, ref.canonical) == (doc_id, canonical)


@pytest.mark.parametrize("url", [None, "", "https://example.org/documents/111-a", "https://www.documentcloud.org/"])
def test_other_urls_are_not_documentcloud(url: str | None) -> None:
    assert backfill.parse_documentcloud(url) is None


def test_doi_item_gets_the_doi_link_and_keeps_its_old_url(world: World) -> None:
    item = add(world, "smith_Paper_2020", itemType="journalArticle", DOI="10.1/abc", url="https://publisher.org/p")
    plan, failures = backfill.run(apply=True)
    assert failures == []
    assert [p.kind for p in plan.items] == ["doi"]
    assert data(world, item)["url"] == "https://doi.org/10.1/abc"
    assert attachments(world, item) == [("https://publisher.org/p", ORIGINAL_TITLE)]
    assert extra.get(data(world, item)["extra"], extra.DOCUMENTCLOUD_ID) is None


def test_doi_item_with_an_empty_url_just_gets_the_link(world: World) -> None:
    item = add(world, "smith_Paper_2021", DOI="10.1/def", url="")
    backfill.run(apply=True)
    assert data(world, item)["url"] == "https://doi.org/10.1/def"
    assert attachments(world, item) == []


def test_an_http_variant_of_the_doi_link_is_replaced_without_keeping_it(world: World) -> None:
    item = add(world, "smith_Paper_2023", DOI="10.1/jkl", url="http://dx.doi.org/10.1/jkl")
    backfill.run(apply=True)
    assert data(world, item)["url"] == "https://doi.org/10.1/jkl"
    assert attachments(world, item) == []


def test_doi_item_already_on_the_doi_link_is_untouched(world: World) -> None:
    add(world, "smith_Paper_2022", DOI="10.1/ghi", url="https://doi.org/10.1/ghi")
    plan, _ = backfill.run()
    assert plan.items == []


def test_documentcloud_in_url(world: World, pub_remote: Path, tmp_path: Path) -> None:
    item = add(world, "madpu_Order_2025", url=DC_PAGE + "/")
    before = remote_commits(pub_remote)
    plan, failures = backfill.run(apply=True)
    assert failures == []
    assert [p.kind for p in plan.items] == ["documentcloud"]
    assert data(world, item)["url"] == "https://pub.switch.box/madpu_Order_2025"
    assert extra.get(data(world, item)["extra"], extra.DOCUMENTCLOUD_ID) == "111"
    assert extra.get(data(world, item)["extra"], extra.CITATION_KEY) == "madpu_Order_2025"
    assert attachments(world, item) == [(DC_PAGE + "/", DOCUMENTCLOUD_TITLE)]
    assert remote_links(pub_remote, tmp_path)["madpu_Order_2025"] == DC_PAGE
    assert remote_commits(pub_remote) == before + 1


def test_documentcloud_in_an_attachment(world: World, pub_remote: Path, tmp_path: Path) -> None:
    item = add(world, "nyserda_Plan_2023", url="")
    s3 = "https://s3.documentcloud.org/documents/222/ny-plan.pdf?X-Amz-Signature=abc"
    link(world, item, s3, mode="imported_url", title="ny-plan.pdf")
    backfill.run(apply=True)
    assert data(world, item)["url"] == "https://pub.switch.box/nyserda_Plan_2023"
    assert extra.get(data(world, item)["extra"], extra.DOCUMENTCLOUD_ID) == "222"
    assert (
        remote_links(pub_remote, tmp_path)["nyserda_Plan_2023"] == "https://www.documentcloud.org/documents/222-ny-plan"
    )
    urls = [u for u, _ in attachments(world, item)]
    assert urls == [s3, "https://www.documentcloud.org/documents/222-ny-plan"]


def test_documentcloud_attachment_and_a_different_original_url(world: World, pub_remote: Path, tmp_path: Path) -> None:
    item = add(world, "kedny_Report_2023", url="https://utility.com/doc.pdf")
    link(world, item, DC_PAGE)
    link(world, item, "https://utility.com/doc.pdf")
    backfill.run(apply=True)
    assert data(world, item)["url"] == "https://pub.switch.box/kedny_Report_2023"
    assert attachments(world, item) == [(DC_PAGE, ""), ("https://utility.com/doc.pdf", "")]  # no duplicates added
    assert remote_links(pub_remote, tmp_path)["kedny_Report_2023"] == DC_PAGE


def test_item_with_neither_is_skipped(world: World, pub_remote: Path) -> None:
    item = add(world, "nrel_Atb_2024", url="https://atb.nrel.gov/")
    before = remote_commits(pub_remote)
    plan, _ = backfill.run(apply=True)
    assert plan.items == [] and plan.skipped == 1
    assert data(world, item)["url"] == "https://atb.nrel.gov/"
    assert world.calls["set_url"] == 0 and remote_commits(pub_remote) == before


def test_item_with_a_doi_and_a_documentcloud_link_follows_the_doi_rule(
    world: World, pub_remote: Path, tmp_path: Path
) -> None:
    item = add(world, "littlefield_Lca_2022", DOI="10.1021/x", url=DC_PAGE + "/#document/p2")
    backfill.run(apply=True)
    assert data(world, item)["url"] == "https://doi.org/10.1021/x"
    assert "littlefield_Lca_2022" not in remote_links(pub_remote, tmp_path)  # DOI items get no short link
    assert extra.get(data(world, item)["extra"], extra.DOCUMENTCLOUD_ID) == "111"  # the copy is still recorded
    assert attachments(world, item) == [(DC_PAGE + "/#document/p2", DOCUMENTCLOUD_TITLE)]


def test_items_outside_reports_trashed_or_without_a_key_are_left_alone(world: World) -> None:
    add(world, "other_Doc_2020", collections=["COL_ELSEWHERE"], url=DC_PAGE)
    add(world, "gone_Doc_2020", url=DC_PAGE, deleted=1)
    nokey = world.add_item({"itemType": "report", "title": "No key", "collections": ["COL_MA"], "url": DC_PAGE})
    plan, _ = backfill.run(apply=True)
    assert plan.items == []
    assert "no pinned citation key" in plan.problems[0] and nokey in plan.problems[0]


def test_existing_short_link_to_another_document_is_not_overwritten(
    world: World, pub_remote: Path, tmp_path: Path
) -> None:
    from lib.sources import shortlinks

    batch = shortlinks.Batch()
    batch.add("madpu_Order_2025", "https://drive.google.com/file/d/X/view")
    batch.publish()
    item = add(world, "madpu_Order_2025", url=DC_PAGE)
    plan, failures = backfill.run(apply=True)
    assert plan.items == [] and "left alone" in backfill.report(plan, apply=True)
    assert failures == [] and data(world, item)["url"] == DC_PAGE


def test_dry_run_writes_nothing(world: World, pub_remote: Path) -> None:
    add(world, "madpu_Order_2025", url=DC_PAGE)
    add(world, "smith_Paper_2020", DOI="10.1/abc", url="https://publisher.org/p")
    before = remote_commits(pub_remote)
    plan, _ = backfill.run()
    assert len(plan.items) == 2
    assert all(world.calls[name] == 0 for name in WRITES)
    assert remote_commits(pub_remote) == before
    text = backfill.report(plan, apply=False)
    assert "set url to doi.org link: 1" in text and "add short link to pub: 1" in text


def test_rerun_after_apply_changes_nothing(world: World, pub_remote: Path) -> None:
    add(world, "madpu_Order_2025", url=DC_PAGE + "/")
    add(world, "smith_Paper_2020", DOI="10.1/abc", url="https://publisher.org/p")
    add(world, "littlefield_Lca_2022", DOI="10.1021/x", url=DC_PAGE + "/#document/p2")
    nyserda = add(world, "nyserda_Plan_2023", url="")
    link(world, nyserda, "https://s3.documentcloud.org/documents/222/ny-plan.pdf", mode="imported_url")
    backfill.run(apply=True)
    commits = remote_commits(pub_remote)
    snapshot = [(it["key"], dict(it["data"])) for it in world.library()]
    world.calls.clear()

    plan, failures = backfill.run(apply=True)

    assert plan.items == [] and failures == []
    assert all(world.calls[name] == 0 for name in WRITES)
    assert remote_commits(pub_remote) == commits
    assert snapshot == [(it["key"], dict(it["data"])) for it in world.library()]


def test_a_failed_item_is_reported_and_a_rerun_finishes_it(world: World, pub_remote: Path) -> None:
    first = add(world, "aaa_Order_2025", url="https://www.documentcloud.org/documents/1-a")
    second = add(world, "bbb_Order_2025", url="https://www.documentcloud.org/documents/2-b")
    world.fail_next("set_extra_fields")
    plan, failures = backfill.run(apply=True)
    assert len(failures) == 1 and "aaa_Order_2025" in failures[0]
    assert (
        data(world, first)["url"] == "https://www.documentcloud.org/documents/1-a"
    )  # url goes last: still the original
    assert data(world, second)["url"] == "https://pub.switch.box/bbb_Order_2025"

    commits = remote_commits(pub_remote)
    plan, failures = backfill.run(apply=True)

    assert failures == [] and [p.citekey for p in plan.items] == ["aaa_Order_2025"]
    assert data(world, first)["url"] == "https://pub.switch.box/aaa_Order_2025"
    assert remote_commits(pub_remote) == commits  # the short links were all published the first time
    assert [url for url, _ in attachments(world, first)] == ["https://www.documentcloud.org/documents/1-a"]
