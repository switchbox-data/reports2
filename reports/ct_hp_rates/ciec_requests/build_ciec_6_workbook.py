"""Helpers for the CIEC-6(c) Excel workpaper.

``ciec_request_6.qmd`` loads the year-by-year net revenue data from CIEC-3(c)
and calls :func:`build_workbook`. Upload uses
:func:`build_ciec_1a_workbook.upload_xlsx`. Yellow cells are inputs. Every
other number is a formula.

Sheets
------
README
    What the file is and how the sheets connect.
bill_impact
    Mean annual and monthly bill increase for residential customers who are not
    on Rate HP. One row per rate year, with floor and ceiling enrollment bounds
    side by side. Net revenue and remaining customers are inputs; the mean bill
    is a formula (net revenue / remaining customers), and the monthly mean
    divides that by 12.
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
            raise ValueError(f"{label} year {r['year']}: remaining customers must be positive")


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
            "Mean annual bill increase for residential customers who do not take Rate HP. "
            "The net revenue reduction (from CIEC-1(a) and CIEC-3(c)) is recovered from "
            "those customers. The mean bill increase is the net revenue divided by the "
            "customers who remain. Non-residential customers, including Rate 39 and Rate 57, "
            "are not charged.",
            False,
        ),
        ("", False),
        ("Yellow cells are inputs. Every other number is a formula.", True),
        ("", False),
        ("bill_impact", True),
        (
            "One row per rate year. Floor and ceiling refer to the enrollment bounds from "
            "CIEC-1(b) and CIEC-1(c). Net revenue and remaining customers are inputs. "
            "The mean annual bill increase is net revenue divided by remaining customers. "
            "The mean monthly bill increase divides that by 12.",
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
    ws.row_dimensions[8].height = 48


def _write_bill_impact(
    wb: Workbook,
    floor_rows: Sequence[dict[str, float]],
    ceiling_rows: Sequence[dict[str, float]],
) -> None:
    ws = wb.create_sheet("bill_impact")
    _heading(ws, 1, "Mean bill increase")
    _note(
        ws,
        2,
        "Mean annual and monthly bill increase for residential customers not on Rate HP. "
        "Net revenue and remaining customers are inputs from CIEC-1(a) and CIEC-3(c). "
        "Mean annual bill = net revenue / remaining customers. Mean monthly = annual / 12.",
        9,
    )
    _headers(
        ws,
        HEADER_ROW,
        [
            "Year",
            "Floor net revenue",
            "Floor remaining customers",
            "Floor mean annual bill",
            "Floor mean monthly bill",
            "Ceiling net revenue",
            "Ceiling remaining customers",
            "Ceiling mean annual bill",
            "Ceiling mean monthly bill",
        ],
    )
    for i, (fl, cl) in enumerate(zip(floor_rows, ceiling_rows, strict=True)):
        row = FIRST_ROW + i
        _put(ws, row, 1, int(fl["year"]))
        # Floor
        net_floor = round(float(fl["net_reduction_dist"]) + float(fl["net_reduction_tx"]))
        _put(ws, row, 2, net_floor, input_=True, fmt=FMT_REVENUE)
        _put(ws, row, 3, round(float(fl["nonhp_customers"])), input_=True, fmt=FMT_COUNT)
        _put(ws, row, 4, f"=B{row}/C{row}", fmt=FMT_BILL)
        _put(ws, row, 5, f"=D{row}/12", fmt=FMT_BILL)
        # Ceiling
        net_ceiling = round(float(cl["net_reduction_dist"]) + float(cl["net_reduction_tx"]))
        _put(ws, row, 6, net_ceiling, input_=True, fmt=FMT_REVENUE)
        _put(ws, row, 7, round(float(cl["nonhp_customers"])), input_=True, fmt=FMT_COUNT)
        _put(ws, row, 8, f"=F{row}/G{row}", fmt=FMT_BILL)
        _put(ws, row, 9, f"=H{row}/12", fmt=FMT_BILL)
    ws.freeze_panes = "B5"
    ws.column_dimensions["A"].width = 10
    for col in range(2, 10):
        ws.column_dimensions[get_column_letter(col)].width = 24


def build_workbook(
    floor_rows: Sequence[dict[str, float]],
    ceiling_rows: Sequence[dict[str, float]],
) -> Workbook:
    """Assemble the CIEC-6(c) workpaper. Inputs are values; the results are formulas."""
    _validate(floor_rows, "floor")
    _validate(ceiling_rows, "ceiling")
    if len(floor_rows) != len(ceiling_rows):
        raise ValueError(f"floor has {len(floor_rows)} rows but ceiling has {len(ceiling_rows)}")
    wb = Workbook()
    _write_readme(wb)
    _write_bill_impact(wb, floor_rows, ceiling_rows)
    return wb
