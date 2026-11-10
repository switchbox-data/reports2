"""Build marginal-cost 8760s with a chosen share of cost in winter.

The distribution and bulk transmission marginal costs that CAIRO uses for BGE
come from one allocation rule: take the top N hours of the utility's load and
give each hour ``load_h / sum(top-N load)`` of the annual ``$/kW-yr``
(``calculate_pop_weights`` in rate-design-platform's
``generate_utility_tx_dx_mc.py``, ``allocate_pcaf`` in ``bulk_tx_pjm.py``).
This module rebuilds that rule and adds a seasonal split, so a sensitivity can
move a chosen share of the cost into winter without rerunning CAIRO: a home's
marginal cost is its hourly load times the 8760, summed, and bills don't
change.

Two splits:

- ``split="cost"`` (the customer-weighted feeder mix): winter carries
  ``x * C`` on the top N winter load hours and summer ``(1 - x) * C`` on the
  top N summer load hours, each load-weighted within its season. The profile
  is ``x * W + (1 - x) * S``, so a home's cost is linear in ``x`` and the
  winter dollar share is exactly ``x``.
- ``split="hours"``: ``round(x * N)`` top winter hours plus the rest from
  summer, load-weighted together. Winter cost lands on fewer, colder hours.

Only top-N allocations can be reshaped this way. Month-hour and KDE
probability-of-peak profiles (Connecticut's defaults) spread cost over about
2,000 hours and have no fixed N.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from datetime import datetime, timedelta
from typing import Literal

import polars as pl

WINTER_MONTHS: tuple[int, ...] = (10, 11, 12, 1, 2, 3, 4)
PJM_HOURLY_DEMAND_S3_BASE = "s3://data.sb/pjm/hourly_demand/utilities/"

Split = Literal["cost", "hours"]


def cairo_8760_timestamps(year: int) -> pl.Series:
    """Naive Eastern hourly timestamps for ``year``, 8760 rows.

    Matches CAIRO's grid: a leap year drops Dec 31 rather than Feb 29.
    """
    start = datetime(year, 1, 1)
    n_hours = 8784 if _is_leap(year) else 8760
    stamps = [start + timedelta(hours=h) for h in range(n_hours)]
    if _is_leap(year):
        stamps = [t for t in stamps if not (t.month == 12 and t.day == 31)]
    return pl.Series("timestamp", stamps, dtype=pl.Datetime("us"))


def _is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def load_pjm_allocation_load(
    utility: str,
    load_year: int,
    output_year: int,
    *,
    s3_base: str = PJM_HOURLY_DEMAND_S3_BASE,
    storage_options: dict[str, str] | None = None,
) -> pl.DataFrame:
    """PJM utility hourly load for ``load_year``, stamped onto ``output_year``.

    Timestamps are converted to naive Eastern wall clock, DST fall-back
    duplicates are averaged, and gaps are interpolated. A ``load_year`` other
    than ``output_year`` is placed onto the output calendar by date: Feb 29 is
    dropped from a leap load year, and every remaining hour keeps its month,
    day and hour. That is how ``representative_home.qmd`` stamps BGE's 2024
    hourly data onto 2025, so a 2024 allocation load and the home's 2024 loads
    line up day for day. With ``load_year == output_year`` the result equals
    the load the rate-design-platform generators allocate on.

    Returns 8760 rows: ``timestamp`` (naive, output year) and ``load_mw``.
    """
    raw = (
        pl.scan_parquet(
            s3_base.rstrip("/") + "/",
            hive_partitioning=True,
            storage_options=storage_options or {"aws_region": "us-west-2"},
        )
        .filter(pl.col("utility") == utility, pl.col("year") == load_year)
        .select("timestamp", "load_mw")
        .collect()
    )
    if raw.is_empty():
        raise FileNotFoundError(f"No PJM load for utility={utility}, year={load_year} under {s3_base}")

    ts_dtype = raw.schema["timestamp"]
    if isinstance(ts_dtype, pl.Datetime) and ts_dtype.time_zone is not None:
        raw = raw.with_columns(pl.col("timestamp").dt.convert_time_zone("America/New_York").dt.replace_time_zone(None))
    raw = (
        raw.with_columns(pl.col("timestamp").cast(pl.Datetime("us")))
        .filter(pl.col("timestamp").dt.year() == load_year)
        .group_by("timestamp")
        .agg(pl.col("load_mw").mean())
    )

    start = datetime(load_year, 1, 1)
    n_hours = 8784 if _is_leap(load_year) else 8760
    grid = [start + timedelta(hours=h) for h in range(n_hours)]
    if load_year == output_year:
        load_grid = cairo_8760_timestamps(load_year)
    else:
        load_grid = pl.Series(
            "timestamp",
            [t for t in grid if not (t.month == 2 and t.day == 29)],
            dtype=pl.Datetime("us"),
        )
    aligned = (
        pl.DataFrame({"timestamp": load_grid})
        .join(raw, on="timestamp", how="left")
        .sort("timestamp")
        .with_columns(pl.col("load_mw").interpolate().forward_fill().backward_fill())
    )
    if aligned.height != 8760:
        raise ValueError(f"Expected 8760 load hours, got {aligned.height}")
    return aligned.with_columns(timestamp=cairo_8760_timestamps(output_year))


def _top_n_weights(
    load: pl.DataFrame,
    n_hours: int,
    *,
    months: Sequence[int] | None,
    load_col: str = "load_mw",
) -> pl.Series:
    """Load-share weights on the top ``n_hours`` hours, optionally within ``months``.

    Weights sum to 1; every other hour is 0. Ties in load are broken by
    timestamp so the selection is deterministic.
    """
    eligible = load.with_row_index("_row")
    if months is not None:
        eligible = eligible.filter(pl.col("timestamp").dt.month().is_in(list(months)))
    if eligible.height < n_hours:
        raise ValueError(f"Only {eligible.height} eligible hours, need n_hours={n_hours}")
    top = eligible.sort([load_col, "timestamp"], descending=[True, False]).head(n_hours)
    total = float(top[load_col].sum())
    if total <= 0:
        raise ValueError("Total load across the selected hours must be positive")
    weights = [0.0] * load.height
    for row, value in zip(top["_row"].to_list(), top[load_col].to_list(), strict=True):
        weights[row] = value / total
    return pl.Series("weight", weights, dtype=pl.Float64)


def build_seasonal_split_mc_8760(
    load: pl.DataFrame,
    annual_cost_kw_yr: float,
    n_hours: int,
    winter_share: float | None,
    *,
    split: Split = "cost",
    winter_months: Sequence[int] = WINTER_MONTHS,
    winter_rank_load: pl.DataFrame | None = None,
    value_col: str = "mc_per_kwh",
) -> pl.DataFrame:
    """8760 marginal cost (``$/kWh``) with share ``winter_share`` of cost in winter.

    Args:
        load: 8760 rows of ``timestamp`` and ``load_mw``; ranks and weights hours.
        annual_cost_kw_yr: Annual cost the 8760 sums to (``$/kW-yr``).
        n_hours: N, the number of cost hours (per season for ``split="cost"``).
        winter_share: x in [0, 1]. ``None`` selects the plain top N of the
            year, reproducing today's generators.
        split: ``"cost"`` puts ``x`` of the dollars on each season's own top
            N hours; ``"hours"`` puts ``round(x * N)`` of one set of N hours in
            winter, load-weighted together.
        winter_months: Months counted as winter (default October to April).
        winter_rank_load: Optional 8760 (``timestamp``, ``load_mw``) used to
            rank and weight winter hours instead of ``load``, e.g. a heating
            class shape. Only for ``split="cost"``, where each season is
            normalized within itself.
        value_col: Name of the output cost column.

    Returns:
        8760 rows of ``timestamp`` and ``value_col``, summing to
        ``annual_cost_kw_yr``.
    """
    if load.height != 8760:
        raise ValueError(f"load must have 8760 rows, got {load.height}")
    if n_hours < 1:
        raise ValueError("n_hours must be at least 1")
    summer_months = [m for m in range(1, 13) if m not in set(winter_months)]

    if winter_share is None:
        if winter_rank_load is not None:
            raise ValueError("winter_rank_load needs a winter_share")
        weights = _top_n_weights(load, n_hours, months=None)
    elif not 0.0 <= winter_share <= 1.0:
        raise ValueError(f"winter_share must be in [0, 1], got {winter_share}")
    elif split == "cost":
        rank = load if winter_rank_load is None else winter_rank_load
        if rank.height != 8760 or not rank["timestamp"].equals(load["timestamp"]):
            raise ValueError("winter_rank_load must share load's 8760 timestamps")
        winter = _top_n_weights(rank, n_hours, months=winter_months)
        summer = _top_n_weights(load, n_hours, months=summer_months)
        weights = winter_share * winter + (1.0 - winter_share) * summer
    elif split == "hours":
        if winter_rank_load is not None:
            raise ValueError('winter_rank_load is only supported with split="cost"')
        n_winter = round(winter_share * n_hours)
        selected = pl.Series("weight", [0.0] * 8760, dtype=pl.Float64)
        if n_winter > 0:
            selected = selected + (_top_n_weights(load, n_winter, months=winter_months) > 0).cast(pl.Float64)
        if n_hours - n_winter > 0:
            selected = selected + (_top_n_weights(load, n_hours - n_winter, months=summer_months) > 0).cast(pl.Float64)
        weighted_load = load["load_mw"] * selected
        weights = weighted_load / float(weighted_load.sum())
    else:
        raise ValueError(f'split must be "cost" or "hours", got {split!r}')

    return pl.DataFrame({"timestamp": load["timestamp"], value_col: weights * annual_cost_kw_yr})


def winter_cost_share(
    profile: pl.DataFrame,
    value_col: str,
    winter_months: Sequence[int] = WINTER_MONTHS,
) -> float:
    """Share of a profile's annual cost that falls in ``winter_months``."""
    total = float(profile[value_col].sum())
    winter = float(profile.filter(pl.col("timestamp").dt.month().is_in(list(winter_months)))[value_col].sum())
    return winter / total if total else 0.0


def build_seasonal_split_mc_grid(
    load: pl.DataFrame,
    annual_cost_kw_yr: float,
    n_hours: int,
    winter_shares: Iterable[float],
    *,
    split: Split = "cost",
    winter_months: Sequence[int] = WINTER_MONTHS,
    value_col: str = "mc_per_kwh",
) -> pl.DataFrame:
    """Long frame of seasonal-split 8760s, one block per ``winter_share``.

    Columns: ``winter_share``, ``n_hours``, ``split``, ``timestamp``,
    ``value_col``.
    """
    frames = [
        build_seasonal_split_mc_8760(
            load,
            annual_cost_kw_yr,
            n_hours,
            share,
            split=split,
            winter_months=winter_months,
            value_col=value_col,
        ).with_columns(
            pl.lit(share).alias("winter_share"),
            pl.lit(n_hours).alias("n_hours"),
            pl.lit(split).alias("split"),
        )
        for share in winter_shares
    ]
    return pl.concat(frames).select("winter_share", "n_hours", "split", "timestamp", value_col)
