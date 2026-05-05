# Plan: reproducible RIE 1-8/1-9 workbooks

## Goal

Revise the RIE 1-8 and RIE 1-9 workbooks so that:

1. A reviewer can **recreate every number** from documented inputs (tariff JSONs,
   rev_req YAMLs, ResStock kWh, CAIRO bills).
2. The workbook values **match the expert testimony** (`expert_testimony.qmd`),
   specifically the inline computed values from `report_variables.pkl` and the
   figures from `analysis.qmd`.

## Current state

The workbook already includes:

- **per_building tab**: bldg_id, weight, annual_kwh_before, annual_kwh_after,
  before/after bills (elec, gas, oil, propane with LMI adjustment), delta, save flag.
- **result tab**: headline percentage (weighted share that saves/loses), computed
  with live Excel formulas from per_building data.
- **assumptions tab**: tariff tables (default before, HP after for 1-9), data
  source S3 paths, column descriptions.

### Gaps

| Gap                                  | Impact                                                                                                                                                                                           |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **kWh derivation is indirect**       | `annual_kwh` is back-derived from delivery bill via `(bill_delivery − annual_fixed_per_customer) / vol_rate`. This is opaque and doesn't surface the actual ResStock kWh or the scaling factors. |
| **Tariff rates not linked to bills** | The assumptions tab lists tariff rates, but there's no formula connecting rates × kWh to the bill components.                                                                                    |
| **Testimony figures not traceable**  | The testimony cites percentages (79% lose, 87% save) that come from `report_variables.pkl`. The workbook computes these independently but doesn't show they match.                               |

## Approach: use total bills, not decomposed bills

The workbook uses `elec_total_bill` from CAIRO directly — the unambiguous total
electric bill. It does **not** decompose into `elec_fixed_charge` /
`elec_delivery_bill` / `elec_supply_bill`, because that decomposition uses
`rie_flat.json` ($11.47/mo) via `build_master_bills.py`, which differs from the
$10.01/mo fixed charge in the calibrated tariffs and the testimony.

Instead, the workbook presents:

- **Total electric bill** from CAIRO (exact, unambiguous)
- **Tariff rates** from the calibrated tariffs (matching the testimony)
- **Fixed charge** of $10.01/mo ($120.12/yr) — the sum of the three per-customer
  line items: $6.00 customer charge + $3.22 RE Growth + $0.79 LIHEAP Enhancement
- **Verification**: `annual_kwh × vol_rate + $10.01 × 12 ≈ elec_total_bill`
  (within ~$1 from CAIRO's hourly billing mechanics)

This is consistent with the testimony, the calibrated tariffs, and what CAIRO
actually billed against (`fixedchargefirstmeter = 10.01` in all calibrated JSONs).

## Plan

### Phase 1: Link tariff rates to bill verification formulas

In the assumptions tab, add a **"How to verify"** section:

```
For building i with annual_kwh_after = K:

  RIE 1-8 (default rates, after HP):
    elec_total_bill ≈ K × weighted_avg_supply_rate + $10.01 × 12
    The default supply tariff is seasonal (winter/summer/shoulder),
    so the annual bill depends on each building's monthly consumption
    profile. The annual total matches CAIRO output within ~$1.

  RIE 1-9 (HP flat rates, after HP):
    elec_total_bill ≈ K × 0.23129 + $10.01 × 12
    The HP flat supply tariff is a single flat rate (delivery+supply
    bundled). This formula reproduces CAIRO's total bill within ~$1.

  Fixed charge ($10.01/mo):
    $6.00/mo customer charge + $3.22/mo RE Growth + $0.79/mo LIHEAP
    Enhancement. These are unchanged by the proposal.

  The ~$1 tolerance arises from CAIRO's hourly billing mechanics
  (48-hour day-of-week timeshift aligning 2018 weather year to 2025).
```

### Phase 2: Surface the kWh derivation

The current kWh back-derivation (`(bill_delivery − fixed) / vol_rate`) is opaque.
Document the derivation clearly:

1. kWh are derived from the status-quo delivery run (run 1+2), where the tariff
   is a single flat rate: `annual_kwh = (annual_bill_delivery − $117.54) / 0.14078`.
   The $117.54 is the revenue-equation residual (see `cairo_bill_decomposition.md`).
2. This produces the same kWh for both RIE 1-8 and RIE 1-9 (before = upgrade 0,
   after = upgrade 2).
3. For 6 PV buildings, `annual_kwh` reflects grid-consumed electricity only
   (import-only kWh), because CAIRO does not credit export hours.

Add a note in the assumptions tab explaining this derivation and citing the
`kwh_scale_factor = 0.9568` from `rie_rate_case_test_year.yaml`.

### Phase 3: Cross-reference with testimony

Add a **testimony_match** section in the assumptions tab that maps workbook
outputs to specific testimony claims:

| Testimony claim                                 | Testimony source                                         | Workbook cell            | Match?     |
| ----------------------------------------------- | -------------------------------------------------------- | ------------------------ | ---------- |
| "79% of gas-heated households would lose money" | Section V, inline `pct(v.pct_natgas_lose_default_lmi40)` | result!B2                | Must match |
| "87% of gas-heated households would save money" | Section V, inline `pct(v.pct_natgas_save_hprate_lmi40)`  | result!B2                | Must match |
| Delivery rate 14.08 ¢/kWh                       | Section V, rate comparison tables                        | assumptions tariff table | Must match |
| HP delivery rate 8.25 ¢/kWh                     | Section V, `cents(c.hp_pct_reduction)`                   | assumptions tariff table | Must match |
| Fixed charge $10.01/mo                          | Section V, `fixed_charges_description`                   | assumptions tariff table | Must match |
| LMI discount at 32% enrollment                  | Section VI                                               | assumptions tab          | Must match |

### Phase 4: Documentation

1. Update the assumptions tab "How bills are computed" section:
   - Bills come from CAIRO's hourly simulation (ResStock loads × tariff rates).
   - The fixed charge is $10.01/mo, matching the calibrated tariff JSONs and testimony.
   - CAIRO applies a `kwh_scale_factor` of 0.9568 and a 48-hour day-of-week
     timeshift (aligning 2018 weather loads to 2025 calendar), which produces
     small (~$1) differences from `kWh × annual_rate + fixed × 12`.
2. Reference `cairo_bill_decomposition.md` for full technical details.

## Implementation order

1. **Phase 1 first** — linking rates to verification formulas is the most impactful
   for reproducibility and doesn't require loading new data.
2. **Phase 3 next** — cross-reference ensures testimony match.
3. **Phase 2** — kWh derivation documentation (the current back-derivation works;
   this phase clarifies it).
4. **Phase 4 throughout** — documentation updates happen alongside each phase.

## Files involved

| File                                                     | Role                              |
| -------------------------------------------------------- | --------------------------------- |
| `testimony_response/build_RIE_1_8_1_9_workbook.py`       | Primary script to modify          |
| `testimony_response/verify_RIE_1_8_1_9_workbook.py`      | Verification script               |
| `testimony_response/context/cairo_bill_decomposition.md` | Reference for bill mechanics      |
| `cache/report_variables.pkl`                             | Source of testimony inline values |
| `notebooks/analysis.qmd`                                 | Source of testimony figures       |
| `expert_testimony.qmd`                                   | The testimony document itself     |

## Key tariff files (rate-design-platform)

All calibrated tariffs use `fixedchargefirstmeter = 10.01` ($6.00 + $3.22 + $0.79).

| File                                 | Rate                                                       | Used in runs |
| ------------------------------------ | ---------------------------------------------------------- | ------------ |
| `rie_default_calibrated.json`        | 14.078 ¢/kWh flat delivery                                 | 1, 3         |
| `rie_default_supply_calibrated.json` | Seasonal delivery+supply bundled (31.38/24.78/29.49 ¢/kWh) | 2, 4         |
| `rie_hp_flat_calibrated.json`        | 8.249 ¢/kWh flat HP delivery                               | 19           |
| `rie_hp_flat_supply_calibrated.json` | 23.129 ¢/kWh flat HP delivery+supply bundled               | 20           |

## CAIRO batch and runs

Batch: `ri_20260331_r1-20_rate_case_test_year`

| Master bill path                    | Runs                        | Description                           |
| ----------------------------------- | --------------------------- | ------------------------------------- |
| `run_1+2/comb_bills_year_target/`   | 1 (delivery) + 2 (supply)   | Before: upgrade 0, default rates      |
| `run_3+4/comb_bills_year_target/`   | 3 (delivery) + 4 (supply)   | After (1-8): upgrade 2, default rates |
| `run_19+20/comb_bills_year_target/` | 19 (delivery) + 20 (supply) | After (1-9): upgrade 2, HP flat rates |
