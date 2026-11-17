"""Helpers for the CIEC-9(c) Excel workpaper.

``ciec_request_9.qmd`` asks what the average converting home's incremental
marginal T&D cost would be if the Company's system became winter peaking. This
workbook gives the home's hourly load before and after the heat pump, the
testimony's hourly marginal capacity costs, and the winter-peaking calculation
as formulas.

Sheets
------
README
    What the file is and what each column means.
hourly
    One row per hour: timestamp, season, load before and after (inputs), the
    added load (formula), the testimony's hourly distribution and bulk
    transmission marginal costs (inputs), each hour's rank by after-retrofit
    load within its season (formula), and the marginal costs reassigned by that
    rank (formulas). The results are formulas in columns M-N.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import polars as pl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

DRIVE_FOLDER_ID = "1sAypEVEBw3DO89Zlfrl5H0BF6GXna9gt"
DRIVE_NAME = "CIEC-9c_winter_peak_marginal_cost.xlsx"

HEADER_FONT = Font(bold=True)
TITLE_FONT = Font(bold=True, size=14)
INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
WRAP = Alignment(wrap_text=True, vertical="top")
FMT_TIMESTAMP = "yyyy-mm-dd hh:mm"
FMT_KWH = "0.0000"
FMT_MC = "0.000000"
FMT_DOLLAR = "$#,##0.00"
HOURS = 8760
WINTER = "Nov-Mar"
SUMMER = "Apr-Oct"
HOURLY_COLUMNS = ("timestamp", "season", "kwh_before", "kwh_after", "mc_dist", "mc_tx")


@dataclass
class Inputs:
    """The average home's hourly load, the hourly marginal costs, and the facts the README describes."""

    hourly: pl.DataFrame
    n_bldg: int
    overpay: float


def _write_readme(wb: Workbook, inp: Inputs) -> None:
    ws = wb.active
    ws.title = "README"
    lines = [
        ("CIEC-9(c) workpaper", True),
        (
            "Docket No. 26-05-10. Witness: Juan-Pablo Velez. Request from Connecticut Industrial Energy Consumers.",
            False,
        ),
        (
            "Illustrative upper bound on the average converting home's incremental marginal T&D cost if the "
            "Company's system became winter peaking. The testimony's hourly marginal capacity costs are sorted from "
            "highest to lowest and reassigned to the hours ranked by the home's load after installing a heat pump, "
            "within each season. This assumes the system peak always coincides with the home's highest-use hours.",
            False,
        ),
        (
            f"Load: the sample-weighted average of {inp.n_bldg:,} ResStock buildings served by Eversource and heated "
            "with natural gas, fuel oil, or propane before the retrofit, before and after the upgrade 2 heat pump "
            "retrofit. Same load and timestamps as Ex. JPV-3, sheets hourly_before and hourly_after.",
            False,
        ),
        ("Yellow cells are inputs; everything else is a formula.", False),
        ("", False),
        ("hourly", True),
        ("timestamp: Eastern Standard Time, hour beginning, on CAIRO's 2025 calendar.", False),
        ("season: Nov-Mar or Apr-Oct, by the month of the timestamp.", False),
        ("kwh_before, kwh_after: the average home's grid kWh before and after the retrofit.", False),
        ("kwh_added: kwh_after - kwh_before.", False),
        (
            "mc_dist, mc_tx: the testimony's hourly marginal distribution and bulk transmission capacity costs, "
            "$/kWh (Ex. JPV-3, sheet marginal_cost). Each column sums to its $/kW-year cost.",
            False,
        ),
        ("rank_in_season: 1 for the hour of highest kwh_after in its season, 2 for the next, and so on.", False),
        ("mc_dist_reassigned, mc_tx_reassigned: the rank_in_season-th largest value of mc_dist or mc_tx.", False),
        (
            "Columns M-N: the testimony's incremental marginal cost (hour by hour, as billed), the same "
            "reassignment applied to Apr-Oct as a check on how much it overstates, the winter-peaking cost, and "
            "the overpayment that would remain under Rate 1.",
            False,
        ),
    ]
    for row, (text, bold) in enumerate(lines, start=1):
        cell = ws.cell(row, 1, text)
        cell.alignment = WRAP
        if bold:
            cell.font = TITLE_FONT if row == 1 else HEADER_FONT
    ws.column_dimensions["A"].width = 120
    for row in (3, 4):
        ws.row_dimensions[row].height = 48


def _write_hourly(wb: Workbook, inp: Inputs) -> None:
    ws = wb.create_sheet("hourly")
    headers = [
        "timestamp",
        "season",
        "kwh_before",
        "kwh_after",
        "kwh_added",
        "mc_dist",
        "mc_tx",
        "rank_in_season",
        "mc_dist_reassigned",
        "mc_tx_reassigned",
    ]
    for col, header in enumerate(headers, start=1):
        ws.cell(1, col, header).font = HEADER_FONT

    last = inp.hourly.height + 1
    rng = {c: f"${c}$2:${c}${last}" for c in "BDEFGIJ"}
    for row, (ts, season, before, after, mc_dist, mc_tx) in enumerate(
        inp.hourly.select(HOURLY_COLUMNS).iter_rows(), start=2
    ):
        ws.cell(row, 1, ts).number_format = FMT_TIMESTAMP
        ws.cell(row, 2, season)
        for col, value, fmt in ((3, before, FMT_KWH), (4, after, FMT_KWH), (6, mc_dist, FMT_MC), (7, mc_tx, FMT_MC)):
            cell = ws.cell(row, col, float(value))
            cell.number_format = fmt
            cell.fill = INPUT_FILL
        ws.cell(row, 5, f"=D{row}-C{row}").number_format = FMT_KWH
        ws.cell(row, 8, f'=COUNTIFS({rng["B"]},B{row},{rng["D"]},">"&D{row})+1')
        ws.cell(row, 9, f"=LARGE({rng['F']},H{row})").number_format = FMT_MC
        ws.cell(row, 10, f"=LARGE({rng['G']},H{row})").number_format = FMT_MC

    e, i, j, b = rng["E"], rng["I"], rng["J"], rng["B"]
    summary = [
        ("Distribution marginal cost, $/kW-year", f"=SUM({rng['F']})", FMT_DOLLAR),
        ("Bulk transmission marginal cost, $/kW-year", f"=SUM({rng['G']})", FMT_DOLLAR),
        ("Incremental marginal cost, as in the testimony", f"=SUMPRODUCT({e},{rng['F']}+{rng['G']})", FMT_DOLLAR),
        ("Apr-Oct, reassigned (check: overstates)", f'=SUMPRODUCT(({b}="{SUMMER}")*{e}*({i}+{j}))', FMT_DOLLAR),
        ("Winter peaking: Nov-Mar, reassigned, distribution", f'=SUMPRODUCT(({b}="{WINTER}")*{e}*{i})', FMT_DOLLAR),
        ("Winter peaking: Nov-Mar, reassigned, transmission", f'=SUMPRODUCT(({b}="{WINTER}")*{e}*{j})', FMT_DOLLAR),
        ("Winter peaking: incremental marginal cost", "=N6+N7", FMT_DOLLAR),
        ("Overpayment under Rate 1 today (testimony)", None, FMT_DOLLAR),
        ("Overpayment remaining if winter peaking", "=N9-(N8-N4)", FMT_DOLLAR),
    ]
    for row, (label, formula, fmt) in enumerate(summary, start=2):
        ws.cell(row, 13, label).font = HEADER_FONT
        cell = ws.cell(row, 14, formula if formula is not None else float(inp.overpay))
        cell.number_format = fmt
        if formula is None:
            cell.fill = INPUT_FILL

    ws.freeze_panes = "A2"
    for col, width in zip("ABCDEFGHIJKLMN", [18, 9, 11, 11, 11, 11, 11, 14, 18, 16, 3, 3, 46, 14], strict=True):
        ws.column_dimensions[col].width = width


def build_workbook(inp: Inputs) -> Workbook:
    missing = set(HOURLY_COLUMNS) - set(inp.hourly.columns)
    if missing:
        raise ValueError(f"hourly frame is missing columns {sorted(missing)}")
    if inp.hourly.height != HOURS:
        raise ValueError(f"expected {HOURS} hours, got {inp.hourly.height}")
    if not inp.hourly["timestamp"].is_sorted():
        raise ValueError("hourly frame must be sorted by timestamp, the row order of Ex. JPV-3")
    if set(inp.hourly["season"].unique()) != {WINTER, SUMMER}:
        raise ValueError(f"season must be {WINTER!r} or {SUMMER!r}")
    wb = Workbook()
    _write_readme(wb, inp)
    _write_hourly(wb, inp)
    return wb


def upload_xlsx(path: Path, folder_id: str, name: str) -> str:
    """Upload the workbook to Drive, overwriting a file of the same name."""
    from build_ciec_1a_workbook import upload_xlsx as _upload

    return _upload(path, folder_id, name)
