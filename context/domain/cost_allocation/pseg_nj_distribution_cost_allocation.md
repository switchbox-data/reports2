# PSE&G electric distribution cost allocation

How PSE&G allocates its electric distribution costs to customer classes and designs rates from that allocation. Based on the testimony of Stephen Swetz (Exhibit P-9E) in the 2023 base rate case (Docket No. ER23120924), and the rates as adopted in the stipulation and effective tariff (B.P.U.N.J. No. 17 Electric).

## The six-segment COSS

PSE&G's cost of service study ("COSS") splits all distribution costs into six functional segments. Each segment has its own cost pool and its own allocation method:

| Segment              | What it covers                                                                                                                                 | How costs are allocated to rate classes             |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **Access**           | Service drops — the wire from the shared distribution system to each customer's premises (FERC Account E369)                                   | Special study of service drop unit costs by class   |
| **Local Delivery**   | Equipment shared among a small number of customers: secondary wire, line transformers, 50% of primary circuits, 21.1% of subtransmission lines | Sum of individual customer peak demands (NCP basis) |
| **System Delivery**  | Bulk distribution: substations, 50% of primary circuits, 78.9% of subtransmission lines                                                        | Each class's contribution to system peak (CP basis) |
| **Street Lighting**  | Luminaires, brackets, and poles used exclusively for street lighting                                                                           | Directly assigned to lighting rate schedules        |
| **Customer Service** | Billing, payment, collection, account maintenance                                                                                              | Separate study of customer service functions        |
| **Measurement**      | Meters and meter reading                                                                                                                       | Relative installed cost of new AMI meters           |

The first three segments — Access, Local Delivery, and System Delivery — are the ones that matter most. They form the core of the distribution business and account for the vast majority of distribution revenue requirements.

## CP vs NCP: how the two demand allocators work

The COSS uses two different kinds of demand allocators, depending on the segment. Understanding the distinction is essential.

### NCP: sum of individual customer peaks (Local Delivery)

**NCP stands for non-coincident peak.** It's the sum of every individual customer's own peak demand, regardless of when each peak occurs.

Consider three customers on the same line transformer:

| Customer | Their individual peak demand | When their peak occurs  |
| -------- | ---------------------------: | ----------------------- |
| A        |                         8 kW | Wednesday 7pm (cooking) |
| B        |                        12 kW | Thursday 3pm (AC + EV)  |
| C        |                         5 kW | Saturday 9am (laundry)  |
| **Sum**  |                    **25 kW** |                         |

The sum of peaks is 25 kW. This is the NCP allocator for this group. It doesn't matter that these peaks never happened at the same time. The logic is: the transformer, the secondary wire, the last stretch of primary circuit — all of this equipment was sized to handle each customer's individual peak, because these local facilities serve so few customers that there isn't much diversity (customers peaking at different times) to reduce the design load. The transformer has to be big enough for Customer B's 12 kW even if B peaks at a totally different hour than A and C.

**Local Delivery costs are allocated using NCP because local equipment is planned for the sum of undiversified customer peaks.** A rate class whose customers tend to have high individual peaks (even if those peaks are scattered across different hours) gets a bigger share of Local Delivery costs.

### CP: class contribution to the system peak (System Delivery)

**CP stands for coincident peak.** It's how much load each rate class is contributing at the moment of the entire system's peak demand.

PSE&G's system peak occurred on Tuesday, August 9, 2022, from 4–5 pm. At that hour, the entire system demand was 4,362,852 kW. Each rate class contributed some share of that:

| Rate class | Load during system peak | CP share |
| ---------- | ----------------------: | -------: |
| RS         |           ~2,500,000 kW |     ~57% |
| GLP        |             ~600,000 kW |     ~14% |
| LPL        |             ~700,000 kW |     ~16% |
| Others     |             ~562,852 kW |     ~13% |
| **System** |        **4,362,852 kW** | **100%** |

The CP allocator for a rate class is its load at the system peak divided by total system load at the system peak. If the residential class (RS) draws 57% of the system load at the peak hour, RS is responsible for 57% of System Delivery costs.

**System Delivery costs are allocated using CP because bulk distribution facilities — substations, the main trunk of the primary circuits — are planned and sized for the system peak.** It doesn't matter what your individual peak was at 3am; what matters is how much load your class was putting on the substation at the hour the substation hit its limit.

### Why the two allocators give different answers

The two allocators create different cost shares because customer classes have different **load diversity**. Residential customers have high load diversity — they peak at scattered times (cooking, laundry, AC cycling), so the sum of their individual peaks is much larger than their combined load at the system peak. Commercial and industrial customers tend to have lower load diversity — they're more likely to all be running at full capacity during business hours, including the system peak.

This means residential customers get a relatively larger share of Local Delivery costs (NCP basis, where their scattered high individual peaks add up) and a relatively smaller share of System Delivery costs (CP basis, where their diversified load is lower at the system peak).

### The numbers from the EV COSS

The Swetz testimony includes an EV sub-class study that shows the RS class totals for each segment:

| Segment         | RS class total revenue requirement | Allocator                                                        |
| --------------- | ---------------------------------: | ---------------------------------------------------------------- |
| Local Delivery  |                       $470,258,234 | NCP: sum of individual customer peaks = 11,830,661 kW            |
| System Delivery |                       $300,953,037 | CP: RS contribution to system peak = 4,362,852 kW (total system) |

This means roughly 61% of the combined Local + System Delivery costs for RS are allocated on an NCP basis and 39% on a CP basis. (The Access, Customer Service, and Measurement segments add additional costs on top of these, recovered through the Service Charge.)

## Worked example: NCP allocation for residential EV chargers

The testimony walks through an NCP allocation for 826 residential EV charging customers. This example is illuminating because it shows the full mechanics.

**Setup:** PSE&G collected 15-minute interval data for 826 residential EV customers from August 2022 through July 2023. From this data, they computed:

- **Sum of individual customer peaks** (NCP) for the EV sub-group: 16,651 kW
- **EV sub-group load during the system peak** (CP): 34 kW
- **Total annual kWh for the EV sub-group**: 2,921,627 kWh

**Step 1 — NCP ratio for Local Delivery:**

$$\text{NCP ratio} = \frac{\text{EV sum of peaks}}{\text{RS class sum of peaks}} = \frac{16{,}651 \text{ kW}}{11{,}830{,}661 \text{ kW}} = 0.1407\%$$

**Step 2 — Allocate Local Delivery costs:**

$$\text{EV Local Delivery cost} = \$470{,}258{,}234 \times 0.001407 = \$661{,}857$$

**Step 3 — CP ratio for System Delivery:**

$$\text{CP ratio} = \frac{\text{EV load at system peak}}{\text{Total system peak}} = \frac{34 \text{ kW}}{4{,}362{,}852 \text{ kW}} = 0.0008\%$$

**Step 4 — Allocate System Delivery costs:**

$$\text{EV System Delivery cost} = \$300{,}953{,}037 \times 0.000008 = \$2{,}348$$

**Step 5 — Total cost and effective rate:**

$$\text{Total delivery cost} = \$661{,}857 + \$2{,}348 = \$664{,}204$$

$$\text{Effective COS rate} = \frac{\$664{,}204}{2{,}921{,}627 \text{ kWh}} = \$0.2273/\text{kWh}$$

**What this tells us:** EV chargers have very peaky load profiles — their NCP share (0.14%) is 175× their CP share (0.0008%). This means virtually all of their allocated cost comes from Local Delivery (99.6%), not System Delivery (0.4%). Their effective cost-of-service rate of `$0.2273/kWh` is nearly 4× the RS class-average distribution rate of about `$0.0585/kWh`. The proposed RS distribution rates dramatically under-recover costs from EV customers, which is part of why PSE&G proposed a TOU rate that sends better price signals.

## How costs flow into rates

The COSS tells you how much revenue each rate class is responsible for. The rate design turns that revenue requirement into actual prices customers see on their bill. This is where the summer/winter differential comes from.

### The summer-only System Delivery rule

The core rate design formula for volumetric (kWh) rate schedules like RS is:

$$\text{Winter rate} = \frac{\text{Local Delivery revenue requirement}}{\text{Annual kWh (all 12 months)}}$$

$$\text{Summer rate} = \frac{\text{System Delivery revenue requirement}}{\text{Summer kWh (Jun–Sep only)}} + \frac{\text{Local Delivery revenue requirement}}{\text{Annual kWh (all 12 months)}}$$

In plain English:

- **Winter kWh charges recover only Local Delivery costs,** spread evenly across the whole year's consumption.
- **Summer kWh charges recover both Local Delivery and System Delivery costs.** The System Delivery portion is concentrated entirely in the four summer billing months (June–September).

This is not arbitrary — it follows from the CP allocation logic. PSE&G's system peak is in summer (a hot August afternoon). System Delivery facilities are planned for the summer peak. So System Delivery costs are recovered only through summer charges, because that's when the cost was caused.

### Current RS rates (B.P.U.N.J. No. 17 Electric, effective 2024)

| Charge component                     | Rate (excl. SUT) | Rate (incl. SUT) |
| ------------------------------------ | ---------------: | ---------------: |
| Service Charge (monthly)             |            $5.63 |            $6.00 |
| Distribution, Oct–May, first 600 kWh |        $0.044817 |        $0.047789 |
| Distribution, Oct–May, over 600 kWh  |        $0.044817 |        $0.047789 |
| Distribution, Jun–Sep, first 600 kWh |        $0.077130 |        $0.082225 |
| Distribution, Jun–Sep, over 600 kWh  |        $0.077130 |        $0.082225 |

The summer distribution rate is roughly 1.7× the winter rate. The difference — about `$0.032/kWh` — is the System Delivery component that only shows up in summer.

### The Service Charge

The Service Charge is designed to recover the per-customer costs from three segments: Access, Customer Service, and Measurement. These are costs that don't vary with how much electricity a customer uses — the service drop exists whether you use 100 kWh or 1,000 kWh; the meter is there regardless; the billing system sends a bill either way.

The COSS indicates that the actual per-customer cost is significantly higher than the current `$5.63/month` Service Charge. The rate was increased by 1.5× the class-average distribution increase, but it's still below cost. The gap is shifted to the volumetric (kWh) charges — specifically to the Local Delivery portion.

## How cost allocation is applied: class level vs schedule level

This is a point that can cause confusion, so here it is step by step.

### Step 1: The COSS produces revenue requirements for each rate schedule

The COSS doesn't just produce one number for "residential." It allocates costs to every individual rate schedule: RS, RHS, RLM, WH, WHS, HS, GLP, LPL-S, LPL-P, HTS-S, HTS-HV, BPL, BPL-POF, PSAL, and several others. This is because each schedule has its own billing determinants (how many kWh, how many customers, what their peaks are), and the COSS uses those to allocate costs.

Schedule SS-E5 in the testimony runs 70 pages and shows, for every plant account and every expense item, exactly how much is allocated to each rate schedule. Schedule SS-E7 summarizes the result: a revenue requirement for each rate schedule, broken down by the six functional segments.

So after the COSS is done, PSE&G knows something like: "RS should be responsible for $X million in Local Delivery, $Y million in System Delivery, etc." And separately: "RHS should be responsible for $A million in Local Delivery, $B million in System Delivery, etc."

### Step 2: The inter-class allocation caps are applied at the class level

This is where it gets tricky. The COSS says what each schedule "should" pay, but PSE&G doesn't just translate COSS results directly into rates. Instead, it applies **gradualism limits** — caps on how much any class's rates can increase in a single rate case.

These limits are:

- No class gets less than 50% of the overall average distribution percentage increase
- No class gets more than 125% of the overall average distribution percentage increase
- No class gets more than 150% of the overall average total bill percentage increase

These limits are applied at the **rate class** level — meaning all residential schedules (RS, RHS, RLM, WH, WHS, HS) are treated as one group for the purpose of determining how much of the total revenue increase goes to residential vs. commercial vs. industrial. The inter-class allocation (Schedule SS-E9) determines how the total increase in distribution revenue is split among classes.

In this rate case, the overall average distribution increase was 39.484%. Under the COSS, some classes were well above that (they'd been underpaying relative to cost), and some were below. The limits ensure no class takes a sudden jump (or gets an artificially small increase). The residential class (RS specifically) was significantly below cost even after the increase — meaning the COSS says residential should be paying more than it is, but gradualism prevents PSE&G from getting all the way to cost in one case.

### Step 3: Within a class, revenue is distributed to individual schedules

After the inter-class allocation determines how much distribution revenue the residential class as a whole must produce, PSE&G distributes that revenue across the individual residential schedules — RS, RHS, RLM, WH, WHS, HS — using the COSS segment breakdowns as a guide.

For each schedule, the process is:

1. **Set the Service Charge** based on the per-customer revenue requirements for the Access, Customer Service, and Measurement segments. For RS and RHS, the Service Charge was increased by 1.5× the class-average increase but is still below cost; the shortfall is shifted to the volumetric charges.

2. **Calculate how much distribution revenue remains** after subtracting Service Charge revenue. This remainder must come from the volumetric (kWh or kW) charges.

3. **Split the remainder into Local Delivery and System Delivery** using each schedule's COSS segment proportions.

4. **Design the volumetric rates:**
   - Local Delivery portion → recovered over annual kWh (applies in all 12 months)
   - System Delivery portion → recovered over summer kWh only (June–September)

This is done individually for each schedule. RS, RHS, RLM, WH, WHS, and HS each go through this process with their own billing determinants and their own COSS segment allocations. That's why the rates are different across schedules — HS (Heating Service) has a different summer/winter usage pattern than RS, so the same formula produces different per-kWh rates.

### What this means in practice

The COSS determines per-schedule revenue requirements, and those requirements flow through to per-schedule rates. But the total revenue collected from all residential schedules combined is constrained by the inter-class allocation — PSE&G can't just set every residential schedule to its full COSS cost in one rate case.

Think of it as a two-level process:

1. **Between classes** (residential vs. commercial vs. industrial): how much of the total distribution revenue increase goes to each class, subject to gradualism limits.
2. **Within a class** (RS vs. RHS vs. RLM vs. HS, etc.): how that class-level revenue target is distributed across individual schedules, guided by the COSS segment proportions.

## The TOU rate design

The proposed RS-TOU rates (specifically RS-TOU 3P, the three-period rate that was adopted) use the same COSS segments but distribute them across time periods:

**System Delivery (CP-based costs):**

The System Delivery component is concentrated in on-peak hours (4–9 pm weekdays), since that's closest to when the system peak occurs. The summer on-peak period gets 1.5× the winter on-peak allocation, reflecting that the system peak is a summer event. Mid-peak and off-peak periods carry no System Delivery cost.

**Local Delivery (NCP-based costs):**

The Local Delivery component is spread across all periods, but not equally. On-peak and mid-peak hours are charged 2× the off-peak rate for Local Delivery. This sends a price signal that individual peaks (which often coincide with evening hours) cost more, while keeping the off-peak rate low.

The resulting RS-TOU 3P distribution rates (as proposed, excl. SUT):

| Period   | Hours                 |    Summer |    Winter |
| -------- | --------------------- | --------: | --------: |
| On-Peak  | 4pm–9pm weekdays      | $0.196495 | $0.144223 |
| Mid-Peak | 6am–4pm, 9pm–midnight | $0.039678 | $0.039678 |
| Off-Peak | Midnight–6am          | $0.019839 | $0.019839 |

The design is revenue-neutral to the RS schedule as a whole — if every RS customer moved to RS-TOU 3P with no change in usage, total distribution revenue would be the same. The rates are shown in workpaper WP-SS-TOU.xlsx.

## Why this matters for heat pumps

The summer-only System Delivery rule is the key feature for heat pump rate design. A heat pump customer who adds substantial winter load (for space heating) pays **zero incremental System Delivery charges** on that load, because System Delivery costs are only recovered through summer kWh. Their winter kWh pays only the Local Delivery rate.

From PSE&G's cost-causation perspective, this is correct: the system peak is in summer, so System Delivery facilities were built for summer loads, and winter loads don't cause those costs. But as heat pump adoption grows, winter peaks will rise. At some point, the winter peak could approach or exceed the summer peak, which would undermine the cost-causation rationale for summer-only System Delivery recovery. The COSS methodology would need to evolve — potentially splitting System Delivery into summer and winter components, or switching to a year-round allocation — to reflect the new load reality.

The TOU rates partially address this by concentrating costs in on-peak hours (which are the same in summer and winter: 4–9 pm weekdays). But the fundamental asymmetry — System Delivery costs recovered only in summer — persists even in the TOU design.

## Sources

Extracts are under `context/sources/nj_hp_rates/`. Citation keys are searchable in Zotero.

- **Swetz Direct Testimony (Exhibit P-9E)** — [`njbpu_er23120924_swetz_p9e_electric.md`](../../sources/nj_hp_rates/njbpu_er23120924_swetz_p9e_electric.md) · `swetz_DocketER23120924Direct_2023` · Docket No. ER23120924, filed December 29, 2023. The primary source for all COSS methodology, segment definitions, allocators, rate design formulas, TOU rate design, and the EV sub-class study.
- **Stipulation of Settlement** — [`njbpu_er23120924_stipulation.md`](../../sources/nj_hp_rates/njbpu_er23120924_stipulation.md) · `pseg_DocketER23120924Stipulation_2024` · Docket No. ER23120924, filed June 20, 2024. The agreed-upon revenue requirements ($341M electric increase), rate design (Attachment E), and RS-TOU 3P approval.
- **PSE&G Electric Tariff, B.P.U.N.J. No. 17 Electric (current)** — [`pseg_electric_tariff_17_current.md`](../../sources/nj_hp_rates/pseg_electric_tariff_17_current.md) · `pseg_ElectricTariffBPUNJ_2026` · The working tariff incorporating the rate case settlement plus subsequent rider adjustments through 2026. RS, RS-TOU 3P, and all other rate schedules with current charges.
- **PSE&G Electric Tariff, B.P.U.N.J. No. 17 Electric (rate case version)** — [`pseg_electric_tariff_17_rate_case.md`](../../sources/nj_hp_rates/pseg_electric_tariff_17_rate_case.md) · `pseg_DocketER23120924Electric_2024` · The tariff as filed with the rate case settlement, before subsequent rider updates.
