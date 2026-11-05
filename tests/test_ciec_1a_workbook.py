"""Formula wiring for the CIEC-1(a) workpaper. Does not load ResStock or upload."""

from __future__ import annotations

import importlib.util
import sys
from datetime import datetime
from pathlib import Path
from types import ModuleType

import polars as pl


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


def test_workbook_derives_bills_and_revenue_from_the_hourly_load() -> None:
    charges = [
        builder.Charge(
            label, "$/kWh" if label != "Customer charge" else "$/month", dict.fromkeys(builder.MONTHS, 0.01), ""
        )
        for _, _, label, _ in builder.RATE_INPUTS
    ]
    hourly = pl.DataFrame(
        {
            "timestamp": [datetime(2025, month, 1) for month in range(1, 13)],
            "kwh": [1.0] * 12,
        }
    )
    case = builder.Case(
        hourly=hourly,
        charges=charges,
        winter_dist=0.03,
        winter_tx=0.01,
        n_buildings=2,
        total_weight=2.0,
        enrollment=builder.EnrollmentInputs(
            rebates_since_2023=4_400,
            clm_2026=3_528,
            hp_share_percent=9,
            rate_year_customers=1_212_521,
            clm_annual=3_460,
            eversource_per_thousand=784,
            years=[2027, 2028, 2029, 2030, 2031],
            statewide_additions=[8_000, 9_000, 10_000, 12_000, 14_000],
        ),
    )
    wb = builder.build_workbook(case)

    assert wb.sheetnames == ["README", "hp_home_8760", "rates", "bill_change", "enrollment", "revenue"]
    hourly_ws = wb["hp_home_8760"]
    assert hourly_ws["C2"].value.startswith("=CHOOSE(MONTH(A2)")
    assert "Winter" in hourly_ws["D2"].value
    assert hourly_ws["B2"].value == 1.0

    bill = wb["bill_change"]
    assert bill["B5"].value.startswith("=SUMIFS(hp_home_8760!")
    assert bill["D5"].value.startswith("=B5*rates!")
    assert bill["C5"].value.startswith("=rates!C")
    assert bill["D22"].value.startswith("=B22-C22")

    enrollment = wb["enrollment"]
    assert enrollment["B5"].value == 4_400
    assert enrollment["B7"].value == "=B5+B6"
    assert enrollment["B10"].value == "=ROUND(B9*B8/100,0)"
    assert enrollment["D16"].value == "=B16*$B$12/1000"
    assert enrollment["B24"].value == "=$B$7"
    assert enrollment["B25"].value == "=B24+C16"

    revenue = wb["revenue"]
    assert revenue["B4"].value == "=bill_change!$D$22"
    assert revenue["C8"].value == "=ROUND(B8*$B$4,0)"
    assert revenue["E8"].value == "=C8+D8"
    assert revenue["B8"].value == "=enrollment!B24"
