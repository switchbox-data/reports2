"""Helpers for the CIEC-1(a) Excel workpaper.

``ciec_request_1.qmd`` passes the per-customer values and enrollment inputs,
then calls :func:`build_workbook` and :func:`upload_xlsx`. Yellow cells in the
workbook are inputs. Every other number is a formula.

Sheets
------
README
    What the file is and how the sheets connect.
enrollment
    One existing-customer count, from EnergizeCT installations, and a floor
    and ceiling for new customers. Cumulative counts keep everyone already
    enrolled.
revenue
    Per-customer decrease (existing) and increase (new) as hardcoded
    constants from the representative-home analysis. Revenue reduced by
    existing customers, increased by new customers, and the net change.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
PER_THOUSAND = 1000

DRIVE_FOLDER_ID = "1nHGEJetAsVbGx2XG-ltaQ9aebba_Pl5c"
DRIVE_NAME = "CIEC-1a_rate_hp_revenue_reduction.xlsx"

INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
HEADER_FONT = Font(bold=True)
TITLE_FONT = Font(bold=True, size=14)
WRAP = Alignment(wrap_text=True, vertical="top")
FMT_DOLLAR = "#,##0.00"
FMT_REVENUE = "$#,##0"
FMT_COUNT = "#,##0"


@dataclass
class EnrollmentInputs:
    """Stated counts the enrollment sheet turns into existing customers and the new-customer bounds.

    ``energizect`` is (heat pump type, installations, systems per home), one row per type.
    """

    energizect: list[tuple[str, int, float]]
    clm_annual: int
    eversource_per_thousand: int
    years: list[int]
    statewide_additions: list[int]


@dataclass
class Case:
    dec_dist: float
    dec_tx: float
    inc_dist: float
    inc_tx: float
    enrollment: EnrollmentInputs


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


def _enrollment_summary(enrollment: EnrollmentInputs) -> dict[str, Any]:
    """The same arithmetic the enrollment sheet does, so the README can quote concrete numbers."""
    homes = sum(installations / systems for _, installations, systems in enrollment.energizect)
    existing = int(homes / 1000 + 0.5) * 1000
    share = enrollment.eversource_per_thousand / PER_THOUSAND
    ceiling_new = [statewide * share for statewide in enrollment.statewide_additions]
    floor_new = [float(enrollment.clm_annual)] * len(enrollment.years)
    return {
        "existing": existing,
        "share_percent": share * 100,
        "floor_new": floor_new,
        "ceiling_new": ceiling_new,
        "floor_total": [existing + sum(floor_new[: i + 1]) for i in range(len(floor_new))],
        "ceiling_total": [existing + sum(ceiling_new[: i + 1]) for i in range(len(ceiling_new))],
    }


def _write_readme(wb: Workbook, enrollment: EnrollmentInputs) -> None:
    ws = wb.active
    ws.title = "README"
    e = _enrollment_summary(enrollment)
    first, last = enrollment.years[0], enrollment.years[-1]
    lines = [
        ("CIEC-1(a) workpaper", True),
        (
            "Docket No. 26-05-10. Witness: Juan-Pablo Velez. Request from Connecticut Industrial Energy Consumers.",
            False,
        ),
        (
            "Annual change in distribution revenue and transmission revenue under Rate HP, "
            "relative to Rate 1, for each of the first five rate years.",
            False,
        ),
        ("", False),
        ("Yellow cells are inputs. Every other number is a formula.", True),
        ("", False),
        ("enrollment: who is enrolled in Rate HP each year", True),
        (
            "The scenario is that PURA auto-enrolls heat pump customers in Rate HP. Two groups enroll, "
            "and the sheet counts them separately. Rate years are numbered by the calendar year in which "
            f"they begin, so Rate Year {first} runs July {first} through June {first + 1}.",
            False,
        ),
        (
            f"1. Existing heat pump customers ({e['existing']:,}). These customers already have a heat pump "
            f"and received an Energize CT heat pump rebate before Rate HP takes effect on July 1, {first}. "
            "They are auto-enrolled all at once, in the first rate year, and stay enrolled. The count starts "
            "from the residential space-heating heat pump installations on the Energize CT dashboard. Each "
            "mini-split counts as less than one home, because a home often has more than one outdoor unit "
            "(123 outdoor units per 90 homes in a 2019 evaluation of 2015\u20132016 mini-split rebate "
            "participants); every other heat pump type counts as one home. The total is rounded to the "
            "nearest thousand. The low and high estimates use this same count.",
            False,
        ),
        (
            f"2. New heat pump customers. These customers install a heat pump in {first} through {last} and "
            "are enrolled in Rate HP when they install it. The low and high estimates differ in how many "
            "customers install each year.",
            False,
        ),
        (
            f"   Low estimate: {enrollment.clm_annual:,} new customers a year. This is the Company's forecast of "
            f"heat pump installations through its Conservation and Load Management programs for {first}, held "
            "flat for every later year because the forecast ends there.",
            False,
        ),
        (
            f"   High estimate: {e['ceiling_new'][0]:,.0f} new customers in {first}, rising to "
            f"{e['ceiling_new'][-1]:,.0f} in {last}. This is ISO New England's Connecticut-wide forecast of "
            f"homes adding a heat pump ({enrollment.statewide_additions[0]:,} in {first}, rising to "
            f"{enrollment.statewide_additions[-1]:,} in {last}), multiplied by Eversource's share of the "
            f"households served by Eversource and United Illuminating ({e['share_percent']:.1f}%).",
            False,
        ),
        (
            "Enrolled customers add up year by year. Each year's total is the previous year's total plus "
            "that year's new customers, because nobody leaves Rate HP. "
            f"Low estimate: {e['existing']:,} existing + {e['floor_new'][0]:,.0f} new = {e['floor_total'][0]:,.0f} "
            f"enrolled in {first}, growing to {e['floor_total'][-1]:,.0f} in {last}. "
            f"High estimate: {e['existing']:,} existing + {e['ceiling_new'][0]:,.0f} new = "
            f"{e['ceiling_total'][0]:,.0f} enrolled in {first}, growing to {e['ceiling_total'][-1]:,.0f} in {last}.",
            False,
        ),
        ("", False),
        ("revenue", True),
        (
            "Per-customer values are hardcoded constants from the representative-home analysis "
            "(Exhibit JPV-2, Section 2). The per-existing-customer decrease is the T&D overcharge "
            "Rate HP removes. The per-new-customer increase is the incremental marginal T&D cost "
            "the heat pump imposes. Revenue reduced is existing customers times the decrease. "
            "Revenue increased is new customers times the increase. The net is the difference. "
            "On this sheet, existing customers are the count above, and new customers are the "
            "cumulative enrolled total minus the existing customers.",
            False,
        ),
    ]
    for row, (text, bold) in enumerate(lines, start=1):
        cell = ws.cell(row, 1, text)
        cell.alignment = WRAP
        if bold:
            cell.font = TITLE_FONT if row == 1 else HEADER_FONT
        ws.row_dimensions[row].height = 22 if row == 1 else max(15, 15 * -(-len(text) // 110))
    ws.column_dimensions["A"].width = 120


def _write_enrollment(wb: Workbook, enrollment: EnrollmentInputs) -> dict[str, str]:
    ws = wb.create_sheet("enrollment")
    _heading(ws, 1, "Enrollment")
    _put(
        ws,
        2,
        1,
        "Two groups enroll in Rate HP. Existing heat pump customers are auto-enrolled all at once when "
        "Rate HP takes effect. New customers enroll in the year they install a heat pump. "
        "The low estimate (floor) and high estimate (ceiling) differ only in how many new customers "
        "install each year. The cumulative table at the bottom adds each year's new customers to "
        "everyone already enrolled.",
        wrap=True,
    )
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 64

    _put(ws, 4, 1, "Existing customers (EnergizeCT residential space-heating installations)", bold=True)
    for col, header in enumerate(["Heat pump type", "Installations", "Systems per home", "Homes"], start=1):
        _put(ws, 5, col, header, bold=True)
    first_type = 6
    for i, (hp_type, installations, systems_per_home) in enumerate(enrollment.energizect):
        row = first_type + i
        _put(ws, row, 1, hp_type)
        _put(ws, row, 2, installations, input_=True, fmt=FMT_COUNT)
        _put(ws, row, 3, systems_per_home, input_=True, fmt="0.00")
        _put(ws, row, 4, f"=B{row}/C{row}", fmt=FMT_COUNT)
    last_type = first_type + len(enrollment.energizect) - 1
    total_type = last_type + 1
    _put(ws, total_type, 1, "Total", bold=True)
    _put(ws, total_type, 2, f"=SUM(B{first_type}:B{last_type})", fmt=FMT_COUNT, bold=True)
    _put(ws, total_type, 4, f"=SUM(D{first_type}:D{last_type})", fmt=FMT_COUNT, bold=True)
    existing = total_type + 1
    _put(ws, existing, 1, "Existing customers", bold=True)
    _put(ws, existing, 4, f"=ROUND(D{total_type},-3)", fmt=FMT_COUNT, bold=True)
    _put(
        ws,
        first_type - 1,
        5,
        "EnergizeCT dashboard, 2017 through 2026 to date, water heaters excluded. Mini-splits: 123 outdoor units "
        "per 90 homes (R1617). Every other type counts as one home. An upper estimate: a home with two systems, "
        "or incentives in two years, counts twice.",
        wrap=True,
    )

    inputs_header = existing + 2
    _put(ws, inputs_header, 1, "New-customer inputs", bold=True)
    clm_row = inputs_header + 1
    share_row = inputs_header + 2
    share_percent = enrollment.eversource_per_thousand / PER_THOUSAND * 100
    inputs = [
        (
            clm_row,
            "CLM installations per year, 2027 on",
            enrollment.clm_annual,
            "2027 forecast, held flat. No forecast after 2027.",
        ),
        (
            share_row,
            "Eversource households per 1,000 served by Eversource and UI",
            enrollment.eversource_per_thousand,
            f"RASS Table 6. {enrollment.eversource_per_thousand} per 1,000 is {share_percent:.1f} percent.",
        ),
    ]
    for row, label, value, note in inputs:
        _put(ws, row, 1, label)
        _put(ws, row, 2, value, input_=True, fmt=FMT_COUNT)
        _put(ws, row, 3, note, wrap=True)

    new_header = share_row + 2
    _put(ws, new_header, 1, "New customers enrolling each year (installing a heat pump that year)", bold=True)
    for col, header in enumerate(
        ["Year", "Statewide additions", "Low estimate (floor)", "High estimate (ceiling)"], start=1
    ):
        _put(ws, new_header + 1, col, header, bold=True)
    first_new = new_header + 2
    for i, (year, statewide) in enumerate(zip(enrollment.years, enrollment.statewide_additions, strict=True)):
        row = first_new + i
        _put(ws, row, 1, year, fmt="0")
        _put(ws, row, 2, statewide, input_=True, fmt=FMT_COUNT)
        _put(ws, row, 3, f"=$B${clm_row}", fmt=FMT_COUNT)
        _put(ws, row, 4, f"=B{row}*$B${share_row}/{PER_THOUSAND}", fmt=FMT_COUNT)
    _put(
        ws,
        new_header + 1,
        5,
        f"Statewide additions are the ISO-NE forecast. The ceiling multiplies by the share in B{share_row}.",
        wrap=True,
    )

    cum_header = first_new + len(enrollment.years) + 2
    _put(ws, cum_header - 1, 1, "Cumulative customers enrolled in Rate HP", bold=True)
    for col, header in enumerate(["Year", "Low estimate (floor)", "High estimate (ceiling)"], start=1):
        _put(ws, cum_header, col, header, bold=True)
    existing_row = cum_header + 1
    _put(ws, existing_row, 1, enrollment.years[0] - 1, fmt="0")
    _put(ws, existing_row, 2, f"=$D${existing}", fmt=FMT_COUNT)
    _put(ws, existing_row, 3, f"=$D${existing}", fmt=FMT_COUNT)
    _put(
        ws,
        existing_row,
        4,
        "Existing customers only, enrolled when Rate HP takes effect. The same in the low and high estimates.",
        wrap=True,
    )
    for i in range(len(enrollment.years)):
        row = existing_row + 1 + i
        new_row = first_new + i
        _put(ws, row, 1, f"=A{new_row}", fmt="0")
        _put(ws, row, 2, f"=B{row - 1}+C{new_row}", fmt=FMT_COUNT)
        _put(ws, row, 3, f"=C{row - 1}+D{new_row}", fmt=FMT_COUNT)

    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 24
    ws.column_dimensions["C"].width = 78
    ws.column_dimensions["D"].width = 16
    ws.column_dimensions["E"].width = 78
    for row in (2, first_type - 1, share_row):
        ws.row_dimensions[row].height = 32
    return {
        "floor_start": f"B{existing_row}",
        "ceiling_start": f"C{existing_row}",
        "existing_row": str(existing_row),
        "n_rows": str(1 + len(enrollment.years)),
    }


def _write_revenue(
    wb: Workbook,
    case: Case,
    enrollment: dict[str, str],
) -> None:
    ws = wb.create_sheet("revenue")
    _heading(ws, 1, "Revenue change")
    _put(
        ws,
        2,
        1,
        "Per-customer values are from the representative-home analysis (Exhibit JPV-2). "
        "Revenue reduced is existing customers times the per-customer decrease. "
        "Revenue increased is new customers times the per-customer increase. "
        "The net is the difference (increased minus reduced, so negative means a net reduction). "
        "The existing customers are included in 2027 through 2031.",
        wrap=True,
    )
    ws.merge_cells("A2:I2")
    ws.row_dimensions[2].height = 48

    _put(ws, 4, 1, "Per-existing-customer decrease", bold=True)
    _put(ws, 4, 2, "Distribution")
    _put(ws, 4, 3, case.dec_dist, input_=True, fmt=FMT_DOLLAR)
    _put(ws, 4, 4, "Transmission")
    _put(ws, 4, 5, case.dec_tx, input_=True, fmt=FMT_DOLLAR)
    _put(ws, 4, 6, "T&D total")
    _put(ws, 4, 7, "=C4+E4", fmt=FMT_DOLLAR)
    _put(
        ws,
        4,
        8,
        "T&D overcharge Rate HP removes. From the representative-home analysis (Exhibit JPV-2).",
        wrap=True,
    )

    _put(ws, 5, 1, "Per-new-customer increase", bold=True)
    _put(ws, 5, 2, "Distribution")
    _put(ws, 5, 3, case.inc_dist, input_=True, fmt=FMT_DOLLAR)
    _put(ws, 5, 4, "Transmission")
    _put(ws, 5, 5, case.inc_tx, input_=True, fmt=FMT_DOLLAR)
    _put(ws, 5, 6, "T&D total")
    _put(ws, 5, 7, "=C5+E5", fmt=FMT_DOLLAR)
    _put(
        ws,
        5,
        8,
        "Incremental marginal T&D cost. Rate HP recovers this from each new customer.",
        wrap=True,
    )

    _put(ws, 6, 1, "Sum (delivery charge increase under Rate 1)")
    _put(ws, 6, 3, "=C4+C5", fmt=FMT_DOLLAR)
    _put(ws, 6, 5, "=E4+E5", fmt=FMT_DOLLAR)
    _put(ws, 6, 7, "=G4+G5", fmt=FMT_DOLLAR)
    _put(ws, 6, 8, "Check: decrease + increase = total delivery charge increase.", wrap=True)

    headers = [
        "Year",
        "Existing customers",
        "New customers",
        "Revenue reduced, dist",
        "Revenue reduced, tx",
        "Revenue increased, dist",
        "Revenue increased, tx",
        "Net change, dist",
        "Net change, tx",
    ]
    header_row = 8
    for col, header in enumerate(headers, start=1):
        _put(ws, header_row, col, header, bold=True)
        ws.cell(header_row, col).alignment = Alignment(wrap_text=True, vertical="bottom")
    ws.row_dimensions[header_row].height = 32

    existing_row = int(enrollment["existing_row"])
    n_rows = int(enrollment["n_rows"])
    floor_existing = f"enrollment!$B${existing_row}"
    ceiling_existing = f"enrollment!$C${existing_row}"

    section_start = header_row + 2
    _put(ws, section_start - 1, 1, "Low estimate of new customers", bold=True)
    for i in range(n_rows):
        row = section_start + i
        src = existing_row + i
        _put(ws, row, 1, f"=enrollment!A{src}", fmt="0")
        _put(ws, row, 2, f"={floor_existing}", fmt=FMT_COUNT)
        _put(ws, row, 3, f"=enrollment!B{src}-{floor_existing}", fmt=FMT_COUNT)
        _put(ws, row, 4, f"=ROUND(B{row}*$C$4,0)", fmt=FMT_REVENUE)
        _put(ws, row, 5, f"=ROUND(B{row}*$E$4,0)", fmt=FMT_REVENUE)
        _put(ws, row, 6, f"=ROUND(C{row}*$C$5,0)", fmt=FMT_REVENUE)
        _put(ws, row, 7, f"=ROUND(C{row}*$E$5,0)", fmt=FMT_REVENUE)
        _put(ws, row, 8, f"=F{row}-D{row}", fmt=FMT_REVENUE)
        _put(ws, row, 9, f"=G{row}-E{row}", fmt=FMT_REVENUE)

    ceiling_start = section_start + n_rows + 2
    _put(ws, ceiling_start - 1, 1, "High estimate of new customers", bold=True)
    for i in range(n_rows):
        row = ceiling_start + i
        src = existing_row + i
        _put(ws, row, 1, f"=enrollment!A{src}", fmt="0")
        _put(ws, row, 2, f"={ceiling_existing}", fmt=FMT_COUNT)
        _put(ws, row, 3, f"=enrollment!C{src}-{ceiling_existing}", fmt=FMT_COUNT)
        _put(ws, row, 4, f"=ROUND(B{row}*$C$4,0)", fmt=FMT_REVENUE)
        _put(ws, row, 5, f"=ROUND(B{row}*$E$4,0)", fmt=FMT_REVENUE)
        _put(ws, row, 6, f"=ROUND(C{row}*$C$5,0)", fmt=FMT_REVENUE)
        _put(ws, row, 7, f"=ROUND(C{row}*$E$5,0)", fmt=FMT_REVENUE)
        _put(ws, row, 8, f"=F{row}-D{row}", fmt=FMT_REVENUE)
        _put(ws, row, 9, f"=G{row}-E{row}", fmt=FMT_REVENUE)

    _put(
        ws,
        section_start,
        10,
        "2026 is the existing stock (new customers = 0). Later rows add each year's new customers.",
        wrap=True,
    )

    ws.freeze_panes = f"A{header_row + 1}"
    ws.column_dimensions["A"].width = 36
    for col in range(2, 10):
        ws.column_dimensions[get_column_letter(col)].width = 22
    ws.column_dimensions["J"].width = 36


def build_workbook(case: Case) -> Workbook:
    wb = Workbook()
    _write_readme(wb, case.enrollment)
    enrollment = _write_enrollment(wb, case.enrollment)
    _write_revenue(wb, case, enrollment)
    return wb


def upload_xlsx(path: Path, folder_id: str, name: str) -> str:
    """Upload the workbook to Drive, overwriting a file of the same name in place.

    Overwriting keeps the file id, so links to the workbook in the responses stay valid.
    """
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    from lib.data.gsheets import get_gspread_client

    gc, _ = get_gspread_client()
    drive = build("drive", "v3", credentials=gc.http_client.auth, cache_discovery=False)
    existing = (
        drive.files()
        .list(
            q=f"name = '{name}' and '{folder_id}' in parents and trashed = false",
            fields="files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    ).get("files", [])
    media = MediaFileUpload(
        str(path),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        resumable=True,
    )
    if existing:
        keep, *duplicates = existing
        for old in duplicates:
            drive.files().update(fileId=old["id"], body={"trashed": True}, supportsAllDrives=True).execute()
        updated = (
            drive.files()
            .update(fileId=keep["id"], media_body=media, fields="id, webViewLink", supportsAllDrives=True)
            .execute()
        )
        return str(updated["webViewLink"])
    uploaded = (
        drive.files()
        .create(
            body={"name": name, "parents": [folder_id]},
            media_body=media,
            fields="id, webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )
    return str(uploaded["webViewLink"])
