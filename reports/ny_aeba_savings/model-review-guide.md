# model.py Review Guide

## Overview

`model.py` is a polars-based reimplementation of an Excel workbook that models
heat pump cost savings for new construction in New York. It computes whether
replacing a fossil fuel furnace + AC + gas water heater with a cold-climate air
source heat pump (ccASHP) + heat pump water heater (HPWH) saves money, across 6
scenarios (2 fuels x 3 climate zones).

The module has three layers:

1. **Data loaders** — read YAML files into polars DataFrames or dicts
2. **Computation pipeline** — a chain of functions, each calling the previous
   one and adding columns
3. **Output formatting** — reshapes the 6-row result into a 12-row wide table
   with weighted averages

## Data Loading (lines 30-174)

Nine YAML files in `data/`, each with a dedicated loader:

| Loader                      | File                      | Returns             | Key contents                                                                      |
| --------------------------- | ------------------------- | ------------------- | --------------------------------------------------------------------------------- |
| `load_model_params()`       | `model_params.yaml`       | `dict`              | mortgage rate, term, discount rate, design temp, sizing factor, propane tank cost |
| `load_operating_params()`   | `operating_params.yaml`   | `dict` (nested)     | maintenance costs, AFUE, HSPF2, fuel BTU content, water heater params             |
| `load_building_params()`    | `building_params.yaml`    | DataFrame (3 rows)  | per-zone R-values, floor area, stories, wall height, HDD, ACH50                   |
| `load_equipment()`          | `equipment.yaml`          | DataFrame           | device prices (furnace, AC, gas water heater, ccASHP by zone, HPWH)               |
| `load_fuel_prices()`        | `fuel_prices.yaml`        | DataFrame (3 rows)  | winter-average electricity, natural gas, propane prices (2020-2025)               |
| `load_counties()`           | `counties.yaml`           | DataFrame (62 rows) | county zone, design temp, new construction share, utilities                       |
| `load_utility_rebates()`    | `utility_rebates.yaml`    | DataFrame           | utility x technology rebate amounts                                               |
| `load_service_line_costs()` | `service_line_costs.yaml` | DataFrame           | gas utility service line costs per foot                                           |
| `load_heating_survey()`     | `heating_survey.yaml`     | DataFrame           | heating system type counts by zone (for weighting)                                |

## Computation Pipeline (lines 206-927)

Each stage calls the previous one, adds columns, and returns the growing
DataFrame. The `overrides` parameter threads through every stage to allow tests
to perturb individual inputs.

```
build_scenario_table     (6 rows: 2 fuels x 3 zones, all inputs joined)
        |
compute_building_geometry   (+ wall_length, surface areas, volume)
        |
compute_heat_loss_rates     (+ per-component BTU/hr/degF, total)
        |
compute_yearly_btu          (+ adjusted HDD, yearly BTU demand)
        |
compute_system_sizing       (+ coldest-day sizing, system capacity)
        |
compute_baseline_costs      (+ furnace/AC/GWH costs, service line, totals)
        |
compute_heat_pump_costs     (+ ccASHP/HPWH costs, rebates, totals)
        |
compute_savings             (+ construction/mortgage/operating savings, PV)
```

### Stage 1: `build_scenario_table` (line 242)

Creates the 6-row scaffold by cross-joining fuels x zones, then joins in:

- Building params (by zone) -- R-values, HDD, floor area, etc.
- Model params (broadcast) -- mortgage rate, discount rate, etc.
- Operating params (broadcast) -- AFUE, HSPF2, maintenance costs, etc.
- Fuel prices (by fuel) -- electricity price (all rows), fuel-specific price

**Review focus:** Verify that fuel-dependent values (gas water heater fuel usage
rate, fuel price, propane tank cost) select the correct branch per fuel.

### Stage 2: `compute_building_geometry` (line 317)

Derives wall length, surface areas, and volume from floor area, stories, wall
height, and window/door percentage.

**Review focus:** The volume formula (line 362) adds basement volume using
`floor_area / stories` for the basement footprint. Verify this matches the Excel
formula `=E10*E13+(E19+E20)*E10/2`.

### Stage 3: `compute_heat_loss_rates` (line 376)

Computes 7 heat loss components (attic, walls, windows, above/below-grade
basement, infiltration, slab) and sums them.

**Review focus:** Infiltration formula `0.018 * (ACH50/20) * volume` — the 0.018
factor converts CFM to BTU/hr/degF. The `/20` converts ACH50 to natural air
changes.

### Stage 4: `compute_yearly_btu` (line 432)

`yearly_btu = total_heat_loss_rate * (HDD - epa_hdd_adjustment) * 24`

Simple; just verify the EPA HDD adjustment is subtracted (not added).

### Stage 5: `compute_system_sizing` (line 455)

Joins county-weighted design temperatures per zone, then computes peak load
and sized capacity.

**Review focus:** `_compute_zone_design_temps()` (line 211) — weights are
`new_construction_share` normalized within each zone, not raw shares. Verify the
weighted average uses proper normalization.

### Stage 6: `compute_baseline_costs` (line 567)

The longest stage. Computes:

- **Furnace:** equipment + gas tank (propane only) = installed cost; fuel
  usage/cost (via AFUE and fuel energy content); electrical usage (blower fans);
  maintenance; total operating
- **Central AC:** equipment cost; operating = maintenance only
- **Gas water heater:** equipment cost; fuel usage/cost; operating
- **Service line:** blended average by zone (natural gas only, 0 for propane)
- **Totals:** `baseline_equipment_total`, `baseline_equipment_with_service_line`,
  `baseline_yearly_operating`

**Review focus:**

- Furnace fuel usage (line 629): `yearly_btu / (AFUE * energy_content)` — the
  divisor differs by fuel (BTU/mcf for gas, BTU/gallon for propane)
- Service line cost (line 686-694): `_compute_zone_service_line_costs()` joins
  counties to service line costs by `gas_utility`, weighted by
  `new_construction_share`. Set to 0 for propane.

### Stage 7: `compute_heat_pump_costs` (line 726)

- **ccASHP:** zone-dependent equipment cost (zone 4 cheaper due to milder
  climate); rebate and tax credit both $0 in current model; net cost; yearly kWh
  via `yearly_btu / (HSPF2 * 1000)`; operating cost
- **HPWH:** fixed device cost; zone-blended rebate (weighted by new construction
  share); net cost; yearly kWh = daily_kwh * 365; operating cost
- **Totals:** `hp_equipment_total`, `hp_yearly_operating_total`

**Review focus:**

- ccASHP pricing (line 770): zone 4 gets a different (smaller/cheaper) unit than
  zones 5 and 6
- HPWH rebate blending (`_compute_zone_hpwh_rebates`, line 525): joins on
  `electric_utility`, fills null with 0 for utilities without rebates

### Stage 8: `compute_savings` (line 845)

Computes deltas and present value:

- Construction savings = baseline equipment - HP equipment (with and without
  service line)
- Mortgage savings = PMT(baseline) - PMT(HP) using **annual compounding**
- Operating savings = baseline operating - HP operating
- Total yearly savings = mortgage savings + operating savings
- 15-year PV = total savings * annuity factor

**Review focus:**

- PMT uses **annual** compounding (line 877-878):
  `pmt = (rate * principal) / (1 - (1 + rate)^(-n))` where rate = 6.38%/yr and
  n = 30 years. This matches the Excel PMT function with annual periods. It does
  NOT use monthly compounding (rate/12, n*12).
- PV annuity factor (line 920): `(1 - (1+r)^(-n)) / r` with r = discount rate,
  n = analysis period (15 years)

## Weighted Averages (lines 929-1069)

Two separate mechanisms exist for weighting:

### `compute_weighted_averages` (line 975)

Used by the **test suite** to verify specific Excel cells. Returns the 6 scenario
rows plus aggregate rows tagged by a `key` column. Only weights
`total_yearly_savings_with_service_line` and PV.

### Inside `build_tidy_results` (line 1087)

Used by the **output pipeline**. Weights ALL measures (equipment costs, operating
costs, mortgage payments, savings, PV) using the same weights:

| Aggregate level       | Weight column                                      | What it means                             |
| --------------------- | -------------------------------------------------- | ----------------------------------------- |
| Statewide by fuel     | `pct_new_construction_in_zone`                     | Zone's share of new construction          |
| Zone-wide (all fuels) | `pct_ff_using_fuel`                                | Fuel's share of fossil fuel users in zone |
| Overall statewide     | `pct_ff_using_fuel * pct_new_construction_in_zone` | Combined fuel+zone weight                 |

The weighting sources:

- `_compute_survey_weights()` (line 929): Heating survey data. Natural gas =
  "Furnace + Gas" + "Boiler + Gas"; propane = "Furnace + Propane or Oil" +
  "Boiler + Propane or Oil". Produces `pct_ff_using_fuel` per (fuel, zone).
- `_compute_zone_new_construction_shares()` (line 966): County-level
  `new_construction_share` summed by zone.

**Review focus:** The two weighting mechanisms should produce identical values for
`total_yearly_savings_with_service_line`. Verify by comparing
`compute_weighted_averages` aggregate rows with the corresponding
`build_tidy_results` Statewide/all_fossil_fuels rows.

## Output Formatting (lines 1082-1260)

### `build_tidy_results` (line 1087)

Produces 12 rows x 23 columns:

| `baseline_tech`       | `geography` | Meaning                  |
| --------------------- | ----------- | ------------------------ |
| `natural_gas_furnace` | Zone 4/5/6  | Raw scenario             |
| `natural_gas_furnace` | Statewide   | Weighted across zones    |
| `propane_furnace`     | Zone 4/5/6  | Raw scenario             |
| `propane_furnace`     | Statewide   | Weighted across zones    |
| `all_fossil_fuels`    | Zone 4/5/6  | Weighted across fuels    |
| `all_fossil_fuels`    | Statewide   | Overall weighted average |

Column order (after the 3 identifier columns):

1. `delta-yearly_total_savings-dollars_per_year` (headline number)
2. `delta-present_value_15yr-dollars_pv`
3. Other delta-only measures (construction savings, mortgage savings, operating
   savings)
4. Paired cost breakdowns: for each measure, `baseline-*`, `hp-*`, `delta-*`

Paired measures: equipment cost, equipment cost incl. service line, yearly
operating, yearly mortgage, yearly mortgage incl. service line.

**Review focus:**

- Mortgage columns (`_bl_mortgage`, `_bl_mortgage_sl`, `_hp_mortgage`) are
  computed inside `build_tidy_results` using the same PMT factor as
  `compute_savings`. Verify these are consistent — the delta of the mortgage
  columns should equal `mortgage_savings` / `mortgage_savings_with_service_line`.
- The `_make_row` helper (line 1155) computes `delta = baseline - hp` for paired
  measures. For the delta-only measures, the value is taken directly from the
  savings columns. Both conventions mean positive = HP saves money.

### `main` (line 1239)

Calls `compute_savings()` -> `build_tidy_results()` -> prints + saves CSV with
git commit hash in the header.

## Testing Strategy

Tests live in `tests/test_ny_aeba_model.py` (139 tests). They use a LibreOffice
recalculation harness (`tests/conftest.py`) that:

1. Copies the source Excel workbook to a temp directory
2. Optionally modifies input cells via openpyxl
3. "Bakes" array formulas (replaces AVERAGEIFS etc. with cached literal values)
4. Recalculates with `libreoffice --headless --convert-to xlsx`
5. Reads back computed values and compares with the Python model

This means the tests validate the Python model against the Excel workbook for
both default inputs and perturbed inputs.

## Key Assumptions to Verify

1. **Annual vs monthly compounding**: PMT uses annual rate (6.38%) and annual
   periods (30), not monthly
2. **Fuel price units**: electricity in cents/kWh (converted to $/kWh),
   natural gas in $/mcf, propane in cents/gallon (converted to $/gallon)
3. **Service line**: only applies to natural gas scenarios, 0 for propane
4. **ccASHP rebate and tax credit**: both set to $0 in current model
5. **Cooling costs**: not modeled; AC operating cost = maintenance only
6. **HSPF2 units**: BTU/Wh, so `yearly_kWh = yearly_btu / (HSPF2 * 1000)`
