# The four cost allocation frameworks: traditional and hourly, embedded and marginal

A detailed guide to the four primary methods for allocating electricity costs to customer classes, subclasses, or individual customers. Each method is presented with formulas, worked examples, and an assessment of how well it captures the temporal load differences that drive the HP/non-HP cross-subsidy.

For the broader context — why cost allocation is the diagnostic tool for cross-subsidies, how these four methods relate to each other, and how rate design is the separate downstream fix — see `domain/cost_allocation_cross_subsidies_and_rate_design.md`.

---

## Overview: two dimensions, four frameworks

Cost allocation methods vary along two dimensions:

- **Cost basis**: what costs are being allocated?
  - **Embedded**: the utility's actual historical revenue requirement — every dollar of recorded accounting cost.
  - **Marginal**: forward-looking economic costs — the cost of serving the next increment of demand. Produces a Marginal Cost Revenue Requirement (MCRR) that is typically much less than the total revenue requirement; the gap is the residual.

- **Time granularity**: how is the cost assigned to time periods?
  - **Traditional (snapshot)**: costs are assigned to one or a few peak hours per year (or per month). The allocator is a single number per group — a peak demand, an NCP, a kWh total.
  - **Hourly (8,760)**: costs are assigned to every hour of the year, and each group's allocation depends on its load in every hour.

|              | Traditional (snapshot)                                                                                | Hourly (8,760)                                                                                                                |
| ------------ | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Embedded** | §1: NARUC three-step (functionalize, classify, allocate). Allocators: CP, NCP, kWh, customer count.   | §3: Average-and-peak or direct resource-to-hour mapping. All accounting costs distributed across hours.                       |
| **Marginal** | §2: NERA method. Unit marginal costs × class peak contribution or kWh. Residual recovered separately. | §4: Probabilistic hourly avoided costs × hourly load. Capacity costs weighted to stress hours. Residual recovered separately. |

---

## 1. Traditional embedded cost allocation (ACOSS)

### What it is

The standard Allocated Cost of Service Study (ACOSS), codified in the 1992 NARUC _Electric Utility Cost Allocation Manual_ and updated by RAP's 2020 _Electric Cost Allocation for a New Era_. It divides the utility's total historical revenue requirement among customer groups using accounting-based allocation factors.

### The three steps

**Step 1 — Functionalization.** Assign each dollar of the revenue requirement to a functional category:

- Generation (including purchased power)
- Transmission
- Distribution (sub-functionalized: substations, primary feeders, line transformers, secondary lines)
- Customer service (meters, service drops, billing)
- Administrative & General (prorated across other functions)

**Step 2 — Classification.** Tag each functionalized cost by its cost driver:

| Cost pool                                            | Classification          | Rationale                                                         |
| ---------------------------------------------------- | ----------------------- | ----------------------------------------------------------------- |
| Generation capacity, fixed O&M                       | Demand (kW)             | Sized for peak demand                                             |
| Fuel, variable purchased power                       | Energy (kWh)            | Varies with production volume                                     |
| Transmission plant                                   | Demand (kW)             | Sized for bulk power transfer at peak                             |
| Distribution plant (poles, conductors, transformers) | Split demand / customer | Contentious — see note on minimum system vs. basic customer below |
| Meters, service drops, billing                       | Customer (count)        | Varies with number of connections                                 |

The demand/customer split for distribution plant is the most consequential classification choice. The **minimum system method** classifies the cost of the smallest functional equipment as customer-related (typically 35–77% of distribution plant). The **basic customer method** classifies only meters, billing, and service drops as customer-related, making nearly all distribution plant demand-related. RAP's 2020 manual recommends the basic customer method.

**Step 3 — Allocation.** Distribute each classified cost pool to groups using allocation factors:

$$C_j = C_{\text{pool}} \times AF_j \quad \text{where} \quad \sum_j AF_j = 1$$

The allocation factor $AF_j$ depends on the classification:

**For demand-classified costs — Coincident Peak (CP):**

$$AF_j^{\text{CP}} = \frac{D_j^{\text{sys peak}}}{D_{\text{system peak}}}$$

where $D_j^{\text{sys peak}}$ is group $j$'s demand during the single hour of annual system peak. The $N$-CP variant averages across $N$ monthly peaks:

$$AF_j^{N\text{-CP}} = \frac{(1/N) \sum_{m=1}^{N} D_j(\text{month } m \text{ peak})}{(1/N) \sum_{m=1}^{N} D_{\text{system}}(\text{month } m \text{ peak})}$$

CP is used for costs driven by system-wide peaks: generation capacity, transmission. The 12-CP method is the historical FERC method for transmission cost allocation.

**For demand-classified costs — Non-Coincident Peak (NCP):**

$$AF_j^{\text{NCP}} = \frac{NCP_j}{\sum_k NCP_k}$$

where $NCP_j$ is group $j$'s own maximum demand, regardless of when it occurs. NCP is the standard allocator for **distribution** demand costs, because distribution facilities (feeders, transformers) are sized to meet local and class-level peaks that may not coincide with the system peak.

**For energy-classified costs:**

$$AF_j^{\text{energy}} = \frac{\text{kWh}_j}{\sum_k \text{kWh}_k}$$

**For customer-classified costs:**

$$AF_j^{\text{customer}} = \frac{N_j}{\sum_k N_k}$$

### Worked example

A utility has a $100M total revenue requirement. After functionalization and classification:

| Cost pool                         | Amount | Classification | Allocator |
| --------------------------------- | ------ | -------------- | --------- |
| Generation capacity               | $40M   | Demand         | 1-CP      |
| Transmission                      | $15M   | Demand         | 12-CP     |
| Distribution                      | $30M   | Demand         | NCP       |
| Energy (fuel, purchased power)    | $10M   | Energy         | kWh       |
| Customer (meters, billing, drops) | $5M    | Customer       | Count     |

Two subclasses within residential: HP (20% of customers, adding winter load) and non-HP (80%).

| Metric                              | HP     | Non-HP | Total residential |
| ----------------------------------- | ------ | ------ | ----------------- |
| Customers                           | 20,000 | 80,000 | 100,000           |
| Annual kWh                          | 240M   | 560M   | 800M              |
| Demand at summer system peak (1-CP) | 30 MW  | 120 MW | 150 MW            |
| Average of 12 monthly CPs (12-CP)   | 35 MW  | 110 MW | 145 MW            |
| Non-coincident peak (NCP)           | 50 MW  | 130 MW | 180 MW            |

HP customers have a higher NCP (50 MW for 20k customers, driven by winter heating peaks) but a lower CP (30 MW, because they contribute less to the summer system peak).

**Allocation:**

| Cost pool                  | HP share        | HP allocation |
| -------------------------- | --------------- | ------------- |
| Generation ($40M, 1-CP)    | 30/150 = 20.0%  | $8.0M         |
| Transmission ($15M, 12-CP) | 35/145 = 24.1%  | $3.6M         |
| Distribution ($30M, NCP)   | 50/180 = 27.8%  | $8.3M         |
| Energy ($10M, kWh)         | 240/800 = 30.0% | $3.0M         |
| Customer ($5M, count)      | 20/100 = 20.0%  | $1.0M         |
| **Total**                  |                 | **$23.9M**    |

HP customers (20% of customers) are allocated 23.9% of costs. The NCP allocator is the main driver: HP customers have a disproportionately high NCP (27.8% share) because their winter heating peak is their individual maximum demand, even though they contribute less to the summer system peak.

### What traditional embedded misses for HP cross-subsidies

**NCP doesn't distinguish when the peak occurs.** An HP customer with a 50 MW winter peak and a non-HP customer with a 50 MW summer peak would get identical NCP-based distribution allocations — even if the distribution system is summer-constrained and the HP customer's winter peak drives no investment. NCP measures _magnitude_ of peak demand, not _timing_. This is a fatal flaw for measuring the HP cross-subsidy, which is fundamentally about timing.

**CP captures timing only for one system-level hour.** The 1-CP allocator correctly shows HP customers contributing less at the summer system peak. But it's a single hour — if the system has winter constraints (e.g., winter-peaking feeders), those don't appear in the summer CP. The 12-CP variant is better (it captures monthly peaks, including winter months) but still collapses each month to one hour.

**The demand/energy classification is a binary that loses information.** Every dollar is classified as either demand-related (allocated by peak) or energy-related (allocated by kWh). There is no mechanism for "this dollar is demand-related but only during certain hours" — which is precisely what you'd need to capture the fact that distribution investment is driven by summer peaks but HP consumption is concentrated in winter.

---

## 2. Traditional marginal cost allocation (NERA method)

### What it is

The marginal cost-of-service study (MCOS), developed by NERA Economic Consulting in the 1970s for California ratemaking and widely adopted since. Instead of allocating the historical revenue requirement, it estimates the forward-looking cost of serving each group's load. The result is a Marginal Cost Revenue Requirement (MCRR) for each group, which is typically less than the group's share of the total revenue requirement. The gap is the residual.

### The components

For each group $j$, the MCRR has three components:

$$MCRR_j = \underbrace{N_j \times c_{\text{customer}}}_{\text{Customer MC}} + \underbrace{D_j \times c_{\text{capacity}}}_{\text{Capacity MC}} + \underbrace{Q_j \times c_{\text{energy}}}_{\text{Energy MC}}$$

where:

- $N_j$ = number of customers in group $j$
- $c_{\text{customer}}$ = marginal cost per customer connection (meters, service drops)
- $D_j$ = group $j$'s peak demand (various measures — see below)
- $c_{\text{capacity}}$ = marginal capacity cost per kW (generation, transmission, distribution — each with its own unit cost and its own demand measure)
- $Q_j$ = group $j$'s annual energy consumption (kWh)
- $c_{\text{energy}}$ = marginal energy cost per kWh (average wholesale price or fuel cost)

### Demand measures by system level

Because load diversity increases as you move up the voltage hierarchy, different peak measures are used at each level:

**Generation and transmission**: allocated by **System Coincident Peak (System 1-CP)** — the group's demand during the single hour of system-wide peak. The marginal capacity cost is typically derived from the cost of a new peaker plant (the "equivalent peaker" method) or from capacity market prices (ICAP, FCM).

$$MC^{\text{gen+TX}}_j = D_j^{\text{sys peak}} \times c^{\text{gen}}_{\text{kW-yr}} + D_j^{\text{sys peak}} \times c^{\text{TX}}_{\text{kW-yr}}$$

**Primary distribution (feeders, substations)**: allocated by **Class NCP at the circuit level** — the sum of the group's load during the peak hour of every individual feeder:

$$MC^{\text{primary dist}}_j = \left(\sum_f D_j^{\text{feeder } f \text{ peak}}\right) \times c^{\text{primary}}_{\text{kW-yr}}$$

where the sum is over all feeders serving group $j$ customers, and $D_j^{\text{feeder } f \text{ peak}}$ is the group's demand during feeder $f$'s peak hour. This captures some timing: a feeder that peaks in winter allocates winter-peaking load to the group that drives it. But in a traditional study, this is still a single hour per feeder, not a full hourly profile.

**Secondary distribution (line transformers, service drops)**: allocated by **Sum of Individual Customer NCP** — the sum of each customer's personal maximum demand:

$$MC^{\text{secondary dist}}_j = \left(\sum_{i \in j} NCP_i\right) \times c^{\text{secondary}}_{\text{kW-yr}}$$

Secondary facilities serve so few customers that there is almost no load diversity. A transformer serving three houses must be sized for the largest of the three individual peaks, so the relevant demand is the sum of individual NCPs.

### The residual and EPMC

The total MCRR across all groups is less than the total revenue requirement:

$$\text{Residual} = TRR - \sum_j MCRR_j$$

To reconcile, the standard method is **equi-proportional marginal cost (EPMC) scaling**:

$$K = \frac{TRR}{\sum_j MCRR_j}$$

Each group's revenue requirement becomes:

$$RR_j = K \times MCRR_j$$

This scales every group's MCRR up by the same factor, preserving relative shares. Under EPMC, the residual is allocated in proportion to each group's MCRR — which means in proportion to their marginal cost-weighted behavior. This makes EPMC equivalent in structure to embedded cost allocation: both allocate the full revenue requirement by current behavior.

### Worked example (same utility as §1)

Suppose the marginal unit costs are:

| Component              | Unit MC         | Demand measure            |
| ---------------------- | --------------- | ------------------------- |
| Generation capacity    | $80/kW-yr       | System 1-CP               |
| Transmission capacity  | $30/kW-yr       | System 1-CP               |
| Primary distribution   | $40/kW-yr       | Class NCP at feeder level |
| Secondary distribution | $20/kW-yr       | Sum of customer NCPs      |
| Energy                 | $0.04/kWh       | Annual kWh                |
| Customer connection    | $60/customer-yr | Customer count            |

Assume primary distribution NCP at feeder level happens to equal the class NCP from §1 (a simplification — in reality, feeder peaks would be more granular):

| Component                      | HP MCRR                      | Non-HP MCRR | Total MCRR |
| ------------------------------ | ---------------------------- | ----------- | ---------- |
| Gen capacity (30 MW × $80)     | $2.4M                        | $9.6M       | $12.0M     |
| TX capacity (30 MW × $30)      | $0.9M                        | $3.6M       | $4.5M      |
| Primary dist (50 MW × $40)     | $2.0M                        | $5.2M       | $7.2M      |
| Secondary dist                 | (depends on individual NCPs) |             |            |
| Energy (240M kWh × $0.04)      | $9.6M                        | $22.4M      | $32.0M     |
| Customer (20k × $60)           | $1.2M                        | $4.8M       | $6.0M      |
| **Subtotal (excl. secondary)** | **$16.1M**                   | **$45.6M**  | **$61.7M** |

Total MCRR ≈ $62M (including secondary). With TRR = $100M, the residual ≈ $38M. EPMC scalar $K$ ≈ 100/62 = 1.61. Every group's MCRR is scaled up by 1.61× to recover the full $100M.

HP MCRR share ≈ 16.1/61.7 = 26.1%. Under EPMC, HP revenue requirement ≈ $26.1M.

Note this differs from the ACOSS result ($23.9M). The difference comes from the different treatment of distribution costs: the ACOSS uses a single NCP number, while the MCOS uses feeder-level NCPs and individual customer NCPs, each with different unit marginal costs. The MCOS is also forward-looking (marginal unit costs) rather than backward-looking (historical accounting costs), so the relative weight of each component differs.

### What traditional marginal captures vs. misses for HP cross-subsidies

**Better than ACOSS for transmission and generation**: the 1-CP allocator correctly attributes less generation and TX cost to HP customers, because HP customers contribute less at the summer system peak. Same as ACOSS for these components.

**Partially time-aware for distribution**: feeder-level NCP captures some timing. If feeder $f$ peaks in July, HP customers contribute less to feeder $f$'s peak and are allocated less. If feeder $g$ peaks in January (a winter-peaking feeder), HP customers contribute more and are allocated more. The sum across feeders produces a distribution allocation that reflects the mix of summer-peaking and winter-peaking feeders in the system. This is more time-aware than the ACOSS's single class-level NCP, which is just the maximum of the aggregate load shape.

**Still a snapshot — one hour per feeder**: the traditional MCOS uses one peak hour per feeder, not a probability distribution. A feeder that barely peaks in July vs. one that is severely stressed in July get the same treatment — the group's demand in that single hour is the allocator. There is no weighting by how close the feeder is to capacity, or how many hours are at risk. The hourly methods address this.

---

## 3. Hourly embedded cost allocation

### What it is

An extension of the traditional ACOSS that distributes accounting costs to all 8,760 hours of the year, rather than assigning demand costs to a single peak hour and energy costs to annual kWh. The goal is the same as traditional embedded — allocate the historical revenue requirement — but with finer time resolution.

### How costs are assigned to hours

The most common hourly embedded approach uses **average-and-peak** logic (borrowed from natural gas utility practices) to split each cost function into two time-varying components before assigning to hours:

**The "average" component.** A fraction of the cost equal to the system load factor ($LF = \text{average load} / \text{peak load}$) is classified as energy-related — the "baseload" cost of having a system that covers a geography and is available at all times. This portion is divided by total annual kWh and assigned equally to all 8,760 hours:

$$c^{\text{avg}}_h = LF \times \frac{C_{\text{function}}}{Q_{\text{annual}}} \quad \text{(same for all hours)}$$

**The "peak" component.** The remaining fraction ($1 - LF$) is classified as demand-related — the extra cost of upsizing equipment to handle peaks. This portion is assigned **only to high-load hours**, weighted by the degree to which each hour's load exceeds the average:

$$c^{\text{peak}}_h = (1 - LF) \times C_{\text{function}} \times \frac{\max(0, \; \text{Load}_h - \text{AvgLoad})}{\sum_{h'} \max(0, \; \text{Load}_{h'} - \text{AvgLoad})}$$

Hours below average load receive zero peak allocation. Hours above average receive allocation proportional to how far they exceed the average.

**Group allocation in each hour:**

$$C_{j,h} = \frac{L_{j,h}}{\sum_k L_{k,h}} \times (c^{\text{avg}}_h + c^{\text{peak}}_h)$$

Each group's share of the hourly cost is proportional to its share of total load in that hour. The group's total allocation is the sum across all hours:

$$RR_j = \sum_{h=1}^{8760} C_{j,h}$$

Because this divides the actual revenue requirement, there is no residual — $\sum_j RR_j = TRR$ by construction.

### Alternative: direct resource-to-hour mapping

Some hourly embedded studies bypass the average-and-peak split and instead map each resource's cost to the hours it operates:

$$C_{j,h} = \frac{L_{j,h}}{\sum_k L_{k,h}} \times \sum_r S_{r,h} \times C_r$$

where $S_{r,h}$ is the share of resource $r$'s output occurring in hour $h$, and $C_r$ is the total cost of resource $r$. A baseload plant ($S_{r,h} \approx 1/8760$ for all hours) distributes its cost evenly; a peaker plant ($S_{r,h}$ concentrated in high-demand hours) concentrates its cost in those hours. This requires resource-level hourly output data.

### Worked example (average-and-peak method)

Using the same utility. System load factor = 0.55. Distribution function = $30M.

- Average component: $0.55 \times \$30M = \$16.5M$, spread across all 8,760 hours by kWh.
- Peak component: $0.45 \times \$30M = \$13.5M$, concentrated in above-average hours.

Consider two illustrative hours:

**Hour A: August peak (300 MW system load, 200 MW non-HP, 100 MW HP):**

This hour is well above average (average = 0.55 × 300 MW peak ≈ 165 MW). It receives a large share of the peak component. HP share of load in this hour: 100/300 = 33%. HP gets 33% of this hour's cost.

**Hour B: January 2 AM (120 MW system load, 80 MW non-HP, 40 MW HP):**

This hour is below average load (120 < 165), so it receives zero peak component — only the average component. HP share: 40/120 = 33%. HP gets 33% of this hour's (smaller) cost.

**Hour C: January 6 PM (250 MW system load, 80 MW non-HP, 170 MW HP):**

Above average. Receives peak component. HP share: 170/250 = 68%. HP gets 68% of this hour's cost.

The key: if summer hours carry most of the peak component (because the system is summer-peaking and most above-average hours are in summer), HP customers get less peak allocation than their NCP share would suggest — because they contribute less during summer peak hours. If winter hours are also above-average (due to HP heating), HP customers get more peak allocation in those hours, but the per-hour cost is smaller (the winter hours are less far above average than the summer hours in a summer-peaking system).

### How hourly embedded compares to traditional embedded for HP cross-subsidies

**Improvement: time-aware distribution of peak costs.** Instead of allocating all distribution demand costs by a single NCP number (which ignores when the peak occurs), hourly embedded spreads peak costs across hours proportionally to load exceedance. Summer peak hours carry more cost than winter hours (in a summer-peaking system), and each group's share is computed hour-by-hour. HP customers, who contribute less in summer peak hours, get less peak-cost allocation.

**Limitation: the average-and-peak split is crude.** The system load factor determines the demand/energy split — a single number that doesn't vary by voltage level, feeder, or season. A feeder that is 90% loaded in winter and 50% loaded in summer gets the same load-factor-based split as one that is 90% loaded in summer and 50% in winter. The average-and-peak method captures the _system-level_ temporal pattern but not _local_ variation.

**Limitation: no probability weighting.** Each above-average hour's peak allocation is proportional to its load exceedance, not to the probability that the hour triggers investment. An hour at 298 MW (2 MW below the peak) gets almost as much allocation as the 300 MW peak hour, even though the 300 MW hour is far more likely to trigger a capacity constraint. The hourly marginal method addresses this with probabilistic weighting.

---

## 4. Hourly marginal cost allocation

### What it is

The most time-granular marginal cost approach: it constructs an 8,760-hour marginal cost signal and allocates costs to groups based on their load in every hour, weighted by the marginal cost of serving load in that hour. Capacity costs are distributed to the specific hours when the system is under stress, using probabilistic methods. This is the framework used by the BAT paper (Simeone et al. 2023), the CPUC Avoided Cost Calculator, and our BAT implementation.

### The 8,760 marginal cost signal

The marginal cost in each hour has multiple components:

$$MC_h = MC^{\text{energy}}_h + MC^{\text{gen cap}}_h + MC^{\text{TX}}_h + MC^{\text{dist}}_h$$

**Energy MC**: the short-run marginal cost of the marginal generator in hour $h$. Operationalized as the locational marginal price (LMP):

$$MC^{\text{energy}}_h = LMP_h$$

This varies every hour — high when expensive peakers are running (summer afternoons, cold winter mornings), low when baseload units are on the margin (spring nights). Nonzero in every hour.

**Generation capacity MC**: the forward-looking cost of the next MW of generation adequacy, allocated to hours with probabilistic peak weighting. In a simple top-$K$ approach:

1. Identify the top $K$ hours by system load (e.g., $K = 100$).
2. Compute a threshold $T$ = load in the $(K+1)$-th hour.
3. For each of the top $K$ hours, compute exceedance weight:

$$w_h = \frac{\text{Load}_h - T}{\sum_{h' \in \text{top } K} (\text{Load}_{h'} - T)}$$

4. Allocate the annual capacity cost:

$$MC^{\text{gen cap}}_h = w_h \times c^{\text{gen cap}}_{\text{kW-yr}}$$

This assigns most of the generation capacity cost to the very highest-load hours — the hours when the system is closest to needing new generation. It is zero in all but $K$ hours.

More sophisticated approaches use **Loss of Load Probability (LOLP)** or **effective load carrying capability (ELCC)** to weight hours by their contribution to reliability risk, rather than simple load ranking.

**Transmission MC**: similar structure — forward-looking cost of the next transmission project, allocated to peak hours using exceedance or seasonal coincident peak weighting. May use seasonal weights (e.g., top 40 hours per season) rather than a single annual peak.

**Distribution MC**: forward-looking cost of the next distribution capacity increment (from MCOS project-level data), allocated to local peak hours:

$$MC^{\text{dist}}_h = w_h \times c^{\text{dist}}_{\text{kW-yr}}$$

where the weights $w_h$ may use a **Probability of Peak (PoP)** method (proportional to system or local load in the top 100 hours) rather than simple exceedance. In our implementation, distribution MC is zero in all but the top ~100 hours by utility load.

### Group allocation

Each group's economic burden is:

$$EB_j = \sum_{h=1}^{8760} L_{j,h} \times MC_h$$

This is the total marginal cost attributable to group $j$'s load pattern. It captures:

- Energy costs: proportional to kWh consumed, but weighted by when — a kWh consumed during an expensive hour costs more than a kWh during a cheap hour.
- Capacity costs: proportional to load during the specific peak hours that drive investment — not the group's own peak, but the system's (or the feeder's) peak. A group with high load during capacity-constrained hours gets a large capacity allocation; a group with high load only during off-peak hours gets almost none.

The residual is:

$$R = TRR - \sum_j EB_j$$

And must be allocated separately — by EPMC ($R_j = R \times EB_j / \sum_k EB_k$), per-customer ($R_j = R \times N_j / N$), or another method.

### Worked example

Same utility. System peaks in August. Distribution MC is concentrated in top 100 summer hours. Generation capacity MC in top 100 system-load hours. Energy MC varies hourly (higher in summer peak, lower in winter night).

Illustrative hourly MC values:

| Hour                    | Energy MC | Gen cap MC | TX MC     | Dist MC   | Total MC  |
| ----------------------- | --------- | ---------- | --------- | --------- | --------- |
| August peak (h=5000)    | $0.12/kWh | $0.40/kWh  | $0.15/kWh | $0.20/kWh | $0.87/kWh |
| August evening (h=5010) | $0.08/kWh | $0.10/kWh  | $0.04/kWh | $0.05/kWh | $0.27/kWh |
| January 6 PM (h=500)    | $0.09/kWh | $0.00      | $0.00     | $0.00     | $0.09/kWh |
| January 2 AM (h=480)    | $0.03/kWh | $0.00      | $0.00     | $0.00     | $0.03/kWh |
| Spring night (h=2200)   | $0.02/kWh | $0.00      | $0.00     | $0.00     | $0.02/kWh |

In the August peak hour, total MC is $0.87/kWh — dominated by capacity components. HP customers, who have lower summer load, contribute less:

- HP load in August peak: 100 MW → HP cost for this hour: 100,000 kW × $0.87 = $87,000
- Non-HP load in August peak: 200 MW → Non-HP cost: 200,000 kW × $0.87 = $174,000

In January 6 PM, total MC is only $0.09/kWh (energy only — no capacity MC because winter hours aren't in the top 100 system hours for this summer-peaking system):

- HP load: 170 MW → HP cost: 170,000 kW × $0.09 = $15,300
- Non-HP load: 80 MW → Non-HP cost: 80,000 kW × $0.09 = $7,200

The HP subclass gets a large energy allocation in winter (they consume a lot of kWh when energy MC is moderate) but a small capacity allocation (they contribute little during the summer hours where capacity MC is concentrated). The non-HP subclass gets the reverse: a large capacity allocation from summer peak hours.

Over 8,760 hours, the HP economic burden is dominated by energy MC, while the non-HP economic burden includes a larger share of capacity MC. The HP share of total MCRR is lower than under the traditional MCOS (which used NCP for distribution, penalizing HP for their high winter peak). This is the time-awareness improvement: hourly marginal correctly identifies that HP customers aren't driving the capacity investments that dominate the system's marginal cost.

### How hourly marginal compares to traditional marginal

**Replaces snapshot peak measures with probabilistic hourly weighting.** Instead of one CP hour for generation/TX and one NCP per feeder for distribution, hourly marginal spreads capacity costs across the top $K$ hours weighted by exceedance or probability of stress. This captures the fact that investment risk isn't concentrated in a single hour — it's distributed across a set of high-stress hours.

**Bypasses the demand/energy classification entirely.** In a traditional MCOS, every cost must be classified as demand-related or energy-related before allocation. In an hourly MCOS, the MC signal naturally integrates both: energy MC is nonzero in every hour (varying with generation cost), capacity MC is nonzero only in stress hours (varying with investment cost). There's no need to decide "is this cost demand or energy?" — the hourly signal answers the question directly.

**Captures seasonal and intra-day variation simultaneously.** Traditional MCOS uses system CP (one summer hour) for generation/TX and feeder NCP (one hour per feeder) for distribution. Hourly MCOS captures summer afternoon peaks, winter evening peaks, shoulder-season lulls, and everything in between — all in a single consistent framework.

**For HP cross-subsidies specifically**: hourly marginal is the most accurate of the four frameworks because the HP cross-subsidy is entirely about timing. HP customers add load in winter, when capacity MC is zero (in a summer-peaking system) and energy MC is moderate. Non-HP customers drive summer peaks, when capacity MC is very high. Only an hourly method with probabilistic peak weighting fully captures this temporal mismatch.

---

## 5. Comparing the frameworks

### Traditional embedded vs. hourly embedded

| Dimension                        | Traditional embedded (ACOSS)                            | Hourly embedded                                                                 |
| -------------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Time resolution**              | 1 hour (CP) or 1 number (NCP) per cost function         | 8,760 hours                                                                     |
| **Distribution cost allocation** | NCP: one number, no timing                              | Average-and-peak: hour-by-hour, with peak costs concentrated in high-load hours |
| **Demand/energy split**          | Binary classification (each dollar is demand OR energy) | Continuous (load factor determines the split, applied to every hour)            |
| **HP sensitivity**               | Low. NCP treats summer and winter peaks equally.        | Moderate. Summer peak hours carry more cost weight, reducing HP allocation.     |
| **Residual**                     | None (allocates full TRR)                               | None (allocates full TRR)                                                       |
| **Data requirements**            | Class-level peak demands, annual kWh, customer counts   | 8,760 hourly load profiles per group, resource output profiles                  |

### Traditional marginal vs. hourly marginal

| Dimension                        | Traditional marginal (NERA)                              | Hourly marginal                                                             |
| -------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------- |
| **Time resolution**              | 1 hour (CP) for gen/TX; 1 hour per feeder (NCP) for dist | 8,760 hours, all components                                                 |
| **Distribution cost allocation** | Class NCP at feeder level × unit MC                      | PoP or exceedance weights across top $K$ hours × unit MC                    |
| **Demand/energy classification** | Required (capacity MC separate from energy MC)           | Not needed (the hourly signal integrates both)                              |
| **HP sensitivity**               | Moderate. Feeder-level NCP captures some timing.         | High. Capacity MC concentrated in the specific hours that drive investment. |
| **Residual**                     | TRR − MCRR (large)                                       | TRR − total economic burden (large)                                         |
| **EPMC equivalence**             | Under EPMC, structurally similar to ACOSS                | Under EPMC, structurally similar to hourly embedded                         |
| **Data requirements**            | Class peak demands at system and feeder level, unit MCs  | 8,760 hourly load profiles per group, 8,760 hourly MC signal                |

### Hourly embedded vs. hourly marginal

Both use 8,760 hours. They differ in cost basis and allocation logic:

| Dimension                  | Hourly embedded                                                                                             | Hourly marginal                                                                                                                                           |
| -------------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cost basis**             | Historical accounting costs (actual revenue requirement)                                                    | Forward-looking economic costs (avoided/marginal)                                                                                                         |
| **What it allocates**      | The full TRR — every dollar of recorded cost                                                                | The MCRR — the marginal slice. Residual allocated separately.                                                                                             |
| **Capacity cost logic**    | Average-and-peak: costs proportional to load exceedance above average                                       | Probabilistic: costs proportional to probability of system stress                                                                                         |
| **Key difference**         | An hour at 295 MW and an hour at 300 MW get similar peak allocation (both above average by similar amounts) | The 300 MW hour gets much more allocation (much higher probability of triggering investment)                                                              |
| **Residual treatment**     | No residual — the full TRR is allocated                                                                     | Explicit residual requiring a separate allocation choice (EPMC, per-customer, etc.)                                                                       |
| **Efficiency orientation** | Historical equity — "what did each group's historical behavior cost?"                                       | Forward-looking efficiency — "what does each group's behavior cost the system going forward?"                                                             |
| **HP outcome**             | Qualitatively similar to hourly marginal if summer hours carry most peak weight                             | Correctly concentrates capacity costs in the stress hours that drive investment, giving HP the most accurate (and typically smallest) capacity allocation |

### When the methods agree and when they diverge

For the question "do HP customers overpay under current flat volumetric rates?", all four methods should give qualitatively similar answers — HP customers are charged proportionally to annual kWh, but their cost responsibility is lower because they contribute less to capacity-driving peaks. The cross-subsidy direction is robust across methods.

The methods diverge on **magnitude**. Traditional embedded (ACOSS) typically produces the largest HP allocation (because NCP penalizes HP for their high winter peak). Hourly marginal typically produces the smallest HP allocation (because capacity MC is concentrated in summer stress hours where HP contributes little). Traditional marginal and hourly embedded fall in between.

The choice of residual allocator (for the marginal methods) also matters. Under EPMC, the HP share of the residual tracks the HP share of MCRR — which is already lower than NCP-based shares, so the cross-subsidy finding is amplified. Under per-customer, the HP share of the residual equals the HP share of customers (20% in our example) — neutral to load profile, so the cross-subsidy finding depends entirely on the economic burden split.

---

## References

- NARUC, _Electric Utility Cost Allocation Manual_ (1992)
- Lazar, J., Chernick, P., Marcus, W. & LeBel, M., _Electric Cost Allocation for a New Era_ (RAP, 2020)
- Simeone, C., et al., "The bill alignment test: A measure of utility tariff performance," _Utilities Policy_ 85 (2023)
- Brown, T. & Faruqui, A., _Structure of Electricity Distribution Network Tariffs: Recovery of Residual Costs_ (Brattle Group / AEMC, 2014)
- Pérez-Arriaga, I.J., Jenkins, J.D. & Batlle, C., "A regulatory framework for an evolving electricity sector," _IEEE Power and Energy Magazine_ 15(3) (2017)
- Borenstein, S., "The economics of fixed cost recovery by utilities," _The Electricity Journal_ 29(7) (2016)
- Schittekatte, T. & Meeus, L., "Least-cost distribution network tariff design in theory and practice," _The Energy Journal_ 41(5) (2020)
