"""Workbook builders recompute cited figures and keep later steps as formulas."""

from __future__ import annotations

from datetime import datetime

import polars as pl
import pytest
from openpyxl import Workbook, load_workbook

from lib.rates_analysis.rate_case_funcs import MONTH_ORDER
from lib.workbooks.bill_decrease_share import build_bill_decrease_share_workbook
from lib.workbooks.representative_overcharge import build_representative_overcharge_workbook

_KWH_BEFORE = 0.1
_KWH_AFTER = 0.2
_MC_TX = 0.01
_MC_DIST = 0.02


def _local_hours() -> pl.Series:
    hours = pl.datetime_range(datetime(2025, 1, 1), datetime(2025, 12, 31, 23), interval="1h", eager=True)
    assert hours.len() == 8760
    return hours


def _rates() -> dict[str, dict[str, object]]:
    specs = [
        ("Customer Charge", "$/month", "customer", 8.0),
        ("Distribution", "$/kWh", "dist", 0.05),
        ("Transmission", "$/kWh", "tx", 0.02),
        ("EmPOWER Maryland", "$/kWh", "empower", 0.01),
        ("Generation", "$/kWh", "gen", 0.08),
    ]
    components: dict[str, dict[str, object]] = {}
    for name, unit, key, base in specs:
        monthly = {}
        for index, month in enumerate(MONTH_ORDER):
            value = base + 0.01 if key == "dist" and month == "Jan" else base
            monthly[f"2025-{index + 1:02d}"] = value
        components[name] = {"charge_unit": unit, "monthly_rates": monthly}
    return components


def _rate_for(month: str, key: str) -> float:
    if key == "customer":
        return 8.0
    if key == "dist" and month == "Jan":
        return 0.06
    return {"dist": 0.05, "tx": 0.02, "empower": 0.01, "gen": 0.08}[key]


def _report_vars(monthly_before: dict[str, float], monthly_after: dict[str, float]) -> dict[str, float]:
    keys = ("customer", "dist", "tx", "empower", "gen")
    totals: dict[str, float] = {f"{key}_{period}": 0.0 for key in keys for period in ("before", "after")}
    for month in MONTH_ORDER:
        for period, kwh in (("before", monthly_before[month]), ("after", monthly_after[month])):
            totals[f"customer_{period}"] += _rate_for(month, "customer")
            for key in ("dist", "tx", "empower", "gen"):
                totals[f"{key}_{period}"] += kwh * _rate_for(month, key)
    hours = 8760
    mc_tx_before = hours * _KWH_BEFORE * _MC_TX
    mc_tx_after = hours * _KWH_AFTER * _MC_TX
    mc_dist_before = hours * _KWH_BEFORE * _MC_DIST
    mc_dist_after = hours * _KWH_AFTER * _MC_DIST
    kwh_before = sum(monthly_before.values())
    kwh_after = sum(monthly_after.values())
    delivery_delta = (totals["dist_after"] - totals["dist_before"]) + (totals["tx_after"] - totals["tx_before"])
    empower_delta = totals["empower_after"] - totals["empower_before"]
    mc_delta = (mc_tx_after + mc_dist_after) - (mc_tx_before + mc_dist_before)
    lambda_dist = (totals["dist_before"] + (mc_dist_after - mc_dist_before)) / totals["dist_after"]
    lambda_tx = (totals["tx_before"] + (mc_tx_after - mc_tx_before)) / totals["tx_after"]
    lambda_empower = totals["empower_before"] / totals["empower_after"]
    names = {
        "customer": "customer_charge",
        "dist": "distribution",
        "tx": "transmission",
        "empower": "empower_maryland",
        "gen": "generation",
    }
    report: dict[str, float] = {
        "all_fossil_annual_kwh_before": kwh_before,
        "all_fossil_annual_kwh_after": kwh_after,
        "all_fossil_annual_kwh_delta": kwh_after - kwh_before,
        "all_fossil_annual_delivery_charges_delta": delivery_delta,
        "all_fossil_annual_empower_maryland_delta": empower_delta,
        "all_fossil_annual_mc_tx_before": mc_tx_before,
        "all_fossil_annual_mc_tx_after": mc_tx_after,
        "all_fossil_annual_mc_dist_before": mc_dist_before,
        "all_fossil_annual_mc_dist_after": mc_dist_after,
        "all_fossil_annual_mc_delivery_before": mc_tx_before + mc_dist_before,
        "all_fossil_annual_mc_delivery_after": mc_tx_after + mc_dist_after,
        "all_fossil_annual_total_overcharge": delivery_delta - mc_delta + empower_delta,
        "rhp_lambda_dist": lambda_dist,
        "rhp_lambda_tx": lambda_tx,
        "rhp_lambda_empower": lambda_empower,
        "rhp_pct_change_dist": lambda_dist - 1.0,
        "rhp_pct_change_tx": lambda_tx - 1.0,
        "rhp_pct_change_empower": lambda_empower - 1.0,
        "rhp_fair_dist_bill_after": totals["dist_before"] + (mc_dist_after - mc_dist_before),
        "rhp_fair_tx_bill_after": totals["tx_before"] + (mc_tx_after - mc_tx_before),
        "rhp_avg_rate_dist": totals["dist_after"] / kwh_after,
        "rhp_avg_rate_tx": totals["tx_after"] / kwh_after,
        "rhp_avg_rate_empower": totals["empower_after"] / kwh_after,
        "rhp_rate_dist": totals["dist_after"] / kwh_after * lambda_dist,
        "rhp_rate_tx": totals["tx_after"] / kwh_after * lambda_tx,
        "rhp_rate_empower": totals["empower_after"] / kwh_after * lambda_empower,
    }
    for key, name in names.items():
        report[f"all_fossil_annual_{name}_before"] = totals[f"{key}_before"]
        report[f"all_fossil_annual_{name}_after"] = totals[f"{key}_after"]
    return report


def _to_utc(local: pl.Series) -> pl.Series:
    shifted = pl.DataFrame({"timestamp": local}).select((pl.col("timestamp") + pl.duration(hours=5)).alias("timestamp"))
    return shifted["timestamp"]


def _profiles():
    local = _local_hours()
    utc = _to_utc(local)
    hourly_before = pl.DataFrame({"timestamp": utc, "kwh": _KWH_BEFORE})
    hourly_after = pl.DataFrame({"timestamp": utc, "kwh": _KWH_AFTER})
    mc = pl.DataFrame({"timestamp": local, "mc_bulk_tx": _MC_TX, "mc_dist_sub_tx": _MC_DIST})
    annual_before = 8760 * _KWH_BEFORE
    annual_after = 8760 * _KWH_AFTER
    monthly_before = dict.fromkeys(MONTH_ORDER, annual_before / 12)
    monthly_after = dict.fromkeys(MONTH_ORDER, annual_after / 12)
    before = pl.DataFrame({"month_label": MONTH_ORDER, "kwh": list(monthly_before.values())})
    after = pl.DataFrame({"month_label": MONTH_ORDER, "kwh": list(monthly_after.values())})
    return before, after, hourly_before, hourly_after, mc, monthly_before, monthly_after


def _build(path, monthly_before, monthly_after, **kwargs):
    before, after, hourly_before, hourly_after, mc, kwh_before, kwh_after = _load_base(monthly_before, monthly_after)
    return build_representative_overcharge_workbook(
        path,
        monthly_before=before,
        monthly_after=after,
        hourly_before=hourly_before,
        hourly_after=hourly_after,
        mc=mc,
        rate_components=_rates(),
        report_vars=_report_vars(kwh_before, kwh_after),
        source_name=kwargs.pop("source_name", "ResStock"),
        note=kwargs.pop("note", "Weighted-average home."),
        **kwargs,
    )


def _load_base(monthly_before: dict[str, float] | None, monthly_after: dict[str, float] | None):
    before, after, hourly_before, hourly_after, mc, default_before, default_after = _profiles()
    if monthly_before is None:
        return before, after, hourly_before, hourly_after, mc, default_before, default_after
    assert monthly_after is not None
    before = pl.DataFrame({"month_label": MONTH_ORDER, "kwh": [monthly_before[m] for m in MONTH_ORDER]})
    after = pl.DataFrame({"month_label": MONTH_ORDER, "kwh": [monthly_after[m] for m in MONTH_ORDER]})
    return before, after, hourly_before, hourly_after, mc, monthly_before, monthly_after


def test_representative_home_workbook_uses_formulas_after_the_average(tmp_path) -> None:
    path = _build(tmp_path / "resstock.xlsx", None, None, n_buildings=100, weight_sum=500.0)
    wb = load_workbook(path)

    assert wb["monthly"]["B2"].value == pytest.approx(8760 * _KWH_BEFORE / 12)
    assert wb["hourly"]["B2"].value == _KWH_BEFORE
    assert wb["hourly_marginal_cost"]["B2"].value == "=hourly!B2"
    assert wb["hourly_marginal_cost"]["F2"].value == "=B2*D2"
    assert wb["bills"]["D3"].value == "=rates!B2"
    assert wb["bills"]["E3"].value == "=B3*rates!C2"
    assert wb["overcharge"]["D13"].value == "=D5-D11+D6"
    assert wb["schedule_rhp"]["B9"].value == "=-B8"
    assert wb["schedule_rhp"]["B13"].value == "=B12*B7"
    assert wb["testimony"]["B7"].value == "=overcharge!D13"
    assert wb["testimony"]["B8"].value == "=schedule_rhp!B9"
    assert wb["population"]["B4"].value == 100
    assert wb["population"]["B5"].value == 500.0


def test_subclass_workbook_divides_totals_by_customer_count(tmp_path) -> None:
    local = _local_hours()
    months = [MONTH_ORDER[ts.month - 1] for ts in local.to_list()]
    customers_before = {month: 10.0 + index for index, month in enumerate(MONTH_ORDER)}
    customers_after = {month: 20.0 + index for index, month in enumerate(MONTH_ORDER)}
    monthly_before = {month: 100.0 * (index + 1) for index, month in enumerate(MONTH_ORDER)}
    monthly_after = {month: 150.0 * (index + 1) for index, month in enumerate(MONTH_ORDER)}
    subclass = pl.DataFrame(
        {
            "month_label": MONTH_ORDER,
            "customers_before": [customers_before[month] for month in MONTH_ORDER],
            "kwh_total_before": [monthly_before[month] * customers_before[month] for month in MONTH_ORDER],
            "customers_after": [customers_after[month] for month in MONTH_ORDER],
            "kwh_total_after": [monthly_after[month] * customers_after[month] for month in MONTH_ORDER],
        }
    )
    utc = _to_utc(local)
    aggregate = pl.DataFrame(
        {
            "timestamp": utc,
            "month": months,
            "agg_kwh_before": [_KWH_BEFORE * customers_before[month] for month in months],
            "agg_kwh_after": [_KWH_AFTER * customers_after[month] for month in months],
        }
    )
    path = _build(
        tmp_path / "bge.xlsx",
        monthly_before,
        monthly_after,
        subclass_monthly=subclass,
        hourly_aggregate=aggregate,
        source_name="BGE customer data",
    )
    wb = load_workbook(path)

    assert wb["subclass_monthly"]["F2"].value == "=C2/B2"
    assert wb["monthly"]["B2"].value == "=subclass_monthly!F2"
    assert wb["hourly"]["E2"].value == "=VLOOKUP(B2,subclass_monthly!$A$2:$G$13,2,FALSE)"
    assert wb["hourly"]["G2"].value == "=C2/E2"
    assert wb["hourly_marginal_cost"]["B2"].value == "=hourly!G2"


def test_workbook_refuses_a_figure_that_disagrees_with_the_report_variable(tmp_path) -> None:
    before, after, hourly_before, hourly_after, mc, kwh_before, kwh_after = _load_base(None, None)
    report = _report_vars(kwh_before, kwh_after)
    report["all_fossil_annual_total_overcharge"] += 1
    path = tmp_path / "wrong.xlsx"
    with pytest.raises(AssertionError, match="all_fossil_annual_total_overcharge"):
        build_representative_overcharge_workbook(
            path,
            monthly_before=before,
            monthly_after=after,
            hourly_before=hourly_before,
            hourly_after=hourly_after,
            mc=mc,
            rate_components=_rates(),
            report_vars=report,
            source_name="ResStock",
            note="Weighted-average home.",
        )
    assert not path.exists()


def test_bill_decrease_share_is_a_weighted_formula(tmp_path) -> None:
    buildings = pl.DataFrame(
        {
            "bldg_id": [3, 1, 2],
            "heating_type_v2": ["natgas", "delivered_fuels", "natgas"],
            "weight": [1.0, 1.0, 2.0],
            "bill_before": [50.0, 100.0, 100.0],
            "bill_after": [50.0, 90.0, 105.0],
        }
    )
    path = build_bill_decrease_share_workbook(
        tmp_path / "share.xlsx",
        buildings,
        expected_pct_decrease=0.25,
        expected_pct_increase=0.5,
        note="Fossil-fuel homes.",
    )
    wb = load_workbook(path)
    assert [wb["buildings"].cell(row, 1).value for row in range(2, 5)] == [1, 2, 3]
    assert wb["buildings"]["F2"].value == "=E2-D2"
    assert wb["share"]["B4"].value == '=SUMIF(buildings!F2:F4,"<0",buildings!C2:C4)'
    assert wb["share"]["B8"].value == "=B4/B7"


def test_bill_decrease_share_refuses_a_different_percentage(tmp_path) -> None:
    buildings = pl.DataFrame(
        {
            "bldg_id": [1],
            "heating_type_v2": ["natgas"],
            "weight": [1.0],
            "bill_before": [10.0],
            "bill_after": [9.0],
        }
    )
    path = tmp_path / "share.xlsx"
    with pytest.raises(AssertionError, match="pct_all_fossil_hp_bill_decrease_rhp"):
        build_bill_decrease_share_workbook(
            path,
            buildings,
            expected_pct_decrease=0.5,
            expected_pct_increase=0.0,
            note="Fossil-fuel homes.",
        )
    assert not path.exists()


def test_upload_xlsx_trashes_the_previous_file(monkeypatch, tmp_path) -> None:
    calls: list[tuple[str, dict]] = []

    class _Result:
        def __init__(self, payload: dict) -> None:
            self.payload = payload

        def execute(self) -> dict:
            return self.payload

    class _Files:
        def list(self, **kwargs):
            calls.append(("list", kwargs))
            return _Result({"files": [{"id": "old-id", "name": "book.xlsx"}]})

        def update(self, **kwargs):
            calls.append(("update", kwargs))
            return _Result({})

        def create(self, **kwargs):
            calls.append(("create", kwargs))
            return _Result({"id": "new-id", "webViewLink": "https://drive.google.com/file/d/new-id/view"})

    class _Drive:
        def files(self) -> _Files:
            return _Files()

    monkeypatch.setattr("lib.data.gsheets.get_user_credentials", lambda: object())
    import googleapiclient.discovery as discovery

    monkeypatch.setattr(discovery, "build", lambda *args, **kwargs: _Drive())

    workbook = Workbook()
    path = tmp_path / "book.xlsx"
    workbook.save(path)

    from lib.data.gsheets import upload_xlsx

    link = upload_xlsx(path, "folder-id")

    assert link == "https://drive.google.com/file/d/new-id/view"
    assert calls[1][0] == "update"
    assert calls[1][1]["fileId"] == "old-id"
    assert calls[1][1]["body"] == {"trashed": True}
    assert calls[2][1]["body"] == {"name": "book.xlsx", "parents": ["folder-id"]}
