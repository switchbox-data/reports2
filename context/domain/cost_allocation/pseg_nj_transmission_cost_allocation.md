# PSE&G transmission cost allocation

How transmission costs are set, allocated, and billed on a PSE&G residential electric bill. Unlike distribution, where PSE&G designs its own rates in a BPU rate case, transmission is governed by FERC through PJM and flows to retail customers as a passthrough. This document explains the PJM mechanisms, how PSE&G converts them into retail charges, and what it means for heat pump customers.

Based on the PSE&G electric tariff (B.P.U.N.J. No. 17 Electric), PJM's OATT, and the 2023 rate case filings (Docket No. ER23120924).

## Why transmission is different from distribution

PSE&G's distribution system (substations, primary circuits, secondary wire, service drops) is entirely PSE&G's. PSE&G owns it, the BPU regulates it, and PSE&G designs the rates in state rate cases. The distribution COSS and rate design described in the companion document are a state-level proceeding.

Transmission is different. The high-voltage grid that moves power from generators to distribution substations is part of a **regional** system operated by PJM Interconnection, the Regional Transmission Organization covering 13 states plus D.C. Transmission facilities may be owned by PSE&G, but the rates are set at the **federal** level — FERC approves the revenue requirements, and PJM's Open Access Transmission Tariff (OATT) governs how those costs are allocated to load-serving entities (LSEs) across the region. PSE&G then passes through the resulting costs to retail customers.

This means transmission cost allocation is **not** something PSE&G decides in a BPU rate case. When Swetz designed the distribution rates, he explicitly excluded transmission: "They do not include the costs for the Company's Transmission business, which is under the jurisdiction of the Federal Energy Regulatory Commission" (Swetz P-9E, p. 16).

## How PJM transmission costs are set

### FERC formula rates

Each transmission owner (TO) in PJM — PSE&G, Atlantic City Electric, Jersey Central Power & Light, PECO, BGE, Dominion, etc. — files a **formula rate** with FERC. The formula rate takes the TO's actual annual costs (revenue requirement: return on rate base, depreciation, O&M, taxes) and produces a `$/MW-year` Network Integration Transmission Service (NITS) rate for that TO's zone.

PSE&G's current NITS rate is **`$155,206.48` per MW per year** — meaning it costs about `$155,000` to reserve 1 MW of continuous transmission service on PSE&G's zone of the PJM grid for a year.

Formula rates update annually (or more frequently with FERC approval), based on the TO's actual costs. The BPU does not approve or modify these rates — they are FERC-jurisdictional.

### Regional Transmission Expansion Plan (RTEP) charges

On top of the base NITS rate, PJM allocates the costs of **transmission enhancement projects** — new lines, substations, and upgrades built to maintain reliability or reduce congestion across the regional grid. These are called RTEP charges, and they are billed separately from the base NITS rate, broken out by the TO that built each project.

The PSE&G tariff lists 15 separate RTEP line items from TOs across the PJM footprint:

| Transmission Owner                             | Charge (per MW per month) |
| ---------------------------------------------- | ------------------------: |
| Trans-Allegheny Interstate Line Company        |                    $43.31 |
| Virginia Electric and Power Company (Dominion) |                    $91.99 |
| PPL Electric Utilities Corporation             |                   $182.71 |
| Jersey Central Power and Light                 |                    $70.42 |
| Atlantic City Electric Company                 |                     $8.11 |
| Mid Atlantic Interstate Transmission           |                    $22.48 |
| PECO Energy Company                            |                    $17.49 |
| Silver Run Electric                            |                    $38.53 |
| Others (8 TOs)                                 |               $0.01–$8.80 |

PSE&G customers pay a share of these regional projects because PJM allocates RTEP costs based on who benefits from the investment (using a formula that considers load ratio share and sometimes a "beneficiary pays" allocation for specific projects). A new 500 kV line built in Virginia by Dominion that improves reliability for the whole PJM region will show up as a small charge on PSE&G customers' bills.

### Other FERC-jurisdictional charges

The tariff also lists:

- **EL05-121**: `$77.50/MW/month` — a legacy FERC settlement charge
- **Reliability Must Run (RMR)**: `$0.00/MW/month` currently — payments to keep specific generators online for grid reliability
- **Seams Elimination Cost Assignment (SECA)**: `$0.00/MW/month` currently — costs from interregional coordination (PJM–MISO, PJM–NYISO boundaries)

### Total transmission rate

All of these components add up to a combined charge of **`$13.5213` per kW of Transmission Obligation per month** (`$14.4171` including SUT). That's about `$162/kW-year`.

## How transmission costs are allocated to customers

### The Transmission Obligation

Each customer has a **Transmission Obligation** measured in kilowatts. This is the customer's share of the total transmission service that PSE&G must procure from PJM to serve its load.

The tariff defines it (Section 9.1) as follows: the Transmission Obligation is determined "in a similar manner to the Generation Obligation" — meaning it's based on the customer's **Peak Load Share** of the overall summer peak load assigned to PSE&G's transmission zone by PJM.

For a residential customer without interval metering (before AMI), the Peak Load Share is estimated from:

1. The **load shape** of a representative sample of customers on the same rate schedule
2. The customer's **actual or estimated summer energy use** (or summer peak demand, if metering allows)
3. **PJM assigned transmission capacity related factors**, updated at least annually

In practice, this means residential customers' transmission costs are allocated based on how much they contribute to the **summer peak**. A customer who uses more electricity in summer (heavy AC use) gets a bigger Transmission Obligation — and pays more for transmission — than a customer with the same annual consumption but a flatter load profile.

### PJM's Network Service Peak Load (NSPL)

Behind the scenes, PJM determines each zone's total transmission obligation using the **Network Service Peak Load (NSPL)**. NSPL is **not** the same as the 5CP used for capacity allocation:

| Attribute       | Capacity (5CP / PLC)                                 | Transmission (NSPL)                                       |
| --------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| Peak selection  | Five highest non-holiday weekday hours, Jun 1–Sep 30 | Single zonal peak hour (varies by zone; typically annual) |
| Window          | Summer only                                          | Twelve months ending October 31 (for most PJM TOs)        |
| Granularity     | Customer-level PLC                                   | Zonal total; EDCs allocate to customers                   |
| Used for        | Capacity obligation (RPM)                            | Transmission obligation (OATT NITS charges)               |
| FERC tariff ref | RAA, PJM Manual 19 §4.3                              | PJM OATT Schedule 9, PJM Manual 27                        |

The key point: NSPL is used to determine **how much** total transmission service PSE&G must procure from PJM. PSE&G then allocates that total to individual customers via the Peak Load Share methodology in the tariff.

## How transmission shows up on a residential bill

### For RS customers: flat per-kWh charge

For residential rate schedules (RS, RHS, RLM, WH, WHS, HS), transmission costs are converted into a **flat per-kWh charge** that appears on the bill as part of the BGS (Basic Generation Service) charges.

The current RS transmission charge is **`$0.060016/kWh`** (excl. SUT) — the same rate in summer and winter, and the same for every kWh regardless of when it was consumed.

This is a significant simplification. The underlying cost is demand-based (driven by the customer's Peak Load Share at the summer peak), but the retail charge is volumetric (per kWh). The conversion works by taking the total transmission revenue requirement for the RS class, dividing by the RS class's total annual kWh, and setting a flat rate.

The result is that **transmission cost recovery from residential customers does not differentiate by time of use**. A kWh consumed at 3 am in January costs the same in transmission charges as a kWh consumed at 5 pm in August — even though only the August kWh contributed to the peak that actually determines the transmission obligation.

### For RS-TOU 3P customers: time-differentiated transmission

The TOU rate introduces time differentiation for transmission:

| Period   | Hours                 |    Summer |    Winter |
| -------- | --------------------- | --------: | --------: |
| On-Peak  | 4pm–9pm weekdays      | $0.136807 | $0.068404 |
| Mid-Peak | 6am–4pm, 9pm–midnight | $0.068404 | $0.068404 |
| Off-Peak | Midnight–6am          | $0.000000 | $0.000000 |

Key features of the TOU transmission design:

- **Off-peak hours pay zero transmission charges.** A customer who shifts all consumption to midnight–6am pays nothing for transmission.
- **Summer on-peak is 2× winter on-peak.** This reflects that the system peak (and thus the transmission obligation) is a summer phenomenon.
- **Mid-peak is the same in summer and winter.** This is the "baseline" transmission rate.
- The rates are revenue-neutral to the RS flat charge — if the entire RS class moved to RS-TOU 3P with no change in consumption, total transmission revenue would be the same.

### For GLP and LPL customers: demand-based (per kW)

For commercial and industrial customers on GLP and LPL schedules, transmission is billed directly as a **demand charge** per kW of Transmission Obligation — `$13.5213/kW/month`. These customers have interval meters, so their Transmission Obligation is calculated from their actual measured Peak Load Share. This is the most cost-reflective approach: the charge is proportional to the customer's actual contribution to the peak.

## The full anatomy of a residential transmission charge

Here's how to trace the chain from FERC to a customer's bill for a residential customer:

**Step 1 — FERC sets the rates:** PSE&G's formula rate produces a NITS rate of `$155,206.48/MW-year`. RTEP charges from 15 TOs add costs. Total: `$162.26/kW-year` (or `$13.52/kW-month`).

**Step 2 — PJM determines the zone's total obligation:** PJM calculates PSE&G's zone-level NSPL — the total MW of transmission service PSE&G must procure.

**Step 3 — PSE&G allocates to rate classes:** Using load research data, PSE&G determines each rate class's share of the zone's summer peak. RS, RHS, etc. each get a portion of the total Transmission Obligation.

**Step 4 — Class Transmission Obligation × rate = class revenue requirement:** The RS class's total Transmission Obligation (in kW) × `$13.52/kW-month` × 12 months = the annual transmission revenue that must be collected from RS customers.

**Step 5 — Convert to per-kWh for residential billing:** RS transmission revenue requirement ÷ RS annual kWh = `$0.060016/kWh`. Every RS customer pays this flat rate on every kWh.

**Step 6 — Bill the customer:** The transmission charge is bundled into the BGS supply charges on the bill. The customer sees a single BGS rate that includes energy, capacity, and transmission — not broken out separately for most billing purposes.

## Comparison with distribution cost allocation

| Feature                 | Distribution                                        | Transmission                                            |
| ----------------------- | --------------------------------------------------- | ------------------------------------------------------- |
| Who sets rates          | BPU (state rate case)                               | FERC (formula rates)                                    |
| Who operates the system | PSE&G                                               | PJM (regional)                                          |
| Cost allocation method  | 6-segment COSS (NCP and CP)                         | Peak Load Share of PJM zonal summer peak (NSPL-derived) |
| Residential rate design | Per-kWh, summer > winter (System Delivery)          | Per-kWh, flat (no seasonal differential for RS)         |
| TOU differentiation     | Yes — summer on-peak vs mid vs off                  | Yes — same period structure as distribution TOU         |
| Rate case frequency     | Every few years                                     | Annual formula rate updates                             |
| Regional cost sharing   | None — PSE&G costs allocated to PSE&G customers     | Yes — RTEP costs from other TOs appear on PSE&G bills   |
| Peak definition         | System CP (summer afternoon, e.g. Aug 9 2022 4-5pm) | NSPL (zonal peak, 12 months ending Oct 31)              |

## Relative size: transmission vs distribution

For an RS customer using 7,800 kWh/year (PSE&G's reference residential usage):

| Component          | Annual cost (approx, excl. SUT) | Share of delivery |
| ------------------ | ------------------------------: | ----------------: |
| Distribution       |                           ~$468 |               50% |
| Transmission       |                           ~$468 |               50% |
| **Total delivery** |                           ~$936 |              100% |

Distribution and transmission are roughly equal in magnitude for PSE&G residential customers. This is unusual — in many jurisdictions, distribution is significantly larger. PSE&G's distribution rates are historically low (the company went years without a base rate case), while PJM transmission costs have risen substantially due to RTEP investment.

The distribution rate varies by season (~`$0.045/kWh` winter, ~`$0.077/kWh` summer), while the RS transmission rate is flat (`$0.060/kWh`). Together, the summer delivery rate is about `$0.137/kWh` and the winter rate is about `$0.105/kWh`.

## Why this matters for heat pumps

### Transmission is flat — distribution is seasonal

For RS customers, the distribution charge explicitly puts System Delivery costs in summer only. But the transmission charge is flat year-round. This means:

- A heat pump customer who adds 5,000 kWh of winter consumption pays `$0.060 × 5,000 = $300` in additional transmission charges, even though that winter consumption may contribute very little to the summer peak that actually drives transmission costs.
- The same 5,000 kWh in summer would cost the same `$300` in transmission — but it would also carry an additional ~`$0.032/kWh` ($160) in System Delivery distribution charges.

The flat transmission rate **cross-subsidizes** in the other direction from distribution: it over-allocates transmission costs to off-peak and winter usage (which doesn't cause the peak) and under-allocates to on-peak summer usage (which does). For heat pump customers who add winter load, this is a disadvantage — they're paying transmission costs that weren't caused by their winter consumption.

### TOU fixes this for opt-in customers

The RS-TOU 3P rate addresses this: off-peak transmission is `$0.00/kWh`, so a heat pump customer who charges overnight or runs their heat pump during off-peak hours pays no transmission. The summer on-peak rate (`$0.137/kWh`) is much higher, correctly concentrating costs on the hours that drive the system peak.

But RS-TOU is voluntary and opt-in. The vast majority of residential customers remain on the flat RS rate, where the transmission cross-subsidy persists.

### RTEP costs are rising

PJM transmission enhancement costs have grown rapidly and are projected to continue growing as the grid is expanded for renewable integration, electrification, and data center load. The 15 RTEP line items in the tariff represent billions of dollars of regional investment flowing through to PSE&G customers. As these costs grow, the flat-rate allocation becomes a larger issue — the gap between what a kWh of winter off-peak load "costs" in transmission (essentially zero) and what it's charged (the same `$0.060/kWh` as a summer peak kWh) widens.

## Sources

Extracts are under `context/sources/nj_hp_rates/`. Citation keys are searchable in Zotero.

- **PSE&G Electric Tariff, B.P.U.N.J. No. 17 Electric (current)** — [`pseg_electric_tariff_17_current.md`](../../sources/nj_hp_rates/pseg_electric_tariff_17_current.md) · `pseg_ElectricTariffBPUNJ_2026` · Sheets 75–84 (BGS Supply Charges including transmission), Section 9.1 (Transmission Obligation, Peak Load Share), Sheet 70 (Infrastructure Improvement Program). The primary source for all current transmission rates and the retail billing mechanism.
- **Swetz Direct Testimony (Exhibit P-9E)** — [`njbpu_er23120924_swetz_p9e_electric.md`](../../sources/nj_hp_rates/njbpu_er23120924_swetz_p9e_electric.md) · `swetz_DocketER23120924Direct_2023` · pp. 16 (transmission excluded from COSS), 51–53 (TOU transmission rate design). Confirms distribution COSS is "wires only" and that transmission is FERC-jurisdictional.
- **Stipulation of Settlement** — [`njbpu_er23120924_stipulation.md`](../../sources/nj_hp_rates/njbpu_er23120924_stipulation.md) · `pseg_DocketER23120924Stipulation_2024` · Paragraphs 29–31 (RS-TOU 3P approval, revenue neutrality, CIP treatment).
- **Faruqui Direct Testimony (Exhibit P-10)** — [`njbpu_er23120924_faruqui_p10_tou.md`](../../sources/nj_hp_rates/njbpu_er23120924_faruqui_p10_tou.md) · `faruqui_DocketER23120924Direct_2023` · TOU rate design rationale and period definitions (4–9pm on-peak, midnight–6am off-peak).
- **PJM OATT, Schedule 9** — Network Integration Transmission Service (NITS) rate methodology. Not extracted; see [PJM OATT](https://agreements.pjm.com/eTariff/) and [PJM Manual 27](https://www.pjm.com/-/media/DotCom/documents/manuals/m27.pdf) (OATT Accounting).
- **PJM Manual 19 §4.3** — Peak Load Allocation (5CP for capacity; NSPL for transmission). Not extracted; see [PJM Manual 19](https://www.pjm.com/-/media/DotCom/documents/manuals/m19.pdf).
