# ComEd Ex. 19.01 — Illustrative Residential BEST Electricity Charge Determination (BESTEC), Corrected Version of Ex. 17.03 (Rehearing Rebuttal)

**Source**: `icc_639689_ex_19_01_bestec_illustrative.pdf` (ICC e-docket file id / filing id 639689)
**Pages**: 4 (spreadsheet-rendered workbook, landscape)
**Date**: May 12, 2025 (filed with ComEd Ex. 19.0)
**Docket**: ICC Docket No. 24-0378 (Commonwealth Edison Co., revenue-neutral tariff changes related to rate design — Rate BEST / DTOU), On Rehearing
**Author(s)**: ComEd (sponsored by Kathleen E. Kremer, Principal Rate Analyst, Retail Rates)
**Document type**: Illustrative exhibit (spreadsheet workpaper printout)
**ComEd exhibit no.**: ComEd Ex. 19.01
**Extraction method**: Embedded PDF text (PyMuPDF), tables verified against rendered page images
**Extraction notes**:

- _Minor typographical errors in the source have been corrected for readability. Substantive corrections are annotated inline._
- The printed header block on every page ("ICC Docket No. 24-0378 (on Rehearing) / ComEd Ex. 19.01 / Page N of 4") is omitted; page boundaries are marked **`[p. N]`**. The spreadsheet's "Illustrative Example" label (top left of every page) and the "For Application of the MONTH 20YY Monthly Billing Period" line (placeholders, not real dates) are kept where they appear in tables.
- Column letters (`a`, `b`, `d = a * c`, …) and every spreadsheet footnote are reproduced exactly as printed. Spreadsheet footnotes are given as a "Notes" block directly under each table (no markdown footnote syntax is used in this document). Cell shading (green = input cells, yellow/pink/blue/green period fills) is not transcribed.
- Page 3 is a workpaper whose print area shows only the first 102 hourly rows (1/1/2023 Hour01 through 1/5/2023 Hour06) of what is evidently an 8,760-row hourly workbook, plus summary blocks. All 102 printed rows are transcribed; the summary blocks reference "rows 3628-6555" of the full workbook, which are not printed.
- Units are as printed. The source does not state units for "RTOUPP Load", "PJM Price" or "Total Estimated Revenue".

**Context / how this exhibit relates to the Compromise Proposal**: Ex. 19.01 is the "corrected version of ComEd Ex. 17.03" (Kremer RH Reb., ComEd Ex. 19.0 at 2:27–28 and fn. 1): the strawman's **energy-only** BESTEC determination, with the Overnight rate corrected from 1.869 to 1.870 ¢/kWh for a rounding issue. It is **not** the final Compromise charge schedule: its Mid-Day Peak row (4.787 summer / 3.383 nonsummer ¢/kWh) contains **no capacity cost**. The Compromise Proposal's Mid-Day Peak charges (18.219 summer / 16.814 nonsummer ¢/kWh, Ex. 19.0 Figure 1) are the energy-only values here **plus** 100% of capacity in the Mid-Day Peak kWh rate, computed in Ex. 19.02 (not part of this extract): ARBREV 17.894 / 16.514 = 4.702 / 3.322 + 13.192 ¢/kWh capacity, then × 1.0128 × 1.0053. Morning, Evening and Overnight rows are identical between this exhibit and Figure 1 of Ex. 19.0.

---

[p. 1]

## Page 1 — Illustrative Residential BEST Electricity Charge Determination

**Illustrative Residential BEST Electricity Charge Determination — Applicable to Retail Customers Served Under Rate BEST — For Application of the MONTH 20YY Monthly Billing Period** (_Illustrative Example_)

Structure: eight numbered columns **a–h**. Columns **a, b** = Adjusted Residential Base Revenue (ARBREV) Price (note 1); **c** = SBUF (note 2); **d, e** = ARBREV Price w/BUF (notes 3, 5), i.e. Base Residential BEST Charge (BRBESTC) with the uncollectible factor; **f** = ISUF (note 4); **g, h** = Basic Electric Service Time of Use Electricity Charge (BESTEC) (note 5), summer (note 6) and nonsummer.

<!-- EPON: midday-peak, profile, capacity-mdppec — final BESTEC by period from the aggregate illustrative profile. In this exhibit the Mid-Day Peak charge (MDPPEC) is ENERGY ONLY (4.787 / 3.383 ¢/kWh); capacity is added separately (kW charge in the strawman, folded into MDPPEC in the compromise, Ex. 19.02) -->

| Time of Use Periods                             | a: Summer ARBREV Price (cents/kWh) | b: NonSummer ARBREV Price (cents/kWh) | c: SBUF (2) | d = a * c: Summer BRBESTC w/BUF (cents/kWh) | e = b * c: Nonsummer BRBESTC w/BUF (cents/kWh) | f: ISUF (4) | g = d * f: Summer (6) BESTEC (cents/kWh) | h = e * f: Nonsummer BESTEC (cents/kWh) |
| ----------------------------------------------- | ---------------------------------: | ------------------------------------: | ----------: | ------------------------------------------: | ---------------------------------------------: | ----------: | ---------------------------------------: | --------------------------------------: |
| Morning Period Electricity Charge (MPEC)        |                              2.959 |                                 2.778 |      1.0128 |                                       2.997 |                                          2.814 |      1.0053 |                                    3.013 |                                   2.829 |
| Mid-Day Peak Period Electricity Charge (MDPPEC) |                              4.702 |                                 3.322 |      1.0128 |                                       4.762 |                                          3.365 |      1.0053 |                                    4.787 |                                   3.383 |
| Evening Period Electricity Charge (EPEC)        |                              3.035 |                                 3.031 |      1.0128 |                                       3.074 |                                          3.070 |      1.0053 |                                    3.090 |                                   3.086 |
| Overnight Period Electricity Charge (OPEC)      |                              1.836 |                                 1.976 |      1.0128 |                                       1.860 |                                          2.001 |      1.0053 |                                **1.870** |                                   2.012 |

(The g and h columns are printed in bold in the source.)

Notes:

1. Base Residential BEST Charges (BRBESTCs) from page 2, determined pursuant to Rate Basic Electric Service Time of Use (Rate BEST). Subject to rounding.
2. Residential Supply Base Uncollectible Cost Factor (SBUF<sub>R</sub>) determined in accordance with the provisions of Rider UF - Uncollectible Factors (Rider UF) and listed in Informational Sheet No. 21.
3. Residential BUF<sub>R</sub> multiplied times BRBESTCs pursuant to Rate BEST. Subject to rounding.
4. Residential Incremental Supply Uncollectible Cost Factors (ISUF<sub>R</sub>) as listed in Informational Sheet No. 20.
5. ISUF<sub>R</sub> applied pursuant to Rate BEST. Subject to rounding.
6. Summer BESTECs are applicable June, July, August and September monthly billing periods.

[p. 2]

## Page 2 — Illustrative Base Residential BEST Charge Determination

**Commonwealth Edison Company — Illustrative Base Residential BEST Charge Determination — Applicable to Retail Customers Served Under Rate BEST — For Application of the MONTH 20YY Monthly Billing Period** (_Illustrative Example_)

Structure: ten columns. `(s)` = summer, `(n)` = nonsummer. Columns **a** = estimated revenue, **b** = estimated kWh, **c** = historical energy charge per \$/kWh (= revenue ÷ kWh), **d** = adjustments per \$/kWh (blank input cells in this illustration), **e** = ARBREV price in cents/kWh (feeds columns a and b on page 1).

<!-- EPON: profile, midday-peak — base (energy-only) price per period = historical RTOUPP revenue ÷ kWh by period; the kWh by period (e.g. Mid-Day Peak 2,012,553 summer / 2,554,445 nonsummer) is the aggregate load shape used to price each period; adjustments d(s), d(n) are blank (set to zero) in this illustration -->

| Time of Use Periods | a(s): Summer Estimated Revenue | a(n): Nonsummer Estimated Revenue | b(s): Summer Estimated kWhs | b(n): Nonsummer Estimated kWhs | c(s) = a(s)/b(s): Historical Summer Energy Charge per \$/kWh Rate | c(n) = a(n)/c(n) [sic; presumably b(n)]: Historical Nonsummer Energy Charge per \$/kWh Rate | d(s): Summer Adjustments per \$/kWh Rate (1) | d(n): Nonsummer Adjustments per \$/kWh Rate (1) | e(s) = (c(s) + d(s)) * 100: Summer ARBREV Price (cents/kWh) (2) | e(n) = (c(n) + d(n)) * 100: Nonsummer ARBREV Price (cents/kWh) (2) |
| ------------------- | -----------------------------: | --------------------------------: | --------------------------: | -----------------------------: | ----------------------------------------------------------------: | ------------------------------------------------------------------------------------------: | -------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------: | -----------------------------------------------------------------: |
| Morning             |                       \$47,528 |                          \$76,603 |                   1,605,949 |                      2,757,222 |                                                           0.02959 |                                                                                     0.02778 | _(blank)_                                    | _(blank)_                                       |                                                           2.959 |                                                              2.778 |
| Mid-Day Peak        |                       \$94,633 |                          \$84,866 |                   2,012,553 |                      2,554,445 |                                                           0.04702 |                                                                                     0.03322 | _(blank)_                                    | _(blank)_                                       |                                                           4.702 |                                                              3.322 |
| Evening             |                       \$22,297 |                          \$31,030 |                     734,676 |                      1,023,637 |                                                           0.03035 |                                                                                     0.03031 | _(blank)_                                    | _(blank)_                                       |                                                           3.035 |                                                              3.031 |
| Overnight           |                       \$52,670 |                          \$93,023 |                   2,869,278 |                      4,707,327 |                                                           0.01836 |                                                                                     0.01976 | _(blank)_                                    | _(blank)_                                       |                                                           1.836 |                                                              1.976 |

Notes:

1. Adjustments are applied to reflect current market energy prices relative to historical energy prices used to determine the base reven [text truncated in source rendering at the cell edge; the identical note in Ex. 17.03 reads "...used to determine the base revenue."]
2. _(Footnote marker (2) appears in the column headers; no note (2) text is printed on this page. Page 1 note 1 states the ARBREV prices are "subject to rounding".)_

[p. 3]

## Page 3 — Hourly workpaper (RTOUPP load × PJM price)

**Header text as printed (in red, top left):** "This Workpaper is set to print Page 1 only". **Label:** _Illustrative Example_. **Start Date** (see page 4): 1/1/2023. **Total kWhs: 18,265,086** (printed above the hourly table).

<!-- EPON: profile — summary blocks (right side of page 3) show how the period base prices come from an hourly RTOUPP load × PJM price workpaper for calendar 2023 -->

### Summary blocks (right side of page)

**Summer Period without Adjustments (rows 3628-6555)**

| Period    | Total \$ | Total kWhs | Average Rate in Period (c/kWh) |
| --------- | -------: | ---------: | -----------------------------: |
| Morn      | \$47,528 |  1,605,949 |                          2.959 |
| Mid-Day   | \$94,633 |  2,012,553 |                          4.702 |
| Eve       | \$22,297 |    734,676 |                          3.035 |
| Overnight | \$52,670 |  2,869,278 |                          1.836 |

**NonSummer Period without Adjustments**

| Period    | Total \$ | Total kWhs | Average Rate in Period (c/kWh) |
| --------- | -------: | ---------: | -----------------------------: |
| Morn      | \$76,603 |  2,757,222 |                          2.778 |
| Mid-Day   | \$84,866 |  2,554,445 |                          3.322 |
| Eve       | \$31,030 |  1,023,637 |                          3.031 |
| Overnight | \$93,023 |  4,707,327 |                          1.976 |

(The "Average Rate in Period" column header appears only above the summer block; the nonsummer block carries the same column positions.)

<!-- EPON: midday-peak, stacking — DTOU period definitions used by the supply illustration; Mid-Day Peak = 1 pm–7 pm = hour ending 14–19, identical to the delivery (DTOU) period -->

**Delivery Service Time of Use (DTOU) Periods**

| Period       | Hours        | Hour Ending |
| ------------ | ------------ | ----------- |
| Morning      | 6 am to 1 pm | 7-13        |
| Mid-Day Peak | 1 pm to 7 pm | 14-19       |
| Evening      | 7 pm to 9 pm | 20-21       |
| Overnight    | 9 pm to 6 am | 1-6, 22-24  |

**Hour Ending → Category lookup**

| Hour Ending     | Category  |
| --------------- | --------- |
| Hour01 – Hour06 | Overnight |
| Hour07 – Hour13 | Morn      |
| Hour14 – Hour19 | Mid-Day   |
| Hour20 – Hour21 | Eve       |
| Hour22 – Hour24 | Overnight |

(Printed as 24 individual rows, Hour01 … Hour24, each with its Category; compressed here into ranges with no loss of information.)

### Hourly rows (print area: 1/1/2023 Hour01 through 1/5/2023 Hour06; 102 rows)

Columns as printed: Date; Data (hour ending); Category; Month; Summer or Nonsummer; Interval; **RTOUPP Load** (grey-shaded column); **PJM Price** (orange-shaded column); **Weighted Residential Distribution Loss Factor to Add**; **Adjusted Hourly Supply Price**; **Total Estimated Revenue**.

<!-- EPON: profile — the load shape (historical Rate RTOUPP load) and 2023 PJM hourly prices underlie every base period price; loss factor 0.0522 is the participant-weighted residential distribution loss factor (page 4) -->

| Date     | Data (hour ending) | Category  | Month | Summer (S) or Nonsummer (N) | Interval | RTOUPP Load | PJM Price | Weighted Residential Distribution Loss Factor to Add | Adjusted Hourly Supply Price | Total Estimated Revenue |
| -------- | ------------------ | --------- | ----: | --------------------------- | -------: | ----------: | --------: | ---------------------------------------------------: | ---------------------------: | ----------------------: |
| 1/1/2023 | Hour01             | Overnight |     1 | N                           |        1 |    2,241.34 |     15.54 |                                              0.05220 |                   0.01634786 |                    \$37 |
| 1/1/2023 | Hour02             | Overnight |     1 | N                           |        2 |    2,106.00 |     14.33 |                                              0.05220 |                  0.015077184 |                    \$32 |
| 1/1/2023 | Hour03             | Overnight |     1 | N                           |        3 |    1,983.12 |     13.53 |                                              0.05220 |                  0.014231439 |                    \$28 |
| 1/1/2023 | Hour04             | Overnight |     1 | N                           |        4 |    1,883.34 |     13.86 |                                              0.05220 |                  0.014583767 |                    \$27 |
| 1/1/2023 | Hour05             | Overnight |     1 | N                           |        5 |    1,841.13 |     15.29 |                                              0.05220 |                    0.0160892 |                    \$30 |
| 1/1/2023 | Hour06             | Overnight |     1 | N                           |        6 |    1,703.49 |     15.60 |                                              0.05220 |                  0.016412233 |                    \$28 |
| 1/1/2023 | Hour07             | Morn      |     1 | N                           |        7 |    1,645.70 |     17.68 |                                              0.05220 |                  0.018599677 |                    \$31 |
| 1/1/2023 | Hour08             | Morn      |     1 | N                           |        8 |    1,614.79 |     20.39 |                                              0.05220 |                  0.021449625 |                    \$35 |
| 1/1/2023 | Hour09             | Morn      |     1 | N                           |        9 |    1,618.82 |     22.34 |                                              0.05220 |                  0.023502385 |                    \$38 |
| 1/1/2023 | Hour10             | Morn      |     1 | N                           |       10 |    1,692.21 |     22.64 |                                              0.05220 |                  0.023818211 |                    \$40 |
| 1/1/2023 | Hour11             | Morn      |     1 | N                           |       11 |    1,758.21 |     22.09 |                                              0.05220 |                  0.023245445 |                    \$41 |
| 1/1/2023 | Hour12             | Morn      |     1 | N                           |       12 |    1,813.27 |     21.32 |                                              0.05220 |                  0.022431815 |                    \$41 |
| 1/1/2023 | Hour13             | Morn      |     1 | N                           |       13 |    1,882.14 |     20.28 |                                              0.05220 |                  0.021335308 |                    \$40 |
| 1/1/2023 | Hour14             | Mid-Day   |     1 | N                           |       14 |    1,826.51 |     19.95 |                                              0.05220 |                  0.020993905 |                    \$38 |
| 1/1/2023 | Hour15             | Mid-Day   |     1 | N                           |       15 |    1,795.58 |     18.75 |                                              0.05220 |                  0.019724236 |                    \$35 |
| 1/1/2023 | Hour16             | Mid-Day   |     1 | N                           |       16 |    1,861.19 |     20.90 |                                              0.05220 |                  0.021991687 |                    \$41 |
| 1/1/2023 | Hour17             | Mid-Day   |     1 | N                           |       17 |    2,050.85 |     26.56 |                                              0.05220 |                  0.027941335 |                    \$57 |
| 1/1/2023 | Hour18             | Mid-Day   |     1 | N                           |       18 |    2,237.30 |     28.71 |                                              0.05220 |                  0.030213881 |                    \$68 |
| 1/1/2023 | Hour19             | Mid-Day   |     1 | N                           |       19 |    2,228.77 |     27.34 |                                              0.05220 |                  0.028767225 |                    \$64 |
| 1/1/2023 | Hour20             | Eve       |     1 | N                           |       20 |    2,175.30 |     26.34 |                                              0.05220 |                  0.027711001 |                    \$60 |
| 1/1/2023 | Hour21             | Eve       |     1 | N                           |       21 |    2,151.01 |     25.53 |                                              0.05220 |                  0.026859277 |                    \$58 |
| 1/1/2023 | Hour22             | Overnight |     1 | N                           |       22 |    2,090.08 |     22.60 |                                              0.05220 |                  0.023784237 |                    \$50 |
| 1/1/2023 | Hour23             | Overnight |     1 | N                           |       23 |    2,371.85 |     18.96 |                                              0.05220 |                  0.019944526 |                    \$47 |
| 1/1/2023 | Hour24             | Overnight |     1 | N                           |       24 |    2,266.30 |     19.63 |                                              0.05220 |                  0.020658016 |                    \$47 |
| 1/2/2023 | Hour01             | Overnight |     1 | N                           |        1 |    2,072.53 |     21.29 |                                              0.05220 |                  0.022399677 |                    \$46 |
| 1/2/2023 | Hour02             | Overnight |     1 | N                           |        2 |    1,881.60 |     19.54 |                                              0.05220 |                  0.020558753 |                    \$39 |
| 1/2/2023 | Hour03             | Overnight |     1 | N                           |        3 |    1,752.31 |     19.59 |                                              0.05220 |                  0.020613782 |                    \$36 |
| 1/2/2023 | Hour04             | Overnight |     1 | N                           |        4 |    1,732.48 |     21.60 |                                              0.05220 |                  0.022724578 |                    \$39 |
| 1/2/2023 | Hour05             | Overnight |     1 | N                           |        5 |    1,787.78 |     24.87 |                                              0.05220 |                   0.02617211 |                    \$47 |
| 1/2/2023 | Hour06             | Overnight |     1 | N                           |        6 |    1,735.79 |     32.40 |                                              0.05220 |                   0.03408913 |                    \$59 |
| 1/2/2023 | Hour07             | Morn      |     1 | N                           |        7 |    1,616.38 |     34.98 |                                              0.05220 |                  0.036805838 |                    \$59 |
| 1/2/2023 | Hour08             | Morn      |     1 | N                           |        8 |    1,621.70 |     35.52 |                                              0.05220 |                  0.037376856 |                    \$61 |
| 1/2/2023 | Hour09             | Morn      |     1 | N                           |        9 |    1,706.77 |     34.29 |                                              0.05220 |                  0.036080793 |                    \$62 |
| 1/2/2023 | Hour10             | Morn      |     1 | N                           |       10 |    1,741.96 |     33.33 |                                              0.05220 |                  0.035070531 |                    \$61 |
| 1/2/2023 | Hour11             | Morn      |     1 | N                           |       11 |    1,749.66 |     33.21 |                                              0.05220 |                  0.034948109 |                    \$61 |
| 1/2/2023 | Hour12             | Morn      |     1 | N                           |       12 |    1,756.58 |     31.65 |                                              0.05220 |                  0.033301786 |                    \$58 |
| 1/2/2023 | Hour13             | Morn      |     1 | N                           |       13 |    1,787.83 |     28.52 |                                              0.05220 |                  0.030008655 |                    \$54 |
| 1/2/2023 | Hour14             | Mid-Day   |     1 | N                           |       14 |    1,814.98 |     27.04 |                                              0.05220 |                  0.028454954 |                    \$52 |
| 1/2/2023 | Hour15             | Mid-Day   |     1 | N                           |       15 |    1,786.65 |     27.41 |                                              0.05220 |                  0.028839204 |                    \$52 |
| 1/2/2023 | Hour16             | Mid-Day   |     1 | N                           |       16 |    1,860.59 |     28.44 |                                              0.05220 |                  0.029919466 |                    \$56 |
| 1/2/2023 | Hour17             | Mid-Day   |     1 | N                           |       17 |    2,053.93 |     33.05 |                                              0.05220 |                  0.034776225 |                    \$71 |
| 1/2/2023 | Hour18             | Mid-Day   |     1 | N                           |       18 |    2,266.63 |     32.44 |                                              0.05220 |                  0.034136425 |                    \$77 |
| 1/2/2023 | Hour19             | Mid-Day   |     1 | N                           |       19 |    2,284.93 |     29.61 |                                              0.05220 |                   0.03115866 |                    \$71 |
| 1/2/2023 | Hour20             | Eve       |     1 | N                           |       20 |    2,272.45 |     26.61 |                                              0.05220 |                  0.028001538 |                    \$64 |
| 1/2/2023 | Hour21             | Eve       |     1 | N                           |       21 |    2,237.03 |     24.72 |                                              0.05220 |                   0.02600519 |                    \$58 |
| 1/2/2023 | Hour22             | Overnight |     1 | N                           |       22 |    2,158.74 |     22.18 |                                              0.05220 |                  0.023333312 |                    \$50 |
| 1/2/2023 | Hour23             | Overnight |     1 | N                           |       23 |    2,461.10 |     18.80 |                                              0.05220 |                  0.019780918 |                    \$49 |
| 1/2/2023 | Hour24             | Overnight |     1 | N                           |       24 |    2,363.76 |     20.19 |                                              0.05220 |                  0.021242971 |                    \$50 |
| 1/3/2023 | Hour01             | Overnight |     1 | N                           |        1 |    2,208.88 |     19.20 |                                              0.05220 |                  0.020204062 |                    \$45 |
| 1/3/2023 | Hour02             | Overnight |     1 | N                           |        2 |    1,961.21 |     18.19 |                                              0.05220 |                   0.01914147 |                    \$38 |
| 1/3/2023 | Hour03             | Overnight |     1 | N                           |        3 |    1,855.62 |     18.86 |                                              0.05220 |                  0.019839389 |                    \$37 |
| 1/3/2023 | Hour04             | Overnight |     1 | N                           |        4 |    1,800.22 |     20.74 |                                              0.05220 |                  0.021824722 |                    \$39 |
| 1/3/2023 | Hour05             | Overnight |     1 | N                           |        5 |    1,780.15 |     26.14 |                                              0.05220 |                  0.027508148 |                    \$49 |
| 1/3/2023 | Hour06             | Overnight |     1 | N                           |        6 |    1,774.02 |     30.90 |                                              0.05220 |                  0.032512035 |                    \$58 |
| 1/3/2023 | Hour07             | Morn      |     1 | N                           |        7 |    1,670.49 |     37.10 |                                              0.05220 |                  0.039037392 |                    \$65 |
| 1/3/2023 | Hour08             | Morn      |     1 | N                           |        8 |    1,690.52 |     35.52 |                                              0.05220 |                  0.037377158 |                    \$63 |
| 1/3/2023 | Hour09             | Morn      |     1 | N                           |        9 |    1,691.02 |     32.75 |                                              0.05220 |                  0.034456261 |                    \$58 |
| 1/3/2023 | Hour10             | Morn      |     1 | N                           |       10 |    1,735.11 |     31.44 |                                              0.05220 |                   0.03307809 |                    \$57 |
| 1/3/2023 | Hour11             | Morn      |     1 | N                           |       11 |    1,744.28 |     28.77 |                                              0.05220 |                  0.030267474 |                    \$53 |
| 1/3/2023 | Hour12             | Morn      |     1 | N                           |       12 |    1,718.59 |     24.40 |                                              0.05220 |                  0.025669996 |                    \$44 |
| 1/3/2023 | Hour13             | Morn      |     1 | N                           |       13 |    1,735.95 |     22.74 |                                              0.05220 |                  0.023925248 |                    \$42 |
| 1/3/2023 | Hour14             | Mid-Day   |     1 | N                           |       14 |    1,737.63 |     20.56 |                                              0.05220 |                  0.021637842 |                    \$38 |
| 1/3/2023 | Hour15             | Mid-Day   |     1 | N                           |       15 |    1,737.16 |     20.10 |                                              0.05220 |                  0.021149798 |                    \$37 |
| 1/3/2023 | Hour16             | Mid-Day   |     1 | N                           |       16 |    1,769.52 |     23.30 |                                              0.05220 |                  0.024512231 |                    \$43 |
| 1/3/2023 | Hour17             | Mid-Day   |     1 | N                           |       17 |    1,918.20 |     35.03 |                                              0.05220 |                  0.036853891 |                    \$71 |
| 1/3/2023 | Hour18             | Mid-Day   |     1 | N                           |       18 |    2,153.79 |     36.98 |                                              0.05220 |                  0.038913064 |                    \$84 |
| 1/3/2023 | Hour19             | Mid-Day   |     1 | N                           |       19 |    2,263.75 |     34.25 |                                              0.05220 |                  0.036038428 |                    \$82 |
| 1/3/2023 | Hour20             | Eve       |     1 | N                           |       20 |    2,261.26 |     31.75 |                                              0.05220 |                  0.033411076 |                    \$76 |
| 1/3/2023 | Hour21             | Eve       |     1 | N                           |       21 |    2,162.73 |     31.38 |                                              0.05220 |                   0.03301905 |                    \$71 |
| 1/3/2023 | Hour22             | Overnight |     1 | N                           |       22 |    2,089.33 |     28.08 |                                              0.05220 |                  0.029547266 |                    \$62 |
| 1/3/2023 | Hour23             | Overnight |     1 | N                           |       23 |    2,357.03 |     24.44 |                                              0.05220 |                  0.025716699 |                    \$61 |
| 1/3/2023 | Hour24             | Overnight |     1 | N                           |       24 |    2,260.50 |     21.17 |                                              0.05220 |                  0.022276685 |                    \$50 |
| 1/4/2023 | Hour01             | Overnight |     1 | N                           |        1 |    2,135.10 |     20.63 |                                              0.05220 |                  0.021704001 |                    \$46 |
| 1/4/2023 | Hour02             | Overnight |     1 | N                           |        2 |    1,981.37 |     20.45 |                                              0.05220 |                  0.021515455 |                    \$43 |
| 1/4/2023 | Hour03             | Overnight |     1 | N                           |        3 |    1,812.50 |     20.79 |                                              0.05220 |                   0.02187038 |                    \$40 |
| 1/4/2023 | Hour04             | Overnight |     1 | N                           |        4 |    1,762.94 |     21.77 |                                              0.05220 |                  0.022905309 |                    \$40 |
| 1/4/2023 | Hour05             | Overnight |     1 | N                           |        5 |    1,773.33 |     27.42 |                                              0.05220 |                  0.028852078 |                    \$51 |
| 1/4/2023 | Hour06             | Overnight |     1 | N                           |        6 |    1,715.90 |     37.07 |                                              0.05220 |                  0.039005458 |                    \$67 |
| 1/4/2023 | Hour07             | Morn      |     1 | N                           |        7 |    1,640.34 |     42.60 |                                              0.05220 |                  0.044821079 |                    \$74 |
| 1/4/2023 | Hour08             | Morn      |     1 | N                           |        8 |    1,710.41 |     30.39 |                                              0.05220 |                  0.031980917 |                    \$55 |
| 1/4/2023 | Hour09             | Morn      |     1 | N                           |        9 |    1,703.19 |     24.07 |                                              0.05220 |                  0.025325424 |                    \$43 |
| 1/4/2023 | Hour10             | Morn      |     1 | N                           |       10 |    1,736.44 |     22.45 |                                              0.05220 |                  0.023617665 |                    \$41 |
| 1/4/2023 | Hour11             | Morn      |     1 | N                           |       11 |    1,720.98 |     21.15 |                                              0.05220 |                  0.022258947 |                    \$38 |
| 1/4/2023 | Hour12             | Morn      |     1 | N                           |       12 |    1,705.72 |     20.56 |                                              0.05220 |                  0.021635582 |                    \$37 |
| 1/4/2023 | Hour13             | Morn      |     1 | N                           |       13 |    1,788.26 |     19.41 |                                              0.05220 |                  0.020419901 |                    \$37 |
| 1/4/2023 | Hour14             | Mid-Day   |     1 | N                           |       14 |    1,782.56 |     18.16 |                                              0.05220 |                  0.019107117 |                    \$34 |
| 1/4/2023 | Hour15             | Mid-Day   |     1 | N                           |       15 |    1,839.49 |     18.13 |                                              0.05220 |                  0.019071793 |                    \$35 |
| 1/4/2023 | Hour16             | Mid-Day   |     1 | N                           |       16 |    1,901.72 |     19.75 |                                              0.05220 |                  0.020779826 |                    \$40 |
| 1/4/2023 | Hour17             | Mid-Day   |     1 | N                           |       17 |    2,078.30 |     29.55 |                                              0.05220 |                  0.031094544 |                    \$65 |
| 1/4/2023 | Hour18             | Mid-Day   |     1 | N                           |       18 |    2,324.32 |     33.09 |                                              0.05220 |                  0.034819577 |                    \$81 |
| 1/4/2023 | Hour19             | Mid-Day   |     1 | N                           |       19 |    2,372.02 |     30.58 |                                              0.05220 |                  0.032178737 |                    \$76 |
| 1/4/2023 | Hour20             | Eve       |     1 | N                           |       20 |    2,347.60 |     22.55 |                                              0.05220 |                  0.023730228 |                    \$56 |
| 1/4/2023 | Hour21             | Eve       |     1 | N                           |       21 |    2,293.35 |     12.38 |                                              0.05220 |                  0.013028988 |                    \$30 |
| 1/4/2023 | Hour22             | Overnight |     1 | N                           |       22 |    2,254.09 |     11.36 |                                              0.05220 |                  0.011949822 |                    \$27 |
| 1/4/2023 | Hour23             | Overnight |     1 | N                           |       23 |    2,685.09 |     10.37 |                                              0.05220 |                  0.010915421 |                    \$29 |
| 1/4/2023 | Hour24             | Overnight |     1 | N                           |       24 |    2,564.71 |      8.62 |                                              0.05220 |                  0.009070315 |                    \$23 |
| 1/5/2023 | Hour01             | Overnight |     1 | N                           |        1 |    2,442.22 |      7.06 |                                              0.05220 |                   0.00742551 |                    \$18 |
| 1/5/2023 | Hour02             | Overnight |     1 | N                           |        2 |    2,202.60 |      5.97 |                                              0.05220 |                  0.006283011 |                    \$14 |
| 1/5/2023 | Hour03             | Overnight |     1 | N                           |        3 |    2,004.24 |      7.22 |                                              0.05220 |                  0.007597105 |                    \$15 |
| 1/5/2023 | Hour04             | Overnight |     1 | N                           |        4 |    1,998.63 |      6.96 |                                              0.05220 |                  0.007323554 |                    \$15 |
| 1/5/2023 | Hour05             | Overnight |     1 | N                           |        5 |    1,959.51 |      8.19 |                                              0.05220 |                  0.008619517 |                    \$17 |
| 1/5/2023 | Hour06             | Overnight |     1 | N                           |        6 |    1,847.39 |     14.75 |                                              0.05220 |                  0.015519023 |                    \$29 |

[p. 4]

## Page 4 — Weighted residential loss factor

_Illustrative Example_. **Start Date:** 1/1/2023.

<!-- EPON: profile — "participant" kWh weights (Historical Rate RTOUPP billing usage, March 2023) by housing group; single-family-without-electric-space-heat dominates (about 84% of participant kWh) -->

| Customer group                                                                        | Participant kWhs (from monthly billing data) (2) | Loss Factors (1) |
| ------------------------------------------------------------------------------------- | -----------------------------------------------: | ---------------: |
| Single Family Without Electric Space Heat                                             |                                        1,110,619 |           0.0517 |
| Multi Family Without Electric Space Heat                                              |                                          127,143 |           0.0532 |
| Single Family With Electric Space Heat                                                |                                           28,533 |           0.0554 |
| Multi Family Without Electric Space Heat [sic; presumably "With" Electric Space Heat] |                                           62,984 |           0.0567 |
| **Weighted Residential Loss Factor**                                                  |                                                  |       **0.0522** |

Notes:

1. Distribution Loss Factors as listed in Informational Sheet No. 33.
2. Historial [sic; Historical] Rate RTOUPP billing usage for the billing month March 2023.
