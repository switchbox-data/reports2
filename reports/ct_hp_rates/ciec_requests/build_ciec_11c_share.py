"""Stage the CAIRO input files shared in response to CIEC-11(c).

CIEC-11(c) asks for every CAIRO input and output file used in the Velez Direct
Testimony that wasn't already provided (Ex. JPV-3, Ex. JPV-4, CIEC-1). The
outputs are copied server-side from ``data.sb`` in the upload step; this script
builds the inputs locally so they can be uploaded and checksummed:

- ResStock metadata (upgrades 00 and 02) and the utility assignment, as-is
- hourly loads for the Eversource buildings, one file per upgrade, with the
  columns CAIRO reads (``utils/mid/patches.py::_return_loads_combined``) plus
  oil and propane, which the combined bills table prices by month
- the two marginal cost files CAIRO reads, checked against the sha256 that
  every run recorded in ``marginal_costs_used.json``
- CT residential heating fuel prices for 2024, and CPI
- the config files the runs read, from rate-design-platform at ``e97a3ca``
  (every run billed exactly these tariffs; see the CIEC-11(c) plan)

Writes ``staged_inputs.csv`` (path, source, bytes, sha256, description) beside
the files, for the manifest.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import boto3
import polars as pl

PATH_HERE = Path(__file__).resolve().parent
PATH_REPORT = PATH_HERE.parent
PATH_REPO = PATH_REPORT.parents[1]

RDP_PIN = "e97a3ca"
UTILITY = "ct_eversource"
N_BLDGS = 3539
HOURS = 8760
BUCKET = "data.sb"
BATCH_PREFIX = "switchbox/cairo/outputs/hp_rates/ct/ct_eversource/ct_20261015_a"
PATH_CT_CONFIG = "rate_design/hp_rates/ct/config/"
PATH_POST_DATA = "utils/post/data/"

SCENARIOS = {
    "r1": ("160225", "160326", "160414", "160511"),
    "r6": ("160633", "160804", "160924", "161051"),
    "r6_ratemc": ("161220", "161357", "161520", "161649"),
    "r6_fixed_ratemc": ("161811", "161941", "162059", "162229"),
    "r6_ratemc_trans": ("162351", "162520", "162643", "162810"),
    "r6_fixed_ratemc_trans": ("162933", "163106", "163235", "163409"),
    "r6_ratemc_mfc0_trans": ("163533", "163702", "163821", "163948"),
    "icos_fair_flat": ("164040", "164139", "164228", "164326"),
    "icos_fair_seasonal": ("164420", "164519", "164607", "164704"),
}
RUN_SUFFIXES = ("precalc_delivery", "precalc_supply", "calibrated_delivery", "calibrated_supply")
RUNS = [
    f"20261015_{ts}_ct_ct_eversource_default_ry1_{scenario}_uncalibrated_{suffix}"
    for scenario, stamps in SCENARIOS.items()
    for ts, suffix in zip(stamps, RUN_SUFFIXES, strict=True)
]

# Electricity, PV and gas are what CAIRO reads. Oil and propane feed post-processing, which reads
# NREL's monthly load files; those equal these hourly columns summed by ``month`` (to ~1e-11 kWh).
HOURLY_COLUMNS = [
    "bldg_id",
    "timestamp",
    "month",
    "out.electricity.total.energy_consumption",
    "out.electricity.pv.energy_consumption",
    "out.natural_gas.total.energy_consumption",
    "out.fuel_oil.total.energy_consumption",
    "out.propane.total.energy_consumption",
]
MC_KEYS = ("dist_and_sub_tx", "bulk_tx")
PATH_EIA861 = "eia/861/electric_utility_stats/year=2024/state=CT/data.parquet"
PATH_FUEL_PRICES = "eia/heating_fuel_prices"
FUEL_PRICE_YEAR = 2024
# The LMI step read the whole fred/cpi/ folder with FPL year 2026 and took the first 2026 row, which
# comes from this file (ratio 1.292962 to 2019); it reproduces every building's elec_lmi_tier.
PATH_CPI = "fred/cpi/cpiaucsl_2019_2026_20260803.parquet"

# Config the runs used that scenario_settings.json doesn't list.
EXTRA_CONFIG = [
    f"{PATH_CT_CONFIG}scenarios/pipeline_ct_eversource.yaml",
    f"{PATH_CT_CONFIG}scenarios/scenarios_ct_eversource.yaml",
    f"{PATH_CT_CONFIG}rev_requirement/ct_eversource_large_number_rate_case_rate_year_1.yaml",
    f"{PATH_CT_CONFIG}rev_requirement/top-ups/monthly_rates/ct_eversource_rate1_proposed_monthly_rates_ry1.yaml",
    f"{PATH_POST_DATA}ct_lidr.yaml",
    f"{PATH_POST_DATA}fpl_guidelines.yaml",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


class Stager:
    """Writes files under ``inputs/`` and records one manifest row per file."""

    def __init__(self, path_output_dir: Path) -> None:
        self.root = path_output_dir
        self.rows: list[dict[str, Any]] = []
        self.s3 = boto3.client("s3")

    def dest(self, rel: str) -> Path:
        path = self.root / "inputs" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def record(self, rel: str, source: str, description: str) -> Path:
        path = self.root / "inputs" / rel
        self.rows.append(
            {
                "path": f"inputs/{rel}",
                "source": source,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "description": description,
            }
        )
        print(f"  inputs/{rel}")
        return path

    def run_json(self, run: str, name: str) -> dict[str, Any]:
        body = self.s3.get_object(Bucket=BUCKET, Key=f"{BATCH_PREFIX}/{run}/{name}")["Body"]
        return json.loads(body.read())

    def download(self, key: str, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.s3.download_file(BUCKET, key, str(path))

    def list_keys(self, prefix: str) -> list[str]:
        paginator = self.s3.get_paginator("list_objects_v2")
        return [
            obj["Key"] for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix) for obj in page.get("Contents", [])
        ]

    def write_manifest(self) -> None:
        path = self.root / "staged_inputs.csv"
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["path", "source", "bytes", "sha256", "description"])
            writer.writeheader()
            writer.writerows(self.rows)
        print(f"Wrote {path} ({len(self.rows)} files)")


def repo_relative(path: str) -> str:
    """``/.../rate-design-platform/rate_design/hp_rates/...`` -> ``rate_design/hp_rates/...``."""
    return path[path.index("rate_design/hp_rates/") :]


def check_settings(settings: dict[str, dict[str, Any]], path_resstock_release: Path) -> None:
    """Every run used the expected ResStock files, so the staged copies are the ones CAIRO read."""
    for run, s in settings.items():
        upgrade = "00" if "_precalc_" in run else "02"
        assert s["utility"] == UTILITY, run
        assert s["path_resstock_metadata"] == str(
            path_resstock_release / f"metadata/state=CT/upgrade={upgrade}/metadata-sb.parquet"
        ), run
        assert s["path_resstock_loads"] == str(
            path_resstock_release / f"load_curve_hourly/state=CT/upgrade={upgrade}"
        ), run
        assert s["path_utility_assignment"] == str(
            path_resstock_release / "metadata_utility/state=CT/utility_assignment.parquet"
        ), run
        # Configured but never read: CAIRO uses EIA-861 only when there is no customer_count_override.
        assert s["path_electric_utility_stats"] == f"s3://{BUCKET}/{PATH_EIA861}", run
        assert s["customer_count_override"], run


def stage_config(stager: Stager, settings: dict[str, dict[str, Any]], path_rdp: Path) -> None:
    """Config files at RDP_PIN: every tariff and tariff map a run read, plus EXTRA_CONFIG."""
    paths: set[str] = set(EXTRA_CONFIG)
    for s in settings.values():
        paths.update(repo_relative(p) for p in s["path_tariffs_electric"].values())
        paths.update(repo_relative(p) for p in s["path_tariffs_gas"].values())
        paths.add(repo_relative(s["path_tariff_maps_electric"]))
        paths.add(repo_relative(s["path_tariff_maps_gas"]))

    counts = {
        "tariffs/electric/": 18,
        "tariff_maps/electric/": 18,
        "tariffs/gas/": 8,
        "tariff_maps/gas/": 2,
    }
    for folder, expected in counts.items():
        n = sum(p.startswith(f"{PATH_CT_CONFIG}{folder}") for p in paths)
        assert n == expected, f"{folder}: {n} files, expected {expected}"

    for repo_path in sorted(paths):
        content = subprocess.run(
            ["git", "-C", str(path_rdp), "show", f"{RDP_PIN}:{repo_path}"],
            capture_output=True,
            check=True,
        ).stdout
        if repo_path.startswith(PATH_CT_CONFIG):
            rel = f"config/{repo_path.removeprefix(PATH_CT_CONFIG)}"
        else:
            rel = f"config/postprocessing/{repo_path.removeprefix(PATH_POST_DATA)}"
        stager.dest(rel).write_bytes(content)
        stager.record(rel, f"rate-design-platform@{RDP_PIN}:{repo_path}", "Run configuration")

    gas_tariffs = {Path(p).stem for p in paths if p.startswith(f"{PATH_CT_CONFIG}tariffs/gas/")}
    for upgrade in ("00", "02"):
        gas_map = pl.read_csv(stager.root / f"inputs/config/tariff_maps/gas/{UTILITY}_u{upgrade}.csv")
        missing = set(gas_map["tariff_key"].unique()) - gas_tariffs
        assert not missing, f"gas map u{upgrade} uses unpublished tariffs: {missing}"


def stage_marginal_costs(stager: Stager, mc_used: dict[str, dict[str, Any]]) -> None:
    """The two hourly marginal cost files CAIRO reads; all 36 runs must agree on path and sha256."""
    for key in MC_KEYS:
        recorded = {(m["marginal_costs"][key]["path"], m["marginal_costs"][key]["sha256"]) for m in mc_used.values()}
        assert len(recorded) == 1, f"{key}: runs disagree: {recorded}"
        ((uri, expected_sha),) = recorded
        rel = f"marginal_costs/{key}.parquet"
        stager.download(uri.removeprefix(f"s3://{BUCKET}/"), stager.dest(rel))
        assert sha256(stager.dest(rel)) == expected_sha, f"{key}: sha256 differs from marginal_costs_used.json"
        stager.record(rel, uri, f"Hourly {key} marginal costs read by CAIRO")


def stage_resstock(stager: Stager, path_resstock_release: Path) -> None:
    """Metadata as-is; hourly loads consolidated for the Eversource buildings."""
    path_assignment = path_resstock_release / "metadata_utility/state=CT/utility_assignment.parquet"
    for upgrade in ("00", "02"):
        src = path_resstock_release / f"metadata/state=CT/upgrade={upgrade}/metadata-sb.parquet"
        rel = f"resstock/metadata_upgrade{upgrade}.parquet"
        shutil.copy2(src, stager.dest(rel))
        stager.record(rel, str(src), f"ResStock building metadata, upgrade {upgrade}")
    shutil.copy2(path_assignment, stager.dest("resstock/utility_assignment.parquet"))
    stager.record(
        "resstock/utility_assignment.parquet", str(path_assignment), "Electric and gas utility of each building"
    )

    bldg_ids = (
        pl.read_parquet(path_assignment, columns=["bldg_id", "sb.electric_utility"])
        .filter(pl.col("sb.electric_utility") == UTILITY)["bldg_id"]
        .sort()
        .to_list()
    )
    assert len(bldg_ids) == N_BLDGS, f"{len(bldg_ids)} Eversource buildings, expected {N_BLDGS}"

    for upgrade in ("00", "02"):
        load_dir = path_resstock_release / f"load_curve_hourly/state=CT/upgrade={upgrade}"
        paths = [load_dir / f"{bldg_id}-{int(upgrade)}.parquet" for bldg_id in bldg_ids]
        rel = f"resstock/loads_hourly_eversource_upgrade{upgrade}.parquet"
        # Streams without a global sort: files are listed in bldg_id order and each is in timestamp order.
        pl.scan_parquet(paths).select(HOURLY_COLUMNS).sink_parquet(stager.dest(rel), compression="zstd")
        written = (
            pl.scan_parquet(stager.dest(rel))
            .select(
                pl.len().alias("rows"),
                pl.col("bldg_id").n_unique().alias("bldgs"),
                (pl.col("bldg_id").diff().fill_null(0) >= 0).all().alias("bldg_order"),
                ((pl.col("timestamp").diff() > pl.duration(hours=0)) | (pl.col("bldg_id").diff() != 0))
                .fill_null(True)
                .all()
                .alias("time_order"),
            )
            .collect()
        )
        assert written.row(0) == (N_BLDGS * HOURS, N_BLDGS, True, True), f"{rel}: {written.row(0)}"
        stager.record(
            rel, str(load_dir), f"ResStock hourly loads (kWh), {N_BLDGS} Eversource buildings, upgrade {upgrade}"
        )


def stage_public_data(stager: Stager) -> None:
    """CT heating fuel prices and CPI, which post-processing read."""
    with tempfile.TemporaryDirectory() as tmp:
        for product in ("heating_oil", "propane"):
            prefix = f"{PATH_FUEL_PRICES}/product={product}/year={FUEL_PRICE_YEAR}/"
            keys = stager.list_keys(prefix)
            assert keys, f"no fuel prices under {prefix}"
            for key in keys:
                stager.download(key, Path(tmp) / key)
        prices = (
            pl.scan_parquet(f"{tmp}/{PATH_FUEL_PRICES}/**/*.parquet", hive_partitioning=True)
            .filter((pl.col("state") == "CT") & (pl.col("price_type") == "residential"))
            .sort("product", "month")
            .collect()
        )
    assert prices.height > 0, "no CT residential fuel prices"
    rel = f"postprocessing/heating_fuel_prices_ct_{FUEL_PRICE_YEAR}.parquet"
    prices.write_parquet(stager.dest(rel))
    stager.record(
        rel,
        f"s3://{BUCKET}/{PATH_FUEL_PRICES}/ (state=CT, year={FUEL_PRICE_YEAR}, residential)",
        "EIA residential heating oil and propane prices used for oil and propane bills",
    )

    rel = f"postprocessing/{Path(PATH_CPI).name}"
    stager.download(PATH_CPI, stager.dest(rel))
    stager.record(
        rel,
        f"s3://{BUCKET}/{PATH_CPI}",
        "FRED CPI-U (CPIAUCSL); the 2026/2019 ratio inflates ResStock incomes for LMI eligibility",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--path-output-dir", type=Path, default=PATH_REPORT / "cache" / "ciec_11c_share")
    parser.add_argument(
        "--path-resstock-release", type=Path, default=Path("/ebs/data/nrel/resstock/res_2024_amy2018_2_sb")
    )
    parser.add_argument("--path-rdp", type=Path, default=PATH_REPO.parent / "rate-design-platform")
    args = parser.parse_args()

    if (args.path_output_dir / "inputs").exists():
        shutil.rmtree(args.path_output_dir / "inputs")
    stager = Stager(args.path_output_dir)

    print(f"Reading scenario_settings.json and marginal_costs_used.json from {len(RUNS)} runs")
    settings = {run: stager.run_json(run, "scenario_settings.json") for run in RUNS}
    mc_used = {run: stager.run_json(run, "marginal_costs_used.json") for run in RUNS}
    check_settings(settings, args.path_resstock_release)

    print("Config")
    stage_config(stager, settings, args.path_rdp)
    print("Marginal costs")
    stage_marginal_costs(stager, mc_used)
    print("ResStock")
    stage_resstock(stager, args.path_resstock_release)
    print("Fuel prices and CPI")
    stage_public_data(stager)
    stager.write_manifest()


if __name__ == "__main__":
    main()
