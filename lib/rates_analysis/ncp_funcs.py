"""Subclass non-coincident-peak (NCP) cost-causation helpers, shared across states/batches.

These reproduce the one piece of RI's `embedded_costs.qmd` that actually made
it into testimony (`reports/ri_hp_rates/expert_testimony.qmd:1202-1210`): for
each residential heating-type subclass, what share of a hypothetical
NCP-based cost allocation would that subclass receive, and when does its own
peak occur. Both are computed purely from ResStock hourly load curves --
no BGE/utility ECOSS dollar or NCP-kW-by-voltage-level data is required.

Every function is parameterized by ``state``, ``batch``, ``segment``, and
``utility`` (never hardcoded to one state) so the same code can be pointed at
a different state/utility/batch by changing the calling notebook's
parameters, not this module.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    import polars as pl

ELECTRIC_LOAD_COL = "out.electricity.total.energy_consumption"
ELECTRIC_PV_COL = "out.electricity.pv.energy_consumption"


def grid_consumption_expr(
    load_col: str = ELECTRIC_LOAD_COL,
    pv_col: str = ELECTRIC_PV_COL,
) -> pl.Expr:
    """Polars expression for ResStock "grid consumption", matching CAIRO's formula.

    ``grid_cons = max(total_load - abs(pv), 0)``. Replicated here from
    rate-design-platform's ``utils/loads.py`` -- reports2 has no dependency on
    that repo's Python package (only ``lib.rdp.fetch_rdp_file``, which fetches
    raw file *contents* for config files, not importable code) -- because it
    is the formula CAIRO actually bills against. RI's original
    ``embedded_costs.qmd`` summed ``out.electricity.net.energy_consumption``
    instead, which ``utils/loads.py`` documents as diverging from ``total``
    by up to ~10% even for non-solar buildings.
    """
    import polars as pl

    return (pl.col(load_col).cast(pl.Float64) - pl.col(pv_col).cast(pl.Float64).abs()).clip(lower_bound=0.0)


def load_subclass_population(
    state: str,
    batch: str,
    segment: str,
    utility: str,
) -> pl.LazyFrame:
    """Per-building heating-type-v2 subclass and weight for one utility.

    Filters CAIRO's master bills table (``rate_case_funcs.load_master_bills``)
    to one utility's buildings and the ``"Annual"`` row (one row per
    building), reusing CAIRO's own heating-type-v2 classification and utility
    assignment rather than re-deriving them from raw ResStock metadata --
    consistent with how other ``md_hp_rates`` notebooks (e.g. ``analysis.qmd``)
    source these fields, and avoids a ``buildstock_fetch`` dependency.

    Returns ``bldg_id``, ``postprocess_group.heating_type_v2``, ``weight``.
    """
    import polars as pl

    from lib.rates_analysis.rate_case_funcs import load_master_bills

    return (
        load_master_bills(state, batch, segment)
        .filter((pl.col("sb.electric_utility") == utility) & (pl.col("month") == "Annual"))
        .select("bldg_id", "postprocess_group.heating_type_v2", "weight")
    )


def scan_hourly_loads_for_buildings(
    path_resstock_release: str,
    state: str,
    upgrade: str,
    bldg_ids: list[int],
) -> pl.LazyFrame:
    """Scan raw ResStock hourly load curves for a specific list of buildings.

    Constructs per-building parquet paths directly and passes the list to
    ``scan_parquet``, rather than scanning the whole ``load_curve_hourly``
    hive partition and filtering -- the latter probes every file in the
    partition just to keep a handful of rows (see the "Parquet reads: local
    vs S3" guidance for a single utility's buildings).

    Returns ``bldg_id``, ``timestamp``, and ``grid_kwh`` (CAIRO-matching
    "grid consumption" -- see ``grid_consumption_expr()``).
    """
    import polars as pl

    base = path_resstock_release.rstrip("/")
    load_dir = f"{base}/load_curve_hourly/state={state}/upgrade={upgrade}"
    upgrade_int = str(int(upgrade))
    paths = [f"{load_dir}/{bldg_id}-{upgrade_int}.parquet" for bldg_id in bldg_ids]
    return pl.scan_parquet(paths).select(
        "bldg_id",
        "timestamp",
        grid_consumption_expr().alias("grid_kwh"),
    )


def validate_hourly_against_annual_kwh(
    computed_annual: pl.DataFrame,
    reference_annual: pl.LazyFrame | pl.DataFrame,
    *,
    computed_col: str = "computed_annual_kwh_grid",
    reference_col: str = "annual_kwh_grid",
    rel_tol: float = 0.02,
) -> pl.DataFrame:
    """Compare hourly-derived per-building annual grid kWh against CAIRO's own export.

    CAIRO can apply a uniform per-utility ``resstock_kwh_scale_factor`` to
    ResStock loads before billing them (see
    ``rate-design-platform/utils/pre/rev_requirement/README.md``), so the raw
    hourly sum computed here will not equal CAIRO's ``annual_kwh_grid`` 1:1
    even when methodology is fully aligned. Rather than hardcode that factor
    (which lives in a different repo's per-state/batch config and would break
    portability), this discovers it empirically: it takes the *median* of
    each building's ``reference / computed`` ratio across the population as
    the implied scale factor, then flags any building whose own ratio departs
    from that median by more than *rel_tol* -- a genuine per-building
    mismatch (e.g. ResStock's ``out.electricity.net``/``total`` calibration
    drift for that building), not just the expected uniform scaling. When no
    scale factor applies, the median ratio is simply ~1.0 and this reduces to
    a direct comparison.

    Warns (does not raise) if any buildings are flagged -- this is a
    data-quality check that should surface for the notebook reader, not
    silently block or silently pass.

    Returns the joined comparison frame (``bldg_id``, *computed_col*,
    *reference_col*, ``ratio``, ``rel_deviation``) either way, for display.
    """
    import warnings

    import polars as pl

    reference_lf = reference_annual if isinstance(reference_annual, pl.LazyFrame) else reference_annual.lazy()
    reference_df = cast("pl.DataFrame", reference_lf.select("bldg_id", reference_col).collect())

    joined = (
        computed_annual.select("bldg_id", computed_col)
        .join(reference_df, on="bldg_id", how="inner")
        .filter(pl.col(computed_col) > 0)
        .with_columns((pl.col(reference_col) / pl.col(computed_col)).alias("ratio"))
    )
    median_ratio = joined["ratio"].median()
    joined = joined.with_columns(
        ((pl.col("ratio") - median_ratio).abs() / median_ratio).alias("rel_deviation"),
    )

    mismatched = joined.filter(pl.col("rel_deviation") > rel_tol)
    if mismatched.height > 0:
        warnings.warn(
            f"{mismatched.height}/{joined.height} buildings' hourly-derived annual grid kWh "
            f"deviate more than {rel_tol:.0%} from the population's implied scale factor "
            f"(median ratio={median_ratio:.6f} = {reference_col}/{computed_col}, consistent "
            "with a uniform CAIRO resstock_kwh_scale_factor if not ~1.0). "
            f"Max deviation: {mismatched['rel_deviation'].max():.1%}. This likely reflects "
            "per-building ResStock out.electricity.net/total calibration drift for those "
            "buildings, not a bug in this notebook -- inspect the returned comparison frame.",
            stacklevel=2,
        )
    return joined


def aggregate_hourly_by_subclass(
    hourly_lf: pl.LazyFrame,
    population_lf: pl.LazyFrame | pl.DataFrame,
) -> pl.DataFrame:
    """Weighted hourly grid kWh aggregated by heating-type-v2 subclass.

    Joins hourly per-building ``grid_kwh`` to the subclass population
    (``weight``, ``postprocess_group.heating_type_v2``), then groups by
    ``(timestamp, heating_type_v2)`` to produce one row per subclass per hour:
    ``electricity_kwh`` (weighted sum) and ``num_homes`` (weight sum). Mirrors
    RI's ``aggregate_curves`` (``embedded_costs.qmd:475-484``).
    """
    import polars as pl

    population = population_lf if isinstance(population_lf, pl.LazyFrame) else population_lf.lazy()

    return cast(
        "pl.DataFrame",
        hourly_lf.join(population, on="bldg_id", how="inner")
        .group_by(["timestamp", "postprocess_group.heating_type_v2"])
        .agg(
            (pl.col("grid_kwh") * pl.col("weight")).sum().alias("electricity_kwh"),
            pl.col("weight").sum().alias("num_homes"),
        )
        .collect(),
    )


def compute_subclass_ncp_shares(
    aggregate_curves: pl.DataFrame,
    *,
    only_consider_summer_peaks: bool = False,
) -> pl.DataFrame:
    """Per-subclass share of a hypothetical non-coincident-peak (NCP) cost allocation.

    Faithful port of RI's ``compute_secondary_ncp_raw``
    (``embedded_costs.qmd:365-394``): for each heating-type-v2 subclass, take
    its own maximum hourly weighted load across the year (the "secondary
    NCP") and the timestamp at which it occurs, then divide by the sum of
    every subclass's own maximum to get that subclass's share of an NCP-based
    cost allocation. This is the basis of the "an NCP allocator conflates
    peak magnitude with peak timing" argument -- summer- and winter-peaking
    subclasses are compared on their own peaks, not a single coincident
    system peak.

    Also adds ``annual_kwh`` (each subclass's total weighted annual
    consumption) and ``num_homes_pct_of_total`` (each subclass's share of the
    population by weight), matching what RI's notebook computes downstream
    before pulling report variables.

    ``only_consider_summer_peaks=False`` (the default) matches the value RI
    actually used for its six reported variables (``embedded_costs.qmd:32``)
    -- RI also computed a summer-only variant for its own internal
    comparison, but never reported those numbers in testimony.
    """
    import polars as pl

    group_col = "postprocess_group.heating_type_v2"
    curves = aggregate_curves
    if only_consider_summer_peaks:
        curves = curves.filter(pl.col("timestamp").dt.month().is_in(range(5, 10)))

    ncp_by_subclass = curves.group_by(group_col).agg(
        pl.col("electricity_kwh").max().alias("secondary_ncp_raw"),
        pl.col("num_homes").max().alias("num_homes"),
        pl.col("timestamp").sort_by("electricity_kwh", descending=True).first().alias("ncp_timestamp"),
    )
    total_ncp = ncp_by_subclass["secondary_ncp_raw"].sum()
    ncp_by_subclass = ncp_by_subclass.with_columns(
        (pl.col("secondary_ncp_raw") / total_ncp * 100).alias("subclass_pct_of_class_share"),
    )

    annual_kwh_by_subclass = aggregate_curves.group_by(group_col).agg(
        pl.col("electricity_kwh").sum().alias("annual_kwh"),
    )
    ncp_by_subclass = ncp_by_subclass.join(annual_kwh_by_subclass, on=group_col, how="left")

    total_homes = ncp_by_subclass["num_homes"].sum()
    return ncp_by_subclass.with_columns(
        (pl.col("num_homes") / total_homes * 100).alias("num_homes_pct_of_total"),
    )


def subclass_ncp_report_vars(
    ncp_df: pl.DataFrame,
    *,
    group_col: str = "postprocess_group.heating_type_v2",
) -> dict:
    """Extract the six scalars RI's expert testimony actually uses.

    Pulls ``{hp,natgas}_pct_of_customers``, ``{hp,natgas}_ncp_share_pct``,
    ``{hp,natgas}_ncp_timestamp`` from a ``compute_subclass_ncp_shares()``
    result -- matching ``embedded_costs.qmd:777-782`` -- keyed off the same
    ``"heat_pump"``/``"natgas"`` heating-type-v2 codes used by
    ``rate_case_funcs.HEATING_TYPE_LABELS``.
    """
    import polars as pl

    def _row(code: str) -> dict:
        matches = ncp_df.filter(pl.col(group_col) == code)
        if matches.height != 1:
            raise ValueError(f"Expected exactly 1 row for {code!r}, got {matches.height}")
        return matches.to_dicts()[0]

    hp = _row("heat_pump")
    natgas = _row("natgas")
    return {
        "hp_pct_of_customers": hp["num_homes_pct_of_total"],
        "hp_ncp_share_pct": hp["subclass_pct_of_class_share"],
        "hp_ncp_timestamp": hp["ncp_timestamp"],
        "natgas_pct_of_customers": natgas["num_homes_pct_of_total"],
        "natgas_ncp_share_pct": natgas["subclass_pct_of_class_share"],
        "natgas_ncp_timestamp": natgas["ncp_timestamp"],
    }
