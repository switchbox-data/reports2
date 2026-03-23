# Tillman's critique of National Grid's cost allocation and rate design

Reconstructed from Gregory W. Tillman's direct testimony on behalf of Walmart in RIPUC Docket No. 4770 (National Grid's 2018 distribution rate case). Tillman is a rate design and cost-of-service expert who had testified in 21 prior regulatory proceedings. His testimony identifies three independent flaws in National Grid's proposed rate design for large-demand customers, each building from the same foundational principle: **rates should reflect cost causation**.

Source: `reports2/context/sources/ri_hp_rates/ripuc_4770_direct_testimony_warlmat_tillman.md`

## The foundational principle: cost-causation rate design

Tillman begins from a standard regulatory economics position: rates should be set based on the utility's cost of service for each rate class. A Cost of Service Study (COSS) is the analytic tool that functionalizes, classifies, and allocates costs to customer classes in proportion to how those customers cause costs to be incurred. Revenue allocated to each class at its COSS-determined cost is free of inter-class subsidies.

When revenue allocation departs from the COSS — for rate shock mitigation, social policy, or other reasons — the result is inter-class subsidies. Classes with a Relative Return Index (RRI) greater than 1.0 are overpaying; classes with RRI below 1.0 are underpaying. The goal is to move all classes toward RRI = 1.0 over successive rate cases.

This principle has two corollaries that Tillman deploys:

1. **Rate design must reflect the nature of the underlying costs.** If the COSS identifies only customer-related and demand-related costs for a class, then the rate structure should consist of customer charges and demand charges — not energy charges.

2. **Class consolidation must precede, not follow, the COSS.** If the utility wants to combine two rate classes, it must perform the COSS on the consolidated class so that the allocation reflects the combined class's actual load characteristics. Simply adding the separately-allocated costs of two classes produces a different (and incorrect) result.

## Critique 1: billing demand calculation error

### The setup

National Grid proposed to consolidate Rate G-62 (customers with demand > 5,000 kW) into Rate G-32 (large demand customers with demand > 200 kW). The consolidated Rate G-32 structure includes the first 200 kW of demand in the customer charge; only demand above 200 kW is billed through the demand charge.

When migrating G-62 customers into this structure, the Company needed to subtract the first 200 kW per customer per month from each G-62 customer's demand to compute the correct billing demand units for the demand charge. The formula for this exclusion was:

$$\text{Excluded kW} = N_{\text{customers}} \times 200 \text{ kW} \times 12 \text{ months}$$

### The error

National Grid used **the number of bills** (156) instead of **the number of customers** (13) for $N_{\text{customers}}$. Since 13 customers × 12 months = 156 bills, the Company effectively triple-counted the exclusion:

| Input                          | Company's value | Correct value  |
| ------------------------------ | --------------- | -------------- |
| $N_{\text{customers}}$         | 156 (bills)     | 13 (customers) |
| Excluded kW                    | 375,315 kW      | 31,200 kW      |
| Billing demand for rate design | 3,512,410 kW    | 3,856,525 kW   |

### The consequence

The error inflated the Excluded kW by a factor of 12, which deflated the billing demand denominator used to compute the demand charge. A lower denominator means the $/kW demand charge would need to be higher to collect the same revenue — but the Company computed the charge using the wrong (lower) denominator, producing a demand charge that under-collects from the demand component and fails to produce the target class revenue.

### The fix

Correct the customer count to 13. The corrected billing demand units are 3,856,525 kW. The rate design must be recalculated using this figure.

## Critique 2: recovering demand-related costs through energy charges creates intra-class subsidies

### The setup

National Grid's COSS for Rate G-32 identified only two cost functions: **customer-related costs** and **demand-related costs**. There were no energy-related distribution costs. Despite this, the proposed rate structure included an energy charge of $0.00631/kWh alongside the demand charge.

| Rate component              | Proposed rate |
| --------------------------- | ------------- |
| Customer Charge             | $1,100/month  |
| Energy Charge               | $0.00631/kWh  |
| Demand Charge (over 200 kW) | $5.00/kW      |

National Grid's own guiding principle — stated by witness Gorman — was that rates should "reflect the nature of the costs they recover." An energy charge for a class with no energy-related costs violates this principle on its face.

### Why it matters: the load factor subsidy

Recovering demand-related (fixed) costs through an energy (variable) charge shifts cost responsibility from low load factor customers to high load factor customers. Two customers with identical peak demand cause identical demand-related costs, but the one that runs more hours (higher load factor) consumes more kWh and thus pays more under an energy charge.

### Numerical illustration

Consider two customers, each with 20 kW peak demand, sharing $2,000 in annual demand-related costs:

|                                  | Customer 1 (60% LF) | Customer 2 (30% LF) |
| -------------------------------- | ------------------- | ------------------- |
| Peak demand                      | 20 kW               | 20 kW               |
| Annual kWh                       | 105,120             | 52,560              |
| Cost responsibility (equal peak) | $1,000              | $1,000              |

**Under a demand charge** ($4.17/kW-month = $2,000 ÷ 40 kW ÷ 12):

- Customer 1 pays $1,000 (20 kW × $4.17 × 12)
- Customer 2 pays $1,000 (20 kW × $4.17 × 12)
- Each pays their cost. No subsidy.

**Under an energy charge** ($0.0127/kWh = $2,000 ÷ 157,680 kWh):

- Customer 1 pays $1,333 ($0.0127 × 105,120)
- Customer 2 pays $667 ($0.0127 × 52,560)
- Customer 1 overpays by $333; Customer 2 underpays by $333.

The high load factor customer (Walmart's stores, which run long hours) subsidizes the low load factor customer by $333/year — one-third of their cost responsibility. This is an **intra-class** subsidy: it occurs within the same rate class, invisible to the inter-class RRI analysis.

### The fix

Eliminate the energy charge from Rate G-32 and recover all demand-related costs through the demand charge. This produces a higher demand charge ($8.41/kW vs. $5.00/kW) but correctly reflects cost causation.

| Rate component              | NG proposed  | Walmart proposed |
| --------------------------- | ------------ | ---------------- |
| Customer Charge             | $1,100/month | $1,100/month     |
| Energy Charge               | $0.00631/kWh | **Eliminated**   |
| Demand Charge (over 200 kW) | $5.00/kW     | **$8.41/kW**     |

## Critique 3: class consolidation methodology — allocate-then-combine vs. combine-then-allocate

### The setup

National Grid ran the COSS with Rate G-32 and Rate G-62 as **separate classes**, then combined the separately-allocated revenue requirements to design rates for the merged class. Tillman argues the correct approach is to consolidate the classes **before** running the COSS, then allocate costs to the consolidated class.

### Why the order matters: load diversity

When the COSS uses a Non-Coincident Peak (NCP) allocator to assign demand-related costs, the allocation depends on each class's NCP relative to the sum of all classes' NCPs. Class peaks that occur at different hours exhibit **load diversity**: their combined peak is less than the sum of their individual peaks.

### Numerical illustration

Three classes, each with NCP = 100 kW but peaking at different hours:

**Method A: Allocate separately, then combine (National Grid's approach)**

Total NCP = 100 + 100 + 100 = 300 kW. Each class gets an NCP allocator of 100/300 = 0.333.

Allocating $1,000: each class gets $333.

If Classes 2 and 3 are then combined: combined revenue requirement = $333 + $333 = **$666**.

**Method B: Combine first, then allocate (Tillman's recommended approach)**

Combining Classes 2 and 3 produces a consolidated load shape with NCP = **185 kW** (not 200 kW), because their individual peaks occur at different hours. The 15 kW reduction is load diversity.

New total NCP = 100 + 185 = 285 kW.

- Class 1 allocator: 100/285 = 0.351 → allocated cost = **$351**
- Class 2+3 allocator: 185/285 = 0.649 → allocated cost = **$649**

### The discrepancy

|                | NG method (A) | Correct method (B) | Difference |
| -------------- | ------------- | ------------------ | ---------- |
| Class 1 cost   | $333          | $351               | +$18       |
| Class 2+3 cost | $666          | $649               | −$17       |

National Grid's method over-allocates costs to the combined class by $17 and under-allocates to Class 1 by $18 (rounding). The error arises because Method A implicitly assumes the two classes have perfectly coincident peaks (NCP sums linearly), while Method B correctly accounts for load diversity in the combined class.

The direction of the error is always the same: the allocate-then-combine approach will **overcharge** the merged class whenever its constituent subclasses have any load diversity (peaks at different hours). For G-32 and G-62 customers — whose load profiles likely differ given the difference in scale (200 kW vs. 5,000 kW threshold) — load diversity is expected.

### The fix

Reject National Grid's method. Perform the COSS using G-32 and G-62 as a single consolidated class from the outset, so that the NCP allocator reflects the actual combined load profile.

## Summary of recommendations

1. **Correct the billing demand error.** Use 13 customers (not 156 bills) to compute Excluded kW, yielding corrected billing demand of 3,856,525 kW.
2. **Eliminate the energy charge.** Recover all demand-related costs through customer and demand charges only ($8.41/kW demand charge), eliminating intra-class load factor subsidies.
3. **Consolidate classes before the COSS.** Combine G-32 and G-62 into a single class, then run the COSS, so that the NCP allocator captures load diversity.

## Relevance to Switchbox's work

Tillman's critique articulates standard cost-causation principles that are directly relevant to our rate design and BAT methodology:

- **Intra-class subsidies from volumetric recovery of fixed costs** are the same mechanism that the BAT's volumetric allocator measures. When distribution delivery costs (demand-related) are recovered through per-kWh energy charges, high-consumption customers (including heat pump homes running through winter) overpay relative to their cost responsibility. This is the central cross-subsidy that heat-pump-friendly rate design aims to correct.

- **The load factor subsidy** is a specific instance of the general principle that recovering fixed costs volumetrically transfers cost responsibility from low-usage to high-usage customers. In the residential context, this manifests as HP customers (high winter kWh, high load factor) subsidizing non-HP customers (lower kWh, lower load factor) through flat volumetric delivery rates.

- **The class consolidation argument** illustrates why allocator choice matters in COSS. The same principle — that combining load profiles changes the relevant peaks — applies when thinking about how to allocate costs between HP and non-HP customer subclasses within a rate class.
