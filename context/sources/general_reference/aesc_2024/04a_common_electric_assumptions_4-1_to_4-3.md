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
extraction_scope: "partial: PDF pp. 82-122 (printed pp. 64-104), Chapter 4 Common Electric Assumptions, sections 4.1 (modeling framework), 4.2 (counterfactuals) and 4.3 (system demand and energy components); PDF p. 122 only up to the heading of section 4.4; the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Opening of Chapter 4 (assumptions common to avoided electric energy, capacity and RPS compliance costs): the EnCompass, REMO and FCM modeling framework and temporal resolution (4.1); the six counterfactuals and two sensitivities and which demand-side components each includes (4.2); and the New England demand forecast components (4.3): conventional load, energy efficiency, demand response, behind-the-meter storage, building electrification, transportation electrification, distributed generation, T&D loss factors, and aggregate annual and peak load impacts."
why_here: "Shows what load, load shape, loss-factor and DER (heat pump, EV, storage) assumptions sit behind the AESC avoided-cost streams that New England rate cases use as marginal energy and capacity costs, including the heat pump load build-up and the shift to winter peaking."
---

_Extractor note (not source text): this file holds PDF pp. 82-122 (printed pp. 64-104) of AESC 2024, Chapter 4 (Common Electric Assumptions), sections 4.1 to 4.3; the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. Chart values in the `[DIAGRAM DESCRIPTION]` blocks are read off the figures and are approximate. Source typos are kept and flagged `[sic]`; underlined words in the source (list lead-ins, a few table words) are shown with `<u>` tags._

[PDF pp. 1-81 not transcribed: cover, front matter, table of contents, Chapter 1 (Executive Summary), Chapter 2 (Avoided Natural Gas Costs) and Chapter 3 (Fuel Oil and Other Fuel Costs), in the other files of this folder (see README.md)]

[PDF p. 82 | printed p. 64]

# 4. Common Electric Assumptions

The following section contains input assumptions that are common to the calculations of avoided electric energy, avoided electric capacity, and avoided RPS compliance.

One of the main tasks of AESC 2024 is to estimate the electricity supply costs that would be avoided by reducing retail sales of electricity through energy efficiency initiatives or other emerging demand-side management (DSM) programs. It includes methodologies, assumptions, and sources relating to the modeling frameworks, electricity demand, transmission, renewable policies, generic resource additions, known and anticipated resource additions, and known and anticipated resource retirements.

In addition to differences in underlying natural gas prices and fuel oil prices (discussed in Chapter 2: _Avoided Natural Gas Costs_ and Chapter 3: _Fuel Oil and Other Fuel Costs_, respectively) modeling assumptions in AESC 2024 differ from those used in AESC 2021 in terms of the following:

- Examination of different load trajectories under four counterfactual scenarios
- Lower projections for annual sales (not including impacts associated with building or transportation electrification)
- Inclusion of impacts of transportation electrification in all four counterfactual scenarios
- Updated assumptions on clean energy additions, including substantial updates to new long-term contracting requirements (e.g., for offshore wind and other renewables), modifications to online dates for certain clean energy projects, and updates of other renewable policies including RPS
- Updated assumptions for known and estimated unit retirements as well as unit additions
- Lower projections for compliance prices under RGGI
- A new capacity accreditation framework reflecting ISO New England's Resource Capacity Accreditation (RCA) project that would accredit resources based on their modeled marginal reliability value

## 4.1. AESC 2024 modeling framework

The wholesale energy markets in New England are managed by ISO New England. There are two primary energy markets: (1) the Day-Ahead Market (where the majority of transactions occur) and (2) the Real-Time Market, in which ISO New England balances the remaining differences in energy supplies and demand.[^68] On average, prices in these two markets are typically close to one another, although there is

[^68]: For more information, see: ISO New England Inc. Internal Market Monitor. 2023. _2022 Annual Markets Report_. Available at: [https://www.iso-ne.com/static-assets/documents/2023/06/2022-annual-markets-report.pdf](https://www.iso-ne.com/static-assets/documents/2023/06/2022-annual-markets-report.pdf).

[PDF p. 83 | printed p. 65]

a tendency for greater volatility in the Real-Time Market. ISO New England also manages a capacity market, which is an auction-based system that ensures the New England power system has sufficient resources to meet future demand for electricity. Forward Capacity Auctions (FCA) are held each year, three years in advance of a specified future operating period. ISO New England also manages other ancillary markets, including regulation and reserve markets.

AESC 2024 uses three models to concurrently forecast avoided energy market and capacity costs. These models include:

### The EnCompass model

Developed by Anchor Power Solutions, EnCompass is a single, fully integrated power system platform that allows for utility-scale generation planning and operations analysis. EnCompass is an optimization model that covers all facets of power system planning, including the following:

- Short-term scheduling, including detailed unit commitment and economic dispatch
- Mid-term energy budgeting analysis, including maintenance scheduling and risk analysis
- Long-term integrated resource planning, including capital project optimization and environmental compliance
- Market price forecasting for energy, ancillary services, capacity, and environmental programs

EnCompass provides unit-specific, detailed forecasts of the composition, operations, and costs of the regional generation fleet given the assumptions described in this document. Synapse has populated the model using the _EnCompass National Database_, created by Horizons Energy. Horizons Energy benchmarked its comprehensive dataset across the 21 North American Electric Reliability Corporation (NERC) Assessment Areas and it incorporates market rules and transmission constructs across 76 distinct zonal pricing points. Synapse uses EnCompass to optimize the generation mix in New England and to estimate the costs of a changing energy system over time, absent any incremental energy efficiency or DSM measures. More information on EnCompass and the Horizons dataset is available at [www.anchor-power.com](http://www.anchor-power.com/).

#### EnCompass modeling topology

EnCompass, like other production-cost and capacity-expansion models, represents load and generation by mapping regional projections for system demand and specific generating units to aggregated geographical regions. These load and generation areas are then linked by transmission areas to create an aggregated balancing area. Table 37 shows load and generation areas reported on in AESC 2024 and Table 38 details modeled load and generation areas. This is the same modeling topology as that used in AESC 2021. For AESC 2024, we use load-weighted averages to translate modeling zones into reporting zones. While some zones under each topology are close matches, other reporting comprise a number of different modeling zones. The percentages for weighting percentages are based on locations of pnodes

[PDF p. 84 | printed p. 66]

in specific states and modeling zones (see Table 39).[^69] These weighting percentages are updated with 2022 nodal data that are similar, but not identical to, the weightings used in AESC 2021 (which was based on 2019 nodal data).

**Table 37. Reporting zones in AESC 2024**

| Zone | AESC Reporting Zones                               |
| ---- | -------------------------------------------------- |
| 1    | Maine                                              |
| 2    | Vermont                                            |
| 3    | New Hampshire                                      |
| 4    | Connecticut                                        |
| 4a   | Southwest Connecticut (including Norwalk-Stamford) |
| 4b   | Rest of Connecticut (Northeast)                    |
| 5    | Rhode Island                                       |
| 6    | Massachusetts                                      |
| 6a   | SEMA (Southeastern Massachusetts)                  |
| 6b   | WCMA (West-Central Massachusetts)                  |
| 6c   | NEMA (Northeastern Massachusetts)                  |

_Extractor note (not source text): the first column of Table 37 has no printed header._

**Table 38. Modeled load zones in AESC 2024**

| EnCompass Region           | ISO New England sub-area |
| -------------------------- | ------------------------ |
| NE Maine Northeast         | BHE                      |
| NE Maine West Central      | ME                       |
| NE Maine Southeast         | SME                      |
| NE New Hampshire           | NH                       |
| NE Vermont                 | VT                       |
| NE Boston                  | Boston                   |
| NE Massachusetts Central   | CMA/NEMA                 |
| NE Massachusetts West      | WMA                      |
| NE Massachusetts Southeast | SEMA                     |
| NE Rhode Island            | RI                       |
| NE Connecticut Northeast   | CT                       |
| NE Connecticut Southwest   | SWCT                     |
| NE Norwalk Stamford        | NOR                      |

[^69]: Pnode load factors for 2022 are available on the ISO New England website. ISO New England Inc. "Nodal Load Weights." _Energy, Load and Demand Reports_. Available at: [https://www.iso-ne.com/isoexpress/web/reports/load-and-demand/-/tree/nodal-load-wgts](https://www.iso-ne.com/isoexpress/web/reports/load-and-demand/-/tree/nodal-load-wgts).

[PDF p. 85 | printed p. 67]

**Table 39. Translation between EnCompass modeling zones (vertical) and AESC 2024 reporting zones (horizontal)**

| EnCompass modeling zone  | ISO New England sub-area | ME  | NH  | RI  | VT  | All CT | SW CT | NE CT | All MA | SE MA | NE MA | WC MA |
| ------------------------ | ------------------------ | --- | --- | --- | --- | ------ | ----- | ----- | ------ | ----- | ----- | ----- |
| NE Maine Northeast       | BHE                      | 15% | -   | -   | -   | -      | -     | -     | -      | -     | -     | -     |
| NE Maine West Central    | ME                       | 50% | -   | -   | -   | -      | -     | -     | -      | -     | -     | -     |
| NE Maine Southeast       | SME                      | 35% | -   | -   | -   | -      | -     | -     | -      | -     | -     | -     |
| NE New Hampshire         | NH                       | -   | 82% | -   | 4%  | -      | -     | -     | -      | -     | -     | -     |
| NE Vermont               | VT                       | -   | 15% | -   | 90% | -      | -     | -     | -      | -     | -     | -     |
| NE Boston                | Boston                   | -   | -   | -   | -   | -      | -     | -     | 46%    | -     | 100%  | 1%    |
| NE Mass. Central         | CMA/NEMA                 | -   | 3%  | -   | -   | -      | -     | -     | 13%    | -     | -     | 46%   |
| NE Mass. West            | WMA                      | -   | -   | -   | 6%  | 1%     | -     | 2%    | 15%    | -     | -     | 53%   |
| NE Mass. Southeast       | SEMA                     | -   | -   | 12% | -   | -      | -     | -     | 20%    | 77%   | -     | -     |
| NE Rhode Island          | RI                       | -   | -   | 88% | -   | -      | -     | -     | 6%     | 23%   | -     | -     |
| NE Connecticut Northeast | CT                       | -   | -   | -   | -   | 49%    | -     | 98%   | -      | -     | -     | -     |
| NE Connecticut Southwest | SWCT                     | -   | -   | -   | -   | 33%    | 66%   | -     | -      | -     | -     | -     |
| NE Norwalk Stamford      | NOR                      | -   | -   | -   | -   | 17%    | 34%   | -     | -      | -     | -     | -     |

_Notes: Totals may not sum to 100 percent due to rounding._

_Extractor note (not source text): in the printed table the first two columns (modeling zone name and ISO New England sub-area) have no column headers; the headers given here are descriptive. Column headings in the PDF are two-line (e.g. "All" over "CT"); they are shown here as "All CT", "SW CT", "NE CT", "All MA", "SE MA", "NE MA" and "WC MA"._

Neighboring regions modeled in this study are New York, Quebec, and the Maritime Provinces. These regions are not represented with unit-specific resolution. Instead, they are represented as a source or sink of import-export flows across existing interfaces in order to reduce modeling run time.[^70]

[^70]: In this analysis, the Maritimes zone includes Versant Power's Maine Public District territory and Eastern Maine Electric Cooperative (EMEC) which are not part of ISO New England and, therefore, are not included in any of the New England pricing zones used in this study. These regions are not modeled as part of the Maine pricing zone and were modeled as part of the New Brunswick transmission area.

[PDF p. 86 | printed p. 68]

### The Renewable Energy Market Outlook model

In addition to EnCompass, AESC 2024 uses Sustainable Energy Advantage's New England Renewable Energy Market Outlook (REMO), a set of models developed by Sustainable Energy Advantage that estimate forecasts of scenario-specific renewable energy buildouts, as well as REC and clean energy certificate (CEC) price forecasts. Within REMO, Sustainable Energy Advantage can define forecasts for both near-term and long-term project buildout and REC pricing.

Near-term renewable builds are defined as projects under development that are in the advanced stages of permitting and have either identified long-term power purchasers or an alternative path to securing financing. These projects are subject to customized, probabilistic adjustments to account for deployment timing and likelihood of achieving commercial operation. The near-term REC price forecasts are a function of existing, RPS-certified renewable energy supplies, near-term renewable builds, regional RPS demand, alternative compliance payment (ACP) levels in each market, and other dynamic factors. Such factors include banking, borrowing, imports, and discretional curtailment of renewable energy.

The long-term REC price forecasts are based on a supply curve analysis taking into account technical potential, resource cost, and market value of production over the study period. These factors are used to identify the marginal, REC price-setting resource for each year in which new renewable energy builds are called upon. The long-term REC price forecast is estimated to be the marginal cost of entry for each year, meaning the premium requirement for the most expensive renewable generation unit deployed for a given year.

### The FCM model

AESC 2024 uses a spreadsheet model to develop FCM auction prices for power years from June 2024 through May 2028. Projections of prices during this period are based on recent FCA clearing prices, adjusted to reflect the load assumptions used in the relevant counterfactual (e.g., whether or not the counterfactual contains energy efficiency measures). We coordinate the major input assumptions regarding the forecasts of peak load and available capacity in each power year with the input assumptions used in the Encompass energy market simulation model. General assumptions for this model include the assumption that resources generally continue to bid FCM capacity in a manner similar to their bidding in FCA 14 through FCA 17 and the assumption that the supply curve in future FCAs features similar slopes to FCA 17. See Chapter 5: _Avoided Capacity Costs_ for more detail on the methodology.

### Modeled market rules

The EnCompass model approximates the market rules used in ISO New England. The following sections provide an overview of the model's approach to these rules.

[PDF p. 87 | printed p. 69]

#### Marginal-cost bidding

In deregulated markets, generation units are assumed to bid marginal cost (opportunity cost of fuel plus variable O&M costs plus opportunity cost of tradable permits). The model prices are based on such representative marginal costs. Notably, the model calculates bid adders to close any gap between energy market revenues and submitted bids. The resulting energy-price outputs are benchmarked against historical and future prices.

#### Capacity accreditation and capacity requirements

The capacity market helps guide resource additions and retirements in New England, and it satisfies the region's resource adequacy objectives by procuring sufficient capacity resources. The constraint to ensure a reliable system is the Installed Capacity Requirement (ICR) and the value that each resource contributes toward the total capacity objective is each resource's accredited capacity. Beginning in June 2028, resources will be accredited based on their Qualified Marginal Reliability Impact Capacity (QMRIC), as proposed in ISO New England's Resource Capacity Accreditation (RCA) project. In AESC 2024, we calculate approximate ICR and QMRIC values based on the latest available ISO proposed methodologies and use these values in EnCompass to (1) ensure the model builds a resource mix that meets system reliability needs and (2) calculate capacity prices. Both capacity accreditation and capacity requirements are determined on a seasonal basis. For the near term through May 2028, before the RCA rules become effective, current estimates of the reserve-margin and installed-capacity requirement (with and without the Hydro Quebec installed-capacity credits) are described in Chapter 5: _Avoided Capacity Costs._

#### Ancillary services

EnCompass allows users to define generating units based on each unit's ability to participate in various ancillary services markets including Regulation, Spinning Reserves, and Non-Spinning Reserves. The model allows users to specify these abilities for each unit, at varying levels of granularity. EnCompass allows units to contribute to contingency and reserve requirements, and it considers applicable costs when determining bids.

#### Day-Ahead Ancillary Services Initiative

ISO New England proposed a package of new day-ahead reserve products through its _Day-Ahead Ancillary Services_ (DASI) proposal to ensure the day-ahead market clears a set of resources that can meet real-time needs and to increase incentives for resources to be available in real time (including by procuring fuel). The proposal utilized call options on energy, which have not been used in other regional transmission organizations, to address what the ISO describes as a "misaligned incentives problem" under the current market rules. The NEPOOL Participants Committee voted in favor of the proposal on August 3, and the proposal will now be filed with and reviewed by FERC. We recommend that any future impacts attributed to DASI be incorporated outside of the AESC study.

[PDF p. 88 | printed p. 70]

### Modeling timescale

In EnCompass, REMO, and the FCM Model, we explicitly model 27 years from 2024 through 2050. In order to develop 30-year levelized avoided costs, AESC 2024 continues the trajectory of each avoided cost component through 2065.[^71]

For each modeled year, we use the temporal resolutions described below.

#### _For avoided energy costs:_

- We first model each year in EnCompass' capacity-expansion construct. In this construct, EnCompass optimizes to determine the most cost-effective capacity additions.[^72] EnCompass is set to optimize over the full study period (2024–2050).[^73] We run EnCompass at the resolution of a typical week. This means that EnCompass represents each year from 2024 to 2050 as an aggregation of 12 months, each of which is represented by a typical week, each week of which is represented by five "on peak" days and two "off peak days," and each day of which is represented by a 24-hour chronological dispatch period.
- After running EnCompass in the capacity-expansion construct, we next run it in production-cost mode for a subset of years. EnCompass' production-cost mode uses the capacity-expansion outputs as "seed" data, and it allows the model to better approximate unit commitment over the course of a year. In this construct, we use an 8,760-hour resolution for each year between 2024 and 2050.
- Hourly 8,760 data are then aggregated using load-weighted averages to the four time periods used for reporting in previous AESC studies (summer on-peak, summer off-peak, winter on-peak, and winter off-peak).[^74]

#### _For avoided capacity costs:_

- Program administrators can claim avoided capacity by either bidding capacity (cleared) into the capacity auctions, or by reducing loads through non-bid capacity (uncleared)

[^71]: In all cases, this involves extrapolating values through 2065. See _Appendix A: Usage Instructions_ for the methodology used.

[^72]: Note that these capacity additions are limited to generic resource types (described below). Note that we enter other capacity as exogenous additions.

[^73]: In AESC 2021, we selected a five-year optimization horizon because this is roughly the horizon used to conceptualize and build large power plant projects (the FCM has a three-year horizon, but projects are conceptualized and qualified in the market at least one year [and possibly more years] before each auction). Earlier AESC studies typically used one-year optimization horizons, largely because of computing power limitations. When comparing resulting avoided costs in AESC 2024 with earlier studies that used different optimization periods, the most likely impact of this change in optimization horizon is to reduce "noise." In other words, this change is unlikely to cause avoided costs to be lower or higher but is more likely to reduce the year-on-year variation in costs.

[^74]: These time periods are defined by ISO New England as follows: Winter on-peak is October through May, weekdays from 7am to 11pm; winter off-peak is October through May, weekdays from 11 p.m. to 7 a.m., plus weekends and holidays; summer on-peak is June through September, weekdays from 7 a.m. to 11 p.m.; and summer off-peak is June through September, weekdays from 11 p.m. to 7 a.m., plus weekends and holidays.

[PDF p. 89 | printed p. 71]

(which then becomes phased in to load forecasts for subsequent capacity auctions). Hence, all avoided capacity is stated per kW of accredited capacity, and we identify the accredited capacity for efficiency resources based on their load profiles and resulting Marginal Reliability Impact (MRI). The effect of uncleared capacity for demand response will vary with the number days each summer or winter for which peak load is reduced and the number of years for which the load reduction continues (see _Appendix J: Guide to Calculating Avoided Costs for Cleared and Uncleared measures_ more information).

- The capacity value of passive demand resource (such as an energy efficiency program) or an active demand resource cleared in the capacity market will be determined by the capacity value accepted by the ISO. The user of the model needs to estimate how much capacity value will be recognized by the ISO for each resource that will be bid into the market. The capacity value of energy efficiency that is not cleared in the capacity market will be approximately the load reduction of the measure at the ISO's normal peak conditions.[^75] However, after the ISO's RCA proposal becomes effective in June 2028, performance during any high-risk hours (such as hours with lower renewable generation) will impact a resource's capacity value.
- ISO New England models peak load by regressing daily peak in each day of July and August on a number of variables, including monthly energy, WTHI,² [sic: superscript 2 as printed, with no matching footnote] a time trend × WTHI, and dummies for weekends and holidays (also × WTHI). While it is difficult to determine exactly how load reductions in various conditions will affect the accredited capacity demand for the region, an energy efficiency measure that reduces load throughout the year or in the days with higher loads and lower renewable generation should fully affect the load forecast. Load management that affects only a few summer or winter days would have a much smaller impact on the load forecast.

#### _For DRIPE:_

- Energy DRIPE is estimated as proportional to avoided energy cost. Thus, energy DRIPE can be applied to any level of disaggregated avoided energy cost.
- Capacity DRIPE is stated per kW of peak load reduction, for bid resources and for non-bid load reductions. Those values can be attributed to programs in the same manner as the avoided capacity costs, and with the same computations for demand response.
- Natural gas supply DRIPE and oil DRIPE are intrinsically annual values.
- Natural gas basis DRIPE is associated with high-load days in the winter, for both electric and natural gas loads.

[^75]: The normal peak conditions are defined as a weighted temperature-humidity index (WTHI) for the day of 79.9°, where the weighting is (10 × the current day's THI, plus 5 × the previous day's THI, plus 2 × the THI two days earlier) ÷ 17. The daily THI is 0.5 × temperature +0.3 × dewpoint + 15. The THIs are computed for eight cities (Boston MA, Hartford CT, Providence RI, Portland ME, Manchester NH, Burlington VT, Springfield MA, and Worcester MA) and weighted by zonal loads.

[PDF p. 90 | printed p. 72]

### Model calibration

Because one of the main outputs of AESC 2024 is the estimation of avoided electric energy costs, it is essential that modeling outputs for wholesale energy prices are in line with actual, recent historical wholesale energy prices. In this analysis, we compare the model's projected regional hourly price forecasts to 2020, 2021, and 2022 prices in the ISO New England's "SMD" dataset.[^76] See Section 6.2: _Benchmarking the EnCompass energy model_ for more information on the results of the model calibration for energy costs.

Note that because several of the AESC counterfactuals project futures that lack any incremental energy efficiency installed beyond 2023, prices in future years are likely to substantially diverge from recent historical prices.

## 4.2. Modeling counterfactuals

The _AESC 2024 User Interface_, a set of standalone Excel workbooks, includes hourly values in addition to the four traditional energy costing periods (summer on-peak, summer off-peak, winter on-peak, and winter off-peak).[^77] These 8,760 avoided cost values may help refine the quantification of traditional DSM programs that have relied upon avoided cost values from previous AESC studies.

As with AESC 2021, AESC 2024 examines a series of counterfactuals. Each of these counterfactuals includes some DSM components and excludes others. Generally speaking, each of the avoided cost streams is the "but for" costs attributed to the counterfactual scenario, so those specific DSM components are excluded in the specified scenario. Table 40 details the DSM components included in each of the counterfactuals. Additional detail on the specifics behind the DSM components modeled in each counterfactual can be found in the subsequent sections of this chapter.

We note that this set of counterfactuals was developed via thorough discussion with the AESC 2024 Study Group, over multiple discussion dates and via a non-scientific survey.

For purposes of simplification and comparison, Counterfactual #1 is the counterfactual used for the discussion of many high-level findings and comparisons with previous AESC study results throughout this report. The following two sections on system demand and renewable energy policies describe the assumptions used for each of the DSM components.

[^76]: "SMD" is a legacy acronym referring to "Standard Market Design." Currently, the primary application of this term is in the naming of this dataset. The SMD dataset containing hourly data for historical years can be found at on the ISO New England website. ISO New England Inc. "Zonal Information." _Energy, Load and Demand Reports_. Available at: [https://www.iso-ne.com/isoexpress/web/reports/load-and-demand/-/tree/zone-info](https://www.iso-ne.com/isoexpress/web/reports/load-and-demand/-/tree/zone-info).

[^77]: _Appendix B: Detailed Electric Outputs_ contains the cost streams associated with the four costing periods consistent with previous AESC studies.

[PDF p. 91 | printed p. 73]

**Table 40. Counterfactual scenarios and sensitivities discussed for modeling in AESC 2024**

| DSM component                                           | Counterfactual #1 "AESC Classic": Avoided costs for EE, ADM, and building electrification | Counterfactual #2 Avoided costs for building electrification only | Counterfactual #3 Avoided costs for EE only | Counterfactual #4 Avoided costs for DR and BTM Storage only | Counterfactual #5 All-in DERs   | Counterfactual #6 Avoided costs for BTM Storage only: Programmatic _and_ non-programmatic measures | Sensitivity #1 High Gas Price (sensitivity on Counterfactual #1) | Sensitivity #2 Increased Clean Electricity (sensitivity on Counterfactual #5) |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------------------------- | ------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Energy efficiency                                       | No                                                                                        | Yes                                                               | No                                          | Yes                                                         | Yes                             | Yes                                                                                                | No                                                               | Yes                                                                           |
| Building electrification                                | No                                                                                        | No                                                                | Yes                                         | Yes                                                         | Yes                             | Yes                                                                                                | No                                                               | Yes                                                                           |
| Demand response                                         | No                                                                                        | Yes                                                               | Yes                                         | No                                                          | Yes                             | Yes                                                                                                | No                                                               | Yes                                                                           |
| BTM storage                                             | No                                                                                        | Yes                                                               | Yes                                         | No                                                          | Yes                             | No (Programmatic <u>and</u> non-programmatic)                                                      | No                                                               | Yes                                                                           |
| Transportation electrification                          | Yes                                                                                       | Yes                                                               | Yes                                         | Yes                                                         | Yes                             | Yes                                                                                                | Yes                                                              | Yes                                                                           |
| Distributed generation                                  | Yes                                                                                       | Yes                                                               | Yes                                         | Yes                                                         | Yes                             | Yes                                                                                                | Yes                                                              | Yes                                                                           |
| Likely to transition to winter peaking in study period? | No                                                                                        | No                                                                | Yes (likely transition by 2035)             | Yes (likely transition by 2035)                             | Yes (likely transition by 2035) | Yes (likely transition by 2035)                                                                    | No                                                               | Yes (likely transition by 2035)                                               |
| RPS and other renewable policies                        | As described in Chapter 7                                                                 | As described in Chapter 7                                         | As described in Chapter 7                   | As described in Chapter 7                                   | As described in Chapter 7       | As described in Chapter 7                                                                          | As described in Chapter 7                                        | As described in Chapter 7, plus an IRCEP policy described in Chapter 12       |

_Notes: A "Yes" indicates that the relevant DSM component is included (e.g., modeled) within that counterfactual. A "No" indicates that the DSM component is not incorporated into the modeling in 2024 or any future year. Unless otherwise stated, a "No" only removes the <u>programmatic</u> resources associated with each DSM component (e.g., energy efficiency associated with codes and standards is modeled in all scenarios, as is storage or demand response owned or funded by entities other than program administrators). The "IRCEP" policy is described in detail in Chapter 12: Sensitivity Analysis._

_Extractor note (not source text): the first column header "DSM component" is not printed; the row labels (Energy efficiency, Building electrification, etc.) are printed in the first column of the PDF table without a header. The page is landscape. The column headings are shown in full as printed, including the underlined and italic words._

[PDF p. 92 | printed p. 74]

## 4.3. New England system demand and energy components

Forecasts of annual peak demand and energy used in each of the AESC 2024 models are in large part based on the 50/50 values published by ISO New England in the 2023 _Forecast Report of Capacity, Energy, Loads and Transmission_ (CELT) study.[^78] However, our forecast includes modifications and enhancements to this forecast. Specifically, our load forecast covers the following components:

- <u>Conventional load</u>: This is a projection of energy consumption (in MWh) and peak demand (in MW) related to traditional electric end uses, based on data provided in ISO New England's 2023 CELT forecast, with adjustments. It also includes historical energy efficiency installed through 2023 but does not include any energy efficiency installed in 2024 or later years. It also does not include impacts from any of the categories discussed below.
- <u>Energy efficiency</u>: This is a projection of programmatic energy efficiency measures for 2024 and later years, for all New England states based on a combination of recent energy efficiency spending and savings, and data provided in ISO New England's 2023 CELT forecast. It is used in counterfactuals that estimate avoided costs for measures _other than_ energy efficiency.
- <u>Building electrification</u>: This is a projection of the impacts from programmatically linked heat pumps and water heating electrification measures, based on data provided in ISO New England's 2023 CELT forecast. It is used in counterfactuals that estimate avoided costs for measures _other than_ building electrification.
- <u>Demand response</u>: This is a projection of the impacts from demand response measures, based on data in ISO New England's FCM and program data reported by states and utilities. It is used in counterfactuals that estimate avoided costs for measures _other than_ demand response. Note that this projection includes separate projections for both programmatically linked and non-programmatic resources.
- <u>Behind-the-meter storage</u>: This is a projection of the impacts from behind-the-meter (BTM) energy storage, based on program data reported by states and utilities. It is used in counterfactuals that estimate avoided costs for measures _other than_ active BTM storage. Note that this projection includes separate projections for both programmatically linked and non-programmatic resources.
- <u>Transportation electrification</u>: This is a projection of the impacts from light-, medium-, and heavy-duty electric vehicles, based on data provided in ISO New England's 2023 CELT forecast, with some minor modifications. It is used in all counterfactuals.

[^78]: The "50/50" forecast contains ISO New England's statistically most-likely estimate of future demand. ISO New England also publishes other forecasts for demand, including a 90/10 and a 10/90 forecast, which represent high and low ranges of estimates for demand.

[PDF p. 93 | printed p. 75]

- <u>Distributed generation</u>: This is a projection of the impacts from distributed solar, based on the implied quantities resulting from state renewable policy. It is used in all counterfactuals. See Section 4.4: _Renewable energy_ for more information on this topic.

### Conventional load

This section focuses on the conventional load (or "econometric") forecast for electricity demand. Generally speaking, this forecast comprises the impacts of "traditional" electric end uses (e.g., not transportation electrification or building electrification), as well as the installation of energy efficient measures no longer addressed by the energy efficiency load component (generally speaking, replacements for programmatic measures have expired, or measures that meet new codes and standards).

In May 2023, ISO New England released its newest electricity demand forecast, CELT 2023.[^79] As in the CELT forecasts before it, in CELT 2023 ISO New England developed a forecast of annual energy for New England as a whole and for each individual state and load zone. These forecasts are based on regression models that integrate inputs on previous annual consumption, real electricity price, real personal income, gross state product, and heating and cooling degree days over 30 years.

Study Group members identified that the projection estimated by ISO New England (a 0.9 percent compound annual growth rate for 2023–2032) seemed high relative to load growth in recent years (estimated to have been about 0.5 percent over the past 10 years, after accounting for impacts from energy efficiency and distributed solar measures). We note that the regression used by ISO New England is based on information from 1996 to 2022, with the primary driver of future load appearing to be gross state product. We also note that increases in gross state product in the 10 most recent years tend to be lower than in the late 1990s and early 2000s, indicating that this entire timespan may not be the best predictor of future load increases. Furthermore, the most recent 10 years span a period that had widespread deployment of energy efficiency measures even beyond those counted in the energy efficiency forecast, as a result of measures deployed via state federal codes and standards. Because future years are likely to continue to be impacted by savings resulting from these policies, and because it is convention by ISO New England for the conventional load forecast to incorporate the impacts of new measures that replace expiring efficient measures, it is likely that future load growth may continue to be lower than would be predicted based on a long timespan of data.

As a result, we develop a conventional load forecast based on the compound annual growth rate of historical electric load, with impacts from energy efficiency and behind-the-meter solar removed. This load growth rate is about 0.5 percent for New England as a whole but varies for each of the modeled regions. Figure 15 illustrates the New England-wide projection of annual electricity demand, relative to

[^79]: Further information about the CELT forecast can be found at ISO New England's website at [https://www.iso-ne.com/system-planning/system-plans-studies/celt](https://www.iso-ne.com/system-planning/system-plans-studies/celt), [https://www.iso-ne.com/system-planning/system-forecasting/load-forecast/](https://www.iso-ne.com/system-planning/system-forecasting/load-forecast/) and [https://www.iso-ne.com/static-assets/documents/2023/04/modeling_procedure_2023.docx](https://www.iso-ne.com/static-assets/documents/2023/04/modeling_procedure_2023.docx) .

[PDF p. 94 | printed p. 76]

recent historical forecasts, ISO New England's forecast as modeled in CELT 2023, and the forecast used in AESC 2021.

**Figure 15. Historical and projected annual energy forecasts for all of ISO New England**

[DIAGRAM DESCRIPTION: Figure 15. Historical and projected annual energy forecasts for all of ISO New England]
Line chart. X-axis: year, 2000 to 2050 (ticks every 5 years). Y-axis: "ISO New England Annual Electricity Demand (TWh)", 100 to 160 (gridlines every 10). Series, labelled directly on the chart (no separate legend): (1) solid black line "Historical net energy for load": about 125 TWh in 2000, rising to a peak of about 136 TWh in 2005, fluctuating between about 127 and 134 TWh through 2013, then declining to about 117 TWh in 2020 and about 119 TWh in 2022 (the label for this end of the line reads "Historical plus behind-the-meter PV", with a pointer to the 2020-2022 segment); (2) dashed black line "Historical plus energy efficiency and behind-the-meter PV": tracks just above the solid black line from roughly 2015 to 2022 (about 128 TWh in 2015, about 122 TWh around 2021); (3) solid orange line "AESC 2021": starts at about 121 TWh in 2020 and rises roughly linearly to about 148 TWh in 2035, where it ends; (4) dashed dark-green line "CELT 2023": starts at about 121 TWh in 2020 and rises to about 138 TWh around 2033, where it ends; (5) solid light-green line "AESC 2024": starts at about 119 TWh in 2023 and rises roughly linearly to about 140 TWh in 2050. Takeaway: the AESC 2024 conventional-load trajectory grows much more slowly (about 0.5 percent per year) than the AESC 2021 trajectory and ISO New England's CELT 2023 forecast. Values read off the chart are approximate.
[→ See original PDF page 94 for visual rendering]

_Notes: In both the CELT 2023 and AESC 2024 trajectories, all data points are decreased to reflect the energy efficiency installed through 2023 (see following section on "Programmatic Energy Efficiency"). No other impacts from energy efficiency, active demand management (demand response, behind-the-meter storage, or managed charging), building electrification, transportation electrification, or distributed solar are included. A similar operation is performed for the AESC 2021 trajectory, with the only energy efficiency savings being included from those measures which were installed through 2020._

In order to develop hourly system energy demand, we apply hourly load shapes developed for each load zone published by ISO New England in the 2023 CELT study.[^80] As a result, the hourly load shape for the conventional load component for January 1, 2024 (for example) is identical to the hourly load shape for this component for January 1, 2050. The primary difference will be that the quantities in 2050 will be larger, reflecting an overall increase in conventional load. These load shapes are based on weather data for 2002, a year identified by ISO as containing relatively average weather relative to other recent years.[^81] While it is possible that load shapes may change over time, or change as a result of the changing

[^80]: In AESC 2024, we rely on the 2002-era load shapes hosted by ISO New England at [https://www.iso-ne.com/system-planning/planning-models-and-data/variable-energy-resource-data/](https://www.iso-ne.com/system-planning/planning-models-and-data/variable-energy-resource-data/) in order to achieve consistency between hourly load shapes and hourly renewable capacity factors. Past editions of AESC have used the hourly load shapes developed by ISO New England for the CELT 2023 forecast that can be found on the ISO New England website at [https://www.iso-ne.com/static-assets/documents/2023/04/hrly_sa_fcst_eei2023.txt](https://www.iso-ne.com/static-assets/documents/2023/04/hrly_sa_fcst_eei2023.txt). We note that there are some differences between these two sets of load shapes, in part due to the fact that the dataset used in AESC 2024 is published at the state level, and the dataset used in previous studies is published at the modeling region level.

[^81]: For more on this assumption, see ISO New England's 2018 slide deck "Review of Assumptions Relating to ICR and Related Values – 2002 Load Shape," available at [https://www.iso-ne.com/static-assets/documents/2018/04/a7_pspc_review_icr_2002_load_shape_04182018.pdf](https://www.iso-ne.com/static-assets/documents/2018/04/a7_pspc_review_icr_2002_load_shape_04182018.pdf).

[PDF p. 95 | printed p. 77]

climate, the scale and shape of these changes are uncertain. As a result, we rely on ISO New England's load shapes for purposes of simplification. Load shapes for other components of system load (e.g., energy efficiency, transportation electrification) are discussed in the _Other System Demand Components_ section, below.[^82]

### Energy efficiency

Since 2008, ISO New England has sought to compensate for these "embedded energy efficiency" effects by explicitly accounting for "passive demand resources" (PDR).[^83] Thus, programmatic energy efficiency is excluded from the main ISO New England econometric forecasts, producing a "gross" forecast for annual energy and peak demand that is higher than it would be without the impact of PDRs. Starting in 2008, ISO New England has put forth a separate PDR forecast for energy efficiency resources, and since 2015, it has published a third forecast for distributed solar (PV). ISO New England then subtracts the forecasted quantities of PDRs and distributed PV from its gross forecast to estimate a "net" forecast, a lower number that reflects the actual estimated demand for each modeled year. Throughout AESC 2024, we assume that all energy efficiency measures are programmatic, unless otherwise stated.

AESC 2024 bases some elements of its energy efficiency projection on the projection issued by ISO New England. This section consists of two subsections: the first describing ISO New England's overall approach and the second describing the modifications applied to this approach for purposes of AESC 2024.

#### ISO New England approach

During the development of each CELT forecast, ISO New England works with the Energy Efficiency Forecast Working Group (EEFWG), which produces an estimate for future energy efficiency based on expected future energy efficiency expenditures and program performance. ISO New England's development of an energy efficiency forecast for CELT 2023 varies in important ways, relative to the CELT 2020 forecast used as the basis for AESC 2021.[^84] ISO New England's forecast is compiled as follows:

- First, ISO New England uses data from the latest completed FCA to establish a total level of energy efficiency in some future year. As of CELT 2023, the latest completed capacity auction was FCA 17, which denoted about 14 TWh of cumulative energy efficiency installed as of 2026. ISO New England then compares this to a "starting" level of energy efficiency installed as of 2010, subtracts the 2026 value from the 2010 value, and divides the result by the number of intervening years. This linear interpolation is performed

[^82]: Study Group members identified a desire to explore the impacts of choosing a different weather year on avoided costs. It was not possible to conduct this analysis under the AESC 2024 timeline and budget, but is a promising area for future analyses.

[^83]: Prior to 2008, ISO New England's forecast implicitly contained some level of reductions from efficiency programs because the programs were in effect during the historical period.

[^84]: ISO New England. 2023. _Final 2023 Energy Efficiency Forecast_. Available at [https://www.iso-ne.com/static-assets/documents/2023/04/eef2023_final_slides.pdf](https://www.iso-ne.com/static-assets/documents/2023/04/eef2023_final_slides.pdf).

[PDF p. 96 | printed p. 78]

independently for each of the six New England states, and produces a single, unchanging quantity of annual installed energy efficiency for each year from 2011 through 2026 (697 GWh, New England-wide).[^85] ISO New England notes that as the amount of energy efficiency that clears the capacity market will change in each year, so too will its estimate of historical energy efficiency. ISO New England also notes that this approach may underestimate the total amount of energy efficiency regionwide, as not all measures participate in the capacity market.[^86]

- Second, ISO New England develops a projection of energy efficiency that will be installed in 2027 through 2032. Generally speaking, this estimate is produced for each state by dividing an annual energy by a production cost to produce annual incremental savings. The energy efficiency budgets are provided by state energy offices and tend to be roughly constant over time, in nominal dollar terms (meaning that they decrease over time when converted to 2024 dollars). Meanwhile, production costs vary in several ways. First, production costs are based on estimates from 2019–2021, which vary by sector and end use (e.g., Residential & Low Income HVAC, C&I Refrigeration).[^87] These costs are then projected to grow both according to inflation and a 1.25 percent escalation rate. Costs also change over time in a third way, reflecting a shift away from some end-use types towards other end-use types (which is generally a shift away from cheaper end uses towards more expensive end uses). As a result, the production costs tend to increase substantially over the study period. For example, Massachusetts' Residential & Low Income production costs change from about $4,300 per MWh in 2027 to about $7,900 per MWh in 2032 (all values are in nominal dollars). This increase in production costs, paired with a decrease in program budgets (in real dollar terms), produces a steady decline in the annual incremental energy efficiency deployed.
- Third, ISO New England now incorporates embedded expiring measures.[^88] This action is intended to capture situations where measures installed through energy efficiency programs expire, but are "naturally" replaced by like measures by consumers. ISO New England posits that this "like-for-like" replacement is otherwise being captured in the conventional load forecast and implements a set of steps to avoid double-counting. Practically speaking, to estimate a quantity of expiring measures, ISO New England compares the amount of energy efficiency that cleared in the most recent capacity auction with the amount of energy efficiency that cleared in the past auction with the most energy efficiency. Subtracting one value from the other yields a quantity of energy efficiency assumed to be expiring in each future year (roughly 800 GWh each year, New England-wide).

[^85]: See Final 2023 Energy Efficiency Forecast, slide 24.

[^86]: Synapse observes that according to ISO New England's methodology, Massachusetts has 328 GWh installed in each year from 2011 through 2026. This is likely to be an overestimate for the earlier years, but for more recent years is likely an underestimate, given MassSave data (see [https://www.masssavedata.com/](https://www.masssavedata.com/)) showing an average of 1,100 GWh installed in Massachusetts between 2019 and 2021.

[^87]: See _Final 2023 Energy Efficiency Forecast_, slides 9 through 15.

[^88]: See _Final 2023 Energy Efficiency Forecast_, slides 20 through 22.

[PDF p. 97 | printed p. 79]

As with other components of the 2023 CELT forecast, this forecast contains estimates of energy efficiency through 2032.

#### AESC 2024 approach

The approach for projecting energy efficiency in AESC 2024 builds on ISO New England's approach in a number of ways. Primarily, the Synapse Team implements modifications to bring the forecast more in line with the program administrators' plans for energy efficiency.

We implement modifications to ISO New England's approach as follows:

- <u>Historical savings</u>: Rather than basing historical savings on an extrapolation of energy efficiency cleared in recent auctions, our projection compiles savings data as reported by energy efficiency program administrators from 2010 through 2022. These data sources are compiled from a variety of sources, with the primary source being the Regional Energy Efficiency Database (REED) product published by Northeast Energy Efficiency Partnerships (NEEP).[^89] Where necessary (e.g., for the most recent years' data and for situations where energy efficiency impacts must be isolated from programs containing kWh impacts from both energy efficiency and heat pump measures), this data is supplemented by information from program administrators' annual reports.
- <u>Future budgets</u>: Using the REED dataset as well as information submitted in program administrators' annual reports, we compile a set of recent budgets for energy efficiency programs (e.g., for 2022) for residential and C&I programs. These budgets are then held constant through 2050 in real-dollar terms.
- <u>Future production costs</u>: As in AESC 2021, we remove the 1.25 percent production-cost escalator assumed by ISO New England but assume the same switch in measure installations that yields a higher production cost over time.[^90]
- <u>Expiring measures</u>: Using measure life data posted by Massachusetts program administrators for 2016 and 2021, we develop a set of expiration schedules for measure types (e.g., HVAC, process, hot water) and sectors (residential and C&I). We then apply these expiration schedules to all historical and future energy efficiency measure types in order to determine an estimate of the quantity of savings expected to be retiring in every year.[^91] As described above, ISO New England assumes that as measures expire, they are replaced by similarly efficient measures within the conventional load forecast. As a result, the savings from these expiring measures must be removed from the energy efficiency component in order to avoid double-counting.

[^89]: For more information on this dataset, see [https://neep.org/emv/regional-energy-efficiency-database](https://neep.org/emv/regional-energy-efficiency-database).

[^90]: Study Group members identified that escalations in production costs were already being sufficiently addressed via the change in measures being implemented, and that a supplementary production-cost escalator was unnecessary.

[^91]: Historical mixes of measure data are derived from a 2022 ISO New England report on this topic. ISO New England. _2023 Energy Efficiency Forecast Data Review and Verification: End Use Measure Data_. December 5, 2022. Available at [https://www.iso-ne.com/static-assets/documents/2022/12/eefwg2023_meas_data.pdf](https://www.iso-ne.com/static-assets/documents/2022/12/eefwg2023_meas_data.pdf).

[PDF p. 98 | printed p. 80]

- <u>Special circumstances</u>: In some situations, we supplement the above methodology with separate datasets. For example, as of October 2023, Rhode Island Energy is in the midst of assembling its energy efficiency plan for 2024–2026.[^92] We assume the level of savings implied in this submitted plan for these years, and then switch to the above method for calculating savings in Rhode Island later years. Likewise, the state of Vermont assembles a long-term plan for energy efficiency for years 2024 to 2043.[^93] We use this plan in place of the above methodology, with savings for 2043 held constant through 2050. In each of these cases, we apply the same assumptions as described above for expiring measures.

For AESC 2024, we must develop two different projections of energy efficiency through 2050. The first is an assumption on the level of energy efficiency that exists in 2023. This projection is used in Counterfactual #1 and Counterfactual #3. In this first projection, we deploy the above algorithm to estimate the measures that would be installed through 2023, and then do not implement any additional energy efficiency measures in 2024 and later years. However, during the 2024 to 2050 time period, measures expire, resulting in an overall diminishing in energy efficiency savings over time.

The second projection is based on a future where program administrators continue to implement energy efficiency throughout the study period. This second projection is used in Counterfactual #2, Counterfactual #4, Counterfactual #5, and Counterfactual #6. In this projection, we deploy the above algorithm for all years to estimate the amount of energy efficiency that would be installed (and would expire) in each year to estimate cumulative impacts from savings in each year.

We note that both of the above projections differ from the analogous projections of energy efficiency developed for previous AESC studies, which typically ignored expiring savings.

Figure 16 illustrates how these two energy efficiency projections compare with one another, and with the projection in ISO New England's CELT 2023 forecast. We note that the level of energy efficiency considered in both AESC 2024 projections is roughly 13 percent of total projected conventional load in the early 2020s (see Figure 15, above).

[^92]: 2024-2026 Energy Efficiency Three-Year Plan and Annual Energy Efficiency Plan for 2024, Rhode Island Public Utility Commission Docket No. 23-35-EE, Pre-Filed Direct Testimony of: Brett Feldman, Michael O'Brien Crayne, Mark Siegal, Toby Ast, and Spencer Lawrence. October 2, 2023. Available at [https://ripuc.ri.gov/sites/g/files/xkgbur841/files/2023-10/2335-RIE-Annual-ThreeYr-EEPlan_10-2-23-Bates.pdf](https://ripuc.ri.gov/sites/g/files/xkgbur841/files/2023-10/2335-RIE-Annual-ThreeYr-EEPlan_10-2-23-Bates.pdf).

[^93]: See EVT 2024-43 Demand Resource Plan proceeding, baseline modeling results Case No. 22-2954-INV and BED 2024-43 Demand Resource Plan proceeding, Plan A modeling results Case No. 22-2954-INV, provided to Synapse by VT DPS.

[PDF p. 99 | printed p. 81]

**Figure 16. Projected cumulative regionwide energy efficiency impacts**

[DIAGRAM DESCRIPTION: Figure 16. Projected cumulative regionwide energy efficiency impacts]
Line chart. X-axis: year, 2020 to 2050 (ticks every 5 years; lines start in 2023). Y-axis: "Cumulative Installed EE (TWh)", 0 to 20 (gridlines every 2). Three series, labelled directly on the chart: (1) dark-blue line "Counterfactual #2, #4, #5, #6": starts at about 18.3 TWh in 2023, declines to about 16.8 TWh in 2026, drops to about 12.5 TWh in 2028 and bottoms at about 11.7 TWh around 2031, then rises to about 13 TWh in 2035, about 14.7 TWh in 2040 and flattens at about 15 to 15.2 TWh from 2045 through 2050; (2) light-blue line "Counterfactual #1 and #3": starts at the same 18.3 TWh in 2023 and falls steadily to about 13.7 TWh in 2026, about 7 TWh in 2028, about 4.3 TWh in 2030, about 1.5 TWh in 2035 and about 0.3 TWh in 2040, reaching 0 TWh by about 2042 and staying at 0 through 2050; (3) orange line "CELT 2023, no adjustments": starts at about 11.6 TWh in 2023, rises to a peak of about 13.9 TWh around 2028, then declines to about 12.8 TWh in 2032, where it ends. Takeaway: with no new programmatic efficiency after 2023 (Counterfactuals #1 and #3) cumulative installed efficiency decays to zero as measures expire; with continued programs (Counterfactuals #2, #4, #5, #6) it dips and then recovers to about 15 TWh. Values read off the chart are approximate.
[→ See original PDF page 99 for visual rendering]

For all modeled counterfactuals, the Synapse Team assumes the same hourly load shape for energy efficiency that is used for the conventional load component of the energy forecast. This effectively reduces the conventional load component in every hour by the fraction of modeled energy efficiency (in MWh) relative to the system demand. While different energy efficiency measures may have different load profiles in reality, this simplified approach is meant to approximate the implementation of a portfolio of energy efficiency measures. We determine peak impacts of energy efficiency and energy efficiency's contribution to the capacity requirement by estimating the peak hour for energy efficiency in each year, based on the annual regionwide energy efficiency amount and annual system demand impact.

### Demand response

Demand response participates in ISO New England's FCM and serves as a peak demand resource. Demand response participation in the FCM has grown incrementally for several years. To forecast demand response impacts in future years, we rely on cleared capacity obligations through 2026. Then, to develop a forecast through 2050, we increase the 2026 quantity of demand response each year by the compound annual growth rate (CAGR) trend observed for capacity between 2018 and 2026. In FCA 17 (e.g., for commitment period 2026/2027), 623 MW of demand response capacity cleared the market and received a capacity supply obligation. This roughly doubles by 2050, growing to 1,130 MW. We assume all demand response that has cleared in the FCM so far is non-programmatic, as is all demand response projected to exist based on historical FCM values. As a result, this quantity of demand response is modeled in all counterfactuals.

In AESC 2021, based on direction from Study Group members from Massachusetts, we also assume an additional quantity of programmatic demand response. This quantity is based on the available-at-the-time draft planning numbers in Massachusetts. Under this assumption, we assume 162 MW of measures capable of demand response in 2020 and double that quantity by 2024. In AESC 2024, at the

[PDF p. 100 | printed p. 82]

recommendation of the Study Group, we update the assumed quantity of programmatic C&I demand response measures to assume a level of 120 MW in 2024 in Massachusetts and an annual increase of 7.5 percent per year through 2050. Based on the Study Group's recommendations, for programmatic residential demand response in Massachusetts, we adopt the AESC 2021 assumption of modeling a constant 54 MW in 2024 through 2050.

In AESC 2024, we also assume additional programmatic demand response based on direction from Study Group members from Rhode Island. Based on actual enrolled programmatic demand response capacities provided by the Study Group, we assume 79.7 MW of C&I demand response, and 5.6 MW of residential demand response. We adopt these values beginning in 2023 and hold them constant through 2050.

Based on recent historical behavior in the energy market, we assume that 10 percent of the entire demand response resource dispatches when prices are greater than $30 per MWh (in 2024 dollars) while 90 percent of this resource dispatches when prices exceed $900 per MWh (e.g., a stand-in for rare, very high price events).[^94]

Figure 17 shows the quantity of demand response modeled in AESC 2024. One series, labelled "Non-programmatic and historical programmatic" includes all non-programmatic demand response (i.e., that which cleared in the capacity market, and is projected into the future based on historical capacity results) and all programmatic demand response assumed to have been installed through 2023. The second series, "Future programmatic" includes all other demand response measures that are projected to be installed by the program administrators. The total quantity of demand response modeled in AESC 2024 is similar to the quantity modeled in AESC 2021. As in AESC 2021, we assumed the majority of demand response measures to be non-programmatic and thus modeled them the same way in every counterfactual. Programmatic demand response is included in Counterfactuals #2, #3, #5, and #6. For modeling purposes, demand response capacities outside of those cleared in the FCM capacities are grossed up by 8 percent to reflect a conversion between retail MW and wholesale MW.[^95]

[^94]: These are the same values assumed in AESC 2021, without adjustments to dollar years (reflecting their nature as high-level assumptions).

[^95]: We assume that capacities cleared in the FCM, and projected future capacity based on these quantities, are already reported in wholesale terms.

[PDF p. 101 | printed p. 83]

**Figure 17. Demand response forecast for New England**

[DIAGRAM DESCRIPTION: Figure 17. Demand response forecast for New England]
Line chart. X-axis: year, 2020 to 2050 (ticks every 5 years). Y-axis: "Modeled Demand Response (MW)", 0 to 2,000 (gridlines every 200). Two series, labelled directly on the chart: (1) dark-red line "Non-programmatic and historical programmatic": about 570 MW in 2020, about 760 to 800 MW in 2021 to 2022, a small dip to about 730 MW in 2023, a peak of about 880 MW in 2025, a drop to about 750 MW in 2026, then rising smoothly to about 1,000 MW in 2040 and about 1,200 MW in 2050; (2) light-pink line "Future programmatic": identical to the dark-red line through about 2025, then slightly above it (about 780 MW in 2026) and rising faster, to about 1,250 MW in 2040 and about 1,880 MW in 2050. Takeaway: total modeled demand response grows from roughly 750 to 780 MW in 2026 to about 1,900 MW in 2050 with future programmatic additions, of which about 1,200 MW is the non-programmatic and historical programmatic base. Values read off the chart are approximate.
[→ See original PDF page 101 for visual rendering]

_Note: Values shown are for retail MW, rather than wholesale MW._

Another type of demand response is flexible load, such as managed charging for electric vehicles or programs that compensate owners of electric water heaters to pre-heat their water several hours ahead of expected use. However, AESC 2024 does not consider any quantity of managed charging or other flexible load resources.

### Behind-the-meter storage

There is currently no regional projection of BTM storage for New England. Furthermore, data availability on existing BTM installations vary by state, and by administrator. To establish a baseline of existing and projected BTM storage installation in New England, we assemble data and projections from policy mandates and incentives for BTM storage for every state and New England. We then aggregate these projections to forecast total BTM storage capacity through 2050.

- <u>Connecticut</u>: On January 1, 2022, the Connecticut Public Utilities Regulatory Authority (PURA) launched the Energy Storage Solutions Program.[^96] This program is administered by Connecticut Green Bank, Eversource, and United Illuminating for both residential and C&I customers, and it is expected to run at least through December 31, 2030. The program has a goal of reaching 580 MW of storage by 2030.[^97] As of August 18, 2023, this program had completed 0.71 MW of BTM storage, with an additional 77 MW of

[^96]: Energy Storage Solutions Administrators. "Energy Storage Solutions." Available at: [https://energystoragect.com/](https://energystoragect.com/).

[^97]: Energy Toolbase Software Inc. 2021. "Connecticut Makes Strides Towards 1,000 MW Statewide Goal with Public Utilities Regulatory Authority (PURA) Approval of New Energy Storage Incentive." Available at: [https://www.energytoolbase.com/newsroom/blog/connecticut-pura-approves-new-energy-storage-incentive](https://www.energytoolbase.com/newsroom/blog/connecticut-pura-approves-new-energy-storage-incentive).

[PDF p. 102 | printed p. 84]

    approved projects that are not yet completed.[^98] Per the Study Group's recommendation, we assume this 580 MW is installed by 2030 and is a programmatic resource.

    Eversource also administers the Connected Solutions program in Connecticut. This program provides residential customers incentives for supplying their own batteries.[^99] Under this program, customers can receive incentive payments of up to $225 per average kW used from their demand response resources over a three-hour period between June and September. This program will be phasing out in Connecticut due to the new Energy Storage Solutions offering and will not accept new customers after December 1, 2023.

- <u>Maine</u>: Efficiency Maine Trust (EMT) currently administers the Energy Storage System Program, which offers performance-based incentives of $200 per kW of reduced grid-supplied load for energy storage systems installed by non-residential, demand-metered customers.[^100]

  In addition, in June 2021, Maine passed LD 528, which set energy storage goals for Maine of 300 MW by 2025 and 400 MW by 2030.[^101] These goals are not modeled as a requirement in AESC 2024.

  Finally, in May 2022, Maine passed LD 2030, which provides a refund of sales and use tax to customers who purchase a qualifying battery energy storage system.[^102] This reimbursement will only apply to systems with a minimum capacity of 50 MW, purchased between January 1, 2023, and December 31, 2025. Given the large minimum capacity constraint, we do not think that this program is pertinent to BTM storage.

- <u>Massachusetts</u>: Through the Solar Massachusetts Renewable Target (SMART) program, participants can receive an incentive for pairing an Energy Storage Adder to their solar project. As of October 2023, this program had approved about 34 MW of BTM storage in Massachusetts.[^103] At the recommendation of the Study Group, we model the SMART

[^98]: Energy Storage Solutions Administrators. "Energy Storage Solutions Performance Report." Available at: [https://energystoragect.com/ess-performance-report/](https://energystoragect.com/ess-performance-report/).

[^99]: Eversource. Last accessed August 18, 2023. "Demand Response for Home Battery Storage." _Demand Response_. Available at: [https://www.eversource.com/content/residential/save-money-energy/energy-efficiency-programs/demand-response/battery-storage-demand-response](https://www.eversource.com/content/residential/save-money-energy/energy-efficiency-programs/demand-response/battery-storage-demand-response).

[^100]: Efficiency Maine. "Energy Storage System Projects." Available at: [https://www.efficiencymaine.com/energy-storage-system-projects/](https://www.efficiencymaine.com/energy-storage-system-projects/).

[^101]: State of Maine Governor's Energy Office. "Energy Storage." Available at: [https://www.maine.gov/energy/initiatives/renewable-energy/energy-storage](https://www.maine.gov/energy/initiatives/renewable-energy/energy-storage).

[^102]: State of Maine Governor's Energy Office. 2023. _Evaluation of the role of existing and potential tax incentives in achieving Maine's energy storage policy goals_. Submitted by the Governor's Energy Office to the Joint Standing Committee on Energy, Utilities and Technology, Pursuant to LD 2030: An Act to Provide for Reimbursement of the Sales Tax Paid on Certain Battery Energy Storage Systems. Available at: [https://legislature.maine.gov/doc/10084](https://legislature.maine.gov/doc/10084).

[^103]: Massachusetts Department of Energy Resources (DOER). Last accessed February 5, 2021. "SMART Qualified Units." Available at: [https://www.mass.gov/doc/smart-qualified-units-0](https://www.mass.gov/doc/smart-qualified-units-0).

[PDF p. 103 | printed p. 85]

    program as being 25 percent programmatic through 2034, and 15 percent programmatic from 2035 on.

    Additionally, the SMART program also offers storage for "standalone solar" projects, labeled in the SMART program separately from BTM projects. We include these projects in our model as well to ensure our forecast accounts for small, standalone storage projects, as our forecast aims to capture all storage. As of October 2023, the SMART program had approved about 279 MW of standalone storage.

    Second, Program Administrators deploy the Connected Solutions program through Mass Save, which provides residential customers an incentive of $275 per average kW used from their demand response resources over a two- to three-hour period for supplying their own batteries.[^104] [^105] Massachusetts requires utilities to report on their energy storage installations annually.[^106] These target reports, in addition to reporting on SMART program installations, contain entries labeled "MA – Energy Efficiency/DR Program." At the guidance of the Study Group, we assume these installations to be associated with the Connected Solutions program.

    Additionally, utility target reports contain entries labeled "MA – DOER/ MassCEC Funded Projects." We assume these projects are related to the Massachusetts Clean Energy Center's (MassCEC) Advancing Commonwealth Energy Storage (ACES) program.[^107] This program consists of a pilot of 26 energy storage demonstration projects, running from 2017–2024.

    Third, in March 2023, Cape Light Compact received approval to launch its Cape & Vineyard Electrification Offering (CVEO) program.[^108] This program will begin with a pilot to serve 100 residential low- and moderate-income customers, 25 of which will receive BTM storage systems.

[^104]: MassSave. Last accessed August 22, 2023. "Use Your Battery Storage Device to Make the Grid More Sustainable." Available at [https://www.masssave.com/saving/residential-rebates/connectedsolutions-batteries](https://www.masssave.com/saving/residential-rebates/connectedsolutions-batteries).

[^105]: During AESC 2021, members of the Study Group provided information on recently installed measures in Massachusetts' Connected Solutions program. For purposes of simplification and to avoid double-counting, we assume that all measures in this program are either also participating as demand response in the FCM or in the SMART program and are already accounted for in either one of the two projections.

    Mass Save. 2020. _Energy Efficiency Program Administrators Quarterly Report_. Available at [https://ma-eeac.org/wp-content/uploads/Quarterly-Report-of-the-PAs-2019-Q4-2-11-20-1.pdf](https://ma-eeac.org/wp-content/uploads/Quarterly-Report-of-the-PAs-2019-Q4-2-11-20-1.pdf), and Mass Save. 2020. _Massachusetts Energy Efficiency Program Administrators Quarterly Report_. Available at [https://ma-eeac.org/wp-content/uploads/Quarterly-Report-of-the-PAs-2020-Q2-Final.pdf](https://ma-eeac.org/wp-content/uploads/Quarterly-Report-of-the-PAs-2020-Q2-Final.pdf).

[^106]: Mass.gov. Last accessed August 24, 2023. "ESI Goals & Storage Target." Available at: [https://www.mass.gov/info-details/esi-goals-storage-target](https://www.mass.gov/info-details/esi-goals-storage-target).

[^107]: Massachusetts Clean Energy Council. "Advancing Commonwealth Energy Storage (ACES)." Available at [https://www.masscec.com/program/advancing-commonwealth-energy-storage-aces](https://www.masscec.com/program/advancing-commonwealth-energy-storage-aces).

[^108]: Olinsky-Paul, T., Epstein, G. 2023. _Innovative Massachusetts Low-Income Battery Pilot Finally Wins Approval (For Now…)_. Clean Energy Group. Available at: [https://www.cleanegroup.org/innovative-massachusetts-low-income-battery-pilot-finally-wins-approval-for-now/](https://www.cleanegroup.org/innovative-massachusetts-low-income-battery-pilot-finally-wins-approval-for-now/).

[PDF p. 104 | printed p. 86]

    Finally, the Clean Peak Standard (CPS), effective June 2020, may also serve as an incentive for BTM storage in the state. Qualified resources under the CPS include new renewable resources that also meet eligibility under Massachusetts' Class I and Class II RPS program.[^109] Existing renewable resources in both programs are eligible, so long as these resources are paired with a new energy storage system. Furthermore, both standalone energy storage systems and demand response resources are eligible to meet the CPS. 2019 modeling published by Massachusetts Department of Energy Resources described the estimated benefits under the CPS, which are projected to reach over 120,000 metric tons by 2030.[^110] Assuming that all of these benefits are provided by BTM storage, and that storage is able to provide a benefit of 60 metric tons per MW, this implies a 2030 capacity of about 2.0 GW.[^111] This is substantially larger than the Commonwealth's current storage target of 500 MW in 2025, and about 1,500 to 1,800 MW larger than the quantity of BTM storage assumed to exist in 2030 in any counterfactual, as a result of the other programs described above.[^112] Because of a lack of information on CPS requirements for each modeled year in AESC, we do not explicitly model this program.

- <u>New Hampshire</u>: In 2019, the New Hampshire Public Utilities Commission approved a BTM Battery Storage Pilot Program for Liberty Utilities' customers.[^113] The pilot contains two phases, the first of which was completed in 2022 and provided 96 participants with a total of 192 batteries, equivalent to roughly 0.96 MW of storage.[^114] Phase 2, if approved, combined with Phase 1 will put a total of 2.5 MW of BTM storage in New Hampshire.
- <u>Rhode Island</u>: As in Massachusetts and Connecticut, Rhode Island Energy administers the Connected Solutions program which provides residential customers incentives of

[^109]: Massachusetts Department of Energy Resources. 2020. _Clean Peak Energy Resource Eligibility Guide_. Available at [https://www.mass.gov/doc/clean-peak-resource-eligibility-guidelines/download](https://www.mass.gov/doc/clean-peak-resource-eligibility-guidelines/download).

[^110]: Massachusetts Department of Energy Resources. 2019. _The Clean Peak Energy Standard_. Available at [https://www.mass.gov/doc/drafts-cps-reg-summary-presentation/download](https://www.mass.gov/doc/drafts-cps-reg-summary-presentation/download). Slide 39.

[^111]: Per members of the Study Group, this metric tons per MW value is the avoided emissions value that has been applied for use in discussions regarding CPS.

    State of Charge. 2017. _Massachusetts Energy Storage Initiative Study_. Prepared for Massachusetts Department of Energy Resources. Available at [https://www.mass.gov/files/2017-07/state-of-charge-report.pdf](https://www.mass.gov/files/2017-07/state-of-charge-report.pdf). P. 95

[^112]: Massachusetts' energy storage goal is 1,000 MWh of storage by 2025. Per data available from the SMART program, the average duration of storage installed to date is 2 hours, which yields a storage target of 500 MW.

    Massachusetts Department of Energy Resources. Last accessed March 11, 2021. "ESI Goals & Storage Target." Available at [https://www.mass.gov/info-details/esi-goals-storage-target](https://www.mass.gov/info-details/esi-goals-storage-target).

[^113]: Gheorghiu, I. 2019. _Designing Liberty Utilities' New Hampshire residential storage program_. Utility Dive. Available at: [https://www.utilitydive.com/news/designing-liberty-utilities-new-hampshire-residential-storage-program/548940/](https://www.utilitydive.com/news/designing-liberty-utilities-new-hampshire-residential-storage-program/548940/).

[^114]: Guidehouse. November 2022. _Battery Storage Pilot Program: Interim Evaluation Report_. Available at: [https://www.puc.nh.gov/Regulatory/Docketbk/2017/17-189/LETTERS-MEMOS-TARIFFS/17-189_2022-11-29_GSEC_INTERIM-EVALUATION-REPORT.PDF](https://www.puc.nh.gov/Regulatory/Docketbk/2017/17-189/LETTERS-MEMOS-TARIFFS/17-189_2022-11-29_GSEC_INTERIM-EVALUATION-REPORT.PDF).

    Liberty. Accessed August 22, 2023. _Battery Storage_. Available at: [https://new-hampshire.libertyutilities.com/bath/residential/smart-energy-use/electric/battery-storage.html#:~:text=The%20battery%20storage%20program%20is,called%20the%20Tesla%20Powerwall%202](https://new-hampshire.libertyutilities.com/bath/residential/smart-energy-use/electric/battery-storage.html#:~:text=The%20battery%20storage%20program%20is,called%20the%20Tesla%20Powerwall%202).

[PDF p. 105 | printed p. 87]

    $400 per average kW used from their demand response resources over a two- to three-hour period between June and September for supplying their own batteries.[^115] At the guidance of Study Group members from Rhode Island, we assume a forecast of 16 MW of BTM storage in 2025, 76 MW in 2035, and 217 MW in 2050.

    Second, the Rhode Island Renewable Energy Fund (REF) Small-Scale Solar Program offers a flat $2,000 per project for energy storage system adders to residential solar projects.[^116] Program data is not currently available.

- <u>Vermont</u>: In Vermont, Green Mountain Power (GMP) offers two residential battery storage programs: the Bring Your Own Device (BYOD) Program, and the Tesla Powerwall Program.[^117] The BYOD Program has incentivized between 13 and 14 MW of BTM storage installed in the state in 2019.[^118] Both programs currently each have a cap of 500 new customers per year, or the equivalent of about 5 MW of storage per year for the next 15 years (e.g., until 2035), and are projected to meet that cap each year for the next 15 years. In 2023, GMP requested to lift this cap due to high customer demand for the programs.[^119]

The storage forecast from 2020 through 2050 for the entire New England region is shown in Figure 18. We model any resources marked as "Unclear" (where it is unknown whether the resource is programmatic or non-programmatic) as non-programmatic, and we assume virtually all future incremental BTM storage to be non-programmatic.

[^115]: Rhode Island Energy. Accessed August 14, 2023. _Battery Program_. Available at: [https://www.rienergy.com/RI-Home/ConnectedSolutions/BatteryProgram](https://www.rienergy.com/RI-Home/ConnectedSolutions/BatteryProgram).

[^116]: State of Rhode Island Office of Energy Resources. Accessed August 22, 2023. _State and Federal Energy Incentives_. Available at: [https://energy.ri.gov/incentives](https://energy.ri.gov/incentives).

[^117]: Green Mountain Power. Accessed August 22, 2023. _Home Energy Storage_. Available at: [https://greenmountainpower.com/rebates-programs/home-energy-storage/](https://greenmountainpower.com/rebates-programs/home-energy-storage/).

[^118]: Gheorghiu, Iulia. 2020. "Green Mountain Power expands PYOD [sic] and Tesla battery programs as it targets fossil peakers." _Utility Dive_. Available at: [https://www.utilitydive.com/news/green-mountain-power-to-roll-out-byod-and-tesla-battery-programs-as-it-targ/578573/](https://www.utilitydive.com/news/green-mountain-power-to-roll-out-byod-and-tesla-battery-programs-as-it-targ/578573/).

[^119]: Green Mountain Power. April 26, 2023. "GMP Requests Removal of Cap on Powerwall and BYOD Home Battery Programs to Expand Customer Access to Cost-Effective Backup Power". Available at: [https://greenmountainpower.com/news/gmp-requests-removal-of-cap-on-powerwall-and-byod-home-battery-programs/](https://greenmountainpower.com/news/gmp-requests-removal-of-cap-on-powerwall-and-byod-home-battery-programs/).

[PDF p. 106 | printed p. 88]

**Figure 18. BTM storage forecast for New England**

[DIAGRAM DESCRIPTION: Figure 18. BTM storage forecast for New England]
Line chart. X-axis: year, 2020 to 2050 (ticks every 5 years). Y-axis: "Modeled BTM Storage (MW)", 0 to 3,500 (gridlines every 500). Three series, labelled directly on the chart: (1) pink line "Future programmatic": about 100 MW in 2020, about 600 MW in 2024, about 1,070 MW in 2028, about 1,480 MW in 2030, about 2,000 MW in 2037, about 2,300 MW in 2040 and about 3,250 MW in 2050 (a visible change in slope near 2030); (2) dark-red line "Non-programmatic and historical programmatic": overlaps the pink line through about 2023 (about 450 to 500 MW), then rises almost linearly to about 940 MW in 2030, about 1,250 MW in 2035, about 1,650 MW in 2040 and about 2,500 MW in 2050; (3) orange horizontal line "Historical BTM storage only": flat at about 470 MW from about 2023 through 2050. Takeaway: modeled BTM storage grows to roughly 2,500 MW (non-programmatic plus historical programmatic) or about 3,250 MW (including future programmatic) by 2050, against about 470 MW of historical installations. Values read off the chart are approximate.
[→ See original PDF page 106 for visual rendering]

Our modeling applies program-specific battery dispatch profiles for BTM storage wherever possible. For programs where a specific battery dispatch profile is not described, we assume that storage will dispatch according to the CPS seasonal peak periods, in line with our methodology in AESC 2021. Under the CPS, systems may only get CPS credits for discharging within these hours, so we assume each system is limited to discharging once per day (or 365 cycles per year). Table 41 describes the dispatch profile we apply to each program.

Our BTM storage modeling assumes a round trip efficiency (RTE) of 85 percent for all storage systems as is consistent with field tests of battery storage performance.[^120] We calculate MWh from capacity assuming a 2-hour duration. For modeling purposes, BTM storage capacities are grossed up by 8 percent to reflect a conversion between retail MW and wholesale MW.

Given the lack of data on BTM storage projections for each program, it is sometimes challenging to determine what portion of the above programs might be deployed as part of an active demand management program managed by one of the AESC 2024 Sponsors, and what portion may be deployed regardless of actions taken by the AESC 2024 Sponsors. Table 41 describes what category each of the above programs appears to fall into. For the purposes of AESC 2024, we assume that only policies marked as "Programmatic" are programmatic; we model all other policies in all counterfactuals. Note that these "Non-programmatic" resources make up the vast majority of all BTM storage resources; constituting over 99 percent of BTM storage capacity in each modeled year.

[^120]: Deline, Chris, et al. July 2019. _Field-Aging Test Bed for Behind-the-Meter PV + Energy Storage_. National Renewable Energy Laboratory (NREL). Available at: [https://www.nrel.gov/docs/fy19osti/74003.pdf](https://www.nrel.gov/docs/fy19osti/74003.pdf).

[PDF p. 107 | printed p. 89]

**Table 41. Behind-the-meter storage categorization**

| State | Policy                                          | Categorization                                                                                                                                                                                                                                                                                                                                                       | AESC 2024 Methodology                                                                                                                                                                                     | Assumed AESC 2024 Dispatch Profile                                                                                 |
| ----- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| CT    | Connected Solutions                             | **Programmatic.** Program entirely administered by Eversource; no data available.                                                                                                                                                                                                                                                                                    | Assuming 0 MW, due to no available data. Program not accepting new participants after 12/1/2023.                                                                                                          | None (modeling program as 0 MW).                                                                                   |
| CT    | Energy Storage Solutions                        | **Programmatic.** Program administered by Connecticut Green Bank, Eversource, and United Illuminating; partial 2022–2023 data available.                                                                                                                                                                                                                             | 2022 and 2023 values are based on actual program data, as of 8/18/2023. We assume program grows linearly to meet the goal of 580 MW by 2030.                                                              | Winter (November 1 through March 31) 3 p.m. to 9 p.m., Summer (June 1 through September 30) 3 p.m. to 9 p.m.[^121] |
| ME    | Energy Storage System Program                   | **Non-Programmatic.** Program administered by Efficiency Maine Trust (EMT); no data available.                                                                                                                                                                                                                                                                       | Program-specific data unavailable. Statewide actual storage data (2019-2022) used from Governor's Energy Office of Maine. Numbers in 2023 and after are held constant at 2 MW.                            | Proposing to adopt CPS dispatch profile.                                                                           |
| MA    | SMART Program                                   | **Partially Programmatic.** Project may overlap with other Massachusetts BTM storage policies. Measures assumed to be counted in the CPS program. BTM projects are assumed to be 25% programmatic and 75% non-programmatic through 2034, and 15% programmatic and 85% non-programmatic from 2035 on. Standalone storage projects are assumed to be non-programmatic. | 2018–2023 values are based on actual program data, available through 10/3/2023. Numbers in 2035 and 2050 are based on MA statewide targets, as well as forecasts provided by the Study Group.             | Proposing to adopt CPS dispatch profile.                                                                           |
| MA    | Connected Solutions                             | **Programmatic.** This refers to data entries in utility target reports labeled "MA – Energy Efficiency/ DR Program."                                                                                                                                                                                                                                                | 2019–2022 values are based on MA 2022 ES Target Report data. Numbers in 2023–2025 assume continued average growth as calculated with existing data. Numbers in 2026 and after are held constant at 9 MW.  | Proposing to adopt CPS dispatch profile.                                                                           |
| MA    | Other                                           | **Unclear.** This refers to data entries in utility target reports that are not associated with SMART or Connected Solutions programs, including "MA–DOER/ MassCEC Funded Projects" and "Other" projects.                                                                                                                                                            | 2019–2022 values are based on MA 2022 ES Target Report data. Numbers in 2023–2025 assume continued average growth as calculated with existing data. Numbers in 2026 and after are held constant at 10 MW. | Proposing to adopt CPS dispatch profile.                                                                           |
| MA    | Cape & Vineyard Electrification Offering (CVEO) | **Programmatic.** Program entirely administered by Cape Light Compact; no data available.                                                                                                                                                                                                                                                                            | 2023–2024 values are based on approved pilot program design. Numbers in 2025 and after are held constant at 0.15 MW.                                                                                      | Proposing to adopt CPS dispatch profile.                                                                           |
| MA    | Clean Peak Standard (CPS)                       | **Unclear.** Project may overlap with other Massachusetts BTM storage policies.                                                                                                                                                                                                                                                                                      | We d not model [sic] additional CPS resources explicitly and are assuming it is otherwise met through other programs.                                                                                     | Winter (December 1 through February 28) 4 p.m. to 8 p.m., Spring (March 1 through May 14) 5 p.m. to 9              |

_Extractor note (not source text): the Clean Peak Standard (CPS) row's last cell breaks across the page; its remainder is the first row of the continued table below, after the page marker. The page also carries footnote 121 (printed at the foot of the page)._

[^121]: Eversource. Accessed August 18, 2023. _Connecticut Home Battery Storage Options_. Available at: [https://www.eversource.com/content/residential/save-money-energy/clean-energy-options/home-battery-storage](https://www.eversource.com/content/residential/save-money-energy/clean-energy-options/home-battery-storage).

[PDF p. 108 | printed p. 90]

_Table 41 (continued; the PDF repeats the header row at the top of the page)_

| State | Policy                                                | Categorization                                                                                                   | AESC 2024 Methodology                                                                                                                                                             | Assumed AESC 2024 Dispatch Profile                                                                                             |
| ----- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
|       |                                                       |                                                                                                                  |                                                                                                                                                                                   | p.m., Summer (May 15 through September 14) 3 p.m. to 7 p.m. and Fall (September 15 through November 30) 4 p.m. to 8 p.m.[^122] |
| NH    | Battery Storage Pilot Program                         | **Programmatic.** Program entirely administered by Liberty Utilities.                                            | 2020–2022 values are based on program evaluation data. 2023–2025 values assume Phase 2 of the pilot will be approved. Numbers in 2026 and after are held constant at 2.5 MW.      | Winter (November 1 through April 30) 3 p.m. to 8 p.m., Summer (May 1 through October 31) 3 p.m. to 8 p.m.[^123]                |
| RI    | Connected Solutions                                   | **Programmatic.** Program entirely administered by Rhode Island Energy.                                          | Values in 2025, 2035, and 2050 are based on forecasts from Rhode Island Energy, assuming linear growth between those years.                                                       | Summer (June 1 through September 30) 3 p.m. to 8 p.m., two to three hours event, for C&I.[^124]                                |
| RI    | Renewable Energy Fund (REF) Small-Scale Solar Program | **Non-Programmatic.** Program administered by Rhode Island Commerce.                                             | Assuming 0 MW, due to no available data.                                                                                                                                          | None (modeling program as 0 MW).                                                                                               |
| VT    | BYOD Program                                          | **Non-Programmatic.** Program entirely administered by Green Mountain Power (GMP) (not a program administrator). | Assuming 5 MW of annual growth, based on maximum allowed annual participation and GMP press statements that program waitlists are full multiple years out. Reaches 75 MW in 2035. | Proposing to adopt CPS dispatch profile.                                                                                       |
| VT    | Tesla Powerwall Program                               | **Non-Programmatic.** Program entirely administered by GMP (not a program administrator).                        | Assuming 5 MW of annual growth, based on maximum allowed annual participation and GMP press statements that program waitlists are full multiple years out. Reaches 88 MW in 2035. | Proposing to adopt CPS dispatch profile.                                                                                       |

Table 42 shows the total cumulative BTM storage projected to be installed in each state in New England, in 2025, 2035, and 2050. The modeled quantity of BTM storage in 2035 (inclusive of both programmatic and non- programmatic resources) is about three times larger than the 2035 quantity modeled in AESC 2021. Non-programmatic BTM storage resources are modeled in all counterfactuals except Counterfactual #6. Programmatic BTM storage resources are only modeled in Counterfactual #2, #3, and #5. In Counterfactual #6, we do not model any new BTM storage (programmatic or non-programmatic) installed in 2024 or any later years.

[^122]: Massachusetts Department of Energy Resources (DOER). August 7, 2019. _The Clean Peak Energy Standard_. Available at: [https://www.mass.gov/doc/drafts-cps-reg-summary-presentation/download](https://www.mass.gov/doc/drafts-cps-reg-summary-presentation/download). Slides 15 and 19.

[^123]: Liberty. Accessed August 22, 2023. _Battery Storage_. Available at: [https://new-hampshire.libertyutilities.com/bath/residential/smart-energy-use/electric/battery-storage.html#:~:text=The%20battery%20storage%20program%20is,called%20the%20Tesla%20Powerwall%202](https://new-hampshire.libertyutilities.com/bath/residential/smart-energy-use/electric/battery-storage.html#:~:text=The%20battery%20storage%20program%20is,called%20the%20Tesla%20Powerwall%202).

[^124]: RI Connected Solutions dispatch profile provided by Rhode Island Energy via email on October 23, 2023.

[PDF p. 109 | printed p. 91]

**Table 42. Modeled quantites [sic] of behind-the-meter storage (MW)**

| State                                                                               | 2025    | 2035      | 2050      |
| ----------------------------------------------------------------------------------- | ------- | --------- | --------- |
| Connecticut                                                                         | 218     | 580       | 580       |
| Maine                                                                               | 2       | 2         | 2         |
| Massachusetts                                                                       | 443     | 1,016     | 2,266     |
| New Hampshire                                                                       | 3       | 3         | 3         |
| Rhode Island                                                                        | 16      | 76        | 217       |
| Vermont                                                                             | 63      | 163       | 163       |
| **Total**                                                                           | **744** | **1,839** | **3,230** |
| Fraction of total MW attributable to incremental programmatic BTM storage resources | 21%     | 32%       | 23%       |

_Note: This table includes capacity from all programs, including both programmatic and non-programmatic BTM storage. Quantities are reported in retail terms, rather than in wholesale terms._

### Building electrification

Measures related to building electrification are projected to be a significant source of load growth over the study period, in certain counterfactuals. Primary examples of such measures include heat pumps for space and water heating. ISO New England developed a forecast of residential and commercial heat pump load as part of its CELT 2023 report.[^125] ISO New England developed this forecast in collaboration with regional stakeholders who provided information about heat pump programs, incentives, and policy targets across the New England states. Broadly speaking, heat pump adoption was modeled by state, by sector (residential and commercial), by end use (HVAC vs. water heating), by heat pump type (partial vs. whole building), by existing fuel system (gas, fuel oil, etc.), and by electrification technology (e.g., air- vs. ground-source heat pump). The modeling extends to 2050, although the report only provides data on energy consumption and peak load from 2023 through 2032.

Generally speaking, ISO New England bases its projections around residential heat pump adoption levels of about 15 percent in 2030 and 85 percent in 2050, and commercial heat pump adoption levels of about 15 percent in 2030 and 80 percent in 2050.

Relative to other load forecast components (e.g., energy efficiency and transportation electrification), ISO New England has published little granular data on its building electrification forecast, aside from state-specific projections. The ISO has published no data on hourly demand impacts. On October 23, ISO New England shared some more detailed information with Synapse (including adoption trajectories and associated demand by state, sector, and heating type from 2023 through 2032), but we have not yet used this data to inform AESC projections because this data was not available until October 23. Instead, Synapse's projections are currently based on the publicly available version of ISO New England's modeling.

[^125]: ISO New England. _Final 2023 Heating Electrification Forecast_. April 28, 2023. Available at [https://www.iso-ne.com/static-assets/documents/2023/04/heatFx2023_final.pdf](https://www.iso-ne.com/static-assets/documents/2023/04/heatFx2023_final.pdf).

[PDF p. 110 | printed p. 92]

Synapse first project the number of heat pumps added in each state from 2023 to 2050, primarily relying on the adoption trajectories published in the 2023 CELT forecast—as mentioned above.[^126] We divide annual heat pump additions into four categories: residential space heating, residential water heating, commercial space heating, and commercial water heating. We then subdivide space heating into partial and whole-home systems using technology breakdowns provided by ISO New England for 2032 and 2050 and calculating values for the intermediate years through linear interpolation.[^127]

Synapse translates these stock values into annual electricity demand using load and coefficient of performance (COP) assumptions. To relate COP to temperature, we apply a regression analysis (separately for residential space heating and commercial space heating, to create COP trendlines) based on data from ISO New England.[^128] We apply load assumptions based on end-use data for natural gas space heating measures from NREL's ResStock and ComStock for Massachusetts.[^129] Consistent with ISO New England's assumptions in the 2023 CELT forecast, we assume that partial systems have zero electricity load when temperatures drop below 20 degrees Fahrenheit; we calculate the number of hours when this is the case using the weather data described below. Also consistent with the 2023 CELT forecast, we assume that whole-home systems switch from heat pump heating to electric resistance heating when temperatures drop below 5 degrees Fahrenheit. Finally, we assume a retail to wholesale conversion factor of 6 percent.

Figure 19 shows the resulting electrification load in each year for New England as a whole. The Synapse estimate is 17 percent higher than ISO New England's in 2025 and nearly identical (0.1 percent higher) in 2032, the last year that ISO New England provides energy data. Differences are due to a combination of lower commercial heating load projections and higher residential load projections, as compared to ISO New England's.

For the purposes of AESC 2024, we assume all building electrification impacts are programmatic.[^130]

[^126]: Id., at slides 21, 25, 28, and 31. Note that based on Study Group feedback, we modified the trajectory for heat pump adoption in Massachusetts by relying on near-term projections of heat-pump builds described in the high end of the ID1 and ID2 projections as summarized in the following documents: [https://ma-eeac.org/wp-content/uploads/MA-EEAC-Workshop-4-Residential-Summary-FINAL.pdf](https://ma-eeac.org/wp-content/uploads/MA-EEAC-Workshop-4-Residential-Summary-FINAL.pdf) and [https://ma-eeac.org/wp-content/uploads/MA-EEAC-Workshop-2-IES-Summary_FINAL.pdf](https://ma-eeac.org/wp-content/uploads/MA-EEAC-Workshop-2-IES-Summary_FINAL.pdf). We received feedback from Study Group members representing program administrators in Rhode Island, Vermont, and Maine, but through discussion decided to not edit the adoption trajectories for these states or any other states save Massachusetts.

[^127]: Id., at slide 36 and 37.

[^128]: Id., at slide 36 and 37.

[^129]: See [https://resstock.nrel.gov/](https://resstock.nrel.gov/) and [https://comstock.nrel.gov/](https://comstock.nrel.gov/). We do not rely on ResStock and ComStock's load shapes for space-heating heat pumps, as we understand that these load shapes may be inappropriate to use due to low sampling and dated COPs. Furthermore, it is possible that the heat pump load shapes do not accurately account for pre-heating activities by users. As a result, we rely on the heating shape implied by natural gas furnaces, and we derive hourly space heating heat pump operation based on this heating demand. We rely on ResStock and ComStock for heat pump water heating operation due to the relative lack of data available on these technologies, their relatively low impact on total and peak loads, and their relative independence of electricity demand to outside temperatures.

[^130]: Note that historically, the CELT forecast has implicitly projected a small amount of heat pump load growth due to ISO New England's regression model.

[PDF p. 111 | printed p. 93]

**Figure 19. Modeled incremental building electrification load**

[DIAGRAM DESCRIPTION: Figure 19. Modeled incremental building electrification load]
Stacked area chart. X-axis: year, 2020 to 2050 (ticks every 5 years; the areas begin in 2023). Y-axis: "Wholesale Building Electrification Impacts (TWh)", 0 to 40 (gridlines every 5). Six stacked layers, labelled directly on the chart at the right edge; from bottom to top: (1) "Res full space heating" (darkest teal): about 1.3 TWh in 2030, about 5.3 TWh in 2040 and about 9.5 TWh in 2050; (2) "Res partial space heating" (medium teal): top of layer at about 4 TWh in 2030, about 14 TWh in 2040 and about 22.5 TWh in 2050; (3) "Res water heating" (light blue): top at about 25.5 TWh in 2050; (4) "Comm full space heating" (dark maroon): top at about 30 TWh in 2050; (5) "Comm partial space heating" (red): top at about 31.5 TWh in 2050; (6) "Comm water heating" (light pink): top at about 33.3 TWh in 2050, the total. The total is about 5 TWh in 2030 and about 20 TWh in 2040. Takeaway: modeled incremental building electrification load grows to about 33 TWh (wholesale) by 2050, with residential space heating (full plus partial) the largest component at about 22.5 TWh. Values read off the chart are approximate.
[→ See original PDF page 111 for visual rendering]

To forecast hourly building electrification for each end use in each state through 2050, we combine the annual building electrification energy demand from 2023 to 2050 and hourly load profiles in EnCompass.

Counterfactuals #1 and #2 only include the building electrification installed through 2023; all other future building electrification measures are not included. In contrast, the full set of building electrification measures projected to be installed through 2050 are modeled in Counterfactuals #3, #4, #5, and #6.

### Transportation electrification

Over the study period of AESC 2024 (e.g., through 2050), vehicle electrification is projected to increase demand for electricity. In CELT 2023, ISO New England developed a forecast for electric vehicle electricity consumption.[^131] The CELT forecast is based on information supplied by state policies and state agencies, federal rulemaking, and other sources. CELT 2023 includes two forecasts—a "Full Electrification" adoption scenario and a "CELT 2023" adoption scenario. The ISO identifies the first scenario ("Full Electrification") as being for informational purposes only and provides less information for it than the "CELT 2023 scenario." Both scenarios are relatively similar, with electric vehicles

[^131]: For more on ISO New England's CELT 2023 transportation electrification forecast, see ISO New England. _Final 2023 Transportation Electrification Forecast_. April 28, 2023. Available at [https://www.iso-ne.com/static-assets/documents/2023/04/transfx2023_final.pdf](https://www.iso-ne.com/static-assets/documents/2023/04/transfx2023_final.pdf).

[PDF p. 112 | printed p. 94]

representing about 20 to 30 percent of vehicles on the road ("stock") by the mid-2030s, and with all or almost all vehicles being electric by the late 2040s (see Figure 20).

In its projections, ISO New England develops state-specific projections of electric vehicle stock and associated electricity demand. These projections are developed for five different classifications of vehicles: (1) light-duty personal vehicles, (2) light-duty fleet vehicles, (3) medium-duty delivery vehicles, (4) school buses, and (5) transit buses. We note that this projection does not include all vehicle types (for example, other medium-duty vehicles, heavy-duty vehicles, and non- and off-road vehicles are not included) but does address the majority of vehicles driven in New England (in terms of number of vehicles, fuel consumption, and emissions impacts). ISO New England's projection considers daily charging for each vehicle type by month; variations in charging profiles by month, vehicle type, and day-of-week; and variations in vehicle-miles traveled and electricity consumption by vehicle type.

Using data posted publicly by ISO New England, Synapse estimates a projection of annual load requirements for electrified vehicles and hourly load shapes. Figure 20 shows forecasts both for CELT 2023 (used in AESC 2024) as well as ISO New England's more ambitious "Full Electrification" case. CELT 2023 provides data for load projections through 2032 only; these projections are extrapolated for each state and vehicle type through 2050, based on the shape of the "Full Electrification" case through 2050.

**Figure 20. ISO New England's 2023 forecast for transportation electrification**

[DIAGRAM DESCRIPTION: Figure 20. ISO New England's 2023 forecast for transportation electrification]
Small-multiple line charts, five panels (three on the top row, two centered on the bottom row), one per vehicle class: "Light-Duty Personal", "Light-Duty Fleet", "Medium-Duty Delivery", "School Bus" and "Transit Bus". Every panel has an X-axis of year from 2020 to 2050, a left Y-axis "Cumulative # of EVs" (Light-Duty Personal: in millions, 0 to above 10; Light-Duty Fleet: 0 to 600,000+; Medium-Duty Delivery: 0 to 20,000; School Bus: 0 to 25,000+; Transit Bus: 0 to 3,000+) and a right Y-axis (orange) "% of Vehicle Stock" from 0% to 100%. Three series per panel, shown in the legend at the bottom of the figure: a light-grey solid line "Full Electrification" (an S-shaped curve that rises from about 2025 and flattens near 100% of the vehicle stock by roughly 2045 to 2050), a dotted colored line "CELT 2022" and a solid colored line "CELT 2023" (the last two run only from about 2021 to 2032, and CELT 2023 generally lies above CELT 2022). Each panel carries an annotation of the total vehicle population (the 100% level): Light-Duty Personal "Vehicle Population: 11,700,000" (CELT 2023 reaches about 3 million EVs by 2032), Light-Duty Fleet "Vehicle Population: 724,000" (CELT 2023 reaches about 250,000 EVs by 2032 versus about 60,000 for CELT 2022), Medium-Duty Delivery "Vehicle Population: 20,000" (CELT 2023 about 3,500 by 2032), School Bus "Vehicle Population: 26,000" (CELT 2023 about 6,500 by 2032) and Transit Bus "Vehicle Population: 3,000" (CELT 2023 about 900 by 2032). Takeaway: ISO New England's CELT 2023 forecast covers only through 2032; the "Full Electrification" case reaches nearly all vehicles by the late 2040s and gives the shape used to extrapolate CELT 2023 to 2050. Values read off the charts are approximate.
[→ See original PDF page 94 for visual rendering]

_Notes: The grey line denotes the "Full Electrification" trajectory. The solid non-grey line indicates the trajectory used by ISO New England in CELT 2023. ISO New England also provides state-specific detail, which is used in AESC 2024's estimate for transportation load._

_Source: "Final 2023 Transportation Electrification Forecast." April 28, 2023. Available at [https://www.iso-ne.com/static-assets/documents/2023/04/transfx2023_final.pdf](https://www.iso-ne.com/static-assets/documents/2023/04/transfx2023_final.pdf). Page 10._

_Extractor note (not source text): in the PDF the hyperlink on this source line points to `https://www.iso-ne.com/static-assets/documents/2023/04/transfx2023_final.pdf.%20Page%2010` (the printed text ", Page 10" was swallowed into the link target); the link above is the clean PDF address._

[PDF p. 113 | printed p. 95]

Based on feedback from the Study Group, we added two vehicle types: heavy-duty "single" vehicles and heavy-duty "combination" vehicles.[^132] The vehicles within these two types are diverse in size and use case, making it challenging to develop a sophisticated projection within the time and budget constraints of AESC 2024. As a result, we assume the adoption of these vehicles and charging load shape follows that of medium-duty vehicles, with adjustments made to reflect the number of heavy-duty vehicles relative to medium-duty vehicles (heavy-duty vehicles are fewer in number), the charging requirements of heavy-duty vehicles relative to medium-duty vehicles (heavy-duty vehicles are typically larger and heavier, implying a greater number of kWh needed to travel a single mile), and the travel requirements of heavy-duty vehicles relative to medium-duty vehicles (heavy-duty vehicles typically travel more miles per year than medium-duty vehicles, suggesting an overall higher level of annual electricity consumption).

Figure 21 illustrates the annual energy projection for electric vehicles we use in AESC 2024. By 2050, annual energy impacts from electric vehicles approach 60 TWh, about half of ISO New England's total electricity demand as of the early 2020s. The figure shows 83 percent of load is attributable to personal light-duty electric vehicles, 11 percent of load is attributable to fleet light-duty electric vehicles, and 6 percent of load attributable to other vehicle types.

**Figure 21. Projected wholesale electricity consumption from electric vehicles in ISO New England for all Counterfactuals**

[DIAGRAM DESCRIPTION: Figure 21. Projected wholesale electricity consumption from electric vehicles in ISO New England for all Counterfactuals]
Stacked area chart. X-axis: year, 2020 to 2050 (ticks every 5 years; the areas begin in about 2023). Y-axis: "Wholesale Annual Energy Impacts from Electric Vehicles (TWh)", 0 to 70 (gridlines every 10). Three stacked layers, labelled directly on the chart at the right edge; from bottom to top: (1) "Light-duty personal" (dark teal): about 9 TWh in 2030, about 42 TWh in 2042 and about 51 TWh in 2050; (2) "Light-duty fleet" (light purple-blue): top of layer at about 57 TWh in 2050; (3) "Medium-duty delivery, school buses, transit buses, heavy duty" (orange): top of layer at about 60 TWh in 2050, the total. The total is about 10 TWh in 2030, about 35 TWh in 2037 and about 50 TWh in 2042. Takeaway: electric-vehicle load grows to about 60 TWh by 2050, of which light-duty personal vehicles are the large majority; growth is fastest between about 2030 and 2042 and flattens after about 2045. Values read off the chart are approximate.
[→ See original PDF page 113 for visual rendering]

_Note: In both the CELT 2023 and AESC 2024 forecast, the first three vehicle categories (medium-duty delivery, school buses, and transit buses) are disaggregated and modeled independently. They are shown as a single series on this chart only for illustrative purposes. Likewise, both CELT 2023 and AESC 2024 model five different vehicle trajectories within each of the six states; these are not shown in this figure._

[^132]: Heavy-duty "single" vehicles include vehicles like dump trucks, which consist of a single chassis. In contrast, heavy-duty "combination" vehicles are those that consist of multiple parts (like a semi cab and an associated trailer).

[PDF p. 114 | printed p. 96]

Figure 22 shows the daily load profiles we use in AESC 2024 for non-holiday weekdays (separate profiles have been created for holidays and weekends). These profiles are derived from the seasonal profiles posted for each vehicle type by ISO New England in CELT 2023, and include some amount of home charging, workplace charging, and public charging.[^133] These daily load profiles are also applied to the monthly variations in daily charging demand aggregated by ISO New England in CELT 2023. Under these assumptions, electric vehicles typically use less electricity in summer months than in winter months, due to HVAC-related demand and other cold weather inefficiencies. For personal light-duty vehicles, we note that ISO New England assumes an average daily charging demand in July that is about three-quarters the daily charging demand in January.

The EnCompass model estimates system peak impacts dynamically based on the combination of aggregate system load in each year, hourly load shapes, and monthly variations in demand. Our modeling assumes static load shapes in line with those described by ISO New England in its CELT 2023 forecast. We do not incorporate any assumptions related to managed charging or time-of-use rates (see Demand response section, above, for more information on this topic).

AESC 2024 includes the transportation electrification component in all counterfactuals. In other words, we assume that all transportation electrification impacts are non-programmatic.

[^133]: In AESC 2024, we only model a single load profile for each vehicle type, rather than profiles that vary by month or season. This is due to the relative similarity in load shapes for personal light-duty vehicles and fleet light-duty vehicles assumed by ISO New England in CELT 2023; this vehicle type has little variation in charging patterns month-to-month, and represents the vast majority of vehicles and electricity consumption.

[PDF p. 115 | printed p. 97]

**Figure 22. Daily load profiles modeled in AESC 2024 for non-holiday weekdays**

[DIAGRAM DESCRIPTION: Figure 22. Daily load profiles modeled in AESC 2024 for non-holiday weekdays]
Five vertically stacked line charts sharing one X-axis, "hour" 1 to 24 (hour of day). Each panel's Y-axis runs 0% to 10%, and the common Y-axis title is "Percent of daily charging" (percent of daily charging in each hour). Series, labelled directly on the chart, from top panel to bottom: (1) "Personal LDVs" (dark blue): about 4% in hour 1, falling to a minimum of about 1.5% in hours 5 to 6, rising to about 5% at hour 10, about 3.5% in hours 13 to 16, then rising to a daily maximum of about 7% in hours 20 to 22 and about 6% in hour 24; (2) "Fleet LDVs" (light purple): about 3.5% in hours 1 to 4, rising to a peak of about 7.5% in hours 8 to 9, falling to about 2.5% in hours 15 to 16, then about 4% in hours 20 to 24; (3) "Medium-duty delivery" (orange): about 7% in hour 1, peaking at about 9% in hour 3, falling to about 5% in hour 6 and about 3% from hour 10 through hour 22, then rising to about 5% in hour 24; (4) "School Bus" (yellow): about 2% in hour 1, a minimum of about 0.7% in hours 4 to 6, rising to a morning peak of about 8% in hour 10, falling to about 2% in hour 15, a second peak of about 7.7% in hours 19 to 20, then about 3% in hour 24; (5) "Transit bus" (dark red): about 5.7% in hours 1 to 2, about 4% from hour 5 through hour 16, a minimum of about 2.6% in hour 19, then rising to about 5% in hours 23 to 24. Takeaway: light-duty personal vehicles charge mostly in the evening, fleet vehicles and school buses charge in the morning (school buses also late afternoon), and medium-duty delivery vehicles charge overnight. Values read off the chart are approximate.
[→ See original PDF page 115 for visual rendering]

_Note: Separate profiles (not shown) are used for weekends and holidays. Heavy-duty vehicles utilize the daily load profile for medium-duty vehicles._

### Distributed generation

For the purposes of AESC 2024, "distributed generation" is assumed to include only distributed solar. As with demand response and BTM storage, we model distributed generation as a supply-side resource in the EnCompass model. Impacts from distributed generation are applied to peak demand calculations in each counterfactual.

The 2023 CELT forecast contains a projection of BTM solar. This forecast applies material discount factors (35 to 50 percent) to post-policy distributed PV installation to reflect uncertainty associated with future policies and/or market conditions. This approach, which yields lower PV load reductions than what may be realistic, is appropriate for reliable planning and operation of the system. For the purpose of the AESC 2024 study, we used a distributed PV forecast that is more representative of expected solar installation under existing policies and future policies (if applicable) and / or market conditions, based on research and market analysis. For more information on the Synapse Team's methodology for

[PDF p. 116 | printed p. 98]

modeling distributed solar, including policies modeled and load profiles, see Section 4.4: _Renewable energy_ .

All counterfactuals include this component and there is no differentiation between programmatic or non-programmatic components.

### Other load components not modeled in AESC 2024

There are other emerging DSM programs (see Table 43) that may be modeled using the 8,760 avoided cost values. As in AESC 2021, these resources are not modeled in any AESC 2024 counterfactuals. Likewise, AESC 2024 does not currently assume any quantity of industrial electrification other than that related to HVAC or water heating.

**Table 43. Current status of emerging DSM technologies**

| Technology                           | Other Components or Considerations                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Conservation Voltage Reduction (CVR) | The traditional avoided costs streams may be applied for CVR programs. CVR occurs in front of the customer meter. Some feeders, such as those with high motor load, may not be appropriate for CVR. CVR factors for feeders would need to be quantified. Utilities must maintain service quality requirements, which may limit applicability. Distribution planning personnel from program administrators should weigh in on the matter. |
| Volt-Var Control (VVO)               | The traditional avoided costs streams may be applied for VVO programs. VVO occurs in front of the customer meter. Hourly data for real and reactive power will determine hourly line losses, and the difference between baseline and impact losses yields energy savings. Distribution planning personnel from program administrators should weigh in on the matter.                                                                     |

### Energy losses

Electric systems incur energy losses when delivering power from power plants to customers' sites through T&D wires. We develop T&D losses in AESC 2024 for two main reasons:

- First, the development of certain categories of load forecast components requires the conversion between retail electricity consumption and wholesale electricity impacts. In this case, T&D losses are inputs into the avoided costs.
- Second, readers of AESC 2024 may wish to apply a T&D loss factor to convert the wholesale avoided costs calculated in AESC into retail avoided costs. In this case, T&D loss factors are applied to modeling outputs.

The following section primarily addresses the development of T&D losses under the first category, as it is our understanding that each program administrator calculates and applies a T&D loss factor (or uses a T&D loss factor based on state precedent). However, readers may wish to review the following section to help inform their selection of loss factors. We note that the selection of T&D loss factors is unchanged from the AESC 2021 study.

[PDF p. 117 | printed p. 99]

#### Marginal loss factors

Multiple factors affect the amount of energy loss, including resistance in wires, system utilization rates, and weather conditions. Energy losses are generally higher when loads are higher and significantly higher during peak periods because resistive losses in wires increase with the square of the load (loss power = $I^2R$). This means that line losses for incremental loads (marginal losses) that would be avoided by DSM programs are likely higher than average line losses. On the other hand, a certain amount of loss, ranging from 20 percent to 30 percent of the entire loss, are "no-load losses" that do not increase with the square of the current, unlike resistive losses. These losses incur to energize the system (i.e., create a voltage available to serve a load).[^134] This means that the influence of resistive losses is greater at higher load levels because the impact of the no-load losses is fixed and relatively smaller at higher load levels.

A 2011 Regulatory Assistant Project (RAP) paper, "Valuing the Contribution of Energy Efficiency to Avoided Marginal Line Losses and Reserve Requirements," discusses line loss factors in detail. This paper presents an example of line loss factors and demonstrates how marginal and average losses vary at different system load levels, as shown in Figure 23. This figure shows that the increases in marginal losses are greater than the increases in average losses as the system load levels increase. For example, when the system is loaded at 50 percent of the capacity, average and marginal losses are approximately 6 percent and 8 percent respectively. And when the load is near its capacity, average and marginal losses are approximately 12 percent and 20 percent respectively.

**Figure 23. Average and marginal line loss factors from Lazar and Baldwin**

[DIAGRAM DESCRIPTION: Figure 23. Average and marginal line loss factors from Lazar and Baldwin]
Line chart reproduced from the RAP paper, with an in-image title "Average and Marginal Line Losses" and subtitle "Assumes 7% average losses; 25% No-load, 75% $I^2R$". X-axis: "Percent of Maximum System Load", ticks at 33%, 42%, 50%, 58%, 67%, 75%, 83%, 92% and 100%. Y-axis: "Losses as percentage of load (incremental load)", 0% to 25% (gridlines every 5%). Two series, labelled directly on the chart: (1) red line "Marginal Losses": starts at about 7.7% near 42% of maximum load, about 8% at 50%, about 10% at 58%, about 13% at 75%, about 15% at 83%, about 17.5% at 92% and about 20% at 100% (the line ends just beyond 100%); (2) blue line "Average Losses": about 5.8% from 33% to 42%, about 6% at 50%, about 8% at 75%, about 9.5% at 83%, about 10.5% at 92% and about 11.5% at the right end. Takeaway: marginal losses rise faster than average losses as system load rises and exceed them everywhere; the text reads about 6% (average) versus 8% (marginal) at 50% load and about 12% versus 20% near capacity. Values read off the chart are approximate.
[→ See original PDF page 117 for visual rendering]

_Source: Reproduced from Figure 4 in "Valuing the Contribution of Energy Efficiency to Avoided Marginal Line Losses and Reserve Requirements." (2011) Regulatory Assistance Project (RAP). Available at [https://www.raponline.org/wp-content/uploads/2016/05/rap-lazar-eeandlinelosses-2011-08-17.pdf](https://www.raponline.org/wp-content/uploads/2016/05/rap-lazar-eeandlinelosses-2011-08-17.pdf)._

[^134]: Regulatory Assistant Project. 2011. Valuing the Contribution of Energy Efficiency to Avoided Marginal Line Losses and Reserve Requirements. Available at [http://www.raponline.org/wp-content/uploads/2016/05/rap-lazar-eeandlinelosses-2011-08-17.pdf](http://www.raponline.org/wp-content/uploads/2016/05/rap-lazar-eeandlinelosses-2011-08-17.pdf).

[PDF p. 118 | printed p. 100]

To accurately estimate annual average marginal losses, we need to know detailed load data and system utilization rates for each hour of a year. However, details on system utilization rates are not readily available for ISO New England. The RAP paper suggests a rule of thumb value that marginal losses are about 1.5 times average losses. Thus, we use a factor of 1.5 to convert annual average line losses to marginal line losses. This value is also the value recommended by some stakeholders, including one local utility, in New Jersey and recently adopted by New Jersey Board of Public Utilities for establishing the New Jersey Cost Test.[^135] In AESC 2024, we apply a marginal loss factor to any incremental load added in a given year; all other portions of the load (i.e., the quantity that is less than or equal to the total load in the previous year) utilize an average loss factor. We use an average loss factor of 6 percent and a marginal loss factor of 9 percent (calculated by multiplying 6 percent by 1.5).[^136]

For estimating marginal losses associated with capacity, we would need to know the system utilization factor at peak hours, or in other words, the degree to which the T&D system is stressed. While the utilization rates at the peak hours are by definition higher than the average rate for an entire year, detailed data for system utilization rates for the entire ISO New England grid for peak hours is not readily available. Thus, we rely on a larger factor than used for annual energy. Based on the data in Figure 23, factors for marginal losses over average losses range from 1.4 at a 50 percent system utilization factor to 2.6 at a 92 percent system utilization factor. Based on this range, we rely on a simple factor of 2.0. For the purposes of calculating the wholesale impact of load components (see above), we apply a marginal loss factor of 16 percent (calculated by multiplying 8 percent by a factor of 2.0) and an average loss factor of 8 percent to any existing demand (e.g., the quantity of demand in a year that is equal to or less than the previous year's demand).[^137]

For more on applying energy losses to wholesale avoided costs, see _Appendix B: Detailed Electric Outputs_.

### Aggregate impacts

This section describes the aggregate impacts of the above load components, both in terms of annual load impacts and seasonal peak demand.

#### Annual load impacts

Figure 24 and Figure 25 show the aggregate annual impacts on load from all load components for Counterfactual #1 and Counterfactual #5, respectively. Counterfactual #1 (which includes transportation

[^135]: New Jersey Board of Public Utilities. 2020. Order Adopting the First New Jersey Cost Test. Docket No. QO19010040 and QO20060389.

[^136]: Note that 6 percent is the average T&D loss factor assumed by ISO New England for its long-term energy forecast. ISO New England. April 28, 2923 [sic]. _Final 2023 Heating Electrification Forecast_. Slide 41. Available at [https://www.iso-ne.com/static-assets/documents/2023/04/heatFx2023_final.pdf](https://www.iso-ne.com/static-assets/documents/2023/04/heatFx2023_final.pdf).

[^137]: See ISO New England Market Rules, Section III.13.1.4.1.1.6.(a).

[PDF p. 119 | printed p. 101]

electrification and non-programmatic BTM storage and demand response but does not include any new energy efficiency or building electrification built after 2023) reaches load levels of about 220 TWh by 2050. This is roughly a 75 percent increase in load, relative to today. Most of this increase in load is a result of transportation electrification. In comparison, Counterfactual #5 (which also includes transportation electrification, as well as new energy efficiency, building electrification measures, and both programmatic and non-programmatic BTM storage and demand response resources) reaches load levels of about 240 TWh by 2050. This is about a doubling in load, relative to today. In this counterfactual, about half of the load increase is attributable to transportation electrification and half of the load increase is attributable to building electrification.

**Figure 24. Aggregate load impacts, Counterfactual #1**

[DIAGRAM DESCRIPTION: Figure 24. Aggregate load impacts, Counterfactual #1]
Stacked area chart with an overlaid line. X-axis: year, 2024 to 2050 (labelled every 2 years). Y-axis: "ISO New England Annual Wholesale Load (TWh)", 0 to 300 (gridlines every 50). Layers, labelled directly on the chart at the right edge: "Conventional load, net of energy efficiency" (brown, bottom): about 123 TWh in 2024 rising to about 160 TWh in 2050; "Transportation elec." (green, above it): brings the total to about 218 TWh in 2050 (the gap between brown and the top of the green grows from near zero in 2024 to about 58 TWh in 2050); "Building elec." (blue label; no visible band in this counterfactual); "Energy efficiency" (orange): a band above the net-load line that is about 20 TWh thick in 2024 (top at about 142 TWh) and narrows to nothing by about 2034 as the measures installed through 2023 expire. The black line "Net load" runs from about 123 TWh in 2024 to about 218 TWh in 2050. Takeaway: in Counterfactual #1, load grows about 75 percent by 2050, mostly from transportation electrification, with efficiency savings from pre-2024 measures fading out. Values read off the chart are approximate.
[→ See original PDF page 119 for visual rendering]

_Note: This figure does not account for demand impacts related to storage._

[PDF p. 120 | printed p. 102]

**Figure 25. Aggregate load impacts, Counterfactuals #4, #5, #6**

[DIAGRAM DESCRIPTION: Figure 25. Aggregate load impacts, Counterfactuals #4, #5, #6]
Stacked area chart with an overlaid line. X-axis: year, 2024 to 2050 (labelled every 2 years). Y-axis: "ISO New England Annual Wholesale Load (TWh)", 0 to 300 (gridlines every 50). Layers, labelled directly on the chart at the right edge, from bottom to top: "Conventional load, net of energy efficiency" (brown): about 123 TWh in 2024 rising to about 145 TWh in 2050; "Transportation elec." (green): top of layer at about 205 TWh in 2050; "Building elec." (blue): top of layer at about 238 TWh in 2050; "Energy efficiency" (orange): a band on top of the stack that stays about 15 to 20 TWh thick (top at about 142 TWh in 2024 and about 253 TWh in 2050), i.e. it sits above the net-load line. The black line "Net load" runs from about 123 TWh in 2024 to about 237 TWh in 2050. Takeaway: with continued programmatic efficiency and building electrification, net load reaches about 240 TWh by 2050, with roughly equal increments from transportation and building electrification. Values read off the chart are approximate.
[→ See original PDF page 120 for visual rendering]

_Note: This figure does not account for demand impacts related to storage._

#### Peak demand forecasts and capacity requirements

Synapse calculates coincident winter and summer peak demand dynamically within the EnCompass model. We apply hourly load shapes for each of the load components (conventional load, energy efficiency, transportation, and so on) to annual projections of load for each component and for each region. We then sum the resulting hourly loads for each component and each region, with the regional, coincident winter, and summer peaks identified endogenously by the model and then used for capacity market calculations. Figure 26 shows the resultant seasonal peaks for summer months (June through September, inclusive) and winter months (all eight other months) in Counterfactual #1 and #5.[^138]

In Counterfactual #1, which does not include any new DERs installed after 2023 but does include demand growth from conventional load and vehicle electrification, coincident summer peak demand is projected to increase by about 57 percent, while coincident winter peak is projected to increase by about 98 percent. This leads to a 2050 where coincident winter peak approaches but does not surpass summer peak, with a 2050 winter peak just 5 percent lower than the 2050 summer peak.

Counterfactual #2, which is the same as Counterfactual #1 except for the inclusion of programmatic energy efficiency, sees summer peaks increasing by 46 percent and winter peaks increasing by 88 percent.[^139] In this counterfactual, the 2050 winter peak just 3 percent lower than the 2050 summer peak. [sic: "is" missing]

[^138]: Note that peaks (exclusive of demand response and storage) for Counterfactuals #4, #5, and #6 are identical.

[^139]: This scenario also includes programmatic behind-the-meter storage and demand response. However, as modeled in EnCompass, these resources do not affect the demand-side peaks.

[PDF p. 121 | printed p. 103]

Meanwhile, in Counterfactual #5, which features new deployment of all programmatic DER types throughout the study period, along with load growth from conventional load and vehicle electrification, coincident winter peak demand surpasses coincident summer peak demand in 2036. By 2050, winter peak demand is 164 percent higher than in 2024. Summer peak demand increases are similar to Counterfactual #1, with increases of about 49 percent from 2024 through 2050.

Counterfactual #3 is similar to Counterfactual #5 in that it includes deployment of programmatic building electrification measures. However, it does not include programmatic energy efficiency measures. As a result, by 2050, winter peak demand is 175 percent higher than in 2024, and summer peak demand is 60 percent higher than in 2024.

We note that seasonal peak demand increases in all modeled counterfactuals are not smooth. Instead, peak demand is observed to increase (and in rare cases decrease) in ways that appear discontinuous relative to neighboring years. This is a result of each of the load components modeled in AESC increasing at different rates, in different parts of the region. This difference in rate-of-increase leads to shifts in when the peak demand may occur within each season, which can lead to discontinuous-looking results in terms of year-on-year peak demand changes. Because of this, counterfactuals with fewer modeled load components (like Counterfactual #1) generally feature smoother increases in seasonal peak demand than counterfactuals with many different modeled load components. Because we conduct our modeling with full optimization, we do not expect these shifts in total peak demand to have a significant impact on resource builds.

**Figure 26. Seasonal peak demand forecasts for ISO New England in Counterfactual #1 and Counterfactual #5**

[DIAGRAM DESCRIPTION: Figure 26. Seasonal peak demand forecasts for ISO New England in Counterfactual #1 and Counterfactual #5]
Line chart. X-axis: year, 2024 to 2050 (labelled every 2 years). Y-axis: "New England-wide Seasonal Peaks (GW)", 0 to 50 (gridlines every 5). Four series, labelled directly on the chart at the right edge: (1) light-blue line "CF#5, Winter": about 17.3 GW in 2024, about 25 GW in 2033, crossing above the summer lines in the mid-2030s, about 34 GW in 2039, about 39 GW in 2042, about 43 GW in 2046 and about 46 GW in 2050; (2) pink line "CF#5, Summer": about 23 GW in 2024, about 27 GW in 2032, about 30 GW in 2038, about 34 GW in 2050; (3) red line "CF#1, Summer": about 23 GW in 2024, about 27 GW in 2030, about 30 GW in 2035, about 34 GW in 2042, about 36 GW in 2050; (4) teal line "CF#1, Winter": about 17.3 GW in 2024, about 25 GW in 2034, about 30 GW in 2040, about 34.5 GW in 2050. The lines are not smooth year to year. Takeaway: in Counterfactual #5 the winter peak overtakes the summer peak around 2036 and reaches about 46 GW by 2050, while in Counterfactual #1 winter peak approaches but stays below summer peak (about 34 versus about 36 GW in 2050). Values read off the chart are approximate.
[→ See original PDF page 121 for visual rendering]

_Note: Peak demand projections for other counterfactuals can be found in the AESC 2024 User Interface Excel workbooks._

The load forecast in one year is used in the FCA early in the next year to set the installed-capacity requirement for the capacity period starting three years after that. For example, under the current capacity market structure, the peak forecast for the summer of 2024 (released in May 2023) will be used

[PDF p. 122 | printed p. 104]

to set the installed-capacity requirement for FCA 18 (held in February 2024) which sets the capacity obligations and prices for the period June 2027 to May 2028. Under our future conceptualization of the capacity market (starting in June 2028), we model a change to a prompt market where projections of demand for a particular year are forecasted only one year in advance of the delivery year. We note that because our models do not differentiate between prompt markets and three-year-ahead markets, there is no functional difference in terms of how projections of peak demand are used as an input to estimating avoided capacity costs in AESC 2024. For more information on how forecasted demand impacts the capacity market, see Chapter 5: _Avoided Capacity Costs_.

_Extractor note (not source text): PDF p. 122 is shared with the next file. The page continues, below this point, with the heading "4.4. Renewable energy assumptions" and its text, and with footnotes 140 and 141, all of which are transcribed in `04b_common_electric_assumptions_4-4_to_4-8.md` and not here._

[PDF pp. 123-436 not transcribed: the rest of Chapter 4 (§4.4 Renewable energy assumptions through §4.8), in `04b_common_electric_assumptions_4-4_to_4-8.md`, and Chapters 5-12 and Appendices A-K, in the other files of this folder (see README.md)]
