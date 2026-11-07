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
extraction_scope: "partial: PDF pp. 365-367 (printed pp. 347-349), Appendix A: Usage Instructions; the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Appendix A: how users extrapolate AESC values past 2050 (CAGR of a linear regression over the last six years), compute levelized costs (10-, 15- and 30-year periods, 1.74 percent real discount rate, Excel PMT/NPV formula), convert 2024 constant dollars to nominal dollars, and compare AESC 2024 with AESC 2021."
why_here: "Tells us how to reproduce AESC levelization, dollar-year conversion and post-2050 extrapolation when we use AESC avoided costs as marginal-cost inputs or benchmarks in New England rate design and cost allocation work."
---

_Extractor note (not source text): this file holds PDF pp. 365-367 (printed pp. 347-349) of AESC 2024, Appendix A: Usage Instructions; the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. The text is transcribed verbatim, including the source's own slips, which are flagged inline with `[sic]`._

[PDF pp. 1-364 not transcribed: front matter and Chapters 1-12 (executive summary through sensitivity analysis), in the other files of this folder (see README.md)]

[PDF p. 365 | printed p. 347]

# Appendix A: Usage Instructions

This appendix describes how AESC 2024 users can extrapolate values post-2050, how to compute levelization, how to convert between nominal and constant dollars, and how to compare results from this AESC study to previous versions. This appendix also includes a description of the role of energy efficiency programs in the capacity market.

### Extrapolation of values post-2050

For AESC 2024, the Synapse Team recommends using the same extrapolation approached [sic] used in AESC 2021. In developing our recommendation, the Synapse Team notes the following:

- The Study Group expressed a desire for a single extrapolation methodology for use across all avoided cost categories for ease of use.
- The Study Group expressed a desire for an extrapolation technique to be both (a) based on data from years close to the extrapolation period and (b) representative of the overall trend during this period (rather than being heavily weighted by one or two outlying data points).
- The "best" extrapolation method should be selected based on the one technique that best meets the needs expressed for extrapolation, rather than the one that produces the best-looking or most reasonable result for a particular avoided cost series.

Specifically, the Synapse Team recommends an approach that estimates a compound annual growth rate (CAGR) of the linearly regressed trend of the last six years of each avoided cost series. Figure 60 displays an illustrative version of this approach; a CAGR is estimated over the red series. This regression step is effectively a smoothing step, as it reduces the impact from individual "noisy" datapoints.[^416]

Note that through the use of the _AESC 2021 User Interface_ and other appendices, readers of AESC 2024 can calculate their own extrapolated values if their policy context requires some alternate methodology

[^416]: There are three exceptions to this recommendation. First, we estimate capacity price shifts in 2051–2068 (used to calculate capacity DRIPE benefits in these years) by examining the median price shift from 2028 through 2050. A median is used rather than a trend plus CAGR because small year-on-year differences in demand or supply can produce substantial swings in price shifts in one year, followed by a return to the original price shift just one year later. These swings are much larger than any swings observed in other avoided cost inputs and are an outcome of the stepwise supply function used by ISO New England (and deployed in AESC). We chose this period because it is the period modeled under the future seasonal capacity market. The second exception is for reserve margins, which use a median of the 2028–2050 for the 2051–2068 time period for the same reasons as price shifts. The third exception is the final avoided cost streams for uncleared measures (e.g., uncleared capacity, uncleared capacity DRIPE). Because avoided costs in these categories vary by measure life, and because they are summed over the entire study period (rather than over the measure life as with all other avoided cost categories), we extrapolate the inputs used for these categories (e.g., capacity clearing prices, loads) but calculate avoided costs explicitly for each year through 2068.

[PDF p. 366 | printed p. 348] to the one recommended above. See Appendix A of AESC 2021 for more discussion on previous extrapolation techniques used in AESC studies.[^417]

**Figure 60. Example of linear regression over a short period**

[DIAGRAM DESCRIPTION: Figure 60. Example of linear regression over a short period]

Line chart with markers. The y-axis is labelled "Avoided Costs (2021 $/MWh)" and runs from $0.025 to $0.045 in steps of $0.005 (horizontal gridlines at each step); the x-axis shows years 2021 to 2035, labelled every second year (2021, 2023, 2025, … 2035). A black line with dot markers, annotated "Modeled avoided costs", shows one value per year: it starts near $0.032 in 2021, drops to its low of about $0.029 in 2022-2023, then rises to about $0.034 in 2026 and a local peak near $0.036 in 2027, dips to about $0.035 in 2028-2029, and climbs to about $0.040 by 2035 (roughly $0.0385-$0.039 in 2032-2034). A thicker red straight line, annotated "Linear Regression: Basis for extrapolation", is drawn over only the last six years (about 2030 to 2035) and runs from about $0.0358 to about $0.040, tracking the black series through its noise. The takeaway is that the regression line smooths the last six years of data and its growth rate is the basis for extrapolation. All values are read from the rendered chart and approximate. _Extractor note (not source text): the axis title says $/MWh but the values ($0.025 to $0.045) are of a size usually quoted in $/kWh; the source prints it as shown._

[→ See original PDF page 366 for visual rendering]

_Note: Reproduced from Figure 61 in AESC 2021._

### Levelization calculations

The AESC Study generally presents levelized costs throughout on a 15-year basis, although the study's appendices also provide levelized costs over two other periods. The three levelization periods are as follows:

- 10-year: 2024 to 2033
- 15-year: 2024 to 2038
- 30-year: 2024 to 2053

All levelized costs are calculated in AESC using a real discount rate of 1.74 percent.

To calculate levelized costs beyond the three periods documented above, readers of AESC will require (a) a real discount rate (1.74 percent or otherwise specified), (b) the number of years and timeframe over which costs are to be levelized (e.g., 10 years—2024 through 2033 inclusive), and (c) the specific

[^417]: Synapse Energy Economics. _Avoided Energy Supply Components in New England: 2021 Report (AESC 2021)_. May 15, 2021. Available at [https://www.synapse-energy.com/sites/default/files/AESC%202021_20-068.pdf](https://www.synapse-energy.com/sites/default/files/AESC%202021_20-068.pdf).

[PDF p. 367 | printed p. 349] avoided cost values for the relevant reporting region. Equation 12 describes the formula used to estimate a levelized cost within Excel.

**Equation 12. Excel formula used for calculating levelized costs**

$$\text{Levelized cost} = -\text{PMT}\big(\text{DiscountRate}, \text{NumberOfYears}, \text{NPV}(\text{DiscountRate}, \text{StreamOfCostsWithinPeriod})\big)$$

### Converting constant 2024 dollars to nominal dollars

Unless specifically noted, this report presents all dollar values in 2024 constant dollars. To convert constant 2024 dollars into nominal (current) dollars, apply the formula described in Equation 13. Inflator and deflator conversion factors for AESC 2024 are presented in _Appendix E: Common Financial Parameters_.

**Equation 13. Nominal-constant dollar conversion**

$$\text{Nominal Value} = \frac{\text{Constant Value (in 2024 \$)}}{\text{Annual Conversion Factor to 2024 \$}}$$

### Comparisons to previous AESC studies

A reader of the AESC 2024 Study may prepare comparisons of the AESC 2024 Study's 15-year levelized avoided costs with the 2021 AESC Study's avoided costs using the following steps:

- Identify the relevant reporting region and costing period
- Obtain the annual values of each avoided cost component from Appendix B in AESC 2024 and AESC 2021 (for the relevant reporting region and costing period)
- Convert the AESC 2021 values from 2021 dollars to 2024 dollars
- Calculate the 15-year levelized cost in 2024 dollars using the AESC 202 [sic] real discount rate (1.74 percent)

[PDF pp. 368-436 not transcribed: Appendices B-K (B detailed electric outputs, C detailed natural gas outputs, D detailed oil and other fuels outputs, E common financial parameters, F user interface, G marginal emission rates and non-embedded environmental cost detail, H DRIPE derivation, I matrix of reliability sources, J guide to calculating avoided costs for cleared and uncleared measures, K scaling factor for uncleared resources), in the other files of this folder (see README.md)]
