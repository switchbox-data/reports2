"""Phase 5 tooling: provenance CSV to draft cards, legacy front matter, MANIFEST.csv folders."""

from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest
import yaml

from lib.sources import frontmatter, metadata, migrate

CSV = """n,state,utility,rate,regulator,docket,filing_date,filer,doc_type,title,source_url,src,repo_path,md_path,type,size
1,MA,Eversource,R1HP,madpu,25-55,2025-04-17,NSTAR,workbook,Petition :: Exh. ES-HP-2.xlsx,https://x.org/a,/stage/a.xlsx,context/sources/ma_hp_rates/a.xlsx,context/sources/ma_hp_rates/a.xlsx,XLSX,1 MB
2,MA,Eversource,R1HP,madpu,25-55,2025-04-17,NSTAR,testimony,Petition :: Exh. ES-HP-1.pdf,https://x.org/b,/stage/b.pdf,context/sources/ma_hp_rates/b.pdf,context/sources/ma_hp_rates/b.md,PDF,400 KB
"""


@pytest.fixture
def provenance(tmp_path: Path) -> pl.DataFrame:
    path = tmp_path / "prov.csv"
    path.write_text(CSV)
    return migrate.read_provenance(path)


def test_source_for_extract_matches_workbooks_by_stem(provenance):
    found_a = migrate.source_for_extract(provenance, "context/sources/ma_hp_rates/a.md")
    found_b = migrate.source_for_extract(provenance, "context/sources/ma_hp_rates/b.md")
    assert found_a is not None and found_a["src"] == "/stage/a.xlsx"
    assert found_b is not None and found_b["src"] == "/stage/b.pdf"
    assert migrate.source_for_extract(provenance, "context/sources/ma_hp_rates/zzz.md") is None


def test_draft_cards_are_prefilled_but_not_yet_valid(provenance, tmp_path):
    paths = migrate.draft_cards(provenance, tmp_path / "cards")
    assert len(paths) == 2
    book, pdf = (yaml.safe_load(p.read_text()) for p in paths)
    assert book["item_type"] == "dataset" and book["extract_path"] == "context/sources/ma_hp_rates/a.md"
    assert pdf["item_type"] == "document" and pdf["projects"] == ["ma_hp_rates"]
    assert pdf["title"] == "Docket 25-55: Petition" and pdf["source_file"] == "b.pdf"
    assert pdf["front_matter"]["utility"] == "Eversource" and pdf["front_matter"]["document_type"] == "testimony"
    with pytest.raises(ValueError):  # creators, citekey and index_row still need filling in
        metadata.load(paths[1])


LEGACY = "---\nsource: b.pdf\noriginal_pdf_path: /stage/b.pdf\ndocket: 25-55\n---\n\nBody\n"


def test_convert_frontmatter_is_a_dry_run_by_default(tmp_path):
    (tmp_path / "x").mkdir()
    (tmp_path / "x" / "b.md").write_text(LEGACY)
    (tmp_path / "done.md").write_text("---\nsource_file: c.pdf\n---\n\nBody\n")
    (tmp_path / "plain.md").write_text("no front matter")
    changes = migrate.convert_frontmatter(tmp_path)
    assert [c.path.name for c in changes] == ["b.md"]
    assert (tmp_path / "x" / "b.md").read_text() == LEGACY
    migrate.convert_frontmatter(tmp_path, dry_run=False)
    fm = frontmatter.read(tmp_path / "x" / "b.md")
    assert fm == {"source_file": "b.pdf", "docket": "25-55"}
    assert migrate.convert_frontmatter(tmp_path) == []


def test_convert_frontmatter_quotes_values_that_are_not_valid_yaml(tmp_path):
    legacy = (
        "---\nsource: b.pdf\nwhy_here: the only testimony in the case: derivation of the rate\n"
        "filer: Jo's Utility # a comment\noriginal_pdf_path: /stage/b.pdf\n---\n\nBody\n"
    )
    (tmp_path / "b.md").write_text(legacy)
    changes = migrate.convert_frontmatter(tmp_path)
    assert [c.detail for c in changes] == ["converted source, original_pdf_path; quoted why_here"]
    migrate.convert_frontmatter(tmp_path, dry_run=False)
    assert frontmatter.read(tmp_path / "b.md") == {
        "source_file": "b.pdf",
        "why_here": "the only testimony in the case: derivation of the rate",
        "filer": "Jo's Utility",
    }


def test_manifest_folder_adds_front_matter_and_uses_the_first_row_per_extract(tmp_path):
    folder = tmp_path / "tou"
    folder.mkdir()
    (folder / "doc.md").write_text("# Doc\n\nBody\n")
    (folder / "MANIFEST.csv").write_text(
        "source_pdf,source_url,md_path,status\n"
        "doc.pdf,https://x.org/doc.pdf,doc.md,extracted\n"
        "workbooks/doc_table.csv,https://x.org/doc.pdf,doc.md,extracted\n"
    )
    changes = migrate.convert_manifest_folder(folder, dry_run=False)
    assert len(changes) == 1
    assert frontmatter.read(folder / "doc.md") == {"source_file": "doc.pdf", "source_url": "https://x.org/doc.pdf"}
    assert (folder / "doc.md").read_text().endswith("---\n\n# Doc\n\nBody\n")
    assert migrate.convert_manifest_folder(folder, dry_run=False) == []


def test_manifest_folder_fills_front_matter(tmp_path):
    folder = tmp_path / "tou"
    folder.mkdir()
    (folder / "doc.pdf").write_bytes(b"%PDF doc")
    (folder / "doc.md").write_text("---\nsource: doc.pdf\n---\n\nBody\n")
    (folder / "MANIFEST.csv").write_text(
        "source_pdf,tier,bytes,pages,text_chars,sha256,source_url,md_path,status,description\n"
        "doc.pdf,1,8,1,10,abc,https://x.org/doc.pdf,doc.md,ok,Doc\n"
        "ghost.pdf,1,8,1,10,abc,https://x.org/ghost.pdf,ghost.md,ok,Missing extract\n"
    )
    assert migrate.manifest_folders(tmp_path) == [folder]
    changes = migrate.convert_manifest_folder(folder, dry_run=False)
    assert len(changes) == 1
    fm = frontmatter.read(folder / "doc.md")
    assert fm["source_file"] == "doc.pdf" and fm["source_url"] == "https://x.org/doc.pdf" and len(fm["md5"]) == 32
    assert migrate.convert_manifest_folder(folder, dry_run=False) == []
