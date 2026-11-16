"""Helpers for the CIEC-6(c) Excel workpaper.

``ciec_request_6.qmd`` loads the year-by-year net revenue reductions and the
residential customers who remain from CIEC-3(c) and calls :func:`build_workbook`.
Upload uses :func:`build_ciec_1a_workbook.upload_xlsx`. Yellow cells are inputs.
Every other number is a formula.

Sheets
------
README
    What the file is and which row the response cites.
bill_impact
    Average annual and monthly bill increase for residential customers who are
    not on Rate HP. One row per rate year, low and high estimates of new heat
    pump customers side by side. Net revenue reduction (T&D) and customers who
    remain are inputs that match CIEC-3 Attachment 1; the averages are formulas.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

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

FMT_REVENUE = "$#,##0"
FMT_BILL = "$#,##0.00"
FMT_COUNT = "#,##0"

HEADER_ROW = 4
FIRST_ROW = 5


def net_revenue(row: dict[str, float]) -> int:
    """T&D net revenue reduction, rounded per component as on the CIEC-3 revenue sheet."""
    return round(float(row["net_reduction_dist"])) + round(float(row["net_reduction_tx"]))


def last_row(n_years: int) -> int:
    """Row of the last rate year on bill_impact, the row the response cites."""
    return FIRST_ROW + n_years - 1


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


def _validate(rows: Sequence[dict[str, float]], label: str) -> None:
    if not rows:
        raise ValueError(f"{label} rows are empty")
    for r in rows:
        for key in ("year", "net_reduction_dist", "net_reduction_tx", "nonhp_customers"):
            if key not in r:
                raise ValueError(f"{label} row missing key {key!r}")
        if float(r["nonhp_customers"]) <= 0:
            raise ValueError(f"{label} year {r['year']}: customers who remain must be positive")


def _write_readme(wb: Workbook) -> None:
    ws = wb.active
    assert ws is not None
    ws.title = "README"
    lines = [
        ("CIEC-6(c) workpaper", True),
        (
            "Docket No. 26-05-10. Witness: Juan-Pablo Velez. Request from Connecticut Industrial Energy Consumers.",
            False,
        ),
        (
            "Average bill increase for residential customers who are not on Rate HP, if the net revenue reduction "
            "from Rate HP were recovered solely from them, as in CIEC-3(c). The reduction comes from existing heat "
            "pump customers who are auto-enrolled in Rate HP. New heat pump customers who enroll at installation pay "
            "slightly more than they did before installing a heat pump, so they do not add to the reduction. The "
            "response to CIEC-6(c) cites 2031 under the high estimate of new heat pump customers (bill_impact sheet, "
            "last row). Non-residential customers are not on this sheet; see the response to CIEC-2(d).",
            False,
        ),
        ("", False),
        ("Yellow cells are inputs. Every other number is a formula.", True),
        ("", False),
        ("bill_impact", True),
        (
            "One row per rate year. Low and high are the estimates of new heat pump customers in CIEC-1(c). "
            "Net revenue reduction is the T&D column of the revenue sheet in CIEC-3 Attachment 1, and customers "
            "who remain is the column of that name on its payers sheet. The average annual bill increase divides "
            "the first by the second, which equals the CIEC-3(c) per-kWh increase times those customers' average "
            "annual kWh. The average monthly bill increase divides it by 12.",
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
    ws.row_dimensions[3].height = 64
    ws.row_dimensions[8].height = 64


def _write_bill_impact(
    wb: Workbook,
    low_rows: Sequence[dict[str, float]],
    high_rows: Sequence[dict[str, float]],
) -> None:
    ws = wb.create_sheet("bill_impact")
    _heading(ws, 1, "Average bill increase")
    _note(
        ws,
        2,
        "Net revenue reduction (CIEC-3 Attachment 1, revenue sheet, T&D) divided by the residential customers "
        "not on Rate HP (payers sheet, customers who remain). Low and high are the estimates of new heat pump "
        "customers in CIEC-1(c). The response to CIEC-6(c) cites 2031 under the high estimate.",
        9,
    )
    _headers(
        ws,
        HEADER_ROW,
        [
            "Rate year",
            "Low: net revenue reduction (T&D)",
            "Low: customers who remain",
            "Low: average annual bill increase",
            "Low: average monthly bill increase",
            "High: net revenue reduction (T&D)",
            "High: customers who remain",
            "High: average annual bill increase",
            "High: average monthly bill increase",
        ],
    )
    for i, (low, high) in enumerate(zip(low_rows, high_rows, strict=True)):
        row = FIRST_ROW + i
        _put(ws, row, 1, int(low["year"]))
        _put(ws, row, 2, net_revenue(low), input_=True, fmt=FMT_REVENUE)
        _put(ws, row, 3, round(float(low["nonhp_customers"])), input_=True, fmt=FMT_COUNT)
        _put(ws, row, 4, f"=B{row}/C{row}", fmt=FMT_BILL)
        _put(ws, row, 5, f"=D{row}/12", fmt=FMT_BILL)
        _put(ws, row, 6, net_revenue(high), input_=True, fmt=FMT_REVENUE)
        _put(ws, row, 7, round(float(high["nonhp_customers"])), input_=True, fmt=FMT_COUNT)
        _put(ws, row, 8, f"=F{row}/G{row}", fmt=FMT_BILL)
        _put(ws, row, 9, f"=H{row}/12", fmt=FMT_BILL)
    ws.freeze_panes = "B5"
    ws.column_dimensions["A"].width = 12
    for col in range(2, 10):
        ws.column_dimensions[get_column_letter(col)].width = 24


def build_workbook(
    low_rows: Sequence[dict[str, float]],
    high_rows: Sequence[dict[str, float]],
) -> Workbook:
    """Assemble the CIEC-6(c) workpaper. Inputs are values; the results are formulas."""
    _validate(low_rows, "low")
    _validate(high_rows, "high")
    if len(low_rows) != len(high_rows):
        raise ValueError(f"low has {len(low_rows)} rows but high has {len(high_rows)}")
    if [int(r["year"]) for r in low_rows] != [int(r["year"]) for r in high_rows]:
        raise ValueError("low and high rate years differ")
    wb = Workbook()
    _write_readme(wb)
    _write_bill_impact(wb, low_rows, high_rows)
    return wb
