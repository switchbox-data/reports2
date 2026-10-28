"""Dedupe finds a document by md5, normalized source URL, legacy manifest and provenance CSV, at any depth."""

from __future__ import annotations

from pathlib import Path

import pytest

from lib.sources import dedupe, zotero

PDF = b"%PDF-1.4 sample\n"


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    root = tmp_path / "sources"
    nested = root / "il_hp_rates" / "tou" / "comed"
    nested.mkdir(parents=True)
    md5 = zotero.file_md5(_write(tmp_path / "x.pdf", PDF))
    (nested / "tariff.md").write_text(
        f'---\ncitekey: comed_Tariff_2025\nmd5: "{md5}"\nsource_url: https://www.example.org/Tariffs/rate.pdf?utm_source=mail\n---\n\nBody\n'
    )
    (root / "plain.md").write_text("# no front matter\n")
    manifest = root / "il_hp_rates" / "tou"
    sha = dedupe.sha256_of(tmp_path / "x.pdf")
    (manifest / "MANIFEST.csv").write_text(
        "source_pdf,tier,bytes,pages,text_chars,sha256,source_url,md_path,status,description\n"
        f"legacy.pdf,1,10,2,100,{sha},https://old.example.org/legacy.pdf,legacy.md,ok,Legacy\n"
    )
    return root


def _write(path: Path, data: bytes) -> Path:
    path.write_bytes(data)
    return path


def test_md5_match_in_nested_front_matter(tree, tmp_path):
    found = dedupe.local_matches(md5=zotero.file_md5(tmp_path / "x.pdf"), root=tree)
    assert [m.kind for m in found] == ["md5"]
    assert found[0].where.endswith("comed/tariff.md")


def test_source_url_is_normalized(tree):
    found = dedupe.local_matches(source_url="http://WWW.example.org/Tariffs/rate.pdf/", root=tree)
    assert [m.kind for m in found] == ["source_url"]


def test_manifest_sha256_and_url(tree, tmp_path):
    by_sha = dedupe.local_matches(sha256=dedupe.sha256_of(tmp_path / "x.pdf"), root=tree)
    assert any(m.kind == "manifest_sha256" and m.detail == "legacy.pdf" for m in by_sha)
    by_url = dedupe.local_matches(source_url="https://old.example.org/legacy.pdf", root=tree)
    assert any(m.kind == "manifest_url" for m in by_url)


def test_provenance_csv(tree, tmp_path):
    csv = tmp_path / "prov.csv"
    csv.write_text("n,source_url,md_path\n7,https://staging.example.org/a.pdf,context/sources/x.md\n")
    found = dedupe.local_matches(source_url="https://staging.example.org/a.pdf", root=tree, provenance_csv=csv)
    assert [(m.kind, m.detail) for m in found] == [("provenance_url", "row 7")]


def test_no_match(tree):
    assert dedupe.local_matches(md5="0" * 32, source_url="https://nowhere.example.org/z.pdf", root=tree) == []
    assert dedupe.summarize([]) == "no matches"


def test_check_combines_repo_and_zotero(tree, tmp_path, monkeypatch):
    monkeypatch.setenv("ZOTERO_GROUP_ID", "999")
    items = [
        {
            "key": "PARENT1",
            "data": {"itemType": "document", "title": "Comed Tariff 2025", "extra": "Citation Key: comed_Tariff_2025"},
        },
        {
            "key": "ATT1",
            "data": {"itemType": "attachment", "parentItem": "PARENT1", "md5": zotero.file_md5(tmp_path / "x.pdf")},
        },
    ]
    found = dedupe.check(tmp_path / "x.pdf", root=tree, items=items)
    kinds = {m.kind for m in found}
    assert {"md5", "manifest_sha256", "zotero_md5"} <= kinds
    zot = next(m for m in found if m.kind == "zotero_md5")
    assert "PARENT1" in zot.where and "comed_Tariff_2025" in zot.detail
    assert dedupe.check(tmp_path / "x.pdf", root=tree, items=items, use_zotero=False) != []


def test_zotero_matches_by_url_doi_and_title():
    items = [
        {
            "key": "A",
            "data": {
                "itemType": "journalArticle",
                "title": "Heat Pump Rates and Cross-Subsidies",
                "DOI": "10.1234/ABC",
                "url": "https://example.org/paper?utm_campaign=x",
            },
        }
    ]
    assert [m.kind for m in dedupe.zotero_matches(doi="https://doi.org/10.1234/abc", items=items)] == ["zotero_doi"]
    assert [m.kind for m in dedupe.zotero_matches(url="http://Example.org/paper/", items=items)] == ["zotero_url"]
    assert [m.kind for m in dedupe.zotero_matches(title="Heat pump rates and cross subsidies", items=items)] == [
        "zotero_title"
    ]
