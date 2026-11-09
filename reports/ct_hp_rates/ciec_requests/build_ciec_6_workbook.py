"""Helpers for the CIEC-6(c) Excel workpaper.

``ciec_request_6.qmd`` loads the CIEC-3(c) revenue reduction for customers who
already have a heat pump, and that response's non-heat-pump buildings, then
calls :func:`build_workbook`. Upload uses :func:`build_ciec_1a_workbook.upload_xlsx`.
Yellow cells are inputs. Every other number is a formula.

Sheets
------
README
    What the file is and how the sheets connect.
revenue
    Floor and ceiling customer counts, and the per-customer distribution and
    transmission decreases, are inputs. The 20, 40, 60, and 80 percent rows
    place the customer count that share of the way from the floor to the
    ceiling. Distribution and transmission are that count times the
    per-customer decrease, rounded to the dollar. Later installers are not
    included. T&D adds the two components.
payers
    One row per step from the floor to the ceiling. Customers who remain are
    the Rate Year residential count minus the customers who move. Weighted kWh
    scales the ResStock total by that count. The increase sheet divides the
    revenue reduction by that weighted kWh.
customers
    One row per Eversource home without a heat pump, sorted by annual kWh.
    Weight is the ResStock sample weight. Bill columns multiply annual kWh by
    the per-kWh increase. That sort is also bill order.
increase
    Each step's distribution, transmission, and T&D charge in $/kWh. Each is
    that step's revenue reduction divided by that step's weighted kWh.
summary
    Weighted mean and percentiles of the annual bill. The mean matches the
    revenue reduction divided by the customers who remain on payers.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import polars as pl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

DRIVE_NAME = "CIEC-6c_nonhp_bill_increase.xlsx"

INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
HEADER_FONT = Font(bold=True)
TITLE_FONT = Font(bold=True, size=14)
WRAP = Alignment(wrap_text=True, vertical="top")
HEADER_ALIGN = Alignment(wrap_text=True, vertical="bottom")

FMT_KWH = "#,##0.000"
FMT_WEIGHT = "#,##0.000000"
FMT_RATE = "0.000000"
FMT_REVENUE = "$#,##0"
FMT_BILL = "$#,##0.00"
FMT_COUNT = "#,##0"

RANGE_STEPS: tuple[tuple[str, str | None], ...] = (
    ("Floor", None),
    ("20%", "1/5"),
    ("40%", "2/5"),
    ("60%", "3/5"),
    ("80%", "4/5"),
    ("Ceiling", None),
)
RANGE_DIST_ROW = 4
RANGE_TX_ROW = 5
RANGE_HEADER = 7
RANGE_FIRST = 8
RANGE_LAST = RANGE_FIRST + len(RANGE_STEPS) - 1
CUSTOMERS_KWH_ROW = 4
CUSTOMERS_COUNT_ROW = 5
CUSTOMERS_WEIGHT_ROW = 6
CUSTOMERS_HEADER = 7
CUSTOMERS_FIRST = 8
SUMMARY_HEADER = 4
SUMMARY_MEAN_DIST = 5
SUMMARY_MEAN_TX = 6
SUMMARY_MEAN_BILL = 7
SUMMARY_PER_CUSTOMER = 8
SUMMARY_QUANTILE_FIRST = 9
PAYERS_RATE_YEAR_ROW = 4

# (label, share of customers). The summary formulas find these shares in kWh order.
QUANTILES: tuple[tuple[str, float], ...] = (
    ("25th percentile", 0.25),
    ("Median", 0.50),
    ("75th percentile", 0.75),
)


@dataclass(frozen=True)
class RevenueRow:
    """Revenue reduction for the auto-enrolled stock, already calculated in CIEC-3(c).

    ``distribution`` and ``transmission`` are dollars, rounded to the dollar.
    """

    label: str
    customers: int
    distribution: float
    transmission: float


def _customer_count(first: int, last: int, fraction: str | None) -> str | None:
    """Formula for a step between the floor and ceiling customer counts.

    ``None`` marks the floor and the ceiling, which stay as inputs.
    """
    if fraction is None:
        return None
    return f"=ROUND($B${first}+({fraction})*($B${last}-$B${first}),0)"


def _put(
    ws: Worksheet,
    row: int,
    col: int,
    value: Any,
    *,
    input_: bool = False,
    fmt: str | None = None,
    bold: bool = False,
    wrap: bool = False,
) -> None:
    cell = ws.cell(row, col, value)
    if input_:
        cell.fill = INPUT_FILL
    if bold:
        cell.font = HEADER_FONT
    if wrap:
        cell.alignment = WRAP
    if fmt:
        cell.number_format = fmt


def _heading(ws: Worksheet, row: int, text: str) -> None:
    ws.cell(row, 1, text).font = TITLE_FONT


def _note(ws: Worksheet, row: int, text: str, last_col: int, *, height: int = 48) -> None:
    _put(ws, row, 1, text, wrap=True)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=last_col)
    ws.row_dimensions[row].height = height


def _headers(ws: Worksheet, row: int, headers: Sequence[str]) -> None:
    for col, header in enumerate(headers, start=1):
        _put(ws, row, col, header, bold=True)
        ws.cell(row, col).alignment = HEADER_ALIGN
    ws.row_dimensions[row].height = 32


def _check_revenue(floor: RevenueRow, ceiling: RevenueRow) -> None:
    if floor.label == "" or floor.label != ceiling.label:
        raise ValueError(f"revenue labels differ: {floor.label!r} and {ceiling.label!r}")
    if floor.customers < 0 or ceiling.customers < 0:
        raise ValueError(f"customers must be non-negative, got {floor.customers} and {ceiling.customers}")
    if min(floor.distribution, floor.transmission, ceiling.distribution, ceiling.transmission) < 0:
        raise ValueError("revenue must be non-negative")


def _customers(buildings: pl.DataFrame) -> pl.DataFrame:
    """One row per home, sorted by annual kWh so the summary percentiles follow bill order."""
    missing = [name for name in ("bldg_id", "weight", "annual_kwh") if name not in buildings.columns]
    if missing:
        raise ValueError(f"buildings is missing {missing}")
    if buildings.height == 0:
        raise ValueError("buildings is empty")
    out = buildings.select("bldg_id", "weight", "annual_kwh").sort("annual_kwh", "bldg_id")
    if out["bldg_id"].n_unique() != out.height:
        raise ValueError("bldg_id is not unique")
    if out["weight"].null_count() or out["annual_kwh"].null_count():
        raise ValueError("weight or annual_kwh has nulls")
    if bool((out["weight"] <= 0).any()):
        raise ValueError("weight must be positive")
    if bool((out["annual_kwh"] < 0).any()):
        raise ValueError("annual_kwh must be non-negative")
    total = float((out["annual_kwh"] * out["weight"]).sum())
    if total <= 0:
        raise ValueError(f"weighted kWh must be positive, got {total}")
    return out


def _write_readme(wb: Workbook) -> None:
    ws = wb.active
    ws.title = "README"
    lines = [
        ("CIEC-6(c) workpaper", True),
        (
            "Docket No. 26-05-10. Witness: Juan-Pablo Velez. Request from Connecticut Industrial Energy Consumers.",
            False,
        ),
        (
            "Annual bill increase for residential customers who do not take Rate HP, if the revenue no longer "
            "collected from auto-enrolled heat pump customers were recovered from those residential customers. "
            "Non-residential customers, including Rate 39 and Rate 57, are not charged. Customers who install a "
            "heat pump later are not part of this recovery. Rate HP is calibrated so that a new heat pump customer "
            "pays the embedded-cost revenue requirement and the additional transmission and distribution marginal cost.",
            False,
        ),
        ("", False),
        ("Yellow cells are inputs. Every other number is a formula.", True),
        ("", False),
        ("revenue", True),
        (
            "Floor and ceiling customer counts are inputs, from CIEC-1(b), including the 2026 installations. "
            "The per-customer distribution and transmission decreases are inputs, from CIEC-1(a). "
            "The 20, 40, 60, and 80 percent rows are that share of the distance from the floor to the ceiling, "
            "rounded to a customer. Distribution and transmission are that count times the per-customer decrease, "
            "rounded to the dollar. T&D adds the two components. Installations in 2027 through 2031 are not on this sheet.",
            False,
        ),
        ("", False),
        ("payers", True),
        (
            "One row per step from the floor to the ceiling. The Rate Year count is an input, the average bills "
            "rendered for Rates 1, 5, and 7. Customers who remain are that count minus the customers who move. "
            "Weighted kWh scales the ResStock total by that count. The increase sheet divides the revenue "
            "reduction by that weighted kWh.",
            False,
        ),
        ("", False),
        ("customers", True),
        (
            "One row per Eversource home without a heat pump in the ResStock baseline, sorted by annual kWh "
            "and then by bldg_id. Annual kWh is CAIRO grid consumption. Weight is the ResStock sample weight. "
            "Weighted kWh multiplies annual kWh by that weight. Each bill column multiplies annual kWh by that "
            "step's T&D increase. Because every bill in a column uses the same per-kWh charge, the kWh sort is also the order of the "
            "bill increase, and the percentiles on summary read that order. Scaling every weight by the same "
            "factor would not change those percentiles. Homes on Rate 5 and Rate 7 are included with Rate 1. "
            "Customers on Rate HP are not on this sheet.",
            False,
        ),
        ("", False),
        ("increase", True),
        (
            "Distribution, transmission, and T&D are that step's revenue reduction divided by that step's "
            "weighted kWh, in dollars per kWh. The customer charge and generation are unchanged and are not "
            "on this sheet.",
            False,
        ),
        ("", False),
        ("summary", True),
        (
            "Weighted mean and percentiles of the annual bill increase. The mean multiplies each customer bill "
            "by the ResStock sample weight. Revenue / customers divides the revenue reduction by the customers "
            "who remain on payers. Those two are the same amount, because the per-kWh charge was spread over "
            "sales scaled to that count and a uniform weight scale does not change the weighted mean. A percentile "
            "is the bill of the first customer in kWh order whose running sample weight reaches that share of customers.",
            False,
        ),
    ]
    for row, (text, bold) in enumerate(lines, start=1):
        cell = ws.cell(row, 1, text)
        cell.alignment = WRAP
        if bold:
            cell.font = TITLE_FONT if row == 1 else HEADER_FONT
    ws.column_dimensions["A"].width = 120
    ws.row_dimensions[1].height = 22
    for row in (3, 8, 11, 14, 17, 20):
        ws.row_dimensions[row].height = 64


def _check_per_customer(floor: RevenueRow, ceiling: RevenueRow, distribution: float, transmission: float) -> None:
    if distribution < 0 or transmission < 0:
        raise ValueError(f"per-customer decrease must be non-negative, got {distribution} and {transmission}")
    if ceiling.customers < floor.customers:
        raise ValueError(f"ceiling {ceiling.customers} is below floor {floor.customers}")
    for row in (floor, ceiling):
        dist = round(row.customers * distribution)
        tx = round(row.customers * transmission)
        if dist != row.distribution or tx != row.transmission:
            raise ValueError(
                f"{row.label} revenue {row.distribution} and {row.transmission} "
                f"is not {row.customers} times the per-customer decrease"
            )


def _write_revenue(
    wb: Workbook,
    floor: RevenueRow,
    ceiling: RevenueRow,
    distribution: float,
    transmission: float,
) -> None:
    ws = wb.create_sheet("revenue")
    _heading(ws, 1, "Revenue reduction")
    _note(
        ws,
        2,
        "Annual revenue reduction for customers who would move from Rate 1 to Rate HP. "
        "The floor and ceiling customer counts are inputs. The 20, 40, 60, and 80 percent "
        "rows are that share of the distance between them, rounded to a customer. "
        "Distribution and transmission are the customer count times the per-customer decrease, "
        "rounded to the dollar. Later heat pump installations are excluded.",
        5,
        height=64,
    )
    _put(ws, RANGE_DIST_ROW, 1, "Per-customer distribution decrease", bold=True)
    _put(ws, RANGE_DIST_ROW, 2, distribution, input_=True, fmt="$#,##0.00", bold=True)
    _put(ws, RANGE_TX_ROW, 1, "Per-customer transmission decrease", bold=True)
    _put(ws, RANGE_TX_ROW, 2, transmission, input_=True, fmt="$#,##0.00", bold=True)
    _headers(ws, RANGE_HEADER, ["Share of the range", "Customers", "Distribution", "Transmission", "T&D"])
    for i, (label, fraction) in enumerate(RANGE_STEPS):
        row = RANGE_FIRST + i
        customers = _customer_count(RANGE_FIRST, RANGE_LAST, fraction)
        _put(ws, row, 1, label)
        if customers is None:
            count = floor.customers if i == 0 else ceiling.customers
            _put(ws, row, 2, count, input_=True, fmt=FMT_COUNT)
        else:
            _put(ws, row, 2, customers, fmt=FMT_COUNT)
        _put(ws, row, 3, f"=ROUND(B{row}*$B${RANGE_DIST_ROW},0)", fmt=FMT_REVENUE)
        _put(ws, row, 4, f"=ROUND(B{row}*$B${RANGE_TX_ROW},0)", fmt=FMT_REVENUE)
        _put(ws, row, 5, f"=C{row}+D{row}", fmt=FMT_REVENUE)
    ws.freeze_panes = "A8"
    ws.column_dimensions["A"].width = 42
    for col in range(2, 6):
        ws.column_dimensions[get_column_letter(col)].width = 22


def _write_customers(wb: Workbook, buildings: pl.DataFrame) -> int:
    ws = wb.create_sheet("customers")
    _heading(ws, 1, "Non-heat-pump bill increase")
    _note(
        ws,
        2,
        "Eversource homes without a heat pump, sorted by annual kWh. Annual kWh is CAIRO grid consumption. "
        "Weight is the ResStock sample weight. Each bill column multiplies annual kWh by that step's T&D increase. "
        "Homes on Rate 5 and Rate 7 are included with Rate 1.",
        10,
        height=48,
    )
    last = CUSTOMERS_FIRST + buildings.height - 1
    _put(ws, CUSTOMERS_KWH_ROW, 1, "Total weighted kWh", bold=True)
    _put(ws, CUSTOMERS_KWH_ROW, 2, f"=SUM(D{CUSTOMERS_FIRST}:D{last})", fmt=FMT_KWH, bold=True)
    _put(ws, CUSTOMERS_COUNT_ROW, 1, "Buildings", bold=True)
    _put(ws, CUSTOMERS_COUNT_ROW, 2, f"=COUNTA(A{CUSTOMERS_FIRST}:A{last})", fmt=FMT_COUNT, bold=True)
    _put(ws, CUSTOMERS_WEIGHT_ROW, 1, "ResStock weight", bold=True)
    _put(ws, CUSTOMERS_WEIGHT_ROW, 2, f"=SUM(B{CUSTOMERS_FIRST}:B{last})", fmt=FMT_WEIGHT, bold=True)
    _headers(
        ws,
        CUSTOMERS_HEADER,
        [
            "bldg_id",
            "weight",
            "annual kWh",
            "weighted kWh",
            *(f"{label} bill" for label, _fraction in RANGE_STEPS),
        ],
    )
    for i, record in enumerate(buildings.iter_rows(named=True)):
        row = CUSTOMERS_FIRST + i
        _put(ws, row, 1, int(record["bldg_id"]), input_=True, fmt=FMT_COUNT)
        _put(ws, row, 2, float(record["weight"]), input_=True, fmt=FMT_WEIGHT)
        _put(ws, row, 3, float(record["annual_kwh"]), input_=True, fmt=FMT_KWH)
        _put(ws, row, 4, f"=B{row}*C{row}", fmt=FMT_KWH)
        for step, _label in enumerate(RANGE_STEPS):
            rate_row = RANGE_FIRST + step
            _put(ws, row, 5 + step, f"=C{row}*increase!$D${rate_row}", fmt=FMT_BILL)
    ws.freeze_panes = "A8"
    ws.auto_filter.ref = f"A{CUSTOMERS_HEADER}:J{last}"
    ws.column_dimensions["A"].width = 14
    for col in range(2, 11):
        ws.column_dimensions[get_column_letter(col)].width = 22
    return last


def _check_rate_year(rate_year_customers: float, floor: RevenueRow, ceiling: RevenueRow) -> None:
    if rate_year_customers <= 0:
        raise ValueError(f"Rate Year customers must be positive, got {rate_year_customers}")
    if floor.customers >= rate_year_customers or ceiling.customers >= rate_year_customers:
        raise ValueError(
            f"enrolled customers leave nobody to pay: Rate Year {rate_year_customers}, "
            f"floor {floor.customers}, ceiling {ceiling.customers}"
        )


def _write_payers(wb: Workbook, rate_year_customers: float) -> None:
    ws = wb.create_sheet("payers")
    _heading(ws, 1, "Customers who move and customers who pay")
    _note(
        ws,
        2,
        "One row per step from the floor to the ceiling. Heat pump customers who move are the customer "
        "count on revenue. Customers who remain are the Rate Year count minus the customers who move. "
        "The scale divides the customers who remain by the ResStock weight sum. Weighted kWh multiplies "
        "the ResStock weighted kWh by that scale. The increase sheet divides each step's revenue by that kWh.",
        5,
        height=64,
    )
    _put(ws, PAYERS_RATE_YEAR_ROW, 1, "Rate Year residential customers", bold=True)
    _put(ws, PAYERS_RATE_YEAR_ROW, 2, rate_year_customers, input_=True, fmt=FMT_COUNT, bold=True)
    _put(ws, 5, 1, "ResStock non-HP customers", bold=True)
    _put(ws, 5, 2, f"=customers!B{CUSTOMERS_WEIGHT_ROW}", fmt=FMT_WEIGHT, bold=True)
    _put(ws, 6, 1, "ResStock non-HP kWh", bold=True)
    _put(ws, 6, 2, f"=customers!B{CUSTOMERS_KWH_ROW}", fmt=FMT_KWH, bold=True)
    _headers(
        ws,
        RANGE_HEADER,
        ["Share of the range", "HP customers", "Non-HP customers", "Scale", "Weighted kWh"],
    )
    for i in range(len(RANGE_STEPS)):
        row = RANGE_FIRST + i
        _put(ws, row, 1, f"=revenue!A{row}")
        _put(ws, row, 2, f"=revenue!B{row}", fmt=FMT_COUNT)
        _put(ws, row, 3, f"=$B${PAYERS_RATE_YEAR_ROW}-B{row}", fmt=FMT_COUNT)
        _put(ws, row, 4, f"=C{row}/$B$5", fmt=FMT_WEIGHT)
        _put(ws, row, 5, f"=$B$6*D{row}", fmt=FMT_KWH)
    ws.freeze_panes = "B8"
    ws.column_dimensions["A"].width = 42
    for col in range(2, 6):
        ws.column_dimensions[get_column_letter(col)].width = 24


def _write_increase(wb: Workbook) -> None:
    ws = wb.create_sheet("increase")
    _heading(ws, 1, "Rate 1 charge increase")
    _note(
        ws,
        2,
        "Each increase is that step's revenue reduction divided by that step's weighted kWh on payers. "
        "Distribution and transmission are separate, and T&D adds them. The bill columns multiply annual "
        "kWh by the T&D charge. The customer charge and generation do not change.",
        4,
        height=60,
    )
    _headers(
        ws,
        RANGE_HEADER,
        [
            "Share of the range",
            "Distribution ($/kWh)",
            "Transmission ($/kWh)",
            "T&D ($/kWh)",
        ],
    )
    for i in range(len(RANGE_STEPS)):
        row = RANGE_FIRST + i
        _put(ws, row, 1, f"=revenue!A{row}")
        _put(ws, row, 2, f"=revenue!C{row}/payers!E{row}", fmt=FMT_RATE)
        _put(ws, row, 3, f"=revenue!D{row}/payers!E{row}", fmt=FMT_RATE)
        _put(ws, row, 4, f"=B{row}+C{row}", fmt=FMT_RATE)
    ws.freeze_panes = "B8"
    ws.column_dimensions["A"].width = 42
    for col in range(2, 5):
        ws.column_dimensions[get_column_letter(col)].width = 26


def _weighted_mean(column: str, last: int) -> str:
    first = CUSTOMERS_FIRST
    weights = f"customers!B{first}:B{last}"
    return f"=SUMPRODUCT(customers!{column}{first}:{column}{last},{weights})/customers!$B${CUSTOMERS_WEIGHT_ROW}"


def _percentile(column: str, share: float, last: int) -> str:
    """Bill at the first home, in kWh order, whose running sample weight reaches ``share``."""
    first = CUSTOMERS_FIRST
    running = f"SCAN(0,customers!$B${first}:$B{last},LAMBDA(acc,w,acc+w))"
    target = f"{share:.2f}*customers!$B${CUSTOMERS_WEIGHT_ROW}"
    return f"=INDEX(customers!{column}${first}:{column}{last},XMATCH({target},{running},1))"


def _write_summary(wb: Workbook, last: int) -> None:
    ws = wb.create_sheet("summary")
    _heading(ws, 1, "Bill increase")
    _note(
        ws,
        2,
        "Annual bill increase for residential customers who are not on Rate HP, at each step from the floor "
        "to the ceiling. The mean bill is weighted by the ResStock sample weight. Revenue / customers divides "
        "the revenue reduction by the customers who remain on payers, and it matches the mean bill. A percentile "
        "is the first home in the kWh sort whose running sample weight reaches that share. Non-residential "
        "customers, including Rate 39 and Rate 57, are outside this sheet. Their bill impact is zero.",
        7,
        height=60,
    )
    _headers(ws, SUMMARY_HEADER, ["Stat", *(label for label, _fraction in RANGE_STEPS)])
    component_rows = [
        (SUMMARY_MEAN_DIST, "Mean distribution", "C"),
        (SUMMARY_MEAN_TX, "Mean transmission", "D"),
        (SUMMARY_PER_CUSTOMER, "Revenue / customers", "E"),
    ]
    for row, label, revenue_col in component_rows:
        _put(ws, row, 1, label)
        for step in range(len(RANGE_STEPS)):
            source = RANGE_FIRST + step
            _put(ws, row, 2 + step, f"=revenue!{revenue_col}{source}/payers!C{source}", fmt=FMT_BILL)
    _put(ws, SUMMARY_MEAN_BILL, 1, "Mean bill", bold=True)
    for step in range(len(RANGE_STEPS)):
        column = get_column_letter(5 + step)
        _put(ws, SUMMARY_MEAN_BILL, 2 + step, _weighted_mean(column, last), fmt=FMT_BILL, bold=True)
    for i, (label, share) in enumerate(QUANTILES):
        row = SUMMARY_QUANTILE_FIRST + i
        _put(ws, row, 1, label, bold=label == "Median")
        for step in range(len(RANGE_STEPS)):
            column = get_column_letter(5 + step)
            _put(ws, row, 2 + step, _percentile(column, share, last), fmt=FMT_BILL, bold=label == "Median")
    ws.column_dimensions["A"].width = 24
    for col in range(2, 8):
        ws.column_dimensions[get_column_letter(col)].width = 16


def build_workbook(
    floor: RevenueRow,
    ceiling: RevenueRow,
    buildings: pl.DataFrame,
    *,
    per_customer_distribution: float,
    per_customer_transmission: float,
    rate_year_customers: float,
) -> Workbook:
    """Assemble the CIEC-6(c) workpaper. Inputs are values; the results are formulas."""
    _check_revenue(floor, ceiling)
    _check_rate_year(rate_year_customers, floor, ceiling)
    _check_per_customer(floor, ceiling, per_customer_distribution, per_customer_transmission)
    rows = _customers(buildings)
    wb = Workbook()
    _write_readme(wb)
    _write_revenue(wb, floor, ceiling, per_customer_distribution, per_customer_transmission)
    _write_payers(wb, rate_year_customers)
    last = _write_customers(wb, rows)
    _write_increase(wb)
    _write_summary(wb, last)
    return wb
