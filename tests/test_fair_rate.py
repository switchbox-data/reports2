"""Unit tests for lib.rates_analysis.fair_rate."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from lib.rates_analysis.fair_rate import (
    FairFlatRate,
    FairSeasonalRate,
    _proportional_decomposition,
    derive_fair_flat_rate,
    derive_fair_seasonal_rate,
    write_custom_rate_yaml,
)

# ---------------------------------------------------------------------------
# Toy-example values (from the Exhibit CLP-RATES-6 spreadsheet)
# ---------------------------------------------------------------------------
TOY_KWH_BEFORE_SUMMER = 4_000.0
TOY_KWH_BEFORE_WINTER = 3_000.0
TOY_KWH_AFTER_SUMMER = 5_000.0
TOY_KWH_AFTER_WINTER = 8_000.0
TOY_R_BASE = 0.16
TOY_DELTA_MC = 0.0  # toy example has no MC

# Rate 1 proposed decomposition (CT Eversource)
CT_BASE_DIST = 0.12196
CT_BASE_TX = 0.05050
CT_OTHER_RIDERS = -0.00911
CT_BASE_DELIVERY = CT_BASE_DIST + CT_BASE_TX + CT_OTHER_RIDERS  # 0.16335


# ---------------------------------------------------------------------------
# _proportional_decomposition
# ---------------------------------------------------------------------------


class TestProportionalDecomposition:
    def test_base_rate_returns_original(self) -> None:
        """If delivery_total equals the base rate, decomposition returns base components."""
        dist, tx = _proportional_decomposition(
            CT_BASE_DELIVERY,
            CT_BASE_DIST,
            CT_BASE_TX,
            CT_OTHER_RIDERS,
        )
        assert dist + tx + CT_OTHER_RIDERS == pytest.approx(CT_BASE_DELIVERY)
        assert dist == pytest.approx(CT_BASE_DIST, abs=1e-10)
        assert tx == pytest.approx(CT_BASE_TX, abs=1e-10)

    def test_sum_equals_delivery_total(self) -> None:
        """dist + tx + other_riders must always equal delivery_total."""
        delivery_total = 0.10
        dist, tx = _proportional_decomposition(
            delivery_total,
            CT_BASE_DIST,
            CT_BASE_TX,
            CT_OTHER_RIDERS,
        )
        assert dist + tx + CT_OTHER_RIDERS == pytest.approx(delivery_total)

    def test_proportions_preserved(self) -> None:
        """The ratio dist/tx in the output matches the base ratio."""
        delivery_total = 0.08
        dist, tx = _proportional_decomposition(
            delivery_total,
            CT_BASE_DIST,
            CT_BASE_TX,
            CT_OTHER_RIDERS,
        )
        base_ratio = CT_BASE_DIST / CT_BASE_TX
        assert dist / tx == pytest.approx(base_ratio)


# ---------------------------------------------------------------------------
# derive_fair_flat_rate
# ---------------------------------------------------------------------------


class TestDeriveFairFlatRate:
    def test_toy_example_no_mc(self) -> None:
        """Toy spreadsheet: r_new * kWh_after = r_base * kWh_before (delta_MC = 0)."""
        kwh_before = TOY_KWH_BEFORE_SUMMER + TOY_KWH_BEFORE_WINTER  # 7000
        kwh_after = TOY_KWH_AFTER_SUMMER + TOY_KWH_AFTER_WINTER  # 13000

        result = derive_fair_flat_rate(
            avg_delta_mc=TOY_DELTA_MC,
            avg_kwh_before=kwh_before,
            avg_kwh_after=kwh_after,
            base_delivery_rate=TOY_R_BASE,
            base_distribution=0.10,
            base_transmission=0.06,
            other_riders=0.0,
        )
        expected_r = TOY_R_BASE * kwh_before / kwh_after  # 1120/13000
        assert result.delivery_total == pytest.approx(expected_r)
        assert result.delivery_total * kwh_after == pytest.approx(
            TOY_R_BASE * kwh_before,
        )

    def test_formula_constraint(self) -> None:
        """r_new * avg(kWh_after) = r_base * avg(kWh_before) + avg(delta_MC)."""
        mc = 150.0
        kwh_before = 8_000.0
        kwh_after = 12_000.0

        result = derive_fair_flat_rate(
            avg_delta_mc=mc,
            avg_kwh_before=kwh_before,
            avg_kwh_after=kwh_after,
            base_delivery_rate=CT_BASE_DELIVERY,
            base_distribution=CT_BASE_DIST,
            base_transmission=CT_BASE_TX,
            other_riders=CT_OTHER_RIDERS,
        )
        lhs = result.delivery_total * kwh_after
        rhs = CT_BASE_DELIVERY * kwh_before + mc
        assert lhs == pytest.approx(rhs)

    def test_decomposition_sums_to_total(self) -> None:
        """distribution + transmission + other_riders == delivery_total."""
        result = derive_fair_flat_rate(
            avg_delta_mc=200.0,
            avg_kwh_before=7_000.0,
            avg_kwh_after=13_000.0,
            base_delivery_rate=CT_BASE_DELIVERY,
            base_distribution=CT_BASE_DIST,
            base_transmission=CT_BASE_TX,
            other_riders=CT_OTHER_RIDERS,
        )
        assert result.distribution + result.transmission + result.other_riders == pytest.approx(result.delivery_total)

    def test_other_riders_unchanged(self) -> None:
        """other_riders passes through unchanged."""
        result = derive_fair_flat_rate(
            avg_delta_mc=100.0,
            avg_kwh_before=7_000.0,
            avg_kwh_after=13_000.0,
            base_delivery_rate=CT_BASE_DELIVERY,
            base_distribution=CT_BASE_DIST,
            base_transmission=CT_BASE_TX,
            other_riders=CT_OTHER_RIDERS,
        )
        assert result.other_riders == CT_OTHER_RIDERS

    def test_zero_kwh_after_raises(self) -> None:
        with pytest.raises(ValueError, match="avg_kwh_after must be non-zero"):
            derive_fair_flat_rate(
                avg_delta_mc=100.0,
                avg_kwh_before=7_000.0,
                avg_kwh_after=0.0,
                base_delivery_rate=CT_BASE_DELIVERY,
                base_distribution=CT_BASE_DIST,
                base_transmission=CT_BASE_TX,
                other_riders=CT_OTHER_RIDERS,
            )


# ---------------------------------------------------------------------------
# derive_fair_seasonal_rate
# ---------------------------------------------------------------------------


class TestDeriveFairSeasonalRate:
    def test_toy_example_no_mc(self) -> None:
        """Toy spreadsheet: seasonal with ΔMC = 0, summer unchanged at r_base."""
        kwh_before = TOY_KWH_BEFORE_SUMMER + TOY_KWH_BEFORE_WINTER  # 7000

        result = derive_fair_seasonal_rate(
            avg_delta_mc_annual=TOY_DELTA_MC,
            avg_kwh_before_annual=kwh_before,
            avg_kwh_after_winter=TOY_KWH_AFTER_WINTER,
            avg_kwh_after_summer=TOY_KWH_AFTER_SUMMER,
            base_delivery_rate=TOY_R_BASE,
            base_distribution=0.10,
            base_transmission=0.06,
            other_riders=0.0,
        )
        # r_win = (0.16 * 7000 + 0 - 0.16 * 5000) / 8000 = 320/8000 = 0.04
        assert result.winter_delivery_total == pytest.approx(0.04)
        assert result.summer_delivery_total == pytest.approx(TOY_R_BASE)

        # Annual constraint: r_win * kWh_after_win + r_base * kWh_after_sum = r_base * kWh_before
        total_after = (
            result.winter_delivery_total * TOY_KWH_AFTER_WINTER + result.summer_delivery_total * TOY_KWH_AFTER_SUMMER
        )
        total_before = TOY_R_BASE * kwh_before
        assert total_after == pytest.approx(total_before)

    def test_annual_constraint_with_mc(self) -> None:
        """r_win * kWh_after_win + r_base * kWh_after_sum = r_base * kWh_before + delta_MC."""
        mc = 250.0
        kwh_before = 8_500.0
        kwh_after_win = 9_000.0
        kwh_after_sum = 5_500.0

        result = derive_fair_seasonal_rate(
            avg_delta_mc_annual=mc,
            avg_kwh_before_annual=kwh_before,
            avg_kwh_after_winter=kwh_after_win,
            avg_kwh_after_summer=kwh_after_sum,
            base_delivery_rate=CT_BASE_DELIVERY,
            base_distribution=CT_BASE_DIST,
            base_transmission=CT_BASE_TX,
            other_riders=CT_OTHER_RIDERS,
        )

        lhs = result.winter_delivery_total * kwh_after_win + result.summer_delivery_total * kwh_after_sum
        rhs = CT_BASE_DELIVERY * kwh_before + mc
        assert lhs == pytest.approx(rhs)

    def test_winter_decomposition_sums(self) -> None:
        result = derive_fair_seasonal_rate(
            avg_delta_mc_annual=200.0,
            avg_kwh_before_annual=7_000.0,
            avg_kwh_after_winter=8_000.0,
            avg_kwh_after_summer=5_000.0,
            base_delivery_rate=CT_BASE_DELIVERY,
            base_distribution=CT_BASE_DIST,
            base_transmission=CT_BASE_TX,
            other_riders=CT_OTHER_RIDERS,
        )
        assert result.winter_distribution + result.winter_transmission + result.other_riders == pytest.approx(
            result.winter_delivery_total
        )

    def test_summer_decomposition_unchanged(self) -> None:
        result = derive_fair_seasonal_rate(
            avg_delta_mc_annual=200.0,
            avg_kwh_before_annual=7_000.0,
            avg_kwh_after_winter=8_000.0,
            avg_kwh_after_summer=5_000.0,
            base_delivery_rate=CT_BASE_DELIVERY,
            base_distribution=CT_BASE_DIST,
            base_transmission=CT_BASE_TX,
            other_riders=CT_OTHER_RIDERS,
        )
        assert result.summer_distribution == pytest.approx(CT_BASE_DIST)
        assert result.summer_transmission == pytest.approx(CT_BASE_TX)
        assert result.summer_distribution + result.summer_transmission + result.other_riders == pytest.approx(
            result.summer_delivery_total
        )

    def test_zero_kwh_after_winter_raises(self) -> None:
        with pytest.raises(ValueError, match="avg_kwh_after_winter must be non-zero"):
            derive_fair_seasonal_rate(
                avg_delta_mc_annual=200.0,
                avg_kwh_before_annual=7_000.0,
                avg_kwh_after_winter=0.0,
                avg_kwh_after_summer=5_000.0,
                base_delivery_rate=CT_BASE_DELIVERY,
                base_distribution=CT_BASE_DIST,
                base_transmission=CT_BASE_TX,
                other_riders=CT_OTHER_RIDERS,
            )


# ---------------------------------------------------------------------------
# write_custom_rate_yaml
# ---------------------------------------------------------------------------


class TestWriteCustomRateYaml:
    def test_flat_yaml_keys(self, tmp_path: Path) -> None:
        rate = FairFlatRate(
            delivery_total=0.10,
            distribution=0.06,
            transmission=0.05,
            other_riders=-0.01,
        )
        out = write_custom_rate_yaml(
            tmp_path / "flat.yaml",
            rate,
            label="test_flat",
            utility="test_util",
            fixed_charge=12.36,
            supply_rate=0.10469,
        )
        doc: dict[str, Any] = yaml.safe_load(out.read_text())
        assert "delivery" in doc
        delivery = doc["delivery"]
        assert set(delivery.keys()) == {"distribution", "transmission", "other_riders"}
        assert delivery["distribution"] + delivery["transmission"] + delivery["other_riders"] == pytest.approx(
            rate.delivery_total,
            abs=1e-4,
        )

    def test_seasonal_yaml_keys(self, tmp_path: Path) -> None:
        rate = FairSeasonalRate(
            winter_delivery_total=0.04,
            winter_distribution=0.02,
            winter_transmission=0.03,
            summer_delivery_total=0.16,
            summer_distribution=0.10,
            summer_transmission=0.06,
            other_riders=-0.01,
        )
        out = write_custom_rate_yaml(
            tmp_path / "seasonal.yaml",
            rate,
            label="test_seasonal",
            utility="test_util",
            fixed_charge=12.36,
            supply_rate=0.10469,
            winter_months=[11, 12, 1, 2, 3],
        )
        doc: dict[str, Any] = yaml.safe_load(out.read_text())
        assert "seasons" in doc
        for season in ("winter", "summer"):
            delivery = doc["seasons"][season]["delivery"]
            assert set(delivery.keys()) == {"distribution", "transmission", "other_riders"}

    def test_seasonal_without_winter_months_raises(self, tmp_path: Path) -> None:
        rate = FairSeasonalRate(
            winter_delivery_total=0.04,
            winter_distribution=0.02,
            winter_transmission=0.03,
            summer_delivery_total=0.16,
            summer_distribution=0.10,
            summer_transmission=0.06,
            other_riders=-0.01,
        )
        with pytest.raises(ValueError, match="winter_months is required"):
            write_custom_rate_yaml(
                tmp_path / "seasonal.yaml",
                rate,
                label="test",
                utility="test",
                fixed_charge=12.36,
                supply_rate=0.10,
            )

    def test_provenance_header(self, tmp_path: Path) -> None:
        rate = FairFlatRate(
            delivery_total=0.10,
            distribution=0.06,
            transmission=0.05,
            other_riders=-0.01,
        )
        out = write_custom_rate_yaml(
            tmp_path / "flat.yaml",
            rate,
            label="test",
            utility="test",
            fixed_charge=12.36,
            supply_rate=0.10,
            provenance={"batch": "ct_20261001_a", "population": "all_fossil"},
        )
        text = out.read_text()
        assert "# batch: ct_20261001_a" in text
        assert "# population: all_fossil" in text
