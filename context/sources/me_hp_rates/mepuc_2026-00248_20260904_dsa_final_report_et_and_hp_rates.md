---
source: mepuc_2026-00248_20260904_2025_12_05_dsa_final_report_et_and_hp_rates.pdf
docket: "2022-152 as printed on every page header ('Docket No. 2022-152, Attachment 6, Page n of 41' for PDF pages 1-41 and 'Docket No. 2022-152, Attachment 7, Page n of 7' for PDF pages 42-48); extractor note: our manifest records this file as a 2026-09-04 filing in docket 2026-00248, and the PDF's embedded title is '2025-12-05 CMP Final Report and Attachments 2025 (2022-152) (1).pdf'"
utility: Central Maine Power Company (CMP)
rate: "Electric Technology (ET) rate and Seasonal Heat Pump (SHP) rate (A-Seasonal); both optional residential delivery rates"
filing_date: "Report dated December 2025 (printed on cover); filed 2026-09-04 per our manifest (not printed in the PDF)"
filer: "Prepared for Central Maine Power by Demand Side Analytics, LLC (DSA); filing party per our manifest: Efficiency Maine Trust (not printed in the PDF)"
document_type: "exhibit (impact evaluation report, PDF pages 1-41, printed 'Attachment 6'; followed by PDF pages 42-48, printed 'Attachment 7': CMP Alternative Rates Survey instrument)"
pages_total: 48
extraction_scope: full
source_url: "https://mpuc-cms.maine.gov/CQM.Public.WebUI/MatterManagement/MatterFilingItem.aspx?FilingSeq=136224&CaseNumber=2026-00248 (doc {40BA6DA0-0000-C172-B975-A2DE17C9D710}) -- download URL recorded in our manifest, not text from the PDF"
original_pdf_path: /ebs/home/jpv_switch_box/hp_rate_docket_staging/me_cmp_versant/mepuc_2026-00248_20260904_2025_12_05_dsa_final_report_et_and_hp_rates.pdf
why_here: "Demand Side Analytics evaluation: what data CMP had (rebate data held only by the evaluator, plus interval data) and the bill and load results."
---

# Impact Evaluation of Central Maine Power's Electric Technology and Seasonal Heat Pump Delivery Rates: Final Report

**Source**: mepuc_2026-00248_20260904_2025_12_05_dsa_final_report_et_and_hp_rates.pdf
**Pages**: 48 (PDF pages 1-41 = report, "Attachment 6"; PDF pages 42-48 = "Attachment 7", the CMP Alternative Rates Survey instrument)
**Date**: December 2025
**Author(s)**: Demand Side Analytics, LLC (DSA), prepared for Central Maine Power

_Extractor note (not source text): Text is transcribed from the PDF text layer and checked against rendered pages; no typographical corrections were made (source typos are kept, some flagged `[sic]`). The running page header ("Docket No. 2022-152 / Attachment 6 / Page n of 41") and footer ("Page | n", "Internal Use", DSA logo) are stripped; PDF page markers are kept, and the report's printed page number equals the PDF page number for PDF pages 1-41 (for the survey, the printed number 1-7 equals PDF page minus 41). The report has two footnotes (both numbered "1" in the source, on PDF pages 5 and 19); they are written here as [^1] and [^2]. Table notes printed under tables are kept as "Note:" lines directly below each table. All 39 figures were inspected as rendered images; figure descriptions give values read off the charts and are approximate unless a number is printed on the figure. Equations are transcribed from the rendered page. The PDF uses a logo, a cover photograph (a lighthouse on a rocky coast) and decorative rules that are not described further. Figures with extractor-measured values are labelled "(read from chart)"._

---

<!-- PDF page 1 (printed "Page 1 of 41", cover) -->

Internal Use

**Final Report**

# IMPACT EVALUATION OF CENTRAL MAINE POWER'S ELECTRIC TECHNOLOGY AND SEASONAL HEAT PUMP DELIVERY RATES

Prepared for Central Maine Power
By Demand Side Analytics, LLC
December 2025

Docket No. 2022-152
Attachment 6
Page 1 of 41

<!-- PDF page 2 (printed Page | 2) -->

## TABLE OF CONTENTS

| Section | Title                                     | Page |
| ------- | ----------------------------------------- | ---- |
| 1       | Introduction                              | 5    |
| 2       | Rate Details                              | 7    |
| 2.1     | ELECTRIC TECHNOLOGY RATE                  | 7    |
| 2.2     | SEASONAL HEAT PUMP RATE                   | 7    |
| 2.3     | ENROLLMENT HISTORY                        | 8    |
| 3       | Data Sources                              | 9    |
| 3.1     | EMT REBATE DATA                           | 9    |
| 3.2     | INTERVAL DATA                             | 9    |
| 3.3     | WEATHER DATA                              | 12   |
| 3.4     | OTHER DATA                                | 13   |
| 4       | Methods                                   | 14   |
| 4.1     | PREPARING THE INTERVAL DATA FOR ANALYSIS  | 15   |
| 4.2     | REMOVING ACCOUNTS WITH CONFOUNDING ISSUES | 17   |
| 4.3     | DEVELOPING THE MATCHED COMPARISON GROUP   | 18   |
| 4.4     | MODELING METHODS                          | 19   |
| 4.5     | WEATHER-NORMALIZING THE RESULTS           | 20   |
| 5       | Results                                   | 21   |
| 5.1     | ELECTRIC TECHNOLOGY RATE                  | 21   |
| 5.1.1   | Key Findings                              | 21   |
| 5.1.2   | Matched Comparison Group                  | 22   |
| 5.1.3   | Difference-in-Differences Results         | 25   |
| 5.1.4   | Weather-Normalizing                       | 26   |
| 5.1.5   | Bill Savings                              | 27   |
| 5.2     | SEASONAL HEAT PUMP RATE                   | 30   |
| 5.2.1   | Key Findings                              | 30   |
| 5.2.2   | Matched Comparison Group                  | 32   |
| 5.2.3   | Difference-in-Differences Results         | 34   |
| 5.2.4   | Weather-Normalizing                       | 35   |
| 5.2.5   | Bill Savings                              | 37   |
| 6       | Conclusion                                | 40   |

<!-- PDF page 3 (printed Page | 3) -->

## Figures

| Figure    | Title                                                                             | Page |
| --------- | --------------------------------------------------------------------------------- | ---- |
| Figure 1  | Difference-in-Difference Results                                                  | 6    |
| Figure 2  | Electric Technology Rate Enrollment History                                       | 8    |
| Figure 3  | Average Daily Consumption in Time, ET Accounts                                    | 10   |
| Figure 4  | Average Daily Consumption in Time, SHP Accounts                                   | 10   |
| Figure 5  | Average Hourly Load Shape by Month, ET Accounts                                   | 11   |
| Figure 6  | Average Hourly Load Shape by Month, SHP Accounts                                  | 11   |
| Figure 7  | Pre-Enrollment Electric Consumption Heat Map, ET Accounts                         | 12   |
| Figure 8  | Pre-Enrollment Electric Consumption Heat Map, SHP Accounts                        | 12   |
| Figure 9  | Weather Mapping                                                                   | 13   |
| Figure 10 | Methodological Overview                                                           | 15   |
| Figure 11 | Distribution of Account-Level Weather-Normalized Annual Consumption, ET Accounts  | 16   |
| Figure 12 | Distribution of Account-Level Weather-Normalized Annual Consumption, SHP Accounts | 17   |
| Figure 13 | Confounding EV Example                                                            | 17   |
| Figure 14 | Confounding Heat Pump Example                                                     | 18   |
| Figure 15 | Hypothetical False Experiment Results                                             | 19   |
| Figure 16 | Average Daily Consumption Time Series, Pre-Enrollment                             | 23   |
| Figure 17 | Distribution of Weather-Normalized Annual Consumption, Pre-Enrollment             | 24   |
| Figure 18 | Average Daily kWh by Average Daily Temperature                                    | 24   |
| Figure 19 | Distribution of Average Demand during the ISO-NE Peak Periods                     | 25   |
| Figure 20 | ET DID Results – Energy Impacts                                                   | 25   |
| Figure 21 | ET DID Results – Demand Impacts during the Winter Peak Period                     | 26   |
| Figure 22 | ET DID Results – Demand Impacts during the Summer Peak Period                     | 26   |
| Figure 23 | Daily DID Estimates against Temperature, ET Analysis                              | 27   |
| Figure 24 | Weather-Normalized Daily Impacts, ET Analysis                                     | 27   |
| Figure 25 | Distribution of Delivery Savings in First Year, ET Analysis                       | 29   |
| Figure 26 | Savings by Month, ET Analysis                                                     | 29   |
| Figure 27 | Average Daily Consumption Time Series, Pre-Enrollment                             | 32   |
| Figure 28 | Distribution of Weather-Normalized Annual Consumption, Pre-Enrollment             | 33   |
| Figure 29 | Average Daily kWh by Average Daily Temperature                                    | 33   |
| Figure 30 | Distribution of Average Demand during the ISO-NE Peak Periods                     | 34   |
| Figure 31 | SHP DID Results – Energy Impacts                                                  | 34   |

<!-- PDF page 4 (printed Page | 4) -->

| Figure    | Title                                                          | Page |
| --------- | -------------------------------------------------------------- | ---- |
| Figure 32 | SHP DID Results – Demand Impacts during the Winter Peak Period | 35   |
| Figure 33 | SHP DID Results – Demand Impacts during the Summer Peak Period | 35   |
| Figure 34 | Daily DID Estimates against Temperature, SHP Analysis          | 36   |
| Figure 35 | Weather-Normalized Daily Impacts, SHP Analysis                 | 36   |
| Figure 36 | Distribution of Delivery Savings in First Year, SHP Analysis   | 38   |
| Figure 37 | Savings by Month, SHP Analysis                                 | 39   |
| Figure 38 | Net Energy Impact by Day of Year, ET Analysis                  | 41   |
| Figure 39 | Net Energy Impact by Day of Year, SHP Analysis                 | 41   |

## Tables

| Table    | Title                                       | Page |
| -------- | ------------------------------------------- | ---- |
| Table 1  | Key Findings                                | 5    |
| Table 2  | Rate A and ET Rate Comparison               | 7    |
| Table 3  | Rate A and SHP Rate Comparison              | 7    |
| Table 4  | Other Data Sources                          | 13   |
| Table 5  | Number of Accounts Removed from Analysis    | 16   |
| Table 6  | High Level Findings                         | 21   |
| Table 7  | Impact Estimates, ET Analysis               | 22   |
| Table 8  | Energy Impacts by Time Period, ET Analysis  | 22   |
| Table 9  | Bill Impact Findings, ET Analysis           | 28   |
| Table 10 | DID Bill Savings, ET Analysis               | 30   |
| Table 11 | Impact Estimates, SHP Analysis              | 31   |
| Table 12 | Energy Impacts by Time Period, SHP Analysis | 31   |
| Table 13 | Bill Impact Findings, SHP Analysis          | 37   |
| Table 14 | SHP Rate Changes                            | 38   |
| Table 15 | DID Bill Savings, SHP Analysis              | 39   |

_Extractor note (not source text): the list of tables prints Table 14 as "SHP Rate Changes"; the table's own caption on PDF page 38 reads "Table 14: SHP and Rate A Changes". Both are kept as printed._

<!-- PDF page 5 (printed Page | 5) -->

## 1 INTRODUCTION

Central Maine Power (CMP) contracted with Demand Side Analytics (DSA) to estimate the impact of rate transitions on household energy consumption for homes that enrolled in one of two new delivery rate options: the Electric Technology (ET) rate and the Seasonal Heat Pump (SHP) rate. The ET rate is an optional delivery rate that offers CMP's residential customers a reduced volumetric charge ($/kWh) paired with a larger monthly service charge. Likewise, the SHP rate is an optional delivery rate that offers CMP's residential customers a significantly reduced volumetric charge during the heating season (November 1st through April 31st [sic]) paired with a larger monthly service charge and a larger volumetric charge outside of the heating season. In Section 2, we provide additional details about the rate structures and enrollment history.

The guiding research questions for this evaluation were:

- **Electric Technology Rate:** Does a year-round reduction in volumetric delivery charges induce additional electric consumption for households that sign up for the rate?
- **Seasonal Heat Pump Rate:** Does a seasonal change in volumetric delivery charges induce additional electric consumption during the heating season, and/or reduced electric consumption during the cooling season?

Key findings are shown in Table 1.

**Table 1: Key Findings**

| Topic                                      | Finding                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Does annual consumption change?            | **ET Rate:** We did not find a statistically significant increase or decrease in average annual consumption or seasonal consumption following rate transition. **SHP Rate:** Following rate transition, we found that SHP accounts increased their electric consumption by about 1.4% (114 kWh) during the heating season (p-value = 0.01). The cooling season impact was also positive (1.1% or 44 kWh) but not statistically significant.                                                                                                 |
| Does peak demand change?[^1]               | We did not find significant increases or decreases in average demand during the summer or winter peak periods following ET or SHP rate transition.                                                                                                                                                                                                                                                                                                                                                                                          |
| What were the bill impacts from the rates? | **ET Rate:** Accounts that moved from Rate A to the ET rate saved over $200 (approximately 10%), on average, in their first year on the ET rate relative to a baseline scenario where they did not change rates. **SHP Rate:** Accounts that moved from Rate A to the SHP rate paid about $100 more (or 8% more), on average, in their first year on the SHP rate relative to a baseline scenario where they did not change rates. However, recent changes to the SHP and Rate A structures likely produce bill savings. See Section 5.2.5. |

[^1]: We used the ISO-NE peak demand definitions (summer: 1:00 to 5:00 PM on non-holiday weekdays in June, July, and August; winter: 5:00 to 7:00 PM on non-holiday weekdays in December and January).

<!-- PDF page 6 (printed Page | 6) -->

To estimate the impact of rate transition on consumption, DSA compared post-enrollment and pre-enrollment consumption data for enrolled accounts with consumption data for a matched comparison group consisting of homes that are on the standard residential rate (Rate A) and had the same technology as the participants. In order to isolate the effect of the rate transition on energy consumption, premises with major load modifier installations (heat pumps, heat pump water heaters, EV chargers, etc.) within a year of rate transition were removed from the analysis. Likewise, control group candidates with major load modifier installations during the analysis window were removed. The goal with this approach was to avoid confounding the impact of the rate transition with the impact of the technology adoption. After developing the matched comparison group, we used the difference-in-differences technique to estimate energy and demand impacts. Estimates were then weather-normalized using typical meteorological year (TMY3) weather conditions. We verified the robustness of the difference-in-differences estimates using fixed-effects and time-effects panel regression models.

For each analysis, Figure 1 shows the energy impacts by time of year. The orange bars represent the change in average daily kWh (positive implies an increase, negative implies a decrease). The black reference lines in the right panel separate the SHP heating and cooling seasons. The figure echoes the takeaways from Table 1 – energy impacts were negligible for ET accounts and small for SHP accounts.

Although our methodological approach was to remove homes where load modifiers were installed within a year of rate transition, it's possible that the pre/post differences in Figure 1 could be explained by load modifiers that we are not aware of, if they affected the participant and matched control group differently (e.g., adding another supplemental heat pump or a second electric vehicle).

**Figure 1: Difference-in-Difference Results**

[DIAGRAM DESCRIPTION: Figure 1: Difference-in-Difference Results]

Two side-by-side line-and-bar charts titled "Net Impact - ET Analysis" (left) and "Net Impact - SHP Analysis" (right). Both plot Average Daily kWh (y axis, 0 to about 60) against Date (x axis, 01/01 to 01/01, one calendar year). A light-blue line ("Participant Post Usage") and a dashed gray line ("Baseline with DID Adjustment") lie almost on top of each other, tracing the seasonal load: roughly 55-62 kWh/day in January, falling to about 30 kWh/day in late spring and summer and rising again to 45-60 kWh/day in December for ET; for SHP the summer trough is lower (about 18-25 kWh/day). Orange bars ("Load Impact (Diff-in-Diff)") sit just above zero and are visually tiny relative to the usage lines. The SHP panel has two vertical dashed black lines near 05/01 and 11/01 separating the heating and cooling seasons. Legend: Participant Post Usage; Baseline with DID Adjustment; Load Impact (Diff-in-Diff).

[→ See original PDF page 6 for visual rendering]

In subsequent sections of this report, we provide additional details regarding the rates, our impact evaluation methodology, our input data sets, and our findings.

<!-- PDF page 7 (printed Page | 7) -->

## 2 RATE DETAILS

### 2.1 ELECTRIC TECHNOLOGY RATE

CMP began offering the ET delivery rate to residential customers in January 2023. CMP designed the ET rate to support the adoption of new electric technologies like heat pumps and electric vehicles (EVs) by reducing the volumetric delivery charge customers pay for energy and increasing fixed charges. Table 2 compares the monthly service charge and the volumetric charge ($/kWh) for the standard residential rate (Rate A) and the ET rate. Note the table shows the rates as they were when this research began, not the current version of the rates.

**Table 2: Rate A and ET Rate Comparison**

| Rate                | Service Charge | Volumetric Charge ($/kWh) |
| ------------------- | -------------- | ------------------------- |
| Rate A              | $26.60         | $0.108980                 |
| Electric Technology | $40.67         | $0.077626                 |

Note: The ET rate does not include the first 50 kWh use in the Service Charge like Rate A does. It does include the first 750 kWh of usage sales-tax free.

### 2.2 SEASONAL HEAT PUMP RATE

Like the ET rate, CMP began offering the SHP delivery rate to residential customers in January 2023. CMP designed the SHP rate to support the use of heat pumps for residential heating loads. Table 3 compares the monthly service charge and the volumetric charge ($/kWh) for the standard residential rate (Rate A) and the SHP rate. The service charge for the SHP rate does not vary seasonally, but the volumetric charge does. The SHP volumetric charge during the heating season is approximately one-tenth of the volumetric charge for Rate A, and the SHP volumetric charge outside of the heating season is approximately 2.5 times larger than the volumetric charge for Rate A. As in the prior section, the table shows the rates as they were when this research began rather than the current version of the rates.

**Table 3: Rate A and SHP Rate Comparison**

| Rate               | Period                | Service Charge | Volumetric Charge ($/kWh) |
| ------------------ | --------------------- | -------------- | ------------------------- |
| Rate A             | All months            | $26.60         | $0.108980                 |
| Seasonal Heat Pump | November 1 – April 30 | $40.55         | $0.011226                 |
| Seasonal Heat Pump | May 1 – October 31    | $40.55         | $0.278592                 |

Note: The SHP rate does not include the first 50 kWh use in the Service Charge like Rate A does. It does include the first 750 kWh of usage sales-tax free.

_Extractor note (not source text): arithmetic check on the printed rates: 0.011226 / 0.108980 = 0.103 (about one-tenth); 0.278592 / 0.108980 = 2.56 (about 2.5 times), consistent with the sentence above Table 3._

<!-- PDF page 8 (printed Page | 8) -->

### 2.3 ENROLLMENT HISTORY

As of October 2024, there were approximately 5,000 accounts enrolled on the ET rate and approximately 3,000 accounts enrolled on the SHP rate. Figure 2 shows the cumulative number of SHP and ET enrollments through October 2024. Not all of these homes were included in our analysis, as homes with less than one year of pre- or post-enrollment consumption data were removed, as were homes that installed load modifying technologies (heat pumps, EV chargers, heat pump water heaters) within one year of rate transition.

**Figure 2: Electric Technology Rate Enrollment History**

[DIAGRAM DESCRIPTION: Figure 2: Electric Technology Rate Enrollment History]

A line chart of cumulative enrollments (y axis, 0 to 5,000+) against date (x axis, 01/01/23 to 01/01/25). Two lines: a solid blue "ET Enrollments" line and a dashed gray "SHP Enrollments" line. Both start at zero in January 2023 and rise together to roughly 1,200 enrollments by about February 2023. After that the ET line climbs steadily, reaching about 2,300 by 07/01/23, about 3,300 by 01/01/24 and about 5,100 by roughly October 2024 where it ends. The SHP line grows more slowly: about 1,600 by 07/01/23, about 2,000 by 01/01/24, about 2,700 by 04/01/24 and about 2,950 where it ends in late 2024. (Values read from chart, approximate.) Legend: ET Enrollments, SHP Enrollments. Note: the chart title says "Electric Technology Rate" but plots both rates.

[→ See original PDF page 8 for visual rendering]

<!-- PDF page 9 (printed Page | 9) -->

## 3 DATA SOURCES

There were three primary data sets used for this analysis:

- Efficiency Maine Trust (EMT) rebate data
- Historical hourly interval data for homes enrolled on the ET or SHP rates and for a control pool of homes on Rate A
- Historical weather data

A number of other data sets – like ET and SHP rate participation data and information regarding which households have generation capability or are low income – were also used for the analysis. Details regarding each data set are provided below.

### 3.1 EMT REBATE DATA

Efficiency Maine administers programs that help energy consumers in Maine reduce their energy costs (via energy efficiency) and lower their greenhouse gas emissions. In running these programs, EMT compiles rebate data, which is a record of who participated in their rebate programs with details about when they participated and the specific equipment they installed. The full history of rebate data was not used for this analysis, but DSA had partial rebate data for heat pump water heaters, heat pumps, and EVs through prior work with EMT. EMT approved the use of this rebate data for the analysis under the condition that DSA not share the data with CMP or any other parties (as agreed to when DSA signed EMT's Confidential Information Management System policy).

The primary role of the rebate data was to identify control group candidates – premises in CMP territory that are not on the ET rate but have installed a heat pump, heat pump water heater, or EV charger within the past few years.

We also used participation dates in the Efficiency Maine rebate data to flag ET or SHP rate accounts that installed heat pumps, heat pump water heaters, or EV chargers within one year of rate transition. Such homes were removed to avoid confounding the effects of the adoption of technology with the rate impacts. For example, suppose a homeowner received a rebate for a heat pump in January and then enrolled on the rate in February. For such a premise, we would not be able to separate the impact of the technology from the impact of the rate.

### 3.2 INTERVAL DATA

The CMP team provided DSA with hourly interval data for accounts enrolled on the ET or SHP rate. For the ET rate accounts, the interval data spanned the period between January 2022 and September 2024. For the SHP rate accounts, the interval data spanned the period between January 2022 and July 2025. The difference in data spans is tied to reporting requirements – the ET analysis had to be completed in by December 2024 while the SHP analysis had to be completed by December 2025. We also received hourly interval data for a control pool of Rate A homes. The control pool primarily consisted of homes with heat pumps, heat pump water heaters, and/or EVs but also included some homes that may not

<!-- PDF page 10 (printed Page | 10) -->

have these technologies since the ET rate is open to all residential customers. The matched comparison groups were selected from the control pool.

Figure 3 and Figure 4 show average daily consumption throughout the analysis window for the ET and SHP accounts respectively (see the blue lines). Note these figures represent a blend of pre-enrollment and post-enrollment data. The purple area in the background shows average daily temperature (see the secondary Y axis on the right side of the figure). Most spikes and dips in consumption can be traced to similar spikes in weather conditions. Average electric use tends to be higher for ET accounts than SHP accounts, in part due to the presence of EVs. Summer load shapes for the ET premises also suggest a higher prevalence of A/C than in SHP premises. Overall, the figures suggest that average daily consumption is seasonal but consistent from one year to the next (despite the rate transition).

**Figure 3: Average Daily Consumption in Time, ET Accounts**

[DIAGRAM DESCRIPTION: Figure 3: Average Daily Consumption in Time, ET Accounts]

A time-series chart, 01/01/2022 to 01/01/2025 on the x axis. Left y axis: Average Daily kWh (0-100); right y axis: Average Daily Temperature (0-80, degrees F). A blue line ("Average Daily kWh") oscillates seasonally between roughly 30 kWh/day in summer and 50-65 kWh/day in winter, ending around October 2024. A lavender shaded area ("Average Daily Temperature (F)") shows the annual temperature cycle, peaking each summer and dropping each winter, mirroring (inversely) the consumption line. Legend: Average Daily kWh; Average Daily Temperature (F).

[→ See original PDF page 10 for visual rendering]

**Figure 4: Average Daily Consumption in Time, SHP Accounts**

[DIAGRAM DESCRIPTION: Figure 4: Average Daily Consumption in Time, SHP Accounts]

Same format as Figure 3 for SHP accounts, x axis 01/01/2022 to about 07/01/2025. The blue Average Daily kWh line has a deeper seasonal swing than the ET chart: roughly 17-25 kWh/day in summer, rising to about 55-70 kWh/day in winter peaks. The lavender temperature area is overlaid on the secondary axis (0-80 F). Legend: Average Daily kWh; Average Daily Temperature (F).

[→ See original PDF page 10 for visual rendering]

<!-- PDF page 11 (printed Page | 11) -->

Figure 5 and Figure 6 show average hourly load shapes by month and period (pre-enrollment or post-enrollment) for the ET and SHP accounts respectively. Demand is generally highest in the winter months and lowest in the shoulder months. The shape varies by season but loads consistently climb in the morning and peak in the late afternoon. Overall, post-enrollment patterns largely follow pre-enrollment patterns.

**Figure 5: Average Hourly Load Shape by Month, ET Accounts**

[DIAGRAM DESCRIPTION: Figure 5: Average Hourly Load Shape by Month, ET Accounts]

A grid of twelve small line charts (panels labeled 1 to 12 for the calendar months, 4 columns by 3 rows). Each panel plots Average Demand (kW, y axis 0-3) against Hour Ending (x axis 1 to 25). Two lines per panel, a solid blue "Pre-Enrollment" line and a dashed gray "Post-Enrollment" line, overlap closely. Winter panels (1, 2, 12) sit around 2-2.5 kW with a modest evening peak; spring and fall panels (4, 5, 9, 10) are lowest at roughly 1-1.5 kW; summer panels (7, 8) climb through the afternoon. Legend: Pre-Enrollment, Post-Enrollment.

[→ See original PDF page 11 for visual rendering]

**Figure 6: Average Hourly Load Shape by Month, SHP Accounts**

[DIAGRAM DESCRIPTION: Figure 6: Average Hourly Load Shape by Month, SHP Accounts]

Same twelve-panel layout as Figure 5 for SHP accounts. Winter panels (1, 2, 3, 12) are highest at roughly 2-2.5 kW and nearly flat across the day with a small evening bump; summer and shoulder panels (5-10) are lowest at roughly 1 kW. Pre-enrollment (solid blue) and post-enrollment (dashed gray) lines nearly coincide in every panel. Legend: Pre-Enrollment, Post-Enrollment.

[→ See original PDF page 11 for visual rendering]

Figure 7 and Figure 8 show electric consumption heat maps for the ET and SHP accounts respectively. Although the scales between the two figures differ, they can be interpreted the same way: pockets of orange represent times of the year when electric use is relatively high, and pockets of blue represent times of the year when electric use is relatively low. Note these heat maps were developed using pre-enrollment data. For both groups, winter loads are relatively high throughout the day. The biggest difference between the two groups is in the summer season – the ET accounts show greater cooling

<!-- PDF page 12 (printed Page | 12) -->

loads than the SHP accounts (see the orange afternoon pocket in the period between July and September). Given the increased volumetric charge during the summer months for the SHP rate, the comparatively lower summer loads for SHP accounts may speak to the type of account the rate attracts.

**Figure 7: Pre-Enrollment Electric Consumption Heat Map, ET Accounts**

[DIAGRAM DESCRIPTION: Figure 7: Pre-Enrollment Electric Consumption Heat Map, ET Accounts]

A heat map with Hour Ending (1 to 24) on the x axis and Date (01/01 at the bottom to 12/31 at the top) on the y axis. Color encodes Average Demand (kW) on a blue-to-orange diverging scale; the legend steps are 1.05, 1.30, 1.55, 1.79, 2.04, 2.28, 2.53, 2.78 and 3.02 kW. Orange (high demand) bands appear across winter months (January-March and November-December), especially in the evening hours (about hours 18-22) and morning; blue (low demand) dominates the overnight hours from roughly April through October, with a lighter orange pocket in the afternoon/evening in July-September (cooling load).

[→ See original PDF page 12 for visual rendering]

**Figure 8: Pre-Enrollment Electric Consumption Heat Map, SHP Accounts**

[DIAGRAM DESCRIPTION: Figure 8: Pre-Enrollment Electric Consumption Heat Map, SHP Accounts]

Same format as Figure 7 for SHP accounts with a different color scale; legend steps are 0.74, 1.02, 1.29, 1.56, 1.84, 2.11, 2.39, 2.66 and 2.93 kW. Winter months (January-March, November-December) are orange across nearly all hours; the rest of the year is predominantly deep blue, with almost no summer afternoon orange pocket, i.e. a much weaker cooling signature than the ET accounts.

[→ See original PDF page 12 for visual rendering]

### 3.3 WEATHER DATA

Using a zip-to-weather-station map provided by EMT, DSA assigned every account in our analysis to a nearby weather station. Figure 9 visualizes the mapping (note the dots with black outlines represent the weather stations). For each weather station, we downloaded historical weather data covering 2022-2025 and also typical meteorological year (TMY3) data. The historical weather data is used to

<!-- PDF page 13 (printed Page | 13) -->

understand the relationship between consumption and weather. The TMY3 data is used to weather-normalize our results (i.e., show what the impacts would look like in a "normal" weather year).

**Figure 9: Weather Mapping**

[DIAGRAM DESCRIPTION: Figure 9: Weather Mapping]

A map of Maine (with parts of New Hampshire, Quebec and New Brunswick visible at the edges) with towns shaded in thirteen colors, each color assigned to the weather station used for accounts in that area; weather stations are marked by dots with black outlines. Legend (13 stations): AUBURN-LEWISTON; AUGUSTA AIRPORT; BANGOR INTERNATIONAL AP; BAR HARBOR (AWOS); BERLIN MUNICIPAL; LEBANON MUNICIPAL; MILLINOCKET MUNICIPAL AP; PEASE INTL TRADEPORT; PORTLAND INTL JETPORT; ROCKLAND/KNOX (AWOS); SANFORD MUNI (AWOS); WATERVILLE (AWOS); WISCASSET. The large northern and western area is assigned to Berlin Municipal (dark green); Bangor and Millinocket cover the east-central area; the other stations cover the coastal and southern parts of the state.

[→ See original PDF page 13 for visual rendering]

### 3.4 OTHER DATA

CMP provided several other data sets for the analysis. These data sets are described in Table 4.

**Table 4: Other Data Sources**

| Data                     | Description and Use                                                                                                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Enrollment data          | Shows the accounts enrolled on the ET and SHP rates and their rate transition dates. The rate transition dates were used to split the consumption data into "pre" and "post" periods.        |
| Low-income account flags | Flags designated low-income accounts; used as a matching dimension and to produce separate rate impact estimates for low income and market rate households.                                  |
| Interconnection data     | Identifies CMP premises with solar arrays that are connected to the grid. For interconnected premises, consumption data that follows the interconnection date was removed from the analysis. |

<!-- PDF page 14 (printed Page | 14) -->

## 4 METHODS

The primary challenge of the impact evaluation was to accurately detect changes in energy consumption attributable to the SHP or ET rate transition while systematically eliminating other plausible explanations for the changes. Figure 10 provides an overview of our evaluation approach.

Once a customer enrolls on one of the new rates, the rate is in place every day, and it is no longer possible to observe their behavior absent the new rate. Moreover, the adoption of one of these rates often occurs around the same time as the adoption of a new electric technology (heat pump, EV, etc.) that undoubtedly affects energy consumption. Thus, estimating energy and demand impacts associated with rate transition requires a control group of customers with the technologies who are not on the rate and, ideally, a year of pre-treatment and post-treatment data for both the participants and the control group. If the new rates lead to changes in energy use, we should observe a change in load patterns for customers who went on the new rates but no similar change for the control group.

Our load impacts for each rate were estimated by comparing outcomes for customers on the new rates with a matched control group using difference-in-differences. In order of importance, we outline the key evaluation challenges in the bullets below and discuss how our methodology addresses them. Additional details are provided in subsequent sections.

- **Confounding factors.** The adoption of heat pumps, heat pump water heaters, and electric vehicles may occur around the same time as enrollment in the SHP and ET rates, making it difficult to disentangle the rate impacts from the technology impacts. Our approach was to identify participants that had the qualifying technology a year before (and after) enrolling on the new rate, so the only change in the analysis period is enrollment onto the rate.
- **Identifying an appropriate control pool.** A good control has nearly identical characteristics and energy usage patterns before the intervention in question (the new rate) goes into effect. Ideally, the control group customers have the same technology (e.g., EVs, heat pumps, heat pump water heaters), are in the same geographic area, and have similar usage patterns as participants before the participant enrolled on the new rate. Our approach emphasizes identifying a high-quality, matched control group and estimating load impacts using difference-in-differences.
- **Comparable periods and balanced datasets.** While difference-in-differences is a powerful technique, it can err when the data is imbalanced (i.e., due to rolling enrollments) and when energy use patterns diverge over time (i.e., the parallel trends assumption). In our analysis, we ensured that every participant's post-intervention period has a similar pre-intervention period, and that the matched control also has the corresponding time periods. In addition, we carefully checked that the treatment and control group energy use trends do not diverge prior to the intervention.

The difference-in-differences approach mentioned above can be used to produce accurate estimates of weather-normalized load impacts associated with enrollment in the SHP or ET rates.

<!-- PDF page 15 (printed Page | 15) -->

**Figure 10: Methodological Overview**

[DIAGRAM DESCRIPTION: Figure 10: Methodological Overview]

A vertical flowchart of seven numbered steps, each a colored box with a "STEP n" label on the left:

- **STEP 1** (light blue): "Identify control pool. These are sites with the qualifying technologies that are not on the ET or SHP rates. Efficiency Maine rebate data was used to identify these premises."
- **STEP 2** (salmon): "Remove sites with changes in EV, solar, heat pump, or heat pump water heater status within one year of rate transition."
- **STEP 3** (gray): "Narrow to sites with comparable pre and post data."
- **STEP 4** (dark blue): "Run a matched control group tournament." With four numbered sub-boxes beneath: 1 "Identify match control models (strata, methods, and variables)"; 2 "Pick match controls using each method"; 3 "Assess accuracy out of sample"; 4 "Identify best match control group and apply".
- **STEP 5** (green): "Estimate impacts using difference-in-differences. 1) Calculate directly (classic diff-in-diff) 2) Panel regression with fixed effects and time effects"
- **STEP 6** (lavender): "Develop a predictive model as a function of weather."
- **STEP 7** (light blue): "Produce hourly estimates of load impacts under typical weather conditions (TMY3)."

[→ See original PDF page 15 for visual rendering]

### 4.1 PREPARING THE INTERVAL DATA FOR ANALYSIS

In preparing the interval data for analysis, our goal is to isolate accounts where we expect that there is sufficient data for a pre/post comparison, there are no confounding load modifiers, and there are no data quality issues. Key steps in preparing the data include:

- Checking for zeroes, missing observations, and duplicates in hourly interval data. Days with missing observations or zero daily kWh are removed from the analysis.
- Create visualizations of average daily loads and the relationship between consumption and temperature to identify potential issues (like the summaries in Section 3.2).
- Review the distribution of account-level annual consumption (pre-enrollment and post-enrollment) and flag potential outliers.

<!-- PDF page 16 (printed Page | 16) -->

- Review consumption patterns for homes that generate their own electricity (via solar panels)
- Merge in rate enrollment dates and technology adoption dates; remove accounts with insufficient data for the analysis or with confounding technology installations.

Table 5 shows the number of accounts we removed from our analysis while reviewing and preparing the analysis dataset. For the ET analysis, our final analysis dataset included 1,795 ET accounts. For the SHP analysis, our final analysis dataset included 1,770 SHP accounts. (Due to the timing of the analyses, we had less post-transition data for the ET accounts. Thus, many more ET accounts were filtered out by the "insufficient data" flag.) Figure 11 shows the distribution of weather-normalized pre- and post-enrollment consumption (left panel) and the distribution of pre/post differences (right panel) for the 1,795 ET accounts, and Figure 12 shows the same distributions for the 1,770 SHP accounts. Both panels suggest annual kWh consumption was similar in the pre-enrollment and post-enrollment periods.

**Table 5: Number of Accounts Removed from Analysis**

_(Column headers: the two right columns are grouped under "Number of Accounts Remaining".)_

| Filter                                                         | ET Accounts (Number of Accounts Remaining) | SHP Accounts (Number of Accounts Remaining) |
| -------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------- |
| **Total accounts with AMI**                                    | **5,002**                                  | **2,741**                                   |
| Insufficient pre- or post-enrollment data ( < 1 year)          | 2,668                                      | 2,362                                       |
| Confounding load modifying technology                          | 1,831                                      | 1,798                                       |
| High pre or post annual consumption ( > 40,000 kWh)            | 1,801                                      | 1,793                                       |
| Low pre or post annual consumption ( < 3,000 kWh)              | 1,798                                      | 1,776                                       |
| Significant change in post annual consumption (+/- 10,000 kWh) | 1,795                                      | 1,770                                       |
| **Total accounts after filtering**                             | **1,795**                                  | **1,770**                                   |

**Figure 11: Distribution of Account-Level Weather-Normalized Annual Consumption, ET Accounts**

[DIAGRAM DESCRIPTION: Figure 11: Distribution of Account-Level Weather-Normalized Annual Consumption, ET Accounts]

Two histograms. Left panel: x axis Annual kWh (0 to 40,000), y axis Percent (0 to 20). Filled blue bars show the pre-enrollment distribution and white outlined bars show post-enrollment; the two nearly coincide. The distribution is right-skewed with its tallest bars (roughly 17-19 percent per bin) at about 12,000-16,000 kWh and a long tail to 40,000 kWh. Right panel: x axis Pre/Post Difference (kWh) from -8,000 to 8,000, y axis Percent (0 to 25); a roughly symmetric, bell-shaped distribution centered near zero with the tallest bars (about 22-25 percent) just either side of zero. Legend: Pre-Enrollment (blue), Post-Enrollment (white outline).

[→ See original PDF page 16 for visual rendering]

<!-- PDF page 17 (printed Page | 17) -->

**Figure 12: Distribution of Account-Level Weather-Normalized Annual Consumption, SHP Accounts**

[DIAGRAM DESCRIPTION: Figure 12: Distribution of Account-Level Weather-Normalized Annual Consumption, SHP Accounts]

Same two-panel format as Figure 11 for SHP accounts. Left panel: right-skewed annual kWh distribution (0-40,000) with the tallest bars (roughly 15-17 percent per bin) at about 8,000-12,000 kWh, lower than for ET accounts; pre-enrollment (blue) and post-enrollment (outline) nearly coincide. Right panel: pre/post difference (-8,000 to 8,000 kWh), bell-shaped around zero with the tallest bars (about 25-27 percent) adjacent to zero. Legend: Pre-Enrollment, Post-Enrollment.

[→ See original PDF page 17 for visual rendering]

### 4.2 REMOVING ACCOUNTS WITH CONFOUNDING ISSUES

The adoption of heat pumps, EVs, and other electric technologies may occur around the same time as enrollment in the ET or SHP rate. In such cases, it is difficult to separate the rate impact from the technology impact. Thus, our evaluation approach is to isolate participants that had the qualifying technology a year before and after enrolling on the ET or SHP rate, so the only change in the analysis period is enrollment onto the rate. Accounts with confounding load modifiers were removed from the analysis. Figure 13 shows an example of a home that was removed due to a confounding issue. Overnight demand patterns at this home abruptly change in June of 2023. The load pattern afterwards is consistent with what we'd expect for a home with an EV charger. This home enrolled on the ET rate in August 2023, two months after the installation of the EV charger. Comparing the pre-enrollment period with the post-enrollment period for this account would provide a biased estimate of the rate impact.

**Figure 13: Confounding EV Example**

[DIAGRAM DESCRIPTION: Figure 13: Confounding EV Example]

A time-series chart of Maximum Overnight Demand (kW, y axis 0-15) against date (x axis, 01/01/2022 to 07/01/2024 and beyond). A solid blue line labeled "Pre EV" runs from January 2022 to about June 2023 at roughly 1-3 kW with occasional spikes to about 5 kW. After about June 2023 a dashed gray line labeled "Post EV" shows frequent sharp spikes to about 10-13 kW (the EV charging signature) on top of a baseline of about 2-3 kW. A vertical dotted black line (about August 2023) marks the enrollment date. Printed note on the figure: "The black reference line represents when this account enrolled on the ET rate." Legend: Pre EV, Post EV.

[→ See original PDF page 17 for visual rendering]

<!-- PDF page 18 (printed Page | 18) -->

To identify homes with confounding load modifier issues, we used participation dates from the EMT rebate data and AMI detection algorithms. The EV detection algorithms looked specifically for changes in overnight consumption patterns like the one shown in Figure 13. We also looked for changes in winter loads to help identify homes that converted from fossil fuel heating to heat pumps (or some other form of electric heating) during the analysis period. Figure 14 shows a confounding heat pump example. This home transitioned onto the SHP rate in December 2023 but installed a heat pump a few months prior to the rate transition. A simple pre/post analysis for this home would attribute the heat pump impact to the rate transition.

**Figure 14: Confounding Heat Pump Example**

[DIAGRAM DESCRIPTION: Figure 14: Confounding Heat Pump Example]

A time-series chart of Average Daily kWh (y axis 0-90) against date (01/01/2022 to 07/01/2025). A solid blue line labeled "Pre Heat Pump" runs from January 2022 to about late 2023 at a steady roughly 10-25 kWh/day with no strong seasonal swing. After roughly late 2023 a dashed gray line labeled "Post Heat Pump" shows a pronounced winter peak (up to about 80-90 kWh/day in early 2024), a summer trough of about 10-15 kWh/day, and another winter peak of about 80 kWh/day in early 2025. A vertical dotted black line near 01/01/2024 marks the SHP enrollment date. Printed note: "The black reference line represents when this account enrolled on the SHP rate." Legend: Pre Heat Pump, Post Heat Pump.

[→ See original PDF page 18 for visual rendering]

### 4.3 DEVELOPING THE MATCHED COMPARISON GROUP

Our analysis methodology relies on the use of a matched comparison group of homes that are on the standard residential rate (Rate A) but have electric technologies like heat pumps, heat pump water heaters, or electric vehicles. The comparison group helps account for exogenous factors that could affect energy consumption, like variation in supply rates and return-to-office mandates. If enrolling in the ET or SHP rate leads to changes in energy use, we should observe a change in load patterns for customers who went on these rates but no similar change for the matched comparison group.

To develop the matched comparison group, CMP provided DSA with approximately three years of interval data for a control pool of approximately 12,000 accounts. From there, our goal was to match each ET and SHP account with one control pool account based on variables like:

- Weather-normalized annual consumption (pre-enrollment) or consumption bins
- Weather sensitivity of load or sensitivity bins
- Overnight demand (to identify homes with EVs)
- Average demand during ISO-NE summer and winter peak periods
- Geographic location
- Income group (low-income or not)

<!-- PDF page 19 (printed Page | 19) -->

Using different combinations of the variables noted above, we made 30 different matched comparison groups.[^2] To determine which combination of variables can produce the best matched comparison group, we assessed the performance of each of the 30 matching models using a false experiment. In essence, we ran the difference-in-differences model (discussed in Section 4.4) over a period when the rate intervention was not in effect. Thus, the right answer (zero impact) is known, and any deviation from zero is error. This allows us to assess the accuracy of the matching models and identify the one that is most accurate and unbiased. Figure 15 illustrates this approach for three hypothetical matching models. The right panel shows the "best" match in this illustrative example.

**Figure 15: Hypothetical False Experiment Results**

[DIAGRAM DESCRIPTION: Figure 15: Hypothetical False Experiment Results]

Three side-by-side panels titled "Poor Match", "Better Match" and "Best Match". Each plots Average Daily Consumption (kWh, y axis 0-80) against Date (x axis, early December to early January, ticks 12/03, 12/10, 12/17, 12/24, 01/01) for a Treatment Group (solid blue line) and a Control Group (dashed gray line), with orange bars along the bottom labeled "Error" showing the difference between them. In "Poor Match" the control line sits well below the treatment line and the orange error bars are large (roughly 5-20 kWh). In "Better Match" the lines track more closely and the error bars are smaller and straddle zero. In "Best Match" the two lines nearly coincide and the error bars are close to zero. Legend: Treatment Group, Control Group, Error.

[→ See original PDF page 19 for visual rendering]

### 4.4 MODELING METHODS

Using a difference-in-differences approach, we estimated energy impacts of the ET and SHP rate transition for each day of the year. To do this, we calculate:

**Equation (difference-in-differences):**

$$(\text{Enrolled Cust. } kWh_{Post} - \text{Enrolled Cust. } kWh_{Pre}) - (\text{Control } kWh_{Post} - \text{Control } kWh_{Pre})$$

where:

- The first difference is the pre/post change in usage for customers enrolled in the ET or SHP rate
- The second difference is the pre/post change in usage for customers in the comparison group
- Taking the difference of the two yields the daily energy impact, net of any changes observed for control group customers.

[^2]: In each group, matches were selected based on different criteria. As an example, the criteria for one of the groups was similar annual consumption and identical geography. The criteria for another was similar annual consumption, similar overnight demand, and identical income group.

<!-- PDF page 20 (printed Page | 20) -->

For robustness, will also developed difference-in-differences impact estimates from a time and fixed effects difference-in-differences regression model. The model specification is as follows:

**Equation (panel regression):**

$$kWh_{i,t} = \alpha_i + \beta_1 Post_{i,t} + \beta_2 Treatment_i + \beta_3 Treatment_i * Post_t + \varepsilon_i + v_i + w_t$$

where:

- $i$ represents individual accounts
- $t$ represents each time period
- $\beta_1$ represents the pre/post change in usage common to both groups
- $\beta_2$ is the pre-existing difference between the treatment and control group. In practice, this parameter is omitted when individual fixed effects are included.
- $\beta_3$ is the difference-in-differences estimate. It is the net impact after accounting for pre-existing differences between treatment and control group customers and for common differences between the pre and post periods.
- $v_i$ are individual fixed effects. These control for time-invariant unobserved customer characteristics.
- $W_t$ are time effects. These control for unobserved time effects that are common across individual customers.

Other explanatory variables, such as weather, can also be included in the model specification to reduce noise in the estimates, but the control group's usage and the use of time-effects should largely account for weather already.

_Extractor note (not source text): the source prints the time-effects term as lowercase $w_t$ in the equation and as capital $W_t$ in the bullet list; both are kept as printed._

### 4.5 WEATHER-NORMALIZING THE RESULTS

Our process to estimate weather-normalized impacts is straightforward:

1. Using the difference-in-differences approach outlined in Section 4.4, estimate daily impacts for each day of the year.
2. Develop a predictive model to estimate impacts as function of weather, day of year, and other relevant characteristics.
3. Use the model to estimate daily impacts under TMY3 conditions. The results can then be aggregated to the month, season, or year level.

<!-- PDF page 21 (printed Page | 21) -->

## 5 RESULTS

Table 6 shows key findings from our analysis. In short, we did not find significant post-transition changes in energy or demand for the ET accounts. For the SHP accounts, changes in annual energy use and heating season energy use were statistically significant but relatively small (p-value = 0.01 for annual, p-value = 0.01 for heating season). Though we attempted to isolate homes where no major load modifiers were installed within one year of rate transition, it's possible that the change in electric consumption we see for the SHP group could be explained by load modifiers we are not aware of (e.g., installing additional supplemental heat pumps or electrifying their domestic hot water system). Subsequent sections highlight additional findings from our analysis. Findings for the ET rate are in Section 5.1, and findings for the SHP rate are in Section 5.2.

**Table 6: High Level Findings**

| Rate            | Metric                         | Impact | 95% Confidence Interval | Percent Impact (%) |
| --------------- | ------------------------------ | ------ | ----------------------- | ------------------ |
| ET (n = 1,795)  | Annual Energy (kWh/yr)         | -16    | -143, 111               | -0.1%              |
| ET (n = 1,795)  | Summer Peak Demand (kW)        | -0.00  | -0.03, 0.02             | 0.0%               |
| ET (n = 1,795)  | Winter Peak Demand (kW)        | -0.04  | -0.08, 0.01             | -1.5%              |
| SHP (n = 1,770) | Annual Energy (kWh/yr)         | +145   | 44, 272                 | +1.3%              |
| SHP (n = 1,770) | Heating Season Energy (kWh/yr) | +114   | 27, 201                 | +1.4%              |
| SHP (n = 1,770) | Cooling Season Energy (kWh/yr) | +44    | -7, 94                  | +1.1%              |
| SHP (n = 1,770) | Winter Peak Demand (kW)        | +0.02  | -0.01, 0.05             | +0.9%              |
| SHP (n = 1,770) | Summer Peak Demand (kW)        | +0.01  | -0.01, 0.03             | +1.1%              |

_Extractor note (not source text): cross-check against Tables 7 and 11. The ET annual figure (-16) equals Table 7's weather-normalized ("Normal") value, whereas the SHP annual figure (+145) equals Table 11's DID value; Table 11's weather-normalized annual value is +158 (and the Conclusion on PDF page 40 cites 158 kWh). [source discrepancy: Table 6 mixes DID and weather-normalized estimates for the annual-energy rows.]_

### 5.1 ELECTRIC TECHNOLOGY RATE

#### 5.1.1 KEY FINDINGS

Table 7 shows difference-in-difference results, weather-normalized impact estimates, and percent impacts. The first line shows the overall energy impact, the next two show energy impacts by income group, and the final two rows show average demand impacts during the ISO-NE summer and winter peak periods. Notably, we did not detect any statistically significant changes in energy consumption after rate enrollment. The impact estimate for the low-income group is large relative to the other impacts but note the estimate only represents about 0.3% of annual energy consumption and only ~100 of the 1,795 ET accounts in the analysis were low income (i.e., the low-income results are based on a relatively small sample).

<!-- PDF page 22 (printed Page | 22) -->

**Table 7: Impact Estimates, ET Analysis**

_Structure: columns are Metric; # of Accts; Participants (Pre, Post); Controls (Pre, Post); Impact (DID, Normal = weather-normalized, %, 95% CI). Kilowatt-hour rows are annual kWh per account; kW rows are average demand in the ISO-NE peak window._

| Metric                  | # of Accts | Participants Pre | Participants Post | Controls Pre | Controls Post | Impact DID | Impact Normal | Impact % | 95% CI      |
| ----------------------- | ---------- | ---------------- | ----------------- | ------------ | ------------- | ---------- | ------------- | -------- | ----------- |
| Annual kWh              | 1,795      | 15,013           | 15,039            | 14,994       | 15,032        | -9         | -16           | -0.1%    | -143, 111   |
| Annual kWh, Market Rate | 1,692      | 15,045           | 15,053            | 15,045       | 15,070        | -14        | -20           | -0.1%    | -154, 114   |
| Annual kWh, Low Income  | 103        | 14,447           | 14,774            | 14,122       | 14,377        | +80        | +50           | 0.3%     | -518, 618   |
| Average kW, Summer Peak | 1,795      | 1.76             | 1.73              | 1.70         | 1.68          | -0.01      | -0.00         | -0.0%    | -0.03, 0.02 |
| Average kW, Winter Peak | 1,795      | 2.61             | 2.56              | 2.60         | 2.57          | -0.02      | -0.04         | -1.5%    | -0.08, 0.01 |

Table 8 shows energy impacts by time period. It is interesting that the seasonal estimates point in opposite directions, but the impacts in the table are not statistically significant (i.e., they do not meaningfully differ from zero).

**Table 8: Energy Impacts by Time Period, ET Analysis**

| Category | Subcategory | DID Impact (kWh) | Weather-Normalized Impact (kWh) | 95% Confidence Interval | Percent Impact (%) |
| -------- | ----------- | ---------------- | ------------------------------- | ----------------------- | ------------------ |
| Month    | January     | -13.0            | -6.2                            | -27.6, 15.2             | -0.4%              |
| Month    | February    | +0.7             | -5.8                            | -26.7, 15.1             | -0.4%              |
| Month    | March       | +15.1            | -3.9                            | -25.2, 17.4             | -0.3%              |
| Month    | April       | +1.4             | -1.9                            | -20.1, 16.3             | -0.2%              |
| Month    | May         | -0.6             | 0.1                             | -16.4, 16.6             | 0.0%               |
| Month    | June        | +8.3             | 2.2                             | -15.1, 19.5             | 0.2%               |
| Month    | July        | +7.7             | 3.6                             | -15.0, 22.2             | 0.3%               |
| Month    | August      | -17.9            | 2.6                             | -16.5, 21.7             | 0.2%               |
| Month    | September   | -3.0             | 1.4                             | -15.3, 18.1             | 0.1%               |
| Month    | October     | +9.7             | -1.0                            | -18.3, 16.3             | -0.1%              |
| Month    | November    | -5.7             | -2.8                            | -23.2, 17.6             | -0.2%              |
| Month    | December    | -11.2            | -4.8                            | -26.4, 16.8             | -0.3%              |
| Season   | Cooling     | +4.2             | +8.9                            | -62.8, 80.6             | 0.1%               |
| Season   | Heating     | -12.8            | -25.4                           | -108.6, 57.8            | -0.3%              |

#### 5.1.2 MATCHED COMPARISON GROUP

Our best matching model for the ET analysis had three matching dimensions: income group, weather-normalized annual consumption (pre-enrollment), and average daily non-weather-dependent consumption. Income group was treated as a "hard" match dimension, meaning that low-income ET accounts could only be matched to low-income accounts in the control pool and market rate accounts

<!-- PDF page 23 (printed Page | 23) -->

could only be matched to other market rate accounts. The other two dimensions were "soft" match dimensions, meaning we required similar values rather than exact matches. Figure 16 visualizes average daily consumption in the participant and matched comparison groups over a period with a sufficient number of pre-enrollment observations. Average daily consumption for the ET group and the best comparison group show strong alignment.

**Figure 16: Average Daily Consumption Time Series, Pre-Enrollment**

[DIAGRAM DESCRIPTION: Figure 16: Average Daily Consumption Time Series, Pre-Enrollment]

A time-series chart of Average Daily kWh (Pre-Rate) (y axis 20-70) against date (x axis 01/01/22 to 05/01/23). A solid blue line ("Matched Comparison Accounts") and a dashed gray line ("ET Accounts") overlap almost exactly, tracing high winter loads (about 55-60 kWh/day in early 2022), a summer trough of about 28-35 kWh/day, and a rise to 55-63 kWh/day from about November 2022 through early 2023. Printed note: "The figure reflects pre-enrollment consumption. Due to rolling enrollment, the number of accounts still in the 'pre' period varies by date. Only days with at least 700 accounts still in the 'pre' period are plotted."

[→ See original PDF page 23 for visual rendering]

Figure 17 and Figure 18 provide additional comparisons between the ET account group and the matched comparison group. The former shows the distribution of weather-normalized annual consumption for homes on the ET rate (pre-enrollment) and for homes in the matched comparison group. The latter shows how average daily consumption varies by average daily temperature in each group and in each period (pre-enrollment and post-enrollment). Like with Figure 16, Figure 17 and Figure 18 show strong alignment between the participant group and the matched comparison group.

<!-- PDF page 24 (printed Page | 24) -->

**Figure 17: Distribution of Weather-Normalized Annual Consumption, Pre-Enrollment**

[DIAGRAM DESCRIPTION: Figure 17: Distribution of Weather-Normalized Annual Consumption, Pre-Enrollment]

A histogram with x axis Weather-Normalized Annual Consumption (Pre-Rate) from 0 to 40,000 kWh and y axis Percent (0-10). Filled blue bars ("Matched Comparison Accounts") are overlaid with white-outlined bars ("ET Accounts"); the two distributions nearly coincide. Right-skewed, with the tallest bars (about 9-10 percent per bin) at roughly 12,000-16,000 kWh and a long right tail.

[→ See original PDF page 24 for visual rendering]

**Figure 18: Average Daily kWh by Average Daily Temperature**

[DIAGRAM DESCRIPTION: Figure 18: Average Daily kWh by Average Daily Temperature]

Two side-by-side scatter plots titled "Electric Technology Accounts" and "Matched Comparison Accounts". Each plots Average Daily kWh (y axis, about 20-80) against Average Daily Temperature (F) (x axis 0-90). Points form a U-shaped (check-mark) curve in both panels: about 55-60 kWh/day at 10-20 F, falling to a minimum of about 31-32 kWh/day near 55-60 F, and rising to about 45-50 kWh/day near 80 F. Pre-enrollment and post-enrollment points are colored differently (legend: Pre, Post) and overlap closely; the two panels are nearly identical. Printed note: "Circle size is proportional to the frequency of days at that temperature."

[→ See original PDF page 24 for visual rendering]

Figure 19 compares average demand during the ISO-NE summer and winter peak periods for the ET accounts and matched comparison accounts. The blue boxes represent the ET accounts and gray the gray boxes represent the matched comparison accounts. Within each period, the distribution of average demand is very similar between the two groups, again suggesting there is strong alignment between the ET accounts and the matched comparison group.

<!-- PDF page 25 (printed Page | 25) -->

**Figure 19: Distribution of Average Demand during the ISO-NE Peak Periods**

[DIAGRAM DESCRIPTION: Figure 19: Distribution of Average Demand during the ISO-NE Peak Periods]

Horizontal box-and-whisker plots of Average Demand (kW, x axis 0-5) for two periods, "Summer Peak" (top) and "Winter Peak" (bottom), each with one blue and one gray box. Summer peak: boxes span roughly 1.2 to 2.1-2.2 kW with medians around 1.55-1.6 kW and whiskers from near 0 to about 3.5-3.7 kW. Winter peak: boxes span roughly 1.9 to 3.1 kW with medians around 2.45 kW and whiskers from about 0.6 to about 4.9-5.0 kW. The pairs of boxes are nearly identical in each period. Legend: blue = "Matched Comparison Accounts", gray = "ET Accounts". Printed note: "The ISO-NE summer and winter peak definitions are used."

_Extractor note (not source text): [source discrepancy: the sentence before this figure (PDF page 24) says the blue boxes are the ET accounts and the gray boxes the matched comparison accounts, but the figure legend assigns blue to "Matched Comparison Accounts" and gray to "ET Accounts".]_

[→ See original PDF page 25 for visual rendering]

#### 5.1.3 DIFFERENCE-IN-DIFFERENCES RESULTS

Figure 20 shows the difference-in-difference results for energy. The left panel of the figure shows average daily consumption for the participant and matched comparison groups during the pre-enrollment period. The orange bars represent the difference. The middle panel shows average daily consumption for the two groups during the post-enrollment period. Finally, the right panel shows the net impact, which is the pre/post difference in participant loads net of any consumption changes observed in the matched comparison group. The net impacts of rate transition (orange bars in the right figure) mostly hover around zero.

**Figure 20: ET DID Results – Energy Impacts**

[DIAGRAM DESCRIPTION: Figure 20: ET DID Results – Energy Impacts]

Three panels titled "Pre Enrollment", "Post Enrollment" and "Net Impact", each plotting Average Daily kWh (y axis 0-60+) against Date (01/01 to 01/01, one year). In the Pre and Post panels, a participant usage line and a control usage line overlap (seasonal pattern: about 55-60 kWh/day in winter, about 30 kWh/day in summer) and orange bars show the treat-minus-control difference, which is small (a few kWh/day at most). In the Net Impact panel, the participant post-usage line and the "Baseline with DID Adjustment" line overlap and the orange "Load Impact (Diff-in-Diff)" bars hover around zero. Legends: Participant Pre Usage / Control Pre Usage / Difference (Treat-Control); Participant Post Usage / Control Post Usage / Difference (Treat-Control); Participant Post Usage / Baseline with DID Adjustment / Load Impact (Diff-in-Diff).

[→ See original PDF page 25 for visual rendering]

Figure 21 and Figure 22 show results for demand. Figure 21 specifically isolates demand during the ISO-NE winter peak period and Figure 22 isolates demand during the ISO-NE summer peak period. Like

<!-- PDF page 26 (printed Page | 26) -->

with energy, demand impacts during the summer and winter peak demand periods do not differ meaningfully from zero.

**Figure 21: ET DID Results – Demand Impacts during the Winter Peak Period**

[DIAGRAM DESCRIPTION: Figure 21: ET DID Results – Demand Impacts during the Winter Peak Period]

Three panels (Pre Enrollment, Post Enrollment, Net Impact) of Average kW (5-7 PM) (y axis 0.0-4.0) against Date (12/02, 12/16, 01/01, 01/15, 01/29). Participant and control demand lines overlap at roughly 2-3.3 kW with day-to-day swings; orange bars of the treat-minus-control difference (or the DID load impact in the right panel) stay close to zero. Legends as in Figure 20 (with "Demand").

[→ See original PDF page 26 for visual rendering]

**Figure 22: ET DID Results – Demand Impacts during the Summer Peak Period**

[DIAGRAM DESCRIPTION: Figure 22: ET DID Results – Demand Impacts during the Summer Peak Period]

Three panels (Pre Enrollment, Post Enrollment, Net Impact) of Average kW (1-5 PM) (y axis 0.0-2.5) against Date (06/01, 07/01, 08/01, 09/01). Participant and control demand lines overlap at roughly 1.3-2.3 kW; orange bars at the bottom (treat-minus-control difference; DID impact in the right panel) are small, up to about 0.1-0.2 kW in the pre/post panels and near zero in the net-impact panel.

[→ See original PDF page 26 for visual rendering]

#### 5.1.4 WEATHER-NORMALIZING

The weather-normalized results (shown in the last column of Table 7) hardly differed from the difference-in-difference results. This is because (1) rate participants and the matched comparison accounts experienced identical weather conditions, (2) the two groups had similar weather-dependent consumption patterns, and (3) the ET rate does not have a seasonal component (like the SHP rate). The result was that the daily difference-in-difference estimates displayed little correlation with weather.

Figure 23 visualizes the relationship between these two variables. The daily impact estimates decrease marginally at low temperatures, increase marginally at high temperatures, and hover around zero in the

<!-- PDF page 27 (printed Page | 27) -->

shoulder season. Casting this relationship over a typical weather year produces the impact distribution shown in Figure 24. In this figure, impacts that are less than zero represent load reductions in the ET group, and impacts that are greater than zero represent load increases.

**Figure 23: Daily DID Estimates against Temperature, ET Analysis**

[DIAGRAM DESCRIPTION: Figure 23: Daily DID Estimates against Temperature, ET Analysis]

A scatter plot of Daily Load Impact (kWh, y axis -2 to 2) against Participant-Weighted Average Temperature (F) (x axis 10-80), with about 300 hollow blue circles (one per day of year). Points scatter around zero; below roughly 30 F more points fall below zero (down to about -1.5 kWh), and above roughly 65 F more points fall above zero (up to about +2 kWh); between 30 and 60 F the points hover around 0 to +1.

[→ See original PDF page 27 for visual rendering]

**Figure 24: Weather-Normalized Daily Impacts, ET Analysis**

[DIAGRAM DESCRIPTION: Figure 24: Weather-Normalized Daily Impacts, ET Analysis]

A bar chart of Daily Impact (kWh, y axis -0.2 to 0.2) by Day of Year (x axis 01/01 to 12/31). Blue bars are negative (load reductions of roughly -0.05 to -0.22 kWh/day) from January through about late April and again from about November through December, and positive (roughly +0.05 to +0.15 kWh/day) from about May through October, peaking in July-August.

[→ See original PDF page 27 for visual rendering]

#### 5.1.5 BILL SAVINGS

In addition to estimating the energy and demand impacts of rate transition, we also estimated bill impacts to understand the financial impact of rate transition. We used two approaches for the bill impact calculation:

- **Shadow bill approach.** Under the shadow bill approach, we answer the question: relative to what they would have paid on rate A for the same amount of energy (delivery only), how much more/less did customers pay during their first year on the ET rate? This approach only examines

<!-- PDF page 28 (printed Page | 28) -->

the post-transition period and ignores changes in consumption patterns across the pre and post periods.

- **Difference-in-difference approach.** This approach mimics the energy and demand impact calculations. We isolate the year before and after the rate transition, perform the rate algebra, then we find (1) the pre/post difference in bills for the ET rate group, (2) the pre/post difference in bills for the matched comparison group, and (3) the difference of these two differences. Unlike the shadow bill approach, this approach does not ignore changes in consumption patterns.

The benefit to the DID approach is that it accounts for pre/post changes in consumption patterns. The benefit to the shadow bill approach is that more accounts can be included (since we do not have to remove accounts with confounding load modifiers). Results are shown in Table 9 and additional details are provided in subsequent sections. At a high level, the two approaches produced directionally similar conclusions: accounts that switched to the ET rate saved upwards of $200, on average, during their first year on the rate.

Note that the results presented in this section use the versions of the ET rate and Rate A that were in place at the time (see Table 2). The service and volumetric charges for both Rate A and the ET rate have since increased.

**Table 9: Bill Impact Findings, ET Analysis**

| Approach                 | Number of Accounts Included | Estimated Bill Savings (First Year) |
| ------------------------ | --------------------------- | ----------------------------------- |
| Shadow Bills             | 4,963                       | $239                                |
| Difference-in-Difference | 1,795                       | $226                                |

##### 5.1.5.1 Shadow Bills

For ET accounts with at least one year of post-enrollment consumption data, DSA calculated customer bills (delivery only) under the ET rate design and under Rate A. To do so, we summed daily consumption by calendar month and performed the rate algebra. Relative to what they would have paid on Rate A for the same amount of energy, customers on the ET rate paid about $240 less during their first year on the ET rate, on average (excluding sales tax). On a percentage basis, this corresponds to about 10% of what they would have paid on Rate A. Figure 25 shows the distribution of first-year delivery savings by account. The majority of accounts fall to the right of zero, meaning the majority paid less for delivery in their first year than they would have paid on Rate A.

<!-- PDF page 29 (printed Page | 29) -->

**Figure 25: Distribution of Delivery Savings in First Year, ET Analysis**

[DIAGRAM DESCRIPTION: Figure 25: Distribution of Delivery Savings in First Year, ET Analysis]

A histogram with x axis Annual Delivery Savings ($) - First Year (-200 to 1,200) and y axis Percent (0-15). Right-skewed distribution: the tallest bar (about 14 percent) is at about 100-150 dollars, with other large bars at 150-250 dollars (about 12-13 percent) and a long right tail toward 1,000+ dollars; a small share of accounts fall below zero (bars near -200 to 0 are about 1-5 percent). Printed note: "The mean and median are $239/yr and $187/yr respectively."

[→ See original PDF page 29 for visual rendering]

Figure 26 shows how delivery savings varied by month. The variation here is tied to the seasonal nature of energy consumption. The white line in the middle of each box represents the median (or the 50th percentile). In February, for example, about 50% of accounts saved more than $25 and about 50% saved less than $25. The left and right sides of the box represent the 25th and 75th percentiles. The whiskers of the box extend to the minimum and maximum savings values (excluding outliers).

**Figure 26: Savings by Month, ET Analysis**

[DIAGRAM DESCRIPTION: Figure 26: Savings by Month, ET Analysis]

Twelve horizontal box-and-whisker plots (y axis Month, 1 at top to 12 at bottom) of Delivery Savings ($/Month) (x axis -25 to 100+). All twelve months are centered above zero. Medians are largest in winter (about $30-35 in January, about $25 in February, about $20 in March, about $20 in November, about $25 in December) and smallest in late spring and early fall (about $3-10 in May, June, August, September, October; about $12 in July). The January whisker extends to about $100 and the minimum whisker is about -$18 in every month. (Values read from chart, approximate.)

[→ See original PDF page 29 for visual rendering]

##### 5.1.5.2 Difference-in-Differences

While the shadow bill approach covered in the prior section focuses exclusively on post-transition bills, the DID approach accounts for any changes in electric consumption that may be attributable to rate transition. Results from the DID bill impact analysis are shown in Table 10. Participant bills were $223/year less, on average, in their first year on the ET rate compared to the year before rate transition.

<!-- PDF page 30 (printed Page | 30) -->

During the same time period, bills for accounts in the matched comparison group increased by $3 on average. Taking the difference of these differences produce an estimated $226 in savings during the first year on the ET rate. Recall that this analysis was performed using the rate structures that were in place at the time, not the current rate structures. Using the current rate structures would not materially change the conclusion, as the volumetric charges for both Rate A and the ET rate have increased by approximately the same amount.

**Table 10: DID Bill Savings, ET Analysis**

| Group                     | # of Accts | Average Annual Bill ($/year) Pre | Average Annual Bill ($/year) Post | Savings |
| ------------------------- | ---------- | -------------------------------- | --------------------------------- | ------- |
| Participants              | 1,795      | 1,847                            | 1,625                             | +223    |
| Controls                  | 1,795      | 1,846                            | 1,849                             | -3      |
| Difference-in-Differences |            |                                  |                                   | +226    |

_Extractor note (not source text): arithmetic check: 1,847 - 1,625 = 222 (printed +223, a rounding difference in the source); 223 - (-3) = 226, matching the printed DID value._

### 5.2 SEASONAL HEAT PUMP RATE

#### 5.2.1 KEY FINDINGS

Table 11 shows difference-in-difference results, weather-normalized impact estimates, percent impacts, and 95% confidence intervals for the weather-normalized impacts. The first line shows the overall energy impact, the next two show energy impacts by income group, the next two show energy impacts by season, and the final two rows show average demand impacts during the ISO-NE summer and winter peak periods. We detected a 1.3% increase in average annual consumption after rate transition (p-value = 0.01), with most of this increase occurring during the heating season. Our estimated heating season increase is 114 kWh per household (p-value = 0.01). One possible explanation for the relatively small response to the rate is that many of these homes may have supplemental heat pumps that were already being maxed out prior to rate transition rather than whole-home heat pumps that were being underutilized. In other words, the rate response is partially a function of heat pump utilization prior to rate transition.

In addition to the annual and heating season changes, we also detected an increase in cooling season loads but this increase was not statistically significant (p-value = 0.09). Although our analysis approach was to remove premises with major load modifier installations within one year of rate transition, it is possible that the pre/post change in electric consumption could be explained by load modifiers we are unaware of (e.g., an additional supplementary heat pump, converting domestic hot water from non-electric to electric) rather than behavioral changes among the SHP premises.

The annual impact estimate for the low-income group is large relative to the market rate group but only 45 of the 1,770 SHP accounts in the analysis were low income (i.e., the low-income results are based on a relatively small sample). Seasonal patterns for the low-income and market rate groups follow the overall seasonal patterns – most of the increase occurs during the heating season.

<!-- PDF page 31 (printed Page | 31) -->

**Table 11: Impact Estimates, SHP Analysis**

_Structure: same columns as Table 7 (Impact: DID, Normal = weather-normalized, %, 95% CI). The seasonal rows are labelled "Oct-Apr" and "May-Nov" in the table._

| Metric                  | # of Accts | Participants Pre | Participants Post | Controls Pre | Controls Post | Impact DID | Impact Normal | Impact % | 95% CI      |
| ----------------------- | ---------- | ---------------- | ----------------- | ------------ | ------------- | ---------- | ------------- | -------- | ----------- |
| Annual kWh              | 1,770      | 11,764           | 11,905            | 11,685       | 11,683        | +145       | +158          | +1.3%    | 44, 272     |
| Annual kWh, Market Rate | 1,725      | 11,820           | 11,957            | 11,738       | 11,739        | +136       | +151          | +1.3%    | 35, 267     |
| Annual kWh, Low Income  | 45         | 9,619            | 9,929             | 9,656        | 9,563         | +403       | +412          | +4.3%    | -178, 1,001 |
| Annual kWh, Oct-Apr     | 1,770      | 7,870            | 7,970             | 7,772        | 7,767         | +105       | +114          | +1.4%    | 27, 201     |
| Annual kWh, May-Nov     | 1,770      | 3,894            | 3,935             | 3,913        | 3,916         | +39        | +44           | +1.1%    | -7, 94      |
| Average kW, Summer Peak | 1,770      | 0.92             | 0.94              | 0.91         | 0.92          | +0.01      | +0.01         | +1.1%    | -0.01, 0.03 |
| Average kW, Winter Peak | 1,770      | 2.36             | 2.35              | 2.34         | 2.31          | +0.02      | +0.02         | +0.9%    | -0.01, 0.05 |

_Extractor note (not source text): [source discrepancy: the Table 11 row labels "Oct-Apr" and "May-Nov" do not match the SHP seasons used elsewhere in the report (heating = November 1 - April 30, cooling = May 1 - October 31, per Table 3 and the sentence under Table 11). The values (+114 kWh heating, +44 kWh cooling) match the heating-season and cooling-season rows of Tables 6 and 12.]_

Table 12 shows energy impacts by period. Note the last two rows (Cooling and Heating seasons) reflect the two SHP seasonal periods (heating includes November through April and cooling includes May through October).

**Table 12: Energy Impacts by Time Period, SHP Analysis**

| Category | Subcategory | DID Impact (kWh) | Weather-Normalized Impact (kWh) | 95% Confidence Interval | Percent Impact (%) |
| -------- | ----------- | ---------------- | ------------------------------- | ----------------------- | ------------------ |
| Month    | January     | +24.9            | +27.7                           | 2.7, 52.7               | 1.7%               |
| Month    | February    | +26.7            | +24.6                           | 1.1, 48.1               | 1.7%               |
| Month    | March       | +29.4            | +17.7                           | -4.3, 39.7              | 1.4%               |
| Month    | April       | +19.2            | +9.0                            | -6.6, 24.6              | 1.0%               |
| Month    | May         | +23.8            | +6.2                            | -5.6, 18.0              | 1.0%               |
| Month    | June        | +18.5            | +7.4                            | -3.8, 18.6              | 1.3%               |
| Month    | July        | +7.9             | +7.6                            | -5.2, 20.4              | 1.1%               |
| Month    | August      | +3.1             | +8.0                            | -5.1, 21.1              | 1.2%               |
| Month    | September   | -2.4             | +7.0                            | -4.0, 18.0              | 1.2%               |
| Month    | October     | -12.3            | +7.3                            | -6.6, 21.2              | 1.0%               |
| Month    | November    | -5.6             | +12.6                           | -8.8, 34.0              | 1.1%               |
| Month    | December    | +10.0            | +22.5                           | -0.9, 45.9              | 1.5%               |
| Season   | Cooling     | +38.5            | +43.5                           | -7.2, 94.2              | 1.1%               |
| Season   | Heating     | +104.5           | +114.1                          | 26.8, 201.4             | 1.4%               |

#### 5.2.2 MATCHED COMPARISON GROUP

Our best matching model for the SHP analysis had five matching dimensions: weather-normalized annual consumption, average daily non-weather-dependent consumption, cold weather sensitivity, 98th percentile of overnight demand, and average demand during the summer peak window. All five dimensions were "soft" matching dimensions, meaning SHP accounts were matched to control accounts with similar values rather than exact matches. All matching metrics were calculated using pre-enrollment consumption for the SHP accounts. Figure 27 visualizes average daily consumption for SHP accounts and the matched comparison groups over a period with a sufficient number of pre-enrollment observations. Average daily consumption for the two groups shows strong alignment.

<!-- PDF page 32 (printed Page | 32) -->

**Figure 27: Average Daily Consumption Time Series, Pre-Enrollment**

[DIAGRAM DESCRIPTION: Figure 27: Average Daily Consumption Time Series, Pre-Enrollment]

A time-series chart of Average Daily kWh (Pre-Rate) (y axis 10-70) against date (01/01/22 to 10/01/23). A solid blue line ("Matched Comparison Accounts") and a dashed gray line ("SHP Accounts") overlap closely: about 40-65 kWh/day in winter 2022, falling to about 18-25 kWh/day from about May to October 2022, rising to a peak of about 70 kWh/day in winter 2022-23, and falling back to about 18-25 kWh/day by about May 2023. Printed note: "The figure reflects pre-enrollment consumption. Due to rolling enrollment, the number of accounts still in the 'pre' period varies by date. Only days with at least 700 accounts still in the 'pre' period are plotted."

[→ See original PDF page 32 for visual rendering]

Figure 28 and Figure 29 provide additional comparisons between the SHP account group and the matched comparison group. The former shows the distribution of weather-normalized annual consumption for homes on the SHP rate (pre-enrollment) and for homes in the matched comparison group. The latter shows how average daily consumption varies by average daily temperature in each group and in each period (pre-enrollment and post-enrollment). Like with Figure 27, Figure 28 and Figure 29 show strong alignment between the participant group and the matched comparison group.

<!-- PDF page 33 (printed Page | 33) -->

**Figure 28: Distribution of Weather-Normalized Annual Consumption, Pre-Enrollment**

[DIAGRAM DESCRIPTION: Figure 28: Distribution of Weather-Normalized Annual Consumption, Pre-Enrollment]

A histogram with x axis Weather-Normalized Annual Consumption (Pre-Rate) from 0 to 40,000 kWh and y axis Percent (0-10). Filled blue bars ("Matched Comparison Accounts") overlaid with white-outlined bars ("SHP Accounts") nearly coincide. Right-skewed, with the tallest bars (about 8-9 percent per bin) at roughly 8,000-14,000 kWh and a long right tail.

[→ See original PDF page 33 for visual rendering]

**Figure 29: Average Daily kWh by Average Daily Temperature**

[DIAGRAM DESCRIPTION: Figure 29: Average Daily kWh by Average Daily Temperature]

Two side-by-side scatter plots titled "Matched Comparison Accounts" and "Seasonal Heat Pump Accounts", each plotting Average Daily kWh (y axis about 10-70) against Average Daily Temperature (F) (x axis 0-90). Both show a U-shaped curve: about 60-65 kWh/day at 5-15 F, falling to a minimum of about 18-20 kWh/day near 60-65 F, and rising slightly to about 26-27 kWh/day near 80 F. Pre- and post-enrollment points (legend: Pre, Post) overlap; the two panels are nearly identical. Printed note: "Circle size is proportional to the frequency of days at that temperature."

[→ See original PDF page 33 for visual rendering]

Figure 30 compares average demand during the ISO-NE summer and winter peak periods for the SHP accounts and matched comparison accounts. The blue boxes represent the SHP accounts and gray the gray boxes represent the matched comparison accounts. Within each period, the distribution of average demand is very similar between the two groups, again suggesting there is strong alignment between the SHP accounts and the matched comparison group.

<!-- PDF page 34 (printed Page | 34) -->

**Figure 30: Distribution of Average Demand during the ISO-NE Peak Periods**

[DIAGRAM DESCRIPTION: Figure 30: Distribution of Average Demand during the ISO-NE Peak Periods]

Horizontal box-and-whisker plots of Average Demand (kW, x axis 0-5) for "Summer Peak" (top) and "Winter Peak" (bottom), each with one blue and one gray box. Summer peak: boxes span roughly 0.6 to 1.25 kW with medians around 0.9 kW and whiskers from near 0 to about 2.2 kW. Winter peak: boxes span roughly 1.6 to 2.9 kW with medians around 2.15-2.2 kW and whiskers from about 0 (blue) or 0.3 (gray) to about 4.7-5.0 kW. Legend: blue = "Matched Comparison Accounts", gray = "SHP Accounts". Printed note: "The ISO-NE summer and winter peak definitions are used."

_Extractor note (not source text): [source discrepancy: as with Figure 19, the sentence before this figure (PDF page 33) says the blue boxes are the SHP accounts and the gray boxes the matched comparison accounts, but the figure legend assigns blue to "Matched Comparison Accounts" and gray to "SHP Accounts".]_

[→ See original PDF page 34 for visual rendering]

#### 5.2.3 DIFFERENCE-IN-DIFFERENCES RESULTS

Figure 31 shows the difference-in-difference results for energy. The left panel of the figure shows average daily consumption for the participant and matched comparison groups during the pre-enrollment period. The orange bars represent the difference. The middle panel shows average daily consumption for the two groups during the post-enrollment period. Finally, the right panel shows the net impact, which is the pre/post difference in participant loads net of any consumption changes observed in the matched comparison group. The net impacts of rate transition (orange bars in the right panel) are generally small but tend to be larger in the winter months than in the summer months.

**Figure 31: SHP DID Results – Energy Impacts**

[DIAGRAM DESCRIPTION: Figure 31: SHP DID Results – Energy Impacts]

Three panels titled "Pre Enrollment", "Post Enrollment" and "Net Impact", each plotting Average Daily kWh (y axis 0-60+) against Date (01/01 to 01/01). Usage lines show the strong SHP seasonal pattern (about 55-62 kWh/day in winter, about 18-25 kWh/day in summer). Two vertical dashed black lines near 04/01-05/01 and 10/01-11/01 separate the heating and cooling seasons. Orange bars at the bottom show the treat-minus-control difference (pre and post panels) and the DID load impact (net panel); they are small, slightly larger in winter than in summer. Legends as in Figure 20.

[→ See original PDF page 34 for visual rendering]

<!-- PDF page 35 (printed Page | 35) -->

Figure 32 and Figure 33 show results for demand. Figure 32 specifically isolates demand during the ISO-NE winter peak period and Figure 33 isolates demand during the ISO-NE summer peak period. Demand impacts during the summer and winter peak demand periods do not differ meaningfully from zero.

**Figure 32: SHP DID Results – Demand Impacts during the Winter Peak Period**

[DIAGRAM DESCRIPTION: Figure 32: SHP DID Results – Demand Impacts during the Winter Peak Period]

Three panels (Pre Enrollment, Post Enrollment, Net Impact) of Average kW (5-7 PM) (y axis 0.0-3.0) against Date (12/02, 12/16, 01/01, 01/15, 01/29). Participant and control demand lines overlap at roughly 1.8-3.0 kW; orange bars (treat-minus-control difference; DID impact in the right panel) are small, with a few occasional bars up to about 0.2-0.3 kW.

[→ See original PDF page 35 for visual rendering]

**Figure 33: SHP DID Results – Demand Impacts during the Summer Peak Period**

[DIAGRAM DESCRIPTION: Figure 33: SHP DID Results – Demand Impacts during the Summer Peak Period]

Three panels (Pre Enrollment, Post Enrollment, Net Impact) of Average kW (1-5 PM) (y axis 0.0-1.5) against Date (06/01, 07/01, 08/01, 09/01). Participant and control demand lines overlap at roughly 0.7-1.2 kW; orange bars at the bottom are small (up to about 0.1 kW).

[→ See original PDF page 35 for visual rendering]

#### 5.2.4 WEATHER-NORMALIZING

Figure 34 shows the relationship between the daily difference-in-difference estimates and outdoor air temperature. Between 40°F and 75°F, the daily impacts tend to hover around zero and show little-to-no relationship with temperature. However, the daily impacts increase when average daily temperatures are under 40°F, indicating the SHP accounts use slightly more electricity than matched comparison accounts when it is cold outside. Casting this relationship over a typical weather year produces the impact distribution shown in Figure 35. The black reference lines in the figure separate the SHP cooling

<!-- PDF page 36 (printed Page | 36) -->

and heating seasons. During the heating season, SHP accounts show a load increase. There is also a load increase in the cooling season, but it is small relative to the load increase in the heating season. It's doubtful that SHP enrollees would increase their summer consumption in response to the rate, as the SHP summer delivery rate is more than double the standard residential delivery rate. One possible directional explanation for this result is that some premises started using their heat pumps for cooling in addition to heating after transitioning to the SHP rate. Regardless, the cooling season increase is not statistically significant.

**Figure 34: Daily DID Estimates against Temperature, SHP Analysis**

[DIAGRAM DESCRIPTION: Figure 34: Daily DID Estimates against Temperature, SHP Analysis]

A scatter plot of Daily Load Impact (kWh, y axis -2 to 2) against Participant-Weighted Average Temperature (F) (x axis 10-80) with about 300 hollow blue circles (one per day of year). Below roughly 40 F the points are mostly above zero (typically +0.3 to +1.5 kWh, a few up to about +2); between 40 and 75 F they scatter around 0 to +0.5 with a few below -1.

[→ See original PDF page 36 for visual rendering]

**Figure 35: Weather-Normalized Daily Impacts, SHP Analysis**

[DIAGRAM DESCRIPTION: Figure 35: Weather-Normalized Daily Impacts, SHP Analysis]

A bar chart of Daily Impact (kWh, y axis 0.00-1.25) by Day of Year (x axis 01/01 to 12/01). All bars are positive. Impacts are about 0.75-1.15 kWh/day from January through about February, decline through March-April to about 0.15-0.2 kWh/day by 05/01, hold at about 0.2-0.28 kWh/day from May through October, and rise again from about 11/01 to about 0.5-1.0 kWh/day in December. Two vertical dashed black lines at about 05/01 and 11/01 mark the heating/cooling season boundaries.

[→ See original PDF page 36 for visual rendering]

<!-- PDF page 37 (printed Page | 37) -->

#### 5.2.5 BILL SAVINGS

In addition to estimating the energy and demand impacts of rate transition, we also estimated bill impacts to understand the financial impact of rate transition. We used two approaches for the bill impact calculation:

- **Shadow bill approach.** Under the shadow bill approach, we answer the question: relative to what they would have paid on rate A for the same amount of energy (delivery only), how much more/less did customers pay during their first year on the SHP rate? This approach only examines the post-transition period and ignores changes in consumption patterns across the pre and post periods.
- **Difference-in-difference approach.** This approach mimics the energy and demand impact calculations. We isolate the year before and after the rate transition, perform the rate algebra, then we find (1) the pre/post difference in bills for the SHP rate group, (2) the pre/post difference in bills for the matched comparison group, and (3) the difference of these two differences. Unlike the shadow bill approach, this approach does not ignore changes in consumption patterns.

The benefit to the DID approach is that it accounts for pre/post changes in consumption patterns. The benefit to the shadow bill approach is that more accounts can be included (since we do not have to remove accounts with confounding load modifiers). Results are shown in Table 13 and additional details are provided in subsequent sections. At a high level, the two approaches produced directionally similar conclusions: accounts that switched to the SHP rate spent more money, on average, than they would have spent in a baseline scenario where they did not changed rates.

Note that the results presented in this section use the versions of the SHP rate and Rate A that were in place at the time (see Table 3). The service and volumetric charges for both Rate A and the SHP rate have since changed (see Table 14). The volumetric charge for Rate A increased, but the seasonal volumetric charges for the SHP rate decreased. The service charge for Rate A increased by about $3 per cycle, and the service charge for the SHP rate increased by less than one dollar per cycle. Using the current rate structures for this analysis paints a different picture. In this alternative scenario, the shadow bill approach results in estimated first-year savings (as opposed to an increase) of $251 and the DID approach results in estimated first-year savings of $184. The gulf between these numbers seems large, but the calculations are performed on different sets of customers (the DID approach isolates customers without confounding load modifiers).

**Table 13: Bill Impact Findings, SHP Analysis**

| Approach                 | Number of Accounts Included | Estimated Bill Savings (First Year) |
| ------------------------ | --------------------------- | ----------------------------------- |
| Shadow Bills             | 2,443                       | -$86                                |
| Difference-in-Difference | 1,770                       | -$132                               |

Note: Please see discussion in the prior paragraph regarding recent changes to the rates.

<!-- PDF page 38 (printed Page | 38) -->

**Table 14: SHP and Rate A Changes**

| Rate               | Charge               | Used in Analysis | As of 10/1/2025 | Difference |
| ------------------ | -------------------- | ---------------- | --------------- | ---------- |
| Rate A             | Service              | $26.60           | $29.88          | +$3.28     |
| Rate A             | Volumetric           | $0.108980        | $0.131239       | +$0.022    |
| Seasonal Heat Pump | Service              | $40.55           | $41.24          | +$0.69     |
| Seasonal Heat Pump | Volumetric (heating) | $0.011226        | $0.008244       | -$0.003    |
| Seasonal Heat Pump | Volumetric (cooling) | $0.278592        | $0.275610       | -$0.003    |

Note: The SHP rate does not include the first 50 kWh use in the Service Charge like Rate A does. It does include the first 750 kWh of usage sales-tax free.

_Extractor note (not source text): arithmetic check of the Difference column: 29.88 - 26.60 = 3.28; 0.131239 - 0.108980 = 0.022259; 41.24 - 40.55 = 0.69; 0.008244 - 0.011226 = -0.002982; 0.275610 - 0.278592 = -0.002982. All consistent with the printed values (rounded)._

##### 5.2.5.1 Shadow Bills

For SHP accounts with at least one year of post-enrollment consumption data, DSA calculated customer bills (delivery only) under the SHP rate design and under Rate A. To do so, we summed daily consumption by calendar month and performed the rate algebra. Relative to what they would have paid on Rate A for the same amount of energy, customers on the SHP rate paid about $90 more during their first year on the SHP rate, on average (excluding sales tax). Customers saved a substantial amount during the heating season ($720) but also spent considerably more in the cooling season ($810). Figure 36 shows the distribution of first-year delivery savings by account. The majority of accounts fall to the left of zero, meaning the majority paid more for delivery in their first year on SHP than they would have paid on Rate A for the same amount of energy. Recall that this analysis was performed using the rate structures that were in place at the time, not the current rate structures.

**Figure 36: Distribution of Delivery Savings in First Year, SHP Analysis**

[DIAGRAM DESCRIPTION: Figure 36: Distribution of Delivery Savings in First Year, SHP Analysis]

A histogram with x axis Annual Delivery Savings ($) - First Year (-1,200 to 1,200) and y axis Percent (0-8). Roughly bell-shaped and centered slightly left of zero: the tallest bars (about 7.5-8 percent) lie between about -150 and 0 dollars, with a long thin tail in both directions (to about -1,200 on the left and about +1,100 on the right). Printed note: "The mean and median are -$86/yr and -$90/yr respectively."

_Extractor note (not source text): the text above says customers "paid about $90 more" in the first year, while Table 13 prints the shadow-bill value as -$86 and the Figure 36 note gives the mean as -$86/yr and the median as -$90/yr; the text appears to cite the median._

[→ See original PDF page 38 for visual rendering]

Figure 37 shows how delivery savings varied by month. The variation here is tied to the seasonal nature of the rate – participants save money during the heating season and spend more money outside of the

<!-- PDF page 39 (printed Page | 39) -->

heating season. The white line in the middle of each box represents the median (or the 50th percentile). In March, for example, about 50% of accounts saved more than $100 and about 50% saved less than $100. The left and right sides of the box represent the 25th and 75th percentiles. The whiskers of the box extend to the minimum and maximum savings values (excluding outliers).

**Figure 37: Savings by Month, SHP Analysis**

[DIAGRAM DESCRIPTION: Figure 37: Savings by Month, SHP Analysis]

Twelve horizontal box-and-whisker plots (y axis Month 1 to 12, x axis Delivery Savings ($/Month) from -400 to 400). Savings are positive in the heating-season months and negative in the cooling-season months: medians of roughly +$150 in January, +$120 in February, +$100 in March, +$70 in April, +$85 in November and +$120 in December; and roughly -$120 to -$140 in each of May through October (boxes about -$180 to -$90). Whiskers reach about +$390 in January and about -$300 in July and October. (Values read from chart, approximate.)

[→ See original PDF page 39 for visual rendering]

##### 5.2.5.2 Difference-in-Differences

While the shadow bill approach covered in the prior section focuses exclusively on post-transition bills, the DID approach accounts for any changes in electric consumption that may be attributable to rate transition. Results from the DID bill impact analysis are shown in Table 15. Participant bills were $132/year greater, on average, in their first year on the SHP rate compared to the year before rate transition. During the same time period, bills for accounts in the matched comparison group increased by $4 on average. Taking the difference of these differences produce an estimated bill increase of $132, on average, during the first year on the SHP rate. Recall that this analysis was performed using the rate structures that were in place at the time, not the current rate structures. The current rate structures are more favorable to SHP participants. Repeating this analysis with the rates as of 10/1/2025 produces a bill savings estimate of $184 rather than a bill increase estimate of $132.

**Table 15: DID Bill Savings, SHP Analysis**

| Group                     | # of Accts | Average Annual Bill ($/year) Pre | Average Annual Bill ($/year) Post | Savings |
| ------------------------- | ---------- | -------------------------------- | --------------------------------- | ------- |
| Participants              | 1,770      | 1,536                            | 1,672                             | -136    |
| Controls                  | 1,770      | 1,528                            | 1,532                             | -4      |
| Difference-in-Differences |            |                                  |                                   | -132    |

_Extractor note (not source text): arithmetic check: 1,536 - 1,672 = -136; 1,528 - 1,532 = -4; -136 - (-4) = -132, matching the printed DID value. The text above says the participants' bills were "$132/year greater" compared with the year before; the table prints -136 for participants (-132 is the difference-in-differences). [source discrepancy: text attributes $132 to the participant pre/post change; the table shows $136 for participants.]_

<!-- PDF page 40 (printed Page | 40) -->

## 6 CONCLUSION

Key findings from the analysis include:

- We did not find a statistically significant increase or decrease in average annual consumption or seasonal consumption following enrollment on the ET. For the SHP rate, we found relatively small but significant increases in post-enrollment annual electric consumption (kWh = 158, percent impact = 1.3%, p-value = 0.01) and post-enrollment heating season electric consumption (kWh = 114, percent impact = 1.4%, p-value = 0.01).
  - Figure 38 shows average daily post-enrollment participant consumption (blue), baseline consumption (gray), and daily impacts (orange) for the ET analysis. Post-enrollment consumption mirrored pre-enrollment consumption.
  - Figure 39 shows the same metrics for the SHP analysis; the black reference lines in the figure separate the rate's heating and cooling seasons.
  - Although our analysis approach was to remove premises with major load modifier installations within one year of rate transition, it is possible that the pre/post change in electric consumption for the SHP group could be explained by load modifiers we are unaware of (e.g., an additional supplementary heat pump, converting domestic hot water from non-electric to electric) rather than behavioral responses to the rate.
- We did not find statistically significant increases or decreases in average demand during the summer peak period or the winter peak period (as defined by ISO-NE) following ET or SHP rate transition.
- Accounts that moved from Rate A to the ET saved money on their energy bills (relative to a baseline scenario where the ET accounts did not change rates), while accounts that moved from Rate A to the SHP saw bill increases (relative to a baseline scenario where the SHP accounts did not change rates). The bill impact calculations were performed using the rates that were in effect during the analysis timeframe, but all three rates (Rate A, ET, and SHP) have since changed. For SHP accounts in particular, the current rate structure is more favorable to enrollees than it was when this research began (see Table 14).

<!-- PDF page 41 (printed Page | 41) -->

**Figure 38: Net Energy Impact by Day of Year, ET Analysis**

[DIAGRAM DESCRIPTION: Figure 38: Net Energy Impact by Day of Year, ET Analysis]

A single chart titled "Net Impact" with Average Daily kWh (y axis 0-60+) against Date (01/01 to 01/01). A light-blue line ("Participant Post Usage") and a dashed gray line ("Baseline with DID Adjustment") overlap almost exactly (about 60 kWh/day in early January, a trough of about 30 kWh/day in May-June and October, and about 45-60 kWh/day in December). Orange bars ("Load Impact (Diff-in-Diff)") hug zero throughout the year.

[→ See original PDF page 41 for visual rendering]

**Figure 39: Net Energy Impact by Day of Year, SHP Analysis**

[DIAGRAM DESCRIPTION: Figure 39: Net Energy Impact by Day of Year, SHP Analysis]

Same format as Figure 38 for SHP accounts: usage about 55-62 kWh/day in January falling to about 18-25 kWh/day from May through October and rising to about 45-58 kWh/day in December. Two vertical dashed black lines at about 05/01 and 11/01 separate the heating and cooling seasons. Orange load-impact bars sit slightly above zero in the winter heating season (visible at roughly 1 kWh/day) and are essentially zero, slightly negative at times, in summer and fall.

[→ See original PDF page 41 for visual rendering]

---

# ATTACHMENT 7: CENTRAL MAINE POWER ALTERNATIVE RATES SURVEY

_Extractor note (not source text): PDF pages 42-48 are a separate attachment bound after the report, printed "Docket No. 2022-152 / Attachment 7 / Page n of 7" (the bottom-of-page number is 1-7). It is the survey instrument (questions and skip logic), not results. Response options are shown as numbered lists as printed; text in square brackets such as [SHOW IF ...] is programming instruction printed in orange in the source. The DSA logo on the first page and the CMP/DSA logos on the second page are omitted._

<!-- PDF page 42 (Attachment 7 page 1 of 7; printed page 1) -->

## CENTRAL MAINE POWER ALTERNATIVE RATES SURVEY

| Item             | Description                                                                                                                                                                                                                                                    |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Survey Objective | Understand (1) why alternative rate customers switched to the alternative rate, (2) their satisfaction with the rate, and (3) their perception of bill savings. Customers on the standard residential rate (Rate A) will also be surveyed as a baseline group. |
| Sample Frame     | All customers on the ET, SHP, ALM, or ATOU rates with a valid email address. A sample of Rate A customers will also be included.                                                                                                                               |
| Survey Platform  | Online survey hosted by CMP                                                                                                                                                                                                                                    |
| Language         | English only                                                                                                                                                                                                                                                   |
| Survey Length    | 5-7 minutes                                                                                                                                                                                                                                                    |

<!-- PDF page 43 (Attachment 7 page 2 of 7; printed page 2) -->

## EMAIL INVITATION TEMPLATE

Dear Customer,

Central Maine Power is conducting a short (5-7 minute) survey to better understand their customers' feelings about their electric rate and how satisfied they are with their experience. We would appreciate if you could take a few minutes to answer our questions so we can better serve our customers.

The responses you provide will be completely confidential and will not be used to identify you personally, nor will your information be shared or sold to a third-party firm.
Your feedback is incredibly valuable to us. By taking just a moment to share your thoughts, you'll help us tailor our services to better suit your needs. Click the link below to participate in a brief survey:

${l://SurveyLink?d=Take%20the%20Survey}
Or Copy and Paste the Following URL:
${l://SurveyURL}

Thank you for helping us serve you better.
Best regards,

Central Maine Power Customer Research Team

## FIELDS FOR SAMPLE FILE

**Fields to Administer Survey** (skip logic or to pipe into questions)

- `ADDRESS` Street & Town
- `WAVE` 0 = Test, 1 = Soft Launch; 2 = Full Launch
- `RATE_DATE` Date of transition to alternative rate
- `RATE_NAME` One of "Seasonal Heat Pump", "Electric Technology", "ALM", "TOU", or "Rate A"

**Fields for Monitoring or Analysis**

- `INCOME` Low-Income (LI) or not LI

## LOGOS ON SURVEY PAGES

[Logos: Central Maine Power; Demand Side Analytics.]

## Contents

| Section                                      | Page |
| -------------------------------------------- | ---- |
| Central Maine Power Alternative Rates Survey | 1    |
| Email invitation template                    | 2    |
| Fields for Sample File                       | 2    |
| Logos on Survey Pages                        | 2    |
| A. Intro Screen                              | 3    |
| B. Screening                                 | 3    |
| C. General                                   | 4    |
| D. Household Information                     | 5    |
| E. Wrap Up                                   | 7    |

_Extractor note (not source text): the contents list prints section D (Household Information) at page 5 and the "Wrap Up" at page 7; in the body, section D begins at the bottom of printed page 5 and its questions D1-D3 appear on printed pages 6-7 (see below)._

<!-- PDF page 44 (Attachment 7 page 3 of 7; printed page 3) -->

## A. INTRO SCREEN

**A1.** Thank you for taking this important survey about your satisfaction and experience with your electric rate. It should take about 5-7 minutes to complete.

Click the arrow below to begin.

[FOOTER] This survey can be taken on a smart phone, tablet, or computer. Some questions will be easier to view on a larger screen. You can access the survey from another device using the link in your email.

## B. SCREENING

**B1.** What is your relationship to <ADDRESS>?

1. Renter
2. Owner – primary residence
3. Owner – second/vacation home
4. Owner/landlord – do not live there
5. Former owner (sold home) [GO TO TERMINATION SCRIPT]
6. Other (Specify)

**B2.** [SHOW IF RATE_NAME != "Rate A"] Our records show that you transitioned to the RATE_NAME rate on or around RATE_DATE. Is that correct?

[SHOW IF RATE_NAME = "Seasonal Heat Pump"] The Seasonal Heat Pump Rate is a pilot program designed for customers using heat pumps. It offers a lower delivery rate per kWh during winter months, potentially reducing heating costs. However, it features a higher delivery rate in summer and a higher monthly customer charge compared to Rate A (the standard rate). Enrollment closed in December 2024, and the rate will expire on December 31, 2025.

[SHOW IF RATE_NAME = "Electric Technology"] The Electric Technology Rate features is designed encourage the adoption of new electric technologies by offering a lower per kWh charge. Customers on this rate receive lower per kWh charges but are subject to a higher monthly charge. Customers can benefit from this rate if their monthly usage is at least 800 kWh.

[SHOW IF RATE_NAME = "A-LM"] Rate A-LM (Load Management Service) is available to customers who install a second meter point of delivery. This is a time-varying rate, with electricity priced differently during on-peak and off-peak periods. Customers can create potential savings by shifting usage to off-peak hours, when rates are lower.

[SHOW IF RATE_NAME = "TOU"] Rate A-TOU (Time-of-Use) is a time-varying rate where electricity costs are highest during on-peak periods and lowest during off-peak periods. The rate also features a shoulder period for times outside of the on- and off-peak hours. Customers can create potential savings by shifting usage to off-peak hours, when rates are lower.

1. Yes
2. No [GO TO TERMINATION SCRIPT]
3. Not sure [GO TO TERMINATION SCRIPT]

**B3.** [SHOW IF RATE_NAME != "Rate A"] Were you involved in the decision to transition to the RATE_NAME rate?

1. Yes
2. No
3. Don't know

<!-- PDF page 45 (Attachment 7 page 4 of 7; printed page 4) -->

**B4.** [SHOW IF RATE_NAME != "Rate A" & B3 = 2 or 3] This survey has questions about the decision to transition to the RATE_NAME rate, as well as experiences with the RATE_NAME rate. If you are the best person to answer these questions, please continue. If there is someone else who should answer these questions, please ask them to start here, or from the link in your email.

1. Continue now [CONTINUE]
2. I will find someone else [SHOW AS ERROR: "Thank you! You can close your browser window. When the person involved with the decision to transition to the RATE_NAME rate is available, they can click on the link in the email you received to continue."]

**B5.** This survey has questions about experiences with the standard residential rate. If you are the best person to answer these questions, please continue. If there is someone else who should answer these questions, please ask them to start here, or from the link in your email.

1. Continue now [CONTINUE]
2. I will find someone else [SHOW AS ERROR: "Thank you! You can close your browser window. When the person is available, they can click on the link in the email you received to continue."]

[TERMINATION SCRIPT]

**B6.** Thank you for your time. Unfortunately, you do not qualify for this survey. You can close this window.

## C. GENERAL

**C1.** On a scale of 1-5 where 1 represents unsatisfied and 5 represents satisfied, how satisfied have you been with the RATE_NAME rate?

1. 1 – Unsatisfied
2. 2
3. 3
4. 4
5. 5 – Satisfied

**C2.** [SHOW IF RATE_NAME != "Rate A"] What motivated you to transition to the RATE_NAME rate? Select all that apply. [MULTIPLE RESPONSE; RANDOMIZE 1 -9]

1. To reduce my electricity costs
2. [SHOW IF RATE_NAME = "ALM" OR "TOU"] To take advantage of off-peak or time-based pricing
3. To better manage high-load appliances or heating
4. [SHOW IF RATE_NAME = "Seasonal Heat Pump"] To participate in a pilot program
5. To support energy efficiency or sustainability goals
6. To try something new or innovative
7. Recommended by CMP or suggested during outreach
8. Based on advice from someone I trust or online research
9. [SHOW IF RATE_NAME = "Seasonal Heat Pump" OR "Electric Technology"] To support the purchase or use of new electric technologies (e.g., heat pump, electric vehicle, EV charger, etc.)
10. Other (Specify)

**C3.** [SHOW IF RATE_NAME != "Rate A"] Since transitioning to the RATE_NAME rate, how do you think your electricity consumption has changed relative to when you were on the standard rate?

1. I use significantly more energy than I did on the standard rate
2. I use slightly more energy than I did on the standard rate
3. My electricity consumption has not changed much
4. I use slightly less energy than I did on the standard rate
5. I use significantly less energy than I did on the standard rate

<!-- PDF page 46 (Attachment 7 page 5 of 7; printed page 5) -->

6. I don't know

**C4.** [SHOW IF RATE_NAME != "Rate A"] Since transitioning to the RATE_NAME rate, how do you think your electric bills have changed relative to when you were on the standard rate?

1. My electric bills are significantly higher than they were on the standard rate
2. My electric bills are slightly higher than they were on the standard rate
3. My electric bills have not changed much
4. My electric bills are slightly lower than they were on the standard rate
5. My electric bills are significantly lower than they were on the standard rate
6. I don't know

**C5.** [SHOW IF RATE_NAME != "Rate A"] Would you recommend the RATE_NAME rate to friends, family, or neighbors with similar homes and/or electric technologies?

1. No, I would not
2. Maybe
3. Yes, I would
4. I already have

**C6.** [SHOW IF C5 = 1,2 & RATE_NAME != "Rate A"] Why did you give that rating? [OPEN END]

**C7.** [SHOW IF RATE_NAME !="Seasonal Heat Pump"] Do you plan to stay on the RATE_NAME rate for the foreseeable future?

1. Yes
2. No
3. I don't know

**C8.** [SHOW IF RATE_NAME !="Seasonal Heat Pump" AND C7 = 2] You indicated that you do not plan to stay on the RATE_NAME rate. Why not? [OPEN END]

**C9.** [SHOW IF RATE_NAME !="Seasonal Heat Pump" AND C7=3] You indicated that you don't know if you will stay on the RATE_NAME rate. Why is that? [OPEN END]

**C10.** [SHOW IF RATE_NAME !="Seasonal Heat Pump" AND C7 = 2] You indicated that you do not plan to stay on the RATE_NAME rate. Which rate do you plan to transition to? [RANDOMIZE 1-4]

1. [SHOW IF RATE_NAME != "Rate A "] Rate A (standard rate)
2. [SHOW IF RATE_NAME != "TOU "] Time-of -Use (A-TOU)
3. [SHOW IF RATE_NAME != "ALM "] Alternative Load Management (A-LM)
4. [SHOW IF RATE_NAME != "ET "] Electric Technology (ET)

**C11.** [SHOW IF (C7 = 2 0r 3) OR RATE_NAME = "Seasonal Heat Pump"] Would you be interested in learning about alternative supply rates offered by Central Maine Power?

1. Yes, email to received details about Central Maine Power's alternative supply rates: [OPEN END; VALID EMAIL]
2. No

**C12.** Is there any other feedback you'd like to provide regarding the RATE_NAME rate? [OPEN END]

## D. HOUSEHOLD INFORMATION

<!-- PDF page 47 (Attachment 7 page 6 of 7; printed page 6) -->

[SKIP SECTION IF B1 = 4 (LANDLORD/NON-OCCUPANT)]

The next few questions are about you and your household and are designed to help Central Maine Power know how to better assist their customers.

This information will not be publicized or shared with any parties outside of Central Maine Power. It will not be used to directly sell or market any products or services to you and will not impact your eligibility for future alternative rates offered by Central Maine Power.

**Click the arrow below to continue.**

**D1.** Which of the following electric technologies are in your home? [MULTIPLE RESPONSE; RANDOMIZE 1-9]

1. Electric vehicle (EV) charger
2. Heat pump
3. Heat pump water heater
4. Heat pump clothes washer/dryer
5. Induction stove
6. Solar PV array
7. Home energy storage
8. Electric resistance heating
9. Hot tub
10. None of these [EXCLUSIVE]

**D2.** [SHOW IF D1 = 1-9 & RATE_NAME != "Rate A"] Approximately when were the electric technologies added?

_Structure: a grid with one row per technology listed in D1 and three response columns; the response cells are blank in the instrument (to be checked by the respondent)._

| Technology (row)                              | More than a year before transitioning to the RATE_NAME rate | Within a year of transitioning to the RATE_NAME rate | More than a year after transitioning to the RATE_NAME rate |
| --------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| 1. [IF D1 = 1] Electric vehicle (EV) charger  |                                                             |                                                      |                                                            |
| 2. [IF D1 = 2] Heat pump                      |                                                             |                                                      |                                                            |
| 3. [IF D1 = 3] Heat pump water heater         |                                                             |                                                      |                                                            |
| 4. [IF D1 = 4] Heat pump clothes washer/dryer |                                                             |                                                      |                                                            |
| 5. [IF D1 = 5] Induction stove                |                                                             |                                                      |                                                            |
| 6. [IF D1 = 6] Solar PV array                 |                                                             |                                                      |                                                            |
| 7. [IF D1 = 7] Home energy storage            |                                                             |                                                      |                                                            |
| 8. [IF D1 = 8] Electric resistance heating    |                                                             |                                                      |                                                            |
| 9. [IF D1 = 9] Hot tub                        |                                                             |                                                      |                                                            |

**D3.** Including yourself, how many people currently live in your home? [SINGLE RESPONSE]

1. 1
2. 2
3. 3
4. 4
5. 5+
6. I prefer not to say.

<!-- PDF page 48 (Attachment 7 page 7 of 7; printed page 7) -->

**D4.** Please select the age ranges of people in your home (including yourself). Select all that apply. [MULTIPLE SELECT]

1. Younger than 5
2. 5 to 17
3. 18 to 34
4. 35 to 64
5. 65 to 84
6. 85 or older
7. Prefer not to say [EXCLUSIVE]

**D5.** What was your 2024 annual household income from all sources before taxes? [SINGLE RESPONSE]

1. $0-$49,999
2. $50,000 - $99,999
3. $100,000 - $149,999
4. $150,000 - $199,999
5. $200,000 - $249,999
6. $250,000 and above

**D6.** How would you describe your living quarters? [SINGLE RESPONSE]

1. Single-family detached house
2. Single-family attached house (e.g. townhouse)
3. Duplex, triplex, or four-plex
4. Apartment or condominium with 5 units or more
5. Manufactured or mobile home
6. Other, please specify: [OPEN-ENDED RESPONSE]

**D7.** Is your household currently enrolled in any of the following? [MULTIPLE RESPONSE; ROTATE 1-5]

1. Energy or Fuel Assistance (LIHEAP, HEAP or LIAP)
2. MaineHousing Rental Assistance or Vouchers
3. Supplemental Nutrition Assistance Program (SNAP)
4. MaineCare for medical insurance coverage
5. Temporary Assistance for Needy Families (TANF)
6. None of these [EXCLUSIVE]
7. Prefer not to say [EXCLUSIVE]

## E. WRAP UP

**E1.** That's it! Thank you for your time and input. Your response has been recorded and you can close this window.

If you have questions about this survey, please contact <CMP survey team contact email>. If you are interested in learning about energy efficiency rebates Efficiency Maine offers to homeowners in Maine, visit https://www.efficiencymaine.com/at-home/ or use a search engine to search "Efficiency Maine rebates."

---

## Footnotes

_See the footnote definitions placed in context above on PDF page 5 ([^1], ISO-NE peak definitions) and PDF page 19 ([^2], matching criteria); the PDF has two footnotes in total and the extract has two definitions._
