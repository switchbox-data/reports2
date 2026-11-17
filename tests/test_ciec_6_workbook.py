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
    low = _rows(1000.0, 400.0, 900.0)
    high = _rows(3000.0, 1200.0, 700.0)
    return low, high


def test_workbook_average_bill_is_net_revenue_over_customers() -> None:
    low, high = _case()
    wb = builder.build_workbook(low, high)

    assert wb.sheetnames == ["README", "bill_impact"]

    ws = wb["bill_impact"]
    assert ws["A4"].value == "Rate year"
    assert ws["B4"].value == "Low: net revenue reduction (T&D)"
    assert ws["C4"].value == "Low: customers who remain"
    assert ws["F4"].value == "High: net revenue reduction (T&D)"
    assert ws["A5"].value == 2027
    assert ws["A6"].value == 2028

    # Low: net revenue and customers who remain are inputs (yellow).
    assert ws["B5"].value == 1400
    assert ws["C5"].value == 900
    assert ws["B5"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert ws["C5"].fill.fgColor.rgb[-6:] == "FFF2CC"

    # Low: average annual = net revenue / customers, monthly = annual / 12.
    assert ws["D5"].value == "=B5/C5"
    assert ws["E5"].value == "=D5/12"
    assert ws["D5"].fill.patternType is None

    # Second year.
    assert ws["B6"].value == round(1000.0 * 0.99) + round(400.0 * 0.99)
    assert ws["C6"].value == 800
    assert ws["D6"].value == "=B6/C6"
    assert ws["E6"].value == "=D6/12"

    # High: same structure in columns F-I.
    assert ws["F5"].value == 4200
    assert ws["G5"].value == 700
    assert ws["H5"].value == "=F5/G5"
    assert ws["I5"].value == "=H5/12"
    assert ws["F5"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert ws["H5"].fill.patternType is None

    assert builder.last_row(len(low)) == 6


def test_net_revenue_rounds_each_component_like_ciec_3() -> None:
    # Rounding the sum would give 1,401; the CIEC-3 revenue sheet rounds each component first.
    row = {"year": 2027, "net_reduction_dist": 1000.4, "net_reduction_tx": 400.4, "nonhp_customers": 10}
    assert builder.net_revenue(row) == 1400
    ws = builder.build_workbook([row], [row])["bill_impact"]
    assert ws["B5"].value == 1400


def test_rejects_invalid_inputs() -> None:
    low, high = _case()

    with pytest.raises(ValueError, match="empty"):
        builder.build_workbook([], high)

    with pytest.raises(ValueError, match="missing key"):
        builder.build_workbook([{"year": 2027}], [{"year": 2027}])

    with pytest.raises(ValueError, match="positive"):
        bad = [{"year": 2027, "net_reduction_dist": 100.0, "net_reduction_tx": 50.0, "nonhp_customers": 0}]
        builder.build_workbook(bad, bad)

    with pytest.raises(ValueError, match="rows"):
        builder.build_workbook(low, high[:1])

    with pytest.raises(ValueError, match="years differ"):
        builder.build_workbook(low, [{**r, "year": r["year"] + 1} for r in high])
