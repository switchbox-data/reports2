"""Formula wiring for the CIEC-6(c) workpaper. Does not load ResStock or upload."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import polars as pl
import pytest


def _load() -> ModuleType:
    path = (
        Path(__file__).resolve().parents[1] / "reports" / "ct_hp_rates" / "ciec_requests" / "build_ciec_6_workbook.py"
    )
    spec = importlib.util.spec_from_file_location("ciec_6_workbook_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


builder = _load()


def _case() -> tuple[object, object, pl.DataFrame, object, object]:
    floor = builder.RevenueRow("Existing", 10, 100.0, 40.0)
    ceiling = builder.RevenueRow("Existing", 30, 300.0, 50.0)
    buildings = pl.DataFrame(
        {
            "bldg_id": [20, 10],
            "weight": [1.5, 2.0],
            "annual_kwh": [100.0, 40.0],
        }
    )
    # Weighted kWh is 40 * 2 + 100 * 1.5 = 230. The charges are those dollars over that kWh.
    floor_charge = builder.ChargeRow(100 / 230, 40 / 230, 140 / 230)
    ceiling_charge = builder.ChargeRow(300 / 230, 50 / 230, 350 / 230)
    return floor, ceiling, buildings, floor_charge, ceiling_charge


def test_workbook_bills_each_home_at_the_per_kwh_increase() -> None:
    floor, ceiling, buildings, floor_charge, ceiling_charge = _case()
    wb = builder.build_workbook(floor, ceiling, buildings, floor_charge, ceiling_charge)

    assert wb.sheetnames == ["README", "revenue", "customers", "increase", "summary"]

    revenue = wb["revenue"]
    assert revenue["A5"].value == "Existing"
    assert revenue["B5"].value == 10
    assert revenue["C5"].value == 100.0
    assert revenue["E5"].value == "=C5+D5"
    assert revenue["G5"].value == 300.0
    assert revenue["I5"].value == "=G5+H5"
    assert revenue["C5"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert revenue["E5"].fill.patternType is None

    customers = wb["customers"]
    assert customers["A8"].value == 10
    assert customers["A9"].value == 20
    assert customers["B8"].value == 2.0
    assert customers["C8"].value == 40.0
    assert customers["D8"].value == "=B8*C8"
    assert customers["D9"].value == "=B9*C9"
    assert customers["E8"].value == "=C8*increase!$B$5"
    assert customers["F8"].value == "=C8*increase!$C$5"
    assert customers["G8"].value == "=E8+F8"
    assert customers["H9"].value == "=C9*increase!$E$5"
    assert customers["J9"].value == "=H9+I9"
    assert all(customers.cell(7, col).value != "cumulative weight" for col in range(1, 11))
    assert customers["B4"].value == "=SUM(D8:D9)"
    assert customers["B6"].value == "=SUM(B8:B9)"
    assert customers["H8"].fill.patternType is None

    increase = wb["increase"]
    assert increase["A5"].value == "Existing"
    assert increase["B5"].value == pytest.approx(100 / 230)
    assert increase["C5"].value == pytest.approx(40 / 230)
    assert increase["D5"].value == pytest.approx(140 / 230)
    assert increase["E5"].value == pytest.approx(300 / 230)
    assert increase["F5"].value == pytest.approx(50 / 230)
    assert increase["G5"].value == pytest.approx(350 / 230)
    assert increase["B5"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert increase["D5"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert all(not str(increase.cell(5, col).value).startswith("=") for col in range(1, 8))

    summary = wb["summary"]
    assert summary["A7"].value == "Mean bill"
    assert summary["B7"].value == "=SUMPRODUCT(customers!G8:G9,customers!B8:B9)/customers!$B$6"
    assert summary["C6"].value == "=SUMPRODUCT(customers!I8:I9,customers!B8:B9)/customers!$B$6"
    assert summary["B8"].value == "=revenue!E5/customers!$B$6"
    assert summary["C8"].value == "=revenue!I5/customers!$B$6"
    assert summary["A9"].value == "25th percentile"
    running = "SCAN(0,customers!$B$8:$B9,LAMBDA(acc,w,acc+w))"
    assert summary["B10"].value == f"=INDEX(customers!G$8:G9,XMATCH(0.50*customers!$B$6,{running},1))"
    assert summary["C9"].value == f"=INDEX(customers!J$8:J9,XMATCH(0.25*customers!$B$6,{running},1))"
    assert summary["A11"].value == "75th percentile"


def test_rejects_inputs_that_cannot_support_the_bill() -> None:
    floor, ceiling, buildings, floor_charge, ceiling_charge = _case()
    with pytest.raises(ValueError, match="labels"):
        builder.build_workbook(
            builder.RevenueRow("Existing", 10, 100.0, 40.0),
            builder.RevenueRow("2027", 30, 300.0, 50.0),
            buildings,
            floor_charge,
            ceiling_charge,
        )
    with pytest.raises(ValueError, match="empty"):
        builder.build_workbook(floor, ceiling, buildings.clear(), floor_charge, ceiling_charge)
    with pytest.raises(ValueError, match="positive"):
        builder.build_workbook(
            floor,
            ceiling,
            buildings.with_columns(pl.lit(0.0).alias("weight")),
            floor_charge,
            ceiling_charge,
        )
    with pytest.raises(ValueError, match="non-negative"):
        builder.build_workbook(
            floor,
            ceiling,
            buildings.with_columns(pl.lit(-1.0).alias("annual_kwh")),
            floor_charge,
            ceiling_charge,
        )
    with pytest.raises(ValueError, match="non-negative"):
        builder.build_workbook(floor, ceiling, buildings, builder.ChargeRow(-0.01, 0.0, 0.0), ceiling_charge)
