# ComEd Ex. 19.02 — Rate BEST Illustrative Electricity Charges, Compromise Proposal (spreadsheet workpaper)

**Source**: `icc_639690_ex_19_02_compromise_bestec_illustrative_charges.pdf` (ICC e-docket file id / filing id 639690)
**Pages**: 121 (landscape workpaper print of `ComEd Ex. 19.02 - Rate BEST Illustrative Electricity Charges Compromise Proposal.xlsx`; PDF created 2025-05-12)
**Date**: Filed May 2025 with ComEd's rehearing rebuttal testimony (PDF creation date 2025-05-12); the sheets themselves carry only the placeholder "MONTH 20YY Monthly Billing Period".
**Docket**: ICC Docket No. 24-0378 (Commonwealth Edison Co., revenue-neutral tariff changes related to rate design — Rate BEST / DTOU), on Rehearing
**Author(s)**: Commonwealth Edison Company (workpaper; sponsored in rehearing rebuttal testimony ComEd Ex. 19.0, Kremer — sponsorship is not stated on the workpaper itself)
**Document type**: Exhibit — spreadsheet workpaper (illustrative charge calculation + 8,760-hour load profile)
**ComEd exhibit no.**: ComEd Ex. 19.02
**Extraction method**: Embedded PDF text (PyMuPDF; the PDF is a digital print of an Excel workbook, text is selectable), summary tables verified against rendered page images; the hourly table (pp. 4–119) parsed programmatically from word coordinates and validated (see "Validation" below).
**Extraction notes**:

- _Minor typographical errors in the source have been corrected for readability. Substantive corrections are annotated inline._
- **Boilerplate omitted** (stated once here): the page-top stamp on every page "ICC Docket No. 24-0378 (on Rehearing) / ComEd Ex. 19.02 / Page n of 121".
- **Table-footnote convention for this document**: each table's own "NOTES" are reproduced as a numbered "Notes" list immediately below the table, keeping the source numbering; reference marks in headers are kept as "(n)". Reference marks equal definitions in every table (p. 1: marks 1–6, notes 1–6; p. 2: marks 1–2, notes 1–2; p. 3: marks 1–3, notes 1–3; p. 121: marks 1–2, notes 1–2).
- **Structure of the PDF**: pp. 1–3 summary tables; pp. 4–119 the hourly profile (8,760 data rows, 76 rows/page except p. 4 = 70 rows and p. 119 = 26 rows); p. 120 a print of the first 102 hourly rows of the _same_ worksheet with extra price/revenue columns plus summary tables ("This Workpaper is set to print Page 1 only"); p. 121 participant kWh by customer group and distribution loss factors.
- **Differences from the shard description / what is NOT in pp. 4–119**: the PJM-price, loss-factor, adjusted-supply-price and revenue columns appear **only on p. 120 and only for the first 102 hours (1/1/2023 Hour01 – 1/5/2023 Hour06)**; pp. 4–119 carry only Date, Data, Category, Month, Summer-or-Nonsummer, Interval and RTOUPP Load. The column header is printed once (p. 4); it is **not** repeated on later pages.
- Cell shading in the source (yellow = Morning, pink = Mid-Day, light blue = Evening, green = Overnight; green-highlighted cells = input parameters; orange = blank adjustment input cells) is not reproduced except where noted.
- Dollar signs are escaped as `\$` in prose/tables.
- **Companion data files** (agent-generated, not source text): `../workbooks/icc_639690_ex_19_02_rtoupp_hourly_profile.csv` (the full 8,760-row table from pp. 4–119) and `../workbooks/icc_639690_ex_19_02_p120_first_102_hours_with_pjm_prices.csv` (the 102 rows printed on p. 120 with the price/revenue columns).

---

## Sheet 1 (PDF p. 1 of 121): Illustrative Residential BEST Electricity Charge Determination

**Title block**: "Illustrative Residential BEST Electricity Charge Determination / Applicable to Retail Customers Served Under Rate BEST / For Application of the MONTH 20YY Monthly Billing Period" (italic label "Illustrative Example").

The table builds the Basic Electric Service Time of Use Electricity Charges (BESTEC) in ¢/kWh from the Adjusted Residential Base Revenue (ARBREV) prices on p. 2 by applying the base uncollectible factor (SBUF) and the incremental supply uncollectible factor (ISUF). Column letters are as printed. Column groups in the printed header: "Adjusted Residential Base Revenue (ARBREV) Price (1)" covers columns a and b; "ARBREV Price w/BUF (3) (5)" covers c, d and e; "Basic Electric Service Time of Use Electricity Charge (BESTEC) (5)" covers f (ISUF), g and h.

<!-- EPON: midday-peak,capacity-mdppec,profile — compromise BESTEC: Mid-Day Peak 18.219 ¢/kWh summer / 16.814 nonsummer (vs Morning ~3.0/2.8, Overnight 1.87/2.01) because 100% of the 602,456 $ capacity cost is loaded into Mid-Day kWh (see p. 2); derived from the RTOUPP participant profile -->

| Customer Group or Subgroup | a: Summer ARBREV Price (cents/kWh) | b: Nonsummer ARBREV Price (cents/kWh) | c: SBUF (2) | d = a \* c: Summer BRBESTC w/BUF | e = b \* c: Nonsummer BRBESTC w/BUF (cents/kWh) | f: ISUF (4) | g = d \* f: Summer (6) BESTEC (cents/kWh) | h = e \* f: Nonsummer BESTEC (cents/kWh) |
| -------------------------- | ---------------------------------- | ------------------------------------- | ----------- | -------------------------------- | ----------------------------------------------- | ----------- | ----------------------------------------- | ---------------------------------------- |
| Morning                    | 2.959                              | 2.778                                 | 1.0128      | 2.997                            | 2.814                                           | 1.0053      | 3.013                                     | 2.829                                    |
| Mid-Day Peak               | 17.894                             | 16.514                                | 1.0128      | 18.123                           | 16.725                                          | 1.0053      | 18.219                                    | 16.814                                   |
| Evening                    | 3.035                              | 3.031                                 | 1.0128      | 3.074                            | 3.070                                           | 1.0053      | 3.090                                     | 3.086                                    |
| Overnight                  | 1.836                              | 1.976                                 | 1.0128      | 1.860                            | 2.001                                           | 1.0053      | 1.870                                     | 2.012                                    |

[source note on the printed column labels: the p. 1 sub-header for the SBUF-adjusted columns reads "Summer BRBESTC w/BUF" and "Nonsummer BRBESTC w/BUF (cents/kWh)"; the printed formulas are "d = a \* c", "e = b \* c", "g = d \* f", "h = e \* f".]

**Notes:**

1. Base Residential BEST Charges (BRBESTCs) from page 2, determined pursuant to Rate Basic Electric Service Time of Use (Rate BEST). Subject to rounding. [source text, sic: "Rate Basic Electric Service Time of Use (Rate BEST)"]
2. Residential Supply Base Uncollectible Cost Factor (SBUF<sub>R</sub>) determined in accordance with the provisions of Rider UF - Uncollectible Factors (Rider UF) and listed in Informational Sheet No. 21.
3. Residential BUF<sub>R</sub> multiplied times BRBESTCs pursuant to Rate BEST. Subject to rounding.
4. Residential Incremental Supply Uncollectible Cost Factors (ISUF<sub>R</sub>) as listed in Informational Sheet No. 20.
5. ISUF<sub>R</sub> applied pursuant to Rate BEST. Subject to rounding.
6. Summer BESTECs are applicable June, July, August and September monthly billing periods.

---

## Sheet 2 (PDF p. 2 of 121): Illustrative Base Residential TOU Charge Determination

**Title block**: "Illustrative Base Residential TOU Charge Determination / Applicable to Retail Customers Served Under Rate RTOUPP / For Application of the MONTH 20YY Monthly Billing Period" (italic label "Illustrative Example"). Note that this sheet is titled for **Rate RTOUPP** (ComEd's Residential Time-of-Use Pricing Pilot), not Rate BEST.

Input cell above the table: **\$ 602,456** (unlabeled in the source; the column formulas call it Cap\$; capacity costs; ties to the "Annual RPM Cost" on p. 3). Rows are the four TOU periods plus a residual row. Column letters are as printed: `p` = period, `s` = summer, `n` = nonsummer. Columns g(s), g(n) ("Adjustments per \$/kWh Rate") are shaded input cells that are **blank** in this illustrative print (no adjustment applied).

<!-- EPON: capacity-mdppec,midday-peak — capacity treatment in the compromise: 100.0% of the \$602,456 annual RPM cost recovered in Mid-Day Peak kWh (capacity adder 0.13192 \$/kWh on top of 0.04702 / 0.03322 recent energy), "Remaining % for kW-based Capacity" = 0.0% -->
<!-- EPON: profile — the kWh denominators d(s), d(n) and the recent energy prices e(s), e(n) are computed from the 1,858-participant RTOUPP hourly profile on pp. 4–119 (summer 7,222,455 kWh / nonsummer 11,042,631 kWh) -->

| Customer Group or Subgroup        | cap%(p): % of Capacity in kWh Rate | c(p) = Cap\$ \* cap%(p): Capacity Costs | d(s): Summer Estimated kWhs | d(n): Nonsummer Estimated kWhs | e(s) = a(s)/d(s): Recent Summer Energy per \$/kWh Rate | e(n) = a(n)/d(n): Recent Nonsummer Energy per \$/kWh Rate | f(p) = c(p)/(d(s)+d(n)): Capacity per \$/kWh Rate | g(s): Summer Adjustments per \$/kWh Rate (1) | g(n): Nonsummer Adjustments per \$/kWh Rate (1) | h(s) = (e(s) + f(p) + g(s)) \* 100: Summer ARBREV Price (cents/kWh) (2) | h(n) = (e(n) + f(p) + g(n)) \* 100: Nonsummer ARBREV Price (cents/kWh) (2) |
| --------------------------------- | ---------------------------------- | --------------------------------------- | --------------------------- | ------------------------------ | ------------------------------------------------------ | --------------------------------------------------------- | ------------------------------------------------- | -------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Morning                           | –                                  | \$ –                                    | 1,605,949                   | 2,757,222                      | 0.02959                                                | 0.02778                                                   | –                                                 | (blank)                                      | (blank)                                         | 2.959                                                                   | 2.778                                                                      |
| Mid-Day Peak                      | 100.0%                             | \$ 602,456                              | 2,012,553                   | 2,554,445                      | 0.04702                                                | 0.03322                                                   | 0.13192                                           | (blank)                                      | (blank)                                         | 17.894                                                                  | 16.514                                                                     |
| Evening                           | –                                  | \$ –                                    | 734,676                     | 1,023,637                      | 0.03035                                                | 0.03031                                                   | –                                                 | (blank)                                      | (blank)                                         | 3.035                                                                   | 3.031                                                                      |
| Overnight                         | –                                  | \$ –                                    | 2,869,278                   | 4,707,327                      | 0.01836                                                | 0.01976                                                   | –                                                 | (blank)                                      | (blank)                                         | 1.836                                                                   | 1.976                                                                      |
| Remaining % for kW-based Capacity | 0.0%                               |                                         |                             |                                |                                                        |                                                           |                                                   |                                              |                                                 |                                                                         |                                                                            |

("–" = the source prints "-", i.e. zero/blank in accounting format. The letters a(s), a(n) in the formulas for e(s), e(n) refer to the period \$ totals ("Total \$") shown in the right-hand table on p. 120: Summer Morning \$47,528, Mid-Day \$94,633, Evening \$22,297, Overnight \$52,670; Nonsummer Morning \$76,603, Mid-Day \$84,866, Evening \$31,030, Overnight \$93,023 — those totals are not printed on p. 2 itself.)

**Notes:**

1. Adjustments are applied to reflect current market energy prices relative to historical energy prices used to determine the base revenue.
2. Subject to rounding.

---

## Sheet 3 (PDF p. 3 of 121): Capacity Obligation and RPM Cost Check

Italic label "Illustrative Example".

**Annual RPM cost table:**

| Year      | Capacity Obligation (MW) | RPM Cost (\$/MW-Day) (1) | Annual RPM Cost (3) |
| --------- | ------------------------ | ------------------------ | ------------------- |
| 2025-2026 | 6.11                     | 270.35                   | \$ 602,456          |

**Capacity obligation build-up** (green label: "January 2024 PLCs for 1,858 accounts with 12 months of historical kWh billing data"):

<!-- EPON: profile,capacity-mdppec — the illustrative customer base is 1,858 RTOUPP accounts; capacity obligation = their Jan-2024 PLCs x PJM zonal scaling factor x forecast pool requirement; this fixed \$ amount is then loaded 100% into Mid-Day kWh rates -->

| Total PLCs (kW) | Estimated Zonal Factor (2) | Estimated Forecast Pool Requirement (2) | Capacity Obligation |
| --------------- | -------------------------- | --------------------------------------- | ------------------- |
| 4899.33         | 1.1156                     | 1.1170                                  | 6105.29             |

**Check Capacity Costs with Updated Annual Data:**

| Number of Accounts | Capacity Obligation |
| ------------------ | ------------------- |
| 1858               | 6105.2916           |

**Notes:**

1. The Net Load Price (NLP) for the ComEd Zone for the 2025/2026 delivery year posted on PJM's web site on August 16, 2024 [source inconsistency: the note says 2025/2026 but the linked file path is the 2024/2025 Third Incremental Auction]: [PJM 2024/2025 Third Incremental Auction results](https://pjm.com/-/media/markets-ops/rpm/rpm-auction-info/2024-2025/2024-2025-3ia-results.ashx)
2. The Estimated Zonal Factor and Estimated Forecast Pool Requirement published by PJM for the 2024/2025 delivery year. New numbers are posted by late May each year.
3. Subject to rounding.

(Units for the capacity obligation columns are not stated beside the "Capacity Obligation" figure in the build-up table; 6105.29 is in kW and equals 6.11 MW in the first table.)

---

## Sheets 4–119 (PDF pp. 4–119): Hourly RTOUPP load profile — "12 Months of Data for 1,858 participants"

<!-- EPON: profile — THE illustrative profile: aggregate hourly kWh of 1,858 RTOUPP (residential TOU pilot) participants, calendar 2023, total 18,265,086 kWh; Formula 1/2 weighting for every Rate BEST customer comes from this single aggregate shape -->

### Structure (verbatim description of what the pages contain)

- **Header (p. 4 only; red italic label)**: "12 Months of Data for 1,858 participants"; italic "Illustrative Example"; "Total kWhs **18,265,086**" (stated total of the RTOUPP Load column).
- **Table columns** (left of every page, one row per hour): `Date` (m/d/yyyy), `Data` (label "Hour01" … "Hour24" = hour **ending**, see key on p. 4), `Category` (Overnight / Morn / Mid-Day / Eve), `Month` (1–12), `Summer or Nonsummer` (`S` or `N`; Month and S/N print adjacent as e.g. "1 N"), `Interval` (1–24), `RTOUPP Load` (kWh in that hour for the whole 1,858-account group, 2 decimals; grey column header). Column header printed once on p. 4 and **not repeated** on pp. 5–119.
- **Rows**: 8,760 data rows = 365 days (1/1/2023 – 12/31/2023, in date order) × 24 hours. p. 4 = 70 rows (1/1/2023 Hour01 – 1/3/2023 Hour22), pp. 5–118 = 76 rows each, p. 119 = 26 rows (ends 12/31/2023 Hour24). First data row corresponds to worksheet row 4 (see "rows 3628-6555" below).
- **Coding**: `Category` by hour-ending label — Hour01–Hour06 Overnight; Hour07–Hour13 Morn; Hour14–Hour19 Mid-Day; Hour20–Hour21 Eve; Hour22–Hour24 Overnight (key table printed on p. 4 and p. 120: "Hour Ending / Category"). `Summer or Nonsummer` = `S` for months 6–9 (June–September; consistent with note (6) on p. 1), `N` otherwise. `Interval` equals the hour number.
- **Right-hand tables (p. 4 only)** — period subtotals of the RTOUPP Load column ("without Adjustments"):

| Summer Period without Adjustments (rows 3628-6555): Total kWhs |           | Nonsummer Period without Adjustments: Total kWhs |           |
| -------------------------------------------------------------- | --------- | ------------------------------------------------ | --------- |
| Morn                                                           | 1,605,949 | Morn                                             | 2,757,222 |
| Mid-Day                                                        | 2,012,553 | Mid-Day                                          | 2,554,445 |
| Eve                                                            | 734,676   | Eve                                              | 1,023,637 |
| Overnight                                                      | 2,869,278 | Overnight                                        | 4,707,327 |

"Check Totals: –" (printed "-", i.e. zero difference between the 18,265,086 total and the sum of the eight subtotals). Below: the "Hour Ending / Category" key (Hour01–Hour06 Overnight; Hour07–Hour13 Morn; Hour14–Hour19 Mid-Day; Hour20–Hour21 Eve; Hour22–Hour24 Overnight).

- **Footnotes on these pages**: none.
- **Source anomalies in the hourly table (reproduced as printed, flagged in the CSV `source_flag` column)**:
  1. `3/12/2023 Hour24` (p. 26): RTOUPP Load is printed as "-" (blank/zero in Excel accounting format); no kWh value is shown. The CSV leaves `rtoupp_load` empty for this row (raw string `-`). The printed 18,265,086 total and the nonsummer Overnight subtotal reconcile with this row excluded (equivalently zero). 3/12/2023 is the 2023 U.S. spring-forward date (that fact is agent knowledge, not stated in the workpaper).
  2. `3/31/2023 Hour24` (p. 32): `Interval` is printed as **23** while the Data label is Hour24 (all other rows have Interval = hour number). RTOUPP Load 1,890.01 as printed. The CSV keeps `interval = 23` as printed.
- **Summer-row note**: "Summer Period without Adjustments (rows 3628-6555)" = worksheet rows 3628–6555 = 2,928 rows = 122 days (1 June – 30 September) × 24 hours; the agent parse puts the first/last `S` rows at worksheet rows 3628 and 6555 (data starting at row 4).

### Sample (first 24 rows, 1/1/2023; as printed)

| Date     | Data   | Category  | Month | Summer or Nonsummer | Interval | RTOUPP Load |
| -------- | ------ | --------- | ----- | ------------------- | -------- | ----------- |
| 1/1/2023 | Hour01 | Overnight | 1     | N                   | 1        | 2,241.34    |
| 1/1/2023 | Hour02 | Overnight | 1     | N                   | 2        | 2,106.00    |
| 1/1/2023 | Hour03 | Overnight | 1     | N                   | 3        | 1,983.12    |
| 1/1/2023 | Hour04 | Overnight | 1     | N                   | 4        | 1,883.34    |
| 1/1/2023 | Hour05 | Overnight | 1     | N                   | 5        | 1,841.13    |
| 1/1/2023 | Hour06 | Overnight | 1     | N                   | 6        | 1,703.49    |
| 1/1/2023 | Hour07 | Morn      | 1     | N                   | 7        | 1,645.70    |
| 1/1/2023 | Hour08 | Morn      | 1     | N                   | 8        | 1,614.79    |
| 1/1/2023 | Hour09 | Morn      | 1     | N                   | 9        | 1,618.82    |
| 1/1/2023 | Hour10 | Morn      | 1     | N                   | 10       | 1,692.21    |
| 1/1/2023 | Hour11 | Morn      | 1     | N                   | 11       | 1,758.21    |
| 1/1/2023 | Hour12 | Morn      | 1     | N                   | 12       | 1,813.27    |
| 1/1/2023 | Hour13 | Morn      | 1     | N                   | 13       | 1,882.14    |
| 1/1/2023 | Hour14 | Mid-Day   | 1     | N                   | 14       | 1,826.51    |
| 1/1/2023 | Hour15 | Mid-Day   | 1     | N                   | 15       | 1,795.58    |
| 1/1/2023 | Hour16 | Mid-Day   | 1     | N                   | 16       | 1,861.19    |
| 1/1/2023 | Hour17 | Mid-Day   | 1     | N                   | 17       | 2,050.85    |
| 1/1/2023 | Hour18 | Mid-Day   | 1     | N                   | 18       | 2,237.30    |
| 1/1/2023 | Hour19 | Mid-Day   | 1     | N                   | 19       | 2,228.77    |
| 1/1/2023 | Hour20 | Eve       | 1     | N                   | 20       | 2,175.30    |
| 1/1/2023 | Hour21 | Eve       | 1     | N                   | 21       | 2,151.01    |
| 1/1/2023 | Hour22 | Overnight | 1     | N                   | 22       | 2,090.08    |
| 1/1/2023 | Hour23 | Overnight | 1     | N                   | 23       | 2,371.85    |
| 1/1/2023 | Hour24 | Overnight | 1     | N                   | 24       | 2,266.30    |

**Full table**: all 8,760 rows are in [`../workbooks/icc_639690_ex_19_02_rtoupp_hourly_profile.csv`](../workbooks/icc_639690_ex_19_02_rtoupp_hourly_profile.csv). Columns: `date` (ISO yyyy-mm-dd; printed as m/d/yyyy in the source), `data` (Hour01…Hour24 as printed), `category` (as printed), `month`, `summer_or_nonsummer` (`S`/`N`), `interval` (as printed), `rtoupp_load` (kWh per hour, aggregate of 1,858 participants; empty for the one row printed "-"), `source_flag` (empty except for the two anomaly rows above). These are exactly the seven printed columns plus `source_flag`. Page of origin: PDF page = 4 for the first 70 rows, then 5 + floor((row index − 70) / 76) for later rows (row index 0-based).

### Validation of the parse (agent-computed; not source text)

| Check                   | Result                                                                                                                                                                                                                                                            |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Row count               | 8,760 (= 70 + 114 × 76 + 26); every PDF page 4–119 parsed with no unparseable rows                                                                                                                                                                                |
| Date continuity         | 365 distinct dates, 1/1/2023–12/31/2023, no gaps or repeats, 24 rows per date, Data labels cycle Hour01…Hour24 in order                                                                                                                                           |
| Month column            | equals the month of the date on every row                                                                                                                                                                                                                         |
| S/N flag                | `S` exactly for June–September (2,928 rows; 7,222,455 kWh), `N` otherwise (5,832 rows; 11,042,631 kWh)                                                                                                                                                            |
| Category vs hour        | matches the hour-ending key on every row                                                                                                                                                                                                                          |
| Sum of RTOUPP Load      | 18,265,086.22 kWh = stated "Total kWhs 18,265,086" (rounded) — **matches**                                                                                                                                                                                        |
| Period subtotals (8)    | all eight agree with the printed p. 4 subtotals to within rounding (max absolute difference 0.51 kWh; e.g. Summer Mid-Day computed 2,012,552.49 vs printed 2,012,553, consistent with the printed 2-decimal row values being rounded from unrounded sheet values) |
| "Check Totals"          | agrees (difference ≈ 0)                                                                                                                                                                                                                                           |
| Rows excluded from sums | 1 (`3/12/2023 Hour24`, load printed "-")                                                                                                                                                                                                                          |
| Overall                 | **Validated** (row count, date continuity, total, and all eight period subtotals reconcile). Two printed-source anomalies are documented above; neither affects the totals.                                                                                       |

---

## Sheet 120 (PDF p. 120 of 121): Hourly profile with PJM prices, losses and revenue (first 102 hours) and summary tables

Red label at top left: "**This Workpaper is set to print Page 1 only**"; italic "Illustrative Example"; "Total kWhs 18,265,086". This page prints the first 102 rows (1/1/2023 Hour01 through 1/5/2023 Hour06) of the same worksheet with extra calculation columns that exist in the workbook for all rows but are printed only here.

**Column headings (left block)**: `Date` | `Data` | `Category` | `Month` | `Summer or Nonsummer` | `Interval` | `RTOUPP Load` | `PJM Price` | `Weighted Residential Distribution Loss Factor to Add` | `Adjusted Hourly Supply Price` | `Total Estimated Revenue`.

<!-- EPON: profile,midday-peak — shows how the base energy charge is built: hourly PJM (ComEd Zone) price x (1 + weighted residential DLF 0.0522) x hourly participant load; summed within each TOU period and divided by that period's kWh gives the ARBREV price (e.g. Mid-Day summer 4.702 ¢/kWh before capacity adder) -->

First rows as printed (units: `PJM Price` is the hourly PJM real-time residual LMP value as shown, in \$/MWh per the tariff definition of HLMP; `Adjusted Hourly Supply Price` in \$/kWh; `Total Estimated Revenue` in whole dollars shown with a "\$" sign):

| Date     | Data   | Category  | Month | S/N | Interval | RTOUPP Load | PJM Price | Weighted Residential Distribution Loss Factor to Add | Adjusted Hourly Supply Price | Total Estimated Revenue |
| -------- | ------ | --------- | ----- | --- | -------- | ----------- | --------- | ---------------------------------------------------- | ---------------------------- | ----------------------- |
| 1/1/2023 | Hour01 | Overnight | 1     | N   | 1        | 2,241.34    | 15.54     | 0.05220                                              | 0.016348                     | \$ 37                   |
| 1/1/2023 | Hour02 | Overnight | 1     | N   | 2        | 2,106.00    | 14.33     | 0.05220                                              | 0.015077                     | \$ 32                   |
| 1/1/2023 | Hour03 | Overnight | 1     | N   | 3        | 1,983.12    | 13.53     | 0.05220                                              | 0.014231                     | \$ 28                   |
| 1/1/2023 | Hour04 | Overnight | 1     | N   | 4        | 1,883.34    | 13.86     | 0.05220                                              | 0.014584                     | \$ 27                   |
| 1/1/2023 | Hour05 | Overnight | 1     | N   | 5        | 1,841.13    | 15.29     | 0.05220                                              | 0.016089                     | \$ 30                   |
| 1/1/2023 | Hour06 | Overnight | 1     | N   | 6        | 1,703.49    | 15.60     | 0.05220                                              | 0.016412                     | \$ 28                   |
| 1/1/2023 | Hour07 | Morn      | 1     | N   | 7        | 1,645.70    | 17.68     | 0.05220                                              | 0.0186                       | \$ 31                   |
| 1/1/2023 | Hour08 | Morn      | 1     | N   | 8        | 1,614.79    | 20.39     | 0.05220                                              | 0.02145                      | \$ 35                   |

All 102 printed rows are in [`../workbooks/icc_639690_ex_19_02_p120_first_102_hours_with_pjm_prices.csv`](../workbooks/icc_639690_ex_19_02_p120_first_102_hours_with_pjm_prices.csv). Agent checks on those rows: RTOUPP Load and labels equal the corresponding rows of the full profile; Total Estimated Revenue = RTOUPP Load × Adjusted Hourly Supply Price (rounded to whole \$) on all 102 rows; Adjusted Hourly Supply Price ≈ PJM Price × (1 + 0.0522) / 1,000 (max difference 6 × 10⁻⁶ \$/kWh, consistent with rounding of the displayed PJM prices). PJM Price units are not labelled on the page.

**Right-hand tables:**

Summer Period without Adjustments (rows 3628-6555):

| Period    | Total \$  | Total kWhs | Average Rate in Period (c/kWh) |
| --------- | --------- | ---------- | ------------------------------ |
| Morn      | \$ 47,528 | 1,605,949  | 2.959                          |
| Mid-Day   | \$ 94,633 | 2,012,553  | 4.702                          |
| Eve       | \$ 22,297 | 734,676    | 3.035                          |
| Overnight | \$ 52,670 | 2,869,278  | 1.836                          |

Nonsummer Period without Adjustments:

| Period    | Total \$  | Total kWhs | Average Rate in Period (c/kWh) |
| --------- | --------- | ---------- | ------------------------------ |
| Morn      | \$ 76,603 | 2,757,222  | 2.778                          |
| Mid-Day   | \$ 84,866 | 2,554,445  | 3.322                          |
| Eve       | \$ 31,030 | 1,023,637  | 3.031                          |
| Overnight | \$ 93,023 | 4,707,327  | 1.976                          |

<!-- EPON: stacking,midday-peak — the workpaper reproduces the DTOU (delivery) TOU periods alongside the supply periods: same Mid-Day Peak 1 pm–7 pm (HE 14–19) window for delivery and supply -->

Delivery Service Time of Use (DTOU) Periods:

| Period       | Hours        | Hour Ending |
| ------------ | ------------ | ----------- |
| Morning      | 6 am to 1 pm | 7-13        |
| Mid-Day Peak | 1 pm to 7 pm | 14-19       |
| Evening      | 7 pm to 9 pm | 20-21       |
| Overnight    | 9 pm to 6 am | 1-6, 22-24  |

"Hour Ending / Category" key (Hour01–Hour06 Overnight; Hour07–Hour13 Morn; Hour14–Hour19 Mid-Day; Hour20–Hour21 Eve; Hour22–Hour24 Overnight) is printed to the right, as on p. 4.

---

## Sheet 121 (PDF p. 121 of 121): Participant kWh by customer group and distribution loss factors

Italic label "Illustrative Example". Green input cell: "Start Date **1/1/2023**".

<!-- EPON: profile,ev-hp — customer-group/subgroup definition for the illustrative profile: only ~6.9% of participant kWh (agent-computed) is from customers WITH electric space heat; the loss factor used in Formula 1 is a participant-kWh-weighted average of these four groups -->

| Customer group                                                                               | Participant kWhs (from monthly billing data) (2) | Loss Factors (1) |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------ | ---------------- |
| Single Family Without Electric Space Heat                                                    | 1,110,619                                        | 0.0517           |
| Multi Family Without Electric Space Heat                                                     | 127,143                                          | 0.0532           |
| Single Family With Electric Space Heat                                                       | 28,533                                           | 0.0554           |
| Multi Family Without Electric Space Heat [sic; duplicate label — presumably intended "With"] | 62,984                                           | 0.0567           |
| **Weighted Residential Loss Factor**                                                         |                                                  | **0.0522**       |

**Notes:**

1. Distribution Loss Factors as listed in Informational Sheet No. 33.
2. Historial [sic] Rate RTOUPP billing usage for the billing month March 2023.

Agent check: kWh-weighted average of the four printed loss factors = 0.05216 → 0.0522 (matches the printed weighted factor; the four kWh values sum to 1,329,279).

---

## Derived statistics from the hourly profile (agent-computed from the CSV; NOT source text)

All figures below are computed by code from the 8,760-row table in the CSV (one `RTOUPP Load` value per hour; the load of the whole 1,858-account group, kWh per hour = average kW over that hour). `3/12/2023 Hour24` (printed "-") is excluded from sums and means. "HE" = hour ending as labelled in the `Data` column. Seasons: Summer = June–September (122 days), Nonsummer = the other 243 days.

### 1. Annual kWh by Time-of-Use period and season

| Period                      | Hours/yr | Summer kWh | Nonsummer kWh | Annual kWh | % of annual kWh | % of annual hours |
| --------------------------- | -------- | ---------- | ------------- | ---------- | --------------- | ----------------- |
| Morning (HE 07–13)          | 2,555    | 1,605,949  | 2,757,222     | 4,363,172  | 23.89%          | 29.17%            |
| Mid-Day Peak (HE 14–19)     | 2,190    | 2,012,552  | 2,554,445     | 4,566,998  | 25.00%          | 25.00%            |
| Evening (HE 20–21)          | 730      | 734,676    | 1,023,637     | 1,758,313  | 9.63%           | 8.33%             |
| Overnight (HE 22–24, 01–06) | 3,285    | 2,869,278  | 4,707,327     | 7,576,604  | 41.48%          | 37.50%            |
| **Total**                   | 8,760    | 7,222,455  | 11,042,631    | 18,265,086 | 100.00%         | 100.00%           |

(The Summer Mid-Day total computes to 2,012,552.49 kWh; the source prints 2,012,553.)

### 2. Share and mean hourly load by period within each season

Mean kWh per hour = mean aggregate load for the 1,858 participants over the hours in that period/season.

| Period                      | Summer: % of summer kWh | Summer: mean kWh per hour | Nonsummer: % of nonsummer kWh | Nonsummer: mean kWh per hour |
| --------------------------- | ----------------------- | ------------------------- | ----------------------------- | ---------------------------- |
| Morning (HE 07–13)          | 22.24%                  | 1,880.5                   | 24.97%                        | 1,620.9                      |
| Mid-Day Peak (HE 14–19)     | 27.87%                  | 2,749.4                   | 23.13%                        | 1,752.0                      |
| Evening (HE 20–21)          | 10.17%                  | 3,011.0                   | 9.27%                         | 2,106.2                      |
| Overnight (HE 22–24, 01–06) | 39.73%                  | 2,613.2                   | 42.63%                        | 2,153.4                      |

### 3. Mean hourly load by hour of day (hour ending), summer vs nonsummer

Mean RTOUPP Load (kWh per hour, 1,858-participant aggregate) across all days in the season for each hour-ending label. The Nonsummer Hour24 mean uses 242 days because `3/12/2023 Hour24` has no printed value.

| Hour ending (Data label) | Category  | Summer mean kWh/h (122 days) | Nonsummer mean kWh/h (243 days; 242 for Hour24) |
| ------------------------ | --------- | ---------------------------- | ----------------------------------------------- |
| Hour01                   | Overnight | 2,973.4                      | 2,379.4                                         |
| Hour02                   | Overnight | 2,583.6                      | 2,167.2                                         |
| Hour03                   | Overnight | 2,319.8                      | 2,026.4                                         |
| Hour04                   | Overnight | 2,136.9                      | 1,948.6                                         |
| Hour05                   | Overnight | 2,009.6                      | 1,915.3                                         |
| Hour06                   | Overnight | 1,779.6                      | 1,764.2                                         |
| Hour07                   | Morn      | 1,526.2                      | 1,643.1                                         |
| Hour08                   | Morn      | 1,594.3                      | 1,672.9                                         |
| Hour09                   | Morn      | 1,694.2                      | 1,628.8                                         |
| Hour10                   | Morn      | 1,826.5                      | 1,609.8                                         |
| Hour11                   | Morn      | 1,984.0                      | 1,597.4                                         |
| Hour12                   | Morn      | 2,167.0                      | 1,591.8                                         |
| Hour13                   | Morn      | 2,371.2                      | 1,602.8                                         |
| Hour14                   | Mid-Day   | 2,547.6                      | 1,595.2                                         |
| Hour15                   | Mid-Day   | 2,535.6                      | 1,581.8                                         |
| Hour16                   | Mid-Day   | 2,685.2                      | 1,628.4                                         |
| Hour17                   | Mid-Day   | 2,830.8                      | 1,759.9                                         |
| Hour18                   | Mid-Day   | 2,948.3                      | 1,929.2                                         |
| Hour19                   | Mid-Day   | 2,948.8                      | 2,017.6                                         |
| Hour20                   | Eve       | 3,024.4                      | 2,087.3                                         |
| Hour21                   | Eve       | 2,997.5                      | 2,125.2                                         |
| Hour22                   | Overnight | 3,017.1                      | 2,105.0                                         |
| Hour23                   | Overnight | 3,437.3                      | 2,556.4                                         |
| Hour24                   | Overnight | 3,261.4                      | 2,519.6                                         |

### 4. Peak, minimum and load factor

- **Peak hour (whole year)**: 6,480.95 kWh on 8/23/2023, Hour23 (Overnight category, summer). Next highest: 6,286.06 kWh on 8/24/2023 Hour18 (Mid-Day); 6,220.44 kWh on 8/24/2023 Hour23.
- **Highest Mid-Day-category hour**: 6,286.06 kWh on 8/24/2023 Hour18.
- **Nonsummer peak hour**: 3,666.33 kWh on 5/30/2023 Hour23 (Overnight category). Note 5/30/2023 is in a `N` month (May).
- **Minimum hour**: 1,107.21 kWh on 5/29/2023 Hour07.
- **Mean hourly load**: 18,265,086.22 / 8,760 = 2,085.06 kWh per hour (2,085.29 using the 8,759 populated hours).
- **Load factor** (mean ÷ peak hour): 2,085.06 / 6,480.95 = **0.322** (0.322 with either denominator).
- **Per-participant equivalents** (÷ 1,858 accounts): 9,830.5 kWh per year; 1.12 kW average; 3.49 kW in the peak hour.
- **Monthly kWh** (rounded): Jan 1,565,338; Feb 1,362,938; Mar 1,394,667 (excl. the blank hour); Apr 1,220,146; May 1,281,159; Jun 1,645,763; Jul 2,085,582; Aug 2,011,587; Sep 1,479,523; Oct 1,320,323; Nov 1,348,207; Dec 1,549,855.
- **Mid-Day Peak share of annual kWh**: 4,566,998 / 18,265,086 = **25.00%**, equal to its share of hours (2,190 / 8,760 = 25.00%). Summer: 27.87% of summer kWh; nonsummer: 23.13% of nonsummer kWh.

### 5. Cross-checks of the summary sheets (agent-computed)

- Sheet 2: f(Mid-Day) = 602,456 / (2,012,553 + 2,554,445) = 0.131915 → matches the printed 0.13192 \$/kWh capacity adder; e(s) = 94,633 / 2,012,553 = 0.04702 and e(n) = 84,866 / 2,554,445 = 0.03322 match.
- Sheet 1: 17.894 × 1.0128 × 1.0053 = 18.219 (summer Mid-Day BESTEC); 16.514 × 1.0128 × 1.0053 = 16.814 (nonsummer). Mid-Day BESTEC excluding the capacity adder would be 4.702 × 1.0128 × 1.0053 = 4.787 ¢/kWh summer and 3.322 × 1.0128 × 1.0053 = 3.382 ≈ 3.383 ¢/kWh nonsummer, i.e. the values on the strawman informational sheet ComEd Ex. 17.02 (MDPPEC 4.787 / 3.383). The Morning, Evening and Overnight BESTEC values on Sheet 1 equal the Ex. 17.02 values. The compromise therefore adds about 13.43 ¢/kWh to the Mid-Day Peak BESTEC in both seasons (18.219 − 4.787 = 13.432 summer; 16.814 − 3.383 = 13.431 nonsummer).
- Sheet 3: 4,899.33 × 1.1156 × 1.1170 = 6,105.2 kW (printed 6,105.29 using unrounded factors); 6,105.2916 kW = 6.1053 MW × 270.35 \$/MW-day × 365 = \$602,456.
- Peak-hour load context: the printed "Total PLCs" for the 1,858 accounts (January 2024 PLCs) is 4,899.33 kW, whereas the single highest-load hour in the 2023 profile is 6,480.95 kWh (6.48 MW-average over the hour for the group). These are different measures (PLC is PJM-coincident-peak based) and are shown only so both magnitudes are on one page.
