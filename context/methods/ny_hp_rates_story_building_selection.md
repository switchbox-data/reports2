# NY HP rates: story building selection

The NY HP rates report profiles a single gas-heated building across multiple
charts to make the rate-design argument concrete. This document records which
building is currently used, how it was selected, and an alternative candidate
that was investigated.

## Population

The building is drawn from all **gas-heated, full-cooling (100% conditioned)**
homes statewide in ResStock, after excluding buildings with nonzero propane or
oil bills (so the visible bill components — electric + gas — equal the full
energy total with nothing hidden). This population contains ~6,500 buildings in
the `ny_20260307_r1-8_gascalcfix` batch.

## Population-level medians (for reference)

| Metric                                   |    P25 |    P50 |    P75 |
| ---------------------------------------- | -----: | -----: | -----: |
| Total energy bill (current)              | $2,082 | $2,904 | $4,084 |
| Total bill delta (gas→HP, default rates) |  -$197 |    -$7 |  +$352 |
| Electricity kWh % change                 |   +22% |   +50% |   +88% |
| Delivery bill % change                   |   +19% |   +40% |   +69% |
| Gas-scenario BAT (delivery)              |  -$300 |   -$90 |  +$178 |
| HP-scenario BAT (delivery)               |   -$89 |  +$359 |  +$957 |

## Current choice: building 168982

### How selected

`weighted_median_row(natgas_full_cooling, sort_col="energy_total")` — the
building at the weighted median of total energy bill among the full-cooling
natgas population. This is the default selection in `analysis.qmd`.

### Physical characteristics

| Attribute         | Value                                 |
| ----------------- | ------------------------------------- |
| Building type     | Single-family detached                |
| Location          | Buffalo, Erie County                  |
| Climate zone      | Cold                                  |
| Electric utility  | National Grid                         |
| Gas utility       | National Fuel Gas                     |
| Sq ft             | 1,228                                 |
| Stories           | 1                                     |
| Bedrooms          | 3                                     |
| Vintage           | Pre-1940                              |
| Wall construction | Wood frame, uninsulated               |
| Heating           | Gas furnace, 80% AFUE                 |
| Cooling           | Central AC, SEER 15, 100% conditioned |
| Income            | $35k–$40k                             |
| Tenure            | Owner                                 |
| Occupants         | 1                                     |

### Stats across all four scenarios

| Metric                | Gas + default | HP + default | Gas + seasonal | HP + seasonal |
| --------------------- | ------------: | -----------: | -------------: | ------------: |
| Elec supply bill      |          $737 |       $1,594 |           $743 |        $1,431 |
| Elec delivery bill    |          $962 |       $1,832 |           $995 |          $987 |
| Elec total bill       |        $1,699 |       $3,426 |         $1,738 |        $2,417 |
| Gas bill              |        $1,205 |         $301 |         $1,205 |          $301 |
| **Total energy bill** |    **$2,904** |   **$3,727** |     **$2,943** |    **$2,718** |

| Metric                    |     Value |
| ------------------------- | --------: |
| Elec kWh before           |     8,821 |
| Elec kWh after HP         |    19,080 |
| **Elec kWh % change**     | **+116%** |
| Gas kWh before            |    44,928 |
| Gas kWh after HP          |     2,981 |
| Total energy kWh % change |      -59% |

| BAT metric                        | Value |
| --------------------------------- | ----: |
| Gas BAT (delivery)                |    $0 |
| HP BAT (delivery, default rates)  | +$840 |
| HP BAT (delivery, seasonal rates) |  +$33 |

### Percentile profile

| Dimension         | Percentile |
| ----------------- | ---------: |
| Total energy bill |        P50 |
| Elec kWh % change |        P86 |
| HP BAT (delivery) |        P71 |
| Total bill delta  |        P90 |

### Strengths

- P50 on total energy bill — answers "what does the median-bill NYer pay, and
  what happens to them."
- Narratively strong: single-family home, owner-occupied, in Buffalo. The kind
  of building readers picture when they think about heat pump adoption.
- Clean BAT arc: $0 → +$840 → +$33. The entire cross-subsidy is caused by the
  switch; seasonal rates eliminate it.

### Weaknesses

- Electricity increase (+116%) is at P86 of the full-cooling population. The
  weighted median is +50%. This exaggerates how much electricity goes up after
  switching.
- HP BAT of $840 is at P71 — above the population median of $359.
- Bill delta of +$823 is at P90 — the typical full-cooling home sees
  essentially flat bills (-$7 median), not an $823 increase.
- The extreme electricity increase is because this building has very high gas
  usage (44,928 kWh) relative to baseline electricity (8,821 kWh). The percent
  change has a small denominator.

## Alternative candidate: building 305979

### How found

Nearest-neighbor search in (gas_bat, hp_bat) space, targeting the population
medians: gas_bat = -$90, hp_bat = +$359. Distances were IQR-normalized so the
two dimensions are comparable (gas BAT IQR = $479, HP BAT IQR = $1,046).
Building 305979 had a normalized distance of 0.04 — essentially sitting on the
population-median BAT point.

### Physical characteristics

| Attribute         | Value                                                    |
| ----------------- | -------------------------------------------------------- |
| Building type     | Multi-family with 2–4 units (3-unit building, top floor) |
| Location          | Queens, New York City                                    |
| Climate zone      | 4A (Mixed-Humid)                                         |
| Electric utility  | Con Edison                                               |
| Gas utility       | Con Edison                                               |
| Sq ft             | 1,138                                                    |
| Stories           | 3                                                        |
| Bedrooms          | 2                                                        |
| Vintage           | Pre-1940                                                 |
| Wall construction | Brick, 12-in, 3-wythe, uninsulated                       |
| Heating           | Gas furnace, 92.5% AFUE                                  |
| Cooling           | Central AC, SEER 13, 100% conditioned                    |
| Income            | $45k–$50k (30–60% AMI)                                   |
| Tenure            | Renter                                                   |
| Occupants         | 3                                                        |

### Stats across all four scenarios

| Metric                | Gas + default | HP + default | Gas + seasonal | HP + seasonal |
| --------------------- | ------------: | -----------: | -------------: | ------------: |
| Elec supply bill      |          $392 |         $653 |           $392 |          $652 |
| Elec delivery bill    |          $970 |       $1,446 |           $982 |          $952 |
| Elec total bill       |        $1,362 |       $2,099 |         $1,374 |        $1,604 |
| Gas bill              |        $1,554 |         $663 |         $1,554 |          $663 |
| **Total energy bill** |    **$2,916** |   **$2,762** |     **$2,928** |    **$2,267** |

| Metric                    |    Value |
| ------------------------- | -------: |
| Elec kWh before           |    5,694 |
| Elec kWh after HP         |    8,773 |
| **Elec kWh % change**     | **+54%** |
| Gas kWh before            |   18,672 |
| Gas kWh after HP          |    3,555 |
| Total energy kWh % change |     -49% |

| BAT metric                        |             Value |
| --------------------------------- | ----------------: |
| Gas BAT (delivery)                | -$101 (underpays) |
| HP BAT (delivery, default rates)  |             +$387 |
| HP BAT (delivery, seasonal rates) |  -$89 (underpays) |

### Percentile profile

| Dimension              | Percentile |
| ---------------------- | ---------: |
| Total energy bill      |        P50 |
| Elec kWh % change      |        P54 |
| Delivery bill % change |        P49 |
| HP BAT (delivery)      |        P51 |
| Total bill delta       |        P29 |

### Strengths

- Near-median on almost every relevant dimension simultaneously: total bill
  (P50), elec kWh change (P54), delivery change (P49), HP BAT (P51).
- More intuitive BAT arc: underpays -$101 → overpays +$387 → back to
  underpaying -$89. The gas-scenario home slightly underpays for delivery
  (which is realistic — the population median gas BAT is -$90), the switch
  creates a large cross-subsidy, and the seasonal rate restores it.
- Larger total-bill savings under seasonal rates: -$649/yr vs -$185 for
  168982.
- Electricity increase (+54%) is representative of the typical full-cooling
  home's experience.

### Weaknesses

- It's a top-floor apartment in a 3-unit multifamily building, not a
  single-family house. Readers may have a harder time picturing this as "their
  home."
- It's a renter. Renters don't make HVAC investment decisions, introducing a
  split-incentive complication that's tangential to the rate-design argument.
- It's in NYC (Con Edison territory), where the climate is mildest in the
  state. The cross-subsidy problem is less acute in mild-climate zones, which
  weakens the argument slightly.
- Bill delta of -$154 (P29) means this home actually saves money even under
  default rates — not representative of the median experience (-$7).

## Switching between buildings

In `analysis.qmd`, the building is selected at a single point:

```python
median_current_state = weighted_median_row(natgas_full_cooling)
median_bldg_id_state = median_current_state[BLDG_ID][0]
```

A commented-out override block for 305979 is provided immediately below. To
switch, uncomment that block. Everything downstream references
`median_bldg_id_state` and flows automatically.
