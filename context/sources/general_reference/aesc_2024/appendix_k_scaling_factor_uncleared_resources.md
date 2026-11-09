---
source_file: "Synapse - 2024 - Avoided Energy Supply Components in New England 2024 Repor.pdf"
citekey: synapse_AvoidedEnergySupply_2024
zotero_item: "4HZWP4NM"
public_url: "https://drive.google.com/file/d/154NYJ1K_xbqwFq1uQeN2rifByQDQrYj0/view"
short_url: "https://pub.switch.box/synapse_AvoidedEnergySupply_2024"
source_url: "https://www.synapse-energy.com/sites/default/files/inline-images/AESC%202024%20May%202024.pdf"
md5: "4fb83ebfe927b541ac86cbf599b380be"
document_type: report
filer: Synapse Energy Economics, Sustainable Energy Advantage, North Side Energy, Resource Insight, Les Deman Consulting
pages_total: 436
extraction_scope: "partial: PDF pp. 411-436 (printed pp. 393-418), Appendix K: Scaling Factor for Uncleared Resources, through the end of the report; the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Appendix K, a reprint (with a new Purpose section) of a 2019 Resource Insight study for National Grid on how load reductions that occur on only some summer days, for only some years, change ISO New England's peak load forecast. It builds a proxy of ISO-NE's summer-peak regression, reports the ratio R of forecast reduction to load reduction by number of event days (1-62) and years of program operation (1-15), tests imperfect dispatch, and includes Subappendices A-C with the full R tables (Tables 182-184) used by the Appendix K workbook to scale uncleared capacity and uncleared capacity DRIPE benefits."
why_here: "Gives the scaling factor to apply to avoided uncleared capacity and capacity DRIPE values for peak-limited measures (demand response, dynamic or peak-pricing rate designs, other measures that do not reduce load on every summer day), which matters when Switchbox values time-varying or demand-response-type rate designs against New England avoided costs."
---

_Extractor note (not source text): this file holds PDF pp. 411-436 (printed pp. 393-418) of AESC 2024, Appendix K: Scaling Factor for Uncleared Resources, to the end of the report; the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. Tables 182, 183 and 184 are transcribed in full as markdown tables (62 rows by 15 years each) rather than as sampled tables with a CSV, because they are the numeric content of the appendix; the text layer of the PDF was used for the values and checked programmatically against a second text extraction of the PDF. The source text is transcribed verbatim; no typographical corrections were made, but the source's superscript ordinals ("14th") are written as plain ordinals and superscript exponents are written with Unicode or LaTeX. Where the printed running text and a figure legend disagree, or a cross-reference is wrong, an inline bracketed note says so. Where a page break falls mid-sentence and footnote definitions are printed at the bottom of the earlier page (PDF pp. 412 and 414), the sentence is split into two paragraphs around the definitions so that each definition stays on its own page._

[PDF pp. 1-410 not transcribed: front matter, Chapters 1-12 and Appendices A-J, in the other files of this folder (see README.md)]

[PDF p. 411 | printed p. 393]

# Appendix K: Scaling Factor for Uncleared Resources

This appendix repeats text originally found in the April 2019 report titled, “The Effect of Uncleared Capacity Load Reductions on Peak Forecasts.” This report was authored by Resource Insight, Inc. with assistance from Synapse Energy Economics, Inc., and was originally commissioned by National Grid as a supplemental study to AESC 2018.[^451] This document was accompanied by a “DR Coefficient Calculator” workbook, which program administrators can use to evaluate how uncleared capacity DRIPE benefits should be adjusted for measures that operate in only some hours of the year.[^452]

Text and analysis in this appendix have not been updated, with the following exceptions:

- The addition of a “Purpose” section summarizing the intended use of this appendix
- Some edits to text to improve readability and consistency with the rest of the AESC 2024 text
- Cross-references to parts of the main AESC 2024 text
- Several modifications and corrections to the DR calculator

Analytical updates to this document were not scoped within AESC 2021 or AESC 2024; however, we do not expect these values to be substantially different than those calculated in the original 2019 report because ISO New England’s load forecasting techniques have not changed substantially. Furthermore, because we do not assume these load forecasting techniques will change under the new market structure (assumed in AESC 2024 to be effective in 2028), we assume that these same values and effects are also applicable to benefits that accrue in the summer season in years in which the new market structure is active. However, we note that this methodology uses the impact of changes in loads on the peak load forecast, assuming that the peak load forecast is a proxy for the amount of capacity that ISO will procure for the region. That has historically been a reasonable proxy, but over time this may become a less accurate assumption as the high-risk hours that determine the ISO’s demand for capacity diverge from the peak hours. As a result, the scaling factors described in this section are likely most accurate for measures active in the next one to five years.

[^451]: Chernick, P., P. Knight, M. Chang. April 22, 2019. _The Effect of Uncleared Capacity Load Reductions on Peak Forecasts._ Synapse Energy Economics prepared for National Grid. Available at [https://www.synapse-energy.com/sites/default/files/The_effect_of_load_reductions_on_peak_forecasts.pdf](https://www.synapse-energy.com/sites/default/files/The_effect_of_load_reductions_on_peak_forecasts.pdf).

[^452]: See original version at [https://www.synapse-energy.com/sites/default/files/DR_Coefficient_Calculator%20%282%29.pdf](https://www.synapse-energy.com/sites/default/files/DR_Coefficient_Calculator%20%282%29.pdf).

[PDF p. 412 | printed p. 394]

### Purpose

This document describes the methodology for creating a scaling factor that adjusts the benefits provided by uncleared resources. It also provides a calculator workbook so that program administrators may create this scaling factor for themselves. This workbook is the file titled “Appendix K.xlsx.”

It is only for resources that are not expected to provide a capacity benefit throughout the summer period (we focus on summer, because it is summer demand that drives the capacity market under current market rules, though that will change with the implementation of ISO’s RCA proposal). For example, this factor is useful for demand response measures that may only be active some summer days. But it is not applicable to resources like energy efficiency that are assumed to provide savings at a more-or-less consistent level throughout the summer.

Program administrators wishing to use this appendix will want to use the Appendix K workbook to estimate the appropriate scaling factor for their DSM resource. This factor is then multiplied by the uncleared capacity or uncleared capacity DRIPE avoided cost (calculated using the _AESC 2024 User Interface_) and the measure’s capacity savings and seasonal coincidence factor to provide the final benefit value.[^453]

This scaling factor is not applicable to cleared capacity, cleared capacity DRIPE, cleared reliability, uncleared reliability, or any other avoided cost category.

### Introduction

This appendix describes our analysis of the effects of load reductions on a varying number of days per year over a varying number of years. This analysis included the construction of a regression model to mimic the ISO New England forecast model and the variation of the historical data to determine the effect of targeted load reductions for the FCAs. We interpret these effects as having an impact on the future value of uncleared capacity and uncleared capacity DRIPE.

Our modeling indicates that a load reduction program that occurs on even a single peak day each summer can affect the load forecast used in the FCA. In most situations, the load forecast will fall more if the historical load is reduced for more days per year or for more years. Regardless of the number of days that a program reduces load annually, the reduction in the load forecast rises steadily for at least eight years. If the program reduces load on less than 55 days, the forecast reduction continues to

[^453]: We note that there may be certain situations when a dispatchable resource (such as demand response or storage) is cleared in the capacity market, but also performs in such a way that creates uncleared capacity benefits. These additional uncleared benefits are likely to be small, as the most likely the way for them to occur is for a resource to operate for a limited number of hours, during periods that are less important to the formulation of ISO New England’s load forecast regression. Calculations to estimate these benefits are complex, dependent on the specific program being analyzed, and may be impossible to calculate without obtaining more specific load regression data from ISO New England. As a result, we do not perform this estimate in AESC 2021. Future editions of this study or follow-up supplemental studies may examine this issue in closer detail.

[PDF p. 413 | printed p. 395]

increase until the program has been running for 12 days. For programs that reduce load on less than 13 days annually, running the program for more years continues to depress the load forecast further, up to the 15 years’ worth of historical data that ISO New England uses to develop each load forecast.

This implies that resources that do not provide load reductions on every day of the summer period should have reduced values for uncleared capacity and uncleared capacity DRIPE, relative to the values estimated in the _AESC 2024 User Interface_.

#### Background

This issue is specific only to uncleared resources.[^454] For example, these may include demand response programs, behavioral programs, or rate-design initiatives that are not eligible capacity resources. Although uncleared resources do not receive capacity payments, they reduce the aggregate amount of capacity that is required, and hence the price of that capacity, by reducing the ISO New England peak load forecast used in the FCA for that year (see Section 5.2: _Uncleared capacity calculations_ for a longer discussion of this dynamic).

The quantity and price of the capacity obligations acquired in the FCA of a particular year (year $t$) depend on the forecast prepared in the previous year ($t - 1$). That forecast is built upon a regression analysis constructed from daily historical data from each of the 62 days in July and August for the previous 15 years ($t - 16$ to $t - 2$), which consists of 930 data points.[^455] The regression formulation for the forecast may vary from year to year, but appears to consistently include multiple independent variables computed from a weighted temperature-humidity index (WTHI), including an annual time trend times WTHI and the gross energy forecast (before energy efficiency and BTM solar PV).

Although we consulted with ISO New England on its forecast data, ISO New England did not provide us with its proprietary demand model data or any details on the functional form of its regression model, beyond those in the Forecast Data summaries provided on the ISO New England web site.[^456] As a result, our analysis reconstructs a proxy ISO New England load forecast. We then use this to quantify the impact of different load reductions over different time periods and under different conditions.

[^454]: This includes any resources or portions of resources that are not bid into the FCA or are bid into FCAs but do not clear the auction.

[^455]: Discussions with ISO New England after the completion of this supplemental study confirmed that the forecast is solely built on summer peak hours. Winter peak hours are not included.

    Knight, P., M. Chang, J. Hall. May 1, 2020. _AESC Supplemental Study Part I: Considering Winter Peak Benefits._ Synapse Energy Economics for Massachusetts Electric Energy Efficiency Program Administrators. Available at [https://www.synapse-energy.com/sites/default/files/AESC_Supplemental_Study_Part_I_Winter_Peak.pdf](https://www.synapse-energy.com/sites/default/files/AESC_Supplemental_Study_Part_I_Winter_Peak.pdf).

[^456]: This data includes ISO New England’s computation of daily WTHI and reconstitution of load for peak-hour energy efficiency reductions, demand response and OP #4 measures, and behind-the-meter solar output.

[PDF p. 414 | printed p. 396]

### The reference regression model

We constructed our proxy for the ISO New England forecast model based on the data used in the 2017 CELT forecast, which was used in FCA 12 to procure capacity for the summer of 2021.[^457] Importantly, all of the effects described below for the reference regression model are for load reductions of various numbers of years that would have been used in producing the 2017 CELT forecast for summer 2021, which was the basis for the demand curve used in FCA 12. Other regressions performed using data for other years could provide different results. A one-year load reduction would affect only the 2016 summer peak day(s), a two-year reduction would affect 2015 and 2016, a three-year reduction would affect 2014–2016, and a 15-year reduction would reduce peaks in 2002–2016.

#### Input data

Since we did not have ISO New England’s exact data, we needed to develop a proxy dataset. As a result, our analysis should be interpreted as an estimate of load reduction effects based upon data and using a _model similar_ to that currently used by ISO New England. We do not claim that our model is a precise prediction of future ISO New England forecasts. Since ISO New England’s data and its model structure change (at least a little) every year, we cannot anticipate the exact form of the ISO New England load forecast model for any specific future year.

##### Development of proxy data

First, we made a number of assumptions to generate our proxy historical dataset, which may not necessarily match ISO New England’s past and future sources and methodology.

The dependent variable in the regression analysis is the daily gross peak demand. This is the actual daily peak demand, plus the effects of BTM solar PV and energy efficiency programs (referred to as PDR by ISO New England) for both peak demand and energy, as well as the effects of Operation Procedure #4 (OP #4) events and load management on peak (which is available only for the summer and winter peaks).[^458], [^459] Our understanding is that ISO New England uses a proprietary data service to estimate the output of installed solar capacity in each historical hour, while assuming that every hour’s PDR reduction is equal to the PDR resource cleared in that capacity delivery year.

We estimated historical daily gross peak load as the sum of (a) the maximum hourly demand for the day in ISO New England’s hourly load data files and (b) the summer peak PV and PDR reported in the ISO

[^457]: FCA 12 was conducted in February 2018 and was the most recent FCA conducted at the time of this analysis.

[^458]: Actual daily peak demand is available from the ISO New England website.

[^459]: ISO New England. March 4, 2021. “ISO New England Operating procedure No. 4 – Action During a Capacity Deficiency” Iso-ne.com. Available at [https://www.iso-ne.com/static-assets/documents/rules_proceds/operating/isone/op4/op4_rto_final.pdf](https://www.iso-ne.com/static-assets/documents/rules_proceds/operating/isone/op4/op4_rto_final.pdf)

[PDF p. 415 | printed p. 397]

New England’s 2017 Forecast Data spreadsheet for the year.[^460], [^461] We computed the gross monthly net energy for load (NEL) by multiplying the historical monthly sum of actual load by the ratio of gross annual energy to net annual energy from the ISO New England 2017 Forecast Data.[^462]

We computed the ISO New England temperature-humidity index (THI) for each day ($0.5 \times \text{dry-bulb temperature} + 0.3 \times \text{wet-bulb temperature} + 15$) as the weighted average of the THI’s (the “WTHI”) from eight weather stations around the region.[^463] We then computed the WTHI for each day using ISO New England’s formula (weights of 10 for today’s THI, 5 for yesterday’s THI, and 2 for the previous day).[^464]

#### Model specification

We estimated the historical relationship of gross load to WTHI, time, NEL and other variables with an ARIMAX (Auto-Regressive Integrated Moving-Average model with eXogenous variables) regression model.[^465] This model incorporates both exogenous variables (e.g., net energy for load, weather) and the autoregressive error terms that ISO New England uses in its regression model. These are summarized in Table 179.

[^460]: ISO New England. Last accessed March 10, 2021. “Energy, Load, and Demand Reports.” _ISO-ne.com._ Available at [https://www.iso-ne.com/isoexpress/web/reports/load-and-demand/-/tree/sys-load-eei-fmt](https://www.iso-ne.com/isoexpress/web/reports/load-and-demand/-/tree/sys-load-eei-fmt).

[^461]: CELT 2017 Forecast Data File, Tab 5, WN. CELT 2017 was analyzed, as it was the projection used as the basis of the 2018 AESC Study.

[^462]: CELT 2017 Forecast Data File, Tab 1, History, Gross ISO-NE Coincident Summer Peak.

[^463]: The Notes sheet of the annual _SMD Hourly.xlsx_ file provide the following weights for the weather stations: Windsor Locks CT (27.7 percent); Bridgeport CT (7 percent); Boston MA (20.1 percent); Burlington VT (4.6 percent); Concord NH (5.8 percent); Worcester MA (21.4 percent); Providence RI (4.9%); Portland ME (8.5 percent). We used the same weights for all years; we have not been able to confirm whether ISO New England has changed the weights over time, as load (especially summer peak) has increased in northern New England compared to the southern portion of the region.

    Iowa State University. March 11, 2021. “Dry Line Over Iowa.” _Iastate.org._ Available at [https://mesonet.agron.iastate.edu/](https://mesonet.agron.iastate.edu/).

[^464]: Forecast Modeling Procedure for the 2018 CELT, May 1, 2018, page 9. [https://www.iso-ne.com/static-assets/documents/2018/04/modeling_procedure_2018fcst.pdf](https://www.iso-ne.com/static-assets/documents/2018/04/modeling_procedure_2018fcst.pdf). Note that this document contains all citations for coefficients and weights used in this analysis.

[^465]: Statmodels. Last accessed March, 10, 2021. _Statsmodels.org._ Available at [https://www.statsmodels.org/devel/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html](https://www.statsmodels.org/devel/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html).

[PDF p. 416 | printed p. 398]

**Table 179. Variables used in summer peak model**

| Variable     | Definition                                                                 |
| ------------ | -------------------------------------------------------------------------- |
| Intercept    | Constant Term                                                              |
| PEAK         | Daily Peak Load, MW                                                        |
| MA_NEL       | 12-month Moving Sum Annual Net Energy for Load, GWh                        |
| WTHI_SQ      | The square of [the 3-day Weighted Temperature-Humidity Index at Peak– 55°] |
| TIME_WTHI    | Year indicator; (2002=11, …, 2016=25) × WTHI                               |
| Weekend_WTHI | WTHI for a weekend day, else 0                                             |
| July_04WTHI  | WTHI for July_4, else 0                                                    |
| HOLWTHI      | WTHI for a Holiday, else 0                                                 |
| Yr2005       | 1 if Year=2005; 0 otherwise                                                |
| Yr2012       | 1 if Year=2012; 0 otherwise                                                |
| AR(1)        | Correction for autocorrelated error from the previous year                 |
| AR(2)        | Correction for autocorrelated error from the two years previously          |

_Note: This reproduces the description of the summer peak model in the Peak Definitions in ISO New England’s 2017 Regional and State Energy & Peak Model Details, corrected to reflect conversations with the ISO forecasters and the specific model described in the Summer Peak Models tab of the Model Details._[^466]

Independent variables included:

- Net Energy for Load, grossed up for PV and energy efficiency, over the 12 months ending in the current month (July or August, depending on the data point).
- The 3-day weighted temperature-humidity index (WTHI) for the eight cities used in ISO New England’s own modeling of weather (see footnote 463). In our analysis, following the treatment in the ISO New England model, the WTHI variable is used as the square ($[\text{WTHI}-55]^2$), and as various cross terms, such as WTHI × weekend dummies.
- Year × (WTHI–55), where the year index is the calendar year minus 1991.
- Boolean flags (i.e., dummies) for holidays, July 4th, weekends, the years 2005 and 2012, and WTHI times the dummy variables for weekends, holidays and July 4th.[^467]

These variables were defined for each July and August day in 2002 through 2016.

[^466]: The ISO New England forecast documentation sometimes refers to gross loads as net of PV and PDR, and the Forecast Modeling Procedure for 2017 CELT describes the composite time variable as using WTHI–55º, while the 2017 Regional and State Energy & Peak Model Details file suggests that WTHI is not reduced by 55º.

[^467]: It is unclear why ISO New England included variables for both holidays and July 4th, since the only holiday in the two summer months is July 4th. We used the two redundant variables; collectively, the two dummies should capture the effect of July 4th. It is also unclear why the years 2005 and 2012 featured Boolean flags.

[PDF p. 417 | printed p. 399]

#### Forecast data

Once we developed the regression equation, we required forecast input values for the equation. One such input is a forecast of gross energy for load, which ISO New England provides in its forecast.[^468] A second set of inputs entails time trend and binary variables: for time trend, we observe that 2017 is year 26, 2018 is year 27, and so on. For binary variables, the weekend binary equals WTHI on future Saturdays and Sundays, the July 4 and holiday binaries equal WTHI on July 4 each year.

ISO New England’s forecasting method does not use a single WTHI value, but instead identifies the highest load for a variety of input conditions:

> Weekly peak load forecast distributions are developed by combining output from the daily peak load models with energy forecasts and weekly distributions of weather variables over 40 years.
>
> The expected weather associated with the seasonal peak is considered to be the 50th percentile of the top 10% of the pertinent week’s historical weather distribution. The monthly peak load is expected to occur at the weather associated with the 20th percentile of the top 10% of the pertinent week’s weather distribution. The “pertinent week” is the week of the month or season with the most extreme weather distribution.
>
> For resource adequacy purposes, peak load distributions are developed for each week of the forecast horizon.[^469]

We do not have access to the distributions that ISO New England used in this method, nor do we have a clear operational description of the method. Therefore, we performed a calculation to estimate a value of WTHI that best reproduced the 2017 CELT peak forecast, which turned out be 81.4°.

#### Base forecast benchmarking

Figure 63 summarizes our modeled Gross and NET 2017 forecast against the 2017 reported Gross and NET CELT forecast. Our modeled forecasted peak demands closely match the ISO’s 2017 CELT forecast. Our forecasts for gross peak are within 0.2 percent of the 2017 CELT forecast for 2021, the year for which the 2017 forecast determined the installed capacity requirement.

[^468]: 2017 Forecast Data File, Tab 6, Monthly NEL.

[^469]: Forecast Modeling Procedure for the 2018 CELT, May 1, 2018, p. 6.

[PDF p. 418 | printed p. 400]

**Figure 63. Comparison of forecasts of gross and net Summer Peak, 2017 CELT and Resource Insight modeled proxy**

[DIAGRAM DESCRIPTION: Figure 63. Comparison of forecasts of gross and net Summer Peak, 2017 CELT and Resource Insight modeled proxy]

A line chart with years 2017 through 2026 on the x axis and "ISO New England Load (GW)" on the y axis (scale 24 to 33 GW, gridlines every 1 GW). Four lines, labeled directly at the right end of the chart rather than in a legend: "Gross: CELT" (solid blue-teal), "Gross: Model" (solid red), "Net: CELT" (dashed blue-teal) and "Net: Model" (dashed red). The two gross lines rise steadily from roughly 29.1 GW (CELT) and 29.6 GW (Model) in 2017 to roughly 31.8 GW (CELT) and 31.7 GW (Model) in 2026; they converge and are nearly indistinguishable from about 2021 onward. The two net lines sit near 26-27 GW: both start at roughly 26.5 GW (CELT) and 26.9 GW (Model) in 2017, drift down to about 26.1-26.2 GW around 2022-2023, then rise slightly to about 26.3 GW by 2026. The chart shows that the proxy model closely reproduces the ISO's 2017 CELT gross and net summer peak forecasts (values read approximately from the chart).

[→ See original PDF page 418 for visual rendering]

### The effect of load reductions on the forecast

The following sections describe our methodology and findings. We also describe a set of sensitivities that were analyzed to provide robustness for our results.

#### Structure of reductions

Using our constructed base forecast, we estimated how various load reductions in 2002 through 2016 would have affected the ISO New England load forecast for 2021. Each sensitivity run for the analysis consisted of four steps:

1. Reduce historical gross peak demands on a specified number of summer event days ($d$) for a specified number of years ($y$) by a constant number of MW ($\Delta L$).
2. Estimate new regression model coefficients using the same functional form and the modified historical data.
3. Develop peak demand forecasts for the years 2017–2026 (and most importantly, 2021) using the new coefficients.
4. Compute the ratio ($R$) of the change between forecast peak ($\Delta F$) to the load reduction ($\Delta L$).

The ratio $R$ can be thought of as a measure of the efficiency of load reduction in reducing the forecast.

For $\Delta L$, we tested load reductions of 250 MW, 500 MW, and 1,000 MW. We used the same reduction in all the days and all the years adjusted in any particular run.

[PDF p. 419 | printed p. 401]

For $d$, we reduced load on the highest days, from one event day to all 62 summer days per affected year. We tested reductions on the highest-load days and the highest-WTHI days and looked at the effect of imperfect forecasting of peak days.

For $y$, we reduced load on the most recent years, from just one year (2016) to all 15 years 2002–2016.

#### The effect of lower input values on regression forecasts

When we began this analysis, we expected that reductions on more days, and reductions in more years, would consistently push down the forecast further. As we discuss in the next section, that is not what we found. Before presenting our results, we will explain how they can arise.

The next four figures show a regression through 15 years of base data. In these examples, we assume a constant 1.5 percent annual growth.[^470] In each figure, we show the base historical data, the linear trend line with the base data, the historical data that would have been observed with 1,000 MW reductions in some years, and the regression trend line with the modified data. For each figure, we identify how the change in load impacts the regression and the projection of 2021 load in particular.

The first figure, Figure 64, shows the effect of load reductions in the last two years of data, representing a demand response program operating in 2015 and 2016. The trend line tilts so that the trend is higher than the actual load in the first few years and in the last two years (the two years with demand response reductions), but lower than the input data for 2008–2014. The projection for 2021 is about 700 MW lower than in the base case.

[^470]: A comparable analysis using weather-normalized loads before PDR and PV for 2002 through 2016 produced very similar results. But, due to a drop in load associated with the 2009–2010 Great Recession, it is more difficult to read. We use a simplified example here.

[PDF p. 420 | printed p. 402]

**Figure 64. Effect of two years of demand response on the forecast**

[DIAGRAM DESCRIPTION: Figure 64. Effect of two years of demand response on the forecast]

A scatter plot with dotted linear trend lines. The x axis is year, 2002 to 2022 (labeled every two years); the y axis is "Forecasted Load (MW)", 23,000 to 33,000 in steps of 1,000. Legend: "Base" (blue open circles), "2 Years" (yellow open circles), "Linear (Base)" (blue dotted line), "Linear (2 Years)" (yellow dotted line). The base points rise from about 24,600 MW in 2002 to about 30,300 MW in 2016, with a 2021 projection of about 32,200 MW on the base trend line. The yellow points coincide with the base points through 2014 and then drop below them in the two reduced years, 2015 (about 28,800 MW) and 2016 (about 29,300 MW). The yellow trend line is slightly above the base line in the earliest years, crosses below it in the mid-2000s, and projects about 31,500 MW for 2021, roughly 700 MW below the base projection, consistent with the text (values read approximately from the chart).

[→ See original PDF page 420 for visual rendering]

Next, Figure 65 shows the effect of five years of demand response reductions. The trend line with the demand response has tilted further, so that it is almost 1,000 MW below the base-case trend by 2016, and 1,400 MW below the base-case forecast for 2021. The trend line mostly rotates clockwise, rather than moving down, so the change from the base case increases over time and the reduction in the 2021 forecast is substantially larger than the reduction in loads in the five years affected by demand response.

**Figure 65. Effect of five years of demand response on the forecast**

[DIAGRAM DESCRIPTION: Figure 65. Effect of five years of demand response on the forecast]

Same format as Figure 64 (x axis 2002-2022, y axis "Forecasted Load (MW)" 23,000-33,000; legend "Base", "5 Years", "Linear (Base)", "Linear (5 Years)"). The yellow "5 Years" points deviate below the base points in the five reduced years 2012-2016 (from about 27,500 MW in 2012 to about 29,300 MW in 2016). The yellow trend line is tilted clockwise relative to the base trend line: it lies slightly above the base line in the earliest years and falls progressively below it, reaching a 2021 projection of about 30,800 MW against about 32,200 MW for the base case (a gap of about 1,400 MW, consistent with the text). Values read approximately from the chart.

[→ See original PDF page 420 for visual rendering]

Third, Figure 66 shows the effects of nine years of demand response, which continues the pattern in Figure 65; the forecast for 2021 would be almost 1,800 MW below the base case.

[PDF p. 421 | printed p. 403]

**Figure 66. Effect of nine years of demand response on the forecast**

[DIAGRAM DESCRIPTION: Figure 66. Effect of nine years of demand response on the forecast]

Same format as Figures 64 and 65. The legend entries are "Base", "10 Years", "Linear (Base)" and "Linear (10 Years)" [source discrepancy: the figure title and the text say nine years, while the legend says "10 Years"]. The yellow points fall progressively further below the base points over the reduced years (starting from about 2007, from about 25,500 MW to about 29,300 MW in 2016). The yellow trend line is tilted well clockwise of the base line and projects about 30,500 MW for 2021, compared with about 32,200 MW for the base case, a gap of roughly 1,700-1,800 MW. Values read approximately from the chart.

[→ See original PDF page 421 for visual rendering]

Finally, Figure 67 shows that 15 years of 1,000-MW load reductions lowers the trend line by 1,000 MW, while leaving the slope the same as in the base case. The forecast for 2021 is thus 1,000 MW lower than in the base case.

**Figure 67. Effect of 15 years of demand response on the forecast**

[DIAGRAM DESCRIPTION: Figure 67. Effect of 15 years of demand response on the forecast]

Same format as Figures 64-66; legend "Base", "15 Years", "Linear (Base)", "Linear (15 Years)". Every one of the 15 historical yellow points (2002-2016) lies about 1,000 MW below the corresponding base point (about 23,600 MW in 2002), and the yellow trend line is parallel to the base trend line, about 1,000 MW below it throughout, projecting about 31,200 MW for 2021 against about 32,200 MW for the base case. Values read approximately from the chart.

[→ See original PDF page 421 for visual rendering]

Thus, demand response in some number of the latest years will tend to produce forecast reductions that exceed the annual reductions in the historical data. Beyond some point, additional years of demand response will result in smaller forecast reductions, and once the demand response effect has been in [PDF p. 422 | printed p. 404] effect for the entire study period, the forecast reduction will equal the reduction in the annual input data.

The same pattern would be expected as the reductions are extended to more of the highest-load days in each year.

#### Results for reductions on highest-load days

Not surprisingly, we found that the decreases in the forecast peaks based on load reductions varied with (a) the number of days on which load was reduced each year and (b) the number of years of load reductions in the historical load data. Interestingly, we found that the size of the load reduction had essentially no effect on the ratio of forecasted load reduction to historical load reduction, or as we have named it, the ratio $R$. For example, we observe that if load is reduced 100 MW on the five highest-load days in each of the last five summers in the modeling dataset (2012–2016), the forecast for 2021 would be reduced by 24 MW; if the reductions in the historical load were 1,000 MW, the forecast would be reduced by 240 MW.

For any duration of a load reduction program, the value of $R$ rises with the number of days in which load is reduced, up to at least 35 days. For load reduction programs lasting more than eight years, the value of $R$ begins to fall if the number of days reduced exceeds some threshold; at about 55 days for a 9-year program and at about 40 days for a 15-year program.

However, the value of $R$ did not vary monotonically with respect to either the number of days or the number of years, and $R$ could be more than 1.0, as shown in Figure 68.

For a load reduction program lasting more than two years, reducing load on a large number of days results in $R > 1$, such that the reduction in the load forecast is larger than the reported reduction in the historical load. For a three-year program, $R$ peaks at about 1.1 with reductions in 60 days; programs lasting 8 to 12 years have peak $R$ above 1.8 for about 50 days of reductions; and a program that reduces load in all 15 years used in the forecast would have a value of $R$ over 1.5 for 31 to 46 days of reduction, with $R$ falling rapidly for any additional days.

A program that reduces load for all 62 summer days each year for 15 years has an $R$ value of exactly 1.0. In effect, such a program would look, for peak-forecasting purposes, like a cleared energy efficiency measure.

[PDF p. 423 | printed p. 405]

**Figure 68. Ratio of forecasted load reduction to historical load reduction, various durations**

[DIAGRAM DESCRIPTION: Figure 68. Ratio of forecasted load reduction to historical load reduction, various durations]

A multi-line chart. The x axis is "Days of reduction per year" (tick labels 1, 11, 21, 31, 41, 51, 61; data run from 1 to 62 days); the y axis is "Ratio of reduction (R)", 0.0 to 2.0 in steps of 0.2. There are 15 lines, one per program duration, listed in the legend from top to bottom as 15 Years, 14 Years, 13 Years, 12 Years, 11 Years, 10 Years, 9 Years, 8 Years, 7 Years, 6 Years, 5 Years, 4 Years, 3 Years, 2 Years, 1 Year. Colors run from dark red (1 Year) to progressively lighter red and pink (15 Years). All lines start near 0 at 1 day and rise with the number of days. The 1-year line rises almost linearly to about 0.49 at 62 days; the 2-year line ends near 0.86; the 3-year line ends near 1.12; the 4- and 5-year lines end near 1.4. Lines for 8 to 12 years reach a peak above 1.8 at roughly 45-55 days; the longer-duration lines (13-15 years) peak earlier (the 15-year line peaks at about 1.5 around 40 days) and then fall, the 15-year line ending at exactly 1.0 at 62 days. The chart shows that R rises with the number of days and years but is not monotonic, and that R exceeds 1.0 for many combinations. The underlying values are tabulated in Table 182 (Subappendix A).

_Note: Ratios are shown for 2021 forecasted year._

[→ See original PDF page 423 for visual rendering]

Figure 69 provides the same data, but with the duration of the reduction in years on the $x$ axis and each line representing a number of days of load reduction in each year (essentially swapping the $x$ axis and legend in Figure 68). For readability, we present only a subset of days, rather than the full 62.

The horizontal axis in Figure 69 is the number of years that a load reduction has been in place, as of the last year of historical data for the forecast (year $t - 2$). See Subappendix A. Ratio of forecast reduction to load reduction for the $R$ values from Figure 68 and Figure 69 numerically.

[PDF p. 424 | printed p. 406]

**Figure 69. Ratio of forecast reduction to load reduction, various numbers of peak days per year**

[DIAGRAM DESCRIPTION: Figure 69. Ratio of forecast reduction to load reduction, various numbers of peak days per year]

A multi-line chart. The x axis is "Years of program reduction", 1 to 15; the y axis is "Ratio of reduction (R)", 0.0 to 2.0 in steps of 0.2. Eleven lines in shades of teal (dark teal for few days, light blue-gray for many days), listed in the legend from top to bottom as 62 Days, 50 Days, 40 Days, 35 Days, 30 Days, 25 Days, 20 Days, 15 Days, 10 Days, 5 Days, 1 Day. The 1-day line is nearly flat and low, rising from about 0.01 to about 0.11. The 5-day line rises from about 0.06 to about 0.45; the 10-day line from about 0.12 to about 0.77; the 15-day line from about 0.17 to about 1.02. Lines for 20 or more days rise more steeply, peak at about 12 years (R of about 1.26 for 20 days, about 1.43 to 1.70 for 25 to 35 days, and about 1.78 to 1.84 for 40 to 50 days) and then decline slightly. The 62-day line rises fastest (about 1.4 at 4 years, about 1.8 at 8 years), then falls to exactly 1.0 at 15 years. The chart is the same data as Figure 68 with the axes swapped; the values are tabulated in Table 182 (Subappendix A). Values read approximately from the chart.

[→ See original PDF page 424 for visual rendering]

#### Applying the results to demand response screening and valuation

The results in Figure 68 and Figure 69 can be used in at least two ways.

First, they can be used to screen potential demand response programs by modifying the values used for uncleared capacity and capacity DRIPE. For example, a new program that would first reduce load in 2020, for the top 10 summer days, would be a one-year reduction in the data for the 2021 forecast, which would be used in the 2022 FCA 16 for the summer of 2025. Since we find that a 10-day program has an $R$ value of 0.12, a 200 MW load reduction in 2021 would reduce the forecast peak by 24 MW and produce the DRIPE benefits of that size load reduction. Once the program has run for three years (e.g., 2020–2022), it would create a three-year reduction for the 2023 forecast used in 2024 for FCA 18 for the summer of 2027. The program would have an $R$ value of 0.30, so the FCA forecast for 2027 would be reduced by 60 MW. Similarly, if the program continues to run for 15 years, the reduction in the forecast used for FCA 30 would be 154 MW.

[PDF p. 425 | printed p. 407]

Second, the results can be used retrospectively, to evaluate the effect of a program that has been operating. In 2019, a Program Administrator might file results for a 100-MW program that it ran in 2014–2018, reducing load on the top 15 days of each summer. From Subappendix A. Ratio of forecast reduction to load reduction, we would use the 15-day row and estimate that the program reduced the load used in the FCA forecasts by 17 MW in 2018 (for which 2014 was the last year of data used in the forecast), 31 MW in 2019, 43 MW in 2020, and 58 MW in 2021. The sum of the avoided capacity and DRIPE from those years would be benefits of the program.

#### Sensitivity analysis: Other demand response dispatch approaches

This section describes the results of our analysis under a variety of dispatch and implementation sensitivities, including situations in which demand response is dispatched according to weather or in line with day-ahead forecasts. We also examine situations in which the dispatch of demand response misses some peak days, is performed according to some forecast of load distribution, and in which demand response is dispatched for only a single day each year.

##### Dispatching according to weather, rather than load

Our main analysis assumes that a demand response program identifies the highest-load days and achieves load reduction on those days. We find that the results are essentially identical for a program that concentrates on reducing load on the days with the worst weather (the highest WTHI values), even though those are slightly different from the highest load days.

##### Dispatching demand response with day-ahead forecasts

We find that the results are also very similar if targeting of the demand response is imperfect, such that the program is activated on some days that are not in the $d$ highest days.[^471] For example, the program administrator may call an event on a day that looks like it will be one of the top $d$ days for the summer, but it may turn out to have an actual load lower than expected. Or, it may turn out that there are more higher-load days that occur later in that summer, after the program administrator has called as many days as is allowed by the tariff or contracts.[^472]

Figure 70 shows the accuracy of demand response program dispatch that is called when the day-ahead peak load is expected to be one of the highest $d$ days. These results factor in the optimistic assumption that the program administrator has perfect information about the highest loads for the current summer but not when those highest load days will occur. With this assumption, programs allowing for 5 to 20 days of load reductions would catch 90 percent of the intended control days.

[^471]: Results are similar, but the curves are less smooth.

[^472]: The ISO New England day-ahead forecasts are actually quite accurate, correctly flagging the highest $d$ days of the summer, if the load of the lowest of those days is known.

[PDF p. 426 | printed p. 408]

Where the day-ahead load would result in activation of a day outside the targeted group, it is almost always close to the intended group. For example, a program targeted at the top 10 days might miss day six, but that unused activation would likely be present on day 11 or 12.

**Figure 70. Percentage of highest days flagged by day-ahead load forecast, by year**

[DIAGRAM DESCRIPTION: Figure 70. Percentage of highest days flagged by day-ahead load forecast, by year]

A clustered bar chart. The x axis has eight groups: the years 2012, 2013, 2014, 2015, 2016, 2017, 2018 and "Avg". The y axis is "Percentage of Actual Peak Days Captured in Forecast", 0% to 100% in steps of 10%. Within each group there are six bars, one for each program size, in progressively darker teal: Top 1, Top 3, Top 5, Top 10, Top 20, Top 30 (legend at the bottom). Bar heights (read approximately from the chart; a missing bar means 0%): 2012: Top 1 = 100%, Top 3 about 67%, Top 5 = 100%, Top 10 about 70%, Top 20 about 85%, Top 30 about 87%. 2013: Top 1, Top 3 and Top 5 = 100%, Top 10 about 85%, Top 20 about 100%, Top 30 about 97%. 2014: Top 1, Top 3 = 100%, Top 5 about 90%, Top 10 about 95%, Top 20 and Top 30 about 97%. 2015: Top 1 not shown (0%), Top 3 about 33%, Top 5 = 100%, Top 10 = 100%, Top 20 about 85%, Top 30 about 94%. 2016: Top 1 not shown (0%), Top 3 about 67%, Top 5 about 60%, Top 10 and Top 20 = 80%, Top 30 about 90%. 2017: Top 1 = 100%, Top 3 = 100%, Top 5 about 80%, Top 10 and Top 20 about 90%, Top 30 about 94%. 2018: Top 1 = 100%, Top 3 about 67%, Top 5 about 80%, Top 10 about 90%, Top 20 about 95%, Top 30 about 90%. Avg: Top 1 about 57%, Top 3 about 77%, Top 5 about 89%, Top 10 about 89%, Top 20 about 88%, Top 30 about 93%. The chart shows that day-ahead forecasts capture most, but not all, of the actual highest-load days, with larger programs (Top 5 and above) averaging close to 90 percent.

[→ See original PDF page 426 for visual rendering]

##### Dispatching demand response, missing some days

Figure 70 shows the targeting errors if the program administrator somehow knew what the load would be on day $d$, the lowest load day for which the administrator should activate the program. A more realistic simulation recognizes that the program administrator does not know in early July whether the rest of the summer will be hot or mild, and thus will not know whether a particular day-ahead load forecast is likely to be one the $d$ highest days.

Table 180 shows how close the load reductions would be to the perfect-information case with typical substitution of peak days with days just outside the targeted period. For example, Sensitivity Case 4 tests the effect on load reductions of calling an event on the 14th highest day rather than the 9th day of a 10-day per year program, while Sensitivity Case 5 models the effect of calling an event on the 14th highest day rather than the 6th day. Other than Sensitivity Case 1 (an unlikely single-day program calling an event on the second-highest day, rather than the highest-load day), the effect of the imperfect dispatch is within 6 percent of the effect of perfect dispatch, and sometimes the dispatch error actually increases the reduction in forecast load.

[PDF p. 427 | printed p. 409]

**Table 180. Ratios of forecast reduction with minor dispatch errors, as a percentage of forecast reduction from perfect dispatch**

_Table structure: the PDF header has two levels. "Changes from Optimal Dispatch" spans the columns "Top Days Missed" and "Non-Top Days added"; "Years of Operation" spans the columns 1, 5, 10 and 15. Day numbers (#n) are the rank of the day among the summer's highest-load days._

| Sensitivity Case | Event Days | Changes from Optimal Dispatch: Top Days Missed | Changes from Optimal Dispatch: Non-Top Days added | Years of Operation: 1 | Years of Operation: 5 | Years of Operation: 10 | Years of Operation: 15 |
| ---------------: | ---------: | ---------------------------------------------- | ------------------------------------------------- | --------------------: | --------------------: | ---------------------: | ---------------------: |
|                1 |          1 | #1                                             | #2                                                |                   67% |                   92% |                    92% |                    81% |
|                2 |          3 | #3                                             | #4                                                |                   99% |                  105% |                    99% |                    98% |
|                3 |          5 | #5                                             | #7                                                |                  101% |                  101% |                    98% |                    98% |
|                4 |         10 | #9                                             | #14                                               |                   99% |                   97% |                    98% |                    98% |
|                5 |         10 | #6                                             | #14                                               |                   99% |                   96% |                    98% |                    97% |
|                6 |         20 | #14, #17                                       | #25, #30                                          |                  100% |                   99% |                    98% |                    96% |
|                7 |         20 | #11, #12                                       | #22, #23                                          |                   98% |                   97% |                    97% |                    96% |
|                8 |         20 | #16, #20                                       | #27, #32                                          |                  103% |                  100% |                    98% |                    97% |
|                9 |         31 | #18, #24, #27, #30                             | #34, #37, #40, #43                                |                   96% |                   96% |                    96% |                    94% |
|               10 |         31 | #18, #27, #31                                  | #34, #37, #40                                     |                   98% |                   97% |                    97% |                    95% |

Table 181 shows the results for poorly targeted dispatch of a load reduction program in the top 30 days of the summer, either 10 events per year on every third day (starting with day 1 or day 2) or 15 events per year on every second day (either the even-numbered days or the odd-numbered). These dispatch choices represent nearly the worst cases for 10 or 15 annual events, yet they still produce 62 percent to 92 percent of the forecast reduction due to load reductions perfectly targeted to the 10 or 15 days with highest loads.

**Table 181. Ratios of forecast reduction with even more imperfect dispatch, as a percentage of forecasted reduction from perfect dispatch**

| Event Days | Dispatch Days, Ranked by Load                                   | Years of Operation: 1 | Years of Operation: 5 | Years of Operation: 10 | Years of Operation: 15 |
| ---------: | --------------------------------------------------------------- | --------------------: | --------------------: | ---------------------: | ---------------------: |
|         10 | Every 3rd day: 1, 4, 7, 10, 13, 16, 19, 22, 25, 28              |                   85% |                   78% |                    75% |                    68% |
|         10 | Every 3rd day: 2, 5, 8, 11, 14, 17, 20, 23, 26, 29              |                   73% |                   72% |                    71% |                    62% |
|         15 | Odd days: 1,3, 5, 7, 9, 11,13,15,17,19,21, 23,25, 27, 29        |                   92% |                   84% |                    82% |                    76% |
|         15 | Even days: 2, 4, 6, 8, 10,12,14, 16, 18, 20, 22, 24, 26, 28, 30 |                   84% |                   78% |                    76% |                    68% |

##### Dispatching demand response with forecast load distribution

To examine dispatch errors more systematically, we tested a case in which the program was activated and load was curtailed when the day-ahead forecast was within $k$% of ISO New England’s forecast of the summer peak, where $k$ is the percentage of peak that, on average over the historical data, was exceeded for $d$ days per year.

This is a simplified example of a typical demand response program (such as dynamic peak pricing), in which the program administrator tries to foresee peak days and curtail load on those days. In some low-load years, the program will miss some days that later turn out to have been in the top $d$ days, while in other years, the program will operate on days that turn out not to be in the top $d$ days.

[PDF p. 428 | printed p. 410]

Demand response program administrators are likely to be more sophisticated than the simple algorithm that we used. For example, the program administrator will know how much of the summer remains, how many event days are left for the year, whether the remainder of the summer is forecast to be warmer or cooler than usual, and what a more detailed forecast for the next week or more shows.

Assuming that the program administrator has no information about the loads for the particular year, dispatching with this simple algorithm results in forecast load savings of 80 percent to 100 percent of the perfect-information dispatch, from about four to 50 event days annually. The detailed pattern of differences between the values shown in Subappendix A and Subappendix B may well be due to the different performance of the algorithm in the specific historical years. Overall, a reasonably thoughtful program administrator should be able to achieve about 95 percent of the benefits shown in Subappendix A.

##### Daily dispatch values

Finally, we estimated the effects of load reductions in just a single day each year, from the highest-load day to the lowest-load day of the summer, and for one to 15 years of program operation. The specific effect of reductions in any particular day is probably very sensitive to the specific historical pattern of daily loads and weather, so the detailed differences in the daily values (for example, between the 18th and 19th days, or between seven years and eight years) may not be significant. See Subappendix C [source says "Appendix C"] for our estimate of the $R$ value (reduction in the 2021 forecast as a fraction of the annual historical load reductions), for various number of years and various numbers of days per year.

These daily values, if summed up for the top $d$ days, produce load reductions lower than those we found for reductions in the top $d$ days. This is illustrated in Figure 71, Figure 72, and Figure 73, for programs lasting 1, 5, and 15 years, respectively. In each figure, we plot the sum of the daily contributions to reducing the load forecast (the sum of days) as compared to the reduction from the top days as a group (the optimal dispatch results). The latter is always larger.

[PDF p. 429 | printed p. 411]

**Figure 71. Reduction ratio (R) for 1-year program, various numbers of days**

[DIAGRAM DESCRIPTION: Figure 71. Reduction ratio (R) for 1-year program, various numbers of days]

A two-line chart. The x axis is "Days of reduction per year" (tick labels 1, 11, 21, 31, 41, 51, 61); the y axis is "Ratio of reduction (R)", 0.0 to 1.6 in steps of 0.2. Two lines are labeled directly at the right: "1 year optimal" (light green) and "1 year sum of days" (dark green). Both start near 0 at 1 day. The optimal line rises steadily to about 0.49 at 62 days (matching the 1-year column of Table 182). The sum-of-days line rises more slowly and flattens, reaching only about 0.23 at 62 days, so the sum of the single-day contributions is less than half the optimal group result for a 1-year program. Values read approximately from the chart.

[→ See original PDF page 429 for visual rendering]

**Figure 72. Reduction ratio (R) for 5-year program, various numbers of days**

[DIAGRAM DESCRIPTION: Figure 72. Reduction ratio (R) for 5-year program, various numbers of days]

Same format as Figure 71 (x axis "Days of reduction per year", y axis "Ratio of reduction (R)" 0.0-1.6), with lines labeled "5 year optimal" (light green) and "5 year sum of days" (dark green). The two lines start together near 0.06 at 1 day and track each other closely up to about 15 days, then diverge. The optimal line rises to about 1.4 at 62 days, with a gradually flattening slope (matching the 5-year column of Table 182). The sum-of-days line rises to a plateau of about 1.1 near 50-62 days and edges down slightly at the end. Values read approximately from the chart.

[→ See original PDF page 429 for visual rendering]

[PDF p. 430 | printed p. 412]

**Figure 73. Reduction ratio (R) for 15-year program, various numbers of days**

[DIAGRAM DESCRIPTION: Figure 73. Reduction ratio (R) for 15-year program, various numbers of days]

Same format as Figures 71 and 72, with lines labeled "15 year optimal" (light green) and "15 year sum of days" (dark green). Both lines start near 0.1 at 1 day and rise together. The optimal line peaks at about 1.5 around 35-41 days (matching the 15-year column of Table 182) and then falls to exactly 1.0 at 62 days. The sum-of-days line peaks lower, at about 1.3 around 35-41 days, then falls faster, to about 0.65 at 62 days. The chart shows that the sum of daily contributions is always below the optimal group dispatch result, and that for a 15-year program both measures decline when load is reduced on a large number of days. Values read approximately from the chart.

[→ See original PDF page 430 for visual rendering]

The question then arises, without computing the effects of reductions on all the possible combinations of days (on the order of $10^{18}$ possibilities), how can the effect of some set of load reductions on uncleared capacity and capacity DRIPE be estimated?

We propose that the load effect ($R$) for reductions on a set of days $S$, for which the lowest-load day in $S$ is the $D$th highest load day of the summer, be estimated as the average of

1. The sum of the R values for the days in S (from Table 184, Subappendix C), and
2. The R value for D days (from Table 182, Subappendix A), minus the sum of the R values for the days less than D that are not in S (from Table 184, Subappendix C).

For days 1, 4, and 5 of a one-year program (or a program that has only been running for a year), the value would be the average of

> _The sum of 0.009, 0.013 and 0.005, or 0.027, and_
>
> _0.06 minus (0.010 + 0.006), or 0.044._
>
> _(0.027 + 0.044) ÷ 2 = 0.036._

If greater precision is necessary, or for more complex situations, for example to estimate the effect of different amounts of load reduction on different days over multiple years, we recommend repeating the regressions we describe above for the specific situation.

[PDF p. 431 | printed p. 413]

### Subappendix A. Ratio of forecast reduction to load reduction

Table 182 displays the values behind Figure 68 and Figure 69. These values can be applied to uncleared capacity and capacity DRIPE values from AESC 2024 to determine new capacity DRIPE values that are specific to a demand response program.

**Table 182. Ratio of forecast reduction to load reduction, by years and days per year**

_Table structure: rows are the number of event days per year (Days, 1-62); columns are Years of Reductions (1-15). The table continues on the next PDF page, where the header row is printed again._

| Days |    1 |    2 |    3 |    4 |    5 |    6 |    7 |    8 |    9 |   10 |   11 |   12 |   13 |   14 |   15 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|    1 | 0.01 | 0.02 | 0.03 | 0.05 | 0.05 | 0.06 | 0.07 | 0.08 | 0.08 | 0.09 | 0.10 | 0.10 | 0.10 | 0.11 | 0.11 |
|    2 | 0.03 | 0.05 | 0.06 | 0.09 | 0.10 | 0.13 | 0.14 | 0.15 | 0.16 | 0.17 | 0.18 | 0.19 | 0.20 | 0.20 | 0.20 |
|    3 | 0.04 | 0.07 | 0.10 | 0.13 | 0.15 | 0.17 | 0.20 | 0.22 | 0.23 | 0.25 | 0.26 | 0.28 | 0.28 | 0.29 | 0.29 |
|    4 | 0.05 | 0.09 | 0.13 | 0.17 | 0.19 | 0.23 | 0.26 | 0.29 | 0.30 | 0.32 | 0.34 | 0.36 | 0.36 | 0.37 | 0.37 |
|    5 | 0.06 | 0.11 | 0.16 | 0.22 | 0.24 | 0.28 | 0.32 | 0.35 | 0.37 | 0.39 | 0.41 | 0.44 | 0.44 | 0.44 | 0.45 |
|    6 | 0.07 | 0.13 | 0.19 | 0.25 | 0.28 | 0.32 | 0.37 | 0.41 | 0.43 | 0.45 | 0.48 | 0.50 | 0.50 | 0.50 | 0.52 |
|    7 | 0.08 | 0.15 | 0.22 | 0.29 | 0.33 | 0.38 | 0.43 | 0.47 | 0.49 | 0.51 | 0.54 | 0.57 | 0.57 | 0.57 | 0.58 |
|    8 | 0.09 | 0.17 | 0.25 | 0.33 | 0.36 | 0.42 | 0.48 | 0.53 | 0.55 | 0.57 | 0.61 | 0.64 | 0.64 | 0.63 | 0.65 |
|    9 | 0.10 | 0.19 | 0.27 | 0.37 | 0.40 | 0.47 | 0.53 | 0.58 | 0.61 | 0.63 | 0.67 | 0.70 | 0.70 | 0.69 | 0.71 |
|   10 | 0.12 | 0.21 | 0.30 | 0.41 | 0.45 | 0.52 | 0.58 | 0.63 | 0.66 | 0.69 | 0.72 | 0.76 | 0.75 | 0.75 | 0.77 |
|   11 | 0.13 | 0.23 | 0.33 | 0.45 | 0.48 | 0.55 | 0.63 | 0.68 | 0.71 | 0.74 | 0.78 | 0.82 | 0.81 | 0.80 | 0.82 |
|   12 | 0.14 | 0.25 | 0.35 | 0.48 | 0.52 | 0.59 | 0.67 | 0.73 | 0.76 | 0.79 | 0.83 | 0.87 | 0.86 | 0.86 | 0.88 |
|   13 | 0.15 | 0.27 | 0.38 | 0.52 | 0.55 | 0.64 | 0.72 | 0.78 | 0.81 | 0.85 | 0.88 | 0.93 | 0.92 | 0.91 | 0.93 |
|   14 | 0.16 | 0.29 | 0.40 | 0.54 | 0.58 | 0.68 | 0.76 | 0.83 | 0.86 | 0.89 | 0.93 | 0.97 | 0.96 | 0.95 | 0.97 |
|   15 | 0.17 | 0.31 | 0.43 | 0.58 | 0.62 | 0.71 | 0.80 | 0.87 | 0.90 | 0.94 | 0.98 | 1.03 | 1.01 | 1.00 | 1.02 |
|   16 | 0.18 | 0.33 | 0.45 | 0.60 | 0.65 | 0.75 | 0.84 | 0.91 | 0.95 | 0.98 | 1.02 | 1.07 | 1.06 | 1.04 | 1.06 |
|   17 | 0.19 | 0.34 | 0.47 | 0.63 | 0.68 | 0.78 | 0.88 | 0.95 | 0.99 | 1.02 | 1.07 | 1.12 | 1.10 | 1.08 | 1.10 |
|   18 | 0.20 | 0.36 | 0.50 | 0.66 | 0.70 | 0.81 | 0.91 | 0.99 | 1.03 | 1.07 | 1.11 | 1.17 | 1.15 | 1.13 | 1.14 |
|   19 | 0.20 | 0.38 | 0.52 | 0.69 | 0.73 | 0.84 | 0.95 | 1.04 | 1.07 | 1.11 | 1.15 | 1.21 | 1.19 | 1.17 | 1.18 |
|   20 | 0.21 | 0.39 | 0.54 | 0.71 | 0.77 | 0.88 | 0.99 | 1.07 | 1.11 | 1.15 | 1.20 | 1.26 | 1.23 | 1.21 | 1.22 |
|   21 | 0.22 | 0.41 | 0.56 | 0.74 | 0.80 | 0.92 | 1.03 | 1.12 | 1.16 | 1.20 | 1.24 | 1.30 | 1.27 | 1.25 | 1.26 |
|   22 | 0.23 | 0.42 | 0.58 | 0.77 | 0.82 | 0.94 | 1.06 | 1.15 | 1.19 | 1.23 | 1.27 | 1.33 | 1.30 | 1.28 | 1.29 |
|   23 | 0.24 | 0.44 | 0.60 | 0.79 | 0.85 | 0.96 | 1.09 | 1.19 | 1.23 | 1.27 | 1.31 | 1.37 | 1.34 | 1.31 | 1.32 |
|   24 | 0.25 | 0.45 | 0.62 | 0.82 | 0.87 | 0.98 | 1.12 | 1.21 | 1.26 | 1.29 | 1.34 | 1.40 | 1.36 | 1.33 | 1.34 |
|   25 | 0.25 | 0.47 | 0.64 | 0.84 | 0.89 | 1.01 | 1.15 | 1.25 | 1.29 | 1.33 | 1.37 | 1.43 | 1.40 | 1.36 | 1.37 |
|   26 | 0.27 | 0.49 | 0.66 | 0.86 | 0.91 | 1.04 | 1.18 | 1.28 | 1.32 | 1.36 | 1.40 | 1.47 | 1.42 | 1.39 | 1.39 |
|   27 | 0.28 | 0.50 | 0.68 | 0.89 | 0.95 | 1.07 | 1.22 | 1.32 | 1.36 | 1.40 | 1.44 | 1.50 | 1.46 | 1.42 | 1.42 |
|   28 | 0.29 | 0.52 | 0.71 | 0.92 | 0.97 | 1.11 | 1.25 | 1.35 | 1.39 | 1.43 | 1.47 | 1.53 | 1.48 | 1.44 | 1.44 |
|   29 | 0.30 | 0.54 | 0.73 | 0.94 | 1.00 | 1.14 | 1.28 | 1.38 | 1.42 | 1.46 | 1.49 | 1.56 | 1.51 | 1.46 | 1.46 |
|   30 | 0.30 | 0.55 | 0.74 | 0.96 | 1.02 | 1.15 | 1.31 | 1.41 | 1.45 | 1.49 | 1.52 | 1.58 | 1.53 | 1.48 | 1.47 |
|   31 | 0.31 | 0.56 | 0.76 | 0.98 | 1.04 | 1.18 | 1.33 | 1.44 | 1.48 | 1.51 | 1.54 | 1.61 | 1.55 | 1.49 | 1.48 |
|   32 | 0.32 | 0.58 | 0.78 | 1.00 | 1.06 | 1.21 | 1.36 | 1.47 | 1.50 | 1.54 | 1.57 | 1.63 | 1.57 | 1.51 | 1.49 |
|   33 | 0.32 | 0.59 | 0.79 | 1.02 | 1.07 | 1.22 | 1.38 | 1.49 | 1.53 | 1.56 | 1.59 | 1.66 | 1.59 | 1.52 | 1.50 |
|   34 | 0.33 | 0.60 | 0.80 | 1.04 | 1.09 | 1.25 | 1.41 | 1.52 | 1.55 | 1.59 | 1.61 | 1.68 | 1.60 | 1.53 | 1.51 |
|   35 | 0.34 | 0.61 | 0.82 | 1.06 | 1.11 | 1.27 | 1.43 | 1.54 | 1.58 | 1.61 | 1.63 | 1.70 | 1.62 | 1.54 | 1.51 |
|   36 | 0.35 | 0.62 | 0.84 | 1.08 | 1.13 | 1.29 | 1.46 | 1.57 | 1.60 | 1.63 | 1.65 | 1.71 | 1.63 | 1.55 | 1.52 |
|   37 | 0.35 | 0.64 | 0.85 | 1.10 | 1.16 | 1.31 | 1.49 | 1.59 | 1.62 | 1.65 | 1.67 | 1.73 | 1.65 | 1.57 | 1.53 |
|   38 | 0.36 | 0.65 | 0.86 | 1.12 | 1.17 | 1.34 | 1.51 | 1.61 | 1.64 | 1.67 | 1.69 | 1.75 | 1.66 | 1.58 | 1.53 |
|   39 | 0.37 | 0.66 | 0.88 | 1.14 | 1.19 | 1.35 | 1.53 | 1.63 | 1.66 | 1.69 | 1.71 | 1.77 | 1.67 | 1.58 | 1.53 |
|   40 | 0.37 | 0.67 | 0.89 | 1.15 | 1.21 | 1.36 | 1.55 | 1.65 | 1.68 | 1.71 | 1.72 | 1.78 | 1.68 | 1.59 | 1.53 |
|   41 | 0.38 | 0.68 | 0.90 | 1.17 | 1.22 | 1.39 | 1.57 | 1.67 | 1.69 | 1.72 | 1.73 | 1.79 | 1.68 | 1.59 | 1.53 |
|   42 | 0.39 | 0.69 | 0.92 | 1.19 | 1.23 | 1.41 | 1.59 | 1.69 | 1.71 | 1.73 | 1.74 | 1.80 | 1.69 | 1.59 | 1.52 |

[PDF p. 432 | printed p. 414]

_Table 182 (continued): the PDF repeats the header ("Years of Reductions", "Days 1 ... 15") at the top of this page._

| Days |    1 |    2 |    3 |    4 |    5 |    6 |    7 |    8 |    9 |   10 |   11 |   12 |   13 |   14 |   15 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|   43 | 0.39 | 0.70 | 0.93 | 1.20 | 1.25 | 1.42 | 1.61 | 1.70 | 1.72 | 1.75 | 1.76 | 1.81 | 1.69 | 1.59 | 1.52 |
|   44 | 0.40 | 0.71 | 0.95 | 1.21 | 1.26 | 1.44 | 1.63 | 1.72 | 1.74 | 1.76 | 1.77 | 1.82 | 1.70 | 1.60 | 1.52 |
|   45 | 0.41 | 0.73 | 0.96 | 1.23 | 1.28 | 1.46 | 1.64 | 1.74 | 1.75 | 1.77 | 1.78 | 1.83 | 1.70 | 1.60 | 1.51 |
|   46 | 0.42 | 0.74 | 0.97 | 1.25 | 1.30 | 1.48 | 1.66 | 1.76 | 1.77 | 1.79 | 1.79 | 1.84 | 1.71 | 1.60 | 1.50 |
|   47 | 0.42 | 0.75 | 0.99 | 1.27 | 1.31 | 1.49 | 1.68 | 1.77 | 1.78 | 1.80 | 1.79 | 1.84 | 1.70 | 1.58 | 1.48 |
|   48 | 0.42 | 0.76 | 1.00 | 1.27 | 1.32 | 1.50 | 1.70 | 1.78 | 1.79 | 1.80 | 1.79 | 1.84 | 1.69 | 1.57 | 1.46 |
|   49 | 0.43 | 0.77 | 1.01 | 1.29 | 1.33 | 1.52 | 1.71 | 1.79 | 1.80 | 1.80 | 1.79 | 1.84 | 1.68 | 1.55 | 1.44 |
|   50 | 0.44 | 0.78 | 1.03 | 1.31 | 1.34 | 1.53 | 1.73 | 1.81 | 1.81 | 1.81 | 1.80 | 1.84 | 1.68 | 1.54 | 1.42 |
|   51 | 0.45 | 0.79 | 1.04 | 1.32 | 1.35 | 1.55 | 1.73 | 1.82 | 1.82 | 1.81 | 1.80 | 1.83 | 1.66 | 1.53 | 1.40 |
|   52 | 0.45 | 0.80 | 1.05 | 1.33 | 1.36 | 1.55 | 1.74 | 1.82 | 1.82 | 1.81 | 1.79 | 1.82 | 1.65 | 1.51 | 1.37 |
|   53 | 0.45 | 0.80 | 1.06 | 1.34 | 1.37 | 1.56 | 1.74 | 1.82 | 1.81 | 1.80 | 1.78 | 1.81 | 1.63 | 1.48 | 1.34 |
|   54 | 0.46 | 0.82 | 1.07 | 1.35 | 1.38 | 1.57 | 1.75 | 1.82 | 1.82 | 1.80 | 1.77 | 1.80 | 1.61 | 1.46 | 1.31 |
|   55 | 0.46 | 0.82 | 1.08 | 1.36 | 1.39 | 1.57 | 1.75 | 1.83 | 1.82 | 1.80 | 1.77 | 1.79 | 1.60 | 1.45 | 1.29 |
|   56 | 0.47 | 0.83 | 1.09 | 1.37 | 1.40 | 1.58 | 1.76 | 1.83 | 1.82 | 1.79 | 1.75 | 1.78 | 1.58 | 1.42 | 1.26 |
|   57 | 0.48 | 0.84 | 1.10 | 1.38 | 1.40 | 1.59 | 1.77 | 1.83 | 1.82 | 1.79 | 1.75 | 1.76 | 1.56 | 1.40 | 1.23 |
|   58 | 0.48 | 0.85 | 1.11 | 1.39 | 1.41 | 1.60 | 1.77 | 1.83 | 1.82 | 1.78 | 1.73 | 1.75 | 1.55 | 1.37 | 1.20 |
|   59 | 0.48 | 0.86 | 1.11 | 1.40 | 1.41 | 1.60 | 1.77 | 1.83 | 1.81 | 1.77 | 1.71 | 1.72 | 1.51 | 1.33 | 1.15 |
|   60 | 0.49 | 0.86 | 1.12 | 1.40 | 1.41 | 1.60 | 1.77 | 1.83 | 1.81 | 1.76 | 1.69 | 1.70 | 1.48 | 1.30 | 1.11 |
|   61 | 0.49 | 0.86 | 1.12 | 1.41 | 1.41 | 1.60 | 1.77 | 1.83 | 1.80 | 1.75 | 1.68 | 1.68 | 1.45 | 1.26 | 1.06 |
|   62 | 0.49 | 0.86 | 1.12 | 1.40 | 1.40 | 1.59 | 1.76 | 1.81 | 1.79 | 1.73 | 1.65 | 1.65 | 1.42 | 1.21 | 1.00 |

[PDF p. 433 | printed p. 415]

### Subappendix B. Ratio of forecast reduction to load reduction, with forecast load distribution

Table 183 displays a modified version of the values in Subappendix A, assuming imperfect dispatch. See the main body of Appendix K, subsection “Dispatching demand response with forecast load distribution” for more information.

**Table 183. Ratio of forecast reduction to load reduction, imperfect dispatch**

_Table structure: rows are the number of event days per year (Days, 1-62); columns are Years of Reductions (1-15). The table continues on the next PDF page, where the header row is printed again._

| Days |    1 |    2 |    3 |    4 |    5 |    6 |    7 |    8 |    9 |   10 |   11 |   12 |   13 |   14 |   15 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|    1 | 0.01 | 0.01 | 0.01 | 0.02 | 0.03 | 0.03 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.05 | 0.05 | 0.05 | 0.05 |
|    2 | 0.02 | 0.02 | 0.02 | 0.05 | 0.06 | 0.07 | 0.09 | 0.09 | 0.09 | 0.10 | 0.10 | 0.11 | 0.11 | 0.11 | 0.12 |
|    3 | 0.03 | 0.06 | 0.08 | 0.11 | 0.13 | 0.15 | 0.17 | 0.17 | 0.17 | 0.19 | 0.20 | 0.21 | 0.21 | 0.21 | 0.21 |
|    4 | 0.04 | 0.09 | 0.13 | 0.17 | 0.19 | 0.21 | 0.25 | 0.26 | 0.26 | 0.27 | 0.28 | 0.30 | 0.30 | 0.30 | 0.30 |
|    5 | 0.05 | 0.11 | 0.15 | 0.20 | 0.22 | 0.25 | 0.29 | 0.30 | 0.31 | 0.33 | 0.34 | 0.36 | 0.36 | 0.36 | 0.36 |
|    6 | 0.06 | 0.13 | 0.17 | 0.23 | 0.25 | 0.29 | 0.34 | 0.36 | 0.37 | 0.39 | 0.40 | 0.42 | 0.42 | 0.42 | 0.42 |
|    7 | 0.07 | 0.14 | 0.20 | 0.27 | 0.29 | 0.33 | 0.38 | 0.40 | 0.41 | 0.44 | 0.45 | 0.47 | 0.47 | 0.46 | 0.46 |
|    8 | 0.08 | 0.16 | 0.23 | 0.30 | 0.32 | 0.37 | 0.42 | 0.45 | 0.46 | 0.48 | 0.50 | 0.52 | 0.52 | 0.51 | 0.51 |
|    9 | 0.09 | 0.18 | 0.25 | 0.32 | 0.35 | 0.40 | 0.46 | 0.49 | 0.50 | 0.52 | 0.54 | 0.57 | 0.56 | 0.55 | 0.55 |
|   10 | 0.10 | 0.20 | 0.27 | 0.35 | 0.39 | 0.44 | 0.51 | 0.54 | 0.55 | 0.58 | 0.60 | 0.62 | 0.62 | 0.61 | 0.60 |
|   11 | 0.12 | 0.22 | 0.29 | 0.38 | 0.42 | 0.49 | 0.56 | 0.59 | 0.60 | 0.63 | 0.65 | 0.68 | 0.68 | 0.66 | 0.66 |
|   12 | 0.12 | 0.23 | 0.31 | 0.41 | 0.45 | 0.53 | 0.60 | 0.64 | 0.65 | 0.68 | 0.70 | 0.73 | 0.73 | 0.71 | 0.71 |
|   13 | 0.13 | 0.24 | 0.32 | 0.44 | 0.47 | 0.55 | 0.64 | 0.67 | 0.69 | 0.71 | 0.74 | 0.77 | 0.77 | 0.75 | 0.75 |
|   14 | 0.14 | 0.25 | 0.34 | 0.47 | 0.51 | 0.60 | 0.68 | 0.71 | 0.73 | 0.76 | 0.79 | 0.82 | 0.82 | 0.80 | 0.80 |
|   15 | 0.15 | 0.29 | 0.38 | 0.52 | 0.57 | 0.66 | 0.75 | 0.79 | 0.82 | 0.85 | 0.88 | 0.91 | 0.91 | 0.88 | 0.88 |
|   16 | 0.15 | 0.30 | 0.40 | 0.55 | 0.59 | 0.69 | 0.78 | 0.83 | 0.85 | 0.88 | 0.92 | 0.96 | 0.94 | 0.92 | 0.91 |
|   17 | 0.17 | 0.32 | 0.43 | 0.58 | 0.62 | 0.73 | 0.82 | 0.88 | 0.90 | 0.94 | 0.98 | 1.02 | 1.00 | 0.98 | 0.97 |
|   18 | 0.17 | 0.34 | 0.45 | 0.60 | 0.64 | 0.75 | 0.85 | 0.92 | 0.94 | 0.98 | 1.02 | 1.06 | 1.04 | 1.00 | 0.99 |
|   19 | 0.18 | 0.35 | 0.46 | 0.62 | 0.67 | 0.78 | 0.88 | 0.95 | 0.98 | 1.01 | 1.05 | 1.09 | 1.07 | 1.03 | 1.02 |
|   20 | 0.19 | 0.37 | 0.48 | 0.64 | 0.69 | 0.80 | 0.91 | 0.98 | 1.01 | 1.05 | 1.09 | 1.14 | 1.11 | 1.06 | 1.06 |
|   21 | 0.19 | 0.38 | 0.49 | 0.66 | 0.71 | 0.82 | 0.93 | 1.00 | 1.03 | 1.07 | 1.10 | 1.15 | 1.13 | 1.08 | 1.07 |
|   22 | 0.20 | 0.39 | 0.50 | 0.68 | 0.73 | 0.84 | 0.96 | 1.03 | 1.06 | 1.10 | 1.13 | 1.19 | 1.16 | 1.10 | 1.09 |
|   23 | 0.21 | 0.41 | 0.54 | 0.71 | 0.76 | 0.88 | 1.00 | 1.07 | 1.11 | 1.14 | 1.18 | 1.24 | 1.20 | 1.14 | 1.13 |
|   24 | 0.22 | 0.43 | 0.56 | 0.74 | 0.78 | 0.90 | 1.02 | 1.10 | 1.13 | 1.17 | 1.21 | 1.26 | 1.23 | 1.16 | 1.15 |
|   25 | 0.23 | 0.44 | 0.58 | 0.76 | 0.81 | 0.93 | 1.06 | 1.14 | 1.18 | 1.21 | 1.25 | 1.31 | 1.27 | 1.21 | 1.19 |
|   26 | 0.23 | 0.45 | 0.58 | 0.78 | 0.82 | 0.95 | 1.08 | 1.16 | 1.20 | 1.23 | 1.27 | 1.33 | 1.30 | 1.23 | 1.22 |
|   27 | 0.24 | 0.47 | 0.60 | 0.80 | 0.84 | 0.97 | 1.10 | 1.18 | 1.22 | 1.26 | 1.30 | 1.36 | 1.33 | 1.26 | 1.25 |
|   28 | 0.25 | 0.48 | 0.61 | 0.81 | 0.86 | 0.99 | 1.13 | 1.21 | 1.25 | 1.29 | 1.32 | 1.38 | 1.34 | 1.27 | 1.26 |
|   29 | 0.26 | 0.50 | 0.63 | 0.84 | 0.88 | 1.02 | 1.16 | 1.25 | 1.29 | 1.32 | 1.36 | 1.42 | 1.38 | 1.31 | 1.29 |
|   30 | 0.26 | 0.50 | 0.63 | 0.85 | 0.89 | 1.03 | 1.17 | 1.26 | 1.30 | 1.34 | 1.37 | 1.43 | 1.39 | 1.31 | 1.29 |
|   31 | 0.27 | 0.52 | 0.66 | 0.87 | 0.92 | 1.06 | 1.21 | 1.29 | 1.34 | 1.37 | 1.40 | 1.46 | 1.42 | 1.33 | 1.32 |
|   32 | 0.28 | 0.53 | 0.68 | 0.90 | 0.94 | 1.08 | 1.24 | 1.32 | 1.36 | 1.40 | 1.43 | 1.49 | 1.44 | 1.35 | 1.33 |
|   33 | 0.29 | 0.55 | 0.71 | 0.93 | 0.98 | 1.12 | 1.28 | 1.37 | 1.41 | 1.44 | 1.47 | 1.53 | 1.48 | 1.39 | 1.35 |
|   34 | 0.30 | 0.56 | 0.72 | 0.95 | 1.00 | 1.15 | 1.31 | 1.39 | 1.44 | 1.47 | 1.49 | 1.56 | 1.50 | 1.41 | 1.37 |
|   35 | 0.31 | 0.58 | 0.74 | 0.98 | 1.03 | 1.18 | 1.34 | 1.43 | 1.47 | 1.50 | 1.53 | 1.58 | 1.53 | 1.44 | 1.40 |
|   36 | 0.33 | 0.60 | 0.78 | 1.01 | 1.06 | 1.21 | 1.37 | 1.47 | 1.51 | 1.54 | 1.56 | 1.62 | 1.56 | 1.46 | 1.43 |
|   37 | 0.34 | 0.62 | 0.80 | 1.04 | 1.09 | 1.24 | 1.41 | 1.50 | 1.54 | 1.57 | 1.59 | 1.65 | 1.58 | 1.48 | 1.44 |
|   38 | 0.35 | 0.63 | 0.82 | 1.06 | 1.11 | 1.27 | 1.44 | 1.53 | 1.57 | 1.60 | 1.62 | 1.68 | 1.59 | 1.50 | 1.44 |
|   39 | 0.35 | 0.64 | 0.83 | 1.09 | 1.13 | 1.29 | 1.46 | 1.55 | 1.60 | 1.63 | 1.64 | 1.69 | 1.60 | 1.50 | 1.45 |
|   40 | 0.36 | 0.66 | 0.85 | 1.10 | 1.15 | 1.31 | 1.48 | 1.58 | 1.62 | 1.65 | 1.66 | 1.71 | 1.62 | 1.52 | 1.46 |
|   41 | 0.37 | 0.67 | 0.87 | 1.12 | 1.17 | 1.33 | 1.51 | 1.61 | 1.64 | 1.67 | 1.68 | 1.73 | 1.61 | 1.50 | 1.43 |
|   42 | 0.37 | 0.67 | 0.88 | 1.13 | 1.17 | 1.34 | 1.52 | 1.61 | 1.65 | 1.67 | 1.69 | 1.73 | 1.60 | 1.48 | 1.41 |
|   43 | 0.38 | 0.68 | 0.89 | 1.15 | 1.19 | 1.35 | 1.53 | 1.63 | 1.67 | 1.69 | 1.70 | 1.75 | 1.61 | 1.50 | 1.42 |
|   44 | 0.39 | 0.69 | 0.90 | 1.15 | 1.20 | 1.37 | 1.55 | 1.64 | 1.68 | 1.70 | 1.71 | 1.75 | 1.62 | 1.50 | 1.41 |

[PDF p. 434 | printed p. 416]

_Table 183 (continued): the PDF repeats the header ("Years of Reductions", "Days 1 ... 15") at the top of this page._

| Days |    1 |    2 |    3 |    4 |    5 |    6 |    7 |    8 |    9 |   10 |   11 |   12 |   13 |   14 |   15 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|   45 | 0.39 | 0.70 | 0.92 | 1.18 | 1.21 | 1.39 | 1.57 | 1.67 | 1.70 | 1.73 | 1.73 | 1.77 | 1.64 | 1.52 | 1.42 |
|   46 | 0.40 | 0.71 | 0.93 | 1.19 | 1.23 | 1.40 | 1.59 | 1.70 | 1.73 | 1.75 | 1.75 | 1.79 | 1.66 | 1.54 | 1.44 |
|   47 | 0.40 | 0.72 | 0.94 | 1.20 | 1.24 | 1.41 | 1.60 | 1.71 | 1.74 | 1.76 | 1.76 | 1.79 | 1.65 | 1.53 | 1.43 |
|   48 | 0.41 | 0.73 | 0.95 | 1.21 | 1.24 | 1.41 | 1.60 | 1.71 | 1.73 | 1.76 | 1.75 | 1.78 | 1.63 | 1.50 | 1.40 |
|   49 | 0.41 | 0.74 | 0.96 | 1.22 | 1.26 | 1.43 | 1.62 | 1.73 | 1.75 | 1.78 | 1.77 | 1.80 | 1.65 | 1.51 | 1.40 |
|   50 | 0.42 | 0.75 | 0.97 | 1.23 | 1.27 | 1.44 | 1.64 | 1.74 | 1.76 | 1.79 | 1.78 | 1.80 | 1.64 | 1.50 | 1.38 |
|   51 | 0.42 | 0.76 | 0.98 | 1.25 | 1.28 | 1.46 | 1.65 | 1.76 | 1.78 | 1.81 | 1.79 | 1.82 | 1.65 | 1.51 | 1.38 |
|   52 | 0.43 | 0.78 | 1.01 | 1.28 | 1.31 | 1.49 | 1.68 | 1.79 | 1.81 | 1.82 | 1.80 | 1.82 | 1.66 | 1.51 | 1.38 |
|   53 | 0.45 | 0.79 | 1.02 | 1.30 | 1.33 | 1.51 | 1.70 | 1.81 | 1.83 | 1.85 | 1.82 | 1.84 | 1.67 | 1.52 | 1.38 |
|   54 | 0.45 | 0.80 | 1.03 | 1.31 | 1.34 | 1.52 | 1.71 | 1.82 | 1.84 | 1.85 | 1.83 | 1.84 | 1.68 | 1.52 | 1.37 |
|   55 | 0.46 | 0.81 | 1.05 | 1.32 | 1.34 | 1.52 | 1.71 | 1.82 | 1.83 | 1.84 | 1.80 | 1.82 | 1.64 | 1.47 | 1.32 |
|   56 | 0.46 | 0.82 | 1.06 | 1.33 | 1.35 | 1.53 | 1.73 | 1.83 | 1.84 | 1.84 | 1.80 | 1.81 | 1.63 | 1.46 | 1.30 |
|   57 | 0.47 | 0.83 | 1.07 | 1.34 | 1.36 | 1.54 | 1.73 | 1.83 | 1.84 | 1.84 | 1.79 | 1.80 | 1.62 | 1.44 | 1.27 |
|   58 | 0.47 | 0.84 | 1.08 | 1.35 | 1.37 | 1.56 | 1.75 | 1.84 | 1.85 | 1.85 | 1.80 | 1.81 | 1.62 | 1.44 | 1.26 |
|   59 | 0.47 | 0.83 | 1.08 | 1.35 | 1.36 | 1.54 | 1.73 | 1.81 | 1.80 | 1.76 | 1.72 | 1.72 | 1.53 | 1.34 | 1.16 |
|   60 | 0.48 | 0.85 | 1.09 | 1.37 | 1.37 | 1.56 | 1.73 | 1.81 | 1.80 | 1.77 | 1.72 | 1.72 | 1.52 | 1.34 | 1.14 |
|   61 | 0.48 | 0.85 | 1.10 | 1.38 | 1.39 | 1.57 | 1.73 | 1.81 | 1.79 | 1.76 | 1.71 | 1.71 | 1.48 | 1.28 | 1.08 |
|   62 | 0.49 | 0.86 | 1.12 | 1.39 | 1.39 | 1.58 | 1.75 | 1.82 | 1.80 | 1.76 | 1.69 | 1.69 | 1.45 | 1.26 | 1.04 |

[PDF p. 435 | printed p. 417]

### Subappendix C. Impact of individual day load reductions

Table 184 shows our estimate of the R value (reduction in the 2021 forecast as a fraction of the annual historical load reductions), for various number of years and various numbers of days per year. See the main body of Appendix K, subsection “Daily dispatch values” for more information.

**Table 184. Effect of individual day load reductions on reduction ratios**

_Table structure: rows are single event days ranked by load (Days, 1-62); columns are Years of Reductions (1-15). Each value is the R value for reducing load on that one day alone each year. The table continues on the next PDF page, where the header row is printed again._

| Days |     1 |     2 |     3 |     4 |     5 |     6 |     7 |     8 |     9 |    10 |    11 |    12 |    13 |    14 |    15 |
| ---: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: |
|    1 | 0.009 | 0.021 | 0.032 | 0.046 | 0.051 | 0.063 | 0.072 | 0.079 | 0.082 | 0.089 | 0.096 | 0.102 | 0.104 | 0.106 | 0.108 |
|    2 | 0.010 | 0.021 | 0.031 | 0.040 | 0.046 | 0.056 | 0.064 | 0.073 | 0.078 | 0.081 | 0.081 | 0.086 | 0.086 | 0.086 | 0.087 |
|    3 | 0.006 | 0.016 | 0.025 | 0.036 | 0.040 | 0.047 | 0.056 | 0.062 | 0.065 | 0.069 | 0.074 | 0.080 | 0.080 | 0.080 | 0.083 |
|    4 | 0.013 | 0.024 | 0.035 | 0.046 | 0.050 | 0.056 | 0.063 | 0.069 | 0.070 | 0.067 | 0.081 | 0.083 | 0.075 | 0.075 | 0.077 |
|    5 | 0.005 | 0.016 | 0.026 | 0.036 | 0.038 | 0.044 | 0.050 | 0.055 | 0.058 | 0.060 | 0.064 | 0.067 | 0.066 | 0.066 | 0.068 |
|    6 | 0.011 | 0.014 | 0.020 | 0.038 | 0.041 | 0.046 | 0.052 | 0.050 | 0.052 | 0.053 | 0.057 | 0.061 | 0.059 | 0.058 | 0.060 |
|    7 | 0.005 | 0.013 | 0.022 | 0.033 | 0.034 | 0.040 | 0.047 | 0.052 | 0.054 | 0.054 | 0.056 | 0.060 | 0.059 | 0.058 | 0.059 |
|    8 | 0.007 | 0.022 | 0.024 | 0.035 | 0.036 | 0.045 | 0.052 | 0.055 | 0.056 | 0.059 | 0.060 | 0.062 | 0.062 | 0.061 | 0.063 |
|    9 | 0.004 | 0.013 | 0.021 | 0.031 | 0.034 | 0.039 | 0.044 | 0.049 | 0.053 | 0.054 | 0.055 | 0.057 | 0.055 | 0.054 | 0.053 |
|   10 | 0.012 | 0.014 | 0.021 | 0.032 | 0.030 | 0.038 | 0.043 | 0.047 | 0.048 | 0.050 | 0.050 | 0.052 | 0.051 | 0.051 | 0.053 |
|   11 | 0.006 | 0.014 | 0.020 | 0.027 | 0.027 | 0.032 | 0.038 | 0.042 | 0.043 | 0.046 | 0.048 | 0.050 | 0.048 | 0.047 | 0.047 |
|   12 | 0.004 | 0.013 | 0.020 | 0.027 | 0.029 | 0.035 | 0.040 | 0.045 | 0.047 | 0.049 | 0.050 | 0.051 | 0.050 | 0.048 | 0.049 |
|   13 | 0.013 | 0.022 | 0.027 | 0.033 | 0.036 | 0.041 | 0.045 | 0.049 | 0.049 | 0.052 | 0.045 | 0.048 | 0.047 | 0.046 | 0.045 |
|   14 | 0.009 | 0.010 | 0.017 | 0.023 | 0.031 | 0.028 | 0.033 | 0.037 | 0.038 | 0.038 | 0.039 | 0.042 | 0.039 | 0.037 | 0.043 |
|   15 | 0.004 | 0.013 | 0.018 | 0.024 | 0.027 | 0.032 | 0.036 | 0.039 | 0.040 | 0.041 | 0.044 | 0.046 | 0.044 | 0.042 | 0.041 |
|   16 | 0.002 | 0.010 | 0.016 | 0.022 | 0.023 | 0.029 | 0.033 | 0.036 | 0.037 | 0.039 | 0.039 | 0.041 | 0.039 | 0.036 | 0.036 |
|   17 | 0.004 | 0.011 | 0.016 | 0.021 | 0.023 | 0.027 | 0.031 | 0.033 | 0.035 | 0.036 | 0.038 | 0.041 | 0.038 | 0.034 | 0.033 |
|   18 | 0.009 | 0.012 | 0.023 | 0.024 | 0.023 | 0.027 | 0.031 | 0.036 | 0.036 | 0.037 | 0.037 | 0.039 | 0.040 | 0.038 | 0.037 |
|   19 | 0.010 | 0.017 | 0.023 | 0.023 | 0.031 | 0.026 | 0.032 | 0.036 | 0.037 | 0.037 | 0.036 | 0.038 | 0.033 | 0.031 | 0.030 |
|   20 | 0.006 | 0.012 | 0.012 | 0.018 | 0.020 | 0.023 | 0.029 | 0.031 | 0.034 | 0.036 | 0.037 | 0.039 | 0.037 | 0.034 | 0.035 |
|   21 | 0.004 | 0.011 | 0.017 | 0.023 | 0.025 | 0.029 | 0.033 | 0.036 | 0.038 | 0.037 | 0.037 | 0.039 | 0.039 | 0.035 | 0.037 |
|   22 | 0.004 | 0.010 | 0.014 | 0.021 | 0.019 | 0.022 | 0.025 | 0.028 | 0.027 | 0.028 | 0.026 | 0.027 | 0.024 | 0.024 | 0.026 |
|   23 | 0.001 | 0.009 | 0.015 | 0.020 | 0.021 | 0.024 | 0.027 | 0.030 | 0.030 | 0.029 | 0.028 | 0.032 | 0.028 | 0.024 | 0.022 |
|   24 | 0.007 | 0.012 | 0.010 | 0.015 | 0.014 | 0.016 | 0.019 | 0.022 | 0.022 | 0.022 | 0.028 | 0.023 | 0.019 | 0.016 | 0.019 |
|   25 | 0.008 | 0.015 | 0.018 | 0.021 | 0.023 | 0.024 | 0.028 | 0.030 | 0.027 | 0.028 | 0.026 | 0.027 | 0.024 | 0.023 | 0.021 |
|   26 | 0.006 | 0.013 | 0.018 | 0.016 | 0.018 | 0.021 | 0.026 | 0.028 | 0.027 | 0.026 | 0.026 | 0.027 | 0.023 | 0.019 | 0.018 |
|   27 | 0.005 | 0.012 | 0.017 | 0.024 | 0.025 | 0.027 | 0.030 | 0.032 | 0.031 | 0.031 | 0.031 | 0.031 | 0.028 | 0.027 | 0.025 |
|   28 | 0.003 | 0.009 | 0.021 | 0.021 | 0.025 | 0.024 | 0.026 | 0.032 | 0.025 | 0.024 | 0.021 | 0.021 | 0.017 | 0.013 | 0.009 |
|   29 | 0.001 | 0.008 | 0.013 | 0.017 | 0.017 | 0.023 | 0.026 | 0.026 | 0.025 | 0.025 | 0.023 | 0.023 | 0.022 | 0.016 | 0.012 |
|   30 | 0.002 | 0.009 | 0.012 | 0.015 | 0.015 | 0.017 | 0.021 | 0.021 | 0.020 | 0.020 | 0.018 | 0.017 | 0.013 | 0.008 | 0.003 |

[PDF p. 436 | printed p. 418]

_Table 184 (continued): the PDF repeats the header ("Years of Reductions", "Days 1 ... 15") at the top of this page._

| Days |      1 |      2 |      3 |      4 |      5 |      6 |      7 |      8 |      9 |     10 |     11 |     12 |     13 |     14 |     15 |
| ---: | -----: | -----: | -----: | -----: | -----: | -----: | -----: | -----: | -----: | -----: | -----: | -----: | -----: | -----: | -----: |
|   31 |  0.002 |  0.013 |  0.016 |  0.014 |  0.013 |  0.016 |  0.019 |  0.021 |  0.020 |  0.020 |  0.019 |  0.019 |  0.014 |  0.009 |  0.005 |
|   32 |  0.008 |  0.007 |  0.010 |  0.015 |  0.015 |  0.016 |  0.020 |  0.021 |  0.021 |  0.020 |  0.017 |  0.018 |  0.014 |  0.010 |  0.005 |
|   33 |  0.000 |  0.005 |  0.007 |  0.011 |  0.012 |  0.015 |  0.018 |  0.020 |  0.020 |  0.019 |  0.018 |  0.018 |  0.012 |  0.009 |  0.005 |
|   34 |  0.006 |  0.005 |  0.013 |  0.018 |  0.018 |  0.021 |  0.024 |  0.025 |  0.024 |  0.023 |  0.013 |  0.013 |  0.008 |  0.005 | -0.001 |
|   35 |  0.009 |  0.015 |  0.018 |  0.022 |  0.021 |  0.017 |  0.019 |  0.018 |  0.016 |  0.016 |  0.013 |  0.013 |  0.008 |  0.005 |  0.000 |
|   36 |  0.002 |  0.006 |  0.010 |  0.015 |  0.015 |  0.016 |  0.019 |  0.018 |  0.016 |  0.015 |  0.013 |  0.012 |  0.008 |  0.004 |  0.002 |
|   37 | -0.001 |  0.006 |  0.009 |  0.014 |  0.015 |  0.018 |  0.020 |  0.018 |  0.016 |  0.015 |  0.014 |  0.014 |  0.009 |  0.007 |  0.002 |
|   38 | -0.001 |  0.005 |  0.007 |  0.018 |  0.018 |  0.015 |  0.016 |  0.016 |  0.016 |  0.015 |  0.013 |  0.012 |  0.009 |  0.005 | -0.001 |
|   39 |  0.000 |  0.005 |  0.008 |  0.011 |  0.010 |  0.012 |  0.014 |  0.012 |  0.012 |  0.011 |  0.010 |  0.008 |  0.002 |  0.000 | -0.006 |
|   40 | -0.001 |  0.005 |  0.009 |  0.012 |  0.010 |  0.010 |  0.013 |  0.013 |  0.012 |  0.010 |  0.008 |  0.008 |  0.002 | -0.002 | -0.008 |
|   41 |  0.001 |  0.006 |  0.009 |  0.011 |  0.011 |  0.014 |  0.015 |  0.014 |  0.012 |  0.012 |  0.010 |  0.008 |  0.002 | -0.002 | -0.006 |
|   42 |  0.008 |  0.005 |  0.008 |  0.010 |  0.008 |  0.010 |  0.012 |  0.010 |  0.008 |  0.005 |  0.003 |  0.002 | -0.004 | -0.008 | -0.015 |
|   43 |  0.001 |  0.005 |  0.006 |  0.007 |  0.008 |  0.012 |  0.013 |  0.013 |  0.010 |  0.008 |  0.006 |  0.004 |  0.000 | -0.003 | -0.010 |
|   44 |  0.008 |  0.013 |  0.007 |  0.016 |  0.011 |  0.013 |  0.015 |  0.012 |  0.011 |  0.010 |  0.007 |  0.006 |  0.003 | -0.001 | -0.008 |
|   45 |  0.001 |  0.005 |  0.007 |  0.009 |  0.009 |  0.011 |  0.012 |  0.009 |  0.006 |  0.003 |  0.003 | -0.001 | -0.007 | -0.009 | -0.016 |
|   46 |  0.007 |  0.005 |  0.008 |  0.011 |  0.012 |  0.012 |  0.015 |  0.014 |  0.011 |  0.009 |  0.008 |  0.005 | -0.001 | -0.006 | -0.011 |
|   47 |  0.001 |  0.005 |  0.009 |  0.010 |  0.009 |  0.011 |  0.011 |  0.008 |  0.005 |  0.001 | -0.004 | -0.007 | -0.013 | -0.019 | -0.026 |
|   48 | -0.001 |  0.003 |  0.004 |  0.005 |  0.002 |  0.004 |  0.009 |  0.007 |  0.005 |  0.001 | -0.002 | -0.004 | -0.011 | -0.018 | -0.026 |
|   49 | -0.002 |  0.003 |  0.008 |  0.011 |  0.008 |  0.009 |  0.008 |  0.006 |  0.003 | -0.001 | -0.005 | -0.007 | -0.013 | -0.018 | -0.023 |
|   50 |  0.001 |  0.004 |  0.007 |  0.008 |  0.007 |  0.009 |  0.007 |  0.005 |  0.004 | -0.001 | -0.004 | -0.008 | -0.012 | -0.018 | -0.026 |
|   51 |  0.007 |  0.011 |  0.014 |  0.013 |  0.010 |  0.012 |  0.009 |  0.006 |  0.004 | -0.005 | -0.008 | -0.011 | -0.018 | -0.023 | -0.031 |
|   52 | -0.001 |  0.002 |  0.003 |  0.003 |  0.000 |  0.001 | -0.001 | -0.001 | -0.004 | -0.009 | -0.011 | -0.013 | -0.019 | -0.024 | -0.029 |
|   53 | -0.002 |  0.001 |  0.002 |  0.003 |  0.001 |  0.001 | -0.001 | -0.005 | -0.008 | -0.013 | -0.018 | -0.021 | -0.026 | -0.033 | -0.041 |
|   54 |  0.000 |  0.004 |  0.004 |  0.005 |  0.003 |  0.002 |  0.000 | -0.003 | -0.007 | -0.010 | -0.015 | -0.019 | -0.024 | -0.027 | -0.034 |
|   55 | -0.002 |  0.002 |  0.003 |  0.006 |  0.003 |  0.005 |  0.003 |  0.003 |  0.001 | -0.005 | -0.008 | -0.010 | -0.016 | -0.021 | -0.027 |
|   56 |  0.004 |  0.001 |  0.003 |  0.004 |  0.001 |  0.000 | -0.001 | -0.005 | -0.007 | -0.013 | -0.019 | -0.023 | -0.021 | -0.027 | -0.034 |
|   57 | -0.001 |  0.001 |  0.003 |  0.003 |  0.000 |  0.000 |  0.000 | -0.003 | -0.005 | -0.010 | -0.013 | -0.018 | -0.024 | -0.030 | -0.038 |
|   58 | -0.002 |  0.001 |  0.002 |  0.003 |  0.000 | -0.001 | -0.003 | -0.008 | -0.010 | -0.013 | -0.018 | -0.021 | -0.025 | -0.029 | -0.036 |
|   59 |  0.004 | -0.001 | -0.001 | -0.001 | -0.006 | -0.007 | -0.009 | -0.011 | -0.014 | -0.021 | -0.028 | -0.032 | -0.039 | -0.045 | -0.051 |
|   60 |  0.002 |  0.004 | -0.002 | -0.001 | -0.004 | -0.003 | -0.004 | -0.008 | -0.011 | -0.017 | -0.024 | -0.028 | -0.035 | -0.042 | -0.050 |
|   61 | -0.005 | -0.003 |  0.006 | -0.001 | -0.005 |  0.002 | -0.007 | -0.009 | -0.004 | -0.018 | -0.025 | -0.029 | -0.038 | -0.047 | -0.055 |
|   62 |  0.000 | -0.001 | -0.002 | -0.003 | -0.009 | -0.013 | -0.014 | -0.018 | -0.022 | -0.029 | -0.037 | -0.040 | -0.048 | -0.058 | -0.068 |
