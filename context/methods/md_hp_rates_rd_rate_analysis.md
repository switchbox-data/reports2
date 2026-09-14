# Schedule RD Rate Analysis — MD HP Rates

This document records the rate landscape, sources, analysis decisions, and known issues
for the Schedule RD cost-vs-charge analysis in the Maryland HP rates testimony
(`reports/md_hp_rates/`).

## What Schedule RD is

Schedule RD ("Residential Delivery and Energy Time-Of-Use — Electric") is BGE's
residential TOU rate. It emerged from Public Conference 44 (PC44),
the Commission's multi-year rate design investigation into time-varying rates.

Schedule RD defines **time-of-use delivery service charges** (distribution) in its
own tariff sheet. Generation and transmission are billed through **Rider 1 —
Standard Offer Service**, which applies TOU rates specific to Schedule RD that
differ from the flat rates applied to Schedule R customers. EmPOWER Maryland,
the environmental surcharge, and the customer charge are flat riders applied
identically to Schedule R and Schedule RD customers.

In other words, for Schedule RD, **everything volumetric is TOU**: distribution
(tariff sheet), generation (Rider 1), and transmission (Rider 1). Only EmPOWER
and the environmental surcharge remain flat.

**Key confirmation:** The ECOSS treats R and RD as one customer class (Karas
testimony line 121: "For purposes of the ECOSS, Schedule R includes residential
customers taking electric service under Schedules EV and RD"). The flat riders
(EmPOWER, environmental surcharge, customer charge) are class-level charges and
therefore identical across schedules — but Rider 1 SOS defines schedule-specific
TOU generation and transmission rates.

RD is designed to be **revenue-neutral** to Schedule R: the same number of
customers consuming the same total kWh would produce the same total delivery
revenue under either schedule (E-Sheet E-13).

## Rate sources

### Current filed rates (Rate Year 3)

Source: [BGE Schedule RD tariff sheet (P.S.C. Md. E-6, Suppl. 749)](https://azure-na-assets.contentstack.com/v3/assets/blt71bfe6e8a1c2d265/bltd9617a8f40ce427f/6a5fb7de0ddda05c707141b1/P3_SCH_RD_1.pdf),
filed 04/16/2026, effective 06/01/2026.

Also saved locally: `context/sources/md_hp_rates/BGE_SCH_RD_1.pdf` (and `.md` extract).

| Component                        | Rate         |
| -------------------------------- | ------------ |
| Customer Charge                  | $10.00/month |
| Delivery Service Charge On-Peak  | $0.08874/kWh |
| Delivery Service Charge Off-Peak | $0.03736/kWh |

Rate history from the same tariff sheet:

| Rate Year | Effective   | Customer Charge | On-Peak  | Off-Peak |
| --------- | ----------- | --------------- | -------- | -------- |
| 1         | Jan 1, 2024 | $9.30/month     | $0.10780 | $0.02856 |
| 2         | Jan 1, 2025 | $9.65/month     | $0.11227 | $0.02939 |
| 3         | Jan 1, 2026 | $10.00/month    | $0.08874 | $0.03736 |

### Karas proposed rates (rate case)

Source: Direct Testimony of Julia A. Karas, E-Sheet E-13
(`context/sources/md_hp_rates/mdpuc_331766_direct_testimony_karas.md`, lines 542-555).
These rates are proposed to be effective August 1, 2026.

| Component                        | Rate         |
| -------------------------------- | ------------ |
| Customer Charge                  | $11.00/month |
| On-Peak Delivery Service Charge  | $0.10733/kWh |
| Off-Peak Delivery Service Charge | $0.04291/kWh |

Revenue-neutral to proposed Schedule R delivery service charge of $0.05699/kWh.

The rate shaping uses a **60/40 split**: 60% of primary distribution system costs
are recovered in the on-peak period and 40% in the off-peak period, consistent
with Commission Order No. 91917 and the May 20, 2026 Letter Order.

From E-Sheet E-13: on-peak kWh represent 21.9% of total kWh but produce 41.2%
of delivery service revenue; off-peak kWh are 78.1% of total kWh and produce
58.8% of revenue.

### Schedule R rates used in the existing analysis

The representative_home notebook uses pre-rate-case rates from
`bge_monthly_rates_2025.yaml` (April 2025 – March 2026):

- **Distribution** = `core_delivery_rate` + `environmental_surcharge`:
  ~$0.04766–$0.04874/kWh flat (varies by month)
- **Transmission** = `transmission_rate_adjustment`: ~$0.01682–$0.02322/kWh flat
- **EmPOWER** = `empower_maryland_charge`: ~$0.01028–$0.01310/kWh flat

These YAML rates are the same vintage as the current filed RD rates (Rate Year 3),
making them an apples-to-apples basis for comparison.

### URDB JSON (`bge_rd_default.json`)

The URDB delivery JSON (`bge_rd_default.json`) bundles distribution TOU +
transmission TOU + EmPOWER + environmental surcharge into a single TOU energy
rate per month per period. The URDB all-in JSON (`bge_rd_default_supply.json`)
adds generation TOU on top. These are what CAIRO uses for per-building bill
calculation.

Decomposition (verified against Rider 1):

- **Delivery JSON** = distribution (tariff sheet) + transmission (Rider 1) + EmPOWER + env surcharge
- **All-in JSON** = delivery + generation (Rider 1)
- **Implied supply** (all-in − delivery) = **generation only** (matches Rider 1 exactly)

The `energyratestructure` contains 18 rate tiers (indices 0-17), organized as
paired off-peak/on-peak rates for each of the 12 months.

The TOU windows encoded in `energyweekdayschedule` match the current filed /
Karas proposed windows (3pm-8pm summer, 6am-9am + 5pm-9pm non-summer), not the
original PC44 pilot windows.

### Rider 1 SOS rates (generation + transmission)

Source: [BGE Rider 1 — Standard Offer Service (P.S.C. Md. E-6, Suppl. 751)](https://azure-na-assets.contentstack.com/v3/assets/blt71bfe6e8a1c2d265/blt970ee32f55c20fde/6a95a29b7935845fd59d7079/Rdr_1_8.pdf),
filed 05/18/26, effective 06/01/26.

Also saved locally: `context/sources/md_hp_rates/BGE_Rdr_1_SOS.pdf` (and `.md` extract).

**Schedule R** (flat):

| Season     | Generation | Transmission | Total SOS |
| ---------- | ---------- | ------------ | --------- |
| Summer     | 12.519¢    | 2.228¢       | 14.747¢   |
| Non-Summer | 12.995¢    | 2.228¢       | 15.223¢   |

**Schedule RD** (TOU):

| Season     | Period   | Generation | Transmission | Total SOS |
| ---------- | -------- | ---------- | ------------ | --------- |
| Summer     | On-Peak  | 25.990¢    | 6.766¢       | 32.756¢   |
| Summer     | Off-Peak | 9.213¢     | 1.114¢       | 10.327¢   |
| Non-Summer | On-Peak  | 21.993¢    | 5.773¢       | 27.766¢   |
| Non-Summer | Off-Peak | 10.266¢    | 1.163¢       | 11.429¢   |

Key finding: for Schedule RD, **both generation and transmission are TOU**. The
PC44 TOU Rate Design Work Group report confirms this design:

> "Starting from the auction-based SOS rates, the Joint Utilities will add
> transmission and estimated capacity costs into the peak periods to create the
> on- to off-peak differential."
> — `context/sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md`, line 94

The Schedule RD tariff sheet itself states: "Generation and Transmission
Market-Priced Service Charges can be found on www.bge.com and Rider 1 –
Standard Offer Service."

**TOU windows for Rider 1 rates:** Rider 1 does not independently define peak
windows; it labels rates as "On-Peak" and "Off-Peak" by season, deferring to
each schedule's own TOU window definitions. For Schedule RD, the distribution
and Rider 1 SOS rates share the same peak/off-peak window definitions from the
Schedule RD tariff sheet.

## TOU windows

### Current filed = Karas proposed (identical)

Source: BGE Schedule RD tariff sheet, page 2 (P.S.C. Md. E-6, Suppl. 723,
filed 08/29/2024, effective 10/01/2024):
[Rider 1 PDF](https://azure-na-assets.contentstack.com/v3/assets/blt71bfe6e8a1c2d265/blt970ee32f55c20fde/6a95a29b7935845fd59d7079/Rdr_1_8.pdf)

Also confirmed in Karas testimony lines 615-627.

**Summer (June–September):**

- On-Peak: weekdays 3pm–8pm (hours ending 16–20), excluding holidays
- Off-Peak: all other times

**Non-Summer (October–May):**

- On-Peak: weekdays 6am–9am (hours ending 7–9) **and** 5pm–9pm (hours ending
  18–21), excluding holidays
- Off-Peak: all other times

**DST transition adjustment:** The non-summer on-peak periods begin and end one
hour later during the transition between Standard Time and Daylight Saving Time
(second Sunday in March to first Sunday in April; last Sunday in October to first
Sunday in November).

**Holidays (always off-peak):** All hours on Saturdays and Sundays, plus:
New Year's Day, President's Day, Good Friday, Memorial Day, Independence Day,
Labor Day, Thanksgiving, Christmas, and the Monday following any that fall on
Sunday.

### History: how the windows changed

The **original PC44 pilot** (2018) used different windows:

- Summer: 2pm–7pm weekdays (5 hours)
- Non-Summer: 6am–9am weekdays only (3 hours)
- Source: PC44 Rate Design Final Report
  (`context/sources/md_hp_rates/mdpuc_218934_pc44_rate_design_final_report.md`,
  line 323)

The **PC44 TOU Rate Design Work Group** subsequently recommended two changes for
BGE (see `context/sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md`,
lines 81-90):

1. **Summer shifted 1 hour later:** 2pm–7pm → 3pm–8pm
2. **Non-summer gained an evening peak:** 6am–9am → 6am–9am + 5pm–9pm

These updated windows were implemented in Suppl. 723 (effective 10/01/2024) and
are what is currently filed. Karas does **not** propose changing the windows.

### Impact on on-peak hour count

| Window version      | Summer hours/day | Non-summer hours/day | Approx. annual on-peak hours |
| ------------------- | ---------------- | -------------------- | ---------------------------- |
| Original PC44 pilot | 5                | 3                    | ~1,000                       |
| Current / proposed  | 5                | 7                    | ~1,650                       |

### Testimony error

The expert testimony (lines 805, 861) describes the original PC44 pilot windows,
not the currently filed windows. Specifically:

- Line 805 says "weekdays from 2pm to 7pm in summer" — should be 3pm to 8pm
- Line 805 says "weekdays from 6am to 9am in winter" — omits the 5pm–9pm evening
  peak
- Line 861 says "3 hours per weekday in winter" — should be 7 hours
- Line 861 says "roughly 1,000 on-peak hours" — should be ~1,650

These errors originated from relying on the PC44 Rate Design Final Report (2018)
rather than the current tariff sheet. The work group's later adjustments
(documented in the 2021 report, implemented in Suppl. 723 effective 10/01/2024)
were not reflected.

## Analysis decisions

### Comparison basis

The cost-vs-charge chart compares **Schedule R before HP → Schedule RD after HP**
(a cross-tariff comparison). This represents the realistic policy scenario where
a customer currently on Schedule R installs a heat pump and switches to RD.

### Population

The "all fossil fuel" representative home — the weighted average across all
fossil-fuel-heated homes in BGE's service territory. This is consistent with the
population used in Section III of the testimony.

### What changes vs. what stays the same

| Component     | Before HP (Schedule R)        | After HP (Schedule RD)                              |
| ------------- | ----------------------------- | --------------------------------------------------- |
| Distribution  | YAML flat rate × monthly kWh  | TOU rates × hourly kWh (tariff sheet, non-seasonal) |
| Transmission  | YAML flat rate × monthly kWh  | TOU rates × hourly kWh (Rider 1, seasonal)          |
| Generation    | YAML flat rate × monthly kWh  | TOU rates × hourly kWh (Rider 1, seasonal)          |
| EmPOWER       | YAML flat rate × monthly kWh  | Same YAML flat rate × monthly kWh (**unchanged**)   |
| Marginal cost | Hourly MC × hourly kWh (8760) | Same computation (**unchanged**)                    |

Distribution, transmission, and generation all change from flat to TOU. The left
bar of the cost-vs-charge chart (marginal cost) and the EmPOWER component are
identical to the Schedule R chart. The right bar uses TOU distribution + TOU
transmission. The 4-bar total bill chart uses TOU generation for the supply
(orange) segment and TOU transmission in the delivery (blue) segment.

### Rate vintage consistency

The current filed RD rates (Rate Year 3, effective June 2026) are the same
vintage as the YAML pre-rate-case R rates used in the existing Schedule R
analysis. This gives an apples-to-apples comparison for the cost-vs-charge chart.

Karas's proposed RD rates (proposed effective August 2026) are from the rate case
being litigated. Computing at both vintages lets us show the result at the rate
level currently in effect and at the proposed rate level.

### Environmental surcharge handling

The environmental surcharge ($0.00015/kWh flat) is negligible (~$1.80/year at
12,000 kWh). In the existing R analysis, it is bundled into the "Distribution"
component. For the RD analysis, it is added as a flat adder on top of the TOU
delivery service charges, maintaining consistency with the R analysis.
