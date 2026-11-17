"""Helpers for the CIEC-15(a) Excel workpaper.

``ciec_request_15a.qmd`` loads the representative home's monthly kWh, the filed
Rate 1 charges, and the Rate 1 billing determinants, then calls
:func:`build_workbook`. Upload uses :func:`build_ciec_1a_workbook.upload_xlsx`.
Yellow cells are inputs. Every other number is a formula.

Sheets, in order
----------------
representative_home_consumption
    The representative fossil-fuel home's monthly kWh, before and after the
    heat pump. The change and the annual totals are formulas.
rate_1
    Proposed Rate 1. Customer charge, generation supply, distribution, and
    transmission, with each rider in the component it is billed under.
    Distribution and transmission totals are formulas.
representative_home_bills
    Annual bills. The customer charge is the sum of the monthly charges.
    Generation, distribution, and transmission are the monthly kWh times the
    Rate 1 totals. The scaling factor divides the marginal-cost change by the
    distribution and transmission change.
class
    Rate 1 annual bills and billed sales. Customers, kWh, and distribution and
    transmission revenue are formulas.
modified_rate_1
    The revenue the lower distribution and transmission rates remove, divided
    across Rate 1's customers, is the monthly increase. The new customer charge
    adds that increase to the proposed charge.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
N_MONTHS = len(MONTHS)
DRIVE_NAME = "CIEC-15a_customer_charge.xlsx"

SHEET_CONSUMPTION = "representative_home_consumption"
SHEET_RATES = "rate_1"
SHEET_BILLS = "representative_home_bills"
SHEET_CLASS = "class"
SHEET_MODIFIED = "modified_rate_1"

INPUT_FILL = PatternFill("solid", fgColor="FFF2CC")
HEADER_FONT = Font(bold=True)
HEADER_ALIGN = Alignment(wrap_text=True, vertical="center", horizontal="center")

FMT_DOLLAR = "$#,##0.00"
FMT_RATE = "0.00000"
FMT_KWH = "#,##0.00"
FMT_FACTOR = "0.000000%"

CONSUMPTION_HEADER = 1
CONSUMPTION_FIRST = 2
CONSUMPTION_LAST = 13
CONSUMPTION_ANNUAL = 14

RATE_GROUP = 1
RATE_LINE = 2
RATE_FIRST = 3
RATE_LAST = 14
COL_MONTH = 1
COL_CUSTOMER = 2
COL_GENERATION = 3
COL_DIST_FIRST = 4

BILLS_HEADER = 1
BILLS_CUSTOMER = 2
BILLS_GEN = 3
BILLS_DIST = 4
BILLS_TX = 5
BILLS_VOL = 6
BILLS_MC = 7
BILLS_LAMBDA = 8

CLASS_HEADER = 1
CLASS_BILLS = 2
CLASS_MWH = 3
CLASS_CUSTOMERS = 4
CLASS_ANNUAL_KWH = 5
CLASS_MONTHLY_KWH = 6
CLASS_REVENUE = 7

MOD_HEADER = 1
MOD_LAMBDA = 2
MOD_REVENUE = 3
MOD_SHIFT = 4
MOD_CUSTOMERS = 5
MOD_INCREASE = 6
MOD_BASE = 7
MOD_FIXED = 8
MOD_FIXED_ROUNDED = 9
MOD_INCREASE_ROUNDED = 10
MOD_PER_CUSTOMER = 12
MOD_FILED = 14
MOD_REDESIGNED = 15
MOD_GAP = 16
MOD_SCALED = 18
MOD_MC = 19
MOD_COST_GAP = 20


@dataclass(frozen=True)
class RateLine:
    """Twelve monthly rates for one Rate 1 charge."""

    name: str
    monthly_rates: tuple[float, ...]


@dataclass(frozen=True)
class WorkbookInputs:
    """Stored inputs. Later steps are formulas on the sheets."""

    kwh_before: tuple[float, ...]
    kwh_after: tuple[float, ...]
    customer_charge: tuple[float, ...]
    generation: tuple[float, ...]
    distribution: tuple[RateLine, ...]
    transmission: tuple[RateLine, ...]
    marginal_cost_before: float
    marginal_cost_after: float
    annual_bills: float
    billed_mwh: float


@dataclass(frozen=True)
class _Layout:
    """Column of the rate each bill uses. A total column exists only when a component has riders."""

    dist_total: int
    tx_first: int
    tx_total: int
    last_col: int


@dataclass(frozen=True)
class Derived:
    """The formula results, in the same order the sheets compute them."""

    annual_kwh_before: float
    annual_kwh_after: float
    annual_customer_charge_before: float
    annual_customer_charge_after: float
    annual_generation_before: float
    annual_generation_after: float
    annual_distribution_before: float
    annual_distribution_after: float
    annual_transmission_before: float
    annual_transmission_after: float
    customer_charge_delta: float
    generation_delta: float
    distribution_delta: float
    transmission_delta: float
    volumetric_delta: float
    marginal_cost_delta: float
    scaling_factor: float
    class_customers: float
    class_monthly_kwh: float
    class_variable_revenue: float
    class_revenue_shift: float
    fixed_charge_delta: float
    fixed_charge: float
    class_variable_revenue_per_customer: float
    revenue_gap: float
    cost_gap: float


def _finite(value: float, where: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{where} is {value!r}, expected a number")
    number = float(value)
    if number != number or number in (float("inf"), float("-inf")):
        raise ValueError(f"{where} must be finite, got {value}")
    return number


def _twelve(values: Sequence[float], where: str) -> tuple[float, ...]:
    if len(values) != N_MONTHS:
        raise ValueError(f"{where} has {len(values)} values, expected {N_MONTHS}")
    return tuple(_finite(value, f"{where} {month}") for value, month in zip(values, MONTHS, strict=True))


def _lines(lines: Sequence[RateLine], where: str) -> tuple[RateLine, ...]:
    if len(lines) == 0:
        raise ValueError(f"{where} is empty")
    checked: list[RateLine] = []
    for line in lines:
        if line.name == "":
            raise ValueError(f"a {where} charge name is empty")
        checked.append(RateLine(line.name, _twelve(line.monthly_rates, line.name)))
    names = [line.name for line in checked]
    if len(names) != len(set(names)):
        raise ValueError(f"{where} charge names are not unique: {names}")
    return tuple(checked)


def _check(inputs: WorkbookInputs) -> None:
    _twelve(inputs.kwh_before, "kWh before")
    _twelve(inputs.kwh_after, "kWh after")
    _twelve(inputs.customer_charge, "customer charge")
    _twelve(inputs.generation, "generation supply")
    _lines(inputs.distribution, "distribution")
    _lines(inputs.transmission, "transmission")
    names = [line.name for line in (*inputs.distribution, *inputs.transmission)]
    if len(names) != len(set(names)):
        raise ValueError(f"charge names are not unique: {names}")
    _finite(inputs.marginal_cost_before, "marginal cost before")
    _finite(inputs.marginal_cost_after, "marginal cost after")
    bills = _finite(inputs.annual_bills, "annual bills")
    _finite(inputs.billed_mwh, "billed MWh")
    if bills <= 0:
        raise ValueError(f"annual bills must be positive, got {bills}")


def _billed_column(first: int, n_lines: int) -> int:
    """The column a bill multiplies. One charge uses that column; several charges use their total."""
    if n_lines < 1:
        raise ValueError(f"a component needs at least one charge, got {n_lines}")
    return first if n_lines == 1 else first + n_lines


def _layout(inputs: WorkbookInputs) -> _Layout:
    dist_total = _billed_column(COL_DIST_FIRST, len(inputs.distribution))
    tx_first = dist_total + 1
    tx_total = _billed_column(tx_first, len(inputs.transmission))
    return _Layout(dist_total=dist_total, tx_first=tx_first, tx_total=tx_total, last_col=tx_total)


def _monthly_total(lines: Sequence[RateLine]) -> tuple[float, ...]:
    return tuple(sum(line.monthly_rates[month] for line in lines) for month in range(N_MONTHS))


def _dot(kwh: Sequence[float], rates: Sequence[float]) -> float:
    return sum(kwh_month * rate for kwh_month, rate in zip(kwh, rates, strict=True))


def derive(inputs: WorkbookInputs) -> Derived:
    """Python twin of the sheet formulas. Checked against the notebook before writing."""
    _check(inputs)
    annual_kwh_before = sum(inputs.kwh_before)
    annual_kwh_after = sum(inputs.kwh_after)
    annual_customer_before = sum(inputs.customer_charge)
    annual_customer_after = annual_customer_before
    annual_generation_before = _dot(inputs.kwh_before, inputs.generation)
    annual_generation_after = _dot(inputs.kwh_after, inputs.generation)
    distribution = _monthly_total(inputs.distribution)
    transmission = _monthly_total(inputs.transmission)
    annual_distribution_before = _dot(inputs.kwh_before, distribution)
    annual_distribution_after = _dot(inputs.kwh_after, distribution)
    annual_transmission_before = _dot(inputs.kwh_before, transmission)
    annual_transmission_after = _dot(inputs.kwh_after, transmission)
    customer_charge_delta = annual_customer_after - annual_customer_before
    generation_delta = annual_generation_after - annual_generation_before
    distribution_delta = annual_distribution_after - annual_distribution_before
    transmission_delta = annual_transmission_after - annual_transmission_before
    volumetric_delta = distribution_delta + transmission_delta
    marginal_cost_delta = inputs.marginal_cost_after - inputs.marginal_cost_before
    if volumetric_delta == 0:
        raise ValueError("incremental distribution and transmission charges are zero")
    scaling_factor = marginal_cost_delta / volumetric_delta
    class_customers = inputs.annual_bills / 12
    class_monthly_kwh = inputs.billed_mwh * 1000 / 12
    class_variable_revenue = (sum(distribution) + sum(transmission)) * class_monthly_kwh
    class_revenue_shift = (1.0 - scaling_factor) * class_variable_revenue
    base_fixed_charge = annual_customer_before / N_MONTHS
    fixed_charge_delta = class_revenue_shift / (class_customers * 12)
    fixed_charge = base_fixed_charge + fixed_charge_delta
    filed = 12 * base_fixed_charge * class_customers + class_variable_revenue
    redesigned = 12 * fixed_charge * class_customers + scaling_factor * class_variable_revenue
    return Derived(
        annual_kwh_before=annual_kwh_before,
        annual_kwh_after=annual_kwh_after,
        annual_customer_charge_before=annual_customer_before,
        annual_customer_charge_after=annual_customer_after,
        annual_generation_before=annual_generation_before,
        annual_generation_after=annual_generation_after,
        annual_distribution_before=annual_distribution_before,
        annual_distribution_after=annual_distribution_after,
        annual_transmission_before=annual_transmission_before,
        annual_transmission_after=annual_transmission_after,
        customer_charge_delta=customer_charge_delta,
        generation_delta=generation_delta,
        distribution_delta=distribution_delta,
        transmission_delta=transmission_delta,
        volumetric_delta=volumetric_delta,
        marginal_cost_delta=marginal_cost_delta,
        scaling_factor=scaling_factor,
        class_customers=class_customers,
        class_monthly_kwh=class_monthly_kwh,
        class_variable_revenue=class_variable_revenue,
        class_revenue_shift=class_revenue_shift,
        fixed_charge_delta=fixed_charge_delta,
        fixed_charge=fixed_charge,
        class_variable_revenue_per_customer=class_variable_revenue / class_customers,
        revenue_gap=redesigned - filed,
        cost_gap=scaling_factor * volumetric_delta - marginal_cost_delta,
    )


def _put(
    ws: Worksheet,
    row: int,
    col: int,
    value: Any,
    *,
    input_: bool = False,
    fmt: str | None = None,
    bold: bool = False,
) -> None:
    cell = ws.cell(row, col, value)
    if input_:
        cell.fill = INPUT_FILL
    if bold:
        cell.font = HEADER_FONT
        cell.alignment = HEADER_ALIGN
    if fmt:
        cell.number_format = fmt


def _headers(ws: Worksheet, row: int, headers: Sequence[str]) -> None:
    for col, header in enumerate(headers, start=1):
        _put(ws, row, col, header, bold=True)


def _sum_product(kwh_col: str, rate_col: str) -> str:
    return (
        f"=SUMPRODUCT({SHEET_CONSUMPTION}!{kwh_col}{CONSUMPTION_FIRST}:{kwh_col}{CONSUMPTION_LAST},"
        f"{SHEET_RATES}!{rate_col}{RATE_FIRST}:{rate_col}{RATE_LAST})"
    )


def _write_consumption(wb: Workbook, inputs: WorkbookInputs) -> None:
    ws = wb.active
    ws.title = SHEET_CONSUMPTION
    _headers(ws, CONSUMPTION_HEADER, ["Month", "Before", "After", "Change"])
    for offset, (month, before, after) in enumerate(zip(MONTHS, inputs.kwh_before, inputs.kwh_after, strict=True)):
        row = CONSUMPTION_FIRST + offset
        _put(ws, row, 1, month)
        _put(ws, row, 2, before, input_=True, fmt=FMT_KWH)
        _put(ws, row, 3, after, input_=True, fmt=FMT_KWH)
        _put(ws, row, 4, f"=C{row}-B{row}", fmt=FMT_KWH)
    _put(ws, CONSUMPTION_ANNUAL, 1, "Annual", bold=True)
    _put(ws, CONSUMPTION_ANNUAL, 2, f"=SUM(B{CONSUMPTION_FIRST}:B{CONSUMPTION_LAST})", fmt=FMT_KWH, bold=True)
    _put(ws, CONSUMPTION_ANNUAL, 3, f"=SUM(C{CONSUMPTION_FIRST}:C{CONSUMPTION_LAST})", fmt=FMT_KWH, bold=True)
    _put(ws, CONSUMPTION_ANNUAL, 4, f"=C{CONSUMPTION_ANNUAL}-B{CONSUMPTION_ANNUAL}", fmt=FMT_KWH, bold=True)
    ws.column_dimensions["A"].width = 14
    for col in ("B", "C", "D"):
        ws.column_dimensions[col].width = 16
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:D{CONSUMPTION_LAST}"


def _total_formula(row: int, first: int, billed: int) -> str | None:
    if billed == first:
        return None
    return f"=SUM({get_column_letter(first)}{row}:{get_column_letter(billed - 1)}{row})"


def _write_component(ws: Worksheet, group: str, lines: Sequence[RateLine], first: int, billed: int) -> None:
    _put(ws, RATE_GROUP, first, group, bold=True)
    if billed != first:
        ws.merge_cells(start_row=RATE_GROUP, start_column=first, end_row=RATE_GROUP, end_column=billed)
    for offset, line in enumerate(lines):
        _put(ws, RATE_LINE, first + offset, f"{line.name} ($/kWh)", bold=True)
    if billed != first:
        _put(ws, RATE_LINE, billed, "Total ($/kWh)", bold=True)


def _write_component_rates(ws: Worksheet, row: int, lines: Sequence[RateLine], first: int, billed: int) -> None:
    for offset, line in enumerate(lines):
        _put(ws, row, first + offset, line.monthly_rates[row - RATE_FIRST], input_=True, fmt=FMT_RATE)
    total = _total_formula(row, first, billed)
    if total is not None:
        _put(ws, row, billed, total, fmt=FMT_RATE)


def _write_rates(wb: Workbook, inputs: WorkbookInputs, layout: _Layout) -> None:
    ws = wb.create_sheet(SHEET_RATES)
    _put(ws, RATE_GROUP, COL_MONTH, "Month", bold=True)
    _put(ws, RATE_GROUP, COL_CUSTOMER, "Customer charge", bold=True)
    _put(ws, RATE_LINE, COL_CUSTOMER, "Customer charge ($/month)", bold=True)
    _put(ws, RATE_GROUP, COL_GENERATION, "Generation supply", bold=True)
    _put(ws, RATE_LINE, COL_GENERATION, "Generation supply ($/kWh)", bold=True)
    _write_component(ws, "Distribution", inputs.distribution, COL_DIST_FIRST, layout.dist_total)
    _write_component(ws, "Transmission", inputs.transmission, layout.tx_first, layout.tx_total)

    for offset in range(N_MONTHS):
        row = RATE_FIRST + offset
        source = CONSUMPTION_FIRST + offset
        _put(ws, row, COL_MONTH, f"={SHEET_CONSUMPTION}!A{source}")
        _put(ws, row, COL_CUSTOMER, inputs.customer_charge[offset], input_=True, fmt=FMT_DOLLAR)
        _put(ws, row, COL_GENERATION, inputs.generation[offset], input_=True, fmt=FMT_RATE)
        _write_component_rates(ws, row, inputs.distribution, COL_DIST_FIRST, layout.dist_total)
        _write_component_rates(ws, row, inputs.transmission, layout.tx_first, layout.tx_total)
    ws.column_dimensions["A"].width = 12
    for col in range(COL_CUSTOMER, layout.tx_total + 1):
        ws.column_dimensions[get_column_letter(col)].width = 18
    ws.row_dimensions[RATE_LINE].height = 32
    ws.freeze_panes = "B3"
    ws.auto_filter.ref = f"A2:{get_column_letter(layout.tx_total)}{RATE_LAST}"


def _write_bills(wb: Workbook, inputs: WorkbookInputs, layout: _Layout) -> None:
    ws = wb.create_sheet(SHEET_BILLS)
    _headers(ws, BILLS_HEADER, ["Component", "Before", "After", "Change"])
    customer = f"=SUM({SHEET_RATES}!B{RATE_FIRST}:B{RATE_LAST})"
    dist_total = get_column_letter(layout.dist_total)
    tx_total = get_column_letter(layout.tx_total)
    rows = (
        (BILLS_CUSTOMER, "Customer charge", customer, customer, FMT_DOLLAR),
        (BILLS_GEN, "Generation supply", _sum_product("B", "C"), _sum_product("C", "C"), FMT_DOLLAR),
        (BILLS_DIST, "Distribution", _sum_product("B", dist_total), _sum_product("C", dist_total), FMT_DOLLAR),
        (BILLS_TX, "Transmission", _sum_product("B", tx_total), _sum_product("C", tx_total), FMT_DOLLAR),
    )
    for row, label, before, after, fmt in rows:
        _put(ws, row, 1, label)
        _put(ws, row, 2, before, fmt=fmt)
        _put(ws, row, 3, after, fmt=fmt)
        _put(ws, row, 4, f"=C{row}-B{row}", fmt=fmt)
    _put(ws, BILLS_VOL, 1, "Distribution and transmission")
    _put(ws, BILLS_VOL, 2, f"=B{BILLS_DIST}+B{BILLS_TX}", fmt=FMT_DOLLAR)
    _put(ws, BILLS_VOL, 3, f"=C{BILLS_DIST}+C{BILLS_TX}", fmt=FMT_DOLLAR)
    _put(ws, BILLS_VOL, 4, f"=D{BILLS_DIST}+D{BILLS_TX}", fmt=FMT_DOLLAR)
    _put(ws, BILLS_MC, 1, "Marginal T&D cost")
    _put(ws, BILLS_MC, 2, inputs.marginal_cost_before, input_=True, fmt=FMT_DOLLAR)
    _put(ws, BILLS_MC, 3, inputs.marginal_cost_after, input_=True, fmt=FMT_DOLLAR)
    _put(ws, BILLS_MC, 4, f"=C{BILLS_MC}-B{BILLS_MC}", fmt=FMT_DOLLAR)
    _put(ws, BILLS_LAMBDA, 1, "Scaling factor")
    _put(ws, BILLS_LAMBDA, 4, f"=D{BILLS_MC}/D{BILLS_VOL}", fmt=FMT_FACTOR)
    ws.column_dimensions["A"].width = 36
    for col in ("B", "C", "D"):
        ws.column_dimensions[col].width = 18
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:D{BILLS_LAMBDA}"


def _revenue_formula(layout: _Layout) -> str:
    dist_total = get_column_letter(layout.dist_total)
    tx_total = get_column_letter(layout.tx_total)
    return (
        f"=(SUM({SHEET_RATES}!{dist_total}{RATE_FIRST}:{dist_total}{RATE_LAST})"
        f"+SUM({SHEET_RATES}!{tx_total}{RATE_FIRST}:{tx_total}{RATE_LAST}))*B{CLASS_MONTHLY_KWH}"
    )


def _write_class(wb: Workbook, inputs: WorkbookInputs, layout: _Layout) -> None:
    ws = wb.create_sheet(SHEET_CLASS)
    _headers(ws, CLASS_HEADER, ["Determinant", "Value"])
    _put(ws, CLASS_BILLS, 1, "Annual bills rendered")
    _put(ws, CLASS_BILLS, 2, inputs.annual_bills, input_=True, fmt=FMT_KWH)
    _put(ws, CLASS_MWH, 1, "Billed sales (MWh)")
    _put(ws, CLASS_MWH, 2, inputs.billed_mwh, input_=True, fmt=FMT_KWH)
    _put(ws, CLASS_CUSTOMERS, 1, "Rate 1 customers")
    _put(ws, CLASS_CUSTOMERS, 2, f"=B{CLASS_BILLS}/12", fmt=FMT_KWH)
    _put(ws, CLASS_ANNUAL_KWH, 1, "Annual kWh")
    _put(ws, CLASS_ANNUAL_KWH, 2, f"=B{CLASS_MWH}*1000", fmt=FMT_KWH)
    _put(ws, CLASS_MONTHLY_KWH, 1, "Monthly kWh")
    _put(ws, CLASS_MONTHLY_KWH, 2, f"=B{CLASS_ANNUAL_KWH}/12", fmt=FMT_KWH)
    _put(ws, CLASS_REVENUE, 1, "Distribution and transmission revenue")
    _put(ws, CLASS_REVENUE, 2, _revenue_formula(layout), fmt=FMT_DOLLAR)
    ws.column_dimensions["A"].width = 44
    ws.column_dimensions["B"].width = 22
    ws.freeze_panes = "A2"


def _write_modified(wb: Workbook) -> None:
    ws = wb.create_sheet(SHEET_MODIFIED)
    _headers(ws, MOD_HEADER, ["Step", "Value"])
    _put(ws, MOD_LAMBDA, 1, "Scaling factor")
    _put(ws, MOD_LAMBDA, 2, f"={SHEET_BILLS}!D{BILLS_LAMBDA}", fmt=FMT_FACTOR)
    _put(ws, MOD_REVENUE, 1, "Distribution and transmission revenue")
    _put(ws, MOD_REVENUE, 2, f"={SHEET_CLASS}!B{CLASS_REVENUE}", fmt=FMT_DOLLAR)
    _put(ws, MOD_SHIFT, 1, "Delivery revenue removed")
    _put(ws, MOD_SHIFT, 2, f"=(1-B{MOD_LAMBDA})*B{MOD_REVENUE}", fmt=FMT_DOLLAR)
    _put(ws, MOD_CUSTOMERS, 1, "Rate 1 customers")
    _put(ws, MOD_CUSTOMERS, 2, f"={SHEET_CLASS}!B{CLASS_CUSTOMERS}", fmt=FMT_KWH)
    _put(ws, MOD_INCREASE, 1, "Monthly increase")
    _put(ws, MOD_INCREASE, 2, f"=B{MOD_SHIFT}/(B{MOD_CUSTOMERS}*12)", fmt=FMT_DOLLAR)
    _put(ws, MOD_BASE, 1, "Proposed customer charge ($/month)")
    _put(ws, MOD_BASE, 2, f"=AVERAGE({SHEET_RATES}!B{RATE_FIRST}:B{RATE_LAST})", fmt=FMT_DOLLAR)
    _put(ws, MOD_FIXED, 1, "Customer charge")
    _put(ws, MOD_FIXED, 2, f"=B{MOD_BASE}+B{MOD_INCREASE}", fmt=FMT_DOLLAR)
    _put(ws, MOD_FIXED_ROUNDED, 1, "Customer charge, rounded to the cent")
    _put(ws, MOD_FIXED_ROUNDED, 2, f"=ROUND(B{MOD_FIXED},2)", fmt=FMT_DOLLAR)
    _put(ws, MOD_INCREASE_ROUNDED, 1, "Monthly increase, rounded to the cent")
    _put(ws, MOD_INCREASE_ROUNDED, 2, f"=ROUND(B{MOD_INCREASE},2)", fmt=FMT_DOLLAR)
    _put(ws, MOD_PER_CUSTOMER, 1, "Volumetric revenue per customer")
    _put(ws, MOD_PER_CUSTOMER, 2, f"=B{MOD_REVENUE}/{SHEET_CLASS}!B{CLASS_CUSTOMERS}", fmt=FMT_DOLLAR)
    _put(ws, MOD_FILED, 1, "Filed class revenue")
    _put(
        ws,
        MOD_FILED,
        2,
        f"=12*B{MOD_BASE}*{SHEET_CLASS}!B{CLASS_CUSTOMERS}+B{MOD_REVENUE}",
        fmt=FMT_DOLLAR,
    )
    _put(ws, MOD_REDESIGNED, 1, "Redesigned class revenue")
    _put(
        ws,
        MOD_REDESIGNED,
        2,
        f"=12*B{MOD_FIXED}*{SHEET_CLASS}!B{CLASS_CUSTOMERS}+B{MOD_LAMBDA}*B{MOD_REVENUE}",
        fmt=FMT_DOLLAR,
    )
    _put(ws, MOD_GAP, 1, "Revenue gap")
    _put(ws, MOD_GAP, 2, f"=B{MOD_REDESIGNED}-B{MOD_FILED}", fmt=FMT_DOLLAR)
    _put(ws, MOD_SCALED, 1, "Scaled incremental charges")
    _put(ws, MOD_SCALED, 2, f"=B{MOD_LAMBDA}*{SHEET_BILLS}!D{BILLS_VOL}", fmt=FMT_DOLLAR)
    _put(ws, MOD_MC, 1, "Incremental marginal cost")
    _put(ws, MOD_MC, 2, f"={SHEET_BILLS}!D{BILLS_MC}", fmt=FMT_DOLLAR)
    _put(ws, MOD_COST_GAP, 1, "Cost gap")
    _put(ws, MOD_COST_GAP, 2, f"=B{MOD_SCALED}-B{MOD_MC}", fmt=FMT_DOLLAR)
    ws.column_dimensions["A"].width = 48
    ws.column_dimensions["B"].width = 22
    ws.freeze_panes = "A2"


def build_workbook(inputs: WorkbookInputs) -> Workbook:
    """Assemble the CIEC-15(a) workpaper. Inputs are values; the results are formulas."""
    _check(inputs)
    layout = _layout(inputs)
    wb = Workbook()
    _write_consumption(wb, inputs)
    _write_rates(wb, inputs, layout)
    _write_bills(wb, inputs, layout)
    _write_class(wb, inputs, layout)
    _write_modified(wb)
    return wb


def _stored_number(value: object, where: str) -> float:
    if isinstance(value, str):
        raise AssertionError(f"{where} is a formula, expected a stored input")
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise AssertionError(f"{where} is {value!r}, expected a number")
    return float(value)


def _require_formula(value: object, expected: str, where: str) -> None:
    if value != expected:
        raise AssertionError(f"{where}: sheet has {value!r}, expected {expected}")


def _close(actual: float, expected: float, where: str) -> None:
    tolerance = max(1e-6, 1e-9 * abs(expected))
    if abs(actual - expected) > tolerance:
        raise AssertionError(f"{where}: sheet has {actual:.10g}, notebook has {expected:.10g}")


def assert_workbook(path: str | Path, inputs: WorkbookInputs, expected: Derived) -> Derived:
    """Read a saved workbook and check it against the notebook that wrote it.

    Stored inputs are compared to ``inputs``. The charge, the class revenue, and
    the intermediate steps are evaluated from those stored cells and compared to
    ``expected``. Returns the evaluation.
    """
    _check(inputs)
    layout = _layout(inputs)
    wb = load_workbook(path, data_only=False)
    consumption = wb[SHEET_CONSUMPTION]
    stored_before: list[float] = []
    stored_after: list[float] = []
    for offset, month in enumerate(MONTHS):
        row = CONSUMPTION_FIRST + offset
        if consumption.cell(row, 1).value != month:
            raise AssertionError(
                f"consumption row {row}: sheet has {consumption.cell(row, 1).value!r}, expected {month}"
            )
        before = _stored_number(consumption.cell(row, 2).value, f"{month} kWh before")
        after = _stored_number(consumption.cell(row, 3).value, f"{month} kWh after")
        _close(before, inputs.kwh_before[offset], f"{month} kWh before")
        _close(after, inputs.kwh_after[offset], f"{month} kWh after")
        _require_formula(consumption.cell(row, 4).value, f"=C{row}-B{row}", f"{month} kWh change")
        stored_before.append(before)
        stored_after.append(after)
    _require_formula(
        consumption.cell(CONSUMPTION_ANNUAL, 2).value,
        f"=SUM(B{CONSUMPTION_FIRST}:B{CONSUMPTION_LAST})",
        "annual kWh before",
    )
    _require_formula(
        consumption.cell(CONSUMPTION_ANNUAL, 4).value,
        f"=C{CONSUMPTION_ANNUAL}-B{CONSUMPTION_ANNUAL}",
        "annual kWh change",
    )

    rates = wb[SHEET_RATES]
    stored_customer: list[float] = []
    stored_generation: list[float] = []
    stored_distribution: list[list[float]] = [[] for _ in inputs.distribution]
    stored_transmission: list[list[float]] = [[] for _ in inputs.transmission]
    for offset, month in enumerate(MONTHS):
        row = RATE_FIRST + offset
        _require_formula(
            rates.cell(row, COL_MONTH).value, f"={SHEET_CONSUMPTION}!A{CONSUMPTION_FIRST + offset}", f"{month} label"
        )
        customer = _stored_number(rates.cell(row, COL_CUSTOMER).value, f"{month} customer charge")
        generation = _stored_number(rates.cell(row, COL_GENERATION).value, f"{month} generation")
        _close(customer, inputs.customer_charge[offset], f"{month} customer charge")
        _close(generation, inputs.generation[offset], f"{month} generation")
        stored_customer.append(customer)
        stored_generation.append(generation)
        for line_index, line in enumerate(inputs.distribution):
            stored = _stored_number(rates.cell(row, COL_DIST_FIRST + line_index).value, f"{line.name} {month}")
            _close(stored, line.monthly_rates[offset], f"{line.name} {month}")
            stored_distribution[line_index].append(stored)
        dist_total = _total_formula(row, COL_DIST_FIRST, layout.dist_total)
        if dist_total is not None:
            _require_formula(rates.cell(row, layout.dist_total).value, dist_total, f"{month} distribution total")
        for line_index, line in enumerate(inputs.transmission):
            stored = _stored_number(rates.cell(row, layout.tx_first + line_index).value, f"{line.name} {month}")
            _close(stored, line.monthly_rates[offset], f"{line.name} {month}")
            stored_transmission[line_index].append(stored)
        tx_total = _total_formula(row, layout.tx_first, layout.tx_total)
        if tx_total is not None:
            _require_formula(rates.cell(row, layout.tx_total).value, tx_total, f"{month} transmission total")

    bills = wb[SHEET_BILLS]
    customer_formula = f"=SUM({SHEET_RATES}!B{RATE_FIRST}:B{RATE_LAST})"
    dist_total = get_column_letter(layout.dist_total)
    tx_total = get_column_letter(layout.tx_total)
    _require_formula(bills.cell(BILLS_CUSTOMER, 2).value, customer_formula, "customer charge before")
    _require_formula(bills.cell(BILLS_CUSTOMER, 3).value, customer_formula, "customer charge after")
    _require_formula(bills.cell(BILLS_GEN, 2).value, _sum_product("B", "C"), "generation before")
    _require_formula(bills.cell(BILLS_GEN, 3).value, _sum_product("C", "C"), "generation after")
    _require_formula(bills.cell(BILLS_DIST, 2).value, _sum_product("B", dist_total), "distribution before")
    _require_formula(bills.cell(BILLS_TX, 2).value, _sum_product("B", tx_total), "transmission before")
    _require_formula(bills.cell(BILLS_VOL, 4).value, f"=D{BILLS_DIST}+D{BILLS_TX}", "volumetric change")
    stored_mc_before = _stored_number(bills.cell(BILLS_MC, 2).value, "marginal cost before")
    stored_mc_after = _stored_number(bills.cell(BILLS_MC, 3).value, "marginal cost after")
    _close(stored_mc_before, inputs.marginal_cost_before, "marginal cost before")
    _close(stored_mc_after, inputs.marginal_cost_after, "marginal cost after")
    _require_formula(bills.cell(BILLS_MC, 4).value, f"=C{BILLS_MC}-B{BILLS_MC}", "marginal-cost change")
    _require_formula(bills.cell(BILLS_LAMBDA, 4).value, f"=D{BILLS_MC}/D{BILLS_VOL}", "scaling factor")

    klass = wb[SHEET_CLASS]
    stored_bills = _stored_number(klass.cell(CLASS_BILLS, 2).value, "annual bills")
    stored_mwh = _stored_number(klass.cell(CLASS_MWH, 2).value, "billed MWh")
    _close(stored_bills, inputs.annual_bills, "annual bills")
    _close(stored_mwh, inputs.billed_mwh, "billed MWh")
    _require_formula(klass.cell(CLASS_CUSTOMERS, 2).value, f"=B{CLASS_BILLS}/12", "customers")
    _require_formula(klass.cell(CLASS_MONTHLY_KWH, 2).value, f"=B{CLASS_ANNUAL_KWH}/12", "monthly kWh")
    _require_formula(klass.cell(CLASS_REVENUE, 2).value, _revenue_formula(layout), "class revenue")

    modified = wb[SHEET_MODIFIED]
    _require_formula(modified.cell(MOD_LAMBDA, 2).value, f"={SHEET_BILLS}!D{BILLS_LAMBDA}", "scaling factor link")
    _require_formula(modified.cell(MOD_REVENUE, 2).value, f"={SHEET_CLASS}!B{CLASS_REVENUE}", "revenue link")
    _require_formula(modified.cell(MOD_SHIFT, 2).value, f"=(1-B{MOD_LAMBDA})*B{MOD_REVENUE}", "revenue removed")
    _require_formula(modified.cell(MOD_CUSTOMERS, 2).value, f"={SHEET_CLASS}!B{CLASS_CUSTOMERS}", "customers link")
    _require_formula(modified.cell(MOD_INCREASE, 2).value, f"=B{MOD_SHIFT}/(B{MOD_CUSTOMERS}*12)", "monthly increase")
    _require_formula(
        modified.cell(MOD_BASE, 2).value,
        f"=AVERAGE({SHEET_RATES}!B{RATE_FIRST}:B{RATE_LAST})",
        "proposed customer charge",
    )
    _require_formula(modified.cell(MOD_FIXED, 2).value, f"=B{MOD_BASE}+B{MOD_INCREASE}", "customer charge")
    _require_formula(modified.cell(MOD_FIXED_ROUNDED, 2).value, f"=ROUND(B{MOD_FIXED},2)", "rounded charge")
    _require_formula(modified.cell(MOD_INCREASE_ROUNDED, 2).value, f"=ROUND(B{MOD_INCREASE},2)", "rounded increase")

    stored = WorkbookInputs(
        kwh_before=tuple(stored_before),
        kwh_after=tuple(stored_after),
        customer_charge=tuple(stored_customer),
        generation=tuple(stored_generation),
        distribution=tuple(
            RateLine(line.name, tuple(stored_distribution[index])) for index, line in enumerate(inputs.distribution)
        ),
        transmission=tuple(
            RateLine(line.name, tuple(stored_transmission[index])) for index, line in enumerate(inputs.transmission)
        ),
        marginal_cost_before=stored_mc_before,
        marginal_cost_after=stored_mc_after,
        annual_bills=stored_bills,
        billed_mwh=stored_mwh,
    )
    actual = derive(stored)
    for name in (
        "annual_kwh_before",
        "annual_kwh_after",
        "annual_customer_charge_before",
        "annual_customer_charge_after",
        "annual_generation_before",
        "annual_generation_after",
        "annual_distribution_before",
        "annual_distribution_after",
        "annual_transmission_before",
        "annual_transmission_after",
        "customer_charge_delta",
        "generation_delta",
        "distribution_delta",
        "transmission_delta",
        "volumetric_delta",
        "marginal_cost_delta",
        "scaling_factor",
        "class_customers",
        "class_monthly_kwh",
        "class_variable_revenue",
        "class_revenue_shift",
        "fixed_charge_delta",
        "fixed_charge",
        "class_variable_revenue_per_customer",
        "revenue_gap",
        "cost_gap",
    ):
        _close(getattr(actual, name), getattr(expected, name), name)
    return actual
