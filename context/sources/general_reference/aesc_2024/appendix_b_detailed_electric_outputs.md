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
extraction_scope: "partial: PDF pp. 368-376 (printed pp. 350-358), Appendix B: Detailed Electric Outputs; the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Appendix B: guide to the detailed avoided electric cost tables (energy, REC, GHG, DRIPE, capacity, reliability, PTF), the four energy costing-period definitions with hours, cleared versus uncleared capacity, and how to convert wholesale avoided costs to retail (wholesale risk premium of 8 percent, marginal T&D loss factors of 9 percent for energy and 16 percent for peak demand, which categories get which factor, default parameters). The year-by-year tables themselves are in the AESC 2024 User Interface workbook, not in this PDF text."
why_here: "Source for the AESC wholesale-to-retail conversion (losses and risk premium), the summer/winter on-peak/off-peak hour definitions and marginal loss factors, useful when we compare Cambium or utility marginal costs and supply rates against New England avoided-cost values."
---

_Extractor note (not source text): this file holds PDF pp. 368-376 (printed pp. 350-358) of AESC 2024, Appendix B: Detailed Electric Outputs; the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. The text is transcribed verbatim, including the source's own slips, which are flagged inline with `[sic]` or `[source discrepancy: …]`; the only changes are stray spacing around punctuation (for example "values ,as" printed on PDF p. 370 is given as "values, as"). The pages in this file contain no Table 156 and no other amended table: the tables on them are Tables 163 and 164 (Appendix B has no numbered year-by-year tables in the PDF text)._

[PDF pp. 1-367 not transcribed: front matter, Chapters 1-12 and Appendix A (usage instructions), in the other files of this folder (see README.md)]

[PDF p. 368 | printed p. 350]

# Appendix B: Detailed Electric Outputs

AESC 2024 provides detailed avoided electricity cost projections, both energy and capacity, for each New England state. This appendix provides an overview of and instructions on how to apply those avoided costs. All values can be found in the _AESC 2024 User Interface_ (see _Appendix F: User Interface_ for more information).

### Structure of Appendix B tables

For each state, Appendix B presents tables with the following avoided costs:

1. Avoided unit cost of electric energy
2. Avoided REC costs to load
3. Avoided non-embedded GHG costs
4. Energy DRIPE for intrastate and rest-of-pool for 2024 installations
5. Electric Cross-DRIPE
6. Avoided unit cost of electric capacity by demand reduction bidding strategy
7. Capacity DRIPE for intrastate and rest-of-pool for 2024 installations
8. Avoided reliability costs
9. Avoided cost of pooled transmission facilities (PTF)

Illustrative levelized values are provided for each avoided cost.

Appendix B is organized into wholesale values, then retail values. Users typically do not need to use or modify the wholesale values directly, but users should apply values in accordance with state regulations.

Within these two categories, avoided costs are further arranged into avoided energy-based costs (presented in $ per kWh) and avoided capacity-based costs (presented in $ per kW-year).

There are two important considerations to applying Appendix B in state benefit-cost (BC) models.

- First, some of the values in the $-per-kWh categories, such as energy DRIPE, change depending on the measure vintage selected in the _AESC 2024 User Interface_.
- Second, some of the values in the $-per-kW categories, such as uncleared capacity DRIPE, change depending on both the measure vintage and the measure lifetime selected in the _AESC 2024 User Interface_. The entire set of avoided costs shown for all measure lives is contained in the "Appendix J" tabs in the _AESC 2024 User Interface_.

To address this first consideration, users should modify the measure vintage to reflect each of the years being analyzed in their benefit-cost analyses (e.g., 2025, 2026, and 2027), and generate a separate Appendix B for each vintage. This will produce separate, more specific series of avoided costs for all $- [PDF p. 369 | printed p. 351] per-kWh values and for the avoided cost of pooled transmission facilities (PTF) (note that not all of these values will vary by vintage, but generating separate Appendix B tables for each vintage will make it easier to implement these tables in most states' BC models. In addition, users should also generate a separate set of Appendix J tables for each measure vintage. These tables should be used to inform avoided costs related to cleared and uncleared capacity, capacity DRIPE, and value of reliability. In other words, users should not simply use the columns for capacity, capacity DRIPE, and value of reliability as they are shown in Appendix B, as these show avoided costs for only the measure life selection specified on the "UserInterface" page.

### Energy-based avoided costs, $ per kWh

Avoided electric energy costs are presented by year in four costing periods: on-peak winter, off-peak winter, on-peak summer, off-peak summer. For the weather year 2002 used in AESC 2024, these costing periods are defined as follows:[^418]

- Summer on-peak: The 16-hour block from 7 a.m. till 11 p.m., Monday–Friday (except ISO holidays), in the months of June–September (1,344 Hours, 15.3 percent of 8,760)[^419]
- Summer off-peak: All other hours between 11 p.m. and 7 a.m., Monday–Friday, weekends, and ISO holidays in the months of June–September (1,582 Hours, 18.1 percent of 8,760)
- Winter on-peak: The 16-hour block from 7 a.m. till 11 p.m., Monday–Friday (except ISO holidays), in the eight months of January–May and October–December (2,736 Hours, 31.2 percent of 8,760)
- Winter off-peak: All other hours between 11 p.m. and 7 a.m., Monday–Friday, all day on weekends, and ISO holidays–in the months of January–May and October–December (3,096 Hours, 35.3 percent of 8,760)

The annual avoided electricity cost for a given year, or set of years, is equal to the hour-weighted average of avoided costs for each of the four costing periods of that year (see Equation 14).

**Equation 14. Calculation of annual avoided electricity cost**

$$\text{Annual avoided electricity cost} = (15.3\% \times \text{Summer OnPeak}) + (18.1\% \times \text{Summer OffPeak}) + (31.2\% \times \text{Winter OnPeak}) + (35.4\% \times \text{Winter OffPeak})$$

_Extractor note (not source text): [source discrepancy: Equation 14 weights Winter OffPeak at 35.4%, but the bullet above prints 35.3 percent of 8,760 for winter off-peak (3,096 / 8,760 = 35.3%). The four printed hour counts sum to 1,344 + 1,582 + 2,736 + 3,096 = 8,758, not 8,760, and the four percentages in the bullets sum to 99.9%; with 35.4% the equation weights sum to 100.0%.]_

The specific wholesale avoided energy costs included in Appendix B are explained below.

[^418]: ISO New England. Last accessed September 25, 2023. "Glossary and Acronyms." _Iso-ne.com_. Available at [https://www.iso-ne.com/participate/support/glossary-acronyms/](https://www.iso-ne.com/participate/support/glossary-acronyms/).

[^419]: ISO New England holidays are New Year's Day, Memorial Day, July 4th, Labor Day, Thanksgiving Day, and Christmas.

[PDF p. 370 | printed p. 352]

- _Wholesale avoided costs of electricity energy_. Annual wholesale electric energy prices are outputted from the EnCompass simulation runs.[^420]
- _Wholesale REC costs to load_. Annual avoided REC costs are specific to each state.
- _Wholesale non-embedded GHG costs_. Annual estimates of non-embedded CO₂ values are provided for each of the four energy costing periods.
- _Wholesale energy DRIPE_. Separate projections are provided for wholesale intrastate and rest-of-pool energy DRIPE.[^421] Users should apply energy DRIPE values in accordance with relevant state regulations governing treatment of energy DRIPE. For example, Massachusetts only considers intrastate DRIPE benefits, whereas Rhode Island considers both intrastate and Rest-of-Pool DRIPE benefits.
- _Wholesale cross-DRIPE_. Annual wholesale electric cross-DRIPE values include both electric-gas cross-DRIPE and electric-gas-electric cross-DRIPE, which represents the benefits from a reduction in the quantity of electricity that reduces gas consumption and that subsequently reduces electric prices. Users should treat the avoided costs for electric cross-DRIPE similarly to energy DRIPE.

### Capacity-based avoided costs, $ per kW-year

Most capacity-based avoided cost components—including wholesale avoided unit cost of electric capacity, wholesale capacity DRIPE, and reliability—are separated into cleared, uncleared, and weighted average values. All of these values except the Avoided cost for PTF should be referenced on the "Appendix J" tabs in the _AESC 2024 User Interface_. These values, as they are shown on the Appendix B tab, show only the avoided costs for a single selected measure lifetime.

_Avoided cost for PTF_ is based on costs allocated to LSEs from ISO New England. This is the only capacity-based avoided cost that is not separated into cleared, uncleared, and weighted average values, because it is not part of the FCM. Utilities that use avoided PTF costs should include only local transmission investments (those not eligible for PTF treatment) in their own avoided transmission cost analyses.

The _cleared_ capacity columns provide estimates for FCA capacity prices reported on a calendar year basis. ISO New England generally reports capacity prices based on power-years (June 1 to May 31).

The _uncleared_ capacity columns provide estimates for capacity based on uncleared capacity or unbid capacity avoided through energy efficiency measures. The values are multiplied by the capacity price load effect and reserve margin percentages. Because under the current market, FCA auctions are set three years in advance of the actual delivery year, avoided capacity not bid into an FCA will not impact ISO New England's determination of forecasted peak until five years after the current year.

[^420]: The avoided energy costs are computed for the aggregate load shape in each zone by costing period as described in more detail in Section 4.3: _New England system demand and energy components_.

[^421]: DRIPE vintage years are available for 2024 through 2028 within the _AESC 2024 User Interface_.

[PDF p. 371 | printed p. 353]

_Wholesale capacity DRIPE_ projections are provided for intrastate and Rest-of-Pool energy DRIPE for installation year 2024. Users should apply capacity DRIPE values in accordance with relevant state regulations governing treatment of capacity DRIPE.

_Wholesale reliability_ projections are provided for installation year 2024. Both cleared and uncleared values are provided.

Three separate sets of values are provided for capacity, capacity DRIPE, and reliability for each of the three capacity costing frameworks: the current capacity market, which extends through 2027, the future summer capacity costing period, which applies to measures with summer peaking values that provide savings in 2028 and later years, and the future winter capacity costing period, which applies to measures with winter peaking values that provide savings in 2028 and later years. Future summer and winter values are provided only in situations where we have modeled a clearing price (or need for seasonal capacity) in those years.

Finally, in the _AESC 2024 User Interface_, users may specify a percentage of measures that are cleared in the FCM. This percentage is then used to calculate a weighted average avoided cost for cleared and uncleared capacity, cleared and uncleared capacity DRIPE, and cleared and uncleared reliability. The weighted average is based on a simplified bidding strategy consisting of $x$ percent of demand reductions from measures in each year bid (cleared) into the FCA for that year and the remaining $1-x$ percent not bid (uncleared) into any FCA. The default value for $x$ is 50 percent. This percentage, as it appears in the _AESC 2024 User Interface_, is not intended to be a primary input for producing usable avoided costs. Instead, its purpose is to provide demonstrative values within the "Appendix J" tabs of the _AESC 2024 User Interface_. Users should plan to develop their own values for x and apply these in their BC models.

### How to convert wholesale avoided costs to retail avoided costs

AESC estimates avoided electric costs at the wholesale level, meaning reductions at power plants or energy markets. The _AESC 2024 User Interface_ allow [sic] users to convert the wholesale values to retail values. Retail avoided costs represent reductions at the customer meter or end-use level, and they are meant to approximate the price customers see on utility bills.

Depending on the avoided cost, two adjustment factors are applied to convert from wholesale to retail values: (1) a factor for transmission and distribution losses, and (2) a wholesale risk premium. Both factors are described in detail below. These adjustments gross up wholesale values, leading to retail values that are greater than wholesale values.

In general, the formula for converting from wholesale to retail is shown in Equation 15.

**Equation 15. Converting from wholesale to retail avoided costs**

$$\text{Avoided retail cost} = (\text{avoided wholesale cost}) \times (1 + \text{losses}) \times (1 + \text{wholesale risk premium})$$

[PDF p. 372 | printed p. 354]

### Wholesale risk premium

The full retail price of electricity is generally greater than the sum of the wholesale market prices for energy, capacity, and ancillary service. This is because retail suppliers incur various market risks when they set contract prices in advance of supply delivery. In AESC, this premium over wholesale prices is called the _wholesale risk premium_, and the default assumption is that retail prices are 8 percent greater than wholesale prices. We note that Study Group members in Vermont utilize values of 4 percent for summer months and 0 percent for winter months; the _AESC 2024 User Interface_ allows users to enter a separate wholesale risk premium value for each season, or set these values to be the same.[^422]

#### Types of risk

The wholesale risk premium accounts for multiple risks. First, there is the retail supplier's cost to mitigate cost risks. Retail suppliers mitigate some risk by hedging their costs in advance, but there is still uncertainty in the final price borne by the supplier. This includes cost risk from hourly energy balancing, ancillary services, and uplift.

The larger component of the risk is the difference between projected and actual energy requirements under the contract, driven by unpredictable variations in weather, economic activity, and/or customer migration. For example, during hot summers and cold winters, LSEs may need to procure additional energy at shortage prices, while in mild weather they may have excess supply under contract that they need to "dump" into the wholesale market at a loss. The same pattern holds in economic boom and bust cycles.

In addition, the suppliers for utility standard-service offers run risks related to customer migration. Customers may migrate from the utility's standard offer service to competitive supply, presumably at times of low market prices, leaving the supplier to sell surplus into a weak market at a loss. Alternatively, customers may switch from competitive supply to the utility's standard offer service at times of high market prices, forcing the supplier to purchase additional power in a high-cost market.

#### Estimating the wholesale risk premium

Estimates of the appropriate premium range from less than 5 percent to around 10 percent, based on analyses of confidential supplier bids—primarily in Massachusetts, Connecticut, and Maryland—to which the Synapse Team or sponsors have been privy.[^423] Short-term procurements (for six months or a

[^422]: In general, these seasonal wholesale risk premium values are applied to the relevant season. For example, the summer wholesale risk premium is applied to summer on-peak energy values, while the winter wholesale risk premium is applied to winter on-peak energy values. There are two exceptions to this. First, the two seasonal wholesale risk premium values are averaged and applied to cross-DRIPE values, since these avoided costs represent avoided costs that span the entire year. Second, summer wholesale risk premium values are applied to capacity market values that get a wholesale risk premium (e.g., uncleared capacity, uncleared capacity DRIPE, and uncleared reliability) for the near-term years when the current capacity market structure applies. In future years, where we model a season capacity market, each season receives the associated seasonal wholesale risk premium value.

[^423]: Note that these bids are confidential and cannot be made public.

[PDF p. 373 | printed p. 355] year into the future) may have smaller risk adders than longer-term procurements (upwards to about three years, which appears to be the limit of suppliers' willingness to offer fixed prices). Utilities that require suppliers to maintain higher credit levels tend to see the resulting costs incorporated into the adders in supplier bids.[^424]

AESC 2024 applies the same wholesale risk premium to avoided wholesale energy prices and to avoided wholesale capacity prices.[^425]

The risk premium is a separate input to the avoided-cost spreadsheet. Therefore, program administrators will be able to input whatever level of risk premium they feel best reflects their specific experience, circumstances, economic and financial conditions, or regulatory direction.

Members of the Study Group have inquired if a similar wholesale risk premium could be applied for natural gas efficiency programs. Natural gas marketers also undertake contracts of varying durations for future delivery and account for risks in their retail pricing. The current scope of AESC 2024 does not include the development of a wholesale risk premium for natural gas, but such work could be included in future AESC studies or updates to this study.

### Transmission and distribution losses

There is a loss of electricity between a generating unit and ISO New England's delivery points. Therefore, a kilowatt load reduction at the ISO New England's delivery points reduces the quantity of electricity that a generator has to produce by one kilowatt plus the additional quantity that would have been required to compensate for losses. These losses occur on both the transmission and distribution systems and apply to both energy and capacity avoided costs.[^426]

When converting from wholesale to retail values, program administrators can use the default T&D loss value in AESC of 8 percent, or program administrators can use their own custom T&D loss factors.

_Extractor note (not source text): [source discrepancy: this sentence gives a default T&D loss of 8 percent, while the next section ("AESC T&D losses") and the "Guide to applying the avoided costs" section give AESC 2024's marginal loss factors as 9 percent for energy and 16 percent for peak demand.]_

[^424]: The default value for Vermont is set in accordance with guidance from the Vermont PUC, which also specifies a default value for municipal utilities. These utilities typically either procure a basket of generation resources or contract for bundled service from suppliers.

[^425]: Capacity costs present a different risk profile than energy costs. With the FCM, suppliers have a good estimate of the capacity price three years in advance and of the capacity requirement for customers about one year in advance. Reconfiguration auctions may affect the capacity charges, but the change in average costs is likely to be small. On the other hand, since suppliers generally charge a dollars-per-MWh rate, and energy sales are subject to variation, the supplier retains some risk of under-recovery of capacity costs. There is no way to determine the extent to which an observed risk premium in bundled prices reflects adders on energy, capacity, ancillary services, RPSs, and other factors. Given the uncertainty and variability in the overall risk premium, we do not believe that differentiating between energy and capacity premiums is warranted. We thus apply the retail premium uniformly to both energy and capacity values.

[^426]: The forecast of capacity costs from the FCM do not reflect these losses; therefore, forecasted capacity costs should be adjusted to account for them.

[PDF p. 374 | printed p. 356]

#### AESC T&D losses

AESC converts avoided costs from wholesale to retail values assuming marginal losses of 9 percent for energy (i.e., all avoided cost categories that are described in terms of $ per kWh) and 16 percent for peak demand (i.e., all avoided cost categories that are described in terms of $ per kW-year). Table 163 displays the recommended loss factors, along with the average factors from which they are derived. We note that previous editions of AESC (such as AESC 2018) have typically recommended a loss factor of 8 percent be applied to all avoided cost categories.[^427] However, this loss factor is average (rather than marginal) and focused on-peak hours (rather than all hours). As a result, AESC 2024 utilizes the same loss factors as AESC 2021. See Section 4.3 _New England system demand and energy components_ for more discussion on deriving marginal loss factors.

**Table 163. Loss factors recommended for use in AESC 2024**

|                                     | Energy | Peak Demand |
| ----------------------------------- | ------ | ----------- |
| Average                             | 6% (a) | 8% (c)      |
| Marginal _Recommended in AESC 2021_ | 9% (b) | 16% (d)     |

_Sources: (a) [https://www.iso-ne.com/static-assets/documents/2019/11/p2_transp_elect_fx_update.pdf](https://www.iso-ne.com/static-assets/documents/2019/11/p2_transp_elect_fx_update.pdf), slide 25; (b) 1.5 x 6%, per 2011 RAP paper; (c) ISO New England Market Rules, Section III.13.1.4.1.1.6.(a); (d) 2 x 8%, per 2011 RAP paper._

#### Custom T&D losses

If a program administrator chooses to apply custom T&D loss values, it needs to consider three types of losses: distribution losses, transmission non-PTF losses, and transmission PTF losses. Below, we estimate PTF losses and describe the need for program administrators to derive their own non-PTF costs. These two components could then be added to custom distribution losses values.

##### PTF losses

ISO New England does not appear to publish estimates of the losses on the ISO-administered transmission system at system peak. ISO New England does release hourly values for system load and non-PTF demand that enable to us [sic] to estimate PTF losses.[^428] On average, system PTF losses between 2010 and 2020 are 1.6 percent. This is the same number described in AESC 2021 and AESC 2018.

[^427]: Note that this 8 percent value includes both transmission losses (2.5 percent) and distribution losses (5.5 percent).
    ISO New England. October 10, 2019. _Transmission Planning Technical Guide_. Available at [https://www.iso-ne.com/static-assets/documents/2017/03/transmission_planning_techincal_guide_rev6.pdf](https://www.iso-ne.com/static-assets/documents/2017/03/transmission_planning_techincal_guide_rev6.pdf).

[^428]: ISO New England defines system load as the sum of generation and net interchange, minus pumping load, and non-PTF demand. ISO New England uses the term "non-PTF demand" for the load delivered into the networks of distribution utilities. Losses on the PTF system are thus the difference between the system load and non-PTF demand.

[PDF p. 375 | printed p. 357]

PTF losses probably vary among zones, because losses in any zone depend both on loads in that zone and flows into and out of that zone to the rest of the region. However, marginal losses by zone could not be identified using the available data provided by ISO New England in December 2020, and it would be difficult to estimate from historical data anyway. Therefore, AESC 2024 re-uses the same approach for average losses used in AESC 2021.

##### Non-PTF losses

AESC does not recommend a calculation for non-PTF losses at this time. Utilities who wish to develop a custom T&D factor should examine their own data and formulate their own non-PTF losses as appropriate. These non-PTF losses include losses over the non-PTF transmission substations and lines to distribution substations.

### Applying wholesale to retail factors

Table 164 summarizes which retail factors are applied when converting wholesale avoided cost to retail avoided costs. Losses apply to all avoided costs.[^429] Losses are applied to avoided capacity costs to be consistent with how generation capacity is procured or avoided.

The wholesale risk premium is applied to energy values except non-embedded values and to uncleared capacity values. The wholesale risk premium does not apply to non-embedded values because, by definition, these costs are not embedded in electricity prices; therefore, retail suppliers do not include these costs in supply contracts. The wholesale risk premium does not apply to cleared capacity values because resources cleared in the FCM receive FCM prices.

Avoided PTF costs represent avoided infrastructure investments, which would not be impacted by line losses or wholesale market risks.

**Table 164. Wholesale to retail factors by avoided cost category**

| Avoided cost categories                         | Losses | Wholesale Risk Premium |
| ----------------------------------------------- | :----: | :--------------------: |
| Electric energy, energy DRIPE, cross-DRIPE      |   ✓    |           ✓            |
| Non-embedded GHG, non-embedded NOx              |   ✓    |                        |
| Cleared capacity, capacity DRIPE, reliability   |   ✓    |                        |
| Uncleared capacity, capacity DRIPE, reliability |   ✓    |           ✓            |
| PTF losses                                      |   ✓    |                        |

_Extractor note (not source text): [source discrepancy: the paragraph above Table 164 says avoided PTF costs "would not be impacted by line losses or wholesale market risks", yet the last row of the table (labelled "PTF losses") shows a check mark under Losses, and footnote 429 says avoided PTF costs "must be increased by a loss factor" to be applied to retail kW savings.]_

[^429]: This includes avoided PTF costs. Avoided PTF costs are calculated on the basis of dollars per _generating_ kW. In order to be applied to retail kW savings, they must be increased by a loss factor.

[PDF p. 376 | printed p. 358]

### Guide to applying the avoided costs

AESC 2024 allows users to specify certain inputs as well as to choose which of the avoided cost components to include in their analyses. The retail avoided costs shown in the "Appendix B" tab of the _AESC 2024 User Interface_ are calculated using the following default values:

1. Wholesale risk premium: 8 percent
2. Losses: 9 percent for dollar-per-kWh values and 16 percent for dollar-per-kW values[^430]
3. Real discount rate: 0.81 percent

_Extractor note (not source text): [source discrepancy: the default real discount rate printed here is 0.81 percent, the AESC 2021 value; Appendix A and Appendix E of this report give AESC 2024's real discount rate as 1.74 percent.]_

[^430]: Each program administrator should obtain or calculate the losses applicable to its specific system as described in Chapter 10 on avoided T&D costs.

[PDF pp. 377-436 not transcribed: Appendices C-K (C detailed natural gas outputs, D detailed oil and other fuels outputs, E common financial parameters, F user interface, G marginal emission rates and non-embedded environmental cost detail, H DRIPE derivation, I matrix of reliability sources, J guide to calculating avoided costs for cleared and uncleared measures, K scaling factor for uncleared resources), in the other files of this folder (see README.md)]
