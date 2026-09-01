"""Unit tests for lib.rates_analysis.cos_funcs."""

from __future__ import annotations

import polars as pl
import pytest

from lib.rates_analysis.cos_funcs import bat_component_delta_with_gap, bat_component_summary_by_heating_type


def _delta_frame() -> pl.DataFrame:
    """Two equally weighted buildings: one natgas, one oil."""
    return pl.DataFrame(
        {
            "bldg_id": [1, 2],
            "weight": [2.0, 2.0],
            "has_hp": [False, False],
            "heating_type_v2": ["natgas", "delivered_fuels"],
            "annual_bill_delivery_before": [100.0, 200.0],
            "annual_bill_delivery_after": [150.0, 220.0],
            "delta_annual_bill_delivery": [50.0, 20.0],
            "economic_burden_delivery_before": [80.0, 180.0],
            "economic_burden_delivery_after": [110.0, 190.0],
            "delta_economic_burden_delivery": [30.0, 10.0],
        }
    )


def test_bat_component_delta_with_gap_filters_joins_kwh_and_adds_columns(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def _fake_delta(
        state: str,
        batch: str,
        segment_before: str,
        segment_after: str,
        *,
        components: list[str] | None = None,
        utility: str | None = None,
    ) -> pl.DataFrame:
        captured["state"] = state
        captured["batch"] = batch
        captured["segment_before"] = segment_before
        captured["segment_after"] = segment_after
        captured["components"] = components
        captured["utility"] = utility
        return _delta_frame()

    def _fake_load_kwh(state: str, utility: str, batch: str, segment: str) -> pl.LazyFrame:
        captured[f"kwh_call_{segment}"] = (state, utility, batch)
        if segment == "default_precalc":
            return pl.DataFrame({"bldg_id": [1, 2], "annual_kwh_grid": [500.0, 600.0]}).lazy()
        return pl.DataFrame({"bldg_id": [1, 2], "annual_kwh_grid": [800.0, 1000.0]}).lazy()

    monkeypatch.setattr("lib.rates_analysis.rate_case_funcs.bat_component_delta", _fake_delta)
    monkeypatch.setattr("lib.rates_analysis.rate_case_funcs.load_billing_kwh_annual", _fake_load_kwh)

    result = bat_component_delta_with_gap(
        "MD",
        "bge",
        "md_test",
        "default_precalc",
        "default_calibrated",
        heating_type="natgas",
    )
    assert captured["state"] == "MD"
    assert captured["utility"] == "bge"
    assert captured["components"] == ["annual_bill_delivery", "economic_burden_delivery"]
    assert result.height == 1
    assert result["heating_type_v2"][0] == "natgas"
    assert "delta_gap" in result.columns
    assert result["delta_gap"][0] == pytest.approx(20.0)  # 50 - 30
    # bldg 1: kwh 500 -> 800
    assert result["annual_kwh_grid_before"][0] == pytest.approx(500.0)
    assert result["annual_kwh_grid_after"][0] == pytest.approx(800.0)
    assert result["delta_annual_kwh_grid"][0] == pytest.approx(300.0)


def _delta_frame_with_kwh_by_group() -> pl.DataFrame:
    """Two natgas buildings (kWh rises after HP) and one resistance-heat building (kWh falls).

    Exercises the "sign flip" case: switching *off* electric resistance heat to a heat
    pump typically *reduces* grid consumption (a much more efficient appliance replacing
    a much less efficient one), the opposite of every combustion heating type.
    """
    return pl.DataFrame(
        {
            "bldg_id": [1, 2, 3],
            "weight": [2.0, 2.0, 2.0],
            "has_hp": [False, False, False],
            "heating_type_v2": ["natgas", "natgas", "electrical_resistance"],
            "annual_bill_delivery_before": [100.0, 200.0, 300.0],
            "delta_annual_bill_delivery": [50.0, 20.0, -50.0],
            "economic_burden_delivery_before": [80.0, 180.0, 250.0],
            "delta_economic_burden_delivery": [30.0, 10.0, -50.0],
            "annual_kwh_grid_before": [500.0, 600.0, 2000.0],
            "delta_annual_kwh_grid": [300.0, 400.0, -500.0],
        }
    )


def test_bat_component_summary_by_heating_type_weighted_sum_ratio() -> None:
    tbl = bat_component_summary_by_heating_type(_delta_frame_with_kwh_by_group())

    assert tbl["heating_type"].to_list() == ["Natural gas", "Electric resistance", "All non-HP"]

    natgas = tbl.filter(pl.col("heating_type") == "Natural gas")
    assert natgas["n_weighted"][0] == pytest.approx(4.0)
    assert natgas["avg_kwh_before"][0] == pytest.approx(550.0)
    assert natgas["avg_kwh_delta"][0] == pytest.approx(350.0)
    assert natgas["revenue_avg_before"][0] == pytest.approx(150.0)
    assert natgas["revenue_avg_delta"][0] == pytest.approx(35.0)
    assert natgas["revenue_pct_change"][0] == pytest.approx(140.0 / 600.0)
    assert natgas["revenue_dollars_per_incremental_kwh"][0] == pytest.approx(140.0 / 1400.0)
    assert natgas["mc_avg_before"][0] == pytest.approx(130.0)
    assert natgas["mc_avg_delta"][0] == pytest.approx(20.0)
    assert natgas["mc_pct_change"][0] == pytest.approx(80.0 / 520.0)
    assert natgas["mc_dollars_per_incremental_kwh"][0] == pytest.approx(80.0 / 1400.0)

    resistance = tbl.filter(pl.col("heating_type") == "Electric resistance")
    # Sign flip: kWh delta is negative (grid draw falls), but $/incremental-kWh is still
    # positive because both the revenue and marginal-cost deltas are also negative --
    # dollars fall right alongside kWh for this group.
    assert resistance["avg_kwh_delta"][0] == pytest.approx(-500.0)
    assert resistance["revenue_dollars_per_incremental_kwh"][0] == pytest.approx(0.1)
    assert resistance["mc_dollars_per_incremental_kwh"][0] == pytest.approx(0.1)

    total = tbl.filter(pl.col("heating_type") == "All non-HP")
    assert total["n_weighted"][0] == pytest.approx(6.0)
    assert total["avg_kwh_delta"][0] == pytest.approx(400.0 / 6.0)
    assert total["revenue_dollars_per_incremental_kwh"][0] == pytest.approx(40.0 / 400.0)
    # Sign flip at the aggregate level: mixing the resistance-heat building's negative
    # deltas into the population total flips the aggregate $/incremental-kWh negative,
    # even though every individual group's ratio was positive -- exactly the kind of
    # aggregation pitfall the by-heating-type breakdown exists to surface.
    assert total["mc_dollars_per_incremental_kwh"][0] == pytest.approx(-20.0 / 400.0)


def test_bat_component_summary_by_heating_type_rejects_has_hp_rows() -> None:
    """The "All non-HP" total row is only accurate if has_hp buildings were already
    excluded upstream (bat_component_delta(exclude_has_hp=True)) -- this function
    can't re-derive that itself, so it must raise rather than silently mislabel the
    total when a caller passes it a frame that still has has_hp=True buildings."""
    bat_delta = _delta_frame_with_kwh_by_group().with_columns(pl.Series("has_hp", [False, True, False]))

    with pytest.raises(ValueError, match="has_hp"):
        bat_component_summary_by_heating_type(bat_delta)
