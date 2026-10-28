from __future__ import annotations

from lib.sources import projects


def test_projects_are_the_union_of_report_folders_zotero_and_source_folders(tmp_path):
    reports, sources = tmp_path / "reports", tmp_path / "sources"
    for name in ("ri_hp_rates", "templates", "docs", ".hidden"):
        (reports / name).mkdir(parents=True)
    for name in ("ri_hp_rates", "ma_hp_rates", "il_hp_rates", "bonbright_1960", "random_notes"):
        (sources / name).mkdir(parents=True)
    (sources / "neep_modern_rate_design.md").write_text("x")
    found = {p.name: p for p in projects.list_projects(reports, sources, ["ma_hp_rates", "ny_aeba", "bonbright_1960"])}
    assert set(found) == {
        "ri_hp_rates",
        "ma_hp_rates",
        "il_hp_rates",
        "ny_aeba",
    }  # no templates, general reference or loose folders
    assert (
        found["ri_hp_rates"].report_folder
        and found["ri_hp_rates"].source_folder
        and not found["ri_hp_rates"].zotero_collection
    )
    assert found["il_hp_rates"].planned and not found["il_hp_rates"].zotero_collection
    assert found["ny_aeba"].zotero_collection and not found["ny_aeba"].source_folder
    assert found["ma_hp_rates"].complete and not found["ny_aeba"].complete


def test_ensure_project_creates_collection_and_folder_once(tmp_path):
    created = []

    def create(name):
        created.append(name)
        return "COL1"

    out = projects.ensure_project("nj_hp_rates", tmp_path, create)
    assert out["zotero_collection"] == "COL1" and (tmp_path / "nj_hp_rates").is_dir()
    projects.ensure_project("nj_hp_rates", tmp_path, create)
    assert created == ["nj_hp_rates", "nj_hp_rates"]  # the collection helper itself is idempotent
