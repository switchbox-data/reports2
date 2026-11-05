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


def test_workbook_divides_pasted_revenue_by_summed_kwh() -> None:
    floor, ceiling, buildings, generation = _case()
    wb = builder.build_workbook(
        floor,
        ceiling,
        buildings,
        distribution=0.11,
        transmission=0.05,
        generation_monthly=generation,
    )

    assert wb.sheetnames == ["README", "revenue", "nonhp_kwh", "rates", "increase"]

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
    assert increase["B5"].value == "=revenue!C5/nonhp_kwh!$B$4"
    assert increase["C5"].value == "=revenue!D5/nonhp_kwh!$B$4"
    assert increase["D5"].value == "=B5+C5"
    assert increase["E5"].value == "=D5/rates!$C$7"
    assert increase["F5"].value == "=D5/rates!$C$25"
    assert increase["G6"].value == "=revenue!G6/nonhp_kwh!$B$4"
    assert increase["I6"].value == "=G6+H6"
    assert increase["K6"].value == "=I6/rates!$C$25"
    assert increase["B5"].value.startswith("=")


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
        )
    with pytest.raises(ValueError, match="empty"):
        builder.build_workbook(
            floor,
            ceiling,
            buildings.clear(),
            distribution=0.11,
            transmission=0.05,
            generation_monthly=generation,
        )
    with pytest.raises(ValueError, match="positive"):
        builder.build_workbook(
            floor,
            ceiling,
            buildings,
            distribution=0.0,
            transmission=0.05,
            generation_monthly=generation,
        )
