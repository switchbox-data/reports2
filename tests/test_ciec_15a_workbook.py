"""Formula wiring for the CIEC-15(a) workpaper. Does not load ResStock or upload."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest
from openpyxl import load_workbook


def _load() -> ModuleType:
    path = (
        Path(__file__).resolve().parents[1] / "reports" / "ct_hp_rates" / "ciec_requests" / "build_ciec_15a_workbook.py"
    )
    spec = importlib.util.spec_from_file_location("ciec_15a_workbook_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


builder = _load()


def _inputs() -> object:
    flat = tuple(1.0 for _ in range(12))
    return builder.WorkbookInputs(
        kwh_before=tuple(10.0 for _ in range(12)),
        kwh_after=tuple(20.0 for _ in range(12)),
        customer_charge=flat,
        generation=tuple(0.1 for _ in range(12)),
        distribution=(
            builder.RateLine("Distribution energy", tuple(0.05 for _ in range(12))),
            builder.RateLine("System benefits", tuple(0.01 for _ in range(12))),
        ),
        transmission=(builder.RateLine("Transmission", tuple(0.02 for _ in range(12))),),
        marginal_cost_before=1.0,
        marginal_cost_after=1.96,
        annual_bills=1_200.0,
        billed_mwh=12.0,
    )


def test_customer_charge_follows_consumption_and_rate_1() -> None:
    inputs = _inputs()
    derived = builder.derive(inputs)
    assert derived.annual_kwh_before == pytest.approx(120.0)
    assert derived.annual_kwh_after == pytest.approx(240.0)
    assert derived.annual_customer_charge_before == pytest.approx(12.0)
    assert derived.customer_charge_delta == pytest.approx(0.0)
    assert derived.annual_generation_before == pytest.approx(12.0)
    assert derived.generation_delta == pytest.approx(12.0)
    # 0.06 $/kWh of distribution, including the rider, and 0.02 of transmission.
    assert derived.distribution_delta == pytest.approx(7.2)
    assert derived.transmission_delta == pytest.approx(2.4)
    assert derived.scaling_factor == pytest.approx(0.1)
    assert derived.class_monthly_kwh == pytest.approx(1_000.0)
    assert derived.class_variable_revenue == pytest.approx(960.0)
    assert derived.class_revenue_shift == pytest.approx(864.0)
    assert derived.fixed_charge_delta == pytest.approx(0.72)
    assert derived.fixed_charge == pytest.approx(1.72)
    assert derived.revenue_gap == pytest.approx(0.0, abs=1e-9)
    assert derived.cost_gap == pytest.approx(0.0, abs=1e-9)

    wb = builder.build_workbook(inputs)
    assert wb.sheetnames == [
        "representative_home_consumption",
        "rate_1",
        "representative_home_bills",
        "class",
        "modified_rate_1",
    ]
    consumption = wb["representative_home_consumption"]
    assert consumption["A2"].value == "Jan"
    assert consumption["B2"].value == 10.0
    assert consumption["C13"].value == 20.0
    assert consumption["D2"].value == "=C2-B2"
    assert consumption["B14"].value == "=SUM(B2:B13)"
    assert consumption["D14"].value == "=C14-B14"
    assert consumption["B2"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert consumption["D2"].fill.patternType is None

    rates = wb["rate_1"]
    assert rates["A1"].value == "Month"
    assert rates["B1"].value == "Customer charge"
    assert rates["C1"].value == "Generation supply"
    assert rates["D1"].value == "Distribution"
    assert rates["G1"].value == "Transmission"
    assert rates["D2"].value == "Distribution energy ($/kWh)"
    assert rates["E2"].value == "System benefits ($/kWh)"
    assert rates["F2"].value == "Total ($/kWh)"
    assert rates["G2"].value == "Transmission ($/kWh)"
    assert rates["A3"].value == "=representative_home_consumption!A2"
    assert rates["B3"].value == 1.0
    assert rates["C3"].value == 0.1
    assert rates["D3"].value == 0.05
    assert rates["E3"].value == 0.01
    assert rates["F3"].value == "=SUM(D3:E3)"
    assert rates["G3"].value == 0.02
    assert rates["D3"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert rates["F3"].fill.patternType is None

    bills = wb["representative_home_bills"]
    assert bills["B2"].value == "=SUM(rate_1!B3:B14)"
    assert bills["C2"].value == "=SUM(rate_1!B3:B14)"
    assert bills["B3"].value == "=SUMPRODUCT(representative_home_consumption!B2:B13,rate_1!C3:C14)"
    assert bills["C4"].value == "=SUMPRODUCT(representative_home_consumption!C2:C13,rate_1!F3:F14)"
    assert bills["B5"].value == "=SUMPRODUCT(representative_home_consumption!B2:B13,rate_1!G3:G14)"
    assert bills["D6"].value == "=D4+D5"
    assert bills["B7"].value == 1.0
    assert bills["D8"].value == "=D7/D6"
    assert bills["B7"].fill.fgColor.rgb[-6:] == "FFF2CC"
    assert bills["B3"].fill.patternType is None

    klass = wb["class"]
    assert klass["B4"].value == "=B2/12"
    assert klass["B7"].value == "=(SUM(rate_1!F3:F14)+SUM(rate_1!G3:G14))*B6"

    modified = wb["modified_rate_1"]
    assert modified["B2"].value == "=representative_home_bills!D8"
    assert modified["B3"].value == "=class!B7"
    assert modified["B4"].value == "=(1-B2)*B3"
    assert modified["B5"].value == "=class!B4"
    assert modified["B6"].value == "=B4/(B5*12)"
    assert modified["B7"].value == "=AVERAGE(rate_1!B3:B14)"
    assert modified["B8"].value == "=B7+B6"
    assert modified["B9"].value == "=ROUND(B8,2)"
    assert modified["B7"].fill.patternType is None
    assert modified["B8"].fill.patternType is None


def test_read_back_rejects_a_changed_marginal_cost(tmp_path: Path) -> None:
    inputs = _inputs()
    path = tmp_path / "charge.xlsx"
    builder.build_workbook(inputs).save(path)
    evaluated = builder.assert_workbook(path, inputs, builder.derive(inputs))
    assert evaluated.fixed_charge == pytest.approx(1.72)

    wb = load_workbook(path)
    wb["representative_home_bills"]["C7"] = 999.0
    wb.save(path)
    with pytest.raises(AssertionError, match="marginal cost after"):
        builder.assert_workbook(path, inputs, builder.derive(inputs))
