# Plan: Migrate Heat Pump Cost Savings Model from Excel to Polars

## Context

The Excel workbook at `reports/ny_aeba_savings/Switchbox - Heat Pump Cost Savings in New Buildings Model (New GSHP in New Construction Incentives).xlsx` encodes a heat pump vs fossil fuel cost comparison model for NY new construction. It computes savings across 3 climate zones x 2 fuel types (natural gas, propane). Maintaining the spreadsheet has become unwieldy, and we need to add GSHP as a third heat pump technology.

The migration moves all data to YAML files (with anchors for DRY-ness) and all computation logic to polars. The Excel file is the source of truth for validation — every intermediate and final value will be tested against it.

## File Structure

```
reports/ny_aeba_savings/
  data/
    model_params.yaml        # financial, sizing, climate scalars
    building_params.yaml     # building design by zone (defaults + overrides)
    equipment.yaml           # device specs + prices, by technology
    operating_params.yaml    # maintenance, efficiency, fuel content
    fuel_prices.yaml         # monthly price time series (list of records)
    utility_rebates.yaml     # rebates per utility x technology
    service_line_costs.yaml  # gas utility service line costs
    counties.yaml            # 62 counties with zone, utilities, design temps
    heating_survey.yaml      # heating system type counts by zone
  model.py                   # all computation logic
  install-libreoffice.sh     # installs LibreOffice if not present
  Justfile                   # run commands
tests/
  test_ny_aeba_model.py      # tests validated against Excel values
  conftest.py                # shared fixtures (create if absent)
```

## Steps

### Step 1: Create YAML data files

Create all 9 YAML files in `reports/ny_aeba_savings/data/`, transcribing directly from the Excel sheets. Use YAML anchors (`&`/`*`) and merge keys (`<<`) where values repeat.

Key files and their anchor patterns:

- **building_params.yaml**: `defaults: &building_defaults` merged into each zone; zones only override `ach50` and `hdd`
- **equipment.yaml**: List-of-records format. Anchors for shared specs where useful (e.g., furnace used by both fuel types).
- **operating_params.yaml**: `&standard_maintenance` anchor for the $229 value shared across multiple device types.
- **fuel_prices.yaml**: List of `{fuel, month, year, price}` records. All months from the Excel "Fuel costs" sheet (winter months only: Jan-Mar, Oct-Dec). Three fuels: electricity (cents/kWh), natural_gas ($/mcf), propane (cents/gallon).
- **counties.yaml**: List of 62 county records with `{county, population, electric_utility, gas_utility, zone, design_temp_f, new_construction_share}`.
- **utility_rebates.yaml**: List of records `{utility, technology, amount, unit, source}`. Long format (one row per utility x technology).
- **service_line_costs.yaml**: List of records per gas utility.
- **heating_survey.yaml**: Summarized counts by zone x fuel-system combo (the bottom summary table from the Excel sheet, rows 37-44).
- **model_params.yaml**: Flat scalars.

Source values from the Excel computed-values dump (already captured in conversation context).

### Step 2: Justfile, LibreOffice setup, and test scaffolding

Set up the test infrastructure first so that model logic can be validated incrementally during development.

**LibreOffice installation script** (`install-libreoffice.sh`): A self-contained script that checks whether `libreoffice` is on PATH and installs it if missing. This is specific to this report — LibreOffice is not a project-wide dependency. The script should handle Debian/Ubuntu (`apt-get`) and exit with a clear message on unsupported platforms.

**Justfile** (`reports/ny_aeba_savings/Justfile`):

```just
# Ensure LibreOffice is available (installs if missing)
ensure-libreoffice:
  ./install-libreoffice.sh

# Run the model
run:
  uv run python model.py

# Run tests for this report (installs LibreOffice if needed)
test: ensure-libreoffice
  uv run python -m pytest tests/test_ny_aeba_model.py -v
```

**Test scaffolding**: Create `tests/test_ny_aeba_model.py` and `tests/conftest.py` with the LibreOffice recalculation fixture, initially testing just that:

1. LibreOffice is callable
2. The Excel workbook can be copied, modified with openpyxl, recalculated, and read back
3. A known cell (e.g., total heat loss rate for NatGas Zone 5 = 508.916) reads back correctly after recalculation with unmodified inputs

This verifies the test harness works before any model code exists.

### Step 3: Write tests

Create the full test suite in `tests/test_ny_aeba_model.py`, validated against the Excel workbook.

**Test strategy — LibreOffice recalculation**: Tests do not merely compare against static point values copied from the spreadsheet. Instead, the test harness programmatically modifies Excel input cells (e.g., changing HDD, fuel prices, equipment costs, AFUE, HSPF2), recalculates the workbook using LibreOffice Calc in headless mode, reads the recomputed outputs, and asserts that the polars model produces identical results. This validates the _logic_ of the migration, not just agreement on a single set of inputs.

**Approach**:

1. A `conftest.py` fixture copies the Excel workbook to a temp directory, uses `openpyxl` to modify specific input cells, then shells out to `libreoffice --headless --calc --convert-to xlsx` to force a full recalculation.
2. The fixture reads back computed values from the recalculated workbook using `openpyxl` with `data_only=True`.
3. The same modified inputs are injected into the polars model (via patched YAML data or function arguments).
4. Tests compare polars outputs to Excel outputs with `pytest.approx(rel=1e-4)`.

**Test cases** (each run with both default and perturbed inputs):

1. **test_building_geometry** — wall length, wall area, attic area, basement area, volume (rows 12-24)
2. **test_heat_loss_rates** — each component + total (rows 33-40). Zone 4/5 vs Zone 6 differ only in air changes.
3. **test_yearly_btu** — adjusted HDD, yearly BTU (rows 45-46). 6 values.
4. **test_system_sizing** — coldest day temp, degree diff, BTU/hr, scaled capacity (rows 49-55). 6 values each.
5. **test_baseline_costs** — furnace installed cost, yearly fuel/electrical/operating costs; AC + GWH costs; service line blended avg; totals (rows 59-96). All 6 columns.
6. **test_heat_pump_costs** — ccASHP equipment cost, rebates, net cost; yearly kWh, electrical cost, operating cost; HPWH same; totals (rows 100-123). All 6 columns.
7. **test_savings** — construction savings, mortgage savings, operating savings, total yearly savings, PV (rows 127-134). All 6 columns.
8. **test_weighted_averages** — survey weights, zone weights, statewide savings (rows 137-149).

**Input perturbations to test**:

- Change HDD values (e.g., Zone 5 HDD from 6300 → 7000)
- Change AFUE (e.g., 0.95 → 0.92)
- Change HSPF2 (e.g., 10 → 9)
- Change fuel prices (e.g., natural gas $/mcf +20%)
- Change mortgage rate (e.g., 6.38% → 7.5%)

This ensures the polars model replicates the Excel _formulas_, not just the current outputs.

Key Excel reference values for spot-checking (NatGas Zone 5, default inputs):

- Total heat loss rate: **508.916** BTU/hr/°F
- Yearly BTU: **72,575,434**
- Baseline yearly operating: **$2,152.14**
- HP yearly operating: **$2,345.96**
- Total yearly savings (with service lines): **$133.57**
- 15yr PV: **$1,485.04**

Key Excel reference values (Propane Zone 5, default inputs):

- Baseline yearly operating: **$4,872.82**
- HP yearly operating: **$2,345.96**
- Total yearly savings: **$2,637.82**
- 15yr PV: **$29,328.29**

### Step 4: Create model.py — data loading

Create `reports/ny_aeba_savings/model.py` with functions to load YAML into polars DataFrames and dicts.

Functions:

- `load_model_params() -> dict` — returns flat dict of scalars
- `load_building_params() -> pl.DataFrame` — merges defaults into each zone, returns one row per zone
- `load_equipment() -> pl.DataFrame` — flattens list-of-records, computes `avg_price` column
- `load_fuel_prices() -> pl.DataFrame` — loads records, computes winter averages for the configured period
- `load_counties() -> pl.DataFrame`
- `load_utility_rebates() -> pl.DataFrame`
- `load_service_line_costs() -> pl.DataFrame`
- `load_heating_survey() -> pl.DataFrame`
- `load_operating_params() -> dict`

The DATA_DIR path is derived from `Path(__file__).parent / "data"`.

### Step 5: Create model.py — building heat loss calculations

Implement the heat loss computation as polars expressions, matching Excel Model rows 10-40:

```
build_scenario_table() -> pl.DataFrame  (12 rows: 3 zones x 2 fuels x 2 HP techs)
compute_building_geometry(scenarios) -> pl.DataFrame  (wall area, attic, basement, volume)
compute_heat_loss_rates(scenarios) -> pl.DataFrame  (per-component BTU/hr/°F, total)
compute_yearly_btu(scenarios) -> pl.DataFrame  (HDD adjusted, yearly BTU demand)
compute_system_sizing(scenarios) -> pl.DataFrame  (coldest day BTU/hr, scaled capacity)
```

Each function takes a DataFrame, adds columns, returns it. Pure column expressions — no loops.

The coldest-day design temperature per zone is a weighted average of county design temps, weighted by new construction share. This is computed from counties.yaml (matching Excel rows 49, `County information!J66:J68`).

### Step 6: Create model.py — cost calculations

Implement baseline and heat pump cost calculations (Excel Model rows 57-123):

```
compute_baseline_costs(scenarios) -> pl.DataFrame
  - furnace: equipment cost, gas tank cost (propane only), yearly fuel + electrical + maintenance
  - AC: equipment cost, yearly maintenance
  - gas water heater: equipment cost, yearly fuel + maintenance
  - service line costs (natural gas only, blended avg by zone)
  - totals: FF+AC+GWH equipment, FF+AC+GWH+service_line, yearly operating

compute_heat_pump_costs(scenarios) -> pl.DataFrame
  - ccASHP/GSHP: equipment cost (zone-dependent), rebates (blended avg by zone), net cost
  - yearly kWh from HSPF2/COP, yearly electrical cost, maintenance
  - HPWH: equipment cost, rebate (blended avg by zone), net cost, yearly electrical + maintenance
  - totals: HP+HPWH equipment, yearly operating
```

Blended average rebates per zone are computed by joining counties → utility_rebates, then taking a weighted average by new_construction_share within each zone.

### Step 7: Create model.py — comparison, savings, and run_model()

Implement the savings comparison (Excel Model rows 125-149):

```
compute_savings(scenarios) -> pl.DataFrame
  - construction_savings (with and without service lines)
  - mortgage_savings via PMT formula (polars expression)
  - operating_savings
  - total_yearly_savings (with and without service lines)
  - 15yr present value at discount rate

compute_weighted_averages(scenarios, counties, survey) -> pl.DataFrame
  - weighted statewide savings by fuel type
  - weighted zonewide savings
  - weighted overall statewide savings + PV
```

PMT formula implemented as a pure polars expression:
`pmt = (rate * pv) / (1 - (1 + rate).pow(-n))`

```python
def run_model() -> pl.DataFrame:
    """Run the full model, returning one row per (zone, fuel, hp_tech) scenario."""
    # loads all data, builds scenarios, computes everything
    # returns the 12-row result DataFrame

def main():
    results = run_model()
    print(results)

if __name__ == "__main__":
    main()
```

### Step 8: Final verification

1. `just test` from repo root — all tests pass (default + perturbed inputs)
2. `just check` from repo root — no lint/type/format errors
3. `uv run python reports/ny_aeba_savings/model.py` — prints the results table
4. Every intermediate value matches the Excel to within 0.01% relative tolerance

## Implementation notes

- Work will be managed and executed using `beads` and the data scientist subagent. Each step above maps to one or more beads — self-contained units of work that the subagent can pick up, execute, validate, and mark complete.
- GSHP rows are **not** populated in this initial migration. The data structure supports them (equipment.yaml has placeholders), but the actual GSHP prices and COP values are TBD. The 6-row scenario table (ccASHP only) will expand to 12 when GSHP data is added.
- The `Propane - Zone 5` and `Natural Gas - Zone 5` sheets in the Excel are older versions of the model (different assumptions, different structure). They are **not** used for validation — only the `Model` sheet is authoritative.
- The ConEd ccASHP rebate is $2,500 per project (not per 10K BTU). The code converts this using system capacity: `2500 / (system_btu / 10000)`. This is already handled in the Excel (`Utility rebates!B5` formula).
- Currently ccASHP rebates and federal tax credits are both $0 in the Model sheet (rows 101-102). The YAML will store the structural data (rebate amounts by utility) but the blended averages for ccASHP will net to $0 since the Model sheet zeroes them. HPWH rebates are active.
