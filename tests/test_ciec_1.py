"""Tests for the CIEC-1 helpers that are not already covered in lib."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


def _load_ciec_1() -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "reports" / "ct_hp_rates" / "ciec_requests" / "ciec_1.py"
    spec = importlib.util.spec_from_file_location("ciec_1_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ciec_1 = _load_ciec_1()
combine_revenue = ciec_1.combine_revenue
group_revenue = ciec_1.group_revenue
makeup_increase = ciec_1.makeup_increase
new_enrollment_path = ciec_1.new_enrollment_path
sum_monthly_rates = ciec_1.sum_monthly_rates
with_winter_rates = ciec_1.with_winter_rates


def test_sum_monthly_rates_adds_each_month() -> None:
    first = {"monthly_rates": {"2025-01": 0.25, "2025-02": 0.50}}
    second = {"monthly_rates": {"2025-01": 0.25, "2025-02": -0.25}}
    assert sum_monthly_rates(first, second) == {"2025-01": 0.50, "2025-02": 0.25}


def test_with_winter_rates_replaces_only_winter_delivery() -> None:
    rate1 = {
        "Distribution": {"charge_unit": "$/kWh", "monthly_rates": {"2025-01": 0.11, "2025-07": 0.11}},
        "Transmission": {"charge_unit": "$/kWh", "monthly_rates": {"2025-01": 0.05, "2025-07": 0.05}},
        "Generation": {"charge_unit": "$/kWh", "monthly_rates": {"2025-01": 0.10, "2025-07": 0.09}},
    }
    rate_hp = with_winter_rates(rate1, 0.03, 0.01, ["2025-01"])
    assert rate_hp["Distribution"]["monthly_rates"] == {"2025-01": 0.03, "2025-07": 0.11}
    assert rate_hp["Transmission"]["monthly_rates"] == {"2025-01": 0.01, "2025-07": 0.05}
    assert rate_hp["Generation"]["monthly_rates"] == rate1["Generation"]["monthly_rates"]


def test_new_enrollment_accumulates_and_adds_to_existing() -> None:
    existing = group_revenue(10, dec_dist=2.0, dec_tx=1.0)
    path = new_enrollment_path([2, 2], [2027, 2028], dec_dist=2.0, dec_tx=1.0)
    combined = combine_revenue(existing, path)
    assert existing["distribution"] == 20
    assert existing["distribution_5"] == 100
    assert [row["customers"] for row in path] == [2, 4]
    assert [row["distribution"] for row in combined] == [24, 28]


def test_makeup_increase_is_the_annual_adder_over_delivery_only() -> None:
    # Five years of $500 on 1,000 kWh is $0.10/kWh per year. Delivery rate is $0.20/kWh.
    result = makeup_increase(500, nonhp_kwh=1_000, delivery_rate=0.20)
    assert result["increase"] == 0.1
    assert result["pct"] == 0.5
