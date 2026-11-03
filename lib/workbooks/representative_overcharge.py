"""Excel workbooks for the representative-home overcharge and Schedule R-HP rates.

Inputs are values. Bills, marginal-cost products, the overcharge, and the rate
reductions are Excel formulas. The Python twin of those formulas is checked
against ``report_vars`` before the file is written.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import polars as pl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.worksheet.worksheet import Worksheet

from lib.rates_analysis.rate_case_funcs import MONTH_ORDER

_UTC_OFFSET_HOURS = -5
_HOURS = 8760
_MONTH_FIRST = 2
_MONTH_LAST = 13
_ANNUAL = 14
_HOUR_FIRST = 2
_HOUR_LAST = _HOURS + 1
_DOLLAR_TOL = 1e-4
_KWH_TOL = 1e-4
_RATE_TOL = 1e-8

_RATE_NAMES = {
    "customer": "Customer Charge",
    "dist": "Distribution",
    "tx": "Transmission",
    "empower": "EmPOWER Maryland",
    "gen": "Generation",
}

_TESTIMONY_ROWS: list[tuple[str, str, str]] = [
    ("Added electricity use (kWh)", "=monthly!D14", "Table 1"),
    ("Added distribution and transmission charges ($)", "=overcharge!D5", "Table 1"),
    ("Added EmPOWER Maryland charges ($)", "=overcharge!D6", "Table 1"),
    ("Added distribution and transmission costs ($)", "=overcharge!D11", "Table 1"),
    ("Overcharge ($)", "=overcharge!D13", "Table 1"),
    ("Schedule R-HP distribution rate reduction", "=schedule_rhp!B9", "Table 1"),
    ("Schedule R-HP transmission rate reduction", "=schedule_rhp!C9", "Table 1"),
    ("Schedule R-HP EmPOWER rate reduction", "=schedule_rhp!D9", "Table 1"),
    ("Annual electricity use, before (kWh)", "=monthly!B14", "Section III"),
]


@dataclass(frozen=True)
class _Annual:
    kwh_before: float
    kwh_after: float
    customer_before: float
    customer_after: float
    dist_before: float
    dist_after: float
    tx_before: float
    tx_after: float
    empower_before: float
    empower_after: float
    gen_before: float
    gen_after: float
    mc_tx_before: float
    mc_tx_after: float
    mc_dist_before: float
    mc_dist_after: float

    @property
    def kwh_delta(self) -> float:
        return self.kwh_after - self.kwh_before

    @property
    def delivery_charges_delta(self) -> float:
        return (self.dist_after - self.dist_before) + (self.tx_after - self.tx_before)

    @property
    def empower_delta(self) -> float:
        return self.empower_after - self.empower_before

    @property
    def mc_delivery_delta(self) -> float:
        return (self.mc_tx_after + self.mc_dist_after) - (self.mc_tx_before + self.mc_dist_before)

    @property
    def overcharge(self) -> float:
        return self.delivery_charges_delta - self.mc_delivery_delta + self.empower_delta

    def _lambda(self, before: float, after: float, mc_delta: float) -> float:
        return (before + mc_delta) / after

    @property
    def lambda_dist(self) -> float:
        return self._lambda(self.dist_before, self.dist_after, self.mc_dist_after - self.mc_dist_before)

    @property
    def lambda_tx(self) -> float:
        return self._lambda(self.tx_before, self.tx_after, self.mc_tx_after - self.mc_tx_before)

    @property
    def lambda_empower(self) -> float:
        return self.empower_before / self.empower_after


def build_representative_overcharge_workbook(
    path: str | Path,
    *,
    monthly_before: pl.DataFrame,
    monthly_after: pl.DataFrame,
    hourly_before: pl.DataFrame,
    hourly_after: pl.DataFrame,
    mc: pl.DataFrame,
    rate_components: dict[str, dict[str, Any]],
    report_vars: dict[str, Any],
    source_name: str,
    note: str,
    subclass_monthly: pl.DataFrame | None = None,
    hourly_aggregate: pl.DataFrame | None = None,
    n_buildings: int | None = None,
    weight_sum: float | None = None,
    utc_offset_hours: int = _UTC_OFFSET_HOURS,
) -> Path:
    """Write the representative-home workbook and return its path.

    ``monthly_*`` and ``hourly_*`` are the per-customer (or representative-home)
    kWh the notebook billed and multiplied by marginal cost. Timestamps on the
    hourly frames are the UTC stamps ``building_delivery_mc_8760`` shifts.

    Pass ``subclass_monthly`` and ``hourly_aggregate`` together when per-customer
    kWh should be formulas. ``subclass_monthly`` columns: ``month_label``,
    ``customers_before``, ``kwh_total_before``, ``customers_after``,
    ``kwh_total_after``. ``hourly_aggregate`` columns: ``timestamp`` (same clock
    as ``hourly_before``), ``month`` (Jan-Dec label used to pick the customer
    count), ``agg_kwh_before``, ``agg_kwh_after``.

    ``n_buildings`` and ``weight_sum`` are written on the population sheet when
    the hourly kWh are a weighted average rather than a metered subclass.
    """
    if (subclass_monthly is None) != (hourly_aggregate is None):
        raise ValueError("subclass_monthly and hourly_aggregate must be provided together")

    rates = _rates_by_month(rate_components)
    kwh_before = _month_kwh(monthly_before)
    kwh_after = _month_kwh(monthly_after)
    if subclass_monthly is not None and hourly_aggregate is not None:
        _check_subclass_monthly(subclass_monthly, kwh_before, kwh_after)
    aligned = _align_hourly(hourly_before, hourly_after, mc, utc_offset_hours)
    if hourly_aggregate is not None and subclass_monthly is not None:
        _check_hourly_aggregate(aligned, hourly_aggregate, subclass_monthly, utc_offset_hours)
    elif (
        abs(float(aligned["kwh_before"].sum()) - sum(kwh_before.values())) > _KWH_TOL
        or abs(float(aligned["kwh_after"].sum()) - sum(kwh_after.values())) > _KWH_TOL
    ):
        raise AssertionError("Hourly kWh and monthly kWh do not sum to the same year")

    annual = _annual_from_inputs(kwh_before, kwh_after, rates, aligned)
    _assert_report_vars(annual, report_vars)

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    default = wb.active
    assert default is not None
    wb.remove(default)
    _write_population(wb.create_sheet("population"), source_name, note, n_buildings, weight_sum)
    if subclass_monthly is not None:
        _write_subclass_monthly(wb.create_sheet("subclass_monthly"), subclass_monthly)
    _write_monthly(wb.create_sheet("monthly"), kwh_before, kwh_after, from_subclass=subclass_monthly is not None)
    _write_rates(wb.create_sheet("rates"), rates)
    _write_bills(wb.create_sheet("bills"))
    _write_hourly(wb.create_sheet("hourly"), aligned, hourly_aggregate, utc_offset_hours)
    _write_marginal_cost(wb.create_sheet("marginal_cost"), aligned)
    _write_hourly_marginal_cost(wb.create_sheet("hourly_marginal_cost"), has_aggregate=hourly_aggregate is not None)
    _write_overcharge(wb.create_sheet("overcharge"))
    _write_schedule_rhp(wb.create_sheet("schedule_rhp"))
    _write_testimony(wb.create_sheet("testimony"), source_name)
    wb.save(out)
    return out


def _rates_by_month(rate_components: dict[str, dict[str, Any]]) -> dict[str, dict[str, float]]:
    by_month: dict[str, dict[str, float]] = {month: {} for month in MONTH_ORDER}
    expected_unit = {"customer": "$/month"}
    for key, name in _RATE_NAMES.items():
        spec = rate_components[name]
        unit = spec["charge_unit"]
        if unit != expected_unit.get(key, "$/kWh"):
            raise ValueError(f"{name} has charge unit {unit}")
        raw: dict[str, float] = spec["monthly_rates"]
        seen: set[str] = set()
        for rate_key, value in raw.items():
            label = MONTH_ORDER[int(str(rate_key).split("-")[1]) - 1]
            by_month[label][key] = float(value)
            seen.add(label)
        missing = [month for month in MONTH_ORDER if month not in seen]
        if missing:
            raise ValueError(f"{name} is missing months: {missing}")
    return by_month


def _month_kwh(df: pl.DataFrame) -> dict[str, float]:
    labels = df.select(pl.col("month_label").cast(pl.Utf8), pl.col("kwh"))
    out = {str(row["month_label"]): float(row["kwh"]) for row in labels.iter_rows(named=True)}
    missing = [month for month in MONTH_ORDER if month not in out]
    if missing:
        raise ValueError(f"monthly kWh missing months: {missing}")
    return out


def _ordered_subclass(subclass_monthly: pl.DataFrame) -> pl.DataFrame:
    needed = ["month_label", "customers_before", "kwh_total_before", "customers_after", "kwh_total_after"]
    missing = [col for col in needed if col not in subclass_monthly.columns]
    if missing:
        raise ValueError(f"subclass_monthly is missing columns: {missing}")
    frame = subclass_monthly.select(
        pl.col("month_label").cast(pl.Utf8),
        pl.col("customers_before").cast(pl.Float64),
        pl.col("kwh_total_before").cast(pl.Float64),
        pl.col("customers_after").cast(pl.Float64),
        pl.col("kwh_total_after").cast(pl.Float64),
    )
    order = {month: index for index, month in enumerate(MONTH_ORDER)}
    return frame.sort(pl.col("month_label").replace_strict(order))


def _check_subclass_monthly(
    subclass_monthly: pl.DataFrame,
    kwh_before: dict[str, float],
    kwh_after: dict[str, float],
) -> None:
    frame = _ordered_subclass(subclass_monthly)
    if frame.height != 12:
        raise ValueError(f"subclass_monthly has {frame.height} rows, expected 12")
    before_customers = frame.select(pl.col("customers_before").min()).item()
    after_customers = frame.select(pl.col("customers_after").min()).item()
    if (
        not isinstance(before_customers, int | float)
        or not isinstance(after_customers, int | float)
        or before_customers <= 0
        or after_customers <= 0
    ):
        raise ValueError("subclass customer counts must be positive")
    for row in frame.iter_rows(named=True):
        month = str(row["month_label"])
        before = float(row["kwh_total_before"]) / float(row["customers_before"])
        after = float(row["kwh_total_after"]) / float(row["customers_after"])
        if abs(before - kwh_before[month]) > _KWH_TOL or abs(after - kwh_after[month]) > _KWH_TOL:
            raise AssertionError(f"{month}: subclass total/customers does not match the monthly profile")


def _shift(df: pl.DataFrame, hours: int) -> pl.DataFrame:
    return df.with_columns((pl.col("timestamp") + pl.duration(hours=hours)).alias("timestamp"))


def _drop_time_zone(df: pl.DataFrame) -> pl.DataFrame:
    dtype = df.schema["timestamp"]
    if isinstance(dtype, pl.Datetime) and dtype.time_zone is not None:
        return df.with_columns(pl.col("timestamp").dt.replace_time_zone(None))
    return df


def _align_hourly(
    hourly_before: pl.DataFrame,
    hourly_after: pl.DataFrame,
    mc: pl.DataFrame,
    utc_offset_hours: int,
) -> pl.DataFrame:
    joined = (
        _shift(hourly_before, utc_offset_hours)
        .rename({"kwh": "kwh_before"})
        .join(_shift(hourly_after, utc_offset_hours).rename({"kwh": "kwh_after"}), on="timestamp")
        .join(mc.select("timestamp", "mc_bulk_tx", "mc_dist_sub_tx"), on="timestamp")
        .sort("timestamp")
    )
    if joined.height != _HOURS:
        raise ValueError(
            f"Expected {_HOURS} hours after aligning load and marginal cost, got {joined.height}. Check the UTC offset."
        )
    return _drop_time_zone(joined)


def _check_hourly_aggregate(
    aligned: pl.DataFrame,
    hourly_aggregate: pl.DataFrame,
    subclass_monthly: pl.DataFrame,
    utc_offset_hours: int,
) -> None:
    needed = ["timestamp", "month", "agg_kwh_before", "agg_kwh_after"]
    missing = [col for col in needed if col not in hourly_aggregate.columns]
    if missing:
        raise ValueError(f"hourly_aggregate is missing columns: {missing}")
    customers = {
        str(row["month_label"]): (float(row["customers_before"]), float(row["customers_after"]))
        for row in _ordered_subclass(subclass_monthly).iter_rows(named=True)
    }
    agg = _drop_time_zone(_shift(hourly_aggregate, utc_offset_hours)).with_columns(pl.col("month").cast(pl.Utf8))
    joined = aligned.join(agg, on="timestamp")
    if joined.height != _HOURS:
        raise ValueError("hourly aggregate timestamps do not match the load profile")
    checked = joined.with_columns(
        joined["month"].replace_strict({month: pair[0] for month, pair in customers.items()}).alias("customers_before"),
        joined["month"].replace_strict({month: pair[1] for month, pair in customers.items()}).alias("customers_after"),
    )
    before_gap = checked.select(
        (pl.col("agg_kwh_before") / pl.col("customers_before") - pl.col("kwh_before")).abs().max()
    ).item()
    after_gap = checked.select(
        (pl.col("agg_kwh_after") / pl.col("customers_after") - pl.col("kwh_after")).abs().max()
    ).item()
    if not isinstance(before_gap, int | float) or not isinstance(after_gap, int | float):
        raise AssertionError("aggregate kWh / customer count does not match the hourly profile")
    if before_gap > _KWH_TOL or after_gap > _KWH_TOL:
        raise AssertionError("aggregate kWh / customer count does not match the hourly profile")


def _annual_from_inputs(
    kwh_before: dict[str, float],
    kwh_after: dict[str, float],
    rates: dict[str, dict[str, float]],
    aligned: pl.DataFrame,
) -> _Annual:
    totals = {f"{key}_{period}": 0.0 for key in _RATE_NAMES for period in ("before", "after")}
    for month in MONTH_ORDER:
        rate = rates[month]
        for period, kwh in (("before", kwh_before[month]), ("after", kwh_after[month])):
            totals[f"customer_{period}"] += rate["customer"]
            for key in ("dist", "tx", "empower", "gen"):
                totals[f"{key}_{period}"] += kwh * rate[key]
    mc_tx_before = float((aligned["kwh_before"] * aligned["mc_bulk_tx"]).sum())
    mc_tx_after = float((aligned["kwh_after"] * aligned["mc_bulk_tx"]).sum())
    mc_dist_before = float((aligned["kwh_before"] * aligned["mc_dist_sub_tx"]).sum())
    mc_dist_after = float((aligned["kwh_after"] * aligned["mc_dist_sub_tx"]).sum())
    return _Annual(
        kwh_before=sum(kwh_before.values()),
        kwh_after=sum(kwh_after.values()),
        customer_before=totals["customer_before"],
        customer_after=totals["customer_after"],
        dist_before=totals["dist_before"],
        dist_after=totals["dist_after"],
        tx_before=totals["tx_before"],
        tx_after=totals["tx_after"],
        empower_before=totals["empower_before"],
        empower_after=totals["empower_after"],
        gen_before=totals["gen_before"],
        gen_after=totals["gen_after"],
        mc_tx_before=mc_tx_before,
        mc_tx_after=mc_tx_after,
        mc_dist_before=mc_dist_before,
        mc_dist_after=mc_dist_after,
    )


def _assert_close(actual: float, report_vars: dict[str, Any], key: str, tol: float) -> None:
    expected = float(report_vars[key])
    if abs(actual - expected) > tol:
        raise AssertionError(f"{key}: inputs produce {actual:.10g}, report variable is {expected:.10g}")


def _assert_report_vars(annual: _Annual, report_vars: dict[str, Any]) -> None:
    _assert_close(annual.kwh_before, report_vars, "all_fossil_annual_kwh_before", _KWH_TOL)
    _assert_close(annual.kwh_after, report_vars, "all_fossil_annual_kwh_after", _KWH_TOL)
    _assert_close(annual.kwh_delta, report_vars, "all_fossil_annual_kwh_delta", _KWH_TOL)
    pairs = [
        ("customer", "customer_charge"),
        ("dist", "distribution"),
        ("tx", "transmission"),
        ("empower", "empower_maryland"),
        ("gen", "generation"),
    ]
    for key, var in pairs:
        _assert_close(getattr(annual, f"{key}_before"), report_vars, f"all_fossil_annual_{var}_before", _DOLLAR_TOL)
        _assert_close(getattr(annual, f"{key}_after"), report_vars, f"all_fossil_annual_{var}_after", _DOLLAR_TOL)
    _assert_close(annual.delivery_charges_delta, report_vars, "all_fossil_annual_delivery_charges_delta", _DOLLAR_TOL)
    _assert_close(annual.empower_delta, report_vars, "all_fossil_annual_empower_maryland_delta", _DOLLAR_TOL)
    _assert_close(annual.mc_tx_before, report_vars, "all_fossil_annual_mc_tx_before", _DOLLAR_TOL)
    _assert_close(annual.mc_tx_after, report_vars, "all_fossil_annual_mc_tx_after", _DOLLAR_TOL)
    _assert_close(annual.mc_dist_before, report_vars, "all_fossil_annual_mc_dist_before", _DOLLAR_TOL)
    _assert_close(annual.mc_dist_after, report_vars, "all_fossil_annual_mc_dist_after", _DOLLAR_TOL)
    _assert_close(
        annual.mc_tx_before + annual.mc_dist_before,
        report_vars,
        "all_fossil_annual_mc_delivery_before",
        _DOLLAR_TOL,
    )
    _assert_close(
        annual.mc_tx_after + annual.mc_dist_after,
        report_vars,
        "all_fossil_annual_mc_delivery_after",
        _DOLLAR_TOL,
    )
    _assert_close(annual.overcharge, report_vars, "all_fossil_annual_total_overcharge", _DOLLAR_TOL)
    _assert_close(annual.lambda_dist, report_vars, "rhp_lambda_dist", _RATE_TOL)
    _assert_close(annual.lambda_tx, report_vars, "rhp_lambda_tx", _RATE_TOL)
    _assert_close(annual.lambda_empower, report_vars, "rhp_lambda_empower", _RATE_TOL)
    _assert_close(annual.lambda_dist - 1.0, report_vars, "rhp_pct_change_dist", _RATE_TOL)
    _assert_close(annual.lambda_tx - 1.0, report_vars, "rhp_pct_change_tx", _RATE_TOL)
    _assert_close(annual.lambda_empower - 1.0, report_vars, "rhp_pct_change_empower", _RATE_TOL)
    fair_dist = annual.dist_before + (annual.mc_dist_after - annual.mc_dist_before)
    fair_tx = annual.tx_before + (annual.mc_tx_after - annual.mc_tx_before)
    _assert_close(fair_dist, report_vars, "rhp_fair_dist_bill_after", _DOLLAR_TOL)
    _assert_close(fair_tx, report_vars, "rhp_fair_tx_bill_after", _DOLLAR_TOL)
    _assert_close(annual.dist_after / annual.kwh_after, report_vars, "rhp_avg_rate_dist", _RATE_TOL)
    _assert_close(annual.tx_after / annual.kwh_after, report_vars, "rhp_avg_rate_tx", _RATE_TOL)
    _assert_close(annual.empower_after / annual.kwh_after, report_vars, "rhp_avg_rate_empower", _RATE_TOL)
    _assert_close(annual.dist_after / annual.kwh_after * annual.lambda_dist, report_vars, "rhp_rate_dist", _RATE_TOL)
    _assert_close(annual.tx_after / annual.kwh_after * annual.lambda_tx, report_vars, "rhp_rate_tx", _RATE_TOL)
    _assert_close(
        annual.empower_after / annual.kwh_after * annual.lambda_empower,
        report_vars,
        "rhp_rate_empower",
        _RATE_TOL,
    )


def _header(ws: Worksheet, row: int, headers: list[str]) -> None:
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row, col, header)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True)


def _excel_timestamp(value: object) -> datetime:
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    raise TypeError(f"Expected a datetime, got {type(value).__name__}")


def _write_population(
    ws: Worksheet,
    source_name: str,
    note: str,
    n_buildings: int | None,
    weight_sum: float | None,
) -> None:
    ws["A1"] = source_name
    ws["A1"].font = Font(bold=True)
    text = note.rstrip() + "\n\nValues are inputs. Every later step is an Excel formula."
    ws.merge_cells("A2:F2")
    ws["A2"] = text
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[2].height = 96
    row = 4
    if n_buildings is not None:
        ws.cell(row, 1, "Buildings in the average")
        ws.cell(row, 2, n_buildings)
        row += 1
    if weight_sum is not None:
        ws.cell(row, 1, "Sum of sample weights")
        ws.cell(row, 2, weight_sum)
    ws.column_dimensions["A"].width = 36
    for col in "BCDEF":
        ws.column_dimensions[col].width = 22


def _write_subclass_monthly(ws: Worksheet, subclass_monthly: pl.DataFrame) -> None:
    frame = _ordered_subclass(subclass_monthly)
    _header(
        ws,
        1,
        [
            "month",
            "customers_before",
            "kwh_total_before",
            "customers_after",
            "kwh_total_after",
            "kwh_per_customer_before",
            "kwh_per_customer_after",
        ],
    )
    for index, row in enumerate(frame.iter_rows(named=True)):
        excel_row = _MONTH_FIRST + index
        ws.cell(excel_row, 1, str(row["month_label"]))
        ws.cell(excel_row, 2, float(row["customers_before"]))
        ws.cell(excel_row, 3, float(row["kwh_total_before"]))
        ws.cell(excel_row, 4, float(row["customers_after"]))
        ws.cell(excel_row, 5, float(row["kwh_total_after"]))
        ws.cell(excel_row, 6, f"=C{excel_row}/B{excel_row}")
        ws.cell(excel_row, 7, f"=E{excel_row}/D{excel_row}")
    ws.column_dimensions["A"].width = 12
    for col in "BCDEFG":
        ws.column_dimensions[col].width = 24


def _write_monthly(
    ws: Worksheet,
    kwh_before: dict[str, float],
    kwh_after: dict[str, float],
    *,
    from_subclass: bool,
) -> None:
    _header(ws, 1, ["month", "kwh_before", "kwh_after", "kwh_change"])
    for index, month in enumerate(MONTH_ORDER):
        excel_row = _MONTH_FIRST + index
        ws.cell(excel_row, 1, month)
        if from_subclass:
            ws.cell(excel_row, 2, f"=subclass_monthly!F{excel_row}")
            ws.cell(excel_row, 3, f"=subclass_monthly!G{excel_row}")
        else:
            ws.cell(excel_row, 2, kwh_before[month])
            ws.cell(excel_row, 3, kwh_after[month])
        ws.cell(excel_row, 4, f"=C{excel_row}-B{excel_row}")
    ws.cell(_ANNUAL, 1, "Annual").font = Font(bold=True)
    for col in "BCD":
        ws[f"{col}{_ANNUAL}"] = f"=SUM({col}{_MONTH_FIRST}:{col}{_MONTH_LAST})"
        ws[f"{col}{_ANNUAL}"].font = Font(bold=True)


def _write_rates(ws: Worksheet, rates: dict[str, dict[str, float]]) -> None:
    _header(
        ws,
        1,
        [
            "month",
            "customer_$/month",
            "distribution_$/kwh",
            "transmission_$/kwh",
            "empower_$/kwh",
            "generation_$/kwh",
        ],
    )
    keys = ["customer", "dist", "tx", "empower", "gen"]
    for index, month in enumerate(MONTH_ORDER):
        excel_row = _MONTH_FIRST + index
        ws.cell(excel_row, 1, month)
        for offset, key in enumerate(keys):
            cell = ws.cell(excel_row, 2 + offset, rates[month][key])
            cell.number_format = "0.00" if key == "customer" else "0.000000"
    for col in "ABCDEF":
        ws.column_dimensions[col].width = 22


def _write_bills(ws: Worksheet) -> None:
    groups = [
        (1, 3, "Monthly consumption"),
        (4, 9, "Before"),
        (10, 15, "After"),
    ]
    for start, end, title in groups:
        ws.merge_cells(start_row=1, start_column=start, end_row=1, end_column=end)
        ws.cell(1, start, title).font = Font(bold=True)
    _header(
        ws,
        2,
        [
            "month",
            "kwh_before",
            "kwh_after",
            "customer_before",
            "distribution_before",
            "transmission_before",
            "empower_before",
            "generation_before",
            "total_before",
            "customer_after",
            "distribution_after",
            "transmission_after",
            "empower_after",
            "generation_after",
            "total_after",
        ],
    )
    # Headers occupy row 2, so the month rows are shifted down one from `monthly`.
    for index in range(12):
        source = _MONTH_FIRST + index
        row = source + 1
        ws.cell(row, 1, f"=monthly!A{source}")
        ws.cell(row, 2, f"=monthly!B{source}")
        ws.cell(row, 3, f"=monthly!C{source}")
        for base, kwh_col in ((4, "B"), (10, "C")):
            ws.cell(row, base, f"=rates!B{source}")
            ws.cell(row, base + 1, f"={kwh_col}{row}*rates!C{source}")
            ws.cell(row, base + 2, f"={kwh_col}{row}*rates!D{source}")
            ws.cell(row, base + 3, f"={kwh_col}{row}*rates!E{source}")
            ws.cell(row, base + 4, f"={kwh_col}{row}*rates!F{source}")
            ws.cell(row, base + 5, f"=SUM({_col(base)}{row}:{_col(base + 4)}{row})")
    annual = _ANNUAL + 1
    ws.cell(annual, 1, "Annual").font = Font(bold=True)
    for col in range(2, 16):
        letter = _col(col)
        cell = ws.cell(annual, col, f"=SUM({letter}3:{letter}{annual - 1})")
        cell.font = Font(bold=True)
    ws.column_dimensions["A"].width = 12


def _col(index: int) -> str:
    letters = ""
    while index:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def _write_hourly(
    ws: Worksheet,
    aligned: pl.DataFrame,
    hourly_aggregate: pl.DataFrame | None,
    utc_offset_hours: int,
) -> None:
    timestamps = [_excel_timestamp(value) for value in aligned["timestamp"].to_list()]
    if hourly_aggregate is None:
        _header(ws, 1, ["timestamp", "kwh_before", "kwh_after"])
        kwh_before = aligned["kwh_before"].to_list()
        kwh_after = aligned["kwh_after"].to_list()
        for index, timestamp in enumerate(timestamps):
            row = _HOUR_FIRST + index
            ws.cell(row, 1, timestamp)
            ws.cell(row, 2, float(kwh_before[index]))
            ws.cell(row, 3, float(kwh_after[index]))
        return

    agg = _drop_time_zone(_shift(hourly_aggregate, utc_offset_hours))
    agg = aligned.select("timestamp").join(
        agg.select("timestamp", pl.col("month").cast(pl.Utf8), "agg_kwh_before", "agg_kwh_after"),
        on="timestamp",
    )
    _header(
        ws,
        1,
        [
            "timestamp",
            "month",
            "agg_kwh_before",
            "agg_kwh_after",
            "customers_before",
            "customers_after",
            "kwh_before",
            "kwh_after",
        ],
    )
    months = agg["month"].to_list()
    agg_before = agg["agg_kwh_before"].to_list()
    agg_after = agg["agg_kwh_after"].to_list()
    lookup = "subclass_monthly!$A$2:$G$13"
    for index, timestamp in enumerate(timestamps):
        row = _HOUR_FIRST + index
        ws.cell(row, 1, timestamp)
        ws.cell(row, 2, str(months[index]))
        ws.cell(row, 3, float(agg_before[index]))
        ws.cell(row, 4, float(agg_after[index]))
        ws.cell(row, 5, f"=VLOOKUP(B{row},{lookup},2,FALSE)")
        ws.cell(row, 6, f"=VLOOKUP(B{row},{lookup},4,FALSE)")
        ws.cell(row, 7, f"=C{row}/E{row}")
        ws.cell(row, 8, f"=D{row}/F{row}")


def _write_marginal_cost(ws: Worksheet, aligned: pl.DataFrame) -> None:
    _header(ws, 1, ["timestamp", "mc_bulk_tx_per_kwh", "mc_dist_sub_tx_per_kwh"])
    timestamps = [_excel_timestamp(value) for value in aligned["timestamp"].to_list()]
    tx = aligned["mc_bulk_tx"].to_list()
    dist = aligned["mc_dist_sub_tx"].to_list()
    for index, timestamp in enumerate(timestamps):
        row = _HOUR_FIRST + index
        ws.cell(row, 1, timestamp)
        ws.cell(row, 2, float(tx[index]))
        ws.cell(row, 3, float(dist[index]))


def _write_hourly_marginal_cost(ws: Worksheet, *, has_aggregate: bool) -> None:
    _header(
        ws,
        1,
        [
            "timestamp",
            "kwh_before",
            "kwh_after",
            "mc_bulk_tx_per_kwh",
            "mc_dist_sub_tx_per_kwh",
            "bulk_tx_dollars_before",
            "dist_dollars_before",
            "total_dollars_before",
            "bulk_tx_dollars_after",
            "dist_dollars_after",
            "total_dollars_after",
        ],
    )
    kwh_before_col = "G" if has_aggregate else "B"
    kwh_after_col = "H" if has_aggregate else "C"
    for row in range(_HOUR_FIRST, _HOUR_LAST + 1):
        ws.cell(row, 1, f"=hourly!A{row}")
        ws.cell(row, 2, f"=hourly!{kwh_before_col}{row}")
        ws.cell(row, 3, f"=hourly!{kwh_after_col}{row}")
        ws.cell(row, 4, f"=marginal_cost!B{row}")
        ws.cell(row, 5, f"=marginal_cost!C{row}")
        ws.cell(row, 6, f"=B{row}*D{row}")
        ws.cell(row, 7, f"=B{row}*E{row}")
        ws.cell(row, 8, f"=F{row}+G{row}")
        ws.cell(row, 9, f"=C{row}*D{row}")
        ws.cell(row, 10, f"=C{row}*E{row}")
        ws.cell(row, 11, f"=I{row}+J{row}")
    ws["M1"] = "Component"
    ws["N1"] = "Before ($)"
    ws["O1"] = "After ($)"
    ws["P1"] = "After - before ($)"
    for cell in ("M1", "N1", "O1", "P1"):
        ws[cell].font = Font(bold=True)
    summary = [
        (2, "Bulk transmission", f"=SUM(F{_HOUR_FIRST}:F{_HOUR_LAST})", f"=SUM(I{_HOUR_FIRST}:I{_HOUR_LAST})"),
        (
            3,
            "Distribution and sub-transmission",
            f"=SUM(G{_HOUR_FIRST}:G{_HOUR_LAST})",
            f"=SUM(J{_HOUR_FIRST}:J{_HOUR_LAST})",
        ),
        (4, "Total", f"=SUM(H{_HOUR_FIRST}:H{_HOUR_LAST})", f"=SUM(K{_HOUR_FIRST}:K{_HOUR_LAST})"),
    ]
    for row, label, before, after in summary:
        ws.cell(row, 13, label)
        ws.cell(row, 14, before)
        ws.cell(row, 15, after)
        ws.cell(row, 16, f"=O{row}-N{row}")
    ws.column_dimensions["M"].width = 40


def _write_overcharge(ws: Worksheet) -> None:
    ws["A1"] = "Overcharge = added distribution and transmission charges - added T&D cost + added EmPOWER charges"
    ws["A1"].font = Font(bold=True)
    _header(ws, 2, ["Component", "Before ($)", "After ($)", "Change ($)"])
    # bills headers are on row 2 and months on rows 3-14, so the annual row is 15.
    bills_annual = _ANNUAL + 1
    rows = [
        (3, "Distribution charges", f"=bills!E{bills_annual}", f"=bills!K{bills_annual}"),
        (4, "Transmission charges", f"=bills!F{bills_annual}", f"=bills!L{bills_annual}"),
        (5, "Distribution and transmission charges", "=B3+B4", "=C3+C4"),
        (6, "EmPOWER Maryland charges", f"=bills!G{bills_annual}", f"=bills!M{bills_annual}"),
        (7, "Customer charge (unchanged)", f"=bills!D{bills_annual}", f"=bills!J{bills_annual}"),
        (9, "Bulk transmission marginal cost", "=hourly_marginal_cost!N2", "=hourly_marginal_cost!O2"),
        (10, "Distribution marginal cost", "=hourly_marginal_cost!N3", "=hourly_marginal_cost!O3"),
        (11, "Distribution and transmission marginal cost", "=hourly_marginal_cost!N4", "=hourly_marginal_cost!O4"),
    ]
    for row, label, before, after in rows:
        ws.cell(row, 1, label)
        ws.cell(row, 2, before)
        ws.cell(row, 3, after)
        ws.cell(row, 4, f"=C{row}-B{row}")
    ws["A13"] = "Overcharge"
    ws["A13"].font = Font(bold=True)
    ws["D13"] = "=D5-D11+D6"
    ws["D13"].font = Font(bold=True)
    ws.column_dimensions["A"].width = 56
    for col in "BCD":
        ws.column_dimensions[col].width = 18


def _write_schedule_rhp(ws: Worksheet) -> None:
    ws["A1"] = "Schedule R-HP: post-retrofit bill equals the pre-retrofit bill plus the marginal-cost increase"
    ws["A1"].font = Font(bold=True)
    _header(ws, 2, ["Step", "Distribution", "Transmission", "EmPOWER Maryland", "How it is computed"])
    steps = [
        (3, "Charges, pre-retrofit ($/yr)", "=overcharge!B3", "=overcharge!B4", "=overcharge!B6", "Annual charges"),
        (4, "Charges, post-retrofit ($/yr)", "=overcharge!C3", "=overcharge!C4", "=overcharge!C6", "Annual charges"),
        (
            5,
            "Marginal-cost change ($/yr)",
            "=overcharge!D10",
            "=overcharge!D9",
            "=0",
            "EmPOWER has no marginal-cost change",
        ),
        (
            6,
            "Fair post-retrofit charges ($/yr)",
            "=B3+B5",
            "=C3+C5",
            "=D3",
            "Pre-retrofit charges plus the cost change. EmPOWER stays flat",
        ),
        (7, "Scale factor", "=B6/B4", "=C6/C4", "=D6/D4", "Fair charges / post-retrofit charges"),
        (8, "Percent change", "=B7-1", "=C7-1", "=D7-1", "Scale factor minus 1"),
        (
            9,
            "Rate reduction in the testimony",
            "=-B8",
            "=-C8",
            "=-D8",
            "The testimony prints the cut as a positive share",
        ),
    ]
    for row, label, dist, tx, empower, how in steps:
        ws.cell(row, 1, label)
        ws.cell(row, 2, dist)
        ws.cell(row, 3, tx)
        ws.cell(row, 4, empower)
        ws.cell(row, 5, how)
        if row in (8, 9):
            for col in "BCD":
                ws[f"{col}{row}"].number_format = "0.00%"
    ws["A9"].font = Font(bold=True)
    ws["A11"] = "Annual kWh, post-retrofit"
    ws["B11"] = f"=monthly!C{_ANNUAL}"
    ws["E11"] = "Monthly sheet"
    ws["A12"] = "Schedule R average rate ($/kWh)"
    ws["B12"] = "=B4/$B$11"
    ws["C12"] = "=C4/$B$11"
    ws["D12"] = "=D4/$B$11"
    ws["E12"] = "Post-retrofit charges / post-retrofit kWh"
    ws["A13"] = "Schedule R-HP rate ($/kWh)"
    ws["B13"] = "=B12*B7"
    ws["C13"] = "=C12*C7"
    ws["D13"] = "=D12*D7"
    ws["E13"] = "Average rate times the scale factor"
    for col in "BCDE":
        ws[f"{col}12"].number_format = "0.000000"
        ws[f"{col}13"].number_format = "0.000000"
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["E"].width = 62
    for col in "BCD":
        ws.column_dimensions[col].width = 22


def _write_testimony(ws: Worksheet, source_name: str) -> None:
    ws["A1"] = f"Surrebuttal numbers from this workbook ({source_name})"
    ws["A1"].font = Font(bold=True)
    _header(ws, 2, ["Item", "Value", "Where it appears"])
    for offset, (label, formula, where) in enumerate(_TESTIMONY_ROWS):
        row = 3 + offset
        ws.cell(row, 1, label)
        ws.cell(row, 2, formula)
        ws.cell(row, 3, where)
        if "reduction" in label:
            ws.cell(row, 2).number_format = "0.00%"
        if label.startswith("Overcharge"):
            ws.cell(row, 1).font = Font(bold=True)
            ws.cell(row, 2).font = Font(bold=True)
    ws.column_dimensions["A"].width = 62
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 16
