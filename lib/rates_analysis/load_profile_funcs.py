"""Load-profile analysis: pre- vs. post-heat-pump electricity consumption.

Reusable functions for building per-building before/after kWh profiles,
computing seasonal and annual percent-change and incremental-kW metrics,
and plotting the results as histograms, scatter plots, dumbbell charts,
and multiplier bars.

Every function is parameterized by ``state``, ``batch``, and segment names
(never hardcoded to one state or utility) so the same notebook can be
copy-pasted to a different jurisdiction by changing the top-level inputs.

Data source: CAIRO's Prefect-produced **master bills** (``comb_bills_year_target``)
which carry monthly ``elec_grid_kwh``, ``gas_therms``,
``postprocess_group.heating_type_v2``, and ``weight`` per building.
Hourly ``billing_kwh_8760.parquet`` is used only for peak-kW analysis.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, cast

import polars as pl

from lib.rates_analysis.rate_case_funcs import (
    HEATING_ORDER,
    HEATING_TYPE_LABELS,
    MONTH_ORDER,
    add_heating_label,
    load_billing_kwh_8760,
    load_master_bills,
    weighted_mean,
    weighted_quantile,
)

if TYPE_CHECKING:
    from matplotlib.figure import Figure
    from plotnine import ggplot

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Heating-type codes excluded from "upgrading to HP" charts: existing HP
# customers aren't upgrading, and "other" is a heterogeneous catch-all.
DEFAULT_EXCLUDED_HEATING_CODES = {"heat_pump", "other"}

# Colors for before/after comparisons.
_BEFORE_COLOR = "#023047"  # SB midnight
_AFTER_COLOR = "#68BED8"  # SB sky

# Fuel-type fill palette (order matches HEATING_ORDER for stacked charts).
FUEL_COLORS: dict[str, str] = {
    "Natural gas": "#023047",  # midnight
    "Oil/propane": "#FC9706",  # carrot
    "Electric resistance": "#68BED8",  # sky
    "Existing heat pump": "#A0AF12",  # pistachio
    "Other": "#999999",  # gray
}

# ---------------------------------------------------------------------------
# Data loading / reshaping
# ---------------------------------------------------------------------------


def _seasonal_kwh(
    bills: pl.LazyFrame,
    summer_month_labels: set[str],
) -> pl.LazyFrame:
    """Add a ``season`` column (``"Summer"`` / ``"Winter"``) to monthly master bills."""
    return bills.with_columns(
        pl.when(pl.col("month").cast(pl.String).is_in(summer_month_labels))
        .then(pl.lit("Summer"))
        .otherwise(pl.lit("Winter"))
        .alias("season"),
    )


def build_load_profile_base(
    state: str,
    batch: str,
    seg_before: str,
    seg_after: str,
    *,
    summer_month_labels: set[str],
    electric_utility: str | None = None,
) -> pl.DataFrame:
    """One row per building with before/after annual and seasonal kWh, percent changes, and labels.

    Parameters
    ----------
    state, batch
        S3 coordinates.
    seg_before, seg_after
        Segment names for the baseline (precalc, upgrade 0) and HP
        (calibrated, upgrade 2) populations.
    summer_month_labels
        Set of 3-letter month abbreviations considered summer
        (e.g. ``{"Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"}``).
    electric_utility
        If given, filters to buildings assigned to this utility
        (``sb.electric_utility``).

    Returns
    -------
    pl.DataFrame
        One row per ``bldg_id`` with columns: ``bldg_id``, ``weight``,
        ``heating_type_v2``, ``heating_label``,
        ``annual_kwh_before``, ``annual_kwh_after``,
        ``summer_kwh_before``, ``summer_kwh_after``,
        ``winter_kwh_before``, ``winter_kwh_after``,
        ``pct_change_annual``, ``pct_change_summer``, ``pct_change_winter``,
        ``incremental_kwh_annual``, ``incremental_kwh_summer``,
        ``incremental_kwh_winter``,
        ``gas_therms_before``, ``gas_therms_after``.
    """
    before_raw = load_master_bills(state, batch, seg_before)
    after_raw = load_master_bills(state, batch, seg_after)
    if electric_utility is not None:
        before_raw = before_raw.filter(pl.col("sb.electric_utility") == electric_utility)
        after_raw = after_raw.filter(pl.col("sb.electric_utility") == electric_utility)

    # Monthly rows only (exclude "Annual" summary row).
    before_monthly = _seasonal_kwh(
        before_raw.filter(pl.col("month") != "Annual"),
        summer_month_labels,
    )
    after_monthly = _seasonal_kwh(
        after_raw.filter(pl.col("month") != "Annual"),
        summer_month_labels,
    )

    def _agg(lf: pl.LazyFrame, suffix: str) -> pl.DataFrame:
        return cast(
            "pl.DataFrame",
            lf.group_by("bldg_id")
            .agg(
                pl.col("weight").first(),
                pl.col("postprocess_group.heating_type_v2").first().alias("heating_type_v2"),
                pl.col("elec_grid_kwh").sum().alias(f"annual_kwh_{suffix}"),
                pl.col("elec_grid_kwh").filter(pl.col("season") == "Summer").sum().alias(f"summer_kwh_{suffix}"),
                pl.col("elec_grid_kwh").filter(pl.col("season") == "Winter").sum().alias(f"winter_kwh_{suffix}"),
                pl.col("gas_therms").sum().alias(f"gas_therms_{suffix}"),
            )
            .collect(),
        )

    before_df = _agg(before_monthly, "before")
    after_df = _agg(after_monthly, "after")

    joined = before_df.join(
        after_df.select(
            "bldg_id",
            "annual_kwh_after",
            "summer_kwh_after",
            "winter_kwh_after",
            "gas_therms_after",
        ),
        on="bldg_id",
        how="inner",
    )

    result = joined.with_columns(
        # Percent changes (guard against division by zero).
        pl.when(pl.col("annual_kwh_before") > 0)
        .then((pl.col("annual_kwh_after") - pl.col("annual_kwh_before")) / pl.col("annual_kwh_before"))
        .otherwise(None)
        .alias("pct_change_annual"),
        pl.when(pl.col("summer_kwh_before") > 0)
        .then((pl.col("summer_kwh_after") - pl.col("summer_kwh_before")) / pl.col("summer_kwh_before"))
        .otherwise(None)
        .alias("pct_change_summer"),
        pl.when(pl.col("winter_kwh_before") > 0)
        .then((pl.col("winter_kwh_after") - pl.col("winter_kwh_before")) / pl.col("winter_kwh_before"))
        .otherwise(None)
        .alias("pct_change_winter"),
        # Incremental kWh (absolute delta).
        (pl.col("annual_kwh_after") - pl.col("annual_kwh_before")).alias("incremental_kwh_annual"),
        (pl.col("summer_kwh_after") - pl.col("summer_kwh_before")).alias("incremental_kwh_summer"),
        (pl.col("winter_kwh_after") - pl.col("winter_kwh_before")).alias("incremental_kwh_winter"),
    )
    return add_heating_label(result)


def build_peak_kw_base(
    state: str,
    utility: str,
    batch: str,
    seg_before: str,
    seg_after: str,
    *,
    summer_month_labels: set[str],
    weights: pl.DataFrame,
) -> pl.DataFrame:
    """One row per building with before/after annual and seasonal peak kW, plus deltas.

    Peak kW is the maximum hourly consumption (kWh in that hour = kW).

    Parameters
    ----------
    weights
        DataFrame with ``bldg_id`` and ``weight`` (from master bills).
    summer_month_labels
        Same definition as :func:`build_load_profile_base`.
    """
    summer_month_nums = {MONTH_ORDER.index(m) + 1 for m in summer_month_labels}

    def _peak_kw(segment: str, suffix: str) -> pl.DataFrame:
        hourly = cast(
            "pl.DataFrame",
            load_billing_kwh_8760(state, utility, batch, segment)
            .with_columns(pl.col("timestamp").dt.month().alias("_month_num"))
            .with_columns(
                pl.when(pl.col("_month_num").is_in(summer_month_nums))
                .then(pl.lit("Summer"))
                .otherwise(pl.lit("Winter"))
                .alias("_season"),
            )
            .collect(),
        )
        annual_peak = hourly.group_by("bldg_id").agg(pl.col("grid_cons_kwh").max().alias(f"peak_kw_annual_{suffix}"))
        seasonal_peak = (
            hourly.group_by("bldg_id", "_season")
            .agg(pl.col("grid_cons_kwh").max().alias("_peak"))
            .pivot(on="_season", index="bldg_id", values="_peak")
            .rename(
                {
                    "Summer": f"peak_kw_summer_{suffix}",
                    "Winter": f"peak_kw_winter_{suffix}",
                }
            )
        )
        return annual_peak.join(seasonal_peak, on="bldg_id")

    before_pk = _peak_kw(seg_before, "before")
    after_pk = _peak_kw(seg_after, "after")

    joined = before_pk.join(after_pk, on="bldg_id", how="inner").join(
        weights.select("bldg_id", "weight"), on="bldg_id", how="inner"
    )
    return joined.with_columns(
        (pl.col("peak_kw_annual_after") - pl.col("peak_kw_annual_before")).alias("incremental_kw_annual"),
        (pl.col("peak_kw_summer_after") - pl.col("peak_kw_summer_before")).alias("incremental_kw_summer"),
        (pl.col("peak_kw_winter_after") - pl.col("peak_kw_winter_before")).alias("incremental_kw_winter"),
    )


# ---------------------------------------------------------------------------
# Summary statistics
# ---------------------------------------------------------------------------


def load_profile_summary(
    df: pl.DataFrame,
    *,
    group_col: str = "heating_label",
) -> pl.DataFrame:
    """Weighted mean/median kWh and multiplier by fuel type.

    Returns one row per group with before/after kWh (annual, summer, winter),
    multiplier (after/before), and weighted mean percent change.
    """
    rows: list[dict[str, object]] = []
    groups = df[group_col].unique().to_list()
    ordered = [g for g in HEATING_ORDER if g in groups]
    ordered.extend(g for g in groups if g not in ordered)

    for group in ordered:
        sub = df.filter(pl.col(group_col) == group)
        n_unweighted = sub.height
        n_weighted = float(sub["weight"].sum())

        row: dict[str, object] = {"group": group, "n_unweighted": n_unweighted, "n_weighted": n_weighted}
        for period in ("annual", "summer", "winter"):
            before_col = f"{period}_kwh_before"
            after_col = f"{period}_kwh_after"
            pct_col = f"pct_change_{period}"

            mean_before = weighted_mean(sub, before_col)
            mean_after = weighted_mean(sub, after_col)
            multiplier = mean_after / mean_before if mean_before > 0 else float("nan")
            mean_pct = weighted_mean(sub, pct_col)
            median_pct = weighted_quantile(sub, pct_col, 0.5)

            row[f"mean_{period}_kwh_before"] = mean_before
            row[f"mean_{period}_kwh_after"] = mean_after
            row[f"multiplier_{period}"] = multiplier
            row[f"mean_pct_change_{period}"] = mean_pct
            row[f"median_pct_change_{period}"] = median_pct
        rows.append(row)

    return pl.DataFrame(rows)


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------

# Colors for stat overlay lines (distinct from bar fills).
_MEAN_COLOR = "#C0392B"  # muted red — visible against all bar fills
_MEDIAN_COLOR = "#333333"  # dark gray


def _weighted_std(values: pl.Series, weights: pl.Series) -> float:
    """Population-weighted standard deviation."""
    import numpy as np

    x = values.to_numpy().astype(float)
    w = weights.to_numpy().astype(float)
    mask = np.isfinite(x) & np.isfinite(w)
    x, w = x[mask], w[mask]
    w_sum = w.sum()
    if w_sum == 0:
        return float("nan")
    mu = float((w * x).sum() / w_sum)
    return float(np.sqrt((w * (x - mu) ** 2).sum() / w_sum))


def _facet_stats(
    long: pl.DataFrame,
    value_col: str,
    facet_col: str | None = None,
    facet_levels: list[str] | None = None,
    label_fmt: str = "{:,.0f}",
) -> pl.DataFrame:
    """Compute weighted mean, median, and ±1 SD — per facet level or globally.

    Parameters
    ----------
    facet_col / facet_levels
        If both are given, compute stats per facet panel.
        If ``None``, compute a single row of global stats.
    label_fmt
        Format string for the numeric labels (e.g. ``"{:,.0f}"`` for kWh,
        ``"{:.0%}"`` for percent).
    """

    def _one_group(sub: pl.DataFrame) -> dict[str, object]:
        w_mean = weighted_mean(sub, value_col)
        w_med = weighted_quantile(sub, value_col, 0.5)
        q25 = weighted_quantile(sub, value_col, 0.25)
        q75 = weighted_quantile(sub, value_col, 0.75)
        iqr = q75 - q25
        return {
            "mean_val": w_mean,
            "median_val": w_med,
            "sd_lo": q25,
            "sd_hi": q75,
            "mean_label": f"Mean: {label_fmt.format(w_mean)}",
            "median_label": f"Median: {label_fmt.format(w_med)}",
            "sd_label": f"IQR: {label_fmt.format(iqr)}",
        }

    if facet_col is not None and facet_levels is not None:
        rows: list[dict[str, object]] = []
        for level in facet_levels:
            row = _one_group(long.filter(pl.col(facet_col) == level))
            row[facet_col] = level
            rows.append(row)
        return pl.DataFrame(rows).with_columns(
            pl.col(facet_col).cast(pl.Enum(facet_levels)),
        )

    return pl.DataFrame([_one_group(long)])


def _add_stat_layers(
    p: ggplot,
    stats_df: pl.DataFrame,
    binned: pl.DataFrame,
    bin_width: float,
    facet_col: str | None = None,
) -> ggplot:
    """Add mean/median lines + ±1 SD band to a histogram.

    Works for both faceted (``facet_col`` set) and non-faceted histograms.
    """
    import plotnine as plt

    # Compute y position for text labels (90% of tallest stacked bar).
    group_cols = ["bin_center", facet_col] if facet_col else ["bin_center"]
    _smax_raw = binned.group_by(group_cols).agg(pl.col("weight_sum").sum())["weight_sum"].cast(pl.Float64).max()
    stacked_max: float = float(_smax_raw) if isinstance(_smax_raw, (int, float)) else 1.0
    label_y = stacked_max * 0.92

    stats_df = stats_df.with_columns(
        pl.lit(0.0).alias("ymin"),
        pl.lit(stacked_max * 2).alias("ymax"),
        pl.lit(label_y).alias("label_y"),
        pl.lit(label_y * 0.82).alias("label_y_sd"),
    )

    return (
        p
        # ±1 SD band
        + plt.geom_rect(
            mapping=plt.aes(xmin="sd_lo", xmax="sd_hi", ymin="ymin", ymax="ymax"),
            data=stats_df,
            fill="#888888",
            alpha=0.10,
            inherit_aes=False,
        )
        # Mean line (dashed red)
        + plt.geom_vline(
            mapping=plt.aes(xintercept="mean_val"),
            data=stats_df,
            linetype="dashed",
            color=_MEAN_COLOR,
            size=0.7,
        )
        # Median line (solid dark gray)
        + plt.geom_vline(
            mapping=plt.aes(xintercept="median_val"),
            data=stats_df,
            linetype="solid",
            color=_MEDIAN_COLOR,
            size=0.7,
        )
        # Labels
        + plt.geom_text(
            mapping=plt.aes(x="mean_val", y="label_y", label="mean_label"),
            data=stats_df,
            color=_MEAN_COLOR,
            ha="left",
            va="top",
            size=8,
            nudge_x=bin_width * 1.5,
            inherit_aes=False,
        )
        + plt.geom_text(
            mapping=plt.aes(x="median_val", y="label_y", label="median_label"),
            data=stats_df,
            color=_MEDIAN_COLOR,
            ha="right",
            va="top",
            size=8,
            nudge_x=-bin_width * 1.5,
            inherit_aes=False,
        )
        # SD value label (positioned at right edge of SD band)
        + plt.geom_text(
            mapping=plt.aes(x="sd_hi", y="label_y_sd", label="sd_label"),
            data=stats_df,
            color="#666666",
            ha="left",
            va="top",
            size=8,
            nudge_x=bin_width * 1.5,
            inherit_aes=False,
        )
    )


# ---------------------------------------------------------------------------
# Plotting: histograms
# ---------------------------------------------------------------------------


def _filter_upgrading(df: pl.DataFrame, fuel_filter: str | None = None) -> pl.DataFrame:
    """Drop existing-HP and 'other' rows; optionally restrict to one fuel code."""
    result = df.filter(~pl.col("heating_type_v2").is_in(DEFAULT_EXCLUDED_HEATING_CODES))
    if fuel_filter is not None:
        result = result.filter(pl.col("heating_type_v2") == fuel_filter)
    return result


def plot_annual_kwh_hist(
    df: pl.DataFrame,
    *,
    fuel_filter: str | None = None,
    bin_width: float = 500.0,
    x_max: float | None = None,
    show_stats: bool = True,
    title: str | None = None,
) -> ggplot:
    """Weighted histogram of annual kWh, faceted Before/After, stacked by fuel type.

    Parameters
    ----------
    fuel_filter
        If given, restrict to one ``heating_type_v2`` code (e.g. ``"natgas"``).
    x_max
        Hard x-axis upper limit (kWh). Data beyond this is clipped from view
        but not dropped from the dataset.
    show_stats
        If ``True`` (default), overlay weighted mean / median lines and a
        ±1 SD shaded band on each facet panel.
    """
    import plotnine as plt

    from lib.plotnine import theme_switchbox

    sub = _filter_upgrading(df, fuel_filter)
    fuel_label = HEATING_TYPE_LABELS.get(fuel_filter, fuel_filter) if fuel_filter else None

    # Reshape to long: one row per building per period.
    before = sub.select(
        "bldg_id",
        "weight",
        "heating_label",
        pl.col("annual_kwh_before").alias("annual_kwh"),
    ).with_columns(pl.lit("Before heat pump").alias("period"))
    after = sub.select(
        "bldg_id",
        "weight",
        "heating_label",
        pl.col("annual_kwh_after").alias("annual_kwh"),
    ).with_columns(pl.lit("After heat pump").alias("period"))
    long = pl.concat([before, after]).with_columns(
        pl.col("period").cast(pl.Enum(["Before heat pump", "After heat pump"])),
        pl.col("heating_label").cast(
            pl.Enum([h for h in HEATING_ORDER if h in sub["heating_label"].unique().to_list()])
        ),
    )

    # Pre-bin for weighted histogram.
    binned = (
        long.with_columns(
            ((pl.col("annual_kwh") / bin_width).floor() * bin_width + bin_width / 2).alias("bin_center"),
        )
        .group_by("bin_center", "period", "heating_label")
        .agg(pl.col("weight").sum().alias("weight_sum"))
    )

    if title is None:
        scope = f"{fuel_label}-heated homes" if fuel_label else "all homes (by baseline fuel)"
        title = f"Annual electricity consumption: {scope}"

    avail = [h for h in HEATING_ORDER if h in sub["heating_label"].unique().to_list()]
    colors = {h: FUEL_COLORS.get(h, "#999999") for h in avail}

    p = (
        plt.ggplot(binned, plt.aes(x="bin_center", y="weight_sum", fill="heating_label"))
        + plt.geom_col(width=bin_width * 0.9)
        + plt.facet_wrap("period", ncol=1)
        + plt.scale_fill_manual(values=colors, breaks=avail, name="Baseline fuel")
        + plt.scale_x_continuous(labels=lambda xs: [f"{x:,.0f}" for x in xs])
        + plt.labs(x="Annual kWh", y="Weighted households", title=title)
        + theme_switchbox()
        + plt.theme(figure_size=(14, 8))
    )
    if x_max is not None:
        p = p + plt.coord_cartesian(xlim=(0, x_max))
    if show_stats:
        facet_levels = ["Before heat pump", "After heat pump"]
        stats_df = _facet_stats(long, "annual_kwh", "period", facet_levels, label_fmt="{:,.0f}")
        p = _add_stat_layers(p, stats_df, binned, bin_width, facet_col="period")
    if fuel_filter:
        p = p + plt.guides(fill=False)
    return p


def plot_pct_change_hist(
    df: pl.DataFrame,
    season: str,
    *,
    fuel_filter: str | None = None,
    bin_width: float = 0.1,
    x_max: float | None = None,
    show_stats: bool = True,
    title: str | None = None,
) -> ggplot:
    """Weighted histogram of percent change in kWh for a season, stacked by fuel.

    Parameters
    ----------
    season
        ``"annual"``, ``"summer"``, or ``"winter"``.
    fuel_filter
        Restrict to one ``heating_type_v2`` code.
    x_max
        Hard x-axis upper limit as a fraction (e.g. ``2.0`` for 200%).
        Overrides the default 1st-99th percentile auto-range.
    show_stats
        If ``True`` (default), overlay weighted mean / median lines and a
        ±1 SD shaded band.
    """
    import plotnine as plt

    from lib.plotnine import theme_switchbox

    sub = _filter_upgrading(df, fuel_filter)
    pct_col = f"pct_change_{season}"
    fuel_label = HEATING_TYPE_LABELS.get(fuel_filter, fuel_filter) if fuel_filter else None

    # Drop buildings with no kWh in the before period (undefined pct change).
    sub = sub.filter(pl.col(pct_col).is_not_null())
    avail = [h for h in HEATING_ORDER if h in sub["heating_label"].unique().to_list()]
    colors = {h: FUEL_COLORS.get(h, "#999999") for h in avail}

    binned = (
        sub.with_columns(
            ((pl.col(pct_col) / bin_width).floor() * bin_width + bin_width / 2).alias("bin_center"),
            pl.col("heating_label").cast(pl.Enum(avail)),
        )
        .group_by("bin_center", "heating_label")
        .agg(pl.col("weight").sum().alias("weight_sum"))
    )

    # Clip display range.
    snap = max(bin_width, 0.05)
    x_lo = math.floor(weighted_quantile(sub, pct_col, 0.01) / snap) * snap
    x_hi = x_max if x_max is not None else math.ceil(weighted_quantile(sub, pct_col, 0.99) / snap) * snap

    if title is None:
        scope = f"{fuel_label}-heated homes" if fuel_label else "all homes (by baseline fuel)"
        title = f"Change in {season} electricity consumption: {scope}"

    p = (
        plt.ggplot(binned, plt.aes(x="bin_center", y="weight_sum", fill="heating_label"))
        + plt.geom_col(width=bin_width * 0.9)
        + plt.geom_vline(xintercept=0, linetype="dotted", color="gray")
        + plt.coord_cartesian(xlim=(x_lo, x_hi))
        + plt.scale_x_continuous(labels=lambda xs: [f"{x:.0%}" for x in xs])
        + plt.scale_fill_manual(values=colors, breaks=avail, name="Baseline fuel")
        + plt.labs(x=f"% change in {season} kWh", y="Weighted households", title=title)
        + theme_switchbox()
        + plt.theme(figure_size=(14, 5.5))
    )
    if show_stats:
        stats_df = _facet_stats(sub, pct_col, label_fmt="{:.0%}")
        p = _add_stat_layers(p, stats_df, binned, bin_width)
    if fuel_filter:
        p = p + plt.guides(fill=False)
    return p


def plot_incremental_kwh_hist(
    df: pl.DataFrame,
    period: str,
    *,
    fuel_filter: str | None = None,
    bin_width: float = 500.0,
    x_range: tuple[float, float] | None = None,
    show_stats: bool = True,
    title: str | None = None,
) -> ggplot:
    """Weighted histogram of incremental kWh (after - before), faceted by fuel type.

    Parameters
    ----------
    period
        ``"annual"``, ``"summer"``, or ``"winter"``.
    x_range
        ``(lo, hi)`` hard x-axis limits. Overrides the default 1st-99th
        percentile auto-range.
    show_stats
        If ``True`` (default), overlay weighted mean / median lines and a
        ±1 SD shaded band on each panel.
    """
    import plotnine as plt

    from lib.plotnine import SB_COLORS, theme_switchbox

    sub = _filter_upgrading(df, fuel_filter)
    value_col = f"incremental_kwh_{period}"
    fuel_label = HEATING_TYPE_LABELS.get(fuel_filter, fuel_filter) if fuel_filter else None

    if title is None:
        scope = f"{fuel_label}-heated homes" if fuel_label else "all homes"
        title = f"Incremental {period} kWh after heat pump: {scope}"

    avail = [h for h in HEATING_ORDER if h in sub["heating_label"].unique().to_list()]

    if x_range is not None:
        x_lo, x_hi = x_range
    else:
        snap = max(bin_width, 100)
        x_lo = math.floor(weighted_quantile(sub, value_col, 0.01) / snap) * snap
        x_hi = math.ceil(weighted_quantile(sub, value_col, 0.99) / snap) * snap

    from mizani.breaks import breaks_extended

    breaks_fn = breaks_extended(n=8)

    binned = (
        sub.with_columns(
            ((pl.col(value_col) / bin_width).floor() * bin_width + bin_width / 2).alias("bin_center"),
        )
        .group_by("bin_center", "heating_label")
        .agg(pl.col("weight").sum().alias("weight_sum"))
    )

    if fuel_filter:
        p = (
            plt.ggplot(binned, plt.aes(x="bin_center", y="weight_sum"))
            + plt.geom_col(width=bin_width * 0.9, fill=SB_COLORS["sky"])
            + plt.geom_vline(xintercept=0, linetype="dotted", color="gray")
            + plt.coord_cartesian(xlim=(x_lo, x_hi))
            + plt.scale_x_continuous(
                breaks=lambda _limits, lo=x_lo, hi=x_hi: list(breaks_fn((lo, hi))),
                labels=lambda xs: [f"{x:,.0f}" for x in xs],
            )
            + plt.labs(x=f"Incremental {period} kWh", y="Weighted households", title=title)
            + theme_switchbox()
            + plt.theme(figure_size=(14, 5))
        )
        if show_stats:
            stats_df = _facet_stats(sub, value_col, label_fmt="{:,.0f}")
            p = _add_stat_layers(p, stats_df, binned, bin_width)
    else:
        binned = binned.with_columns(pl.col("heating_label").cast(pl.Enum(avail)))
        facet_scales = "free_y" if x_range is not None else "free"
        p = (
            plt.ggplot(binned, plt.aes(x="bin_center", y="weight_sum"))
            + plt.geom_col(width=bin_width * 0.9, fill=SB_COLORS["sky"])
            + plt.geom_vline(xintercept=0, linetype="dotted", color="gray")
            + plt.facet_wrap("heating_label", scales=facet_scales)
            + plt.coord_cartesian(xlim=(x_lo, x_hi))
            + plt.scale_x_continuous(labels=lambda xs: [f"{x:,.0f}" for x in xs])
            + plt.labs(x=f"Incremental {period} kWh", y="Weighted households", title=title)
            + theme_switchbox()
            + plt.theme(figure_size=(14, 7))
        )
        if show_stats:
            stats_df = _facet_stats(
                sub,
                value_col,
                "heating_label",
                avail,
                label_fmt="{:,.0f}",
            )
            p = _add_stat_layers(p, stats_df, binned, bin_width, facet_col="heating_label")
    return p


def plot_incremental_kw_hist(
    df: pl.DataFrame,
    period: str,
    *,
    bin_width: float = 0.5,
    show_stats: bool = True,
    title: str | None = None,
    heating_labels: pl.DataFrame | None = None,
) -> ggplot:
    """Weighted histogram of incremental peak kW (after - before), faceted by fuel type.

    *df* is the output of :func:`build_peak_kw_base`, which has no
    ``heating_label`` column. Pass *heating_labels* (a DataFrame with
    ``bldg_id``, ``heating_type_v2``, ``heating_label``) to add it.
    """
    import plotnine as plt

    from lib.plotnine import SB_COLORS, theme_switchbox

    value_col = f"incremental_kw_{period}"
    data = df
    if heating_labels is not None:
        data = data.join(
            heating_labels.select("bldg_id", "heating_type_v2", "heating_label"),
            on="bldg_id",
            how="inner",
        )
        data = data.filter(~pl.col("heating_type_v2").is_in(DEFAULT_EXCLUDED_HEATING_CODES))

    if title is None:
        title = f"Incremental {period} peak kW after heat pump"

    avail = [h for h in HEATING_ORDER if h in data["heating_label"].unique().to_list()]

    snap = max(bin_width, 0.5)
    x_lo = math.floor(weighted_quantile(data, value_col, 0.01) / snap) * snap
    x_hi = math.ceil(weighted_quantile(data, value_col, 0.99) / snap) * snap

    from mizani.breaks import breaks_extended

    breaks_fn = breaks_extended(n=8)

    binned = (
        data.with_columns(
            ((pl.col(value_col) / bin_width).floor() * bin_width + bin_width / 2).alias("bin_center"),
            pl.col("heating_label").cast(pl.Enum(avail)),
        )
        .group_by("bin_center", "heating_label")
        .agg(pl.col("weight").sum().alias("weight_sum"))
    )

    p = (
        plt.ggplot(binned, plt.aes(x="bin_center", y="weight_sum"))
        + plt.geom_col(width=bin_width * 0.9, fill=SB_COLORS["sky"])
        + plt.geom_vline(xintercept=0, linetype="dotted", color="gray")
        + plt.facet_wrap("heating_label", scales="free")
        + plt.coord_cartesian(xlim=(x_lo, x_hi))
        + plt.scale_x_continuous(
            breaks=lambda _limits, lo=x_lo, hi=x_hi: list(breaks_fn((lo, hi))),
            labels=lambda xs: [f"{x:,.1f}" for x in xs],
        )
        + plt.labs(x=f"Incremental {period} peak kW", y="Weighted households", title=title)
        + theme_switchbox()
        + plt.theme(figure_size=(14, 7))
    )
    if show_stats:
        stats_df = _facet_stats(
            data,
            value_col,
            "heating_label",
            avail,
            label_fmt="{:,.1f}",
        )
        p = _add_stat_layers(p, stats_df, binned, bin_width, facet_col="heating_label")
    return p


# ---------------------------------------------------------------------------
# Plotting: before-vs-after scatter
# ---------------------------------------------------------------------------


def plot_before_after_scatter(
    df: pl.DataFrame,
    period: str = "annual",
    *,
    fuel_filter: str | None = None,
    axis_max: float | None = None,
    title: str | None = None,
    alpha: float = 0.35,
) -> Figure:
    """Scatter of before-kWh vs. after-kWh with a y = x reference line.

    Points above the diagonal increased usage after heat pump installation.
    Returns a matplotlib Figure (use ``display_figure`` for embedding).

    Parameters
    ----------
    period
        ``"annual"``, ``"summer"``, or ``"winter"``.
    axis_max
        Hard upper limit for both axes (kWh). If ``None``, auto-scales to
        1.05x the data maximum.
    """
    import matplotlib.pyplot as pyplot
    import numpy as np

    sub = _filter_upgrading(df, fuel_filter)
    before_col = f"{period}_kwh_before"
    after_col = f"{period}_kwh_after"
    fuel_label = HEATING_TYPE_LABELS.get(fuel_filter, fuel_filter) if fuel_filter else None

    avail = [h for h in HEATING_ORDER if h in sub["heating_label"].unique().to_list()]

    fig, ax = pyplot.subplots(figsize=(8, 8))
    max_val = 0.0
    for label in avail:
        group = sub.filter(pl.col("heating_label") == label)
        x = group[before_col].to_numpy()
        y = group[after_col].to_numpy()
        color = FUEL_COLORS.get(label, "#999999")
        ax.scatter(x, y, alpha=alpha, s=12, color=color, label=label, edgecolors="none")
        max_val = max(max_val, float(np.nanmax(x)), float(np.nanmax(y)))

    lim = axis_max if axis_max is not None else max_val * 1.05
    ax.plot([0, lim], [0, lim], color="#999999", linewidth=1, linestyle="--", zorder=0)
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_aspect("equal")

    ax.set_xlabel(f"{period.capitalize()} kWh (before heat pump)", fontsize=11)
    ax.set_ylabel(f"{period.capitalize()} kWh (after heat pump)", fontsize=11)
    if title is None:
        scope = f"{fuel_label}-heated homes" if fuel_label else "all homes"
        title = f"{period.capitalize()} electricity: before vs. after heat pump ({scope})"
    ax.set_title(title, fontsize=13, fontweight="bold", loc="left")
    ax.legend(fontsize=10, frameon=False)

    ax.text(
        lim * 0.97,
        lim * 0.60,
        "Uses more\nafter HP →",
        ha="right",
        va="center",
        fontsize=10,
        color="#666666",
        fontstyle="italic",
    )
    fig.tight_layout()
    pyplot.close(fig)
    return fig


# ---------------------------------------------------------------------------
# Plotting: percent-change vs. base load
# ---------------------------------------------------------------------------


def plot_pct_change_vs_base_load(
    df: pl.DataFrame,
    season: str = "annual",
    *,
    x_max: float | None = None,
    y_range: tuple[float, float] | None = None,
    title: str | None = None,
    alpha: float = 0.20,
) -> Figure:
    """Scatter: baseline kWh (x) vs. percent change in kWh (y), faceted by fuel.

    Reveals whether the magnitude of change depends on baseline load size.
    Returns a matplotlib Figure (use ``display_figure`` for embedding).
    """
    import matplotlib.pyplot as pyplot

    sub = _filter_upgrading(df)
    pct_col = f"pct_change_{season}"
    sub = sub.filter(pl.col(pct_col).is_not_null())
    avail = [h for h in HEATING_ORDER if h in sub["heating_label"].unique().to_list()]

    n_fuels = len(avail)
    fig, axes = pyplot.subplots(1, n_fuels, figsize=(14, 5), sharey=True)
    if n_fuels == 1:
        axes = [axes]

    for ax, label in zip(axes, avail, strict=False):
        group = sub.filter(pl.col("heating_label") == label)
        x = group["annual_kwh_before"].to_numpy()
        y = group[pct_col].to_numpy()
        color = FUEL_COLORS.get(label, "#999999")
        ax.scatter(x, y, alpha=alpha, s=8, color=color, edgecolors="none")
        ax.axhline(0, color="#999999", linewidth=0.8, linestyle="--")
        ax.set_title(label, fontsize=12, fontweight="bold")
        ax.set_xlabel("Baseline annual kWh", fontsize=10)
        ax.xaxis.set_major_formatter(pyplot.FuncFormatter(lambda v, p: f"{v:,.0f}"))
        ax.yaxis.set_major_formatter(pyplot.FuncFormatter(lambda v, p: f"{v:.0%}"))
        if x_max is not None:
            ax.set_xlim(0, x_max)
        else:
            ax.set_xlim(left=0)
        if y_range is not None:
            ax.set_ylim(*y_range)

    axes[0].set_ylabel(f"% change in {season} kWh", fontsize=10)
    if title is None:
        title = f"{season.capitalize()} electricity change vs. baseline load, by heating fuel"
    fig.suptitle(title, fontsize=13, fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.94))
    pyplot.close(fig)
    return fig


def plot_outcome_spread(
    df: pl.DataFrame,
    season: str = "annual",
    *,
    bin_width: float = 1000.0,
    x_max: float | None = None,
    title: str | None = None,
) -> ggplot:
    """IQR ribbon of percent change as a function of baseline kWh.

    Shows that post-HP outcome variance widens for homes with higher
    baseline electricity consumption.  The ribbon spans Q25-Q75
    (interquartile range) and the line is the weighted median.
    The IQR is computed per baseline-kWh bin using survey weights.
    """
    import plotnine as plt

    from lib.plotnine import theme_switchbox

    sub = _filter_upgrading(df)
    pct_col = f"pct_change_{season}"
    sub = sub.filter(pl.col(pct_col).is_not_null())

    # Bin by baseline annual kWh.
    sub = sub.with_columns(
        ((pl.col("annual_kwh_before") / bin_width).floor() * bin_width + bin_width / 2).alias("base_bin"),
    )

    rows: list[dict[str, object]] = []
    for (base_bin, heating_label), grp in sub.group_by("base_bin", "heating_label"):
        if grp.height < 5:
            continue
        q25 = weighted_quantile(grp, pct_col, 0.25)
        q50 = weighted_quantile(grp, pct_col, 0.50)
        q75 = weighted_quantile(grp, pct_col, 0.75)
        rows.append(
            {
                "base_bin": float(cast(float, base_bin)),
                "heating_label": str(heating_label),
                "q25": q25,
                "median": q50,
                "q75": q75,
                "iqr": q75 - q25,
            }
        )

    if not rows:
        msg = f"No data to plot for outcome spread ({season})"
        raise ValueError(msg)

    ribbon = pl.DataFrame(rows)
    avail = [h for h in HEATING_ORDER if h in ribbon["heating_label"].unique().to_list()]
    ribbon = ribbon.with_columns(
        pl.col("heating_label").cast(pl.Enum(avail)),
    )
    colors = {h: FUEL_COLORS.get(h, "#999999") for h in avail}

    p = (
        plt.ggplot(ribbon, plt.aes(x="base_bin", color="heating_label", fill="heating_label"))
        + plt.geom_ribbon(plt.aes(ymin="q25", ymax="q75"), alpha=0.25, color="none")
        + plt.geom_line(plt.aes(y="median"), size=0.9)
        + plt.geom_hline(yintercept=0, linetype="dashed", color="#999999")
        + plt.facet_wrap("heating_label", scales="free_y")
        + plt.scale_color_manual(values=colors, breaks=avail)
        + plt.scale_fill_manual(values=colors, breaks=avail)
        + plt.scale_x_continuous(labels=lambda xs: [f"{x:,.0f}" for x in xs])
        + plt.scale_y_continuous(labels=lambda ys: [f"{y:.0%}" for y in ys])
        + plt.labs(
            x="Baseline annual kWh",
            y=f"% change in {season} kWh",
            title=title or f"Outcome spread: {season} electricity change by baseline load",
        )
        + theme_switchbox()
        + plt.theme(figure_size=(14, 5.5))
        + plt.guides(color=False, fill=False)
    )
    if x_max is not None:
        p = p + plt.coord_cartesian(xlim=(0, x_max))
    return p


# ---------------------------------------------------------------------------
# Plotting: dumbbell chart (summary-level before/after)
# ---------------------------------------------------------------------------


def plot_dumbbell_summary(
    summary: pl.DataFrame,
    period: str = "annual",
    *,
    title: str | None = None,
) -> Figure:
    """Horizontal dumbbell chart: weighted-mean before vs. after kWh by fuel type.

    Each row is one fuel type (from :func:`load_profile_summary`). Left dot =
    before, right dot = after, the connecting line is the change.

    Returns a matplotlib Figure.
    """
    import matplotlib.pyplot as pyplot

    before_col = f"mean_{period}_kwh_before"
    after_col = f"mean_{period}_kwh_after"

    # Filter to groups with nonzero before/after.
    data = summary.filter((pl.col(before_col) > 0) | (pl.col(after_col) > 0))
    groups = data["group"].to_list()
    n_groups = len(groups)

    fig, ax = pyplot.subplots(figsize=(14, max(3, n_groups * 1.0 + 1.5)))

    for i, group in enumerate(reversed(groups)):
        row = data.filter(pl.col("group") == group)
        before_val = float(row[before_col][0])
        after_val = float(row[after_col][0])
        y = i

        # Connecting line.
        ax.plot(
            [before_val, after_val],
            [y, y],
            color="#CCCCCC",
            linewidth=2,
            zorder=1,
        )
        # Before dot (midnight).
        ax.scatter(before_val, y, color=_BEFORE_COLOR, s=80, zorder=2, label="Before HP" if i == 0 else "")
        # After dot (sky).
        ax.scatter(after_val, y, color=_AFTER_COLOR, s=80, zorder=2, label="After HP" if i == 0 else "")

        # Multiplier annotation.
        multiplier = after_val / before_val if before_val > 0 else float("nan")
        x_mid = (before_val + after_val) / 2
        ax.text(
            x_mid,
            y + 0.3,
            f"{multiplier:.1f}x",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#333333",
        )

    ax.set_yticks(range(n_groups))
    ax.set_yticklabels(list(reversed(groups)), fontsize=11)
    ax.set_xlabel(f"Mean {period} kWh", fontsize=11)
    ax.xaxis.set_major_formatter(pyplot.FuncFormatter(lambda x, p: f"{x:,.0f}"))
    ax.set_xlim(left=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="lower right", fontsize=10, frameon=False)

    if title is None:
        title = f"Mean {period} electricity consumption: before vs. after heat pump"
    ax.set_title(title, fontsize=13, fontweight="bold", loc="left")

    fig.tight_layout()
    pyplot.close(fig)
    return fig


# ---------------------------------------------------------------------------
# Plotting: multiplier bar chart
# ---------------------------------------------------------------------------


def plot_multiplier_bar(
    summary: pl.DataFrame,
    *,
    title: str | None = None,
) -> ggplot:
    """Grouped bar chart: kWh multiplier (after/before) by fuel type and season.

    Directly shows "2x annual, 3x winter, 0.9x summer" for each fuel.
    """
    import plotnine as plt

    from lib.plotnine import SB_COLORS, theme_switchbox

    rows: list[dict[str, object]] = []
    for row_dict in summary.to_dicts():
        group = row_dict["group"]
        for period in ("Annual", "Summer", "Winter"):
            rows.append(
                {
                    "group": group,
                    "period": period,
                    "multiplier": row_dict[f"multiplier_{period.lower()}"],
                }
            )

    chart_df = pl.DataFrame(rows).with_columns(
        pl.col("period").cast(pl.Enum(["Winter", "Annual", "Summer"])),
        pl.col("group").cast(pl.Enum([g for g in HEATING_ORDER if g in summary["group"].to_list()])),
    )

    season_colors = {
        "Winter": SB_COLORS["midnight"],
        "Annual": SB_COLORS["sky"],
        "Summer": SB_COLORS["carrot"],
    }

    if title is None:
        title = "Electricity consumption multiplier after heat pump"

    return (
        plt.ggplot(chart_df, plt.aes(x="group", y="multiplier", fill="period"))
        + plt.geom_col(position="dodge", width=0.7)
        + plt.geom_hline(yintercept=1, linetype="dashed", color="gray")
        + plt.geom_text(
            plt.aes(label="multiplier"),
            position=plt.position_dodge(width=0.7),
            va="bottom",
            format_string="{:.1f}x",
            size=9,
            fontweight="bold",
        )
        + plt.scale_fill_manual(values=season_colors, name="Period")
        + plt.scale_y_continuous(expand=(0, 0, 0.15, 0))
        + plt.labs(x="", y="kWh multiplier (after / before)", title=title)
        + theme_switchbox()
        + plt.theme(figure_size=(14, 5.5))
    )
