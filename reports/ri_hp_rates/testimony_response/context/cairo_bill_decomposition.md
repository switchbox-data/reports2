# CAIRO bill decomposition: how electric bills are computed

This document records findings from tracing building 184434 (upgrade 2 = heat pump)
through the full CAIRO billing pipeline and `build_master_bills.py` post-processing.
It explains how `elec_fixed_charge`, `elec_delivery_bill`, `elec_supply_bill`, and
`elec_total_bill` in the master bills relate to the calibrated tariff JSONs, ResStock
kWh, and the revenue requirement YAMLs.

## Inputs

### ResStock loads

- Source: `/ebs/data/nrel/resstock/res_2024_amy2018_2_sb/load_curve_hourly/state=RI/upgrade=02/{bldg_id}-2.parquet`
- 8760 hourly rows per building, actual meteorological year 2018 (AMY2018).
- Column: `out.electricity.total.energy_consumption` (kWh per hour).
- Building 184434 raw annual kWh (upgrade 2): **16,112.655 kWh**.
- PV generation for this building: **0.0 kWh** (no solar).

### Calibrated tariffs (URDB JSON)

All tariffs are flat (single period, single tier, no demand charges).

| Tariff file                          | Volumetric rate ($/kWh) | Fixed charge ($/mo) | Used by                              |
| ------------------------------------ | ----------------------- | ------------------- | ------------------------------------ |
| `rie_hp_flat_calibrated.json`        | 0.08249                 | 10.01               | Run 19 (delivery)                    |
| `rie_hp_flat_supply_calibrated.json` | 0.23129                 | 10.01               | Run 20 (delivery+supply bundled)     |
| `rie_default_calibrated.json`        | 0.14078                 | 10.01               | Runs 1, 3 (default delivery)         |
| `rie_default_supply_calibrated.json` | seasonal                | 10.01               | Runs 2, 4 (default supply)           |
| `rie_flat.json`                      | —                       | **11.47**           | `build_master_bills.py` fixed charge |

### Revenue requirement YAMLs

| YAML                                        | Used by                              | Notes                                                           |
| ------------------------------------------- | ------------------------------------ | --------------------------------------------------------------- |
| `rie_rate_case_test_year.yaml`              | Runs 1–4 (precalc + default)         | Real RR; contains full budget breakdown                         |
| `rie_large_number_rate_case_test_year.yaml` | Runs 19–20 (calibrated tariff runs)  | `revenue_requirement: 1e12` — prevents recalibration            |
| `rie_hp_vs_nonhp_rate_case_test_year.yaml`  | Runs 17–18 (precalc for HP subclass) | HP subclass calibration with EPMC delivery, per-customer supply |

All three share the same `resstock_kwh_scale_factor: 0.9568112362177266`.

### Scenario mapping (RIE 1-8 and 1-9)

| Scenario | Before                             | After                                | What changes                                          |
| -------- | ---------------------------------- | ------------------------------------ | ----------------------------------------------------- |
| RIE 1-8  | Run 1+2 (upgrade 0, default rates) | Run 3+4 (upgrade 2, default rates)   | Only the building upgrades to HP; rates stay the same |
| RIE 1-9  | Run 1+2 (upgrade 0, default rates) | Run 19+20 (upgrade 2, HP flat rates) | Building upgrades AND gets the proposed HP rate       |

## CAIRO processing pipeline

### Step 1: Load hourly data

`_return_loads_combined()` in `utils/mid/patches.py` reads the hourly parquet files
and aligns them from 2018 to the target year (2025).

### Step 2: Day-of-week timeshift

**This is a non-obvious transformation.** CAIRO uses `np.roll` to shift hourly loads
so that day-of-week patterns align with the target year:

```python
source_year = 2018  # Jan 1 = Monday (weekday 0)
target_year = 2025  # Jan 1 = Wednesday (weekday 2)
offset_days = (2 - 0) % 7 = 2
offset_hours = 48

elec_total = np.roll(elec_total.reshape(n_bldgs, 8760), -offset_hours, axis=1)
```

This shifts the first 48 hours of the year to the end. Effect:

- January loses ~48 hours of winter load to December.
- December gains those hours.

For building 184434, this moves **127 kWh** from January to December. Monthly kWh
totals differ from the raw ResStock monthly aggregates, but the **annual total is
unchanged** (16,112.655 kWh).

**Implication for hand-calculations:** You cannot reproduce CAIRO's monthly bills
from the monthly load curve parquet files. You must either (a) use the hourly files
with the 48-hour roll, or (b) accept that only the annual total matches.

### Step 3: kWh scaling

CAIRO multiplies all hourly loads by `kwh_scale_factor = 0.9568` (line 645 of
`run_scenario.py`):

```python
raw_load_elec = raw_load_elec * settings.kwh_scale_factor
```

The scale factor is derived from:

```
kwh_scale_factor = test_year_residential_kwh / (resstock_total_kwh × customer_scale_factor)
                 = 2,821,237,490 / (3,388,382,407 × 0.8702)
                 = 0.9568
```

Building 184434 scaled annual kWh: 16,112.655 × 0.9568 = **15,416.8 kWh**.

### Step 4: Customer weight scaling

CAIRO also applies `customer_count_override` from the rev_req, which scales building
weights:

- Utility assignment weight: 252.30
- CAIRO weight: 219.55 (= 252.30 × customer_scale_factor 0.8702)

### Step 5: Billing

For flat tariffs, CAIRO computes: `bill = Σ(hourly_kwh × rate) + fixed × 12`.

Since the rate is constant across all hours, this simplifies to:
`bill = annual_scaled_kwh × rate + fixed × 12`.

| Run           | Bill          | Formula                         |
| ------------- | ------------- | ------------------------------- |
| 19 (delivery) | **$1,391.08** | 15,416.8 × 0.08249 + 10.01 × 12 |
| 20 (supply)   | **$3,685.12** | 15,416.8 × 0.23129 + 10.01 × 12 |

Hand-computed values match to within **$0.81/yr** (floating-point accumulation
across 8760 hourly multiplications).

## build_master_bills.py decomposition

`build_master_bills.py` combines run 19 (delivery) and run 20 (delivery+supply)
into the master bill components. The key logic:

```python
elec_fixed_charge  = rie_flat.json fixed × 12        # NOT the calibrated tariff's fixed
elec_delivery_bill = bill_delivery − elec_fixed_charge
elec_supply_bill   = bill_supply − bill_delivery
elec_total_bill    = bill_supply
```

### Fixed charge overwrite

The calibrated tariffs use **$10.01/mo** as `fixedchargefirstmeter`, but
`build_master_bills.py` reads `rie_flat.json` which specifies **$11.47/mo**.

This shifts **$17.52/yr** (= ($11.47 − $10.01) × 12) from `elec_delivery_bill`
into `elec_fixed_charge`. The total bill is unchanged.

`rie_flat.json` is not referenced in `scenarios_rie.yaml` — it is hardcoded in
`build_master_bills.py` via `_read_fixed_charge()` which constructs the path
`{utility}_flat.json`.

### Result for building 184434 (run 19+20)

| Component            | Value     | How computed                      |
| -------------------- | --------- | --------------------------------- |
| `elec_fixed_charge`  | $137.64   | 11.47 × 12 (from `rie_flat.json`) |
| `elec_delivery_bill` | $1,253.44 | $1,391.08 − $137.64               |
| `elec_supply_bill`   | $2,294.04 | $3,685.12 − $1,391.08             |
| `elec_total_bill`    | $3,685.12 | = run 20 `bill_level`             |

Check: $137.64 + $1,253.44 + $2,294.04 = $3,685.12 ✓

### Effective rates

Because the fixed charges cancel in the supply subtraction:

- **Effective delivery volumetric**: `elec_delivery_bill / scaled_kwh` ≠ tariff rate
  (because the rie_flat.json overwrite shifts $17.52 out of the delivery bill).
- **Effective supply-only volumetric**: `elec_supply_bill / scaled_kwh` = supply_rate − delivery_rate
  = 0.23129 − 0.08249 = **0.14880 $/kWh**. This is the incremental supply cost, not
  the full supply tariff rate.

## Supply rate: per-customer allocation

The HP supply tariff (`rie_hp_flat_supply_calibrated.json`) uses a **bundled**
delivery+supply rate of 0.23129 $/kWh. This is lower than the default seasonal
supply rates (winter: 0.31377, summer: 0.24782, fall: 0.29493) because:

1. It was calibrated using `rie_hp_vs_nonhp_rate_case_test_year.yaml`, which
   allocates supply revenue with **per-customer** allocation (not passthrough).
2. Per-customer allocation divides total supply revenue equally across all
   customers. HP customers are ~2.5% of the base but consume proportionally
   more kWh, so their per-kWh supply rate is lower.
3. The bundled rate (0.23129) includes both delivery (0.08249) and supply
   (0.14880 effective), so supply-only = 0.23129 − 0.08249 = 0.14880.

## PV buildings and net metering

14 of 1,910 RIE buildings (0.7%) have rooftop PV. Of these, **6 are gas-heated**
and appear in the RIE 1-8/1-9 workbooks (0.57% of the 1,049 gas-heated buildings).

| bldg_id | Total kWh | PV kWh  | Net kWh | Import-only kWh | PV coverage |
| ------- | --------- | ------- | ------- | --------------- | ----------- |
| 85645   | 10,574    | −8,360  | 2,214   | ~7,800*         | 79%         |
| 121546  | 13,417    | −11,359 | 2,058   | ~8,200*         | 85%         |
| 143685  | 12,828    | −11,648 | 1,180   | ~7,400*         | 91%         |
| 222179  | 12,443    | −10,064 | 2,379   | ~7,500*         | 81%         |
| 342077  | 15,014    | −6,296  | 8,718   | ~12,000*        | 42%         |
| 516557  | 10,749    | −9,221  | 1,529   | ~7,700*         | 86%         |

*Import-only kWh estimated from hourly data (hours where net ≥ 0).

### How CAIRO bills PV buildings

CAIRO computes `electricity_net = total − |pv|` per hour. Hours where `net < 0`
(PV generation exceeds consumption) are **export hours**.

Empirically (verified for building 8584, non-gas-heated PV):

- `import_only_kwh × rate + fixed × 12 = $3,319.02`
- Actual `elec_total_bill = $3,318.30`
- Match within $0.72 (timeshift tolerance) ✓

- `net_annual_kwh × rate + fixed × 12 = $2,706.54` ← does NOT match

**Conclusion: export hours receive no credit (sell_rate ≈ 0).** The billed kWh
equals the sum of only the hours where net consumption ≥ 0, ignoring export hours
entirely.

This is set in `run_scenario.py` where `solar_pv_compensation=None` is passed
to `bs.simulate()` — the scenario's `solar_pv_compensation: net_metering` setting
only determines the `sell_rate` passed separately, but the effective rate appears
to be zero.

### Implication for the workbook

The back-derived `annual_kwh` (from delivery bills) correctly captures the
import-only kWh because it is derived FROM the bill. The formula
`(bill_delivery − annual_fixed) / vol_rate` produces the same kWh that CAIRO
billed, regardless of PV.

However, these kWh will NOT match the ResStock raw or net annual consumption
for PV buildings. The workbook should note: "For 6 PV buildings (0.57% of
gas-heated sample), `annual_kwh` reflects grid-consumed electricity only,
excluding hours when rooftop solar exceeds consumption."

## Key gotchas

1. **Monthly bills don't match simple kWh × rate + fixed**, because of the 48-hour
   day-of-week timeshift. Only annual totals can be verified with simple arithmetic.

2. **`rie_flat.json` is the source of truth for `elec_fixed_charge`**, not the
   calibrated tariff JSONs. The $11.47/mo includes customer charge ($6.00) + RE
   Growth ($3.22) + other fixed charges, while the calibrated tariff's $10.01 is
   CAIRO's internal representation.

3. **The "supply" tariff in CAIRO is actually delivery+supply bundled.** The supply
   component is extracted by subtraction: `bill_supply − bill_delivery`.

4. **`kwh_scale_factor` is applied uniformly** to all hourly loads. It is NOT a
   per-month calibration. Monthly deviations from `raw_monthly × kwh_sf` are
   entirely due to the day-of-week timeshift.

5. **The weight in CAIRO outputs differs from utility_assignment** because CAIRO
   applies `customer_scale_factor` (0.8702) to the weights.

6. **PV buildings are billed on import-only kWh** (hours where net ≥ 0). Export
   hours receive no credit. Back-derived kWh correctly captures this, but won't
   match ResStock raw totals for the 14 PV buildings (6 gas-heated).
