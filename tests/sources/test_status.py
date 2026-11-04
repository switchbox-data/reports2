"""sources-status: green once ingest finished, red with a fix hint for whatever is missing."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from lib.sources import documentcloud, indexes, ingest, status
from lib.sources.doctor import FAIL, OK, WARN
from tests.sources.conftest import make_card, use_repo_env


@pytest.fixture
def ingested(world, repo, pdf_file, monkeypatch):
    use_repo_env(monkeypatch, repo)
    monkeypatch.setattr(indexes, "GLOBAL_README", repo / "context" / "README.md")
    doc = SimpleNamespace(status="success", access="public")
    monkeypatch.setattr(documentcloud, "client", lambda: SimpleNamespace(documents=SimpleNamespace(get=lambda i: doc)))
    (repo / "context" / "sources" / "ma_hp_rates" / "madpu_25-55_order.md").write_text(
        "---\nsource: order.pdf\n---\n\nBody\n"
    )
    card = make_card()
    assert ingest.ingest(card, source=pdf_file, repo_root=repo).ok
    return card


def levels(checks):
    return {c.name: c.level for c in checks}


def test_everything_green_after_ingest(ingested, repo):
    checks = status.source_status(ingested.citekey, repo / "context" / "sources")
    assert status.all_green(checks), [c.line() for c in checks if c.level != OK]
    assert levels(checks)["tagged processed"] == OK and levels(checks)["short link in pub"] == OK


def test_unknown_key_is_one_red_line(world):
    checks = status.source_status("nope_X_2025")
    assert len(checks) == 1 and checks[0].level == FAIL and not status.all_green(checks)


def test_missing_pieces_are_red_with_hints(ingested, repo, world):
    item = next(iter(world.items.values()))
    item["data"]["tags"] = []
    item["data"]["url"] = "https://example.org/wrong"
    world.children[item["key"]] = [c for c in world.children[item["key"]] if c["linkMode"] != "imported_file"]
    checks = status.source_status(ingested.citekey, repo / "context" / "sources")
    result = levels(checks)
    assert (
        result["tagged processed"] == FAIL
        and result["Zotero url is the citation link"] == FAIL
        and result["file stored in Zotero"] == FAIL
    )
    assert all(c.hint for c in checks if c.level == FAIL)


def test_no_extract_is_only_a_warning(ingested, repo):
    next(iter((repo / "context" / "sources").rglob("madpu_25-55_order.md"))).unlink()
    checks = status.source_status(ingested.citekey, repo / "context" / "sources")
    assert levels(checks)["extract with this citekey in the repo"] == WARN and status.all_green(checks)
