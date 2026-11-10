"""Helpers for the CIEC-1(a) Excel workpaper.

``ciec_request_1.qmd`` loads the home, the rates, and the enrollment inputs,
then calls :func:`build_workbook` and :func:`upload_xlsx`. Yellow cells in the
workbook are inputs. Every other number is a formula.

Sheets
------
README
    What the file is and how the sheets connect.
home_8760
    One row per hour for the representative heat pump customer: the
    weighted average of upgrade 02 loads for Eversource homes heated with
    natural gas, fuel oil, or propane, the population of the direct
    testimony. Month and season are formulas on the timestamp.
rates
    Rate 1 components, the Rate HP winter rates, and the monthly schedule.
bill_change
    Monthly bills for that home. The decrease is the cent-rounded annual bill,
    applied to every enrolled customer.
enrollment
    One existing-customer count, from EnergizeCT installations, and a floor
    and ceiling for new customers. Cumulative counts keep everyone already
    enrolled.
revenue
    Enrolled customers times the per-customer decrease. The starting stock
    and the later enrollees each round to the dollar.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import polars as pl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
# The ceiling formula divides by this after multiplying, so 784 per 1,000 stays exact.
PER_THOUSAND = 1000

DRIVE_FOLDER_ID = "1nHGEJetAsVbGx2XG-ltaQ9aebba_Pl5c"
DRIVE_NAME = "CIEC-1a_rate_hp_revenue_reduction.xlsx"

# (yaml group, key, label, note). group is "already", "drr", or "srr".
# The first eight volumetric charges sum to the distribution rate.
RATE_INPUTS: list[tuple[str, str, str, str]] = [
    ("already", "customer_charge", "Customer charge", "Dollars per month. Unchanged under Rate HP."),
    ("already", "core_delivery_rate", "Core delivery", "Distribution energy charge, before riders."),
    (
        "drr",
        "electric_system_improvements_esi",
        "Electric system improvements (ESI)",
        "Rider. Included in distribution.",
    ),
    (
        "drr",
        "revenue_decoupling_mechanism_rdm",
        "Revenue decoupling mechanism (RDM)",
        "Rider. Included in distribution.",
    ),
    (
        "drr",
        "competitive_transition_assessment_cta",
        "Competitive transition assessment (CTA)",
        "Rider. Included in distribution.",
    ),
    (
        "drr",
        "non_bypassable_fmcc_delivery",
        "Non-bypassable FMCC",
        "Rider. Included in distribution.",
    ),
    (
        "drr",
        "conservation_adjustment_mechanism_cam",
        "Conservation adjustment mechanism (CAM)",
        "Rider. Included in distribution.",
    ),
    (
        "drr",
        "renewable_energy_investment_clean_energy_fund",
        "Clean energy fund",
        "Rider. Included in distribution.",
    ),
    ("drr", "system_benefits_charge_sbc", "System benefits charge (SBC)", "Rider. Included in distribution."),
    ("drr", "transmission_charge", "Transmission", "Unchanged in summer. Replaced in winter under Rate HP."),
    (
        "srr",
        "supply_commodity_bundled",
        "Generation",
        "Supply. Unchanged under Rate HP.",
    ),
]
DISTRIBUTION_LABELS = [
    "Core delivery",
    "Electric system improvements (ESI)",
    "Revenue decoupling mechanism (RDM)",
    "Competitive transition assessment (CTA)",
    "Non-bypassable FMCC",
    "Conservation adjustment mechanism (CAM)",
    "Clean energy fund",
    "System benefits charge (SBC)",
]

INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
HEADER_FONT = Font(bold=True)
TITLE_FONT = Font(bold=True, size=14)
WRAP = Alignment(wrap_text=True, vertical="top")
FMT_KWH = "#,##0.000"
FMT_RATE = "0.000000"
FMT_CENTS = "0.000"
FMT_DOLLAR = "#,##0.00"
FMT_REVENUE = "$#,##0"
FMT_COUNT = "#,##0"
FMT_TIME = "YYYY-MM-DD HH:MM"


@dataclass
class Charge:
    label: str
    unit: str
    rates: dict[str, float]
    note: str


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
    hourly: pl.DataFrame
    charges: list[Charge]
    winter_dist: float
    winter_tx: float
    n_buildings: int
    total_weight: float
    enrollment: EnrollmentInputs


def _rates_by_month(monthly_rates: dict[str, float]) -> dict[str, float]:
    out: dict[str, float] = {}
    for key, value in monthly_rates.items():
        month_num = int(str(key).split("-")[1])
        out[MONTHS[month_num - 1]] = float(value)
    missing = [month for month in MONTHS if month not in out]
    if missing:
        raise RuntimeError(f"monthly rates missing {missing}")
    return out


def charges_from_groups(
    already: dict[str, Any],
    drr: dict[str, Any],
    srr: dict[str, Any],
) -> list[Charge]:
    """Rate 1 component rows from the three groups in the monthly-rates YAML."""
    groups = {"already": already, "drr": drr, "srr": srr}
    return [
        Charge(
            label=label,
            unit=str(groups[group][key]["charge_unit"]),
            rates=_rates_by_month(groups[group][key]["monthly_rates"]),
            note=note,
        )
        for group, key, label, note in RATE_INPUTS
    ]


def _naive_utc(ts: datetime) -> datetime:
    if ts.tzinfo is not None:
        return ts.astimezone(UTC).replace(tzinfo=None)
    return ts


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
        ("CIEC-1(a) workpaper", True),
        (
            "Docket No. 26-05-10. Witness: Juan-Pablo Velez. Request from Connecticut Industrial Energy Consumers.",
            False,
        ),
        (
            "Annual reduction in distribution revenue and in transmission revenue under Rate HP, "
            "relative to Rate 1, for each of the first five rate years.",
            False,
        ),
        ("", False),
        ("Yellow cells are inputs. Every other number is a formula.", True),
        ("", False),
        ("home_8760", True),
        (
            "8,760 hours for the representative heat pump customer, the same home as the direct testimony: "
            "Eversource homes heated with natural gas, fuel oil, or propane, on their ResStock upgrade 02 "
            "(heat pump) load. Each hour is the sum of kWh times sample weight, divided by the sum of weight. "
            "kWh is CAIRO grid consumption. Timestamps are UTC, and the month follows that timestamp, "
            "which is how the bill is calculated. Month and season are formulas. "
            "Every enrolled customer, existing or new, is billed as this home.",
            False,
        ),
        ("", False),
        ("rates", True),
        (
            "Rate 1 is the proposed Rate Year schedule. Distribution is core delivery plus the riders. "
            "Rate HP replaces distribution and transmission in January, February, March, November, and "
            "December. The winter rates include the riders. Summer, generation, and the customer charge "
            "stay at Rate 1. The winter rates are the unrounded rates behind Table 4 of the direct testimony.",
            False,
        ),
        ("", False),
        ("bill_change", True),
        (
            "Each month's kWh is the sum of that month on home_8760. Volumetric charges are kWh times "
            "the rate on the rates sheet. The customer charge is dollars per month. The comparison rounds "
            "each annual component to the cent, then adds those cents. The decrease is Rate 1 minus Rate HP.",
            False,
        ),
        ("", False),
        ("enrollment", True),
        (
            "Customers on Rate HP, from the stock already enrolled through 2031. "
            "Existing customers are EnergizeCT residential space-heating installations divided by "
            "systems per home, rounded to the thousand. The same count starts the floor and the ceiling. "
            "The new floor holds the 2027 forecast flat. "
            "The new ceiling is the statewide forecast times Eversource's share of Eversource and "
            "United Illuminating. Cumulative counts add that year's installations and keep everyone already enrolled.",
            False,
        ),
        ("", False),
        ("revenue", True),
        (
            "Each row is a full year for the customers enrolled by that year, at the per-customer decrease "
            "on bill_change. The starting stock and the customers added after it each round to the dollar, "
            "then the two are added. T&D adds those dollars. The existing customers are included in every later year.",
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
        ws.row_dimensions[row].height = 48


def _write_hourly(
    wb: Workbook,
    sheet_name: str,
    hourly: pl.DataFrame,
    n_buildings: int,
    total_weight: float,
) -> int:
    ws = wb.create_sheet(sheet_name)
    headers = ["timestamp_utc", "kwh", "month", "season"]
    for col, header in enumerate(headers, start=1):
        _put(ws, 1, col, header, bold=True)
    timestamps = [_naive_utc(ts) for ts in hourly["timestamp"].to_list()]
    kwh = [float(value) for value in hourly["kwh"].to_list()]
    for i, (ts, hour_kwh) in enumerate(zip(timestamps, kwh, strict=True), start=2):
        _put(ws, i, 1, ts, fmt=FMT_TIME)
        _put(ws, i, 2, hour_kwh, fmt=FMT_KWH)
        _put(
            ws,
            i,
            3,
            f'=CHOOSE(MONTH(A{i}),"Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")',
        )
        _put(
            ws,
            i,
            4,
            f'=IF(OR(MONTH(A{i})=1,MONTH(A{i})=2,MONTH(A{i})=3,MONTH(A{i})=11,MONTH(A{i})=12),"Winter","Summer")',
        )
    last = 1 + len(timestamps)
    _put(ws, 1, 6, "buildings", bold=True)
    _put(ws, 1, 7, n_buildings, fmt=FMT_COUNT)
    _put(ws, 2, 6, "sample weight", bold=True)
    _put(ws, 2, 7, total_weight, fmt="#,##0.00")
    _put(ws, 3, 6, "annual kWh", bold=True)
    _put(ws, 3, 7, f"=SUM(B2:B{last})", fmt=FMT_KWH)
    _put(ws, 4, 6, "winter kWh", bold=True)
    _put(ws, 4, 7, f'=SUMIF(D2:D{last},"Winter",B2:B{last})', fmt=FMT_KWH)
    _put(ws, 5, 6, "hours", bold=True)
    _put(ws, 5, 7, f"=COUNTA(A2:A{last})", fmt=FMT_COUNT)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:D{last}"
    for col, width in enumerate([20, 14, 12, 12, 3, 16, 16], start=1):
        ws.column_dimensions[get_column_letter(col)].width = width
    return last


def _write_rates(wb: Workbook, case: Case) -> dict[str, int]:
    ws = wb.create_sheet("rates")
    _heading(ws, 1, "Rate 1 and Rate HP")
    _put(
        ws,
        2,
        1,
        "Distribution sums core delivery and the riders. Rate HP winter rates replace that sum, riders included.",
        wrap=True,
    )
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=8)
    ws.row_dimensions[2].height = 32

    header_row = 4
    _put(ws, header_row, 1, "Component", bold=True)
    _put(ws, header_row, 2, "Unit", bold=True)
    for i, month in enumerate(MONTHS):
        _put(ws, header_row, 3 + i, month, bold=True)
    _put(ws, header_row, 15, "Note", bold=True)

    first_input = header_row + 1
    rows_by_label: dict[str, int] = {}
    for offset, charge in enumerate(case.charges):
        row = first_input + offset
        rows_by_label[charge.label] = row
        _put(ws, row, 1, charge.label)
        _put(ws, row, 2, charge.unit)
        number_fmt = FMT_DOLLAR if charge.unit == "$/month" else FMT_RATE
        for i, month in enumerate(MONTHS):
            _put(ws, row, 3 + i, charge.rates[month], input_=True, fmt=number_fmt)
        _put(ws, row, 15, charge.note, wrap=True)

    dist_row = first_input + len(case.charges) + 1
    _put(ws, dist_row, 1, "Distribution", bold=True)
    _put(ws, dist_row, 2, "$/kWh")
    dist_rows = [rows_by_label[label] for label in DISTRIBUTION_LABELS]
    for i in range(12):
        col = get_column_letter(3 + i)
        _put(ws, dist_row, 3 + i, "=" + "+".join(f"{col}{row}" for row in dist_rows), fmt=FMT_RATE, bold=True)
    _put(ws, dist_row, 15, "Core delivery plus riders. This is the distribution rate on the bill.", wrap=True)

    riders_row = dist_row + 1
    core_row = rows_by_label["Core delivery"]
    _put(ws, riders_row, 1, "Riders")
    _put(ws, riders_row, 2, "$/kWh")
    for i in range(12):
        col = get_column_letter(3 + i)
        _put(ws, riders_row, 3 + i, f"={col}{dist_row}-{col}{core_row}", fmt=FMT_RATE)
    _put(ws, riders_row, 15, "Distribution minus core delivery. Same under Rate 1 and Rate HP.", wrap=True)

    winter_row = riders_row + 2
    _put(ws, winter_row, 1, "Rate HP winter distribution", bold=True)
    _put(ws, winter_row, 2, "$/kWh")
    _put(ws, winter_row, 3, case.winter_dist, input_=True, fmt=FMT_RATE)
    _put(
        ws,
        winter_row,
        4,
        "Replaces distribution in Jan, Feb, Mar, Nov, and Dec. Includes riders. Unrounded Table 4 rate.",
        wrap=True,
    )
    ws.merge_cells(start_row=winter_row, start_column=4, end_row=winter_row, end_column=10)
    winter_tx_row = winter_row + 1
    _put(ws, winter_tx_row, 1, "Rate HP winter transmission", bold=True)
    _put(ws, winter_tx_row, 2, "$/kWh")
    _put(ws, winter_tx_row, 3, case.winter_tx, input_=True, fmt=FMT_RATE)
    _put(ws, winter_tx_row, 4, "Replaces transmission in the same winter months. Unrounded Table 4 rate.", wrap=True)

    cents_row = winter_tx_row + 2
    _put(ws, cents_row, 1, "Rate 1 distribution energy", bold=True)
    _put(ws, cents_row, 2, "¢/kWh")
    _put(ws, cents_row, 3, f"=C{core_row}*100", fmt=FMT_CENTS)
    _put(ws, cents_row + 1, 1, "Rate HP winter distribution energy")
    _put(ws, cents_row + 1, 2, "¢/kWh")
    _put(ws, cents_row + 1, 3, f"=(C{winter_row}-C{riders_row})*100", fmt=FMT_CENTS)
    tx_row = rows_by_label["Transmission"]
    _put(ws, cents_row + 2, 1, "Rate 1 transmission")
    _put(ws, cents_row + 2, 2, "¢/kWh")
    _put(ws, cents_row + 2, 3, f"=C{tx_row}*100", fmt=FMT_CENTS)
    _put(ws, cents_row + 3, 1, "Rate HP winter transmission")
    _put(ws, cents_row + 3, 2, "¢/kWh")
    _put(ws, cents_row + 3, 3, f"=C{winter_tx_row}*100", fmt=FMT_CENTS)
    _put(ws, cents_row, 4, "Core delivery only, the energy charge quoted in the response.", wrap=True)
    _put(ws, cents_row + 1, 4, "Winter distribution minus the riders.", wrap=True)

    billed_header = cents_row + 5
    _put(ws, billed_header - 1, 1, "Monthly rates used to bill the home", bold=True)
    billed_headers = [
        "Month",
        "Season",
        "Customer, Rate 1",
        "Distribution, Rate 1",
        "Transmission, Rate 1",
        "Generation, Rate 1",
        "Customer, Rate HP",
        "Distribution, Rate HP",
        "Transmission, Rate HP",
        "Generation, Rate HP",
    ]
    for col, header in enumerate(billed_headers, start=1):
        _put(ws, billed_header, col, header, bold=True)
    customer_row = rows_by_label["Customer charge"]
    gen_row = rows_by_label["Generation"]
    first_billed = billed_header + 1
    for i, month in enumerate(MONTHS):
        row = first_billed + i
        src = get_column_letter(3 + i)
        _put(ws, row, 1, month)
        _put(
            ws,
            row,
            2,
            f'=IF(OR(A{row}="Jan",A{row}="Feb",A{row}="Mar",A{row}="Nov",A{row}="Dec"),"Winter","Summer")',
        )
        _put(ws, row, 3, f"={src}{customer_row}", fmt=FMT_DOLLAR)
        _put(ws, row, 4, f"={src}{dist_row}", fmt=FMT_RATE)
        _put(ws, row, 5, f"={src}{tx_row}", fmt=FMT_RATE)
        _put(ws, row, 6, f"={src}{gen_row}", fmt=FMT_RATE)
        _put(ws, row, 7, f"=C{row}", fmt=FMT_DOLLAR)
        _put(ws, row, 8, f'=IF(B{row}="Winter",$C${winter_row},D{row})', fmt=FMT_RATE)
        _put(ws, row, 9, f'=IF(B{row}="Winter",$C${winter_tx_row},E{row})', fmt=FMT_RATE)
        _put(ws, row, 10, f"=F{row}", fmt=FMT_RATE)

    ws.freeze_panes = "C5"
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["B"].width = 22
    for i in range(12):
        ws.column_dimensions[get_column_letter(3 + i)].width = 14
    ws.column_dimensions["O"].width = 56
    ws.row_dimensions[header_row].height = 20
    return {"first_billed": first_billed, "cents_row": cents_row}


def _write_bills(
    wb: Workbook,
    sheet_name: str,
    hourly_sheet: str,
    rates_rows: dict[str, int],
    last_hour: int,
    *,
    title: str,
) -> dict[str, str]:
    ws = wb.create_sheet(sheet_name)
    _heading(ws, 1, title)
    _put(
        ws,
        2,
        1,
        f"kWh sums {hourly_sheet}. Volumetric charges multiply that kWh by the rates sheet. "
        "The customer charge does not. The table below rounds the annual total of each component to the cent.",
        wrap=True,
    )
    ws.merge_cells("A2:H2")
    ws.row_dimensions[2].height = 32

    headers = [
        "Month",
        "kWh",
        "Rate 1 customer",
        "Rate 1 distribution",
        "Rate 1 transmission",
        "Rate 1 generation",
        "Rate 1 total",
        "Rate HP customer",
        "Rate HP distribution",
        "Rate HP transmission",
        "Rate HP generation",
        "Rate HP total",
    ]
    for col, header in enumerate(headers, start=1):
        _put(ws, 4, col, header, bold=True)
        ws.cell(4, col).alignment = Alignment(wrap_text=True, vertical="bottom")
    ws.row_dimensions[4].height = 32

    first = 5
    first_billed = rates_rows["first_billed"]
    for i in range(12):
        row = first + i
        rate_row = first_billed + i
        _put(ws, row, 1, f"=rates!A{rate_row}")
        kwh_formula = f"=SUMIFS({hourly_sheet}!$B$2:$B${last_hour},{hourly_sheet}!$C$2:$C${last_hour},A{row})"
        _put(ws, row, 2, kwh_formula, fmt=FMT_KWH)
        _put(ws, row, 3, f"=rates!C{rate_row}", fmt=FMT_DOLLAR)
        _put(ws, row, 4, f"=B{row}*rates!D{rate_row}", fmt=FMT_DOLLAR)
        _put(ws, row, 5, f"=B{row}*rates!E{rate_row}", fmt=FMT_DOLLAR)
        _put(ws, row, 6, f"=B{row}*rates!F{rate_row}", fmt=FMT_DOLLAR)
        _put(ws, row, 7, f"=SUM(C{row}:F{row})", fmt=FMT_DOLLAR)
        _put(ws, row, 8, f"=rates!G{rate_row}", fmt=FMT_DOLLAR)
        _put(ws, row, 9, f"=B{row}*rates!H{rate_row}", fmt=FMT_DOLLAR)
        _put(ws, row, 10, f"=B{row}*rates!I{rate_row}", fmt=FMT_DOLLAR)
        _put(ws, row, 11, f"=B{row}*rates!J{rate_row}", fmt=FMT_DOLLAR)
        _put(ws, row, 12, f"=SUM(H{row}:K{row})", fmt=FMT_DOLLAR)
    annual = first + 12
    _put(ws, annual, 1, "Annual", bold=True)
    for col in range(2, 13):
        letter = get_column_letter(col)
        _put(
            ws,
            annual,
            col,
            f"=SUM({letter}{first}:{letter}{annual - 1})",
            fmt=FMT_DOLLAR if col > 2 else FMT_KWH,
            bold=True,
        )

    presented = annual + 2
    _put(ws, presented, 1, "Annual bill, rounded to the cent", bold=True)
    for col, header in enumerate(["Component", "Rate 1", "Rate HP", "Decrease"], start=1):
        _put(ws, presented + 1, col, header, bold=True)
    # Columns on the annual row: customer 3/8, distribution 4/9, transmission 5/10, generation 6/11.
    pairs = [
        ("Customer Charge", "C", "H"),
        ("Distribution", "D", "I"),
        ("Transmission", "E", "J"),
        ("Generation", "F", "K"),
    ]
    first_component = presented + 2
    for offset, (label, rate1_col, hp_col) in enumerate(pairs):
        row = first_component + offset
        _put(ws, row, 1, label)
        _put(ws, row, 2, f"=ROUND({rate1_col}{annual},2)", fmt=FMT_DOLLAR)
        _put(ws, row, 3, f"=ROUND({hp_col}{annual},2)", fmt=FMT_DOLLAR)
        _put(ws, row, 4, f"=B{row}-C{row}", fmt=FMT_DOLLAR)
    total_row = first_component + len(pairs)
    _put(ws, total_row, 1, "Total", bold=True)
    for col in range(2, 5):
        letter = get_column_letter(col)
        _put(
            ws,
            total_row,
            col,
            f"=SUM({letter}{first_component}:{letter}{total_row - 1})",
            fmt=FMT_DOLLAR,
            bold=True,
        )

    _put(ws, total_row + 2, 1, "Winter kWh")
    _put(ws, total_row + 2, 2, f"={hourly_sheet}!G4", fmt=FMT_KWH)
    _put(ws, total_row + 3, 1, "Annual kWh")
    _put(ws, total_row + 3, 2, f"=B{annual}", fmt=FMT_KWH)

    ws.freeze_panes = "A5"
    ws.column_dimensions["A"].width = 38
    for col in range(2, 13):
        ws.column_dimensions[get_column_letter(col)].width = 16
    return {
        "dec_dist": f"$D${first_component + 1}",
        "dec_tx": f"$D${first_component + 2}",
    }


def _write_enrollment(wb: Workbook, enrollment: EnrollmentInputs) -> dict[str, str]:
    ws = wb.create_sheet("enrollment")
    _heading(ws, 1, "Enrollment")
    _put(
        ws,
        2,
        1,
        "The existing row is the stock in place when Rate HP takes effect. "
        "Each later row adds that year's installations and keeps everyone already enrolled.",
        wrap=True,
    )
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 32

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
    _put(ws, new_header, 1, "New installations", bold=True)
    for col, header in enumerate(["Year", "Statewide additions", "Floor", "Ceiling"], start=1):
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
    _put(ws, cum_header - 1, 1, "Cumulative customers", bold=True)
    for col, header in enumerate(["Year", "Floor", "Ceiling"], start=1):
        _put(ws, cum_header, col, header, bold=True)
    existing_row = cum_header + 1
    _put(ws, existing_row, 1, enrollment.years[0] - 1, fmt="0")
    _put(ws, existing_row, 2, f"=$D${existing}", fmt=FMT_COUNT)
    _put(ws, existing_row, 3, f"=$D${existing}", fmt=FMT_COUNT)
    _put(ws, existing_row, 4, "Existing stock, the same at the floor and the ceiling.", wrap=True)
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
    decrease: dict[str, str],
    enrollment: dict[str, str],
) -> None:
    ws = wb.create_sheet("revenue")
    _heading(ws, 1, "Revenue reduction")
    _put(
        ws,
        2,
        1,
        "A full year of bills for the customers enrolled by that year. "
        "Every customer is billed at the per-customer decrease on bill_change. "
        "The starting stock and later enrollees each round to the dollar, then they are added. "
        "The existing customers are included in 2027 through 2031.",
        wrap=True,
    )
    ws.merge_cells("A2:E2")
    ws.row_dimensions[2].height = 48

    _put(ws, 4, 1, "Per-customer distribution decrease")
    _put(ws, 4, 2, f"=bill_change!{decrease['dec_dist']}", fmt=FMT_DOLLAR)
    _put(ws, 5, 1, "Per-customer transmission decrease")
    _put(ws, 5, 2, f"=bill_change!{decrease['dec_tx']}", fmt=FMT_DOLLAR)

    headers = [
        "Year",
        "Floor customers",
        "Floor distribution",
        "Floor transmission",
        "Floor T&D",
        "Ceiling customers",
        "Ceiling distribution",
        "Ceiling transmission",
        "Ceiling T&D",
    ]
    for col, header in enumerate(headers, start=1):
        _put(ws, 9, col, header, bold=True)
        ws.cell(9, col).alignment = Alignment(wrap_text=True, vertical="bottom")
    ws.row_dimensions[9].height = 32

    existing_row = int(enrollment["existing_row"])
    n_rows = int(enrollment["n_rows"])
    floor_existing = f"enrollment!$B${existing_row}"
    ceiling_existing = f"enrollment!$C${existing_row}"
    for i in range(n_rows):
        row = 10 + i
        src = existing_row + i
        floor_new = f"(B{row}-{floor_existing})"
        ceiling_new = f"(F{row}-{ceiling_existing})"
        _put(ws, row, 1, f"=enrollment!A{src}", fmt="0")
        _put(ws, row, 2, f"=enrollment!B{src}", fmt=FMT_COUNT)
        _put(
            ws,
            row,
            3,
            f"=ROUND({floor_existing}*$B$4,0)+ROUND({floor_new}*$B$4,0)",
            fmt=FMT_REVENUE,
        )
        _put(
            ws,
            row,
            4,
            f"=ROUND({floor_existing}*$B$5,0)+ROUND({floor_new}*$B$5,0)",
            fmt=FMT_REVENUE,
        )
        _put(ws, row, 5, f"=C{row}+D{row}", fmt=FMT_REVENUE)
        _put(ws, row, 6, f"=enrollment!C{src}", fmt=FMT_COUNT)
        _put(
            ws,
            row,
            7,
            f"=ROUND({ceiling_existing}*$B$4,0)+ROUND({ceiling_new}*$B$4,0)",
            fmt=FMT_REVENUE,
        )
        _put(
            ws,
            row,
            8,
            f"=ROUND({ceiling_existing}*$B$5,0)+ROUND({ceiling_new}*$B$5,0)",
            fmt=FMT_REVENUE,
        )
        _put(ws, row, 9, f"=G{row}+H{row}", fmt=FMT_REVENUE)
    _put(ws, 10, 10, "2026 is the existing stock. Later rows add each year's new customers.", wrap=True)

    ws.freeze_panes = "A8"
    ws.column_dimensions["A"].width = 46
    for col in range(2, 10):
        ws.column_dimensions[get_column_letter(col)].width = 22
    ws.column_dimensions["J"].width = 36


def build_workbook(case: Case) -> Workbook:
    wb = Workbook()
    _write_readme(wb)
    last_hour = _write_hourly(wb, "home_8760", case.hourly, case.n_buildings, case.total_weight)
    rate_rows = _write_rates(wb, case)
    decrease = _write_bills(
        wb,
        "bill_change",
        "home_8760",
        rate_rows,
        last_hour,
        title="Bill change, representative heat pump customer",
    )
    enrollment = _write_enrollment(wb, case.enrollment)
    _write_revenue(wb, decrease, enrollment)
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
