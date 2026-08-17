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


def quadrant_pcts(df: pl.DataFrame, weight_col: str = "weight") -> dict[str, float]:
    """Weighted % of households in each bill-change quadrant.

    *df* must have a ``delta`` column (dollar change in annual bill) and a
    weight column. Quadrant boundaries are fixed at +/- $1,000, matching the
    savings/loss framing used throughout the rate-case reports.
    """
    import polars as pl

    total = cast(float, df[weight_col].sum())
    return {
        "savings > $1k": cast(float, df.filter(pl.col("delta") < -1000)[weight_col].sum()) / total * 100,
        "savings $0-1k": cast(
            float,
            df.filter((pl.col("delta") >= -1000) & (pl.col("delta") < 0))[weight_col].sum(),
        )
        / total
        * 100,
        "losses $0-1k": cast(
            float,
            df.filter((pl.col("delta") >= 0) & (pl.col("delta") < 1000))[weight_col].sum(),
        )
        / total
        * 100,
        "losses > $1k": cast(float, df.filter(pl.col("delta") >= 1000)[weight_col].sum()) / total * 100,
    }


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
    for group in avail_heating:
        pct = quadrant_pcts(delta.filter(pl.col("heating_label") == group))
        for q in QUADRANT_ORDER:
            records.append({"heating_label": group, "quadrant": q, "pct": pct[q]})

    plot_df = pl.DataFrame(records).with_columns(
        pl.col("heating_label").cast(pl.Enum(list(reversed(avail_heating)))),
        pl.col("quadrant").cast(pl.Enum(QUADRANT_ORDER)),
    )

    return (
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
        + plt.scale_y_continuous(expand=(0, 0, 0.02, 0))
        + plt.coord_flip()
        + plt.guides(fill=False)
        + plt.labs(
            x="",
            y="% of weighted households",
            title=f"Change in total annual energy bill after switching to a heat pump, under the {rate_name}",
        )
        + theme_switchbox()
        + plt.theme(figure_size=(10.5, max(3.5, 1.0 + 1.4 * len(avail_heating))))
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
