"""Cost-of-service helpers for incremental revenue vs. marginal-cost analysis.

These wrap ``rate_case_funcs.bat_component_delta()`` to compare each
building's delivery revenue and delivery marginal-cost allocation between
two ``{scenario}_{stage}`` segments (typically pre-retrofit ``*_precalc``
vs. post-retrofit ``*_calibrated``). The resulting ``delta_gap`` —
incremental revenue minus incremental marginal cost — says whether a heat
pump conversion is a net contributor or a net cost to the delivery system
under the rate design in those segments.

They also join in each building's incremental grid electricity consumption
(``rate_case_funcs.load_billing_kwh_annual()``) so revenue/marginal-cost
changes can be related to the kWh actually driving them — important because
not every heating type gains load: electric-resistance homes typically see
*less* grid consumption after switching to a heat pump (a much more
efficient electric appliance replacing a much less efficient one), while
combustion-heated homes see more (new electric load replacing gas/oil/
propane).

Every function is parameterized by ``state``, ``utility``, ``batch``, and
segment names (never hardcoded to one utility) so the same code works
across reports.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    import polars as pl


def bat_component_delta_with_gap(
    state: str,
    utility: str,
    batch: str,
    segment_before: str,
    segment_after: str,
    *,
    heating_type: str | None = None,
    revenue_col: str = "annual_bill_delivery",
    marginal_cost_col: str = "economic_burden_delivery",
    kwh_col: str = "annual_kwh_grid",
) -> pl.DataFrame:
    """Per-building delta of delivery revenue, marginal cost, and grid kWh, plus the revenue/MC gap.

    Calls ``rate_case_funcs.bat_component_delta()`` (filtered to *utility*)
    for *revenue_col* and *marginal_cost_col*, then adds ``delta_gap`` =
    ``delta_{revenue_col} - delta_{marginal_cost_col}``.

    Also loads CAIRO's raw per-building kWh export
    (``rate_case_funcs.load_billing_kwh_annual()``) at both *segment_before*
    and *segment_after*, and joins on ``bldg_id`` to add ``{kwh_col}_before``,
    ``{kwh_col}_after``, and ``delta_{kwh_col}`` — the incremental grid
    consumption driving each building's revenue/marginal-cost change.

    When *heating_type* is set, filters to that ``heating_type_v2`` code
    (e.g. ``"natgas"``). Baseline heat-pump buildings are already dropped
    by ``bat_component_delta`` (``exclude_has_hp=True``). Pass
    ``heating_type=None`` (the default) to keep all non-HP heating types in
    one frame and facet/group downstream instead of re-fetching per type.
    """
    import polars as pl

    from lib.rates_analysis.rate_case_funcs import bat_component_delta, load_billing_kwh_annual

    delta = bat_component_delta(
        state,
        batch,
        segment_before,
        segment_after,
        components=[revenue_col, marginal_cost_col],
        utility=utility,
    ).with_columns(
        (pl.col(f"delta_{revenue_col}") - pl.col(f"delta_{marginal_cost_col}")).alias("delta_gap"),
    )

    kwh_before = cast(
        "pl.DataFrame",
        load_billing_kwh_annual(state, utility, batch, segment_before)
        .select("bldg_id", pl.col(kwh_col).alias(f"{kwh_col}_before"))
        .collect(),
    )
    kwh_after = cast(
        "pl.DataFrame",
        load_billing_kwh_annual(state, utility, batch, segment_after)
        .select("bldg_id", pl.col(kwh_col).alias(f"{kwh_col}_after"))
        .collect(),
    )
    delta = (
        delta.join(kwh_before, on="bldg_id", how="inner", validate="1:1")
        .join(kwh_after, on="bldg_id", how="inner", validate="1:1")
        .with_columns(
            (pl.col(f"{kwh_col}_after") - pl.col(f"{kwh_col}_before")).alias(f"delta_{kwh_col}"),
        )
    )

    if heating_type is not None:
        delta = delta.filter(pl.col("heating_type_v2") == heating_type)
    return delta


def bat_component_summary_by_heating_type(
    bat_delta: pl.DataFrame,
    *,
    revenue_col: str = "annual_bill_delivery",
    marginal_cost_col: str = "economic_burden_delivery",
    kwh_col: str = "annual_kwh_grid",
    group_col: str = "heating_type_v2",
    weight_col: str = "weight",
) -> pl.DataFrame:
    """Weighted revenue/marginal-cost/kWh summary by baseline heating type.

    Takes a ``bat_component_delta_with_gap()`` result (all heating types in
    one frame) and summarizes it one row per *group_col* value, plus a
    trailing "All non-HP" total row.

    Precondition: *bat_delta* must already have baseline heat-pump buildings
    excluded (e.g. via ``bat_component_delta(exclude_has_hp=True)``, the
    default that ``bat_component_delta_with_gap()`` goes through) — this
    function trusts that exclusion for the "All non-HP" label rather than
    re-deriving it, and raises ``ValueError`` if any ``has_hp`` row slips
    through.

    Percent change and `$`-per-incremental-kWh are both **weighted-sum
    ratios** (``sum(weight * x) / sum(weight * y)``), not averages of each
    building's own ratio. A per-building ratio blows up for any building
    whose denominator (e.g. ``delta_{kwh_col}``) is near zero, which is
    common near the population's own mean; the weighted-sum ratio is the
    correct way to ask "in aggregate, how many incremental dollars per
    incremental kWh" for a group.

    Returns columns: ``heating_type`` (ordered by
    ``rate_case_funcs.HEATING_ORDER`` when *group_col* is the default
    heating-type column, with the label-mapped ``rate_case_funcs.HEATING_TYPE_LABELS``
    names), ``n_weighted``, ``avg_kwh_before``, ``avg_kwh_delta``, and for
    both revenue and marginal cost: ``{prefix}_avg_before``,
    ``{prefix}_avg_delta``, ``{prefix}_pct_change``,
    ``{prefix}_dollars_per_incremental_kwh`` (``prefix`` is ``revenue`` or
    ``mc``).
    """
    import polars as pl

    from lib.rates_analysis.rate_case_funcs import HEATING_ORDER, HEATING_TYPE_LABELS

    if bat_delta["has_hp"].any():
        n_hp = bat_delta["has_hp"].sum()
        raise ValueError(
            f"bat_component_summary_by_heating_type() assumes has_hp buildings were already "
            f"excluded upstream (see bat_component_delta(exclude_has_hp=True)); got {n_hp} rows "
            f"with has_hp=True."
        )

    revenue_before_col = f"{revenue_col}_before"
    revenue_delta_col = f"delta_{revenue_col}"
    mc_before_col = f"{marginal_cost_col}_before"
    mc_delta_col = f"delta_{marginal_cost_col}"
    kwh_before_col = f"{kwh_col}_before"
    kwh_delta_col = f"delta_{kwh_col}"

    weight = pl.col(weight_col)
    agg_exprs = [
        weight.sum().alias("n_weighted"),
        (weight * pl.col(kwh_before_col)).sum().alias("wsum_kwh_before"),
        (weight * pl.col(kwh_delta_col)).sum().alias("wsum_kwh_delta"),
        (weight * pl.col(revenue_before_col)).sum().alias("wsum_revenue_before"),
        (weight * pl.col(revenue_delta_col)).sum().alias("wsum_revenue_delta"),
        (weight * pl.col(mc_before_col)).sum().alias("wsum_mc_before"),
        (weight * pl.col(mc_delta_col)).sum().alias("wsum_mc_delta"),
    ]

    by_group = bat_delta.group_by(group_col).agg(*agg_exprs).rename({group_col: "heating_type"})
    total_row = bat_delta.select(*agg_exprs).with_columns(pl.lit("All non-HP").alias("heating_type"))
    combined = pl.concat([by_group, total_row.select(by_group.columns)], how="vertical")

    combined = combined.with_columns(
        (pl.col("wsum_kwh_before") / pl.col("n_weighted")).alias("avg_kwh_before"),
        (pl.col("wsum_kwh_delta") / pl.col("n_weighted")).alias("avg_kwh_delta"),
        (pl.col("wsum_revenue_before") / pl.col("n_weighted")).alias("revenue_avg_before"),
        (pl.col("wsum_revenue_delta") / pl.col("n_weighted")).alias("revenue_avg_delta"),
        (pl.col("wsum_revenue_delta") / pl.col("wsum_revenue_before")).alias("revenue_pct_change"),
        (pl.col("wsum_revenue_delta") / pl.col("wsum_kwh_delta")).alias("revenue_dollars_per_incremental_kwh"),
        (pl.col("wsum_mc_before") / pl.col("n_weighted")).alias("mc_avg_before"),
        (pl.col("wsum_mc_delta") / pl.col("n_weighted")).alias("mc_avg_delta"),
        (pl.col("wsum_mc_delta") / pl.col("wsum_mc_before")).alias("mc_pct_change"),
        (pl.col("wsum_mc_delta") / pl.col("wsum_kwh_delta")).alias("mc_dollars_per_incremental_kwh"),
    ).select(
        "heating_type",
        "n_weighted",
        "avg_kwh_before",
        "avg_kwh_delta",
        "revenue_avg_before",
        "revenue_avg_delta",
        "revenue_pct_change",
        "revenue_dollars_per_incremental_kwh",
        "mc_avg_before",
        "mc_avg_delta",
        "mc_pct_change",
        "mc_dollars_per_incremental_kwh",
    )

    if group_col == "heating_type_v2":
        combined = combined.with_columns(
            pl.col("heating_type").replace_strict(HEATING_TYPE_LABELS, default=pl.col("heating_type"))
        )
        row_order = [*(h for h in HEATING_ORDER if h in combined["heating_type"].to_list()), "All non-HP"]
    else:
        non_total = combined.filter(pl.col("heating_type") != "All non-HP")
        row_order = [*non_total["heating_type"].to_list(), "All non-HP"]

    return combined.with_columns(pl.col("heating_type").cast(pl.Enum(row_order))).sort("heating_type")
