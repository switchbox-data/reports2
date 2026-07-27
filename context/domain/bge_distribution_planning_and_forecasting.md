# BGE distribution planning and forecasting: the machinery behind the 8760s we want

We want BGE's **forecasted 8760 hourly load profiles for each distribution
feeder and each substation transformer** — the baseline profiles and the
versions with distributed energy resource (DER), electric-vehicle (EV), and
electrification overlays — plus the ratings and constraint data that sit
underneath them. Those profiles are the natural input to a Bill Alignment
Test and to any analysis of whether winter heat-pump load actually drives
incremental distribution-capacity cost on BGE's system.

The good news, established below, is that **BGE already models exactly this**.
Its 2026 Annual Electric System Plan Update ("ASP") describes a forecasting
stack — LoadSEER, the new DER & LF System, and CYME — that produces
per-feeder and per-substation-transformer hourly forecasts as a matter of
course. The catch is that **the public filing discloses only
system/area-aggregate results.** The granular data exists; it simply isn't in
the document.

This doc has two jobs:

1. **Explain BGE's forecasting and planning machinery** in enough detail that
   we know precisely what data objects exist, what they are called, and how
   they are produced — so a discovery request can name them.
2. **Draft the discovery requests** to obtain the underlying per-feeder /
   per-transformer 8760s and the ratings/constraint data behind the aggregate
   counts, with the target dockets and the likely confidentiality posture for
   each.

It is a companion to two sibling docs. [`bge_tou_rates.md`](./bge_tou_rates.md)
covers the distribution-capacity-**deferral** debate — BGE's argument (in its
July 1, 2026 DRIVE Act report) that time-of-use rates can't defer distribution
capex but virtual power plants can — which is the _policy_ fight these load
profiles inform. [`md_drive_act_tou.md`](./md_drive_act_tou.md) covers the
DRIVE Act statutory architecture, the Case No. 9761 docket, and the July 2026
reporting obligations — the _procedural_ hooks the discovery requests hang on.

**Primary sources:**

- [`../sources/md_hp_rates/mdpuc_331109_bge_2026_annual_electric_system_plan_update.md`](../sources/md_hp_rates/mdpuc_331109_bge_2026_annual_electric_system_plan_update.md)
  — BGE's **2026 Annual Electric System Plan Update** (Case No. 9665, ML
  331109, June 12, 2026). The key source; page numbers below refer to it
  unless otherwise noted.
- [`../sources/md_hp_rates/mdpuc_9761_bge_drive_act_report.md`](../sources/md_hp_rates/mdpuc_9761_bge_drive_act_report.md)
  — BGE's **DRIVE Act Capital Deferral Potential July 1 Report** (Case No.
  9761, ML 331727, July 1, 2026). Source of the overload-MW quantification,
  duration analysis, and the firm/locational/dispatchable framing.
- [`rie_distribution_planning_and_thermal_screening.md`](./rie_distribution_planning_and_thermal_screening.md)
  — Rhode Island Energy's planning process. Used throughout as the comparison
  point (RIE's systematic thermal screen vs. BGE's criteria).

A note on how this doc flags certainty, following the convention in
`bge_tou_rates.md`: statements traceable to the ASP or the DRIVE report are
cited to a page or section; everything else is marked as an **inference** in
italics, and the [caveats](#whats-genuinely-unknown) section collects the
open questions.

---

## What BGE models vs. what it discloses — the whole point

Everything downstream turns on one distinction, so state it first.

**What BGE internally models (per the ASP):**

- Coincident **feeder-, substation-transformer-, and substation-level**
  forecasts (p. 9).
- **8760 hourly** load profiles, per feeder, weather-normalized (pp. 9–12).
  LoadSEER "support[s] 8760 hourly forecasting" and spatial load allocation
  (p. 10); the new DER & LF System overlays "DER generation and EV charging
  profiles onto baseline hourly feeder load profiles" (p. 12).
- A **15-year forecast** for every feeder, substation transformer, and
  substation (p. 7), feeding the **10-Year Distribution Capacity Plan**.
- Per-component **normal and emergency ratings** (summer and winter) and a
  flag for any component at/above 100% of its normal rating (p. 18).
- **Overload duration** and hourly loading profiles for constrained
  components — BGE does this explicitly in its non-wires-solution ("NWS")
  evaluations (p. 13) and in the DRIVE report's Duration Analysis
  (DRIVE report §5.2, Table 2) and Time-of-Day Analysis (§5.3, Table 3).

**What the ASP publicly discloses:**

- **Aggregate counts.** Table 11 (p. 45) reports the _number_ of forecasted
  feeder overloads (190) and substation-transformer overloads (33) per year,
  2027–2036 — and warns the counts "are not necessarily representative of
  unique feeders or transformers." Section 4 reports 291 total
  constraints and 112 planned projects by _type_ (Table 4, p. 25).
- **System-wide MW totals.** The DRIVE report adds that those overloads sum to
  **547 MW (feeders) + 393 MW (substations)** and bins them by duration — but
  again with no named component, no rating, no year-by-component detail
  (DRIVE report Tables 1–2).
- **A handful of named-asset anecdotes**, only where a specific NWS was
  deployed: the **Hereford Substation** 3 MW battery (BESS); the **Chesapeake**
  (1 MW / 2 MWh) and **Fairhaven** (2.5 MW / 9.74 MWh) BESS mitigating a
  **Marriott Hill 34 kV** winter post-contingency overload "of up to 3.5 MW"
  (pp. 24, 45).

So the gap is stark: **BGE holds per-feeder and per-transformer 8760s with
DER/EV overlays and knows exactly which components overload in which years by
how much — and publishes only rolled-up counts and MW totals.** No named
feeder or substation with an individual load, rating, or overload year; no
actual hourly time series or load-duration curve plotted at any granularity.

One more thing that matters for how we ask. **This is editorial aggregation,
not redaction.** There is _no_ confidentiality, Critical Energy Infrastructure
Information ("CEII"), redaction, or protective-order statement anywhere in the
ASP — the granular data is modeled but simply not included in the narrative
filing. The one place BGE says it _cannot_ produce something granular is the
**equity-stratified reliability metrics** (SAIDI/SAIFI by underserved
community), which it waived for good cause because "a methodology has not been
developed to determine how to map electric system infrastructure such as
feeders and substations to overburdened and underserved communities" (Section
7, p. 46). That is a **methodology gap, not a confidentiality claim** — and it
is a useful tell: BGE _can_ produce feeder- and substation-level data, it just
lacks a feeder→community crosswalk. The 8760s and ratings we want do not depend
on that crosswalk.

---

## Forecasting methodology, end to end

BGE's distribution planning cycle is an annual, four-phase process — **forecast
→ constraint identification → develop/evaluate solutions → 10-year prioritized
plan** — that kicks off in July and concludes around June (Table 1, p. 8). The
forecast phase is what produces the profiles we want. It runs top-down to
bottom-up in roughly five steps.

### 1. Top-down econometric forecast by customer class

BGE builds forecasts using **econometric regression and exponential-smoothing
models by customer class**, calibrated to revenue and rate classes in a
**top-down zonal and system model** (p. 9). Inputs are historical series from
**2000–2025** for sales, customers, demand, economics, prices, energy
efficiency, and solar; sales are weather-normalized using heating-degree-day
("HDD") and temperature-humidity-index-degree-day ("TDD") spline models with
lag and seasonality (p. 9). The 2025–2030 result: sales (MWh) and zonal peak
(MW) grow ~**1%/yr**, driven by data centers, large loads, and EV adoption
partly offset by efficiency; customer count grows ~**0.4%/yr** (p. 9).

### 2. Weather normalization → a 90th-percentile synthetic hourly year

Observed system loading is normalized to weather using ~**30 years of
historical data from the National Weather Service BWI station** (dry-bulb
temperature, humidity, wind speed). The normalization produces **"a synthetic
year of hourly loads analogous to a typical meteorological year"** that
**"represents the 90th percentile from the simulated distribution"** (p. 9).
This synthetic hourly year is the **base profile**; the rest of the forecast
adds to or subtracts from it to derive "the expected hourly forecast by year"
(p. 9).

> **Comparison to RIE.** RIE designs its peak forecast for a
> **1-in-20-year (95th-percentile) extreme-weather** condition
> (`rie_distribution_planning_and_thermal_screening.md`). BGE's stated basis is
> the **90th percentile** of its simulated distribution. These are not the same
> design standard, and the difference matters for any cross-utility comparison
> of headroom — worth confirming what "90th percentile" indexes (annual peak
> hour? each hour's distribution?) in discovery.

### 3. Spatial allocation to feeders and transformers (the DER & LF System)

The top-down class forecast is then **spatially allocated** across the system.
Historically BGE used an "internally developed forecasting application based
primarily on regression analysis of observed peak feeder and transformer
loading" — peak-only, with "limited capability to model hourly load behavior,
DER impacts, or spatial allocation" (p. 11). Beginning with the **2026 planning
cycle**, that is replaced by the **Distributed Energy Resources and Load
Forecasting ("DER & LF") System**, which:

- does **8760 hourly forecasting**;
- performs **spatial allocation of EV, PV, and load-growth projections** across
  the distribution system; and
- **overlays DER generation and managed/unmanaged EV-charging profiles onto
  baseline hourly feeder load profiles** to evaluate feeder and transformer
  loading (pp. 11–12).

This is the engine that produces the exact object we want: a baseline hourly
feeder profile plus DER, managed-EV, and unmanaged-EV overlays. Refinement of
"spatial allocation methodologies associated with EV, PV, and distributed load
growth projections" is listed as an ongoing development area (p. 12).

**Electrification is folded into a generic input, not broken out.** The
forecast incorporates "electrification impacts" alongside customer growth and
DER (p. 9), and EV adoption is an _explicit, separately named_ input (p. 10,
"EV adoption assumptions"). But **heat pumps / building electrification are not
called out as a distinct forecast driver** — they sit inside the general
"electrification impacts" term. _This is a notable gap for our purposes: BGE's
public methodology does not reveal a heat-pump adoption curve or a
winter-electrification load shape, even though its DER & LF System is clearly
capable of carrying one. (Inference from the absence of any heat-pump-specific
input in the ASP's forecast-input list, p. 10.)_

### 4. Power-flow validation (CYME)

**CYME** is BGE's power-flow tool "supporting feeder-level modeling" (p. 10).
_As in RIE's process, CYME is where a bulk feeder forecast becomes a
segment-aware circuit model; the ASP does not detail how the DER & LF System
hourly profiles feed CYME, but the two are the forecasting and power-flow
halves of the same pipeline. (Inference — the ASP lists both tools but does not
describe the handoff.)_

### 5. Supporting tools and data inputs

- **Inputs** (p. 10): SCADA data, AMI data, NWS BWI weather, known customer
  growth, DER interconnection information, EV adoption assumptions, economic
  development projects, planned load/system transfers, planned capital
  projects, corporate residential/commercial growth assumptions, and GIS/
  spatial data.
- **Tools** (p. 10): **LoadSEER** (8760 forecasting + spatial allocation + load
  planning management); **CYME** (power flow); **IntellioConnect** (new-business
  / interconnection management); **Power BI** dashboards (visualization,
  reporting, forecast assessment); hosting-capacity and restricted-circuit maps.
- **Outputs** (p. 10): feeder-, substation-transformer-, and substation-level
  constraints; hosting-capacity analyses; EV/load capacity assessments;
  seasonal summer and winter loading forecasts; and identified system
  constraints/overloads.

_LoadSEER and the "DER & LF System" appear to be the same platform (or the
DER & LF System is the DER/EV-overlay layer built on LoadSEER): the ASP uses
both names for 8760 hourly forecasting and spatial allocation and even
attributes the EV/PV overlay to "LoadSEER capabilities" on p. 13. Worth
clarifying in discovery which system of record holds the profiles. (Inference
from overlapping descriptions on pp. 10–13.)_

### Forecast accuracy check

BGE reports a short-term forecast-accuracy metric: it counts feeders/
transformers forecast to be at ≥90% of rating (or observed at ≥90% where
forecast and observed differ by more than ±10%), divided by total components.
Its most recent result shows deviation on **2.2%** of impacted components
(p. 43). _This metric's very definition confirms BGE holds per-component
forecast-vs-observed loading at the ≥90%-of-rating threshold — i.e., exactly
the component-level ratings-relative loading data we would request._

---

## Overload definitions and planning criteria

BGE's criteria (Section 2, pp. 18–20) define what "constraint" and "overload"
mean and are the semantic key to any ratings request.

### Thermal criteria — the N-0 flag

Each major component carries a **normal rating** ("maximum permitted loading
… under normal operating conditions," accounting for daily load cycles and
seasonal ambient temperature) and an **emergency rating** ("maximum permitted
loading … for a 24-hour time interval" during a contingency) (p. 18).

The screening rule is a simple **N-0 thermal flag**:

> "Any feeder or substation transformer which is at or above **100% of either
> its summer or winter normal rating** is flagged for further analysis to
> develop remediation." (p. 18)

So a **forecasted overload** = the 15-year forecast puts a component's loading
at ≥100% of its summer _or_ winter normal rating in some year. This is the
definition behind Table 11's counts and the DRIVE report's MW totals. Note it
is explicitly **bi-seasonal** — winter loading is screened on equal footing
with summer, which is directly relevant to heat-pump-driven winter peaks.

> **Comparison to RIE.** RIE's Criterion 1 is the same idea — peak (or
> forecast peak within the horizon) vs. normal rating — but in _practice_ RIE
> screens **summer peaks only** and does not expect winter to bind until the
> late 2030s/2040s
> (`rie_distribution_planning_and_thermal_screening.md`). BGE's criterion is
> **symmetric across summer and winter on paper**, which is a meaningfully
> better starting point for a winter-electrification argument — _if_ the winter
> ratings and winter-hour forecasts are actually produced (they are, per the
> DRIVE report's winter overload findings).

### Contingency criteria — N-1, but case-by-case

For **feeders**, BGE's design "sectionalizes a feeder into three equally loaded
segments" via automated switches; under an N-1 fault the design "relies on a
neighboring feeder's emergency rating to accommodate one segment of its load"
(p. 19). Crucially:

> "**Current practice does not include system-wide assessments of this design
> practice; rather, analyses are carried out on a case-by-case basis** depending
> on specific project or system conditions." (p. 19)

For **substation transformers**, contingency capability is a _classification_,
not a per-event screen:

- **Firm** — withstands full N-1 loss of the largest transformer; ~**50%** of
  substations are Firm, and BGE analyzes Firm substations to confirm they
  remain Firm under future load.
- **Semi-Firm** — has a transfer scheme that restricts transfer if it would
  create an overload; only **13** substations.
- **Non-Firm** — lacks a transfer scheme or sufficient capacity, or is a
  single-transformer station; the remainder (p. 19).

> **Comparison to RIE.** This is the sharpest contrast in the whole document.
> RIE runs a **systematic, year-by-year N-1 "load-at-risk" screen** across every
> feeder — computing MWh at risk against explicit thresholds (16 MWh feeder;
> 240 MWh transformer/sub-transmission), driven by manual GIS tie-lists and a
> spreadsheet transfer to neighbors' emergency ratings
> (`rie_distribution_planning_and_thermal_screening.md`). **BGE does not run a
> system-wide feeder N-1 screen at all** — it does feeder contingency analysis
> "case-by-case," and reduces substation contingency to a three-bucket Firm/
> Semi-Firm/Non-Firm classification. So BGE's _published_ constraint counts
> (Table 11) are essentially **thermal N-0** results; the N-1 story lives in
> scattered case studies, not a screen. This means our ask for "the N-1 studies"
> is really an ask for a _set of individual case analyses_, not one screening
> table — phrase it accordingly.

### Other criteria

- **Voltage:** ANSI C84.1, **0.95–1.05 per unit** on ~12,300 circuit miles of
  34.5 kV / 13.2 kV / 4.16 kV line (p. 18).
- **Current imbalance:** target max **10%** between any two phases; flagged
  semi-annually (p. 19).
- **Power factor:** target **unity** on the high side of substation
  transformers, achieved with capacitor banks (p. 20).

### Duration of overload — done for NWS, not as a general criterion

BGE's _planning_ criteria are the thermal/voltage/contingency thresholds above.
**Duration-of-overload analysis is not a general planning criterion** — it
appears only in the NWS/deferral context. NWS evaluations "assess … hourly
feeder and station loading profiles, seasonal peak loading conditions, required
MW and MWh load relief, **overload duration**, and recharge capability" (p. 13).
The DRIVE report then generalizes this to the whole constraint set, defining
duration as "the maximum number of hours a component is projected to operate
above its design rating on any single day within the 10-year planning horizon"
and binning every overload MW into 1–6+ hour buckets (DRIVE report §5.2). The
finding — ~**90%** of overload MW is 6+ hours (494.2 of 547 feeder MW; 342.5 of
393 substation MW), only ~**10%** is ≤5 hours — is the crux of BGE's TOU-vs-VPP
argument (see [`bge_tou_rates.md`](./bge_tou_rates.md), Part 7). For us, the
point is narrower: **BGE can and does compute per-component hours-above-rating
and load-duration curves** — it just publishes them only in aggregate.

---

## How the forecast feeds capital planning and deferral

The forecast doesn't sit on a shelf; it drives a governed capital pipeline.

**From constraint to project.** The forecast identifies constraints; BGE then
develops conceptual solutions and iterates them into the 10-Year Distribution
Capacity Plan (Section 4, p. 24). In the latest cycle: **291 constraints → 112
projects** (Table 4, p. 25), where project types run from new substations and
feeders to 23 energy-storage projects. **Load transfers are the first
mitigation tried** — "low-cost solutions to leverage existing capacity on
adjacent feeders and substations … the first option investigated" (p. 24); of
28 remediations completed in 2025, **24 were load transfers** (13 summer, 11
winter) (pp. 24, 44).

**Governance.** Projects run through a structured **Project Authorization
Process**: the **Asset Investment Committee ("AIC")** evaluates technical
solutions/alternatives, and the **Project Review Committee ("PRC")** validates
financial assumptions and funding (pp. 16–17). Reliability Planning and
Capacity Planning coordinate to avoid redundant investment.

**NWS trigger and framing.** Every capacity-driven project **above ~`$500k`**
gets an NWS assessment (p. 13). To date NWS work has focused on utility-owned
**BESS** (standardized 1 MW / 2 MWh and 1 MW / 4 MWh units), compared against
traditional infrastructure using the hourly-loading / MW-MWh-relief / duration /
recharge analysis noted above (p. 13). Two NWS have gone live — the Hereford
BESS and the Chesapeake+Fairhaven pair — and the DBESS program is slated for
**22 other constraints** in conceptual stages (pp. 24, 45).

**Tie to the deferral debate.** This is where BGE's July 1, 2026 DRIVE report
picks up: BGE argues the ~90% long-duration majority of overloads needs a wires
(or not-yet-viable storage) solution, that only the ~10% short-duration slice
is NWS-addressable, and that within that slice **dispatchable, locational,
firm** resources (VPPs, DR, storage) beat behavioral TOU — which it rates
"Poor" scalability / "Low" locational signal (DRIVE report Table 4). The full
argument, and BGE's revealed preference to earn a WACC return on VPP deferral,
is in [`bge_tou_rates.md`](./bge_tou_rates.md), Parts 7–8. **The load profiles
we are requesting are the evidentiary substrate for that whole debate** — they
let an intervenor independently test the duration/timing claims and, separately,
run a heat-pump cross-subsidy analysis.

**Filing cadence** (the discovery calendar). BGE files **Annual Plan Updates**
now; its **Preliminary ESP is due June 2027**; and an **August 2026 Technical
Conference** on this ASP is the near-term venue (ASP Introduction, p. 4;
`md_drive_act_tou.md`). The DRIVE VPP/V2G/TOU pilot targets the Commission's
**2% peak-reduction goal** (DRIVE report; ASP p. 28).

---

## Discovery requests

Below are concrete, numbered data requests, phrased the way regulatory data
requests are written. They target the objects named above by their BGE names
(LoadSEER / DER & LF System / CYME; normal and emergency ratings; Firm/Semi-
Firm/Non-Firm) so BGE cannot claim it doesn't know what is being asked for.

**Where to serve them.** Two live proceedings are the natural homes:

- **Case No. 9665** (Electric System Planning for Maryland Electric Utilities)
  — the docket for this ASP (ML 331109). The **August 2026 Technical
  Conference** and the **Preliminary ESP due June 2027** are the procedural
  openings; COMAR 20.50.15 also gives stakeholders a "discrete opportunity" to
  comment on BGE's Electric System Plan data sources and assumptions (ASP
  Section 5, p. 39). This is the cleanest home for the forecasting/ratings
  requests because BGE's ESP obligation _is_ to describe this machinery.
- **Case No. 9761** (DRIVE Act Implementation) — where BGE filed its **July 1,
  2026 Capital Deferral Report** (ML 331727) and where the Commission opened a
  **comment period on July 14, 2026** (ML 332115). This is the home for
  requests that go behind the DRIVE report's aggregate MW/duration tables,
  because BGE put those numbers at issue there. The common-metrics orders that
  scoped that report — **Order No. 92158** (ML 326582) and **Order No. 92422**
  (ML 330633) — are the hook: they _asked_ BGE for constraint-level detail, and
  BGE declined to provide some of it (see DR-7). **Public Conference 77** (ML
  327574) is a secondary venue for the program-inventory side.

**Confidentiality posture.** BGE has **not** marked any of this data CEII or
confidential in the ASP — the granular data is modeled but simply omitted from
the narrative (see [above](#what-bge-models-vs-what-it-discloses--the-whole-point)).
That said, per-feeder / per-substation loads, ratings, and locations are
routinely produced under a **protective order and/or CEII designation** in
utility proceedings. So each request should **offer to accept the data under
the applicable protective order or CEII procedures**, which removes BGE's most
plausible objection and shifts the fight (if any) to burden, not confidentiality.
_(Maryland has no bespoke CEII rule cited in these sources; the standard PSC
protective-order practice applies. Inference — confirm the operative protective
order in the chosen docket with counsel.)_

**How to justify the asks.** Tie every request to (a) BGE's **COMAR 20.50.15
ESP obligation** to describe its forecasting/planning processes and constraints
(the ASP is literally the response to that regulation), and (b) the **DRIVE Act
July 1 reporting obligation** and the **2% peak-reduction goal** — BGE itself
grounded its deferral report in this ASP's forecast, so the underlying
component-level data is squarely relevant to testing that report. Where a
request goes behind a DRIVE-report table, cite **Order No. 92422**'s
constraint-level metrics (projected peak exceedance, overload duration,
time-of-day distribution) as the Commission-endorsed level of granularity.

---

### DR-1 — Per-feeder and per-transformer forecasted 8760 hourly load profiles

For each distribution feeder and each substation transformer on BGE's system,
produce the **forecasted 8760 hourly load profile** for each year of the
current planning horizon (the 15-year forecast and/or the 2027–2036 window
underlying Table 11 of the ASP), in **machine-readable form (CSV or Parquet)**,
keyed by **feeder ID and substation-transformer ID**. Produce:

- (a) the **baseline** hourly profile (the weather-normalized synthetic-year
  profile per ASP p. 9), and
- (b) each **overlay/scenario** profile the DER & LF System generates — with
  DER generation, **managed** EV charging, and **unmanaged** EV charging, and
  with electrification impacts (ASP pp. 11–12) — identifying which drivers are
  included in each profile.

_Target:_ Case No. 9665 (ESP data-source/assumptions comment opportunity, or
Technical Conference discovery). _Justification:_ COMAR 20.50.15 ESP process;
these are the "coincident feeder, substation transformer, and substation level
forecasts using weather-normalized hourly load profiles" BGE describes at p. 9.
_Confidentiality:_ offer to accept under protective order / CEII.

### DR-2 — Component ratings and the data behind Table 11's counts

For each feeder and each substation transformer, produce:

- (a) **summer and winter normal ratings** and **summer and winter emergency
  ratings** (ASP p. 18), in machine-readable form keyed by component ID;
- (b) the **forecasted year(s)** in which the component reaches ≥100% of its
  summer or winter normal rating (i.e., the per-component detail underlying the
  190 feeder / 33 substation-transformer overload counts in **Table 11**, p.
  45), and the **magnitude** of each exceedance (forecast load in MW/MVA and as
  a percent of rating); and
- (c) a mapping showing which forecasted overloads correspond to which of the
  **291 constraints** and **112 planned projects** in Section 4 / Table 4.

_Target:_ Case No. 9665 (primary); Case No. 9761 (the 547 MW / 393 MW totals in
the DRIVE report derive from these). _Justification:_ Table 11 states its counts
"are not necessarily representative of unique feeders or transformers" — the
per-component data is required to interpret them. _Confidentiality:_ protective
order / CEII.

### DR-3 — LoadSEER / DER & LF System spatial-allocation factors and assumptions

Produce the **spatial-allocation factors and modeling assumptions** used by
LoadSEER and the DER & LF System (ASP pp. 10–12) to allocate the top-down class
forecast to individual feeders and transformers, including:

- (a) **EV adoption curves**, separately for **managed** vs. **unmanaged**
  charging, and the charging load shapes applied;
- (b) **DER/PV growth** assumptions and generation profiles;
- (c) **electrification / heat-pump** adoption assumptions and load shapes
  (identify separately whether heat-pump load is modeled distinctly or subsumed
  in a generic "electrification impacts" input — ASP p. 9); and
- (d) the **weather-normalization basis**, including the derivation of the
  **90th-percentile synthetic hourly year** from ~30 years of NWS BWI data
  (ASP p. 9): what the 90th percentile indexes, and the HDD/TDD spline
  specification.

_Target:_ Case No. 9665. _Justification:_ COMAR 20.50.15 requires a description
of forecasting processes and assumptions; the ASP describes these capabilities
but not their numeric assumptions. _Confidentiality:_ mostly non-sensitive
methodology; offer protective order only for any component-keyed allocation
factors.

### DR-4 — Load-duration curves / hours-above-rating for overloaded components

For each forecasted overloaded feeder and substation transformer, produce the
**load-duration curve** and the **hours-above-rating** profile (the
"overload duration" analysis BGE performs for NWS evaluation, ASP p. 13, and
generalized in the DRIVE report §5.2, Table 2), keyed by component ID and year,
including the **worst-day hourly loading profile** and the **season** (summer
vs. winter) in which the exceedance occurs. Produce the component-level data
underlying the DRIVE report's duration bins (1–6+ hours) and Time-of-Day
Analysis (§5.3, Table 3), not just the aggregate MW totals.

_Target:_ Case No. 9761 (behind the DRIVE report's Tables 2–3) and Case No.
9665. _Justification:_ Order No. 92422 asked for per-constraint overload
duration and time-of-day distribution; this is the component-level basis.
_Confidentiality:_ protective order / CEII.

### DR-5 — Case-by-case feeder N-1 studies

Produce all **feeder N-1 contingency studies** BGE has performed (ASP p. 19
states feeder N-1 is done "case-by-case," not system-wide), including, for each
study: the feeder(s) analyzed, the assumed contingency, the neighboring feeders
and tie configuration relied upon, the emergency ratings applied, the
resulting load-at-risk or post-contingency loading, and the study date. If BGE
has **not** performed a system-wide feeder N-1 screen, so state, and identify
the criteria BGE uses to decide _which_ feeders receive a case-by-case study.

_Target:_ Case No. 9665. _Justification:_ Section 2 contingency-planning
criteria. _Confidentiality:_ protective order / CEII.

### DR-6 — Firm / Semi-Firm / Non-Firm substation classification

Produce the **Firm / Semi-Firm / Non-Firm classification for every substation**
(ASP p. 19: ~50% Firm; 13 Semi-Firm), keyed by substation, including the
largest-transformer size and the transfer-scheme capability that supports each
classification, and BGE's analysis confirming that **Firm** substations remain
Firm under the future (15-year) load forecast.

_Target:_ Case No. 9665. _Justification:_ Section 2 contingency criteria and
the 15-year forecast. _Confidentiality:_ protective order / CEII.

### DR-7 — The constraint-level NWS/deferral metric BGE excluded

In its July 1, 2026 Capital Deferral Report, BGE **excluded** the Order No.
92422 metric requiring, per constraint, the "peak load reduction potential of
… the distribution programs an IOU has assessed as possible non-wires
solutions," stating it "does not currently evaluate demand-side program impacts
at the individual constraint level" (DRIVE report; see
[`bge_tou_rates.md`](./bge_tou_rates.md), Part 7). Request that BGE either
(a) produce any constraint-level NWS / peak-reduction analysis it _does_ hold,
or (b) confirm on the record that no such component-level analysis exists and
describe what would be required to produce it. Separately, request the
**per-component NWS screening inputs** (hourly loading profile, required MW/MWh
relief, recharge requirements) for every constraint that has undergone an NWS
assessment (ASP p. 13), not only the three deployed BESS projects.

_Target:_ Case No. 9761 (this is where BGE made the exclusion) and PC 77 (ML
327574) for the program-inventory side. _Justification:_ Order No. 92422
squarely requested this; the exclusion is BGE's choice, not a data limitation.
_Confidentiality:_ protective order / CEII.

### DR-8 — Data format and system-of-record clarification

Ask BGE to identify the **system of record** for the forecasted hourly profiles
(LoadSEER vs. the DER & LF System vs. CYME — the ASP uses these names somewhat
interchangeably, pp. 10–13), and to confirm it can export the DR-1/DR-4 data
directly from that system in bulk machine-readable form. This forecloses a
"data exists only in dashboards" objection and pins down the export path.

_Target:_ whichever docket carries DR-1. _Justification:_ efficiency; avoids a
burden objection. _Confidentiality:_ n/a.

---

## What's genuinely unknown

Flagging inferences vs. knowns, per the `bge_tou_rates.md` convention.

- **Whether heat-pump load is a distinct forecast driver.** _Inferred_ to be
  subsumed in a generic "electrification impacts" input (ASP p. 9 lists
  "electrification impacts" and, separately, "EV adoption assumptions," but no
  heat-pump-specific input on p. 10). DR-3(c) is designed to resolve this. If
  BGE does not break out heat pumps, its winter overload forecast may understate
  or misshape heat-pump-driven load — a substantive analytic point, not just a
  data gap.
- **What "90th percentile" indexes.** The ASP says the synthetic hourly year
  "represents the 90th percentile from the simulated distribution" (p. 9) but
  not the 90th percentile _of what_ (annual peak? each hour's distribution?
  degree-days?). This differs from RIE's 1-in-20 (95th-percentile) basis;
  DR-3(d) targets it. _Known:_ the ~30-year BWI basis and the HDD/TDD spline
  approach.
- **LoadSEER vs. DER & LF System.** _Inferred_ to be one platform (or the
  DER & LF System is the overlay layer on LoadSEER), from overlapping
  descriptions (pp. 10–13); DR-8 confirms.
- **How the DER & LF System hourly profiles feed CYME.** _Inferred_ to be the
  forecasting→power-flow handoff; the ASP names both tools but not the interface.
- **Whether a system-wide feeder N-1 screen exists.** _Known:_ the ASP says
  feeder N-1 is "case-by-case" and "does not include system-wide assessments"
  (p. 19). DR-5(final clause) confirms the negative and asks how feeders are
  selected for study.
- **Confidentiality treatment on production.** _Known:_ nothing in the ASP is
  marked CEII/confidential, and the ASP is entirely aggregate. _Inferred:_ if
  BGE produces component-level data, it will likely designate it under a
  protective order / CEII — hence the standing offer to accept it that way. The
  operative protective order in Case 9665 / 9761 should be confirmed with
  counsel.
- **Table 11 double-counting.** _Known:_ BGE states the counts "are not
  necessarily representative of unique feeders or transformers" and that "some
  constraints [are] counted in multiple years" (p. 45). So the 190/33 totals are
  _constraint-years_, not unique components; DR-2 resolves the true unique count.
- **The equity-stratification waiver is not a confidentiality precedent.**
  _Known:_ BGE waived SAIDI/SAIFI-by-community metrics for lack of a
  feeder→community mapping _methodology_ (Section 7, p. 46) — a methodology gap,
  not a refusal to disclose feeder data. Do not let BGE conflate the two in
  response to DR-1/DR-2.
