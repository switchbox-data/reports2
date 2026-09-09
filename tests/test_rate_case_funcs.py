"""Unit tests for lib.rates_analysis.rate_case_funcs (no-S3 helpers)."""

from __future__ import annotations

import math

import polars as pl
import pytest

from lib.rates_analysis.rate_case_funcs import (
    MONTH_ORDER,
    _annual_bill_component_stack_data,
    plot_annual_bill_component_stacked,
    quadrant_pcts,
    tariff_month_rate_table,
    weighted_range_pcts,
)

QUADRANTS = [
    ("savings > $1k", -math.inf, -1000.0),
    ("savings $0-1k", -1000.0, 0.0),
    ("losses $0-1k", 0.0, 1000.0),
    ("losses > $1k", 1000.0, math.inf),
]


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


def _monthly_bill_rows(values: dict[str, float]) -> pl.DataFrame:
    return pl.DataFrame(
        [{"component": component, "month": "Jan", "value": value / 12} for component, value in values.items()]
    )


def test_annual_bill_component_stack_data_totals_match_after() -> None:
    before = _monthly_bill_rows(
        {
            "Customer Charge": 120.0,
            "Distribution": 600.0,
            "Generation": 1400.0,
        }
    )
    after = _monthly_bill_rows(
        {
            "Customer Charge": 120.0,
            "Distribution": 1000.0,
            "Generation": 2400.0,
        }
    )

    stacked = _annual_bill_component_stack_data(before, after)
    totals = stacked.group_by("component").agg(pl.col("value").sum().alias("total"))
    expected = after.group_by("component").agg(pl.col("value").sum().alias("after_total"))
    joined = totals.join(expected.cast({"component": stacked["component"].dtype}), on="component")
    assert joined["total"].to_list() == pytest.approx(joined["after_total"].to_list())


def test_annual_bill_component_stack_data_raises_on_negative_increment() -> None:
    before = _monthly_bill_rows({"Distribution": 600.0})
    after = _monthly_bill_rows({"Distribution": 500.0})

    with pytest.raises(ValueError, match="non-negative"):
        _annual_bill_component_stack_data(before, after)


def test_plot_annual_bill_component_stacked_renders(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("lib.quarto.display_figure", lambda fig: None)

    before = _monthly_bill_rows(
        {
            "Customer Charge": 121.0,
            "Distribution": 598.0,
            "Transmission": 280.0,
            "EmPOWER Maryland": 141.0,
            "Generation": 1467.0,
        }
    )
    after = _monthly_bill_rows(
        {
            "Customer Charge": 121.0,
            "Distribution": 1003.0,
            "Transmission": 469.0,
            "EmPOWER Maryland": 233.0,
            "Generation": 2446.0,
        }
    )

    fig = plot_annual_bill_component_stacked(before, after, title="Test")
    assert fig is not None


def test_weighted_range_pcts_partitions_known_weights() -> None:
    df = pl.DataFrame(
        {
            "bill_change": [-1500.0, -500.0, 500.0, 1500.0],
            "weight": [1.0, 1.0, 2.0, 1.0],
        }
    )
    pct = weighted_range_pcts(df, value_col="bill_change", ranges=QUADRANTS)
    assert list(pct) == [
        "savings > $1k",
        "savings $0-1k",
        "losses $0-1k",
        "losses > $1k",
    ]
    assert pct["savings > $1k"] == pytest.approx(20.0)
    assert pct["savings $0-1k"] == pytest.approx(20.0)
    assert pct["losses $0-1k"] == pytest.approx(40.0)
    assert pct["losses > $1k"] == pytest.approx(20.0)
    assert sum(pct.values()) == pytest.approx(100.0)


def test_weighted_range_pcts_zero_weight() -> None:
    df = pl.DataFrame({"bill_change": [100.0], "weight": [0.0]})
    pct = weighted_range_pcts(
        df,
        value_col="bill_change",
        ranges=[
            ("low", -math.inf, 0.0),
            ("mid", 0.0, 200.0),
            ("high", 200.0, math.inf),
        ],
    )
    assert pct == {"low": 0.0, "mid": 0.0, "high": 0.0}


def test_weighted_range_pcts_rejects_duplicate_labels() -> None:
    df = pl.DataFrame({"bill_change": [1.0], "weight": [1.0]})
    with pytest.raises(ValueError, match="duplicates: \\['same'\\]"):
        weighted_range_pcts(
            df,
            value_col="bill_change",
            ranges=[
                ("same", -math.inf, 0.0),
                ("same", 0.0, 1.0),
                ("high", 1.0, math.inf),
            ],
        )


def test_quadrant_pcts_wrapper_uses_delta_column() -> None:
    df = pl.DataFrame(
        {
            "delta": [-1500.0, -500.0, 500.0, 1500.0],
            "weight": [1.0, 1.0, 2.0, 1.0],
        }
    )
    pct = quadrant_pcts(df)
    assert pct["savings > $1k"] == pytest.approx(20.0)
    assert pct["losses $0-1k"] == pytest.approx(40.0)


def test_weighted_range_pcts_five_bins() -> None:
    df = pl.DataFrame(
        {
            "bill_change": [-2500.0, -1500.0, -500.0, 500.0, 1500.0],
            "weight": [1.0, 1.0, 1.0, 1.0, 1.0],
        }
    )
    pct = weighted_range_pcts(
        df,
        value_col="bill_change",
        ranges=[
            ("save > $2k", -math.inf, -2000.0),
            ("save $1k-2k", -2000.0, -1000.0),
            ("save $0-1k", -1000.0, 0.0),
            ("lose $0-1k", 0.0, 1000.0),
            ("lose > $1k", 1000.0, math.inf),
        ],
    )
    assert list(pct) == [
        "save > $2k",
        "save $1k-2k",
        "save $0-1k",
        "lose $0-1k",
        "lose > $1k",
    ]
    assert all(v == pytest.approx(20.0) for v in pct.values())
