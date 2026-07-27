# How BGE Designed a "Cost-Based" TOU Rate: The Schedule RD Methodology

_A companion to [`bge_tou_rates.md`](./bge_tou_rates.md). That explainer tells you **what** Schedule RD is and how the four BGE TOU rates relate. This one goes deeper on the single hardest question: **how did BGE and the Maryland PC44 Rate Design Work Group actually design a TOU rate that is "cost-based" for both supply and distribution?** What does "cost-based" mean mechanically, when did they decide costs "occur," and how did that produce specific hours and a specific price ratio?_

---

## What I'm assuming you already know

This report is calibrated to an analyst fluent in the concepts in the [NY HP rates report](../../reports/ny_hp_rates/index.qmd): the split between **supply costs** (generation, wholesale energy, capacity, transmission) and **delivery/distribution costs** (poles and wires); **cost of service** vs. **bill**; **cost causation** (rates should track the costs a customer imposes); **marginal cost**; **cross-subsidy**; and the fact that **distribution capacity is driven by peak demand, not total energy**. I won't re-explain those.

I _will_ introduce the TOU-specific machinery the analyst hasn't dug into: **peak-period definition from load curves**, **average-and-peak cost allocation**, **PJM coincident-peak (5CP) capacity mechanics**, **revenue-neutral rate shaping**, the **"all-in" ratio**, and **free ridership**.

One framing to hold onto throughout: **"cost-based" here does not mean "built from an 8760 hourly marginal-cost vector."** It means something much more modest and much more common — take the utility's existing embedded (accounting) cost of service, decide which broad hours those costs are "responsible for," and shovel the costs into those hours. The entire methodological fight in Maryland is about _how much_ to shovel and _into which hours_ — not about building a granular hourly cost curve. That is the single most important thing to understand, so I'll return to it.

---

## Part 1: The methodology arc (2017 → 2025), as a story

The design of Schedule RD was not one decision. It was a five-stage evolution in which the _method_ stayed roughly constant while the _aggressiveness_ ratcheted down, driven by a persistent tension between price-signal strength and customer enrollment.

| Stage                             | Document                                                                                     | What the method was                                                                                                            | Resulting BGE ratio                           |
| --------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------- |
| **Straw proposal** (Jun 2017)     | [straw proposal](../sources/md_hp_rates/mdpuc_pc44_rate_design_straw_proposal_20170627.md)   | Narrow peak windows from load curves; allocate ~100% of primary distribution to on-peak; layer capacity/transmission into peak | Supply 3:1; distribution ~7:1                 |
| **Final Report** (Feb 2018)       | [Final Report](../sources/md_hp_rates/mdpuc_218934_pc44_rate_design_final_report.md) §1.b    | Same, refined to a genuinely cost-based ratio using the EV-tariff method                                                       | All-in **4.3:1** (supply 4.0:1, dist. 5.2:1)  |
| **Pilot as run** (2019–2021)      | [2022 report](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md) | Same method, per-utility                                                                                                       | All-in **4:1–6:1** across the three utilities |
| **Full-scale / permanent** (2022) | [2022 report](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md) | **Non-consensus:** Staff/Utility "100%-primary-on-peak" vs. OPC "average-and-peak (~60/40)"                                    | RD launched **3.2:1** (primary-on-peak)       |
| **DRIVE Act reshape** (2025)      | [Order 91917](../sources/md_hp_rates/mdpuc_9761_order_91917_drive_act_implementation.md)     | Commission adopts OPC's **average-and-peak 60/40** split                                                                       | RD **2.8:1**                                  |

The plot: PC44 designed an aggressive, defensibly cost-based rate; the pilot proved customers respond (BGE −9.3% summer weekday peak, −4.9% non-summer); the permanent rollout barely enrolled anyone (~1,200 of 1.25M); and DRIVE responded by **weakening the signal to sell more of it** — which, conveniently, also meant adopting the _milder_ of the two cost-allocation methods that had been on the table since 2022.

### The disagreements that actually shaped the rate

Three fights matter methodologically, because the filed rate is literally the residue of who won them:

1. **How steep, and why (2017–2018).** The straw proposal floated a 3:1 supply / ~7:1 distribution structure (and a 7:1 "innovative" Pilot 2). The Final Report pulled back to a genuinely cost-derived ~4:1, explicitly worrying that a _forced_ 3:1 "would require that the SOS TOU supply rate be forced to undergo a significant administrative adjustment… [that] could raise concerns as not being cost-based" ([Final Report §1.b](../sources/md_hp_rates/mdpuc_218934_pc44_rate_design_final_report.md)). This is the pivotal conceptual move: **they chose to let the ratio be an _output_ of a cost method rather than an _input_ chosen for behavioral effect.** A round-number target picked for its psychological punch is not cost-based; a number that falls out of an allocation rule is.

2. **100%-to-on-peak vs. average-and-peak (2022).** This is the crux and gets its own section (Part 2). Staff and the utilities wanted to keep dumping **all** primary distribution cost into the on-peak window (the pilot design). OPC wanted an **average-and-peak** split — roughly **60% on-peak, 40% spread across all hours** — arguing the wires serve load in _every_ hour, not just at peak. The Work Group deadlocked and sent both to the Commission.

3. **Weaken it for enrollment (2025).** Under DRIVE, BGE asked to drop RD from 3.2:1 to 2.8:1 because "the peak rate itself was the barrier." Solar/storage intervenors (SEIA, Advanced Energy United, CHESSA) objected that a lower ratio worsens **free ridership** — customers whose load is already off-peak enroll, collect savings, change nothing. The Commission sided with BGE on RD **on enrollment grounds** ([Order 91917 §II.C.1](../sources/md_hp_rates/mdpuc_9761_order_91917_drive_act_implementation.md)), and adopting OPC's 60/40 average-and-peak was the mechanism that produced the milder 2.8:1.

So the rate you see today — 60/40 average-and-peak, 2.8:1 all-in — is OPC's 2022 method, ratified in 2025 for a reason (enrollment) only loosely related to why OPC proposed it (cost causation + enrollment).

---

## Part 2: When do distribution costs "occur"? (The analyst's #1 question)

Here is the honest headline, stated plainly because the sources support stating it plainly:

> **They did not build an 8760 hourly cost vector. They did not do a probability-of-peak / loss-of-load-probability weighting of the top ~100 hours. There is no `$/kWh`-per-hour marginal cost curve anywhere in this record.** The method is a **two-step embedded-cost allocation**: (1) define broad on-peak _windows_ by looking at residential load shapes, then (2) assign a share of the utility's existing (accounting) distribution revenue requirement to those windows.

That is a genuinely different animal from the granular marginal-cost approaches the analyst may be picturing. Let me walk both steps.

### Step 1 — Defining the on-peak windows (load-shape judgment, not marginal cost)

The peak windows come from **utility residential load curves / load research** — i.e., "when is residential demand actually high?" — tempered by judgment and by rough alignment with PJM's peak. They are _not_ derived by ranking 8760 hours by marginal cost and drawing a line.

The straw proposal is explicit that windows are "based on utility load curves" and deliberately **narrow** (a "relatively narrow peak window (i.e. 5 hours)"), giving BGE a 3–8pm summer peak from the start ([straw proposal, Pilot #1 Rate Structure](../sources/md_hp_rates/mdpuc_pc44_rate_design_straw_proposal_20170627.md)). The 2022 report says the Work Group set periods "based on analysis of system elements" and shifted BGE's summer peak one hour later and **added a second winter evening peak** ([2022 report, Peak Periods](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md)). The final windows now in the tariff ([Karas testimony, Schedule RD Rating Periods](../sources/md_hp_rates/mdpuc_331766_direct_testimony_karas.md)):

| Season     | On-peak (weekdays, ex-holidays) | What drives it                                                                                               |
| ---------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Summer     | 3–8pm                           | AC at max, evening arrival, solar declining — coincides with both distribution loading _and_ PJM system peak |
| Non-summer | 6–9am **and** 5–9pm             | The two-humped winter residential shape: morning wake-up (heat, hot water, showers) and evening return       |

The winter **two-hump** is the tell that this is a **residential load-shape** design, not a system-marginal-cost design. A summer-peaking distribution system does not incur its capacity cost at 7am in January — but residential _load_ has a morning hump then, so the window is there.

**How judgment enters, concretely:** in the parallel Potomac Edison discussion, OPC showed that **46% of PJM's 5CP hours (2018–2024) occurred before 5pm**, so it recommended shifting a proposed 5–9pm summer window to 4–8pm; the Commission agreed, noting this "will better align the company's on-peak window with PJM's historical coincident peak hours" ([Order 91917 §II.C.3](../sources/md_hp_rates/mdpuc_9761_order_91917_drive_act_implementation.md)). That is the closest anyone in this record gets to a data-driven, hour-ranking peak definition — and it's a _sanity check against 5CP frequency_, not a cost-vector optimization.

### Step 2 — Allocating distribution cost into the windows (the two rival methods)

Once the hours are fixed, the question is: **how much of BGE's distribution revenue requirement belongs in those hours?** Two answers competed.

**Method A — "100% of primary distribution to on-peak" (straw proposal, then Staff/Utility 2022 option).** The logic: the **primary** distribution system (the medium-voltage backbone) is _sized_ to meet peak demand, so all of its cost is "caused" by the peak, so all of it goes into the on-peak hours. This is a peak-responsibility allocation taken to its limit. It produces steep distribution ratios (straw: ~7:1; Final Report BGE: 5.2:1). The utilities liked it because it "avoids adding another layer of complexity" and preserves a strong signal ([2022 report, Distribution Rate Options](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md)).

**Method B — "average-and-peak" (OPC, 2022; adopted 2025).** The logic: the wires don't _only_ serve the peak — they carry load in all 8760 hours — so only the _incremental_ capacity above average belongs to the peak, while the "average" baseline is spread across all hours. Mechanically, the split is driven by the **residential class load factor** (average demand ÷ peak demand). For BGE this lands at roughly **60% of primary distribution in the on-peak period, 40% spread across all hours** ([2022 report](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md); [Karas testimony](../sources/md_hp_rates/mdpuc_331766_direct_testimony_karas.md), confirming the filed 60/40). It produces gentler ratios (2.8:1 all-in for RD).

**Average-and-peak, unpacked.** This is a standard, decades-old **hourly-embedded** allocator (it appears in NARUC's cost-allocation manual and is discussed at length in [`traditional_vs_hourly_ecoss_and_mcos.md`](../domain/traditional_vs_hourly_ecoss_and_mcos.md)). The "average" piece classifies a chunk of demand-related cost as if it were energy-like (present in all hours); the "peak" piece assigns the rest to the peak hours. The higher a class's load factor, the more "average" and the less "peak" — which is exactly why OPC's split varies by utility. In the Commission's words, moderating the differential "will serve to reallocate a significant portion of transmission and capacity costs across all hours, not just peak hours… in a manner that reflects the typical residential load factor" ([Order 91917 §II.C.2](../sources/md_hp_rates/mdpuc_9761_order_91917_drive_act_implementation.md), in the PHI holding).

**Neither method is marginal cost.** Both start from the **embedded** class cost-of-service study (the same ACOSS/ECOSS used to set the flat rate) and re-time it. Method A says "100% of it is peak-caused"; Method B says "load-factor% of it is peak-caused." That's the whole disagreement. The 2022 report is candid that even the _pilot's_ cost basis was "designed from existing distribution rates and shifted all primary distribution system costs into the on-peak period" ([2022 report](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md)) — i.e., a re-timing of embedded rates, not a fresh marginal study.

> **Gap flag.** The corpus never states which percentile of the load curve, or which specific load-research hours, were used to pick "3–8pm." "Based on utility load curves" and "analysis of system elements" is as specific as it gets. Nor does it show the arithmetic of the 60/40 split (the underlying load-factor number). Those live in BGE cost-of-service workpapers not in this corpus.

---

## Part 3: When do supply costs "occur"? (Same trick, different inputs)

Supply is handled with the **same two-step logic** — define windows, load costs into them — but with different cost components, and it's worth separating the three pieces of "supply."

The recipe, unchanged from pilot to permanent: **start from the auction-based SOS rate, then add transmission and estimated capacity costs into the peak periods to create the on/off differential** ([2022 report, Supply Rate](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md)). This deliberately mirrors "the methodology used by BGE and Pepco in their permanent electric vehicle tariffs" ([Final Report §1.b](../sources/md_hp_rates/mdpuc_218934_pc44_rate_design_final_report.md)). So:

- **(a) Wholesale energy.** _Not_ resolved to hourly LMPs. The SOS energy cost is the **seasonally-reset auction price** — effectively a within-season average. It provides the baseline that is essentially flat across the day; the auction embeds wholesale energy value but the rate does **not** carry an hourly LMP shape. This is the biggest "cost-based-in-name" simplification on the supply side: there is no LMP 8760 either.

- **(b) Generation capacity.** This is the piece that is genuinely peak-driven and gets loaded into the on-peak window. PJM assigns each zone a capacity obligation based on its **Peak Load Contribution (PLC)** — its load during PJM's **five coincident-peak (5CP) hours** of the prior summer. Because a customer's capacity cost is caused almost entirely by consumption during those handful of hours, allocating capacity cost to the on-peak window is defensible cost causation. The Commission spells out the 5CP mechanic explicitly ([Order 91917, n.73](../sources/md_hp_rates/mdpuc_9761_order_91917_drive_act_implementation.md)).

- **(c) Transmission.** Similar logic via **network transmission PLC** (a coincident-peak allocator). Loaded into peak alongside capacity. The Work Group agreed there is "a cost-basis for allocating these PJM regional costs to the TOU peak-periods… consistent with the existing EV tariffs" ([Final Report, n.17](../sources/md_hp_rates/mdpuc_218934_pc44_rate_design_final_report.md)).

The reporting regime confirms which allocators are the live ones: annual metrics track **PLC for PJM capacity** and **network transmission PLC**, plus class **coincident peak (CP)** and **non-coincident peak (NCP)** ([2022 report, Metrics](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md)). Capacity/transmission are coincident-peak (5CP-style) costs; distribution CP/NCP is the local peak.

Net: the supply side is **auction energy (flat within season) + peak-loaded capacity + peak-loaded transmission**. Only the capacity and transmission adders create the on/off differential, and both rest on coincident-peak allocation, which is real cost causation. The energy piece is not hourly.

---

## Part 4: From cost analysis to a schedule and a ratio (revenue-neutral shaping)

Now the two halves come together into an actual tariff. Two mechanics to understand.

### Revenue-neutral rate shaping

The distribution TOU rate is designed to be **revenue neutral to the flat Schedule R** ([Karas testimony](../sources/md_hp_rates/mdpuc_331766_direct_testimony_karas.md): "TOU distribution rates designed to be revenue neutral to Schedule R"). Concretely: hold the total distribution revenue collected from an **average-load-profile customer who does _not_ shift** roughly constant, then split that same revenue between on- and off-peak prices according to the chosen allocation (60/40 for RD). The on-peak price is whatever makes the on-peak bucket collect its share; the off-peak price collects the rest.

Two consequences the Work Group cared about:

1. **The ratio is an _output_, not a target.** Once you fix (a) the windows, (b) the allocation split, and (c) revenue neutrality, the peak:off-peak ratio is determined. This is why the Final Report insisted on deriving the ratio rather than forcing a round number.

2. **Seasonal tempering.** A pure allocation produced summer distribution prices so high that a summer customer "being unable to achieve any bill savings during the summer months relative to the standard residential rate — even if they shifted 10% of their load" ([2022 report](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md)). All parties agreed to temper this so that both seasons offer achievable savings. Notably, **BGE's RD delivery prices are _not_ seasonally differentiated** — only the hour definitions change by season (see [`bge_tou_rates.md`](./bge_tou_rates.md), Part 6). That's an administrative simplification that departs from strict cost causation.

### Why the ratio is quoted "all-in"

A "2.8:1 ratio" means on-peak total price ÷ off-peak total price = 2.8, where "total" = **supply + delivery + riders**, i.e., what actually hits the bill. It's quoted all-in for two reasons: (1) it's what the customer experiences and responds to, and (2) a strong ratio on one component gets **diluted** once flat components are added to both sides. The Final Report's BGE table makes this visible: distribution ratio 5.2:1 and supply ratio 4.0:1 blend to an **all-in 4.3:1** ([Final Report §1.b](../sources/md_hp_rates/mdpuc_218934_pc44_rate_design_final_report.md)). Any single-component ratio overstates the behavioral signal.

---

## Part 5: Are supply and distribution costs correlated? (Does one combined period even make sense?)

This is the deepest question in the brief, and the sources answer it only partially — so I'll separate what's documented from what's inference.

**What the design assumes:** a **single combined on-peak period** applies to _both_ supply and distribution ([Final Report summary table](../sources/md_hp_rates/mdpuc_218934_pc44_rate_design_final_report.md): "Peak Period: Supply — Same as Distribution Peak Periods"). This only makes sense if the hours that drive distribution cost roughly coincide with the hours that drive supply (PJM) cost.

**Summer: they largely coincide.** The summer 3–8pm window catches both BGE's distribution loading (AC + evening arrival) _and_ PJM's system 5CP, which lands in summer afternoons. Here the combined period is well-justified — one window signals both cost drivers. The Potomac Edison 5CP evidence (91% of PJM peaks captured by a 4–8pm window) confirms summer alignment is achievable.

**Winter: they diverge — and this is the crack in the design.** BGE's distribution/residential load has a winter **two-hump** (6–9am, 5–9pm), so the winter on-peak window is fundamentally a **distribution/load-shape** window. But PJM capacity and network transmission costs — the supply adders loaded into on-peak — are driven by the **summer** 5CP. So a winter-morning on-peak kWh:

- _does_ plausibly drive **local winter distribution** loading (if the feeder peaks in winter), but
- _does not_ drive **PJM summer capacity/transmission** cost at all —

yet the rate charges the capacity/transmission adder on it anyway. The combined period **over-assigns summer-driven supply costs to winter on-peak hours.** This is the same structural point flagged in [`bge_tou_rates.md`](./bge_tou_rates.md), Part 6 (winter-morning kWh on a summer-peaking system), viewed from the correlation angle. It's precisely the kind of divergence that matters for heat pump work, since heat pumps concentrate new load in exactly those winter hours.

**Is the divergence documented as a correlation study? No.** The corpus never presents an explicit "do distribution-peak hours coincide with supply-peak hours?" analysis. The 2022 report even concedes it never quantified the distribution-side cost reductions at all: "while cost can be calculated by extrapolation for distribution system margin cost of service, that analysis was not undertaken" ([2022 report, intro](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md)). The Commission's forward-looking metrics (tracking CP, NCP, and PLC separately) are arguably an implicit acknowledgment that these peaks can diverge and should be watched — but no one closed the loop. **The summer-coincide / winter-diverge reading above is my synthesis of the load shapes and the 5CP mechanics, not a finding the sources state outright.**

---

## Part 6: How typical is any of this? (National context — largely my inference)

To calibrate whether the analyst is looking at standard practice or something distinctive. Where I'm inferring prevalence from general knowledge of U.S. rate design rather than citing these sources, I say so.

- **Embedded-cost allocation onto judgment-defined windows: standard, even dominant.** _(Inference.)_ Most U.S. residential TOU rates define peak windows from load-shape judgment and system-peak timing, then allocate embedded revenue-requirement into them, exactly as PC44 did. A true 8760 marginal-cost / LOLP-weighted design is the _exception_, mostly seen in sophisticated CPP/RTP pilots, some California work, and academic/consultant studies (the kind of hourly marginal-cost work Switchbox itself does). So the absence of an 8760 cost vector here is **normal**, not a Maryland failing.

- **Average-and-peak allocation: standard and well-established.** _(Inference + [`traditional_vs_hourly_ecoss_and_mcos.md`](../domain/traditional_vs_hourly_ecoss_and_mcos.md).)_ It's a textbook NARUC allocator. What's mildly notable is seeing it used to set _TOU period prices_ rather than just to split demand vs. energy classification in a static COSS — but it's a natural extension, not novel.

- **100%-to-on-peak: aggressive but not unheard-of.** _(Inference.)_ Assigning all peak-dimensioned distribution cost to the peak window is a defensible peak-responsibility position; it's on the steep end of common practice and tends to lose to average-and-peak when consumer advocates are at the table — which is exactly what happened here.

- **Two-period, no-intermediate design: common for modern opt-in residential TOU.** _(Inference.)_ Simpler for customers; the intermediate period is more of a legacy-meter artifact (BGE's 1984 Schedule RL still has one). The PC44 choice to drop the intermediate is mainstream modern practice.

- **Loading PJM capacity/transmission (coincident-peak costs) into the on-peak window: standard in RTO territories.** _(Inference.)_ Any utility in PJM/ISO-NE/NYISO faces 5CP-style capacity allocation and commonly reflects it in TOU supply. This is orthodox.

- **The PC44 process itself — a multi-year, Commission-convened stakeholder work group with a formal EM&V pilot before a permanent rate — is somewhat distinctive.** _(Inference, supported by the corpus's own framing.)_ Many utilities file TOU rates directly in a rate case without a dedicated pilot. Maryland's deliberate pilot-then-scale arc with Brattle EM&V, LMI sub-sampling, and published load-shift results is on the more rigorous, transparent end of the spectrum. The specific _cost methodology_, though, is conventional; it's the _process_ that's above-average.

**Bottom line for the analyst:** the Schedule RD methodology is **methodologically ordinary but procedurally careful.** If you were expecting a granular hourly marginal-cost design, you won't find it — and that's not because Maryland cut corners, but because that's simply not how most U.S. TOU rates (including "cost-based" ones) are built.

---

## Summary of what "cost-based" meant here

| Question                                               | Answer                                                                                                                                                                                 |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Full 8760 hourly cost vector?                          | **No.**                                                                                                                                                                                |
| Top-~100-hours / LOLP / probability-of-peak weighting? | **No.**                                                                                                                                                                                |
| Hourly LMP shape on supply energy?                     | **No** — seasonal auction price (flat within season).                                                                                                                                  |
| How peak windows were set                              | Residential **load curves / load-shape judgment**, sanity-checked against PJM 5CP timing.                                                                                              |
| How distribution cost was timed                        | **Embedded** class cost re-timed: either 100%-primary-on-peak (Staff/Utility) or **average-and-peak ~60/40** (OPC, adopted).                                                           |
| How supply cost was timed                              | Auction energy baseline + **peak-loaded capacity (PJM 5CP/PLC)** + **peak-loaded transmission (network PLC)**.                                                                         |
| How the ratio was set                                  | **Revenue-neutral shaping**: fix windows + allocation split, hold non-shifter revenue constant → ratio falls out. Quoted **all-in**.                                                   |
| Supply/distribution correlation                        | **Coincide in summer, diverge in winter**; single combined period over-assigns summer capacity/transmission cost to winter on-peak hours. (Synthesis, not an explicit source finding.) |

---

## Sources

All in [`context/sources/md_hp_rates/`](../sources/md_hp_rates/):

- [PC44 Straw Proposal (Jun 2017)](../sources/md_hp_rates/mdpuc_pc44_rate_design_straw_proposal_20170627.md) — original cost-based method: narrow load-curve windows, ~100% primary distribution to on-peak, 3:1 supply / ~7:1 distribution.
- [PC44 Final Report (Feb 2018, ML 218934)](../sources/md_hp_rates/mdpuc_218934_pc44_rate_design_final_report.md) — §1.b cost-based ~4:1 ratio, EV-tariff supply method, capacity/transmission-to-peak rationale (n.17), pilot design.
- [PC44 Full-Scale Report (Jun 2022, ML 240945)](../sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md) — the two distribution options (100%-primary-on-peak vs. OPC average-and-peak 60/40), peak-period changes, supply method, revenue-neutral/seasonality discussion, metrics.
- [Order No. 91917 (Oct 2025, Case 9761)](../sources/md_hp_rates/mdpuc_9761_order_91917_drive_act_implementation.md) — RD 3.2→2.8 on enrollment grounds; PHI cost-causation defense of average-and-peak; 5CP mechanics (n.73); Potomac Edison window shift.
- [Karas direct testimony (Jul 2026, ML 331766)](../sources/md_hp_rates/mdpuc_331766_direct_testimony_karas.md) — filed RD design: 60/40 on/off-peak split, revenue neutral to Schedule R, current rating periods and delivery charges.
- Companion explainer: [`bge_tou_rates.md`](./bge_tou_rates.md) (Part 3 Schedule RD, Part 6 non-seasonal delivery point).
