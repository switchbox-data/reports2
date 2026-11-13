"""Helpers for the CIEC-2(d) Excel workpaper.

``ciec_request_2d.qmd`` computes the per-year RDM and TAC impact of
auto-enrolling existing heat pump customers in Rate HP on non-residential
classes.  This workbook lays out the inputs and formulas so reviewers can
trace every number.

Sheets
------
README
    What the file is and how the sheets connect.
inputs
    Per-customer revenue decrease, existing-customer count, RDM/TAC
    allocation shares, and company-wide billed sales.  Yellow cells are
    inputs.
shortfall
    Annual distribution and transmission shortfall, non-residential share,
    and the RDM per-kWh impact.  Every number is a formula referencing
    the inputs sheet.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.worksheet import Worksheet

DRIVE_FOLDER_ID = "1nHGEJetAsVbGx2XG-ltaQ9aebba_Pl5c"
DRIVE_NAME = "CIEC-2d_rdm_tac_nonres_impact.xlsx"

INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
HEADER_FONT = Font(bold=True)
TITLE_FONT = Font(bold=True, size=14)
WRAP = Alignment(wrap_text=True, vertical="top")
FMT_DOLLAR = "#,##0.00"
FMT_REVENUE = "$#,##0"
FMT_COUNT = "#,##0"
FMT_PCT = "0.00%"
FMT_CENTS = "0.000"
FMT_MWH = "#,##0.00"


@dataclass
class Inputs:
    """All inputs to the shortfall calculation."""

    dec_dist: float
    dec_tx: float
    existing_customers: int
    rdm_total_mwh: float
    residential_mwh: float
    tac_total_kw: float
    tac_res_kw: float


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


def _write_readme(wb: Workbook) -> None:
    ws = wb.active
    ws.title = "README"
    lines = [
        ("CIEC-2(d) workpaper", True),
        (
            "Docket No. 26-05-10. Witness: Juan-Pablo Velez. Request from Connecticut Industrial Energy Consumers.",
            False,
        ),
        (
            "RDM and TAC impact of auto-enrolling existing heat pump customers in Rate HP on non-residential classes.",
            False,
        ),
        ("", False),
        ("Yellow cells are inputs. Every other number is a formula.", True),
        ("", False),
        ("inputs", True),
        (
            "Per-customer revenue decrease (distribution and transmission) from "
            "CIEC-1(a).  Existing-customer count from CIEC-1(b).  "
            "Company-wide billed MWh from Exhibit CLP-RATES-2 at 3.  "
            "TAC demand allocation from Docket 26-01-03 Exhibit 4 at 4.",
            False,
        ),
        ("", False),
        ("shortfall", True),
        (
            "Annual distribution and transmission shortfall = existing customers * "
            "per-customer decrease.  Non-residential share = shortfall * allocation "
            "share (kWh for RDM, demand for TAC).  RDM cents/kWh = distribution shortfall "
            "/ company-wide kWh.",
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
    for row in (8, 11):
        ws.row_dimensions[row].height = 48


def _write_inputs(wb: Workbook, inp: Inputs) -> dict[str, str]:
    """Write the inputs sheet and return cell references for the shortfall sheet."""
    ws = wb.create_sheet("inputs")
    _heading(ws, 1, "Inputs")

    r = 3
    _put(ws, r, 1, "Per-existing-customer revenue decrease", bold=True)
    r += 1
    _put(ws, r, 1, "Distribution (annual)")
    _put(ws, r, 2, inp.dec_dist, input_=True, fmt=FMT_DOLLAR)
    _put(ws, r, 3, "CIEC-1(a), representative home", wrap=True)
    dec_dist_cell = f"B{r}"
    r += 1
    _put(ws, r, 1, "Transmission (annual)")
    _put(ws, r, 2, inp.dec_tx, input_=True, fmt=FMT_DOLLAR)
    _put(ws, r, 3, "CIEC-1(a), representative home", wrap=True)
    dec_tx_cell = f"B{r}"
    r += 1
    _put(ws, r, 1, "T&D total")
    _put(ws, r, 2, f"={dec_dist_cell}+{dec_tx_cell}", fmt=FMT_DOLLAR, bold=True)

    r += 2
    _put(ws, r, 1, "Existing heat pump customers", bold=True)
    r += 1
    _put(ws, r, 1, "Count (auto-enrolled)")
    _put(ws, r, 2, inp.existing_customers, input_=True, fmt=FMT_COUNT)
    _put(ws, r, 3, "CIEC-1(b), EnergizeCT installations rounded to thousand", wrap=True)
    existing_cell = f"B{r}"

    r += 2
    _put(ws, r, 1, "RDM allocation (by kWh)", bold=True)
    r += 1
    _put(ws, r, 1, "Company-wide billed sales (MWh)")
    _put(ws, r, 2, inp.rdm_total_mwh, input_=True, fmt=FMT_MWH)
    _put(ws, r, 3, "Exhibit CLP-RATES-2 at 3, all retail classes", wrap=True)
    rdm_total_cell = f"B{r}"
    r += 1
    _put(ws, r, 1, "Residential billed sales (MWh)")
    _put(ws, r, 2, inp.residential_mwh, input_=True, fmt=FMT_MWH)
    _put(ws, r, 3, "Rates 1, 5, and 7", wrap=True)
    res_mwh_cell = f"B{r}"
    r += 1
    _put(ws, r, 1, "Non-residential share")
    _put(ws, r, 2, f"=1-{res_mwh_cell}/{rdm_total_cell}", fmt=FMT_PCT, bold=True)
    nonres_kwh_cell = f"B{r}"

    r += 2
    _put(ws, r, 1, "TAC allocation (by demand at 12 monthly system peaks)", bold=True)
    r += 1
    _put(ws, r, 1, "Company-wide demand (kW)")
    _put(ws, r, 2, inp.tac_total_kw, input_=True, fmt="#,##0.0")
    _put(ws, r, 3, "Docket 26-01-03, Exhibit 4 at 4", wrap=True)
    tac_total_cell = f"B{r}"
    r += 1
    _put(ws, r, 1, "Residential demand (kW)")
    _put(ws, r, 2, inp.tac_res_kw, input_=True, fmt="#,##0.0")
    _put(ws, r, 3, "Rates 1+7 and Rate 5", wrap=True)
    tac_res_cell = f"B{r}"
    r += 1
    _put(ws, r, 1, "Non-residential share")
    _put(ws, r, 2, f"=1-{tac_res_cell}/{tac_total_cell}", fmt=FMT_PCT, bold=True)
    nonres_demand_cell = f"B{r}"

    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 56

    return {
        "dec_dist": dec_dist_cell,
        "dec_tx": dec_tx_cell,
        "existing": existing_cell,
        "rdm_total": rdm_total_cell,
        "nonres_kwh": nonres_kwh_cell,
        "nonres_demand": nonres_demand_cell,
    }


def _write_shortfall(wb: Workbook, refs: dict[str, str]) -> None:
    """Write the shortfall sheet with formulas referencing the inputs sheet."""
    ws = wb.create_sheet("shortfall")
    _heading(ws, 1, "Annual shortfall and non-residential impact")
    _put(
        ws,
        2,
        1,
        "All numbers are formulas referencing the inputs sheet. "
        "The shortfall is the same every year: existing customers are enrolled once.",
        wrap=True,
    )
    ws.merge_cells("A2:E2")
    ws.row_dimensions[2].height = 32

    dec_dist = f"inputs!{refs['dec_dist']}"
    dec_tx = f"inputs!{refs['dec_tx']}"
    existing = f"inputs!{refs['existing']}"
    rdm_total = f"inputs!{refs['rdm_total']}"
    nonres_kwh = f"inputs!{refs['nonres_kwh']}"
    nonres_demand = f"inputs!{refs['nonres_demand']}"

    r = 4
    _put(ws, r, 1, "Annual shortfall", bold=True)
    r += 1
    headers = ["", "Distribution", "Transmission", "T&D total"]
    for col, h in enumerate(headers, start=1):
        _put(ws, r, col, h, bold=True)
    r += 1
    _put(ws, r, 1, "Total shortfall")
    _put(ws, r, 2, f"={existing}*{dec_dist}", fmt=FMT_REVENUE)
    _put(ws, r, 3, f"={existing}*{dec_tx}", fmt=FMT_REVENUE)
    _put(ws, r, 4, f"=B{r}+C{r}", fmt=FMT_REVENUE)
    total_dist = f"B{r}"
    total_tx = f"C{r}"
    r += 1
    _put(ws, r, 1, "Non-residential share")
    _put(ws, r, 2, f"={total_dist}*{nonres_kwh}", fmt=FMT_REVENUE)
    _put(ws, r, 3, f"={total_tx}*{nonres_demand}", fmt=FMT_REVENUE)
    _put(ws, r, 4, f"=B{r}+C{r}", fmt=FMT_REVENUE)

    r += 2
    _put(ws, r, 1, "RDM per-kWh impact", bold=True)
    r += 1
    _put(ws, r, 1, "¢/kWh")
    _put(ws, r, 2, f"={total_dist}/({rdm_total}*1000)*100", fmt=FMT_CENTS)
    _put(ws, r, 3, "Distribution shortfall ÷ company-wide kWh", wrap=True)

    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 22
    ws.column_dimensions["E"].width = 50


def build_workbook(inp: Inputs) -> Workbook:
    wb = Workbook()
    _write_readme(wb)
    refs = _write_inputs(wb, inp)
    _write_shortfall(wb, refs)
    return wb


def upload_xlsx(path: Path, folder_id: str, name: str) -> str:
    """Upload the workbook to Drive, overwriting a file of the same name."""
    from build_ciec_1a_workbook import upload_xlsx as _upload

    return _upload(path, folder_id, name)
