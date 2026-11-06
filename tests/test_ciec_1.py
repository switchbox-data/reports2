"""CIEC-1 charge-increase arithmetic. Does not load ResStock."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


def _load() -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "reports" / "ct_hp_rates" / "ciec_requests" / "ciec_1.py"
    spec = importlib.util.spec_from_file_location("ciec_1_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ciec = _load()


def test_cents_converts_dollars_per_kwh() -> None:
    assert ciec.cents(0.001234) == "0.1234¢"
    assert ciec.cents(0.001234, accuracy=3) == "0.123¢"


def test_five_year_average_matches_makeup_increase() -> None:
    rows = [
        {"year": 2027, "distribution": 100.0, "transmission": 40.0},
        {"year": 2028, "distribution": 200.0, "transmission": 80.0},
        {"year": 2029, "distribution": 300.0, "transmission": 50.0},
        {"year": 2030, "distribution": 400.0, "transmission": 60.0},
        {"year": 2031, "distribution": 500.0, "transmission": 70.0},
    ]
    kwh = 1_000_000.0
    increases = ciec.per_kwh_increases(rows, kwh)
    dist = ciec.makeup_increase(sum(row["distribution"] for row in rows), kwh, 0.11)
    tx = ciec.makeup_increase(sum(row["transmission"] for row in rows), kwh, 0.05)
    assert sum(row["distribution"] for row in increases) / 5 == pytest.approx(dist["increase"])
    assert sum(row["transmission"] for row in increases) / 5 == pytest.approx(tx["increase"])
    assert dist["pct"] == pytest.approx(dist["increase"] / 0.11)
    assert tx["pct"] == pytest.approx(tx["increase"] / 0.05)


def test_charge_increase_table_labels_years_and_rejects_a_mismatch() -> None:
    floor = [{"year": 2027.0, "distribution": 0.001, "transmission": 0.0004}]
    ceiling = [{"year": 2027.0, "distribution": 0.002, "transmission": 0.0008}]
    table = ciec.charge_increase_table(floor, ceiling, accuracy=4)
    assert "| Year | Floor distribution (¢/kWh) |" in table
    assert "| 2027 | 0.1000 | 0.0400 | 0.2000 | 0.0800 |" in table

    floor_avg = [{"label": "Five-year average", "distribution": 0.001, "transmission": 0.0004}]
    ceiling_other = [{"label": "Other", "distribution": 0.002, "transmission": 0.0008}]
    with pytest.raises(ValueError, match="charge-increase labels differ"):
        ciec.charge_increase_table(floor_avg, ceiling_other)


def test_td_increase_table_divides_rounded_revenue_by_kwh() -> None:
    enrolled = [(2026, 10), (2027, 25)]
    table = ciec.td_increase_table(
        enrolled,
        1.2,
        0.34,
        1_000.0,
        td_rate=0.10,
        full_rate=0.20,
    )
    assert "| Year | Distribution (¢/kWh) |" in table
    # round(10 * 1.2) = 12 and round(10 * 0.34) = 3, over 1,000 kWh.
    assert "| Existing | 1.2000 | 0.3000 | 1.5000 | 15.00% | 7.50% |" in table
    # round(25 * 1.2) = 30 and round(25 * 0.34) = 8.
    assert "| 2027 | 3.0000 | 0.8000 | 3.8000 | 38.00% | 19.00% |" in table
    with pytest.raises(ValueError, match="kwh must be positive"):
        ciec.td_increase_table(enrolled, 1.2, 0.34, 0.0, td_rate=0.10, full_rate=0.20)


def test_cohort_revenue_bills_later_enrollees_at_the_second_rate() -> None:
    enrolled = [(2026, 10), (2027, 25)]
    rows = ciec.cohort_revenue_rows(enrolled, 1.2, 0.34, 2.0, 0.5)
    assert rows[0]["existing_customers"] == 10
    assert rows[0]["new_customers"] == 0
    assert rows[0]["distribution"] == 12  # round(10 * 1.2)
    assert rows[0]["transmission"] == 3  # round(10 * 0.34)
    assert rows[1]["new_customers"] == 15
    assert rows[1]["distribution"] == 42  # 12 + round(15 * 2.0)
    assert rows[1]["transmission"] == 11  # 3 + round(15 * 0.5)
    assert rows[1]["total"] == 53
    with pytest.raises(ValueError, match="starting stock"):
        ciec.cohort_revenue_rows([(2026, 10), (2027, 4)], 1.0, 1.0, 1.0, 1.0)


def test_per_kwh_increases_rejects_nonpositive_sales() -> None:
    with pytest.raises(ValueError, match="kwh must be positive"):
        ciec.per_kwh_increases([{"year": 2027, "distribution": 1.0, "transmission": 1.0}], 0.0)
