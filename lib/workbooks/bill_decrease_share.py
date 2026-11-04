"""Excel workbook for the share of homes whose annual bill falls under Schedule R-HP.

Each building is one row. The annual bills are inputs. The bill change and the
weighted share are Excel formulas.
"""

from __future__ import annotations

from pathlib import Path

import polars as pl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet

_TOL = 1e-10


def build_bill_decrease_share_workbook(
    path: str | Path,
    buildings: pl.DataFrame,
    *,
    expected_pct_decrease: float,
    expected_pct_increase: float,
    note: str,
) -> Path:
    """Write the bill-share workbook and return its path.

    ``buildings`` has one row per home: ``bldg_id``, ``heating_type_v2``,
    ``weight``, ``bill_before``, ``bill_after``. The decrease share is the
    weight of rows whose bill falls, divided by total weight.
    """
    needed = ["bldg_id", "heating_type_v2", "weight", "bill_before", "bill_after"]
    missing = [col for col in needed if col not in buildings.columns]
    if missing:
        raise ValueError(f"buildings is missing columns: {missing}")
    frame = buildings.select(needed).sort("bldg_id")
    if frame.height == 0:
        raise ValueError("buildings is empty")
    if frame["bill_before"].null_count() or frame["bill_after"].null_count() or frame["weight"].null_count():
        raise ValueError("bill and weight columns contain nulls")

    weight = frame["weight"].cast(pl.Float64)
    delta = frame["bill_after"].cast(pl.Float64) - frame["bill_before"].cast(pl.Float64)
    total = float(weight.sum())
    if total == 0:
        raise ValueError("weights sum to zero")
    pct_decrease = float(weight.filter(delta < 0).sum()) / total
    pct_increase = float(weight.filter(delta > 0).sum()) / total
    if abs(pct_decrease - expected_pct_decrease) > _TOL:
        raise AssertionError(
            f"pct_all_fossil_hp_bill_decrease_rhp: inputs produce {pct_decrease:.10g}, "
            f"report variable is {expected_pct_decrease:.10g}"
        )
    if abs(pct_increase - expected_pct_increase) > _TOL:
        raise AssertionError(
            f"pct_all_fossil_hp_bill_increase_rhp: inputs produce {pct_increase:.10g}, "
            f"report variable is {expected_pct_increase:.10g}"
        )

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    default = wb.active
    assert default is not None
    wb.remove(default)
    last = _write_buildings(wb.create_sheet("buildings"), frame)
    _write_share(wb.create_sheet("share"), note, last)
    wb.save(out)
    return out


def _write_buildings(ws: Worksheet, frame: pl.DataFrame) -> int:
    headers = ["bldg_id", "heating_type", "weight", "bill_before", "bill_after", "delta"]
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(1, col, header)
        cell.font = Font(bold=True)
    for index, row in enumerate(frame.iter_rows(named=True)):
        excel_row = 2 + index
        bldg_id = row["bldg_id"]
        ws.cell(excel_row, 1, int(bldg_id) if isinstance(bldg_id, int) else bldg_id)
        ws.cell(excel_row, 2, str(row["heating_type_v2"]))
        ws.cell(excel_row, 3, float(row["weight"]))
        ws.cell(excel_row, 4, float(row["bill_before"]))
        ws.cell(excel_row, 5, float(row["bill_after"]))
        ws.cell(excel_row, 6, f"=E{excel_row}-D{excel_row}")
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 18
    for col in "CDEF":
        ws.column_dimensions[col].width = 16
    return frame.height + 1


def _note_text(note: str, boilerplate: str) -> str:
    note = note.strip()
    if not note:
        return boilerplate
    return f"{note}\n\n{boilerplate}"


def _write_share(ws: Worksheet, note: str, last: int) -> None:
    ws["A1"] = "Share of fossil-fuel-heated homes whose annual bill falls under Schedule R-HP"
    ws["A1"].font = Font(bold=True)
    ws.merge_cells("A2:B2")
    text = _note_text(note, "Annual bills are inputs. delta and the shares are Excel formulas.")
    ws["A2"] = text
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[2].height = 36 if "\n\n" not in text else 72
    weight = f"buildings!C2:C{last}"
    delta = f"buildings!F2:F{last}"
    rows = [
        (4, "Weight of homes whose bill falls", f'=SUMIF({delta},"<0",{weight})'),
        (5, "Weight of homes whose bill rises", f'=SUMIF({delta},">0",{weight})'),
        (6, "Weight of homes whose bill is unchanged", f'=SUMIF({delta},"=0",{weight})'),
        (7, "Total weight", f"=SUM({weight})"),
        (8, "Share whose bill falls", "=B4/B7"),
        (9, "Share whose bill rises", "=B5/B7"),
        (10, "Buildings", f"=COUNTA(buildings!A2:A{last})"),
    ]
    for row, label, formula in rows:
        ws.cell(row, 1, label)
        ws.cell(row, 2, formula)
    ws["A8"].font = Font(bold=True)
    ws["B8"].font = Font(bold=True)
    ws["B8"].number_format = "0.00%"
    ws["B9"].number_format = "0.00%"
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 22
