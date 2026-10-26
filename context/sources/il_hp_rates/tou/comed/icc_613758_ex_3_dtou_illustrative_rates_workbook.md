# ComEd Ex. 3.04 — Illustrative TOU Distribution Rate (Determination of the Time of Use Delivery Facilities Charges by Delivery Class; Initial RDI Filing)

**Source**: `icc_613758_ex_3_dtou_illustrative_rates_workbook.pdf` (ICC e-docket file id / filing id 613758)
**Pages**: 9 (five workbook tabs rendered to PDF: tab 1 on pp. 1–3, tab 2 on pp. 4–5, tab 3 on pp. 6–7, tab 4 on p. 8, tab 5 on p. 9)
**Date**: Filed May 23, 2024 as an attachment to ComEd Ex. 3.0 (the rendered exhibit itself is undated and carries the placeholder caption "ICC Docket No. 24-____")
**Docket**: ICC Docket No. 24-0378 (Commonwealth Edison Co., revenue-neutral tariff changes related to rate design — Rate BEST / DTOU) — initial RDI phase
**Author(s)**: Commonwealth Edison Company (sponsored by Kathleen E. Kremer, Principal Rate Analyst, Retail Rates)
**Document type**: Exhibit — spreadsheet rendered to PDF (workbook titled "Illustrative TOU Distribution Rate"), five tabs
**ComEd exhibit no.**: ComEd Ex. 3.04 (cited in Ex. 3.0, p. 3: "an illustrative example showing the determination of the TOU DFCs")
**Extraction method**: Embedded PDF text (PyMuPDF), every table and column count verified against rendered page images
**Extraction notes**:

- _Minor typographical errors in the source have been corrected for readability. Substantive corrections are annotated inline._ The workbook's own tab name "4_Shared Distrubution Lines" is reproduced exactly as in the source (the misspelling "Distrubution" is the actual tab label; the body testimony in Ex. 3.0 spells it "Distribution").
- Each page of the render carries the page header "Commonwealth Edison Company / [tab-specific title] / Illustrative Example", the right-hand label "Illustrative TOU Distribution Rate / Tab: <tab name>", and the exhibit stamp "ICC Docket No. 24-____ / ComEd Ex. 3.04 / Page N of 9". The tab name and page number are given in each page heading below; the rest of the repeated header and stamp are omitted after being stated once here.
- The spreadsheet's "Line No." labels and formula text (e.g. `Line 7 = Line 2 / Line 6`) appear to the right of each row in the source; they are kept as a final **Line / formula** column. The class columns in every table are, in order: **SFNH** (Single Family, No Elec. Space Heat), **MFNH** (Multi Family, No Elec. Space Heat), **SFH** (Single Family, Elec. Space Heat), **MFH** (Multi Family, Elec. Space Heat) — the same abbreviations used in Ex. 3.0 at p. 18. Source column headers are written out in full in each table.
- Cell colors in the source (yellow = Morning, red/pink = Mid-Day Peak, light blue = Evening, green = Overnight; red/orange/green = System High/Moderate/Base) are conveyed here by the row labels.
- Notes blocks under each table (numbered (1), (2), …) are reproduced as "Notes" lines directly under the table they belong to; all numeric footnotes are in this form (no separate Footnotes section).
- Dollar signs are escaped as `\$`. Where the render shows a $/kWh rate to five decimals, all five decimals are preserved.
- This document's illustrative values are 2026 rates. A rebuttal-phase version with a 10 pm overnight boundary (ComEd Ex. 6.03) is extracted separately as `icc_620687_dtou_illustrative_10pm_overnight_rebuttal_rdi.md`.

---

## Tab 1: `1_DTOU DFC Rates` (pp. 1–3)

**The Determination of the Time of Use Delivery Facilities Charges by Delivery Class — Illustrative Example**

### Page 1 of 9

**Section A. Delivery Service Time of Use (DTOU) Periods**

<!-- EPON: midday-peak — DTOU period definitions in this exhibit: Mid-Day Peak 1 pm–7 pm (hour ending 14–19), the same window every day; Morning 6 am–1 pm; Evening 7–11 pm; Overnight 11 pm–6 am -->

| DTOU Period  | Hours         | Hour Ending |
| ------------ | ------------- | ----------- |
| Morning      | 6 am to 1 pm  | 7-13        |
| Mid-Day Peak | 1 pm to 7 pm  | 14-19       |
| Evening      | 7 pm to 11 pm | 20-23       |
| Overnight    | 11 pm to 6 am | 1-6, 24     |

**Section B. 2026 Average per kWh DFC by Delivery Class** (Note 1)

<!-- EPON: ev-hp,fixed-vs-volumetric — current flat (non-time-varying) residential DFC by delivery class: electric-space-heat classes already pay a lower flat per-kWh DFC than non-heat classes: about 48% (single family) and 59% (multi family) of the no-heat rate (SF heat $0.02657 vs SF no heat $0.05568; MF heat $0.02526 vs MF no heat $0.04248) -->

|                          | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line   |
| ------------------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------ |
| 2026 average per kWh DFC | \$0.05568                         | \$0.04248                        | \$0.02657                      | \$0.02526                     | Line 1 |

Notes: (1) These are the 2026 DFCs by delivery class shown in ComEd Ex. 2.02. (See Notes under page 3.)

**Section C. 2026 Annual Billed kWh by DTOU Period and by Delivery Class** (Note 2)

<!-- EPON: profile,midday-peak — class billed kWh by period (Section C) built from the average customer's load shape; electric-space-heat classes are a small share of the residential base (SFH 0.675 billion and MFH 1.579 billion kWh vs SFNH 20.06 billion kWh) -->

| DTOU Period  | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                 |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------------------------------ |
| Morning      | 5,306,933,486                     | 1,370,864,294                    | 201,417,739                    | 465,266,160                   | Line 2                         |
| Mid-Day Peak | 6,129,549,262                     | 1,420,394,572                    | 177,787,988                    | 416,019,068                   | Line 3                         |
| Evening      | 4,026,635,272                     | 993,077,851                      | 120,921,719                    | 291,317,516                   | Line 4                         |
| Overnight    | 4,592,622,074                     | 1,247,167,105                    | 174,617,202                    | 406,333,685                   | Line 5                         |
| Total        | 20,055,740,094                    | 5,031,503,822                    | 674,744,648                    | 1,578,936,429                 | Line 6 = Sum (Line 2 : Line 5) |

**Section D. 2026 Annual Billed kWh Distribution by DTOU Period**

<!-- EPON: profile,ev-hp,midday-peak — share of 2026 billed kWh by DTOU period; Mid-Day Peak share is 30.56% (SFNH) and 28.23% (MFNH) vs 26.35% for both electric-space-heat classes, i.e., heat-class load is flatter across the day than the no-heat classes -->

| DTOU Period  | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                   |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | -------------------------------- |
| Morning      | 26.46%                            | 27.25%                           | 29.85%                         | 29.47%                        | Line 7 = Line 2 / Line 6         |
| Mid-Day Peak | 30.56%                            | 28.23%                           | 26.35%                         | 26.35%                        | Line 8 = Line 3 / Line 6         |
| Evening      | 20.08%                            | 19.74%                           | 17.92%                         | 18.45%                        | Line 9 = Line 4 / Line 6         |
| Overnight    | 22.90%                            | 24.78%                           | 25.88%                         | 25.73%                        | Line 10 = Line 5 / Line 6        |
| Total        | 100.00%                           | 100.00%                          | 100.00%                        | 100.00%                       | Line 11 = Sum (Line 7 : Line 10) |

### Page 2 of 9

**Section E. System Loading Categories**

| System Loading Category | Description                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------- |
| System High             | Costs of distribution equipment required to deliver power to a heavily loaded grid    |
| System Moderate         | Costs of distribution equipment required to deliver power to a moderately loaded grid |
| System Base             | Costs of baseline equipment required to deliver power                                 |

**Section F. DFC Revenue Responsibility by System Loading Category by Delivery Class** (Note 3)

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                    |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | --------------------------------- |
| System High             | \$400,184,224                     | \$77,604,096                     | \$5,769,596                    | \$12,367,350                  | Line 12                           |
| System Moderate         | \$118,051,203                     | \$22,892,691                     | \$1,699,967                    | \$3,642,506                   | Line 13                           |
| System Base             | \$598,468,181                     | \$113,241,496                    | \$10,458,402                   | \$23,874,078                  | Line 14                           |
| Total                   | \$1,116,703,608                   | \$213,738,283                    | \$17,927,965                   | \$39,883,934                  | Line 15 = Sum (Line 12 : Line 14) |

**Section G1. 2026 Annual Billed kWh by System Loading Category Applicable Period and by Delivery Class** (Note 4)

<!-- EPON: stacking,midday-peak — System High kWh = Mid-Day Peak kWh only; System Moderate kWh = Morning + Mid-Day Peak + Evening; System Base kWh = all hours (divisors for the stacked rate layers) -->

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                     |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ---------------------------------- |
| System High             | 6,129,549,262                     | 1,420,394,572                    | 177,787,988                    | 416,019,068                   | Line 16 = Line 3                   |
| System Moderate         | 15,463,118,020                    | 3,784,336,717                    | 500,127,446                    | 1,172,602,744                 | Line 17 = Line 2 + Line 3 + Line 4 |
| System Base             | 20,055,740,094                    | 5,031,503,822                    | 674,744,648                    | 1,578,936,429                 | Line 18 = Line 6                   |

**Section G2. Applicable kWh for each System Loading Category**

| System Categories | TOU Periods (col. 1) | TOU Periods (col. 2) | TOU Periods (col. 3) | TOU Periods (col. 4) |
| ----------------- | -------------------- | -------------------- | -------------------- | -------------------- |
| System High       |                      | Mid-Day Peak         |                      |                      |
| System Moderate   | Morning              | Mid-Day Peak         | Evening              |                      |
| System Base       | Morning              | Mid-Day Peak         | Evening              | Overnight            |

(The source shows a merged "TOU Periods" header over four unlabeled columns; the cell colors place Morning, Mid-Day Peak, Evening and Overnight in columns 1–4 respectively.)

### Page 3 of 9

**Section H. Compute Per kWh DFC Revenue Responsibility by System Loading Category by Delivery Class**

<!-- EPON: ev-hp,midday-peak,stacking — per-kWh cost layers: System High layer $0.06529 (SFNH) vs $0.03245 (SFH) and $0.05464 (MFNH) vs $0.02973 (MFH); the electric-space-heat classes carry lower layers per kWh: System High layer is 50% (single family) and 54% (multi family) of the no-heat class, System Base layer 52% and 67% -->

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula              |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | --------------------------- |
| System High             | \$0.06529                         | \$0.05464                        | \$0.03245                      | \$0.02973                     | Line 19 = Line 12 / Line 16 |
| System Moderate         | \$0.00763                         | \$0.00605                        | \$0.00340                      | \$0.00311                     | Line 20 = Line 13 / Line 17 |
| System Base             | \$0.02984                         | \$0.02251                        | \$0.01550                      | \$0.01512                     | Line 21 = Line 14 / Line 18 |

**Section I. Compute Per kilowatt-hour (kWh) Distribution Facilities Charges (DFCs) by DTOU Period by Delivery Class**

<!-- EPON: ev-hp,midday-peak,stacking,fixed-vs-volumetric — THE DTOU RATES by delivery class (2026 illustrative, $/kWh): Mid-Day Peak SFNH $0.10276 / MFNH $0.08320 / SFH (elec. space heat) $0.05135 / MFH $0.04796; Morning=Evening SFNH $0.03747 / MFNH $0.02856 / SFH $0.01890 / MFH $0.01823; Overnight SFNH $0.02984 / MFNH $0.02251 / SFH $0.01550 / MFH $0.01512. Space-heat classes pay lower rates in every period (single family about 50% of the no-heat rate; multi family 58–67%); Mid-Day Peak-to-Overnight ratio is about 3.3x (SFH) and 3.4x (SFNH), 3.2x (MFH) and 3.7x (MFNH) -->

| DTOU Period                       | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                        |
| --------------------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------------------------------------- |
| Morning                           | \$0.03747                         | \$0.02856                        | \$0.01890                      | \$0.01823                     | Line 22 = Line 20 + Line 21           |
| Mid-Day Peak                      | \$0.10276                         | \$0.08320                        | \$0.05135                      | \$0.04796                     | Line 23 = Line 19 + Line 20 + Line 21 |
| Evening                           | \$0.03747                         | \$0.02856                        | \$0.01890                      | \$0.01823                     | Line 24 = Line 20 + Line 21           |
| Overnight                         | \$0.02984                         | \$0.02251                        | \$0.01550                      | \$0.01512                     | Line 25 = Line 21                     |
| TOU kWh Weighted Average (Note 5) | \$0.05568                         | \$0.04249                        | \$0.02657                      | \$0.02526                     | Line 26                               |
| Check with Class Average DFC      | \$0.00000                         | \$0.00001                        | \$0.00000                      | \$0.00000                     | Line 27 = Line 26 - Line 1            |

(The source shows the weighted average for MFNH as \$0.04249 and the check as \$0.00001, i.e., a one-unit rounding difference from the \$0.04248 class average; no other class differs.)

<!-- EPON: profile,fixed-vs-volumetric — revenue neutrality is verified only at the class-average load shape: TOU rates weighted by the class's own kWh shares (Lines 7–10) reproduce the flat class DFC -->

Notes:

1. These are the 2026 DFCs by delivery class shown in ComEd Ex. 2.02.
2. From Lines 7 through 10 of the 5_DTOU kWhs tab.
3. From Lines 27 through 29 of the 2_DTOU DFC RevResp tab.
4. Arrange kWhs by TOU period in Section C to kWhs by System Loading Categories in accordance with the chart shown in Section G2.
5. The TOU kWh Weighted Average DFC is computed by applying the DFC for each TOU period for each delivery class shown in Lines 22 through 25 by the percentage [source says "parentage"] of kWh of the TOU period in Lines 7 through 10, i.e., Sumproduct (Line 22 : Line 25, Line 7 : Line 10).

---

## Tab 2: `2_DTOU DFC RevResp` (pp. 4–5)

**The Development of Allocation Factors for Allocating Distribution Facilities Costs by Sub-function to System High, System Moderate, and System Base Loading Categories — Illustrative Example**

### Page 4 of 9

**Section A. Distribution Facilities Charge (DFC) Revenue Responsibilities** (Note 1, under page 5)

|                            | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line   |
| -------------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------ |
| DFC Revenue Responsibility | \$1,116,703,608                   | \$213,738,282                    | \$17,927,965                   | \$39,883,934                  | Line 1 |

(The MFNH figure here is \$213,738,282; the same quantity on Tab 1 Section F, Line 15 shows \$213,738,283.)

**Section B. Distribution Facilities Cost by Sub-function** (Note 2, under page 5)

| Sub-functions                                     | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                   |
| ------------------------------------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | -------------------------------- |
| High Voltage Dist. Substations                    | \$170,545,645                     | \$33,026,797                     | \$2,272,831                    | \$4,750,642                   | Line 2                           |
| High Voltage Dist. Lines                          | \$30,779,633                      | \$5,960,590                      | \$410,195                      | \$857,384                     | Line 3                           |
| Shared Distribution Substations (At or Below 4kV) | \$1,223,431                       | \$236,922                        | \$16,304                       | \$34,079                      | Line 4                           |
| Shared Distribution Substations (Over 4kV)        | \$20,251,301                      | \$3,921,739                      | \$269,885                      | \$564,111                     | Line 5                           |
| Secondary Voltage Dist. Substations               | \$30,177,863                      | \$5,949,796                      | \$933,630                      | \$2,343,006                   | Line 6                           |
| Shared Distribution Lines (At or Below 4kV)       | \$28,775,085                      | \$5,572,402                      | \$383,480                      | \$801,546                     | Line 7                           |
| Shared Distribution Lines (Over 4kV)              | \$677,446,671                     | \$131,546,977                    | \$9,154,932                    | \$19,187,956                  | Line 8                           |
| Secondary Voltage Dist. Lines                     | \$105,173,757                     | \$17,361,193                     | \$2,707,627                    | \$6,836,773                   | Line 9                           |
| Primary Voltage Transformers                      | \$0                               | \$0                              | \$0                            | \$0                           | Line 10                          |
| Secondary Voltage Transformers                    | \$63,339,997                      | \$12,487,963                     | \$1,959,585                    | \$4,917,710                   | Line 11                          |
| Total                                             | \$1,127,713,383                   | \$216,064,379                    | \$18,108,469                   | \$40,293,207                  | Line 12 = Sum (Line 2 : Line 11) |

**Section C. System Loading Categories**

| System Loading Category | Description                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------- |
| System High             | Costs of distribution equipment required to deliver power to a heavily loaded grid    |
| System Moderate         | Costs of distribution equipment required to deliver power to a moderately loaded grid |
| System Base             | Costs of baseline equipment required to deliver power                                 |

**Section D. Allocation Factors for Allocating Distribution Facilities Cost by Sub-function to System Loading Categories**

<!-- EPON: midday-peak,stacking,profile — allocation of distribution cost to System High/Moderate/Base by sub-function: all substation and high-voltage items use the feeder-peak split 76% / 22% / 2%; shared distribution lines use plant/feeder-peak 30% / 9% / 61%; secondary lines and transformers are 100% System Base -->

| Sub-function                                      | Allocation Factors (basis) | System High % | System Moderate % | System Base % | System Total | Line    |
| ------------------------------------------------- | -------------------------- | ------------- | ----------------- | ------------- | ------------ | ------- |
| High Voltage Dist. Substations                    | Feeder Peak (Note 3)       | 76%           | 22%               | 2%            | 100%         | Line 13 |
| High Voltage Dist. Lines                          | Feeder Peak (Note 3)       | 76%           | 22%               | 2%            | 100%         | Line 14 |
| Shared Distribution Substations (At or Below 4kV) | Feeder Peak (Note 3)       | 76%           | 22%               | 2%            | 100%         | Line 15 |
| Shared Distribution Substations (Over 4kV)        | Feeder Peak (Note 3)       | 76%           | 22%               | 2%            | 100%         | Line 16 |
| Secondary Voltage Dist. Substations               | Feeder Peak (Note 3)       | 76%           | 22%               | 2%            | 100%         | Line 17 |
| Shared Distribution Lines (At or Below 4kV)       | Plant/Feeder Peak (Note 4) | 30%           | 9%                | 61%           | 100%         | Line 18 |
| Shared Distribution Lines (Over 4kV)              | Plant/Feeder Peak (Note 4) | 30%           | 9%                | 61%           | 100%         | Line 19 |
| Secondary Voltage Dist. Lines                     | Base Delivery (Note 5)     | 0%            | 0%                | 100%          | 100%         | Line 20 |
| Primary Voltage Transformers                      | Base Delivery (Note 5)     | 0%            | 0%                | 100%          | 100%         | Line 21 |
| Secondary Voltage Transformers                    | Base Delivery (Note 5)     | 0%            | 0%                | 100%          | 100%         | Line 22 |

### Page 5 of 9

**Section E. Compute Distribution Facilities Costs by System Loading Category** (Note 6)

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                   |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | -------------------------------- |
| System High             | \$404,129,710                     | \$78,448,655                     | \$5,827,686                    | \$12,494,259                  | Line 23                          |
| System Moderate         | \$119,215,090                     | \$23,141,830                     | \$1,717,083                    | \$3,679,884                   | Line 24                          |
| System Base             | \$604,368,583                     | \$114,473,894                    | \$10,563,700                   | \$24,119,064                  | Line 25                          |
| Total                   | \$1,127,713,383                   | \$216,064,379                    | \$18,108,469                   | \$40,293,207                  | Line 26 = Sum (Line 23: Line 25) |

**Section F. Compute DFC Revenue Responsibility by System Loading Category** (Note 7)

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                       |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------------------------------------ |
| System High             | \$400,184,224                     | \$77,604,096                     | \$5,769,596                    | \$12,367,350                  | Line 27 = Line 1*(Line 23 / Line 26) |
| System Moderate         | \$118,051,203                     | \$22,892,691                     | \$1,699,967                    | \$3,642,506                   | Line 28 = Line 1*(Line 24 / Line 26) |
| System Base             | \$598,468,181                     | \$113,241,496                    | \$10,458,402                   | \$23,874,078                  | Line 29 = Line 1*(Line 25 / Line 26) |
| Total                   | \$1,116,703,608                   | \$213,738,283                    | \$17,927,965                   | \$39,883,934                  | Line 30 = Sum (Line 27: Line 29)     |

Notes (Tab 2; apply to Sections A–F on pages 4–5):

1. See the 2026 DFC Revenue by delivery class in ComEd Ex. 2.02, col. (J).
2. ComEd Ex. 2.01 (2026 Embedded Cost of Service Study), Schedule 2a. (Allocation), Lines 244-253.
3. From the Allocation Factors row in the table starting in Section C of the 3_Feeder Peak tab. The costs of the distribution sub-functions other than the Shared Distribution Lines are allocated based on the percentage of the average feeder peaks in 2022 and 2023 for each of the 24 hours and the assignment of these hours to System Categories.
4. From the Allocation Factors for Shared Distribution Lines in Section C of the 4_Shared Distribution Lines tab.
5. Local transformation and secondary distribution lines are 100% base distribution facilities.
6. The Distribution Costs for each System Category are computed by applying the Allocation Factors by sub-function for the System Category shown in Line 13 through Line 22 to the Distribution Facilities Costs by sub-function for the delivery class shown in Line 2 through Line 11. For example, the costs for Line 23, System High, for a Delivery Class = Sumproduct (Line 2 : Line 11 costs for the Delivery Class, Line 13 : Line 22 allocation factors under the System High % column).
7. These DFC Revenue Responsibility by System Category and Delivery Class are used in the table starting in Section F of the 1_DTOU DFC Rates tab.

---

## Tab 3: `3_Feeder Peak` (pp. 6–7)

**The Development of the Allocation Factors for Distribution Facilities Costs by Sub-function — Feeder Peak Hour Data — Illustrative Example**

### Page 6 of 9

Time of Use Periods header table (repeated on this tab):

| Time of Use Period | Hours         | Hour Ending |
| ------------------ | ------------- | ----------- |
| Morning            | 6 am to 1 pm  | 7-13        |
| Mid-Day Peak       | 1 pm to 7 pm  | 14-19       |
| Evening            | 7 pm to 11 pm | 20-23       |
| Overnight          | 11 pm to 6 am | 1-6, 24     |

**A.** During 2022 and 2023, there were approximately 5,500 feeders in ComEd's service area.

**B.** The following table shows the frequency of feeders reaching the feeder maximum load in 24 hourly periods in 2022 and 2023:

<!-- EPON: profile,midday-peak — feeder-peak hour data that sets the 76% System High share: counts of ~5,500 feeders hitting annual max load by hour-ending, 2022 and 2023; peak hours are HE17 (1,138 avg feeders, 20.67%) and HE18 (1,028, 18.68%); HE14–19 total 76% -->

Column labels (from the source): (A) Hour Ending; (B) 2022 Feeder Count; (C) 2023 Feeder Count; (D) = Avg ((B):(C)) = 2022-2023 Average Feeder Count; (E) % Feeder Count; (F) % Feeder Count in TOU Periods. Column (F) is a merged cell per TOU period in the source (shown here in the last column, on every row of the block; merged-cell blocks: hour ending 24, 1–6 = Overnight 2%; 7–13 = Morning 17%; 14–19 = Mid-Day Peak 76%; 20–23 = Evening 5%). The source lists hour ending 24 first, then 1 through 23.

| Hour Ending (A) | 2022 Feeder Count (B) | 2023 Feeder Count (C) | 2022-2023 Average Feeder Count (D) | % Feeder Count (E) | % Feeder Count in TOU Periods (F) |
| --------------- | --------------------- | --------------------- | ---------------------------------- | ------------------ | --------------------------------- |
| 24              | 1                     | -                     | 0.5                                | 0.01%              | 2% (Overnight)                    |
| 1               | 3                     | 1                     | 2.0                                | 0.04%              | 2% (Overnight)                    |
| 2               | -                     | -                     | -                                  | 0.00%              | 2% (Overnight)                    |
| 3               | -                     | -                     | -                                  | 0.00%              | 2% (Overnight)                    |
| 4               | -                     | -                     | -                                  | 0.00%              | 2% (Overnight)                    |
| 5               | 18                    | 41                    | 29.5                               | 0.54%              | 2% (Overnight)                    |
| 6               | 24                    | 98                    | 61.0                               | 1.11%              | 2% (Overnight)                    |
| 7               | 47                    | 35                    | 41.0                               | 0.74%              | 17% (Morning)                     |
| 8               | 136                   | 54                    | 95.0                               | 1.73%              | 17% (Morning)                     |
| 9               | 146                   | 72                    | 109.0                              | 1.98%              | 17% (Morning)                     |
| 10              | 163                   | 57                    | 110.0                              | 2.00%              | 17% (Morning)                     |
| 11              | 183                   | 123                   | 153.0                              | 2.78%              | 17% (Morning)                     |
| 12              | 241                   | 177                   | 209.0                              | 3.80%              | 17% (Morning)                     |
| 13              | 235                   | 211                   | 223.0                              | 4.05%              | 17% (Morning)                     |
| 14              | 362                   | 427                   | 394.5                              | 7.17%              | 76% (Mid-Day Peak)                |
| 15              | 376                   | 573                   | 474.5                              | 8.62%              | 76% (Mid-Day Peak)                |
| 16              | 483                   | 984                   | 733.5                              | 13.33%             | 76% (Mid-Day Peak)                |
| 17              | 880                   | 1,396                 | 1,138.0                            | 20.67%             | 76% (Mid-Day Peak)                |
| 18              | 1,299                 | 757                   | 1,028.0                            | 18.68%             | 76% (Mid-Day Peak)                |
| 19              | 590                   | 244                   | 417.0                              | 7.58%              | 76% (Mid-Day Peak)                |
| 20              | 167                   | 154                   | 160.5                              | 2.92%              | 5% (Evening)                      |
| 21              | 102                   | 83                    | 92.5                               | 1.68%              | 5% (Evening)                      |
| 22              | 53                    | 13                    | 33.0                               | 0.60%              | 5% (Evening)                      |
| 23              | -                     | -                     | -                                  | 0.00%              | 5% (Evening)                      |
| Total           | 5,509                 | 5,500                 | 5,505                              | 100.00%            | 100%                              |

[DIAGRAM DESCRIPTION: 2022 - 2023 Average Feeder Count]

A blue bar chart at the right of the table: x-axis hour ending 1–24, y-axis "2022 - 2023 Average Feeder Count" from 0 to 1,200.0 in steps of 200; legend "2022 - 2023 Average Feeder Count". Bars are near zero for hours 1–6, climb gradually through the morning (about 41–223 in hours 7–13), then jump through the afternoon (about 395, 475 and 734 in hours 14–16) to a maximum of about 1,138 in hour 17 and about 1,028 in hour 18, then fall to about 417 in hour 19 and about 160, 93 and 33 in hours 20–22 and zero in hour 23 — i.e., the same values as column (D) of the table. [→ See original PDF page 6 for visual rendering]

### Page 7 of 9

**C.** The following table shows the average frequency of feeders reaching the feeder maximum load in 2022 and 2023 during the four TOU Periods and the assignment of the TOU Periods to System Loading Categories:

<!-- EPON: midday-peak,stacking — feeder peaks by TOU period assigned to System Loading categories: Morning+Evening = System Moderate (17%+5% = 22%), Mid-Day Peak = System High (76%), Overnight = System Base (2%) -->

| TOU Period   | Feeder Count | % of Feeders | System Loading Category     | System High % | System Moderate % | System Base % |
| ------------ | ------------ | ------------ | --------------------------- | ------------- | ----------------- | ------------- |
| Morning      | 940          | 17%          | System Moderate             |               | 17%               |               |
| Mid-Day Peak | 4,186        | 76%          | System High                 | 76%           |                   |               |
| Evening      | 286          | 5%           | System Moderate             |               | 5%                |               |
| Overnight    | 93           | 2%           | System Base                 |               |                   | 2%            |
| Total        | 5,505        | 100%         | Allocation Factors (Note 1) | 76%           | 22%               | 2%            |

**D.** The following table shows the frequency of feeders reaching the feeder maximum load in 2022 and 2023 during three TOU Periods and the assignment of the TOU Periods to System Loading Categories:

| TOU Period   | Feeder Count | % of Feeders | System Loading Category     | System High % | System Moderate % |
| ------------ | ------------ | ------------ | --------------------------- | ------------- | ----------------- |
| Morning      | 940          | 17.4%        | System Moderate             |               | 17.4%             |
| Mid-Day Peak | 4,186        | 77.3%        | System High                 | 77.3%         |                   |
| Evening      | 286          | 5.3%         | System Moderate             |               | 5.3%              |
| Total        | 5,412        | 100%         | Allocation Factors (Note 2) | 77%           | 23%               |

Notes:

1. These allocation factors are used to allocate the costs of the High Voltage Distribution Substations, High Voltage Distribution Lines, Shared Distribution Substations, and Secondary Voltage Distribution Substations sub-functions. See the allocation of these costs to the System Categories in the table starting in Section D of the 2_DTOU DFC RevResp tab.
2. These allocation factors are restated in the table starting in Section B of the 4_Shared Distribution Lines tab. In there, these allocation factors are used to allocate the costs assigned to System Loading (i.e., System High and System Moderate) to System High and System Moderate individually. See the table starting in Section C [source says "Second C"] of the 4_Shared Distribution Lines tab.

---

## Tab 4: `4_Shared Distrubution Lines` (p. 8) [tab name as in source]

**The Development of the Allocation Factors for Shared Distribution Lines — Illustrative Example**

### Page 8 of 9

Time of Use Periods header table (repeated on this tab; identical to Tab 3: Morning 6 am to 1 pm, HE 7-13; Mid-Day Peak 1 pm to 7 pm, HE 14-19; Evening 7 pm to 11 pm, HE 20-23; Overnight 11 pm to 6 am, HE 1-6, 24).

**Section A. Plant-in Service Data** (Note 1)

Column labels: (A) FERC Account; (B) Account Description; (C) Plant in Service; (D) % of Total; (E) and (F) = "Allocation Factor (Note 2)": System Loaded (Moderate and High) and System Base; (G) = (D) * (E) and (H) = (D) * (F) = "Shared Distribution Line": System Loaded (Moderate and High) and System Base.

| FERC Account (A)                         | Account Description (B)            | Plant in Service (C) | % of Total (D) | Alloc. Factor: System Loaded (Moderate and High) (E) | Alloc. Factor: System Base (F) | Shared Dist. Line: System Loaded (G) = (D) * (E) | Shared Dist. Line: System Base (H) = (D) * (F) | Line                           |
| ---------------------------------------- | ---------------------------------- | -------------------- | -------------- | ---------------------------------------------------- | ------------------------------ | ------------------------------------------------ | ---------------------------------------------- | ------------------------------ |
| 364                                      | Poles, Towers, and Fixtures        | \$3,510,828,908      | 18.4%          | 0%                                                   | 100%                           | 0.0%                                             | 18.4%                                          | Line 1                         |
| 365                                      | Overhead Conductors and Devices    | \$5,178,335,506      | 27.1%          | 24%                                                  | 76%                            | 6.5%                                             | 20.6%                                          | Line 2                         |
| 366                                      | Underground Conduit                | \$1,188,740,550      | 6.2%           | 0%                                                   | 100%                           | 0.0%                                             | 6.2%                                           | Line 3                         |
| 367                                      | Underground Conductors and Devices | \$9,238,804,836      | 48.3%          | 67%                                                  | 33%                            | 32.4%                                            | 15.9%                                          | Line 4                         |
| Shared Distribution Line (Accts 364-367) |                                    | \$19,116,709,800     | 100.0%         |                                                      |                                | 39%                                              | 61%                                            | Line 5 = Sum (Line 1 : Line 4) |

(The Line 5 total row's "to Section B" and "to Section C" arrows in the source point from the 39% and 61% cells to Sections B and C respectively.)

**Section B. Allocate the System Loading (Moderate and High) between System High and System Moderate**

| (A) System Loaded (Moderate and High) | (B) Allocation Factor: System High % | (C) Allocation Factor: System Moderate % | (D) = (A) * (B): System High % | (E) = (A) * (C): System Moderate % | Line   |
| ------------------------------------- | ------------------------------------ | ---------------------------------------- | ------------------------------ | ---------------------------------- | ------ |
| 39%                                   | 77%                                  | 23%                                      | 30%                            | 9%                                 | Line 6 |

(Note 3 applies to the allocation factors in (B) and (C).)

**Section C. Allocation Factors for Shared Distribution Lines by Sub-function to System Categories** (Note 4)

<!-- EPON: midday-peak,stacking — shared distribution lines allocated 30% System High (Mid-Day Peak only), 9% System Moderate, 61% System Base (all hours) -->

| System High % | System Moderate % | System Base | Line / formula             |
| ------------- | ----------------- | ----------- | -------------------------- |
| 30%           | 9%                | 61%         | Line 7 = Line 5 and Line 6 |

Notes:

1. ComEd Ex. 2.01 (2026 Embedded Cost of Service Study), Schedule 1a. (Function), Lines 18-21.
2. Accounts 364 and 366 are allocated to System Base. The allocation factors for Accounts 365 and 367 to System Loading (Moderate and High) and System Base are determined in the WP_Accts 365 and 367 workpaper.
3. See the Allocation Factors row in the table starting in Section D of the 3_Feeder Peak tab.
4. These allocation factors are used to allocate the costs of the Shared Distribution Lines sub-functions. See the allocation of these costs to the System Categories in the table starting in Section D of the 2_DTOU DFC RevResp tab.

---

## Tab 5: `5_DTOU kWhs` (p. 9)

**The Development of Annual Billed kWh by DTOU Period by Delivery Class — Illustrative Example**

### Page 9 of 9

Time of Use Periods header table (repeated on this tab; same as Tab 3).

**Section A. 2026 Annual Billed kWh by Delivery Classes** (Note 1)

|                        | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line   |
| ---------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------ |
| 2026 annual billed kWh | 20,055,740,094                    | 5,031,503,822                    | 674,744,649                    | 1,578,936,429                 | Line 1 |

**Section B. 2021 Annual Average Per Customer kWh by DTOU Period by Residential Delivery Class** (Note 2)

<!-- EPON: profile,ev-hp,midday-peak — the load-shape input to DTOU rate design: 2021 AVERAGE per-customer annual kWh by period and class (not electrified-home or heat-pump specific); electric-space-heat customers use about twice the kWh of non-heat customers (SFH 18,926 vs SFNH 9,183 kWh/yr), with Mid-Day Peak 26.35% vs 30.56% of kWh -->

| DTOU Period  | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                 |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------------------------------ |
| Morning      | 2,430                             | 1,155                            | 5,649                          | 2,696                         | Line 2                         |
| Mid-Day Peak | 2,807                             | 1,197                            | 4,987                          | 2,411                         | Line 3                         |
| Evening      | 1,844                             | 837                              | 3,392                          | 1,688                         | Line 4                         |
| Overnight    | 2,103                             | 1,051                            | 4,898                          | 2,355                         | Line 5                         |
| Total        | 9,183                             | 4,238                            | 18,926                         | 9,150                         | Line 6 = Sum (Line 2 : Line 5) |

**Section C. Compute 2026 Delivery Class Annual Billed kWh by DTOU Period** (Note 3)

| DTOU Period  | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                       |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------------------------------------ |
| Morning      | 5,306,933,486                     | 1,370,864,294                    | 201,417,739                    | 465,266,160                   | Line 7 = Line 1 * (Line 2 / Line 6)  |
| Mid-Day Peak | 6,129,549,262                     | 1,420,394,572                    | 177,787,988                    | 416,019,068                   | Line 8 = Line 1 * (Line 3 / Line 6)  |
| Evening      | 4,026,635,272                     | 993,077,851                      | 120,921,719                    | 291,317,516                   | Line 9 = Line 1 * (Line 4 / Line 6)  |
| Overnight    | 4,592,622,074                     | 1,247,167,105                    | 174,617,202                    | 406,333,685                   | Line 10 = Line 1 * (Line 5 / Line 6) |
| Total        | 20,055,740,094                    | 5,031,503,822                    | 674,744,648                    | 1,578,936,429                 | Line 11 = Sum (Line 7 : Line 10)     |

(In the source, Section A shows the SFH annual total as 674,744,649 while the Section C total shows 674,744,648, a one-kWh rounding difference.)

Notes:

1. These are the 2026 annual billed kWhs by delivery class used to determine the 2026 Delivery Service Charges in ComEd Ex. 2.02.
2. The 8,760 hourly average use per customer for 2021 provided in the WP_Load Profiles workpaper are grouped in the Morning, Mid-Day Peak, Evening, and Overnight DTOU periods.
3. These 2026 Delivery Class Annual Billed kWh by DTOU Period [source says "D TOU Period"] are used in the table starting in Section C of the 1_DTOU DFC Rates tab.
