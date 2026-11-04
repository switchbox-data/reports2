"""Two-block seasonal energy rates, and the bill change from personalizing the block threshold.

A two-block month charges ``r1`` up to ``threshold_kwh`` and ``r2`` above it. Personalizing
moves that threshold from the tariff's filed value (700 kWh on CT Eversource Rate 6) to the
home's own pre-retrofit usage in that month. For one month, with pre-retrofit kWh ``B`` and
post-retrofit kWh ``A``:

- filed threshold: ``r1 * min(A, T) + r2 * max(A - T, 0)``
- personalized threshold: ``r1 * min(A, B) + r2 * max(A - B, 0)``

The difference is ``(r2 - r1) * [max(A - B, 0) - max(A - T, 0)]``. Months with one block,
the fixed charge, and any rider that does not differ between blocks contribute zero.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal, cast

import polars as pl

from lib.rates_analysis.rate_case_funcs import MONTH_ORDER


def month_block_rates(tariff: Mapping[str, Any]) -> pl.DataFrame:
    """One row per calendar month: Block 1 rate, Block 2 rate, and the kWh threshold between them.

    ``r2`` and ``threshold_kwh`` are null in a single-block month. The weekday and weekend
    schedules must match, and each month's schedule must be flat across the 24 hours,
    because the row uses the first hour's period.
    """
    weekday = tariff["energyweekdayschedule"]
    weekend = tariff["energyweekendschedule"]
    if weekday != weekend:
        raise ValueError("month_block_rates requires the same weekday and weekend schedule")
    structure = tariff["energyratestructure"]
    rows: list[dict[str, object]] = []
    for index, schedule in enumerate(weekday):
        if len(set(schedule)) != 1:
            raise ValueError(f"{MONTH_ORDER[index]} varies by hour; month_block_rates needs an hour-flat schedule")
        tiers = structure[int(schedule[0])]
        if len(tiers) > 2:
            raise ValueError(f"{MONTH_ORDER[index]} has {len(tiers)} energy tiers; expected one or two")
        two_blocks = len(tiers) == 2
        if two_blocks and "max" not in tiers[0]:
            raise ValueError(f"{MONTH_ORDER[index]} Block 1 has no kWh max")
        rows.append(
            {
                "month": MONTH_ORDER[index],
                "r1": float(tiers[0]["rate"]),
                "r2": float(tiers[1]["rate"]) if two_blocks else None,
                "threshold_kwh": float(tiers[0]["max"]) if two_blocks else None,
            }
        )
    return pl.DataFrame(rows).with_columns(pl.col("r2").cast(pl.Float64), pl.col("threshold_kwh").cast(pl.Float64))


def personalized_block_adjustment(monthly_kwh: pl.DataFrame | pl.LazyFrame, rates: pl.DataFrame) -> pl.DataFrame:
    """Per building-month dollar change from moving the threshold to pre-retrofit kWh.

    ``monthly_kwh`` has ``bldg_id``, ``month``, ``kwh_before``, and ``kwh_after``. Only
    months with two blocks are returned. The adjustment is negative when personalizing
    lowers the bill.
    """
    required = {"bldg_id", "month", "kwh_before", "kwh_after"}
    missing = required - set(monthly_kwh.collect_schema().names())
    if missing:
        raise ValueError(f"monthly_kwh is missing columns: {sorted(missing)}")
    kwh = monthly_kwh.lazy() if isinstance(monthly_kwh, pl.DataFrame) else monthly_kwh
    winter = rates.filter(pl.col("r2").is_not_null())
    return cast(
        pl.DataFrame,
        (
            kwh.join(winter.lazy(), on="month", how="inner")
            .with_columns(
                (
                    (pl.col("r2") - pl.col("r1"))
                    * (
                        (pl.col("kwh_after") - pl.col("kwh_before")).clip(lower_bound=0)
                        - (pl.col("kwh_after") - pl.col("threshold_kwh")).clip(lower_bound=0)
                    )
                ).alias("adjustment")
            )
            .select("bldg_id", "month", "adjustment")
            .collect()
        ),
    )


def add_adjustment(
    frame: pl.DataFrame,
    adjustment: pl.DataFrame,
    columns: Sequence[str],
    *,
    how: Literal["inner", "left"] = "inner",
) -> pl.DataFrame:
    """Add a per-building ``adjustment`` column onto each named column of ``frame``.

    An inner join requires every building in ``frame`` to have an adjustment. A left
    join treats a missing building as zero, which is the right join for a season whose
    months have no second block.
    """
    joined = frame.join(adjustment.select("bldg_id", "adjustment"), on="bldg_id", how=how)
    if joined.height != frame.height:
        raise ValueError(f"adjustment join changed the row count: {frame.height} -> {joined.height}")
    return (
        joined.with_columns(pl.col("adjustment").fill_null(0.0))
        .with_columns([(pl.col(column) + pl.col("adjustment")).alias(column) for column in columns])
        .drop("adjustment")
    )
