"""
Test suite for the ny_aeba_savings heat pump cost savings model.

Validates the polars model against LibreOffice-recalculated Excel workbook
values. Tests run with BOTH default inputs AND perturbation inputs to ensure
the migration replicates Excel formulas, not just static point values.

The Model sheet column layout:
    E = Natural Gas Zone 4
    F = Natural Gas Zone 5
    G = Natural Gas Zone 6
    H = Propane Zone 4
    I = Propane Zone 5
    J = Propane Zone 6

Excel cell references are documented in each test for traceability.
"""

from __future__ import annotations

import subprocess
from typing import Any

import pytest

# model.py is added to sys.path at runtime by conftest.py, so ty cannot
# resolve it statically.  The ignore directive silences the false positive.
from model import (  # ty: ignore[unresolved-import]
    compute_baseline_costs,
    compute_building_geometry,
    compute_heat_loss_rates,
    compute_heat_pump_costs,
    compute_savings,
    compute_system_sizing,
    compute_weighted_averages,
    compute_yearly_btu,
    run_model,
)

# ---------------------------------------------------------------------------
# Constants: column layout for the 6 scenario columns (E through J)
# ---------------------------------------------------------------------------
COLUMNS = ["E", "F", "G", "H", "I", "J"]

# Scenario labels matching each column
SCENARIOS = [
    ("natural_gas", "4"),
    ("natural_gas", "5"),
    ("natural_gas", "6"),
    ("propane", "4"),
    ("propane", "5"),
    ("propane", "6"),
]

# Tolerance for numeric comparisons. rel=1e-4 means 0.01% relative tolerance.
REL_TOL = 1e-4


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _col_idx(col_letter: str) -> int:
    """Map column letter to 0-based index into the 6-column scenario layout."""
    return COLUMNS.index(col_letter)


def _read_row(wb, row: int, sheet: str = "Model") -> list[Any]:
    """Read values from all 6 scenario columns (E-J) for a given row."""
    return [wb.cell_value(f"{c}{row}", sheet=sheet) for c in COLUMNS]


# =========================================================================
# Smoke tests (existing, preserved from Step 2 scaffolding)
# =========================================================================


class TestSmoke:
    """Basic infrastructure tests -- these must pass before anything else."""

    def test_libreoffice_callable(self):
        """Verify that LibreOffice is installed and responds to --version."""
        result = subprocess.run(
            ["libreoffice", "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, f"libreoffice --version failed (rc={result.returncode}): {result.stderr}"
        output = result.stdout + result.stderr
        assert "LibreOffice" in output or "libreoffice" in output.lower(), (
            f"Unexpected output from libreoffice --version: {output}"
        )

    def test_workbook_recalculation(self, recalculated_workbook):
        """Verify the workbook can be recalculated; F40 is numeric."""
        value = recalculated_workbook.cell_value("F40", sheet="Model")
        assert value is not None, "Cell F40 is None after recalculation"
        assert isinstance(value, (int, float)), f"Expected numeric in F40, got {type(value).__name__}: {value}"

    def test_known_cell_value(self, recalculated_workbook):
        """Spot-check: total heat loss rate NatGas Zone 5 (F40) = 508.916."""
        value = recalculated_workbook.cell_value("F40", sheet="Model")
        assert value == pytest.approx(508.916, rel=REL_TOL), f"Expected F40 ~ 508.916 BTU/hr/degF, got {value}"


# =========================================================================
# 1. Building geometry (Model rows 10-24)
# =========================================================================


# Default inputs that define building geometry. These match the unmodified
# workbook. The perturbation changes floor area from 2363 to 2000.
_GEOM_DEFAULT_ID = "default"
_GEOM_PERTURBED_ID = "floor_area_2000"

_GEOM_PARAMS = [
    pytest.param(
        {},  # no modifications
        _GEOM_DEFAULT_ID,
        id=_GEOM_DEFAULT_ID,
    ),
    pytest.param(
        # Modify floor area in all 6 columns (Model E10:J10)
        {f"Model!{c}10": 2000 for c in COLUMNS},
        _GEOM_PERTURBED_ID,
        id=_GEOM_PERTURBED_ID,
    ),
]


class TestBuildingGeometry:
    """Building geometry: wall length, wall area, attic area, basement, volume.

    Excel rows: 10 (floor area), 11 (stories), 12 (wall length), 13 (wall
    height), 14 (total wall area), 15 (attic area), 16 (window %), 17 (walls
    excl windows), 18 (windows+doors), 19 (above-grade bsmt height), 20
    (below-grade bsmt height), 21 (above-grade bsmt walls area), 22
    (below-grade bsmt walls area), 23 (bsmt floor perimeter), 24 (volume).

    Geometry is identical across all 6 columns with default inputs because
    building design doesn't depend on fuel type or zone.
    """

    @pytest.mark.parametrize("modifications,param_id", _GEOM_PARAMS)
    def test_wall_length(self, recalculate, modifications, param_id):
        """Row 12: wall_length = sqrt(floor_area / stories)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 12)
        model_result = compute_building_geometry(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "wall_length_ft")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"wall_length [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _GEOM_PARAMS)
    def test_total_wall_area(self, recalculate, modifications, param_id):
        """Row 14: total wall surface area = 4 * wall_length * height * stories."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 14)
        model_result = compute_building_geometry(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "wall_surface_area_sf")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"wall_area [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _GEOM_PARAMS)
    def test_attic_area(self, recalculate, modifications, param_id):
        """Row 15: attic floor area = floor_area / stories."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 15)
        model_result = compute_building_geometry(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "attic_floor_area_sf")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"attic_area [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _GEOM_PARAMS)
    def test_walls_excl_windows(self, recalculate, modifications, param_id):
        """Row 17: wall area excluding windows = wall_area * (1 - window_pct)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 17)
        model_result = compute_building_geometry(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "wall_area_excl_windows_sf")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"walls_excl_windows [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _GEOM_PARAMS)
    def test_window_door_area(self, recalculate, modifications, param_id):
        """Row 18: window + door area = wall_area * window_pct."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 18)
        model_result = compute_building_geometry(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "window_door_area_sf")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"window_door_area [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _GEOM_PARAMS)
    def test_above_grade_basement_area(self, recalculate, modifications, param_id):
        """Row 21: above-grade basement wall area."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 21)
        model_result = compute_building_geometry(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "above_grade_basement_wall_area_sf")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"above_grade_bsmt [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _GEOM_PARAMS)
    def test_below_grade_basement_wall_area(self, recalculate, modifications, param_id):
        """Row 22: below-grade basement wall area."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 22)
        model_result = compute_building_geometry(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "below_grade_basement_wall_area_sf")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"below_grade_bsmt_wall [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _GEOM_PARAMS)
    def test_basement_floor_perimeter(self, recalculate, modifications, param_id):
        """Row 23: below-grade basement floor perimeter."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 23)
        model_result = compute_building_geometry(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "basement_floor_perimeter_ft")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"bsmt_perimeter [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _GEOM_PARAMS)
    def test_volume(self, recalculate, modifications, param_id):
        """Row 24: house cubic volume (including basement)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 24)
        model_result = compute_building_geometry(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "volume_cf")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"volume [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )


# =========================================================================
# 2. Heat loss rates (Model rows 27-40)
# =========================================================================


# Perturbation: change ACH50 for Zone 5 (F32) from 3.0 to 4.0
_HLOSS_DEFAULT_ID = "default"
_HLOSS_PERTURBED_ID = "ach50_zone5_4.0"

_HLOSS_PARAMS = [
    pytest.param({}, _HLOSS_DEFAULT_ID, id=_HLOSS_DEFAULT_ID),
    pytest.param(
        {"Model!F32": 4.0, "Model!I32": 4.0},
        _HLOSS_PERTURBED_ID,
        id=_HLOSS_PERTURBED_ID,
    ),
]


class TestHeatLossRates:
    """Heat loss rates per component and total (rows 33-40).

    Components:
      Row 33: attic
      Row 34: exterior walls
      Row 35: windows and doors
      Row 36: above-grade basement walls
      Row 37: air changes (depends on ACH50 -- differs Zone 6 vs 4/5)
      Row 38: below-grade basement walls
      Row 39: slab
      Row 40: total
    """

    @pytest.mark.parametrize("modifications,param_id", _HLOSS_PARAMS)
    def test_heat_loss_attic(self, recalculate, modifications, param_id):
        """Row 33: heat loss through attic = attic_area / R_attic."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 33)
        model_result = compute_heat_loss_rates(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "heat_loss_attic")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"attic [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HLOSS_PARAMS)
    def test_heat_loss_walls(self, recalculate, modifications, param_id):
        """Row 34: heat loss through exterior walls = wall_area_excl_windows / R_walls."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 34)
        model_result = compute_heat_loss_rates(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "heat_loss_walls")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"walls [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HLOSS_PARAMS)
    def test_heat_loss_windows(self, recalculate, modifications, param_id):
        """Row 35: heat loss through windows and doors."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 35)
        model_result = compute_heat_loss_rates(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "heat_loss_windows_doors")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"windows [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HLOSS_PARAMS)
    def test_heat_loss_above_grade_basement(self, recalculate, modifications, param_id):
        """Row 36: heat loss through above-grade basement walls."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 36)
        model_result = compute_heat_loss_rates(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "heat_loss_above_grade_basement")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"above_grade_bsmt [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HLOSS_PARAMS)
    def test_heat_loss_air_changes(self, recalculate, modifications, param_id):
        """Row 37: heat loss through air changes -- depends on ACH50 and volume."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 37)
        model_result = compute_heat_loss_rates(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "heat_loss_air_changes")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"air_changes [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HLOSS_PARAMS)
    def test_heat_loss_below_grade_basement(self, recalculate, modifications, param_id):
        """Row 38: heat loss through below-grade basement walls."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 38)
        model_result = compute_heat_loss_rates(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "heat_loss_below_grade_basement")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"below_grade_bsmt [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HLOSS_PARAMS)
    def test_heat_loss_slab(self, recalculate, modifications, param_id):
        """Row 39: heat loss through slab = perimeter * slab_f_factor."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 39)
        model_result = compute_heat_loss_rates(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "heat_loss_slab")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"slab [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HLOSS_PARAMS)
    def test_total_heat_loss_rate(self, recalculate, modifications, param_id):
        """Row 40: total heat loss rate = sum of all components.

        Default reference values:
            Zone 4/5 NatGas: 508.9155897 (F40)
            Zone 6 NatGas: 492.9653397 (G40)
        """
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 40)
        model_result = compute_heat_loss_rates(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "total_heat_loss_rate")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"total [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )


# =========================================================================
# 3. Yearly BTU (Model rows 43-46)
# =========================================================================


# Perturbation: change Zone 5 HDD from 6300 to 7000
_BTU_DEFAULT_ID = "default"
_BTU_PERTURBED_ID = "hdd_zone5_7000"

_BTU_PARAMS = [
    pytest.param({}, _BTU_DEFAULT_ID, id=_BTU_DEFAULT_ID),
    pytest.param(
        {"Model!F43": 7000, "Model!I43": 7000},
        _BTU_PERTURBED_ID,
        id=_BTU_PERTURBED_ID,
    ),
]


class TestYearlyBtu:
    """Yearly BTU demand: adjusted HDD and yearly BTU required.

    Row 43: Heating degree days (input)
    Row 44: EPA statewide adjustment (input)
    Row 45: Adjusted HDD = HDD - EPA adjustment
    Row 46: Yearly BTU = total_heat_loss_rate * adjusted_HDD * 24

    Default reference: NatGas Zone 5 yearly BTU = 72,575,434 (F46)
    """

    @pytest.mark.parametrize("modifications,param_id", _BTU_PARAMS)
    def test_adjusted_hdd(self, recalculate, modifications, param_id):
        """Row 45: adjusted HDD = HDD - EPA adjustment."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 45)
        model_result = compute_yearly_btu(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "adjusted_hdd")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"adjusted_hdd [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BTU_PARAMS)
    def test_yearly_btu(self, recalculate, modifications, param_id):
        """Row 46: yearly BTU required."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 46)
        model_result = compute_yearly_btu(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "yearly_btu")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"yearly_btu [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )


# =========================================================================
# 4. System sizing (Model rows 49-55)
# =========================================================================


_SIZING_DEFAULT_ID = "default"
_SIZING_PERTURBED_ID = "hdd_zone5_7000"

_SIZING_PARAMS = [
    pytest.param({}, _SIZING_DEFAULT_ID, id=_SIZING_DEFAULT_ID),
    pytest.param(
        # HDD change affects yearly BTU but not system sizing directly.
        # Instead, change floor area which affects volume and thus sizing.
        {f"Model!{c}10": 2800 for c in COLUMNS},
        "floor_area_2800",
        id="floor_area_2800",
    ),
]


class TestSystemSizing:
    """System sizing: coldest day temp, degree diff, BTU/hr, scaled capacity.

    Row 49: Coldest day design temp (weighted avg of county design temps)
    Row 50: Internal heat gains (constant)
    Row 51: Indoor design temp (constant)
    Row 52: Degree difference on coldest day
    Row 53: BTU/hr on coldest day
    Row 54: Sizing scale up factor (constant)
    Row 55: Heating system BTU estimate (scaled capacity)
    """

    @pytest.mark.parametrize("modifications,param_id", _SIZING_PARAMS)
    def test_coldest_day_temp(self, recalculate, modifications, param_id):
        """Row 49: weighted-average coldest day design temperature per zone."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 49)
        model_result = compute_system_sizing(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "coldest_day_temp_f")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"coldest_day [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SIZING_PARAMS)
    def test_degree_difference(self, recalculate, modifications, param_id):
        """Row 52: degree difference = design_temp - coldest_day - heat_gains/24/total_loss."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 52)
        model_result = compute_system_sizing(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "degree_diff_coldest_day")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"degree_diff [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SIZING_PARAMS)
    def test_btu_per_hr_coldest_day(self, recalculate, modifications, param_id):
        """Row 53: BTU/hr on coldest day = total_heat_loss_rate * degree_diff."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 53)
        model_result = compute_system_sizing(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "btu_hr_coldest_day")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"btu_hr [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SIZING_PARAMS)
    def test_system_capacity(self, recalculate, modifications, param_id):
        """Row 55: heating system BTU estimate = BTU/hr * scale_up_factor."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 55)
        model_result = compute_system_sizing(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "system_capacity_btu_hr")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"system_capacity [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )


# =========================================================================
# 5. Baseline costs (Model rows 59-96)
# =========================================================================


# Perturbation: change AFUE from 0.95 to 0.92
_BASELINE_DEFAULT_ID = "default"
_BASELINE_AFUE_ID = "afue_0.92"

_BASELINE_PARAMS = [
    pytest.param({}, _BASELINE_DEFAULT_ID, id=_BASELINE_DEFAULT_ID),
    pytest.param(
        {f"Model!{c}63": 0.92 for c in COLUMNS},
        _BASELINE_AFUE_ID,
        id=_BASELINE_AFUE_ID,
    ),
]

# Separate perturbation for fuel price tests
_BASELINE_FUELPRICE_ID = "natgas_price_plus20pct"

_BASELINE_FUELPRICE_PARAMS = [
    pytest.param({}, _BASELINE_DEFAULT_ID, id=_BASELINE_DEFAULT_ID),
    pytest.param(
        # Increase natural gas price by 20% in NatGas columns (E-G row 6)
        # Original: 15.2921875. New: 15.2921875 * 1.2 = 18.350625
        {
            "Model!E6": 15.2921875 * 1.2,
            "Model!F6": 15.2921875 * 1.2,
            "Model!G6": 15.2921875 * 1.2,
        },
        _BASELINE_FUELPRICE_ID,
        id=_BASELINE_FUELPRICE_ID,
    ),
]


class TestBaselineCosts:
    """Baseline (fossil fuel) system costs.

    Furnace (rows 59-71):
      59: Equipment cost
      61: Gas tank cost (0 for NatGas, 1400 for propane)
      62: Installed cost
      63: AFUE
      65: Yearly fuel usage
      66: Yearly fuel cost
      68: Yearly electrical usage
      69: Yearly electrical cost
      70: Yearly maintenance cost
      71: Yearly operating cost

    Central AC (rows 74-78):
      74: Equipment cost
      77: Yearly maintenance cost
      78: Yearly operating cost

    Gas Water Heater (rows 81-88):
      81: Equipment cost
      85: Yearly fuel usage
      86: Yearly fuel cost
      87: Yearly maintenance cost
      88: Yearly operating cost

    Infrastructure (row 91):
      91: Blended average service line cost (NatGas only, None for propane)

    Totals (rows 94-96):
      94: FF + AC + GWH equipment cost
      95: FF + AC + GWH + service line cost
      96: FF + AC + GWH yearly operating cost

    Default reference: NatGas Zone 5 yearly operating = $2,152.14 (F96)
    """

    # --- Furnace ---

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_furnace_equipment_cost(self, recalculate, modifications, param_id):
        """Row 59: furnace equipment cost (same across all scenarios)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 59)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "furnace_equipment_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"furnace_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_furnace_installed_cost(self, recalculate, modifications, param_id):
        """Row 62: installed cost = equipment + gas tank (propane only)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 62)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "furnace_installed_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"furnace_installed [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_furnace_yearly_fuel_usage(self, recalculate, modifications, param_id):
        """Row 65: yearly fuel usage = yearly_btu / (AFUE * energy_content)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 65)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "furnace_yearly_fuel_usage")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"fuel_usage [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_FUELPRICE_PARAMS)
    def test_furnace_yearly_fuel_cost(self, recalculate, modifications, param_id):
        """Row 66: yearly fuel cost = fuel_usage * fuel_price."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 66)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "furnace_yearly_fuel_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"fuel_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_furnace_yearly_electrical_cost(self, recalculate, modifications, param_id):
        """Row 69: yearly furnace electrical cost."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 69)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "furnace_yearly_electrical_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"elec_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_furnace_yearly_operating_cost(self, recalculate, modifications, param_id):
        """Row 71: yearly operating = fuel + electrical + maintenance."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 71)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "furnace_yearly_operating_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"furnace_operating [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    # --- Central AC ---

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_ac_equipment_cost(self, recalculate, modifications, param_id):
        """Row 74: AC equipment cost."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 74)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "ac_equipment_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"ac_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_ac_yearly_operating_cost(self, recalculate, modifications, param_id):
        """Row 78: AC yearly operating = maintenance only (cooling costs zeroed)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 78)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "ac_yearly_operating_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"ac_operating [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    # --- Gas Water Heater ---

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_gwh_equipment_cost(self, recalculate, modifications, param_id):
        """Row 81: gas water heater equipment cost."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 81)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "gwh_equipment_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"gwh_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_gwh_yearly_fuel_cost(self, recalculate, modifications, param_id):
        """Row 86: gas water heater yearly fuel cost."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 86)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "gwh_yearly_fuel_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"gwh_fuel_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_gwh_yearly_operating_cost(self, recalculate, modifications, param_id):
        """Row 88: gas water heater yearly operating = fuel + maintenance."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 88)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "gwh_yearly_operating_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"gwh_operating [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    # --- Service line costs ---

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_service_line_blended_avg(self, recalculate, modifications, param_id):
        """Row 91: blended average service line cost (NatGas zones only).

        Propane columns (H-J) should be None or 0 because there is no gas
        service line for propane heating.
        """
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 91)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "service_line_cost")
            excel_val = excel_vals[i]
            if fuel == "propane":
                # Propane has no service line. Excel shows None.
                assert model_val is None or model_val == 0 or model_val == pytest.approx(0, abs=1e-2), (
                    f"service_line [{fuel} Z{zone}]: expected 0/None, got {model_val} ({param_id})"
                )
            else:
                assert model_val == pytest.approx(excel_val, rel=REL_TOL), (
                    f"service_line [{fuel} Z{zone}]: model={model_val}, excel={excel_val} ({param_id})"
                )

    # --- Totals ---

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_baseline_equipment_total(self, recalculate, modifications, param_id):
        """Row 94: FF + AC + GWH equipment cost total."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 94)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "baseline_equipment_total")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"equip_total [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_baseline_equipment_with_service_line(self, recalculate, modifications, param_id):
        """Row 95: FF + AC + GWH + service line cost."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 95)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "baseline_equipment_with_service_line")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"equip+service [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _BASELINE_PARAMS)
    def test_baseline_yearly_operating(self, recalculate, modifications, param_id):
        """Row 96: FF + AC + GWH total yearly operating cost.

        Default reference: NatGas Zone 5 = $2,152.14
        """
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 96)
        model_result = compute_baseline_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "baseline_yearly_operating")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"yearly_operating [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )


# =========================================================================
# 6. Heat pump costs (Model rows 100-123)
# =========================================================================


# Perturbation: change HSPF2 from 10 to 9
_HP_DEFAULT_ID = "default"
_HP_HSPF2_ID = "hspf2_9"

_HP_PARAMS = [
    pytest.param({}, _HP_DEFAULT_ID, id=_HP_DEFAULT_ID),
    pytest.param(
        {f"Model!{c}105": 9 for c in COLUMNS},
        _HP_HSPF2_ID,
        id=_HP_HSPF2_ID,
    ),
]


class TestHeatPumpCosts:
    """Heat pump system costs.

    ccASHP (rows 100-109):
      100: Equipment cost (zone-dependent)
      101: Clean Heat rebate (blended avg by zone -- currently $0)
      102: Federal tax credit (currently $0)
      103: Net equipment cost
      105: HSPF2
      106: Yearly kWh needed
      107: Yearly electrical cost
      108: Yearly maintenance cost
      109: Yearly operating cost

    HPWH (rows 112-120):
      112: Device cost
      113: Clean Heat rebate (blended avg by zone)
      114: Net device cost
      116: Fuel efficiency (kWh/day)
      117: Yearly electrical usage (kWh)
      118: Yearly electrical cost
      119: Yearly maintenance cost
      120: Total yearly spend

    Totals (rows 122-123):
      122: ASHP + HPWH equipment costs
      123: ASHP + HPWH yearly operating costs

    Default reference: NatGas Zone 5 HP yearly operating = $2,345.96 (F123)
    """

    # --- ccASHP ---

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_ccashp_equipment_cost(self, recalculate, modifications, param_id):
        """Row 100: ccASHP equipment cost (zone-dependent sizing)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 100)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "ccashp_equipment_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"ccashp_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_ccashp_rebate(self, recalculate, modifications, param_id):
        """Row 101: Clean Heat rebate (blended avg -- currently $0 for ccASHP)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 101)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "ccashp_rebate")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"ccashp_rebate [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_ccashp_net_cost(self, recalculate, modifications, param_id):
        """Row 103: net ccASHP cost = equipment - rebate - tax_credit."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 103)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "ccashp_net_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"ccashp_net [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_ccashp_yearly_kwh(self, recalculate, modifications, param_id):
        """Row 106: yearly kWh = yearly_btu / (HSPF2 * 1000/3412)... i.e., yearly_btu / (HSPF2 * Wh/BTU * 1000)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 106)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "ccashp_yearly_kwh")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"ccashp_kwh [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_ccashp_yearly_electrical_cost(self, recalculate, modifications, param_id):
        """Row 107: yearly electrical cost = yearly_kwh * electricity_price."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 107)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "ccashp_yearly_electrical_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"ccashp_elec_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_ccashp_yearly_operating_cost(self, recalculate, modifications, param_id):
        """Row 109: ccASHP yearly operating = electrical + maintenance."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 109)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "ccashp_yearly_operating_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"ccashp_operating [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    # --- HPWH ---

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_hpwh_device_cost(self, recalculate, modifications, param_id):
        """Row 112: HPWH device cost."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 112)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "hpwh_device_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"hpwh_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_hpwh_rebate(self, recalculate, modifications, param_id):
        """Row 113: HPWH Clean Heat rebate (blended avg by zone)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 113)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "hpwh_rebate")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"hpwh_rebate [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_hpwh_net_cost(self, recalculate, modifications, param_id):
        """Row 114: HPWH net cost = device - rebate."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 114)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "hpwh_net_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"hpwh_net [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_hpwh_yearly_electrical_cost(self, recalculate, modifications, param_id):
        """Row 118: HPWH yearly electrical cost."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 118)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "hpwh_yearly_electrical_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"hpwh_elec_cost [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_hpwh_yearly_operating_cost(self, recalculate, modifications, param_id):
        """Row 120: HPWH total yearly spend = electrical + maintenance."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 120)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "hpwh_yearly_operating_cost")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"hpwh_operating [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    # --- HP Totals ---

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_hp_equipment_total(self, recalculate, modifications, param_id):
        """Row 122: ASHP + HPWH equipment costs total."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 122)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "hp_equipment_total")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"hp_equip_total [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _HP_PARAMS)
    def test_hp_yearly_operating_total(self, recalculate, modifications, param_id):
        """Row 123: ASHP + HPWH yearly operating costs total.

        Default reference: NatGas Zone 5 = $2,345.96
        """
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 123)
        model_result = compute_heat_pump_costs(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "hp_yearly_operating_total")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"hp_yearly_operating [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )


# =========================================================================
# 7. Savings comparison (Model rows 126-134)
# =========================================================================


# Perturbation: change mortgage rate from 6.38% to 7.5%
_SAVINGS_DEFAULT_ID = "default"
_SAVINGS_MORTGAGE_ID = "mortgage_7.5pct"

_SAVINGS_PARAMS = [
    pytest.param({}, _SAVINGS_DEFAULT_ID, id=_SAVINGS_DEFAULT_ID),
    pytest.param(
        {f"Model!{c}126": 0.075 for c in COLUMNS},
        _SAVINGS_MORTGAGE_ID,
        id=_SAVINGS_MORTGAGE_ID,
    ),
]


class TestSavings:
    """Savings comparison: construction, mortgage, operating, total, PV.

    Row 126: Mortgage rate (input)
    Row 127: Construction cost savings (without service lines)
    Row 128: Construction cost savings (with service lines)
    Row 129: Mortgage savings (without service lines)
    Row 130: Mortgage savings (with service lines)
    Row 131: Yearly operating cost savings
    Row 132: Total yearly savings (without service lines)
    Row 133: Total yearly savings (with service lines)
    Row 134: 15-year present value @ 4% discount

    Default references (NatGas Zone 5):
      Total yearly savings (with service lines): $133.57 (F133)
      15yr PV: $1,485.04 (F134)

    Default references (Propane Zone 5):
      Total yearly savings: $2,637.82 (I133)
      15yr PV: $29,328.29 (I134)
    """

    @pytest.mark.parametrize("modifications,param_id", _SAVINGS_PARAMS)
    def test_construction_savings_no_service_line(self, recalculate, modifications, param_id):
        """Row 127: construction savings = baseline_equip - hp_equip (no service line)."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 127)
        model_result = compute_savings(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "construction_savings")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"constr_savings [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SAVINGS_PARAMS)
    def test_construction_savings_with_service_line(self, recalculate, modifications, param_id):
        """Row 128: construction savings with service line costs included."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 128)
        model_result = compute_savings(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "construction_savings_with_service_line")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"constr_savings_sl [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SAVINGS_PARAMS)
    def test_mortgage_savings_no_service_line(self, recalculate, modifications, param_id):
        """Row 129: mortgage savings (no service line) via PMT formula."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 129)
        model_result = compute_savings(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "mortgage_savings")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"mortgage_savings [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SAVINGS_PARAMS)
    def test_mortgage_savings_with_service_line(self, recalculate, modifications, param_id):
        """Row 130: mortgage savings (with service line) via PMT formula."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 130)
        model_result = compute_savings(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "mortgage_savings_with_service_line")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"mortgage_savings_sl [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SAVINGS_PARAMS)
    def test_operating_savings(self, recalculate, modifications, param_id):
        """Row 131: yearly operating cost savings = baseline_op - hp_op."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 131)
        model_result = compute_savings(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "operating_savings")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"op_savings [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SAVINGS_PARAMS)
    def test_total_yearly_savings_no_service_line(self, recalculate, modifications, param_id):
        """Row 132: total yearly savings = mortgage_savings + operating_savings."""
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 132)
        model_result = compute_savings(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "total_yearly_savings")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"total_savings [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SAVINGS_PARAMS)
    def test_total_yearly_savings_with_service_line(self, recalculate, modifications, param_id):
        """Row 133: total yearly savings (with service line).

        Default reference (NatGas Zone 5): $133.57
        Default reference (Propane Zone 5): $2,637.82
        """
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 133)
        model_result = compute_savings(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "total_yearly_savings_with_service_line")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"total_savings_sl [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )

    @pytest.mark.parametrize("modifications,param_id", _SAVINGS_PARAMS)
    def test_present_value_15yr(self, recalculate, modifications, param_id):
        """Row 134: 15-year present value at 4% discount rate.

        Default reference (NatGas Zone 5): $1,485.04
        Default reference (Propane Zone 5): $29,328.29
        """
        wb = recalculate(modifications)
        excel_vals = _read_row(wb, 134)
        model_result = compute_savings(_build_scenarios(modifications))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "present_value_15yr")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"pv_15yr [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]} ({param_id})"
            )


# =========================================================================
# 8. Weighted averages (Model rows 137-149)
# =========================================================================


class TestWeightedAverages:
    """Weighted statewide and zonewide savings (rows 137-149).

    Weighting uses survey data (heating system type counts) and county-level
    new construction shares.

    Row 137: New construction projects using fuel (survey counts)
    Row 138: Total fossil fuel survey responses
    Row 139: Percent of fossil fuel in this zone using this fuel type
    Row 140: Percent of new construction in each zone
    Row 141: Percent of new construction in zone using this fuel type

    Savings figures (rows 144-149):
    Row 144: Weighted statewide yearly savings by fuel type (E, H only)
    Row 146: Weighted zonewide yearly savings (E, F, G only)
    Row 148: Weighted statewide yearly savings overall (E only)
    Row 149: 15 year PV (E only)

    These are aggregate figures; the default-only test is sufficient because
    the weighting factors come from external survey data, not model inputs
    that we'd perturb.
    """

    def test_survey_counts(self, recalculate):
        """Row 137: survey counts for each fuel-zone combination.

        NatGas counts: 25 (Zone 4), 259 (Zone 5), 27 (Zone 6)
        Propane counts: 2 (Zone 4), 72 (Zone 5), 55 (Zone 6)
        """
        wb = recalculate()
        excel_vals = _read_row(wb, 137)
        model_result = compute_weighted_averages(_build_scenarios({}))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "survey_count")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"survey_count [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_total_ff_survey_responses(self, recalculate):
        """Row 138: total fossil fuel survey responses per zone.

        Zone 4: 27, Zone 5: 331, Zone 6: 82
        """
        wb = recalculate()
        excel_vals = _read_row(wb, 138)
        model_result = compute_weighted_averages(_build_scenarios({}))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "total_ff_survey_responses")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"total_ff [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_pct_ff_using_fuel(self, recalculate):
        """Row 139: percent of fossil fuel using this fuel type."""
        wb = recalculate()
        excel_vals = _read_row(wb, 139)
        model_result = compute_weighted_averages(_build_scenarios({}))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "pct_ff_using_fuel")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"pct_ff [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_pct_new_construction_in_zone(self, recalculate):
        """Row 140: percent of new construction in each zone."""
        wb = recalculate()
        excel_vals = _read_row(wb, 140)
        model_result = compute_weighted_averages(_build_scenarios({}))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "pct_new_construction_in_zone")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"pct_new_constr [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_pct_new_construction_fuel_zone(self, recalculate):
        """Row 141: percent of new construction in zone using this fuel."""
        wb = recalculate()
        excel_vals = _read_row(wb, 141)
        model_result = compute_weighted_averages(_build_scenarios({}))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "pct_new_construction_fuel_zone")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"pct_fuel_zone [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_weighted_statewide_savings_by_fuel(self, recalculate):
        """Row 144: weighted statewide yearly savings by fuel type.

        Only columns E (NatGas) and H (Propane) have values.
        E144 = $330.35, H144 = $2,653.76
        """
        wb = recalculate()
        natgas_val = wb.cell_value("E144", sheet="Model")
        propane_val = wb.cell_value("H144", sheet="Model")

        model_result = compute_weighted_averages(_build_scenarios({}))

        model_natgas = _get_weighted_avg_value(model_result, "natural_gas", "weighted_statewide_savings_by_fuel")
        model_propane = _get_weighted_avg_value(model_result, "propane", "weighted_statewide_savings_by_fuel")

        assert model_natgas == pytest.approx(natgas_val, rel=REL_TOL), (
            f"NatGas statewide savings: model={model_natgas}, excel={natgas_val}"
        )
        assert model_propane == pytest.approx(propane_val, rel=REL_TOL), (
            f"Propane statewide savings: model={model_propane}, excel={propane_val}"
        )

    def test_weighted_zonewide_savings(self, recalculate):
        """Row 146: weighted zonewide yearly savings (both fuels combined).

        Only columns E (Zone 4), F (Zone 5), G (Zone 6) have values.
        E146 = $1,031.70, F146 = $678.30, G146 = $2,051.28
        """
        wb = recalculate()
        zone4_val = wb.cell_value("E146", sheet="Model")
        zone5_val = wb.cell_value("F146", sheet="Model")
        zone6_val = wb.cell_value("G146", sheet="Model")

        model_result = compute_weighted_averages(_build_scenarios({}))

        model_z4 = _get_weighted_avg_value(model_result, "4", "weighted_zonewide_savings")
        model_z5 = _get_weighted_avg_value(model_result, "5", "weighted_zonewide_savings")
        model_z6 = _get_weighted_avg_value(model_result, "6", "weighted_zonewide_savings")

        assert model_z4 == pytest.approx(zone4_val, rel=REL_TOL), f"Zone 4 savings: model={model_z4}, excel={zone4_val}"
        assert model_z5 == pytest.approx(zone5_val, rel=REL_TOL), f"Zone 5 savings: model={model_z5}, excel={zone5_val}"
        assert model_z6 == pytest.approx(zone6_val, rel=REL_TOL), f"Zone 6 savings: model={model_z6}, excel={zone6_val}"

    def test_weighted_statewide_overall_savings(self, recalculate):
        """Row 148: weighted overall statewide yearly savings.

        Only E148 has a value: $1,083.59
        """
        wb = recalculate()
        excel_val = wb.cell_value("E148", sheet="Model")

        model_result = compute_weighted_averages(_build_scenarios({}))
        model_val = _get_weighted_avg_value(model_result, "overall", "weighted_statewide_savings")

        assert model_val == pytest.approx(excel_val, rel=REL_TOL), (
            f"Overall statewide savings: model={model_val}, excel={excel_val}"
        )

    def test_weighted_statewide_pv(self, recalculate):
        """Row 149: 15-year PV at 4% discount.

        Only E149 has a value: $12,047.82
        """
        wb = recalculate()
        excel_val = wb.cell_value("E149", sheet="Model")

        model_result = compute_weighted_averages(_build_scenarios({}))
        model_val = _get_weighted_avg_value(model_result, "overall", "weighted_statewide_pv")

        assert model_val == pytest.approx(excel_val, rel=REL_TOL), (
            f"Overall statewide PV: model={model_val}, excel={excel_val}"
        )


# =========================================================================
# 9. End-to-end run_model() integration test
# =========================================================================


class TestRunModel:
    """Integration test: run_model() produces the full result table."""

    def test_run_model_returns_dataframe(self):
        """run_model() returns a polars DataFrame with the expected shape."""
        import polars as pl

        result = run_model()
        assert isinstance(result, pl.DataFrame), f"Expected pl.DataFrame, got {type(result)}"
        # 12 rows: 3 zones x 2 fuels x 2 technologies (ccASHP + GSHP)
        assert len(result) == 12, f"Expected 12 rows, got {len(result)}"
        # 6 ccASHP rows and 6 GSHP rows
        assert len(result.filter(pl.col("hp_technology") == "ccASHP")) == 6
        assert len(result.filter(pl.col("hp_technology") == "GSHP")) == 6

    def test_run_model_spot_check_natgas_zone5(self, recalculate):
        """Spot-check: NatGas Zone 5 ccASHP values from run_model() vs Excel."""
        wb = recalculate()
        result = run_model()

        # Filter to NatGas Zone 5 ccASHP (the Excel-validated technology)
        row = result.filter(
            (result["fuel"] == "natural_gas") & (result["zone"] == "5") & (result["hp_technology"] == "ccASHP")
        )
        assert len(row) == 1, f"Expected 1 row for NatGas Zone 5 ccASHP, got {len(row)}"

        # Check key reference values from the project plan
        checks = {
            "total_heat_loss_rate": wb.cell_value("F40"),
            "yearly_btu": wb.cell_value("F46"),
            "baseline_yearly_operating": wb.cell_value("F96"),
            "hp_yearly_operating_total": wb.cell_value("F123"),
            "total_yearly_savings_with_service_line": wb.cell_value("F133"),
            "present_value_15yr": wb.cell_value("F134"),
        }

        for col_name, excel_val in checks.items():
            model_val = row[col_name][0]
            assert model_val == pytest.approx(excel_val, rel=REL_TOL), (
                f"NatGas Z5 {col_name}: model={model_val}, excel={excel_val}"
            )

    def test_run_model_spot_check_propane_zone5(self, recalculate):
        """Spot-check: Propane Zone 5 ccASHP values from run_model() vs Excel."""
        wb = recalculate()
        result = run_model()

        row = result.filter(
            (result["fuel"] == "propane") & (result["zone"] == "5") & (result["hp_technology"] == "ccASHP")
        )
        assert len(row) == 1, f"Expected 1 row for Propane Zone 5 ccASHP, got {len(row)}"

        checks = {
            "baseline_yearly_operating": wb.cell_value("I96"),
            "hp_yearly_operating_total": wb.cell_value("I123"),
            "total_yearly_savings_with_service_line": wb.cell_value("I133"),
            "present_value_15yr": wb.cell_value("I134"),
        }

        for col_name, excel_val in checks.items():
            model_val = row[col_name][0]
            assert model_val == pytest.approx(excel_val, rel=REL_TOL), (
                f"Propane Z5 {col_name}: model={model_val}, excel={excel_val}"
            )


# =========================================================================
# 10. End-to-end integration test with ALL perturbations applied at once
# =========================================================================

# Combine one perturbation from each computation stage so that every link
# in the pipeline is exercised with non-default values simultaneously.
_ALL_PERTURBATIONS: dict[str, Any] = {
    # Stage 2 - building geometry: floor area 2363 -> 2000
    **{f"Model!{c}10": 2000 for c in COLUMNS},
    # Stage 3 - heat loss rates: ACH50 Zone 5 from 3.0 -> 4.0
    "Model!F32": 4.0,
    "Model!I32": 4.0,
    # Stage 4 - yearly BTU: HDD Zone 5 from 6300 -> 7000
    "Model!F43": 7000,
    "Model!I43": 7000,
    # Stage 6 - baseline costs: furnace AFUE 0.95 -> 0.92
    **{f"Model!{c}63": 0.92 for c in COLUMNS},
    # Stage 6 - baseline costs: natural gas price +20%
    "Model!E6": 15.2921875 * 1.2,
    "Model!F6": 15.2921875 * 1.2,
    "Model!G6": 15.2921875 * 1.2,
    # Stage 7 - heat pump costs: ccASHP HSPF2 10 -> 9
    **{f"Model!{c}105": 9 for c in COLUMNS},
    # Stage 8 - savings: mortgage rate 6.38% -> 7.5%
    **{f"Model!{c}126": 0.075 for c in COLUMNS},
}


class TestEndToEndPerturbed:
    """Integration test: perturb ALL stages at once, check final savings.

    Each unit test class perturbs one input at a time. This test applies
    every perturbation simultaneously so that errors in how intermediate
    values compose (e.g., a perturbed floor area feeding into heat loss
    feeding into yearly BTU feeding into sizing feeding into costs) are
    caught even if each stage passes individually.
    """

    def test_total_yearly_savings_with_service_line(self, recalculate):
        """Row 133: total yearly savings (with service line), all perturbations."""
        wb = recalculate(_ALL_PERTURBATIONS)
        excel_vals = _read_row(wb, 133)
        model_result = compute_savings(_build_scenarios(_ALL_PERTURBATIONS))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "total_yearly_savings_with_service_line")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"total_savings_sl [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_present_value_15yr(self, recalculate):
        """Row 134: 15-year present value, all perturbations."""
        wb = recalculate(_ALL_PERTURBATIONS)
        excel_vals = _read_row(wb, 134)
        model_result = compute_savings(_build_scenarios(_ALL_PERTURBATIONS))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "present_value_15yr")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"pv_15yr [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_baseline_yearly_operating(self, recalculate):
        """Row 96: baseline operating cost, all perturbations."""
        wb = recalculate(_ALL_PERTURBATIONS)
        excel_vals = _read_row(wb, 96)
        model_result = compute_savings(_build_scenarios(_ALL_PERTURBATIONS))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "baseline_yearly_operating")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"baseline_op [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_hp_yearly_operating_total(self, recalculate):
        """Row 123: heat pump operating cost, all perturbations."""
        wb = recalculate(_ALL_PERTURBATIONS)
        excel_vals = _read_row(wb, 123)
        model_result = compute_savings(_build_scenarios(_ALL_PERTURBATIONS))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "hp_yearly_operating_total")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"hp_op [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_construction_savings_with_service_line(self, recalculate):
        """Row 128: construction savings with service line, all perturbations."""
        wb = recalculate(_ALL_PERTURBATIONS)
        excel_vals = _read_row(wb, 128)
        model_result = compute_savings(_build_scenarios(_ALL_PERTURBATIONS))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "construction_savings_with_service_line")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"constr_savings_sl [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )

    def test_mortgage_savings_with_service_line(self, recalculate):
        """Row 130: mortgage savings with service line, all perturbations."""
        wb = recalculate(_ALL_PERTURBATIONS)
        excel_vals = _read_row(wb, 130)
        model_result = compute_savings(_build_scenarios(_ALL_PERTURBATIONS))

        for i, (fuel, zone) in enumerate(SCENARIOS):
            model_val = _get_scenario_value(model_result, fuel, zone, "mortgage_savings_with_service_line")
            assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL), (
                f"mortgage_savings_sl [{fuel} Z{zone}]: model={model_val}, excel={excel_vals[i]}"
            )


# =========================================================================
# 11. GSHP-specific tests (no Excel reference — validated analytically)
# =========================================================================


class TestGSHPScenarios:
    """Tests for GSHP scenarios added in R2-91.

    GSHP calculations are validated analytically (not against Excel) since
    the Excel workbook only contains ccASHP scenarios.

    Key GSHP parameters:
      - Equipment cost: $43,500 (horizontal loop installed)
      - COP: 3.6 (ENERGY STAR minimum, closed-loop water-to-air)
      - NY State geo tax credit: 25% of cost, capped at $10,000
      - Federal 25D credit: 30% of cost, no cap
      - Clean Heat rebate: blended by zone (new construction)
    """

    def test_gshp_scenario_count(self):
        """12-row table: 6 ccASHP + 6 GSHP."""
        import polars as pl

        result = compute_savings()
        assert len(result) == 12
        assert len(result.filter(pl.col("hp_technology") == "GSHP")) == 6
        assert len(result.filter(pl.col("hp_technology") == "ccASHP")) == 6

    def test_gshp_equipment_cost(self):
        """GSHP equipment cost = $50,000 for all scenarios."""
        result = compute_heat_pump_costs()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                val = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_equipment_cost")
                assert val == pytest.approx(50000.0, rel=1e-6), (
                    f"gshp_equipment_cost [{fuel} Z{zone}]: got {val}, expected 50000"
                )

    def test_gshp_energy_calculation(self):
        """GSHP yearly kWh = yearly_btu / (COP * 3412).

        COP = 3.6, so factor = 3.6 * 3412 = 12283.2 BTU/kWh.
        """
        result = compute_heat_pump_costs()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                yearly_btu = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "yearly_btu")
                gshp_kwh = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_yearly_kwh")
                expected_kwh = yearly_btu / (3.6 * 3412)
                assert gshp_kwh == pytest.approx(expected_kwh, rel=1e-6), (
                    f"gshp_kwh [{fuel} Z{zone}]: got {gshp_kwh}, expected {expected_kwh}"
                )

    def test_gshp_ny_state_tax_credit(self):
        """NY geo credit: 25% of $50,000 = $12,500, capped at $10,000."""
        result = compute_heat_pump_costs()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                ny_credit = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_ny_tax_credit")
                # 25% of 50000 = 12500, cap = 10000
                assert ny_credit == pytest.approx(10000.0, rel=1e-6), (
                    f"gshp_ny_credit [{fuel} Z{zone}]: got {ny_credit}, expected 10000"
                )

    def test_gshp_federal_25d_credit(self):
        """Federal 25D: 30% of $50,000 = $15,000, no cap."""
        result = compute_heat_pump_costs()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                fed_credit = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_federal_tax_credit")
                expected = 50000.0 * 0.30
                assert fed_credit == pytest.approx(expected, rel=1e-6), (
                    f"gshp_fed_credit [{fuel} Z{zone}]: got {fed_credit}, expected {expected}"
                )

    def test_gshp_net_cost_formula(self):
        """Net cost = max(0, equipment - rebate - ny_credit - fed_credit)."""
        result = compute_heat_pump_costs()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                equip = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_equipment_cost")
                rebate = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_rebate")
                ny = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_ny_tax_credit")
                fed = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_federal_tax_credit")
                net = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_net_cost")
                expected = max(0.0, equip - rebate - ny - fed)
                assert net == pytest.approx(expected, rel=1e-6), (
                    f"gshp_net [{fuel} Z{zone}]: got {net}, expected {expected}"
                )

    def test_gshp_rebate_positive(self):
        """GSHP rebate should be positive for all zones (all utilities offer it)."""
        result = compute_heat_pump_costs()
        for zone in ["4", "5", "6"]:
            rebate = _get_scenario_value_by_tech(result, "natural_gas", zone, "GSHP", "gshp_rebate")
            assert rebate > 0, f"gshp_rebate Zone {zone}: expected > 0, got {rebate}"

    def test_gshp_hp_totals_include_hpwh(self):
        """hp_equipment_total for GSHP = gshp_net_cost + hpwh_net_cost."""
        result = compute_heat_pump_costs()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                gshp_net = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_net_cost")
                hpwh_net = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "hpwh_net_cost")
                total = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "hp_equipment_total")
                assert total == pytest.approx(gshp_net + hpwh_net, rel=1e-6), (
                    f"hp_total [{fuel} Z{zone}]: got {total}, expected {gshp_net + hpwh_net}"
                )

    def test_gshp_yearly_operating_includes_hpwh(self):
        """hp_yearly_operating_total for GSHP = gshp_operating + hpwh_operating."""
        result = compute_heat_pump_costs()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                gshp_op = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "gshp_yearly_operating_cost")
                hpwh_op = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "hpwh_yearly_operating_cost")
                total = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "hp_yearly_operating_total")
                assert total == pytest.approx(gshp_op + hpwh_op, rel=1e-6), (
                    f"hp_op_total [{fuel} Z{zone}]: got {total}, expected {gshp_op + hpwh_op}"
                )

    def test_ccashp_values_zero_on_gshp_rows(self):
        """On GSHP rows, ccASHP-specific columns should be 0."""
        result = compute_heat_pump_costs()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                for col in ["ccashp_equipment_cost", "ccashp_net_cost", "ccashp_yearly_kwh"]:
                    val = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", col)
                    assert val == pytest.approx(0.0, abs=1e-6), (
                        f"{col} on GSHP row [{fuel} Z{zone}]: expected 0, got {val}"
                    )

    def test_gshp_values_zero_on_ccashp_rows(self):
        """On ccASHP rows, GSHP-specific columns should be 0."""
        result = compute_heat_pump_costs()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                for col in ["gshp_equipment_cost", "gshp_net_cost", "gshp_yearly_kwh"]:
                    val = _get_scenario_value_by_tech(result, fuel, zone, "ccASHP", col)
                    assert val == pytest.approx(0.0, abs=1e-6), (
                        f"{col} on ccASHP row [{fuel} Z{zone}]: expected 0, got {val}"
                    )

    def test_gshp_savings_present_value(self):
        """GSHP savings PV should be finite and real for all scenarios."""
        result = compute_savings()
        for fuel in ["natural_gas", "propane"]:
            for zone in ["4", "5", "6"]:
                pv = _get_scenario_value_by_tech(result, fuel, zone, "GSHP", "present_value_15yr")
                assert pv is not None
                assert pv == pv  # not NaN

    def test_ccashp_unchanged_by_gshp_addition(self):
        """ccASHP total yearly savings unchanged from known values.

        Reference values from the passing Excel tests (default inputs):
          NatGas Zone 5: $133.57 (F133)
          Propane Zone 5: $2,637.82 (I133)
        """
        result = compute_savings()
        natgas_z5 = _get_scenario_value_by_tech(
            result, "natural_gas", "5", "ccASHP", "total_yearly_savings_with_service_line"
        )
        propane_z5 = _get_scenario_value_by_tech(
            result, "propane", "5", "ccASHP", "total_yearly_savings_with_service_line"
        )
        assert natgas_z5 == pytest.approx(133.57, rel=0.01), f"NatGas Z5 ccASHP savings: {natgas_z5}"
        assert propane_z5 == pytest.approx(2637.82, rel=0.01), f"Propane Z5 ccASHP savings: {propane_z5}"

    def test_tidy_results_row_count(self):
        """Tidy results should have 24 rows: 12 per technology."""
        from model import build_tidy_results  # ty: ignore[unresolved-import]

        tidy = build_tidy_results(compute_savings())
        assert len(tidy) == 24, f"Expected 24 tidy rows, got {len(tidy)}"

    def test_tidy_results_has_gshp(self):
        """Tidy results should include GSHP rows."""
        import polars as pl
        from model import build_tidy_results  # ty: ignore[unresolved-import]

        tidy = build_tidy_results(compute_savings())
        gshp_rows = tidy.filter(pl.col("hp_tech") == "GSHP")
        assert len(gshp_rows) == 12, f"Expected 12 GSHP tidy rows, got {len(gshp_rows)}"


# =========================================================================
# Adapter helpers — translate between Excel cell references and model API.
# =========================================================================


def _build_scenarios(modifications: dict[str, Any]):
    """Build the scenario input structure, optionally overriding parameters.

    The modifications dict uses Excel-style cell references as keys. This
    helper translates those into the parameter overrides that the model
    functions expect.

    This is a thin adapter between Excel cell references used in tests and
    the model's Python API. It will be fully implemented once model.py
    defines its input contract.
    """
    # Map Excel cell modifications to model parameter overrides.
    # The model functions will accept an optional 'overrides' dict.
    overrides = {}

    for key, value in modifications.items():
        if "!" in key:
            _sheet, cell_ref = key.split("!", 1)
        else:
            cell_ref = key

        # Extract column letter and row number from cell reference
        col = ""
        row_str = ""
        for ch in cell_ref:
            if ch.isalpha():
                col += ch
            else:
                row_str += ch
        row = int(row_str)

        # Map column to scenario index
        if col in COLUMNS:
            scenario_idx = _col_idx(col)
            fuel, zone = SCENARIOS[scenario_idx]
        else:
            # Non-scenario column -- skip or store separately
            continue

        # Map row number to parameter name
        param_name = _ROW_TO_PARAM.get(row)
        if param_name is None:
            continue

        if (fuel, zone) not in overrides:
            overrides[(fuel, zone)] = {}
        overrides[(fuel, zone)][param_name] = value

    return overrides if overrides else None


# Mapping of Model sheet row numbers to parameter names used by the model.
# Only rows that represent modifiable inputs (not computed values) are listed.
_ROW_TO_PARAM: dict[int, str] = {
    5: "electricity_price",
    6: "fuel_price",
    10: "floor_area_sf",
    11: "stories",
    13: "wall_height_ft",
    16: "window_door_pct",
    19: "above_grade_basement_wall_height_ft",
    20: "below_grade_basement_wall_height_ft",
    27: "r_attic",
    28: "r_walls",
    29: "r_windows_doors",
    30: "r_basement_wall",
    31: "slab_f_factor",
    32: "ach50",
    43: "hdd",
    44: "epa_hdd_adjustment",
    50: "internal_heat_gains_btu",
    51: "indoor_design_temp_f",
    54: "sizing_scale_up_factor",
    63: "furnace_afue",
    67: "furnace_electrical_usage_kwh_per_mmbtu",
    70: "furnace_maintenance_cost",
    83: "gwh_fuel_usage_rate",
    84: "gwh_daily_operating_hours",
    105: "ccashp_hspf2",
    116: "hpwh_daily_kwh",
    126: "mortgage_rate",
}


def _get_scenario_value(model_result, fuel: str, zone: str, column: str):
    """Extract a value from the model result for a specific scenario.

    The model returns a polars DataFrame with columns 'fuel', 'zone', and
    various computed value columns. This helper filters and extracts.
    """
    import polars as pl

    if isinstance(model_result, pl.DataFrame):
        row = model_result.filter((model_result["fuel"] == fuel) & (model_result["zone"] == zone))
        if len(row) == 0:
            raise ValueError(f"No row found for fuel={fuel}, zone={zone} in model result")
        return row[column][0]
    elif isinstance(model_result, dict):
        # Fallback for dict-based returns
        return model_result.get((fuel, zone), {}).get(column)
    else:
        raise TypeError(f"Unexpected model result type: {type(model_result)}")


def _get_scenario_value_by_tech(model_result, fuel: str, zone: str, hp_technology: str, column: str):
    """Extract a value from the model result for a specific scenario and technology."""

    row = model_result.filter(
        (model_result["fuel"] == fuel)
        & (model_result["zone"] == zone)
        & (model_result["hp_technology"] == hp_technology)
    )
    if len(row) == 0:
        raise ValueError(f"No row found for fuel={fuel}, zone={zone}, hp_technology={hp_technology}")
    return row[column][0]


def _get_weighted_avg_value(model_result, key: str, column: str):
    """Extract a weighted average value from the model result.

    For weighted averages, the model may return a separate structure:
      - By fuel type: key is "natural_gas" or "propane"
      - By zone: key is "4", "5", or "6"
      - Overall: key is "overall"
    """
    import polars as pl

    if isinstance(model_result, pl.DataFrame):
        row = model_result.filter(model_result["key"] == key)
        if len(row) == 0:
            raise ValueError(f"No row found for key={key} in weighted averages result")
        return row[column][0]
    elif isinstance(model_result, dict):
        return model_result.get(key, {}).get(column)
    else:
        raise TypeError(f"Unexpected model result type: {type(model_result)}")
