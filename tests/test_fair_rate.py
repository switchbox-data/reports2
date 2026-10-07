"""Tests for fair-rate derivation functions.

Covers:
- Fair flat rate: r' = avg_mc / avg_kwh identity
- Fair seasonal rate: annual overpayment zeroed by construction
- Edge cases: zero delta_kwh raises
- YAML output round-trip for both flat and seasonal formats
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from lib.rates_analysis.fair_rate import (
    FairFlatRate,
    FairSeasonalRate,
    derive_fair_flat_rate,
    derive_fair_seasonal_rate,
    write_custom_rate_yaml,
)

# ---------------------------------------------------------------------------
# Fair flat rate
# ---------------------------------------------------------------------------


class TestDeriveFairFlatRate:
    def test_basic_identity(self) -> None:
        """r' = avg_mc / avg_kwh, decomposed as distribution + riders."""
        result = derive_fair_flat_rate(
            avg_delta_mc=800.0,
            avg_delta_kwh=10_000.0,
            base_delivery_rate=0.16335,
            riders_total=0.04139,
        )
        assert result.delivery_total == pytest.approx(0.08)
        assert result.distribution == pytest.approx(0.08 - 0.04139)
        assert result.riders == pytest.approx(0.04139)

    def test_decomposition_adds_up(self) -> None:
        """delivery_total == distribution + riders."""
        result = derive_fair_flat_rate(
            avg_delta_mc=1200.0,
            avg_delta_kwh=8000.0,
            base_delivery_rate=0.16335,
            riders_total=0.04139,
        )
        assert result.delivery_total == pytest.approx(result.distribution + result.riders)

    def test_zero_delta_kwh_raises(self) -> None:
        """Cannot derive a rate when there's no incremental kWh."""
        with pytest.raises(ValueError, match="avg_delta_kwh must be non-zero"):
            derive_fair_flat_rate(
                avg_delta_mc=500.0,
                avg_delta_kwh=0.0,
                base_delivery_rate=0.16335,
                riders_total=0.04139,
            )

    def test_negative_rate_when_mc_negative(self) -> None:
        """If avg MC is negative, the derived rate is negative (valid result)."""
        result = derive_fair_flat_rate(
            avg_delta_mc=-200.0,
            avg_delta_kwh=5000.0,
            base_delivery_rate=0.16335,
            riders_total=0.04139,
        )
        assert result.delivery_total < 0.0


# ---------------------------------------------------------------------------
# Fair seasonal rate
# ---------------------------------------------------------------------------


class TestDeriveFairSeasonalRate:
    def test_annual_overpayment_zero(self) -> None:
        """r_win * delta_kwh_winter + r_base * delta_kwh_summer == delta_mc_annual."""
        avg_mc = 900.0
        avg_kwh_winter = 6000.0
        avg_kwh_summer = 2000.0
        base_rate = 0.16335

        result = derive_fair_seasonal_rate(
            avg_delta_mc_annual=avg_mc,
            avg_delta_kwh_winter=avg_kwh_winter,
            avg_delta_kwh_summer=avg_kwh_summer,
            base_delivery_rate=base_rate,
            riders_total=0.04139,
        )

        reconstructed_mc = result.winter_delivery_total * avg_kwh_winter + result.summer_delivery_total * avg_kwh_summer
        assert reconstructed_mc == pytest.approx(avg_mc)

    def test_summer_unchanged(self) -> None:
        """Summer rate is the base delivery rate, unchanged."""
        base_rate = 0.16335
        result = derive_fair_seasonal_rate(
            avg_delta_mc_annual=1000.0,
            avg_delta_kwh_winter=5000.0,
            avg_delta_kwh_summer=3000.0,
            base_delivery_rate=base_rate,
            riders_total=0.04139,
        )
        assert result.summer_delivery_total == pytest.approx(base_rate)
        assert result.summer_distribution == pytest.approx(base_rate - 0.04139)

    def test_decomposition_winter(self) -> None:
        """winter_delivery_total == winter_distribution + riders."""
        result = derive_fair_seasonal_rate(
            avg_delta_mc_annual=1000.0,
            avg_delta_kwh_winter=5000.0,
            avg_delta_kwh_summer=3000.0,
            base_delivery_rate=0.16335,
            riders_total=0.04139,
        )
        assert result.winter_delivery_total == pytest.approx(result.winter_distribution + result.riders)

    def test_zero_winter_kwh_raises(self) -> None:
        """Cannot concentrate correction in winter with no incremental winter kWh."""
        with pytest.raises(ValueError, match="avg_delta_kwh_winter must be non-zero"):
            derive_fair_seasonal_rate(
                avg_delta_mc_annual=1000.0,
                avg_delta_kwh_winter=0.0,
                avg_delta_kwh_summer=5000.0,
                base_delivery_rate=0.16335,
                riders_total=0.04139,
            )

    def test_hand_verified_example(self) -> None:
        """Hand-verified: mc=1000, kwh_w=8000, kwh_s=2000, base=0.10."""
        # r_win = (1000 - 0.10 * 2000) / 8000 = (1000 - 200) / 8000 = 0.10
        result = derive_fair_seasonal_rate(
            avg_delta_mc_annual=1000.0,
            avg_delta_kwh_winter=8000.0,
            avg_delta_kwh_summer=2000.0,
            base_delivery_rate=0.10,
            riders_total=0.02,
        )
        assert result.winter_delivery_total == pytest.approx(0.10)
        assert result.winter_distribution == pytest.approx(0.08)

    def test_negative_winter_rate_possible(self) -> None:
        """If summer already over-recovers, winter rate goes negative."""
        # mc=100, base=0.20, kwh_s=2000, kwh_w=1000
        # r_win = (100 - 0.20*2000) / 1000 = (100-400)/1000 = -0.30
        result = derive_fair_seasonal_rate(
            avg_delta_mc_annual=100.0,
            avg_delta_kwh_winter=1000.0,
            avg_delta_kwh_summer=2000.0,
            base_delivery_rate=0.20,
            riders_total=0.04,
        )
        assert result.winter_delivery_total == pytest.approx(-0.30)


# ---------------------------------------------------------------------------
# YAML output
# ---------------------------------------------------------------------------


class TestWriteCustomRateYaml:
    def test_flat_yaml_structure(self, tmp_path: Path) -> None:
        """Flat rate YAML matches create_custom_flat_tariff.py input format."""
        rate = FairFlatRate(delivery_total=0.10, distribution=0.06, riders=0.04)
        out = tmp_path / "test_flat.yaml"

        write_custom_rate_yaml(
            out,
            rate,
            label="icos_fair_flat",
            utility="ct_eversource",
            fixed_charge=12.36,
            supply_rate=0.11190,
        )

        doc = yaml.safe_load(out.read_text())
        assert doc["label"] == "icos_fair_flat"
        assert doc["utility"] == "ct_eversource"
        assert doc["fixed_charge"] == 12.36
        assert doc["delivery"]["distribution"] == pytest.approx(0.06)
        assert doc["delivery"]["riders"] == pytest.approx(0.04)
        assert doc["supply_rate"] == pytest.approx(0.11190)

    def test_seasonal_yaml_structure(self, tmp_path: Path) -> None:
        """Seasonal rate YAML matches create_custom_seasonal_tariff.py input format."""
        rate = FairSeasonalRate(
            winter_delivery_total=0.08,
            winter_distribution=0.04,
            summer_delivery_total=0.16,
            summer_distribution=0.12,
            riders=0.04,
        )
        out = tmp_path / "test_seasonal.yaml"

        write_custom_rate_yaml(
            out,
            rate,
            label="icos_fair_seasonal",
            utility="ct_eversource",
            fixed_charge=12.36,
            supply_rate=0.11190,
            winter_months=[11, 12, 1, 2, 3],
        )

        doc = yaml.safe_load(out.read_text())
        assert doc["label"] == "icos_fair_seasonal"
        assert doc["fixed_charge"] == 12.36
        assert "seasons" in doc
        assert doc["seasons"]["winter"]["months"] == [12, 1, 2, 3, 11]
        assert doc["seasons"]["winter"]["delivery"]["distribution"] == pytest.approx(0.04)
        assert doc["seasons"]["summer"]["delivery"]["distribution"] == pytest.approx(0.12)
        summer_months = doc["seasons"]["summer"]["months"]
        assert sorted(summer_months) == [4, 5, 6, 7, 8, 9, 10]

    def test_seasonal_requires_winter_months(self, tmp_path: Path) -> None:
        """Seasonal rate YAML raises if winter_months not provided."""
        rate = FairSeasonalRate(
            winter_delivery_total=0.08,
            winter_distribution=0.04,
            summer_delivery_total=0.16,
            summer_distribution=0.12,
            riders=0.04,
        )
        with pytest.raises(ValueError, match="winter_months is required"):
            write_custom_rate_yaml(
                tmp_path / "test.yaml",
                rate,
                label="test",
                utility="test",
                fixed_charge=10.0,
                supply_rate=0.10,
            )

    def test_provenance_header(self, tmp_path: Path) -> None:
        """Provenance metadata appears as comments in the YAML."""
        rate = FairFlatRate(delivery_total=0.10, distribution=0.06, riders=0.04)
        out = tmp_path / "test_prov.yaml"

        write_custom_rate_yaml(
            out,
            rate,
            label="test",
            utility="test",
            fixed_charge=10.0,
            supply_rate=0.10,
            provenance={"batch": "ct_20261001_a", "population": "all_fossil"},
        )

        text = out.read_text()
        assert "# batch: ct_20261001_a" in text
        assert "# population: all_fossil" in text
        doc = yaml.safe_load(text)
        assert doc["label"] == "test"
