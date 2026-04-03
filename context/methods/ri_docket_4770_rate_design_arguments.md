# Rate design arguments in RIPUC Docket 4770

Reconstructed from direct testimony of all intervenors in National Grid's 2018 Rhode Island distribution rate case (Docket 4770). This document focuses on the reasoning chains behind each party's rate design positions — not just what they recommend, but why.

Sources (all in `reports2/context/sources/ri_hp_rates/`):

- `ripuc_4770_direct_testimony_neri_rabago.md` — Karl Rábago, on behalf of the Northeast Clean Energy Council (NERI)
- `ripuc_4770_direct_testimony_acadia_lebel.md` — Mark LeBel, Acadia Center
- `ripuc_4770_direct_testimony_ridiv_athas.md` — John Athas, Daymark Energy Advisors, on behalf of the RI Division of Public Utilities
- `ripuc_4770_direct_testimony_warlmat_tillman.md` — Gregory Tillman, on behalf of Walmart
- `ripuc_4770_direct_testimony_wileycenter.md` — George Wiley Center
- `ripuc_4770_direct_testimony_oer.md` — Office of Energy Resources

For Tillman's COSS methodology critique (class consolidation, billing demand error, intra-class load factor subsidies), see the companion document `methods/bat_mc_residual/tillman_coss_rate_design_critique.md`.

---

## National Grid's proposal

National Grid proposed a residential rate design with:

- Customer charge increased from $5/month to $8.50/month (a 70% increase)
- Volumetric charge increased from $0.03664/kWh to $0.04438/kWh (21% increase)
- This shifts residential revenue collection from 20% fixed / 80% volumetric to 26% fixed / 74% volumetric

The Company's justification rested on two pillars:

1. **Customer-related costs from the ACOSS.** The 2017 Allocated Cost of Service Study (ACOSS) determined $9.61/month in customer-related costs for the residential class (up from $7.57 in the 2012 ACOSS). The $8.50 proposal is a partial step toward that level.
2. **A "maximum fixed monthly charge" that includes demand-related costs.** Witness Gorman argued that the first 0.5 kW of demand — a level exceeded by 90% of residential customers each month — represents a minimum demand that should be recovered through the fixed charge. At $11.57/kW-month in demand-related costs, this adds $5.78/month, bringing the "maximum" to $15.39/month. The proposed $8.50 is 55% of that ceiling.

For low-income customers (Rate A-60): equalize A-60 and A-16 base rates, phase in the customer charge over 3 years, and replace the current base-rate discount with a 15% total-bill discount.

For large demand (Rate G-32): a three-part rate with $1,100/month customer charge + $5.00/kW demand charge (over 200 kW) + $0.00631/kWh energy charge.

---

## The central debate: should demand-related costs be recovered through fixed or volumetric charges?

This is the deepest substantive question in the docket, and the intervenors split on it in a way that reveals a genuine tension in rate design theory.

### The utility's argument: revenue/rate stability and minimum demand universality

National Grid's stated justification for including demand-related costs in the customer charge had two parts. First, a stability argument: doing so would "align the utility's revenue and costs more closely, and help stabilize the utility's revenue and customers' costs" (Gorman testimony, p. 27). Second, a universality argument: nearly all residential customers (90% each month, 98% at least once per year) exceed 0.5 kW of demand, so the demand-related unit cost ($11.57/kW-month) times 0.5 kW yields $5.78/month that everyone effectively incurs anyway. The reasoning amounts to: this demand level is universal, so it's effectively a fixed cost of being a customer — might as well put it in the fixed charge.

The argument does not engage with the question of what price signal the fixed charge sends or whether customers can respond to a demand signal. Rabago characterizes the underlying premise more bluntly: "because these demand-related costs are fixed, the charge for these costs should be fixed, too." That's his framing of what he takes to be the implicit logic, not Gorman's words.

### Rabago's counter-argument: cost structure and rate structure serve different purposes

Rabago (NERI) delivers the most developed theoretical response. His argument has several independent layers:

**1. There is no ratemaking principle that requires cost structure to be replicated in rate design.** The COSS determines how to allocate costs to customer classes. Rate design determines how to collect an already-allocated revenue requirement from customers within a class. These are separate steps with separate objectives. Cost classification as "fixed" or "variable" tells you something about how costs behave over a given time horizon — it tells you nothing about which billing determinant best recovers those costs.

**2. All costs are variable given sufficient time.** The fixed/variable distinction is an artifact of the time horizon. A distribution transformer is "fixed" over its accounting life, but loading during high demand shortens its useful life. Demand reductions extend that life and defer the next capital expenditure. A volumetric charge sends the price signal that encourages the demand reductions that reduce future fixed costs. A fixed charge suppresses that signal.

**3. Residential customers can only control demand through energy use.** This is Rabago's most practically grounded point. Without demand meters (no AMI in RI at the time), residential customers have no way to respond to a demand signal distinct from an energy signal. Their demand is a function of their home's energy performance (often a rented home they can't retrofit), their appliances (expensive to replace), and the weather (uncontrollable). The only lever they have is energy consumption. Therefore, volumetric energy rates are the best available proxy for sending both energy and demand cost-causation signals to residential customers. Demand charges are appropriate for large C&I customers, who do have demand meters, load management capability, and experience with demand-based billing.

**4. Higher fixed charges harm low-use customers, who are disproportionately low-income, elderly, and minority.** Rabago cites NCLC data (from the 2009 Residential Energy Consumption Survey) showing that in RI, CT, ME, NH, and VT, median electricity usage rises monotonically with income: < $25k → 3,904 kWh; ≥ $100k → 9,957 kWh. The same pattern holds for age (over-65 households use 5,275 vs. 7,376 kWh) and race (Asian 3,369 kWh, Latino 4,794 kWh vs. Caucasian 7,266 kWh). National Grid's proposed $5 → $8.50 customer charge increase would cause bill increases of 12.5% for a 150 kWh/month customer but only 3.9% for a 2,000 kWh/month customer. The rate change is economically regressive.

**5. Higher fixed charges weaken incentives for EE, DG, and demand response.** Every dollar shifted from the volumetric charge to the fixed charge reduces the per-kWh savings from investing in efficiency, installing solar, or shifting load. This undermines RI's Least-Cost Procurement mandate and Power Sector Transformation goals. Rabago cites Peter Kind (the author of EEI's own "Disruptive Challenges" paper) acknowledging that fixed charges "do not promote efficiency of energy resource demand and capital investment" and "reduce customer control over energy costs."

**6. Fixed-charge recovery insulates the utility from the consequences of bad forecasting.** If demand falls short of the forecast used to size infrastructure, volumetric under-recovery creates pressure to improve forecasting and embrace DER. Fixed-charge recovery eliminates that pressure — the utility collects regardless of whether customers reduce demand. This is the monopoly-incentive argument: guaranteed cost recovery through fixed charges perpetuates the capital bias that Power Sector Transformation is trying to correct.

**7. The Company's demand-charge calculation is statistically invalid.** National Grid's proposal to include demand-related costs in the customer charge was based on a sample of 230 of 440,000 residential customers (and 153 of 52,000 small commercial). The Company didn't demonstrate the sample was representative, didn't show how 0.5 kW of non-coincident demand causes costs, and didn't explain how class-wide average demand costs per kW relate to any individual customer's actual cost responsibility. The Company conducted no evaluation of price elasticity.

### Tillman's argument for the opposite conclusion (large demand class)

Tillman (Walmart) reaches the opposite rate design recommendation for Rate G-32 (large demand, > 200 kW): eliminate the energy charge entirely and recover all costs through demand charges. His reasoning mirrors Rabago's framework — rate structure should reflect cost causation — but applies it to a class where the conditions are different:

- The COSS identified **zero energy-related distribution costs** for G-32. The functional classification includes only customer-related and demand-related costs. An energy charge for a class with no energy costs fails the Company's own stated guiding principle that rates should "reflect the nature of the costs they recover."
- Large demand customers **have demand meters** and can directly manage peak demand independently of energy use. The demand charge is a precise instrument for this class; the energy charge is not.
- Recovering demand costs via energy charges creates **intra-class load factor subsidies**: a high-LF customer (Walmart, running long hours) and a low-LF customer with identical peak demand pay different amounts for identical cost responsibility. Tillman's numerical example shows a $333/year subsidy — one-third of cost responsibility — transferred from the 60% LF customer to the 30% LF customer.

### Reconciling Rabago and Tillman

These positions aren't contradictory — they reach opposite conclusions because they apply the same principle (rate structure should send cost-reflective signals) to classes with different characteristics:

|                         | Residential (Rabago)                      | Large demand (Tillman)                     |
| ----------------------- | ----------------------------------------- | ------------------------------------------ |
| Metering                | No demand meters                          | Demand meters                              |
| Customer's demand lever | Energy use is the only lever              | Can manage peak demand directly            |
| COSS energy costs       | Not discussed                             | Zero — all demand and customer             |
| Optimal rate structure  | Volumetric (best proxy for demand signal) | Demand-only (precise match to cost driver) |

The key variable is whether the customer can respond to a demand signal independently of energy use. Where they can (large C&I), demand charges are the right instrument. Where they can't (residential without AMI), volumetric rates are the best available proxy.

---

## The customer charge: what costs belong in it?

All intervenors agree that the customer charge should be limited to costs that vary with the number of customers (the "cost of connection"). The dispute is over what counts.

### National Grid's definition

The Company's ACOSS assigned $50.8M to the residential class as customer-related costs, split between:

- **Secondary distribution system** (service drops): $18.2M ($3.43/month)
- **Billing/Customer Service** (meters, billing, A&G): $32.6M ($6.17/month)

This produces the $9.61/month figure. The increase from the 2012 ACOSS ($7.57) was driven almost entirely by a $10.1M (+125%) increase in secondary system revenue requirements (service-drop accounts).

### Rabago: A&G and General Plant costs are not customer-related

Rabago argues that the Billing function includes $26.4M in General Plant ($10.3M) and Administrative & General ($16.1M) costs that do not vary exclusively with customer count. These costs bear a relation to demand and should not be classified as customer-related. His reasoning:

- **Modern meters do more than log consumption.** Smart meters support energy efficiency, demand response, demand charges, EV charging scheduling, and grid communication. Categorizing all meter costs as customer-related was reasonable when meters were analog consumption loggers. It is "a simple answer that is simply wrong" in a world of multi-function AMI.
- **Customer service staff increasingly support EE and DER programs.** As staff spend more time referring customers to efficiency programs and managing DER integration, their costs are no longer purely a function of customer count.

Removing A&G and General Plant drops the residential customer-related cost to **$5.90/month** — below the current $5 customer charge. For small commercial (C-06), the same correction drops the customer-related cost from $13.78 to **$7.48/month** — below the current $10 charge.

### LeBel: same direction, less granular

LeBel (Acadia Center) makes overlapping arguments: demand-related costs are categorically inappropriate in the customer charge; and National Grid's definition of customer-related costs is over-inclusive (citing the same A&G accounts). After removing the A&G overhead, he estimates the customer-related cost at $7.28/month for residential. He also cites the RAP "Smart Rate Design" principles (customer charge ≤ cost of connection) and the Bonbright principles. His recommendation: leave the residential charge at $5 pending a corrected ACOSS.

### Athas: the pragmatist's middle ground

Athas (Division) is the most analytical and least ideological. He acknowledges the ACOSS cost-causation argument for a higher customer charge — he explicitly notes that the $10.1M increase in secondary-system costs (service drops) "suggests that an increase in monthly fixed charges would be consistent with cost causation principles." But he opposes the increase for pragmatic reasons:

1. **Too aggressive and too fast.** The 70% increase violates gradualism. Low-use customers (< 200 kWh/month) would face total bill increases of 10–47% under National Grid's proposal, vs. 1–5% at the $5 status quo.
2. **AMI changes the calculus.** AMI deployment is imminent. Once AMI is installed, the Commission can implement TOU rates, demand charges, critical peak pricing, and other mechanisms that more precisely allocate demand costs. Locking in a large customer charge increase now forecloses options that AMI will soon enable.
3. **A minimum bill may be a better instrument.** Athas introduces the minimum distribution bill ($9.61/month, matching the ACOSS customer-related cost) as an alternative to raising the customer charge. A minimum bill ensures every customer pays at least the customer-related cost, but — unlike a high fixed charge — it only binds on very low-use customers. Average and above-average users are unaffected and continue to face the full volumetric price signal. Athas develops six alternative rate designs (3 customer charge levels × with/without minimum bill) to map the tradeoff space.

Athas's key insight is that the tradeoffs among rate design principles are real and that there is no single "right" answer. He treats cost-of-service, gradualism, price signals, and low-income impact as genuine competing objectives — not as arguments to be won.

---

## Low-income rate design (Rate A-60)

### National Grid's proposal

Equalize A-60 and A-16 base distribution rates (same customer charge and energy charge), phase in the A-60 customer charge from $0 to $8.50 over 3 years, and replace the current base-rate discount with a 15% total-bill discount. The discount cost would be recovered through a Low Income Discount Recovery Factor (LDRF) applied as a uniform per-kWh surcharge on all other classes.

### Athas: transparent discounts are better, but protect low-use customers

Athas supports the structural change — equalizing rates and making the discount explicit — because it provides "better transparency to the discount, rather than conflating policy-related questions of low-income support with cost of service and revenue allocation." This aligns with Docket 4600 principles.

But he recommends that if a minimum bill mechanism is adopted, it should exempt A-60 customers. The revenue shortfall from this exception would be de minimis and could be collected through the LDRF.

### Rabago: oppose the customer charge for low-income entirely

Rabago opposes applying any customer charge to A-60, and opposes converting the discount to a 15% total-bill format. His reasoning:

- The regressive effects of a fixed charge are most severe for the lowest-use customers, who are disproportionately low-income. For a 150 kWh/month A-60 customer, the monthly charge would comprise nearly 25% of their bill after the discount — leaving very little room for EE investment to reduce their bill.
- A total-bill discount weakens the price signal for efficiency investment. The current base-rate discount preserves the full marginal incentive to reduce kWh; a percentage-of-total discount reduces it.

### Wiley Center: 15% is inadequate

The George Wiley Center doesn't engage with the rate design structure but argues on the adequacy of the discount. Based on direct experience working with "thousands of households facing the loss of their utility services," they state that 15% "is simply and wholly inadequate" and that the figure needs to be **≥ 35%** to "begin to alleviate the cost burden." They also advocate for tiered/income-sensitive rates tied to actual household income at the lowest tiers, citing evidence that such plans reduce terminations while increasing revenue collection.

---

## Time-varying rates

### LeBel: opt-in TOU rates immediately

LeBel is the only witness to push for immediate action. His reasoning:

1. **National Grid's opt-out TOU rollout won't happen until 2023.** That's a five-year gap with no time-varying rates available to any residential or small commercial customer.
2. **Opt-in TOU doesn't require AMI.** In National Grid's own New York territory, opt-in TOU is available using an upgrade to existing AMR meters. The incremental capital cost is modest.
3. **The waiting period wastes opportunities.** Five years without TOU means no meaningful customer load-shifting response, no experience base for RI customers, no market development for energy management technologies, and no lessons learned for the eventual opt-out rollout.
4. **Docket 4600 stakeholders recommended an opt-in transition period** before any opt-out requirement. Implementing opt-in TOU now fulfills that recommendation.

### Athas: defer to AMI

Athas agrees TOU is important and the Division is committed to it, but says the right vehicle is a future proceeding that jointly addresses AMI deployment and revenue-neutral time-varying rate design. Current meters can't support TOU for most customers.

### Rabago: supportive but not his focus

Rabago endorses the Docket 4600 direction toward time-varying rates and notes that "higher volumetric charges for on-peak usage can support demand response programs and energy storage deployment." But his testimony focuses on opposing the customer charge increase rather than designing the TOU alternative.

---

## The Docket 4600 rate design principles

The Commission's Order 22851 in Docket 4600 (July 2017) adopted rate design principles that all parties reference. The Order required any party proposing a rate design to address how it advances, detracts from, or is neutral to each principle. The principles are:

- Ensure safe, reliable, affordable, and environmentally responsible electricity service
- Promote economic efficiency over the short and long term
- Provide efficient price signals that reflect long-run marginal cost
- Address externalities not counted in current rate structures
- Empower consumers to manage their costs
- Enable fair opportunity for utility cost recovery and revenue stability
- Ensure fair compensation for value and services received and delivered
- Be transparent and understandable to all customers
- Implement with due consideration to gradualism
- Provide opportunities to reduce energy burden and address low-income needs
- Be consistent with policy goals (climate, innovation, least cost procurement)
- Encourage appropriate investments enabling the future energy system

Athas notes that National Grid's witness Gorman provided only "a high level and relatively perfunctory characterization" of how the proposal advances these principles, asserting it "does not detract from a single rate design principle" — a claim Athas disputes. In particular, the customer charge increase detracts from gradualism, consumer cost empowerment, and support for distributed generation.

---

## Relevance to Switchbox's work

Several arguments from this proceeding directly inform our rate design methodology:

- **Rabago's argument that volumetric rates are the best proxy for demand signals when customers lack demand meters** is the residential-class analog of what our BAT analysis measures. The BAT's volumetric allocator captures the cross-subsidy that arises when demand-related delivery costs are recovered per-kWh — the same mechanism Rabago defends for residential customers but that Tillman identifies as creating intra-class subsidies for large-demand customers. The difference is the customer's ability to respond to a demand signal independently of energy use.
- **The customer-related cost classification debate** (what belongs in the customer charge vs. volumetric rates) is directly relevant to how we model the fixed-charge component of delivery rates. The spread between Rabago's $5.90 and National Grid's $9.61 for the same class illustrates how cost classification assumptions drive rate design outcomes.
- **Athas's minimum bill concept** is worth understanding as an alternative to higher customer charges. A minimum bill preserves the full marginal volumetric incentive for average and above-average users while ensuring a cost-of-service floor for very low-use customers. This is a more surgical instrument than a flat customer charge increase.
- **The Rabago-Tillman split** on volumetric recovery illustrates that the right rate design depends on the customer class's metering capabilities and demand-response options. This maps to a key design choice in our work: whether to model HP-friendly rates as TOU-based (time-varying volumetric), demand-based, or some combination, and for which customer segments.
