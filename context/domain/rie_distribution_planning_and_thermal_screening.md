# RIE distribution planning: thermal screening and area studies

Rhode Island Energy's Distribution Planning department is responsible for
keeping the distribution system — feeders, substation transformers, and
sub-transmission lines — reliable and within operating limits. When equipment
is overloaded, or when a single failure would leave too many customers without
power, the system needs investment: upgraded conductors, new feeders, new
substations, or non-wires alternatives like demand response and energy
storage.

This document explains RIE's two-stage process for identifying those needs
and acting on them:

1. **Annual screening** — A system-wide check of every component against
   thermal loading criteria. This is the first-order filter that flags
   components for deeper analysis. It is the focus of this document both
   because we are interested in distribution capacity constraints (and when
   heat pump load growth might trigger them), and because the screening is the
   structured, quantitative step that determines what enters the planning
   pipeline.

2. **Integrated Area Studies** — Deep engineering investigations of flagged
   areas, evaluating not just thermal loading but also voltage, reliability,
   asset condition, and other concerns. These studies produce the capital
   project recommendations that ultimately get funded.

The screening identifies problems; the area study diagnoses root causes,
develops solutions, and gets them approved and funded.

**Primary sources:**

- `context/sources/rie_distribution_planning_guide.md` — The planning
  criteria document (Feb 2011). Defines equipment ratings, N-1 contingency
  rules, load-at-risk thresholds, and project prioritization.
- `context/sources/rie_distribution_planning_study_process.md` — The
  integrated planning study process (Nov 2020). Defines annual screening,
  area study milestones, stakeholder consultation, and documentation
  requirements.
- Call with Ryan Constable (RIE Distribution Planning engineer), Mar 19 2026.
  Clarified how the screening is actually performed in practice — what data
  they have, what tools they use, and what simplifying assumptions they make.

---

## Annual screening: how thermal loading violations are identified

The Distribution Planning team runs an annual screening across all feeders,
substation transformers, and sub-transmission lines. For each component, the
screening checks whether it violates either of two thermal loading criteria.
Components that violate a criterion are flagged and enter the planning
pipeline for an area study — the process that ultimately produces funded
infrastructure projects.

### Criterion 1: Normal rating exceedance

Does the component's peak load exceed its **normal (continuous) rating**?

The planning guide states this plainly for each equipment type:

- "A distribution feeder circuit will not be loaded above its normal rating
  during non-contingency operating periods." (Section 2.2.4.1)
- "A substation transformer will not be loaded above its Normal rating during
  non-contingency operating periods." (Section 2.2.2.1)
- "A sub-transmission supply line will not be loaded above its normal rating
  during non-contingency operating periods." (Section 2.2.3.1)

If the peak exceeds the normal rating — or if the load forecast says it will
within the study horizon (typically 15 years) — the component is flagged.

**In practice** (from the call): the screening is run against summer peaks.
Winter peaks are not screened today; RIE does not expect winter peaks to drive
constraints until the late 2030s or 2040s given current heat pump adoption
forecasts.

### Criterion 2: N-1 contingency load at risk

If the component goes down entirely, is the resulting **load at risk** above
the MWh threshold?

This is the more complex criterion. The planning guide defines N-1
contingency rules for each equipment type (Sections 2.2.2.2, 2.2.3.2,
2.2.4.2). For feeders, the rule is:

> If more than 16 MWHrs of load is at risk at peak load periods for a single
> feeder fault, alternatives to eliminate or significantly reduce this risk
> shall be evaluated. (Section 2.2.4.2)

The MWh thresholds by equipment type are:

| Equipment              | MWh-at-risk threshold |
| ---------------------- | --------------------- |
| Feeder                 | 16 MWh                |
| Substation transformer | 240 MWh               |
| Sub-transmission line  | 240 MWh               |

The screening also flags components that are **borderline** (within 80% of
the threshold), though only components that actually exceed the threshold
enter the planning pipeline for area studies. (From the call: "the yeses go
into our plan.")

#### Two sources of "load at risk"

When a feeder goes down, load at risk — the load that can't be served — can
arise from two distinct causes. To build intuition, consider a simple feeder
with three segments:

```text
                  Segment A        Segment B        Segment C
[Substation] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                       │                                  │
                   tie to F2                           tie to F3
```

Segments A and B are connected to neighbor F2 via a tie switch. Segment C is
connected to neighbor F3. Now suppose the feeder's breaker at the substation
trips, de-energizing all three segments.

**Load at risk by topology.** Suppose Segment B has no tie switch to any
neighbor. Even if F2 and F3 have unlimited spare capacity, Segment B's
customers simply can't be reached — there's no physical path to re-energize
them. Their load is at risk purely because of the feeder's topology: a dead
end with no tie.

**Load at risk by thermal limits.** Suppose every segment does have a tie,
but the neighbor feeders are already heavily loaded. F2 is carrying 8 MW
against a 10 MW emergency rating, so it can only absorb 2 MW from Segment A.
If Segment A has 3 MW of load, the remaining 1 MW is at risk — not because
it's unreachable, but because F2 would exceed its emergency rating.

In reality, both sources contribute to the total load at risk. However,
**at the screening level, only load at risk by thermal limits is
calculated.** Conversations with RIE engineers (Ryan Constable, Mar 2026)
made this clear: the screening treats each feeder as a single bulk load
number, identifies which neighbor feeders are tied to it (by manually
searching GIS maps), and does a spreadsheet transfer of the downed feeder's
total load to its neighbors up to their emergency ratings. It does not model
the internal segment-level topology of the downed feeder. Load at risk by
topology — unreachable segments — may be considered during the deeper area
study, where engineers use CYME load flow software and examine section-level
faults.

#### How the screening calculates load at risk (thermal limits only)

The planning guide defines the concept of load at risk but not the mechanical
screening procedure. Ryan Constable described the screening-level calculation
for feeders:

1. **Identify ties.** Engineers manually search GIS maps to find all tie
   switches connecting the feeder to neighboring feeders. This is labor
   intensive — "there's a lot of sifting through maps and geographic stuff to
   find the ties." There is no automated topology model (like OpenDSS) at this
   stage.

2. **Build a tie list.** For each feeder, list its neighbors: e.g., F1 ties
   to F2 and F3. A feeder might have 2, 3, or 5 ties.

3. **Assume total feeder loss.** The screening always assumes the entire
   feeder goes down (fault at the breaker). Segment-level faults are only
   analyzed in the deeper area study.

4. **Mathematical load transfer.** In a spreadsheet, transfer the downed
   feeder's load to its neighbors, up to each neighbor's **24-hour emergency
   (LTE) rating** minus its current load. This is a bulk calculation — the
   downed feeder's total load is treated as a single number, not
   segment-by-segment.

5. **Remaining load = load at risk.** Whatever the neighbors can't absorb
   (because they'd exceed their emergency ratings) is the load at risk, in MW.

6. **Convert to MWh.** Multiply load at risk (MW) by assumed repair time.
   For feeders, the assumed repair time is **4 hours**. (From the call:
   "assume to four hour repair.") So the 16 MWh threshold at 4 hours implies
   a trigger of roughly **4 MW of unservable load**.

7. **Check threshold.** If MWh at risk > 16 for feeders (or > 240 for
   transformers/sub-transmission lines), the component is flagged.

**Why this matters for understanding constraints:** a feeder can be flagged
even if its own peak load is well within its normal rating. The problem may be
that its neighbors are heavily loaded, so if _it_ goes down, there's no
headroom to absorb its load. Ryan's example of the Johnston station
illustrated this: several feeders in the area all have high loading, so when
any one goes down, the others can't absorb the load — a thermal capacity
problem driven by the area's aggregate loading, not any single feeder's
individual peak.

#### Year-by-year and forecast

The screening must be run year by year with the load forecast applied,
because the contingency result depends on the loading of both the downed
feeder _and_ its neighbors in a given year. There is no shortcut — "you got
to do each year independently." The load forecast includes adjustments for
energy efficiency, distributed generation, EVs, heat electrification, and
system reconfigurations (feeder upgrades, voltage conversions, load
rebalancing).

Some feeders show dramatically different growth rates than the system average
because of planned construction: 4 kV to 12 kV conversions, feeder
retirements, load transfers to new feeders. These are real operational
changes, not customer growth — "there's no customers going away... it's the
system being reconfigured."

### Screening data and tooling

The screening is not done with power system simulation software. It is a
manual, spreadsheet-based process that relies on three main data inputs.
(All details in this section are from the call unless otherwise noted.)

**SCADA data from PI Historian.** Real-time load measurements for each feeder,
transformer, and supply line are recorded by SCADA (Supervisory Control and
Data Acquisition) systems and stored in OSIsoft PI Historian. To find peaks
for the screening, engineers must extract the PI data and then manually scrub
each feeder's load history. The scrubbing is necessary because the raw data
contains anomalies — switching events, maintenance outages, data dropouts,
instrument errors — that do not represent true customer load. There is no
single discrete set of anomalies that can be filtered automatically;
engineers use scripting tools to speed things up, but each feeder ultimately
requires manual review. This pre-processing step is the bottleneck: producing
clean historical peaks for four years of data across all feeders "takes all
the time." Once clean peaks exist, applying the load forecast and running the
contingency calculations is "fairly straightforward and easy — just simple
equations."

**GIS maps.** Engineers identify feeder ties by visually searching GIS maps
to find normally-open tie switches between feeders. This is the only source
of feeder interconnection data at the screening level. There is no automated
topology model of the distribution system (no OpenDSS, no circuit model with
segment-level connectivity). The GIS search is labor intensive — "there's a
lot of sifting through maps and geographic stuff to find the ties" — and the
result is a simple list: F1 ties to F2 and F3.

**Load forecast.** A regional econometric regression model that considers
historic loading, weather conditions, and economic indicators, adjusted for
known spot load additions and DSM forecasts (planning guide, Section 2.2.1.1).
The forecast is designed for a 1-in-20-year extreme weather scenario. As of
the 2020 study process update, the forecast incorporates separate inputs for
base load, energy efficiency, distributed generation, EVs, heat
electrification, demand response, and energy storage. See
`context/sources/rie_2024_peak_forecast_2025-2039.md` for the 2024 edition
of the 15-year peak forecast and its scenario assumptions.

**The spreadsheet.** With clean peaks, a tie list, and a forecast in hand,
the screening calculations are done in Excel. For criterion 1, this is a
simple comparison: peak load vs. normal rating. For criterion 2, the
spreadsheet transfers the downed feeder's total load to its neighbors up to
their emergency ratings and computes the MWh at risk. The whole screening
produces a table with one row per component and columns for current peak,
normal rating, contingency load at risk, and a yes/borderline/no flag.

**What the screening does NOT have:**

- No segment-level feeder topology (which customers are on which segment,
  where tie switches connect along the mainline)
- No power flow simulation (voltage, losses, reactive power)
- No 8760-hour load profiles per feeder (these exist in PI but are not
  routinely extracted for the screen)
- No winter peak screening (as of 2026 — only summer peaks are screened)

---

## What happens when a component is flagged: area studies

When the annual screening flags a component (load at risk exceeds the MWh
threshold), it enters the planning pipeline for an **Integrated Area Study**.
The area study is the mechanism by which the flagged concern turns into a
funded capital project — or a non-wires alternative. The full study process
is documented in `context/sources/rie_distribution_planning_study_process.md`.

Completed area studies are publicly available at RIE's
[System Data Portal](https://portalconnect.rienergy.com/RI/s/article/Rhode-Island-System-Data-Portal).

### Scope: not just thermal loading

While the annual screening's primary quantitative trigger is thermal loading
(criteria 1 and 2 above), the area study evaluates a broader set of system
performance concerns:

- **Thermal loading** — load vs. equipment capability
- **Voltage performance** — whether voltage stays within ANSI C84.1 limits
  (113–123V at the service point in RI)
- **Reactive compensation** — adequacy of capacitor banks
- **Asset condition** — physical state of aging equipment (breakers,
  underground cable, substations), assessed via condition reports
- **Reliability performance** — CKAIDI and CKAIFI indices against state
  targets (using 5-year data, or 3-year to exclude major storm years)
- **Arc flash** — incident energy levels (worker safety)
- **Fault duty / short circuit** — whether breakers can handle fault current
- **Protective coordination** — proper relay/recloser/fuse coordination

In practice, the comprehensive plan developed by the area study addresses
multiple concerns simultaneously. From the call: "when we address a
contingency issue, I don't just try to address this contingency issue by
itself... there might be voltage issues, or reliability issues... we try to
roll all that in together." This means that the cost of resolving a thermal
loading violation typically includes resolution of co-located asset condition,
reliability, and voltage concerns as well.

### Study milestones

Area studies follow 9 milestones (details in the study process document):

1. **Scoping** — Gather inputs: planning guidelines, equipment ratings, load
   forecasts (now with separate EE/DG/EV/heat electrification/DR/ES
   forecasts), asset condition reports, GIS maps, DER queues. Build system
   models (CYME, PSS/e). Assemble cross-functional study team.

2. **Initial system assessment** — Quick-pass analysis of thermal, voltage,
   reactive support, asset condition, reliability, arc flash, and fault duty.
   Enough to lead a productive kickoff, not so much that findings would need
   rework.

3. **Study kickoff** — Large stakeholder meeting (operations, design, control
   center, community management, resource planning). Present known concerns,
   solicit input on operational issues, asset conditions, upcoming loads, and
   construction constraints.

4. **Detailed engineering analysis** — Full load flow studies, fault studies,
   protective coordination, arc flash calculations, loss studies, voltage
   analysis, DER impact analysis. Quick operational fixes (load rebalancing,
   switching) are implemented immediately and folded into the base case.

5. **Plan development and estimating** — Develop multiple alternative plans
   (wires and non-wires), get feasibility review from engineering functions,
   request cost estimates (8–12 week turnaround).

6. **Recommended plan** — Compare alternatives on cost, technical
   performance, schedule, permitting, environmental impact, outage
   requirements, climate resiliency, and grid modernization alignment.

7. **Technical review** — Formal presentation to senior leadership (up to VP
   of Electric Operations and jurisdictional president). Assumptions and
   analysis are challenged.

8. **Documentation** — Formal area study report.

9. **Sanctioning** — Capital approval. Projects spending in the next 3 fiscal
   years are sanctioned immediately; longer-term projects are tracked.

### Area study data and tooling

The area study represents a major step up in analytical depth from the
screening. Where the screening uses Excel and GIS, the area study uses full
power system simulation software with detailed circuit models. (Details in
this section are from the study process document, Sections 5.1 and 5.4, and
the planning guide, Section 4.1, unless otherwise noted.)

**Circuit modeling software:**

- **CYME (Cymedist)** — Radial distribution feeder load flow and voltage
  analysis. This is the primary tool for feeder-level engineering. CYME
  models include segment-level topology: each conductor section, load point,
  capacitor bank, regulator, and tie switch. This is what enables the area
  study to analyze section-level faults and topology-based load at risk that
  the screening cannot.
- **PSS/e** — Network load flow software for sub-transmission and
  transmission analysis. Used for supply system studies and network (non-
  radial) configurations.
- **ASPEN** — Protective device coordination and short circuit analysis.

**Additional tools:**

- **ArcPro** — Arc flash incident energy calculations (worker safety).
- **GIS** — Supports CYME model construction and geographic analysis.
- **FeedPro** — Equipment loading and ratings database.
- **EMS and PI** — Energy Management System data and PI Historian time-series
  data (same SCADA source as the screening, but analyzed in more depth).
- **Annual Planning Screening Spreadsheets** — The screening results feed
  directly into the area study as a starting point.

**What the area study adds over the screening:**

- **Segment-level feeder topology** via CYME models, enabling analysis of
  where faults occur along the mainline, which customers are served by which
  segments, and which segments can be re-energized via ties. This is where
  load at risk by topology (unreachable dead-end segments) can be identified
  — something the screening's bulk-transfer spreadsheet cannot capture.
- **Power flow simulation** — voltage profiles along feeders, reactive power
  flows, loss calculations. The screening only checks thermal loading; the
  area study checks whether voltage stays within limits (113–123V at the
  service point in RI) and whether reactive compensation is adequate.
- **Fault analysis** — short circuit currents, protective device coordination,
  breaker capability. Determines whether protection equipment can handle
  fault levels and whether faults are isolated properly.
- **8760-hour load data** — When available, full yearly load profiles for
  feeders, substations, and supply lines (from PI Historian). The study
  process document calls for gathering these as part of scoping (Section
  5.1).

From the call, Ryan noted that the deeper area study is where they "look at
other sections" beyond the whole-feeder-loss assumption: "sometimes there can
be a secondary limit where a section near the source — not the main — is the
worst criteria because it actually takes out the tie." This kind of analysis
requires the segment-level CYME model and is not possible with the screening
spreadsheet.

### Cost of resolving thermal loading violations

From the call, the cost range for addressing contingency load-at-risk
violations is wide and highly dependent on the specific engineering context:

- Simple cases: **hundreds of thousands of dollars**
- Moderate cases: **low single-digit millions**
- Complex comprehensive plans (like East Bay, which also addresses asset
  condition and sub-transmission rebuilds): **tens of millions**

There is no reliable $/kW or $/MW generic figure. RIE's own energy efficiency
team uses a system-average distribution cost figure for their analyses,
acknowledging the same difficulty.
