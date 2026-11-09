"""Formula wiring for the CIEC-3(c) workpaper. Does not load ResStock or upload."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import polars as pl
import pytest


def _load() -> ModuleType:
    path = (
        Path(__file__).resolve().parents[1] / "reports" / "ct_hp_rates" / "ciec_requests" / "build_ciec_3_workbook.py"
    )
    spec = importlib.util.spec_from_file_location("ciec_3_workbook_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


builder = _load()


def _generation() -> dict[str, float]:
    return {f"2025-{month:02d}": 0.02 for month in range(1, 13)}


def _case() -> tuple[list, list, pl.DataFrame, dict[str, float]]:
    floor = [
        builder.RevenueRow("Existing", 10, 100.0, 40.0),
        builder.RevenueRow("2027", 12, 200.0, 80.0),
    ]
    ceiling = [
        builder.RevenueRow("Existing", 30, 300.0, 50.0),
        builder.RevenueRow("2027", 40, 400.0, 90.0),
    ]
    buildings = pl.DataFrame(
        {
            "bldg_id": [20, 10],
            "weight": [1.5, 2.0],
            "annual_kwh": [100.0, 40.0],
        }
    )
    return floor, ceiling, buildings, _generation()


def test_workbook_divides_pasted_revenue_by_scaled_kwh() -> None:
    floor, ceiling, buildings, generation = _case()
    wb = builder.build_workbook(
        floor,
        ceiling,
        buildings,
        distribution=0.11,
        transmission=0.05,
        generation_monthly=generation,
        rate_year_customers=100,
    )

    assert wb.sheetnames == ["README", "revenue", "nonhp_kwh", "payers", "rates", "increase"]

    revenue = wb["revenue"]
    assert revenue["A5"].value == "Existing"
    assert revenue["A6"].value == 2027
    assert revenue["C5"].value == 100.0
    assert revenue["D5"].value == 40.0
    assert revenue["E5"].value == "=C5+D5"
    assert revenue["G6"].value == 400.0
    assert revenue["I6"].value == "=G6+H6"
    assert revenue["C5"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert revenue["E5"].fill.patternType is None

    kwh = wb["nonhp_kwh"]
    assert kwh["A8"].value == 10
    assert kwh["A9"].value == 20
    assert kwh["B8"].value == 2.0
    assert kwh["C8"].value == 40.0
    assert kwh["D8"].value == "=B8*C8"
    assert kwh["D9"].value == "=B9*C9"
    assert kwh["B4"].value == "=SUM(D8:D9)"
    assert kwh["B5"].value == "=COUNTA(A8:A9)"
    assert kwh["B6"].value == "=SUM(B8:B9)"
    assert kwh["A6"].value == "ResStock customers"

    payers = wb["payers"]
    assert payers["B4"].value == 100
    assert payers["B4"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert payers["B5"].value == "=nonhp_kwh!B6"
    assert payers["B6"].value == "=nonhp_kwh!B4"
    assert payers["A9"].value == "=revenue!A5"
    assert payers["B9"].value == "=revenue!B5"
    assert payers["C9"].value == "=$B$4-B9"
    assert payers["D9"].value == "=C9/$B$5"
    assert payers["E9"].value == "=$B$6*D9"
    assert payers["F9"].value == "=revenue!F5"
    assert payers["G9"].value == "=$B$4-F9"
    assert payers["H9"].value == "=G9/$B$5"
    assert payers["I9"].value == "=$B$6*H9"
    assert payers["B10"].value == "=revenue!B6"
    assert payers["C9"].fill.patternType is None

    rates = wb["rates"]
    assert rates["C5"].value == 0.11
    assert rates["C6"].value == 0.05
    assert rates["C7"].value == "=C5+C6"
    assert rates["D5"].value == "=C5*100"
    assert rates["C11"].value == 0.02
    assert rates["C22"].value == 0.02
    assert rates["D11"].value == "=C11*100"
    assert rates["C23"].value == "=AVERAGE(C11:C22)"
    assert rates["C25"].value == "=C7+C23"

    increase = wb["increase"]
    assert increase["A5"].value == "=revenue!A5"
    assert increase["B5"].value == "=revenue!C5/payers!E9"
    assert increase["C5"].value == "=revenue!D5/payers!E9"
    assert increase["D5"].value == "=B5+C5"
    assert increase["E5"].value == "=D5/rates!$C$7"
    assert increase["F5"].value == "=D5/rates!$C$25"
    assert increase["G6"].value == "=revenue!G6/payers!I10"
    assert increase["I6"].value == "=G6+H6"
    assert increase["K6"].value == "=I6/rates!$C$25"
    assert increase["B5"].value.startswith("=")


def test_enrollment_range_is_formulas_between_floor_and_ceiling() -> None:
    floor = [builder.RevenueRow("Existing", 10, 100.0, 40.0)]
    ceiling = [builder.RevenueRow("Existing", 30, 300.0, 120.0)]
    _floor, _ceiling, buildings, generation = _case()
    wb = builder.build_workbook(
        floor,
        ceiling,
        buildings,
        distribution=0.11,
        transmission=0.05,
        generation_monthly=generation,
        rate_year_customers=100,
        per_customer_distribution=10.0,
        per_customer_transmission=4.0,
    )

    revenue = wb["revenue"]
    assert revenue["B4"].value == 10.0
    assert revenue["B5"].value == 4.0
    assert revenue["B4"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert [revenue.cell(row, 1).value for row in range(8, 14)] == ["Floor", "20%", "40%", "60%", "80%", "Ceiling"]
    assert revenue["B8"].value == 10
    assert revenue["B13"].value == 30
    assert revenue["B9"].value == "=ROUND($B$8+(1/5)*($B$13-$B$8),0)"
    assert revenue["B10"].value == "=ROUND($B$8+(2/5)*($B$13-$B$8),0)"
    assert revenue["B12"].value == "=ROUND($B$8+(4/5)*($B$13-$B$8),0)"
    assert revenue["C8"].value == "=ROUND(B8*$B$4,0)"
    assert revenue["D13"].value == "=ROUND(B13*$B$5,0)"
    assert revenue["E9"].value == "=C9+D9"
    assert revenue["C8"].fill.patternType is None
    assert revenue["B9"].fill.patternType is None

    payers = wb["payers"]
    assert payers["A8"].value == "=revenue!A8"
    assert payers["B9"].value == "=revenue!B9"
    assert payers["C12"].value == "=$B$4-B12"
    assert payers["E13"].value == "=$B$6*D13"

    increase = wb["increase"]
    assert increase["A11"].value == "=revenue!A11"
    assert increase["B8"].value == "=revenue!C8/payers!E8"
    assert increase["C13"].value == "=revenue!D13/payers!E13"
    assert increase["D9"].value == "=B9+C9"
    assert increase["E12"].value == "=D12/rates!$C$7"
    assert increase["F13"].value == "=D13/rates!$C$25"
    assert increase["B8"].fill.patternType is None


def test_rejects_inputs_that_cannot_support_the_increase() -> None:
    floor, ceiling, buildings, generation = _case()
    with pytest.raises(ValueError, match="labels"):
        builder.build_workbook(
            [floor[0]],
            ceiling,
            buildings,
            distribution=0.11,
            transmission=0.05,
            generation_monthly=generation,
            rate_year_customers=100,
        )
    missing = dict(generation)
    missing.pop("2025-07")
    with pytest.raises(ValueError, match="generation months"):
        builder.build_workbook(
            floor,
            ceiling,
            buildings,
            distribution=0.11,
            transmission=0.05,
            generation_monthly=missing,
            rate_year_customers=100,
        )
    with pytest.raises(ValueError, match="empty"):
        builder.build_workbook(
            floor,
            ceiling,
            buildings.clear(),
            distribution=0.11,
            transmission=0.05,
            generation_monthly=generation,
            rate_year_customers=100,
        )
    with pytest.raises(ValueError, match="positive"):
        builder.build_workbook(
            floor,
            ceiling,
            buildings,
            distribution=0.0,
            transmission=0.05,
            generation_monthly=generation,
            rate_year_customers=100,
        )
    with pytest.raises(ValueError, match="nobody"):
        builder.build_workbook(
            floor,
            ceiling,
            buildings,
            distribution=0.11,
            transmission=0.05,
            generation_monthly=generation,
            rate_year_customers=40,
        )
