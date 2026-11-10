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


def test_autoenrolled_tables_use_only_the_existing_decrease() -> None:
    assert ciec.enrollment_range(10, 25) == [
        ("Floor", 10),
        ("20%", 13),
        ("40%", 16),
        ("60%", 19),
        ("80%", 22),
        ("Ceiling", 25),
    ]
    with pytest.raises(ValueError, match="below floor"):
        ciec.enrollment_range(25, 10)

    reduction = ciec.autoenrolled_reduction_table(10, 25, 1.2, 0.34)
    assert "| Share of the range | Customers | Distribution | Transmission | T&D |" in reduction
    assert "| Floor | 10 | \\$12 | \\$3 | \\$15 |" in reduction
    assert "| 20% | 13 | \\$16 | \\$4 | \\$20 |" in reduction
    assert "| 40% | 16 | \\$19 | \\$5 | \\$24 |" in reduction
    assert "| 60% | 19 | \\$23 | \\$6 | \\$29 |" in reduction
    assert "| 80% | 22 | \\$26 | \\$7 | \\$33 |" in reduction
    assert "| Ceiling | 25 | \\$30 | \\$8 | \\$38 |" in reduction

    increase = ciec.autoenrolled_increase_table(10, 25, 1.2, 0.34, 1_000.0, td_rate=0.10, full_rate=0.20)
    assert "| Share of the range | Distribution (¢/kWh) |" in increase
    assert "| Floor | 1.2000 | 0.3000 | 1.5000 | 15.00% | 7.50% |" in increase
    assert "| 20% | 1.6000 | 0.4000 | 2.0000 | 20.00% | 10.00% |" in increase
    assert "| 40% | 1.9000 | 0.5000 | 2.4000 | 24.00% | 12.00% |" in increase
    assert "| 60% | 2.3000 | 0.6000 | 2.9000 | 29.00% | 14.50% |" in increase
    assert "| 80% | 2.6000 | 0.7000 | 3.3000 | 33.00% | 16.50% |" in increase
    assert "| Ceiling | 3.0000 | 0.8000 | 3.8000 | 38.00% | 19.00% |" in increase
    with pytest.raises(ValueError, match="kwh must be positive"):
        ciec.autoenrolled_increase_table(10, 25, 1.2, 0.34, 0.0, td_rate=0.10, full_rate=0.20)


def test_per_kwh_increases_rejects_nonpositive_sales() -> None:
    with pytest.raises(ValueError, match="kwh must be positive"):
        ciec.per_kwh_increases([{"year": 2027, "distribution": 1.0, "transmission": 1.0}], 0.0)


def test_annual_bill_increase_stats_weights_kwh_times_the_charge() -> None:
    import polars as pl

    buildings = pl.DataFrame({"weight": [1.0, 1.0], "annual_kwh": [1000.0, 3000.0]})
    stats = ciec.annual_bill_increase_stats(buildings, 0.004)
    assert stats["mean"] == pytest.approx(8)
    assert stats["median"] == pytest.approx(4)
    assert stats["p25"] == pytest.approx(4)
    assert stats["p75"] == pytest.approx(12)
    assert stats["mean"] == pytest.approx(0.004 * 2000)

    zeros = ciec.annual_bill_increase_stats(buildings, 0.0)
    assert zeros["mean"] == 0
    assert zeros["median"] == 0
    with pytest.raises(ValueError, match="non-negative"):
        ciec.annual_bill_increase_stats(buildings, -0.01)
    with pytest.raises(ValueError, match="empty"):
        ciec.annual_bill_increase_stats(buildings.clear(), 0.01)
    with pytest.raises(ValueError, match="annual_kwh"):
        ciec.annual_bill_increase_stats(buildings.drop("annual_kwh"), 0.01)


def test_autoenrolled_increases_are_the_charge_applied_to_each_home() -> None:
    import polars as pl

    increases = ciec.autoenrolled_increases(10, 25, 1.2, 0.4, 4_000.0)
    assert [row["label"] for row in increases] == ["Floor", "20%", "40%", "60%", "80%", "Ceiling"]
    assert increases[0]["customers"] == 10
    assert increases[0]["distribution"] == 12  # round(10 * 1.2)
    assert increases[0]["transmission"] == 4  # round(10 * 0.4)
    assert increases[0]["distribution_per_kwh"] == pytest.approx(12 / 4_000)
    assert increases[0]["transmission_per_kwh"] == pytest.approx(4 / 4_000)
    assert increases[0]["per_kwh"] == pytest.approx(16 / 4_000)
    assert increases[-1]["per_kwh"] == pytest.approx(40 / 4_000)
    with pytest.raises(ValueError, match="kwh must be positive"):
        ciec.autoenrolled_increases(10, 25, 1.2, 0.4, 0.0)
    with pytest.raises(ValueError, match="enrollment rows"):
        ciec.autoenrolled_increases(10, 25, 1.2, 0.4, [1_000.0, 2_000.0])

    buildings = pl.DataFrame({"bldg_id": [1, 2], "weight": [1.0, 1.0], "annual_kwh": [1000.0, 3000.0]})
    from_rows = ciec.bill_table_from_increases(increases, buildings)
    assert from_rows == ciec.autoenrolled_bill_table(10, 25, 1.2, 0.4, buildings)
    with pytest.raises(ValueError, match="empty"):
        ciec.bill_table_from_increases([], buildings)


def test_autoenrolled_bill_table_applies_the_existing_decrease_to_each_home() -> None:
    import polars as pl

    buildings = pl.DataFrame({"bldg_id": [1, 2], "weight": [1.0, 1.0], "annual_kwh": [1000.0, 3000.0]})
    table = ciec.autoenrolled_bill_table(10, 25, 1.2, 0.4, buildings)
    assert "| Share of the range | Customers | Mean | 25th | Median | 75th |" in table
    # round(10 * 1.2) + round(10 * 0.4) = 16, over 4,000 kWh. Bills are $4 and $12.
    assert "| Floor | 10 | \\$8.00 | \\$4.00 | \\$4.00 | \\$12.00 |" in table
    # 13 customers: round(15.6) + round(5.2) = 21. Bills are $5.25 and $15.75.
    assert "| 20% | 13 | \\$10.50 | \\$5.25 | \\$5.25 | \\$15.75 |" in table
    # 25 customers: 30 + 10 = 40. Bills are $10 and $30.
    assert "| Ceiling | 25 | \\$20.00 | \\$10.00 | \\$10.00 | \\$30.00 |" in table
    with pytest.raises(ValueError, match="kwh must be positive"):
        ciec.autoenrolled_bill_table(10, 25, 1.2, 0.4, pl.DataFrame({"weight": [1.0], "annual_kwh": [0.0]}))


def test_scaled_nonhp_sales_uses_each_rows_customers_who_remain() -> None:
    import polars as pl

    sales = ciec.scaled_nonhp_sales(800.0, 4_000.0, 1_200, 100)
    assert sales["customers"] == 1_100
    assert sales["scale"] == pytest.approx(1_100 / 800)
    assert sales["kwh"] == pytest.approx(4_000 * 1_100 / 800)
    with pytest.raises(ValueError, match="no customers"):
        ciec.scaled_nonhp_sales(800.0, 4_000.0, 100, 100)

    # Floor enrolls 10 and ceiling enrolls 25. Paying customers fall as enrollment rises,
    # so each row divides by a smaller kWh total.
    enrolled = [10, 13, 16, 19, 22, 25]
    paying = [1_200 - customers for customers in enrolled]
    kwh = [4_000.0 * customers / 800.0 for customers in paying]
    increases = ciec.autoenrolled_increases(10, 25, 1.2, 0.4, kwh, nonhp_customers=paying)
    assert increases[0]["distribution_per_kwh"] == pytest.approx(12 / kwh[0])
    assert increases[-1]["per_kwh"] == pytest.approx(40 / kwh[-1])
    assert increases[2]["nonhp_customers"] == 1_184
    assert increases[2]["nonhp_kwh"] == pytest.approx(kwh[2])

    table = ciec.autoenrolled_increase_table(
        10, 25, 1.2, 0.4, kwh, td_rate=0.10, full_rate=0.20, nonhp_customers=paying
    )
    assert "| Share of the range | Non-HP customers | Distribution (¢/kWh) |" in table
    assert "| Floor | 1,190 |" in table

    # The bill mean uses unscaled weights. It still equals revenue / paying customers,
    # because the charge was spread over kWh scaled by the same factor.
    buildings = pl.DataFrame({"weight": [1.0, 3.0], "annual_kwh": [1_000.0, 1_000.0]})
    raw_customers = 4.0
    raw_kwh = 4_000.0
    one = ciec.scaled_nonhp_sales(raw_customers, raw_kwh, 1_200, 100)
    row = ciec.autoenrolled_increases(100, 100, 1.2, 0.4, one["kwh"], nonhp_customers=one["customers"])[0]
    stats = ciec.annual_bill_increase_stats(buildings, row["per_kwh"])
    revenue = row["distribution"] + row["transmission"]
    assert stats["mean"] == pytest.approx(revenue / one["customers"])


def _write_energizect_export(path: Path, sector_2018: str = "Residential") -> None:
    import openpyxl

    wb = openpyxl.Workbook()
    ws = wb.active
    assert ws is not None
    ws.title = "Export"
    ws.append(["Year", None, None, 2017, 2018, "Total"])
    ws.append([None, None, "Air Source Mini-Split Heat Pump", "=SUMIFS(Detail!F:F)", None, None])
    detail = wb.create_sheet("Detail")
    detail.append(["Company", "Sector", "Heat Pump Type", "Sub Program", "Year", "Installations"])
    detail.append(["Eversource Electric", "Residential", "Air Source Mini-Split Heat Pump", None, 2017, 20])
    detail.append(["Eversource Electric", "Residential", "Air Source Mini-Split Heat Pump", "RES - HVAC", 2018, 30])
    detail.append(["Eversource Electric", sector_2018, "Air Source Mini-Split Heat Pump", "RES - Retrofit", 2018, 10])
    detail.append(["Eversource Electric", "Residential", "Heat Pump Water Heater", None, 2017, 10])
    detail.append(["Eversource Electric", "Residential", "VRF Heat Pump", "RES - HVAC", 2018, 1])
    wb.save(path)


def test_energizect_export_sums_sub_programs_from_detail(tmp_path: Path) -> None:
    path = tmp_path / "export.xlsx"
    _write_energizect_export(path)
    long = ciec.read_energizect_installations(path)
    assert long.rows() == [
        ("Air Source Mini-Split Heat Pump", 2017, 20),
        ("Air Source Mini-Split Heat Pump", 2018, 40),
        ("Heat Pump Water Heater", 2017, 10),
        ("VRF Heat Pump", 2018, 1),
    ]

    _write_energizect_export(path, sector_2018="Commercial")
    with pytest.raises(ValueError, match="more than one Sector"):
        ciec.read_energizect_installations(path)


def test_energizect_households_excludes_water_heaters_and_needs_every_ratio(tmp_path: Path) -> None:
    path = tmp_path / "export.xlsx"
    _write_energizect_export(path)
    long = ciec.read_energizect_installations(path)
    households = ciec.energizect_households(long, {"Air Source Mini-Split Heat Pump": 1.5, "VRF Heat Pump": 1.0})
    assert households["heat_pump_type"].to_list() == ["Air Source Mini-Split Heat Pump", "VRF Heat Pump"]
    assert households["households"].to_list() == pytest.approx([40.0, 1.0])

    with pytest.raises(ValueError, match="no systems-per-home ratio"):
        ciec.energizect_households(long, {"Air Source Mini-Split Heat Pump": 1.5})
    with pytest.raises(ValueError, match="at least 1"):
        ciec.energizect_households(long, {"Air Source Mini-Split Heat Pump": 0.5, "VRF Heat Pump": 1.0})
