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

import warnings
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    import polars as pl

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
    import polars as pl

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
    import polars as pl

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


def bill_delta_between_segments(
    state: str,
    batch: str,
    segment_before: str,
    segment_after: str,
    *,
    bill_col: str = "energy_total_bill",
    month: str = "Annual",
) -> pl.DataFrame:
    """Diff a per-building bill column between any two ``{scenario}_{stage}`` segments.

    Both axes of comparison reduce to the same join on ``bldg_id``:

    - Same scenario, different stage (e.g. ``"default_precalc"`` ->
      ``"default_calibrated"``): before/after a heat-pump retrofit, holding the
      tariff fixed.
    - Same stage, different scenario (e.g. ``"default_precalc"`` ->
      ``"hp_seasonal_percustomer_passthrough_precalc"``): same population,
      comparing two tariffs.

    Metadata columns (``heating_type_v2``, ``has_hp``) are carried from
    *segment_before* — they are baseline-derived and identical across
    segments/stages for the same population (see rate-design-platform PR #503's
    ``master_metadata.py``).

    Returns a DataFrame with ``bldg_id``, ``weight``, ``has_hp``,
    ``heating_type_v2``, ``bill_before``, ``bill_after``, ``delta``.
    """
    import polars as pl

    before = (
        load_master_bills(state, batch, segment_before)
        .filter(pl.col("month") == month)
        .select(
            "bldg_id",
            "weight",
            pl.col(bill_col).alias("bill_before"),
            pl.col("postprocess_group.has_hp").alias("has_hp"),
            pl.col("postprocess_group.heating_type_v2").alias("heating_type_v2"),
        )
    )
    after = (
        load_master_bills(state, batch, segment_after)
        .filter(pl.col("month") == month)
        .select("bldg_id", pl.col(bill_col).alias("bill_after"))
    )
    joined = before.join(after, on="bldg_id", how="inner").with_columns(
        (pl.col("bill_after") - pl.col("bill_before")).alias("delta")
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
    import polars as pl

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
) -> pl.DataFrame:
    """Weighted mean BAT and weighted customer count by *group_col*, read from ``{scenario}_precalc``."""
    import polars as pl

    bat = cast("pl.DataFrame", load_master_bat(state, batch, segment_name(scenario, "precalc")).collect())
    return (
        bat.group_by(group_col)
        .agg(
            ((pl.col(bat_col) * pl.col("weight")).sum() / pl.col("weight").sum()).alias("mean_per_year"),
            pl.col("weight").sum().alias("n_weighted"),
        )
        .sort("n_weighted", descending=True)
    )


def compare_bat_across_scenarios(state: str, batch: str, scenarios: list[str], **kwargs) -> pl.DataFrame:
    """One row per scenario of ``hp_bat_summary``, for a before/after table.

    E.g. ``compare_bat_across_scenarios(state, batch, ["default", "hp_seasonal_percustomer_passthrough"])``
    gives the HP subclass's overpayment before and after a reform tariff in one table.
    """
    import polars as pl

    rows = [hp_bat_summary(state, batch, scenario, **kwargs) for scenario in scenarios]
    return pl.DataFrame(rows)


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
    import polars as pl

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
