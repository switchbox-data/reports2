"""Shared plotting and aggregation utilities for HP rate notebooks.

This file intentionally lives in ``rate-utils/`` (not a Python package yet).
Notebooks import it by adding the ``rate-utils`` directory to ``sys.path``.
"""

from __future__ import annotations

import io
import json
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd

if TYPE_CHECKING:
    import polars as pl


def _parse_s3_uri(uri: str) -> tuple[str, str]:
    """Split an ``s3://bucket/key`` URI into ``(bucket, key)``."""
    without_prefix = uri[len("s3://"):]
    bucket, _, key = without_prefix.partition("/")
    return bucket, key


def read_s3_csv(s3_uri: str, **kwargs) -> pd.DataFrame:
    """Read a CSV from an S3 URI using boto3 (no s3fs required).

    Extra keyword arguments are forwarded to ``pd.read_csv``.
    """
    import boto3

    bucket, key = _parse_s3_uri(s3_uri)
    response = boto3.client("s3").get_object(Bucket=bucket, Key=key)
    return pd.read_csv(io.BytesIO(response["Body"].read()), **kwargs)


def read_s3_json(s3_uri: str) -> dict:
    """Read a JSON object from an S3 URI using boto3 (no s3fs required)."""
    import boto3

    bucket, key = _parse_s3_uri(s3_uri)
    response = boto3.client("s3").get_object(Bucket=bucket, Key=key)
    return json.loads(response["Body"].read())


def find_latest_run_dir(run_base: str, run_name: str) -> str:
    """Return the S3 URI of the most recent output directory matching ``run_name``.

    Output directories are named ``{YYYYMMDD_HHMMSS}_{run_name}``. This
    function lists all directories under ``run_base`` whose name ends with
    ``_{run_name}``, then returns the lexicographically latest one (the
    timestamp prefix ensures recency ordering).

    Raises ``FileNotFoundError`` if no matching directory is found.
    """
    import boto3

    bucket, prefix = _parse_s3_uri(run_base)
    prefix = prefix.rstrip("/") + "/"
    suffix = f"_{run_name}/"

    paginator = boto3.client("s3").get_paginator("list_objects_v2")
    matching: list[str] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
        for entry in page.get("CommonPrefixes", []):
            dir_prefix = entry["Prefix"]
            dir_name = dir_prefix[len(prefix):].rstrip("/")
            if dir_name.endswith(f"_{run_name}"):
                matching.append(dir_name)

    if not matching:
        raise FileNotFoundError(
            f"No output directory matching run_name={run_name!r} found under {run_base}. "
            "Re-run the scenario to generate outputs."
        )

    latest = sorted(matching)[-1]
    return f"{run_base.rstrip('/')}/{latest}"


DIST_PARAM_KEYS = (
    "annual_future_distr_costs",
    "distr_peak_hrs",
    "nc_ratio_baseline",
)


def resolve_dist_params(defaults: dict, candidates: list[Path] | None = None) -> dict:
    """Return distribution-cost parameters from the first existing JSON candidate."""
    candidates = candidates or []
    for path in candidates:
        if not path.exists():
            continue
        with open(path) as f:
            loaded = json.load(f)
        return {key: loaded[key] for key in DIST_PARAM_KEYS}
    return defaults


def choose_latest_run(run_root: Path) -> Path:
    """Return the lexicographically latest run directory under ``run_root``."""
    runs = sorted(path for path in run_root.iterdir() if path.is_dir())
    if not runs:
        raise FileNotFoundError(f"No run directories found in {run_root}")
    return runs[-1]


def load_dist_mc_from_run(run_dir: Path | str) -> pd.Series:
    """Load distribution_marginal_costs.csv saved by run_scenario.py into a pandas Series.

    The CSV is written by run_scenario.py with index name 'time' and a single
    column 'Marginal Distribution Costs ($/kWh)'.

    ``run_dir`` may be a local ``Path`` or an S3 URI string (``s3://...``).
    S3 URIs are read via boto3 (no s3fs required).
    """
    csv_path = f"{str(run_dir).rstrip('/')}/distribution_marginal_costs.csv"
    if csv_path.startswith("s3://"):
        df = read_s3_csv(csv_path, index_col="time", parse_dates=True)
    else:
        df = pd.read_csv(csv_path, index_col="time", parse_dates=True)
    series = df.iloc[:, 0].rename("Marginal Distribution Costs ($/kWh)")
    if series.index.tz is None:
        series.index = series.index.tz_localize("EST")
    else:
        series.index = series.index.tz_convert("EST")
    return series


def force_timezone_est(df: pd.DataFrame, time_col: str = "time") -> pd.DataFrame:
    """Ensure a pandas datetime column is timezone-aware and converted to EST."""
    out = df.copy()
    out[time_col] = pd.to_datetime(out[time_col], errors="coerce")
    if out[time_col].dt.tz is None:
        out[time_col] = out[time_col].dt.tz_localize("EST")
    else:
        out[time_col] = out[time_col].dt.tz_convert("EST")
    return out


def force_timezone_est_polars(frame: pl.DataFrame, timestamp_col: str = "timestamp") -> pl.DataFrame:
    """Ensure a Polars datetime column is timezone-aware and converted to EST."""
    import polars as pl

    if timestamp_col not in frame.columns:
        raise ValueError(f"{timestamp_col} not found in frame columns")

    dtype = frame.schema[timestamp_col]
    if isinstance(dtype, pl.Datetime) and dtype.time_zone is not None:
        expr = pl.col(timestamp_col).dt.convert_time_zone("EST")
    else:
        expr = pl.col(timestamp_col).cast(pl.Datetime, strict=False).dt.replace_time_zone("EST")
    return frame.with_columns(expr.alias(timestamp_col))


def build_bldg_id_to_load_filepath(path_resstock_loads: Path, building_ids: list[int]) -> dict[int, Path]:
    """Map requested building IDs to their ResStock load parquet paths."""
    bldg_set = {int(i) for i in building_ids}
    mapping: dict[int, Path] = {}
    for parquet_file in path_resstock_loads.glob("*.parquet"):
        try:
            bldg_id = int(parquet_file.stem.split("-")[0])
        except ValueError:
            continue
        if bldg_id in bldg_set:
            mapping[bldg_id] = parquet_file
    missing = bldg_set - set(mapping)
    if missing:
        print(f"Warning: missing load files for {len(missing)} building IDs")
    return mapping


_CROSS_SUBSIDY_WEIGHTED_COLS: dict[str, str] = {
    "BAT_vol": "BAT_vol_weighted_avg",
    "BAT_peak": "BAT_peak_weighted_avg",
    "BAT_percustomer": "BAT_percustomer_weighted_avg",
    "customer_level_residual_share_volumetric": "residual_vol_weighted_avg",
    "customer_level_residual_share_peak": "residual_peak_weighted_avg",
    "customer_level_residual_share_percustomer": "residual_percustomer_weighted_avg",
    "Annual": "Annual_bill_weighted_avg",
    "customer_level_economic_burden": "Economic_burden_weighted_avg",
}


def summarize_cross_subsidy(cross: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    """Compute weighted cross-subsidy metrics for HP and Non-HP groups."""
    merged = cross.merge(
        metadata[["bldg_id", "postprocess_group.has_hp", "weight"]],
        on=["bldg_id", "weight"],
        how="left",
    )

    rows = []
    for has_hp, group in merged.groupby("postprocess_group.has_hp"):
        weight_sum = group["weight"].sum()
        row = {
            "postprocess_group.has_hp": has_hp,
            "customers_weighted": weight_sum,
            "group": "HP" if has_hp else "Non-HP",
        }
        for source_col, output_col in _CROSS_SUBSIDY_WEIGHTED_COLS.items():
            row[output_col] = (group[source_col] * group["weight"]).sum() / weight_sum
        rows.append(row)

    return pd.DataFrame(rows)


def summarize_cross_subsidy_by_heating_type(
    cross: pd.DataFrame, metadata: pd.DataFrame
) -> pd.DataFrame:
    """Compute weighted cross-subsidy metrics grouped by ``postprocess_group.heating_type``.

    Returns one row per heating type with the same weighted-average columns as
    ``summarize_cross_subsidy``, plus a ``group`` column equal to the heating type label.
    """
    merged = cross.merge(
        metadata[["bldg_id", "postprocess_group.heating_type", "weight"]],
        on=["bldg_id", "weight"],
        how="left",
    )

    rows = []
    for heating_type, group in merged.groupby("postprocess_group.heating_type"):
        weight_sum = group["weight"].sum()
        row = {
            "postprocess_group.heating_type": heating_type,
            "customers_weighted": weight_sum,
            "group": str(heating_type),
        }
        for source_col, output_col in _CROSS_SUBSIDY_WEIGHTED_COLS.items():
            row[output_col] = (group[source_col] * group["weight"]).sum() / weight_sum
        rows.append(row)

    return pd.DataFrame(rows).sort_values("customers_weighted", ascending=False).reset_index(drop=True)


def build_cost_mix(cross_summary: pd.DataFrame) -> pd.DataFrame:
    """Build long-form marginal vs residual cost totals by customer group.

    If ``cross_summary`` contains a ``run_label`` column it is preserved as an
    additional id column throughout the melt operations so callers can facet by run.
    """
    residual_labels = {
        "residual_vol_weighted_avg": "Volumetric residual",
        "residual_peak_weighted_avg": "Peak residual",
        "residual_percustomer_weighted_avg": "Per-customer residual",
    }

    extra_ids = [c for c in ("run_label",) if c in cross_summary.columns]

    cost_mix = (
        cross_summary[
            [
                *extra_ids,
                "group",
                "customers_weighted",
                "Economic_burden_weighted_avg",
                *residual_labels.keys(),
            ]
        ]
        .melt(
            id_vars=[*extra_ids, "group", "customers_weighted", "Economic_burden_weighted_avg"],
            value_vars=list(residual_labels.keys()),
            var_name="benchmark_key",
            value_name="residual_usd_per_customer_year",
        )
        .assign(
            benchmark=lambda d: d["benchmark_key"].map(residual_labels),
            marginal_usd_per_customer_year=lambda d: d["Economic_burden_weighted_avg"],
            weighted_customers=lambda d: d["customers_weighted"],
        )
        [[*extra_ids, "group", "benchmark", "weighted_customers",
          "marginal_usd_per_customer_year", "residual_usd_per_customer_year"]]
    )

    totals = cost_mix.assign(
        marginal_total_usd_per_year=lambda d: d["marginal_usd_per_customer_year"] * d["weighted_customers"],
        residual_total_usd_per_year=lambda d: d["residual_usd_per_customer_year"] * d["weighted_customers"],
    )

    return (
        totals.melt(
            id_vars=[*extra_ids, "group", "benchmark"],
            value_vars=["marginal_total_usd_per_year", "residual_total_usd_per_year"],
            var_name="cost_source_key",
            value_name="usd_total_per_year",
        )
        .assign(
            cost_source=lambda d: d["cost_source_key"].map(
                {
                    "marginal_total_usd_per_year": "Marginal (economic burden)",
                    "residual_total_usd_per_year": "Residual allocation",
                }
            ),
            musd_total_per_year=lambda d: d["usd_total_per_year"] / 1e6,
        )
        [[*extra_ids, "group", "benchmark", "cost_source", "musd_total_per_year"]]
    )


def build_hourly_group_loads(raw_load_elec: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    """Aggregate weighted hourly electricity load by HP flag and total."""
    weighted = raw_load_elec[["electricity_net"]].reset_index().merge(
        metadata[["bldg_id", "postprocess_group.has_hp", "weight"]],
        on="bldg_id",
        how="left",
    )
    weighted["weighted_load_kwh"] = weighted["electricity_net"] * weighted["weight"]

    hourly = (
        weighted.groupby(["time", "postprocess_group.has_hp"], as_index=False)["weighted_load_kwh"]
        .sum()
        .pivot(index="time", columns="postprocess_group.has_hp", values="weighted_load_kwh")
        .rename(columns={False: "non_hp_load_kwh", True: "hp_load_kwh"})
        .fillna(0.0)
        .sort_index()
    )
    hourly["total_load_kwh"] = hourly["non_hp_load_kwh"] + hourly["hp_load_kwh"]
    return hourly


def build_cross_components(cross_summary: pd.DataFrame) -> pd.DataFrame:
    """Build benchmark component contributions for charting cross-subsidy impacts."""
    component_labels = {
        "BAT_vol_weighted_avg": "Volumetric benchmark",
        "BAT_peak_weighted_avg": "Peak benchmark",
        "BAT_percustomer_weighted_avg": "Per-customer benchmark",
    }
    return (
        cross_summary.melt(
            id_vars=["group", "customers_weighted"],
            value_vars=list(component_labels.keys()),
            var_name="component",
            value_name="weighted_avg_bat_usd_per_customer_year",
        )
        .assign(
            component_label=lambda d: d["component"].map(component_labels),
            component_transfer_total_musd_per_year=lambda d: (
                d["weighted_avg_bat_usd_per_customer_year"] * d["customers_weighted"] / 1e6
            ),
        )
    )


def summarize_positive_distribution_hours(
    hourly: pd.DataFrame,
    customer_count_map: dict[str, float],
) -> pd.DataFrame:
    """Summarize per-customer load behavior in positive marginal distribution-cost hours."""
    rows = []
    for col, label in [("hp_load_kwh", "HP"), ("non_hp_load_kwh", "Non-HP")]:
        customer_count = float(customer_count_map[label])
        annual = hourly[col].sum()
        positive = hourly.loc[hourly["mdc_positive"], col].sum()
        rows.append(
            {
                "group": label,
                "weighted_customers": customer_count,
                "annual_load_mwh_per_customer": (annual / customer_count) / 1000,
                "positive_dist_cost_hours_load_mwh_per_customer": (positive / customer_count) / 1000,
                "share_of_annual_load_in_positive_dist_cost_hours": positive / annual,
                "avg_hourly_load_kwh_during_positive_dist_hours": (
                    hourly.loc[hourly["mdc_positive"], col].mean() / customer_count
                ),
                "avg_hourly_load_kwh_during_zero_dist_hours": (
                    hourly.loc[~hourly["mdc_positive"], col].mean() / customer_count
                ),
            }
        )
    return pd.DataFrame(rows)


def build_tariff_components(
    hourly: pd.DataFrame,
    cross_summary: pd.DataFrame,
    fixed_monthly: float,
    vol_rate: float,
) -> pd.DataFrame:
    """Compute annual fixed and volumetric charges collected by customer group."""
    group_load = pd.DataFrame(
        {
            "group": ["Non-HP", "HP"],
            "annual_load_kwh": [hourly["non_hp_load_kwh"].sum(), hourly["hp_load_kwh"].sum()],
        }
    )

    tariff_components = group_load.merge(
        cross_summary[["group", "customers_weighted"]].rename(
            columns={"customers_weighted": "weighted_customers"}
        ),
        on="group",
        how="left",
    )
    tariff_components["annual_fixed_charge_collected_usd"] = (
        fixed_monthly * 12 * tariff_components["weighted_customers"]
    )
    tariff_components["annual_volumetric_charge_collected_usd"] = (
        vol_rate * tariff_components["annual_load_kwh"]
    )
    return tariff_components
