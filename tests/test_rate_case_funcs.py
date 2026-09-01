"""Unit tests for lib.rates_analysis.rate_case_funcs (no-S3 helpers)."""

from __future__ import annotations

import polars as pl
import pytest

from lib.rates_analysis.rate_case_funcs import MONTH_ORDER, tariff_month_rate_table


def _flat_rates(rate: float) -> dict:
    """A single-period (flat) tariff's extract_tariff_rates()-shaped dict."""
    return {
        "fixed_charge": 10.0,
        "period_rates": {0: rate},
        "month_to_period": dict.fromkeys(MONTH_ORDER, 0),
    }


def _seasonal_rates(summer_rate: float, winter_rate: float) -> dict:
    """A two-period seasonal tariff: period 0 = Jun-Sep, period 1 = the rest."""
    summer_months = {"Jun", "Jul", "Aug", "Sep"}
    return {
        "fixed_charge": 10.0,
        "period_rates": {0: summer_rate, 1: winter_rate},
        "month_to_period": {m: (0 if m in summer_months else 1) for m in MONTH_ORDER},
    }


def test_tariff_month_rate_table_single_tariff() -> None:
    tbl = tariff_month_rate_table({"Flat rate (¢/kWh)": _flat_rates(0.10)})
    assert tbl["month"].to_list() == MONTH_ORDER
    # rate is in $/kWh internally, table reports cents
    assert tbl["Flat rate (¢/kWh)"].to_list() == pytest.approx([10.0] * 12)


def test_tariff_month_rate_table_joins_multiple_tariffs_on_month() -> None:
    tbl = tariff_month_rate_table(
        {
            "Flat rate (¢/kWh)": _flat_rates(0.10),
            "Seasonal rate (¢/kWh)": _seasonal_rates(0.12, 0.08),
        }
    )
    assert tbl.columns == ["month", "Flat rate (¢/kWh)", "Seasonal rate (¢/kWh)"]
    assert tbl.height == 12
    assert tbl["month"].to_list() == MONTH_ORDER

    jun_row = tbl.filter(pl.col("month") == "Jun")
    assert jun_row["Flat rate (¢/kWh)"][0] == pytest.approx(10.0)
    assert jun_row["Seasonal rate (¢/kWh)"][0] == pytest.approx(12.0)

    jan_row = tbl.filter(pl.col("month") == "Jan")
    assert jan_row["Seasonal rate (¢/kWh)"][0] == pytest.approx(8.0)
