# ComEd Ex. 19.03 — Transmission and Miscellaneous Component kWh Charge (TMC kWh Charge) Determination, Compromise Proposal (Rehearing Rebuttal)

**Source**: `icc_639691_ex_19_03_tmc_kwh_illustrative.pdf` (ICC e-docket file id / filing id 639691)
**Pages**: 6 (spreadsheet-rendered workbook, landscape)
**Date**: May 12, 2025 (date of ComEd Ex. 19.0, with which this exhibit was filed; no date is printed on the exhibit itself)
**Docket**: ICC Docket No. 24-0378 (Commonwealth Edison Co., revenue-neutral tariff changes related to rate design — Rate BEST / DTOU), On Rehearing
**Author(s)**: ComEd (sponsored by Kathleen E. Kremer, Principal Rate Analyst, Retail Rates)
**Document type**: Illustrative exhibit (spreadsheet workpaper printout)
**ComEd exhibit no.**: ComEd Ex. 19.03
**Extraction method**: Embedded PDF text (PyMuPDF), tables verified against rendered page images
**Extraction notes**:

- _Minor typographical errors in the source have been corrected for readability. Substantive corrections are annotated inline._
- The printed header block on every page ("ICC Docket No. 24-0378 (onRehearing) / ComEd Ex. 19.03 / Page N of 6") is omitted; page boundaries are marked **`[p. N]`**. The "Illustrative Example" label, the "Commonwealth Edison Company" title line, and the placeholder dates "MONTH 20XX" are kept where they appear.
- Column letters / line letters (`a`, `c = a * b`, …) and every spreadsheet footnote are reproduced as printed. Spreadsheet footnotes are given as a "Notes" block directly under each table (no markdown footnote syntax is used). Cell shading and blue "input" font colors are not transcribed.
- Page references printed inside this exhibit's notes do not all match this 6-page version (it was evidently trimmed from a longer workbook, cf. the 7-page strawman Ex. 17.05): the notes cite "Page 7 of this work paper" for the NSPL/sales table that is on page 6, and page 4 says "See Page 6 for notes pertaining to Page 5". These are annotated `[source says "…"]` where they occur.
- Arithmetic cross-checks performed during extraction: line `j` on page 2 = 7,621+398+576+4,341+4,811+1,618+1,101+175+12 = \$20,653 ✓; line `n` = 20,653 − 9,955 − 9,579 + 3,337 + 7,707 = \$12,163 ✓; page 4 total = 11,503+2,107+188,855+18,526−3,105−2,479−361 = \$215,046 ✓; \$215,046 ÷ 19,219 MWh = \$11.19/MWh ✓; × 1.0517 ÷ 10 = 1.177 ¢/kWh ✓; 0.066 + 1.177 = 1.243 ✓; 1.243 × 1.0128 = 1.259 ✓; 1.259 × 1.0053 = 1.266 ✓. On page 2, \$12,163 ÷ 19,219 × 1.0517 ÷ 10 computes to 0.0666 ¢/kWh; the source prints 0.066 (presumably from unrounded inputs). On page 6, the printed column totals (19,526 / 19,219 / 18,265) differ by ±1 from the sum of the printed monthly rows (19,525 / 19,219 / 18,266), consistent with rounding.

**Differences vs strawman exhibit**: This is the compromise's single flat kWh TMC charge. Versus the strawman Ex. 17.05: (i) page 1 here = **1.243 → 1.259 → 1.266 ¢/kWh** (transmission 1.177 + miscellaneous 0.066, all in one kWh rate) vs strawman page 1 = 0.066 → 0.067 → 0.067 ¢/kWh (miscellaneous procurement only); (ii) the strawman had a separate **TMC kW charge of 3.656 → 3.703 → 3.723 \$/kW-month** (Ex. 17.05 pages 4–5) for the NSPL-based transmission services, which the compromise converts to kWh on page 4 here (\$215,046 ÷ 19,219 MWh × 1.0517 = 1.177 ¢/kWh). The underlying dollars (\$215,046 transmission; \$12,163 misc.) and the NSPL / sales table are identical in both.

---

[p. 1]

## Page 1 — TMC kWh Charge Determination (summary)

**Commonwealth Edison Company — Transmission and Miscellaneous Component kWh Charge Determination — Applicable to Retail Customers Served Under Rate BEST — _Illustrative Example_ — For Application Beginning with the MONTH 20XX Monthly Billing Period and Extending Through the MONTH 20XX Monthly Billing Period**

<!-- EPON: tmc — the compromise's single flat TMC kWh charge: 1.266 ¢/kWh after uncollectible factors (1.243 before), applied to all kWh in all four periods -->

| a: Transmission and Miscellaneous Component kWh Charge (TMC kWh Charge) Prior to Including Uncollectible Factors (cents/kWh) (1) (6) | b: SBUF (2) | c = a * b: TMC kWh Charge w/SBUF (cents/kWh) (3) (6) | d: ISUF (4) | e = c * d: TMC kWh Charge (cents/kWh) (5) (6) |
| -----------------------------------------------------------------------------------------------------------------------------------: | ----------: | ---------------------------------------------------: | ----------: | --------------------------------------------: |
|                                                                                                                                1.243 |      1.0128 |                                                1.259 |      1.0053 |                                     **1.266** |

Notes:

1. Transmission and Miscellaneous Components kWh Charge (TMC kWh Charge) determined pursuant to Rate Basic Electric Service Time-Of-Use (Rate BEST). See page 2 for determination.
2. Residential Supply Base Uncollectible Cost Factor (SBUF<sub>R</sub>) listed in Informational Sheet No. 21.
3. SBUF<sub>R</sub> applied pursuant to Rate BEST.
4. Residential Incremental Supply Uncollectible Cost Factor (ISUF<sub>R</sub>) listed in Informational Sheet No. 20.
5. ISUF<sub>R</sub> applied pursuant to Rate BEST.
6. Subject to rounding.

[p. 2]

## Page 2 — Miscellaneous procurement components (PJM ancillary + supply admin + working capital)

_Illustrative Example._ **Commonwealth Edison Company — Determination of the Transmission and Miscellaneous Component kWh Charge (TMC kWh Charge) Prior to Applying Uncollectibles Factors.** The TMC kWh Charge prior to applying uncollectibles factors is determined pursuant to Rate BEST. For Application Beginning with the MONTH 20XX Monthly Billing Period and Extending Through the MONTH 20XX Monthly Billing Period.

Expected expenses for the applicable PJM component services required for retail customers taking service under Rate BEST. Layout in the source: description (with note marker) · dollar amount · line letter and formula.

<!-- EPON: tmc — miscellaneous-procurement half of the TMC kWh charge: \$12,163 expected annual expense spread over 19,219 MWh (energy sales plus distribution losses) gives 0.066 ¢/kWh before uncollectibles; PJM per-MWh rates are applied to forecast Rate BEST volumes, not to individual customer load shape -->

| Line                                                            | Item                                                                                           |       Amount | Formula                       |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | -----------: | ----------------------------- |
| a                                                               | PJM Scheduling, System Control and Dispatch Service ("PJM Administration Charge") Expenses (1) |      \$7,621 | a = \$0.3903 * 19,526         |
| b                                                               | North American Electric Reliability Corporation Charge (Schedule 10-NERC) (1)                  |        \$398 | b = \$0.0204 * 19,526         |
| c                                                               | Reliability First Corporation Charge (Schedule 10-RFC) (1)                                     |        \$576 | c = \$0.0295 * 19,526         |
| d                                                               | Transmission Owner Scheduling, System Control and Dispatch Service (Schedule 1A) (1)           |      \$4,341 | d = \$0.2223 * 19,526         |
| e                                                               | Regulation and Frequency Response Service (2)                                                  |      \$4,811 | e = \$0.2503 * 19,219         |
| f                                                               | Synchronized Reserves Service (2)                                                              |      \$1,618 | f = \$0.0842 * 19,219         |
| g                                                               | Operating Reserves - Day-Ahead Service (2)                                                     |      \$1,101 | g = \$0.0573 * 19,219         |
| h                                                               | Day Ahead Scheduling Reserve (2)                                                               |        \$175 | h = \$0.0091 * 19,219         |
| i                                                               | Reactive Services (2)                                                                          |         \$12 | i = \$0.0006 * 19,219         |
| j                                                               | **Transmission Ancillary Expenses**                                                            | **\$20,653** | j = Sum of a through i        |
| k                                                               | Balancing Transmission Credits (3)                                                             |    (\$9,955) | k = (\$0.5180) * 19,219       |
| k [sic; letter repeated in source — presumably a separate line] | Transmission Loss Credits (3)                                                                  |    (\$9,579) | k = (\$0.4984) * 19,219       |
| l                                                               | Supply Administration Costs (4)                                                                |      \$3,337 | l                             |
| m                                                               | Cost of Working Capital (4)                                                                    |      \$7,707 | m                             |
| n                                                               | **Total Miscellaneous Procurement Components Expenses**                                        | **\$12,163** | n = j + k + l + m             |
| o                                                               | Total Energy Sales plus Distribution Losses in MWh (5)                                         |       19,219 | o                             |
| p                                                               | **TMC kWh Charge, in \$/MWh**                                                                  |   **\$0.63** | p = n / o                     |
| q                                                               | Expansion Factor (6)                                                                           |       1.0517 | q                             |
| r                                                               | **TMC kWh Charge (cents per kWh) prior to applying Uncollectible Factors**                     |    **0.066** | r = p * q * (1/1,000)*(100/1) |

See Page 3 for notes pertaining to Page 2 of this Work Paper.

[p. 3]

## Page 3 — Notes for Page 2 of this Work Paper

_Illustrative Example._ **Commonwealth Edison Company — Notes for Page 2 of this Work Paper**

1. The result of multiplying the per MWh rate for each service obtained from the PJM Interconnection, L.L.C. (PJM), by 19,526 MWhs. The per MWh rate for each service is determined based on PJM Open Access Transmission Tariff (OATT) and historical PJM bill analysis provided by ComEd's Energy Acquisition (EA) Department. The amount, 19,526 MWhs, is from the "Total" row under the "Energy Sales plus T&D Losses (in MWh)" column on Page 7 [source says "Page 7"; the table is on page 6 of this exhibit] of this work paper. It is the amount of energy sales to retail customers expected to take service under Rate BEST beginning with the MONTH 20XX monthly billing period and extending through the MONTH 20XX billing period, including Transmission and Distribution (T&D) losses.
2. The result of multiplying the per MWh rate for each service obtained from the PJM Interconnection, L.L.C. (PJM), by 19,219 MWhs. The per MWh rate for each service is determined based on PJM Open Access Transmission Tariff (OATT), PJM Operating Agreement, and historical PJM bill analysis provided by ComEd's EA Department. The amount, 19,219 MWhs, is from the "Total" row under the "Energy Sales plus Distribution Losses (in MWh)" column on Page 7 [source says "Page 7"; the table is on page 6 of this exhibit] of this work paper. It is the amount of energy sales to customers expected to take service under Rate BEST beginning with the MONTH 20XX monthly billing period and extending through the MONTH 20XX monthly billing period, including distribution losses.
3. The per MWh rate is determined based on the PJM Operating Agreement and historical PJM bill analysis provided by ComEd's EA Department. Please see Note (2) for the description of the amount, 19,219 MWhs.
4. Provided by ComEd's EA Department. The total of the costs allocated to BEST customers based on forecasted energy sales plus distribution losses.
5. Please see Note (2) for the description of the amount, 19,219 MWhs.
6. The Expansion Factor is determined from the 0.0517 Residential Single Family with No Space Heat Distribution Loss Factor, plus 1, listed in Informational Sheet No. 33, as filed on December 20, 2023 pursuant to the ICC Order dated December 14, 2023, in Docket Nos. 22-0486/23-0055 (Cons.).

[p. 4]

## Page 4 — Transmission (kW-related) costs converted to a kWh charge

_Illustrative Example._ **Commonwealth Edison Company — Determination of the Transmission and Miscellaneous Component kW-Related Costs Prior to Applying Uncollectibles.** The TMC kW-Related Charges prior to applying uncollectibles is determined pursuant to Rate BEST - Basic Electric Service Time-of-Use (Rate BEST). For Application Beginning with the MONTH 20XX Monthly Billing Period and Extending Through the MONTH 20XX Monthly Billing Period.

Expected expenses for the applicable PJM component services required for retail customers taking service under Rate BEST. Layout in the source: description (with note marker) · dollar amount · line letter and formula.

<!-- EPON: tmc, capacity-mdppec — transmission service costs (NITS \$188,855 etc., previously a kW-based/NSPL charge in the strawman) are now divided by Rate BEST energy sales (19,219 MWh) and recovered as a flat 1.177 ¢/kWh across all periods; the expected-load basis is the forecast "Rate BEST" population -->

| Line | Item                                                                        |        Amount | Formula                                                                      |
| ---- | --------------------------------------------------------------------------- | ------------: | ---------------------------------------------------------------------------- |
| a    | Reactive Supply and Voltage Control from Generation Sources Service (1)     |      \$11,503 | a = \$6.4301 * 1,789                                                         |
| b    | Black Start Service (2)                                                     |       \$2,107 | b = \$1.1778 * 1,789                                                         |
| c    | Network Integration Transmission Services (NITS) (3)                        |     \$188,855 | c = \$105.5648 * 1,789                                                       |
| d    | Transmission Enhancement Charges (Schedule 12) (4)                          |      \$18,526 | d = \$10.3553 * 1,789                                                        |
| e    | Transmission Enhancement Charges Adjustment (Schedule 12-C, Appendix C) (5) |     (\$3,105) | e = (\$1.7355) * 1,789                                                       |
| f    | Firm Point-To-Point (PTP) Transmission Revenue Credit (6)                   |     (\$2,479) | f = (\$1.3855) * 1,789                                                       |
| g    | Non-Firm PTP Transmission Revenue Credit (7)                                |       (\$361) | g = (\$0.2016) * 1,789                                                       |
| h    | **Total Expected Expenses**                                                 | **\$215,046** | h = Sum of a through f [sic; the total includes line g as well: a through g] |
| i    | Total Energy Sales plus Distribution Losses in MWh (5)                      |        19,219 | i                                                                            |
| j    | **TMC kWh Charge, in \$/MWh**                                               |   **\$11.19** | j = h / i                                                                    |
| k    | Expansion Factor (6)                                                        |        1.0517 | k                                                                            |
| l    | **TMC kWh Charge (cents per kWh) prior to applying Uncollectible Factors**  |     **1.177** | l = j * k * (1/1,000)*(100/1)                                                |

See Page 6 [source says "Page 6"; the notes for this page are on page 5] for notes pertaining to Page 5 [source says "Page 5"; this is page 4] of this Work Paper.

(Note markers (5) and (6) on the "Total Energy Sales" and "Expansion Factor" lines of this page coincide with the page-2 note numbering — see page 3 notes (5) and (6) — whereas the page-5 notes numbered (5) and (6) describe the Transmission Enhancement Charge credit and the Firm PTP credit. The page-5 notes have no separate entry for "Total Energy Sales" or "Expansion Factor"; page-5 note (8) is the note for 1,789 MW.)

[p. 5]

## Page 5 — Notes for Page 5 of this Work Paper

_Illustrative Example._ **Commonwealth Edison Company — Notes for Page 5 of this Work Paper** [source says "Page 5"; these are the notes to the page-4 table of this exhibit]

1. The result of multiplying the daily per MW charge of \$6.4301 by 1,789 MW. The daily per MW charge rate, \$6.4301, for the Reactive Supply and Voltage Control from Generation Sources Service is determined based on a \$52,730,002 annual revenue requirement for this service for the ComEd Zone as shown in PJM's September 6, 2024 posting of Reactive Supply and Voltage Control Revenue Requirements and 22,467 MW of daily Network Service Peak Load (NSPL) for the ComEd Zone. The 22,467 MW of daily NSPL for the ComEd Zone is found on the PJM website. The amount, 1,789 MW, is from the "Total" row under the "Sum of Daily NSPL (in MW)" column on page seven (7) [source says "page seven (7)"; the table is on page 6 of this exhibit] of this workpaper. It is the sum of the daily NSPL for retail customers expected to take service under Rate BEST for the period beginning with the MONTH 20XX monthly billing period and extending through the MONTH 20XX billing period.
2. The result of multiplying the daily per MW charge of \$1.1778 by 1,789 MW. The daily per MW charge rate, \$1.1778, for the Black Start Service is determined based on a \$9,658,313 annual revenue requirement for this service in the ComEd Zone as shown in PJM's September 6, 2024 posting of Black Start Revenue Requirements, and 22,467 MW of daily NSPL for the ComEd Zone. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
3. The result of multiplying the per MW Network Integration Transmission Services (NITS) charge of \$105.5648 by 1,789 MW. The daily charge rate of \$105.5648 per MW is the result of dividing the annual Transmission Revenue Requirement of \$865,679,148 by the product of the zonal NSPL of 22,467 MW and 365 days, subject to rounding. The \$865,679,148 is stated in the documents filed on April 24, 2024 with the Federal Energy Regulatory Commission (FERC) in Docket No. ER09-1145-000. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
4. The result of multiplying the daily per MW Transmission Enhancement Charge of \$10.3553 by 1,789 MW. The daily Transmission Enhancement Charge rate is an estimated amount based on \$84.9 million expected annual amount for the ComEd Zone for the MONTH 20XX through MONTH 20XX period and 22,467 MW of daily Network Service Peak Load (NSPL) for the ComEd Zone. The \$84.9 million expected amount is based on a monthly revenue requirement of \$7.1 million from PJM's June 7, 2024 posting of Transmission Enhancements allocated to the ComEd Zone. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
5. The result of multiplying the daily per MW Transmission Enhancement Charge credit of \$1.7355 by 1,789 MW. The daily Transmission Enhancement Charge credit rate is the result of dividing an estimated total 12-month (MONTH 20XX through MONTH 20XX) credit of \$14.2 million for the ComEd Zone by the product of the Zonal NSPL, 22,467 MW, multiplied by 365 days, the expected 12-month period (MONTH 20XX through MONTH 20XX) the adjustment will be applicable. The Transmission Enhancement Charge Adjustment is based on the FERC approved settlement agreement dated May 31, 2018 in FERC Docket No. EL05-121-009. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
6. The result of multiplying the daily per MW Firm Point-to-Point (PTP) credit of \$1.3855 by 1,789 MW. The daily per MW Firm PTP credit rate is determined based on \$10.3 million expected annual credit amount for the ComEd Zone and 22,467 MW of daily NSPL for the ComEd Zone. The \$10.3 million expected amount is provided by ComEd's EA Department. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
7. The result of multiplying the daily per MW Non-Firm PTP credit of \$0.2016 by 1,789 MW. The daily per MW Non-Firm PTP credit rate is determined based on \$1.4 million expected annual credit amount for the ComEd Zone and 22,467 MW of daily NSPL for the ComEd Zone. The \$1.4 million expected amount is provided by ComEd's EA Department. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
8. Please see Note (1) for the description of the 1,789 MW.

[p. 6]

## Page 6 — Expected NSPL and energy sales for Rate BEST customers

_Illustrative Example._ **Commonwealth Edison Company — Expected Network Service Peak Load (NSPL), electric energy sales plus T&D Losses, electric energy sales plus Distribution Losses, and electric energy sales without losses for retail customers expected to be taking service under Rate Basic Electric Service Time-Of-Use (Rate BEST), Beginning with the MONTH 20XX Monthly Billing Period and Extending Through the MONTH 20XX Monthly Billing Period.**

<!-- EPON: profile, tmc — forecast Rate BEST participant volumes by month (Jun-24 to May-25): 18,265 MWh energy sales and a flat 4.90 MW daily NSPL for the whole population; monthly sales are heavily summer-weighted (Jul/Aug highest); these totals are the denominators for the TMC kWh charge -->

| Month     | a: Expected Daily NSPL (in MW) (1) | b: Number of Days in the Month | c = a * b: Sum of Daily NSPL (in MW) | d: Energy Sales plus T&D Losses (in MWh) (1) | e: Energy Sales plus Distribution Losses (in MWh) (1) | f: Energy Sales without Losses (in MWh) (1) |
| --------- | ---------------------------------: | -----------------------------: | -----------------------------------: | -------------------------------------------: | ----------------------------------------------------: | ------------------------------------------: |
| Jun-24    |                               4.90 |                             30 |                                  147 |                                        1,759 |                                                 1,732 |                                       1,646 |
| Jul-24    |                               4.90 |                             31 |                                  152 |                                        2,230 |                                                 2,194 |                                       2,086 |
| Aug-24    |                               4.90 |                             31 |                                  152 |                                        2,150 |                                                 2,117 |                                       2,012 |
| Sep-24    |                               4.90 |                             30 |                                  147 |                                        1,582 |                                                 1,557 |                                       1,480 |
| Oct-24    |                               4.90 |                             31 |                                  152 |                                        1,411 |                                                 1,389 |                                       1,320 |
| Nov-24    |                               4.90 |                             30 |                                  147 |                                        1,441 |                                                 1,419 |                                       1,348 |
| Dec-24    |                               4.90 |                             31 |                                  152 |                                        1,657 |                                                 1,631 |                                       1,550 |
| Jan-25    |                               4.90 |                             31 |                                  152 |                                        1,673 |                                                 1,647 |                                       1,565 |
| Feb-25    |                               4.90 |                             28 |                                  137 |                                        1,457 |                                                 1,434 |                                       1,363 |
| Mar-25    |                               4.90 |                             31 |                                  152 |                                        1,491 |                                                 1,467 |                                       1,395 |
| Apr-25    |                               4.90 |                             30 |                                  147 |                                        1,304 |                                                 1,284 |                                       1,220 |
| May-25    |                               4.90 |                             31 |                                  152 |                                        1,370 |                                                 1,348 |                                       1,281 |
| **Total** |                                    |                            365 |                                1,789 |                                       19,526 |                                                19,219 |                                      18,265 |

Notes:

1. Provided by ComEd's Load Forecasting Department. Forecasts for MONTH 20XX through MONTH 20XX were updated in a MONTH 20XX forecast provided to the Illinois Power Authority in compliance with Section 16-111.5 of the Public Utilities Act.
