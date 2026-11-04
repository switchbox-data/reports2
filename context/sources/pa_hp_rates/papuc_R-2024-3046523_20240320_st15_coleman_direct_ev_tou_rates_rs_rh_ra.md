---
source_file: papuc_R-2024-3046523_20240320_dlc_st15_coleman_direct_ev_tou_rates_rs_rh_ra.pdf
citekey: coleman_DocketR20243046523Direct_2024
zotero_item: "DFCX3WIH"
public_url: https://drive.google.com/file/d/1Uc9HKUB_xFtd63ZWfQcBy0GrrKo4KiPG/view
short_url: https://pub.switch.box/coleman_DocketR20243046523Direct_2024
docket: R-2024-3046523
utility: Duquesne Light
rate: Rate RA / RH
filing_date: 2024-03-20
filer: David Coleman (Duquesne Light)
document_type: testimony
pages_total: 26
extraction_scope: full
source_url: https://www.puc.pa.gov/pcdocs/1823419.pdf  # from our download manifest, not text from the PDF
md5: "8c2a2bca72ad853a5c99246a378d4ccd"
validated: 2026-10-29
why_here: Shows the proposed pre-settlement RA winter and summer rates beside RH and RS, and how a TOU layer would sit on the seasonal RA structure. Its rates were updated in rebuttal (Statement 15-R, in the combined exhibit file); it does not discuss heat pumps or how RA customers are identified.
context: Duquesne Light's direct testimony in its March 2024 rate filing on the EV time-of-use distribution rate pilot (Rider No. 4), companion to Ogden's Statement No. 14 on base rates.
contents: Design and calculation of the EV TOU distribution rates for RS, RH and RA. Table 1 (p. 6) lists the proposed non-TOU volumetric rates (RA winter 3.5598 c/kWh against RH 7.5466 and RS 8.4662; summer 8.4662 for all three); Tables 2-4 derive the whole-home and EV-only TOU rates for each class.
---

# Before the Pennsylvania Public Utility Commission — Docket No. R-2024-3046523 — Duquesne Light Company Statement No. 15 — Direct Testimony of David Coleman

**Source**: papuc_R-2024-3046523_20240320_dlc_st15_coleman_direct_ev_tou_rates_rs_rh_ra.pdf
**Pages**: 26 PDF pages (cover, 2 front-matter pages numbered i–ii, 23 numbered body pages)
**Date**: March 20, 2024
**Author(s)**: David C. Coleman, The NorthBridge Group, Inc., on behalf of Duquesne Light Company
**Subjects (as printed on cover)**: Electric Vehicle Time of Use Distribution Rate Pilot

_Extractor note (not source text): Text is transcribed verbatim; no typographical corrections were made. Questions ("Q.") are bold in the source and are bold here; answers ("A.") are roman. Page markers give the 1-based physical PDF page and, where it differs, the document's own printed page number. The testimony does not define RS, RH or RA beyond calling them "RS, RH, and RA classes" of residential customers (we know from the docket assignment that RH and RA are the electric-heating and add-on heat pump rates, but that is not stated here), and it does not mention heat pumps. Its subject is the EV pilot; the RS/RH/RA rate comparison appears in Table 1 (PDF p. 9) and in the EV rate tables (Tables 2–4)._

---

<!-- PDF page 1 (cover; no printed page number) -->

BEFORE THE
PENNSYLVANIA PUBLIC UTILITY COMMISSION

Docket No. R-2024-3046523

Duquesne Light Company
Statement No. 15

Direct Testimony of David Coleman

Subjects: Electric Vehicle Time of Use Distribution Rate Pilot

Date: March 20, 2024

---

<!-- PDF page 2 (printed page i) -->

## Table of Contents

|       | Section                                                                                                                                                                                                                                   | Page |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| I.    | Introduction                                                                                                                                                                                                                              | 1    |
| II.   | EV TOU Distribution Rate Pilot Program Overview                                                                                                                                                                                           | 4    |
| III.  | Calculation of Distribution EV-TOU Rates                                                                                                                                                                                                  | 7    |
| IV.   | EV TOU Distribution Rate Is Designed to Achieve Goal #1: Save Money for Customers Who Charge Their EVs During Hours When the Distribution System Is Less Utilized                                                                         | 10   |
| V.    | EV TOU Distribution Rate Is Designed to Achieve Goal #2: Provide Incentives for EV Customers to Utilize the Distribution System More Efficiently by Charging During Off-Peak Hours and Avoid Adding Incremental Load During On-Peak Hours | 12   |
| VI.   | EV TOU Distribution Rate Is Designed to Achieve Goal #3: Ensure that Incremental Load from EV Charging does not Change the Allocation of Costs to Customers by Creating a Higher Non-Coincident Peak                                      | 15   |
| VII.  | Alternative Distribution Ratemaking Mechanisms and Rate Design Considerations                                                                                                                                                             | 18   |
| VIII. | Conclusion                                                                                                                                                                                                                                | 23   |

<!-- PDF page 3 (printed page ii) -->

## List of Tables

| Table                                                                              | Page |
| ---------------------------------------------------------------------------------- | ---- |
| Table 1: Proposed Non-TOU Volumetric Rates for RS, RH, and RA Classes              | 6    |
| Table 2: Proposed EV Distribution TOU Rates                                        | 7    |
| Table 3: Calculation of Off-Peak WholeHome TOU Distribution Rate                   | 9    |
| Table 4: Calculation of Off-Peak EV-Only TOU Distribution Rate                     | 10   |
| Table 5: Historical Hours of Residential (Non-Lighting) Non-Coincident Peak Demand | 12   |

## List of Figures

| Figure                                                                                      | Page |
| ------------------------------------------------------------------------------------------- | ---- |
| Figure 1: Generation EV-TOU Pilot Program EV Charging is Concentrated During Off-Peak Hours | 14   |
| Figure 2: Estimated Impact of EV Adoption on Residential NCP                                | 16   |

---

<!-- PDF page 4 (printed page 1) -->

## I. Introduction

**Q.** **Please state your name and business address.**

A. My name is David C. Coleman. My business address is 30 Monument Square, Suite 105, Concord, Massachusetts, 01742.

**Q.** **What is your current position?**

A. I am a Partner with The NorthBridge Group, Inc. (“NorthBridge”), an economic and strategic consulting firm serving the electric and natural gas industries.

**Q.** **On whose behalf are you submitting testimony?**

A. I am submitting testimony on behalf of Duquesne Light Company (“Duquesne Light” or the “Company”).

**Q.** **Please summarize your professional and academic background.**

A. I have over 20 years of experience as a consultant to the electric and natural gas industries. I advise Fortune 500 and smaller energy companies on matters related to energy and capacity price forecasting, market design, commodity risk exposure, business and regulatory strategy, asset valuation, portfolio management, electricity supply procurement, and product pricing. My expertise involves developing and implementing the analytical tools necessary to analyze challenging strategic questions. These tools have included Monte Carlo simulations of spot and forward commodity prices, modeling loss-of-load

<!-- PDF page 5 (printed page 2) -->

probability (LOLP) and system reliability, estimating Effective Load Carrying Capacity (ELCC) for intermittent resources, developing generation portfolio commitment and dispatch models, and optimizing battery energy storage solutions (BESS). I have also served as an expert witness in both regulatory and civil litigation proceedings. I graduated cum laude from Dartmouth College with an A.B. in physics and received my M.B.A. from the Tuck School at Dartmouth where I was a Tuck Scholar and where I have served as a guest lecturer in both Managerial Economics and Energy Economics.

**Q.** **Have you testified previously before the Pennsylvania Public Utility Commission (“Commission”)?**

A. No.

**Q.** **What is the purpose of your direct testimony?**

A. The purpose of my testimony is to support Duquesne Light’s proposed rate structure and rate design for the EV Time-of-Use Distribution Rate Pilot (“EV TOU Distribution Rate Pilot”). I calculate the WholeHome and EV-Only TOU Distribution Rates, collectively the “EV TOU Distribution Rates”. These rates are contained in Rider No. 4 (Electric Vehicle Time of Use Distribution Rate Pilot). I will also address the rate structure and rate design goals for the EV TOU Distribution Rate Pilot and how its rates are designed to achieve these goals.

<!-- PDF page 6 (printed page 3) -->

**Q.** **Are you sponsoring any exhibits, parts of exhibits, or responses to the Commission’s filing requirements as part of your direct testimony?**

A. Yes. I am responding to the Commission’s filing requirements identified in 52 PA. code §§ 69.3301 and 69.3302.

**Q.** **What are the rate structure and rate design goals of the EV TOU Distribution Rate Pilot?**

A. The EV TOU Distribution Rate Pilot has three main rate structure and rate design goals.

- The first goal is to provide savings versus the non-time-of-use rate to customers who charge electric vehicles (“EVs”) during hours when the distribution system is less utilized (e.g., off-peak hours).
- The second goal is to provide incentives for EV customers to utilize the system more efficiently by charging them during off-peak hours, when the distribution system is less utilized, and to avoid charging them during on-peak hours when incremental EV load could create incremental system costs.
- The third goal is to ensure that, at the scale of this pilot, incremental load from EV charging does not change the allocation of distribution costs to customers by increasing the residential non-coincident peak demand materially.

<!-- PDF page 7 (printed page 4) -->

**Q.** **Please summarize your conclusions.**

A. EV TOU Distribution Rates are appropriately designed to achieve these goals.

- The first goal is achieved by the rate design of EV TOU Distribution Rates, which results in lower bills for EV customers with typical consumption than they would otherwise see if all of their consumption were billed at non-TOU rates.
- The second goal is achieved by establishing a differential in volumetric rates between on-peak and off-peak hours. EV TOU Distribution Rate establishes a lower off-peak volumetric rate than both the EV TOU Distribution Rates’ on-peak volumetric rates and the standard RS, RH, and RA non-time-of-use volumetric rates. This differential should both encourage charging during off-peak hours and discourage charging during on-peak hours.
- The third goal is achieved because incremental EV charging load is not expected to increase load materially during the hours when the residential non-coincident peak currently takes place. Incremental EV load during other hours is not expected to be substantial enough at the scale of this pilot to create a new and higher non-coincident peak.

## II. EV TOU Distribution Rate Pilot Program Overview

**Q.** **Which customers will be eligible for EV TOU Distribution Rates?**

A. As explained by Duquesne Light witness Sarah J. Olexsak (Duquesne Light Statement No. 6), the EV Distribution Rate Pilot will be offered to residential customers in the RS, RH,

<!-- PDF page 8 (printed page 5) -->

and RA classes who own or lease a plug-in battery electric vehicle or a plug-in hybrid electric vehicle.

**Q.** **What is the proposed non-TOU distribution service rate structure for RS customers?**

A. As explained by Duquesne Light witness David B. Ogden (Duquesne Light Statement No. 14), Duquesne Light proposes that RS customers be billed via a two-part rate. The first part is a fixed monthly customer charge. This fixed charge is the same for all RS customers, regardless of usage. The second part is a proposed volumetric rate of 8.4662 cents/kWh, which is also the same for all RS customers, and applies to the total volume of electricity consumed during a billing period. Both the customer and volumetric charges are independent of when a customer consumes electricity. The only variable in the calculation of the monthly billed amount is the total kWh used (to which the volumetric charge is applied).

**Q.** **What is the proposed non-TOU distribution service rate structure for RH and RA customers?**

A. As explained by Duquesne Light witness David B. Ogden (Duquesne Light Statement No. 14), the proposed distribution rate structures for RH and RA rates mirror that of the RS rate in that each also has a proposed fixed monthly customer charge. Unlike the RS rate, however, RH and RA rates have volumetric rates that differ by season. The proposed volumetric rate for RH customers is 7.5466 cents/kWh during the winter (November – April) and 8.4662 cents/kWh during the summer (May – October). The proposed

<!-- PDF page 9 (printed page 6) -->

volumetric rate for RA customers is 3.5598 cents/kWh during the winter (November – April) and 8.4662 cents/kWh during the summer (May – October). These rates are summarized in Table 1 below.

**Table 1: Proposed Non-TOU Volumetric Rates for RS, RH, and RA Classes**

| Season \ Rate Class | Units | RS     | RH     | RA     |
| ------------------- | ----- | ------ | ------ | ------ |
| All Months          | c/kWh | 8.4662 |        |        |
| Winter Months       | c/kWh |        | 7.5466 | 3.5598 |
| Summer Months       | c/kWh |        | 8.4662 | 8.4662 |

_Extractor note (not source text): Blank cells are blank in the source (RS has a single all-months rate; RH and RA have winter and summer rates only)._

**Q.** **What is the proposed rate structure for customers who enroll in EV Distribution Rate Pilot?**

A. Duquesne Light proposes that rates under the EV Distribution Rate Pilot program will be composed of i) a monthly fixed customer charge, which would be independent of usage, ii) an on-peak volumetric rate, and iii) an off-peak volumetric rate. For RH and RA customers, those volumetric rates would differ by season (i.e., winter and summer). Further, Duquesne Light proposes two variations of this rate structure: one for customers whose entire household load is metered using a single meter (“WholeHome”) where household and EV load is not differentiated, and a second for customers whose EV load is metered separately via vehicle telematics or charging station energy consumption data (“EV-Only”). In the case of the EV-Only TOU Distribution Rate, a customer’s existing household non-EV load would continue being billed at non-time-of-use rates. The volumetric rates proposed are summarized below in Table 2.

<!-- PDF page 10 (printed page 7) -->

**Table 2: Proposed EV Distribution TOU Rates**

_Extractor note (not source text): Rates are in c/kWh (the table prints no units; the units are c/kWh per Table 1 and the surrounding text). The "Proposed Non-TOU Rate" cell is a single merged cell spanning each class/season's on-peak and off-peak rows in the source, shown here in the on-peak row; the off-peak row of that column is blank in the source._

| Class | Months     | Period   | Proposed Non-TOU Rate | Proposed WholeHome TOU Rate | Proposed EV-Only TOU Rate |
| ----- | ---------- | -------- | --------------------- | --------------------------- | ------------------------- |
| RS    | All Months | On-Peak  | 8.4662                | 8.4662                      | 8.4662                    |
| RS    | All Months | Off-Peak |                       | 6.7827                      | 4.0924                    |
| RH    | Winter     | On-Peak  | 7.5466                | 7.5466                      | 7.5466                    |
| RH    | Winter     | Off-Peak |                       | 6.5694                      | 3.6480                    |
| RH    | Summer     | On-Peak  | 8.4662                | 8.4662                      | 8.4662                    |
| RH    | Summer     | Off-Peak |                       | 6.7596                      | 4.0923                    |
| RA    | Winter     | On-Peak  | 3.5598                | 3.5598                      | 3.5598                    |
| RA    | Winter     | Off-Peak |                       | 3.0435                      | 1.7208                    |
| RA    | Summer     | On-Peak  | 8.4662                | 8.4662                      | 8.4662                    |
| RA    | Summer     | Off-Peak |                       | 7.0869                      | 4.0923                    |

**Q.** **How will the EV TOU Distribution Rate on-peak and off-peak hours be defined?**

A. On-peak hours are defined as the period extending from 3:00 pm to 9:00 pm during non-holiday weekdays. The off-peak period will be defined as all other hours. Holidays follow the PJM definition and include New Year's Day, Memorial Day, Independence Day, Labor Day, Thanksgiving Day, and Christmas Day.

## III. Calculation of Distribution EV-TOU Rates

**Q.** **How are the proposed EV-TOU Distribution Rates the same as non-time-of-use rates?**

A. The proposed RS, RH, and RA TOU distribution rates will continue to include a fixed monthly charge in the same amount as the non-TOU rates. Similarly, load consumed during on-peak hours will be billed at the same volumetric rates as non-TOU volumetric rates.

<!-- PDF page 11 (printed page 8) -->

**Q.** **How are the proposed EV-TOU Distribution Rates different from non-time-of-use rates?**

A. The only structural difference between EV-TOU Distribution Rates and non-time-of-use distribution rates is that the EV-TOU Distribution Rates will have a different, and lower, volumetric rate applied to off-peak consumption.

**Q.** **How are the off-peak WholeHome TOU Distribution Rates Calculated?**

A. To calculate the off-peak WholeHome TOU Distribution Rates, I

i) Estimate the revenue collected from a typical customer prior to including EV charging load and using proposed non-TOU rates,

ii) Estimate the revenue that would have been collected from this customer after including incremental EV charging load, but still billed using proposed non-TOU rates,

iii) Calculate the incremental revenue between step (i) and (ii),

iv) Calculate a discount to the off-peak TOU rate that reduces revenue, after including EV charging load, by an amount equal to 50% of the incremental revenue (“shared revenue”) calculated in step (iii).

These calculations are illustrated in Table 3 below.

<!-- PDF page 12 (printed page 9) -->

**Table 3: Calculation of Off-Peak WholeHome TOU Distribution Rate**

_Extractor note (not source text): The source table is an embedded spreadsheet image in three blocks (Steps i, ii, and iii–iv). Row letters A–I and the formulas in the right-hand margin ("= B - A", etc.) are printed in the source. Values were read from the rendered page and checked against the PDF text layer. Column headers are "RS", "RH/Winter", "RH/Summer", "RA/Winter" (printed "RA/WInter") and "RA/Summer"._

**Step i) Volumetric Charge for Typical Customer Without EV Under Proposed Non-TOU Rates**

| Row | Rate Class / Season | RS     | RH/Winter | RH/Summer | RA/Winter | RA/Summer |
| --- | ------------------- | ------ | --------- | --------- | --------- | --------- |
|     | Volume (kWh)        | 648    | 1,147     | 637       | 997       | 900       |
|     | Rate (c/kWh)        | 8.4662 | 7.5466    | 8.4662    | 3.5598    | 8.4662    |
| A   | Charge ($)          | $54.90 | $86.59    | $53.94    | $35.47    | $76.17    |

**Step ii) Volumetric Charge for Typical Customer With EV Under Proposed Non-TOU Rates**

| Row | Rate Class / Season | RS     | RH/Winter | RH/Summer | RA/Winter | RA/Summer |
| --- | ------------------- | ------ | --------- | --------- | --------- | --------- |
|     | Volume (kWh)        | 977    | 1,474     | 968       | 1,323     | 1,231     |
|     | Rate (c/kWh)        | 8.4662 | 7.5466    | 8.4662    | 3.5598    | 8.4662    |
| B   | Charge ($)          | $82.73 | $111.22   | $81.97    | $47.09    | $104.19   |

**Steps iii and iv) Off-Peak TOU Rate Discount Calculation**

| Row | Rate Class / Season                           | RS     | RH/Winter | RH/Summer | RA/Winter | RA/Summer | Formula (as printed) |
| --- | --------------------------------------------- | ------ | --------- | --------- | --------- | --------- | -------------------- |
| C   | Incremental Revenue ($/month)                 | $27.83 | $24.63    | $28.02    | $11.62    | $28.02    | = B - A              |
| D   | Applied to Discount to non-TOU Rate ($/month) | $13.91 | $12.32    | $14.01    | $5.81     | $14.01    | = C * 50%            |
| E   | Applicable Off-Peak Volume (kWh)              | 826.5  | 1,260.2   | 821.0     | 1,125.2   | 1,015.9   |                      |
| F   | Rate Discount (c/kWh)                         | 1.6835 | 0.9772    | 1.7066    | 0.5163    | 1.3793    | = D * 100 / E        |
| G   | Proposed non-TOU Rate (c/kWh)                 | 8.4662 | 7.5466    | 8.4662    | 3.5598    | 8.4662    |                      |
| H   | % Discount to non-TOU Rate (%)                | 20%    | 13%       | 20%       | 15%       | 16%       | = F / G              |
| I   | Proposed Off-Peak TOU Rate (c/kWh)            | 6.7827 | 6.5694    | 6.7596    | 3.0435    | 7.0869    | = G - F              |

**Q.** **How does the calculation of the off-peak EV-Only TOU Distribution Rate differ?**

A. The calculation of the off-peak EV-Only TOU Distribution Rate is identical to the off-peak WholeHome TOU Distribution Rate with one notable difference. While the off-peak WholeHome TOU Distribution Rate calculates a discount in off-peak hours by allocating the shared revenue over the entirety of the customer’s metered load, the EV-Only TOU Distribution Rate allocates the same shared revenue over only the customer’s incremental off-peak load, as that is the only load that will be billed at the off-peak EV-Only TOU Distribution Rate. These calculations are illustrated in Table 4 below.

<!-- PDF page 13 (printed page 10) -->

**Table 4: Calculation of Off-Peak EV-Only TOU Distribution Rate**

_Extractor note (not source text): Same layout and conventions as Table 3. Steps i and ii (rows A and B) are identical to Table 3; only rows E, F, H and I differ._

**Step i) Volumetric Charge for Typical Customer Without EV Under Proposed Non-TOU Rates**

| Row | Rate Class / Season | RS     | RH/Winter | RH/Summer | RA/Winter | RA/Summer |
| --- | ------------------- | ------ | --------- | --------- | --------- | --------- |
|     | Volume (kWh)        | 648    | 1,147     | 637       | 997       | 900       |
|     | Rate (c/kWh)        | 8.4662 | 7.5466    | 8.4662    | 3.5598    | 8.4662    |
| A   | Charge ($)          | $54.90 | $86.59    | $53.94    | $35.47    | $76.17    |

**Step ii) Volumetric Charge for Typical Customer With EV Under Proposed Non-TOU Rates**

| Row | Rate Class / Season | RS     | RH/Winter | RH/Summer | RA/Winter | RA/Summer |
| --- | ------------------- | ------ | --------- | --------- | --------- | --------- |
|     | Volume (kWh)        | 977    | 1,474     | 968       | 1,323     | 1,231     |
|     | Rate (c/kWh)        | 8.4662 | 7.5466    | 8.4662    | 3.5598    | 8.4662    |
| B   | Charge ($)          | $82.73 | $111.22   | $81.97    | $47.09    | $104.19   |

**Steps iii and iv) Off-Peak TOU Rate Discount Calculation**

| Row | Rate Class / Season                           | RS     | RH/Winter | RH/Summer | RA/Winter | RA/Summer | Formula (as printed) |
| --- | --------------------------------------------- | ------ | --------- | --------- | --------- | --------- | -------------------- |
| C   | Incremental Revenue ($/month)                 | $27.83 | $24.63    | $28.02    | $11.62    | $28.02    | = B - A              |
| D   | Applied to Discount to non-TOU Rate ($/month) | $13.91 | $12.32    | $14.01    | $5.81     | $14.01    | = C * 50%            |
| E   | Applicable Off-Peak Volume (kWh)              | 318.1  | 315.9     | 320.4     | 315.9     | 320.4     |                      |
| F   | Rate Discount (c/kWh)                         | 4.3738 | 3.8986    | 4.3739    | 1.8390    | 4.3739    | = D * 100 / E        |
| G   | Proposed non-TOU Rate (c/kWh)                 | 8.4662 | 7.5466    | 8.4662    | 3.5598    | 8.4662    |                      |
| H   | % Discount to non-TOU Rate (%)                | 52%    | 52%       | 52%       | 52%       | 52%       | = F / G              |
| I   | Proposed Off-Peak TOU Rate (c/kWh)            | 4.0924 | 3.6480    | 4.0923    | 1.7208    | 4.0923    | = G - F              |

## IV. EV TOU Distribution Rate Is Designed to Achieve Goal #1: Save Money for Customers Who Charge Their EVs During Hours When the Distribution System Is Less Utilized

**Q.** **Will EV-TOU TOU Distribution Rate achieve the first policy goal, specifically to provide savings versus the non-TOU rate to customers who charge EVs during off-peak hours when the distribution system is less utilized?**

A. Yes. This goal is achieved by the rate design of EV TOU Distribution Rate. EV TOU Distribution Rate provides for lower volumetric rates during off-peak periods for both WholeHome and EV-Only customers while the on-peak rates will equal the non-TOU volumetric rate. This will result in savings for customers relative to what they would have been billed on non-TOU rates.

RS customers who take advantage of the WholeHome TOU Rate will save 1.6835 cents/kWh during off-peak hours (saving 20% vs. the non-TOU rate). RS customers taking

<!-- PDF page 14 (printed page 11) -->

advantage of the EV-Only rate will save 4.3738 cents/kWh (savings 52% vs. the non-TOU rate).

RH customers who take advantage of the WholeHome TOU Rate will save 0.9772 cents/kWh during winter off-peak hours (saving 13% vs. the non-TOU rate) and will save 1.7066 cents/kWh during summer off-peak hours (saving 20% vs. the non-TOU rate). RH customers who take advantage of the EV-Only TOU Rate will save 3.8986 cents/kWh during winter off-peak hours (saving 52% vs. the non-TOU rate) and will save 4.3739 cents/kWh during summer off-peak hours (saving 52% vs. the non-TOU rate).

RA customers who take advantage of the WholeHome TOU Rate will save 0.5163 cents/kWh during winter off-peak hours (saving 15% vs. the non-TOU rate) and will save 1.3793 cents/kWh during summer off-peak hours (saving 16% vs. the non-TOU rate). RA customers who take advantage of the EV-Only TOU Rate will save 1.8390 cents/kWh during winter off-peak hours (saving 52% vs. the non-TOU rate) and will save 4.3739 cents/kWh during summer off-peak hours (saving 52% vs. the non-TOU rate).

I estimate that typical RS WholeHome and EV-Only TOU Distribution Rate customers would see a reduction in their bills of $13.91/month relative to what they would be charged under the standard (non-time-of-use) RS rate. I also estimate that RH and RA customers would see reductions of $13.16/month and $9.91/month, respectively, relative to what they would have been charged under the non-TOU rates. Consequently, EV TOU Distribution Rate Pilot is designed to save money for customers who adopt EVs and charge their EVs during periods when the distribution system is less utilized (e.g., off-peak hours).

_Extractor note (not source text): The $13.16 and $9.91 figures are consistent with simple averages of the winter and summer monthly discounts in row D of Tables 3 and 4: RH (12.32 + 14.01)/2 = 13.165; RA (5.81 + 14.01)/2 = 9.91. The testimony does not state how they were derived._

<!-- PDF page 15 (printed page 12) -->

**Q.** **Why do you believe that EV TOU Distribution Rate Pilot’s off-peak hours represent hours during which the distribution system is less utilized?**

A. As explained by Duquesne Light witness Howard S. Gorman (Duquesne Light Statement No. 13), the bulk of distribution system costs are estimated to be driven by non-coincident peak demand. The non-coincident peak demands for the RS class, which serves the vast majority of residential customers, currently take place in the afternoon and early evening, typically between 4:00 pm and 7:00 pm, as shown in Table 5.

**Table 5: Historical Hours of Residential (Non-Lighting) Non-Coincident Peak Demand**

| Hour Ending          | 2019    | 2020    | 2021    | 2022    | 2023    |
| -------------------- | ------- | ------- | ------- | ------- | ------- |
| Highest Peak Day     | 6:00 PM | 6:00 PM | 7:00 PM | 7:00 PM | 6:00 PM |
| 2nd Highest Peak Day | 7:00 PM | 6:00 PM | 7:00 PM | 5:00 PM | 6:00 PM |
| 3rd Highest Peak Day | 6:00 PM | 7:00 PM | 7:00 PM | 7:00 PM | 7:00 PM |
| 4th Highest Peak Day | 7:00 PM | 7:00 PM | 6:00 PM | 5:00 PM | 7:00 PM |
| 5th Highest Peak Day | 7:00 PM | 7:00 PM | 6:00 PM | 7:00 PM | 6:00 PM |

In comparison, the off-peak period for EV TOU Distribution Rate (9:00 pm to 3:00 pm) does not include any of the non-coincident peak hours shown in Table 5.

## V. EV TOU Distribution Rate Is Designed to Achieve Goal #2: Provide Incentives for EV Customers to Utilize the Distribution System More Efficiently by Charging During Off-Peak Hours and Avoid Adding Incremental Load During On-Peak Hours

<!-- PDF page 16 (printed page 13) -->

**Q.** **Is it likely that EV-charging customers will respond to the EV TOU Distribution Rate’s price signals to charge during the off-peak period?**

A. Yes. Figure 1 provides a sample historical profile of weekday hourly EV charging for customers who have elected Duquesne Light’s Generation EV-TOU pilot program. Under Generation EV-TOU pilot, WholeHome EV customers are billed at different rates for consumption during Peak, Off-Peak, and Super Off-Peak hours.[^1] Off-Peak and Super Off-Peak generation rates are lower than the Peak rate.[^2] The figure illustrates that 96.9% of the incremental weekday load expected from EV charging is likely to take place outside the on-peak 3:00 PM to 9:00 PM window.

[^1]: See [Duquesne Light WholeHome EV Rate page](https://duquesnelight.com/energy-money-savings/electric-vehicles/wholehome-ev-rate). As of the time of this filing, Peak hours were defined as 1:00 pm to 9:00 pm, Super Off-Peak hours are defined as 11:00 pm to 6:00 am, and Off-Peak hours are defined as all other hours. No distinction is made between weekdays, weekends, or holidays.

[^2]: As of the date of this filing, the Peak generation rate was 11.16 cents/kWh and the Off-Peak and Super Off-Peak generation rates were 7.06 and 5.09 cents/kWh, respectively.

<!-- PDF page 17 (printed page 14) -->

**Figure 1: Generation EV-TOU Pilot Program EV Charging is Concentrated During Off-Peak Hours**

[DIAGRAM DESCRIPTION: Figure 1: Generation EV-TOU Pilot Program EV Charging is Concentrated During Off-Peak Hours]

A bar chart of average weekday hourly EV charging demand for Generation EV-TOU pilot customers. The y-axis is "Hourly Demand (kW)", running 0.0 to 1.8 in steps of 0.2. The x-axis is "Hour Ending", with one bar per hour from 1 AM through 12 AM (24 bars). Bars outside the on-peak window are solid gray and sit under a bracket labelled "Off-Peak Hours (96.8% of EV Load)". A vertical-line-bounded region over hours ending 4 PM through 9 PM is labelled "On-Peak Hours (3.2% of EV Load)" with a double-headed arrow, and its bars are hatched. Approximate bar heights read from the image (not printed values): demand is highest overnight, about 1.5 kW at 1 AM and about 1.65 kW at 2 AM (the peak), declining to about 1.35 kW at 3 AM, 1.1 kW at 4 AM, 0.95 kW at 5 AM, 0.8 kW at 6 AM and 0.5 kW at 7 AM; it is about 0.1–0.2 kW through the daytime (8 AM to 3 PM, about 0.07 kW at 3 PM); within the on-peak window it is near zero at 4 PM, zero at 5 PM and 6 PM, and rises to about 0.1, 0.17 and 0.2 kW at 7, 8 and 9 PM; then it climbs after the window to about 0.3 kW at 10 PM, 0.47 kW at 11 PM and 0.58 kW at 12 AM. The chart conveys that EV charging is concentrated overnight and late evening, outside the 3–9 PM window.

[→ See original PDF page 17 for visual rendering]

Figure 1 illustrates that EV customers on generation TOU rates primarily charge during the off-peak hours when generation volumetric rates are the lowest, indicating that these customers are responsive to price signals. The EV TOU Distribution Rate will further strengthen this price signal to charge during the off-peak period. Further, the higher on-peak EV TOU Distribution Rate will disincentivize EV customers to charge during on-peak hours.

_Extractor note (not source text): [source discrepancy: the body text on PDF p. 16 says 96.9% of incremental weekday EV load falls outside the on-peak window, while the Figure 1 label reads "96.8% of EV Load" for off-peak hours and "3.2% of EV Load" for on-peak (96.8% + 3.2% = 100%).]_

<!-- PDF page 18 (printed page 15) -->

## VI. EV TOU Distribution Rate Is Designed to Achieve Goal #3: Ensure that Incremental Load from EV Charging does not Change the Allocation of Costs to Customers by Creating a Higher Non-Coincident Peak

**Q.** **Is EV TOU Distribution Rate designed to achieve its third main goal, to ensure that incremental load from EV charging does not change the allocation of costs to customers by creating a higher non-coincident peak?**

A. Yes. At the scale of this pilot, incremental load from EV charging is not expected to add material demand during the current non-coincident peak demand hour, nor will incremental load from EV charging be sufficient to create a higher non-coincident peak demand during a different hour. Consequently, incremental load from EV charging is not expected to change the allocation of distribution system costs to customers.

**Q.** **How could EV charging lead to a different allocation of distribution system costs to customers?**

A. As discussed by Duquesne Light witness Howard S. Gorman (Duquesne Light Statement No. 13), distribution costs are allocated to customers on the basis of either customer-based or demand-based allocators. It is possible that EV charging associated with the EV TOU Distribution Rate could result in an increase to the residential non-coincident peak demand, which could increase distribution costs allocated to residential customers.

<!-- PDF page 19 (printed page 16) -->

**Q.** **At what level of adoption would EV charging materially increase residential customers’ non-coincident peak?**

A. Using hourly load data for residential customers from 2019-2023 and sample EV TOU data provided by Duquesne Light, I have analyzed how residential non-coincident peak demand might be impacted by EV charging at different levels of customer adoption.

**Figure 2: Estimated Impact of EV Adoption on Residential NCP**

[DIAGRAM DESCRIPTION: Figure 2: Estimated Impact of EV Adoption on Residential NCP]

A dual-axis line chart. The x-axis is "Additional EV Accounts (#)", 0 to 600,000 in steps of 100,000. The left y-axis is "Estimated Residential NCP (MW)", 0 to 2,000 in steps of 200. The right y-axis is "Marginal kW NCP / EV Customer", 0.0 to 3.0 in steps of 0.5. A blue line labelled "Estimated Total Residential NCP (Left Axis)" is roughly flat at about 1,350 MW from 0 to about 250,000 additional EV accounts, then rises steadily to about 1,830 MW at 600,000. A red line labelled "Estimated Marginal NCP per Customer (Right Axis)" sits near 0.1 kW per EV customer out to about 230,000 accounts, then rises steeply between about 250,000 and 350,000 accounts to about 1.5 kW, and is roughly flat at about 1.5 kW from there to 600,000. Two dashed vertical lines are labelled: one at about 230,000 additional accounts, labelled "EV Contribution Becomes Material" (with an arrow pointing to the point where the red line begins to climb), and one at about 550,000 accounts, labelled "Current Total Residential Customer Accounts". Values are approximate readings from the image, not printed numbers. The chart conveys that added EV charging does not materially raise the residential non-coincident peak until about 230,000 additional customers.

[→ See original PDF page 19 for visual rendering]

In Figure 2 above, I show that the additional load associated with EV charging is not expected to materially increase the combined residential (i.e., RS, RH, and RA combined) non-coincident peak until approximately 230,000 customers add EV charging load. This compares to roughly 550,000 total residential customer accounts. As discussed by Duquesne Light witness Sarah J. Olexsak (Duquesne Light Statement No. 6), the pilot program is anticipated to be capped at 1,500 customers and Duquesne Light is anticipating

<!-- PDF page 20 (printed page 17) -->

that light-duty EV registrations in the Company’s service territory will be between 79,200 and 205,000 by 2030.

**Q.** **Would EV charging during off-peak times for customers enrolled in the EV TOU Distribution Rate lead to changes in allocated system costs?**

A. No. As shown in Table 5, the non-coincident peak demand for the RS class, which is the vast majority of residential customers, has tended to occur during late afternoon. In contrast, EV charging load is overwhelmingly expected to take place during off-peak hours, as shown in Figure 1. And, as shown in Figure 2, customer adoption of the EV TOU Distribution Rate, at the scale anticipated by this pilot, is not expected to increase residential non-coincident peak demand materially. Consequently, I believe that the allocation of distribution system costs to customers would not be materially impacted by incremental load from EV TOU Distribution Rate customers when considering the scale of this Pilot.

**Q.** **Could large scale adoption of EV charging result in changes to the allocation of distribution system costs in the future?**

A. Yes. As discussed by Duquesne Light witness Howard S. Gorman (Duquesne Light Statement No. 13), demand-based distribution costs are currently allocated to the RS, RH, and RA rate classes on the basis of their non-coincident peak demands. Given the scale of this Pilot, I do not expect that incremental EV charging load will have a material impact on residential non-coincident peak demands. However, it is possible in the future that larger

<!-- PDF page 21 (printed page 18) -->

scale adoption of EVs and the accompanying growth in EV charging load could become material. At that time, Duquesne Light could determine that the incremental load associated with EV charging might impact distribution system cost allocations to customers.

## VII. Alternative Distribution Ratemaking Mechanisms and Rate Design Considerations

**Q.** **The commission’s policy statement on alternative distribution ratemaking mechanisms, 52 PA. Code §§ 69.3301 and 69.3302, identifies a number of factors the commission may consider when evaluating an alternative distribution rate mechanism. Has the company considered these factors with respect to EV-TOU Distribution Rate?**

A. Yes. I address each of them below.

_(1) How the ratemaking mechanism and rate design align revenues with cost causation principles as to both fixed and variable costs._

The rate design for the EV-TOU Distribution Rate is based on current rates for RS, RH, and RA, all of which are based on cost causation principles. EV-TOU is simply a discount during off-peak hours to these rates. As I describe earlier in my testimony (pp. 16-17), the incremental sales associated with electric vehicle charging are not anticipated to lead to changes in cost allocations at the scale proposed in this pilot. The Pilot will also provide the Company with information regarding whether TOU rates can be relied upon to mitigate peak usage and eliminate or delay system upgrades.

_(2) How the ratemaking mechanism and rate design impact the fixed utility’s capacity utilization._

<!-- PDF page 22 (printed page 19) -->

EV-TOU rates are designed to incentivize customers to charge electric vehicles during off-peak hours when the distribution system is less utilized and to disincentivize them from charging electric vehicles during on-peak hours when the distribution system is more utilized.

_(3) Whether the ratemaking mechanism and rate design reflect the level of demand associated with the customer’s anticipated consumption levels._

The proposed rates reflect the anticipated on- and off-peak consumption associated with electric vehicle charging. As I discuss earlier (p. 16), incremental electric vehicle charging load during off-peak hours is not anticipated to materially increase the residential class non-coincident peak demand or cost allocation at the scale of this pilot.

_(4) How the ratemaking mechanism and rate design limit or eliminate interclass and intraclass cost shifting._

The EV-TOU rate only applies to RS, RH, and RA customers who charge an electric vehicle and will provide a discount off of the residential rates that will be set in this proceeding. This will not shift costs to other classes.

_(5) How the ratemaking mechanism and rate design limit or eliminate disincentives for the promotion of efficiency programs._

The proposed discounts to volumetric rates during off-peak hours will still create an incentive for energy efficiency measures. The EV-Only TOU Distribution Rate only applies to incremental load associated with electric vehicle charging. Incentives for energy efficiency for existing household load would be unaffected for customers under this rate. Second, the discounts for EV-Only and WholeHome only apply to off-peak hours, so

<!-- PDF page 23 (printed page 20) -->

consumers will still be incentivized to invest in energy efficiency systems during on-peak hours when their average household load is already the highest. Third, the EV-TOU off-peak rates, though discounted, are still non-zero and provide customers with an opportunity to achieve savings from reducing consumption.

_(6) How the ratemaking mechanism and rate design impact customer incentives to employ efficiency measures and distributed energy resources._

The proposed discounts do not apply to on-peak hours, so EV-TOU customers will continue to be incentivized to invest in energy efficiency measures to the same extent as customers on non-TOU rates for consumption during those hours. Similarly, EV-Only customers will continue to be incentivized to invest in energy efficiency measures for their existing household load to the same extent as non-TOU customers. Both EV-Only and WholeHome customers will continue to be incentivized to reduce consumption during off-peak hours because the off-peak TOU rates are non-zero and any reduction in usage will result in reduced charges.

_(7) How the ratemaking mechanism and rate design impact low-income customers and support consumer assistance programs._

The proposed rates represent a discount to non-TOU rates during off-peak hours and would provide savings to low-income customers who charge electric vehicles during off-peak hours. This program is, in part, an assistance program that makes transportation more affordable to customers.

_(8) How the ratemaking mechanism and rate design impact customer rate stability principles._

<!-- PDF page 24 (printed page 21) -->

The rate design creates a discount to the customer’s off-peak volumetric rate. Therefore, it is linked to proposed rates and thus the customer’s rate stability remains the same as if the customer were on their non-TOU rate. Therefore, the rate structure is stable and transparent.

_(9) How weather impacts utility revenue under the ratemaking mechanism and rate design._

These rates are linked to RS, RH, and RA rates and thus experience similar impacts attributable to weather.

_(10) How the ratemaking mechanism and rate design impact the frequency of rate case filings and affect regulatory lag._

This rate design will not impact the frequency of rate case filings or regulatory lag.

_(11) If or how the ratemaking mechanism and rate design interact with other revenue sources, such as Section 1307 automatic adjustment surcharges, 66 Pa.C.S. § 1307 (relating to sliding scale of rates; adjustments), riders such as 66 Pa.C.S. § 2804(9) (relating to standards for restructuring of electric industry) or system improvement charges, 66 Pa.C.S. § 1353 (relating to distribution system improvement charge)._

Not applicable.

_(12) Whether the alternative ratemaking mechanism and rate design include appropriate consumer protections._

The rate is an optional rate and provides a discount to the current rates a customer would otherwise be charged. Therefore, the customer is better off under this rate design (and has the option to not choose the rate). This provides adequate protections as the

<!-- PDF page 25 (printed page 22) -->

customer’s bill cannot be greater under this tariff than under the otherwise applicable RS, RH, and RA rates.

_(13) Whether the alternative ratemaking mechanism and rate design are understandable to consumers._

By applying a simple discount that is transparent and predictable, it is very easy for a customer to understand the rider structure. RS, RH, and RA customers already have the option to select a time-of-use supply rate and many have done so. This suggests that customers can understand time-of-use rates. In addition, the Company will provide education to customers regarding the distribution EV-TOU rate.

_(14) How the ratemaking mechanism and rate design will support improvements in utility reliability._

This rate design is based on proposed RS, RH, and RA rates with a simple discount to the off-peak volumetric rate when the distribution system is less utilized. The customer receives no discount during on-peak hours when the distribution system is more utilized. Further, as I show in Figure 2, incremental load associated with electric vehicle charging is not likely to increase the non-coincident peak demand of the residential class at the scale proposed in this pilot. From a long-term perspective, this pilot will yield information on how customers may respond to price signals by shifting load. This information may allow the Company to improve reliability in the future.

_(b) In any distribution rate filing by a fixed utility under 66 Pa.C.S. § 1308 (relating to voluntary changes in rates) that proposes an alternative ratemaking mechanism and rate design, the fixed utility shall explain how these factors impact the distribution rates for each customer class._

<!-- PDF page 26 (printed page 23) -->

Table 2 demonstrates the rate impact expected for participating customers. Further, as noted above, these customers continue to pay fixed customer charges and on-peak volumetric rates consistent with the RS, RH, and RA class rates.

## VIII. Conclusion

**Q.** **Does this conclude your direct testimony?**

A. Yes, it does.

---

_Extractor note (not source text): Verification. Footnotes: the PDF has 2 footnote reference marks (both on PDF p. 16) and this extract has 2 definitions. Tables 1–5 are reproduced; Tables 2, 3, 4 and 5 were checked against rendered page images, and the arithmetic in Tables 3–4 was spot-checked (G − F = I; F/G = H; D × 100 / E = F). Figures: Figure 1 (PDF p. 17) and Figure 2 (PDF p. 19) are the only images in the PDF. The PDF has 1 external hyperlink (footnote 1) and internal links from the table of contents and the lists of tables and figures. The Table 3 and Table 4 spreadsheets are embedded as vector graphics in the source; their values were read from the rendered page and agree with the PDF text layer._
