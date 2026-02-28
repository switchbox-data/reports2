# Test Suite Review Guide

## Overview

The test suite validates `model.py` against the source Excel workbook by
recalculating the workbook with LibreOffice in headless mode and comparing cell
values. Tests use both default inputs and perturbed inputs to ensure the Python
model replicates the Excel formulas, not just memorized point values.

139 tests across 11 test classes. Runs in ~2 minutes (dominated by LibreOffice
recalculation time).

## Architecture

```text
tests/
  conftest.py          # LibreOffice recalculation harness + fixtures
  test_ny_aeba_model.py  # All tests + Excel-to-model adapter helpers
```

The testing strategy has three layers:

1. **Recalculation harness** (`conftest.py`) — copies the Excel workbook,
   optionally modifies input cells, recalculates with LibreOffice, reads back
   values
2. **Adapter helpers** (bottom of `test_ny_aeba_model.py`) — translate between
   Excel cell references and the model's Python API
3. **Test classes** — one per computation stage, each comparing Python model
   output to Excel cell values

## conftest.py — Recalculation Harness

### Array Formula Baking (lines 40-83)

**Problem:** LibreOffice cannot evaluate certain Excel-specific array formulas
(AVERAGEIFS, SUMPRODUCT-with-criteria), returning `#NAME?`. These cells feed
into downstream calculations, causing cascading failures.

**Solution:** Before recalculating, scan the workbook for `ArrayFormula` objects
and replace them with their cached literal values from the original workbook.
This is safe because these formulas depend only on county data (not on model
inputs), so their values are constant across all perturbations.

**Review focus:** `_get_array_formula_cells()` uses a global cache
(`_ARRAY_FORMULA_CELLS`) discovered once by scanning the workbook. The scan
iterates all cells in all sheets looking for `openpyxl.worksheet.formula.ArrayFormula`
instances. If the Excel workbook adds new array formulas, this will automatically
pick them up.

### RecalculatedWorkbook (lines 86-137)

A dataclass wrapping the recalculated `.xlsx` file with convenience methods:

- `cell_value(cell_ref, sheet)` — read a single cell
- `row_values(row, columns, sheet)` — read E through J for a given row
- Lazy-loads the openpyxl workbook on first access

### `_recalculate_workbook` (lines 140-225)

The core function:

1. Copies the source workbook to `input/` subdirectory
2. Opens with openpyxl, bakes array formulas, applies cell modifications, saves
3. Runs `libreoffice --headless --calc --convert-to xlsx --outdir output/ input/file.xlsx`
4. Returns a `RecalculatedWorkbook` pointing to the output file

**Key detail:** Input and output directories must be separate. When they're the
same, LibreOffice silently fails to save (returns rc=0 but emits
`SfxBaseModel::impl_store` error), leaving formula cells without cached values.

### Fixtures (lines 228-267)

Two fixtures, both using `pytest.fixture` with generator cleanup:

- **`recalculated_workbook`** — recalculates once with no modifications. Used by
  smoke tests and non-parametrized tests.
- **`recalculate`** — factory fixture. Each call creates an independent copy and
  recalculation in its own subdirectory. Used by parametrized tests that need
  both default and perturbed workbooks.

## test_ny_aeba_model.py — Test Structure

### Constants (lines 40-56)

```python
COLUMNS = ["E", "F", "G", "H", "I", "J"]    # Excel Model sheet columns
SCENARIOS = [                                  # Maps column index to (fuel, zone)
    ("natural_gas", "4"), ("natural_gas", "5"), ("natural_gas", "6"),
    ("propane", "4"),     ("propane", "5"),     ("propane", "6"),
]
REL_TOL = 1e-4                                 # 0.01% relative tolerance
```

### Test Pattern

Every test follows the same pattern:

```python
def test_some_value(self, recalculate, modifications, param_id):
    # 1. Recalculate Excel with these modifications
    wb = recalculate(modifications)
    # 2. Read the expected values from the Excel row
    excel_vals = _read_row(wb, ROW_NUMBER)
    # 3. Run the Python model with equivalent overrides
    model_result = compute_something(_build_scenarios(modifications))
    # 4. Compare all 6 scenarios
    for i, (fuel, zone) in enumerate(SCENARIOS):
        model_val = _get_scenario_value(model_result, fuel, zone, "column_name")
        assert model_val == pytest.approx(excel_vals[i], rel=REL_TOL)
```

### Perturbation Strategy

Each test class defines a `_*_PARAMS` list with at least two entries: `default`
(no modifications) and one perturbation that changes an input relevant to that
computation stage. This ensures the model tracks formula changes, not just static
values.

| Test Class               | Perturbation             | What Changes                                   |
| ------------------------ | ------------------------ | ---------------------------------------------- |
| TestBuildingGeometry     | `floor_area_2000`        | Floor area E10:J10 from 2363 to 2000           |
| TestHeatLossRates        | `ach50_zone5_4.0`        | ACH50 for Zone 5 (F32, I32) from 3.0 to 4.0    |
| TestYearlyBtu            | `hdd_zone5_7000`         | HDD for Zone 5 (F43, I43) from 6300 to 7000    |
| TestSystemSizing         | `floor_area_2800`        | Floor area E10:J10 from 2363 to 2800           |
| TestBaselineCosts        | `afue_0.92`              | Furnace AFUE (E63:J63) from 0.95 to 0.92       |
| TestBaselineCosts (fuel) | `natgas_price_plus20pct` | Natural gas price (E6:G6) +20%                 |
| TestHeatPumpCosts        | `hspf2_9`                | ccASHP HSPF2 (E105:J105) from 10 to 9          |
| TestSavings              | `mortgage_7.5pct`        | Mortgage rate (E126:J126) from 6.38% to 7.5%   |
| TestWeightedAverages     | (none)                   | Default only — weights come from external data |
| TestRunModel             | (none)                   | Integration tests — default only               |
| TestEndToEndPerturbed    | (all at once)            | All perturbations applied simultaneously       |

**Review focus:** Each perturbation modifies the same cell in both fuel columns
for a given zone (e.g., F32 and I32 are both Zone 5 — natural gas and propane).
This is necessary because the Excel workbook has separate columns per scenario,
while the model uses a single `overrides` dict keyed by `(fuel, zone)`.

### Test Classes and Excel Row Coverage

#### TestSmoke (3 tests, lines 77-104)

Infrastructure checks. Verifies LibreOffice is installed, the workbook
recalculates, and a known cell value (F40 = 508.916) is correct.

#### TestBuildingGeometry (10 methods x 2 params = 20 tests, lines 131-260)

Excel rows 12-24. Wall length, surface area, attic area, window/door area,
basement areas, perimeter, volume. Geometry is identical across all 6 columns
with default inputs (doesn't depend on fuel or zone).

#### TestHeatLossRates (8 methods x 2 params = 16 tests, lines 281-403)

Excel rows 33-40. Seven heat loss components (attic, walls, windows,
above/below-grade basement, infiltration, slab) plus total. The ACH50
perturbation specifically tests Zone 5 infiltration because Zone 6 has a
different ACH50 value from zones 4/5 in the default data.

#### TestYearlyBtu (2 methods x 2 params = 4 tests, lines 424-460)

Excel rows 45-46. Adjusted HDD and yearly BTU demand. The HDD perturbation tests
that the EPA adjustment is properly subtracted.

#### TestSystemSizing (4 methods x 2 params = 8 tests, lines 482-545)

Excel rows 49-55. Coldest-day temperature (county-weighted by zone), degree
difference, BTU/hr on coldest day, sized system capacity.

#### TestBaselineCosts (16 methods, lines 584-840)

Excel rows 59-96. The largest test class. Covers furnace (equipment, fuel usage,
fuel cost, electrical cost, operating), AC (equipment, operating), gas water
heater (equipment, fuel cost, operating), service line, and totals.

Two parameter sets: most tests use `_BASELINE_PARAMS` (AFUE perturbation), but
`test_furnace_yearly_fuel_cost` uses `_BASELINE_FUELPRICE_PARAMS` (fuel price
perturbation) to specifically test the fuel cost calculation path.

**Review focus:** `test_service_line_blended_avg` (row 91) — this test verifies
the blended average service line cost, which depends on county-level data joined
through `_compute_zone_service_line_costs()`. It only runs with default params
(no perturbation) because the service line cost comes from external data, not
from model inputs that can be overridden via cell modifications.

#### TestHeatPumpCosts (15 methods x 2 params = 30 tests, lines 861-1069)

Excel rows 100-123. ccASHP (equipment, rebate, net cost, yearly kWh, electrical
cost, operating) and HPWH (device cost, rebate, net cost, electrical cost,
operating), plus totals. The HSPF2 perturbation changes how many kWh the heat
pump uses, which flows through to electrical cost and operating cost.

#### TestSavings (9 methods x 2 params = 18 tests, lines 1090-1223)

Excel rows 127-134. Construction savings (with/without service line), mortgage
savings (with/without service line), operating savings, total yearly savings
(with/without service line), 15-year present value.

**Review focus:** The mortgage rate perturbation (6.38% to 7.5%) tests the PMT
formula. This is where the annual-vs-monthly compounding difference would show up
if the model got it wrong.

#### TestWeightedAverages (8 tests, no perturbation, lines 1230-1392)

Excel rows 137-149. Survey counts, fossil fuel percentages, zone construction
shares, and four levels of weighted averages. No perturbation because the weights
come from external survey/county data, not from model inputs.

Uses `_get_weighted_avg_value()` helper instead of `_get_scenario_value()` to
extract aggregate rows by key.

#### TestRunModel (3 tests, no perturbation, lines 1399-1456)

End-to-end integration. Verifies `run_model()` returns a 6-row DataFrame with
correct shape, then spot-checks several computed values for natural gas Zone 5
and propane Zone 5 against hardcoded expected values.

#### TestEndToEndPerturbed (6 tests, all perturbations, lines 1462-1569)

Integration test that applies **all** perturbations simultaneously — one from
each computation stage — and checks final output values against the
simultaneously-perturbed Excel workbook. This catches composition bugs where
intermediate values interact incorrectly across pipeline stages, even if each
stage passes its own unit tests in isolation.

The combined perturbation set (`_ALL_PERTURBATIONS`) includes:

| Stage             | Perturbation                 | Cells Modified |
| ----------------- | ---------------------------- | -------------- |
| Building geometry | Floor area 2363 -> 2000      | E10:J10        |
| Heat loss rates   | ACH50 Zone 5: 3.0 -> 4.0     | F32, I32       |
| Yearly BTU        | HDD Zone 5: 6300 -> 7000     | F43, I43       |
| Baseline costs    | Furnace AFUE: 0.95 -> 0.92   | E63:J63        |
| Baseline costs    | Natural gas price +20%       | E6:G6          |
| Heat pump costs   | ccASHP HSPF2: 10 -> 9        | E105:J105      |
| Savings           | Mortgage rate: 6.38% -> 7.5% | E126:J126      |

Six tests check output rows that depend on multiple upstream stages: total
yearly savings (row 133), 15-year PV (row 134), baseline operating cost
(row 96), heat pump operating cost (row 123), construction savings (row 128),
and mortgage savings (row 130).

**Review focus:** Because all perturbations are applied at once, every
intermediate value in the pipeline is non-default. A bug in how stage N
consumes stage N-1's output would only show up here, not in the per-stage
unit tests which perturb one input at a time.

## Adapter Helpers (lines 1574-1697)

These translate between the two different addressing schemes:

### `_build_scenarios(modifications)` (line 1574)

Converts Excel cell references like `{"Model!F32": 4.0}` into the model's
override format `{("natural_gas", "5"): {"ach50": 4.0}}`.

Uses `_ROW_TO_PARAM` (line 1627) to map Excel row numbers to model parameter
names. Only 34 input rows are mapped — computed value rows are not overridable.

**Review focus:** If a new input parameter is added to the model, a
corresponding entry must be added to `_ROW_TO_PARAM` for perturbation tests to
work. Missing entries are silently skipped (the override is not applied).

### `_get_scenario_value(model_result, fuel, zone, column)` (line 1658)

Filters the model's polars DataFrame by fuel and zone to extract a single value.

### `_get_weighted_avg_value(model_result, key, column)` (line 1678)

Filters the weighted averages DataFrame by the `key` column (fuel name, zone
number, or "overall") to extract aggregate values.

## Known Limitations

1. **LibreOffice dependency** — tests require LibreOffice installed and on PATH.
   The `install-libreoffice.sh` script handles this for the devcontainer. The
   `TestSmoke.test_libreoffice_callable` test fails fast if it's missing.

2. **Array formula baking** — formulas that depend on model inputs (not just
   county data) would give stale values after baking. Currently all baked
   formulas are input-independent, but this assumption should be re-verified if
   the Excel workbook changes.

3. **No column C/D tests** — the Excel workbook has input cells in columns C and
   D (global parameters). The test perturbations only modify columns E-J
   (per-scenario values). Global parameter changes (e.g., changing the discount
   rate in C8) are not tested via Excel comparison, though the model's override
   mechanism supports them.

4. **Tolerance** — `REL_TOL = 1e-4` (0.01%) is tight enough to catch formula
   errors but loose enough to absorb floating-point differences between Excel's
   calculation engine and Python/polars. If a test fails at this tolerance, it
   likely indicates a real formula discrepancy, not a precision issue.

5. **Memory** — each LibreOffice recalculation spawns a subprocess. Running the
   full test suite in a container with less than 16 GB RAM can trigger OOM kills.
   Tests are run sequentially (`-x` flag recommended) to limit concurrent memory
   usage.
