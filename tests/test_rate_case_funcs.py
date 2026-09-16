"""Unit tests for lib.rates_analysis.rate_case_funcs (no-S3 helpers)."""

from __future__ import annotations

import math
from typing import cast

import polars as pl
import pytest

from lib.rates_analysis import rate_case_funcs
from lib.rates_analysis.rate_case_funcs import (
    MONTH_ORDER,
    _annual_bill_component_stack_data,
    _normalize_bill_months,
    bill_period_phrase,
    load_master_bat_for_utility,
    plot_annual_bill_component_stacked,
    quadrant_pcts,
    segment_upgrade,
    tariff_month_rate_table,
    weighted_range_pcts,
)

QUADRANTS = [
    ("savings > $1k", -math.inf, -1000.0),
    ("savings $0-1k", -1000.0, 0.0),
    ("losses $0-1k", 0.0, 1000.0),
    ("losses > $1k", 1000.0, math.inf),
]


def test_load_master_bat_for_utility_filters_and_selects_columns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pl.DataFrame(
        {
            "bldg_id": [1, 2, 3],
            "sb.electric_utility": ["bge", "pepco", "bge"],
            "weight": [1.0, 2.0, 3.0],
        }
    ).lazy()
    monkeypatch.setattr(rate_case_funcs, "load_master_bat", lambda *_: source)

    result = cast(
        "pl.DataFrame",
        load_master_bat_for_utility(
            "MD",
            "batch",
            "scenario_precalc",
            "bge",
            columns={"bldg_id", "weight"},
        ).collect(),
    )

    assert result.columns == ["bldg_id", "weight"]
    assert result["bldg_id"].to_list() == [1, 3]


def test_segment_upgrade_returns_the_single_upgrade_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pl.DataFrame({"upgrade": [1, 1, 1]}).lazy()
    monkeypatch.setattr(rate_case_funcs, "load_master_bills", lambda *_: source)

    assert segment_upgrade("MD", "batch", "default_rd_uncalibrated_calibrated") == 1


def test_segment_upgrade_rejects_mixed_upgrade_ids(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pl.DataFrame({"upgrade": [0, 1]}).lazy()
    monkeypatch.setattr(rate_case_funcs, "load_master_bills", lambda *_: source)

    with pytest.raises(ValueError, match="distinct upgrade IDs"):
        segment_upgrade("MD", "batch", "mixed_segment")


def test_load_master_bat_for_utility_rejects_missing_columns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = pl.DataFrame(
        {
            "bldg_id": [1],
            "sb.electric_utility": ["bge"],
        }
    ).lazy()
    monkeypatch.setattr(rate_case_funcs, "load_master_bat", lambda *_: source)

    with pytest.raises(
        ValueError,
        match="scenario_precalc is missing required columns: \\['weight'\\]",
    ):
        load_master_bat_for_utility(
            "MD",
            "batch",
            "scenario_precalc",
            "bge",
            columns={"bldg_id", "weight"},
        )


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


def test_normalize_bill_months_rejects_annual_mix() -> None:
    with pytest.raises(ValueError, match="Cannot combine"):
        _normalize_bill_months(["Annual", "Jan"])
    with pytest.raises(ValueError, match="non-empty"):
        _normalize_bill_months([])
    assert _normalize_bill_months("Jan") == ["Jan"]


def test_bill_period_phrase() -> None:
    assert bill_period_phrase("Annual") == "annual"
    assert bill_period_phrase("Jan") == "Jan"
    assert bill_period_phrase(["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]) == "Oct-Mar"


# ---------------------------------------------------------------------------
# normalize_peak_split_to_monthly
# ---------------------------------------------------------------------------


def test_normalize_peak_split_matches_monthly_totals() -> None:
    """Rescaled segments sum to the monthly billing total, preserving peak share."""
    peak_split = pl.DataFrame(
        {
            "month_label": MONTH_ORDER,
            "kwh_offpeak": [900.0] * 12,
            "kwh_peak": [100.0] * 12,
        }
    )
    # Billing totals differ from the hourly-derived 1000/month
    monthly = pl.DataFrame({"month_label": MONTH_ORDER, "before_kwh": [800.0] * 12})

    out = rate_case_funcs.normalize_peak_split_to_monthly(peak_split, monthly, kwh_col="before_kwh")

    totals = (out["kwh_offpeak"] + out["kwh_peak"]).to_list()
    assert all(t == pytest.approx(800.0) for t in totals)
    # Peak fraction preserved at 10%
    fracs = (out["kwh_peak"] / (out["kwh_offpeak"] + out["kwh_peak"])).to_list()
    assert all(f == pytest.approx(0.10) for f in fracs)


def test_normalize_peak_split_per_month_scaling() -> None:
    """Each month scales independently by its own ratio."""
    peak_split = pl.DataFrame(
        {
            "month_label": MONTH_ORDER,
            "kwh_offpeak": [500.0] * 12,
            "kwh_peak": [500.0] * 12,
        }
    )
    targets = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0]
    monthly = pl.DataFrame({"month_label": MONTH_ORDER, "kwh": targets})

    out = rate_case_funcs.normalize_peak_split_to_monthly(peak_split, monthly)

    for row, target in zip(out.iter_rows(named=True), targets, strict=True):
        assert row["kwh_offpeak"] + row["kwh_peak"] == pytest.approx(target)
        # 50/50 split preserved
        assert row["kwh_peak"] == pytest.approx(target / 2)


def test_normalize_peak_split_zero_hourly_month() -> None:
    """A month with zero hourly load stays zero rather than dividing by zero."""
    peak_split = pl.DataFrame(
        {
            "month_label": MONTH_ORDER,
            "kwh_offpeak": [0.0] + [900.0] * 11,
            "kwh_peak": [0.0] + [100.0] * 11,
        }
    )
    monthly = pl.DataFrame({"month_label": MONTH_ORDER, "kwh": [500.0] * 12})

    out = rate_case_funcs.normalize_peak_split_to_monthly(peak_split, monthly)

    jan = out.row(0, named=True)
    assert jan["kwh_offpeak"] == pytest.approx(0.0)
    assert jan["kwh_peak"] == pytest.approx(0.0)
    feb = out.row(1, named=True)
    assert feb["kwh_offpeak"] + feb["kwh_peak"] == pytest.approx(500.0)


def test_normalize_peak_split_rejects_month_mismatch() -> None:
    peak_split = pl.DataFrame(
        {
            "month_label": MONTH_ORDER,
            "kwh_offpeak": [900.0] * 12,
            "kwh_peak": [100.0] * 12,
        }
    )
    monthly = pl.DataFrame({"month_label": MONTH_ORDER[:6], "kwh": [500.0] * 6})
    with pytest.raises(ValueError, match="month_label mismatch"):
        rate_case_funcs.normalize_peak_split_to_monthly(peak_split, monthly)


# ---------------------------------------------------------------------------
# plot_monthly_load_before_after — peak wedge stacking
# ---------------------------------------------------------------------------


def _make_peak_stacking_data(
    before: list[float],
    after: list[float],
    peak_after: list[float],
) -> pl.DataFrame:
    """Build the internal _m DataFrame that plot_monthly_load_before_after computes.

    Replicates the segment arithmetic without invoking the full plotting
    function (which needs matplotlib/plotnine).
    """
    assert len(before) == len(after) == len(peak_after) == 12
    _m = (
        pl.DataFrame(
            {
                "month_label": MONTH_ORDER,
                "before_kwh": before,
                "after_kwh": after,
                "after_peak": peak_after,
            }
        )
        .with_columns(
            pl.min_horizontal("before_kwh", "after_kwh").alias("base_kwh"),
            (pl.col("before_kwh") - pl.col("after_kwh")).clip(lower_bound=0).alias("savings_kwh"),
            (pl.col("after_kwh") - pl.col("before_kwh")).clip(lower_bound=0).alias("new_hp_kwh"),
        )
        .with_columns(
            pl.min_horizontal("after_peak", "new_hp_kwh").alias("peak_in_new"),
        )
        .with_columns(
            pl.min_horizontal(
                (pl.col("after_peak") - pl.col("peak_in_new")).clip(lower_bound=0),
                pl.col("base_kwh"),
            ).alias("peak_in_base"),
        )
    )
    return _m


def _check_stacking_invariants(m: pl.DataFrame) -> None:
    """Verify the stacking arithmetic is internally consistent."""
    for row in m.iter_rows(named=True):
        base_offpeak = row["base_kwh"] - row["peak_in_base"]
        new_hp_offpeak = row["new_hp_kwh"] - row["peak_in_new"]

        assert base_offpeak >= -1e-9, f"Negative base off-peak in {row['month_label']}"
        assert new_hp_offpeak >= -1e-9, f"Negative new HP off-peak in {row['month_label']}"
        assert row["peak_in_base"] >= -1e-9
        assert row["peak_in_new"] >= -1e-9
        assert row["savings_kwh"] >= -1e-9

        total = base_offpeak + row["peak_in_base"] + row["savings_kwh"] + new_hp_offpeak + row["peak_in_new"]
        expected = max(row["before_kwh"], row["after_kwh"])
        assert total == pytest.approx(expected, abs=1e-9), f"{row['month_label']}: stack total {total} != {expected}"

        total_red = row["peak_in_base"] + row["peak_in_new"]
        assert total_red == pytest.approx(row["after_peak"], abs=1e-9), (
            f"{row['month_label']}: red total {total_red} != after_peak {row['after_peak']}"
        )


def test_peak_stacking_red_within_light_yellow() -> None:
    """When peak kWh < new HP increment, red stays entirely in light yellow."""
    before = [700.0] * 12
    after = [900.0] * 12
    peak = [100.0] * 12

    m = _make_peak_stacking_data(before, after, peak)
    _check_stacking_invariants(m)

    row = m.row(0, named=True)
    assert row["peak_in_new"] == pytest.approx(100.0)
    assert row["peak_in_base"] == pytest.approx(0.0)


def test_peak_stacking_red_overflows_into_dark_yellow() -> None:
    """When peak kWh > new HP increment, red spills from light into dark yellow."""
    before = [700.0] * 12
    after = [900.0] * 12
    peak = [250.0] * 12

    m = _make_peak_stacking_data(before, after, peak)
    _check_stacking_invariants(m)

    row = m.row(0, named=True)
    assert row["new_hp_kwh"] == pytest.approx(200.0)
    assert row["peak_in_new"] == pytest.approx(200.0)
    assert row["peak_in_base"] == pytest.approx(50.0)


def test_peak_stacking_savings_month() -> None:
    """Savings months (after < before): all red carved from dark yellow."""
    before = [800.0] * 12
    after = [700.0] * 12
    peak = [40.0] * 12

    m = _make_peak_stacking_data(before, after, peak)
    _check_stacking_invariants(m)

    row = m.row(0, named=True)
    assert row["savings_kwh"] == pytest.approx(100.0)
    assert row["new_hp_kwh"] == pytest.approx(0.0)
    assert row["peak_in_new"] == pytest.approx(0.0)
    assert row["peak_in_base"] == pytest.approx(40.0)


def test_peak_stacking_mixed_months() -> None:
    """Mixed scenario: some months grow, some shrink, with varying peak sizes."""
    before = [800.0, 700.0, 600.0] + [700.0] * 9
    after = [700.0, 900.0, 900.0] + [700.0] * 9
    peak = [40.0, 150.0, 350.0] + [0.0] * 9

    m = _make_peak_stacking_data(before, after, peak)
    _check_stacking_invariants(m)

    jan = m.row(0, named=True)
    assert jan["savings_kwh"] == pytest.approx(100.0)
    assert jan["peak_in_base"] == pytest.approx(40.0)
    assert jan["peak_in_new"] == pytest.approx(0.0)

    feb = m.row(1, named=True)
    assert feb["new_hp_kwh"] == pytest.approx(200.0)
    assert feb["peak_in_new"] == pytest.approx(150.0)
    assert feb["peak_in_base"] == pytest.approx(0.0)

    mar = m.row(2, named=True)
    assert mar["new_hp_kwh"] == pytest.approx(300.0)
    assert mar["peak_in_new"] == pytest.approx(300.0)
    assert mar["peak_in_base"] == pytest.approx(50.0)
