"""Turn the CIEC-11(c) MANIFEST.csv into CIEC-11 Attachment 2, a reader-facing Excel file list.

Lists every public file with its rate scenario, a plain-English description, its size and a
download link. The checksums stay in MANIFEST.csv. Writes the workbook next to the manifest;
``--upload-xlsx`` also uploads it to the CIEC Drive folder.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

PATH_HERE = Path(__file__).resolve().parent
PATH_REPORT = PATH_HERE.parent

TITLE = "CIEC-11(c): model input and output files"
SUBTITLE = (
    "PURA Docket No. 26-05-10. Files used in the Direct Testimony of Juan-Pablo Velez that were not "
    "already provided in Exhibits JPV-3 and JPV-4 or in response to CIEC-1."
)
XLSX_NAME = "CIEC-11c_file_list.xlsx"
URL_BASE = "https://switchbox-public-data.s3.us-west-2.amazonaws.com/ct_hp_rates/pura_26-05-10/ciec-11c"

INPUT_DESCRIPTIONS = {
    "inputs/marginal_costs/bulk_tx.parquet": "Hourly marginal bulk transmission cost",
    "inputs/marginal_costs/dist_and_sub_tx.parquet": "Hourly marginal distribution and sub-transmission cost",
    "inputs/postprocessing/cpiaucsl_2019_2026_20260803.parquet": (
        "Consumer Price Index (CPI-U), used to update ResStock household incomes to 2026 dollars"
        " for low-income eligibility"
    ),
    "inputs/postprocessing/heating_fuel_prices_ct_2024.parquet": (
        "Connecticut residential heating oil and propane prices, 2024, used to calculate oil and propane bills"
    ),
    "inputs/resstock/loads_hourly_eversource_upgrade00.parquet": (
        "Hourly electricity use of the 3,539 modeled homes, before heat pump installation"
    ),
    "inputs/resstock/loads_hourly_eversource_upgrade02.parquet": (
        "Hourly electricity use of the 3,539 modeled homes, after heat pump installation"
    ),
    "inputs/resstock/metadata_upgrade00.parquet": "Characteristics of the modeled homes, before heat pump installation",
    "inputs/resstock/metadata_upgrade02.parquet": "Characteristics of the modeled homes, after heat pump installation",
    "inputs/resstock/utility_assignment.parquet": "Electric and gas utility of each modeled home",
}
CONFIG_DESCRIPTIONS = {
    "tariffs": "Electric or gas rate",
    "tariff_maps": "Which rate applies to each modeled home",
    "scenarios": "Scenario definitions",
    "rev_requirement": "Revenue requirement settings",
    "postprocessing": "Settings used to calculate bills after each model run",
}
RUN_DESCRIPTIONS = {
    "tariff_final_config.json": "Rates applied in this run",
    "scenario_settings.json": "Settings for this run",
    "marginal_costs_used.json": "Marginal cost files used in this run",
    "billing_kwh_annual.parquet": "Annual electricity use billed, per home",
    "billing_kwh_8760.parquet": "Hourly electricity use billed, per home (times in UTC)",
}
MASTER_DESCRIPTIONS = {
    "comb_bills_year_target": "Monthly and annual bills of each modeled home",
    "cross_subsidization_BAT_values": "Bill alignment results for each modeled home",
}
# Scenario key in the folder names -> (tariff_base in the pipeline config, name as in the testimony).
SCENARIO_NAMES = {
    "r1": ("rate1_proposed", "Rate 1"),
    "r6": ("rate6", "Rate 6, as proposed by the Company"),
    "r6_ratemc_mfc0_trans": (
        "rate6_ratemc_mfc0_trans",
        "Modified Rate 6: winter Block 2 local facilities, upstream distribution and transmission charges"
        " at marginal cost",
    ),
    "icos_fair_seasonal": ("icos_fair_seasonal", "Rate HP: lower winter delivery rate"),
}
# Every scenario was run twice on the same tariff: on the homes as they are, and after the heat pump retrofit.
STAGE_NAMES = {"precalc": "Before heat pump installation", "calibrated": "After heat pump installation"}
CHARGE_NAMES = {"delivery": "delivery charges only", "supply": "delivery and supply charges"}
SEGMENT_PREFIX = "default_ry1_"
SEGMENT_INFIX = "_uncalibrated_"


@dataclass
class FileRow:
    folder: str
    scenario: str
    homes: str
    file: str
    description: str
    size: str
    url: str


def parse_segment(segment: str) -> tuple[str, str, str | None]:
    """(scenario name, homes, charges or None) from a master segment or run folder name."""
    scenario, rest = segment.split(SEGMENT_PREFIX, 1)[1].split(SEGMENT_INFIX)
    stage, _, charges = rest.partition("_")
    return SCENARIO_NAMES[scenario][1], STAGE_NAMES[stage], CHARGE_NAMES[charges] if charges else None


def check_scenarios(path_pipeline: Path) -> None:
    """Each scenario key must still bill the tariff its plain name describes."""
    import yaml
    from build_ciec_11c_share import SCENARIOS

    assert set(SCENARIO_NAMES) == set(SCENARIOS), set(SCENARIO_NAMES) ^ set(SCENARIOS)
    scenarios = yaml.safe_load(path_pipeline.read_text())["scenarios"]
    for key, (tariff_base, _) in SCENARIO_NAMES.items():
        assert scenarios[f"{SEGMENT_PREFIX}{key}_uncalibrated"]["tariff_base"] == tariff_base, key


def human_size(n_bytes: int) -> str:
    for unit, scale in (("GB", 1e9), ("MB", 1e6), ("KB", 1e3)):
        if n_bytes >= scale:
            return f"{n_bytes / scale:,.1f} {unit}"
    return f"{n_bytes} bytes"


def describe(path: str) -> tuple[str, str, str, str, str]:
    """(folder, scenario, homes, file, description) for a public path."""
    parts = path.split("/")
    if parts[:2] == ["outputs", "master"]:
        segment, table = parts[2], parts[3]
        scenario, homes, _ = parse_segment(segment)
        return (
            f"outputs/master/{segment}",
            scenario,
            homes,
            f"{table}/{'/'.join(parts[4:])}",
            MASTER_DESCRIPTIONS[table],
        )
    if parts[:2] == ["outputs", "runs"]:
        scenario, homes, charges = parse_segment(parts[2])
        description = RUN_DESCRIPTIONS[parts[3]]
        if not parts[3].startswith("billing_kwh"):
            description = f"{description}; {charges}"
        return "/".join(parts[:3]), scenario, homes, parts[3], description
    if parts[:2] == ["inputs", "config"]:
        return "/".join(parts[:-1]), "", "", parts[-1], CONFIG_DESCRIPTIONS[parts[2]]
    return "/".join(parts[:-1]), "", "", parts[-1], INPUT_DESCRIPTIONS[path]


def read_rows(path_manifest: Path) -> list[FileRow]:
    with path_manifest.open() as f:
        manifest = list(csv.DictReader(f))
    rows = []
    for m in manifest:
        assert m["url"] == f"{URL_BASE}/{m['path']}", m["path"]
        rows.append(FileRow(*describe(m["path"]), human_size(int(m["bytes"])), m["url"]))
    scenario_order = [name for _, name in SCENARIO_NAMES.values()]
    return sorted(
        rows,
        key=lambda r: (
            not r.folder.startswith("outputs"),
            not r.folder.startswith("outputs/master"),
            scenario_order.index(r.scenario) if r.scenario else 0,
            r.homes != STAGE_NAMES["precalc"],
            r.folder,
            r.file,
        ),
    )


def write_xlsx(rows: list[FileRow], path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    assert ws is not None
    ws.title = "files"
    ws["A1"] = TITLE
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = SUBTITLE
    ws["A3"] = f"Folder README: {URL_BASE}/README.md"
    header = ["Rate scenario", "Modeled homes", "Description", "Size", "Download link", "Folder", "File"]
    wrap = Alignment(wrap_text=True, vertical="top")
    for col, name in enumerate(header, 1):
        ws.cell(row=5, column=col, value=name).font = Font(bold=True)
    for i, r in enumerate(rows, 6):
        ws.cell(row=i, column=1, value=r.scenario).alignment = wrap
        ws.cell(row=i, column=2, value=r.homes).alignment = wrap
        ws.cell(row=i, column=3, value=r.description).alignment = wrap
        ws.cell(row=i, column=4, value=r.size).alignment = Alignment(horizontal="right", vertical="top")
        link = ws.cell(row=i, column=5, value="Download")
        link.hyperlink = r.url
        link.style = "Hyperlink"
        ws.cell(row=i, column=6, value=r.folder).alignment = Alignment(vertical="top")
        ws.cell(row=i, column=7, value=r.file).alignment = Alignment(vertical="top")
    ws.freeze_panes = "A6"
    ws.auto_filter.ref = f"A5:G{5 + len(rows)}"
    for col, width in zip("ABCDEFG", (55, 18, 55, 11, 13, 70, 50), strict=True):
        ws.column_dimensions[col].width = width
    wb.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--path-staged-dir", type=Path, default=PATH_REPORT / "cache" / "ciec_11c_share")
    parser.add_argument("--upload-xlsx", action="store_true", help="upload the workbook to the CIEC Drive folder")
    args = parser.parse_args()

    check_scenarios(args.path_staged_dir / "inputs" / "config" / "scenarios" / "pipeline_ct_eversource.yaml")
    rows = read_rows(args.path_staged_dir / "MANIFEST.csv")
    path_xlsx = args.path_staged_dir / XLSX_NAME
    write_xlsx(rows, path_xlsx)
    print(f"{len(rows)} files -> {path_xlsx}")

    if args.upload_xlsx:
        from build_ciec_1a_workbook import DRIVE_FOLDER_ID, upload_xlsx

        print(upload_xlsx(path_xlsx, DRIVE_FOLDER_ID, XLSX_NAME))


if __name__ == "__main__":
    main()
