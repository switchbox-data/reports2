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


def _case() -> tuple[object, object, pl.DataFrame]:
    floor = builder.RevenueRow("Existing", 10, 100.0, 40.0)
    ceiling = builder.RevenueRow("Existing", 30, 300.0, 120.0)
    buildings = pl.DataFrame(
        {
            "bldg_id": [20, 10],
            "weight": [1.5, 2.0],
            "annual_kwh": [100.0, 40.0],
        }
    )
    return floor, ceiling, buildings


def _build(floor: object, ceiling: object, buildings: pl.DataFrame, **kwargs: object):
    arguments: dict[str, object] = {
        "per_customer_distribution": 10.0,
        "per_customer_transmission": 4.0,
        "rate_year_customers": 100,
    }
    arguments.update(kwargs)
    return builder.build_workbook(floor, ceiling, buildings, **arguments)


def test_workbook_bills_each_home_at_the_per_kwh_increase() -> None:
    floor, ceiling, buildings = _case()
    wb = _build(floor, ceiling, buildings)

    assert wb.sheetnames == ["README", "revenue", "payers", "customers", "increase", "summary"]

    revenue = wb["revenue"]
    assert revenue["B4"].value == 10.0
    assert revenue["B5"].value == 4.0
    assert revenue["B4"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert [revenue.cell(row, 1).value for row in range(8, 14)] == ["Floor", "20%", "40%", "60%", "80%", "Ceiling"]
    assert revenue["B8"].value == 10
    assert revenue["B13"].value == 30
    assert revenue["B9"].value == "=ROUND($B$8+(1/5)*($B$13-$B$8),0)"
    assert revenue["C8"].value == "=ROUND(B8*$B$4,0)"
    assert revenue["D13"].value == "=ROUND(B13*$B$5,0)"
    assert revenue["E9"].value == "=C9+D9"
    assert revenue["C8"].fill.patternType is None

    payers = wb["payers"]
    assert payers["B4"].value == 100
    assert payers["B4"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert payers["B5"].value == "=customers!B6"
    assert payers["B6"].value == "=customers!B4"
    assert payers["B8"].value == "=revenue!B8"
    assert payers["C9"].value == "=$B$4-B9"
    assert payers["E13"].value == "=$B$6*D13"
    assert payers["C8"].fill.patternType is None

    customers = wb["customers"]
    assert customers["A8"].value == 10
    assert customers["A9"].value == 20
    assert customers["B8"].value == 2.0
    assert customers["C8"].value == 40.0
    assert customers["D8"].value == "=B8*C8"
    assert customers["D9"].value == "=B9*C9"
    assert customers["E8"].value == "=C8*increase!$D$8"
    assert customers["F9"].value == "=C9*increase!$D$9"
    assert customers["J8"].value == "=C8*increase!$D$13"
    assert all(customers.cell(7, col).value != "cumulative weight" for col in range(1, 11))
    assert customers["B4"].value == "=SUM(D8:D9)"
    assert customers["A6"].value == "ResStock weight"
    assert customers["B6"].value == "=SUM(B8:B9)"
    assert customers["H8"].fill.patternType is None

    increase = wb["increase"]
    assert increase["A8"].value == "=revenue!A8"
    assert increase["B9"].value == "=revenue!C9/payers!E9"
    assert increase["C13"].value == "=revenue!D13/payers!E13"
    assert increase["D8"].value == "=B8+C8"
    assert increase["B8"].fill.patternType is None

    summary = wb["summary"]
    assert summary["A7"].value == "Mean bill"
    assert summary["B7"].value == "=SUMPRODUCT(customers!E8:E9,customers!B8:B9)/customers!$B$6"
    assert summary["G7"].value == "=SUMPRODUCT(customers!J8:J9,customers!B8:B9)/customers!$B$6"
    assert summary["B5"].value == "=revenue!C8/payers!C8"
    assert summary["C6"].value == "=revenue!D9/payers!C9"
    assert summary["G8"].value == "=revenue!E13/payers!C13"
    assert summary["A9"].value == "25th percentile"
    running = "SCAN(0,customers!$B$8:$B9,LAMBDA(acc,w,acc+w))"
    assert summary["B10"].value == f"=INDEX(customers!E$8:E9,XMATCH(0.50*customers!$B$6,{running},1))"
    assert summary["C9"].value == f"=INDEX(customers!F$8:F9,XMATCH(0.25*customers!$B$6,{running},1))"
    assert summary["G11"].value == f"=INDEX(customers!J$8:J9,XMATCH(0.75*customers!$B$6,{running},1))"
    assert summary["A11"].value == "75th percentile"


def test_rejects_inputs_that_cannot_support_the_bill() -> None:
    floor, ceiling, buildings = _case()
    with pytest.raises(ValueError, match="labels"):
        builder.build_workbook(
            builder.RevenueRow("Existing", 10, 100.0, 40.0),
            builder.RevenueRow("2027", 30, 300.0, 120.0),
            buildings,
            per_customer_distribution=10.0,
            per_customer_transmission=4.0,
            rate_year_customers=100,
        )
    with pytest.raises(ValueError, match="empty"):
        _build(floor, ceiling, buildings.clear())
    with pytest.raises(ValueError, match="positive"):
        _build(floor, ceiling, buildings.with_columns(pl.lit(0.0).alias("weight")))
    with pytest.raises(ValueError, match="non-negative"):
        _build(floor, ceiling, buildings.with_columns(pl.lit(-1.0).alias("annual_kwh")))
    with pytest.raises(ValueError, match="non-negative"):
        builder.build_workbook(
            floor,
            ceiling,
            buildings,
            per_customer_distribution=-0.01,
            per_customer_transmission=4.0,
            rate_year_customers=100,
        )
    with pytest.raises(ValueError, match="nobody"):
        _build(floor, ceiling, buildings, rate_year_customers=30)
