---
source_file: "Eversource - 2026 - Docket 26-05-10 Exhibit CLP-RATES-6.pdf"
citekey: clp_Docket260510Exhibit_2026i
docket: "26-05-10"
utility: The Connecticut Light and Power Company d/b/a Eversource Energy
filer: The Connecticut Light and Power Company d/b/a Eversource Energy
document_type: exhibit
pages_total: 3
extraction_scope: full
citation_scheme: page_line
context: Supporting schedule to the Davis and Parsons joint direct testimony (Exhibit CLP-RATES-1) in CL&P's 2026 rate case, Connecticut PURA Docket 26-05-10. It sets the proposed distribution rates for Rate 6, the optional residential space heating rate (not stated in the PDF itself; extractor note).
contents: Page 1 is the cover and contents. Page 2 is the Rate 6 rate design worksheet, a two-column Excel print. The left column builds the customer charge and the Block 1 and winter Block 2 energy charges from proposed Rate 1 revenues. The right column rebuilds the winter Block 2 rate from marginal facilities cost, marginal energy cost and a coincidence-factor-adjusted residual. Page 3 shows the Rate 6 and Rate 1 distribution rates, the Rate 6 minus Rate 1 differences, an illustrative monthly bill-impact table, and an embedded consumption-profile chart.
why_here: Shows how Eversource derives the Rate 6 Block 1 rate ($0.09431/kWh) and the discounted winter Block 2 rate ($0.07517/kWh), and whether any line of the worksheet recovers the Block 2 discount elsewhere. Use it for questions on the heat pump (space heating) rate design.
---

# Exhibit CLP-RATES-6 — Rate 6 Optional Residential Space Heating Rate (Rate Design Worksheet and Bill Impacts)

**Source**: `Exhibit CLP-RATES-6.pdf` (Excel print of `Exhibit CLP-RATES-6.xlsx`)
**Pages**: 3 total (cover/TOC + worksheet + rates/bill-impacts)
**Date**: Printed July 13, 2026 (PDF metadata `creationDate`); filed with the July 14, 2026 rate-case application
**Author(s)**: Kimberly Parsons (PDF metadata author)
**Author affiliations**: None on the exhibit (supporting schedules to Davis & Parsons joint testimony, Exhibit CLP-RATES-1)
**Docket**: Connecticut PURA Docket No. 26-05-10 — Application of The Connecticut Light and Power Company d/b/a Eversource Energy to Amend Its Rate Schedules
**Exhibit**: CLP-RATES-6

**Extraction method**: PyMuPDF text + word coordinates, then page renders to reconstruct the two-column worksheet (page 2) and the Rate 6 vs Rate 1 layout plus embedded bar chart (page 3). Page and line markers were added afterwards from the PDF's text layer (`just sources-page-skeleton`; checked with `just sources-check-pages`). The PDF prints Excel row numbers in the left margin (1–49 on page 2; 1–64 on page 3), and these are treated as the margin line numbers: `{n}` is the Excel row. Each worksheet row is one markdown line (on page 2, one table row that carries both columns), so a row number cites both the left-column and right-column items printed on that row. Page 2 rows 1–9 are printed in the margin but are not recognised as line numbers by the page-line tooling (they sit slightly off the column of rows 10–49), so rows 1–9 on page 2 carry no `{n}`; Marginal Customer Cost (row 9) is cited by page only. Dollar signs that the print placed in a separate column are shown with the values. Row labels in the first column of the page 3 rate table ("Threshold", "Distribution energy") and the labels "Left"/"Right" in the page 2 table header are extractor additions, not source text.

Note: Minor typographical errors in the source (double closing parenthesis in `(l=k/h))`, `Energy_Charge` underscore) are preserved where they appear in labels. Substantive formula notes are annotated inline. Page 2 transcription was checked against the PDF's text layer for this repair; no values in the earlier extract needed correcting.

_Extractor note (not source text):_ **How to read this exhibit.** Page 2 is a two-column Excel print. The **left** column builds the Rate 6 customer charge from marginal customer cost + GET, then backs a class-level energy-charge revenue requirement out of proposed Rate 1 customer-charge and energy-charge revenues, yielding Block 1 `$0.09431/kWh` and winter Block 2 `$0.07517/kWh`. The **right** column (“MC Based Distribution EC Rate Detail”) shows why that winter tail rate equals unit facilities-cost recovery + energy MC + a coincidence-factor-reduced residual. Page 3 applies those rates to an illustrative monthly kWh profile versus Rate 1. GET throughout is **6.80%** (gross earnings tax), applied as a mark-up on pre-GET unit costs. The letter keys (b), (h), (i), (j) etc. are reused in the two columns with different meanings (for example, (j) is the Distribution Energy Charge Discount on the left and Marginal Facilities Cost on the right).

---

[PDF p. 1 | printed p. 1]

## Cover (page 1 of 3)

The Connecticut Light and Power Company\
d/b/a Eversource Energy\
Docket No. 26-05-10\
Exhibit CLP-RATES-6\
Page 1 of 3

**EXHIBIT CLP-RATES-6**\
**Rate 6 - Optional Residential Space Heating Rate**

| Contents                                  | Page |
| ----------------------------------------- | ---- |
| Rate 6 Rate Design Worksheet              | 2    |
| Rate 6 Distribution Rate and Bill Impacts | 3    |

---

[PDF p. 2 | printed p. 2]

## Page 2 of 3 — Rate 6 Rate Design Worksheet

The Connecticut Light & Power Company dba Eversource Energy\
Docket No. 26-05-10

Customer Charge (Excel rows 8–11):

| Customer Charge (left column)                   | Value               |
| ----------------------------------------------- | ------------------- |
| Marginal Customer Cost (row 9, no `{n}` marker) | $28.98 /cust-mo     |
| {10} GET                                        | 6.80%               |
| {11} Rate 6 Customer Charge (a)                 | **$30.95** /cust-mo |

Distribution Energy Charge worksheet. The two columns of the Excel print share row numbers, so each row below carries a left-column item and value and a right-column item and value (the right column is headed “MC Based Distribution EC Rate Detail”; its section labels A–E are printed as `A.Base FC Recovery`, `B.Marginal Cost`, `C.Subtotal (A + B)`, `D.Reconciliation Adjustment`, `E.Winter Block 2 Rate`). Blank rows (12, 22, 29, 34, 36, 40, 42, 47) are left out. Rows 43–49 (the coincidence-factor notes) are printed in the right column.

| Left column: item                              | Left column: value | Right column: item                   | Right column: value |
| ---------------------------------------------- | ------------------ | ------------------------------------ | ------------------- |
| {13} Distribution Energy Charge                |                    | MC Based Distribution EC Rate Detail |                     |
| {14} Customer Billing Months (b)               | 12,555,775         | A. Base FC Recovery                  |                     |
| {15} Adjusted CC Revenue (c=a×b)               | $388,609,278       | Marginal Facilities Cost (j)         | $24.51              |
| {16}                                           |                    | Customer Billing Months (b)          | 12,555,775          |
| {17} Proposed CC Revenue (d)                   | $155,195,848       | MFC Revenue (k)                      | 307,742,050.2       |
| {18} Energy Charge Adj. (e=d−c)                | $(233,413,430)     | RY Billed kWh (h)                    | 8,440,783,007       |
| {19} Proposed EC Revenue (f)                   | $1,029,467,601     | Unit FC Recovery (l=k/h))            | $0.03646            |
| {20} Energy Charge Adj. (e)                    | $(233,413,430)     | GET                                  | 6.80%               |
| {21} Rate 6 EC Revenue Requirement (g=f−e)     | $796,054,171       | Unit FC Recovery (w/GET) (m)         | **$0.03894** /kWh   |
| {23} RY Billed kWh (h)                         | 8,440,783,007      | B. Marginal Cost                     |                     |
| {24} Rate 6 Block 1 Energy Charge (i=g/h)      | **$0.09431** /kWh  | MC Energy \*\*\*                     | $0.00242            |
| {25}                                           |                    | GET                                  | 6.80%               |
| {26} Distribution Energy Charge Discount (j)   | $(0.01914) /kWh    | MC w/GET (o)                         | **$0.00258** /kWh   |
| {27} Rate 6 Block 2 Winter Energy Charge (i+j) | **$0.07517** /kWh  |                                      |                     |
| {28}                                           |                    | C. Subtotal (A + B)                  | **$0.04152** /kWh   |
| {30}                                           |                    | D. Reconciliation Adjustment         |                     |
| {31}                                           |                    | Rate 6 EC (block 1) (i)              | $0.09431 /kWh       |
| {32}                                           |                    | Unit FC Recovery (m)                 | −$0.03894 /kWh      |
| {33}                                           |                    | Difference (n)                       | $0.05537 /kWh       |
| {35}                                           |                    | MC Energy (o)                        | $0.00258 /kWh       |
| {37}                                           |                    | Incr above MC (p = n − o)            | $0.05279 /kWh       |
| {38}                                           |                    | Coinc. Fct. Adj. \* (q)              | 63.7%               |
| {39}                                           |                    | Reduced Reconciliation Adj. (r)      | **$0.03365** /kWh   |
| {41}                                           |                    | E. Winter Block 2 Rate               | **$0.07517** /kWh   |
| {43}                                           |                    | \*System Peak CF Adj                 |                     |
| {44}                                           |                    | CF w/ space htg \*\*                 | 25.6%               |
| {45}                                           |                    | CF w/o space htg \*\*                | 40.1%               |
| {46}                                           |                    | Ratio                                | 63.7%               |
| {48}                                           |                    | \*\* source: Load Research           |                     |
| {49}                                           |                    | \*\*\* source: MCOS Study            |                     |

_Extractor notes (not source text): arithmetic checks on page 2._

- Left column: line 11 (a) × line 14 (b) is `$30.95 × 12,555,775 ≈ $388,601,236`; the printed (c) is `$388,609,278`. The difference is about `$8,000`, which is consistent with (c) using the unrounded customer charge (`$28.98 × 1.0680 = $30.9506`) rather than the printed `$30.95`; transcribed as printed.
- (e=d−c) = `$155,195,848 − $388,609,278 = $(233,413,430)`.
- The label (g=f−e) uses the **absolute** energy-charge adjustment: `$1,029,467,601 − $233,413,430 = $796,054,171` (not `f` minus the signed negative e).
- (i=g/h) = `$796,054,171 / 8,440,783,007 = $0.09431/kWh`. The divisor (h) is all RY billed kWh on row 23; the worksheet does not split that kWh by block or season.
- Winter Block 2 = `$0.09431 + (−$0.01914) = $0.07517/kWh`.
- Right column: (k) ≈ `$24.51 × 12,555,775`; (m) = `$0.03646 × 1.0680 = $0.03894/kWh`; Subtotal C = `$0.03894 + $0.00258 = $0.04152`; (n) = `$0.09431 − $0.03894`; (p) = `$0.05537 − $0.00258`; (r) = `$0.05279 × 63.7% ≈ $0.03365`; E = `C + r` = `$0.04152 + $0.03365 = $0.07517`, which matches left-column row 27.
- Ratio = `25.6% / 40.1% ≈ 63.8%`, printed as **63.7%**. [source discrepancy: the printed ratio is 63.7%; the printed inputs give 63.8% when rounded.]

---

[PDF p. 3 | printed p. 3]

## Page 3 of 3 — Rate 6 Distribution Rate and Bill Impacts

{1} **EXHIBIT CLP-RATES-6**
{3} **Rate 6 Distribution Rate and Bill Impacts**
{5} The Connecticut Light & Power Company dba Eversource Energy
{6} Docket No. 26-05-10

### Proposed distribution rates (Rate 6 vs Rate 1)

_Extractor note (not source text):_ Rate 6 is the only rate on this page with a seasonal 700 kWh block. Rate 1 is a single volumetric distribution energy charge.

| Rate 6 (left side of page)              | Rate 1 (right side of page)    |
| --------------------------------------- | ------------------------------ |
| {9} **Rate 6 Distribution Rates**       | **Rate 1 Distribution Rates**  |
| {11} Customer Charge: $30.95 /month     | Customer Charge: $12.36 /month |
| {13} Distribution Energy Charge ($/kWh) | Energy Charge: $0.12196 /kWh   |

Rate 6 distribution energy charge by season and block (rows 14–19):

|                          | Heating (Nov–Mar) | Heating (Nov–Mar) | Non-Heating (Apr–Oct) | Non-Heating (Apr–Oct) |
| ------------------------ | ----------------- | ----------------- | --------------------- | --------------------- |
| {14-15}                  |                   |                   |                       |                       |
| {16}                     | Block 1           | Block 2           | Block 1               | Block 2               |
| {17} Threshold           | ≤ 700 kWh         | > 700 kWh         | ≤ 700 kWh             | > 700 kWh             |
| {19} Distribution energy | **$0.09431**      | **$0.07517**      | **$0.09431**          | **$0.09431**          |

### Rate Changes (Rate 6 versus Rate 1)

{22} **Rate Changes (Rate 6 versus Rate 1):**

- {24} Customer Charge: $18.59 /month
- {25} Energy_Charge
  - {26} All Hours: (0.02765) /kWh
  - {27} Winter: $(0.04679) /kWh

_Extractor note (not source text):_ `$30.95 − $12.36 = $18.59`. All-hours (Block 1) delta = `$0.09431 − $0.12196 = $(0.02765)`. Winter Block 2 delta = `$0.07517 − $0.12196 = $(0.04679)`.

### Illustrative monthly bill-impact table

Columns after the kWh split are **dollar bill deltas vs Rate 1** for the same kWh: the extra customer charge, the all-hours (non-heating / Block 1) energy delta, the winter Block 2 (heating) energy delta, and the net. The printed column headings wrap over rows 28–30; rows 29–30 are numbered as one header row below.

| {29-30} Month | Total (kWh) | Block 1 & Block 2 (Non-heating) (kWh) | Block 2 (Heating) (kWh) | CC ($)  | Block 1 & Block 2 (Non-heating) ($) | Block 2 (Heating) ($) | Net Bill Impact ($) |
| ------------- | ----------- | ------------------------------------- | ----------------------- | ------- | ----------------------------------- | --------------------- | ------------------- |
| {31} 1        | 1,550       | 700                                   | 850                     | $18.59  | $(19.36)                            | $(39.77)              | $(40.54)            |
| {32} 2        | 1,300       | 700                                   | 600                     | 18.59   | (19.36)                             | (28.08)               | (28.84)             |
| {33} 3        | 1,000       | 700                                   | 300                     | 18.59   | (19.36)                             | (14.04)               | (14.81)             |
| {34} 4        | 800         | 800                                   | —                       | 18.59   | (22.12)                             | —                     | (3.53)              |
| {35} 5        | 800         | 800                                   | —                       | 18.59   | (22.12)                             | —                     | (3.53)              |
| {36} 6        | 900         | 900                                   | —                       | 18.59   | (24.89)                             | —                     | (6.30)              |
| {37} 7        | 1,500       | 1,500                                 | —                       | 18.59   | (41.48)                             | —                     | (22.89)             |
| {38} 8        | 1,500       | 1,500                                 | —                       | 18.59   | (41.48)                             | —                     | (22.89)             |
| {39} 9        | 1,000       | 1,000                                 | —                       | 18.59   | (27.65)                             | —                     | (9.06)              |
| {40} 10       | 800         | 800                                   | —                       | 18.59   | (22.12)                             | —                     | (3.53)              |
| {41} 11       | 1,200       | 700                                   | 500                     | 18.59   | (19.36)                             | (23.40)               | (24.16)             |
| {42} 12       | 1,450       | 700                                   | 750                     | 18.59   | (19.36)                             | (35.10)               | (35.86)             |
| {43} Total    | 13,800      | 10,800                                | 3,000                   | $223.08 | $(298.65)                           | $(140.38)             | $(215.95)           |

_Extractor notes (not source text):_

- Heating months (1–3, 11–12, i.e. Nov–Mar) put the first 700 kWh in “Block 1 & Block 2 (Non-heating)” and kWh above 700 in “Block 2 (Heating)”. Non-heating months (4–10) put all kWh in the non-heating column; the heating-dollar column is a dash.
- Annual net: extra customer charges of `$223.08` (`$18.59 × 12`) are more than offset by volumetric reductions of `$298.65 + $140.38`, for a **$(215.95)** illustrative annual distribution-bill decrease versus Rate 1.
- Spot checks against the stated rate deltas: heating-month Block 1 dollars = `700 × $(0.02765) = $(19.355) ≈ $(19.36)`; month 1 heating Block 2 = `850 × $(0.04679) = $(39.77)`; month 7 all-hours = `1,500 × $(0.02765) = $(41.475) ≈ $(41.48)`.
- The monthly kWh profile appears to have the same shape as the CLF-001 “700 kWh annual-average Rate 1” months scaled up (winter and summer peaks), with heating-season kWh above 700 treated as incremental space-heating load. This comparison was not verified against the CLF-001 document.

### Chart (page 3, bottom)

The source introduces the figure under the bill-impact table (Excel rows 47–64). Title and series names are in the embedded chart image, not in the selectable worksheet text.

{47-64} [DIAGRAM DESCRIPTION: Residential Rate 6 — Illustrative Regular and Incremental Consumption Profile]

A vertical stacked-bar chart of monthly kWh for calendar months 1–12 (x-axis). The y-axis is kWh from 0 to 1800 with major ticks every 200. A horizontal **black dashed line** at **700 kWh** is the Block 1 / Block 2 **Breakpoint**.

Each month is a stacked bar with up to three series (legend, left to right):

- **Regular w/o HP** — dark blue (bottom of each bar). In every month this segment reaches about the 700 kWh breakpoint (Block 1).
- **Incremental Heating Consumption** — cyan/teal. Appears only in heating months **1, 2, 3, 11, 12** (Nov–Mar), stacked above the blue segment. Bar totals match the table: ~1,550; 1,300; 1,000; 1,200; 1,450 kWh.
- **Incremental HP Consumption** — green. Appears in non-heating months **4–10** (Apr–Oct), stacked above the blue segment. Totals match the table: ~800; 800; 900; **1,500; 1,500**; 1,000; 800 kWh. Months 7–8 are the tallest green stacks (summer cooling / other incremental HP use). Months 4, 5, and 10 are only slightly above the 700 kWh line.

The chart is the visual counterpart of the kWh columns in the bill-impact table: winter usage above 700 kWh is labeled incremental **heating**; summer usage above 700 kWh is labeled incremental **HP** (not priced at the winter Block 2 discount).

[→ See original PDF page 3 for visual rendering]
