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
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    import polars as pl
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
    import polars as pl

    from lib.data.s3 import list_s3_subdirs, run_dir

    base = f"{S3_BASE}/{state.lower()}/{utility}/{batch}/"
    subdirs = list_s3_subdirs(base)
    run_path = run_dir(subdirs, name_ends_with=f"{utility}_{segment}_delivery")
    return pl.scan_parquet(f"{run_path}/billing_kwh_annual.parquet")


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
    import polars as pl

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


def bat_component_delta(
    state: str,
    batch: str,
    segment_before: str,
    segment_after: str,
    *,
    components: list[str] | None = None,
    exclude_has_hp: bool = True,
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
    """
    import polars as pl

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

    before = load_master_bat(state, batch, segment_before).select(before_select)
    # annual_bill_delivery and economic_burden_delivery are valid at calibrated
    # (see docstring), so suppress the stage warning from load_master_bat.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message=".*not a `_precalc` segment.*")
        after = load_master_bat(state, batch, segment_after).select(after_select)

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
    import polars as pl

    return df.with_columns(
        pl.col(code_col).replace_strict(HEATING_TYPE_LABELS, default=pl.col(code_col)).alias("heating_label")
    )


def weighted_range_pcts(
    df: pl.DataFrame,
    *,
    value_col: str,
    weight_col: str = "weight",
    low_end: Mapping[str, float],
    middle: Sequence[tuple[str, float, float]],
    high_end: Mapping[str, float],
) -> dict[str, float]:
    """Weighted percent of rows in labeled low / middle / high ranges.

    ``low_end`` maps a label to an exclusive upper bound (``value < bound``).
    ``middle`` is a sequence of ``(label, lo, hi)`` half-open intervals
    ``[lo, hi)``; pass as many interior ranges as the chart needs.
    ``high_end`` maps a label to an inclusive lower bound (``value >= bound``).

    Labels are returned in ``low_end``, then ``middle``, then ``high_end``
    order. Percents are on a 0-100 scale and sum to 100 when the ranges
    partition the data and every row has a finite weight.
    """
    import polars as pl

    middle_labels = [label for label, _lo, _hi in middle]
    labels = [*low_end.keys(), *middle_labels, *high_end.keys()]
    if len(labels) != len(set(labels)):
        duplicates = sorted({label for label in labels if labels.count(label) > 1})
        raise ValueError(f"Range labels must be unique; duplicates: {duplicates}")

    total = cast("float", df[weight_col].sum())
    if total == 0:
        return dict.fromkeys(labels, 0.0)

    value = pl.col(value_col)
    out: dict[str, float] = {}
    for label, bound in low_end.items():
        out[label] = cast("float", df.filter(value < bound)[weight_col].sum()) / total * 100
    for label, lo, hi in middle:
        out[label] = cast("float", df.filter((value >= lo) & (value < hi))[weight_col].sum()) / total * 100
    for label, bound in high_end.items():
        out[label] = cast("float", df.filter(value >= bound)[weight_col].sum()) / total * 100
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
        low_end={"savings > $1k": -1000},
        middle=[
            ("savings $0-1k", -1000, 0),
            ("losses $0-1k", 0, 1000),
        ],
        high_end={"losses > $1k": 1000},
    )


def plot_bill_change_quadrants(
    state: str,
    batch: str,
    segment_before: str,
    segment_after: str,
    *,
    rate_name: str = "current rate",
    heating_types: list[str] | None = None,
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

    Each bar shows the weighted % of households in four bins: savings/losses
    of $0-1k and >$1k a year. *rate_name* is threaded into the chart title
    (e.g. ``"default rate"``, ``"seasonal HP rate"``) so charts built under
    different scenarios are self-labeling.

    *heating_types* restricts to specific baseline ``heating_type_v2`` codes
    (e.g. ``["natgas"]``). If ``None`` (default), includes every available
    heating type except ``"heat_pump"`` (already has a heat pump, not
    "upgrading") and ``"other"`` (heterogeneous/unclassified) — see
    ``DEFAULT_EXCLUDED_HEATING_CODES``.

    Since each bar's quadrant mix can look very different (e.g. an
    electric-resistance row might be almost entirely "savings > $1k" while a
    natural-gas row is split across all four bins), the chart replaces the
    usual plotnine fill legend with short color-matched captions
    (``QUADRANT_LABELS``) drawn above *every* bar's segments (skipped only
    when a segment is under 2% of that bar) rather than a single reference
    row — a single row's mix isn't guaranteed to include every quadrant.
    """
    import plotnine as plt
    import polars as pl

    from lib.plotnine import theme_switchbox

    delta = bill_delta_between_segments(state, batch, segment_before, segment_after)
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

    # Build one caption per bar segment >= 2% of that bar, positioned in the
    # gap just above the bar it belongs to (an "x" offset past the bar's own
    # categorical position, since coord_flip makes "x" the vertical axis).
    # Ported from the evolved plot_quadrant_bar() in ny_hp_rates's
    # notebooks/analysis.qmd, adapted from per-scenario rows to per-heating-
    # type rows.
    stacking_order = list(reversed(QUADRANT_ORDER))
    seg_label_offset = 0.45
    seg_label_records: list[dict[str, object]] = []
    for i, group in enumerate(avail_heating):
        group_x = len(avail_heating) - i
        pct = group_pcts[group]
        cum = 0.0
        for q in stacking_order:
            seg_start = cum
            mid = cum + pct[q] / 2
            cum += pct[q]
            if pct[q] < 2:
                continue
            label_y, label_ha = (seg_start, "left") if seg_start < 1 else (mid, "center")
            seg_label_records.append(
                {
                    "x": group_x + seg_label_offset,
                    "y": label_y,
                    "label": QUADRANT_LABELS[q],
                    "color": QUADRANT_COLORS[q],
                    "ha": label_ha,
                }
            )
    seg_label_df = pl.DataFrame(seg_label_records) if seg_label_records else None

    p = (
        plt.ggplot(plot_df, plt.aes(x="heating_label", y="pct", fill="quadrant"))
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
        + plt.scale_x_discrete(expand=(0, 0, 0, 0.6))
        + plt.coord_flip()
        + plt.guides(fill=False)
        + plt.labs(
            x="",
            y="% of weighted households",
            title=f"Change in total annual energy bill after switching to a heat pump, under the {rate_name}",
        )
        + theme_switchbox()
        + plt.theme(figure_size=(11.5, max(3.5, 1.0 + 1.4 * len(avail_heating))))
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


def plot_weighted_bill_change_hist(
    df: pl.DataFrame,
    title: str,
    *,
    bin_width: int = 100,
    show_mean_median: bool = False,
) -> ggplot:
    """Weighted histogram of annual bill change, colored by quadrant.

    *df* must have ``delta`` (dollar change) and ``weight`` columns. Bins are
    colored with ``QUADRANT_COLORS`` at the same +/- $1,000 boundaries as
    ``plot_bill_change_quadrants()``.

    When *show_mean_median* is True, adds dashed vertical lines for the
    weighted mean (carrot) and median (midnight) with text annotations.
    """
    import plotnine as plt
    import polars as pl

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
        + plt.labs(x="Annual bill change ($)", y="Weighted households", title=title)
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
    import polars as pl

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
    import polars as pl

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
    blank rather than tiled white), draws with plotnine, and rasterizes the
    tile layer before returning so ``display_svg``/``display_figure`` produces
    a compact SVG. Expects *df* to already have day-of-year and hour columns
    (e.g. via ``.dt.ordinal_day()`` / ``.dt.hour()`` on a timestamp column).
    """
    import plotnine as plt
    import polars as pl

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
    fig = p.draw()
    for ax in fig.get_axes():
        for img in ax.get_images():
            img.set_rasterized(True)
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
    import polars as pl

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
    import polars as pl

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
    import polars as pl

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
    import polars as pl

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
    import polars as pl

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
    import polars as pl

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
    import polars as pl

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

# Bar labels (x-axis categories) for plot_representative_cost_breakdown().
COST_BREAKDOWN_BAR_ORDER = ["Annual\nkWh", "Cost of\nService", "Delivery\nBill"]

# Stacking order (bottom to top, via position_stack(reverse=True)) within each
# bar. Only kWh, marginal cost, and delivery volumetric get an "existing" /
# "incremental" split in the HP panel -- residual and the fixed charge are flat,
# per-customer costs that don't move with load, so they render as a single block
# in both panels (which is itself part of the story: they *shouldn't* grow with
# incremental consumption).
COST_BREAKDOWN_COMPONENT_ORDER = [
    "kWh (existing)",
    "kWh (incremental)",
    "Marginal Cost (existing)",
    "Marginal Cost (incremental)",
    "Residual",
    "Delivery Fixed",
    "Delivery Volumetric (existing)",
    "Delivery Volumetric (incremental)",
]
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
    import polars as pl

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
    import matplotlib.patches as mpatches
    import matplotlib.pyplot as pyplot
    import numpy as np

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

    side_x = x[2] + w / 2 + 0.15
    d3 = after_reform
    side_specs = [
        ("Delivery\n(Fixed)", d3["delivery_fixed"] / 2, DECOMPOSED_BILL_LABEL_COLORS["delivery_fixed"]),
        (
            "Delivery\n(Volumetric)",
            d3["delivery_fixed"] + d3["delivery_volumetric"] / 2,
            DECOMPOSED_BILL_LABEL_COLORS["delivery_volumetric"],
        ),
        (
            "Supply",
            d3["delivery_fixed"] + d3["delivery_volumetric"] + d3["supply"] / 2,
            DECOMPOSED_BILL_LABEL_COLORS["supply"],
        ),
        (
            "Gas",
            d3["delivery_fixed"] + d3["delivery_volumetric"] + d3["supply"] + d3["gas"] / 2,
            DECOMPOSED_BILL_LABEL_COLORS["gas"],
        ),
    ]
    for lbl, ym, clr in side_specs:
        ax.plot([x[2] + w / 2 + 0.02, side_x - 0.03], [ym, ym], color=clr, linewidth=0.7, alpha=0.6)
        ax.text(side_x, ym, lbl, color=clr, ha="left", va="center", fontsize=8.5, fontweight="bold")

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


def plot_representative_cost_breakdown(
    data: dict[str, dict[str, float]],
    *,
    title: str,
    ng_label: str = "Natural Gas",
    hp_label: str = "Heat Pump",
    min_label_share: float = 0.03,
) -> ggplot:
    """Render the representative-household cost-breakdown chart.

    Takes the dict from ``representative_cost_data()`` -- ``data["ng"]`` and
    ``data["hp"]``, each with ``kwh``, ``mc``, ``residual``,
    ``delivery_fixed``, ``delivery_volumetric``.

    Three facet panels in one row -- annual kWh, cost of service (marginal
    cost + residual), delivery bill (fixed + volumetric) -- each with two
    bars, *ng_label* and *hp_label*. Panels use independent
    (``scales="free_y"``) y-axes since kWh and dollar values are on wildly
    different scales (thousands vs. hundreds); putting them on one shared
    axis squashes the dollar bars into illegibly thin slivers. The HP bar in
    the kWh/marginal-cost/volumetric panels splits into an "existing" portion
    (held at the NG bar's value) and an "incremental" portion stacked on top
    in a lighter shade of the same color -- residual and the fixed charge get
    no incremental split, since they're flat, per-customer costs that don't
    move with load.

    Every segment at least *min_label_share* of its bar's total gets a
    value-and-unit annotation (skipped for single-component bars, whose value
    is already shown by the bar-total label above it). Y-axis ticks/labels
    are hidden throughout -- annotations carry the values, so the tick marks
    would only add clutter.
    """
    import plotnine as plt
    import polars as pl

    from lib.plotnine import theme_switchbox

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
    incremental_spec = [
        ("kwh", "kWh (incremental)", "Annual\nkWh"),
        ("mc", "Marginal Cost (incremental)", "Cost of\nService"),
        ("delivery_volumetric", "Delivery Volumetric (incremental)", "Delivery\nBill"),
    ]

    def _records(scenario: str, d: dict[str, float], *, incr: dict[str, float]) -> list[dict[str, str | float]]:
        recs = [
            {
                "scenario": scenario,
                "bar": "Annual\nkWh",
                "component": "kWh (existing)",
                "value": d["kwh"] - incr.get("kwh", 0.0),
            },
            {
                "scenario": scenario,
                "bar": "Cost of\nService",
                "component": "Marginal Cost (existing)",
                "value": d["mc"] - incr.get("mc", 0.0),
            },
            {"scenario": scenario, "bar": "Cost of\nService", "component": "Residual", "value": d["residual"]},
            {
                "scenario": scenario,
                "bar": "Delivery\nBill",
                "component": "Delivery Fixed",
                "value": d["delivery_fixed"],
            },
            {
                "scenario": scenario,
                "bar": "Delivery\nBill",
                "component": "Delivery Volumetric (existing)",
                "value": d["delivery_volumetric"] - incr.get("delivery_volumetric", 0.0),
            },
        ]
        for key, component, bar in incremental_spec:
            if key in incr:
                recs.append({"scenario": scenario, "bar": bar, "component": component, "value": incr[key]})
        return recs

    records = _records(ng_label, ng, incr={})
    records += _records(hp_label, hp, incr=incremental)

    plot_df = pl.DataFrame(records).with_columns(
        pl.col("scenario").cast(pl.Enum([ng_label, hp_label])),
        pl.col("bar").cast(pl.Enum(COST_BREAKDOWN_BAR_ORDER)),
        pl.col("component").cast(pl.Enum(COST_BREAKDOWN_COMPONENT_ORDER)),
    )

    def _fmt_value(component: str, value: float) -> str:
        return f"{value:,.0f} kWh" if component in _COST_BREAKDOWN_KWH_COMPONENTS else f"${value:,.0f}"

    def _fmt_total(bar: str, value: float) -> str:
        return f"{value:,.0f} kWh" if bar == "Annual\nkWh" else f"${value:,.0f}"

    bar_totals = (
        plot_df.group_by("scenario", "bar")
        .agg(pl.col("value").sum().alias("total"), pl.len().alias("n_components"))
        .with_columns(
            pl.col("scenario").cast(pl.Enum([ng_label, hp_label])),
            pl.col("bar").cast(pl.Enum(COST_BREAKDOWN_BAR_ORDER)),
        )
    )
    bar_totals = bar_totals.with_columns(
        (pl.col("total") * 1.02).alias("label_y"),
        pl.struct(["bar", "total"])
        .map_elements(lambda s: _fmt_total(str(s["bar"]), s["total"]), return_dtype=pl.String)
        .alias("total_label"),
    )

    seg_label_df = (
        plot_df.sort("scenario", "bar", "component")
        .with_columns(pl.col("value").cum_sum().over("scenario", "bar").alias("_cum"))
        .with_columns((pl.col("_cum") - pl.col("value") / 2).alias("y_mid"))
        .join(bar_totals.select("scenario", "bar", "total", "n_components"), on=["scenario", "bar"])
        .filter((pl.col("value") >= min_label_share * pl.col("total")) & (pl.col("n_components") > 1))
        .with_columns(
            pl.struct(["component", "value"])
            .map_elements(lambda s: _fmt_value(str(s["component"]), s["value"]), return_dtype=pl.String)
            .alias("value_label"),
            pl.col("component").cast(pl.String).replace_strict(COST_BREAKDOWN_LABEL_COLORS).alias("label_color"),
        )
    )

    return (
        plt.ggplot(plot_df, plt.aes(x="scenario", y="value", fill="component"))
        + plt.geom_col(position=plt.position_stack(reverse=True), width=0.55)
        + plt.geom_text(
            mapping=plt.aes(x="scenario", y="y_mid", label="value_label", color="label_color"),
            data=seg_label_df,
            fontweight="bold",
            size=8.5,
            inherit_aes=False,
        )
        + plt.geom_text(
            mapping=plt.aes(x="scenario", y="label_y", label="total_label"),
            data=bar_totals,
            va="bottom",
            color="#333333",
            fontweight="bold",
            size=9,
            inherit_aes=False,
        )
        + plt.scale_fill_manual(values=COST_BREAKDOWN_COLORS, breaks=COST_BREAKDOWN_COMPONENT_ORDER)
        + plt.scale_color_identity()
        + plt.scale_y_continuous(expand=(0, 0, 0.16, 0))
        + plt.facet_wrap("bar", ncol=3, scales="free_y")
        + plt.labs(x="", y="", fill="", title=title)
        + theme_switchbox()
        + plt.theme(
            figure_size=(10.5, 5.25),
            legend_position="none",
            axis_text_y=plt.element_blank(),
            axis_ticks_major_y=plt.element_blank(),
        )
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


def tariff_month_rate_table(rates_by_label: dict[str, dict]) -> pl.DataFrame:
    """Month-by-month volumetric delivery rate (¢/kWh), for one or more tariffs side by side.

    *rates_by_label* maps a display column label (e.g. ``"Default rate
    (¢/kWh)"``) to the corresponding ``extract_tariff_rates()`` output. Builds
    one rate column per label from its ``period_rates``/``month_to_period``,
    then joins all of them on ``month`` (ordered Jan-Dec via ``MONTH_ORDER``).
    Works for any number of tariffs, not just the historical pair/triple.
    """
    import polars as pl

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
