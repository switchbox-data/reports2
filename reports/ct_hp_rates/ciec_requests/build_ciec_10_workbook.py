"""Helpers for the CIEC-10(a) Excel workpaper.

``ciec_request_10.qmd`` computes the average fossil fuel-heated Eversource
home's hourly load after the heat pump retrofit (upgrade 2), split into
electric resistance backup, heat pump, and whole-home load.  This workbook
gives those 8,760 hours with the annual totals and peak hours as formulas.

Sheets
------
README
    What the file is, where the load comes from, and what each column means.
hourly_load
    One row per hour in columns A-F (timestamps, the three loads, and heat
    pump plus backup as a formula), and the annual totals, backup ratio, and
    peak hours as formulas in columns H-I.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import polars as pl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

DRIVE_FOLDER_ID = "1sAypEVEBw3DO89Zlfrl5H0BF6GXna9gt"
DRIVE_NAME = "CIEC-10a_hourly_backup_load.xlsx"

HEADER_FONT = Font(bold=True)
TITLE_FONT = Font(bold=True, size=14)
WRAP = Alignment(wrap_text=True, vertical="top")
FMT_TIMESTAMP = "yyyy-mm-dd hh:mm"
FMT_KWH = "0.000"
HOURS = 8760
HOURLY_COLUMNS = ("timestamp", "weather_hour", "backup_kwh", "heat_pump_kwh", "grid_kwh")


@dataclass
class Inputs:
    """The average home's hourly load and the facts the README describes."""

    hourly: pl.DataFrame
    n_bldg: int
    release: str
    kwh_scale: float


def _write_readme(wb: Workbook, inp: Inputs) -> None:
    ws = wb.active
    ws.title = "README"
    lines = [
        ("CIEC-10(a) workpaper", True),
        (
            "Docket No. 26-05-10. Witness: Juan-Pablo Velez. Request from Connecticut Industrial Energy Consumers.",
            False,
        ),
        (
            "Modeled hourly load of the average fossil fuel-heated Eversource home after heat pump installation: "
            f"the sample-weighted average of {inp.n_bldg:,} ResStock {inp.release} buildings served by Eversource "
            "and heated with natural gas, fuel oil, or propane before the retrofit, modeled after the upgrade 2 "
            f"cold-climate heat pump retrofit. Every kWh is multiplied by the CAIRO scale factor {inp.kwh_scale:.6f}, "
            "so whole-home load sums to the annual kWh used in the direct testimony.",
            False,
        ),
        ("", False),
        ("hourly_load", True),
        (
            "timestamp: the hour on CAIRO's 2025 billing calendar, Eastern Standard Time, hour beginning. "
            "Same timestamps and row order as Ex. JPV-3, sheet hourly_after.",
            False,
        ),
        (
            "weather_hour_2018: the ResStock hour simulated in that row (2018 weather). CAIRO shifts the 2018 year "
            "by two days so weekdays line up with 2025; January 1-2, 2018 appear at the end of the year.",
            False,
        ),
        ("backup_kwh: electric resistance backup element (out.electricity.heating_hp_bkup).", False),
        (
            "heat_pump_kwh: compressor plus supply fan (out.electricity.heating, heating_fans_pumps, "
            "heating_hp_bkup_fa).",
            False,
        ),
        (
            "whole_home_kwh: grid consumption, the load billed in the direct testimony (Ex. JPV-3, sheet hourly_after).",
            False,
        ),
        ("heat_pump_plus_backup_kwh: formula, backup_kwh + heat_pump_kwh.", False),
        ("Columns H-I: annual totals, backup relative to heat pump kWh, and the peak hours, all formulas.", False),
    ]
    for row, (text, bold) in enumerate(lines, start=1):
        cell = ws.cell(row, 1, text)
        cell.alignment = WRAP
        if bold:
            cell.font = TITLE_FONT if row == 1 else HEADER_FONT
    ws.column_dimensions["A"].width = 120
    ws.row_dimensions[3].height = 64


def _write_hourly(wb: Workbook, hourly: pl.DataFrame) -> None:
    ws = wb.create_sheet("hourly_load")
    headers = [
        "timestamp",
        "weather_hour_2018",
        "backup_kwh",
        "heat_pump_kwh",
        "whole_home_kwh",
        "heat_pump_plus_backup_kwh",
    ]
    for col, header in enumerate(headers, start=1):
        ws.cell(1, col, header).font = HEADER_FONT
    for row, values in enumerate(hourly.select(HOURLY_COLUMNS).iter_rows(), start=2):
        ws.cell(row, 1, values[0]).number_format = FMT_TIMESTAMP
        ws.cell(row, 2, values[1]).number_format = FMT_TIMESTAMP
        for col, value in enumerate(values[2:], start=3):
            ws.cell(row, col, float(value)).number_format = FMT_KWH
        ws.cell(row, 6, f"=C{row}+D{row}").number_format = FMT_KWH

    last = hourly.height + 1
    summary = [
        ("Annual backup kWh", f"=SUM(C2:C{last})", "#,##0.0"),
        ("Annual heat pump kWh", f"=SUM(D2:D{last})", "#,##0.0"),
        ("Annual whole-home kWh", f"=SUM(E2:E{last})", "#,##0.0"),
        ("Backup / heat pump kWh", "=I2/I3", "0.0%"),
        ("Peak backup kWh", f"=MAX(C2:C{last})", "0.00"),
        ("Peak backup hour", f"=INDEX(A2:A{last},MATCH(I6,C2:C{last},0))", FMT_TIMESTAMP),
        ("Peak heat pump + backup kWh", f"=MAX(F2:F{last})", "0.00"),
        ("Peak heat pump + backup hour", f"=INDEX(A2:A{last},MATCH(I8,F2:F{last},0))", FMT_TIMESTAMP),
    ]
    for row, (label, formula, fmt) in enumerate(summary, start=2):
        ws.cell(row, 8, label).font = HEADER_FONT
        ws.cell(row, 9, formula).number_format = fmt

    ws.freeze_panes = "A2"
    for col, width in zip("ABCDEFGHI", [18, 18, 12, 14, 16, 26, 3, 30, 18], strict=True):
        ws.column_dimensions[col].width = width


def build_workbook(inp: Inputs) -> Workbook:
    missing = set(HOURLY_COLUMNS) - set(inp.hourly.columns)
    if missing:
        raise ValueError(f"hourly frame is missing columns {sorted(missing)}")
    if inp.hourly.height != HOURS:
        raise ValueError(f"expected {HOURS} hours, got {inp.hourly.height}")
    if not inp.hourly["timestamp"].is_sorted():
        raise ValueError("hourly frame must be sorted by timestamp, the row order of Ex. JPV-3")
    wb = Workbook()
    _write_readme(wb, inp)
    _write_hourly(wb, inp.hourly)
    return wb


def upload_xlsx(path: Path, folder_id: str, name: str) -> str:
    """Upload the workbook to Drive, overwriting a file of the same name."""
    from build_ciec_1a_workbook import upload_xlsx as _upload

    return _upload(path, folder_id, name)
