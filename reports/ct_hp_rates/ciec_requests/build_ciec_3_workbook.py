"""Helpers for the CIEC-3(c) Excel workpaper.

``ciec_request_3.qmd`` loads the CIEC-1 revenue reductions, the non-heat-pump
buildings, and today's Rate 1 charges, then calls :func:`build_workbook`.
Upload uses :func:`build_ciec_1a_workbook.upload_xlsx`. Yellow cells are inputs.
Every other number is a formula.

Sheets
------
README
    What the file is and how the sheets connect.
revenue
    Floor and ceiling distribution and transmission reductions for the
    customers already on a heat pump who would be auto-enrolled. These are
    the CIEC-1(a) dollars for that stock, pasted as values. Later installers
    are not included. T&D adds the two components.
nonhp_kwh
    One row per Eversource home without a heat pump. Annual kWh is CAIRO grid
    consumption. Weight is the ResStock sample weight. Weighted kWh is the product.
    The totals are sums, still on the ResStock weight.
payers
    For each revenue row, the heat pump customers who move to Rate HP and the
    residential customers who remain. Customers who remain are the Rate Year
    residential count minus the customers who move. Weighted kWh scales the
    ResStock total by that count over the ResStock weight sum.
rates
    Today's Rate 1 distribution, transmission, and twelve monthly generation
    charges. T&D and T&D-plus-generation are formulas. The increase sheet
    divides by them.
increase
    The auto-enrolled revenue reduction divided by that bound's weighted kWh
    on payers, and that increase as a share of the Rate 1 charges.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import polars as pl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DRIVE_NAME = "CIEC-3c_rate1_charge_increase.xlsx"

INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
HEADER_FONT = Font(bold=True)
TITLE_FONT = Font(bold=True, size=14)
WRAP = Alignment(wrap_text=True, vertical="top")
HEADER_ALIGN = Alignment(wrap_text=True, vertical="bottom")

FMT_KWH = "#,##0.000"
FMT_WEIGHT = "#,##0.000000"
FMT_RATE = "0.000000"
FMT_CENTS = "0.000"
FMT_REVENUE = "$#,##0"
FMT_COUNT = "#,##0"
FMT_PCT = "0.00%"

# Row map the increase formulas and the tests both rely on.
REVENUE_HEADER = 4
REVENUE_FIRST = 5
KWH_TOTAL_ROW = 4
KWH_CUSTOMERS_ROW = 6
KWH_HEADER = 7
KWH_FIRST = 8
RATES_DIST_ROW = 5
RATES_TX_ROW = 6
RATES_TD_ROW = 7
RATES_GEN_FIRST = 11
RATES_GEN_LAST = 22
RATES_AVG_ROW = 23
RATES_FULL_ROW = 25
INCREASE_HEADER = 4
INCREASE_FIRST = 5
PAYERS_RATE_YEAR_ROW = 4
PAYERS_RAW_CUSTOMERS_ROW = 5
PAYERS_RAW_KWH_ROW = 6
PAYERS_HEADER = 8
PAYERS_FIRST = 9


@dataclass(frozen=True)
class RevenueRow:
    """One year's revenue reduction, already calculated in CIEC-1.

    ``distribution`` and ``transmission`` are dollars, rounded to the dollar.
    ``label`` is ``"Existing"`` or a rate year such as ``"2027"``.
    """

    label: str
    customers: int
    distribution: float
    transmission: float


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


def _check_revenue(floor: Sequence[RevenueRow], ceiling: Sequence[RevenueRow]) -> None:
    if len(floor) == 0:
        raise ValueError("revenue rows are empty")
    floor_labels = [row.label for row in floor]
    ceiling_labels = [row.label for row in ceiling]
    if floor_labels != ceiling_labels:
        raise ValueError(f"revenue labels differ: {floor_labels} and {ceiling_labels}")
    if any(label == "" for label in floor_labels):
        raise ValueError("revenue label is empty")


def _check_rates(distribution: float, transmission: float, generation_monthly: Mapping[str, float]) -> list[float]:
    if distribution <= 0 or transmission <= 0:
        raise ValueError(f"rates must be positive, got distribution={distribution} and transmission={transmission}")
    expected = [f"2025-{month:02d}" for month in range(1, 13)]
    found = sorted(generation_monthly)
    if found != expected:
        raise ValueError(f"generation months {found} are not the twelve months of 2025")
    rates = [float(generation_monthly[key]) for key in expected]
    if any(rate <= 0 for rate in rates):
        raise ValueError(f"generation rates must be positive, got {rates}")
    return rates


def _buildings(buildings: pl.DataFrame) -> pl.DataFrame:
    missing = [name for name in ("bldg_id", "weight", "annual_kwh") if name not in buildings.columns]
    if missing:
        raise ValueError(f"buildings is missing {missing}")
    if buildings.height == 0:
        raise ValueError("buildings is empty")
    out = buildings.select("bldg_id", "weight", "annual_kwh").sort("bldg_id")
    if out["bldg_id"].n_unique() != out.height:
        raise ValueError("bldg_id is not unique")
    if out["weight"].null_count() or out["annual_kwh"].null_count():
        raise ValueError("weight or annual_kwh has nulls")
    total = float((out["annual_kwh"] * out["weight"]).sum())
    if total <= 0:
        raise ValueError(f"weighted kWh must be positive, got {total}")
    customers = float(out["weight"].sum())
    if customers <= 0:
        raise ValueError(f"weight must be positive, got {customers}")
    return out


def _write_readme(wb: Workbook) -> None:
    ws = wb.active
    ws.title = "README"
    lines = [
        ("CIEC-3(c) workpaper", True),
        (
            "Docket No. 26-05-10. Witness: Juan-Pablo Velez. Request from Connecticut Industrial Energy Consumers.",
            False,
        ),
        (
            "Increase in the Rate 1 distribution and transmission charges if the revenue no longer collected "
            "from auto-enrolled heat pump customers were recovered from residential customers who are not on Rate HP. "
            "Customers who install a heat pump later are not part of this recovery. Rate HP is calibrated so that "
            "a new heat pump customer pays the embedded-cost revenue requirement and the additional transmission "
            "and distribution marginal cost.",
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
        ("nonhp_kwh", True),
        (
            "One row per Eversource home without a heat pump in the ResStock baseline. Annual kWh is CAIRO "
            "grid consumption. Weight is the ResStock sample weight, before the Rate Year scale. Weighted kWh "
            "multiplies annual kWh by that weight. Homes on Rate 5 and Rate 7 are included with Rate 1. "
            "Customers on Rate HP are not on this sheet. The per-kWh increase divides by the scaled total on payers.",
            False,
        ),
        ("", False),
        ("payers", True),
        (
            "Heat pump customers who move to Rate HP, and the residential customers who remain and pay the "
            "increase. The Rate Year count is an input, the average bills rendered for Rates 1, 5, and 7. "
            "Customers who remain are that count minus the customers who move. The scale is the customers who "
            "remain divided by the ResStock weight sum. Weighted kWh is the ResStock weighted kWh times that scale. "
            "Floor and ceiling each have their own scale, because a different number of customers move.",
            False,
        ),
        ("", False),
        ("rates", True),
        (
            "Today's Rate 1 charges, the denominators of the percent change. Distribution includes riders and "
            "is flat across months. Transmission is flat across months. Generation is the twelve monthly supply "
            "rates, and the average is their mean. T&D is distribution plus transmission. T&D and generation "
            "adds that average. The customer charge is unchanged and is not part of these percents.",
            False,
        ),
        ("", False),
        ("increase", True),
        (
            "Each row divides that bound's revenue reduction by that bound's weighted kWh on payers. "
            "Distribution and transmission are separate. T&D adds them. % of T&D divides the combined increase "
            "by the T&D rate. % of T&D and generation divides it by T&D plus average generation.",
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
    for row in (8, 11, 14, 17, 20):
        ws.row_dimensions[row].height = 64


def _write_revenue(wb: Workbook, floor: Sequence[RevenueRow], ceiling: Sequence[RevenueRow]) -> None:
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
    for i, (left, right) in enumerate(zip(floor, ceiling, strict=True)):
        row = REVENUE_FIRST + i
        _put(ws, row, 1, _year_value(left.label))
        _put(ws, row, 2, left.customers, input_=True, fmt=FMT_COUNT)
        _put(ws, row, 3, left.distribution, input_=True, fmt=FMT_REVENUE)
        _put(ws, row, 4, left.transmission, input_=True, fmt=FMT_REVENUE)
        _put(ws, row, 5, f"=C{row}+D{row}", fmt=FMT_REVENUE)
        _put(ws, row, 6, right.customers, input_=True, fmt=FMT_COUNT)
        _put(ws, row, 7, right.distribution, input_=True, fmt=FMT_REVENUE)
        _put(ws, row, 8, right.transmission, input_=True, fmt=FMT_REVENUE)
        _put(ws, row, 9, f"=G{row}+H{row}", fmt=FMT_REVENUE)
    ws.freeze_panes = "A5"
    ws.column_dimensions["A"].width = 14
    for col in range(2, 10):
        ws.column_dimensions[get_column_letter(col)].width = 22


def _write_kwh(wb: Workbook, buildings: pl.DataFrame) -> None:
    ws = wb.create_sheet("nonhp_kwh")
    _heading(ws, 1, "Non-heat-pump electricity use")
    _note(
        ws,
        2,
        "Eversource homes without a heat pump in the ResStock baseline. Annual kWh is CAIRO grid consumption, "
        "the same billing basis as the heat pump bill in CIEC-1(a). Weight is the ResStock sample weight. "
        "Weighted kWh is annual kWh times that weight. The payers sheet scales this total. Homes on Rate 5 and "
        "Rate 7 are included with Rate 1.",
        4,
        height=48,
    )
    last = KWH_FIRST + buildings.height - 1
    _put(ws, KWH_TOTAL_ROW, 1, "Total weighted kWh", bold=True)
    _put(ws, KWH_TOTAL_ROW, 2, f"=SUM(D{KWH_FIRST}:D{last})", fmt=FMT_KWH, bold=True)
    _put(ws, 5, 1, "Buildings", bold=True)
    _put(ws, 5, 2, f"=COUNTA(A{KWH_FIRST}:A{last})", fmt=FMT_COUNT, bold=True)
    _put(ws, KWH_CUSTOMERS_ROW, 1, "ResStock customers", bold=True)
    _put(ws, KWH_CUSTOMERS_ROW, 2, f"=SUM(B{KWH_FIRST}:B{last})", fmt=FMT_WEIGHT, bold=True)
    _headers(ws, KWH_HEADER, ["bldg_id", "weight", "annual kWh", "weighted kWh"])
    for i, record in enumerate(buildings.iter_rows(named=True)):
        row = KWH_FIRST + i
        _put(ws, row, 1, int(record["bldg_id"]), input_=True, fmt=FMT_COUNT)
        _put(ws, row, 2, float(record["weight"]), input_=True, fmt=FMT_WEIGHT)
        _put(ws, row, 3, float(record["annual_kwh"]), input_=True, fmt=FMT_KWH)
        _put(ws, row, 4, f"=B{row}*C{row}", fmt=FMT_KWH)
    ws.freeze_panes = "A8"
    ws.auto_filter.ref = f"A{KWH_HEADER}:D{last}"
    ws.column_dimensions["A"].width = 22
    for col in range(2, 5):
        ws.column_dimensions[get_column_letter(col)].width = 20


def _write_rates(
    wb: Workbook,
    distribution: float,
    transmission: float,
    generation: Sequence[float],
) -> None:
    ws = wb.create_sheet("rates")
    _heading(ws, 1, "Rate 1 charges")
    _note(
        ws,
        2,
        "Today's Rate 1 charges, used as the denominators of the percent change. Distribution includes riders. "
        "Transmission is separate. Both are flat across months. Generation is the twelve monthly supply rates. "
        "The customer charge is unchanged and is not part of these percents.",
        5,
    )
    _headers(ws, 4, ["Component", "Unit", "$/kWh", "¢/kWh", "Note"])
    _put(ws, RATES_DIST_ROW, 1, "Distribution")
    _put(ws, RATES_DIST_ROW, 2, "$/kWh")
    _put(ws, RATES_DIST_ROW, 3, distribution, input_=True, fmt=FMT_RATE)
    _put(ws, RATES_DIST_ROW, 4, f"=C{RATES_DIST_ROW}*100", fmt=FMT_CENTS)
    _put(ws, RATES_DIST_ROW, 5, "Includes riders. Flat across months.", wrap=True)
    _put(ws, RATES_TX_ROW, 1, "Transmission")
    _put(ws, RATES_TX_ROW, 2, "$/kWh")
    _put(ws, RATES_TX_ROW, 3, transmission, input_=True, fmt=FMT_RATE)
    _put(ws, RATES_TX_ROW, 4, f"=C{RATES_TX_ROW}*100", fmt=FMT_CENTS)
    _put(ws, RATES_TX_ROW, 5, "Flat across months.", wrap=True)
    _put(ws, RATES_TD_ROW, 1, "T&D", bold=True)
    _put(ws, RATES_TD_ROW, 2, "$/kWh")
    _put(ws, RATES_TD_ROW, 3, f"=C{RATES_DIST_ROW}+C{RATES_TX_ROW}", fmt=FMT_RATE, bold=True)
    _put(ws, RATES_TD_ROW, 4, f"=C{RATES_TD_ROW}*100", fmt=FMT_CENTS, bold=True)
    _put(ws, RATES_TD_ROW, 5, "Denominator of % of T&D.", wrap=True)

    _put(ws, 9, 1, "Generation", bold=True)
    _headers(ws, 10, ["Month", "Unit", "$/kWh", "¢/kWh", "Note"])
    for i, (month, rate) in enumerate(zip(MONTHS, generation, strict=True)):
        row = RATES_GEN_FIRST + i
        _put(ws, row, 1, month)
        _put(ws, row, 2, "$/kWh")
        _put(ws, row, 3, rate, input_=True, fmt=FMT_RATE)
        _put(ws, row, 4, f"=C{row}*100", fmt=FMT_CENTS)
    _put(ws, RATES_AVG_ROW, 1, "Average", bold=True)
    _put(ws, RATES_AVG_ROW, 2, "$/kWh")
    _put(
        ws,
        RATES_AVG_ROW,
        3,
        f"=AVERAGE(C{RATES_GEN_FIRST}:C{RATES_GEN_LAST})",
        fmt=FMT_RATE,
        bold=True,
    )
    _put(ws, RATES_AVG_ROW, 4, f"=C{RATES_AVG_ROW}*100", fmt=FMT_CENTS, bold=True)
    _put(ws, RATES_AVG_ROW, 5, "Mean of the twelve monthly rates.", wrap=True)

    _put(ws, RATES_FULL_ROW, 1, "T&D and generation", bold=True)
    _put(ws, RATES_FULL_ROW, 2, "$/kWh")
    _put(ws, RATES_FULL_ROW, 3, f"=C{RATES_TD_ROW}+C{RATES_AVG_ROW}", fmt=FMT_RATE, bold=True)
    _put(ws, RATES_FULL_ROW, 4, f"=C{RATES_FULL_ROW}*100", fmt=FMT_CENTS, bold=True)
    _put(ws, RATES_FULL_ROW, 5, "Denominator of % of T&D and generation.", wrap=True)

    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 12
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 14
    ws.column_dimensions["E"].width = 48


def _check_rate_year(rate_year_customers: float, floor: Sequence[RevenueRow], ceiling: Sequence[RevenueRow]) -> None:
    if rate_year_customers <= 0:
        raise ValueError(f"Rate Year customers must be positive, got {rate_year_customers}")
    for left, right in zip(floor, ceiling, strict=True):
        if left.customers >= rate_year_customers or right.customers >= rate_year_customers:
            raise ValueError(
                f"enrolled customers leave nobody to pay: Rate Year {rate_year_customers}, "
                f"floor {left.customers}, ceiling {right.customers}"
            )


def _write_payers(wb: Workbook, n_years: int, rate_year_customers: float) -> None:
    ws = wb.create_sheet("payers")
    _heading(ws, 1, "Customers who move and customers who pay")
    _note(
        ws,
        2,
        "Heat pump customers who move from Rate 1 to Rate HP, and the residential customers who remain. "
        "The Rate Year count is the average bills rendered for Rates 1, 5, and 7. Customers who remain are "
        "that count minus the customers who move. The scale divides the customers who remain by the ResStock "
        "weight sum on nonhp_kwh. Weighted kWh multiplies the ResStock weighted kWh by that scale. The increase "
        "sheet divides each bound's revenue reduction by that bound's weighted kWh.",
        9,
        height=64,
    )
    _put(ws, PAYERS_RATE_YEAR_ROW, 1, "Rate Year residential customers", bold=True)
    _put(ws, PAYERS_RATE_YEAR_ROW, 2, rate_year_customers, input_=True, fmt=FMT_COUNT, bold=True)
    _put(ws, PAYERS_RAW_CUSTOMERS_ROW, 1, "ResStock non-HP customers", bold=True)
    _put(ws, PAYERS_RAW_CUSTOMERS_ROW, 2, f"=nonhp_kwh!B{KWH_CUSTOMERS_ROW}", fmt=FMT_WEIGHT, bold=True)
    _put(ws, PAYERS_RAW_KWH_ROW, 1, "ResStock non-HP kWh", bold=True)
    _put(ws, PAYERS_RAW_KWH_ROW, 2, f"=nonhp_kwh!B{KWH_TOTAL_ROW}", fmt=FMT_KWH, bold=True)
    _headers(
        ws,
        PAYERS_HEADER,
        [
            "Year",
            "Floor HP customers",
            "Floor non-HP customers",
            "Floor scale",
            "Floor weighted kWh",
            "Ceiling HP customers",
            "Ceiling non-HP customers",
            "Ceiling scale",
            "Ceiling weighted kWh",
        ],
    )
    for i in range(n_years):
        row = PAYERS_FIRST + i
        src = REVENUE_FIRST + i
        _put(ws, row, 1, f"=revenue!A{src}")
        _put(ws, row, 2, f"=revenue!B{src}", fmt=FMT_COUNT)
        _put(ws, row, 3, f"=$B${PAYERS_RATE_YEAR_ROW}-B{row}", fmt=FMT_COUNT)
        _put(ws, row, 4, f"=C{row}/$B${PAYERS_RAW_CUSTOMERS_ROW}", fmt=FMT_WEIGHT)
        _put(ws, row, 5, f"=$B${PAYERS_RAW_KWH_ROW}*D{row}", fmt=FMT_KWH)
        _put(ws, row, 6, f"=revenue!F{src}", fmt=FMT_COUNT)
        _put(ws, row, 7, f"=$B${PAYERS_RATE_YEAR_ROW}-F{row}", fmt=FMT_COUNT)
        _put(ws, row, 8, f"=G{row}/$B${PAYERS_RAW_CUSTOMERS_ROW}", fmt=FMT_WEIGHT)
        _put(ws, row, 9, f"=$B${PAYERS_RAW_KWH_ROW}*H{row}", fmt=FMT_KWH)
    ws.freeze_panes = "B9"
    ws.column_dimensions["A"].width = 36
    for col in range(2, 10):
        ws.column_dimensions[get_column_letter(col)].width = 26


def _write_increase(wb: Workbook, n_years: int) -> None:
    ws = wb.create_sheet("increase")
    _heading(ws, 1, "Rate 1 charge increase")
    _note(
        ws,
        2,
        "Each increase is that bound's auto-enrolled revenue reduction divided by that bound's weighted kWh on payers. "
        "Distribution and transmission are separate, and T&D adds them. % of T&D divides the combined "
        "increase by the T&D rate. % of T&D and generation divides it by T&D plus average generation.",
        11,
    )
    _headers(
        ws,
        INCREASE_HEADER,
        [
            "Year",
            "Floor distribution ($/kWh)",
            "Floor transmission ($/kWh)",
            "Floor T&D ($/kWh)",
            "Floor % of T&D",
            "Floor % of T&D and generation",
            "Ceiling distribution ($/kWh)",
            "Ceiling transmission ($/kWh)",
            "Ceiling T&D ($/kWh)",
            "Ceiling % of T&D",
            "Ceiling % of T&D and generation",
        ],
    )
    for i in range(n_years):
        row = INCREASE_FIRST + i
        src = REVENUE_FIRST + i
        _put(ws, row, 1, f"=revenue!A{src}")
        payers = PAYERS_FIRST + i
        _put(ws, row, 2, f"=revenue!C{src}/payers!E{payers}", fmt=FMT_RATE)
        _put(ws, row, 3, f"=revenue!D{src}/payers!E{payers}", fmt=FMT_RATE)
        _put(ws, row, 4, f"=B{row}+C{row}", fmt=FMT_RATE)
        _put(ws, row, 5, f"=D{row}/rates!$C${RATES_TD_ROW}", fmt=FMT_PCT)
        _put(ws, row, 6, f"=D{row}/rates!$C${RATES_FULL_ROW}", fmt=FMT_PCT)
        _put(ws, row, 7, f"=revenue!G{src}/payers!I{payers}", fmt=FMT_RATE)
        _put(ws, row, 8, f"=revenue!H{src}/payers!I{payers}", fmt=FMT_RATE)
        _put(ws, row, 9, f"=G{row}+H{row}", fmt=FMT_RATE)
        _put(ws, row, 10, f"=I{row}/rates!$C${RATES_TD_ROW}", fmt=FMT_PCT)
        _put(ws, row, 11, f"=I{row}/rates!$C${RATES_FULL_ROW}", fmt=FMT_PCT)
    ws.freeze_panes = "B5"
    ws.column_dimensions["A"].width = 14
    for col in range(2, 12):
        ws.column_dimensions[get_column_letter(col)].width = 24


def build_workbook(
    floor: Sequence[RevenueRow],
    ceiling: Sequence[RevenueRow],
    buildings: pl.DataFrame,
    *,
    distribution: float,
    transmission: float,
    generation_monthly: Mapping[str, float],
    rate_year_customers: float,
) -> Workbook:
    """Assemble the CIEC-3(c) workpaper. Inputs are values; the results are formulas."""
    _check_revenue(floor, ceiling)
    _check_rate_year(rate_year_customers, floor, ceiling)
    generation = _check_rates(distribution, transmission, generation_monthly)
    rows = _buildings(buildings)
    wb = Workbook()
    _write_readme(wb)
    _write_revenue(wb, floor, ceiling)
    _write_kwh(wb, rows)
    _write_payers(wb, len(floor), rate_year_customers)
    _write_rates(wb, distribution, transmission, generation)
    _write_increase(wb, len(floor))
    return wb
