"""Formula wiring for the CIEC-6(c) workpaper. Does not load ResStock or upload."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

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


def _rows(net_dist: float, net_tx: float, customers: float) -> list[dict[str, float]]:
    return [
        {"year": 2027, "net_reduction_dist": net_dist, "net_reduction_tx": net_tx, "nonhp_customers": customers},
        {
            "year": 2028,
            "net_reduction_dist": net_dist * 0.99,
            "net_reduction_tx": net_tx * 0.99,
            "nonhp_customers": customers - 100,
        },
    ]


def _case() -> tuple[list[dict[str, float]], list[dict[str, float]]]:
    floor = _rows(1000.0, 400.0, 900.0)
    ceiling = _rows(3000.0, 1200.0, 700.0)
    return floor, ceiling


def test_workbook_mean_bill_is_net_revenue_over_customers() -> None:
    floor, ceiling = _case()
    wb = builder.build_workbook(floor, ceiling)

    assert wb.sheetnames == ["README", "bill_impact"]

    ws = wb["bill_impact"]
    assert ws["A5"].value == 2027
    assert ws["A6"].value == 2028

    # Floor: net revenue and remaining customers are inputs (yellow).
    assert ws["B5"].value == round(1000.0 + 400.0)
    assert ws["C5"].value == 900
    assert ws["B5"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert ws["C5"].fill.fgColor.rgb[-6:] == "FFF2CC"

    # Floor: mean annual = net_revenue / customers, monthly = annual / 12.
    assert ws["D5"].value == "=B5/C5"
    assert ws["E5"].value == "=D5/12"
    assert ws["D5"].fill.patternType is None

    # Second year.
    assert ws["B6"].value == round(1000.0 * 0.99 + 400.0 * 0.99)
    assert ws["C6"].value == 800
    assert ws["D6"].value == "=B6/C6"
    assert ws["E6"].value == "=D6/12"

    # Ceiling: same structure in columns F-I.
    assert ws["F5"].value == round(3000.0 + 1200.0)
    assert ws["G5"].value == 700
    assert ws["H5"].value == "=F5/G5"
    assert ws["I5"].value == "=H5/12"
    assert ws["F5"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert ws["H5"].fill.patternType is None


def test_rejects_invalid_inputs() -> None:
    floor, ceiling = _case()

    with pytest.raises(ValueError, match="empty"):
        builder.build_workbook([], ceiling)

    with pytest.raises(ValueError, match="missing key"):
        builder.build_workbook([{"year": 2027}], [{"year": 2027}])

    with pytest.raises(ValueError, match="positive"):
        bad = [{"year": 2027, "net_reduction_dist": 100.0, "net_reduction_tx": 50.0, "nonhp_customers": 0}]
        builder.build_workbook(bad, bad)

    with pytest.raises(ValueError, match="rows"):
        builder.build_workbook(floor, ceiling[:1])
