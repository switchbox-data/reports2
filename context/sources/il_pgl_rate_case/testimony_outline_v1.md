# Direct Testimony of Juan-Pablo Velez — Outline (v1)

**Docket:** ICC Docket 26-0065 (The Peoples Gas Light and Coke Company general rate case; **not consolidated** with the parallel North Shore Gas docket — caption is 26-0065 only).

**Sponsoring party:** Switchbox, on behalf of Citizens Utility Board (CUB).

**Witness:** Juan-Pablo Velez (JPV), Switchbox.

**Form:** Direct testimony (intervener).

**Q-formatting (consistent throughout):** label-only, sentence case, period — `**Q.**` and `**A.**`.

**Exhibits (referenced by short form below):**

- **Ex. 1** — Statement of Qualifications (CV).
- **Ex. 2** — Methodology Memo (data sources, transformations, cost inputs, limitations; mirrors `notebooks/analysis.qmd` and the Data and Methods appendix of the Switchbox NPA report).
- **Ex. 3** — Histogram of block-level cost-effectiveness ratios (NPA cost / PRP cost), three scenarios overlaid.
- **Ex. 4** — Cumulative savings curve, three scenarios overlaid.
- **Ex. 5** — Total spending bar comparison (PRP vs. PRP-with-scattershot vs. coordinated NPA portfolio).
- **Ex. 6** — Density-vs-cost-effectiveness scatter (single-family and multi-family blocks).
- **Ex. 7** — Maps of cost-effective blocks under each scenario, plus three project-area zoom-ins (Lincoln Square, Garfield Ridge, Englewood) and summary table.

(Numbering is sequential; figures regroup at typeset if useful.)

---

## I. Introduction and qualifications

**Q.** Please state your name and business address.

**A.** Name; Switchbox business address.

**Q.** By whom are you employed and in what capacity?

**A.** Switchbox; role; one-paragraph description of Switchbox as a nonprofit policy data shop.

**Q.** On whose behalf are you submitting this testimony?

**A.** Citizens Utility Board.

**Q.** Please summarize your professional and educational background.

**A.** Career chronology in prose; references **Ex. 1** for CV.

**Q.** Have you previously testified before the Illinois Commerce Commission?

**A.** Brief; yes/no.

**Q.** Have you previously testified or submitted comments before regulatory commissions in other states?

**A.** List jurisdictions and topic areas (e.g., Rhode Island heat-pump rate work).

**Q.** Was this testimony prepared by you or under your direct supervision?

**A.** Yes.

**Q.** Are you sponsoring any exhibits with this testimony?

**A.** Yes — list **Ex. 1–Ex. 7**.

**Q.** What is the purpose of your testimony?

**A.** Two-sentence thesis: I quantify the upfront capital cost of meeting the 2035 CI/DI retirement deadline through targeted electrification ("non-pipe alternatives," NPAs) versus the company's proposed Pipe Retirement Program (PRP) on the residential blocks within PGL's planned 2026–2027 PRP project areas, and I identify the blocks and the framework conditions under which NPAs are cheaper than the PRP. The testimony recommends that the Commission require PGL to evaluate NPAs at the block and portfolio level before authorizing PRP spending in the test year.

**Q.** Please summarize your recommendations.

**A.** Numbered list (cross-references **§ IX**). Lead the testimony with the punch list so the reader has the asks before the analysis.

**Q.** Should your silence on any issue in this proceeding be construed as agreement with PGL or any other party?

**A.** No — the standard silence-is-not-agreement disclaimer (verbatim Leyko/DeLeon/Rábago boilerplate). Acknowledged here even though the device is more typical of rebuttal, because the testimony's scope is narrow and we want the hedge on the record.

---

## II. Background

Short. The reader is the ALJ and Commissioners; assume general familiarity with PGL but not with NPA methodology.

**Q.** Please briefly describe the regulatory and policy context for this case.

**A.** 2024 SMP Investigation Order requires retirement of all CI/DI mains under 36" in Chicago by January 1, 2035; PGL has rebranded its replacement program as the **Pipe Retirement Program (PRP)**; PGL's first PRP tranche in this case is roughly 1,020 miles of pipe across 179 projects, with project-level spending of about $188M in 2026 and $306M in 2027. Cite NSG-PGL Ex. 3.0 (Eldringhoff/Dickson) for scope; cite Eidukas overview for revenue-requirement context.

**Q.** Please briefly describe Chicago's electrification goals.

**A.** Chicago Climate Action Plan: ~30% of residential buildings electrified by 2035. Note the structural conflict between that goal and PGL's parallel goal of replacing 25% of mains over the same horizon — money spent twice on the same blocks unless planning is coordinated.

**Q.** What did PGL itself say in this docket about non-pipeline alternatives?

**A.** Quote NSG-PGL Ex. 3.0 at p. 99: PGL commits to considering NPAs and lists "geothermal systems, targeted electrification, and cured-in-place liners" as current options. Then quote the Graves/Figueroa/Sreenath foreclosure passage (PART_5 part1of68.pdf p. 8): "First, we believe it is neither feasible nor realistic for PGL to present material resource or service design plans in the current rate case that call for decarbonization …" Frame the gap between PGL's stated openness to NPAs and its argument that NPAs cannot be evaluated in this proceeding as the wedge this testimony addresses.

---

## III. Scope and approach

**Q.** What did your analysis examine?

**A.** Block-level comparison of upfront capital cost of (a) replacing CI/DI mains under PGL's PRP versus (b) electrifying all residential units on the block and decommissioning the gas main, across PGL's planned 2026–2027 PRP project areas in Chicago. Limited to **fully residential blocks** — 1,488 of 2,057 total blocks in the planned project areas — containing 28,689 residential units across 108 fully residential miles (subset of ~148 planned miles, of ~1,451 total remaining miles).

**Q.** What cost components did you include?

**A.** Upfront capital only: pipeline replacement (~~$4.96M/mi, sourced from Docket 24-0081); decommissioning (~$66K/mi, same source); single-family electrification (~~ $29K/unit, ComEd Whole Home Electrification Program); multi-family electrification (~$15K/unit, same source); grid upgrade ($209.74/peak kW, ~$944/household, E3 VDER in Illinois); scattershot baseline (30% of units electrify over 10 years, 5% discount rate, anchored to Chicago Climate Action Plan). Full table in **Ex. 2**.

**Q.** What did you exclude, and why is the analysis conservative?

**A.** Excluded operating costs, ongoing utility rate impacts, financing mechanisms, hydraulic feasibility (PGL has not released sufficient data to determine which sections of the low-pressure network are decommissionable as a unit), pipe lining/repair as a third pathway, and commercial/industrial parcels. All electrification costs are at-current; PRP cost growth (PGL forecasts 5.4% O&M growth vs. ~3% inflation) is not applied. Each exclusion biases the analysis **toward overstating the cost of electrification relative to PRP** — the findings are a lower bound on NPA savings.

**Q.** What three scenarios did you evaluate?

**A.** (1) **Block-level strict** — electrify a block only when its NPA cost ≤ its PRP cost. (2) **Portfolio cost-neutral** — rank blocks by NPA/PRP ratio, electrify in increasing order until cumulative net savings reach zero. (3) **Portfolio with scattershot** — compare NPA to PRP-with-scattershot (PRP cost + NPV of the scattershot electrification PGL is already implicitly relying on). Each scenario answers a progressively realistic version of the same question.

---

## IV. Finding 1 — Block-level strict cost-effectiveness

(Six-step affirmative-direct arc: problem → why it matters → remedy → analytical support → anticipate objections → recommendation.)

**Q.** Under a strict block-by-block comparison, how many residential blocks in PGL's planned PRP project areas could be electrified at or below the cost of pipeline replacement?

**A.** Establish the finding first: **approximately 23.5%** of fully residential blocks (350 of 1,488), affecting **3,558 residential units** (2,449 SF, 1,109 MF), avoiding **23.9 miles** of pipe replacement, with **~$28.2M in net upfront savings** ($90.3M NPA vs. $118.5M PRP for these 350 blocks). All quantitative claims hedged ("approximately," "roughly"). Reference **Ex. 3** for the histogram.

**Q.** Why does this finding matter?

**A.** Connects to ICC's existing mandates: cost-causation, just and reasonable rates, the SMP Investigation Order's leak-reduction objective, and the Commission's interest in keeping bills affordable as PGL acknowledges declining residential gas demand (~5% by 2027 per Eidukas). Even the most conservative scenario shows a non-trivial subset of in-scope blocks where the NPA path satisfies all four interests at lower cost.

**Q.** What do you recommend the Commission do with this finding?

**A.** Stub for §IX cross-reference: at minimum, require PGL to flag and exclude the strictly-cheaper-to-electrify blocks from PRP cost recovery in the test year unless PGL has demonstrated that NPAs are infeasible for those specific blocks.

**Q.** What analytical support backs this finding?

**A.** Walk through the cost comparison briefly; defer methodology detail to **Ex. 2**. Reference **Ex. 3** (histogram) — describe what the reader sees: a left tail of NPA/PRP ratios under 1.0 representing the 23.5% of blocks.

**Q.** Wouldn't this require coordinating electrification across every household on a block, which is not realistic?

**A.** Acknowledge: the 100%-participation assumption is a programmatic constraint, not a free assumption. Pivot: PGL itself proposes to tear up streets across these same blocks under PRP, which is also a coordination problem. The question is which coordinated investment the ratepayer is funding. Note PGL's existing list of NPA tools (geothermal, TE, CIPL).

**Q.** What is your recommendation on this scenario?

**A.** Re-state the §IX recommendation in one sentence; close.

---

## V. Finding 2 — Portfolio cost-neutral approach

**Q.** What if PGL took a portfolio rather than a block-by-block view of cost-neutrality?

**A.** Establish: under a cost-neutral portfolio approach — ranking blocks by NPA/PRP ratio and using savings from cheaper blocks to fund electrification on next-cheapest blocks until cumulative net savings cross zero — **approximately 55.2%** of fully residential blocks (821 of 1,488) could be electrified at no net additional cost compared to pipeline replacement. Reference **Ex. 4** (cumulative savings curve) and the updated histogram in **Ex. 3**.

**Q.** Why is this framing more appropriate than block-by-block?

**A.** PGL itself plans the PRP at the portfolio level (179 projects across the city, sized $1–3M to >$5M each per NSG-PGL Ex. 3.0 pp. 106–107). Project-level NPA evaluation is tractable for the larger jobs but carries prohibitive overhead for the smaller-project tail. Portfolio-level matching of cheap and expensive blocks — "banking the savings" — uses the same money PGL is asking ratepayers to fund and stretches it further.

**Q.** What do you recommend?

**A.** Stub for §IX: framework requirement that PGL evaluate cost-effectiveness of the PRP portfolio against an NPA portfolio, not project-by-project. **TK — JPV input on whether §IX includes specific framework-design detail (governance, evaluation cadence, who runs the screen) or defers to a separate Commission proceeding.**

**Q.** What does the cumulative savings curve show?

**A.** Walk the reader through **Ex. 4**: the curve is positive (savings) on the cheapest blocks, peaks near the cost-neutral crossover, and turns negative as expensive blocks are added. The crossover at 55.2% is the cost-neutrality breakpoint.

**Q.** Wouldn't using savings from cheap blocks to fund expensive ones constitute cross-subsidization?

**A.** Acknowledge the framing. Pivot: PGL's existing PRP cost recovery already pools costs across all blocks in base rates — every PRP customer subsidizes the most expensive miles regardless of where they live. The portfolio NPA is the same pooling logic applied to a cheaper portfolio.

**Q.** What is your recommendation on this scenario?

**A.** Re-state the §IX recommendation; close.

---

## VI. Finding 3 — Portfolio with scattershot baseline

**Q.** What is wrong with comparing NPA cost to PRP cost in isolation?

**A.** Establish the problem: the PRP-only baseline assumes nothing else changes — that the 30% of Chicago residential buildings the city expects to electrify by 2035 (Climate Action Plan) does not exist. In reality, ratepayers will pay twice on the same blocks: once for new pipe under PRP, again for uncoordinated household-by-household electrification. PGL itself acknowledges declining gas demand in this docket.

**Q.** What does your analysis find under a scattershot-aware comparison?

**A.** **Across the entire portfolio of 1,488 in-scope fully residential blocks, the total cost of coordinated targeted electrification is lower than the cost of PRP plus the scattershot electrification that would happen anyway.** At the block level, **approximately 60.1%** of blocks are individually cheaper to electrify under this comparison. Reference **Ex. 5** (total spending bar) and the updated histogram in **Ex. 3** and curve in **Ex. 4**.

**Q.** Why does this matter for the Commission?

**A.** This is the scenario that matches the actual world the rate case is asking the Commission to authorize spending in. PGL's revenue requirement already embeds shrinking demand (~5% residential decline by 2027 per Eidukas); the Commission is being asked to fund pipe in front of customers who are leaving the system anyway.

**Q.** Wouldn't a coordinated-NPA approach raise rates more than just replacing pipes, since the utility doesn't pay for the scattershot?

**A.** Acknowledge directly — under the current cost-recovery design, yes: PGL's ratepayers pay the PRP through base rates while individual customers pay for their own scattershot heat-pump installations. The two cost streams are not netted at the utility. The ~$200M aggregate gap is real but small relative to the $214M / $306M annual PRP ask, and there are several mechanisms — program design, bill-impact mitigation through Rider LIDA's 3% energy-burden floor, federal funding leveraging — that the Commission can apply. This is a design problem, not a fatal flaw.

**Q.** What is your recommendation on this scenario?

**A.** Stub for §IX: require PGL to use a scattershot-aware baseline in any NPA cost-effectiveness screen the Commission orders, not a PRP-only baseline.

---

## VII. What predicts whether a block is cost-effective to electrify?

**Q.** Across all three scenarios, what attribute most strongly predicts whether a block is cost-effective to electrify?

**A.** **Housing density** is the dominant predictor: lower-density single-family blocks and blocks with vacant lots are usually cheap to electrify; high-density multi-family blocks are usually expensive. Reference **Ex. 6** (scatter) and explain what the reader sees.

**Q.** Is this a real-world finding or an artifact of your model?

**A.** Both, and we are explicit about it. The model uses an average cost per mile to estimate PRP cost, and an average per-unit cost to estimate electrification cost — so the relationship between density and cost-effectiveness is partly mechanical. But the underlying drivers (more expensive electrification per parcel-mile in dense MF blocks; vacant lots costing nothing to electrify) are real. **Ex. 2** documents this caveat.

**Q.** What does this mean for prioritization?

**A.** Cost-effective blocks cluster in low-density single-family neighborhoods with vacant parcels. The first wave of NPA-eligible blocks is identifiable from public assessor data, before any building-level survey.

---

## VIII. Geographic implications across PGL's planned PRP project areas

**Q.** Does cost-effectiveness vary across PGL's planned project areas?

**A.** Yes. Reference **Ex. 7**: maps and a summary table contrasting three planned project areas.

**Q.** Please walk through the three example areas.

**A.** Three short paragraphs:

- **Lincoln Square** — high income / low share of cost-effective blocks (denser, more MF).
- **Garfield Ridge** — mid income / mid share (mixed SF/MF, more vacant parcels).
- **Englewood** — low income / high share (lower density, more SF and vacant parcels).

Anti-correlation between income and NPA cost-effectiveness is a finding worth surfacing on its own — it has direct implications for the Rider LIDA design PGL is proposing to align with the Ameren and Nicor orders.

**Q.** What does the geographic pattern imply for program design?

**A.** A first-tranche NPA pilot would land disproportionately in lower-income neighborhoods. That can be the right thing — those customers carry the highest energy burden and would benefit most from the operating-cost reduction of full electrification — but it requires program-design discipline (consent, equitable participation, no displacement). Stub for §IX cross-reference.

---

## IX. Summary of recommendations

**Q.** Please summarize your recommendations to the Commission.

**A.** **TK — JPV input on the recommendations slate.** Candidate items, to be confirmed:

1. Require PGL to evaluate NPAs at both block and portfolio level before authorizing PRP cost recovery for any block in the test year, using a scattershot-aware baseline.
2. Require PGL to publish, with each annual PRP filing, the share of in-scope residential blocks for which NPA cost is at or below PRP cost under each of the three scenarios analyzed here.
3. Require PGL to release the data necessary to assess hydraulic feasibility (which low-pressure network sections are decommissionable as a unit).
4. Direct PGL to coordinate NPA scoping with the City of Chicago's Climate Action Plan implementation, to avoid duplicative ratepayer-funded scattershot electrification.
5. **TK — JPV input** on whether to include framework-design detail (governance, evaluation cadence, who runs the screen, treatment of equity in block prioritization) or defer those to a separate Commission proceeding.

**Q.** Are these recommendations dependent on each other?

**A.** Stub: explain whether the recommendations are severable or stand as a package.

---

## X. Reservations

**Q.** Are there limitations on the conclusions in this testimony?

**A.** Re-state the conservative-bias scope; note the un-modeled pathways (lining/repair, hydraulic feasibility, commercial/industrial parcels); note that the analysis uses average rather than project-specific costs because PGL has not made project-specific cost data public; reserve the right to update findings if PGL's rebuttal puts new data on the record.

**Q.** Should your silence on any other issue in this proceeding be construed as agreement?

**A.** No (re-affirm silence-is-not-agreement disclaimer).

---

## Closing

**Q.** Does this conclude your direct testimony?

**A.** Yes, it does.

---

## Open items flagged in this draft

- **§ IX:** JPV to specify the recommendations slate.
- **§ IX:** JPV to decide whether framework-design detail belongs in this testimony or defers to a separate Commission proceeding.
