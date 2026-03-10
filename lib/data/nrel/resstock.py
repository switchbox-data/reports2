"""Load ResStock load curves for a specific utility from S3."""

from __future__ import annotations

import polars as pl


def scan_load_curves_for_utility(
    path_resstock_release: str,
    state: str,
    upgrade: str,
    utility: str,
    load_curve_type: str = "hourly",
) -> pl.LazyFrame:
    """Scan load curves for buildings belonging to a specific utility.

    Reads ``metadata_utility`` to get bldg_ids, constructs per-building paths,
    and passes them to ``scan_parquet`` (no directory listing of irrelevant files).
    """
    base = path_resstock_release.rstrip("/")
    meta_path = f"{base}/metadata_utility/state={state}/utility_assignment.parquet"
    bldg_ids: list[int] = (
        pl.scan_parquet(meta_path)
        .filter(pl.col("sb.electric_utility") == utility)
        .select("bldg_id")
        .collect()
        .to_series()
        .to_list()
    )
    if not bldg_ids:
        raise ValueError(f"No buildings for utility '{utility}' in {meta_path}")
    load_dir = f"{base}/load_curve_{load_curve_type}/state={state}/upgrade={upgrade}"
    upgrade_int = str(int(upgrade))
    paths = [f"{load_dir}/{bid}-{upgrade_int}.parquet" for bid in bldg_ids]
    return pl.scan_parquet(paths)
