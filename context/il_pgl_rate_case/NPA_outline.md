## Introduction (~1-2 paragraphs)

This memo compares the upfront capital costs between the current PRP strategy and three different TE scenarios across PGL's planned project areas in Chicago.

**Problem:** There is an intrinsic conflict between Chicago's 2035 building-electrification goal (30% of residential buildings) and PGL's 2035 PRP goals (25% of pipes replaced).

**Questions:**

- Is there a cost-effective way to avoid leaks and meet electrification goals using heat pumps?
- What frameworks could the ICC adopt to make that happen?
- What's the potential scale of savings under each of these?

We modeled three different potential scenarios and got three different outcomes.

**OPEN QUESTION:** Do we need to name CUB and the testimony/evidence context of the memo explicitly?

## Executive Summary

In the fully residential blocks in PGL's PRP project areas, there is always an opportunity to save money with TE, and with good implementation, savings can scale across nearly the entire portfolio.

- **23.5% of blocks** (350 of 1,488) in planned PRP project areas could be electrified for less than or equal to the cost of pipeline replacement under a block-level NPA cost analysis.
- **55.2% of blocks** would be cheaper to electrify under a portfolio-level NPA cost analysis (cost-neutrality / "banking savings" where savings from cheaper blocks fund electrification of more expensive ones).
- **The entire portfolio of in-scope blocks is cheaper than the alternative** under a portfolio-level NPA cost analysis with scattershot electrification. Across all 1,488 fully residential blocks in scope, the total cost of targeted electrification stays below the cost of pipeline replacement plus the scattershot electrification that would happen anyway. At the block level, 60.1% of blocks are individually cheaper to electrify under this comparison.
- Taking the average cost per mile for pipeline replacement vs. the cost to electrify, **housing density is the best predictor** of block-level cost-effectiveness. Lower-density single-family blocks and blocks with vacant lots are usually cheap. High-density multi-family blocks are usually expensive.

## Background

Keep this short.

- Context of PRP
- Context of Chicago climate goals

## Scope and Assumptions

**Scope:**

- We looked at **1,488 fully residential blocks** out of 2,057 total blocks in planned PRP project areas. Commercial and industrial parcels excluded.
- These 1,488 blocks contain **28,689 residential units** (16,707 single-family parcels and 11,982 multi-family units).
- Total remaining PRP miles vs. planned mileage in mapped project areas vs. fully residential subset of that: **1,451 total remaining miles → 148 planned → 108 fully residential.**
  - **VISUALS:** 2-3 maps here showing the narrowing down.
- Only the upfront capital costs of TE vs. pipeline replacement.
- Defined cost-effectiveness narrowly.
  - Average cost per mile to replace pipes
  - Vs. Average cost to electrify the units on that block
- All residents assumed to participate vs. the real world.
- Current cost estimates only.
- So results are likely conservative.

## Findings

### (Block-level) How many residential blocks could be immediately electrified at or below the cost of pipeline replacement?

Simple cost comparison: is this block cheaper to electrify? Still better than not asking at all.

- **23.5% of fully residential blocks** (350 of 1,488).
- **3,558 residential units** affected (2,449 SF parcels, 1,109 MF units).
- **23.9 miles** of pipeline avoided.
- **\$28.2M in net savings** (NPA cost \$90.3M vs. PRP cost \$118.5M for these 350 blocks).

**VISUAL:** Histogram of number of blocks that save vs. cost more.

### (Portfolio-level) How many residential blocks could be electrified using a cost-neutral approach?

But you were already going to spend that money! What if you used it to further the city's TE goals?

This is also compatible with the ICC's own goals (TE, fixing leaks, keeping prices low for consumers). If we "bank" the savings from the cheapest blocks and use them to fund TE on the next-cheapest remaining blocks, we can do TE on **55.2% of fully residential blocks** at no net additional cost compared to pipeline replacement.

- 55.2% of fully residential blocks (821 blocks under the cumulative-saving curve where it first crosses zero).
- Some strategies for banking the savings.
- Numbers (blocks, residential units).

**VISUAL:** Updated histogram + cumulative savings curve.

### (Portfolio-level with scattershot) What if we combined strategic pipeline replacement with a "Total Cost" perspective?

Currently PGL pursues a risk-portfolio approach to pipeline replacement. It just replaces pipes that are risky without considering the full context of where they are.

- This is bad and not cost-effective.
- You don't take into account the fact that some households will adopt heat pumps, so you end up paying twice.

**Alternative approach:**

- Do system-wide planning for pipe replacement.
- Account for early adopters.
- ^^ would make it cheaper for 60% of blocks to adopt heat pumps.
- And then if you combine this with a portfolio-level view, cumulative savings are never less than zero! The whole project is cheaper.

**VISUALS:** Updated histogram + cumulative savings curve+ total spending bar

**Caveat:** on the face of it, this would raise rates more than just fixing pipes.

- Utility doesn't pay for the scattershot approach.
- Seemingly in conflict with ICC goals of keeping costs low.

But the difference isn't also crazy big (~\$200M); here are some ways you could handle it.

### What predicts whether a block is cost-effective to electrify?

- We don't have the actual costs of pipeline replacement so we use average cost/mile as a proxy.
- Then compare this to the average cost to electrify all the units on a residential block
- Using this model, density is the dominant predictor.
- Geographic details - lots of vacant lots and (less so) single-family homes.

**VISUALS:** Map of saving blocks under three scenarios and scatterplot of single- vs. multi-family residences.

### What does this mean for specific PRP project areas?

Certain neighborhoods are more affected / better candidates for TE.

- Lincoln Square (high income / low share)
  - **VISUAL:** Map
- Garfield Ridge (mid income / mid share)
  - **VISUAL:** Map
- Englewood (low income / high share)
  - **VISUAL:** Map
- Summary table of ^^

## Appendix

### Acknowledgments

Named people at CUB?

### Data and Methods

**Overview** (brief restatement of the comparison).

**What dataset was used?**

- PGL construction polygons, Census blocks, Cook County parcels, Chicago building footprints, Chicago street centerlines, cost estimates Google Sheet.

**What transformations were applied?**

- Here's how we filtered down the blocks.
- Here's how we did the cost comparison.
- Here's how we modeled the cost of electrification.
  - **Caveat:** Distribution costs were aggregated.
  - We used ComEd Whole Home Electrification Program data, which has limits.

**What assumptions were made (and why)?**

- Restate assumptions ^^ in more technical terms.
- Cost inputs from analysis.qmd:
  - Pipeline replacement: **~\$4.96M per mile** - _PGL Docket 24-0081, exhibit TK_
  - Decommissioning: **~\$66K per mile** - _PGL Docket 24-0081, exhibit TK_
  - Single-family electrification: **~\$29K per unit** - _ComEd Whole Home Electrification Program_
  - Multi-family electrification: **~\$15K per unit** - _ComEd Whole Home Electrification Program_
  - Grid upgrade: **\$209.74 per peak kW** (translates to ~\$944 per household) - _E3 VDER in Illinois_
  - Scattershot parameters: 30% of units electrify over 10 years, 5% discount rate - _Chicago Climate Action Plan, citation TK_

**What limitations apply?**

- Density is an artifact of how we set up the model. We use an average cost per mile to calculate pipeline replacement. We calculate cost to electrify a block by multiplying number of units times cost to electrify. So we have constructed that relationship ourselves
- We didn't model pipe lining/repair (cheaper than TE).
  - You could do lining/repair where possible and then TE on remaining units.
  - We didn't examine that scenario, but it's real.
- Hydraulic feasibility not modeled.
  - PGL has not released data sufficient to determine which sections of the low-pressure network are decommissionable as a unit.
