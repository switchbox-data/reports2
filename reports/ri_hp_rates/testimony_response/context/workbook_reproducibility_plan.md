# Plan: reproducible RIE 1-8/1-9 workbooks

## Goal

Revise the RIE 1-8 and RIE 1-9 workbooks so that:

1. A reviewer can **recreate every number** from documented inputs (tariff JSONs,
   exported billing kWh, CAIRO bills).
2. The workbook values **match the expert testimony** (`expert_testimony.qmd`),
   specifically the inline computed values from `report_variables.pkl` and the
   figures from `analysis.qmd`.

## Status: implemented

All phases below have been implemented. The workbook script
(`build_RIE_1_8_1_9_workbook.py`) has been updated.

## Approach: use total bills, not decomposed bills

The workbook uses `elec_total_bill` from CAIRO directly — the unambiguous total
electric bill. It does **not** decompose into `elec_fixed_charge` /
`elec_delivery_bill` / `elec_supply_bill`, because that decomposition uses
`rie_flat.json` ($11.47/mo) via `build_master_bills.py`, which differs from the
$10.01/mo fixed charge in the calibrated tariffs and the testimony.

Instead, the workbook presents:

- **Total electric bill** from CAIRO (exact, unambiguous)
- **Tariff rates** from the calibrated tariffs (matching the testimony)
- **Fixed charge** of $10.01/mo ($120.12/yr) — used consistently across all
  workbooks (RIE 1-8, 1-9, and 1-11). This is the sum of the three per-customer
  line items: $6.00 customer charge + $3.22 RE Growth + $0.79 LIHEAP Enhancement.
  It matches `fixedchargefirstmeter = 10.01` in all calibrated tariff JSONs and
  what the testimony cites.
- **Billing kWh** exported directly from CAIRO's billing pipeline
  (`billing_kwh_annual.parquet`), not back-derived from bills.

## Key decisions

### Consistent fixed charge: $10.01/mo

All workbooks use $10.01/mo ($120.12/yr). This is:

- The sum of the three per-customer line items on the bill ($6.00 customer charge
  - $3.22 RE Growth + $0.79 LIHEAP Enhancement)
- What the calibrated tariff JSONs use (`fixedchargefirstmeter = 10.01`)
- What the testimony cites as the fixed charges
- What CAIRO actually bills against hourly

Other fixed charge values exist in different contexts but are NOT used in the
workbooks:

- $11.47/mo — `rie_flat.json` (used only by `build_master_bills.py` to
  decompose the bill into delivery/supply components; not the actual billing
  fixed charge)
- $117.54/yr — revenue-equation residual from the old kWh back-derivation
  (now removed)
- $137.64/yr ($11.47 × 12) — what `build_master_bills.py` reports as
  `elec_fixed_charge` (a different decomposition)

### kWh source: exported from CAIRO billing pipeline

kWh values are loaded from `billing_kwh_annual.parquet`, exported directly from
CAIRO's billing pipeline during runs. These are the exact grid-consumed kWh that
CAIRO uses for billing, after:

- PV clipping (`grid_cons = max(electricity_net, 0)`)
- `kwh_scale_factor` application (0.9568)
- 48-hour day-of-week timeshift (aligning 2018 weather year to 2025)

Each building gets exactly two kWh values: upgrade 0 (before HP) and upgrade 2
(after HP). These are the same regardless of which tariff is applied.

Source files:

- Upgrade 0: `s3://data.sb/switchbox/cairo/outputs/hp_rates/ri/rie/ri_20260504_kwh_export_v2/20260505_011359_ri_rie_run1_up00_precalc__default/billing_kwh_annual.parquet`
- Upgrade 2: `s3://data.sb/switchbox/cairo/outputs/hp_rates/ri/rie/ri_20260504_kwh_export_v2/20260505_011437_ri_rie_run3_up02_default__default/billing_kwh_annual.parquet`

### Bill-verification formula: RIE 1-9 only

RIE 1-9 uses the HP flat supply tariff (`rie_hp_flat_supply_calibrated.json`),
which has a single flat rate of 23.129 ¢/kWh (delivery + supply bundled). The
verification formula is:

```
elec_bill_formula = annual_kwh_after × 0.23129 + 10.01 × 12
```

This reproduces CAIRO's total bill within ~$1. The residual column
(`elec_bill_residual = elec_bill_after - elec_bill_formula`) is included in the
per_building sheet.

### Why no bill-verification formula for RIE 1-8

The default supply tariff (`rie_default_supply_calibrated.json`) uses three
seasonal rates:

- Winter (Jan, Feb, Mar, Nov, Dec): 31.38 ¢/kWh
- Summer (Jun, Jul, Aug, Sep): 24.78 ¢/kWh
- Shoulder (Apr, May, Oct): 29.49 ¢/kWh

These rates bundle delivery + supply. Because each building has a different
monthly consumption profile, a single `annual_kwh × rate` formula cannot
reproduce the bill — it would require 12 monthly kWh values and per-month rate
assignments. CAIRO computes bills hourly (8,760 hours), applying the correct
seasonal rate to each hour's consumption, then sums to the annual total.

The `elec_total_bill` column is the exact annual bill from CAIRO. To verify it
independently, one would need the building's hourly load profile (available in
`billing_kwh_8760.parquet`) and the seasonal rate schedule above.

## What each workbook tab contains

### assumptions tab

- Discovery request text
- LMI discount tier (32% enrollment)
- Bill columns used and filtering criteria
- **Tariff tables**: Default tariffs (before) and HP subclass tariffs (after,
  1-9 only), replicating `tbl-rie-energy-tariffs` from the testimony. Includes
  electric delivery, supply (seasonal and flat), gas, oil, and propane rates.
- **How bills are computed**: Fixed charge ($10.01/mo), kWh source (exported
  from CAIRO), electric bill source (CAIRO hourly simulation).
- **Why no formula (1-8)** or **Bill-verification formula (1-9)**: Explains
  the seasonal rate limitation for 1-8, or provides the verification formula
  for 1-9.
- **Data sources**: S3 paths for master bills and billing kWh parquets.
- **Column descriptions**: All per_building columns documented.

### per_building tab

- bldg_id, weight
- annual_kwh_before (upgrade 0), annual_kwh_after (upgrade 2)
- Before/after bills: elec, gas, oil, propane (undiscounted and LMI-adjusted)
- LMI discount amounts, total energy bills, delta, saves flag, weighted saves
- **RIE 1-9 only**: elec_bill_formula and elec_bill_residual columns

### result tab

- Total gas-heated customers (weighted)
- Customers that save (weighted)
- Percentage that save / lose
- Headline figure

## Key tariff files (rate-design-platform)

All calibrated tariffs use `fixedchargefirstmeter = 10.01` ($6.00 + $3.22 + $0.79).

| File                                 | Rate                                                       | Used in runs |
| ------------------------------------ | ---------------------------------------------------------- | ------------ |
| `rie_default_calibrated.json`        | 14.078 ¢/kWh flat delivery                                 | 1, 3         |
| `rie_default_supply_calibrated.json` | Seasonal delivery+supply bundled (31.38/24.78/29.49 ¢/kWh) | 2, 4         |
| `rie_hp_flat_calibrated.json`        | 8.249 ¢/kWh flat HP delivery                               | 19           |
| `rie_hp_flat_supply_calibrated.json` | 23.129 ¢/kWh flat HP delivery+supply bundled               | 20           |

## CAIRO batch and runs

Bills batch: `ri_20260331_r1-20_rate_case_test_year`
kWh batch: `ri_20260504_kwh_export_v2`

| Master bill path                    | Runs                        | Description                           |
| ----------------------------------- | --------------------------- | ------------------------------------- |
| `run_1+2/comb_bills_year_target/`   | 1 (delivery) + 2 (supply)   | Before: upgrade 0, default rates      |
| `run_3+4/comb_bills_year_target/`   | 3 (delivery) + 4 (supply)   | After (1-8): upgrade 2, default rates |
| `run_19+20/comb_bills_year_target/` | 19 (delivery) + 20 (supply) | After (1-9): upgrade 2, HP flat rates |

## Files involved

| File                                                     | Role                              |
| -------------------------------------------------------- | --------------------------------- |
| `testimony_response/build_RIE_1_8_1_9_workbook.py`       | Primary script (updated)          |
| `testimony_response/context/cairo_bill_decomposition.md` | Reference for bill mechanics      |
| `cache/report_variables.pkl`                             | Source of testimony inline values |
| `notebooks/analysis.qmd`                                 | Source of testimony figures       |
| `expert_testimony.qmd`                                   | The testimony document itself     |
