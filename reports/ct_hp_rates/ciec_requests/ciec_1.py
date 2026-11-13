"""CIEC-1 helpers for the Rate HP revenue reduction.

The weighted monthly load and the monthly bill calculation already live in
``lib.rates_analysis.rate_case_funcs``. Percent text comes from
``lib.format.pct``. The functions here are the CIEC-1 steps those modules do
not cover: folding Rate 1 charges, applying the winter Rate HP rates, selecting
a heat-pump subclass, and scaling one customer's revenue reduction to the
enrollment bounds, a non-HP per-kWh increase, and the annual bill increase
that charge produces.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

import polars as pl

from lib.format import pct as format_pct
from lib.rates_analysis.hh_summary_funcs import resstock_metadata_path, scan_utility_bldg_ids
from lib.rates_analysis.rate_case_funcs import monthly_bill_from_profile, weighted_mean, weighted_quantile

RateSpec = dict[str, Any]


def dollar(x: float, accuracy: int = 0) -> str:
    """Dollar text for inline prose, e.g. ``1234.5`` -> ``"$1,234.50"``."""
    return f"${x:,.{accuracy}f}"


def num(x: float, accuracy: int = 0) -> str:
    """Number text with thousands separators."""
    return f"{x:,.{accuracy}f}"


def cents(x: float, accuracy: int = 4) -> str:
    """Cents per kWh. ``x`` is $/kWh, so ``0.001234`` -> ``"0.1234¢"``."""
    return f"{x * 100:,.{accuracy}f}¢"


def pct(x: float, accuracy: int = 2) -> str:
    """Percent text. Two decimals by default, unlike ``lib.format.pct``."""
    return format_pct(x, accuracy)


def money(x: float, accuracy: int) -> str:
    """Dollar text for a markdown table. The backslash keeps Quarto from treating it as math."""
    return f"\\${x:,.{accuracy}f}"


def sum_monthly_rates(*charges: Mapping[str, Any]) -> dict[str, float]:
    """Add ``monthly_rates`` across charge dicts, month by month."""
    result: dict[str, float] = {}
    for charge in charges:
        for month, rate in charge["monthly_rates"].items():
            result[month] = result.get(month, 0.0) + float(rate)
    return result


def with_winter_rates(
    rate_components: Mapping[str, RateSpec],
    dist: float,
    tx: float,
    winter_keys: Sequence[str],
) -> dict[str, RateSpec]:
    """Copy a rate schedule and replace winter distribution and transmission."""
    adjusted: dict[str, RateSpec] = {}
    for name, spec in rate_components.items():
        rates = dict(spec["monthly_rates"])
        if name == "Distribution":
            for month in winter_keys:
                rates[month] = dist
        elif name == "Transmission":
            for month in winter_keys:
                rates[month] = tx
        adjusted[name] = {"charge_unit": spec["charge_unit"], "monthly_rates": rates}
    return adjusted


def annual_bill(monthly_kwh: pl.DataFrame, rate_components: Mapping[str, RateSpec]) -> dict[str, float]:
    """Annual bill by component. ``Total`` is the sum of the components."""
    bills = monthly_bill_from_profile(monthly_kwh, dict(rate_components))
    totals = {
        row["component"]: float(row["value"])
        for row in bills.group_by("component").agg(pl.col("value").sum()).iter_rows(named=True)
    }
    totals["Total"] = sum(totals.values())
    return totals


def subclass_weights(
    release: str,
    state: str,
    utility: str,
    upgrade: str,
    *,
    has_hp: bool,
) -> pl.DataFrame:
    """Eversource buildings in one upgrade, kept or dropped by ``has_hp``, with sample weights."""
    path = resstock_metadata_path(release, state, upgrade)
    return cast(
        pl.DataFrame,
        pl.scan_parquet(path)
        .select("bldg_id", "weight", pl.col("postprocess_group.has_hp").alias("has_hp"))
        .join(scan_utility_bldg_ids(release, state, utility), on="bldg_id", how="semi")
        .filter(pl.col("has_hp") == has_hp)
        .collect(),
    )


def presented_bills(
    source: Mapping[str, Mapping[str, float]], bill_order: Sequence[str]
) -> dict[str, dict[str, float]]:
    """Cent-rounded component bills. The total row is the sum of those cents, so the table adds."""
    presented: dict[str, dict[str, float]] = {"rate1": {}, "rate_hp": {}, "decrease": {}}
    for component in bill_order:
        if component == "Total":
            continue
        rate1_bill = round(float(source["rate1"][component]), 2)
        rate_hp_bill = round(float(source["rate_hp"][component]), 2)
        presented["rate1"][component] = rate1_bill
        presented["rate_hp"][component] = rate_hp_bill
        presented["decrease"][component] = round(rate1_bill - rate_hp_bill, 2)
    components = [component for component in bill_order if component != "Total"]
    for key in ("rate1", "rate_hp", "decrease"):
        presented[key]["Total"] = round(sum(presented[key][component] for component in components), 2)
    return presented


def group_revenue(customers: int, dec_dist: float, dec_tx: float) -> dict[str, float]:
    """Annual revenue reduction for a fixed group, and the same amount in each of five years."""
    dist = float(round(customers * dec_dist))
    tx = float(round(customers * dec_tx))
    return {
        "customers": float(customers),
        "distribution": dist,
        "transmission": tx,
        "total": dist + tx,
        "distribution_5": dist * 5,
        "transmission_5": tx * 5,
        "total_5": (dist + tx) * 5,
    }


def new_enrollment_path(
    annual_new: Sequence[int],
    years: Sequence[int],
    dec_dist: float,
    dec_tx: float,
) -> list[dict[str, float]]:
    """Customers are counted from the year they enroll, and they stay enrolled."""
    rows: list[dict[str, float]] = []
    enrolled = 0
    for year, new in zip(years, annual_new, strict=True):
        enrolled += new
        dist = float(round(enrolled * dec_dist))
        tx = float(round(enrolled * dec_tx))
        rows.append(
            {
                "year": float(year),
                "customers": float(enrolled),
                "distribution": dist,
                "transmission": tx,
                "total": dist + tx,
            }
        )
    return rows


def combine_revenue(existing: Mapping[str, float], new_years: Sequence[Mapping[str, float]]) -> list[dict[str, float]]:
    """Add a fixed existing group to each year of a new-enrollment path."""
    rows: list[dict[str, float]] = []
    for new in new_years:
        dist = existing["distribution"] + new["distribution"]
        tx = existing["transmission"] + new["transmission"]
        rows.append(
            {
                "year": new["year"],
                "customers": existing["customers"] + new["customers"],
                "distribution": dist,
                "transmission": tx,
                "total": dist + tx,
            }
        )
    return rows


def makeup_increase(dollars_5: float, nonhp_kwh: float, delivery_rate: float) -> dict[str, float]:
    """Annual increase per non-HP kWh, and that increase as a share of a Rate 1 charge.

    ``dollars_5`` is five years of revenue reduction. Dividing by five puts the
    increase on one year of ``nonhp_kwh``. ``delivery_rate`` is the Rate 1 charge
    the increase is compared with, in $/kWh. For the combined delivery figure
    that charge is distribution plus transmission, and it does not include
    generation.
    """
    increase = dollars_5 / 5 / nonhp_kwh
    return {"increase": increase, "pct": increase / delivery_rate}


def per_kwh_increases(revenue_rows: Sequence[Mapping[str, float]], kwh: float) -> list[dict[str, float]]:
    """Divide each year's distribution and transmission dollars by annual kWh.

    Returned ``distribution`` and ``transmission`` are $/kWh. ``revenue_rows``
    come from :func:`group_revenue` (or the same keys) and each has ``year``.
    """
    if kwh <= 0:
        raise ValueError(f"kwh must be positive, got {kwh}")
    return [
        {
            "year": float(row["year"]),
            "distribution": float(row["distribution"]) / kwh,
            "transmission": float(row["transmission"]) / kwh,
        }
        for row in revenue_rows
    ]


def charge_increase_table(
    floor: Sequence[Mapping[str, float]],
    ceiling: Sequence[Mapping[str, float]],
    *,
    accuracy: int = 4,
) -> str:
    """Rate 1 distribution and transmission increases, in ¢/kWh.

    Each row has ``distribution`` and ``transmission`` in $/kWh, and either
    ``label`` or ``year``.
    """

    def label(row: Mapping[str, float]) -> str:
        if "label" in row:
            return str(row["label"])
        return str(int(row["year"]))

    def line(left: Mapping[str, float], right: Mapping[str, float]) -> str:
        left_label = label(left)
        right_label = label(right)
        if left_label != right_label:
            raise ValueError(f"charge-increase labels differ: {left_label} and {right_label}")
        cells = [
            left_label,
            f"{left['distribution'] * 100:,.{accuracy}f}",
            f"{left['transmission'] * 100:,.{accuracy}f}",
            f"{right['distribution'] * 100:,.{accuracy}f}",
            f"{right['transmission'] * 100:,.{accuracy}f}",
        ]
        return "| " + " | ".join(cells) + " |"

    body = [line(left, right) for left, right in zip(floor, ceiling, strict=True)]
    return "\n".join(
        [
            "| Year | Floor distribution (¢/kWh) | Floor transmission (¢/kWh) | Ceiling distribution (¢/kWh) | Ceiling transmission (¢/kWh) |",
            "| --- | ---: | ---: | ---: | ---: |",
            *body,
        ]
    )


def bill_table(bills: Mapping[str, Mapping[str, float]], bill_order: Sequence[str]) -> str:
    """Markdown table of Rate 1, Rate HP, and the decrease."""

    def row(component: str) -> str:
        cells = [
            component,
            money(bills["rate1"][component], 2),
            money(bills["rate_hp"][component], 2),
            money(bills["decrease"][component], 2),
        ]
        return "| " + " | ".join(cells) + " |"

    return "\n".join(
        [
            "| Component | Rate 1 | Rate HP | Decrease |",
            "| --- | ---: | ---: | ---: |",
            *[row(component) for component in bill_order],
        ]
    )


def _revenue_row(
    floor: Mapping[str, float],
    ceiling: Mapping[str, float],
    label: str | None = None,
    *,
    customers: bool = True,
) -> str:
    year = label if label is not None else str(int(floor["year"]))
    floor_customers = f"{int(floor['customers']):,}" if customers else "—"
    ceiling_customers = f"{int(ceiling['customers']):,}" if customers else "—"
    cells = [
        year,
        floor_customers,
        money(floor["distribution"], 0),
        money(floor["transmission"], 0),
        ceiling_customers,
        money(ceiling["distribution"], 0),
        money(ceiling["transmission"], 0),
    ]
    return "| " + " | ".join(cells) + " |"


def _enrollment_rows(
    floor: Sequence[tuple[int, int]],
    ceiling: Sequence[tuple[int, int]],
    first_label: str,
) -> list[tuple[str, int, int]]:
    """Pair each floor point with its ceiling point and label the starting stock."""
    rows: list[tuple[str, int, int]] = []
    for i, ((year, floor_n), (ceiling_year, ceiling_n)) in enumerate(zip(floor, ceiling, strict=True)):
        if year != ceiling_year:
            raise ValueError(f"enrollment years differ: {year} and {ceiling_year}")
        label = first_label if i == 0 else str(year)
        rows.append((label, floor_n, ceiling_n))
    return rows


def enrollment_table(
    floor: Sequence[tuple[int, int]],
    ceiling: Sequence[tuple[int, int]],
    *,
    first_label: str = "Existing",
) -> str:
    """Customer counts from the starting stock through each later year."""
    body = [
        f"| {label} | {floor_n:,} | {ceiling_n:,} |"
        for label, floor_n, ceiling_n in _enrollment_rows(floor, ceiling, first_label)
    ]
    return "\n".join(
        [
            "| Year | Floor | Ceiling |",
            "| --- | ---: | ---: |",
            *body,
        ]
    )


def td_increase_table(
    enrolled: Sequence[tuple[int, int]],
    dec_dist: float,
    dec_tx: float,
    kwh: float,
    *,
    td_rate: float,
    full_rate: float,
    first_label: str = "Existing",
    accuracy: int = 4,
) -> str:
    """Per-kWh charge increase for one enrollment path.

    Each row divides that year's revenue reduction, from :func:`group_revenue`,
    by ``kwh``. Distribution, transmission, and T&D are ¢/kWh. The last two
    columns are the T&D increase as a share of ``td_rate`` and of ``full_rate``.
    ``td_rate`` is today's distribution plus transmission, in $/kWh. ``full_rate``
    adds generation. The first row is the starting stock.
    """
    if kwh <= 0:
        raise ValueError(f"kwh must be positive, got {kwh}")
    if td_rate <= 0 or full_rate <= 0:
        raise ValueError(f"rates must be positive, got td_rate={td_rate} and full_rate={full_rate}")
    body: list[str] = []
    for i, (_year, customers) in enumerate(enrolled):
        label = first_label if i == 0 else str(_year)
        rev = group_revenue(customers, dec_dist, dec_tx)
        dist = rev["distribution"] / kwh
        tx = rev["transmission"] / kwh
        td = dist + tx
        cells = [
            label,
            f"{dist * 100:,.{accuracy}f}",
            f"{tx * 100:,.{accuracy}f}",
            f"{td * 100:,.{accuracy}f}",
            pct(td / td_rate),
            pct(td / full_rate),
        ]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join(
        [
            "| Year | Distribution (¢/kWh) | Transmission (¢/kWh) | T&D (¢/kWh) | % of T&D | % of T&D and generation |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
            *body,
        ]
    )


def cohort_revenue_rows(
    enrolled: Sequence[tuple[int, int]],
    existing_dec_dist: float,
    existing_dec_tx: float,
    new_dec_dist: float,
    new_dec_tx: float,
) -> list[dict[str, float]]:
    """Annual revenue reduction when the starting stock and later enrollees have different bills.

    The first point in ``enrolled`` is the stock already enrolled. Those customers
    are billed at the existing-home decrease. Customers added after that point are
    billed at the new-home decrease. Each group's dollars are rounded, then added.
    Later rows keep the starting stock.
    """
    if len(enrolled) == 0:
        raise ValueError("enrolled is empty")
    existing_n = int(enrolled[0][1])
    rows: list[dict[str, float]] = []
    for year, customers in enrolled:
        customers_n = int(customers)
        new_n = customers_n - existing_n
        if new_n < 0:
            raise ValueError(f"{year} has {customers_n} customers, below the starting stock of {existing_n}")
        existing = group_revenue(existing_n, existing_dec_dist, existing_dec_tx)
        new = group_revenue(new_n, new_dec_dist, new_dec_tx)
        dist = existing["distribution"] + new["distribution"]
        tx = existing["transmission"] + new["transmission"]
        rows.append(
            {
                "year": float(year),
                "customers": float(customers_n),
                "existing_customers": float(existing_n),
                "new_customers": float(new_n),
                "distribution": dist,
                "transmission": tx,
                "total": dist + tx,
            }
        )
    return rows


def net_revenue_rows(
    enrolled: Sequence[tuple[int, int]],
    dec_dist: float,
    dec_tx: float,
    inc_dist: float,
    inc_tx: float,
) -> list[dict[str, float]]:
    """Revenue reduced (existing), increased (new), and net for each rate year.

    The first point in ``enrolled`` is the stock already enrolled — all existing
    customers. Later points add new customers. Existing customers *reduce*
    revenue (they switch from Rate 1 to Rate HP, post-HP loads, paying less).
    New customers *increase* revenue (they switch from pre-HP Rate 1 to post-HP
    Rate HP, paying more). Each group's dollars are rounded, then the net is
    the difference.

    Skips the first enrollment point (the pre-Rate-Year stock). Returns one row
    per rate year.
    """
    if len(enrolled) < 2:
        raise ValueError("enrolled needs at least the starting stock and one rate year")
    existing_n = int(enrolled[0][1])
    rows: list[dict[str, float]] = []
    for year, customers in enrolled[1:]:
        new_n = int(customers) - existing_n
        if new_n < 0:
            raise ValueError(f"{year} has {int(customers)} customers, below the starting stock of {existing_n}")
        reduced_dist = float(round(existing_n * dec_dist))
        reduced_tx = float(round(existing_n * dec_tx))
        increased_dist = float(round(new_n * inc_dist))
        increased_tx = float(round(new_n * inc_tx))
        rows.append(
            {
                "year": float(year),
                "existing_customers": float(existing_n),
                "new_customers": float(new_n),
                "reduced_dist": reduced_dist,
                "reduced_tx": reduced_tx,
                "increased_dist": increased_dist,
                "increased_tx": increased_tx,
                "net_dist": increased_dist - reduced_dist,
                "net_tx": increased_tx - reduced_tx,
            }
        )
    return rows


def net_revenue_table(rows: list[dict[str, float]]) -> str:
    """Markdown table of revenue reduced / increased / net from ``net_revenue_rows``."""
    lines = [
        "| Rate year | Existing customers | New customers | Revenue reduced, distribution | Revenue reduced, transmission | Revenue increased, distribution | Revenue increased, transmission | Net change, distribution | Net change, transmission |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    def _m(x: float) -> str:
        return f"{x / 1e6:,.1f}"

    for r in rows:
        lines.append(
            f"| {int(r['year'])} "
            f"| {int(r['existing_customers']):,} "
            f"| {int(r['new_customers']):,} "
            f"| {_m(r['reduced_dist'])} "
            f"| {_m(r['reduced_tx'])} "
            f"| {_m(r['increased_dist'])} "
            f"| {_m(r['increased_tx'])} "
            f"| {_m(r['net_dist'])} "
            f"| {_m(r['net_tx'])} |"
        )
    return "\n".join(lines)


def cohort_reduction_table(
    enrolled: Sequence[tuple[int, int]],
    existing_dec_dist: float,
    existing_dec_tx: float,
    new_dec_dist: float,
    new_dec_tx: float,
    *,
    first_label: str = "Existing",
) -> str:
    """Annual revenue reduction for one enrollment path billed on two loads.

    The first row is the starting stock at the existing-home decrease. Each later
    row keeps that stock and adds the new-home decrease for customers enrolled
    since the first point. T&D is distribution plus transmission.
    """
    body: list[str] = []
    for i, row in enumerate(
        cohort_revenue_rows(enrolled, existing_dec_dist, existing_dec_tx, new_dec_dist, new_dec_tx)
    ):
        label = first_label if i == 0 else str(int(row["year"]))
        cells = [
            label,
            f"{int(row['customers']):,}",
            money(row["distribution"], 0),
            money(row["transmission"], 0),
            money(row["total"], 0),
        ]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join(
        [
            "| Year | Customers | Distribution | Transmission | T&D |",
            "| --- | ---: | ---: | ---: | ---: |",
            *body,
        ]
    )


def cohort_increase_table(
    enrolled: Sequence[tuple[int, int]],
    existing_dec_dist: float,
    existing_dec_tx: float,
    new_dec_dist: float,
    new_dec_tx: float,
    kwh: float,
    *,
    td_rate: float,
    full_rate: float,
    first_label: str = "Existing",
    accuracy: int = 4,
) -> str:
    """Per-kWh charge increase when the starting stock and later enrollees have different bills.

    Revenue comes from :func:`cohort_revenue_rows`. Each row divides that revenue
    by ``kwh``. The last two columns are the T&D increase as a share of ``td_rate``
    and of ``full_rate``.
    """
    if kwh <= 0:
        raise ValueError(f"kwh must be positive, got {kwh}")
    if td_rate <= 0 or full_rate <= 0:
        raise ValueError(f"rates must be positive, got td_rate={td_rate} and full_rate={full_rate}")
    body: list[str] = []
    for i, row in enumerate(
        cohort_revenue_rows(enrolled, existing_dec_dist, existing_dec_tx, new_dec_dist, new_dec_tx)
    ):
        label = first_label if i == 0 else str(int(row["year"]))
        dist = row["distribution"] / kwh
        tx = row["transmission"] / kwh
        td = dist + tx
        cells = [
            label,
            f"{dist * 100:,.{accuracy}f}",
            f"{tx * 100:,.{accuracy}f}",
            f"{td * 100:,.{accuracy}f}",
            pct(td / td_rate),
            pct(td / full_rate),
        ]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join(
        [
            "| Year | Distribution (¢/kWh) | Transmission (¢/kWh) | T&D (¢/kWh) | % of T&D | % of T&D and generation |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
            *body,
        ]
    )


def enrollment_range(floor_customers: int, ceiling_customers: int) -> list[tuple[str, int]]:
    """Customer counts from the floor to the ceiling in steps of 20 percent.

    Zero is the floor and 100 percent is the ceiling. Each step in between is that
    share of the distance from the floor to the ceiling, rounded to a customer.
    """
    if ceiling_customers < floor_customers:
        raise ValueError(f"ceiling {ceiling_customers} is below floor {floor_customers}")
    span = ceiling_customers - floor_customers
    rows: list[tuple[str, int]] = []
    for share in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        customers = round(floor_customers + share * span)
        label = "Floor" if share == 0 else "Ceiling" if share == 1 else f"{share:.0%}"
        rows.append((label, customers))
    return rows


def autoenrolled_reduction_table(
    floor_customers: int,
    ceiling_customers: int,
    dec_dist: float,
    dec_tx: float,
) -> str:
    """Annual revenue reduction for the auto-enrolled stock, from the floor to the ceiling.

    Rows are :func:`enrollment_range`. Every row uses the existing-home decrease.
    Customers who install a heat pump later are not included. T&D is distribution
    plus transmission.
    """

    def line(label: str, customers: int) -> str:
        rev = group_revenue(customers, dec_dist, dec_tx)
        cells = [
            label,
            f"{customers:,}",
            money(rev["distribution"], 0),
            money(rev["transmission"], 0),
            money(rev["distribution"] + rev["transmission"], 0),
        ]
        return "| " + " | ".join(cells) + " |"

    return "\n".join(
        [
            "| Share of the range | Customers | Distribution | Transmission | T&D |",
            "| --- | ---: | ---: | ---: | ---: |",
            *[line(label, customers) for label, customers in enrollment_range(floor_customers, ceiling_customers)],
        ]
    )


def scaled_nonhp_sales(
    raw_customers: float,
    raw_kwh: float,
    rate_year_customers: float,
    enrolled: int,
) -> dict[str, float]:
    """Scale non-heat-pump ResStock weights to the Rate Year customers who stay off Rate HP.

    ``raw_customers`` and ``raw_kwh`` are sums over homes without a heat pump:
    ResStock sample weights, and CAIRO grid kWh times those weights. ``enrolled``
    is the existing heat pump customers who move to Rate HP, already counted on
    the Rate Year customer total. The scale is
    ``(rate_year_customers - enrolled) / raw_customers``. Scaled weights sum to
    the customers who remain, and ``kwh`` is ``raw_kwh`` times that same scale.
    CAIRO's grid kWh already carries the small rate-year energy calibration, so
    this scale is the customer adjustment only.
    """
    if raw_customers <= 0:
        raise ValueError(f"raw_customers must be positive, got {raw_customers}")
    if raw_kwh <= 0:
        raise ValueError(f"raw_kwh must be positive, got {raw_kwh}")
    paying = float(rate_year_customers) - float(enrolled)
    if paying <= 0:
        raise ValueError(f"enrolled {enrolled} leaves no customers in a Rate Year class of {rate_year_customers}")
    scale = paying / float(raw_customers)
    return {"customers": paying, "kwh": float(raw_kwh) * scale, "scale": scale}


def _per_row(values: float | Sequence[float], n: int, name: str) -> list[float]:
    """One number repeated, or one number per enrollment row."""
    # bool is a subclass of int, so reject it before the numeric branch.
    if isinstance(values, bool):
        raise TypeError(f"{name} must be a number or a sequence of numbers, got bool")
    if isinstance(values, (int, float)):
        number = float(values)
        if number <= 0:
            raise ValueError(f"{name} must be positive, got {number}")
        return [number] * n
    row_values = [float(value) for value in values]
    if len(row_values) != n:
        raise ValueError(f"{name} has {len(row_values)} values for {n} enrollment rows")
    if any(value <= 0 for value in row_values):
        raise ValueError(f"{name} must be positive, got {row_values}")
    return row_values


def autoenrolled_increases(
    floor_customers: int,
    ceiling_customers: int,
    dec_dist: float,
    dec_tx: float,
    kwh: float | Sequence[float],
    *,
    nonhp_customers: float | Sequence[float] | None = None,
) -> list[dict[str, Any]]:
    """Per-kWh charge that recovers only the auto-enrolled revenue reduction.

    One row per :func:`enrollment_range` step. ``distribution`` and
    ``transmission`` are dollars from :func:`group_revenue`.
    ``distribution_per_kwh`` and ``transmission_per_kwh`` are those dollars
    divided by that row's ``kwh``. A single ``kwh`` is used for every row.
    ``per_kwh`` is the T&D charge, in $/kWh. ``nonhp_kwh`` is the denominator.
    ``nonhp_customers`` is the customer count that denominator was scaled to,
    when the caller passes it. CIEC-3 stores these rows. CIEC-6 pastes the
    three rates and multiplies ``per_kwh`` by each home's annual kWh.
    """
    steps = enrollment_range(floor_customers, ceiling_customers)
    row_kwh = _per_row(kwh, len(steps), "kwh")
    row_customers = None if nonhp_customers is None else _per_row(nonhp_customers, len(steps), "nonhp_customers")
    rows: list[dict[str, Any]] = []
    for i, (label, customers) in enumerate(steps):
        rev = group_revenue(customers, dec_dist, dec_tx)
        dist = float(rev["distribution"])
        tx = float(rev["transmission"])
        sales = row_kwh[i]
        row: dict[str, Any] = {
            "label": label,
            "customers": customers,
            "distribution": dist,
            "transmission": tx,
            "distribution_per_kwh": dist / sales,
            "transmission_per_kwh": tx / sales,
            "per_kwh": (dist + tx) / sales,
            "nonhp_kwh": sales,
        }
        if row_customers is not None:
            row["nonhp_customers"] = row_customers[i]
        rows.append(row)
    return rows


def autoenrolled_increase_table(
    floor_customers: int,
    ceiling_customers: int,
    dec_dist: float,
    dec_tx: float,
    kwh: float | Sequence[float],
    *,
    td_rate: float,
    full_rate: float,
    nonhp_customers: float | Sequence[float] | None = None,
    accuracy: int = 4,
) -> str:
    """Per-kWh charge increase that recovers only the auto-enrolled revenue reduction.

    Rows are :func:`autoenrolled_increases`. Distribution, transmission, and T&D
    are ¢/kWh. The last two columns are the T&D increase as a share of
    ``td_rate`` and of ``full_rate``. ``full_rate`` is distribution plus
    transmission plus generation. When ``nonhp_customers`` is set, the table
    includes the customers the row's kWh was scaled to.
    """
    rows = autoenrolled_increases(
        floor_customers,
        ceiling_customers,
        dec_dist,
        dec_tx,
        kwh,
        nonhp_customers=nonhp_customers,
    )
    if td_rate <= 0 or full_rate <= 0:
        raise ValueError(f"rates must be positive, got td_rate={td_rate} and full_rate={full_rate}")
    show_payers = nonhp_customers is not None

    def line(row: Mapping[str, Any]) -> str:
        dist = float(row["distribution_per_kwh"])
        tx = float(row["transmission_per_kwh"])
        td = float(row["per_kwh"])
        cells = [str(row["label"])]
        if show_payers:
            cells.append(f"{round(float(row['nonhp_customers'])):,}")
        cells.extend(
            [
                f"{dist * 100:,.{accuracy}f}",
                f"{tx * 100:,.{accuracy}f}",
                f"{td * 100:,.{accuracy}f}",
                pct(td / td_rate),
                pct(td / full_rate),
            ]
        )
        return "| " + " | ".join(cells) + " |"

    header = "| Share of the range | "
    rule = "| --- | "
    if show_payers:
        header += "Non-HP customers | "
        rule += "---: | "
    header += "Distribution (¢/kWh) | Transmission (¢/kWh) | T&D (¢/kWh) | % of T&D | % of T&D and generation |"
    rule += "---: | ---: | ---: | ---: | ---: |"
    return "\n".join([header, rule, *[line(row) for row in rows]])


def _usage(buildings: pl.DataFrame) -> pl.DataFrame:
    """``annual_kwh`` and ``weight`` for the bill-increase stats, or an error naming what is wrong."""
    missing = [name for name in ("annual_kwh", "weight") if name not in buildings.columns]
    if missing:
        raise ValueError(f"buildings is missing {missing}")
    if buildings.height == 0:
        raise ValueError("buildings is empty")
    usage = buildings.select("annual_kwh", "weight")
    if usage["weight"].null_count() or usage["annual_kwh"].null_count():
        raise ValueError("weight or annual_kwh has nulls")
    weight = float(usage["weight"].sum())
    if weight <= 0:
        raise ValueError(f"weight must be positive, got {weight}")
    return usage


def annual_bill_increase_stats(buildings: pl.DataFrame, dollars_per_kwh: float) -> dict[str, float]:
    """Weighted mean and percentiles of ``annual_kwh * dollars_per_kwh``.

    The mean is that charge times weighted-mean consumption. When
    ``dollars_per_kwh`` is a revenue reduction divided by weighted kWh, the
    mean is that revenue divided by the customer count those weights sum to.
    Scaling every weight by the same factor does not change the mean or the
    percentiles, so unscaled ResStock weights give the same bill distribution
    as weights scaled to the Rate Year customers who remain. Keys are
    ``mean``, ``p25``, ``median``, and ``p75``.
    """
    if dollars_per_kwh < 0:
        raise ValueError(f"dollars_per_kwh must be non-negative, got {dollars_per_kwh}")
    usage = _usage(buildings)
    bills = usage.select((pl.col("annual_kwh") * dollars_per_kwh).alias("bill"), "weight")
    return {
        "mean": weighted_mean(bills, "bill"),
        "p25": weighted_quantile(bills, "bill", 0.25),
        "median": weighted_quantile(bills, "bill", 0.50),
        "p75": weighted_quantile(bills, "bill", 0.75),
    }


def bill_table_from_increases(
    increases: Sequence[Mapping[str, Any]],
    buildings: pl.DataFrame,
) -> str:
    """Weighted annual bill increase for each CIEC-3 per-kWh charge.

    ``increases`` rows have ``label``, ``customers``, and ``per_kwh`` in $/kWh,
    as returned by :func:`autoenrolled_increases`. Each row multiplies that
    charge by each home's ``annual_kwh``. The mean and the percentiles use
    ``weight``.
    """
    if not increases:
        raise ValueError("increases is empty")
    usage = _usage(buildings)
    kwh = float((usage["annual_kwh"] * usage["weight"]).sum())
    if kwh <= 0:
        raise ValueError(f"kwh must be positive, got {kwh}")

    def line(row: Mapping[str, Any]) -> str:
        stats = annual_bill_increase_stats(buildings, float(row["per_kwh"]))
        cells = [
            str(row["label"]),
            f"{int(row['customers']):,}",
            money(stats["mean"], 2),
            money(stats["p25"], 2),
            money(stats["median"], 2),
            money(stats["p75"], 2),
        ]
        return "| " + " | ".join(cells) + " |"

    return "\n".join(
        [
            "| Share of the range | Customers | Mean | 25th | Median | 75th |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
            *[line(row) for row in increases],
        ]
    )


def autoenrolled_bill_table(
    floor_customers: int,
    ceiling_customers: int,
    dec_dist: float,
    dec_tx: float,
    buildings: pl.DataFrame,
) -> str:
    """Weighted annual bill increase that recovers only the auto-enrolled revenue reduction.

    Rows are :func:`autoenrolled_increases` for the weighted kWh in ``buildings``.
    Each row multiplies that per-kWh charge by each home's ``annual_kwh``.
    The mean and the percentiles use ``weight``.
    """
    usage = _usage(buildings)
    kwh = float((usage["annual_kwh"] * usage["weight"]).sum())
    increases = autoenrolled_increases(floor_customers, ceiling_customers, dec_dist, dec_tx, kwh)
    return bill_table_from_increases(increases, buildings)


def td_reduction_table(
    enrolled: Sequence[tuple[int, int]],
    dec_dist: float,
    dec_tx: float,
    *,
    first_label: str = "Existing",
) -> str:
    """Annual revenue reduction for one enrollment path.

    Each row is that year's enrolled customers times the one-customer
    distribution and transmission reductions, rounded to the dollar. The first
    row is the starting stock, and each later row includes it. T&D is
    distribution plus transmission.
    """
    body: list[str] = []
    for i, (_year, customers) in enumerate(enrolled):
        label = first_label if i == 0 else str(_year)
        rev = group_revenue(customers, dec_dist, dec_tx)
        cells = [
            label,
            f"{customers:,}",
            money(rev["distribution"], 0),
            money(rev["transmission"], 0),
            money(rev["distribution"] + rev["transmission"], 0),
        ]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join(
        [
            "| Year | Customers | Distribution | Transmission | T&D |",
            "| --- | ---: | ---: | ---: | ---: |",
            *body,
        ]
    )


def bounds_table(floor_rows: Sequence[Mapping[str, float]], ceiling_rows: Sequence[Mapping[str, float]]) -> str:
    """Floor and ceiling revenue by year, with a five-year total of the revenue columns."""
    total_floor = {
        "year": 0.0,
        "customers": 0.0,
        "distribution": sum(row["distribution"] for row in floor_rows),
        "transmission": sum(row["transmission"] for row in floor_rows),
    }
    total_ceiling = {
        "year": 0.0,
        "customers": 0.0,
        "distribution": sum(row["distribution"] for row in ceiling_rows),
        "transmission": sum(row["transmission"] for row in ceiling_rows),
    }
    body = [_revenue_row(floor, ceiling) for floor, ceiling in zip(floor_rows, ceiling_rows, strict=True)]
    return "\n".join(
        [
            "| Year | Floor customers | Floor distribution | Floor transmission | Ceiling customers | Ceiling distribution | Ceiling transmission |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            *body,
            _revenue_row(total_floor, total_ceiling, label="Five-year total", customers=False),
        ]
    )


def existing_customers_table(floor: Mapping[str, float], ceiling: Mapping[str, float]) -> str:
    """Annual and five-year revenue reduction for the two existing-customer bounds."""

    def row(label: str, group: Mapping[str, float]) -> str:
        cells = [
            label,
            f"{int(group['customers']):,}",
            money(group["distribution"], 0),
            money(group["transmission"], 0),
            money(group["distribution_5"], 0),
            money(group["transmission_5"], 0),
        ]
        return "| " + " | ".join(cells) + " |"

    return "\n".join(
        [
            "| Bound | Customers | Annual distribution | Annual transmission | Five-year distribution | Five-year transmission |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
            row("Floor", floor),
            row("Ceiling", ceiling),
        ]
    )


_EXHIBIT_RATES_2 = (
    Path(__file__).resolve().parents[3] / "context/sources/ct_hp_rates/exhibit_clp_rates_2_residential.md"
)
_RATE_YEAR_HEADING = "### 4b. Page 2"
_BILL_ROW = re.compile(r"^\|\s*(1|5|7)\s*\|[^|]*\|\s*([0-9,]+(?:\.\d+)?)", re.MULTILINE)


def rate_year_residential_customers(path: Path | None = None) -> int:
    """Residential customers Eversource filed for the Rate Year.

    Sum of the average number of bills rendered for Rates 1, 5, and 7 on
    Exhibit CLP-RATES-2.10, page 2 (Rate Year ending June 30, 2028), rounded
    to a customer. Rate 5's Rate Year cell is unreadable in the workbook, so
    the extract carries the Test Year count forward, as the exhibit notes.
    """
    text = (path or _EXHIBIT_RATES_2).read_text()
    try:
        section = text.split(_RATE_YEAR_HEADING, 1)[1].split("\n## ", 1)[0]
    except IndexError as exc:
        raise RuntimeError(f"{path or _EXHIBIT_RATES_2} has no {_RATE_YEAR_HEADING!r} section") from exc
    bills = {rate: float(count.replace(",", "")) for rate, count in _BILL_ROW.findall(section)}
    missing = {"1", "5", "7"} - bills.keys()
    if missing:
        raise RuntimeError(f"Rate Year bill counts missing for rates {sorted(missing)}")
    return round(sum(bills.values()))


def cumulative_enrollment(
    existing: int,
    annual_new: Sequence[int],
    years: Sequence[int],
) -> list[tuple[int, int]]:
    """Cumulative customers from the year before the first rate year through the last.

    The first point is the stock already enrolled. Each later point adds that
    year's installations and keeps everyone already enrolled.
    """
    if len(years) == 0:
        raise ValueError("years is empty")
    stock = existing
    points = [(int(years[0]) - 1, stock)]
    for year, new in zip(years, annual_new, strict=True):
        stock += new
        points.append((int(year), stock))
    return points


def makeup_table(rows: Sequence[tuple[str, str, Mapping[str, float]]]) -> str:
    """Markdown table of the non-HP $/kWh increase and its percent of the delivery rate."""

    def row(group: str, bound: str, values: Mapping[str, float]) -> str:
        cells = [group, bound, money(values["increase"], 6), pct(values["pct"])]
        return "| " + " | ".join(cells) + " |"

    return "\n".join(
        [
            "| Group | Bound | Increase (\\$/kWh) | Change |",
            "| --- | --- | ---: | ---: |",
            *[row(group, bound, values) for group, bound, values in rows],
        ]
    )


def read_energizect_installations(path: Path) -> pl.DataFrame:
    """EnergizeCT heat pump export as ``heat_pump_type``, ``year``, ``installations``.

    Reads the workbook's Detail sheet, one row per company, sector, heat pump
    type, sub-program and year. The Export sheet is SUMIFS formulas over
    Detail with no cached values, so openpyxl reads it as blank. Sub-programs
    are summed within each type and year. The sheet must hold a single
    company and sector, so a broader export can't be counted as Eversource
    residential.
    """
    import openpyxl

    sheet = openpyxl.load_workbook(path, data_only=True)["Detail"]
    header, *rows = sheet.iter_rows(values_only=True)
    detail = pl.DataFrame(
        [row for row in rows if any(cell is not None for cell in row)],
        schema=[str(name) for name in header],
        orient="row",
    )
    for column in ("Company", "Sector"):
        values = detail[column].unique().to_list()
        if len(values) != 1:
            raise ValueError(f"{path}: Detail has more than one {column}: {values}")
    return (
        detail.group_by(pl.col("Heat Pump Type").alias("heat_pump_type"), pl.col("Year").cast(pl.Int64).alias("year"))
        .agg(pl.col("Installations").cast(pl.Int64).sum().alias("installations"))
        .sort("heat_pump_type", "year")
    )


def energizect_households(
    installations: pl.DataFrame,
    systems_per_home: Mapping[str, float],
    exclude: Sequence[str] = ("Heat Pump Water Heater",),
) -> pl.DataFrame:
    """Installations and implied households for each heat pump type, all years.

    One installation is one rebated system. Households are installations
    divided by ``systems_per_home`` for that type. Every type that is not
    excluded needs a ratio, so a new equipment type in the export fails here
    rather than counting as one system per home by default.
    """
    totals = (
        installations.filter(~pl.col("heat_pump_type").is_in(list(exclude)))
        .group_by("heat_pump_type")
        .agg(pl.col("installations").sum())
    )
    missing = sorted(set(totals["heat_pump_type"]) - set(systems_per_home))
    if missing:
        raise ValueError(f"no systems-per-home ratio for {missing}")
    if any(ratio < 1 for ratio in systems_per_home.values()):
        raise ValueError(f"systems per home must be at least 1, got {dict(systems_per_home)}")
    ratios = pl.DataFrame(
        {"heat_pump_type": list(systems_per_home), "systems_per_home": [float(v) for v in systems_per_home.values()]}
    )
    return (
        totals.join(ratios, on="heat_pump_type", how="left")
        .with_columns((pl.col("installations") / pl.col("systems_per_home")).alias("households"))
        .sort("installations", descending=True)
    )
