# ComEd Ex. 6.03 — Illustrative TOU Distribution Rate, 10 pm Overnight Version (Rebuttal Phase, Aug. 2024)

**Source**: `icc_620687_dtou_illustrative_10pm_overnight_rebuttal_rdi.pdf` (ICC e-docket file id / filing id 620687)
**Pages**: 11 (five workbook tabs rendered to PDF: tab 1 on pp. 1–5, tab 2 on pp. 6–7, tab 3 on pp. 8–9, tab 4 on p. 10, tab 5 on p. 11)
**Date**: August 2024 (rebuttal phase; the date is printed at the foot of every page as "August 2024")
**Docket**: ICC Docket No. 24-0378 (Commonwealth Edison Co., revenue-neutral tariff changes related to rate design — Rate BEST / DTOU) — initial RDI phase, rebuttal testimony attachment
**Author(s)**: Commonwealth Edison Company (a rebuttal exhibit accompanying ComEd Ex. 6.0, Rebuttal Testimony of Kathleen E. Kremer; the sheet itself names no witness)
**Document type**: Exhibit — spreadsheet rendered to PDF (workbook titled "Illustrative TOU D Rate 10 pm Overnight" [sic; the rendered label reads "llustrative TOU D Rate 10 pm Overnight", missing the initial "I"]), five tabs
**ComEd exhibit no.**: ComEd Ex. 6.03 (identified by the stamp "ICC Docket No. 24-0378 / ComEd Ex. 6.03 / Page N of 11")
**Extraction method**: Embedded PDF text (PyMuPDF), every table and column count verified against rendered page images
**Extraction notes**:

- _Minor typographical errors in the source have been corrected for readability. Substantive corrections are annotated inline._ The workbook's own tab name "4_Shared Distrubution Lines" is reproduced exactly as in the source.
- Each page of the render carries the page header ("Commonwealth Edison Company / [tab-specific title] / Illustrative Example"), the right-hand label "llustrative TOU D Rate 10 pm Overnight / Tab: <tab name>", the foot label "August 2024", and the exhibit stamp "ICC Docket No. 24-0378 / ComEd Ex. 6.03 / Page N of 11". The tab name and page number are given in each page heading below; the rest of the repeated header, foot label and stamp are omitted after being stated once here.
- The spreadsheet's "Line No." labels and formula text appear to the right of each row in the source; they are kept as a final **Line / formula** column. The class columns in every table are, in order: **SFNH** (Single Family, No Elec. Space Heat), **MFNH** (Multi Family, No Elec. Space Heat), **SFH** (Single Family, Elec. Space Heat), **MFH** (Multi Family, Elec. Space Heat); source column headers are written out in full in each table.
- Cell colors in the source (yellow = Morning, red/pink = Mid-Day Peak, light blue = Evening, green = Overnight; red/orange/green = System High/Moderate/Base) are conveyed by the row labels.
- Notes blocks (1), (2), … are reproduced as "Notes" lines under the tab they belong to (no separate Footnotes section).
- Dollar signs are escaped as `\$`.

**Differences vs Ex. 3.04** (each item verified line-by-line against the initial-phase workbook, `icc_613758_ex_3_dtou_illustrative_rates_workbook.md`; identical items are listed last):

1. **Period boundaries (the purpose of this version).** Evening is **7 pm–10 pm** (hour ending 20–22) here vs 7 pm–11 pm (HE 20–23) in Ex. 3.04; Overnight is **10 pm–6 am** (HE 1–6, 23–24) here vs 11 pm–6 am (HE 1–6, 24). Morning (6 am–1 pm, HE 7–13) and Mid-Day Peak (1 pm–7 pm, HE 14–19) are unchanged. The tab label reads "10 pm Overnight".
2. **kWh by period shift from Evening to Overnight.** Morning and Mid-Day Peak kWh are identical to Ex. 3.04. Evening kWh fall (SFNH 4,026,635,272 → 3,123,172,662; MFNH 993,077,851 → 759,275,153; SFH 120,921,719 → 92,995,550; MFH 291,317,516 → 223,023,893) and Overnight kWh rise by the same amounts (SFNH 4,592,622,074 → 5,496,084,683; MFNH 1,247,167,105 → 1,480,969,803; SFH 174,617,202 → 202,543,372; MFH 406,333,685 → 474,627,308). Evening kWh share falls to 15.57% / 15.09% / 13.78% / 14.12% (from 20.08% / 19.74% / 17.92% / 18.45%); Overnight share rises to 27.40% / 29.42% / 30.02% / 30.06% (from 22.90% / 24.78% / 25.88% / 25.73%). This follows from the Tab 5 per-customer inputs (2021 average kWh): Evening 1,430 / 640 / 2,608 / 1,292 (from 1,844 / 837 / 3,392 / 1,688) and Overnight 2,516 / 1,248 / 5,681 / 2,750 (from 2,103 / 1,051 / 4,898 / 2,355). Rounding: SFNH annual total is 20,055,740,093 (vs ...094) and the SFNH and MFNH distribution totals display 99.99%.
3. **System Moderate kWh are smaller** (System Moderate = Morning + Mid-Day Peak + Evening): SFNH 14,559,655,410 (from 15,463,118,020); MFNH 3,550,534,019 (from 3,784,336,717); SFH 472,201,277 (from 500,127,446); MFH 1,104,309,121 (from 1,172,602,744). System High and System Base kWh and all DFC revenue responsibilities by loading category (Section F) are unchanged.
4. **System Moderate rate layer is higher** because the same revenue is spread over fewer kWh: \$0.00811 / \$0.00645 / \$0.00360 / \$0.00330 (from \$0.00763 / \$0.00605 / \$0.00340 / \$0.00311). System High and System Base layers are unchanged.
5. **Resulting DTOU rates (Section I) change for Morning, Mid-Day Peak and Evening; Overnight is unchanged.** Morning = Evening: \$0.03795 / \$0.02896 / \$0.01910 / \$0.01842 (from \$0.03747 / \$0.02856 / \$0.01890 / \$0.01823); Mid-Day Peak: \$0.10324 / \$0.08360 / \$0.05155 / \$0.04815 (from \$0.10276 / \$0.08320 / \$0.05135 / \$0.04796); Overnight unchanged at \$0.02984 / \$0.02251 / \$0.01550 / \$0.01512. The MFNH check line now reads \$0.00000 (Ex. 3.04: \$0.00001), and the Line 26 label reads "Load (in Lines 7-10) Weighted Average DFCs".
6. **New Sections J and K and new Note 6 (Staff Ex. 1.0 recommendations).** Page 4 adds a "Staff recommendation" scenario that keeps the Evening and Overnight DFCs at the Ex. 3.04 values and adds a revenue-neutralizing per-kWh adjustment (Line 28: \$0.00014 / \$0.00010 / \$0.00005 / \$0.00005) to the Morning and Mid-Day Peak DFCs, giving final rates in Section K (Lines 29–33, 35). Note 6 cites "Staff Ex. 1.0, 12:247-13:251". Ex. 3.04 has no equivalent.
7. **Tab 3 (Feeder Peak) table B** lists hour ending 23 first, shows Evening as HE 20–22, and its Total row (5,456 / 5,487 / 5,472) is **lower** than Ex. 3.04's (5,509 / 5,500 / 5,505) by exactly the hour-ending-22 counts (53, 13, 33.0); the per-hour counts are otherwise identical, and the "% Feeder Count" column uses the 5,472 denominator (e.g., HE17 20.80% vs 20.67%; HE18 18.79% vs 18.68%), while the TOU-period percentages in column (F) remain 2% / 17% / 76% / 5%. Sections C and D of Tab 3 (counts 940 / 4,186 / 286 / 93; total 5,505; allocation factors 76% / 22% / 2% and 77% / 23%) are **unchanged** from Ex. 3.04, so the allocation factors are not recomputed from the revised table. (HE 23 has zero feeder peaks, so moving it from Evening to Overnight does not change period feeder counts.)
8. **Format.** 11 pages vs 9 (the Section J/K page and a separate Notes page are added); header label, "August 2024" foot label, and stamp "ICC Docket No. 24-0378 / ComEd Ex. 6.03" replace the draft stamp "ICC Docket No. 24-____ / ComEd Ex. 3.04".
9. **Identical to Ex. 3.04:** 2026 flat class DFCs (Line 1); DFC revenue responsibilities by class and loading category (Sections F and Tab 2 Sections A, E, F); distribution facilities cost by sub-function (Tab 2 Section B); Tab 2 allocation factors; Tab 4 shared-distribution-line allocation (39% / 61%; 77% / 23%; 30% / 9% / 61%); Tab 5 Morning and Mid-Day Peak kWh; 2026 annual billed kWh by class. Minor wording differences in a few notes (e.g., "Section Cof" run-together in Tab 2 Note 4) are not substantive.

---

## Tab 1: `1_DTOU DFC Rates` (pp. 1–5)

**The Determination of the Time of Use Delivery Facilities Charges by Delivery Class — Illustrative Example**

### Page 1 of 11

**Section A. Delivery Service Time of Use (DTOU) Periods**

<!-- EPON: midday-peak — period definitions in the 10 pm-overnight version: Mid-Day Peak still 1 pm–7 pm (HE 14–19); Evening shortened to 7–10 pm; Overnight now 10 pm–6 am -->

| DTOU Period  | Hours         | Hour Ending |
| ------------ | ------------- | ----------- |
| Morning      | 6 am to 1 pm  | 7-13        |
| Mid-Day Peak | 1 pm to 7 pm  | 14-19       |
| Evening      | 7 pm to 10 pm | 20-22       |
| Overnight    | 10 pm to 6 am | 1-6, 23-24  |

**Section B. 2026 Average per kWh DFC by Delivery Class** (Note 1)

|                          | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line   |
| ------------------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------ |
| 2026 average per kWh DFC | \$0.05568                         | \$0.04248                        | \$0.02657                      | \$0.02526                     | Line 1 |

**Section C. 2026 Annual Billed kWh by DTOU Period and by Delivery Class** (Note 2)

<!-- EPON: profile,ev-hp — class kWh by period under the 10 pm boundary; the Evening/Overnight split is built from 2021 average customer load shapes; electric-space-heat classes carry the heaviest Overnight shares (30.02% SFH, 30.06% MFH) -->

| DTOU Period  | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                 |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------------------------------ |
| Morning      | 5,306,933,486                     | 1,370,864,294                    | 201,417,739                    | 465,266,160                   | Line 2                         |
| Mid-Day Peak | 6,129,549,262                     | 1,420,394,572                    | 177,787,988                    | 416,019,068                   | Line 3                         |
| Evening      | 3,123,172,662                     | 759,275,153                      | 92,995,550                     | 223,023,893                   | Line 4                         |
| Overnight    | 5,496,084,683                     | 1,480,969,803                    | 202,543,372                    | 474,627,308                   | Line 5                         |
| Total        | 20,055,740,093                    | 5,031,503,822                    | 674,744,649                    | 1,578,936,429                 | Line 6 = Sum (Line 2 : Line 5) |

**Section D. 2026 Annual Billed kWh Distribution by DTOU Period**

| DTOU Period  | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                   |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | -------------------------------- |
| Morning      | 26.46%                            | 27.25%                           | 29.85%                         | 29.47%                        | Line 7 = Line 2 / Line 6         |
| Mid-Day Peak | 30.56%                            | 28.23%                           | 26.35%                         | 26.35%                        | Line 8 = Line 3 / Line 6         |
| Evening      | 15.57%                            | 15.09%                           | 13.78%                         | 14.12%                        | Line 9 = Line 4 / Line 6         |
| Overnight    | 27.40%                            | 29.42%                           | 30.02%                         | 30.06%                        | Line 10 = Line 5 / Line 6        |
| Total        | 99.99%                            | 99.99%                           | 100.00%                        | 100.00%                       | Line 11 = Sum (Line 7 : Line 10) |

### Page 2 of 11

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

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                     |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ---------------------------------- |
| System High             | 6,129,549,262                     | 1,420,394,572                    | 177,787,988                    | 416,019,068                   | Line 16 = Line 3                   |
| System Moderate         | 14,559,655,410                    | 3,550,534,019                    | 472,201,277                    | 1,104,309,121                 | Line 17 = Line 2 + Line 3 + Line 4 |
| System Base             | 20,055,740,093                    | 5,031,503,822                    | 674,744,649                    | 1,578,936,429                 | Line 18 = Line 6                   |

**Section G2. Applicable kWh for each System Loading Category**

| System Categories | TOU Periods (col. 1) | TOU Periods (col. 2) | TOU Periods (col. 3) | TOU Periods (col. 4) |
| ----------------- | -------------------- | -------------------- | -------------------- | -------------------- |
| System High       |                      | Mid-Day Peak         |                      |                      |
| System Moderate   | Morning              | Mid-Day Peak         | Evening              |                      |
| System Base       | Morning              | Mid-Day Peak         | Evening              | Overnight            |

(The source shows a merged "TOU Periods" header over four unlabeled columns; cell colors place Morning, Mid-Day Peak, Evening and Overnight in columns 1–4.)

### Page 3 of 11

**Section H. Compute Per kWh DFC Revenue Responsibility by System Loading Category by Delivery Class**

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula              |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | --------------------------- |
| System High             | \$0.06529                         | \$0.05464                        | \$0.03245                      | \$0.02973                     | Line 19 = Line 12 / Line 16 |
| System Moderate         | \$0.00811                         | \$0.00645                        | \$0.00360                      | \$0.00330                     | Line 20 = Line 13 / Line 17 |
| System Base             | \$0.02984                         | \$0.02251                        | \$0.01550                      | \$0.01512                     | Line 21 = Line 14 / Line 18 |

**Section I. Compute Per kilowatt-hour (kWh) Distribution Facilities Charges (DFCs) by DTOU Period by Delivery Class**

<!-- EPON: ev-hp,midday-peak,stacking,fixed-vs-volumetric — DTOU rates by delivery class under the 10 pm boundary ($/kWh): Mid-Day Peak SFNH $0.10324 / MFNH $0.08360 / SFH (elec. space heat) $0.05155 / MFH $0.04815; Morning=Evening SFNH $0.03795 / MFNH $0.02896 / SFH $0.01910 / MFH $0.01842; Overnight SFNH $0.02984 / MFNH $0.02251 / SFH $0.01550 / MFH $0.01512; electric-space-heat classes pay lower per-kWh rates than no-heat classes in every period -->

| DTOU Period                       | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                                       |
| --------------------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ---------------------------------------------------- |
| Morning                           | \$0.03795                         | \$0.02896                        | \$0.01910                      | \$0.01842                     | Line 22 = Line 20 + Line 21                          |
| Mid-Day Peak                      | \$0.10324                         | \$0.08360                        | \$0.05155                      | \$0.04815                     | Line 23 = Line 19 + Line 20 + Line 21                |
| Evening                           | \$0.03795                         | \$0.02896                        | \$0.01910                      | \$0.01842                     | Line 24 = Line 20 + Line 21                          |
| Overnight                         | \$0.02984                         | \$0.02251                        | \$0.01550                      | \$0.01512                     | Line 25 = Line 21                                    |
| TOU kWh Weighted Average (Note 5) | \$0.05568                         | \$0.04248                        | \$0.02657                      | \$0.02526                     | Line 26 = Load (in Lines 7-10) Weighted Average DFCs |
| Check with Class Average DFC      | \$0.00000                         | \$0.00000                        | \$0.00000                      | \$0.00000                     | Line 27 = Line 26 - Line 1                           |

### Page 4 of 11

**Section J. Staff recommendation on maintaining the Evening Period and Overnight Period DFCs as determined in ComEd Ex. 3.04 requires an adjustment to the Morning Period and Mid-Day Peak Period DFCs** (Note 6)

<!-- EPON: midday-peak,fixed-vs-volumetric — Staff-recommendation scenario: Evening and Overnight DFCs held at Ex. 3.04 levels, so the Morning and Mid-Day Peak DFCs are raised by a small per-kWh adjustment to keep the class's flat DFC revenue-neutral -->

|            | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line    |
| ---------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------- |
| Adjustment | \$0.00014                         | \$0.00010                        | \$0.00005                      | \$0.00005                     | Line 28 |

**Section K. Compute Per kWh DFCs by Delivery Class with Staff Recommendations on maintaining the Evening Period and Overnigh Period [source says "Overnigh"] DFCs as determined in ComEd Ex. 3.04**

<!-- EPON: ev-hp,midday-peak,stacking,fixed-vs-volumetric — final DTOU rates in the Staff-recommendation scenario (Section K, $/kWh): Mid-Day Peak SFNH $0.10338 / MFNH $0.08370 / SFH $0.05160 / MFH $0.04820; Morning SFNH $0.03809 / MFNH $0.02906 / SFH $0.01915 / MFH $0.01847; Evening and Overnight as in Ex. 3.04 -->

| DTOU Period                  | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                                                                                               |
| ---------------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Morning                      | \$0.03809                         | \$0.02906                        | \$0.01915                      | \$0.01847                     | Line 29 = Line 22 + Line 28                                                                                  |
| Mid-Day Peak                 | \$0.10338                         | \$0.08370                        | \$0.05160                      | \$0.04820                     | Line 30 = Line 23 + Line 28                                                                                  |
| Evening                      | \$0.03747                         | \$0.02856                        | \$0.01890                      | \$0.01823                     | Line 31 = ComEd Ex. 3.04, Pg3, Ln 24                                                                         |
| Overnight                    | \$0.02984                         | \$0.02251                        | \$0.01550                      | \$0.01512                     | Line 32 = ComEd Ex. 3.04, Pg3, Ln 24 [sic; as in source — Overnight rate corresponds to Ex. 3.04 Pg 3 Ln 25] |
| TOU kWh Weighted Average     | \$0.05568                         | \$0.04248                        | \$0.02657                      | \$0.02526                     | Line 33 = Load (in Lines 7-10) Weighted Average DFCs                                                         |
| Check with Class Average DFC | \$0.00000                         | \$0.00000                        | \$0.00000                      | \$0.00000                     | Line 35 = Line 33 - Line 1                                                                                   |

(The source has no "Line 34" label; the check row is labeled Line 35. The source's check row shows \$0.00000 for every class.)

### Page 5 of 11

Page 5 contains only the Tab 1 notes (below the header "Section / Notes:").

Notes (Tab 1):

1. These are the 2026 DFCs by delivery class shown in ComEd Ex. 2.02.
2. From Lines 7 through 10 of the 5_DTOU kWhs tab.
3. From Lines 27 through 29 of the 2_DTOU DFC RevResp tab.
4. Arrange kWhs by TOU period in Section C to kWhs by System Loading Categories in accordance with the chart shown in Section G2.
5. The TOU kWh Weighted Average DFC is computed by applying the DFC for each TOU period for each delivery class shown in Lines 22 through 25 by the percentage [source says "parentage"] of kWh of the TOU period in Lines 7 through 10, i.e., Sumproduct (Line 22 : Line 25, Line 7 : Line 10).
6. These modifications to DFCs by time period are based on Staff recommendations in Staff Ex. 1.0, 12:247-13:251, while maintaining the same single rate DFC for the class. The Staff recommendations are:
   - (a) maintaining Evening and Overnight Period DFCs as determined in ComEd Ex. 3.04,
   - (b) DFC for morning period [source says "peirod"] higher than flat DFC, and
   - (c) Mid-Day Peak period DFCs are higher than the level determined in ComEd Ex. 3.04.

   By maintaining the same DFCs determined for the Evening and Overnight Periods, an adjustment to the DFC for the Morning and/or the Mid-Day Peak Period is necessary. Section J provides an adjustment amount to be applied to the Morning Period and the Mid-Day Peak Period and Section K shows the result with this adjustment included in the DFCs for the Morning Period and the Mid-Day Peak Period.

---

## Tab 2: `2_DTOU DFC RevResp` (pp. 6–7)

**The Development of Allocation Factors for Allocating Distribution Facilities Costs by Sub-function to System High, System Moderate, and System Base Loading Categories — Illustrative Example**

### Page 6 of 11

**Section A. Distribution Facilities Charge (DFC) Revenue Responsibilities** (Note 1, under page 7)

|                            | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line   |
| -------------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------ |
| DFC Revenue Responsibility | \$1,116,703,608                   | \$213,738,282                    | \$17,927,965                   | \$39,883,934                  | Line 1 |

**Section B. Distribution Facilities Cost by Sub-function** (Note 2, under page 7)

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
| System Base             | Costs of baseline equipment required to deliver power.                                |

**Section D. Allocation Factors for Allocating Distribution Facilities Cost by Sub-function to System Loading Categories**

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

### Page 7 of 11

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

Notes (Tab 2; apply to Sections A–F on pages 6–7):

1. See the 2026 DFC Revenue by delivery class in ComEd Ex. 2.02, col. (J).
2. ComEd Ex. 2.01 (2026 Embedded Cost of Service Study), Schedule 2a. (Allocation), Lines 244-253.
3. From the Allocation Factors row in the table starting in Section C of the 3_Feeder Peak tab. The costs of the distribution sub-functions other than the Shared Distribution Lines are allocated based on the percentage of the average feeder peaks in 2022 and 2023 for each of the 24 hours and the assignment of these hours to System Categories.
4. From the Allocation Factors for Shared Distribution Lines in Section C of the 4_Shared Distribution Lines tab.
5. Local transformation and secondary distribution lines are 100% base distribution facilities.
6. The Distribution Costs for each System Category are computed by applying the Allocation Factors by sub-function for the System Category shown in Line 13 through Line 22 to the Distribution Facilities Costs by sub-function for the delivery class shown in Line 2 through Line 11. For example, the costs for Line 23, System High, for a Delivery Class = Sumproduct (Line 2 : Line 11 costs for the Delivery Class, Line 13 : Line 22 allocation factors under the System High % column).
7. These DFC Revenue Responsibility by System Category and Delivery Class are used in the table starting in Section F of the 1_DTOU DFC Rates tab.

---

## Tab 3: `3_Feeder Peak` (pp. 8–9)

**The Development of the Allocation Factors for Distribution Facilities Costs by Sub-function — Feeder Peak Hour Data — Illustrative Example**

### Page 8 of 11

Time of Use Periods header table (repeated on this tab):

| Time of Use Period | Hours         | Hour Ending |
| ------------------ | ------------- | ----------- |
| Morning            | 6 am to 1 pm  | 7-13        |
| Mid-Day Peak       | 1 pm to 7 pm  | 14-19       |
| Evening            | 7 pm to 10 pm | 20-22       |
| Overnight          | 10 pm to 6 am | 1-6, 23-24  |

**A.** During 2022 and 2023, there were approximately 5,500 feeders in ComEd's service area.

**B.** The following table shows the frequency of feeders reaching the feeder maximum load in 24 hourly periods in 2022 and 2023:

<!-- EPON: profile,midday-peak — same feeder-peak data as Ex. 3.04 (Mid-Day Peak HE14–19 = 76%; HE17 20.80%, HE18 18.79%) but with a changed Total row/denominator and hour 23 re-assigned to Overnight; allocation factors in Section C are not recomputed -->

Column labels (from the source): (A) Hour Ending; (B) 2022 Feeder Count; (C) 2023 Feeder Count; (D) = Avg ((B):(C)) = 2022 - 2023 Average Feeder Count; (E) % Feeder Count; (F) % Feeder Count in TOU Periods. Column (F) is a merged cell per TOU period in the source (shown here on every row of the block; merged-cell blocks: hour ending 23, 24, 1–6 = Overnight 2%; 7–13 = Morning 17%; 14–19 = Mid-Day Peak 76%; 20–22 = Evening 5%). The source lists hour ending 23 first, then 24, then 1 through 22.

| Hour Ending (A) | 2022 Feeder Count (B) | 2023 Feeder Count (C) | 2022 - 2023 Average Feeder Count (D) | % Feeder Count (E) | % Feeder Count in TOU Periods (F) |
| --------------- | --------------------- | --------------------- | ------------------------------------ | ------------------ | --------------------------------- |
| 23              | -                     | -                     | -                                    | 0.00%              | 2% (Overnight)                    |
| 24              | 1                     | -                     | 0.5                                  | 0.01%              | 2% (Overnight)                    |
| 1               | 3                     | 1                     | 2.0                                  | 0.04%              | 2% (Overnight)                    |
| 2               | -                     | -                     | -                                    | 0.00%              | 2% (Overnight)                    |
| 3               | -                     | -                     | -                                    | 0.00%              | 2% (Overnight)                    |
| 4               | -                     | -                     | -                                    | 0.00%              | 2% (Overnight)                    |
| 5               | 18                    | 41                    | 29.5                                 | 0.54%              | 2% (Overnight)                    |
| 6               | 24                    | 98                    | 61.0                                 | 1.11%              | 2% (Overnight)                    |
| 7               | 47                    | 35                    | 41.0                                 | 0.75%              | 17% (Morning)                     |
| 8               | 136                   | 54                    | 95.0                                 | 1.74%              | 17% (Morning)                     |
| 9               | 146                   | 72                    | 109.0                                | 1.99%              | 17% (Morning)                     |
| 10              | 163                   | 57                    | 110.0                                | 2.01%              | 17% (Morning)                     |
| 11              | 183                   | 123                   | 153.0                                | 2.80%              | 17% (Morning)                     |
| 12              | 241                   | 177                   | 209.0                                | 3.82%              | 17% (Morning)                     |
| 13              | 235                   | 211                   | 223.0                                | 4.08%              | 17% (Morning)                     |
| 14              | 362                   | 427                   | 394.5                                | 7.21%              | 76% (Mid-Day Peak)                |
| 15              | 376                   | 573                   | 474.5                                | 8.67%              | 76% (Mid-Day Peak)                |
| 16              | 483                   | 984                   | 733.5                                | 13.41%             | 76% (Mid-Day Peak)                |
| 17              | 880                   | 1,396                 | 1,138.0                              | 20.80%             | 76% (Mid-Day Peak)                |
| 18              | 1,299                 | 757                   | 1,028.0                              | 18.79%             | 76% (Mid-Day Peak)                |
| 19              | 590                   | 244                   | 417.0                                | 7.62%              | 76% (Mid-Day Peak)                |
| 20              | 167                   | 154                   | 160.5                                | 2.93%              | 5% (Evening)                      |
| 21              | 102                   | 83                    | 92.5                                 | 1.69%              | 5% (Evening)                      |
| 22              | 53                    | 13                    | 33.0                                 | 0.60%              | 5% (Evening)                      |
| Total           | 5,456                 | 5,487                 | 5,472                                | 100.00%            | 100%                              |

[DIAGRAM DESCRIPTION: 2022 - 2023 Average Feeder Count]

A blue bar chart at the right of the table: x-axis hour ending 1–24, y-axis "2022 - 2023 Average Feeder Count" from 0 to 1,200.0 in steps of 200; legend "2022 - 2023 Average Feeder Count". Same shape as in Ex. 3.04: small bars for hours 1–6 (hour ending 5 and 6 are 29.5 and 61.0; hours 1–4 are near zero), a gradual morning rise, a sharp afternoon climb to a maximum of about 1,138 at hour 17 and about 1,028 at hour 18, then a fall to about 417 at hour 19 and about 160, 93 and 33 at hours 20–22. [→ See original PDF page 8 for visual rendering]

### Page 9 of 11

**C.** The following table shows the average frequency of feeders reaching the feeder maximum load in 2022 and 2023 during the four TOU Periods and the assignment of the TOU Periods to System Loading Categories:

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

## Tab 4: `4_Shared Distrubution Lines` (p. 10) [tab name as in source]

**The Development of the Allocation Factors for Shared Distribution Lines — Illustrative Example**

### Page 10 of 11

Time of Use Periods header table (repeated on this tab; identical to Tab 3 of this document: Morning 6 am to 1 pm, HE 7-13; Mid-Day Peak 1 pm to 7 pm, HE 14-19; Evening 7 pm to 10 pm, HE 20-22; Overnight 10 pm to 6 am, HE 1-6, 23-24).

**Section A. Plant-in Service Data** (Note 1)

Column labels: (A) FERC Account; (B) Account Description; (C) Plant in Service; (D) % of Total; (E) and (F) = "Allocation Factor (Note 2)": System Loaded (Moderate and High) and System Base; (G) = (D) * (E) and (H) = (D) * (F) = "Shared Distribution Line": System Loaded (Moderate and High) and System Base.

| FERC Account (A)                         | Account Description (B)            | Plant in Service (C) | % of Total (D) | Alloc. Factor: System Loaded (Moderate and High) (E) | Alloc. Factor: System Base (F) | Shared Dist. Line: System Loaded (G) = (D) * (E) | Shared Dist. Line: System Base (H) = (D) * (F) | Line                           |
| ---------------------------------------- | ---------------------------------- | -------------------- | -------------- | ---------------------------------------------------- | ------------------------------ | ------------------------------------------------ | ---------------------------------------------- | ------------------------------ |
| 364                                      | Poles, Towers, and Fixtures        | \$3,510,828,908      | 18.4%          | 0%                                                   | 100%                           | 0.0%                                             | 18.4%                                          | Line 1                         |
| 365                                      | Overhead Conductors and Devices    | \$5,178,335,506      | 27.1%          | 24%                                                  | 76%                            | 6.5%                                             | 20.6%                                          | Line 2                         |
| 366                                      | Underground Conduit                | \$1,188,740,550      | 6.2%           | 0%                                                   | 100%                           | 0.0%                                             | 6.2%                                           | Line 3                         |
| 367                                      | Underground Conductors and Devices | \$9,238,804,836      | 48.3%          | 67%                                                  | 33%                            | 32.4%                                            | 15.9%                                          | Line 4                         |
| Shared Distribution Line (Accts 364-367) |                                    | \$19,116,709,800     | 100.0%         |                                                      |                                | 39%                                              | 61%                                            | Line 5 = Sum (Line 1 : Line 4) |

**Section B. Allocate the System Loading (Moderate and High) between System High and System Moderate**

| (A) System Loaded (Moderate and High) | (B) Allocation Factor: System High % | (C) Allocation Factor: System Moderate % | (D) = (A) * (B): System High % | (E) = (A) * (C): System Moderate % | Line   |
| ------------------------------------- | ------------------------------------ | ---------------------------------------- | ------------------------------ | ---------------------------------- | ------ |
| 39%                                   | 77%                                  | 23%                                      | 30%                            | 9%                                 | Line 6 |

**Section C. Allocation Factors for Shared Distribution Lines by Sub-function to System Categories** (Note 4)

| System High % | System Moderate % | System Base | Line / formula             |
| ------------- | ----------------- | ----------- | -------------------------- |
| 30%           | 9%                | 61%         | Line 7 = Line 5 and Line 6 |

(In the source, the middle column header of Section C is rendered as "%"; it is the System Moderate % column, per Ex. 3.04.)

Notes:

1. ComEd Ex. 2.01 (2026 Embedded Cost of Service Study), Schedule 1a. (Function), Lines 18-21.
2. Accounts 364 and 366 are allocated to System Base. The allocation factors for Accounts 365 and 367 to System Loading (Moderate and High) and System Base are determined in the WP_Accts 365 and 367 workpaper.
3. See the Allocation Factors row in the table starting in Section D of the 3_Feeder Peak tab.
4. These allocation factors are used to allocate the costs of the Shared Distribution Lines sub-functions. See the allocation of these costs to the System Categories in the table starting in Section D of the 2_DTOU DFC RevResp tab.

---

## Tab 5: `5_DTOU kWhs` (p. 11)

**The Development of Annual Billed kWh by DTOU Period by Delivery Class — Illustrative Example**

### Page 11 of 11

Time of Use Periods header table (repeated on this tab; Morning 6 am to 1 pm, HE 7-13; Mid-Day Peak 1 pm to 7 pm, HE 14-19; Evening 7 pm to 10 pm, HE 20-22; Overnight 10 pm to 6 am, HE 1-6, 23-24).

**Section A. 2026 Annual Billed kWh by Delivery Classes** (Note 1)

|                        | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line   |
| ---------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------ |
| 2026 annual billed kWh | 20,055,740,094                    | 5,031,503,822                    | 674,744,649                    | 1,578,936,429                 | Line 1 |

**Section B. 2021 Annual Average Per Customer kWh by DTOU Period by Residential Delivery Class** (Note 2)

<!-- EPON: profile,ev-hp,midday-peak — load-shape inputs: 2021 AVERAGE per-customer kWh by period and class, re-cut for the 10 pm Evening/Overnight boundary (Evening 1,430 / 640 / 2,608 / 1,292; Overnight 2,516 / 1,248 / 5,681 / 2,750); electric-space-heat classes use about twice the kWh of no-heat classes -->

| DTOU Period  | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                 |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------------------------------ |
| Morning      | 2,430                             | 1,155                            | 5,649                          | 2,696                         | Line 2                         |
| Mid-Day Peak | 2,807                             | 1,197                            | 4,987                          | 2,411                         | Line 3                         |
| Evening      | 1,430                             | 640                              | 2,608                          | 1,292                         | Line 4                         |
| Overnight    | 2,516                             | 1,248                            | 5,681                          | 2,750                         | Line 5                         |
| Total        | 9,183                             | 4,238                            | 18,926                         | 9,150                         | Line 6 = Sum (Line 2 : Line 5) |

**Section C. Compute 2026 Delivery Class Annual Billed kWh by DTOU Period** (Note 3)

| DTOU Period  | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat | Line / formula                       |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- | ------------------------------------ |
| Morning      | 5,306,933,486                     | 1,370,864,294                    | 201,417,739                    | 465,266,160                   | Line 7 = Line 1 * (Line 2 / Line 6)  |
| Mid-Day Peak | 6,129,549,262                     | 1,420,394,572                    | 177,787,988                    | 416,019,068                   | Line 8 = Line 1 * (Line 3 / Line 6)  |
| Evening      | 3,123,172,662                     | 759,275,153                      | 92,995,550                     | 223,023,893                   | Line 9 = Line 1 * (Line 4 / Line 6)  |
| Overnight    | 5,496,084,683                     | 1,480,969,803                    | 202,543,372                    | 474,627,308                   | Line 10 = Line 1 * (Line 5 / Line 6) |
| Total        | 20,055,740,093                    | 5,031,503,822                    | 674,744,649                    | 1,578,936,429                 | Line 11 = Sum (Line 7 : Line 10)     |

Notes:

1. These are the 2026 annual billed kWhs by delivery class used to determine the 2026 Delivery Service Charges in ComEd Ex. 2.02.
2. The 8,760 hourly average use per customer for 2021 provided in the WP_Load Profiles workpaper are grouped in the Morning, Mid-Day Peak, Evening, and Overnight DTOU periods.
3. These 2026 Delivery Class Annual Billed kWh by DTOU Period [source says "D TOU Period"] are used in the table starting in Section C of the 1_DTOU DFC Rates tab.
