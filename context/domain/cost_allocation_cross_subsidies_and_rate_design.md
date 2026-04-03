# Cost allocation, cross-subsidies, and rate design: a step-by-step guide

How cross-subsidies are diagnosed (cost allocation), how different cost allocation methods relate to each other, at what level of granularity allocation must be performed to reveal intra-class cross-subsidies, and how rate design is the separate downstream step that fixes them.

---

## Part 1: Diagnosing cross-subsidies through cost allocation

### 1.1 Cross-subsidies are statements about cost allocation, not rate design

A cross-subsidy exists when one group of customers pays more than their allocated cost of service and another group pays less. To prove a cross-subsidy, you need two numbers for each group:

1. **What the group should pay** — determined by a cost allocation methodology.
2. **What the group actually pays** — determined by the tariff applied to their consumption.

If these don't match, there is a cross-subsidy. The diagnosis is entirely in the cost allocation step. Rate design is the fix, not the finding.

### 1.2 Cost allocation can be performed at three levels of granularity

| Level                   | Groups                                                     | What it reveals                                                                                      |
| ----------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Customer class**      | Residential, Commercial, Industrial, Lighting, etc.        | Inter-class cross-subsidies (does the residential class as a whole overpay?)                         |
| **Subclass**            | HP vs. non-HP within residential; or LMI vs. non-LMI, etc. | Intra-class cross-subsidies between subgroups with systematically different load profiles            |
| **Individual customer** | Each building / meter                                      | Full distribution of cost responsibility; identifies which individual customers are over/underpaying |

The standard rate case performs cost allocation at the **class level only**. The utility runs an Allocated Cost of Service Study (ACOSS) or Marginal Cost of Service Study (MCOS), computes each class's revenue requirement, and sets class-level tariffs. If the allocation is done accurately and the commission sets each class's revenue at its allocated cost, inter-class cross-subsidies are eliminated by construction.

But this tells you nothing about what's happening _within_ a class. If HP customers and non-HP customers share the same residential tariff, and their load profiles differ systematically, one subgroup may be overpaying and the other underpaying — and the class-level allocation cannot detect this. **To show an intra-class cross-subsidy, you must perform cost allocation at least at the subclass level.** This is what the Bill Alignment Test does: it performs cost allocation at the individual customer level, then aggregates to subclasses to reveal the systematic pattern.

### 1.3 The four cost allocation frameworks

Cost allocation methods vary along two dimensions:

- **Cost basis**: embedded (historical accounting costs) vs. marginal (forward-looking economic costs)
- **Time granularity**: traditional (snapshot — one or a few peak hours) vs. hourly (8,760 hours)

This produces four frameworks (see `domain/traditional_vs_hourly_ecoss_and_mcos.md` for full details):

|              | Traditional (snapshot)                                                                                                                  | Hourly (8,760)                                                                                                                         |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Embedded** | NARUC three-step: functionalize, classify, allocate. Demand costs allocated by CP or NCP, energy costs by kWh, customer costs by count. | Maps actual accounting costs to hours using average-and-peak logic or direct resource-to-hour matching.                                |
| **Marginal** | NERA method: unit capacity costs × class peak contribution (CP for TX, NCP for dist). Energy at average marginal energy cost × kWh.     | Avoided costs assigned to every hour. Capacity costs distributed to high-stress hours using probabilistic weighting (PoP, LOLE, PCAF). |

Each framework can be applied at any level — class, subclass, or individual customer — though in practice traditional methods are almost always applied at the class level only.

### 1.4 Why these frameworks are more similar than they appear

Despite different theoretical motivations (historical equity vs. forward-looking efficiency) and different terminology (functionalize/classify/allocate vs. marginal cost + residual), the four frameworks are doing fundamentally the same thing when you look at what they produce:

**They all measure each group's current behavior relative to cost drivers, and use that measurement to split the revenue requirement.**

- Traditional embedded (ACOSS): measures the class's share of system peak (CP), class peak (NCP), total kWh, and customer count. Multiplies these shares by the corresponding cost pools. The result is the class's allocated revenue requirement.
- Traditional marginal (MCOS): measures the class's peak contribution and kWh, multiplies by unit marginal costs, gets a Marginal Cost Revenue Requirement (MCRR). The MCRR is less than the total revenue requirement (because MC < AC). The gap is the residual.
- Hourly marginal: measures each group's load in each hour, multiplies by the hourly marginal cost signal, sums to get the economic burden. The gap between total economic burden and total revenue requirement is the residual.
- Hourly embedded: measures each group's load in each hour, multiplies by each resource's hourly cost (proportional to the resource's output in that hour), sums directly to the full revenue requirement.

**The deep equivalence**: all four measure current behavior as a proxy for cost-causation. The difference is the precision of the measurement — how many hours, how many cost components, how the capacity cost is spread across time. The embedded methods allocate the full revenue requirement directly. The marginal methods allocate a marginal slice and then must deal with the residual separately.

### 1.5 The residual allocation choice is what breaks the equivalence

For **embedded** methods, there is no residual. The full revenue requirement is allocated directly — every dollar of historical cost is assigned to a group through the functionalize/classify/allocate process. The allocation of sunk costs is implicit in the demand and customer allocators: when the ACOSS assigns distribution plant to classes by NCP, it is allocating sunk transformer costs based on current peak behavior. The assumption — current peak behavior ≈ historical cost-causation — is baked in, never stated, and never questioned.

For **marginal** methods, the residual is explicit and must be allocated separately. This is where a choice appears that has no analog in the embedded world:

- **EPMC (equi-proportional marginal cost)**: scale all marginal-cost-based allocations up by a uniform factor $K = TRR / \text{total MCRR}$ so that the total recovers the full revenue requirement. Each group's share of the residual ends up proportional to its share of the MCRR. **Under EPMC, the marginal method produces the same conceptual result as an embedded method**: current cost-causation is used as a proxy for all cost-causation, marginal and sunk alike. The only difference is measurement precision.

- **Per-customer**: each customer (or each customer within a subclass) pays an equal share of the residual: $R/N$. This is a different allocation philosophy: it says sunk costs should not be allocated by cost-causation (for normative and/or efficiency reasons — see `rate-design-platform/context/domain/bat_mc_residual/fairness_in_cost_allocation.md`). The normative argument: cost-causation fails for sunk costs because the original causers may be gone and the current beneficiaries are everyone on the system. The efficiency argument: allocating sunk costs by current behavior distorts volumetric prices above marginal cost, discouraging efficient electrification.

- **Other methods** (income-graduated, historical consumption, contracted capacity): various compromises between cost-causation and non-distortion. See `rate-design-platform/context/methods/bat_mc_residual/residual_allocation_lit_review_and_cairo.md`.

**The key implication**: if you choose EPMC for residual allocation, the marginal and embedded methods are doing the same thing at different levels of precision. They both say "current behavior drives all cost allocation." The marginal method just has a finer instrument — hourly, component-by-component, probabilistically weighted — compared to the embedded method's single-number CP or NCP allocator. If you choose per-customer residual allocation, the marginal method is doing something different: it splits the revenue requirement into a cost-causation-based component (marginal costs) and a non-cost-causation-based component (the residual), and only the first tracks behavior.

### 1.6 Why time-awareness matters for heat pumps

The cross-subsidy between HP and non-HP customers is driven by _when_ they consume. HP customers add winter load (heating); non-HP customers drive summer peaks (cooling). The cost allocation method must capture this temporal difference to measure the cross-subsidy accurately.

**Traditional embedded (ACOSS)**: typically uses a single system coincident peak (summer in most U.S. systems) for transmission costs and NCP for distribution. NCP is the class's maximum demand regardless of when it occurs. Neither measure distinguishes between a customer who peaks at 20 kW in January and one who peaks at 20 kW in July. If distribution investment is driven by summer loading, a winter-peaking HP customer is allocated the same distribution cost as a summer-peaking non-HP customer with the same NCP — even though the HP customer isn't driving the investment. This is a fatal flaw for detecting the HP cross-subsidy.

**Traditional marginal (MCOS)**: partially time-aware. Transmission costs are allocated by system CP (one or a few hours), so timing matters for TX. Distribution costs are allocated by class NCP at the circuit level — the sum of the class's load during each feeder's peak hour. This captures _some_ timing: if feeders peak in summer, HP customers contribute less to feeder peaks and get a smaller distribution allocation. But NCP is still a single number per feeder, not a full hourly profile.

**Hourly embedded**: depends on the allocation logic. Many modern studies use the average-and-peak method: the "average" component (proportional to the system load factor) is spread across all hours and allocated by kWh share; the "peak" component is allocated to high-load hours. If the peak component correctly identifies summer hours as the cost-driving hours, HP customers get less peak allocation and the cross-subsidy becomes visible. The precision depends on how the peak hours are identified and weighted.

**Hourly marginal**: the most time-aware. Capacity marginal costs are zero in most hours and concentrated in the specific hours when the system is capacity-constrained — identified probabilistically (PoP, LOLE, top-$K$ exceedance). If the distribution system is summer-constrained, capacity MC is concentrated in summer peak hours. HP customers, who add little load during those hours, get a small capacity MC allocation. Non-HP customers, who drive summer peaks, get a large one. The cross-subsidy is measured with full temporal precision: which hours matter, how much load each group has in those hours, weighted by the probability that each hour triggers investment.

**The progression**: traditional embedded → traditional marginal → hourly embedded → hourly marginal is a progression from "whose peak demand is bigger" to "whose load during the specific hours that cause specific infrastructure investments is bigger." For heat pumps — where the entire cross-subsidy story is about _timing_ — you need at least hourly granularity and ideally probabilistic peak weighting.

### 1.7 Cost allocation at the subclass level

Any of the four frameworks can be applied at the subclass level. The mechanics are straightforward: instead of computing the residential class's CP contribution, NCP, or hourly load profile, you compute these separately for the HP subclass and the non-HP subclass, and allocate costs to each.

**Subclass allocation with embedded methods:**

$$RR_{\text{HP}} = \sum_f \left( \text{FunctionalizedCost}_f \times AF_{\text{HP},f} \right)$$

where $f$ indexes cost functions (generation, TX, distribution, customer) and $AF_{\text{HP},f}$ is the HP subclass's allocation factor for function $f$ (e.g., HP share of residential class CP for TX, HP share of residential class NCP for distribution, HP customer count share for customer costs). The full residential revenue requirement is split between HP and non-HP by these factors.

**Subclass allocation with hourly marginal methods:**

$$RR_{\text{HP}} = \underbrace{\sum_h L_{\text{HP},h} \times MC_h}_{\text{HP economic burden}} + \underbrace{g(\text{HP}, R)}_{\text{HP residual share}}$$

where $L_{\text{HP},h} = \sum_{i \in \text{HP}} L_{i,h}$ is the aggregate HP load in hour $h$, and $g(\text{HP}, R)$ is the residual allocation — either EPMC ($R \times EB_{\text{HP}} / EB_{\text{total}}$), per-customer ($R \times N_{\text{HP}} / N$), or some other method.

**The cross-subsidy finding**: once you have $RR_{\text{HP}}$ and $RR_{\text{non-HP}}$, compare them to the revenue each subclass actually pays under the current tariff. If HP customers pay more than $RR_{\text{HP}}$, they are being cross-subsidized (overpaying). If they pay less, they are cross-subsidizing others.

### 1.8 Cost allocation at the individual customer level

You can go one level deeper and allocate costs to each individual customer. This is what the BAT does:

$$\text{AllocatedCost}_i = \sum_h L_{i,h} \times MC_h + f(i, R)$$

where $f(i, R)$ is the customer's residual share. Bill alignment is then:

$$\text{BA}_i = \frac{\text{ActualBill}_i}{\text{AllocatedCost}_i}$$

Customer-level allocation gives you the full distribution of cost responsibility — not just subclass averages but percentiles, outliers, story buildings, bill impact histograms. It lets you see that the cross-subsidy is not uniform: some HP customers overpay more than others, depending on their specific load shape, location, and building characteristics.

### 1.9 Customer-level allocation aggregated to subclass = direct subclass allocation

A critical mathematical property: **summing customer-level allocations to the subclass level produces exactly the same subclass revenue requirement as doing the allocation directly at the subclass level.** This holds for any linear residual allocator.

**Proof for the economic burden:**

$$\sum_{i \in \text{HP}} \sum_h L_{i,h} \times MC_h = \sum_h \left(\sum_{i \in \text{HP}} L_{i,h}\right) \times MC_h = \sum_h L_{\text{HP},h} \times MC_h$$

This is just swapping the order of summation. The left side is "compute each customer's economic burden, then sum." The right side is "compute the subclass load shape, then compute the subclass economic burden." Identical.

**Proof for per-customer residual:**

$$\sum_{i \in \text{HP}} \frac{R}{N} = \frac{N_{\text{HP}}}{N} \times R$$

Summing each HP customer's $R/N$ equals the subclass share under per-customer allocation.

**Proof for EPMC residual:**

$$\sum_{i \in \text{HP}} R \times \frac{EB_i}{EB_{\text{total}}} = R \times \frac{\sum_{i \in \text{HP}} EB_i}{EB_{\text{total}}} = R \times \frac{EB_{\text{HP}}}{EB_{\text{total}}}$$

Summing each HP customer's EPMC residual equals the subclass EPMC share.

The same holds for volumetric and peak allocators. **Any linear residual allocator satisfies this property.** Therefore, customer-level BAT and direct subclass MCOS give the same subclass cross-subsidy finding. The customer-level approach is strictly more informative — it produces the same subclass answer plus individual-level diagnostics.

### 1.10 Residual allocation can differ by level

The cost allocation at each level is a separate step, and you are free to use different residual allocation methods at different levels. For example:

- **EPMC at the subclass level**: the HP subclass's total residual share is proportional to its share of total economic burden. This follows cost-causation logic: the subclass whose load causes more marginal cost bears more residual.
- **Per-customer within each subclass**: once the HP subclass's residual is determined, it is divided equally among all HP customers. Every HP customer pays the same fixed residual charge, but that charge differs from what non-HP customers pay (because the subclass EPMC shares differ).

This hybrid (EPMC across subclasses, per-customer within) gives:

$$R_i = \frac{R \times EB_{\text{HP}}}{EB_{\text{total}} \times N_{\text{HP}}} \quad \text{for } i \in \text{HP}$$

The subclass cross-subsidy finding is the same as under full EPMC (the HP subclass total is $EB_{\text{HP}} \times K$). But within the subclass, every customer pays the same residual — no individual-level EPMC weirdness where one customer's residual varies because they ran their AC a few extra hours.

You could also use EPMC at the class level, per-customer at the subclass level, and stop — never going to individual customers at all. Or EPMC at the class level, EPMC at the subclass level, and per-customer at the individual level. The levels are independent.

### 1.11 Corollary: presenting BAT results as subclass-level cost allocation

The BAT computes cost allocation at the individual customer level. But you do not need to present results that way. Because customer-level BAT aggregated to subclass = direct subclass allocation (§1.9), you can present the same numbers as a subclass-level cost allocation study.

This can be useful for audiences who find customer-level residual allocation unfamiliar or counterintuitive. Two specific concerns:

- **Per-customer residual at the individual level** can feel strange: "my neighbor and I pay the same delivery infrastructure costs even though my house is twice as big." At the subclass level, this becomes "every residential customer contributes the same share of the residual" — which is just a standard fixed charge, the most common residential rate design in the country.
- **EPMC residual at the individual level** can feel arbitrary and volatile: "my residual varies because I happened to consume more during a few expensive hours." At the subclass level, this becomes "the HP subclass's share of the residual is proportional to its share of marginal costs" — which is standard MCOS-based cost allocation, the same logic utilities use for inter-class allocation.

If you do EPMC at the subclass level, you can frame the result as: "We are doing cost allocation at the subclass level using the same logic as a traditional MCOS study, but with a more accurate, time-aware measurement of cost-causation. Our marginal cost signal captures which hours actually drive infrastructure investment — not just who has the biggest peak. This matters for heat pumps because the cross-subsidy is about timing: HP customers add winter load but current flat rates charge them as if they were driving summer peaks."

This is a true statement. It is mathematically equivalent to running BAT at the customer level and aggregating. And it lands in a conceptual framework that regulators and utility witnesses already understand.

(Of course, you could also do hourly ACOSS from the start, since the precise allocation differs depending on the method — but the finding about HP cross-subsidies should be qualitatively similar across any time-aware method, because the cross-subsidy is driven by the temporal mismatch between HP load patterns and system peak, which any hourly method will capture.)

---

## Part 2: Fixing the cross-subsidy through rate design

Cost allocation diagnoses the problem. Rate design fixes it. These are separate steps — you can change the rate design without changing the cost allocation, and vice versa. The cost allocation determines each group's revenue requirement. The rate design determines how that revenue is collected from customers' bills.

Once subclass cost allocation shows that HP customers are overpaying relative to their cost responsibility, there are two broad approaches to closing the gap through rate design.

### 2.1 Approach 1: Separate tariff for the subclass

Create a distinct rate schedule for HP customers, calibrated to collect the HP subclass's revenue requirement from HP customers specifically. This is the same logic as having separate rate classes (residential, commercial, industrial) — each class has its own tariff designed to match its allocated costs.

**How it works**: the HP subclass revenue requirement is $RR_{\text{HP}}$. Design a tariff — some combination of customer charge, demand charge, energy charge, and/or time-varying components — that collects $RR_{\text{HP}}$ from HP customers' consumption patterns. Non-HP customers remain on the default tariff, which is recalibrated to collect $RR_{\text{non-HP}}$.

**Examples**:

- A seasonal rate with a lower $/kWh delivery charge in winter (when HP customers consume heavily but capacity costs are low) and a higher charge in summer. The seasonal structure shifts revenue collection from HP toward non-HP by aligning the price signal with cost-causation.
- A TOU rate within the HP tariff that charges less during off-peak hours (when HP heating loads are concentrated) and more during on-peak hours.
- A demand-based HP tariff with lower volumetric charges and higher demand charges, if HP customers tend to have lower peak demand relative to their total consumption.

**Advantages**: eliminates the intra-class cross-subsidy by construction (each subclass has its own tariff calibrated to its own costs). Provides the cleanest price signal to each group.

**Challenges**: requires identifying which customers qualify (enrollment, metering, or billing system changes). Creates a new rate schedule that must be maintained. Raises questions about who can opt in/out and how to handle customers who install heat pumps in the future.

### 2.2 Approach 2: Redesign the common tariff to reduce the cross-subsidy

Keep all residential customers on the same rate schedule, but change the tariff structure so that revenue collected from each subclass moves closer to their cost allocation.

**How it works**: instead of a flat volumetric $/kWh rate that allocates costs proportionally to annual kWh (which over-charges high-kWh winter consumers and under-charges high-kWh summer consumers, in a summer-peaking system), restructure the tariff so that the price signal better reflects when costs are incurred.

**Examples**:

- **Time-of-use rates**: define peak/off-peak periods aligned with system capacity constraints (e.g., summer afternoons are on-peak, winter nights are off-peak). HP customers, who consume heavily in winter off-peak, pay less per kWh for most of their consumption. Non-HP customers, who consume heavily in summer on-peak, pay more. The cross-subsidy shrinks because the price ratio between peak and off-peak approximates the marginal cost ratio.
- **Seasonal rates**: higher volumetric delivery charge in summer, lower in winter. Simpler than full TOU but captures the main seasonal dimension of the cross-subsidy.
- **Demand charges for residential**: add a $/kW charge based on each customer's peak demand, and reduce the volumetric $/kWh charge correspondingly. This shifts cost recovery from energy-proportional (which penalizes HP customers for high winter kWh) to demand-proportional (which tracks the actual cost driver). Requires interval metering (AMI).
- **Restructuring the customer charge vs. volumetric split**: increase the fixed customer charge to recover more of the sunk/customer-related costs, and reduce the volumetric charge toward marginal cost levels. This reduces the residual embedded in the $/kWh price, narrowing the gap between marginal cost and retail price. (But this approach faces the regressivity and efficiency concerns debated in Docket 4770 — see `methods/ri_docket_4770_rate_design_arguments.md`.)

**Advantages**: no enrollment, no separate rate schedule, no identification of HP customers required. All customers face the same tariff. The cross-subsidy reduction happens automatically through the rate structure.

**Limitations**: a common tariff can reduce but rarely eliminate the cross-subsidy. TOU periods are coarse approximations of the 8760 MC signal — a 2-period TOU captures summer/winter or peak/off-peak but loses the finer within-season variation. Seasonal rates capture the seasonal dimension but not intra-day variation. The more precisely the common tariff tracks marginal costs, the more it reduces the cross-subsidy — but at the cost of complexity and customer understanding.

### 2.3 The tradeoff between the two approaches

|                           | Separate tariff (Approach 1)                                         | Redesigned common tariff (Approach 2)                |
| ------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------- |
| Cross-subsidy elimination | Full (by construction)                                               | Partial (depends on precision of the rate structure) |
| Administrative complexity | Higher (new rate schedule, enrollment)                               | Lower (one tariff for all)                           |
| Price signal quality      | Can be precisely calibrated to HP cost structure                     | Limited by TOU/seasonal period coarseness            |
| Customer understanding    | Must explain why HP customers get a different rate                   | All customers see the same rate; simpler             |
| Gradualism                | New rate is a visible change for HP customers                        | Can be phased in for all customers                   |
| Future-proofing           | Requires updating as HP penetration grows and cost allocation shifts | Automatically adapts as load shapes change           |

In practice, these approaches are not mutually exclusive. A jurisdiction could offer a separate HP tariff (Approach 1) while also moving the default tariff toward TOU (Approach 2), so that even customers who don't opt into the HP rate benefit from a more cost-reflective structure.

### 2.4 Rate design is about recovery, not allocation

A final point that is easy to lose sight of: the rate design step determines _how revenue is collected_, not _how much each group owes_. The cost allocation step determines what each group owes. The rate design step determines the tariff structure that collects that amount.

This means:

- You can do cost allocation accurately (hourly marginal, subclass-level, with whatever residual method you choose) and then implement a rate design that is simple and imprecise (flat volumetric). You'll know the cross-subsidy exists (from the allocation), you'll know the rate design doesn't fix it (from comparing bills to allocations), and you'll have a quantified gap.
- You can do cost allocation and rate design using different principles. For example, allocate the marginal cost component by cost-causation (hourly MC × load), allocate the residual by per-customer or income-graduated, and then design a tariff that recovers the MC component through TOU volumetric charges and the residual through a fixed monthly charge. The allocation tells you each customer's cost responsibility in dollars; the tariff is a separate mechanism that tries to collect approximately that amount through billing determinants that customers can observe and respond to.
- You can have a rate design that is "efficient" (prices at marginal cost levels, residual in a fixed charge) but produces a different revenue-from-each-subclass than the cost allocation implies. This happens when the tariff is designed for the class as a whole without regard to subclass cost allocation. The tariff may be efficient in the sense that it sends correct marginal price signals, but it can still produce cross-subsidies between subclasses if the fixed charge / volumetric split doesn't happen to match the subclass cost allocation.

The purpose of doing cost allocation at the subclass level is to _see_ these mismatches. The purpose of rate design is to _fix_ them. They are different tools for different jobs, even though they are often discussed as if they were the same thing.
