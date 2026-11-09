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
extraction_scope: "partial: PDF pp. 337-347 (printed pp. 319-329), Chapter 11 Value of Reliability (11.1-11.3); the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Chapter 11 of AESC 2024: how the value of lost load (VoLL, $61 per kWh) is derived from the ICE Calculator for New England, how it is applied to cleared and uncleared generation-reliability benefits through the Forward Capacity Market (Tables 147-150, 15-year levelized $0.38 and $4.82 per kW-year), the loss-of-energy-expectation risk by month, and an illustrative National Grid Massachusetts transmission and distribution (T&D) reliability calculation ($0.87 per MWh)."
why_here: "Source for the value-of-lost-load figure, the generation and T&D reliability avoided-cost components and the load-related-outage method that a New England heat pump rate design or marginal cost of service analysis may cite or contrast with its own distribution marginal costs."
---

_Extractor note (not source text): this file holds PDF pp. 337-347 (printed pp. 319-329) of AESC 2024, Chapter 11: Value of Reliability; the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. The text is transcribed verbatim; no source typos were corrected (apparent source errors are marked `[sic]` or `[source discrepancy: …]`)._

[PDF pp. 1-336 not transcribed: front matter and Chapters 1-10, in the other files of this folder (see README.md)]

[PDF p. 337 | printed p. 319]

# 11. Value of Reliability

The reduction in electric loads can improve reliability in several ways. First, it can increase installed generation reserves and thus reduce the probability of inadequate supply under variable loads and generation outages. Second, the reduction decreases the thermal wear and tear on transformers and conductors and thereby reduces failures. Third, it reduces the probability of overloads on T&D equipment to reduce faults. The last of these three categories overlaps with avoided T&D costs, since the ISO and utilities usually expand capacity to avoid system overloads. To the extent that lower loads result in less new T&D capacity, the reduced capacity will tend to offset the benefits of lower loads. We have not been able to determine a method for accounting for that overlap. Hence, we do not estimate any value for reduced acute overloads on the delivery system, even though there are undoubtedly some situations in which lower load would allow the system to survive some equipment failures, without deferring capacity additions.

In AESC 2024, we find a default average VoLL value of $61 per kWh. This value is about 26 percent less than the value derived in AESC 2021 ($82 per kWh in 2024 dollars). The change in the VoLL component is a result of specifying the value to the New England states. We apply this VoLL to the calculation of reliability benefits resulting from dynamics in New England's FCM to estimate cleared and uncleared benefits linked to improving generation reliability. In AESC 2024, we find 15-year levelized values of $0.38 per kW-year for cleared benefits and $4.82 per kW-year for uncleared benefits. These are 25 to 50 percent lower than the same values estimated in AESC 2021, after adjusting for inflation. The primary differences for these changes include a reduction in the assumed VoLL (as described above) and different input parameters related to the capacity market supply and demand curves.

As in AESC 2021, we also provide an estimated benefit for T&D reliability, based on data for National Grid Massachusetts. This section provides an example calculation of how different utilities could calculate their own T&D reliability benefit. This value would likely differ for each jurisdiction.

The following sections describe VoLL, the application of that value to generation reliability, and the potential for extension to distribution reliability.

## 11.1. Calculating value of lost load

In AESC 2018, we identified the most recent and detailed analysis of the VoLL to be that in the Lawrence Berkeley National Laboratory's (LBNL) 2015 study on _Updated Value of Service Reliability Estimated for Electric Utility Customers in the United States._ In AESC 2021, we used the analysis found in AESC 2018 and a 2018 study from Europe written by Cambridge Policy Associates to determine a VoLL value of $82 per kWh (in 2024 dollars). For AESC 2024, we review the recent literature on VoLL, looking for values more relevant to New England.

[PDF p. 338 | printed p. 320]

In our updated literature review, we identify an Interruption Cost Estimate (ICE) Calculator funded by the U.S. Department of Energy and developed by LBNL and Nexant, Inc.[^389] The meta-analysis and econometrics models used in the ICE Calculator are documented in the LBNL 2015 study that was used to inform the AESC 2018 and 2021 VoLL values. The ICE Calculator allows the user to specify the state(s), number of residential and non-residential customers, and two of the three index values used to measure reliability for a given area of interest. For AESC 2024, we chose to use the ICE Calculator to determine the VoLL because it allow us to enter specific inputs relevant to New England, thus allowing us to estimate a VoLL specific to New England.[^390]

The ICE Calculator provides a Cost of Unserved kWh value for the residential, small C&I, and large C&I customer classes, in the states selected by the users. Users must also specify a set of other inputs into the model. First, the ICE Calculator requires users to enter values for two measures of reliability: System Average Interruption Frequency Index (SAIFI) and System Average Interruption Duration Index (SAIDI).[^391] SAIFI is the number of times in a year the average customer experiences an interruption. SAIDI is the total number of minutes in a year the average customer experiences an interruption. These values vary over time. For the ICE Calculator, we average the SAIDI and SAIFI values provided by EIA from 2013 to 2021 (see Table 145).[^392] EIA provides SAIDI and SAIFI values including Major Event Days and excluding Major Event Days. A Major Event Day is any day that exceeds a daily SAIDI threshold, as defined by the Institute of Electrical and Electronics Engineers (IEEE) 1366 guide.[^393] The IEEE 1366 also defines the SAIDI, SAIFI, and CAIDI reliability metrics and is the industry standard. We include Major Event Days in our SAIDI and SAIFI averages. We determine the number of residential and non-residential customers in New England by averaging the number of customers in New England from 2018 to 2022 using EIA's form 861.[^394] We also make an adjustment to the following two assumptions made by the ICE Calculator to be consistent with our inputs: the total number of customers in each customer class and the weighted average annual usage per customer of each customer class using values from EIA's Form

[^389]: Sullivan, M., et al. July 2018. _Estimating Power System Interruption Costs: A Guidebook for Electric Utilities._ Lawrence Berkeley National Lab (LBNL). Available at [https://icecalculator.com/](https://icecalculator.com/).

[^390]: Note that our VoLL literature review also identified a number of other sources on the subject new to AESC. These sources generally described VoLL values for other regions or for long-duration power outages and were thus not included in the AESC 2024 calculation as they are less relevant than the ICE Calculator. These sources have been added to _Appendix I: Matrix of Reliability Sources_.

[^391]: We note that the ICE calculator accepts any two of the three reliability measures: SAIDI, SAIFI, and Customer Average Interruption Duration Index (CAIDI, or the average number of minutes an interruption lasts. It is calculated from dividing the SAIDI by the SAIFI). For the development of VoLL in AESC 2024, we have only populated the SAIDI and SAIFI parameters, and have ignored CAIDI.

[^392]: For historical SAIDI and SAIFI values, see U.S. Energy Information Administration, Form EIA-861, Annual Electric Power Industry Report. Available at [https://www.eia.gov/electricity/annual/html/epa_11_04.html](https://www.eia.gov/electricity/annual/html/epa_11_04.html) and U.S. Energy Information Administration, Form EIA-861, Annual Electric Power Industry Report. Available at [https://www.eia.gov/electricity/annual/html/epa_11_05.html](https://www.eia.gov/electricity/annual/html/epa_11_05.html).

[^393]: "IEEE Guide for Electric Power Distribution Reliability Indices," in _IEEE Std 1366-2022 (Revision of IEEE Std 1366-2012)_, vol., no., pp.1-44, 22 Nov. 2022, doi: 10.1109/IEEESTD.2022.9955492.

[^394]: U.S. Energy Information Administration, Form EIA-861. Available at [https://www.eia.gov/electricity/data/eia861/](https://www.eia.gov/electricity/data/eia861/).

[PDF p. 339 | printed p. 321]

861.[^395] Synapse performed these edits in the Interruption Costs Spreadsheet provided in the documentation of the ICE Calculator.[^396] Using share-of-sales data from EIA's Form 861 and the ICE Calculator outputs, we calculated a weighted average (see Table 146).

**Table 145. ICE calculator inputs**

| Input                               | Average from 2013 to 2021 in New England |
| ----------------------------------- | ---------------------------------------- |
| SAIDI (minutes per year)            | 515.0                                    |
| SAIFI (times per year)              | 1.489                                    |
| Number of residential customers     | 8,233,989                                |
| Number of non-residential customers | 1,293,086                                |

**Table 146. Calculation of VoLL**

|                           | VoLL estimated by ICE Calculator (2024 $/kWh) | Sale shares (%) [sic] |
| ------------------------- | --------------------------------------------- | --------------------- |
| Residential               | $2.86                                         | 40%                   |
| Small C&I                 | $103.42                                       | 45%                   |
| Large C&I                 | $91.77                                        | 14%                   |
| **Weighted Average VoLL** | **$61**                                       |                       |

_Extractor note (not source text): the third column header is printed "Sale shares" with the unit row "%"; the shares as printed sum to 99%._

## 11.2. Value of reliability: generation component

We observe that reducing loads can improve generation reliability in three ways:

- Some resources that do not clear the FCA will continue to operate as energy-only resources, adding to available reserves. While not obligated to do so, these resources are likely to operate at times of tight supply and high energy prices. They may also be available to assume the capacity obligations of resources that unexpectedly retire or otherwise become unavailable.
- Not all energy efficiency load reductions will clear in the capacity market or immediately affect the load forecast used to determine the amount of capacity acquired. Those load reductions will increase reserve margins.
- The operation of the ISO New England capacity market increases the amount of capacity acquired as the price falls. To the extent that energy efficiency programs reduce the capacity clearing price, reserve margins and reliability will increase.

The following sections describe how we calculate this component for cleared measures and uncleared measures.

[^395]: Ibid.

[^396]: Sullivan, M., et al. July 2018. _Estimating Power System Interruption Costs: A Guidebook for Electric Utilities._ Lawrence Berkeley National Lab (LBNL). Available at [https://icecalculator.com/documentation](https://icecalculator.com/documentation).

[PDF p. 340 | printed p. 322]

### Calculating cleared reliability

In order to calculate cleared reliability benefits, we first assemble several input parameters. First, ISO New England annually publishes MRI curves, which estimate the expected unserved energy avoided per MW of additional supply as the reserve margin rises. In AESC 2024, we examine the slope of the MRI curve at each auction's clearing price. The resulting value can be thought of as the estimated change in unserved energy per MW of reserve. Values calculated in FCA 15 through 18 utilize the MRI curve published for each auction. Values calculated in FCA 19 and after are similarly calculated based on the future-year MRI curves that set the demand for capacity in EnCompass. Table 147 displays the estimated change in MWh of reliability benefits per MW of reserve, and how it varies with the capacity market clearing price.

**Table 147. Change in MWh of reliability benefits per MW of reserve for Counterfactual #1 in Rest-of-Pool region**

| FCA    | Year | Clearing price (2024 $/kW-month) | ∆ MWh LOEE per MW (MWh / MW) |
| ------ | ---- | -------------------------------- | ---------------------------- |
| FCA 15 | 2024 | $2.66                            | 0.17                         |
| FCA 16 | 2025 | $2.53                            | 0.26                         |
| FCA 17 | 2026 | $2.48                            | 0.27                         |
| FCA 18 | 2027 | $2.48                            | 0.22                         |
| FCA 19 | 2028 | $1.42                            | 0.13                         |
| FCA 20 | 2029 | $1.38                            | 0.13                         |
| FCA 21 | 2030 | $1.42                            | 0.13                         |
| FCA 22 | 2031 | $1.42                            | 0.13                         |
| FCA 23 | 2032 | $4.25                            | 0.39                         |
| FCA 24 | 2033 | $4.25                            | 0.39                         |
| FCA 25 | 2034 | $5.66                            | 0.51                         |
| FCA 26 | 2035 | $7.08                            | 0.64                         |
| FCA 27 | 2036 | $5.66                            | 0.51                         |
| FCA 28 | 2037 | $7.08                            | 0.64                         |
| FCA 29 | 2038 | $7.08                            | 0.64                         |

_Note: Values for other counterfactuals and regions can be found in the AESC 2024 User Interface._

Due to the slopes of the supply and demand curves, bidding an additional MW into the FCA at $0 per kW-month price shifts the supply curve to the right. This shifts out some smaller amount of capacity that would otherwise have cleared, and it results in the amount of cleared supply increasing by only a fraction of the additional supply. That fraction is small when the clearing price is set at a shallow part of the supply curve, and it increases if the clearing price is set at a steeper part of the supply curve (see Table 148). We calculate this value by dividing the supply price shift by the difference between the supply price shift and the slope of the demand curve at the demand value implied by the clearing price.

[PDF p. 341 | printed p. 323]

**Table 148. Net increase in cleared supply for Counterfactual #1 in Rest-of-Pool region**

| FCA    | Year | Clearing price (2024 $/kW-month) | Net increase in cleared supply (%) |
| ------ | ---- | -------------------------------- | ---------------------------------- |
| FCA 15 | 2024 | $2.66                            | 47%                                |
| FCA 16 | 2025 | $2.53                            | 0%                                 |
| FCA 17 | 2026 | $2.48                            | 0%                                 |
| FCA 18 | 2027 | $2.48                            | 0%                                 |
| FCA 19 | 2028 | $1.42                            | 0%                                 |
| FCA 20 | 2029 | $1.38                            | 0%                                 |
| FCA 21 | 2030 | $1.42                            | 1%                                 |
| FCA 22 | 2031 | $1.42                            | 1%                                 |
| FCA 23 | 2032 | $4.25                            | 3%                                 |
| FCA 24 | 2033 | $4.25                            | 4%                                 |
| FCA 25 | 2034 | $5.66                            | 3%                                 |
| FCA 26 | 2035 | $7.08                            | 30%                                |
| FCA 27 | 2036 | $5.66                            | 4%                                 |
| FCA 28 | 2037 | $7.08                            | 29%                                |
| FCA 29 | 2038 | $7.08                            | 30%                                |

_Note: Values for other counterfactuals and regions can be found in the AESC 2024 User Interface._

The final component used to calculate cleared reliability benefits is a decay effect. Over time, customers will respond to lower prices by using somewhat more energy, including at the peak. In addition, lower capacity prices may result in the retirement of some generation resources and termination of some demand response resources, which will result in these resources being removed from the supply curve. Further, some new proposed resources that have not cleared for several auctions may be withdrawn (if, for example, contracts and approvals expire, raising the cost of offering the resource into future auctions). The decay schedule used for cleared reliability is the same as the one used for cleared capacity DRIPE (see Section 9.3: _Electric capacity DRIPE_, above).

Finally, we determine the cleared reliability benefit by calculating the product of (a) the change in MWh of reliability benefits per MW of reserve, (b) the net increase in cleared supply, (c) the decay effect, and (d) the VoLL, as calculated above.[^397] Table 149 describes the overall benefit for a measure installed in 2024. We note that these values are very small compared to the estimated avoided costs in many other categories.

[^397]: The AESC 2024 User Interface allows users to specify their own VoLL, if they so choose.

[PDF p. 342 | printed p. 324]

**Table 149. Estimated cleared reliability benefits for Counterfactual #1 in Rest-of-Pool region for measures installed in 2024, assuming a VoLL of $72 per kWh**

| FCA    | Year | ∆ MWh LOEE per MW (MWh / MW) | Net Increase in Cleared supply (%) | Decay Schedule (%) | Cleared reliability benefits (2024 $/kW-month) |
| ------ | ---- | ---------------------------- | ---------------------------------- | ------------------ | ---------------------------------------------- |
| FCA 15 | 2024 | 0.00                         | 47%                                | 100%               | $4.94                                          |
| FCA 16 | 2025 | 0.01                         | 40%                                | 83%                | $0.03                                          |
| FCA 17 | 2026 | 0.27                         | 0%                                 | 67%                | $0.00                                          |
| FCA 18 | 2027 | 0.22                         | 0%                                 | 50%                | $0.00                                          |
| FCA 19 | 2028 | 0.13                         | 0%                                 | 33%                | $0.04                                          |
| FCA 20 | 2029 | 0.13                         | 0%                                 | 17%                | $0.02                                          |
| FCA 21 | 2030 | 0.13                         | 1%                                 | 0%                 | $0.00                                          |
| FCA 22 | 2031 | 0.13                         | 1%                                 | 0%                 | $0.00                                          |
| FCA 23 | 2032 | 0.39                         | 3%                                 | 0%                 | $0.00                                          |
| FCA 24 | 2033 | 0.39                         | 4%                                 | 0%                 | $0.00                                          |
| FCA 25 | 2034 | 0.51                         | 3%                                 | 0%                 | $0.00                                          |
| FCA 26 | 2035 | 0.64                         | 30%                                | 0%                 | $0.00                                          |
| FCA 27 | 2036 | 0.51                         | 4%                                 | 0%                 | $0.00                                          |
| FCA 28 | 2037 | 0.64                         | 29%                                | 0%                 | $0.00                                          |
| FCA 29 | 2038 | 0.64                         | 30%                                | 0%                 | $0.00                                          |

_Note: Values for other counterfactuals, regions, and resource vintages can be found in the AESC 2024 User Interface. The "decay schedule" series is identical for measures installed in later years, except shifted by the relevant number of years._

_Extractor note (not source text): the Table 149 title prints a VoLL of $72 per kWh, while Section 11.1 derives $61 per kWh and Table 150 prints $61 per kWh [source discrepancy: $72 vs. $61 per kWh]. Table 149 also prints FCA 15 and FCA 16 values of ∆ MWh LOEE per MW (0.00 and 0.01) that differ from the 0.17 and 0.26 in Table 147; all values are kept as printed._

### Calculating uncleared reliability

As with cleared reliability, the calculation of uncleared reliability benefits requires the assembly of several input parameters.

The first is the estimated change in MWh of reliability benefits per MW of reserve. This parameter is the same as is used in the calculation of cleared reliability benefits (see Table 147, above).

Second, we gross up uncleared reliability benefits to account for the impact of the reserve margin. As with uncleared capacity and uncleared capacity DRIPE, because uncleared reliability benefits accrue outside of the FCM, they are effectively "counted" in the demand side of the capacity auction. See Section 5.2: _Uncleared capacity calculations_, above, for more information on this effect.

Third, we assume reliability has a phased impact on the load forecast. In contrast to uncleared capacity and uncleared capacity DRIPE, reliability value is realized before the impact of the energy efficiency measure is felt on ISO New England's load forecast and capacity market. As soon as load is reduced, the reserve margin increases (since the uncleared capacity does not initially reduce capacity procurement) and reliability is improved. Hedging of capacity supply, either short- or long-term, does not reduce the reliability effect, as it does capacity DRIPE. Thus, the reliability improvement starts at 100 percent in the first year and persists until the load reduction affects the capacity auction. Unlike other uncleared avoided cost categories, which operate through the effect on the econometric load forecast, the reliability improvement from any given measure does not rise with the number of years it has been in

[PDF p. 343 | printed p. 325]

place, but only by the increase in reserves for the year.[^398] Because of the switch to a prompt market in 2028, this means these effects are moved forward three years when counting benefits that accrue in 2028 and later years relative to the phase-out of reliability benefits in the market rules today, and to the same phase-out modeled in AESC 2021.

Fourth, uncleared reliability benefits will gradually decay over time, as the load reduction is reflected in the load forecast, reducing the amount of capacity that ISO New England acquires. Eventually, the load reduction would be fully captured in the load forecast, and the reliability benefit would be extinguished. The decay of the reliability benefit of uncleared resources starts later and is more gradual than the one used for cleared resources, because the market does not react to the resources and reduce procurement until it is picked up in the load forecast. Under the new market structure, we assume that because the load effects start three years early (compared to the effects in the current market structure), decay is also shifted forward by three years relative to the assumption in AESC 2021.

Finally, we calculate the uncleared reliability benefit by calculating the product of (a) the change in MWh of reliability benefits per MW of reserve, (b) one plus the reserve margin, (c) the load forecast effect, (d) the decay effect, and (e) the VoLL.[^399] Table 150 describes the overall benefit for a measure installed in 2024. Generally speaking, reliability effects of uncleared resources are greater than those of cleared resources. This is because the cleared resources immediately displace other resources, resulting in a smaller net gain in reliability. Uncleared resources increase reliability more than cleared resources do, for the same reason that uncleared resources have no immediate effect on capacity bills or prices—uncleared resources are invisible to the capacity market.

[^398]: In this regard, the reliability benefit of unclear [sic] capacity operates more like avoided energy or cleared capacity than like uncleared capacity or capacity DRIPE.

[^399]: Note that the AESC 2024 User Interface allows users to specify their own VoLL, if they so choose.

[PDF p. 344 | printed p. 326]

**Table 150. Estimated uncleared reliability benefits for Counterfactual #1 in Rest-of-Pool region for measures installed in 2024, assuming a VoLL of $61 per kWh**

| FCA    | Year | ∆ MWh LOEE per MW (MWh / MW) | Reserve Margin (%) | Load Forecast Effect (%) | Decay Schedule (%) | Uncleared reliability benefits (2024 $/kW-year) |
| ------ | ---- | ---------------------------- | ------------------ | ------------------------ | ------------------ | ----------------------------------------------- |
| FCA 15 | 2024 | 0.17                         | 14%                | 100%                     | 100%               | $11.85                                          |
| FCA 16 | 2025 | 0.26                         | 13%                | 100%                     | 100%               | $18.04                                          |
| FCA 17 | 2026 | 0.27                         | 11%                | 100%                     | 100%               | $18.03                                          |
| FCA 18 | 2027 | 0.22                         | 13%                | 100%                     | 100%               | $15.37                                          |
| FCA 19 | 2028 | 0.13                         | 5%                 | 100%                     | 100%               | $2.24                                           |
| FCA 20 | 2029 | 0.13                         | 5%                 | 70%                      | 100%               | $0.63                                           |
| FCA 21 | 2030 | 0.13                         | 4%                 | 50%                      | 95%                | $0.00                                           |
| FCA 22 | 2031 | 0.13                         | 3%                 | 30%                      | 87%                | $0.00                                           |
| FCA 23 | 2032 | 0.39                         | 1%                 | 10%                      | 75%                | $0.00                                           |
| FCA 24 | 2033 | 0.39                         | 1%                 | 0%                       | 60%                | $0.00                                           |
| FCA 25 | 2034 | 0.51                         | 0%                 | 0%                       | 43%                | $0.00                                           |
| FCA 26 | 2035 | 0.64                         | -2%                | 0%                       | 27%                | $0.00                                           |
| FCA 27 | 2036 | 0.51                         | -1%                | 0%                       | 0%                 | $0.00                                           |
| FCA 28 | 2037 | 0.64                         | -3%                | 0%                       | 0%                 | $0.00                                           |
| FCA 29 | 2038 | 0.64                         | -3%                | 0%                       | 0%                 | $0.00                                           |

_Note: Values for other counterfactuals, regions, and resource vintages can be found in the AESC 2024 User Interface. The "decay schedule" series is identical for measures installed in later years, except shifted by the relevant number of years._

#### Important caveats for applying reliability values

Unlike other uncleared avoided cost categories (e.g., uncleared capacity, uncleared capacity DRIPE) uncleared reliability avoided costs are summed over the time period that a measure is active. This is similar to the approach used to sum avoided costs for most categories.

Unlike other uncleared avoided cost categories, users should not apply a scaling factor (like the kind described in _Appendix K: Scaling Factor for Uncleared Resources_). The scaling factor reflects a demand measure's effect on the load forecast, which is a function of the number of daily peaks (the inputs to the ISO New England demand forecast regression) that the measures reduces. Because changes in reliability do not impact the load forecast, the scaling factor should not be used to adjust uncleared reliability benefits.

### Other considerations: reliability impact on non-summer peak hours

Measures increase generation reliability to the extent that they reduce load at hours that would contribute to ISO New England's estimate of loss-of-energy expectation (LOEE) in high-risk hours throughout the year, under the RCA framework. An efficiency measure that clears as 1 kW of supply in the capacity auction may provide more or less load reduction during the highest LOEE hours. These hours may not necessarily coincide with ISO New England's definition of on-peak hours for on-peak resources (weekday hours ending 14–17 from June through August and hours ending 18 and 19 in December and January) or seasonal resources (hours in June through August, December, and January with load greater than 90 percent of the seasonal 50/50 peak), especially as solar generation reduces LOEE in sunny summer hours.

[PDF p. 345 | printed p. 327]

In setting the demand curve for each capacity auction (both the FCAs and the annual reconfiguration auctions), ISO New England derives various measures of generation risk, including loss-of-load expectation (LOLE), which is a measure of the fraction of time intervals for which supply might be inadequate, and the LOEE, the amount of energy that would not be served on average. ISO New England provided its risk results from the second annual reconfiguration auction for the 2022–2023 capacity compliance period (the period covered by FCA 13), as shown in Table 151. All months other than the summer had zero risk in this analysis.

Table 151 suggests that only the reductions in the highest-net-load hours of the summer are likely to have any effect on reliability, at least in the near term.[^400] That may change as electrification increases winter loads and renewable and storage deployment shifts the hours at greatest risk of energy shortage.

**Table 151. Monthly distribution of risk prices for capacity commitment period 2022–23, annual reconfiguration auction #2**

|                         | June    | July    | August  | Annual  |
| ----------------------- | ------- | ------- | ------- | ------- |
| LOLE (days)             | 0.00066 | 0.02059 | 0.07868 | 0.09994 |
| LOLE (hours)            | 0.00194 | 0.11075 | 0.43035 | 0.54303 |
| LOEE (MWh)              | 0.953   | 119.184 | 524.418 | 645.153 |
| **Percentage by month** |         |         |         |         |
| LOLE (days)             | 0.7%    | 20.6%   | 78.7%   |         |
| LOLE (hours)            | 0.4%    | 20.4%   | 79.2%   |         |
| LOEE (MWh)              | 0.1%    | 18.5%   | 81.3%   |         |

## 11.3. Value of reliability: T&D component

As in AESC 2021, we provide an example methodology of how utilities might calculate a value of reliability associated with T&D.

### Theory

Reducing loads can also reduce overloads and violations of T&D planning standards, by:

- Leaving additional capacity across this system to accommodate flows from facilities or equipment that are forced out of service by non-load-related problems,
- Reducing overloads under extreme weather conditions, and

[^400]: See [https://www.synapse-energy.com/sites/default/files/AESC_Supplemental_Study_Part_I_Winter_Peak.pdf](https://www.synapse-energy.com/sites/default/files/AESC_Supplemental_Study_Part_I_Winter_Peak.pdf) for more discussion on this topic.

[PDF p. 346 | printed p. 328]

- Reducing wear on lines and transformers from the cumulative effects of many hours with high loads.[^401]

The aging of transformers (both at substations and along primary feeders) primarily results from the breakdown of insulation due to heating. That deterioration can be driven by the following:

1. Short periods of very high load levels: transformers typically can be operated at over 150 percent of their rated capacity for an hour or two, if they start cool.
2. Long periods (such as many hours or days) of lower but still high loads, which heat up the insulation.
3. Even more so, very high load levels following a long period of high loads.

Similar considerations also apply to underground T&D lines that are insulated in the ground. These underground lines and their insulation also heat up due to long periods of high loads.

Some overhead lines are subject to a different set of load-related failure modes. Generally, the surrounding air cools the lines and reduces the effect of heat buildup at moderate load levels. However, when lines are loaded near their thermal ratings, this can lead to deterioration of insulation (if they are insulated). High loads can also stretch and weaken the metal conductor and reduce line clearance from the ground or other objects below the line. Stretched lines are more vulnerable to breakage from other stresses, such as wind load.[^402]

We examined utility reports on distribution outages to attempt to estimate the amount of load lost due to potentially load-related equipment failure, as opposed to events such as tree, vehicle, or animal contact.

The value of increased T&D reliability is complementary, not duplicative, of the avoided T&D costs. Reducing loads (or avoiding rising loads) will tend to increase reliability even when the T&D system does not change. By contrast, the reliability for a T&D element (e.g., distribution substation, feeder, line transformer, secondary lines) is not likely to improve for T&D equipment that is avoided by a load reduction.[^403]

### Example calculation

AESC 2024 repurposes the review conducted in AESC 2021. The text in the following section has not been updated since the AESC 2021 report.

[^401]: Other causes (tree, weather, animal contact, etc.) of outages are not load-related and are thus outside the scope of this analysis.

[^402]: Many overhead lines are self-supporting and thus vulnerable to stretching and physical stress. Line supported by much stronger steel messenger wire are less sensitive to the mechanical stresses.

[^403]: Logically, similar considerations would apply to the reliability of natural gas supply by LDCs, but that subject is beyond the scope of AESC 2021.

[PDF p. 347 | printed p. 329]

In the AESC 2021 analysis, we reviewed the 2019 outages in National Grid Massachusetts "Unplanned Significant Outage Report" in DPU 20-SQ-11, which included about 4,700,000 customer-hours of outage. Those hours were about 65 percent due to trees, with failed equipment accounting for over 14 percent (over 682,000 customer-hours), and other categories (lightning, animals, and other miscellaneous) totaling about 20 percent. The outages that National Grid listed as due to failed equipment included some that were clearly not due to electrical failure, such as broken poles, lightning arresters, and brackets; many categories that might conceivably be related to heavy loading (e.g., "tired fuses," fires, and failed switches, breakers, and reclosers); and a few likely to be load-related (failed transformers, underground cables, and splices). That last group of outages amounted to about 176,000 customer-hours, about 4 percent of the total outage hours. We note that some portion of these outages may be associated with deferred maintenance or defective parts, and they may not ultimately be avoidable through load reductions.

Exhibit NG-HSG-3A to National Grid's filing in DPU 18-150 provides customer number and sales by class. The average non-streetlighting customer uses about 15 MWh annually, but many of the largest customers are served at primary or even transmission voltage. The customers served at secondary voltage would be exposed to more outages than customers served at primary voltage, and the transmission-level customers would not be affected by any of these distribution outages. Counting only 50 percent of the sales at primary and none of the sales at transmission, the average usage falls to 14 MWh per customer annually, or about 1.6 kWh per customer-hour.

Multiplying together the number of customer-hours related to load-related outages (about 176,000), 1.6 kWh per customer-hour and $61 per kWh VoLL yields a total annual cost of the potentially load-related outages of about $17 million annually. Dividing by total distribution sales of about 19.8 TWh, this resulting per-MWh cost is $0.87 per MWh. The load-related failures in 2019 were presumably due to accumulated damage over decades of service, but the energy delivered in 2019 will contribute to failures that occur in 2019 as well as future years. Hence, it appears reasonable to estimate the load-related costs of lost distribution reliability in future years to be similar to the cost derived from 2019 data. The distribution reliability cost may vary by time period, with potentially higher costs in peak hours than off-peak hours and higher costs in summer months than the rest of the year.[^404]

The methodology of this analysis could be applied for other investor-owned utilities that file similar data, and for additional years. Similar data may be available from electric utilities in other states. We recommend that utilities or program administrators examine data local to their own jurisdictions and evaluate their own estimates of T&D reliability benefits.

[^404]: High winter loads may also contribute to the aging of transformers, but lower air temperatures reduce overheating and damage. For example, National Grid (MA) aims to change out residential transformers when they reach half-hour peak loads of 160 percent of rated capacity in the summer or 200 percent in the winter (see DPU 16-SG-11 Filing Attachment 2).

[PDF pp. 348-436 not transcribed: Chapter 12 Sensitivity Analysis, Appendices A-K and the report's remaining pages, in the other files of this folder (see README.md)]
