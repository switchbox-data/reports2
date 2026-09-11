"""Generalized rate-case analysis functions, shared across states/batches/scenarios.

These functions read CAIRO's Prefect-produced master tables (see the
rate-design-platform AGENTS.md "Master tables" section and
https://github.com/switchbox-data/rate-design-platform/pull/503 for how they're
built) and compute the statistics rate-case reports need: bill-change incidence,
heat-pump delivery over/underpayment (BAT), representative-household bill
decomposition, and tariff introspection.

Every function is parameterized by ``state``, ``batch``, and ``scenario`` (never
hardcoded to one state or run) so the same code works for today's ``default``
schedule and for scenarios that don't exist yet (e.g. a future ``hp_flat_*``
design) without changes.

Terminology, following the new Prefect orchestration (no more numbered runs):

- A **scenario** is a named tariff design (e.g. ``"default"``,
  ``"hp_seasonal_percustomer_passthrough"``).
- A **stage** is either ``"precalc"`` (ResStock upgrade 00, today's mixed
  heating population, un-recalibrated tariff) or ``"calibrated"`` (ResStock
  upgrade 02, buildings retrofitted to HP, tariff recalibrated to meet revenue
  requirements).
- A **segment** is ``"{scenario}_{stage}"`` — the directory name CAIRO's
  post-processing writes master tables under.

Critical fact from PR #503: cross-subsidy/BAT metrics are only reliable at the
``precalc`` stage. Calibrated-stage BAT is inflated by a deliberately oversized
revenue requirement — bills themselves are correct at that stage, but
BAT/``residual_share`` is not. Every BAT-reading function here reads
``{scenario}_precalc`` only.
"""

from __future__ import annotations

import math
import warnings
from collections.abc import Sequence
from typing import TYPE_CHECKING, cast

import matplotlib.patches as mpatches
import matplotlib.pyplot as pyplot
import numpy as np
import polars as pl

if TYPE_CHECKING:
    import polars as pl
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from plotnine import ggplot

S3_BASE = "s3://data.sb/switchbox/cairo/outputs/hp_rates"
MONTH_ORDER = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# --- Loading -----------------------------------------------------------------


def segment_name(scenario: str, stage: str) -> str:
    """Return the ``{scenario}_{stage}`` segment name CAIRO writes master tables under."""
    return f"{scenario}_{stage}"


def master_table_uri(
    state: str,
    batch: str,
    segment: str,
    dataset: str,
    *,
    all_utilities: bool = True,
    utility: str | None = None,
) -> str:
    """Return the S3 URI for a master-table dataset within a batch segment.

    Only the ``all_utilities`` master tables (Hive-partitioned by
    ``sb.electric_utility``, one row per building) are wired up here — they are
    the primary data source per the rate-design-platform AGENTS.md. To scope to
    one utility, filter the loaded frame by ``sb.electric_utility`` instead of
    passing a per-utility path; pass ``utility`` only for documentation/clarity
    at call sites, it doesn't change the URI.
    """
    if not all_utilities:
        raise NotImplementedError(
            "Per-utility raw run paths (with a cairo_ts prefix) aren't wired up here. "
            "Use the all_utilities master tables and filter by `sb.electric_utility` instead."
        )
    del utility  # documentation-only; see docstring
    return f"{S3_BASE}/{state.lower()}/all_utilities/{batch}/{segment}/{dataset}/"


def load_master_bills(state: str, batch: str, segment: str) -> pl.LazyFrame:
    """Load the ``comb_bills_year_target`` master table for one batch segment.

    One row per building per month (Jan-Dec + Annual), incl. ``energy_total_bill``,
    ``postprocess_group.heating_type_v2``, ``postprocess_group.has_hp``, ``weight``.
    """
    return pl.scan_parquet(
        master_table_uri(state, batch, segment, "comb_bills_year_target"),
        hive_partitioning=True,
    )


def load_master_bat(state: str, batch: str, segment: str) -> pl.LazyFrame:
    """Load the ``cross_subsidization_BAT_values`` master table for one batch segment.

    One row per building (annual), incl. ``BAT_percustomer_delivery``,
    ``annual_bill_delivery``, ``postprocess_group.has_hp``, ``weight``.

    Warning: BAT values are only valid at the ``precalc`` stage (see module
    docstring / PR #503). Calibrated-stage BAT is inflated by an oversized
    revenue requirement; don't use ``*_calibrated`` segments for cross-subsidy
    analysis, even though the bills in that segment are correct.
    """
    if not segment.endswith("_precalc"):
        warnings.warn(
            f"Loading BAT from segment {segment!r}, which is not a `_precalc` segment. "
            "Calibrated-stage BAT is inflated and unsuitable for cross-subsidy analysis (see PR #503).",
            stacklevel=2,
        )
    return pl.scan_parquet(
        master_table_uri(state, batch, segment, "cross_subsidization_BAT_values"),
        hive_partitioning=True,
    )


def load_billing_kwh_annual(state: str, utility: str, batch: str, segment: str) -> pl.LazyFrame:
    """Load per-building annual kWh from a CAIRO run's raw ``billing_kwh_annual.parquet``.

    Unlike master bills/BAT (Prefect ``all_utilities`` tables), CAIRO's raw
    per-building kWh export is only written to each individual per-utility run
    directory (with a ``{cairo_ts}_...`` prefix), never promoted to a master
    table. This resolves that run directory via ``list_s3_subdirs`` + ``run_dir``,
    matching on the ``"{utility}_{segment}_delivery"`` suffix -- the kWh export
    only exists in ``_delivery`` runs, not ``_supply`` runs.

    Returns a LazyFrame with ``bldg_id``, ``annual_kwh_grid`` (post-PV-netting
    grid consumption), ``annual_kwh_total`` (pre-PV gross consumption), and
    ``has_pv``.
    """
    from lib.data.s3 import list_s3_subdirs, run_dir

    base = f"{S3_BASE}/{state.lower()}/{utility}/{batch}/"
    subdirs = list_s3_subdirs(base)
    run_path = run_dir(subdirs, name_ends_with=f"{utility}_{segment}_delivery")
    return pl.scan_parquet(f"{run_path}/billing_kwh_annual.parquet")


def load_billing_kwh_8760(state: str, utility: str, batch: str, segment: str) -> pl.LazyFrame:
    """Load per-building hourly kWh from a CAIRO run's ``billing_kwh_8760.parquet``.

    Same run-directory resolution as :func:`load_billing_kwh_annual`. Returns a
    LazyFrame with ``bldg_id``, ``timestamp``, and ``grid_cons_kwh`` (post-PV-
    netting grid consumption, floored at 0).

    Timestamps are returned as-is (UTC in current CAIRO output). Callers that
    join against local-time marginal costs should shift by the appropriate UTC
    offset before joining.
    """
    import polars as pl

    from lib.data.s3 import list_s3_subdirs, run_dir

    base = f"{S3_BASE}/{state.lower()}/{utility}/{batch}/"
    subdirs = list_s3_subdirs(base)
    run_path = run_dir(subdirs, name_ends_with=f"{utility}_{segment}_delivery")
    return pl.scan_parquet(f"{run_path}/billing_kwh_8760.parquet").select("bldg_id", "timestamp", "grid_cons_kwh")


def weighted_avg_hourly(
    kwh_8760: pl.LazyFrame,
    bldg_ids: list[int],
    weights: pl.DataFrame,
) -> pl.DataFrame:
    """Weighted-average hourly load profile for a set of buildings.

    Parameters
    ----------
    kwh_8760
        LazyFrame from :func:`load_billing_kwh_8760` with columns
        ``bldg_id``, ``timestamp``, ``grid_cons_kwh``.
    bldg_ids
        Building IDs to include (one population).
    weights
        DataFrame with ``bldg_id`` and ``weight`` columns.

    Returns
    -------
    pl.DataFrame
        8760-row DataFrame with ``timestamp`` and ``kwh``.
    """
    import polars as pl

    hourly = cast(
        pl.DataFrame,
        kwh_8760.filter(pl.col("bldg_id").is_in(bldg_ids)).collect(),
    ).join(weights.select("bldg_id", "weight"), on="bldg_id")
    return (
        hourly.group_by("timestamp")
        .agg(((pl.col("grid_cons_kwh") * pl.col("weight")).sum() / pl.col("weight").sum()).alias("kwh"))
        .sort("timestamp")
    )


def weighted_avg_monthly(
    kwh_8760: pl.LazyFrame,
    bldg_ids: list[int],
    weights: pl.DataFrame,
) -> pl.DataFrame:
    """Weighted-average monthly kWh for a set of buildings.

    Sums each building's hourly kWh to monthly totals, then takes the weighted
    average across buildings. Replaces notebook-local functions that read
    ``elec_grid_kwh`` from master bills.

    Parameters
    ----------
    kwh_8760
        LazyFrame from :func:`load_billing_kwh_8760`.
    bldg_ids
        Building IDs to include (one population).
    weights
        DataFrame with ``bldg_id`` and ``weight`` columns.

    Returns
    -------
    pl.DataFrame
        12-row DataFrame with ``month_label`` (Enum Jan-Dec) and ``kwh``.
        Compatible with :func:`plot_monthly_load`, :func:`plot_monthly_load_before_after`,
        and :func:`monthly_bill_from_profile`.
    """
    import polars as pl

    monthly_per_bldg = cast(
        pl.DataFrame,
        kwh_8760.filter(pl.col("bldg_id").is_in(bldg_ids))
        .with_columns(pl.col("timestamp").dt.month().alias("_month_num"))
        .group_by("bldg_id", "_month_num")
        .agg(pl.col("grid_cons_kwh").sum().alias("kwh"))
        .collect(),
    ).join(weights.select("bldg_id", "weight"), on="bldg_id")
    month_num_to_label = {i + 1: m for i, m in enumerate(MONTH_ORDER)}
    return (
        monthly_per_bldg.group_by("_month_num")
        .agg(((pl.col("kwh") * pl.col("weight")).sum() / pl.col("weight").sum()).alias("kwh"))
        .sort("_month_num")
        .with_columns(pl.col("_month_num").replace_strict(month_num_to_label).alias("month_label"))
        .select(
            pl.col("month_label").cast(pl.Enum(MONTH_ORDER)),
            "kwh",
        )
    )


def sum_8760_to_monthly(hourly: pl.DataFrame, value_col: str = "kwh") -> pl.DataFrame:
    """Sum an 8760-row hourly series to 12 monthly totals.

    Parameters
    ----------
    hourly
        DataFrame with ``timestamp`` and *value_col*.
    value_col
        Column to sum within each month.

    Returns
    -------
    pl.DataFrame
        12-row DataFrame with ``month_label`` (Enum Jan-Dec) and the summed
        *value_col*.
    """
    import polars as pl

    month_num_to_label = {i + 1: m for i, m in enumerate(MONTH_ORDER)}
    return (
        hourly.with_columns(pl.col("timestamp").dt.month().alias("_month_num"))
        .group_by("_month_num")
        .agg(pl.col(value_col).sum())
        .sort("_month_num")
        .with_columns(pl.col("_month_num").replace_strict(month_num_to_label).alias("month_label"))
        .select(
            pl.col("month_label").cast(pl.Enum(MONTH_ORDER)),
            value_col,
        )
    )


def sum_monthly_peak_offpeak_kwh(
    load_8760: pl.DataFrame,
    mc_8760: pl.DataFrame,
    *,
    utc_offset_hours: int = -5,
) -> pl.DataFrame:
    """Split hourly kWh into peak vs. off-peak and sum to monthly totals.

    An hour is "peak" when either the bulk-transmission or distribution
    marginal cost is positive (same definition used in
    ``analysis.qmd::_pct_mc_peak_hours_in_summer``).

    Parameters
    ----------
    load_8760
        8760-row DataFrame with ``timestamp`` (UTC) and ``kwh`` — a single
        building or population-average hourly profile from
        :func:`weighted_avg_hourly`.
    mc_8760
        DataFrame from :func:`load_delivery_mc_heatmap` with ``timestamp``
        (local), ``mc_bulk_tx``, ``mc_dist_sub_tx``.
    utc_offset_hours
        Hours to shift ``load_8760`` timestamps to align with ``mc_8760``.
        Default ``-5`` converts CAIRO's UTC to Eastern Standard Time.

    Returns
    -------
    pl.DataFrame
        12-row DataFrame with ``month_label`` (Enum Jan-Dec),
        ``kwh_offpeak``, ``kwh_peak``.  The two columns sum to the same
        monthly totals as :func:`weighted_avg_monthly`.
    """
    import polars as pl

    load_local = load_8760.with_columns((pl.col("timestamp") + pl.duration(hours=utc_offset_hours)).alias("timestamp"))
    joined = load_local.join(
        mc_8760.select("timestamp", "mc_bulk_tx", "mc_dist_sub_tx"),
        on="timestamp",
    )
    if joined.height != 8760:
        raise ValueError(
            f"Expected 8760 rows after join, got {joined.height}. Check timestamp alignment between load and MC data."
        )

    month_num_to_label = {i + 1: m for i, m in enumerate(MONTH_ORDER)}
    flagged = joined.with_columns(
        pl.col("timestamp").dt.month().alias("_month_num"),
        ((pl.col("mc_bulk_tx") > 0) | (pl.col("mc_dist_sub_tx") > 0)).alias("_is_peak"),
    )
    return (
        flagged.group_by("_month_num")
        .agg(
            pl.col("kwh").filter(~pl.col("_is_peak")).sum().alias("kwh_offpeak"),
            pl.col("kwh").filter(pl.col("_is_peak")).sum().alias("kwh_peak"),
        )
        .sort("_month_num")
        .with_columns(pl.col("_month_num").replace_strict(month_num_to_label).alias("month_label"))
        .select(
            pl.col("month_label").cast(pl.Enum(MONTH_ORDER)),
            "kwh_offpeak",
            "kwh_peak",
        )
    )


def building_delivery_mc_8760(
    load_8760: pl.DataFrame,
    mc_8760: pl.DataFrame,
    *,
    utc_offset_hours: int = -5,
) -> pl.DataFrame:
    """Multiply an hourly load profile by delivery marginal costs.

    Takes a single building (or population-average) load profile and the 8760
    delivery marginal-cost schedule, aligns their timestamps, and returns
    hourly marginal cost in dollars for transmission and distribution separately.

    Parameters
    ----------
    load_8760
        8760-row DataFrame with ``timestamp`` and ``kwh``. Timestamps may be
        UTC (as returned by :func:`weighted_avg_hourly` on data from
        :func:`load_billing_kwh_8760`).
    mc_8760
        DataFrame from :func:`load_delivery_mc_heatmap` with ``timestamp``,
        ``mc_bulk_tx``, ``mc_dist_sub_tx``. Timestamps are local.
    utc_offset_hours
        Hours to shift ``load_8760`` timestamps to align with ``mc_8760``.
        Default ``-5`` converts CAIRO's UTC to Eastern Standard Time.

    Returns
    -------
    pl.DataFrame
        8760-row DataFrame with ``timestamp`` (local), ``mc_tx_dollars``,
        ``mc_dist_dollars``.
    """
    import polars as pl

    load_local = load_8760.with_columns((pl.col("timestamp") + pl.duration(hours=utc_offset_hours)).alias("timestamp"))
    joined = load_local.join(
        mc_8760.select("timestamp", "mc_bulk_tx", "mc_dist_sub_tx"),
        on="timestamp",
    )
    if joined.height != 8760:
        raise ValueError(
            f"Expected 8760 rows after join, got {joined.height}. Check timestamp alignment between load and MC data."
        )
    return joined.select(
        "timestamp",
        (pl.col("kwh") * pl.col("mc_bulk_tx")).alias("mc_tx_dollars"),
        (pl.col("kwh") * pl.col("mc_dist_sub_tx")).alias("mc_dist_dollars"),
    )


def load_delivery_mc_heatmap(state: str, utility: str, year: int) -> pl.DataFrame:
    """Load and join hourly bulk-transmission and distribution/sub-transmission marginal costs.

    Reads the two per-utility marginal-cost parquet files CAIRO's marginal-cost
    pipeline writes to S3 (not part of the master-table Prefect pipeline), joins
    them on ``timestamp``, and adds ``day_of_year``/``hour`` columns for
    ``plot_mc_heatmap()``. Raises if the result doesn't cover all 8,760 hours of
    *year*.

    Returns columns ``timestamp``, ``mc_bulk_tx``, ``mc_dist_sub_tx``,
    ``day_of_year``, ``hour``.
    """
    s3_opts = {"aws_region": "us-west-2"}
    path_bulk_tx = (
        f"s3://data.sb/switchbox/marginal_costs/{state.lower()}/bulk_tx/utility={utility}/year={year}/data.parquet"
    )
    path_dist_sub_tx = (
        f"s3://data.sb/switchbox/marginal_costs/{state.lower()}/dist_and_sub_tx/"
        f"utility={utility}/year={year}/data.parquet"
    )

    bulk_tx = pl.read_parquet(path_bulk_tx, storage_options=s3_opts)
    dist_sub_tx = pl.read_parquet(path_dist_sub_tx, storage_options=s3_opts)

    heatmap_df = (
        bulk_tx.join(dist_sub_tx.select("timestamp", "mc_total_per_kwh"), on="timestamp")
        .rename({"bulk_tx_cost_enduse": "mc_bulk_tx", "mc_total_per_kwh": "mc_dist_sub_tx"})
        .with_columns(
            pl.col("timestamp").dt.ordinal_day().alias("day_of_year"),
            pl.col("timestamp").dt.hour().alias("hour"),
        )
    )
    if heatmap_df.height != 8760:
        raise ValueError(f"Expected 8760 hourly rows for {state}/{utility}/{year}, got {heatmap_df.height}.")
    return heatmap_df


# --- Weighted stats ------------------------------------------------------------


def weighted_mean(df: pl.DataFrame, col: str, weight_col: str = "weight") -> float:
    """Weighted arithmetic mean of *col*."""
    numerator = float((df[col] * df[weight_col]).sum())
    denominator = float(df[weight_col].sum())
    return numerator / denominator


def weighted_quantile(df: pl.DataFrame, col: str, q: float, weight_col: str = "weight") -> float:
    """Weighted quantile of *col* via cumulative weight (e.g. ``q=0.5`` for the median)."""
    sorted_df = df.sort(col)
    total_weight = float(sorted_df[weight_col].sum())
    cum = sorted_df[weight_col].cum_sum() / total_weight
    return float(sorted_df.filter(cum >= q)[col][0])


def weighted_pct(df: pl.DataFrame, predicate: pl.Expr | pl.Series, weight_col: str = "weight") -> float:
    """Weighted share of rows in *df* matching *predicate* (a boolean Polars expression or mask)."""
    total = float(df[weight_col].sum())
    matching = float(df.filter(predicate)[weight_col].sum())
    return matching / total


# --- Bill-change diff ----------------------------------------------------------


def _normalize_bill_months(month: str | Sequence[str]) -> list[str]:
    """Coerce ``month=`` to a non-empty list of master-bills ``month`` labels."""
    months = [month] if isinstance(month, str) else list(month)
    if not months:
        raise ValueError("month must be a non-empty month name or sequence of month names")
    if "Annual" in months and len(months) > 1:
        raise ValueError("Cannot combine 'Annual' with calendar months; pass one or the other")
    return months


def bill_period_phrase(month: str | Sequence[str]) -> str:
    """Short phrase for chart titles: ``annual``, ``Jan``, or ``Oct-May``."""
    months = _normalize_bill_months(month)
    if months == ["Annual"]:
        return "annual"
    if len(months) == 1:
        return months[0]
    return f"{months[0]}-{months[-1]}"


def _month_bills_for_delta(
    bills: pl.LazyFrame,
    months: list[str],
    bill_col: str,
    *,
    bill_alias: str,
    keep_meta: bool,
    electric_utility: str | None = None,
) -> pl.LazyFrame:
    """Filter to *months* and optionally sum them to one row per building."""
    filtered = bills.filter(pl.col("month").is_in(months))
    if electric_utility is not None:
        filtered = filtered.filter(pl.col("sb.electric_utility") == electric_utility)

    if len(months) == 1:
        cols: list[pl.Expr | str] = ["bldg_id"]
        if keep_meta:
            cols.extend(
                [
                    "weight",
                    pl.col("postprocess_group.has_hp").alias("has_hp"),
                    pl.col("postprocess_group.heating_type_v2").alias("heating_type_v2"),
                ]
            )
        cols.append(pl.col(bill_col).alias(bill_alias))
        return filtered.select(cols)

    agg: list[pl.Expr] = [pl.col(bill_col).sum().alias(bill_alias)]
    if keep_meta:
        agg = [
            pl.col("weight").first(),
            pl.col(bill_col).sum().alias(bill_alias),
            pl.col("postprocess_group.has_hp").first().alias("has_hp"),
            pl.col("postprocess_group.heating_type_v2").first().alias("heating_type_v2"),
        ]
    return filtered.group_by("bldg_id").agg(agg)


def bill_delta_between_segments(
    state: str,
    batch: str,
    segment_before: str,
    segment_after: str,
    *,
    bill_col: str = "energy_total_bill",
    month: str | Sequence[str] = "Annual",
    electric_utility: str | None = None,
) -> pl.DataFrame:
    """Diff a per-building bill column between any two ``{scenario}_{stage}`` segments.

    Both axes of comparison reduce to the same join on ``bldg_id``:

    - Same scenario, different stage (e.g. ``"default_precalc"`` ->
      ``"default_calibrated"``): before/after a heat-pump retrofit, holding the
      tariff fixed.
    - Same stage, different scenario (e.g. ``"default_precalc"`` ->
      ``"hp_seasonal_percustomer_passthrough_precalc"``): same population,
      comparing two tariffs.

    *month* selects which master-bills rows to diff. ``"Annual"`` (default) uses
    the annual total. A calendar month (``"Jan"``) diffs that month alone. A
    sequence of calendar months (e.g. BGE winter ``Oct``-``May``) sums those
    months per building before the join — the ``delta`` is then the change over
    that season, not a scaled annual figure.

    Metadata columns (``heating_type_v2``, ``has_hp``) are carried from
    *segment_before* — they are baseline-derived and identical across
    segments/stages for the same population (see rate-design-platform PR #503's
    ``master_metadata.py``).

    *electric_utility* optionally restricts to one ``sb.electric_utility``
    value (from *segment_before*) before the join.

    Returns a DataFrame with ``bldg_id``, ``weight``, ``has_hp``,
    ``heating_type_v2``, ``bill_before``, ``bill_after``, ``delta``.
    """
    months = _normalize_bill_months(month)
    before = _month_bills_for_delta(
        load_master_bills(state, batch, segment_before),
        months,
        bill_col,
        bill_alias="bill_before",
        keep_meta=True,
        electric_utility=electric_utility,
    )
    after = _month_bills_for_delta(
        load_master_bills(state, batch, segment_after),
        months,
        bill_col,
        bill_alias="bill_after",
        keep_meta=False,
    )
    joined = before.join(after, on="bldg_id", how="inner").with_columns(
        (pl.col("bill_after") - pl.col("bill_before")).alias("delta")
    )
    return cast("pl.DataFrame", joined.collect())


def bat_component_delta(
    state: str,
    batch: str,
    segment_before: str,
    segment_after: str,
    *,
    components: list[str] | None = None,
    exclude_has_hp: bool = True,
    utility: str | None = None,
) -> pl.DataFrame:
    """Per-building delta of BAT cost-allocation components between two segments.

    Analogous to ``bill_delta_between_segments()`` but reads the master BAT
    table (one row per building, annual) and diffs multiple columns at once.

    The default *components* are ``annual_bill_delivery`` (delivery revenue)
    and ``economic_burden_delivery`` (marginal-cost allocation).  Both are
    valid at *both* precalc and calibrated stages: ``annual_bill`` is the
    actual bill (correct at calibrated per module-level docs), and
    ``economic_burden`` is purely load x MC (independent of revenue
    requirement / tariff calibration).

    Returns one row per building with ``bldg_id``, ``weight``, ``has_hp``,
    ``heating_type_v2``, and for each component *c*: ``{c}_before``,
    ``{c}_after``, ``delta_{c}``.

    When *exclude_has_hp* is True (default), buildings with a heat pump at
    baseline (``postprocess_group.has_hp == True`` in *segment_before*) are
    dropped — they already have a heat pump and aren't "converting".

    When *utility* is set, both segments' master BAT are filtered to
    ``sb.electric_utility == utility`` before joining — a no-op for
    single-utility batches, but avoids silently mixing in other utilities'
    buildings (and the wasted read) once a batch covers more than one.
    """
    if components is None:
        components = ["annual_bill_delivery", "economic_burden_delivery"]

    before_select: list[pl.Expr | str] = [
        "bldg_id",
        "weight",
        pl.col("postprocess_group.has_hp").alias("has_hp"),
        pl.col("postprocess_group.heating_type_v2").alias("heating_type_v2"),
        *[pl.col(c).alias(f"{c}_before") for c in components],
    ]
    after_select: list[pl.Expr | str] = [
        "bldg_id",
        *[pl.col(c).alias(f"{c}_after") for c in components],
    ]

    before = load_master_bat(state, batch, segment_before)
    # annual_bill_delivery and economic_burden_delivery are valid at calibrated
    # (see docstring), so suppress the stage warning from load_master_bat.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=".*not a `_precalc` segment.*")
        after = load_master_bat(state, batch, segment_after)

    if utility is not None:
        before = before.filter(pl.col("sb.electric_utility") == utility)
        after = after.filter(pl.col("sb.electric_utility") == utility)
    before = before.select(before_select)
    after = after.select(after_select)

    joined = before.join(after, on="bldg_id", how="inner")
    if exclude_has_hp:
        joined = joined.filter(pl.col("has_hp") == False)  # noqa: E712
    joined = joined.with_columns(
        *[(pl.col(f"{c}_after") - pl.col(f"{c}_before")).alias(f"delta_{c}") for c in components]
    )
    return cast("pl.DataFrame", joined.collect())


def bill_change_incidence(delta_df: pl.DataFrame, weight_col: str = "weight") -> dict:
    """Weighted incidence stats for a ``bill_delta_between_segments`` result.

    Composes on top of any such result regardless of which axis (before/after
    retrofit, or same population/different tariff) it came from.
    """
    total = delta_df[weight_col].sum()
    return {
        "pct_increase": weighted_pct(delta_df, delta_df["delta"] > 0, weight_col),
        "pct_decrease": weighted_pct(delta_df, delta_df["delta"] < 0, weight_col),
        "pct_unchanged": weighted_pct(delta_df, delta_df["delta"] == 0, weight_col),
        "mean_delta": weighted_mean(delta_df, "delta", weight_col),
        "median_delta": weighted_quantile(delta_df, "delta", 0.5, weight_col),
        "n_weighted": float(total),
    }


# --- Bill-change quadrant chart --------------------------------------------------

# Human-readable labels for postprocess_group.heating_type_v2 codes. Attributes
# always come from the baseline (precalc) upgrade, so this classification holds
# on every segment -- including calibrated, where ResStock would otherwise mark
# every building as a heat pump.
HEATING_TYPE_LABELS: dict[str, str] = {
    "heat_pump": "Existing heat pump",
    "electrical_resistance": "Electric resistance",
    "natgas": "Natural gas",
    "delivered_fuels": "Oil/propane",
    "other": "Other",
}
# Display order for heating groups in charts and tables.
HEATING_ORDER = ["Natural gas", "Oil/propane", "Electric resistance", "Existing heat pump", "Other"]
# Codes excluded by default from plot_bill_change_quadrants(): "heat_pump"
# customers already have a heat pump (not "upgrading" to one), and "other" is a
# heterogeneous/unclassified bucket not worth breaking out on its own.
DEFAULT_EXCLUDED_HEATING_CODES = {"heat_pump", "other"}

QUADRANT_COLORS: dict[str, str] = {
    "savings > $1k": "#1b5e20",
    "savings $0-1k": "#81c784",
    "losses $0-1k": "#ef9a9a",
    "losses > $1k": "#b71c1c",
}
QUADRANT_ORDER = list(QUADRANT_COLORS.keys())
# Short, human-readable captions drawn inline next to each bar segment in
# plot_bill_change_quadrants() in lieu of a standard plotnine legend (which
# would need a separate lookup against QUADRANT_COLORS to interpret).
QUADRANT_LABELS: dict[str, str] = {
    "losses > $1k": "LOSE > $1K",
    "losses $0-1k": "LOSE $0-1K",
    "savings $0-1k": "SAVE $0-1K",
    "savings > $1k": "SAVE > $1K",
}


def add_heating_label(df: pl.DataFrame, code_col: str = "heating_type_v2") -> pl.DataFrame:
    """Map heating-type codes to human-readable labels, added as a ``heating_label`` column.

    *code_col* defaults to ``"heating_type_v2"``, the alias
    ``bill_delta_between_segments`` gives ``postprocess_group.heating_type_v2``.
    Pass ``code_col="postprocess_group.heating_type_v2"`` when operating
    directly on a master bills/BAT table instead of a delta table.
    """
    return df.with_columns(
        pl.col(code_col).replace_strict(HEATING_TYPE_LABELS, default=pl.col(code_col)).alias("heating_label")
    )


def weighted_range_pcts(
    df: pl.DataFrame,
    *,
    value_col: str,
    ranges: Sequence[tuple[str, float, float]],
    weight_col: str = "weight",
) -> dict[str, float]:
    """Weighted percent of rows in labeled half-open intervals.

    ``ranges`` is ``(label, lo, hi)`` meaning ``lo <= value < hi``. Use
    ``-math.inf`` / ``math.inf`` for unbounded tails. Labels are returned in
    the order given. Percents are on a 0-100 scale and sum to 100 when the
    ranges partition the data and every row has a finite weight.
    """
    labels = [label for label, _lo, _hi in ranges]
    if len(labels) != len(set(labels)):
        duplicates = sorted({label for label in labels if labels.count(label) > 1})
        raise ValueError(f"Range labels must be unique; duplicates: {duplicates}")

    total = cast("float", df[weight_col].sum())
    if total == 0:
        return dict.fromkeys(labels, 0.0)

    value = pl.col(value_col)
    out: dict[str, float] = {}
    for label, lo, hi in ranges:
        out[label] = cast("float", df.filter((value >= lo) & (value < hi))[weight_col].sum()) / total * 100
    return out


def quadrant_pcts(
    df: pl.DataFrame,
    weight_col: str = "weight",
    value_col: str = "delta",
) -> dict[str, float]:
    """Weighted % of households in each bill-change quadrant.

    *df* must have a dollar-change column (default ``delta``) and a weight
    column. Quadrant boundaries are fixed at +/- $1,000, matching the
    savings/loss framing used throughout the rate-case reports.

    For custom cutoffs or labels, call :func:`weighted_range_pcts` instead.
    """
    return weighted_range_pcts(
        df,
        value_col=value_col,
        weight_col=weight_col,
        ranges=[
            ("savings > $1k", -math.inf, -1000),
            ("savings $0-1k", -1000, 0),
            ("losses $0-1k", 0, 1000),
            ("losses > $1k", 1000, math.inf),
        ],
    )


# Below this width, a quadrant caption is dropped rather than drawn: showing
# one for a sub-rounding-error sliver (e.g. 0.05%) would add clutter without
# conveying anything real.
_QUADRANT_MIN_CAPTIONED_PCT = 0.5
# A segment counts as touching an edge -- and gets its caption anchored at
# that edge, extending inward -- whenever the cumulative width of all
# segments from that edge (inclusive) is within this threshold. This is
# checked cumulatively rather than per-segment so that a *chain* of small
# segments at the same edge (e.g. both loss quadrants tiny) all anchor
# consistently, instead of the second one falling through to "center" and
# overlapping the first (which centering text over a near-zero-width segment
# would otherwise do, since the text overflows both sides of the segment).
_QUADRANT_EDGE_ANCHOR_PCT = 5.0
# Two edge-anchored captions on the same side of the same bar (e.g. both
# small losses at the start) are placed at the same "y" starting point --
# without this, their text would still collide despite being correctly
# anchored. Stack them onto successive lines above the bar instead.
_QUADRANT_SEG_LABEL_OFFSET = 0.45
_QUADRANT_SEG_LABEL_STAGGER = 0.22


def _quadrant_seg_label_df(pcts_by_row: list[dict[str, float]]) -> pl.DataFrame | None:
    """Build the caption layout shared by plot_bill_change_quadrants() and
    plot_bill_change_quadrant_comparison().

    *pcts_by_row* is one ``quadrant_pcts()``-shaped dict per bar, in
    top-to-bottom drawing order (row 0 ends up on top, since coord_flip()
    draws the first categorical position at the bottom). Returns a frame with
    one row per caption actually drawn: ``x`` (categorical position, offset
    above its bar), ``y`` (position along the bar), ``label``, ``color``, and
    ``ha`` (text alignment) -- or ``None`` if every segment was empty.
    """
    stacking_order = list(reversed(QUADRANT_ORDER))
    n_rows = len(pcts_by_row)
    records: list[dict[str, object]] = []
    for i, pct in enumerate(pcts_by_row):
        row_x = n_rows - i
        cum = 0.0
        edge_caption_count = {"left": 0, "right": 0}
        for q in stacking_order:
            seg_start = cum
            mid = cum + pct[q] / 2
            cum += pct[q]
            if pct[q] < _QUADRANT_MIN_CAPTIONED_PCT:
                continue
            if cum <= _QUADRANT_EDGE_ANCHOR_PCT:
                label_y, label_ha = seg_start, "left"
            elif (100 - seg_start) <= _QUADRANT_EDGE_ANCHOR_PCT:
                label_y, label_ha = cum, "right"
            else:
                label_y, label_ha = mid, "center"
            stack_idx = edge_caption_count.get(label_ha, 0)
            if label_ha in edge_caption_count:
                edge_caption_count[label_ha] += 1
            records.append(
                {
                    "x": row_x + _QUADRANT_SEG_LABEL_OFFSET + stack_idx * _QUADRANT_SEG_LABEL_STAGGER,
                    "y": label_y,
                    "label": QUADRANT_LABELS[q],
                    "color": QUADRANT_COLORS[q],
                    "ha": label_ha,
                }
            )
    return pl.DataFrame(records) if records else None


def plot_bill_change_quadrants(
    state: str,
    batch: str,
    segment_before: str,
    segment_after: str,
    *,
    bill_col: str = "energy_total_bill",
    rate_name: str = "current rate",
    heating_types: list[str] | None = None,
    month: str | Sequence[str] = "Annual",
) -> ggplot:
    """Stacked horizontal bar chart of bill-change quadrants by baseline heating type.

    Wraps ``bill_delta_between_segments()`` — *segment_before* and
    *segment_after* are ``{scenario}_{stage}`` segment names, exactly as passed
    there. The most common usage holds *segment_before* fixed at today's actual
    bill (e.g. ``"default_precalc"``) while varying *segment_after* across
    scenarios' calibrated stage (e.g. ``"default_calibrated"`` vs.
    ``"hp_seasonal_percustomer_passthrough_calibrated"``), so each call answers
    "would this customer save money switching to a heat pump" under a
    different candidate rate, all relative to the same before-retrofit
    baseline bill.

    *bill_col* is passed straight through to ``bill_delta_between_segments()``
    — defaults to ``"energy_total_bill"`` (baseline bills) but can be set to
    an LMI-discounted column (e.g. ``"energy_total_bill_lmi_48"``) when the
    master bills table has one, to show bill changes net of existing
    low-income assistance instead.

    Each bar shows the weighted % of households in four bins: savings/losses
    of $0-1k and >$1k a year. *rate_name* is threaded into the chart title
    (e.g. ``"default rate"``, ``"seasonal HP rate"``) so charts built under
    different scenarios are self-labeling.

    *heating_types* restricts to specific baseline ``heating_type_v2`` codes
    (e.g. ``["natgas"]``). If ``None`` (default), includes every available
    heating type except ``"heat_pump"`` (already has a heat pump, not
    "upgrading") and ``"other"`` (heterogeneous/unclassified) — see
    ``DEFAULT_EXCLUDED_HEATING_CODES``.

    *month* is passed through to ``bill_delta_between_segments()``. The default
    ``"Annual"`` diffs the annual total; pass a sequence of calendar months
    (e.g. BGE winter ``["Oct", ..., "May"]``) to bin the seasonal sum. Quadrant
    cutoffs stay at +/- $1,000 of that period's dollar change — they are not
    scaled to a 12-month equivalent.

    Since each bar's quadrant mix can look very different (e.g. an
    electric-resistance row might be almost entirely "savings > $1k" while a
    natural-gas row is split across all four bins), the chart replaces the
    usual plotnine fill legend with short color-matched captions
    (``QUADRANT_LABELS``) drawn above *every* bar's segments that's actually
    present (skipped only when a segment rounds to ~0%) rather than a single
    reference row — a single row's mix isn't guaranteed to include every
    quadrant.
    """
    import plotnine as plt

    from lib.plotnine import theme_switchbox

    delta = bill_delta_between_segments(state, batch, segment_before, segment_after, bill_col=bill_col, month=month)
    if heating_types is not None:
        delta = delta.filter(pl.col("heating_type_v2").is_in(heating_types))
    else:
        delta = delta.filter(~pl.col("heating_type_v2").is_in(DEFAULT_EXCLUDED_HEATING_CODES))
    delta = add_heating_label(delta)

    avail_heating = [h for h in HEATING_ORDER if h in delta["heating_label"].unique().to_list()]
    if not avail_heating:
        raise ValueError(
            f"No heating types remain to plot for segments {segment_before!r} -> {segment_after!r} "
            f"after applying heating_types={heating_types!r}."
        )

    records: list[dict[str, object]] = []
    group_pcts: dict[str, dict[str, float]] = {}
    for group in avail_heating:
        pct = quadrant_pcts(delta.filter(pl.col("heating_label") == group))
        group_pcts[group] = pct
        for q in QUADRANT_ORDER:
            records.append({"heating_label": group, "quadrant": q, "pct": pct[q]})

    plot_df = pl.DataFrame(records).with_columns(
        pl.col("heating_label").cast(pl.Enum(list(reversed(avail_heating)))),
        pl.col("quadrant").cast(pl.Enum(QUADRANT_ORDER)),
    )

    # Build one caption per bar segment that's actually present, positioned
    # in the gap just above the bar it belongs to (an "x" offset past the
    # bar's own categorical position, since coord_flip makes "x" the vertical
    # axis). Ported from the evolved plot_quadrant_bar() in ny_hp_rates's
    # notebooks/analysis.qmd, adapted from per-scenario rows to per-heating-
    # type rows.
    seg_label_df = _quadrant_seg_label_df([group_pcts[g] for g in avail_heating])

    n_bars = len(avail_heating)
    bar_w = 0.7 if n_bars <= 2 else 0.55
    fig_h = max(2.5, 0.8 + 1.4 * n_bars)
    x_expand_top = 0.45 if n_bars <= 2 else 0.6

    p = (
        plt.ggplot(plot_df, plt.aes(x="heating_label", y="pct", fill="quadrant"))
        + plt.geom_col(position="stack", width=bar_w)
        + plt.geom_text(
            mapping=plt.aes(label="pct"),
            data=plot_df.filter(pl.col("pct") >= 3),
            position=plt.position_stack(vjust=0.5),
            format_string="{:.1f}%",
            color="white",
            size=11,
            fontweight="bold",
        )
        + plt.scale_fill_manual(values=QUADRANT_COLORS, breaks=QUADRANT_ORDER)
        + plt.scale_y_continuous(expand=(0, 0, 0.04, 0))
        + plt.scale_x_discrete(expand=(0, 0, 0, x_expand_top))
        + plt.coord_flip()
        + plt.guides(fill=False)
        + plt.labs(
            x="",
            y="% of weighted households",
            title=(
                f"Change in total {bill_period_phrase(month)} energy bill after "
                f"switching to a heat pump, under the {rate_name}"
            ),
        )
        + theme_switchbox()
        + plt.theme(
            figure_size=(11.5, fig_h),
            # The %-of-households scale is redundant with the in-bar labels
            # above, so drop its axis entirely (title/text/ticks/line). Since
            # coord_flip() renders the "x" aesthetic (heating_label) as the
            # screen's vertical axis, its per-category breaks are what draw
            # the faint horizontal lines across the panel -- blank those too.
            axis_title_x=plt.element_blank(),
            axis_text_x=plt.element_blank(),
            axis_ticks_x=plt.element_blank(),
            axis_line_x=plt.element_blank(),
            panel_grid_major_y=plt.element_blank(),
        )
    )

    if seg_label_df is not None:
        for ha_val in seg_label_df["ha"].unique().to_list():
            sub = seg_label_df.filter(pl.col("ha") == ha_val)
            p = p + plt.geom_text(
                mapping=plt.aes(x="x", y="y", label="label", color="color"),
                data=sub,
                ha=ha_val,
                va="bottom",
                size=9,
                fontweight="bold",
                inherit_aes=False,
                show_legend=False,
            )
        p = p + plt.scale_color_identity()

    return p


def plot_bill_change_quadrant_single(
    state: str,
    batch: str,
    segment_before: str,
    segment_after: str,
    *,
    heating_type: str,
    bill_col: str = "energy_total_bill",
    rate_name: str = "current rate",
    month: str | Sequence[str] = "Annual",
    title: str | None = None,
) -> ggplot:
    """Single horizontal bar of bill-change quadrants for one heating type under one rate.

    Like ``plot_bill_change_quadrants`` but shows only one heating type as a
    single bar, giving it more visual weight when the analysis discusses each
    fuel individually rather than comparing them side-by-side.

    Parameters
    ----------
    state, batch, segment_before, segment_after
        Passed through to ``bill_delta_between_segments()``.
    heating_type
        A single ``heating_type_v2`` code (e.g. ``"natgas"``,
        ``"delivered_fuels"``).
    bill_col
        Column to diff; defaults to ``"energy_total_bill"``.
    rate_name
        Threaded into the default title (e.g. ``"Schedule R"``).
    month
        ``"Annual"`` or a sequence of calendar months for seasonal analysis.
    title
        Override the auto-generated title.

    Returns
    -------
    ggplot
    """
    import plotnine as plt

    from lib.plotnine import theme_switchbox

    delta = bill_delta_between_segments(state, batch, segment_before, segment_after, bill_col=bill_col, month=month)
    delta = delta.filter(pl.col("heating_type_v2") == heating_type)
    delta = add_heating_label(delta)

    heating_label = delta["heating_label"].unique().to_list()[0]

    pct = quadrant_pcts(delta)
    records: list[dict[str, object]] = []
    for q in QUADRANT_ORDER:
        records.append({"quadrant": q, "pct": pct[q]})

    plot_df = pl.DataFrame(records).with_columns(
        pl.col("quadrant").cast(pl.Enum(QUADRANT_ORDER)),
    )

    seg_label_df = _quadrant_seg_label_df([pct])

    chart_title = title or (
        f"Change in total {bill_period_phrase(month)} energy bill for "
        f"{heating_label.lower()}-heated homes after switching to a heat pump, "
        f"under the {rate_name}"
    )

    p = (
        plt.ggplot(plot_df, plt.aes(x=1, y="pct", fill="quadrant"))
        + plt.geom_col(position="stack", width=0.55)
        + plt.geom_text(
            mapping=plt.aes(label="pct"),
            data=plot_df.filter(pl.col("pct") >= 3),
            position=plt.position_stack(vjust=0.5),
            format_string="{:.1f}%",
            color="white",
            size=11,
            fontweight="bold",
        )
        + plt.scale_fill_manual(values=QUADRANT_COLORS, breaks=QUADRANT_ORDER)
        + plt.scale_y_continuous(expand=(0, 0, 0.04, 0))
        + plt.scale_x_continuous(expand=(0, 0.35, 0, 1.2))
        + plt.coord_flip()
        + plt.guides(fill=False)
        + plt.labs(x="", y="", title=chart_title)
        + theme_switchbox()
        + plt.theme(
            figure_size=(13.5, 2.6),
            axis_text=plt.element_blank(),
            axis_ticks_x=plt.element_blank(),
            axis_ticks_y=plt.element_blank(),
            axis_line_x=plt.element_blank(),
            axis_line_y=plt.element_blank(),
            panel_grid=plt.element_blank(),
        )
    )

    if seg_label_df is not None:
        for ha_val in seg_label_df["ha"].unique().to_list():
            sub = seg_label_df.filter(pl.col("ha") == ha_val)
            p = p + plt.geom_text(
                mapping=plt.aes(x="x", y="y", label="label", color="color"),
                data=sub,
                ha=ha_val,
                va="bottom",
                size=10,
                fontweight="bold",
                inherit_aes=False,
                show_legend=False,
            )
        p = p + plt.scale_color_identity()

    return p


def plot_bill_change_quadrant_rate_comparison(
    state: str,
    batch: str,
    segment_before: str,
    rates: Sequence[tuple[str, str]],
    *,
    heating_type: str,
    bill_col: str = "energy_total_bill",
    month: str | Sequence[str] = "Annual",
    title_parts: list[tuple[str, str]] | None = None,
) -> ggplot | Figure:
    """Compare bill-change quadrants for one heating type across multiple rate scenarios.

    Convenience wrapper around ``plot_bill_change_quadrant_comparison()`` that
    handles the ``bill_delta_between_segments()`` calls and filtering
    internally, so the caller just passes segment names and labels.

    Parameters
    ----------
    state, batch, segment_before
        Passed through to ``bill_delta_between_segments()`` for each rate.
    rates
        Sequence of ``(segment_after, bar_label)`` tuples — one per rate
        scenario, e.g. ``[("default_calibrated", "Schedule R"),
        ("hp_seasonal_…_calibrated", "Schedule R-HP")]``.
    heating_type
        A single ``heating_type_v2`` code (e.g. ``"natgas"``).
    bill_col
        Column to diff; defaults to ``"energy_total_bill"``.
    month
        ``"Annual"`` or a sequence of calendar months.
    title_parts
        Optional multi-color title parts (see
        ``plot_bill_change_quadrant_comparison``).

    Returns
    -------
    ggplot | Figure
        ggplot when *title_parts* is None, Figure when multi-color title is
        used.
    """
    heating_label = HEATING_TYPE_LABELS.get(heating_type, heating_type)

    rows: list[tuple[str, pl.DataFrame]] = []
    for segment_after, bar_label in rates:
        delta = bill_delta_between_segments(state, batch, segment_before, segment_after, bill_col=bill_col, month=month)
        delta = delta.filter(pl.col("heating_type_v2") == heating_type)
        rows.append((bar_label, delta))

    default_title = (
        f"How {bill_period_phrase(month)} bills would change for "
        f"{heating_label.lower()}-heated homes after switching to heat pumps"
    )

    return plot_bill_change_quadrant_comparison(
        rows,
        title=default_title,
        title_parts=title_parts,
    )


def plot_bill_change_quadrant_comparison(
    rows: list[tuple[str, pl.DataFrame]],
    title: str = "How bills would change after switching to heat pumps:",
    title_parts: list[tuple[str, str]] | None = None,
) -> ggplot | Figure:
    """Horizontal stacked bar(s) of bill-change quadrants, one bar per *rows* entry.

    Unlike ``plot_bill_change_quadrants()`` (one bar per baseline heating
    type, all under the *same* rate), this is the comparison in the other
    direction: pass pre-built ``(label, df)`` pairs to put one population's
    (e.g. one heating type's) bill-change distribution side by side across
    *multiple* rates (e.g. default vs. seasonal HP rate vs. flat HP rate).
    Each *df* must already be filtered to the population of interest and have
    ``delta`` (dollar bill change) and ``weight`` columns — typically built by
    calling ``bill_delta_between_segments()`` once per rate scenario and
    filtering to one ``heating_type_v2``. *label* becomes that row's
    right-hand caption (e.g. ``"Default rate"``); rows are drawn top-to-bottom
    in the order given.

    When *title_parts* is given (a list of ``(text, color)`` tuples, e.g.
    ``[("How bills would change for ", "#000000"), ("natural gas",
    "#7A8A10"), (" heated homes after switching to ", "#000000"),
    ("heat pumps", "#c47600")]``), the plotnine title is replaced by a
    matplotlib multi-color title and the function returns a ``Figure``
    instead of a ``ggplot`` (plotnine titles can't mix colors within one
    string). Otherwise the plain *title* string is used as a standard
    plotnine title.

    Since row labels are drawn as captions rather than axis text (there is no
    axis at all — see below), a single row renders with no right-hand label;
    pass at least two rows to see per-row captions.
    """
    import plotnine as plt

    from lib.plotnine import theme_switchbox

    records: list[dict[str, object]] = []
    all_pcts: list[dict[str, float]] = []
    for row_label, df in rows:
        pct = quadrant_pcts(df)
        all_pcts.append(pct)
        for q in QUADRANT_ORDER:
            records.append({"scenario": row_label, "quadrant": q, "pct": pct[q]})

    scenario_order = [r[0] for r in reversed(rows)]
    plot_df = pl.DataFrame(records).with_columns(
        pl.col("quadrant").cast(pl.Enum(QUADRANT_ORDER)),
        pl.col("scenario").cast(pl.Enum(scenario_order)),
    )

    n_scenarios = len(rows)

    # Build one caption per bar segment that's actually present, positioned
    # in the gap just above the bar it belongs to (an "x" offset past the
    # bar's own categorical position, since coord_flip makes "x" the vertical
    # axis) -- same approach and edge-anchoring rationale as
    # plot_bill_change_quadrants().
    seg_label_df = _quadrant_seg_label_df(all_pcts)

    # Unlike plot_bill_change_quadrants() (whose categorical axis text *is*
    # the row label), here the whole axis is blanked below, so row labels
    # (e.g. "Default rate") are drawn as text past the right end of each bar.
    row_label_records: list[dict[str, object]] = []
    if n_scenarios > 1:
        for i, (row_label, _) in enumerate(rows):
            bar_pos = n_scenarios - i
            row_label_records.append({"x": bar_pos, "y": 101, "label": row_label})
    row_label_df = pl.DataFrame(row_label_records) if row_label_records else None

    top_expand = 0.7 if n_scenarios > 1 else 1.2
    plotnine_title = "" if title_parts else title

    p = (
        plt.ggplot(plot_df, plt.aes(x="scenario", y="pct", fill="quadrant"))
        + plt.geom_col(position="stack", width=0.55)
        + plt.geom_text(
            mapping=plt.aes(label="pct"),
            data=plot_df.filter(pl.col("pct") >= 3),
            position=plt.position_stack(vjust=0.5),
            format_string="{:.1f}%",
            color="white",
            size=11,
            fontweight="bold",
        )
        + plt.scale_fill_manual(values=QUADRANT_COLORS, breaks=QUADRANT_ORDER)
        + plt.scale_y_continuous(expand=(0, 0, 0.32, 0))
        + plt.scale_x_discrete(expand=(0, 0.35, 0, top_expand))
        + plt.coord_flip()
        + plt.guides(fill=False)
        + plt.labs(x="", y="", title=plotnine_title)
        + theme_switchbox()
        + plt.theme(
            figure_size=(13.5, max(2.6, 1.0 + 1.4 * n_scenarios)),
            # No axis at all here: percentages are already captioned in-bar,
            # and row labels are captioned at the right end of each bar (see
            # row_label_df above), so the categorical axis text would be
            # redundant.
            axis_text=plt.element_blank(),
            axis_ticks_x=plt.element_blank(),
            axis_ticks_y=plt.element_blank(),
            axis_line_x=plt.element_blank(),
            axis_line_y=plt.element_blank(),
            panel_grid=plt.element_blank(),
            plot_title=(
                plt.element_blank() if title_parts else plt.element_text(ha="left", margin={"b": -8, "unit": "pt"})
            ),
        )
    )
    if seg_label_df is not None:
        for ha_val in seg_label_df["ha"].unique().to_list():
            sub = seg_label_df.filter(pl.col("ha") == ha_val)
            p = p + plt.geom_text(
                mapping=plt.aes(x="x", y="y", label="label", color="color"),
                data=sub,
                ha=ha_val,
                va="bottom",
                size=10,
                fontweight="bold",
                inherit_aes=False,
                show_legend=False,
            )
        p = p + plt.scale_color_identity()
    if row_label_df is not None:
        p = p + plt.geom_text(
            mapping=plt.aes(x="x", y="y", label="label"),
            data=row_label_df,
            ha="left",
            va="center",
            size=11,
            fontweight="bold",
            inherit_aes=False,
        )

    if title_parts:
        fig = p.draw()
        # get_window_extent() below needs a renderer to measure text against;
        # draw() once here so it can fall back to the figure's cached
        # renderer instead of calling the backend-specific fig.canvas.get_renderer().
        fig.canvas.draw()
        fig_w_px = fig.get_window_extent().width

        # Measure the width of a single space in this font by diffing two
        # probe strings, so multi-color title segments can be laid out
        # left-to-right with normal word spacing between them.
        _t1 = fig.text(0, -1, "xx", fontsize=12, fontweight="bold", fontfamily="GT Planar")
        _t2 = fig.text(0, -1, "x x", fontsize=12, fontweight="bold", fontfamily="GT Planar")
        space_fig = (_t2.get_window_extent().width - _t1.get_window_extent().width) / fig_w_px
        _t1.remove()
        _t2.remove()

        x_pos = fig.axes[0].get_position().x0
        for i, (text_str, color) in enumerate(title_parts):
            t = fig.text(
                x_pos,
                0.92,
                text_str.strip(),
                color=color,
                fontsize=12,
                fontweight="bold",
                fontfamily="GT Planar",
                va="bottom",
            )
            bb = t.get_window_extent()
            x_pos = bb.transformed(fig.transFigure.inverted()).x1
            if i < len(title_parts) - 1:
                x_pos += space_fig
        return fig

    return p


def plot_weighted_bill_change_hist(
    df: pl.DataFrame,
    title: str,
    *,
    bin_width: int = 100,
    show_mean_median: bool = False,
    x_label: str = "Annual bill change ($)",
) -> ggplot:
    """Weighted histogram of annual bill change, colored by quadrant.

    *df* must have ``delta`` (dollar change) and ``weight`` columns. Bins are
    colored with ``QUADRANT_COLORS`` at the same +/- $1,000 boundaries as
    ``plot_bill_change_quadrants()``.

    When *show_mean_median* is True, adds dashed vertical lines for the
    weighted mean (carrot) and median (midnight) with text annotations.

    *x_label* overrides the default x-axis label, for callers whose ``delta``
    column isn't a plain bill change (e.g. incremental revenue minus marginal cost).
    """
    import plotnine as plt

    from lib.plotnine import SB_COLORS, theme_switchbox

    hist_df = df.select("delta", "weight")
    hist_snap = max(bin_width, 50)
    hist_x_lo = math.floor(weighted_quantile(hist_df, "delta", 0.01) / hist_snap) * hist_snap
    hist_x_hi = math.ceil(weighted_quantile(hist_df, "delta", 0.99) / hist_snap) * hist_snap
    _range = hist_x_hi - hist_x_lo
    _tick_step = bin_width if _range <= bin_width * 12 else bin_width * 2
    _tick_lo = math.floor(hist_x_lo / _tick_step) * _tick_step
    _tick_hi = math.ceil(hist_x_hi / _tick_step) * _tick_step
    hist_binned = (
        hist_df.with_columns(
            ((pl.col("delta") / bin_width).floor() * bin_width + bin_width / 2).alias("bin_center"),
        )
        .with_columns(
            pl.when(pl.col("bin_center") <= -1000)
            .then(pl.lit("savings > $1k"))
            .when((pl.col("bin_center") > -1000) & (pl.col("bin_center") < 0))
            .then(pl.lit("savings $0-1k"))
            .when((pl.col("bin_center") >= 0) & (pl.col("bin_center") < 1000))
            .then(pl.lit("losses $0-1k"))
            .otherwise(pl.lit("losses > $1k"))
            .alias("quadrant"),
        )
        .group_by("bin_center", "quadrant")
        .agg(pl.col("weight").sum().alias("weight_sum"))
        .with_columns(pl.col("quadrant").cast(pl.Enum(QUADRANT_ORDER)))
    )
    p = (
        plt.ggplot(hist_binned, plt.aes(x="bin_center", y="weight_sum", fill="quadrant"))
        + plt.geom_col(width=bin_width * 0.9)
        + plt.geom_vline(xintercept=[-1000, 0, 1000], linetype="dotted", color="gray")
        + plt.scale_fill_manual(values=QUADRANT_COLORS, breaks=QUADRANT_ORDER)
        + plt.scale_x_continuous(
            breaks=list(range(_tick_lo, _tick_hi + _tick_step, _tick_step)),
            labels=lambda xs: [f"${x:,.0f}" if x >= 0 else f"-${abs(x):,.0f}" for x in xs],
        )
        + plt.coord_cartesian(xlim=(hist_x_lo, hist_x_hi))
        + plt.labs(x=x_label, y="Weighted households", title=title)
        + plt.guides(fill=False)
        + theme_switchbox()
        + plt.theme(figure_size=(10.5, 4.5))
    )
    if show_mean_median:
        w_mean = weighted_mean(hist_df, "delta")
        w_median = weighted_quantile(hist_df, "delta", 0.50)
        y_top = cast("float", hist_binned["weight_sum"].max())
        p = (
            p
            + plt.geom_vline(xintercept=w_mean, linetype="dashed", color=SB_COLORS["carrot"], size=0.8)
            + plt.geom_vline(xintercept=w_median, linetype="dashed", color=SB_COLORS["midnight"], size=0.8)
            + plt.annotate(
                "text",
                x=w_mean + bin_width * 0.4,
                y=y_top * 0.97,
                label=f"Mean ${w_mean:,.0f}",
                ha="left",
                va="top",
                color=SB_COLORS["carrot"],
                size=9,
                fontweight="bold",
            )
            + plt.annotate(
                "text",
                x=w_median + bin_width * 0.4,
                y=y_top * 0.87,
                label=f"Median ${w_median:,.0f}",
                ha="left",
                va="top",
                color=SB_COLORS["midnight"],
                size=9,
                fontweight="bold",
            )
        )
    return p


def plot_weighted_hist_by_group(
    df: pl.DataFrame,
    value_col: str,
    group_col: str,
    title: str,
    *,
    bin_width: float = 100.0,
    x_label: str = "Value",
) -> ggplot:
    """Weighted histogram of *value_col*, faceted by *group_col*.

    Unlike ``plot_weighted_bill_change_hist()``, bins are a single flat color
    (no quadrant thresholds) since this is used for non-dollar values like
    incremental kWh, where the +/- $1,000 bill-change boundaries don't apply.
    Each facet gets its own free x/y scale (``facet_wrap(..., scales="free")``)
    since different groups (e.g. heating types) can have very different
    ranges and magnitudes.

    *df* must have *value_col*, ``weight``, and *group_col* columns.
    """
    import plotnine as plt
    import polars as pl
    from mizani.breaks import breaks_extended

    from lib.plotnine import SB_COLORS, theme_switchbox

    hist_df = df.select(value_col, "weight", group_col)
    hist_snap = max(bin_width, 1)
    hist_x_lo = math.floor(weighted_quantile(hist_df, value_col, 0.01) / hist_snap) * hist_snap
    hist_x_hi = math.ceil(weighted_quantile(hist_df, value_col, 0.99) / hist_snap) * hist_snap
    hist_binned = (
        hist_df.with_columns(
            ((pl.col(value_col) / bin_width).floor() * bin_width + bin_width / 2).alias("bin_center"),
        )
        .group_by("bin_center", group_col)
        .agg(pl.col("weight").sum().alias("weight_sum"))
    )
    # coord_cartesian() only zooms the view -- it doesn't affect break calculation,
    # so the default breaks are spaced to cover the full (unclipped) data range and
    # most land outside the zoomed-in window. Force breaks over the same
    # (hist_x_lo, hist_x_hi) window we're actually displaying instead.
    breaks_fn = breaks_extended(n=8)
    return (
        plt.ggplot(hist_binned, plt.aes(x="bin_center", y="weight_sum"))
        + plt.geom_col(width=bin_width * 0.9, fill=SB_COLORS["sky"])
        + plt.geom_vline(xintercept=0, linetype="dotted", color="gray")
        + plt.facet_wrap(group_col, scales="free")
        + plt.coord_cartesian(xlim=(hist_x_lo, hist_x_hi))
        + plt.scale_x_continuous(
            breaks=lambda _limits, lo=hist_x_lo, hi=hist_x_hi: breaks_fn((lo, hi)),
            labels=lambda xs: [f"{x:,.0f}" for x in xs],
        )
        + plt.labs(x=x_label, y="Weighted households", title=title)
        + theme_switchbox()
        + plt.theme(figure_size=(10.5, 4.5))
    )


# --- Rate-design-only bill change (pre-retrofit, tariff-only comparison) --------


def plot_ratedesign_monthly_hist(
    delta_df: pl.DataFrame,
    median_delta: float,
    *,
    binwidth: float = 1,
    fill_color: str | None = None,
) -> ggplot:
    """Unweighted monthly-$ histogram of a rate-design-only bill change.

    *delta_df* is a ``bill_delta_between_segments()`` result (or a subset of
    one), already filtered to the population of interest -- typically the
    non-heat-pump subclass under a reform tariff, holding HVAC equipment
    fixed and varying only the tariff. *median_delta* is that population's
    weighted median **annual** ``delta`` (e.g.
    ``bill_change_incidence(delta_df)["median_delta"]``); both the histogram
    and the reference line are shown in $/month.
    """
    import plotnine as plt

    from lib.plotnine import SB_COLORS, theme_switchbox

    fill_color = fill_color or SB_COLORS["midnight"]
    plot_df = delta_df.with_columns((pl.col("delta") / 12).alias("delta_monthly"))

    return (
        plt.ggplot(plot_df, plt.aes(x="delta_monthly"))
        + plt.geom_histogram(binwidth=binwidth, fill=fill_color)
        + plt.geom_vline(xintercept=median_delta / 12, color=SB_COLORS["carrot"], linetype="dashed")
        + plt.labs(x="Change in monthly energy bill ($)", y="Count of households")
        + plt.scale_x_continuous(
            breaks=lambda limits: list(range((int(limits[0]) // 5) * 5, int(limits[1]) + 5, 5)),
            labels=lambda xs: [f"${x:,.0f}" if x >= 0 else f"-${abs(x):,.0f}" for x in xs],
            minor_breaks=[],
        )
        + theme_switchbox()
        + plt.theme(figure_size=(10.5, 4.5))
    )


def plot_ratedesign_cdf(
    delta_df: pl.DataFrame,
    median_delta: float,
    *,
    exclude_heating_types: list[str] | None = None,
    series_labels: tuple[str, str] = ("All non-HP", "Excl. electric resistance & heat pump"),
    y_label: str = "Share of non-HP households",
) -> ggplot:
    """Weighted CDF of a rate-design-only monthly bill change, all vs. a heating-type-excluded subset.

    *delta_df* is a ``bill_delta_between_segments()`` result already filtered
    to the population of interest (typically the non-heat-pump subclass).
    Draws two step CDFs -- the full population and, by default, that
    population excluding ``"electrical_resistance"``/``"heat_pump"`` baseline
    heating types (pass *exclude_heating_types* to change which codes are
    dropped for the second series). *median_delta* is the full population's
    weighted median **annual** delta; the dashed reference line is drawn in
    $/month.
    """
    import plotnine as plt

    from lib.plotnine import SB_COLORS, theme_switchbox

    exclude_heating_types = (
        exclude_heating_types if exclude_heating_types is not None else ["electrical_resistance", "heat_pump"]
    )

    def _weighted_monthly_cdf(df: pl.DataFrame) -> pl.DataFrame:
        return (
            df.with_columns((pl.col("delta") / 12).alias("delta_monthly"))
            .sort("delta_monthly")
            .with_columns((pl.col("weight").cum_sum() / pl.col("weight").sum()).alias("cdf"))
        )

    cdf_df = pl.concat(
        [
            _weighted_monthly_cdf(delta_df).with_columns(pl.lit(series_labels[0]).alias("series")),
            _weighted_monthly_cdf(
                delta_df.filter(~pl.col("heating_type_v2").is_in(exclude_heating_types))
            ).with_columns(pl.lit(series_labels[1]).alias("series")),
        ]
    ).with_columns(pl.col("series").cast(pl.Enum(list(series_labels))))

    return (
        plt.ggplot(cdf_df, plt.aes(x="delta_monthly", y="cdf", color="series"))
        + plt.geom_step()
        + plt.geom_vline(xintercept=median_delta / 12, color=SB_COLORS["carrot"], linetype="dashed")
        + plt.labs(x="Change in monthly energy bill ($)", y=y_label, color=None)
        + plt.scale_color_manual(values=[SB_COLORS["midnight"], SB_COLORS["sky"]])
        + plt.scale_x_continuous(
            breaks=lambda limits: list(range((int(limits[0]) // 5) * 5, int(limits[1]) + 5, 5)),
            minor_breaks=lambda limits: list(range(int(limits[0]), int(limits[1]) + 1, 1)),
            labels=lambda xs: [f"${x:,.0f}" if x >= 0 else f"-${abs(x):,.0f}" for x in xs],
        )
        + plt.scale_y_continuous(
            breaks=[i / 10 for i in range(11)],
            minor_breaks=[i / 20 for i in range(21)],
            labels=lambda ys: [f"{y:.0%}" for y in ys],
        )
        + theme_switchbox()
        + plt.theme(figure_size=(10.5, 4.5), legend_position="bottom")
    )


def plot_mc_heatmap(
    df: pl.DataFrame,
    value_col: str,
    *,
    title: str,
    high_color: str,
    x_col: str = "day_of_year",
    y_col: str = "hour",
    fill_label: str = "$/kWh",
    figure_size: tuple[float, float] = (10.5, 4),
) -> Figure:
    """Render an 8760-hour (day-of-year x hour-of-day) marginal-cost heatmap.

    Filters to rows where *value_col* is positive (zero-cost hours are left
    blank rather than tiled white) and draws with plotnine.  Expects *df* to
    already have day-of-year and hour columns (e.g. via
    ``.dt.ordinal_day()`` / ``.dt.hour()`` on a timestamp column).

    The caller should pass the returned ``Figure`` to
    ``display_figure`` / ``display_svg`` for Quarto embedding.
    """
    import plotnine as plt

    from lib.plotnine import theme_switchbox

    nz = df.filter(pl.col(value_col) > 0)
    p = (
        plt.ggplot(nz, plt.aes(x=x_col, y=y_col, fill=value_col))
        + plt.geom_tile()
        + plt.scale_fill_gradient(low="#FFFFFF", high=high_color)
        + plt.scale_x_continuous(
            breaks=[1, 91, 182, 274, 365],
            labels=["Jan", "Apr", "Jul", "Oct", "Dec"],
            limits=(1, 365),
        )
        + plt.scale_y_continuous(breaks=[0, 6, 12, 18, 23], limits=(0, 23))
        + plt.coord_cartesian(expand=False)
        + plt.labs(title=title, x="", y="Hour of day", fill=fill_label)
        + theme_switchbox()
        + plt.theme(figure_size=figure_size, legend_position="right")
    )
    return p.draw()


# --- Energy burden ---------------------------------------------------------------


def burden_shares(
    bills_lf: pl.LazyFrame,
    bldg_ids: list,
    income_df: pl.DataFrame,
    bill_cols: list[str],
    burden_threshold: float = 0.06,
    *,
    income_col: str = "in.representative_income",
    income_cpi_ratio: float = 1.0,
    bldg_id_col: str = "bldg_id",
    month: str = "Annual",
) -> tuple[float, float]:
    """Return ``(weighted_pct_below, weighted_pct_above)`` an energy-burden threshold.

    *bill_cols* controls which columns of *bills_lf* are summed to form each
    building's total energy bill for this call -- pass a single LMI-discounted
    column (e.g. ``["energy_total_bill_lmi_48"]``) to compute burden under an
    LMI discount, or several delivered-fuel columns to sum them into one bill.

    Burden is ``bill / (income * income_cpi_ratio)``. *income_col* is
    typically ResStock's ``in.representative_income``, denominated in an
    earlier dollar year than the bills; *income_cpi_ratio* inflates it to the
    bills' dollar year (pass ``1.0``, the default, if *income_df* is already
    in the right dollar year).

    *bldg_ids* restricts the computation to a cohort (e.g. low-income,
    gas-heated buildings); *income_df* must have *bldg_id_col* and
    *income_col*.
    """
    collected = cast(
        "pl.DataFrame",
        bills_lf.filter(pl.col("month") == month).select(bldg_id_col, "weight", *bill_cols).collect(),
    )
    annual = (
        collected.filter(pl.col(bldg_id_col).is_in(bldg_ids))
        .with_columns(pl.sum_horizontal(bill_cols).alias("total_bill"))
        .join(income_df.select(bldg_id_col, income_col), on=bldg_id_col, how="inner")
        .with_columns(
            (pl.col("total_bill") / (pl.col(income_col) * income_cpi_ratio)).alias("burden"),
        )
        .with_columns((pl.col("burden") > burden_threshold).alias("is_burdened"))
    )
    total_weight = float(annual["weight"].sum())
    burdened_weight = float(annual.filter(pl.col("is_burdened"))["weight"].sum())
    pct_above = burdened_weight / total_weight * 100
    pct_below = 100 - pct_above
    return (pct_below, pct_above)


def plot_burden_bar_by_utility(
    burden_data: dict[str, dict[str, tuple[float, float]]],
    utility_names: dict[str, str],
    utility_order_codes: list[str],
    scenario_keys: list[str],
    scenario_labels: list[str],
    burden_threshold: float = 0.06,
    title: str = "",
) -> Figure:
    """Diverging burden bars (above/below *burden_threshold*) for each utility.

    *burden_data* is ``{utility_code: {scenario_key: (pct_below, pct_above)}}``
    -- exactly the shape produced by calling ``burden_shares()`` once per
    utility per scenario. *utility_order_codes* fixes utility ordering (top to
    bottom); utilities present in *burden_data* but missing from
    *utility_order_codes* are silently dropped. *scenario_keys* indexes into
    each utility's per-scenario dict, in the order bars are drawn within a
    utility's group; *scenario_labels* are the labels drawn next to those bars
    (same length and order as *scenario_keys*).

    Draws with raw matplotlib -- bar heights, group spacing, and the
    threshold-line/label layout don't map cleanly onto plotnine's grammar.
    Returns the ``Figure``; wrap in ``display_svg``/``display_figure`` to embed.
    """
    from lib.plotnine import SB_COLORS

    bar_height = 0.55
    group_gap = 0.7
    intra_gap = 0.15
    header_space = 0.55
    label_space = 0.35

    label_above = f"ENERGY BURDEN ABOVE {burden_threshold:.0%}"
    label_below = f"ENERGY BURDEN BELOW {burden_threshold:.0%}"

    ordered_codes = list(reversed(utility_order_codes))
    active_codes = [c for c in ordered_codes if c in burden_data]
    n_utils = len(active_codes)
    n_scenarios = len(scenario_keys)

    bar_positions: list[float] = []
    bar_labels: list[str] = []
    bar_above: list[float] = []
    bar_below: list[float] = []
    utility_header_ys: list[tuple[float, str]] = []
    label_rows: list[tuple[float, float]] = []

    y = 0.0
    for u_idx, code in enumerate(active_codes):
        utility_header_ys.append((y, utility_names[code]))
        y += header_space

        # Both header labels sit the same distance from the center line (mirrored),
        # rather than each centered on its own side's average bar width -- above and
        # below values are complementary (they sum to 100 per bar), so this average
        # is a stable, data-derived offset rather than a hardcoded constant.
        group_values = [burden_data[code][key] for key in scenario_keys]
        label_offset = sum(below + above for below, above in group_values) / (4 * len(group_values))
        label_rows.append((y, label_offset))
        y += label_space

        for s_idx, key in enumerate(scenario_keys):
            below, above = burden_data[code][key]
            bar_positions.append(y)
            bar_labels.append(scenario_labels[s_idx])
            bar_above.append(above)
            bar_below.append(below)
            y += bar_height + (intra_gap if s_idx < n_scenarios - 1 else 0)
        if u_idx < n_utils - 1:
            y += group_gap

    y_max = y + 0.1
    fig_height = 1.5 + n_utils * 3.6

    fig, ax = pyplot.subplots(figsize=(12.5, fig_height))
    ax.set_xlim(-100, 100)
    ax.set_ylim(-0.1, y_max)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    carrot = SB_COLORS["carrot"]
    sky = SB_COLORS["sky"]

    for bp, above, below in zip(bar_positions, bar_above, bar_below, strict=True):
        ax.barh(bp, above, left=0, height=bar_height, color=carrot, edgecolor="none", align="edge")
        ax.barh(bp, -below, left=0, height=bar_height, color=sky, edgecolor="none", align="edge")
        if above >= 3:
            ax.text(
                above / 2,
                bp + bar_height / 2,
                f"{round(above)}%",
                ha="center",
                va="center",
                color="white",
                fontsize=10,
                fontweight="bold",
                fontfamily="IBM Plex Sans",
            )
        if below >= 3:
            ax.text(
                -below / 2,
                bp + bar_height / 2,
                f"{round(below)}%",
                ha="center",
                va="center",
                color="white",
                fontsize=10,
                fontweight="bold",
                fontfamily="IBM Plex Sans",
            )

    for bp, label in zip(bar_positions, bar_labels, strict=True):
        ax.text(
            101,
            bp + bar_height / 2,
            label,
            ha="left",
            va="center",
            fontsize=8,
            fontweight="bold",
            fontfamily="IBM Plex Sans",
        )

    for header_y, util_name in utility_header_ys:
        ax.text(
            -100,
            header_y,
            util_name,
            ha="left",
            va="top",
            fontsize=11,
            fontweight="bold",
            fontfamily="GT Planar",
            color="#333333",
        )

    ax.axvline(x=0, color="#333333", linewidth=1.5)

    for label_y, label_offset in label_rows:
        ax.text(
            label_offset,
            label_y,
            label_above,
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
            color=carrot,
            fontfamily="IBM Plex Sans",
        )
        ax.text(
            -label_offset,
            label_y,
            label_below,
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
            color=sky,
            fontfamily="IBM Plex Sans",
        )

    fig.subplots_adjust(left=0.02, right=0.82, top=0.95, bottom=0.01)

    if title:
        ax_pos = ax.get_position()
        fig.text(
            ax_pos.x0,
            0.97,
            title,
            fontsize=12,
            fontweight="bold",
            fontfamily="GT Planar",
            color="black",
            va="top",
        )

    return fig


# --- HP overpayment / BAT -------------------------------------------------------


def hp_bat_summary(
    state: str,
    batch: str,
    scenario: str,
    *,
    bat_col: str = "BAT_percustomer_delivery",
    group_col: str = "postprocess_group.has_hp",
    group_value: bool = True,
) -> dict:
    """Weighted mean and total $/yr BAT for one group, always read from ``{scenario}_precalc``.

    Positive BAT = overpaying relative to cost of service; negative = underpaying.
    """
    bat = cast("pl.DataFrame", load_master_bat(state, batch, segment_name(scenario, "precalc")).collect())
    sub = bat.filter(pl.col(group_col) == group_value)
    total_per_year = float((sub[bat_col] * sub["weight"]).sum())
    return {
        "scenario": scenario,
        "mean_per_year": weighted_mean(sub, bat_col, "weight"),
        "total_per_year_millions": total_per_year / 1e6,
        "n_weighted": float(sub["weight"].sum()),
    }


def bat_by_group(
    state: str,
    batch: str,
    scenario: str,
    *,
    bat_col: str = "BAT_percustomer_delivery",
    group_col: str = "postprocess_group.heating_type_v2",
    residual: str | None = None,
) -> pl.DataFrame:
    """Weighted mean BAT and cost-of-service components by *group_col*.

    Always read from ``{scenario}_precalc``. Columns:

    - ``mean_per_year`` — weighted mean of *bat_col* (over/underpayment)
    - ``revenue_per_customer`` — weighted mean ``annual_bill_delivery``
    - ``marginal_cost_per_customer`` — weighted mean ``economic_burden_delivery``
    - ``residual_per_customer`` — weighted mean ``residual_share_*_delivery``
    - ``cost_of_service_per_customer`` — weighted mean
      ``economic_burden_delivery + residual_share_*_delivery``
    - ``n_weighted`` — sum of sample weights

    *residual* selects the residual-share column the same way as
    ``cost_of_service_by_subclass``: ``None`` / ``"percustomer"`` →
    ``residual_share_delivery``; otherwise ``residual_share_{residual}_delivery``.
    """
    residual_col = (
        "residual_share_delivery"
        if residual is None or residual == "percustomer"
        else f"residual_share_{residual}_delivery"
    )

    bat = cast("pl.DataFrame", load_master_bat(state, batch, segment_name(scenario, "precalc")).collect())
    return (
        bat.with_columns(
            (pl.col("economic_burden_delivery") + pl.col(residual_col)).alias("_cost_of_service"),
        )
        .group_by(group_col)
        .agg(
            ((pl.col(bat_col) * pl.col("weight")).sum() / pl.col("weight").sum()).alias("mean_per_year"),
            ((pl.col("annual_bill_delivery") * pl.col("weight")).sum() / pl.col("weight").sum()).alias(
                "revenue_per_customer"
            ),
            ((pl.col("economic_burden_delivery") * pl.col("weight")).sum() / pl.col("weight").sum()).alias(
                "marginal_cost_per_customer"
            ),
            ((pl.col(residual_col) * pl.col("weight")).sum() / pl.col("weight").sum()).alias("residual_per_customer"),
            ((pl.col("_cost_of_service") * pl.col("weight")).sum() / pl.col("weight").sum()).alias(
                "cost_of_service_per_customer"
            ),
            pl.col("weight").sum().alias("n_weighted"),
        )
        .sort("n_weighted", descending=True)
    )


def compare_bat_across_scenarios(state: str, batch: str, scenarios: list[str], **kwargs) -> pl.DataFrame:
    """One row per scenario of ``hp_bat_summary``, for a before/after table.

    E.g. ``compare_bat_across_scenarios(state, batch, ["default", "hp_seasonal_percustomer_passthrough"])``
    gives the HP subclass's overpayment before and after a reform tariff in one table.
    """
    rows = [hp_bat_summary(state, batch, scenario, **kwargs) for scenario in scenarios]
    return pl.DataFrame(rows)


# --- Cost of service by subclass -------------------------------------------------


def cost_of_service_by_subclass(
    state: str,
    batch: str,
    utility: str,
    scenario: str,
    *,
    group_col: str = "postprocess_group.heating_type_v2",
    bat_col: str = "BAT_percustomer_delivery",
    residual: str | None = None,
) -> pl.DataFrame:
    """Delivery revenue, cost of service, and cross-subsidy by heating-type subclass.

    Reads master BAT at ``{scenario}_precalc`` (BAT is only valid at precalc,
    see module docstring) filtered to *utility*, joins CAIRO's raw per-building
    kWh export (``load_billing_kwh_annual``) on ``bldg_id``, and aggregates by
    *group_col*.

    "Cost of service" is ``economic_burden_delivery + residual_share_*_delivery``
    -- confirmed to reconstruct ``annual_bill_delivery`` together with
    ``BAT_percustomer_delivery`` (the module's default ``bat_col``) to within
    floating-point error, i.e. ``economic_burden + residual_share + BAT ==
    annual_bill``. The residual column is ``residual_share_delivery`` when
    *residual* is ``None`` or ``"percustomer"``, else
    ``residual_share_{residual}_delivery`` (e.g. ``"epmc"`` →
    ``residual_share_epmc_delivery``). Percentages are self-normalized against
    the weighted total across all customers, not an external
    revenue-requirement figure -- that's state/docket-specific and not
    available for every state.

    Returns one row per *group_col* value present in the data (ordered by
    ``HEATING_ORDER`` when *group_col* is the default heating-type column) plus
    a trailing "All customers" total row, with columns ``subclass``,
    ``n_customers``, ``consumption_gwh``, ``revenue_delivery``,
    ``marginal_cost``, ``residual``, ``cost_of_service`` (= marginal + residual),
    ``cross_subsidy``, and their ``pct_all_*`` shares plus
    ``pct_overpayment_vs_cos`` (``cross_subsidy / cost_of_service``).
    """
    residual_col = (
        "residual_share_delivery"
        if residual is None or residual == "percustomer"
        else f"residual_share_{residual}_delivery"
    )

    bat = cast(
        "pl.DataFrame",
        load_master_bat(state, batch, segment_name(scenario, "precalc"))
        .filter(pl.col("sb.electric_utility") == utility)
        .collect(),
    )
    kwh = cast(
        "pl.DataFrame",
        load_billing_kwh_annual(state, utility, batch, segment_name(scenario, "precalc")).collect(),
    )
    joined = bat.join(kwh, on="bldg_id", how="inner", validate="1:1").with_columns(
        (pl.col("economic_burden_delivery") + pl.col(residual_col)).alias("cost_of_service"),
    )

    by_group = (
        joined.group_by(group_col)
        .agg(
            pl.col("weight").sum().alias("n_customers"),
            (pl.col("weight") * pl.col("annual_kwh_grid")).sum().alias("total_kwh"),
            (pl.col("weight") * pl.col("annual_bill_delivery")).sum().alias("revenue_delivery"),
            (pl.col("weight") * pl.col("economic_burden_delivery")).sum().alias("marginal_cost"),
            (pl.col("weight") * pl.col(residual_col)).sum().alias("residual"),
            (pl.col("weight") * pl.col("cost_of_service")).sum().alias("cost_of_service"),
            (pl.col("weight") * pl.col(bat_col)).sum().alias("cross_subsidy"),
        )
        .rename({group_col: "subclass"})
    )
    if group_col == "postprocess_group.heating_type_v2":
        by_group = by_group.with_columns(
            pl.col("subclass").replace_strict(HEATING_TYPE_LABELS, default=pl.col("subclass")),
        )
        row_order = [*(h for h in HEATING_ORDER if h in by_group["subclass"].to_list()), "All customers"]
    else:
        row_order = [*by_group["subclass"].to_list(), "All customers"]

    total_row = by_group.select(
        pl.lit("All customers").alias("subclass"),
        pl.col("n_customers").sum(),
        pl.col("total_kwh").sum(),
        pl.col("revenue_delivery").sum(),
        pl.col("marginal_cost").sum(),
        pl.col("residual").sum(),
        pl.col("cost_of_service").sum(),
        pl.col("cross_subsidy").sum(),
    )

    cos_tbl = (
        pl.concat([by_group, total_row], how="vertical")
        .with_columns(pl.col("subclass").cast(pl.Enum(row_order)))
        .sort("subclass")
    )

    total_customers = float(by_group["n_customers"].sum())
    total_kwh = float(by_group["total_kwh"].sum())
    total_revenue = float(by_group["revenue_delivery"].sum())
    total_cos = float(by_group["cost_of_service"].sum())

    return (
        cos_tbl.with_columns(
            (pl.col("total_kwh") / 1e6).alias("consumption_gwh"),
            (pl.col("n_customers") / total_customers).alias("pct_all_customers"),
            (pl.col("total_kwh") / total_kwh).alias("pct_all_consumption"),
            (pl.col("revenue_delivery") / total_revenue).alias("pct_all_revenue"),
            (pl.col("cost_of_service") / total_cos).alias("pct_all_cost_of_service"),
            pl.when(pl.col("cost_of_service") > 0)
            .then(pl.col("cross_subsidy") / pl.col("cost_of_service"))
            .otherwise(None)
            .alias("pct_overpayment_vs_cos"),
        )
        .drop("total_kwh")
        .select(
            "subclass",
            "n_customers",
            "pct_all_customers",
            "consumption_gwh",
            "pct_all_consumption",
            "revenue_delivery",
            "pct_all_revenue",
            "marginal_cost",
            "residual",
            "cost_of_service",
            "pct_all_cost_of_service",
            "cross_subsidy",
            "pct_overpayment_vs_cos",
        )
    )


# --- Revenue requirement breakdown (marginal cost vs. residual) -----------------

REVENUE_REQ_COMPONENT_COLORS: dict[str, str] = {
    "Marginal cost": "#023047",  # SB_COLORS["midnight"] -- hardcoded to avoid importing lib.plotnine at module load
    "Residual": "#fc9706",  # SB_COLORS["carrot"]
}
# Enum order for geom_col(position="stack"): the *first* level renders at the
# top of a vertical stack (last at the bottom); after coord_flip that puts the
# first level at the left of the horizontal bar. Listing "Residual" first here
# puts "Marginal cost" at the left / "Residual" at the right, reading
# left-to-right in the same order as the legend (which uses the reversed list
# as its `breaks`, since legend order isn't reversed by coord_flip).
REVENUE_REQ_COMPONENT_ORDER = ["Residual", "Marginal cost"]


def revenue_requirement_breakdown_by_subclass(
    state: str,
    batch: str,
    utility: str,
    scenario: str,
    *,
    group_col: str = "postprocess_group.heating_type_v2",
) -> pl.DataFrame:
    """Delivery revenue requirement split into marginal cost recovery vs. residual, by subclass.

    Reads master BAT at ``{scenario}_precalc`` (BAT/cost-of-service columns
    are only valid at precalc, see module docstring) filtered to *utility*,
    and sums each customer's ``economic_burden_delivery`` (the marginal-cost
    -based charge) and ``residual_share_delivery`` (the allocated residual
    revenue requirement) by *group_col*. Together these two components sum to
    the same ``cost_of_service`` total ``cost_of_service_by_subclass()``
    computes -- this function keeps the two pieces separate instead of
    combining them, for a marginal-cost-vs-residual chart rather than a
    cross-subsidy table.

    Long-form output, one row per ``(subclass, component)``, ready for
    ``plot_revenue_requirement_breakdown()``. Columns: ``subclass``,
    ``component`` (``"Marginal cost"`` or ``"Residual"``), ``value`` ($/yr).
    Includes a trailing ``"All customers"`` subclass with the utility-wide
    total.
    """
    bat = cast(
        "pl.DataFrame",
        load_master_bat(state, batch, segment_name(scenario, "precalc"))
        .filter(pl.col("sb.electric_utility") == utility)
        .collect(),
    )
    by_group = (
        bat.group_by(group_col)
        .agg(
            (pl.col("weight") * pl.col("economic_burden_delivery")).sum().alias("Marginal cost"),
            (pl.col("weight") * pl.col("residual_share_delivery")).sum().alias("Residual"),
        )
        .rename({group_col: "subclass"})
    )
    if group_col == "postprocess_group.heating_type_v2":
        by_group = by_group.with_columns(
            pl.col("subclass").replace_strict(HEATING_TYPE_LABELS, default=pl.col("subclass")),
        )
        row_order = [*(h for h in HEATING_ORDER if h in by_group["subclass"].to_list()), "All customers"]
    else:
        row_order = [*by_group["subclass"].to_list(), "All customers"]

    total_row = by_group.select(
        pl.lit("All customers").alias("subclass"),
        pl.col("Marginal cost").sum(),
        pl.col("Residual").sum(),
    )

    wide = (
        pl.concat([by_group, total_row], how="vertical")
        .with_columns(pl.col("subclass").cast(pl.Enum(row_order)))
        .sort("subclass")
    )
    return wide.unpivot(
        on=["Marginal cost", "Residual"],
        index="subclass",
        variable_name="component",
        value_name="value",
    )


def plot_revenue_requirement_breakdown(
    breakdown: pl.DataFrame,
    *,
    title: str = "Delivery revenue requirement: marginal cost vs. residual",
    include_total: bool = False,
) -> ggplot:
    """Stacked horizontal bar chart of the marginal-cost / residual split by subclass.

    Takes the long-form output of ``revenue_requirement_breakdown_by_subclass()``
    directly. Drops the ``"All customers"`` row by default -- the utility-wide
    total dwarfs every individual subclass on a shared dollar axis, making the
    per-subclass bars unreadable; pass ``include_total=True`` to keep it as an
    extra bar (e.g. for a single-utility summary chart with no subclasses).

    No in-bar dollar labels: subclasses vary too widely in magnitude for a
    single label-size threshold to work well (small subclasses' segments are
    too narrow), and the exact figures already live in the companion
    ``cost_of_service_by_subclass()`` table.
    """
    import plotnine as plt

    from lib.plotnine import theme_switchbox

    df = breakdown if include_total else breakdown.filter(pl.col("subclass") != "All customers")
    avail = [s for s in HEATING_ORDER if s in df["subclass"].to_list()]
    if include_total:
        avail = [*avail, "All customers"]
    if not avail:
        raise ValueError("No subclasses remain to plot in `breakdown` (empty after excluding 'All customers'?).")

    plot_df = df.with_columns(
        pl.col("subclass").cast(pl.String).cast(pl.Enum(list(reversed(avail)))),
        pl.col("component").cast(pl.Enum(REVENUE_REQ_COMPONENT_ORDER)),
        (pl.col("value") / 1e6).alias("value_millions"),
    )

    return (
        plt.ggplot(plot_df, plt.aes(x="subclass", y="value_millions", fill="component"))
        + plt.geom_col(position="stack", width=0.6)
        + plt.scale_fill_manual(values=REVENUE_REQ_COMPONENT_COLORS, breaks=list(reversed(REVENUE_REQ_COMPONENT_ORDER)))
        + plt.scale_y_continuous(expand=(0, 0, 0.06, 0))
        + plt.coord_flip()
        + plt.labs(x="", y="$ millions / year", fill="", title=title)
        + theme_switchbox()
        + plt.theme(figure_size=(10.5, max(3.5, 1.0 + 0.9 * len(avail))))
    )


# --- Representative household + monthly decomposition ---------------------------


def weighted_median_bldg_id(df: pl.DataFrame, sort_col: str, weight_col: str = "weight") -> int:
    """Return the ``bldg_id`` at the weighted median of *sort_col*.

    Same logic as picking a representative row, but returns just the ID so it
    can be reused to select a representative building from any filtered
    population, then pull whatever other data (e.g. monthly bills) is needed
    for that specific building.
    """
    total_weight = float(df[weight_col].sum())
    sorted_df = df.sort(sort_col)
    cum = sorted_df[weight_col].cum_sum()
    median_row = sorted_df.filter(cum >= 0.5 * total_weight).head(1)
    if median_row.is_empty():
        raise ValueError("Cannot compute weighted median bldg_id: empty data or non-positive weights")
    return int(median_row["bldg_id"][0])


def monthly_bill_components(state: str, batch: str, segment: str, bldg_id: int) -> pl.DataFrame:
    """Return one building's 12 monthly electric bill rows, decomposed into delivery vs. supply.

    Long-form ``(month, component, value)``, ``component`` in
    ``{"Electric Delivery Bill", "Electric Supply Bill"}``
    (``elec_fixed_charge + elec_delivery_bill`` vs. ``elec_supply_bill``).
    ``month`` is ordered Jan-Dec (the ``"Annual"`` row is excluded).
    """
    filtered = (
        load_master_bills(state, batch, segment)
        .filter((pl.col("bldg_id") == bldg_id) & (pl.col("month") != "Annual"))
        .select(
            pl.col("month").cast(pl.Enum(MONTH_ORDER)),
            (pl.col("elec_fixed_charge") + pl.col("elec_delivery_bill")).alias("Electric Delivery Bill"),
            pl.col("elec_supply_bill").alias("Electric Supply Bill"),
        )
    )
    bills = cast("pl.DataFrame", filtered.collect()).sort("month")
    return bills.unpivot(
        on=["Electric Delivery Bill", "Electric Supply Bill"],
        index="month",
        variable_name="component",
        value_name="value",
    )


MONTHLY_BILL_COMPONENT_ORDER = ["Electric Supply Bill", "Electric Delivery Bill"]
MONTHLY_BILL_COMPONENT_COLORS: dict[str, str] = {
    "Electric Delivery Bill": "#023047",  # SB_COLORS["midnight"]
    "Electric Supply Bill": "#fc9706",  # SB_COLORS["carrot"]
}


def plot_monthly_bill_components(monthly_df: pl.DataFrame, title: str) -> ggplot:
    """Stacked monthly electric bill chart, delivery vs. supply.

    Takes the long-form output of ``monthly_bill_components()`` directly.
    """
    import plotnine as plt

    from lib.plotnine import theme_switchbox

    plot_df = monthly_df.with_columns(pl.col("component").cast(pl.Enum(MONTHLY_BILL_COMPONENT_ORDER)))

    return (
        plt.ggplot(plot_df, plt.aes(x="month", y="value", fill="component"))
        + plt.geom_col(position="stack", width=0.7)
        + plt.scale_fill_manual(values=MONTHLY_BILL_COMPONENT_COLORS, breaks=MONTHLY_BILL_COMPONENT_ORDER)
        + plt.scale_x_discrete(limits=MONTH_ORDER)
        + plt.scale_y_continuous(expand=(0, 0, 0.08, 0))
        + plt.labs(x="", y="$ / month", fill="", title=title)
        + theme_switchbox()
        + plt.theme(figure_size=(10.5, 4.5))
    )


def annual_bill_components(state: str, batch: str, segment: str, bldg_id: int) -> dict[str, float]:
    """Return one building's annual bill, decomposed into delivery fixed/volumetric, supply, and gas.

    Companion to ``monthly_bill_components()`` — same inputs, but the
    ``"Annual"`` row instead of the 12 monthly rows, with delivery split into
    ``delivery_fixed``/``delivery_volumetric`` (not combined) so callers can
    build a full electric+gas bill decomposition for a single household.
    """
    row = cast(
        "pl.DataFrame",
        load_master_bills(state, batch, segment)
        .filter((pl.col("bldg_id") == bldg_id) & (pl.col("month") == "Annual"))
        .select(
            pl.col("elec_fixed_charge").alias("delivery_fixed"),
            pl.col("elec_delivery_bill").alias("delivery_volumetric"),
            pl.col("elec_supply_bill").alias("supply"),
            pl.col("gas_total_bill").alias("gas"),
            pl.col("energy_total_bill").alias("energy_total"),
        )
        .collect(),
    )
    return {col: float(row[col][0]) for col in row.columns}


# --- Representative household cost-breakdown chart -------------------------------

# Only kWh, marginal cost, and delivery volumetric get an "existing" /
# "incremental" split in the HP bar -- residual and the fixed charge are flat,
# per-customer costs that don't move with load, so they render as a single block
# in both bars (which is itself part of the story: they *shouldn't* grow with
# incremental consumption). Incremental segments always stack last (on top),
# regardless of metric.
COST_BREAKDOWN_COLORS: dict[str, str] = {
    "kWh (existing)": "#023047",
    "kWh (incremental)": "#5b90a8",
    "Marginal Cost (existing)": "#1b7837",
    "Marginal Cost (incremental)": "#7cb894",
    "Residual": "#a6dba0",
    "Delivery Fixed": "#023047",
    "Delivery Volumetric (existing)": "#56B4E9",
    "Delivery Volumetric (incremental)": "#a9d8f0",
}
COST_BREAKDOWN_LABEL_COLORS: dict[str, str] = {
    "kWh (existing)": "white",
    "kWh (incremental)": "white",
    "Marginal Cost (existing)": "white",
    "Marginal Cost (incremental)": "#333333",
    "Residual": "#333333",
    "Delivery Fixed": "white",
    "Delivery Volumetric (existing)": "white",
    "Delivery Volumetric (incremental)": "#333333",
}
# Components measured in kWh rather than dollars, for annotation formatting.
_COST_BREAKDOWN_KWH_COMPONENTS = {"kWh (existing)", "kWh (incremental)"}


def representative_cost_data(
    state: str,
    utility: str,
    batch: str,
    bldg_id: int,
    hp_segment: str,
    *,
    ng_segment: str | None = None,
    residual: str = "percustomer",
) -> dict[str, dict[str, float]]:
    """Collect one building's kWh, marginal cost, residual, and delivery-bill
    components for its baseline (natural-gas) and heat-pump states, for
    ``plot_representative_cost_breakdown()``.

    *ng_segment* (default ``"default_precalc"``) is the building's actual,
    un-recalibrated baseline: upgrade 00, today's default tariff. It's the
    same regardless of which HP scenario is being examined. *hp_segment* is
    any ``*_calibrated`` segment (upgrade 02, e.g. ``"default_calibrated"``,
    ``"hp_seasonal_percustomer_passthrough_calibrated"``) and is what varies
    across chart calls -- this is the "one route for default precalc [the NG
    side], one route for any calibrated tariff [the HP side]" the chart needs.

    Per the module-level PR #503 note, the per-customer residual allocation
    reflects utility-wide costs and doesn't change when one building switches
    to a heat pump, so *ng_segment*'s residual is reused for the HP side too,
    rather than reading the unreliable calibrated-stage residual.
    """
    ng_segment = ng_segment or segment_name("default", "precalc")
    residual_col = (
        "residual_share_delivery"
        if residual is None or residual == "percustomer"
        else f"residual_share_{residual}_delivery"
    )

    def _marginal_cost(segment: str) -> float:
        # economic_burden_delivery (marginal cost) is pure load x MC and valid
        # at both precalc and calibrated (see module docstring); suppress the
        # calibrated-stage BAT warning here since we deliberately do read it.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*not a `_precalc` segment.*")
            row = cast(
                "pl.DataFrame",
                load_master_bat(state, batch, segment)
                .filter(pl.col("bldg_id") == bldg_id)
                .select(pl.col("economic_burden_delivery").alias("mc"))
                .collect(),
            )
        return float(row["mc"][0])

    def _kwh(segment: str) -> float:
        row = cast(
            "pl.DataFrame",
            load_billing_kwh_annual(state, utility, batch, segment)
            .filter(pl.col("bldg_id") == bldg_id)
            .select("annual_kwh_grid")
            .collect(),
        )
        return float(row["annual_kwh_grid"][0])

    ng_residual_row = cast(
        "pl.DataFrame",
        load_master_bat(state, batch, ng_segment)
        .filter(pl.col("bldg_id") == bldg_id)
        .select(pl.col(residual_col).alias("residual"))
        .collect(),
    )
    ng_residual = float(ng_residual_row["residual"][0])

    ng_bill = annual_bill_components(state, batch, ng_segment, bldg_id)
    hp_bill = annual_bill_components(state, batch, hp_segment, bldg_id)

    return {
        "ng": {
            "kwh": _kwh(ng_segment),
            "mc": _marginal_cost(ng_segment),
            "residual": ng_residual,
            "delivery_fixed": ng_bill["delivery_fixed"],
            "delivery_volumetric": ng_bill["delivery_volumetric"],
        },
        "hp": {
            "kwh": _kwh(hp_segment),
            "mc": _marginal_cost(hp_segment),
            "residual": ng_residual,
            "delivery_fixed": hp_bill["delivery_fixed"],
            "delivery_volumetric": hp_bill["delivery_volumetric"],
        },
    }


DECOMPOSED_BILL_COMPONENT_KEYS = ["delivery_fixed", "delivery_volumetric", "supply", "gas"]
DECOMPOSED_BILL_COLORS: dict[str, str] = {
    "delivery_fixed": "#023047",
    "delivery_volumetric": "#56B4E9",
    "supply": "#E69F00",
    "gas": "#CCCCCC",
}
DECOMPOSED_BILL_LABEL_COLORS: dict[str, str] = {**DECOMPOSED_BILL_COLORS, "gas": "#888888"}


def _fmt_dollar(v: float) -> str:
    return f"${v:,.0f}"


def plot_decomposed_bill_3bar(
    before: dict[str, float],
    after_default: dict[str, float],
    after_reform: dict[str, float],
    *,
    third_scenario_label: str,
    title: str,
    side_labels: dict[str, str] | None = None,
) -> tuple[Figure, float, float, float, float]:
    """Three-bar decomposed annual bill chart: natural gas, HP on the default rate, HP on a reform rate.

    Each of *before*, *after_default*, *after_reform* is an
    ``annual_bill_components()``-shaped dict (``delivery_fixed``,
    ``delivery_volumetric``, ``supply``, ``gas``). *third_scenario_label*
    names the reform bar (e.g. ``"Heat pump\\n(seasonal rate)"``).

    Draws with raw matplotlib (not plotnine) for the per-segment $ labels,
    the dashed "today's delivery cost" reference line, and the bracketed
    savings annotation between the second and third bars — none of which map
    cleanly onto plotnine's grammar.

    Returns ``(fig, savings $, savings pct as a fraction, total default-rate
    HP bill, total reform-rate HP bill)``.
    """
    from lib.plotnine import SB_COLORS

    scenarios = ["Natural gas\nfurnace", "Heat pump\n(default rate)", third_scenario_label]
    x = np.arange(len(scenarios))
    w = 0.55
    comp_keys = DECOMPOSED_BILL_COMPONENT_KEYS
    bars_data = [before, after_default, after_reform]

    fig, ax = pyplot.subplots(figsize=(12, 7))
    ax.set_title(
        title,
        fontfamily="GT Planar",
        fontweight="bold",
        fontsize=15,
        loc="left",
        pad=12,
    )

    bottoms = [0.0] * 3
    for ck in comp_keys:
        vals = [bars_data[i][ck] for i in range(3)]
        ax.bar(x, vals, w, bottom=bottoms, color=DECOMPOSED_BILL_COLORS[ck], edgecolor="none")
        for i, (v, b) in enumerate(zip(vals, bottoms, strict=False)):
            if v > 80:
                ax.text(
                    x[i],
                    b + v / 2,
                    _fmt_dollar(v),
                    ha="center",
                    va="center",
                    color="white",
                    fontweight="bold",
                    fontsize=11,
                    zorder=11,
                )
        bottoms = [b + v for b, v in zip(bottoms, vals, strict=False)]

    totals = [sum(bars_data[i][k] for k in comp_keys) for i in range(3)]

    for i in (0, 1):
        ax.text(
            x[i],
            totals[i] + 50,
            _fmt_dollar(totals[i]),
            ha="center",
            va="bottom",
            color="#333333",
            fontweight="bold",
            fontsize=12,
        )

    delivery_before = before["delivery_fixed"] + before["delivery_volumetric"]
    ax.hlines(
        y=delivery_before,
        xmin=-0.5,
        xmax=x[2] + w / 2,
        color=SB_COLORS["saffron"],
        linewidth=1.8,
        linestyle=(0, (6, 4)),
        zorder=10,
    )

    savings = totals[1] - totals[2]
    pct_savings = savings / totals[1] * 100

    rect = mpatches.FancyBboxPatch(
        (x[2] - w / 2, totals[2]),
        w,
        savings,
        boxstyle="square,pad=0",
        facecolor=SB_COLORS["saffron"],
        alpha=0.12,
        edgecolor="#B8960A",
        linewidth=2.0,
        linestyle=(0, (5, 3)),
        hatch="////",
        zorder=3,
    )
    ax.add_patch(rect)

    ax.text(
        x[2],
        totals[2] + 50,
        _fmt_dollar(totals[2]),
        ha="center",
        va="bottom",
        color="#333333",
        fontweight="bold",
        fontsize=12,
        zorder=8,
    )
    ax.annotate(
        "",
        xy=(x[2], totals[2] + 180),
        xytext=(x[2], totals[1] - 60),
        arrowprops={"arrowstyle": "->,head_length=0.4,head_width=0.25", "color": SB_COLORS["saffron"], "lw": 2.2},
        zorder=6,
    )
    ax.text(
        x[2],
        totals[1] + 180,
        f"-{pct_savings:.0f}%",
        ha="center",
        va="bottom",
        color=SB_COLORS["saffron"],
        fontweight="bold",
        fontsize=14,
    )
    ax.text(
        x[2],
        totals[1] + 50,
        f"-{_fmt_dollar(savings)}",
        ha="center",
        va="bottom",
        color=SB_COLORS["saffron"],
        fontsize=11,
        alpha=0.8,
    )

    _labels = side_labels or {}
    side_x = x[2] + w / 2 + 0.15
    d3 = after_reform
    side_specs = [
        (
            _labels.get("delivery_fixed", "Delivery\n(Fixed)"),
            d3["delivery_fixed"] / 2,
            DECOMPOSED_BILL_LABEL_COLORS["delivery_fixed"],
        ),
        (
            _labels.get("delivery_volumetric", "Delivery\n(Volumetric)"),
            d3["delivery_fixed"] + d3["delivery_volumetric"] / 2,
            DECOMPOSED_BILL_LABEL_COLORS["delivery_volumetric"],
        ),
        (
            _labels.get("supply", "Supply"),
            d3["delivery_fixed"] + d3["delivery_volumetric"] + d3["supply"] / 2,
            DECOMPOSED_BILL_LABEL_COLORS["supply"],
        ),
        (
            _labels.get("gas", "Gas"),
            d3["delivery_fixed"] + d3["delivery_volumetric"] + d3["supply"] + d3["gas"] / 2,
            DECOMPOSED_BILL_LABEL_COLORS["gas"],
        ),
    ]
    for lbl, ym, clr in side_specs:
        ax.plot([x[2] + w / 2 + 0.02, side_x - 0.03], [ym, ym], color=clr, linewidth=0.7, alpha=0.6)
        ax.text(side_x, ym, lbl, color=clr, ha="left", va="center", fontsize=11, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=11)
    ax.set_ylabel("Annual energy bill ($)", fontsize=12)
    ax.set_ylim(0, max(totals) * 1.22)
    ax.set_xlim(-0.5, x[2] + w / 2 + 0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_bounds(-0.5, x[2] + w / 2)
    fig.tight_layout()
    return fig, savings, pct_savings / 100, totals[1], totals[2]


def plot_decomposed_bill_2bar(
    before: dict[str, float],
    after: dict[str, float],
    *,
    bar_labels: tuple[str, str],
    title: str,
    reserve_third: bool = False,
    side_labels: dict[str, str] | None = None,
) -> Figure:
    """Two-bar decomposed annual bill chart: fossil-fuel furnace vs. heat pump.

    Each of *before* and *after* is a dict with keys matching
    ``DECOMPOSED_BILL_COMPONENT_KEYS`` (``delivery_fixed``,
    ``delivery_volumetric``, ``supply``, ``gas``).  *bar_labels* names the
    two bars (e.g. ``("Natural gas\\nfurnace", "Heat pump")``).

    When *reserve_third* is True, the chart reserves space for a third bar
    slot (matching the layout of ``plot_decomposed_bill_3bar``) so the two
    charts share identical bar widths and proportions.

    Draws with raw matplotlib for per-segment dollar labels and total
    annotations.  Returns the ``Figure`` (caller uses ``display_figure``).
    """
    scenarios = list(bar_labels)
    n_slots = 3 if reserve_third else 2
    x = np.arange(n_slots)
    w = 0.55
    comp_keys = DECOMPOSED_BILL_COMPONENT_KEYS
    bars_data = [before, after]

    figsize = (12, 7) if reserve_third else (10.5, 6)
    fig, ax = pyplot.subplots(figsize=figsize)
    ax.set_title(
        title,
        fontfamily="GT Planar",
        fontweight="bold",
        fontsize=15,
        loc="left",
        pad=12,
    )

    bottoms = [0.0, 0.0]
    for ck in comp_keys:
        vals = [bars_data[i][ck] for i in range(2)]
        ax.bar(x[:2], vals, w, bottom=bottoms, color=DECOMPOSED_BILL_COLORS[ck], edgecolor="none")
        for i, (v, b) in enumerate(zip(vals, bottoms, strict=False)):
            if v > 80:
                ax.text(
                    x[i],
                    b + v / 2,
                    _fmt_dollar(v),
                    ha="center",
                    va="center",
                    color="white",
                    fontweight="bold",
                    fontsize=11,
                    zorder=11,
                )
        bottoms = [b + v for b, v in zip(bottoms, vals, strict=False)]

    totals = [sum(bars_data[i][k] for k in comp_keys) for i in range(2)]

    for i in range(2):
        ax.text(
            x[i],
            totals[i] + 40,
            _fmt_dollar(totals[i]),
            ha="center",
            va="bottom",
            color="#333333",
            fontweight="bold",
            fontsize=12,
        )

    _labels = side_labels or {}
    side_x = x[1] + w / 2 + 0.15
    y_cursor = 0.0
    for key, label in [
        ("delivery_fixed", _labels.get("delivery_fixed", "Delivery\n(Fixed)")),
        ("delivery_volumetric", _labels.get("delivery_volumetric", "Delivery\n(Volumetric)")),
        ("supply", _labels.get("supply", "Supply")),
        ("gas", _labels.get("gas", "Fossil fuel")),
    ]:
        val = after[key]
        if val > 30:
            ym = y_cursor + val / 2
            ax.plot(
                [x[1] + w / 2 + 0.02, side_x - 0.03],
                [ym, ym],
                color=DECOMPOSED_BILL_LABEL_COLORS[key],
                linewidth=0.7,
                alpha=0.6,
            )
            ax.text(
                side_x,
                ym,
                label,
                color=DECOMPOSED_BILL_LABEL_COLORS[key],
                ha="left",
                va="center",
                fontsize=11,
                fontweight="bold",
            )
        y_cursor += val

    x_end = x[n_slots - 1] + w / 2
    ax.set_xticks(x[:2])
    ax.set_xticklabels(scenarios, fontsize=11)
    ax.set_ylabel("Annual energy bill ($)", fontsize=12)
    ax.set_ylim(0, max(totals) * 1.18)
    ax.set_xlim(-0.5, x_end + 0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_bounds(-0.5, x_end)
    fig.tight_layout()
    return fig


def _cost_breakdown_stack(
    ax: Axes,
    components: list[tuple[str, float]],
    *,
    min_label_share: float,
    width: float = 0.55,
) -> tuple[float, dict[str, float]]:
    """Draw one stacked bar and return its total and each segment's y-midpoint
    (data coordinates), for later side-label placement."""
    total = sum(value for _, value in components)
    bottom = 0.0
    mids: dict[str, float] = {}
    for component, value in components:
        ax.bar(0, value, width, bottom=bottom, color=COST_BREAKDOWN_COLORS[component], edgecolor="none", zorder=2)
        mids[component] = bottom + value / 2
        if value >= min_label_share * total and len(components) > 1:
            ax.text(
                0,
                bottom + value / 2,
                _fmt_cost_breakdown_value(component, value),
                ha="center",
                va="center",
                color=COST_BREAKDOWN_LABEL_COLORS[component],
                fontweight="bold",
                fontsize=12,
                zorder=3,
            )
        bottom += value
    ax.text(
        0,
        total * 1.02,
        _fmt_cost_breakdown_value(components[0][0], total),
        ha="center",
        va="bottom",
        color="#333333",
        fontweight="bold",
        fontsize=13,
    )
    return total, mids


def _fmt_cost_breakdown_value(component: str, value: float) -> str:
    return f"{value:,.0f} kWh" if component in _COST_BREAKDOWN_KWH_COMPONENTS else f"${value:,.0f}"


def plot_representative_cost_breakdown(
    data: dict[str, dict[str, float]],
    *,
    title: str,
    ng_label: str = "Natural Gas",
    hp_label: str = "Heat Pump",
    min_label_share: float = 0.03,
) -> Figure:
    """Render the representative-household cost-breakdown chart.

    Takes the dict from ``representative_cost_data()`` -- ``data["ng"]`` and
    ``data["hp"]``, each with ``kwh``, ``mc``, ``residual``,
    ``delivery_fixed``, ``delivery_volumetric``.

    Six bars in one row, grouped by metric: *ng_label*/*hp_label* for annual
    kWh, then for cost of service (marginal cost + residual), then for
    delivery bill (fixed + volumetric). Each pair shares a y-axis scale (so
    the *ng_label*-to-*hp_label* height is directly comparable). The kWh
    group is scaled independently, since kWh and dollar values are on wildly
    different scales (thousands vs. hundreds) -- sharing one axis across
    those would squash the dollar bars into illegible slivers. The cost-of-
    service and delivery-bill groups, both dollar-denominated, additionally
    share one scale *across* the two groups, so a given bar height means the
    same dollar amount in either group. This is drawn with raw matplotlib
    rather than plotnine: plotnine's faceting can only share a y-scale per
    full row (``facet_grid``) or per individual panel (``facet_wrap``), not
    per pair of panels.

    Within the *hp_label* bar, kWh, marginal cost, and delivery volumetric
    each split into an "existing" portion (held at the *ng_label* bar's
    value) and an "incremental" portion, always stacked last (on top)
    regardless of metric -- residual and the fixed charge get no incremental
    split, since they're flat, per-customer costs that don't move with load.

    Every segment at least *min_label_share* of its bar's total gets a
    value-and-unit annotation (skipped for single-component bars, whose value
    is already shown by the bar-total label above it), plus a component-name
    label connected by a thin line to the right of each group's *hp_label*
    bar (ported from ``plot_decomposed_bill_3bar``'s side labels).
    """
    ng, hp = data["ng"], data["hp"]
    # HP - NG for each load-driven component; can go negative in unusual cases
    # (e.g. a rate redesign that lowers the volumetric rate enough to offset
    # higher usage), in which case the "incremental" segment just renders as a
    # small negative stack rather than being silently dropped.
    incremental = {
        "kwh": hp["kwh"] - ng["kwh"],
        "mc": hp["mc"] - ng["mc"],
        "delivery_volumetric": hp["delivery_volumetric"] - ng["delivery_volumetric"],
    }

    groups: list[tuple[str, list[tuple[str, float]], list[tuple[str, float]]]] = [
        (
            "Annual\nkWh",
            [("kWh (existing)", ng["kwh"])],
            [("kWh (existing)", hp["kwh"] - incremental["kwh"]), ("kWh (incremental)", incremental["kwh"])],
        ),
        (
            "Cost of\nService",
            [("Residual", ng["residual"]), ("Marginal Cost (existing)", ng["mc"])],
            [
                ("Residual", hp["residual"]),
                ("Marginal Cost (existing)", hp["mc"] - incremental["mc"]),
                ("Marginal Cost (incremental)", incremental["mc"]),
            ],
        ),
        (
            "Delivery\nBill",
            [
                ("Delivery Fixed", ng["delivery_fixed"]),
                ("Delivery Volumetric (existing)", ng["delivery_volumetric"]),
            ],
            [
                ("Delivery Fixed", hp["delivery_fixed"]),
                (
                    "Delivery Volumetric (existing)",
                    hp["delivery_volumetric"] - incremental["delivery_volumetric"],
                ),
                ("Delivery Volumetric (incremental)", incremental["delivery_volumetric"]),
            ],
        ),
    ]

    # Bar axes in visual order, interleaved with two narrow spacer axes that
    # separate the three metric groups.
    fig, axes = pyplot.subplots(1, 8, figsize=(14, 6.5), gridspec_kw={"width_ratios": [1, 1, 0.35, 1, 1, 0.35, 1, 1]})
    bar_axes = [axes[0], axes[1], axes[3], axes[4], axes[6], axes[7]]
    for spacer_idx in (2, 5):
        axes[spacer_idx].axis("off")
        axes[spacer_idx].patch.set_alpha(0)

    fig.suptitle(title, x=0.02, y=0.98, ha="left", va="top", fontweight="bold", fontsize=14)
    fig.subplots_adjust(top=0.78)

    # Draw every group's bars first (without setting a y-scale yet), so the
    # cost-of-service and delivery-bill groups' totals are both known before
    # picking a shared ymax for them below.
    group_records: list[tuple[str, Axes, Axes, float, float, dict[str, float]]] = []
    for group_idx, (group_title, ng_components, hp_components) in enumerate(groups):
        ax_ng, ax_hp = bar_axes[2 * group_idx], bar_axes[2 * group_idx + 1]
        total_ng, _ = _cost_breakdown_stack(ax_ng, ng_components, min_label_share=min_label_share)
        total_hp, mids_hp = _cost_breakdown_stack(ax_hp, hp_components, min_label_share=min_label_share)
        group_records.append((group_title, ax_ng, ax_hp, total_ng, total_hp, mids_hp))

    # Cost of service (index 1) and delivery bill (index 2) are both
    # dollar-denominated, so they share one ymax across *both* groups -- not
    # just within each ng/hp pair -- so a bar's height means the same dollar
    # amount whether it's cost-of-service or delivery bill. The kWh group
    # (index 0) keeps its own independent scale, per the docstring above.
    dollar_ymax = max(total for *_, total_ng, total_hp, _ in group_records[1:] for total in (total_ng, total_hp)) * 1.2

    group_hp_axes: list[tuple[Axes, dict[str, float]]] = []
    for group_idx, (group_title, ax_ng, ax_hp, total_ng, total_hp, mids_hp) in enumerate(group_records):
        ymax = max(total_ng, total_hp) * 1.2 if group_idx == 0 else dollar_ymax
        for ax, scenario_label in ((ax_ng, ng_label), (ax_hp, hp_label)):
            ax.set_ylim(0, ymax)
            ax.set_xlim(-0.5, 0.5)
            ax.set_xticks([0])
            ax.set_xticklabels([scenario_label], fontsize=11)
            ax.set_yticks([])
            for spine in ("top", "right", "left"):
                ax.spines[spine].set_visible(False)
        # Group title, centered over the pair, placed from the pair's actual
        # post-layout figure position (subplots_adjust above already applied).
        fig.canvas.draw()
        pos_ng, pos_hp = ax_ng.get_position(), ax_hp.get_position()
        fig.text(
            (pos_ng.x0 + pos_hp.x1) / 2,
            pos_ng.y1 + 0.03,
            group_title,
            ha="center",
            va="bottom",
            fontsize=13,
            fontweight="bold",
        )
        group_hp_axes.append((ax_hp, mids_hp))

    # Component-name labels, connected by a thin line, to the right of each
    # group's hp_label bar. Drawn on a full-figure transparent overlay axes
    # (in figure-fraction coordinates converted from each bar's data
    # coordinates) rather than directly on the bar's own axes with
    # clip_on=False: overflow text drawn that way gets visually occluded by
    # whichever axes' patch is drawn next in z-order, once the text crosses
    # into that axes' screen region. The overlay, added and drawn last, has
    # nothing drawn after it to occlude it.
    overlay = fig.add_axes((0, 0, 1, 1))
    overlay.axis("off")
    overlay.patch.set_alpha(0)
    fig.canvas.draw()
    inv = fig.transFigure.inverted()
    for ax_hp, mids_hp in group_hp_axes:
        x_bar_edge, _ = inv.transform(ax_hp.transData.transform((0.275, 0)))
        for component, y_mid in mids_hp.items():
            label_color = COST_BREAKDOWN_LABEL_COLORS[component]
            line_color = COST_BREAKDOWN_COLORS[component] if label_color == "white" else label_color
            _, y_fig = inv.transform(ax_hp.transData.transform((0, y_mid)))
            x0, x1 = x_bar_edge + 0.006, x_bar_edge + 0.03
            overlay.plot(
                [x0, x1], [y_fig, y_fig], color=line_color, linewidth=0.7, alpha=0.6, transform=fig.transFigure
            )
            overlay.text(
                x1 + 0.004,
                y_fig,
                component.replace(" (", "\n("),
                color=line_color,
                ha="left",
                va="center",
                fontsize=11,
                fontweight="bold",
                transform=fig.transFigure,
            )

    return fig


# --- Tariff introspection --------------------------------------------------------


def load_tariff_json(state: str, utility: str, stem: str, ref: str) -> dict:
    """Fetch and parse a URDB tariff JSON from rate-design-platform's electric tariff config.

    *ref* has no default: every call site must pass the notebook's pinned
    ``RDP_REF`` (read from ``batch_config.yaml``) explicitly, so the tariff JSON
    always comes from the exact commit paired with the CAIRO batch, never a
    possibly-drifted ``main``.
    """
    from lib.rdp import fetch_rdp_file, parse_urdb_json

    del utility  # reserved for future multi-utility batches; path is state-scoped today
    path = f"rate_design/hp_rates/{state.lower()}/config/tariffs/electric/{stem}.json"
    content = fetch_rdp_file(path, ref=ref)
    return parse_urdb_json(content)["items"][0]


def extract_tariff_rates(tariff: dict) -> dict:
    """Extract fixed charge, per-period volumetric rates, and the month->period map from a URDB tariff.

    Works for flat (1-period), quarterly-ish (N-period, no seasonal grouping),
    and seasonal (N-period, grouped by month) tariffs alike — the caller decides
    how to use ``month_to_period`` based on how many distinct periods there are.

    Returns a dict with:

    - ``fixed_charge``: monthly fixed charge ($/month)
    - ``period_rates``: ``{period_index: rate}`` ($/kWh)
    - ``month_to_period``: ``{month_abbrev: period_index}`` (e.g. ``{"Jan": 1, ...}``),
      built from ``energyweekdayschedule`` (one row per month, Jan first)
    """
    fixed_charge = float(tariff.get("fixedchargefirstmeter", 0.0))
    period_rates = {i: float(tiers[0]["rate"]) for i, tiers in enumerate(tariff["energyratestructure"])}
    weekday_schedule = tariff.get("energyweekdayschedule", [])
    month_to_period = {MONTH_ORDER[i]: int(row[0]) for i, row in enumerate(weekday_schedule)}
    return {
        "fixed_charge": fixed_charge,
        "period_rates": period_rates,
        "month_to_period": month_to_period,
    }


def tariff_month_rate_table(rates_by_label: dict[str, dict]) -> pl.DataFrame:
    """Month-by-month volumetric delivery rate (¢/kWh), for one or more tariffs side by side.

    *rates_by_label* maps a display column label (e.g. ``"Default rate
    (¢/kWh)"``) to the corresponding ``extract_tariff_rates()`` output. Builds
    one rate column per label from its ``period_rates``/``month_to_period``,
    then joins all of them on ``month`` (ordered Jan-Dec via ``MONTH_ORDER``).
    Works for any number of tariffs, not just the historical pair/triple.
    """

    def _one_tariff_table(rates: dict, label: str) -> pl.DataFrame:
        return pl.DataFrame(
            {
                "month": MONTH_ORDER,
                label: [rates["period_rates"][rates["month_to_period"][m]] * 100 for m in MONTH_ORDER],
            }
        )

    tables = [_one_tariff_table(rates, label) for label, rates in rates_by_label.items()]
    result = tables[0]
    for table in tables[1:]:
        result = result.join(table, on="month")
    return result.with_columns(pl.col("month").cast(pl.Enum(MONTH_ORDER)))


# --- Representative-home bill decomposition ----------------------------------

# Month keys used in bge_monthly_rates_2025.yaml (Apr-Mar fiscal year).
_RATE_YAML_MONTH_TO_LABEL: dict[str, str] = {
    "2025-04": "Apr",
    "2025-05": "May",
    "2025-06": "Jun",
    "2025-07": "Jul",
    "2025-08": "Aug",
    "2025-09": "Sep",
    "2025-10": "Oct",
    "2025-11": "Nov",
    "2025-12": "Dec",
    "2026-01": "Jan",
    "2026-02": "Feb",
    "2026-03": "Mar",
}


def monthly_bill_from_profile(
    monthly_kwh: pl.DataFrame,
    rate_components: dict[str, dict[str, object]],
) -> pl.DataFrame:
    """Compute monthly bills by component from a kWh profile and rate schedule.

    Parameters
    ----------
    monthly_kwh
        12-row DataFrame with ``month_label`` (Jan-Dec) and ``kwh`` columns.
    rate_components
        Dict keyed by display component name (e.g. ``"Distribution"``).
        Each value is a dict with:

        - ``charge_unit``: ``"$/kWh"`` or ``"$/month"``
        - ``monthly_rates``: ``{YYYY-MM: float, ...}`` — 12 entries keyed by
          the rate-year month string (e.g. ``"2025-04"`` for April).

    Returns
    -------
    pl.DataFrame
        Long-form: ``month_label`` (Enum Jan-Dec), ``component`` (str),
        ``value`` (f64, dollars).
    """
    import polars as pl

    frames: list[pl.DataFrame] = []
    for component_name, spec in rate_components.items():
        unit = spec["charge_unit"]
        raw_rates: dict[str, float] = spec["monthly_rates"]  # type: ignore[assignment]
        label_rates = {_RATE_YAML_MONTH_TO_LABEL[k]: v for k, v in raw_rates.items()}

        if unit == "$/kWh":
            rows = [
                {
                    "month_label": m,
                    "component": component_name,
                    "value": float(monthly_kwh.filter(pl.col("month_label") == m)["kwh"][0]) * label_rates[m],
                }
                for m in MONTH_ORDER
            ]
        else:
            rows = [{"month_label": m, "component": component_name, "value": label_rates[m]} for m in MONTH_ORDER]
        frames.append(pl.DataFrame(rows))

    return pl.concat(frames).with_columns(pl.col("month_label").cast(pl.Enum(MONTH_ORDER)))


# --- Monthly load before/after chart -----------------------------------------

_MONTHLY_LOAD_BEFORE_COLOR = "#C8A200"
_MONTHLY_LOAD_PEAK_COLOR = "#C85436"
_MONTHLY_LOAD_X_EXPAND = (0.02, 0, 0.02, 0)
_MONTHLY_LOAD_PANEL_RIGHT = 0.82


def _finalize_monthly_load_fig(fig: Figure) -> Figure:
    """Reserve matching right margin on all monthly-load charts for alignment."""
    fig.subplots_adjust(right=_MONTHLY_LOAD_PANEL_RIGHT)
    return fig


def monthly_load_y_max(
    *,
    kwh: pl.Series | None = None,
    before_kwh: pl.Series | None = None,
    after_kwh: pl.Series | None = None,
) -> int:
    """Round peak monthly kWh up to the next 500 for aligned y-axes."""
    import math

    peak = 0.0
    for series in (kwh, before_kwh, after_kwh):
        if series is not None:
            peak = max(peak, cast(float, series.max()))
    return max(500, int(math.ceil(peak / 500) * 500))


def _add_monthly_load_side_callouts(fig: Figure, monthly: pl.DataFrame) -> None:
    """Add December segment callouts in the right margin without shrinking bars."""
    import polars as pl
    from matplotlib.transforms import blended_transform_factory

    from lib.plotnine import SB_COLORS

    ax = fig.axes[0]
    trans = blended_transform_factory(ax.transAxes, ax.transData)
    dec = monthly.filter(pl.col("month_label") == "Dec").row(0, named=True)
    dec_base = float(min(dec["before_kwh"], dec["after_kwh"]))
    dec_new = float(max(0.0, dec["after_kwh"] - dec["before_kwh"]))

    for y, label, color in (
        (dec_base / 2, "Electricity use\nbefore heat pump", _MONTHLY_LOAD_BEFORE_COLOR),
        (dec_base + dec_new / 2, "New electricity use\nfrom heat pump", SB_COLORS["saffron"]),
    ):
        ax.annotate(
            "",
            xy=(12, y),
            xytext=(1.0, y),
            xycoords=("data", "data"),
            textcoords=trans,
            arrowprops={"arrowstyle": "-", "color": color, "lw": 1.5, "shrinkA": 0, "shrinkB": 0},
            annotation_clip=False,
        )
        ax.text(
            1.02,
            y,
            label,
            transform=trans,
            ha="left",
            va="center",
            fontsize=13,
            color=color,
            fontweight="bold",
            clip_on=False,
        )


_SEGMENT_ORDER = [
    "New electricity use from heat pump",
    "More efficient cooling",
    "Electricity use before heat pump",
]
_SEGMENT_COLORS: dict[str, str | tuple[float, ...]] = {
    "Electricity use before heat pump": _MONTHLY_LOAD_BEFORE_COLOR,
    "More efficient cooling": (0.784, 0.635, 0.0, 0.35),
    "New electricity use from heat pump": "#FFC729",
}
_SAVINGS_LABEL_COLOR = "#D4BA46"


def plot_monthly_load(
    monthly: pl.DataFrame,
    *,
    title: str = "",
    figure_size: tuple[float, float] = (14, 5),
    y_max: int | None = None,
) -> Figure:
    """Single-series monthly kWh bar chart (pre-heat-pump electricity use)."""
    import polars as pl
    from plotnine import (
        aes,
        geom_col,
        ggplot,
        labs,
        scale_x_discrete,
        scale_y_continuous,
        theme,
    )

    from lib.plotnine import theme_switchbox

    chart_data = monthly.with_columns(pl.col("month_label").cast(pl.Enum(MONTH_ORDER)))
    ymax = y_max if y_max is not None else monthly_load_y_max(kwh=monthly["kwh"])

    p = (
        ggplot(chart_data, aes(x="month_label", y="kwh"))
        + geom_col(width=0.7, fill=_MONTHLY_LOAD_BEFORE_COLOR)
        + scale_y_continuous(limits=(0, ymax), expand=(0, 0))
        + scale_x_discrete(expand=_MONTHLY_LOAD_X_EXPAND)
        + labs(title=title, x="", y="Electricity consumption (kWh)")
        + theme_switchbox()
        + theme(figure_size=figure_size, legend_position="none")
    )

    return _finalize_monthly_load_fig(p.draw())


def plot_monthly_load_with_peak(
    monthly: pl.DataFrame,
    *,
    title: str = "",
    figure_size: tuple[float, float] = (14, 5),
    y_max: int | None = None,
) -> Figure:
    """Monthly kWh bar chart with peak-hour wedges highlighted.

    Like :func:`plot_monthly_load` but splits each bar into off-peak (gold)
    and peak-hour (terracotta) segments so the reader can see which months
    have electricity consumption during the grid's peak hours.

    Parameters
    ----------
    monthly
        12-row DataFrame with ``month_label``, ``kwh_offpeak``, ``kwh_peak``
        (from :func:`sum_monthly_peak_offpeak_kwh`).
    title
        Optional chart title.
    figure_size
        plotnine figure size in inches.
    y_max
        Y-axis upper limit in kWh.  Defaults to the next 500 above the peak
        total monthly kWh.

    Returns
    -------
    Figure
        matplotlib Figure; wrap in ``display_figure`` to embed.
    """
    import polars as pl
    from matplotlib.transforms import blended_transform_factory
    from plotnine import (
        aes,
        geom_col,
        ggplot,
        labs,
        scale_fill_manual,
        scale_x_discrete,
        scale_y_continuous,
        theme,
    )

    from lib.plotnine import theme_switchbox

    _PEAK_SEGMENT_ORDER = ["Peak-hour usage", "Off-peak usage"]
    _PEAK_SEGMENT_COLORS = {
        "Off-peak usage": _MONTHLY_LOAD_BEFORE_COLOR,
        "Peak-hour usage": _MONTHLY_LOAD_PEAK_COLOR,
    }

    total_kwh = monthly["kwh_offpeak"] + monthly["kwh_peak"]
    ymax = y_max if y_max is not None else monthly_load_y_max(kwh=total_kwh)

    chart_data = pl.concat(
        [
            monthly.select(
                "month_label",
                pl.col("kwh_offpeak").alias("kwh"),
            ).with_columns(pl.lit("Off-peak usage").alias("segment")),
            monthly.select(
                "month_label",
                pl.col("kwh_peak").alias("kwh"),
            ).with_columns(pl.lit("Peak-hour usage").alias("segment")),
        ]
    ).with_columns(
        pl.col("month_label").cast(pl.Enum(MONTH_ORDER)),
        pl.col("segment").cast(pl.Enum(_PEAK_SEGMENT_ORDER)),
    )

    p = (
        ggplot(chart_data, aes(x="month_label", y="kwh", fill="segment"))
        + geom_col(width=0.7)
        + scale_fill_manual(values=_PEAK_SEGMENT_COLORS)
        + scale_y_continuous(limits=(0, ymax), expand=(0, 0))
        + scale_x_discrete(expand=_MONTHLY_LOAD_X_EXPAND)
        + labs(title=title, x="", y="Electricity consumption (kWh)")
        + theme_switchbox()
        + theme(figure_size=figure_size, legend_position="none")
    )

    fig = _finalize_monthly_load_fig(p.draw())

    # --- Direct annotations instead of a legend ---
    ax = fig.axes[0]
    trans = blended_transform_factory(ax.transAxes, ax.transData)

    # Side callout for the gold base segment — anchor to December (rightmost
    # bar, always pure off-peak) so the line draws cleanly into the margin.
    dec_offpeak = float(monthly.filter(pl.col("month_label") == "Dec")["kwh_offpeak"][0])
    callout_y = dec_offpeak / 2
    ax.annotate(
        "",
        xy=(12, callout_y),
        xytext=(1.0, callout_y),
        xycoords=("data", "data"),
        textcoords=trans,
        arrowprops={
            "arrowstyle": "-",
            "color": _MONTHLY_LOAD_BEFORE_COLOR,
            "lw": 1.5,
            "shrinkA": 0,
            "shrinkB": 0,
        },
        annotation_clip=False,
    )
    ax.text(
        1.02,
        callout_y,
        "Electricity use",
        transform=trans,
        ha="left",
        va="center",
        fontsize=13,
        color=_MONTHLY_LOAD_BEFORE_COLOR,
        fontweight="bold",
        clip_on=False,
    )

    # In-chart annotation above the tallest peak wedge
    _peak_idx = monthly["kwh_peak"].arg_max()
    assert _peak_idx is not None, "kwh_peak column is empty"
    peak_month_idx = int(_peak_idx)
    peak_month_label = monthly["month_label"][peak_month_idx]
    peak_bar_x = MONTH_ORDER.index(peak_month_label) + 1
    peak_bar_top = float(monthly["kwh_offpeak"][peak_month_idx] + monthly["kwh_peak"][peak_month_idx])

    ax.text(
        peak_bar_x,
        peak_bar_top + 25,
        "Usage during\npeak hours",
        ha="center",
        va="bottom",
        fontsize=13,
        color=_MONTHLY_LOAD_PEAK_COLOR,
        fontweight="bold",
        transform=ax.transData,
    )

    return fig


def plot_monthly_load_before_after(
    monthly: pl.DataFrame,
    *,
    title: str = "",
    figure_size: tuple[float, float] = (14, 5),
    y_max: int | None = None,
    peak_before: pl.DataFrame | None = None,
    peak_after: pl.DataFrame | None = None,
) -> Figure:
    """Three-segment monthly bar chart: base + savings + new load from heat pump.

    When *peak_before* and *peak_after* are supplied, peak-hour kWh wedges are
    added at the top of the base and new-HP segments (never in the savings
    segment), with delta labels showing increase/decrease in peak-hour usage.

    Parameters
    ----------
    monthly
        DataFrame with columns ``month_label``, ``before_kwh``, ``after_kwh``.
        Works for a single building (12 rows) or a population average.
    title
        Optional chart title.
    figure_size
        plotnine figure size in inches.
    y_max
        Y-axis upper limit in kWh. Defaults to the next 500 above the peak
        before or after monthly kWh.
    peak_before
        12-row DataFrame with ``month_label``, ``kwh_offpeak``, ``kwh_peak``
        from :func:`sum_monthly_peak_offpeak_kwh` for the pre-HP profile.
        Must be provided together with *peak_after* or both ``None``.
    peak_after
        Same as *peak_before* but for the post-HP profile.

    Returns
    -------
    Figure
        matplotlib Figure; wrap in ``display_figure`` to embed.
    """
    import polars as pl
    from plotnine import (
        aes,
        annotate,
        geom_col,
        ggplot,
        labs,
        scale_fill_manual,
        scale_x_discrete,
        scale_y_continuous,
        theme,
    )

    from lib.plotnine import theme_switchbox

    show_peak = peak_before is not None and peak_after is not None
    if (peak_before is None) != (peak_after is None):
        raise ValueError("peak_before and peak_after must both be provided or both None")

    if not show_peak:
        # --- Original 3-segment path (no peak data) ---
        segment_order = _SEGMENT_ORDER
        segment_colors = _SEGMENT_COLORS

        chart_data = pl.concat(
            [
                monthly.select(
                    "month_label",
                    pl.min_horizontal("before_kwh", "after_kwh").alias("kwh"),
                ).with_columns(pl.lit("Electricity use before heat pump").alias("segment")),
                monthly.select(
                    "month_label",
                    (pl.col("before_kwh") - pl.col("after_kwh")).clip(lower_bound=0).alias("kwh"),
                ).with_columns(pl.lit("More efficient cooling").alias("segment")),
                monthly.select(
                    "month_label",
                    (pl.col("after_kwh") - pl.col("before_kwh")).clip(lower_bound=0).alias("kwh"),
                ).with_columns(pl.lit("New electricity use from heat pump").alias("segment")),
            ]
        ).with_columns(
            pl.col("month_label").cast(pl.Enum(MONTH_ORDER)),
            pl.col("segment").cast(pl.Enum(segment_order)),
        )
    else:
        # --- 5-segment path with peak wedges ---
        assert peak_before is not None
        assert peak_after is not None
        # Join peak data with monthly for per-month computation
        _m = monthly.join(
            peak_before.select("month_label", pl.col("kwh_peak").alias("before_peak")),
            on="month_label",
        ).join(
            peak_after.select("month_label", pl.col("kwh_peak").alias("after_peak")),
            on="month_label",
        )

        # Per-month segment computation — ONE red wedge per bar.
        # The red wedge shows after_peak (peak-hour kWh in the post-HP
        # profile), carved from whichever segment is on top:
        #   - Winter (after > before): red at top of new-HP saffron
        #   - Summer (before >= after): red at top of base gold
        _m = _m.with_columns(
            pl.min_horizontal("before_kwh", "after_kwh").alias("base_kwh"),
            (pl.col("before_kwh") - pl.col("after_kwh")).clip(lower_bound=0).alias("savings_kwh"),
            (pl.col("after_kwh") - pl.col("before_kwh")).clip(lower_bound=0).alias("new_hp_kwh"),
        ).with_columns(
            # Savings months: peak carved from base; clamp to base size
            pl.when(pl.col("new_hp_kwh") > 0)
            .then(0)
            .otherwise(pl.min_horizontal("after_peak", "base_kwh"))
            .alias("peak_in_base"),
            # New-HP months: peak carved from new-HP; clamp to segment size
            pl.when(pl.col("new_hp_kwh") > 0)
            .then(pl.min_horizontal("after_peak", "new_hp_kwh"))
            .otherwise(0)
            .alias("peak_in_new"),
        )

        segment_order = [
            "New HP peak",
            "New HP off-peak",
            "More efficient cooling",
            "Base peak",
            "Base off-peak",
        ]
        segment_colors: dict[str, str | tuple[float, ...]] = {
            "Base off-peak": _MONTHLY_LOAD_BEFORE_COLOR,
            "Base peak": _MONTHLY_LOAD_PEAK_COLOR,
            "More efficient cooling": (0.784, 0.635, 0.0, 0.35),
            "New HP off-peak": "#FFC729",
            "New HP peak": _MONTHLY_LOAD_PEAK_COLOR,
        }

        chart_data = pl.concat(
            [
                _m.select("month_label", (pl.col("base_kwh") - pl.col("peak_in_base")).alias("kwh")).with_columns(
                    pl.lit("Base off-peak").alias("segment")
                ),
                _m.select("month_label", pl.col("peak_in_base").alias("kwh")).with_columns(
                    pl.lit("Base peak").alias("segment")
                ),
                _m.select("month_label", pl.col("savings_kwh").alias("kwh")).with_columns(
                    pl.lit("More efficient cooling").alias("segment")
                ),
                _m.select("month_label", (pl.col("new_hp_kwh") - pl.col("peak_in_new")).alias("kwh")).with_columns(
                    pl.lit("New HP off-peak").alias("segment")
                ),
                _m.select("month_label", pl.col("peak_in_new").alias("kwh")).with_columns(
                    pl.lit("New HP peak").alias("segment")
                ),
            ]
        ).with_columns(
            pl.col("month_label").cast(pl.Enum(MONTH_ORDER)),
            pl.col("segment").cast(pl.Enum(segment_order)),
        )

    ymax = (
        y_max
        if y_max is not None
        else monthly_load_y_max(
            before_kwh=monthly["before_kwh"],
            after_kwh=monthly["after_kwh"],
        )
    )

    savings_by_month = monthly.with_columns((pl.col("before_kwh") - pl.col("after_kwh")).alias("savings"))
    max_savings_month = savings_by_month.sort("savings", descending=True).row(0, named=True)
    # Only label the savings segment when summer kWh drops by at least 5%
    _summer_before = float(
        monthly.filter(pl.col("month_label").is_in(["Jun", "Jul", "Aug", "Sep"]))["before_kwh"].sum()
    )
    _summer_after = float(monthly.filter(pl.col("month_label").is_in(["Jun", "Jul", "Aug", "Sep"]))["after_kwh"].sum())
    _summer_pct_decrease = (_summer_before - _summer_after) / _summer_before if _summer_before > 0 else 0.0
    has_savings = max_savings_month["savings"] > 0 and _summer_pct_decrease >= 0.05

    p = (
        ggplot(chart_data, aes(x="month_label", y="kwh", fill="segment"))
        + geom_col(width=0.7)
        + scale_fill_manual(values=segment_colors)
        + scale_y_continuous(limits=(0, ymax), expand=(0, 0))
        + scale_x_discrete(expand=_MONTHLY_LOAD_X_EXPAND)
        + labs(title=title, x="", y="Electricity consumption (kWh)")
        + theme_switchbox()
        + theme(figure_size=figure_size, legend_position="none")
    )

    if has_savings:
        sav_label = max_savings_month["month_label"]
        sav_idx = MONTH_ORDER.index(sav_label) + 1
        sav_base = float(min(max_savings_month["before_kwh"], max_savings_month["after_kwh"]))
        sav_amount = float(max_savings_month["savings"])
        p = p + annotate(
            "text",
            x=sav_idx,
            y=sav_base + sav_amount + 30,
            label="More efficient cooling\nlowers use",
            ha="center",
            va="bottom",
            size=13,
            color=_SAVINGS_LABEL_COLOR,
            fontweight="bold",
        )

    fig = _finalize_monthly_load_fig(p.draw())
    _add_monthly_load_side_callouts(fig, monthly)

    # --- Peak-hour delta annotations ---
    if show_peak:
        assert peak_before is not None
        assert peak_after is not None
        ax = fig.axes[0]
        delta_peak = (
            peak_after.select("month_label", pl.col("kwh_peak").alias("after_peak"))
            .join(
                peak_before.select("month_label", pl.col("kwh_peak").alias("before_peak")),
                on="month_label",
            )
            .with_columns((pl.col("after_peak") - pl.col("before_peak")).alias("delta"))
        )

        # Label on the month with the largest peak-hour increase
        max_increase = delta_peak.sort("delta", descending=True).row(0, named=True)
        if max_increase["delta"] > 0:
            inc_label = max_increase["month_label"]
            inc_x = MONTH_ORDER.index(inc_label) + 1
            inc_bar_top = float(monthly.filter(pl.col("month_label") == inc_label)["after_kwh"][0])
            ax.text(
                inc_x,
                inc_bar_top + 25,
                "Peak-hour usage\nincrease \u2191",
                ha="center",
                va="bottom",
                fontsize=13,
                color=_MONTHLY_LOAD_PEAK_COLOR,
                fontweight="bold",
                transform=ax.transData,
            )

        # Label on the month with the largest peak-hour decrease — placed
        # below the base-peak wedge (inside the bar) to avoid colliding with
        # the "More efficient cooling" label that sits above the bar top.
        max_decrease = delta_peak.sort("delta").row(0, named=True)
        if max_decrease["delta"] < 0:
            dec_label = max_decrease["month_label"]
            dec_x = MONTH_ORDER.index(dec_label) + 1
            dec_row = _m.filter(pl.col("month_label") == dec_label)
            base_offpeak = float(dec_row["base_kwh"][0] - dec_row["peak_in_base"][0])
            base_peak = float(dec_row["peak_in_base"][0])
            dec_y = base_offpeak + base_peak / 2
            ax.annotate(
                "Peak-hour\nusage\ndecrease \u2193",
                xy=(dec_x, dec_y),
                xytext=(dec_x + 1.8, dec_y),
                ha="left",
                va="center",
                fontsize=13,
                color=_MONTHLY_LOAD_PEAK_COLOR,
                fontweight="bold",
                arrowprops={
                    "arrowstyle": "-",
                    "color": _MONTHLY_LOAD_PEAK_COLOR,
                    "lw": 1.5,
                    "shrinkA": 0,
                    "shrinkB": 2,
                },
            )

    return fig


# --- Annual bill component stacked chart ------------------------------------

_BILL_COMPONENT_ORDER = [
    "Customer Charge",
    "Distribution",
    "Transmission",
    "EmPOWER Maryland",
    "Generation",
]

_BILL_SEGMENT_ORDER = [
    "Increment",
    "Before",
]

_BILL_COLORS: dict[str, str] = {
    "Customer Charge|Before": "#023047",
    "Customer Charge|Increment": "#023047",
    "Distribution|Before": "#023047",
    "Distribution|Increment": "#5b90a8",
    "Transmission|Before": "#023047",
    "Transmission|Increment": "#5b90a8",
    "EmPOWER Maryland|Before": "#023047",
    "EmPOWER Maryland|Increment": "#5b90a8",
    "Generation|Before": "#fc9706",
    "Generation|Increment": "#ffc729",
}


def _annual_bill_component_stack_data(
    before_bills: pl.DataFrame,
    after_bills: pl.DataFrame,
) -> pl.DataFrame:
    """Reshape annual bill totals into before + increment segments for stacking."""
    import polars as pl

    before_annual = before_bills.group_by("component").agg(pl.col("value").sum().alias("before"))
    after_annual = after_bills.group_by("component").agg(pl.col("value").sum().alias("after"))
    joined = before_annual.join(after_annual, on="component", how="inner").with_columns(
        (pl.col("after") - pl.col("before")).alias("increment"),
    )

    negative = joined.filter(pl.col("increment") < 0)
    if not negative.is_empty():
        details = ", ".join(
            f"{row['component']} (before={row['before']:.2f}, after={row['after']:.2f})"
            for row in negative.iter_rows(named=True)
        )
        msg = f"Annual bill component increments must be non-negative; got negative values for: {details}"
        raise ValueError(msg)

    long = joined.select(
        pl.col("component"),
        pl.lit("Before").alias("segment"),
        pl.col("before").alias("value"),
    ).vstack(
        joined.select(
            pl.col("component"),
            pl.lit("Increment").alias("segment"),
            pl.col("increment").alias("value"),
        )
    )

    return long.with_columns(
        (pl.col("component") + "|" + pl.col("segment")).alias("fill_key"),
        pl.col("component").cast(pl.Enum(_BILL_COMPONENT_ORDER)),
        pl.col("segment").cast(pl.Enum(_BILL_SEGMENT_ORDER)),
    )


_BILL_SINGLE_COLORS: dict[str, str] = {
    "Customer Charge": "#023047",
    "Distribution": "#023047",
    "Transmission": "#023047",
    "EmPOWER Maryland": "#023047",
    "Generation": "#fc9706",
}


def plot_annual_bill_component_single(
    bills: pl.DataFrame,
    *,
    title: str = "",
    figure_size: tuple[float, float] = (10.5, 5),
    y_max: float | None = None,
) -> Figure:
    """Single-bar chart of annual bills by component (one period only).

    Shows one bar per component with a dollar label centered inside. Uses
    midnight for delivery components and carrot for Generation, matching the
    "Before" color scheme of the stacked chart.

    Parameters
    ----------
    bills
        Long-form monthly bills from ``monthly_bill_from_profile()``.
    title
        Optional chart title.
    figure_size
        plotnine figure size in inches.
    y_max
        Optional y-axis upper limit. Defaults to auto with 8 % headroom.

    Returns
    -------
    Figure
        matplotlib Figure; wrap in ``display_figure`` to embed.
    """
    import polars as pl
    from plotnine import (
        aes,
        geom_col,
        geom_text,
        ggplot,
        labs,
        position_stack,
        scale_fill_manual,
        scale_x_discrete,
        scale_y_continuous,
        theme,
    )

    from lib.plotnine import theme_switchbox

    annual = (
        bills.group_by("component")
        .agg(pl.col("value").sum().alias("value"))
        .with_columns(
            pl.col("component").cast(pl.Enum(_BILL_COMPONENT_ORDER)),
            pl.when(pl.col("value").abs() >= 1.0)
            .then(pl.col("value").round(0).cast(pl.Int64).cast(pl.Utf8).str.replace(r"^(-?\d+)$", "$$$1"))
            .otherwise(pl.lit(""))
            .alias("label"),
        )
    )

    y_upper = y_max if y_max is not None else cast(float, annual["value"].max()) * 1.08

    p = (
        ggplot(annual, aes(x="component", y="value", fill="component"))
        + geom_col(width=0.6)
        + geom_text(
            aes(label="label"),
            position=position_stack(vjust=0.5),
            size=9,
            color="white",
            fontweight="bold",
        )
        + scale_fill_manual(values=_BILL_SINGLE_COLORS)
        + scale_x_discrete(limits=_BILL_COMPONENT_ORDER)
        + scale_y_continuous(
            labels=lambda xs: [f"${x:,.0f}" for x in xs],
            limits=(0, y_upper),
            expand=(0, 0, 0.08, 0),
        )
        + labs(title=title, x="", y="Annual bill")
        + theme_switchbox()
        + theme(figure_size=figure_size, legend_position="none")
    )

    return p.draw()


def plot_annual_bill_component_stacked(
    before_bills: pl.DataFrame,
    after_bills: pl.DataFrame,
    *,
    title: str = "",
    figure_size: tuple[float, float] = (10.5, 5),
) -> Figure:
    """Stacked bar chart of annual bills by component, before vs after HP.

    Each bar stacks the pre-HP bill component (bottom) and the incremental
    amount added after heat pump installation (top). Bar height equals the
    post-HP component total.

    Parameters
    ----------
    before_bills
        Long-form monthly bills from ``monthly_bill_from_profile()``
        (upgrade 0).
    after_bills
        Long-form monthly bills from ``monthly_bill_from_profile()``
        (upgrade 2).
    title
        Optional chart title.
    figure_size
        plotnine figure size in inches.

    Returns
    -------
    Figure
        matplotlib Figure rendered via ``display_figure``.

    Raises
    ------
    ValueError
        If any component's after-minus-before increment is negative.
    """
    import polars as pl
    from plotnine import (
        aes,
        geom_col,
        geom_text,
        ggplot,
        labs,
        position_stack,
        scale_fill_manual,
        scale_x_discrete,
        scale_y_continuous,
        theme,
    )

    from lib.plotnine import theme_switchbox
    from lib.quarto import display_figure

    chart_data = _annual_bill_component_stack_data(before_bills, after_bills).with_columns(
        pl.when(pl.col("value").abs() >= 1.0)
        .then(pl.col("value").round(0).cast(pl.Int64).cast(pl.Utf8).str.replace(r"^(-?\d+)$", "$$$1"))
        .otherwise(pl.lit(""))
        .alias("label"),
    )

    bar_totals = (
        chart_data.group_by("component")
        .agg(pl.col("value").sum().alias("total"))
        .with_columns(
            pl.format("${}", pl.col("total").round(0).cast(pl.Int64)).alias("total_label"),
        )
    )

    p = (
        ggplot(chart_data, aes(x="component", y="value", fill="fill_key"))
        + geom_col(width=0.6, position=position_stack(reverse=True))
        + geom_text(
            aes(label="label"),
            position=position_stack(vjust=0.5, reverse=True),
            size=9,
            color="white",
            fontweight="bold",
        )
        + geom_text(
            bar_totals,
            aes(x="component", y="total", label="total_label"),
            va="bottom",
            size=10,
            color="#333333",
            fontweight="bold",
            nudge_y=5,
            inherit_aes=False,
        )
        + scale_fill_manual(values=_BILL_COLORS)
        + scale_x_discrete(limits=_BILL_COMPONENT_ORDER)
        + scale_y_continuous(
            labels=lambda xs: [f"${x:,.0f}" for x in xs],
            expand=(0, 0, 0.10, 0),
        )
        + labs(title=title, x="", y="Annual bill")
        + theme_switchbox()
        + theme(figure_size=figure_size, legend_position="none")
    )

    fig = p.draw()
    display_figure(fig)
    return fig


# --- Delivery marginal cost charts ------------------------------------------

_MC_COMPONENT_ORDER = ["Transmission", "Distribution"]
_MC_COLORS = {
    "Distribution": "#A0AF12",
    "Transmission": "#546800",
}
_ALL_MONTH_ABBRS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _season_labels(summer_months: set[str]) -> tuple[str, str]:
    """Derive ``("May-Sep", "Oct-Apr")``-style labels from a set of summer month abbreviations."""
    ordered = [m for m in _ALL_MONTH_ABBRS if m in summer_months]
    winter = [m for m in _ALL_MONTH_ABBRS if m not in summer_months]
    summer_label = f"{ordered[0]}-{ordered[-1]}"
    winter_label = f"{winter[0]}-{winter[-1]}"
    return summer_label, winter_label


def plot_monthly_delivery_mc(
    monthly_mc: pl.DataFrame,
    *,
    title: str = "",
    figure_size: tuple[float, float] = (14, 5),
) -> Figure:
    """Stacked bar chart of monthly delivery marginal costs (transmission + distribution).

    Parameters
    ----------
    monthly_mc
        12-row DataFrame with ``month_label`` (Enum Jan-Dec),
        ``mc_tx_dollars``, and ``mc_dist_dollars``.
    title
        Chart title.
    figure_size
        plotnine figure size in inches.

    Returns
    -------
    Figure
        matplotlib Figure; wrap in ``display_figure`` to embed.
    """
    import polars as pl
    from plotnine import (
        aes,
        geom_col,
        ggplot,
        labs,
        scale_fill_manual,
        scale_x_discrete,
        scale_y_continuous,
        theme,
    )

    from lib.plotnine import theme_switchbox

    chart_data = pl.concat(
        [
            monthly_mc.select("month_label", pl.col("mc_tx_dollars").alias("dollars")).with_columns(
                pl.lit("Transmission").alias("component")
            ),
            monthly_mc.select("month_label", pl.col("mc_dist_dollars").alias("dollars")).with_columns(
                pl.lit("Distribution").alias("component")
            ),
        ]
    ).with_columns(
        pl.col("month_label").cast(pl.Enum(MONTH_ORDER)),
        pl.col("component").cast(pl.Enum(_MC_COMPONENT_ORDER)),
    )

    p = (
        ggplot(chart_data, aes(x="month_label", y="dollars", fill="component"))
        + geom_col(width=0.7)
        + scale_fill_manual(values=_MC_COLORS)
        + scale_x_discrete(expand=(0.02, 0, 0.02, 0))
        + scale_y_continuous(
            labels=lambda xs: [f"${x:,.2f}" for x in xs],
            expand=(0, 0, 0.05, 0),
        )
        + labs(title=title, x="", y="Delivery marginal cost ($)", fill="")
        + theme_switchbox()
        + theme(figure_size=figure_size)
    )

    return p.draw()


def _aggregate_seasonal_mc(
    monthly_mc: pl.DataFrame,
    *,
    summer_months: set[str],
) -> dict[str, dict[str, float]]:
    """Aggregate 12-row monthly MC into summer and winter totals.

    *summer_months* is a set of 3-letter month abbreviations (e.g.
    ``{"May", "Jun", "Jul", "Aug", "Sep"}``).  The returned dict is keyed by
    the derived season labels (e.g. ``{"May-Sep": {...}, "Oct-Apr": {...}}``).
    """
    summer_label, winter_label = _season_labels(summer_months)
    seasonal = (
        monthly_mc.with_columns(
            pl.when(pl.col("month_label").cast(pl.String).is_in(summer_months))
            .then(pl.lit(summer_label))
            .otherwise(pl.lit(winter_label))
            .alias("season")
        )
        .group_by("season")
        .agg(
            pl.col("mc_tx_dollars").sum(),
            pl.col("mc_dist_dollars").sum(),
        )
    )
    result: dict[str, dict[str, float]] = {}
    for row in seasonal.iter_rows(named=True):
        result[row["season"]] = {
            "tx": row["mc_tx_dollars"],
            "dist": row["mc_dist_dollars"],
        }
    return result


def _fmt_mc_dollar(v: float) -> str:
    """Format a marginal-cost dollar value (smaller than bill amounts)."""
    return f"${v:,.2f}"


def _draw_seasonal_mc_bar(
    ax: Axes,
    x: float,
    tx: float,
    dist: float,
    width: float,
    *,
    min_label_height: float = 1.5,
) -> float:
    """Draw one stacked bar: Distribution (sky) bottom, Transmission (midnight) top.

    In-bar labels are shown only when a segment is tall enough to read.
    A total label is placed above the bar.

    Returns the total height (dist + tx).
    """
    ax.bar(x, dist, width, bottom=0, color=_MC_COLORS["Distribution"], edgecolor="none")
    ax.bar(x, tx, width, bottom=dist, color=_MC_COLORS["Transmission"], edgecolor="none")

    total = dist + tx

    if dist >= min_label_height:
        ax.text(
            x,
            dist / 2,
            _fmt_mc_dollar(dist),
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=11,
            zorder=11,
        )
    if tx >= min_label_height:
        ax.text(
            x,
            dist + tx / 2,
            _fmt_mc_dollar(tx),
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=11,
            zorder=11,
        )

    ax.text(
        x,
        total * 1.01,
        _fmt_mc_dollar(total),
        ha="center",
        va="bottom",
        color="#333333",
        fontweight="bold",
        fontsize=12,
    )

    return total


def _add_mc_side_callouts(fig: Figure, ax: Axes, dist: float, tx: float, *, bar_x: float, bar_w: float) -> None:
    """Add 'Distribution' and 'Transmission' side callouts touching the rightmost bar."""
    bar_right = bar_x + bar_w / 2
    label_x = bar_right + 0.12
    callouts = [
        (dist / 2, "Distribution", _MC_COLORS["Distribution"]),
        (dist + tx / 2, "Transmission", _MC_COLORS["Transmission"]),
    ]
    for y, label, color in callouts:
        ax.plot(
            [bar_right + 0.02, label_x - 0.02],
            [y, y],
            color=color,
            linewidth=1.5,
            clip_on=False,
        )
        ax.text(
            label_x,
            y,
            label,
            ha="left",
            va="center",
            fontsize=13,
            color=color,
            fontweight="bold",
            clip_on=False,
        )


def plot_seasonal_delivery_mc(
    monthly_mc: pl.DataFrame,
    *,
    summer_months: set[str],
    title: str = "",
    figure_size: tuple[float, float] = (10.5, 5),
) -> Figure:
    """Two-bar seasonal delivery MC chart (one bar per season).

    Aggregates monthly transmission and distribution costs into summer and
    winter buckets, then draws a stacked bar for each with in-bar component
    labels and an above-bar total.

    Parameters
    ----------
    monthly_mc
        12-row DataFrame with ``month_label`` (Enum Jan-Dec),
        ``mc_tx_dollars``, and ``mc_dist_dollars``.
    summer_months
        Set of 3-letter month abbreviations defining the summer season
        (e.g. ``{"May", "Jun", "Jul", "Aug", "Sep"}``).
    title
        Chart title.
    figure_size
        matplotlib figure size in inches.

    Returns
    -------
    Figure
        matplotlib Figure; wrap in ``display_figure`` to embed.
    """
    agg = _aggregate_seasonal_mc(monthly_mc, summer_months=summer_months)
    season_order = list(reversed(_season_labels(summer_months)))

    fig, ax = pyplot.subplots(figsize=figure_size)
    ax.set_title(title, fontfamily="GT Planar", fontweight="bold", fontsize=15, loc="left", pad=12)

    w = 0.5
    positions = [0, 0.8]

    max_total = 0.0
    for i, season in enumerate(season_order):
        total = _draw_seasonal_mc_bar(ax, positions[i], agg[season]["tx"], agg[season]["dist"], w)
        max_total = max(max_total, total)

    ax.set_xticks(positions)
    ax.set_xticklabels(season_order, fontsize=11, fontfamily="IBM Plex Sans")
    ax.set_ylabel("Delivery marginal cost ($)", fontsize=12, fontfamily="IBM Plex Sans")
    ax.set_ylim(0, max_total * 1.15)
    ax.set_xlim(positions[0] - 0.5, positions[-1] + 1.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_formatter(lambda x, _: f"${x:,.2f}")
    fig.tight_layout()

    # Side callouts on the tallest bar
    tallest_idx = 0 if sum(agg[season_order[0]].values()) >= sum(agg[season_order[1]].values()) else 1
    tallest_season = season_order[tallest_idx]
    _add_mc_side_callouts(
        fig, ax, agg[tallest_season]["dist"], agg[tallest_season]["tx"], bar_x=positions[tallest_idx], bar_w=w
    )

    return fig


def plot_seasonal_delivery_mc_comparison(
    monthly_before: pl.DataFrame,
    monthly_after: pl.DataFrame,
    *,
    summer_months: set[str],
    title: str = "",
    figure_size: tuple[float, float] = (10.5, 6),
) -> Figure:
    """Four-bar seasonal delivery MC chart comparing before and after heat pump.

    Groups bars into two pairs (summer and winter), each with a before and
    after bar.  A hatched rectangle and delta annotation between each pair
    shows the seasonal change, and a bracket across the top shows the net
    annual change.

    Parameters
    ----------
    monthly_before
        12-row monthly MC DataFrame for the pre-HP period.
    monthly_after
        12-row monthly MC DataFrame for the post-HP period.
    summer_months
        Set of 3-letter month abbreviations defining the summer season
        (e.g. ``{"May", "Jun", "Jul", "Aug", "Sep"}``).
    title
        Chart title.
    figure_size
        matplotlib figure size in inches.

    Returns
    -------
    Figure
        matplotlib Figure; wrap in ``display_figure`` to embed.
    """
    from lib.plotnine import SB_COLORS

    agg_before = _aggregate_seasonal_mc(monthly_before, summer_months=summer_months)
    agg_after = _aggregate_seasonal_mc(monthly_after, summer_months=summer_months)
    season_order = list(reversed(_season_labels(summer_months)))

    fig, ax = pyplot.subplots(figsize=figure_size)
    ax.set_title(title, fontfamily="GT Planar", fontweight="bold", fontsize=15, loc="left", pad=12)

    w = 0.45
    gap_within = 0.55
    gap_between = 1.1

    x = np.array([0, gap_within, gap_between, gap_between + gap_within])

    pairs = [
        (agg_before[season_order[0]], agg_after[season_order[0]]),
        (agg_before[season_order[1]], agg_after[season_order[1]]),
    ]

    totals: list[float] = []
    for group_idx, (before_data, after_data) in enumerate(pairs):
        t_before = _draw_seasonal_mc_bar(ax, x[group_idx * 2], before_data["tx"], before_data["dist"], w)
        t_after = _draw_seasonal_mc_bar(ax, x[group_idx * 2 + 1], after_data["tx"], after_data["dist"], w)
        totals.extend([t_before, t_after])

    max_total = max(totals)

    # --- Delta annotations between before/after pairs ---
    deltas: list[float] = []
    for group_idx in range(2):
        before_total = totals[group_idx * 2]
        after_total = totals[group_idx * 2 + 1]
        delta = after_total - before_total
        deltas.append(delta)

        short_top = min(before_total, after_total)
        tall_top = max(before_total, after_total)

        # Hatched box on the shorter bar of the pair
        x_short = x[group_idx * 2] if before_total <= after_total else x[group_idx * 2 + 1]

        rect = mpatches.FancyBboxPatch(
            (x_short - w / 2, short_top),
            w,
            tall_top - short_top,
            boxstyle="square,pad=0",
            facecolor=SB_COLORS["saffron"],
            alpha=0.12,
            edgecolor="#B8960A",
            linewidth=1.5,
            linestyle=(0, (5, 3)),
            hatch="////",
            zorder=3,
        )
        ax.add_patch(rect)

        sign = "+" if delta >= 0 else ""
        ax.text(
            x_short,
            tall_top + max_total * 0.02,
            f"{sign}{_fmt_mc_dollar(delta)}",
            ha="center",
            va="bottom",
            color=SB_COLORS["saffron"],
            fontweight="bold",
            fontsize=12,
        )

    # --- X-axis labels ---
    ax.set_xticks([])

    for group_idx, season_label in enumerate(season_order):
        group_center = (x[group_idx * 2] + x[group_idx * 2 + 1]) / 2
        ax.text(
            group_center,
            -max_total * 0.10,
            season_label,
            ha="center",
            va="top",
            fontsize=12,
            fontweight="bold",
            fontfamily="IBM Plex Sans",
        )

    bar_labels = ["Before", "After", "Before", "After"]
    for i, label in enumerate(bar_labels):
        ax.text(
            x[i],
            -max_total * 0.04,
            label,
            ha="center",
            va="top",
            fontsize=10,
            fontfamily="IBM Plex Sans",
            color="#666666",
        )

    ax.set_ylabel("Delivery marginal cost ($)", fontsize=12, fontfamily="IBM Plex Sans")
    ax.set_ylim(0, max_total * 1.25)
    ax.set_xlim(x[0] - 0.55, x[-1] + 1.2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_formatter(lambda val, _: f"${val:,.2f}")
    fig.tight_layout()

    # Side callouts on the tallest bar (summer-before is typically tallest)
    all_bars = [(agg_before[s]["dist"], agg_before[s]["tx"], x[i * 2]) for i, s in enumerate(season_order)] + [
        (agg_after[s]["dist"], agg_after[s]["tx"], x[i * 2 + 1]) for i, s in enumerate(season_order)
    ]
    tallest = max(all_bars, key=lambda t: t[0] + t[1])
    _add_mc_side_callouts(fig, ax, tallest[0], tallest[1], bar_x=tallest[2], bar_w=w)

    return fig
