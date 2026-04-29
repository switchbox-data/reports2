# IL NPA — Recurring Regulatory Content (Observed in Corpus)

What recurs across the 10 expert testimony exemplars in `reports/il_npa/sources/`. The corpus is **one consolidated docket** (ICC Dkts. 23-0068 / 23-0069 cons., PGL & North Shore Gas) with **six witnesses across four filing rounds** between 2023-05-09 and 2024-03-05 — not a representative sample of Illinois ICC practice. Findings here describe what shows up _in this corpus_, not what Illinois law or convention universally requires of new testimony. Frequency-bucketed claims should be read as "observed in N of 10 of these specific exemplars."

Counts were re-verified by `grep` against the source files; numbers in the existing `required_content.md` were taken as starting hypotheses but several were revised down where the prior file appears to have inferred citation from topic discussion rather than verified the textual reference.

Witness shorthand (per `_scratch/format_conventions.md`):

| Code  | Witness  | Filing              | Party       |
| ----- | -------- | ------------------- | ----------- |
| C-D   | Cebulko  | Direct              | PIO         |
| S-D   | Schott   | Direct              | PIO         |
| D-D   | Dismukes | Direct              | AG          |
| C-R   | Cebulko  | Rebuttal            | PIO         |
| E-R   | Elder    | Rebuttal            | PIO         |
| L-R   | Leyko    | Rebuttal            | CUB/PCR/COC |
| DL-R  | DeLeon   | Rebuttal            | COC         |
| R-R   | Rábago   | Rebuttal            | COC         |
| W-R   | Walker   | Rebuttal            | AG          |
| Ef-DR | Effron   | Direct on Rehearing | AG          |

> **No item in the corpus is cited by all 10 witnesses, and none reaches "near-universal" (8–9).** Every witness writes to a narrow slice of the case, and several short rebuttals (Leyko on incentive comp, Effron on incremental plant, Schott on equity) cite almost no shared authority. The "Frequently cited" tier (5–7 of 10) is the practical ceiling.

---

## A. Primary regulatory authority

Statutes, ICC orders, and prior dockets cited as binding or persuasive precedent.

### Frequently cited (5–7 of 10)

#### Illinois Public Utilities Act — 220 ILCS 5/... (general)

Cited in several specific subsections; no single section is shared across files. S-D anchors equity recommendations in Section 1-102(d); C-D footnotes Sections 8-103B and 8-104 for energy-efficiency context; D-D cites Section 9-220.3 (the QIP statute, which is itself a PUA section); C-R quotes the Company's invocation of the PUA on non-discriminatory access; DL-R invokes the PUA's just-and-reasonable obligation as the framing peg.

- **Citation forms in corpus:** `220 ILCS 5/1-102(d)`, `220 ILCS 5/8-103B (b-27)`, `220 ILCS 5/8-104`, `220 ILCS 5/9-220.3(b)`, "the Public Utilities Act."
- **Count: 5/10** — S-D, C-D, D-D, C-R, DL-R.
- **Quote (S-D, footnote 40, line 544):** _"(220 ILCS 5/1-102(d)) [Illinois Public Utilities Act — Section 1-102]."_
- **Quote (D-D, footnote 14, line 267):** _"220 ILCS 5/9-220.3(b)."_

### Sometimes cited (3–4 of 10)

#### Climate and Equitable Jobs Act (CEJA) — Public Act 102-0662

Cited as the controlling state climate policy frame (100% renewables by 2050, electric-utility electrification authority, ICC mandate to study renewable progress). Treated as binding for forecasting/planning purposes by witnesses who reach the energy-transition argument; the rate-design and revenue-requirement specialists do not cite it.

- **Citation forms:** `Climate and Equitable Jobs Act (CEJA, Public Act 102-0662)`, `the CEJA`, `Public Act 102-0662`.
- **Count: 4/10** — S-D, C-D, D-D, C-R. Not cited in E-R, L-R, DL-R, R-R, W-R, Ef-DR (verified by `grep -i "CEJA\|102-0662\|Climate and Equitable"`).
- **Quote (C-D, line 198):** _"the Climate and Equitable Jobs Act (CEJA, Public Act 102-0662) that will reduce or restrict the sale of natural gas."_ (15 words)
- **Quote (D-D, line 156):** _"requirements set forth by the Climate and Equitable Jobs Act ('CEJA') for the Commission to study."_ (15 words)

#### Prior PGL/North Shore base rate order — Docket Nos. 14-0224 / 14-0225 (cons.), Final Order Jan. 21, 2015

The 2015 base-rate order referenced for customer-charge classification, ECOSS treatment, and as the rate-base baseline.

- **Citation forms:** `Docket No. 14-0224/14-0225 (cons.) (Jan. 21, 2015)`, `Docket No. 14-0224/14-0225 (Consol.) Order (January 21, 2015)`, `rate case 14-0225`, `Docket Nos. 14-0224/0225`.
- **Count: 3/10** — C-D, C-R, R-R. The prior `required_content.md` listed 8/10 by including witnesses who discussed rate-case context without textually citing this docket; verified `grep` returns zero hits for D-D, E-R, L-R, DL-R, W-R, Ef-DR.
- **Quote (R-R, footnote 62, line 343):** _"See Final Order, Docket No. 14-0224/14-0225 (cons.) (Jan. 21, 2015) at 194."_
- **Quote (C-R, footnote 117, line 683):** _"Docket No. 14-0224/14-0225 (Consol.) Order (January 21, 2015) at 176."_

#### QIP statute — 220 ILCS 5/9-220.3

The 2013 Qualifying Infrastructure Plant rider statute that funded a decade of pipeline replacement. Centerpiece for D-D; supporting authority for C-D and W-R.

- **Citation forms:** `Section 9-220.3`, `ILCS Section 9-220.3(d)(1)`, `220 ILCS 5/9-220.3(b)`, "the QIP Statute."
- **Count: 3/10** — C-D, D-D, W-R. (C-R discusses QIP rollover but `grep -i "QIP\|9-220"` returns 0 hits in the C-R source; topic ≠ citation.)
- **Quote (D-D, line 242):** _"Following passage of Illinois Compiled Statutes ('ILCS') Section 9-220.3 in 2013 (the 'QIP Statute')."_ (14 words)

#### Nicor parallel rate case — ICC Docket 23-0066

Contemporaneous gas rate case; cited where PIO witnesses had filed substantially similar testimony.

- **Citation forms:** `Docket No. 23-0066`, `ICC Docket 23-0066`, `Northern Illinois Gas Company's (Nicor) rate case, Docket No. 23-0066`.
- **Count: 3/10** — C-D, C-R, E-R.
- **Quote (E-R, line 70):** _"I recently submitted rebuttal testimony in Northern Illinois Gas Company's (Nicor) rate case, Docket No. 23-0066."_ (15 words)

### Occasional (2 of 10)

#### Prior PGL SMP review dockets — ICC Docket 16-0376 and ICC Docket 18-1092

Procedural history of PGL's accelerated main-replacement program approvals; only invoked by the two witnesses recommending SMP-specific changes.

- **Citation forms:** `ICC Docket No. 16-0376`, `ICC Docket No. 18-1092`, `the ICC's order in Docket No. 16-0376`.
- **Count: 2/10** — C-D, DL-R.
- **Quote (DL-R, line 249):** _"the Commission assessed the SMP in ICC Docket No. 16-0376 and ICC Docket No. 18-1092."_ (15 words)

#### PHMSA federal pipeline rules — 49 CFR Parts 191 / 192 / 195

Federal pipeline-integrity rule driving MAOP reconfirmation; only invoked by the two witnesses with capex-integrity scope.

- **Citation forms:** `PHMSA federal regulations (49 CFR Parts 191/195)`, `49 CFR Part 192`.
- **Count: 2/10** — C-D, D-D.
- **Quote (D-D, line 661 footnote summary):** _"PHMSA federal regulations (49 CFR Parts 191/195)."_

> Two other authority sets carry weight in this corpus despite appearing in only one filing: (i) the **prior incentive-compensation orders** (Dockets 20-0308 Ameren, 18-0463, 18-1775, 19-0436), cited only in L-R but as the legal scaffold for the entire incentive-comp issue; and (ii) the **220 ILCS 5/8-201.10(b) credit/collections/arrearage reporting statute**, cited only in S-D but as the equity-data hook for the LIDC argument. Listing them here for completeness; both are 1-of-10 by count and excluded from the recurring tally.

---

## B. Commission-adopted principles

Substantive ratemaking standards witnesses invoke (often without specific docket citation).

### Sometimes cited (3–4 of 10)

#### "Just and reasonable" rate standard

The PUA's overarching test, named explicitly in the body prose (rather than only in PUA-section footnotes).

- **Count: 4/10** — C-D, D-D, DL-R, R-R.
- **Quote (DL-R, line 405):** _"the Commission's obligation to ensure just and reasonable rates under the Public Utilities Act."_ (14 words)
- **Quote (R-R, line 326):** _"That finding says nothing about whether the rate design is just and reasonable on either an inter- or intra-class basis."_

#### "Prudent" / prudence standard

The traditional ratemaking test for whether an investment was reasonably incurred. Used as the framing peg for disallowance arguments.

- **Count: 4/10** — C-D, C-R, DL-R, W-R.
- **Quote (W-R, line 118):** _"there are potentially costs that may be prudently incurred above and beyond the benchmark."_ (14 words)

#### Cost-causation principle

The Commission-adopted standard that fixed customer charges should recover only customer-related, not demand-related, costs. Centerpiece for the rate-design rebuttals.

- **Citation forms in corpus:** `cost causation principles`, `cost-causation principle`.
- **Count: 3/10** — C-D, C-R, R-R.
- **Quote (R-R, line 150):** _"recovering through the fixed customer charge only those costs absolutely necessary ... follows cost causation principles."_ (15 words)
- **Quote (C-D, line 125):** _"reduce the residential heating customer charge to $24.86/month ... to better reflect cost causation."_ (13 words)

#### Gradualism (rate-design transition)

The principle that customer-charge changes be transitioned to soften bill-impact shock.

- **Count: 3/10** — C-D, C-R, R-R.
- **Quote (R-R, line 150):** _"order a gradual, but short transition to the basic customer method ECOSS approach to rate design."_ (15 words)

### Occasional (2 of 10)

#### "Used and useful" standard

The traditional rate-base inclusion test (plant must be in service and used to provide service to ratepayers). Centerpiece of W-R's distribution-pipeline disallowance; passing reference in C-D's stranded-asset framing.

- **Count: 2/10** — C-D, W-R. (Verified by `grep -i "used and useful"`; the prior `required_content.md` listed 7/10 but most of those witnesses use the rate-base framework without invoking the "used and useful" phrase textually.)
- **Quote (W-R, line 82):** _"the forecasted projects will not be used and useful within the scope of this rate case."_ (15 words)

---

## C. Standard methodologies

Analytical frameworks invoked to support a position. Some of these are foundational ratemaking arithmetic that any rate-case witness would necessarily use; their corpus presence reflects who happens to write substantive analytical sections vs. short topical rebuttals.

### Frequently cited (5–7 of 10)

#### Test year construct (forecasted 2024 / future test year)

The forecast-year framework that anchors PGL/NS's revenue-requirement arithmetic.

- **Count: 7/10** — C-D, D-D, E-R, L-R, DL-R, R-R, Ef-DR.
- **Quote (Ef-DR, line 111):** _"The test year rate base reflects the average of plant as of the beginning of the year and the end."_ (≈19 words; shortened) → _"the test year rate base reflects the average of plant... beginning... and end of the year."_ (15 words)

#### Revenue requirement components (rate base × ROR + depreciation + O&M + taxes)

Standard ratemaking arithmetic invoked when proposing disallowances or alternative revenue requirements.

- **Count: 6/10** — C-D, D-D, C-R, E-R, R-R, Ef-DR.
- **Quote (Ef-DR, line 99):** _"the return on the net increase in rate base and depreciation expense."_ (12 words)

#### Rate base mechanics

Closely related to revenue requirement; counted separately because some witnesses (W-R, E-R) discuss rate-base inclusion without doing the full revenue-requirement arithmetic.

- **Count: 6/10** — C-D, D-D, C-R, E-R, W-R, Ef-DR.

#### Stranded-asset / declining-throughput framing

Not a "principle" or "method" in the doctrinal sense, but a standard analytical framing this corpus uses to position recommendations against the energy-transition risk.

- **Count: 5/10** — C-D, D-D, C-R, E-R, DL-R.
- **Quote (C-D, line 252):** _"significant continued investment in the natural gas system will likely result in ... underutilized and stranded gas assets."_ (15 words)

#### Safety Modernization Program (SMP) — analytical scrutiny of

PGL's accelerated cast/ductile-iron pipe replacement program; the case's largest capex line. Substantive discussion (not just topic-mention) appears in 5 filings.

- **Count: 5/10** — C-D, C-R, DL-R, W-R, plus a single passing reference in D-D (line 205, "<u>2024 Safety Modernization Investment</u>: $12.1 million increase"). Excluding D-D as topic-mention-only would drop this to 4/10; include the bare-mention to read as 5/10.
- **Quote (DL-R, line 70):** _"the need to reevaluate PGL's Safety Modernization Program ('SMP')"_ (9 words)

### Sometimes cited (3–4 of 10)

#### Non-Pipeline Alternatives (NPAs) / alternatives analysis

Recommendation that the utility analyze NPAs (efficiency, electrification, demand response) before approving major capex.

- **Count: 4/10** — C-D, D-D, C-R, DL-R.
- **Quote (DL-R, line 70):** _"analyses related to Non-Pipeline Alternatives ('NPAs') and Greenhouse Gas ('GHG') emissions."_ (11 words)

#### Performance-based regulation / metrics / PIMs

Reporting metrics, MYRPs, performance incentive mechanisms.

- **Count: 4/10** — C-D, S-D (1 hit), D-D, C-R, L-R (2 hits). Marking 4/10 conservatively (S-D and L-R hits are passing references).
- **Quote (C-D, summary):** _"establish a set of performance metrics that the Company is required to report annually."_ (14 words)

#### Depreciation analysis

Rate-base offset arithmetic; appears wherever revenue-requirement arithmetic is worked.

- **Count: 4/10** — C-D, D-D, C-R, Ef-DR.
- **Quote (Ef-DR, line 99):** _"return on the net increase in rate base and depreciation expense."_ (11 words)

#### "Future of Gas" proceeding (recommendation to open)

Recommendation to open a separate state-wide docket to set planning rules for gas utilities.

- **Count: 3/10** — C-D, C-R, DL-R (centerpiece). (D-D's "Potential Illinois Policy Changes" section gestures at the same idea without using the phrase; not counted.)
- **Quote (DL-R, line 47):** _"THE COMMISSION SHOULD INITIATE A ROBUST 'FUTURE OF GAS' PROCEEDING."_ (10 words)

### Occasional (2 of 10)

#### Embedded Cost of Service Study (ECOSS) / Basic Customer Method

The cost-allocation study used to classify customer vs. demand costs; the basic customer method is the rate-design counter-proposal.

- **Citation forms:** `ECOSS`, `Embedded Cost of Service Study`, `Basic Customer Method ECOSS`.
- **Count: 2/10** — C-R, R-R. (Prior version listed 3/10 including C-D; verified `grep -i "ECOSS\|Embedded Cost of Service"` returns zero hits in C-D. C-D discusses cost-causation in rate design but does not use the ECOSS term textually — counted under the cost-causation principle in §B instead.)
- **Quote (R-R, line 150):** _"the Basic Customer Method ECOSS is direct proof of my conclusion."_ (11 words)

#### Pipeline cost benchmarking ($/mile, $/inch-mile)

Quantitative cost-discipline tool: cap on $/mile of replaced main; transmission benchmarking.

- **Count: 2/10** — D-D ($7.2M/mile distribution caps), W-R (transmission inch-mile).
- **Quote (D-D):** _"establishing a cap of $7.2 million per mile of replaced distribution main."_ (12 words)

#### MAOP reconfirmation analysis

Federal pipeline-integrity rule driving a chunk of capex; six approved reconfirmation methods.

- **Count: 2/10** — C-D (centerpiece), D-D.
- **Quote (C-D):** _"evaluate each of the six MAOP reconfirmation methods for all future MAOP rule investments."_ (14 words)

#### Certificate of Public Convenience and Necessity (CPCN)

Pre-approval gate for major non-reliability gas projects.

- **Count: 2/10** — D-D (centerpiece, $12M threshold), C-D (passing).
- **Quote (D-D):** _"adopt a Certificate of Public Convenience and Necessity ('CPCN') requirement... estimated to cost $12.0 million or greater."_ (≈18; shorten) → _"adopt a Certificate of Public Convenience and Necessity ('CPCN') requirement."_ (10 words)

---

## D. Secondary external authorities

Industry, academic, and federal-policy references invoked as persuasive but not binding. None of these appears in more than 4 filings.

### Sometimes cited (3–4 of 10)

#### Inflation Reduction Act (IRA) — federal heat-pump credits / rebates

Federal subsidy frame for the cost-competitiveness-of-electrification argument.

- **Count: 4/10** — S-D, C-D, D-D, C-R.
- **Quote (C-D):** _"increasing cost competitiveness of heat pumps, buttressed by IRA credits and rebates."_ (12 words)

#### NARUC Gas Manual (cost-allocation guidance)

Industry reference invoked on classification of distribution mains and service lines.

- **Count: 3/10** — C-D, C-R, R-R.
- **Quote (C-D, line 1098):** _"According to the NARUC Gas Manual, the classification of distribution costs ... 'can be controversial.'"_ (14 words)

### Occasional (2 of 10)

#### Brattle "Future of Gas Utilities" report (2021)

Industry analysis of utility-side decarbonization options. Notable because PGL's own rebuttal witness Graves was the principal Brattle author.

- **Count: 2/10** — C-R (attached as PIO Ex. 4.1), DL-R (attached as City Ex. 3.01). (Updates the prior `required_content.md`'s 4/10 — verified by `grep -i brattle`; only C-R and DL-R have textual references.)
- **Quote (C-R, line 124):** _"the Graves Brattle Report ... 'almost half of non-electricity gas demand has a high likelihood to be electrified.'"_ (15 words)

> Single-witness external authorities also appear, including (i) the **EPRI Ameren electrification study** (centerpiece of C-R, attached as PIO Ex. 4.3/4.4 — verified `grep -i EPRI` returns hits only in C-R; the prior version's listing of DL-R and R-R was unverified topic-inference); (ii) the API Infrastructure Study, Oil & Gas Journal 2022, and EIA Natural Gas Pipeline Projects (W-R); and (iii) the LEAD Tool, EEP framework, and Colton LIDC excerpt (S-D). All are 1-of-10 by textual count and excluded from the recurring tally.

---

## What this corpus suggests for a new testimony in this docket family

These are inferences from the observed corpus, not universal Illinois requirements. A different docket, a different witness scope, or a different procedural posture could materially change what is appropriate.

1. **No single citation is mandatory across the corpus.** The "must include" framing in the prior `required_content.md` overstated several counts (notably 14-0224/14-0225 listed 8/10, verified at 3/10; CEJA listed 7/10, verified at 4/10). What this corpus does suggest is **scope-dependent expectations**:
   - **Capex-disallowance scope** (C-D, D-D, E-R, W-R, DL-R, Ef-DR): the test-year revenue-requirement arithmetic is universal; QIP-statute discussion is common where the disallowance touches QIP-funded plant; SMP discussion is common where it touches main replacement.
   - **Rate-design scope** (C-D, C-R, R-R): cost-causation language and the 14-0224/14-0225 prior order are the shared anchors; ECOSS / Basic Customer Method appears in C-R and R-R (and underpins C-D's recommendation even where C-D does not use the term).
   - **Energy-transition scope** (C-D, C-R, DL-R, partly D-D): CEJA, stranded-asset framing, and Brattle co-occur (Brattle in C-R and DL-R; EPRI is C-R-only and not a shared anchor).
   - **Equity scope** (S-D only in this corpus): the equity-specific authorities (220 ILCS 5/8-201.10(b), Section 1-102(d), the EEP four-pillar framework) are S-D-unique, so a new equity witness would be drawing fresh ground from a single precedent within the docket.
   - **Incentive-compensation scope** (L-R only): the four-docket incentive-comp line (20-0308, 18-1775, 19-0436, 18-0463) is the entire authority base; a new witness on this issue would necessarily echo it.
2. **"Just and reasonable" and "used and useful" are invoked less often than ratemaking lore would predict** — 4/10 and 2/10 respectively in this corpus. Witnesses tend to do the underlying analysis and let the legal label sit in the introduction or framing rather than threading it through the body.
3. **Footnoting prior testimony in this docket** (using the `Witness Name, Party Ex. X.0 at PAGE:LINE` form) is the more universal convention than any specific external authority — see `_scratch/format_conventions.md` §5. The mechanical citation form is more reliably "required" than the substantive citation list.
4. **For a new witness with a narrow rebuttal scope**, the corpus is consistent with citing only what their issue requires. Effron's rehearing testimony cites no statutes, no prior orders by docket number, and no external authorities — and the filing was accepted. That is a corpus data point about what a focused rebuttal can look like, not a recommendation.
