"""Formula wiring for the CIEC-1(a) workpaper. Does not load ResStock or upload."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def _load() -> ModuleType:
    path = (
        Path(__file__).resolve().parents[1] / "reports" / "ct_hp_rates" / "ciec_requests" / "build_ciec_1a_workbook.py"
    )
    spec = importlib.util.spec_from_file_location("ciec_1a_workbook_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


builder = _load()


def test_workbook_has_enrollment_and_revenue_sheets() -> None:
    case = builder.Case(
        dec_dist=723.61,
        dec_tx=316.73,
        inc_dist=2.22,
        inc_tx=8.08,
        enrollment=builder.EnrollmentInputs(
            energizect=[
                ("Air Source Mini-Split Heat Pump", 40_000, 1.37),
                ("Air Source, Ducted Heat Pump", 15_000, 1.0),
            ],
            clm_annual=3_460,
            eversource_per_thousand=784,
            years=[2027, 2028, 2029, 2030, 2031],
            statewide_additions=[8_000, 9_000, 10_000, 12_000, 14_000],
        ),
    )
    wb = builder.build_workbook(case)

    assert wb.sheetnames == ["README", "enrollment", "revenue"]

    enrollment = wb["enrollment"]
    assert enrollment["B6"].value == 40_000
    assert enrollment["C6"].value == 1.37
    assert enrollment["D6"].value == "=B6/C6"

    revenue = wb["revenue"]
    assert revenue["C4"].value == 723.61
    assert revenue["E4"].value == 316.73
    assert revenue["C5"].value == 2.22
    assert revenue["E5"].value == 8.08
    assert revenue["G4"].value == "=C4+E4"
    assert revenue["G5"].value == "=C5+E5"

    # First floor data row: existing customers x decrease, new x increase, net = inc - red
    first_floor = 10
    assert revenue[f"D{first_floor}"].value == f"=ROUND(B{first_floor}*$C$4,0)"
    assert revenue[f"E{first_floor}"].value == f"=ROUND(B{first_floor}*$E$4,0)"
    assert revenue[f"F{first_floor}"].value == f"=ROUND(C{first_floor}*$C$5,0)"
    assert revenue[f"G{first_floor}"].value == f"=ROUND(C{first_floor}*$E$5,0)"
    assert revenue[f"H{first_floor}"].value == f"=F{first_floor}-D{first_floor}"
    assert revenue[f"I{first_floor}"].value == f"=G{first_floor}-E{first_floor}"
