"""CIEC-1 helpers for the Rate HP revenue reduction.

The weighted monthly load and the monthly bill calculation already live in
``lib.rates_analysis.rate_case_funcs``. Percent text comes from
``lib.format.pct``. The functions here are the CIEC-1 steps those modules do
not cover: folding Rate 1 charges, applying the winter Rate HP rates, selecting
a heat-pump subclass, and scaling one customer's revenue reduction to the
enrollment bounds and a non-HP per-kWh increase.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, cast

import polars as pl

from lib.format import pct as format_pct
from lib.rates_analysis.hh_summary_funcs import resstock_metadata_path, scan_utility_bldg_ids
from lib.rates_analysis.rate_case_funcs import monthly_bill_from_profile

RateSpec = dict[str, Any]


def dollar(x: float, accuracy: int = 0) -> str:
    """Dollar text for inline prose, e.g. ``1234.5`` -> ``"$1,234.50"``."""
    return f"${x:,.{accuracy}f}"


def num(x: float, accuracy: int = 0) -> str:
    """Number text with thousands separators."""
    return f"{x:,.{accuracy}f}"


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
        "distribution_5": dist * 5,
        "transmission_5": tx * 5,
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
    """Annual increase per non-HP kWh, and that increase as a share of the Rate 1 delivery rate.

    ``dollars_5`` is five years of revenue reduction. Dividing by five puts the
    increase on one year of ``nonhp_kwh``. ``delivery_rate`` is distribution plus
    transmission, in $/kWh, and does not include generation.
    """
    increase = dollars_5 / 5 / nonhp_kwh
    return {"increase": increase, "pct": increase / delivery_rate}


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
