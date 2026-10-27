# ComEd Ex. 17.05 — Transmission and Miscellaneous Component kWh Charge and kW Charge Determination, Strawman Proposal (Rehearing Direct)

**Source**: `icc_636691_ex_17_05_tmc_kwh_illustrative.pdf` (ICC e-docket file id / filing id 636691)
**Pages**: 7 (spreadsheet-rendered workbook, landscape)
**Date**: April 4, 2025 (date of ComEd Ex. 17.0, the rehearing direct testimony with which this exhibit was filed; no date is printed on the exhibit itself)
**Docket**: ICC Docket No. 24-0378 (Commonwealth Edison Co., revenue-neutral tariff changes related to rate design — Rate BEST / DTOU), On Rehearing
**Author(s)**: ComEd (sponsored by Kathleen E. Kremer, Principal Rate Analyst, Retail Rates)
**Document type**: Illustrative exhibit (spreadsheet workpaper printout)
**ComEd exhibit no.**: ComEd Ex. 17.05
**Extraction method**: Embedded PDF text (PyMuPDF), tables verified against rendered page images
**Extraction notes**:

- _Minor typographical errors in the source have been corrected for readability. Substantive corrections are annotated inline._
- The printed header block on every page ("ICC Docket No. 24-0378 (On Rehearing) / ComEd Ex. 17.05 / Page N of 7") is omitted; page boundaries are marked **`[p. N]`**. The "Illustrative Example" label, the "Commonwealth Edison Company" title line, and the placeholder dates "MONTH 20XX" are kept where they appear.
- Column letters / line letters (`a`, `c = a * b`, …) and every spreadsheet footnote are reproduced as printed. Spreadsheet footnotes are given as a "Notes" block directly under each table (no markdown footnote syntax is used). Cell shading and blue "input" font colors are not transcribed.
- Pages 2, 3, 6 and 7 of this exhibit are text-identical (apart from page numbers) to pages 2, 3, 5 and 6 of the compromise exhibit Ex. 19.03; they are nevertheless transcribed in full below. Page references inside the notes (e.g. "Page 7", "page seven (7)", "See Page 6 for notes pertaining to Page 5") are correct in this 7-page version.
- Arithmetic cross-checks: page 5 total = 11,503+2,107+188,855+18,526−3,105−2,479−361 = \$215,046 ✓; (\$215,046 ÷ 1,789) × 365 ÷ 12 ÷ 1,000 = \$3.656/kW-month ✓; 3.656 × 1.0128 = 3.703 ✓; 3.703 × 1.0053 = 3.723 ✓. Page 1: 0.066 × 1.0128 = 0.067 ✓; × 1.0053 = 0.067 ✓. Page 2 arithmetic as in Ex. 19.03 (line j \$20,653 ✓, line n \$12,163 ✓). On page 7, the printed column totals (19,526 / 19,219 / 18,265) differ by ±1 from the sum of the printed monthly rows (19,525 / 19,219 / 18,266), consistent with rounding.

**Differences vs compromise exhibit** (verified by line-by-line comparison of this exhibit's text with Ex. 19.03, and by viewing the rendered pages):

- **Page 1 — kWh charge**: strawman TMC kWh charge is **0.066 → 0.067 → 0.067 ¢/kWh** (miscellaneous procurement only: PJM admin/NERC/RFC/Schedule 1A/ancillary services, loss and balancing credits, supply administration, working capital = \$12,163). The compromise (Ex. 19.03 page 1) is **1.243 → 1.259 → 1.266 ¢/kWh**.
- **Pages 4–5 — extra kW charge (strawman only)**: the strawman charges transmission-service costs (reactive supply, black start, NITS, Schedule 12 TEC and adjustment, firm/non-firm PTP credits; total \$215,046) as a separate **TMC kW charge of \$3.656 → \$3.703 → \$3.723 per kW-month** (= \$215,046 ÷ 1,789 MW-days × 365 ÷ 12 ÷ 1,000). In the compromise (Ex. 19.03 page 4) the same \$215,046 is instead divided by 19,219 MWh of energy sales plus distribution losses and multiplied by the 1.0517 expansion factor, giving **1.177 ¢/kWh**, added to the 0.066 ¢/kWh miscellaneous component to make the single 1.243 ¢/kWh (1.266 ¢/kWh after uncollectible factors).
- **Unchanged**: all dollar inputs on page 2 (\$12,163 miscellaneous total) and page 5 (\$215,046 transmission total), the 22,467 MW zonal NSPL, 1,789 MW-day and 19,219 MWh forecasts, the expansion factor 1.0517, SBUF 1.0128 and ISUF 1.0053, and the monthly NSPL/sales table (page 7 here, page 6 of Ex. 19.03). The page count is 7 here vs 6 in the compromise because the kW charge needs its own summary page (page 4) and determination page (page 5).
- This exhibit does not show the billing determinant (e.g. customer NSPL or peak-load contribution) to which the \$/kW-month TMC charge would be applied.

---

[p. 1]

## Page 1 — TMC kWh Charge Determination (summary)

**Commonwealth Edison Company — Transmission and Miscellaneous Component kWh Charge Determination — Applicable to Retail Customers Served Under Rate BEST — For Application Beginning with the MONTH 20XX Monthly Billing Period and Extending Through the MONTH 20XX Monthly Billing Period** (_Illustrative Example_)

<!-- EPON: tmc — strawman TMC kWh charge is only the miscellaneous-procurement piece: 0.067 ¢/kWh after uncollectible factors (transmission services are in the separate kW charge, pages 4–5) -->

| a: Transmission and Miscellaneous Component kWh Charge (TMC kWh Charge) Prior to Including Uncollectible Factors (cents/kWh) (1) (6) | b: SBUF (2) | c = a * b: TMC kWh Charge w/SBUF (cents/kWh) (3) (6) | d: ISUF (4) | e = c * d: TMC kWh Charge (cents/kWh) (5) (6) |
| -----------------------------------------------------------------------------------------------------------------------------------: | ----------: | ---------------------------------------------------: | ----------: | --------------------------------------------: |
|                                                                                                                                0.066 |      1.0128 |                                                0.067 |      1.0053 |                                     **0.067** |

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

<!-- EPON: tmc — in the strawman this miscellaneous-procurement block is the ENTIRE TMC kWh charge: \$12,163 expected annual expense spread over 19,219 MWh (energy sales plus distribution losses) gives 0.066 ¢/kWh before uncollectibles; PJM per-MWh rates are applied to forecast Rate BEST volumes, not to individual customer load shape -->

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

1. The result of multiplying the per MWh rate for each service obtained from the PJM Interconnection, L.L.C. (PJM), by 19,526 MWhs. The per MWh rate for each service is determined based on PJM Open Access Transmission Tariff (OATT) and historical PJM bill analysis provided by ComEd's Energy Acquisition (EA) Department. The amount, 19,526 MWhs, is from the "Total" row under the "Energy Sales plus T&D Losses (in MWh)" column on Page 7 of this work paper. It is the amount of energy sales to retail customers expected to take service under Rate BEST beginning with the MONTH 20XX monthly billing period and extending through the MONTH 20XX billing period, including Transmission and Distribution (T&D) losses.
2. The result of multiplying the per MWh rate for each service obtained from the PJM Interconnection, L.L.C. (PJM), by 19,219 MWhs. The per MWh rate for each service is determined based on PJM Open Access Transmission Tariff (OATT), PJM Operating Agreement, and historical PJM bill analysis provided by ComEd's EA Department. The amount, 19,219 MWhs, is from the "Total" row under the "Energy Sales plus Distribution Losses (in MWh)" column on Page 7 of this work paper. It is the amount of energy sales to customers expected to take service under Rate BEST beginning with the MONTH 20XX monthly billing period and extending through the MONTH 20XX monthly billing period, including distribution losses.
3. The per MWh rate is determined based on the PJM Operating Agreement and historical PJM bill analysis provided by ComEd's EA Department. Please see Note (2) for the description of the amount, 19,219 MWhs.
4. Provided by ComEd's EA Department. The total of the costs allocated to BEST customers based on forecasted energy sales plus distribution losses.
5. Please see Note (2) for the description of the amount, 19,219 MWhs.
6. The Expansion Factor is determined from the 0.0517 Residential Single Family with No Space Heat Distribution Loss Factor, plus 1, listed in Informational Sheet No. 33, as filed on December 20, 2023 pursuant to the ICC Order dated December 14, 2023, in Docket Nos. 22-0486/23-0055 (Cons.).

[p. 4]

## Page 4 — TMC kW Charge Determination (summary)

**Commonwealth Edison Company — Transmission and Miscellaneous Component kW Charge Determination — Applicable to Retail Customers Served Under Rate BEST — _Illustrative Example_ — For Application Beginning with the MONTH 20XX Monthly Billing Period and Extending Through the MONTH 20XX Monthly Billing Period**

<!-- EPON: tmc — strawman kW-based TMC charge for transmission services: 3.723 \$/kW-month after uncollectible factors (removed in the compromise, which converts this cost to 1.177 ¢/kWh) -->

| a: Transmission and Miscellaneous Component kW Charge (TMC kW Charge) Prior to Including Uncollectible Factors (\$/kW-month) (1) (6) | b: SBUF (2) | c = a * b: TMC kW Charge w/SBUF (\$/kW-month) (3) (6) | d: ISUF (4) | e = c * d: TMC kW Charge (\$/kW-month) (5) (6) |
| -----------------------------------------------------------------------------------------------------------------------------------: | ----------: | ----------------------------------------------------: | ----------: | ---------------------------------------------: |
|                                                                                                                                3.656 |      1.0128 |                                                 3.703 |      1.0053 |                                      **3.723** |

Notes:

1. Determined pursuant to Rate BEST - Rate Basic Electric Service Time-Of-Use. See Page 5 for determination.
2. Residential Supply Base Uncollectible Cost Factor (SBUF<sub>R</sub>) listed in Informational Sheet No. 21.
3. SBUF<sub>R</sub> applied pursuant to Rate BEST.
4. Residential Incremental Supply Uncollectible Cost Factor (ISUF<sub>R</sub>) listed in Informational Sheet No. 20.
5. ISUF<sub>R</sub> applied pursuant to Rate BEST.
6. Subject to rounding.

[p. 5]

## Page 5 — TMC kW Charge Determination (transmission-service costs)

_Illustrative Example._ **Commonwealth Edison Company — Determination of the Transmission and Miscellaneous Component kW Charge (TMC kW Charge) Prior to Applying Uncollectibles.** The TMC kW Charge prior to applying uncollectibles is determined pursuant to Rate BEST - Basic Electric Service Time-of-Use (Rate BEST). For Application Beginning with the MONTH 20XX Monthly Billing Period and Extending Through the MONTH 20XX Monthly Billing Period.

Expected expenses for the applicable PJM component services required for retail customers taking service under Rate BEST. Layout in the source: description (with note marker) · dollar amount · line letter and formula.

<!-- EPON: tmc — strawman: \$215,046 of transmission-service cost converted to \$/kW-month using 1,789 MW-days of expected Rate BEST NSPL (4.90 MW daily × 365), 365 days, 12 months -->

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
| i    | Sum of Daily NSPL in MW-days (8)                                            |         1,789 | i                                                                            |
| j    | Days in the Year                                                            |           365 | j                                                                            |
| k    | Monthly Billing Periods in a Year                                           |            12 | k                                                                            |
| l    | **Total Expected TMC kW Charge in \$/kW-month**                             |   **\$3.656** | l = (h / i) * j / k / 1000                                                   |

See Page 6 for notes pertaining to Page 5 of this Work Paper.

[p. 6]

## Page 6 — Notes for Page 5 of this Work Paper

_Illustrative Example._ **Commonwealth Edison Company — Notes for Page 5 of this Work Paper**

1. The result of multiplying the daily per MW charge of \$6.4301 by 1,789 MW. The daily per MW charge rate, \$6.4301, for the Reactive Supply and Voltage Control from Generation Sources Service is determined based on a \$52,730,002 annual revenue requirement for this service for the ComEd Zone as shown in PJM's September 6, 2024 posting of Reactive Supply and Voltage Control Revenue Requirements and 22,467 MW of daily Network Service Peak Load (NSPL) for the ComEd Zone. The 22,467 MW of daily NSPL for the ComEd Zone is found on the PJM website. The amount, 1,789 MW, is from the "Total" row under the "Sum of Daily NSPL (in MW)" column on page seven (7) of this workpaper. It is the sum of the daily NSPL for retail customers expected to take service under Rate BEST for the period beginning with the MONTH 20XX monthly billing period and extending through the MONTH 20XX billing period.
2. The result of multiplying the daily per MW charge of \$1.1778 by 1,789 MW. The daily per MW charge rate, \$1.1778, for the Black Start Service is determined based on a \$9,658,313 annual revenue requirement for this service in the ComEd Zone as shown in PJM's September 6, 2024 posting of Black Start Revenue Requirements, and 22,467 MW of daily NSPL for the ComEd Zone. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
3. The result of multiplying the per MW Network Integration Transmission Services (NITS) charge of \$105.5648 by 1,789 MW. The daily charge rate of \$105.5648 per MW is the result of dividing the annual Transmission Revenue Requirement of \$865,679,148 by the product of the zonal NSPL of 22,467 MW and 365 days, subject to rounding. The \$865,679,148 is stated in the documents filed on April 24, 2024 with the Federal Energy Regulatory Commission (FERC) in Docket No. ER09-1145-000. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
4. The result of multiplying the daily per MW Transmission Enhancement Charge of \$10.3553 by 1,789 MW. The daily Transmission Enhancement Charge rate is an estimated amount based on \$84.9 million expected annual amount for the ComEd Zone for the MONTH 20XX through MONTH 20XX period and 22,467 MW of daily Network Service Peak Load (NSPL) for the ComEd Zone. The \$84.9 million expected amount is based on a monthly revenue requirement of \$7.1 million from PJM's June 7, 2024 posting of Transmission Enhancements allocated to the ComEd Zone. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
5. The result of multiplying the daily per MW Transmission Enhancement Charge credit of \$1.7355 by 1,789 MW. The daily Transmission Enhancement Charge credit rate is the result of dividing an estimated total 12-month (MONTH 20XX through MONTH 20XX) credit of \$14.2 million for the ComEd Zone by the product of the Zonal NSPL, 22,467 MW, multiplied by 365 days, the expected 12-month period (MONTH 20XX through MONTH 20XX) the adjustment will be applicable. The Transmission Enhancement Charge Adjustment is based on the FERC approved settlement agreement dated May 31, 2018 in FERC Docket No. EL05-121-009. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
6. The result of multiplying the daily per MW Firm Point-to-Point (PTP) credit of \$1.3855 by 1,789 MW. The daily per MW Firm PTP credit rate is determined based on \$10.3 million expected annual credit amount for the ComEd Zone and 22,467 MW of daily NSPL for the ComEd Zone. The \$10.3 million expected amount is provided by ComEd's EA Department. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
7. The result of multiplying the daily per MW Non-Firm PTP credit of \$0.2016 by 1,789 MW. The daily per MW Non-Firm PTP credit rate is determined based on \$1.4 million expected annual credit amount for the ComEd Zone and 22,467 MW of daily NSPL for the ComEd Zone. The \$1.4 million expected amount is provided by ComEd's EA Department. Please see Note (1) for the description of the amounts, 22,467 MW and 1,789 MW.
8. Please see Note (1) for the description of the 1,789 MW.

[p. 7]

## Page 7 — Expected NSPL and energy sales for Rate BEST customers

_Illustrative Example._ **Commonwealth Edison Company — Expected Network Service Peak Load (NSPL), electric energy sales plus T&D Losses, electric energy sales plus Distribution Losses, and electric energy sales without losses for retail customers expected to be taking service under Rate Basic Electric Service Time-Of-Use (Rate BEST), Beginning with the MONTH 20XX Monthly Billing Period and Extending Through the MONTH 20XX Monthly Billing Period.**

<!-- EPON: profile, tmc — forecast Rate BEST participant volumes (same table as the compromise; the 1,789 MW-day total is the divisor of the strawman's kW-based TMC charge) by month (Jun-24 to May-25): 18,265 MWh energy sales and a flat 4.90 MW daily NSPL for the whole population; monthly sales are moderately summer-weighted (Jul/Aug highest); these totals are the denominators for the TMC kWh charge -->

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
