# RIE objections to seasonal HP rates: interpretation and responses

This document catalogs the objections and questions Rhode Island Energy raised during the September 2024 call about seasonal heat pump rates, interprets the underlying concerns driving each, and outlines how our RI-specific research answers them. Written to help prepare expert testimony.

Context: at the time of the call, we only had Massachusetts results to show. RIE's team included Carrie Gill (electric regulatory strategy), Lance Schaefer and Peter Blazuna (Concentric Energy Advisors, rate design and CCOS), Stephanie Briggs (rates and revenue requirements), Tim Jones and Jared Long (sales analysis/forecasting), Adam Ramos and Jennifer Brooks Hutchinson (outside counsel), and several others. Their pushback was substantive and well-coordinated — it came from rate design consultants, planners, and regulatory strategists.

## 1. "You haven't demonstrated cost causation" -> now we have, via a method that does the same thing as yours, assign subclass cost responsibility based on historical cost-causation, but is not broken because it looks at time

### What they said

Lance (Concentric) pressed hard on this. He challenged the use of ISO-NE seasonal peak ratios as a proxy for distribution cost causation, noting that distribution planning uses non-coincident peaks (NCP), not coincident peaks:

> "Generally when we look at the distribution system, we're looking at more localized peaks, which is why we use a non coincident peak instead of a coincident peak. If that ratio were wholly explicative of the distribution system, we would probably use coincident peak when we're doing class cost of service studies, right?"

He also pushed on whether winter usage truly imposes zero marginal O&M and depreciation costs:

> "I'm curious to know if you think that there are no marginal O&M or depreciation costs associated with winter usage."

And he got JP to concede the point: "maybe more cost analysis would be necessary."

### Where they were coming from

This was the most technically precise objection. Lance is a CCOS analyst — his job is to allocate costs to customer classes using well-established methods. He was saying: you showed us a revenue analysis and waved at ISO-NE peak ratios, but that's not the same as measuring what these customers actually cost to serve. The ISO-NE coincident peak drives generation and transmission costs, but distribution costs are driven by local feeder and transformer peaks — which may not follow the same seasonal pattern. Without a proper marginal cost analysis, the words "over-collection" and "cross-subsidy" are assertions, not findings.

This was also strategic: if the cost analysis is weak, RIE can frame the entire proposal as a policy subsidy dressed up as cost-based rate design. Peter (Concentric) made this explicit: "if there's a policy argument, that's much different from the underlying cost analysis."

### How our research answers this

Our RI report does exactly what was missing in September 2024: a full Bill Alignment Test (BAT) using marginal cost-of-service analysis.

We computed the actual delivery cost-of-service for every ResStock building in Rhode Island using:

- Cambium marginal energy costs (hourly, location-specific)
- Cambium marginal generation capacity costs (allocated to top hours)
- Marginal bulk transmission costs (from RIE's own OATT filings)
- Marginal distribution capacity costs derived from RIE's own feeder-level thermal screening data — using local feeder peaks, not ISO-NE coincident peaks

The results are unambiguous:

- HP customers' delivery cost-of-service is only **4% higher** than fossil fuel customers ($1,224 vs. $1,176/year)
- But HP customers' delivery **bills** are **142% higher** ($2,525 vs. $1,044/year)
- The average overpayment is **$1,301 per year** per HP customer

This is no longer a revenue analysis with hand-waving about grid capacity. It is a direct comparison of what HP customers pay versus what they cost to serve, using the utility's own distribution data and established marginal cost methodologies. The cross-subsidy is measured, not asserted.

On Lance's specific point about O&M and depreciation: our BAT allocates all marginal costs — capacity, energy, O&M — hour by hour. Winter consumption does impose some marginal costs (energy and O&M). But the capacity cost — which is by far the largest driver of delivery cost-of-service — is near zero in winter because no feeders are winter-constrained (see objection #3).

## 2. "Any rate must be revenue-neutral" -> it is, at the customer class level. it can't be at the subclass-level, or you don't fix the cost allocation problem.

### What they said

Carrie pointed to Central Maine Power's pilot, which was revenue-neutral: CMP raised the customer charge ($29 → $40/month), lowered winter delivery to $0.01/kWh, and raised summer delivery to $0.27/kWh. She framed revenue neutrality as a core ratemaking principle:

> "That revenue neutrality, I think, is a key component that is important to us from a rate making principles perspective."

### Where they were coming from

RIE was defining the design space for any acceptable rate: if you lower winter delivery charges, you must raise something else to keep total collections constant _from HP customers as a class_. They weren't asking for revenue neutrality across all customers — they were saying the rate should not create a revenue shortfall that other customers subsidize.

This was partly a legitimate ratemaking concern and partly a framing device. By insisting on revenue neutrality _within the HP class_, they're implicitly rejecting the premise that HP customers are currently overpaying. If HP customers are paying too much, then reducing their bills isn't a revenue "loss" — it's a correction. But RIE hadn't seen the cost analysis to prove that, so from their perspective, a winter discount is a revenue reduction unless offset.

### How our research answers this

Our proposed rate IS correcting an overcollection, not creating a subsidy. The BAT shows HP customers pay $1,301/year more than their cost-of-service, on average. Reducing their winter delivery rate to align bills with costs is not a revenue shortfall — it's the removal of an unjust cross-subsidy.

That said, the proposal does have a revenue impact: when HP customers stop overpaying, the flat rate for everyone else must rise slightly to make up the difference. Our analysis quantifies this precisely:

- Non-HP customers would see bills rise by **$2.37/month** on average
- **93%** of non-HP households see increases under $5/month
- The total cross-subsidy being removed is ~$12 million/year, spread across the full residential customer base

This is modest and proportionate. The CMP model (raising summer rates to $0.27/kWh) would be problematic in RI due to summer AC loads — Carrie herself flagged this. Our approach avoids that entirely: summer rates stay at the current default. The "revenue neutrality" comes from correctly pricing delivery for the HP class, not from shifting costs between seasons.

The real question: why should HP customers continue to subsidize everyone else by $1,301/year each, so that fossil fuel customers can enjoy a $2.37/month discount? That's the tradeoff RIE is implicitly defending.

## 3. "Eight years from now, the system flips to winter-peaking — then what?" -> your own data says it will take 2 decades.

### What they said

This was a two-part objection. Lance raised the macro question:

> "Do you think it's a problem if we drop the rates by 50%, knowing that, like, eight years from now that reverses?... where suddenly the key metric for distribution system investment reverses."

And Carrie raised the customer experience angle, calling it a "ticking time bomb":

> "Within the lifetime of that heat pump, they are going to see first a very low rate, and then, when we account for the winter peaking of the system, a very high rate. And that is extremely concerning to us today."

She also cited CMP's experience: "25% of their circuits are already winter peaking. And they're expected to be winter peaking by 2030."

### Where they were coming from

This was their strongest rhetorical argument, even though it collapses under scrutiny. The concern is genuine from a customer relations perspective: utilities dread the scenario where customers blame them for "pulling the rug out." If RIE promotes a low winter rate, and then winter peaks catch up, they'd have to raise it — and customers who invested in heat pumps based on those economics would be furious.

They were also conflating three different things: (a) the ISO-NE system becoming winter-peaking (a macro event), (b) individual distribution feeders becoming winter-constrained (what actually drives local distribution costs), and (c) CMP's experience in Maine (a different climate, utility, and grid). Lance's eight-year number came from an ISO-NE forecast of system-wide peaks. But system-wide winter peaking doesn't mean every feeder is constrained — it just means aggregate winter demand exceeds aggregate summer demand. The distribution grid's local headroom is what actually matters for delivery cost-of-service.

### How our research answers this

This is where our RI-specific feeder analysis is devastating:

- RIE's distribution grid is so summer-dominated that **planners don't even measure winter peaks**. They estimate them at 70% of summer.
- **Zero feeders** are currently winter-constrained. Not one.
- **98% of feeders** have more than 30% winter headroom. The **median winter headroom is 56%**.
- Even by **2039**, with 19–22% of customers having heat pumps (per RIE's own adoption forecast), **zero feeders are expected to become winter-constrained** due to winter peak growth.
- **84% of feeders** are expected to still have more than 20% winter headroom in 2039.
- RIE's own grid modernization study says HPs are not expected to strain the distribution system until the **2040s**.
- In 2039, the system-wide winter peak is still only expected to be **86%** of the summer peak.

The "eight years" claim from the call was based on an ISO-NE system-level forecast, not distribution-level analysis. Rhode Island's distribution grid has far more winter headroom than the ISO-NE system as a whole, because distribution systems are sized for local non-coincident peaks (which are highly summer-dominated in RI).

CMP's experience in Maine is not transferable. Maine has minimal AC load, so its summer peaks are lower relative to winter — meaning Maine feeders become winter-constrained at lower HP penetration rates. Rhode Island's summer peaks are robust (and growing due to AC), which preserves the winter-summer gap.

On the "rate whiplash" concern: the correct response is not to keep overcharging HP customers for 15+ years. It's to design the rate with a transparent glide path. The report's framework already addresses this — the rate is designed for the current period, while the system has ample headroom, and should evolve as cost-of-service changes. Regulators revisit rates every few years anyway. The alternative — doing nothing — means forcing HP customers to overpay by $1,301/year for the next two decades.

## 4. "TOU rates solve this better" -> sure, if you solve the underlying cost allocation first. if not, then no, actually.

### What they said

Carrie and Peter argued that time-of-use rates (which are being rolled out alongside AMI) would marry cost and policy objectives better than a seasonal rate:

> "The nice thing about the time of use rate... is it kind of marries the two. In a way that maybe this heat pump rate would not."

Carrie cited CMP sunsetting its seasonal pilot in favor of TOU:

> "The commission is just having a sunset both of these pilots in 2026 because time of use rates are more popular and just as effective."

### Where they were coming from

This serves multiple purposes for RIE. First, it's a delay tactic: AMI rollout takes years, and TOU design proceedings take more years on top of that. Saying "let's wait for TOU" is a polite way of saying "let's not do this now." Second, it's genuine preference — TOU is a more comprehensive rate design that Concentric would design and implement (generating consulting revenue). Third, it positions the utility as pro-innovation without requiring the specific action CLF is asking for.

But the argument conflates two problems. TOU addresses within-day peak management: shifting load from expensive peak hours to cheaper off-peak hours. The seasonal HP rate addresses a fundamentally different problem: the structural overcollection from HP customers due to volumetric delivery pricing. These are orthogonal.

### How our research answers this

TOU and seasonal HP rates solve different problems:

- **TOU** helps customers manage their bills by shifting consumption to cheaper hours. It addresses the _within-day_ allocation of costs. It benefits customers with flexible loads (HP preheating, EV charging, etc.) and can help manage peak growth.
- **The seasonal HP rate** corrects the _structural overcollection_ that volumetric rates impose on HP customers. A customer who perfectly load-shifts under TOU still has the same total kWh flowing through volumetric delivery rates. TOU does not fix the cross-subsidy.

Moreover, TOU requires AMI, which is years from full deployment in Rhode Island. The cross-subsidy exists today — HP customers are overpaying by $1,301/year right now. Waiting for AMI and TOU design proceedings means accepting years of continued unfairness.

The CMP comparison is misleading. Maine customers don't use much AC, so CMP's high-summer-rate revenue-neutrality trick was painless there. In Rhode Island, Carrie herself pointed out that summer AC is a public health concern. A CMP-style TOU rate with high summer peaks would hurt summer cooling. That's precisely why a seasonal HP rate — which leaves summer rates unchanged — is the better near-term approach.

Finally, the two are not mutually exclusive. You can have a seasonal HP rate now and layer TOU on top later. Massachusetts is doing exactly this.

## 5. "Enrollment will be too low to matter" -> not if you retroactively opt exiting HP customers people in, which our design lets you do. and pair accelerator and utility HP programs with enrollment.

### What they said

Carrie was struck by CMP's experience:

> "They have less than 1% of eligible households enrolled for this heat pump rate. So that was fairly shocking to us."

She then framed the calculus as an ROI question:

> "Deploying rates... require resources, time and money. And so the calculus from our point of view is: is it worth it?"

### Where they were coming from

This is partly a practical concern and partly a way to argue the rate isn't worth the effort. If enrollment is low, the rate doesn't accomplish its goals — and the utility still bears the implementation costs (billing system changes, customer outreach, etc.), which get recovered from all ratepayers. It's a "why bother?" argument.

But CMP's low enrollment is a design flaw, not an inherent feature of seasonal HP rates. CMP requires customers to know about the rate and opt in. If customers don't know it exists, they can't enroll. Massachusetts solved this by auto-enrolling heat pump customers through Mass Save. The question isn't whether CMP got low enrollment — it's whether RI can design a better enrollment mechanism.

### How our research answers this

Our proposal is designed to be retroactively applicable to all known heat pump customers. Combined with enrollment through Clean Heat Rhode Island (RI's heat pump incentive program), this addresses the CMP problem directly. Every customer who receives a heat pump rebate should be automatically enrolled.

The report also shows why enrollment matters: the average HP customer is overpaying by $1,301/year. Even with low HP penetration (~2% of residential customers), the per-household stakes are enormous. CMP's low enrollment hurt customers who could have saved, but it didn't create a macro revenue problem — which is exactly Carrie's point that "the changes in collections are relatively small in aggregate."

In other words, low enrollment doesn't harm the utility — it harms customers. The question is whether the PUC and stakeholders accept that harm.

## 6. "Summer AC load makes the CMP model unworkable here"

### What they said

Carrie pointed out that CMP's revenue-neutral design (high summer delivery rate) was painless in Maine because Mainers don't use much AC:

> "Down here, obviously, we're having record heat stretches. And really odd weather and air conditioning is actually public health concern."

### Where they were coming from

This was a legitimate and perceptive point. CMP's pilot raised summer delivery to $0.27/kWh to offset the winter discount. In a climate with significant summer AC use, that would be counterproductive: it would penalize customers for using their heat pumps as AC during heat waves, create affordability problems in summer, and potentially increase summer peak stress.

### How our research answers this

Our proposed rate does not raise summer rates. The summer volumetric delivery rate equals the current default rate — no change. The winter rate is lowered to align HP customer bills with their delivery cost-of-service.

The revenue impact is absorbed across the full customer base: non-HP customers see an average increase of $2.37/month. This is a far better design than CMP's seasonal swap.

Moreover, RIE's own load forecasts assume that heat pumps _lower_ the summer peak due to their increased efficiency over traditional air conditioning. So HP customers are arguably making summer peaks better, not worse.

## 7. "You didn't model the cascading effects" -> yes, in a simple way (your own forecast)

### What they said

Someone (unclear who, likely Carrie or one of the Concentric team) asked:

> "Does your analysis consider sort of the cascading effect of if the rate goes into effect, and there has increased, accelerated adoption? How that cascades into increased cost, acceleration of transition to winter peak?"

### Where they were coming from

The concern is that the rate works under static conditions, but success changes the conditions. If the rate accelerates HP adoption, that accelerates winter peak growth, which accelerates the timeline to winter-constrained feeders, which increases costs. The analysis might show the rate is good today but not account for the dynamic it sets in motion.

### How our research answers this

The report's feeder analysis already accounts for this. RIE's own peak growth forecasts (which incorporate HP adoption growth) show that even with 19–22% HP penetration by 2039:

- Zero feeders become winter-constrained
- 84% of feeders still have >20% winter headroom
- The system-wide winter peak is only 86% of summer

The grid has so much winter headroom that even aggressive adoption scenarios don't create distribution constraints for 15+ years. The "cascading effect" concern assumes a much shorter timeline to winter constraints than the data supports.

The report also includes adoption scenarios that project grid impact from accelerated HP adoption under fair rates. The additional load from fair-rate-induced adoption is modest relative to the grid's available winter capacity.

## 8. The meta-argument: "policy vs. cost"—this is cost-based. and 4600 principles say policy also matters.

### What they said

Peter (Concentric) drew a bright line:

> "If there's a policy argument, that's much different from the underlying cost analysis. And so you could justify certain things on the basis of the policy as opposed to necessarily the cost."

Carrie echoed this as RIE's institutional stance:

> "We will use a cost-based method. That is our role as a regulated utility... If there is a policy element and we are directed to do so because of the policy, that's not our decision to make on behalf of all of our customers."

### Where they were coming from

This is the utility's core framing strategy: position themselves as neutral cost-of-service technicians who defer to regulators on policy. If the HP rate is policy, the PUC has to order it. If it's cost-based, the utility can design it themselves. By insisting the evidence is insufficient for a cost-based justification, they force the issue into a regulatory proceeding where they can delay, litigate, and control the narrative.

It's also a genuine belief: Concentric's rate design consultants live in the CCOS world. They genuinely think cost analysis must precede rate design, and at the time of the call, the cost analysis hadn't been done.

### How our research answers this

Our RI analysis is cost-based. The BAT is a marginal cost-of-service methodology. We've computed delivery cost-of-service for every building class using the utility's own data. The result — $1,301/year average overpayment by HP customers — is a cost finding, not a policy preference.

That said, the cost analysis _also_ supports good policy. Correcting the cross-subsidy would cause 97% of gas-heated households (vs. 26% today) to save money by switching to heat pumps. The fact that fairness and climate goals align is not a coincidence — it's what happens when rates actually reflect costs.

RIE's framing is a false dichotomy. Cost-based ratemaking and policy objectives are not in tension here. The cost analysis shows the current rates are unfair. Fixing them happens to advance state climate goals. Both arguments point in the same direction.

## Summary table

| RIE objection                   | Their real concern                                             | Our response (short form)                                                                                                                              |
| ------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Cost causation not demonstrated | Revenue analysis ≠ cost analysis; ISO-NE CP ≠ distribution NCP | Full BAT with feeder-level marginal costs. HP cost-of-service is 4% higher than FF; HP bills are 142% higher. Overpayment: $1,301/yr.                  |
| Must be revenue-neutral         | Don't create a revenue shortfall other customers subsidize     | It's not a shortfall — it's removing a $12M/yr overcollection. Non-HP impact: $2.37/month.                                                             |
| Winter peaking in 8 years       | Customers get low rate then high rate within HP lifetime       | Zero feeders winter-constrained today or by 2039. 98% have >30% winter headroom. Median: 56%. RIE's own planners say 2040s earliest.                   |
| TOU rates solve this better     | Wait for AMI; TOU marries cost and policy                      | TOU solves a different problem (within-day peaks, not volumetric overcollection). Not mutually exclusive. AMI is years away; cross-subsidy exists now. |
| Low enrollment                  | Admin costs not worth it for low take-up                       | CMP's low enrollment is a design flaw (no auto-enroll). Propose auto-enrollment via Clean Heat RI.                                                     |
| Summer AC concerns              | Can't raise summer rates like CMP did in Maine                 | Our rate doesn't touch summer rates. Summer = current default.                                                                                         |
| Cascading effects not modeled   | Success accelerates winter peaking                             | Even with 19–22% HP adoption by 2039, zero feeders become winter-constrained. Grid has massive headroom.                                               |
| "Policy, not cost"              | Force issue into regulatory proceeding; maintain control       | Our analysis IS cost-based. BAT is marginal cost-of-service. Cost and policy happen to align.                                                          |
