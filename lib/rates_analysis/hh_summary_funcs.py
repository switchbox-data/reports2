"""Household-level base table: ResStock metadata + LMI eligibility, by building.

Builds the per-building dataset ``hh_summary_by_heating_type``-style notebooks
summarize: the heating/fuel attributes CAIRO's post-processing already carries
onto every master-bills row (see rate-design-platform's
``utils/post/master_metadata.py`` ``ATTR_COLS``), the three
``in.hvac_cooling_*`` equipment columns, income (banded + representative),
federal poverty level, and the ``is_lmi_any`` flag joined in from CAIRO's
master bills table.

Every function is parameterized by ``state``, ``batch``, ``resstock_release``,
and an optional ``utility`` filter (never hardcoded to one state or utility)
so any ``<state>_hp_rates`` report can reuse this module for any utility --
same convention as ``ncp_funcs.py`` and ``cos_funcs.py``. ResStock metadata
carries no utility assignment of its own; when *utility* is given, functions
restrict to that utility's buildings via a semi-join against
``utility_assignment.parquet`` (``scan_utility_bldg_ids()``).

Two summary aggregations are built on top of the base table so far:
``cooling_coverage_share_by_heating_type()`` (weighted cooling-coverage mix per
baseline heating type) and ``bill_delta_direction_by_cooling_coverage()``
(weighted bill-increase/decrease shares per cooling-coverage level, given a
``rate_case_funcs.bill_delta_between_segments()`` result) -- each with a
matching ``plot_*()`` function.
"""

from __future__ import annotations

from typing import cast

import polars as pl

METADATA_UPGRADE = "00"

# Attributes CAIRO's post-processing already carries onto every master-bills/BAT
# row (rate-design-platform's utils/post/master_metadata.py ATTR_COLS) -- keeping
# this table consistent with what every other <state>_hp_rates notebook joins.
MASTER_BILLS_ATTR_COLS = [
    "postprocess_group.has_hp",
    "postprocess_group.heating_type_v2",
    "heats_with_electricity",
    "heats_with_natgas",
    "heats_with_oil",
    "heats_with_propane",
    "in.representative_income",
    "in.hvac_cooling_partial_space_conditioning",
]

# The three in.hvac_cooling_* equipment columns (device type, efficiency, and
# fraction of floor area conditioned) -- excludes the separate
# in.cooling_setpoint* thermostat-schedule/offset columns, which describe
# occupant behavior rather than the cooling system itself.
COOLING_COLS = [
    "in.hvac_cooling_type",
    "in.hvac_cooling_efficiency",
    "in.hvac_cooling_partial_space_conditioning",
]

# in.income is ResStock's raw banded household income; in.representative_income
# (already in MASTER_BILLS_ATTR_COLS) is the SB-added continuous 2019-USD figure
# used for burden calculations elsewhere in these reports. Both are kept here.
INCOME_COLS = ["in.income", "in.representative_income"]

FPL_COL = "in.federal_poverty_level"

# Deduped union of the above, used as the default column set for
# load_household_metadata(). Order-preserving dedup so column order in the
# resulting DataFrame is stable and readable.
HH_SUMMARY_COLS = list(dict.fromkeys([*MASTER_BILLS_ATTR_COLS, *COOLING_COLS, *INCOME_COLS, FPL_COL]))

# Bottom-to-top stacking order for a stacked bar of cooling coverage: plotnine's
# geom_col (stacked) draws the *first* Enum level on top and the *last* at the
# bottom (see reports2/AGENTS.md's plotnine pitfalls), so listing "100% Conditioned"
# first puts full coverage at the top of the bar and "None" at the bottom.
COOLING_COVERAGE_ORDER = [
    "100% Conditioned",
    "80% Conditioned",
    "60% Conditioned",
    "40% Conditioned",
    "20% Conditioned",
    "<10% Conditioned",
    "None",
]
COOLING_COVERAGE_LABELS = {
    "100% Conditioned": "100%",
    "80% Conditioned": "80%",
    "60% Conditioned": "60%",
    "40% Conditioned": "40%",
    "20% Conditioned": "20%",
    "<10% Conditioned": "<10%",
    "None": "No cooling",
}

# Heating-type display labels/order are *not* redefined here -- they're imported
# from lib.rates_analysis.rate_case_funcs (HEATING_TYPE_LABELS/HEATING_ORDER),
# the same lookup reports/md_hp_rates/notebooks/analysis.qmd uses, so this module's
# charts stay in sync with every other heating-type breakdown in the report. Those
# codes (``natgas``, ``delivered_fuels``, ``electrical_resistance``, ``heat_pump``,
# ``other``) come from ``postprocess_group.heating_type_v2``, which has no null rows.


def resstock_metadata_path(resstock_release: str, state: str, upgrade: str = METADATA_UPGRADE) -> str:
    """Path to a state's ``metadata-sb.parquet`` -- local EBS mirror if present, else S3.

    Mirrors the local-disk-first pattern in ``ncp_cos.qmd``'s ``PATH_RESSTOCK_RELEASE``:
    on devcontainers/EC2 with a local ResStock mirror, reading from disk avoids S3 GET
    overhead; otherwise falls back to the canonical S3 path.
    """
    from pathlib import Path

    local = Path(
        f"/ebs/data/nrel/resstock/{resstock_release}/metadata/state={state}/upgrade={upgrade}/metadata-sb.parquet"
    )
    if local.exists():
        return str(local)
    return f"s3://data.sb/nrel/resstock/{resstock_release}/metadata/state={state}/upgrade={upgrade}/metadata-sb.parquet"


def utility_assignment_path(resstock_release: str, state: str) -> str:
    """Path to a state's ``utility_assignment.parquet`` -- local EBS mirror if present, else S3.

    Same local-disk-first pattern as ``resstock_metadata_path()``. This file
    (not ``metadata-sb.parquet``) is the source of ``sb.electric_utility`` --
    ResStock metadata itself carries no utility assignment (see
    rate-design-platform's ``utils/post/master_metadata.py``).
    """
    from pathlib import Path

    local = Path(
        f"/ebs/data/nrel/resstock/{resstock_release}/metadata_utility/state={state}/utility_assignment.parquet"
    )
    if local.exists():
        return str(local)
    return f"s3://data.sb/nrel/resstock/{resstock_release}/metadata_utility/state={state}/utility_assignment.parquet"


def scan_utility_bldg_ids(resstock_release: str, state: str, utility: str) -> pl.LazyFrame:
    """Scan ``bldg_id`` for buildings assigned to one electric utility.

    Meant to be used as a semi-join filter (``.join(..., on="bldg_id", how="semi")``)
    against ``metadata-sb.parquet`` reads, which carry no utility column of their own.
    """
    import polars as pl

    path = utility_assignment_path(resstock_release, state)
    return pl.scan_parquet(path).filter(pl.col("sb.electric_utility") == utility).select("bldg_id")


def scan_cooling_columns(
    resstock_release: str,
    state: str,
    upgrade: str = METADATA_UPGRADE,
    utility: str | None = None,
) -> pl.LazyFrame:
    """Scan ``bldg_id`` + the three ``in.hvac_cooling_*`` columns, for exploring their distinct values.

    Intended for a notebook's first look at the cooling columns (e.g.
    ``.collect()`` then ``.get_column(col).value_counts()`` per column) before
    committing to them as part of a larger household summary table.

    When *utility* is set, restricts to that utility's buildings via a
    semi-join against ``utility_assignment.parquet`` (``scan_utility_bldg_ids()``).
    """
    import polars as pl

    path = resstock_metadata_path(resstock_release, state, upgrade)
    lf = pl.scan_parquet(path).select("bldg_id", *COOLING_COLS)
    if utility is not None:
        lf = lf.join(scan_utility_bldg_ids(resstock_release, state, utility), on="bldg_id", how="semi")
    return lf


def load_household_metadata(
    resstock_release: str,
    state: str,
    upgrade: str = METADATA_UPGRADE,
    columns: list[str] | None = None,
    utility: str | None = None,
) -> pl.DataFrame:
    """Load upgrade-00 ``metadata-sb.parquet``: ``bldg_id``, ``weight``, + the household-summary columns.

    *columns* defaults to ``HH_SUMMARY_COLS`` (master-bills attributes + the
    cooling trio + income + FPL). Pass a custom list to select a different
    subset -- ``bldg_id`` and ``weight`` are always included.

    When *utility* is set, restricts to that utility's buildings via a
    semi-join against ``utility_assignment.parquet`` (``scan_utility_bldg_ids()``)
    -- ``metadata-sb.parquet`` itself carries no utility column.
    """
    import polars as pl

    cols = columns if columns is not None else HH_SUMMARY_COLS
    path = resstock_metadata_path(resstock_release, state, upgrade)
    lf = pl.scan_parquet(path).select("bldg_id", "weight", *cols)
    if utility is not None:
        lf = lf.join(scan_utility_bldg_ids(resstock_release, state, utility), on="bldg_id", how="semi")
    return cast("pl.DataFrame", lf.collect())


def join_lmi_flag(
    metadata: pl.DataFrame,
    state: str,
    batch: str,
    scenario: str,
    stage: str = "precalc",
) -> pl.DataFrame:
    """Left-join ``is_lmi_any`` from CAIRO's master bills onto a per-building metadata table.

    ``is_lmi_any`` (LMI program eligibility) is a post-processing attribute
    computed onto the master bills table, not raw ResStock metadata (see
    rate-design-platform's ``utils/post/apply_ny_lmi_to_master_bills.py``), so
    it has to be joined in from ``load_master_bills`` rather than read
    directly off ``metadata-sb.parquet``. Reads the ``"Annual"`` row of
    ``{scenario}_{stage}`` -- baseline attributes are identical across
    segments for the same population (see ``rate_case_funcs`` module
    docstring), so any segment's ``default``/precalc pairing works.
    """
    import polars as pl

    from lib.rates_analysis.rate_case_funcs import load_master_bills, segment_name

    segment = segment_name(scenario, stage)
    lmi = cast(
        "pl.DataFrame",
        load_master_bills(state, batch, segment)
        .filter(pl.col("month") == "Annual")
        .select("bldg_id", "is_lmi_any")
        .unique()
        .collect(),
    )
    return metadata.join(lmi, on="bldg_id", how="left")


def load_household_summary_base(
    resstock_release: str,
    state: str,
    batch: str,
    scenario: str,
    upgrade: str = METADATA_UPGRADE,
    stage: str = "precalc",
    columns: list[str] | None = None,
    utility: str | None = None,
) -> pl.DataFrame:
    """Full pipeline: ResStock metadata + ``is_lmi_any``, one row per building.

    The main entrypoint template notebooks (e.g.
    ``hh_summary_by_heating_type.qmd``) call: combines
    ``load_household_metadata()`` and ``join_lmi_flag()`` so a notebook can
    build the whole base table in one call, parameterized by
    state/batch/release.

    When *utility* is set (e.g. ``"bge"``), restricts to that utility's
    buildings -- see ``load_household_metadata()``.
    """
    metadata = load_household_metadata(resstock_release, state, upgrade, columns, utility)
    return join_lmi_flag(metadata, state, batch, scenario, stage)


def cooling_coverage_share_by_heating_type(
    hh_base: pl.DataFrame,
    weight_col: str = "weight",
    heating_col: str = "postprocess_group.heating_type_v2",
    cooling_col: str = "in.hvac_cooling_partial_space_conditioning",
) -> pl.DataFrame:
    """Weighted share of each cooling-coverage level within each heating type.

    Drops buildings with a null *heating_col* (defensive -- ``heating_type_v2`` has
    no null rows in practice, unlike the older ``heating_type``) before aggregating.
    Maps *heating_col*'s codes (``natgas``, ``delivered_fuels``, ``electrical_resistance``,
    ``heat_pump``, ``other``) to the same human-readable labels/order
    ``analysis.qmd`` uses (``rate_case_funcs.add_heating_label``/``HEATING_ORDER``),
    so this chart's categories read the same way as every other heating-type
    breakdown in the report.

    Returns one row per (heating type, cooling coverage) pair with a ``share``
    column that sums to 1 *within* each heating type -- not across the whole
    table -- so it's ready to feed straight into
    ``plot_cooling_coverage_by_heating_type()`` as a stacked-bar input. Renames
    *cooling_col* to plain ``cooling_coverage`` (dots in column names don't play
    well with plotnine's ``aes()`` string parsing).
    """
    from lib.rates_analysis.rate_case_funcs import HEATING_ORDER, add_heating_label

    labeled = add_heating_label(hh_base.filter(pl.col(heating_col).is_not_null()), code_col=heating_col)
    heating_order = [h for h in HEATING_ORDER if h in labeled["heating_label"].unique().to_list()]

    return (
        labeled.group_by(["heating_label", cooling_col])
        .agg(pl.col(weight_col).sum().alias("weighted_n"))
        .with_columns((pl.col("weighted_n") / pl.col("weighted_n").sum().over("heating_label")).alias("share"))
        .select(
            pl.col("heating_label").cast(pl.Enum(heating_order)).alias("heating_type"),
            pl.col(cooling_col).cast(pl.Enum(COOLING_COVERAGE_ORDER)).alias("cooling_coverage"),
            "share",
        )
        .sort("heating_type", "cooling_coverage")
    )


def plot_cooling_coverage_by_heating_type(share_df: pl.DataFrame, label_min_share: float = 0.03) -> object:
    """Stacked bar chart: cooling-coverage share within each baseline heating type.

    *share_df* is the output of ``cooling_coverage_share_by_heating_type()`` --
    proportions, not counts, so bars are directly comparable across heating types
    regardless of how many buildings are in each. ``heating_type`` already carries
    ``rate_case_funcs.HEATING_TYPE_LABELS``' human-readable labels (e.g. "Natural
    gas"), in ``HEATING_ORDER``'s order, so the x-axis needs no relabeling here.
    Segments use a single-hue sequential scale (light = full cooling coverage, dark
    = none), reading top-to-bottom as coverage decreases. In-bar percentage labels
    are omitted for segments under *label_min_share* so small slivers don't overlap.
    """
    import matplotlib.colors as mcolors
    import polars as pl
    from plotnine import (
        aes,
        geom_col,
        geom_text,
        ggplot,
        labs,
        position_stack,
        scale_fill_manual,
        scale_y_continuous,
        theme,
    )

    from lib.plotnine import SB_COLORS, theme_switchbox

    cmap = mcolors.LinearSegmentedColormap.from_list("cooling_coverage", [SB_COLORS["sky"], SB_COLORS["midnight"]])
    n = len(COOLING_COVERAGE_ORDER)
    color_map = {cat: mcolors.to_hex(cmap(i / (n - 1))) for i, cat in enumerate(COOLING_COVERAGE_ORDER)}

    label_df = share_df.filter(pl.col("share") >= label_min_share)

    return (
        ggplot(share_df, aes(x="heating_type", y="share", fill="cooling_coverage"))
        + geom_col(position=position_stack())
        + geom_text(
            mapping=aes(label="share * 100"),
            data=label_df,
            position=position_stack(vjust=0.5),
            format_string="{:.0f}%",
            size=9,
            color="white",
            fontweight="bold",
        )
        + scale_fill_manual(
            values=color_map,
            breaks=COOLING_COVERAGE_ORDER,
            labels=[COOLING_COVERAGE_LABELS[cat] for cat in COOLING_COVERAGE_ORDER],
        )
        + scale_y_continuous(labels=lambda ls: [f"{v:.0%}" for v in ls], expand=(0, 0, 0.02, 0))
        + labs(x="Baseline heating type", y="Share of homes", fill="Cooling coverage")
        + theme_switchbox()
        + theme(figure_size=(10.5, 5))
    )


def bill_delta_direction_by_cooling_coverage(
    hh_base: pl.DataFrame,
    delta_df: pl.DataFrame,
    cooling_col: str = "in.hvac_cooling_partial_space_conditioning",
    weight_col: str = "weight",
) -> pl.DataFrame:
    """Weighted share of bill increases vs. decreases within each cooling-coverage level.

    *delta_df* is a ``rate_case_funcs.bill_delta_between_segments()`` result (one row per
    building, with ``bldg_id``, *weight_col*, and ``delta``) -- typically already filtered to
    one baseline heating type (e.g. natural gas, the population actually facing a
    fuel-switching decision; see ``analysis.qmd``'s ``delta_natgas_default_to_flat``-style
    cells). *hh_base* supplies each building's cooling-coverage attribute via a ``bldg_id``
    join.

    Within each cooling-coverage category, runs ``rate_case_funcs.bill_change_incidence()``
    on that subgroup, so "increase"/"unchanged"/"decrease" is defined identically to every
    other bill-change stat in this report (weighted shares of ``delta > 0`` / ``== 0`` /
    ``< 0``). Returns one row per (cooling coverage, direction) triple with a ``share``
    column that sums to 1 *within* each cooling-coverage category -- ready to feed
    ``plot_bill_delta_direction_by_cooling_coverage()``.
    """
    from lib.rates_analysis.rate_case_funcs import bill_change_incidence

    joined = delta_df.join(hh_base.select("bldg_id", cooling_col), on="bldg_id", how="inner")
    coverage_order = [c for c in COOLING_COVERAGE_ORDER if c in joined[cooling_col].unique().to_list()]

    rows = []
    for category in coverage_order:
        incidence = bill_change_incidence(joined.filter(pl.col(cooling_col) == category), weight_col=weight_col)
        rows.append({"cooling_coverage": category, "direction": "increase", "share": incidence["pct_increase"]})
        rows.append({"cooling_coverage": category, "direction": "unchanged", "share": incidence["pct_unchanged"]})
        rows.append({"cooling_coverage": category, "direction": "decrease", "share": incidence["pct_decrease"]})

    return (
        pl.DataFrame(rows)
        .select(
            pl.col("cooling_coverage").cast(pl.Enum(coverage_order)),
            pl.col("direction").cast(pl.Enum(["increase", "unchanged", "decrease"])),
            "share",
        )
        .sort("cooling_coverage", "direction")
    )


def plot_bill_delta_direction_by_cooling_coverage(share_df: pl.DataFrame, label_min_share: float = 0.03) -> object:
    """Stacked bar chart: bill-increase vs. bill-decrease share within each cooling-coverage level.

    *share_df* is the output of ``bill_delta_direction_by_cooling_coverage()``. Bars are
    ordered the same as ``plot_cooling_coverage_by_heating_type()`` (full coverage to none,
    left to right) so the two charts read consistently together. "Bill increase" segments
    are warm-colored (carrot), "bill decrease" cool-colored (sky); the "no change" sliver
    (an exact tie in a continuous dollar figure, so vanishingly rare in practice) is light
    gray. In-bar percentage labels are omitted for segments under *label_min_share* so small
    slivers don't overlap.
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

    from lib.plotnine import SB_COLORS, theme_switchbox

    color_map = {
        "increase": SB_COLORS["carrot"],
        "unchanged": SB_COLORS["gray_light"],
        "decrease": SB_COLORS["sky"],
    }
    direction_labels = {"increase": "Bill increase", "unchanged": "No change", "decrease": "Bill decrease"}

    label_df = share_df.filter(pl.col("share") >= label_min_share)

    return (
        ggplot(share_df, aes(x="cooling_coverage", y="share", fill="direction"))
        + geom_col(position=position_stack())
        + geom_text(
            mapping=aes(label="share * 100"),
            data=label_df,
            position=position_stack(vjust=0.5),
            format_string="{:.0f}%",
            size=9,
            color="white",
            fontweight="bold",
        )
        + scale_fill_manual(
            values=color_map,
            breaks=list(color_map.keys()),
            labels=[direction_labels[k] for k in color_map],
        )
        # Full coverage-level names (e.g. "100% Conditioned") wrap/collide with 7 x categories
        # side by side; the short COOLING_COVERAGE_LABELS forms (e.g. "100%") fit on one line.
        + scale_x_discrete(labels=lambda cats: [COOLING_COVERAGE_LABELS.get(c, c) for c in cats])
        + scale_y_continuous(labels=lambda ls: [f"{v:.0%}" for v in ls], expand=(0, 0, 0.02, 0))
        + labs(x="Cooling coverage", y="Share of homes", fill="Bill change")
        + theme_switchbox()
        + theme(figure_size=(10.5, 5))
    )
