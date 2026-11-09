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
    Floor and ceiling distribution and transmission reductions for the
    customers already on a heat pump who would be auto-enrolled. These are
    the CIEC-1(a) dollars for that stock, pasted as values. Later installers
    are not included. T&D adds the two components.
payers
    Heat pump customers who move to Rate HP, and the residential customers who
    remain. Customers who remain are the Rate Year residential count minus the
    customers who move. The summary divides the revenue reduction by that count.
customers
    One row per Eversource home without a heat pump, sorted by annual kWh.
    Weight is the ResStock sample weight. Bill columns multiply annual kWh by
    the per-kWh increase. That sort is also bill order.
increase
    The CIEC-3(c) distribution, transmission, and T&D charges in $/kWh, pasted
    as values. This sheet does not divide revenue by kWh.
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

REVENUE_HEADER = 4
REVENUE_ROW = 5
CUSTOMERS_KWH_ROW = 4
CUSTOMERS_COUNT_ROW = 5
CUSTOMERS_WEIGHT_ROW = 6
CUSTOMERS_HEADER = 7
CUSTOMERS_FIRST = 8
INCREASE_HEADER = 4
INCREASE_ROW = 5
SUMMARY_HEADER = 4
SUMMARY_MEAN_DIST = 5
SUMMARY_MEAN_TX = 6
SUMMARY_MEAN_BILL = 7
SUMMARY_PER_CUSTOMER = 8
SUMMARY_QUANTILE_FIRST = 9
PAYERS_RATE_YEAR_ROW = 4
PAYERS_FLOOR_HP_ROW = 5
PAYERS_FLOOR_NONHP_ROW = 6
PAYERS_CEILING_HP_ROW = 7
PAYERS_CEILING_NONHP_ROW = 8

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


@dataclass(frozen=True)
class ChargeRow:
    """Rate 1 charge increase in $/kWh, already calculated in CIEC-3(c).

    ``td`` is the distribution charge plus the transmission charge.
    """

    distribution: float
    transmission: float
    td: float


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


def _year_value(label: str) -> str | int:
    return int(label) if label.isdigit() else label


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
            "Floor and ceiling revenue reductions from CIEC-1(a) for the customers already enrolled, including "
            "the 2026 installations. Distribution and transmission are the values already calculated there, "
            "rounded to the dollar. This sheet does not recompute them. T&D adds the two components. "
            "Installations in 2027 through 2031 are not on this sheet.",
            False,
        ),
        ("", False),
        ("payers", True),
        (
            "Heat pump customers who move to Rate HP, and the residential customers who remain. The Rate Year "
            "count is an input, the average bills rendered for Rates 1, 5, and 7. Customers who remain are that "
            "count minus the customers who move. The summary divides the revenue reduction by the customers who remain.",
            False,
        ),
        ("", False),
        ("customers", True),
        (
            "One row per Eversource home without a heat pump in the ResStock baseline, sorted by annual kWh "
            "and then by bldg_id. Annual kWh is CAIRO grid consumption. Weight is the ResStock sample weight. "
            "Weighted kWh multiplies annual kWh by that weight. Each bill column multiplies annual kWh by the "
            "matching per-kWh increase from CIEC-3(c), which already divides by sales scaled to the customers "
            "who remain. Because every bill uses the same per-kWh charge, the kWh sort is also the order of the "
            "bill increase, and the percentiles on summary read that order. Scaling every weight by the same "
            "factor would not change those percentiles. Homes on Rate 5 and Rate 7 are included with Rate 1. "
            "Customers on Rate HP are not on this sheet.",
            False,
        ),
        ("", False),
        ("increase", True),
        (
            "Distribution, transmission, and T&D are the Rate 1 charge increases from CIEC-3(c), in dollars "
            "per kWh. They are inputs. This sheet does not divide the revenue reduction by kWh again. The "
            "customer charge and generation are unchanged and are not on this sheet.",
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


def _write_revenue(wb: Workbook, floor: RevenueRow, ceiling: RevenueRow) -> None:
    ws = wb.create_sheet("revenue")
    _heading(ws, 1, "Revenue reduction")
    _note(
        ws,
        2,
        "Annual revenue reduction from CIEC-1(a) for customers who would move from Rate 1 to Rate HP. "
        "The row is the starting stock, including the 2026 installations. Distribution and transmission "
        "are inputs, already rounded to the dollar. T&D adds them. Later heat pump installations are excluded.",
        9,
    )
    _headers(
        ws,
        REVENUE_HEADER,
        [
            "Year",
            "Floor customers",
            "Floor distribution",
            "Floor transmission",
            "Floor T&D",
            "Ceiling customers",
            "Ceiling distribution",
            "Ceiling transmission",
            "Ceiling T&D",
        ],
    )
    _put(ws, REVENUE_ROW, 1, _year_value(floor.label))
    _put(ws, REVENUE_ROW, 2, floor.customers, input_=True, fmt=FMT_COUNT)
    _put(ws, REVENUE_ROW, 3, floor.distribution, input_=True, fmt=FMT_REVENUE)
    _put(ws, REVENUE_ROW, 4, floor.transmission, input_=True, fmt=FMT_REVENUE)
    _put(ws, REVENUE_ROW, 5, f"=C{REVENUE_ROW}+D{REVENUE_ROW}", fmt=FMT_REVENUE)
    _put(ws, REVENUE_ROW, 6, ceiling.customers, input_=True, fmt=FMT_COUNT)
    _put(ws, REVENUE_ROW, 7, ceiling.distribution, input_=True, fmt=FMT_REVENUE)
    _put(ws, REVENUE_ROW, 8, ceiling.transmission, input_=True, fmt=FMT_REVENUE)
    _put(ws, REVENUE_ROW, 9, f"=G{REVENUE_ROW}+H{REVENUE_ROW}", fmt=FMT_REVENUE)
    ws.freeze_panes = "A5"
    ws.column_dimensions["A"].width = 14
    for col in range(2, 10):
        ws.column_dimensions[get_column_letter(col)].width = 22


def _write_customers(wb: Workbook, buildings: pl.DataFrame) -> int:
    ws = wb.create_sheet("customers")
    _heading(ws, 1, "Non-heat-pump bill increase")
    _note(
        ws,
        2,
        "Eversource homes without a heat pump, sorted by annual kWh. Annual kWh is CAIRO grid consumption. "
        "Weight is the ResStock sample weight. The bill columns multiply annual kWh by the per-kWh increase. "
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
            "floor distribution",
            "floor transmission",
            "floor bill",
            "ceiling distribution",
            "ceiling transmission",
            "ceiling bill",
        ],
    )
    for i, record in enumerate(buildings.iter_rows(named=True)):
        row = CUSTOMERS_FIRST + i
        _put(ws, row, 1, int(record["bldg_id"]), input_=True, fmt=FMT_COUNT)
        _put(ws, row, 2, float(record["weight"]), input_=True, fmt=FMT_WEIGHT)
        _put(ws, row, 3, float(record["annual_kwh"]), input_=True, fmt=FMT_KWH)
        _put(ws, row, 4, f"=B{row}*C{row}", fmt=FMT_KWH)
        _put(ws, row, 5, f"=C{row}*increase!$B${INCREASE_ROW}", fmt=FMT_BILL)
        _put(ws, row, 6, f"=C{row}*increase!$C${INCREASE_ROW}", fmt=FMT_BILL)
        _put(ws, row, 7, f"=E{row}+F{row}", fmt=FMT_BILL)
        _put(ws, row, 8, f"=C{row}*increase!$E${INCREASE_ROW}", fmt=FMT_BILL)
        _put(ws, row, 9, f"=C{row}*increase!$F${INCREASE_ROW}", fmt=FMT_BILL)
        _put(ws, row, 10, f"=H{row}+I{row}", fmt=FMT_BILL)
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
        "Heat pump customers who move from Rate 1 to Rate HP, and the residential customers who remain. "
        "The Rate Year count is the average bills rendered for Rates 1, 5, and 7. Customers who remain are "
        "that count minus the customers who move. The summary divides the revenue reduction by the customers "
        "who remain. The bill of each home is annual kWh times the CIEC-3(c) per-kWh charge.",
        2,
        height=64,
    )
    _put(ws, PAYERS_RATE_YEAR_ROW, 1, "Rate Year residential customers", bold=True)
    _put(ws, PAYERS_RATE_YEAR_ROW, 2, rate_year_customers, input_=True, fmt=FMT_COUNT, bold=True)
    _put(ws, PAYERS_FLOOR_HP_ROW, 1, "Floor HP customers")
    _put(ws, PAYERS_FLOOR_HP_ROW, 2, f"=revenue!B{REVENUE_ROW}", fmt=FMT_COUNT)
    _put(ws, PAYERS_FLOOR_NONHP_ROW, 1, "Floor non-HP customers", bold=True)
    _put(ws, PAYERS_FLOOR_NONHP_ROW, 2, f"=B{PAYERS_RATE_YEAR_ROW}-B{PAYERS_FLOOR_HP_ROW}", fmt=FMT_COUNT, bold=True)
    _put(ws, PAYERS_CEILING_HP_ROW, 1, "Ceiling HP customers")
    _put(ws, PAYERS_CEILING_HP_ROW, 2, f"=revenue!F{REVENUE_ROW}", fmt=FMT_COUNT)
    _put(ws, PAYERS_CEILING_NONHP_ROW, 1, "Ceiling non-HP customers", bold=True)
    _put(
        ws,
        PAYERS_CEILING_NONHP_ROW,
        2,
        f"=B{PAYERS_RATE_YEAR_ROW}-B{PAYERS_CEILING_HP_ROW}",
        fmt=FMT_COUNT,
        bold=True,
    )
    ws.column_dimensions["A"].width = 36
    ws.column_dimensions["B"].width = 18


def _check_charge(charge: ChargeRow, bound: str) -> None:
    if min(charge.distribution, charge.transmission, charge.td) < 0:
        raise ValueError(f"{bound} charge must be non-negative")


def _write_increase(wb: Workbook, label: str, floor: ChargeRow, ceiling: ChargeRow) -> None:
    ws = wb.create_sheet("increase")
    _heading(ws, 1, "Rate 1 charge increase")
    _note(
        ws,
        2,
        "Distribution, transmission, and T&D are the Rate 1 charge increases from CIEC-3(c), in dollars per kWh. "
        "They are inputs. This sheet does not divide the revenue reduction by kWh again. The bill columns "
        "multiply annual kWh by these charges. The customer charge and generation do not change.",
        7,
        height=60,
    )
    _headers(
        ws,
        INCREASE_HEADER,
        [
            "Year",
            "Floor distribution ($/kWh)",
            "Floor transmission ($/kWh)",
            "Floor T&D ($/kWh)",
            "Ceiling distribution ($/kWh)",
            "Ceiling transmission ($/kWh)",
            "Ceiling T&D ($/kWh)",
        ],
    )
    _put(ws, INCREASE_ROW, 1, _year_value(label))
    _put(ws, INCREASE_ROW, 2, floor.distribution, input_=True, fmt=FMT_RATE)
    _put(ws, INCREASE_ROW, 3, floor.transmission, input_=True, fmt=FMT_RATE)
    _put(ws, INCREASE_ROW, 4, floor.td, input_=True, fmt=FMT_RATE)
    _put(ws, INCREASE_ROW, 5, ceiling.distribution, input_=True, fmt=FMT_RATE)
    _put(ws, INCREASE_ROW, 6, ceiling.transmission, input_=True, fmt=FMT_RATE)
    _put(ws, INCREASE_ROW, 7, ceiling.td, input_=True, fmt=FMT_RATE)
    ws.freeze_panes = "B5"
    ws.column_dimensions["A"].width = 14
    for col in range(2, 8):
        ws.column_dimensions[get_column_letter(col)].width = 28


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
        "Annual bill increase for residential customers who are not on Rate HP. The mean is weighted by the "
        "ResStock sample weight. Revenue / customers divides the revenue reduction by the customers who remain "
        "on payers, and it matches the mean bill. A percentile is the first home in the kWh sort whose running "
        "sample weight reaches that share. Non-residential customers, including Rate 39 and Rate 57, are outside "
        "this sheet. Their bill impact is zero.",
        3,
        height=60,
    )
    _headers(ws, SUMMARY_HEADER, ["Stat", "Floor", "Ceiling"])
    rows = [
        (SUMMARY_MEAN_DIST, "Mean distribution", "E", "H"),
        (SUMMARY_MEAN_TX, "Mean transmission", "F", "I"),
        (SUMMARY_MEAN_BILL, "Mean bill", "G", "J"),
    ]
    for row, label, floor_col, ceiling_col in rows:
        _put(ws, row, 1, label, bold=row == SUMMARY_MEAN_BILL)
        _put(ws, row, 2, _weighted_mean(floor_col, last), fmt=FMT_BILL, bold=row == SUMMARY_MEAN_BILL)
        _put(ws, row, 3, _weighted_mean(ceiling_col, last), fmt=FMT_BILL, bold=row == SUMMARY_MEAN_BILL)
    _put(ws, SUMMARY_PER_CUSTOMER, 1, "Revenue / customers")
    _put(
        ws,
        SUMMARY_PER_CUSTOMER,
        2,
        f"=revenue!E{REVENUE_ROW}/payers!B{PAYERS_FLOOR_NONHP_ROW}",
        fmt=FMT_BILL,
    )
    _put(
        ws,
        SUMMARY_PER_CUSTOMER,
        3,
        f"=revenue!I{REVENUE_ROW}/payers!B{PAYERS_CEILING_NONHP_ROW}",
        fmt=FMT_BILL,
    )
    for i, (label, share) in enumerate(QUANTILES):
        row = SUMMARY_QUANTILE_FIRST + i
        _put(ws, row, 1, label, bold=label == "Median")
        _put(ws, row, 2, _percentile("G", share, last), fmt=FMT_BILL, bold=label == "Median")
        _put(ws, row, 3, _percentile("J", share, last), fmt=FMT_BILL, bold=label == "Median")
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 18


def build_workbook(
    floor: RevenueRow,
    ceiling: RevenueRow,
    buildings: pl.DataFrame,
    floor_charge: ChargeRow,
    ceiling_charge: ChargeRow,
    *,
    rate_year_customers: float,
) -> Workbook:
    """Assemble the CIEC-6(c) workpaper. Inputs are values; the results are formulas."""
    _check_revenue(floor, ceiling)
    _check_rate_year(rate_year_customers, floor, ceiling)
    _check_charge(floor_charge, "floor")
    _check_charge(ceiling_charge, "ceiling")
    rows = _customers(buildings)
    wb = Workbook()
    _write_readme(wb)
    _write_revenue(wb, floor, ceiling)
    _write_payers(wb, rate_year_customers)
    last = _write_customers(wb, rows)
    _write_increase(wb, floor.label, floor_charge, ceiling_charge)
    _write_summary(wb, last)
    return wb
