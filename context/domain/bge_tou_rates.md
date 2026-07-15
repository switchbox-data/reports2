# BGE's Time-of-Use Rates, Explained

*Section to append to "Maryland DRIVE Act TOU Implementation: IOU Compliance, Opt-Out Authority, and the July 2026 Reports."*

BGE has four residential time-of-use offerings, created across four decades, and they overlap confusingly. This section explains what each one is, why BGE built it, what problem it was solving, and which ones still matter. It then answers the question of how BGE views TOU going forward.

Part 1 sets up the concepts. If you already know why TOU rates exist, skip to Part 2, which is where BGE's specific situation starts.

---

## Part 1: What TOU rates are trying to do

### The problem

The cost of serving an electricity customer is not constant across the hours of the year, but a conventional flat rate pretends it is.

Costs vary in two distinct ways:

**Energy and capacity costs vary hourly.** Wholesale power prices swing enormously — cheap at 3 a.m. when demand is low and efficient plants are running, expensive at 6 p.m. on a hot August weekday when the last, worst peaking units are dispatched. On top of that, PJM assigns each utility a capacity obligation based largely on its load during a handful of the highest-demand hours of the prior summer (the "5 coincident peaks," or 5CP). A kWh consumed during one of those hours is enormously more expensive to the system than a kWh consumed at 3 a.m., even though both are "one kilowatt-hour."

**Distribution costs are driven by peak, not by energy.** A transformer, a feeder, a substation — each is sized to handle the maximum load it will ever be asked to carry. If a feeder hits its limit at 6 p.m. in August, you upgrade the feeder. The fact that the same feeder is at 30% loading at 3 a.m. saves you nothing. Distribution investment responds to peak demand, not to total consumption.

A flat rate charges the same cents-per-kWh regardless. That has three consequences:

1. **No signal.** Customers have no financial reason to move flexible load (EV charging, water heating, laundry, pool pumps, pre-cooling) out of expensive hours.
2. **Cross-subsidy.** A customer whose usage is concentrated in peak hours costs more to serve than one whose usage is spread out, but both pay the same rate. The flat customer subsidizes the peaky one.
3. **More infrastructure than necessary.** Because nobody has a reason to flatten their load, the utility builds wires and buys capacity for a peak that is higher than it needed to be.

A time-of-use rate tries to fix all three by charging more during hours when incremental usage actually drives cost, and less during hours when it doesn't.

### The tension that explains everything else

Here is the thing to hold onto, because it drives nearly every decision in the BGE record:

**A TOU rate only produces benefits if two conditions are both met — the customer has to be enrolled, and the price difference has to be large enough to actually change their behavior. These two conditions pull against each other.**

A big gap between peak and off-peak prices is a strong signal but a frightening product. Customers look at a peak price three or four times the flat rate and decline to sign up. A small gap is an easy sell but changes nobody's behavior — and worse, it invites what economists call **free ridership**: customers whose usage already happens to be off-peak-heavy enroll, save money, change nothing, and the system gets no benefit while the utility loses revenue that other customers must make up.

Every utility offering an opt-in TOU rate is picking a point on this tradeoff. BGE's choices — and the fights about them — make sense only in this light.

### Three vocabulary items

**Opt-in vs. opt-out vs. default.** *Opt-in* means the customer must affirmatively choose the rate. *Opt-out* (also called *default*) means the customer is placed on the rate automatically and must act to leave. This distinction is the single biggest determinant of enrollment — research consistently finds opt-in TOU enrollment in the low tens of percent at best, while default TOU enrollment runs above 80%, because most people never change anything. Maryland's DRIVE Act requires opt-in TOU tariffs and only *permits* the Commission to require automatic enrollment in narrow circumstances. The July 1, 2026 reports are supposed to evaluate whether to go further.

**The ratio.** Shorthand for the on-peak price divided by the off-peak price. A "3.2:1 ratio" means peak electricity costs 3.2 times what off-peak electricity costs. In this docket the ratios are quoted on an **all-in basis** — supply plus delivery plus riders, i.e., what actually shows up on the bill. This matters because a strong ratio on one component can be diluted into a weak ratio overall once the flat components are added to both sides.

**Rate schedule vs. rider.** A *rate schedule* is the customer's base rate — you're on Schedule R, or Schedule RD, and so on; you can only be on one. A *rider* is an add-on that modifies or supplements a schedule. This distinction turns out to matter a great deal for BGE, because its most successful TOU product is a rider, not a schedule — and that's not an accident.

---

## Part 2: The one structural fact that makes BGE's stack legible

Maryland restructured its electricity market. That means BGE's bill has two separable halves:

- **Delivery (distribution).** The poles, wires, transformers, and meters. BGE is a regulated monopoly here. Every customer pays BGE for delivery, no exceptions.
- **Supply (generation and transmission).** The actual electricity. This is competitive — customers may buy from a third-party retail supplier. Customers who don't choose one get **Standard Offer Service (SOS)**, which is BGE's default supply, procured through periodic auctions. SOS prices reset on a schedule, with the SOS year beginning June 1.

**This means a "TOU rate" in Maryland can time-vary the supply half, the delivery half, or both — and these are genuinely different products.**

- A rate that time-varies **supply only** signals wholesale energy and capacity costs. It tells the customer something about PJM. It says nothing about BGE's wires.
- A rate that time-varies **delivery** signals distribution costs. This is the piece that connects to feeder loading, transformer sizing, and capital deferral.

Here is BGE's entire residential stack, organized by that distinction plus one other — whether the rate exposes the customer's whole house or just their EV charger:

| | Whole house | EV charger only |
|---|---|---|
| **Supply TOU only** *(delivery is flat)* | **Schedule RL** (1984)<br>**Schedule EV** (2013) | **Rider 6 / VC-TOU** (2020) |
| **Supply *and* delivery TOU** | **Schedule RD** (2019) | — |

**Only Schedule RD time-varies the distribution charge.** RL, EV, and Rider 6 all sit on top of a flat delivery rate. Rider 6 says so explicitly in its tariff: all metered usage is billed Schedule R distribution rates regardless.

Keep that in mind. It is the reason BGE's distribution-deferral arguments live in its virtual power plant filings and not in its TOU filings, which is the crux of the answer to your last question.

There is also a fifth instrument that nobody calls a TOU rate but which belongs in this discussion: **Rider 26 – Peak Time Rebate**, which applies to every residential schedule and is the one time-varying program BGE already runs on a default basis. More on that below.

---

## Part 3: The four rates

For each: what problem it was built to solve, how it works, how it's actually doing, and where it stands.

### Schedule RL — Residential Optional Time-of-Use (1984)

**The problem it was solving.** In 1984 BGE was a vertically integrated utility that built its own power plants. Central air conditioning was spreading rapidly through its territory, summer afternoon peaks were climbing, and meeting those peaks meant building generation that would sit idle most of the year. A TOU rate was a demand-side alternative: convince some customers to run their AC less, or their laundry later, and you defer a peaker.

The metering technology of the era constrained the design. These were mechanical multi-register meters that could count kWh into a few coarse time blocks and nothing finer. So the rate got a very broad peak window.

**How it works today.**

- Customer charge: $12.00/month
- **Delivery Service Charge: a single flat $0.04830/kWh** (Rate Year 3, effective January 1, 2026). No time variation whatsoever.
- All of RL's time-of-use character lives in the SOS supply rates under Rider 1.

Three rating periods (Suppl. 745, filed 04/30/2026, effective 05/01/2026):

| Season | Peak | Intermediate | Off-peak |
|---|---|---|---|
| Summer | 10 a.m.–8 p.m. weekdays | 7–10 a.m., 8–11 p.m. | everything else |
| Non-summer | 7–11 a.m., 5–9 p.m. weekdays | 11 a.m.–5 p.m. | everything else |

Weekends and listed national holidays are entirely off-peak. Non-summer periods shift one hour during the daylight-saving transition windows.

A **ten-hour summer peak** is the giveaway that this is a 1984 design. Modern rates target a narrow window because that's where the cost actually is; a 10 a.m.–8 p.m. block treats noon and 6 p.m. as equally expensive, which they are not.

**Eligibility** carries a curious legacy: the tariff offers it "for all residential purposes for single family buildings having electric central air conditioning or electric central heating, or where otherwise requested and approved by the Company." BGE's customer segmentation even splits it in two — **RL** is "Residential Time-of-Use (non-electric heat)," tariff code 44; **RLH** is "Residential Time-of-Use (electric heat)," code 45. (Flagging this now because it's relevant to your heat pump work — see Part 6.)

**How it's doing: badly, and BGE says so.** Over 50,000 customers were enrolled as of July 2025 — by far BGE's largest TOU population. But BGE told the Commission there has been **"little to no difference" in usage patterns of RL customers compared to customers on the flat Schedule R.** Fifty thousand customers, no measurable behavior change.

The reason is arithmetic. September 2025 SOS supply rates were 22.388¢ on-peak, 13.357¢ intermediate, 12.750¢ off-peak — a 1.76:1 supply ratio. But then you add the flat 4.83¢ delivery charge to *both* sides, and the all-in ratio collapses to roughly 1.5:1. BGE cited **1.3:1** on May 2025 rates. A 30% peak premium is simply not enough money to make anyone reschedule their life.

OPC saw the same numbers and drew the optimistic conclusion: this large customer base is an **"untapped"** resource, and a stronger price signal could produce substantial peak reductions at relatively low cost. You already have 50,000 people on a TOU rate; you just have to make the rate mean something.

**What DRIVE changed.** BGE is applying Schedule EV's rate-shaping to RL, moving the all-in ratio from **1.3:1 to 1.9:1**, while keeping the intermediate period to soften the impact on existing customers. Because RL's time variation lives entirely in SOS supply, BGE implements this through an SOS filing rather than a standalone rate case — which is why it lands as a Rider 1 revision timed to the June 1 SOS year rather than as its own proceeding.

**Status: live, and it is where the volume is.** If BGE's TOU program produces measurable peak reduction, the most likely source is 50,000 RL customers finally facing a signal worth responding to.

*One structural implication worth noting: because RL's time variation is entirely on the supply side, an RL customer who buys supply from a third-party retailer would face a flat delivery charge and their supplier's pricing — meaning the rate does nothing at all for them. This follows logically from the tariff structure rather than from an explicit statement in the record.*

### Schedule RD — Residential Delivery and Energy Time-of-Use (2019)

**The problem it was solving — and this is the most important "why" in the section.**

Three things converged in the late 2010s:

1. **BGE finished deploying smart meters (AMI).** For the first time, BGE could measure and bill every residential customer's consumption on an hourly basis. RL's coarse blocks were a technology constraint that no longer existed.
2. **The Commission opened PC 44**, its grid-modernization proceeding ("Transforming Maryland's Electric Distribution Systems"). One of its work groups — the Rate Design Work Group — was tasked specifically with designing full-scale TOU offerings for Maryland. Its 2022 report is cited in Order No. 91917 as the origin of the ratio methodology now in use.
3. **BGE's existing TOU rates were supply-only and weak.** RL demonstrably did nothing. Schedule EV was tiny. Neither said anything about distribution costs.

**Schedule RD is the answer to the question "what would a real TOU rate look like if we designed one from scratch, with modern meters, to reflect what actually drives cost?"** It is the only BGE residential rate that time-varies the delivery charge — meaning it is the only one that tells a customer anything about the cost of the wires serving them.

**How it works.**

- Customer charge: $10.00/month (RY3, effective January 1, 2026)
- **Delivery Service Charge: on-peak $0.11550/kWh, off-peak $0.02987/kWh** — a 3.87:1 ratio *in delivery alone*
- Layered on TOU supply: 36.778¢ on-peak vs. 10.575¢ off-peak (September 2025)
- All-in: roughly 48¢ against 14¢

Two periods, no intermediate:

| Season | On-peak | Off-peak |
|---|---|---|
| Summer | 3–8 p.m. weekdays | everything else |
| Non-summer | 6–9 a.m., 5–9 p.m. weekdays | everything else |

These windows are the modern design, and each is chosen for a reason. **The summer 3–8 p.m. window** is five hours targeting when PJM's system peak and BGE's distribution loading actually occur — air conditioning at maximum, people arriving home, solar output declining. **The winter 6–9 a.m. and 5–9 p.m. windows** reflect the two-humped shape of winter residential load: the morning wake-up (heat, hot water, showers, cooking) and the evening return.

**Eligibility:** any residential customer on request, provided they have a smart meter capable of measuring hourly time-of-use data. Worth knowing that RD used to exclude solar customers — the earlier tariff (Suppl. 709) said the schedule was "not available to Rider 18 Net Energy Metering customers starting October 1, 2022," grandfathering anyone already on both. That exclusion has since been removed; the current sheet lists Rider 18 among applicable riders.

**How it's doing: 1,200 customers.** Out of roughly 1.25 million residential accounts. That is the tension from Part 1 in its purest form — BGE built the technically correct rate, and almost nobody wants it.

BGE surveyed customers to find out why, and the answer was exactly what you'd predict: **the peak rate itself was the barrier.** At 3.2:1 all-in, the rate reads as risky. So BGE's DRIVE Act proposal was to *weaken* its best rate — **3.2:1 down to 2.8:1** — in order to sell more of it. Revised tariff filed 04/16/2026 (ML 329078), accepted 05/20/2026 (ML 330315).

**The fight this caused is worth understanding**, because it inverts the usual assumption that regulators push utilities toward stronger signals while utilities resist.

SEIA, Advanced Energy United, and the Chesapeake Solar and Storage Association jointly objected. Their argument: keep the ratios high, because a lower ratio worsens free ridership — customers who can save money without changing anything have an incentive to enroll, and with a lower ratio, the ones who do enroll have less reason to actually shift consumption. You end up paying out savings and buying nothing.

The Commission sided with BGE, and — in the parallel discussion of Pepco's and Delmarva's rates — offered an affirmative cost-causation defense of the weaker signal that's worth quoting because it's a substantive rate-design position, not a concession: moderating the differential "will serve to reallocate a significant portion of transmission and capacity costs across all hours, not just peak hours," which "will better align the companies' R-TOU-P rates with cost causation principles as costs will be allocated in a manner that reflects the typical residential load factor."

The argument being made there is that an extremely high peak ratio *over*-assigns capacity and transmission costs to a handful of hours relative to how residential load actually causes those costs. Whether you buy that or not, it's a real position and not merely a rationalization of the enrollment problem.

**Status: live; BGE's flagship, and the only rate that matters for distribution cost causation.**

### Schedule EV — Residential Electric Vehicle Time-of-Use (2013)

**The problem it was solving.** EVs arrived around 2011. A single EV adds roughly 2–4 MWh per year to a home — comparable to adding a second air conditioner. Worse, the default charging behavior is the worst possible one: plug in on arriving home at 6 p.m., which lands the entire load directly on the system peak. Utilities urgently wanted EV charging pushed to overnight hours.

There were two ways to price EV charging differently from the rest of the house:

1. **Install a second meter** dedicated to the charger. Accurate, but expensive — a second service, a second meter, an electrician, and a second monthly customer charge.
2. **Put the whole house on a TOU rate** and hope the customer, knowing the EV is their biggest flexible load, shifts it.

BGE chose option 2. Schedule EV is a whole-house TOU rate gated on EV ownership.

**How it works.** Customer charge $9.00; **delivery is a flat $0.04239/kWh** (Rate Year 3, effective January 1, 2023 — the number is stale, which itself tells you how much attention this rate gets). TOU only in supply: 27.835¢ on-peak vs. 10.441¢ off-peak (September 2025), a 2.67:1 supply ratio. Periods mirror RL's peak windows but drop the intermediate — summer 10 a.m.–8 p.m., non-summer 7–11 a.m. and 5–9 p.m.

**Eligibility:** BGE Standard Offer Service residential customers who purchase or lease a plug-in EV and charge it through a BGE connection, at their primary residence, "on a single time-of-use meter that is also used to measure consumption at the primary residence (whole house) level," requiring a smart meter.

**How it's doing: 190 customers.** It failed, and it failed for two identifiable reasons.

*First, the trade is bad.* To influence one appliance, the customer must put their refrigerator, air conditioning, dryer, and everything else onto a TOU rate. That's a lot of downside risk to accept in exchange for cheaper overnight charging. Most EV owners decline.

*Second, and more damning: it excluded exactly the population it needed.* Look at Schedule EV's rider list and notice what isn't there — **Rider 18, Net Energy Metering, does not appear.** Solar customers cannot take the rate. But EV owners and rooftop solar owners are heavily overlapping populations. BGE said so directly in its EVsmart 2.0 filing: the main reason for un-enrollments from its EV rates has been customers installing solar panels. Customers were signing up, going solar, and being kicked off.

**Status: dying — but its ghost persists, which is genuinely useful to know.**

BGE proposed in Case No. 9478 (EV Phase II) to close Schedule EV to new enrollment while grandfathering the existing 190. Order No. 91917 pointedly declined to rule on it: "the Commission does not reach any decision in this docket with regard to modifying the Utilities' existing EV TOU rates. Those proposals were also filed in Case No. 9478, and the Commission will address them in that docket."

But Schedule EV doesn't actually disappear even if closed, because **it is the pricing reference for Rider 6.** BGE's SOS rate sheet states it plainly: "For customers participating in Rider 6 – Vehicle Charging TOU (VC-TOU) Adjustment Program, the VC-TOU On-Peak and Off-Peak Total SOS Rates are equal to the Schedule EV On-Peak and Off-Peak Total SOS Rates, respectively." Rider 6 needs a TOU price shape to compute against, and Schedule EV's is the one it uses. Schedule EV's shape is also the template BGE is applying to RL.

So Schedule EV is becoming a rate-design artifact rather than a rate — closed to customers, but still the pricing engine underneath BGE's fastest-growing offering *and* its largest legacy one. If you're modeling BGE's rates, you can't discard it.

### Rider 6 — Vehicle Charging Time-of-Use Adjustment (2020), marketed as EVsmart® EV-TOU

**The problem it was solving: everything that was wrong with Schedule EV.**

By 2020 the technology had changed. Networked Level 2 chargers and manufacturer telematics APIs could report EV-only consumption with timestamps, straight from the charger or the car. That meant you could finally price *just the EV* — without a second meter, and without touching the rest of the house.

**How it works — and the mechanism is the whole point.** Rider 6 is not a rate schedule. It's a **billing adjustment**. The customer stays on flat Schedule R. The charger or the vehicle reports EV kWh by time period. BGE then computes what those kWh would have cost at Schedule EV's TOU supply rates versus what they cost at Schedule R's flat supply rate, and applies the difference as a line item:

```
Adjustment = (EV On-Peak SOS − R SOS) × EV on-peak kWh
           + (EV Off-Peak SOS − R SOS) × EV off-peak kWh
```

Charge off-peak and the adjustment is a credit. Charge on-peak and it's a charge. Everything else in the house is untouched — and per the tariff, **all metered usage is billed Schedule R distribution rates and applicable riders** regardless.

**Eligibility** is the most demanding of any BGE TOU offering, because the mechanism depends on a data pipeline:

- Enrolled as a Schedule R customer buying supply from BGE (no third-party supplier)
- Working WiFi at the charging premise
- A qualified Level 2 charger behind the meter, or an eligible vehicle with manufacturer telematics enabled
- Agreement to share charging data with BGE and its designated vendor (WeaveGrid)
- Not participating in another BGE pilot such as Rider 32 – Community Energy
- No third-party vendors managing the utility account electronically
- MyAccount enrollment
- **Two** separate applications — one on bge.com, one at the vendor's site — both approved before enrollment takes effect
- Not eligible if already on any TOU rate (Schedule EV, RD, or RL)

There's a sensible backstop for the data dependency: if charger data is delayed, the premise is billed Schedule R supply and the adjustment appears on the next bill — as long as the delay is under 60 days. Past 60 days, BGE cannot provide the credit.

**How it's doing: 3,700 customers as of July 2025**, up from 1,862 in mid-2024, with BGE reporting month-over-month enrollment growth since its May 2020 launch and minimal un-enrollment. Compare Schedule EV's 190. Same underlying price signal, roughly 20x the uptake, because the two objections are gone: no second meter, no whole-house risk.

**And BGE keeps removing barriers**, which is the clearest evidence of where its priorities are. The single constraint that killed Schedule EV — the solar exclusion — was lifted for Rider 6: "Are you a Budget Billing or Net Metering Customer? Starting December 13, 2024 you are now eligible to enroll in EV TOU." That change came through Suppl. 727, filed 12/06/2024, effective 01/22/2025.

**And BGE actively markets it**, which it does not do for anything else in the stack. There's a brand (EVsmart®), a vendor partnership, an advertised savings figure — "$120 or more per year," resting on 27 kWh/100 miles efficiency and a 3¢/kWh saving, with an honest warning that on-peak charging while enrolled may cost more than staying on Schedule R. Bundled with Smart Charge Management, BGE advertises up to $240 annually, and WeaveGrid's platform builds automated charge schedules around the customer's stated departure time, desired state of charge, rates, and grid needs, with manual override.

**Status: live, growing, actively promoted, and retained in BGE's Case 9478 proposal.**

**What it does not do:** no distribution TOU at all. It is a pure supply-side product by design. It will move EV charging off the PJM peak. It contributes nothing to distribution cost causation, and cannot be counted on for a feeder deferral.

### Rider 26 — Peak Time Rebate (the default that nobody calls TOU)

Applies to Schedules R, RL, RD, and EV alike — it shows up in every residential rider list — and is billed to residential customers at $0.00013/kWh.

**A peak time rebate is time-varying pricing with the downside removed.** BGE declares a peak event, and customers who use less than their calculated baseline during that event get paid for the difference. Use more, and nothing happens. There's no penalty, only upside.

This matters more than its obscurity suggests, for one reason: **it is enrolled on a default basis, and BGE has run it for over a decade.** As Brattle analysts noted when it launched, "the first residential default dynamic pricing deployments have just begun in Maryland and Delaware, where BGE and PHI are enrolling all of their residential customers in peak time rebates."

So when the July 2026 reports take up opt-out TOU, the question is not *whether BGE is capable of, or philosophically opposed to, defaulting customers into time-varying pricing.* It has been doing exactly that since the early 2010s. The question is narrower and sharper: **will BGE default customers into a rate that can make their bill go up?** PTR never could. That asymmetry is the entire distinction, and it's the one BGE has spent fifteen years on the comfortable side of.

---

## Part 4: The enrollment reality check

| Offering | Created | What's exposed | Delivery TOU? | Enrolled | Status |
|---|---|---|---|---|---|
| Schedule RL | 1984 | Whole house, 3 periods | No | >50,000 | Live; re-shaped 1.3:1 → 1.9:1 |
| Rider 6 (VC-TOU) | 2020 | EV charger only, 2 periods | No | 3,700 | Live; growing; actively marketed |
| Schedule RD | 2019 | Whole house, 2 periods | **Yes** | 1,200 | Live; re-shaped 3.2:1 → 2.8:1 |
| Schedule EV | 2013 | Whole house, 2 periods | No | 190 | Closure proposed in Case 9478 |

BGE told the Commission its marketing "targets a total of 11 percent of residential customers enrolled in a TOU rate by 2028 (compared to today's 5 percent enrollment)," with a specific target of **3,200 additional customers** in Schedule RD or RL by January 1, 2028.

**Two things about that "5 percent" are worth pausing on.**

First, roughly 91% of it is the 1984 RL population — sitting on a rate BGE itself says produces no measurable behavior change. So the existing enrollment base, impressive-sounding, is mostly inert. It is also probably invisible to the customers on it: BGE and Staff made precisely this argument about Pepco's identical-vintage Schedule R-TM, warning that "a significant portion of Schedule R-TM customers may be unaware that they are on a TOU rate." There's no reason to think RL is different.

Second, the arithmetic doesn't close where you'd expect. On roughly 1.25 million residential accounts, going from 5% to 11% means roughly **75,000 net new TOU customers**. But only 3,200 of those come from the RD/RL marketing effort BGE budgeted for. The remaining ~72,000 have to come from what BGE calls "its existing EV TOU target" — i.e., Rider 6.

If that reading is right, **BGE's TOU strategy is, in substance, an EV strategy**, and the whole-house rates are a side program. *(This decomposition is my inference from BGE's stated figures, not something BGE published — worth verifying against the July 1, 2025 filing at 34–35.)*

---

## Part 5: How BGE views TOU going forward

You asked three questions: is BGE just checking a box, is it promoting TOU, and does it see deferred distribution capacity savings? The record supports fairly clear answers to all three.

### Is BGE just checking a box?

**On the whole-house rates: close to it — and the Commission rewarded the restraint.**

BGE proposed a total budget of **$369,000 over two years** for 3,200 incremental customers. The Commission's approval reasoning is the tell: "the company's estimated budget of $369,000 in incremental costs is moderate. Further, as Staff points out, these costs are related only to marketing and education; **BGE does not have system programming costs** associated with implementing these TOU offerings."

That's the crux. BGE had to build nothing. It already had RD, RL, EV, and Rider 6, and AMI was already deployed. Its DRIVE Act compliance consisted of adjusting numbers in rates that already existed and then advertising them. Compare PHI, which proposed over **$2.8 million across three years** at roughly $305 per new Delmarva customer against BGE's $115 — and got sent back with a 45-day homework assignment demanding a cost-benefit analysis and a detailed marketing plan.

To be fair, the outreach isn't nothing: Staff supported BGE's plan to **directly contact 800,000 residential customers**. That's a real campaign. But it's a campaign for products BGE already had, funded at a level nobody thought worth arguing about.

### Is BGE promoting TOU?

**Yes — enthusiastically, and specifically where the customer's exposure is ring-fenced to one device.**

The contrast within BGE's own portfolio makes the pattern unmistakable. Rider 6 has a brand, a vendor partnership, an advertised dollar savings figure, a two-step enrollment funnel, an automated-charging companion program, and eligibility that BGE keeps widening. Schedule EV — the whole-house version of the identical price signal — is being closed. Schedule RD, the technically superior rate, gets a share of a $369K education budget.

The generalization: **BGE markets time-varying pricing hard when the customer's downside is limited to a single controllable appliance, and softly when the whole house is on the line.** That is a rational read of customer psychology, and it's also the path of least resistance.

### Where has BGE landed on how strong the signal should be?

Somewhere in the **1.9:1 to 2.8:1 band** — and revealingly, it arrived there from both directions at once. It asked to *lower* RD from 3.2:1 to 2.8:1 because the peak rate deterred enrollment. It asked to *raise* RL from 1.3:1 to 1.9:1 because that ratio "is not a sufficient price signal to incent customers to shift their behavior." The Commission described 1.9:1 as a "middle ground" for customers who find RD's peak rates too high.

Read generously, BGE is triangulating toward an optimum between enrollment and effect — which is a legitimate thing to do and arguably what the tension in Part 1 demands. Read skeptically, BGE is optimizing for the thing it will actually be measured against on January 1, 2028, which is an **enrollment target — a headcount, not a megawatt.** Nothing in the DRIVE Act's TOU provisions holds BGE accountable for load actually shifting.

### Does BGE see deferred distribution capacity savings?

**Yes — and this is the most revealing part of the record. But it sees them in its virtual power plant program, not in its TOU rates. And it has attached a condition.**

*First, the condition.* Per OPC's characterization of BGE's PC 77 filing (ML 328165 at 17): "BGE has proposed that if demand response or other EDSSS resources are used to defer or avoid distribution system upgrades, those resources should receive **the same favorable cost recovery treatment that traditional capital infrastructure would have received.**" Alongside that, BGE asked to recover its VPP costs through a **regulatory asset earning a return at its weighted average cost of capital** until fully recovered.

Brief translation, since these are ratemaking terms of art: a *regulatory asset* lets the utility put spending on its balance sheet and recover it from customers later, earning a return in the meantime. *WACC* is the blended debt-and-equity return — substantially higher than the cost of debt alone. So BGE is asking to earn on avoided infrastructure roughly what it would have earned on built infrastructure.

OPC's rebuttal is the classic non-wires-alternative argument, and it lands cleanly: "A non-wires alternative is supposed to reduce customer costs by avoiding unnecessary infrastructure spending. **It should not preserve the same earnings opportunity the utility would have received if the avoided capital project had been built anyway.** If the lower-cost alternative is treated as though it were the higher-cost investment it replaces, much of the value of the substitution is lost." OPC also distinguishes the risk profiles: physical infrastructure carries construction, operational, and multi-decade maintenance obligations, whereas aggregator fees and customer incentives "are largely programmatic. They compensate participation or services, rather than finance utility-owned infrastructure."

So the honest summary is: **BGE affirmatively asserts that demand-side resources can defer distribution capex — and conditions its enthusiasm on being made whole for the earnings it would lose by not building.** That's not hypocrisy; it's the throughput and capex-return incentive doing exactly what the regulatory structure asks it to do. But it means you should read BGE's deferral analysis knowing what BGE wants out of it.

*Second, and more important for your purposes: the deferral numbers live in the VPP filings, not the TOU filings.*

BGE's EDSSS (virtual power plant) pilot came with quantification: **$1,545,955 in cost against an estimated 7.621 MW peak reduction**, which BGE explicitly framed as demonstrating "a return on investment in terms of grid capacity management," with stated goals including support for "customer affordability by potentially deferring costly infrastructure upgrades, improving load forecasting accuracy, and providing direct compensation to participating customers." When the Commission rejected that pilot as insufficiently ambitious and ordered a refiling, BGE came back with **up to 188 MW** of flexible load.

BGE has published **no comparable MW or dollar deferral estimate for its TOU rates.** Not a small one — none.

**That asymmetry is the answer to your question, and it isn't an oversight.** Deferring a distribution upgrade requires three things: load reduction that is *firm* (you can count on it), *locational* (on the specific constrained feeder), and *dispatchable* (available on the specific day the constraint binds). An opt-in TOU rate delivers none of the three. It is a voluntary, diffuse, system-wide price nudge with no performance obligation. A VPP delivers all three — contracted MW, at known locations, callable on command.

The Commission is alive to this. It agreed with stakeholders who "criticized certain electric company EDSSS proposals for focusing on system peak reduction and neglecting local peak reduction," and directed the utilities to develop strategies for identifying local needs and locational marketing targeting.

BGE's implicit theory of the case, then, is that **TOU is a customer-choice affordability product and the VPP is the grid asset.** That's coherent — arguably correct — but it sits awkwardly against a statute that asks BGE to evaluate deferral potential *from TOU rates* specifically.

This is also why the shape of BGE's July 1, 2026 filing is interesting: it filed both as a party to the joint Exelon "Deferring Distribution System Upgrades Report" (ML 331710) **and separately** its own "Drive Act Capital Deferral Potential July 1 Report" (ML 331727). A separate company-specific capital-deferral document implies BGE did quantification it didn't want blended into a three-utility joint filing.

### The move that actually matters financially

It isn't TOU at all. BGE's PC 77 filing proposes **moving its existing EmPOWER load-management programs into the DRIVE pilot beginning in 2027** — specifically Rider 15 (Demand Response Service) and Rider 26 (Peak Time Rebate).

Why this matters: House Bill 864 (2024) restricted EmPOWER cost recovery, directing that new EmPOWER costs be recovered in the year incurred and capping carrying costs on unamortized balances at the utility's average cost of outstanding debt. BGE's DRIVE proposal, by contrast, seeks a regulatory asset earning WACC. **Same programs, same customers, same devices — materially better cost recovery, achieved by changing which statute they sit under.** OPC's characterization is that a pilot built substantially on migrated EmPOWER demand response "would largely relabel existing activity" and would "reveal much less about whether DRIVE is actually working as intended."

If BGE prevails, its entire residential demand-side portfolio — including the default PTR program that is arguably its most successful time-varying instrument — migrates into a framework with equity-like returns. **That dwarfs the $369K TOU budget by three orders of magnitude**, and it's the right lens for reading BGE's DRIVE Act posture as a whole. The TOU proceeding is where BGE spends the least and gets watched the most; the EmPOWER migration is where the money is.

### So where will BGE land on opt-out?

Its actual position lives in ML 331727, which I couldn't retrieve. The structural read points negative-to-conditional:

- BGE just finished arguing that customers won't opt in at 3.2:1 because the peak price frightens them. That's an odd predicate for then defaulting non-consenting customers into those same prices.
- The DRIVE Act's own findings flag protecting low- and moderate-income households "from negative bill impacts during a transition to TOU rates" — a caution BGE can point to.
- Pepco's revenue-erosion argument about Schedule R-TM shows the Exelon utilities are alert to a specific mechanical problem: revenue targets are set per rate class, so customers migrating between classes changes authorized revenue. A wholesale opt-out transition would trigger that at maximum scale.
- BGE's default instrument of choice has always been the no-downside PTR — which it now proposes to move *into DRIVE* rather than convert into a TOU default.

If BGE endorses opt-out, expect the endorsement to arrive conditioned on cost-recovery and revenue-target treatment.

---

## Part 6: Two things relevant to your heat pump work

**1. BGE has operated an electric-heat-differentiated TOU schedule since 1984, and nobody seems to be looking at it.**

The RL/RLH split (tariff codes 44 and 45) means BGE has maintained separate TOU treatment for electric-heating and non-electric-heating customers for forty years, with an availability clause explicitly conditioned on electric central air conditioning *or electric central heating*. That is, functionally, a latent heat pump rate class sitting inside a legacy tariff.

It's relevant to your New England campaign for two reasons. It's a precedent — a major IOU already runs a heating-differentiated TOU schedule at scale, which is useful when a utility elsewhere claims the concept is novel or administratively infeasible. And it's a live gap: BGE is about to re-shape RL's price signal from 1.3:1 to 1.9:1, and nothing in the record indicates any heating-specific analysis behind that. Whether the re-shaping was tested separately for RLH customers — who have a fundamentally different load shape from RL customers — is a clean data request.

**2. Schedule RD's delivery charges appear not to be seasonally differentiated — only the period definitions change.**

The tariff shows a single on-peak delivery rate ($0.11550) and a single off-peak rate ($0.02987), while separately defining summer on-peak as 3–8 p.m. and non-summer on-peak as 6–9 a.m. and 5–9 p.m. So the *hours* change by season but the *prices* don't.

The consequence for a heat pump customer: they face the same 11.55¢ on-peak delivery charge at 7 a.m. in January as at 4 p.m. in August — on a system that peaks in summer. That's a defensible administrative simplification, but it isn't cost causation. A winter morning kWh on a summer-peaking distribution system does not drive distribution capacity cost the way an August afternoon kWh does.

This matters directly if BGE's July 1 report leans on RD as evidence that TOU rates can defer distribution investment. It's also the exact structural question at issue in your Rhode Island MCOSS work — whether winter heat pump load actually causes incremental distribution capacity cost — and BGE's rate design implicitly assumes an answer without doing the analysis. *(Verify against the post-May-2026 tariff sheet; the version I retrieved is Suppl. 723, and ML 329078/330315 revised it.)*

---

## Part 7: What to look for when you get the reports

- **Whether ML 331727 quantifies deferral in MW or dollars at the feeder level, or only qualitatively** — and whether it separates TOU deferral from VPP deferral. My expectation is that it either folds TOU into the VPP number or concedes that TOU can't be relied on for deferral because it isn't dispatchable. Either would be a useful admission.
- **Whether BGE conditions any opt-out endorsement on cost-recovery treatment.** Given the pattern above, expect the endorsement to come with an invoice.
- **Whether there's any EM&V baseline for the RL re-shaping.** There isn't one today. Potomac Edison was directed to build evaluation, measurement, and verification metrics with the Rate Design Work Group because it had no existing residential TOU rate — but BGE's RL has been running since 1984 with, on BGE's own account, no measurable effect ever detected. Re-shaping it to 1.9:1 without an EM&V design means nobody will be able to say whether it worked.
- **The common metrics prescribed by Orders 92158 (ML 326582) and 92422 (ML 330633)**, which constrain what these reports could say in the first place.
- **BGE's non-residential SOS TOU analysis**, due to the Rate Design Work Group within six months of Order No. 91917 (so roughly April 2026), covering supply ratios, use of intermediate periods, and peak periods. The Commission opened this door deliberately, noting the DRIVE Act "does not specifically limit TOU rate participation to residential customers."

---

## Caveats

- **Rate levels are point-in-time and several are stale.** The SOS supply figures are a September 2025 snapshot and predate the DRIVE modifications; RD's delivery rates are from Suppl. 723 (filed 08/29/2024) and were revised by ML 329078 (accepted 05/20/2026); Schedule EV's delivery rate is Rate Year 3 effective January 1, 2023. The post-June-2026 SOS rate sheet and the current RD tariff page were not retrievable — BGE's CDN serves versioned asset URLs and the tariff index page is JavaScript-rendered. Pull live sheets from bge.com → My Account → Rates & Tariffs → Electric Service before citing any number.
- **The ratio figures BGE cited (3.2:1, 1.3:1, 2.8:1, 1.9:1) are BGE's own, based on May 2025 rates**, and are all-in. My recomputations from the September 2025 SOS sheet come out somewhat higher, which is expected given seasonal SOS variation — don't treat the two as reconcilable without the underlying workpapers.
- **RL's open/closed status has a documentary conflict.** The tariff sheet has no closed-to-new-customers language (unlike Rider 7, which says so explicitly), Order No. 91917 treats RL as an active marketing target, and one BGE supplier document states that "customers choose from Schedule R or Schedule RL when applying for service" — while a version of that same segmentation document annotates codes 44 and 45 as "(closed)". Weight of evidence says open; worth a data request if it matters.
- **BGE's positions in ML 328165 (PC 77 inventory) are quoted as characterized by OPC**, not from the filing itself, which I couldn't retrieve. OPC gives pin cites (at 15–17); confirm against the original before relying on the WACC/deferral characterization in testimony.
- **The 5%→11% decomposition is my inference**, derived from BGE's stated targets and an approximate residential customer count. BGE did not publish it.
- **Case No. 9478's disposition of Schedule EV is unconfirmed.** Order No. 91917 deferred it; I found no subsequent 9478 order resolving whether Schedule EV is now closed. It remains in BGE's published tariff. Check the 9478 docket directly.
- **The observation about third-party-supply customers on Schedule RL is a logical inference** from the tariff structure (flat delivery + supply-side-only TOU), not a statement found in the record.

---

## Primary sources

| Source | Locator |
|---|---|
| Order No. 91917 (DRIVE Act Implementation, Oct. 21, 2025) | psc.maryland.gov/wp-content/uploads/Order-91917_ML-323522-9761-1.pdf |
| Case No. 9761 docket jacket | webpscxb.pscmaryland.com/DMS/case/9761 |
| BGE Schedule RD tariff (Suppl. 723) | bge.com CDN — `P3_SCH_RD.pdf` |
| BGE Schedule RL tariff (Suppl. 717/745) | contentstack — `P3_SCH_RL.pdf` |
| BGE Schedule EV tariff (Suppl. 659/674) | contentstack — `ScheduleEV.pdf` |
| BGE Riders 6/7/8 (Suppl. 727) | contentstack — `Rdrs_6_7_8.pdf` |
| BGE SOS rates & misc. charges (Sept. 2025) | bge.com CDN — `POLR_Rates_PTC_MiscCharges.pdf` |
| OPC Comments, Case 9761 & PC 77 (Apr. 1, 2026) | opc.maryland.gov/Portals/0/Files/Publications/Others/ |
| BGE EVsmart 2.0 / EV Phase II (Case 9478) | e9insight.com/wp-content/uploads/2024/06/7-CN9478_BGE-EVsmart2.0-_F-3.pdf |
| BGE EVsmart EV-TOU program page | bge.com/SmartEnergy/InnovationTechnology/Pages/EVTOURate.aspx |
| DLS Fiscal & Policy Note, HB 1256 (2024RS) | mgaleg.maryland.gov/2024RS/fnotes/bil_0006/hb1256.pdf |
