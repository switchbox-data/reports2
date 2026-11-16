"""Formula wiring for the CIEC-10(a) workpaper. Does not load ResStock or upload."""

from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timedelta
from pathlib import Path
from types import ModuleType

import polars as pl
import pytest


def _load() -> ModuleType:
    path = (
        Path(__file__).resolve().parents[1] / "reports" / "ct_hp_rates" / "ciec_requests" / "build_ciec_10_workbook.py"
    )
    spec = importlib.util.spec_from_file_location("ciec_10_workbook_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


builder = _load()


def _hourly() -> pl.DataFrame:
    start = datetime(2025, 1, 1)
    backup = [0.0] * 8760
    backup[100] = 9.5
    return pl.DataFrame(
        {
            "timestamp": [start + timedelta(hours=h) for h in range(8760)],
            "weather_hour": [datetime(2018, 1, 3) + timedelta(hours=h) for h in range(8760)],
            "backup_kwh": backup,
            "heat_pump_kwh": [1.0] * 8760,
            "grid_kwh": [2.0] * 8760,
        }
    )


def _inputs(hourly: pl.DataFrame) -> object:
    return builder.Inputs(hourly=hourly, n_bldg=3, release="res_test", kwh_scale=0.99)


def test_hourly_sheet_layout_and_formulas() -> None:
    wb = builder.build_workbook(_inputs(_hourly()))

    assert wb.sheetnames == ["README", "hourly_load"]
    ws = wb["hourly_load"]
    assert [ws.cell(1, c).value for c in range(1, 7)] == [
        "timestamp",
        "weather_hour_2018",
        "backup_kwh",
        "heat_pump_kwh",
        "whole_home_kwh",
        "heat_pump_plus_backup_kwh",
    ]
    assert ws.max_row == 8761
    assert ws["A2"].value == datetime(2025, 1, 1)
    assert ws["B2"].value == datetime(2018, 1, 3)
    assert ws["C102"].value == 9.5
    assert ws["D2"].value == 1.0
    assert ws["E2"].value == 2.0
    assert ws["F2"].value == "=C2+D2"
    assert ws["F8761"].value == "=C8761+D8761"

    assert ws["I2"].value == "=SUM(C2:C8761)"
    assert ws["I3"].value == "=SUM(D2:D8761)"
    assert ws["I4"].value == "=SUM(E2:E8761)"
    assert ws["I5"].value == "=I2/I3"
    assert ws["I6"].value == "=MAX(C2:C8761)"
    assert ws["I7"].value == "=INDEX(A2:A8761,MATCH(I6,C2:C8761,0))"
    assert ws["I8"].value == "=MAX(F2:F8761)"
    assert ws["I9"].value == "=INDEX(A2:A8761,MATCH(I8,F2:F8761,0))"
    assert ws["H5"].value == "Backup / heat pump kWh"


def test_readme_describes_population_and_scale() -> None:
    wb = builder.build_workbook(_inputs(_hourly()))
    text = " ".join(str(c.value) for c in wb["README"]["A"] if c.value)
    assert "3 ResStock res_test buildings" in text
    assert "0.990000" in text


def test_rejects_hourly_frames_that_do_not_match_jpv3() -> None:
    hourly = _hourly()
    with pytest.raises(ValueError, match="8760 hours"):
        builder.build_workbook(_inputs(hourly.head(10)))
    with pytest.raises(ValueError, match="missing columns"):
        builder.build_workbook(_inputs(hourly.drop("grid_kwh")))
    with pytest.raises(ValueError, match="sorted"):
        builder.build_workbook(_inputs(hourly.reverse()))
