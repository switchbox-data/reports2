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
extraction_scope: "partial: PDF pp. 402-410 (printed pp. 384-392), Appendix J: Guide to Calculating Avoided Costs for Cleared and Uncleared measures; the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Appendix J: a worked, simplified illustration (10 MW measure, illustrative Massachusetts-like values) of how AESC calculates cleared and uncleared capacity, capacity DRIPE and reliability avoided costs, including the load forecast effect (LFE) schedule, reserve-margin gross-up, decay schedules, the 2028 switch to a seasonal prompt capacity market, and how to split a portfolio into cleared and uncleared shares."
why_here: "Explains the mechanics (and the electrification caveat that heat pumps raise rather than lower capacity costs) behind the capacity, capacity DRIPE and reliability avoided-cost streams in the AESC User Interface, which Switchbox can use to interpret or rebuild New England capacity-cost and DRIPE treatments of heat pump load."
---

_Extractor note (not source text): this file holds PDF pp. 402-410 (printed pp. 384-392) of AESC 2024, Appendix J: Guide to Calculating Avoided Costs for Cleared and Uncleared measures; the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. The text is transcribed verbatim, including the source's own slips, which are flagged inline with `[sic]` or `[source discrepancy: …]`. The appendix has no tables, figures or equations; the cross-references in the text to Chapter 5, Chapter 9, Chapter 11, Appendix B and Appendix K point to other parts of the report._

[PDF pp. 1-401 not transcribed: front matter, Chapters 1-12 and Appendices A-I, in the other files of this folder (see README.md)]

[PDF p. 402 | printed p. 384]

# Appendix J: Guide to Calculating Avoided Costs for Cleared and Uncleared measures

This appendix provides a simplified explanation of the methodologies and applications of capacity and capacity DRIPE. It uses a set of illustrative numbers to more simply describe the calculations underlying cleared and uncleared capacity and capacity DRIPE. It accompanies the "AppdxJ" tabs of the _AESC 2024 User Interface_, which provide specific numbers for all years, states, and measure lives for the following avoided cost categories:

- Cleared capacity
- Uncleared capacity
- Cleared capacity DRIPE
- Uncleared capacity DRIPE
- Cleared reliability
- Uncleared reliability
- Appendix J tabs are provided for three costing periods: "O" representing original capacity market conditions, which extend through 2027; "S", representing summer capacity market valuations from 2028 through the remainder of the study period; and "W", representing winter capacity market valuations from 2028 through the remainder of the study period.

This appendix is not intended to substitute the more in-depth explanations provided in Chapter 5: _Avoided Capacity Costs_, Section 9.3: _Electric capacity DRIPE_, and Section 11.2: _Value of reliability: generation component_. A few caveats about this summary:

- This section uses illustrative values only. We have selected values that superficially resemble Massachusetts' avoided costs.[^443]
- We simplify some calculation steps for readability but provide footnotes where these steps are more complex in practice.
- We discuss avoided costs as applied to energy efficiency measures, but the avoided costs apply just as easily to demand increases (e.g., from electrification).
- These examples ignore price separation. For more information on the actions performed with auctions that feature price separation, see Section 9.3: _Electric capacity DRIPE._

[^443]: Massachusetts is chosen as an example because it constitutes roughly half of New England's electricity demand.

[PDF p. 403 | printed p. 385]

- The approaches below describe wholesale avoided costs. Further steps are needed to convert wholesale values to retail values. See _Appendix B: Detailed Electric Outputs_ for additional instructions.

### Cleared capacity

Cleared capacity values in AESC represent the avoided cost associated with energy efficiency resources a program administrator has offered and cleared in ISO New England's FCM.

AESC estimates a capacity price for a future delivery year based on the capacity market (e.g., $2 per kW-month, equivalent to $24 per kW-year) as detailed in Chapter 5: _Avoided Capacity Costs_. This value is the avoided cost of cleared capacity. Program administrators then multiply this avoided cost by energy efficiency savings in that year (e.g., 10 MW) to determine the measure's annual benefit. In this example, the annual benefit is $240,000, after converting units. This is $240,000 that ratepayers would not otherwise spend to procure capacity in the capacity market. If the capacity price did not change year-to-year, this measure would provide $240,000 in benefits for every year the illustrative 10 MW measure is in place. The 10 MW measure would provide $960,000 in benefits if the savings persisted for four years.[^444]

This calculation works the same in both the original capacity market period, and the new capacity market projected in 2028 and later years. The sole difference is that in the original period, monthly capacity prices are multiplied by 12 months; in the new capacity market periods, monthly capacity market prices are multiplied by however many months exist in the summer and winter seasons (four months and eight months, respectively). If the 10-MW measure in the above example persisted for eight years (four under the old market structure, and four under the new market structure), and the capacity prices were the same throughout ($2 per kW-month in the old structure, and $2 per kW-month for both summer and winter in the new structure), the total benefits would be $1.9 million.

### Uncleared capacity

A program administrator may choose not to bid all of its energy efficiency portfolio's capacity savings into the capacity market, or it may be possible that a resource does not receive a capacity obligation but is nonetheless built (as is the case with building electrification measures).[^445] As a result, the savings from the "uncleared" amounts do not produce direct savings within the capacity market. However, these measures still provide indirect system benefits by impacting ISO New England's forecast of load, which is

[^444]: This is a simplified example. In practice, program administrators typically discount future benefits and apply T&D losses to convert wholesale avoided costs to retail costs. Capacity values also typically differ year-to-year. Similar caveats apply to the subsequent sections.

[^445]: We note that building electrification measures (such as heat pumps) typically lead to increased capacity costs, rather than savings. For the sake of readability, this appendix refers to savings only. We expect that impacts for measures that cause capacity demand increases (rather than produce capacity demand savings) can be calculated in exactly the same manner.

[PDF p. 404 | printed p. 386] one of the inputs used to develop prices in the capacity market. See Section 5.2: _Uncleared capacity calculations_ for more detail on this avoided cost category.

Because ISO New England's load forecast is based on 15 years of historical data, uncleared measures will eventually impact future load forecasts. However, it takes a few years of sustained savings before the uncleared measures impact the load forecast directly. At that point, the measure's impact can be generally described as a "ramp up" followed by a "fade out." We have created the "load forecast effect" (LFE) schedule to account for this market dynamic. The LFE schedule is a percentage factor that scales a measure's impact on future load forecasts. The percentage varies by calendar year and with the length of time an efficiency measure provides savings (i.e., measure life year). For years covered in the original capacity market, these benefits begin phasing in five years after a measure is installed. This delay is tied to a lag in between (a) when a measure is installed, (b) when a load regression is made, and (c) when the auction occurs—in the original market, three years after the load forecast is assembled. Because we assume that the future capacity market utilizes a prompt auction, we shift the phase-in of this effect forward three years.

Importantly, unlike cleared capacity, benefits from uncleared resources must be summed over the study period, rather than the measure life. This is because benefits do not accrue until after the measure has been in effect for a few years, and because benefits continue to accrue for several years after the measure ceases to be active, as the load reduction moves through the 15 years of data used in the ISO load-forecast regression. In AESC we calculate the stream of annual avoided uncleared capacity costs for each measure life within the study period. For measures with savings that cross the boundary between markets (e.g., a measure installed in 2024 that persist [sic] through 2030), we assume that these effects persist in both market types, as both markets are expected to utilize the same load regression in the same way.

To calculate benefits from uncleared capacity resources, AESC uses the same capacity price calculated in "Cleared capacity," above. We then scale up this capacity price by the reserve margin (e.g., 15 percent) because, by reducing load, uncleared resources avoid the need to purchase additional supply reserves.[^446] We further adjust the resulting value to account for the delayed impact on the load forecast (i.e., the LFE). If we now assume that the 10-MW measure from our above example is uncleared, then the uncleared capacity avoided cost is equal to the product of (a) the capacity price at $24 per kW-year, (b) one plus the reserve margin or 1.15, and (c) the LFE (which varies by year and measure life). For years when the LFE is 100 percent, the resulting avoided cost is $27.6 per kW-year. For a 10 MW measure, this implies benefits in that year of $276,000. However, because the switch to the new market structure occurs before the uncleared capacity benefits begin phasing-in, this measure receives benefits

[^446]: Uncleared measures are effectively "counted" in the demand side of the capacity auction (i.e., within the load forecast). In contrast, cleared measures are effectively treated the same as conventional power plants (i.e., supply), and through the auction require the purchase of some extra amount of capacity to act as a reserve margin. We increase the uncleared capacity benefit by a value equal to one plus the reserve margin to reflect changes on the demand side of the market. Note that in future capacity market periods, the reserve margin can sometimes be negative (reflecting the design of seasonal ELCCs rather than conventional reserve margins), which can cause this "gross-up" to actually be a de-rating.

[PDF p. 405 | printed p. 387] associated with future summer capacity prices and winter capacity prices, rather than benefits associated with prices under the current capacity market structure. Finally, because the LFE varies over time, this value changes in each year. As a result, total undiscounted lifetime benefits are $1.7 million.[^447]

Viewed in isolation, uncleared capacity resources have a larger value than cleared capacity resources. This is because the cleared resources only provide benefits in the years that the measure is active and participating in the capacity market, whereas uncleared resources provide benefits (even at a reduced level) for several years after the measure ceases to provide savings. Uncleared capacity resources may also be larger because they include an avoided reserve margin. Because many of the uncleared capacity benefits accrue in the mid- to far-future, but the cleared capacity benefits accrue in the near term, applying a discount rate could cause the uncleared capacity benefit (in this hypothetical example, $1.4 million) to be equal to or perhaps less than the cleared capacity benefit (here, $1.2 million).

### Cleared capacity DRIPE

DRIPE describes the phenomenon wherein 1 MW of savings not only avoids a purchased quantity, but also changes the price that all purchasers in the capacity market pay for capacity. Cleared capacity DRIPE, specifically, represents the price effects on the capacity market from measures bid into the capacity market. These effects can be further subdivided into two categories: benefits to consumers within the state where the measure is installed (intrazonal effects) and benefits to consumers outside of the state where the measure is installed (interzonal effects). AESC translates these price effects (which describe how the system's prices change as demand changes) into DRIPE values (which describe the benefits that accrue to any one measure due to this price effect). See Chapter 9: _Demand Reduction Induced Price Effect_ for more background on the concept of DRIPE and Section 9.3: _Electric capacity DRIPE_ for more details about capacity DRIPE in particular.

Cleared capacity DRIPE is calculated as follows: first, the "price shift" is estimated. The price shift represents how the capacity price would change if 1 fewer MW of capacity were required. It is calculated by examining the supply curves observed by ISO New England and calculating the slope of each line segment between each auction round.[^448] This price shift is measured in terms of capacity price per unit demand, or $/kW-month per MW. These price shifts are generally very small numbers. For example, the price shift might be $0.001/kW-month per MW, or $0.012/kW-year per MW.[^449]

Second, we multiply these price shifts by the capacity requirement for each state because the price effect impacts resources throughout in the FCM, not just the efficiency resources responsible for the

[^447]: We note that because the phase-in is shifted three years early under the new market structure, measures installed before 2028 may miss out on those benefits that occur in the earliest phase-in years.

[^448]: We assume that all future supply curves have the same shape as the most recent capacity auction, but shifted to account for changes in supply. In AESC 2021, this is FCA 15.

[^449]: Price shifts may change year-to-year as the corresponding year's capacity price changes position on the supply curve.

[PDF p. 406 | printed p. 388] price shift. However, we assume that only a subset of these resources is subject to the price shift. Load-serving utilities purchase some amount of their capacity outside of the FCM to mitigate the risk of price volatility in the capacity market—i.e., as a financial hedge. In AESC, only the "unhedged" portion of the capacity requirement (i.e., the share that is bought via the capacity market) would be impacted by DRIPE effects.[^450]

Finally, we apply an annual decay schedule. AESC assumes the price effect fades out over time as retail prices fall (encouraging higher load), existing resources retire, and new potential resources are abandoned. As a result, price effects are fully realized in the year of installation, but completely phased out six years later. The benefit of cleared capacity DRIPE decays over time, but that decay does not change with the efficiency resource's measure life (unlike the LFE schedule used for uncleared capacity and uncleared capacity DRIPE, which changes with the measure life).

If we assume that our example state has 10,000 MW in unhedged capacity requirement, multiplying this by the $0.012/kW-year per MW price effect from above yields a value of $120 per kW-year. Scaled by the decay effect, this value will be $120 per kW-year in years with no decay and $0 per kW-year in subsequent years with full decay. This is then the avoided cost for cleared capacity DRIPE.

As with cleared capacity, the effects of cleared capacity DRIPE should be summed over the measure lifetime, rather than the study period. As our 10-MW measure lasts for eight years, we find that it produces undiscounted intrazonal DRIPE benefits of $4.2 million. Assuming our example state's 10,000 MW of unhedged demand is exactly half of the regional unhedged capacity requirement, the interzonal DRIPE benefits are also $4.2 million, without discounting. Total cleared capacity DRIPE benefits are the sum of these two values, or $8.4 million. We assume that these effects extend across the market transition year; under the new market, benefits are simply estimated using the new markets' price shifts rather than the old market's price shifts.

### Uncleared capacity DRIPE

Uncleared capacity DRIPE is the price-shifting benefit that accrues to measures not bid into ISO New England's FCM. Even though these measures are outside the capacity market, they impact the load forecast inputs, and thus provide uncleared capacity DRIPE benefits. As with cleared capacity DRIPE, there are both intrazonal and interzonal benefits.

For the most part, uncleared capacity DRIPE is calculated the same as cleared capacity DRIPE. We begin with a price shift observed from the latest FCA (e.g., $0.0012/kW-year per MW) [source discrepancy: the cleared capacity DRIPE example above uses $0.012/kW-year per MW, and $0.012 × 10,000 MW gives the $120 per kW-year stated next], which is then multiplied by a zone's unhedged capacity requirement (e.g., 10,000 MW). This $120 per kW-year result is the avoided cost. But there are two key differences compared to cleared capacity DRIPE.

[^450]: In practice, over a long enough period, prices paid for hedged capacity ought to converge to the market price. Because our estimates of DRIPE exclude this hedged amount, they can be considered a conservative estimate.

[PDF p. 407 | printed p. 389]

1. First, uncleared capacity DRIPE utilizes an LFE schedule. For uncleared capacity DRIPE, we assume the load forecast and thus the capacity market gradually incorporates the impacts of uncleared load reductions (just like with uncleared capacity). This effect persists for some period before the market readjusts, and the DRIPE benefit fades out. This LFE schedule is based on the one used for uncleared capacity but is adjusted to reflect a decay in DRIPE benefits over time. This is the same decay schedule used for capacity DRIPE. As with uncleared capacity, this LFE schedule varies depending on measure lifetime. As with uncleared capacity, we assume this LFE schedule is shifted forward three years in the new market structure, as we assume a prompt market comes into effect.
2. Second, because uncleared capacity DRIPE results from a reduction in the load forecast rather than the addition of capacity, we multiply these benefits by a factor of one plus the reserve margin.

The annual intrazonal uncleared capacity DRIPE is equal to the product of (a) the price shift in that year, (b) the zone's unhedged capacity requirement for that year, (c) one plus the reserve margin, and (d) that year's LFE value. Interzonal uncleared capacity DRIPE is calculated the same way but uses the regional unhedged capacity requirement, less the unhedged capacity requirement for the zone in question.

As with uncleared capacity, uncleared capacity DRIPE benefits are summed over the study period (rather than the measure life), as benefits continue to accrue years after the measure has been installed and expires.

In our continued example, because there is a phase-in of uncleared capacity DRIPE benefits, no benefits accrue during the years when the current capacity market is active. Instead, they accrue under the load regressions used in the future markets, producing undiscounted intrazonal and internzonal [sic] uncleared capacity DRIPE benefits of $3.7 million each. Total uncleared capacity DRIPE benefits are $7.4 million.

### Cleared reliability

The operation of the ISO New England capacity market increases the amount of capacity acquired as the price falls. To the extent that energy efficiency programs reduce the capacity clearing price, reserve margins and reliability will increase.

To calculate cleared reliability benefits, we first estimate four values:

- First, VoLL is the cost experienced by customers during an outage. It is determined through a review of the literature. In AESC 2024, we estimate this value at $61 per kWh.
- Second, we estimate the change in MWh of reliability benefits per MW of reserve. This is calculated by observing the slope of the demand curve used in the FCA at the point of the clearing price. A typical value might be 0.2 MWh per MW.
- Third, we derate reliability benefits based on the fact that bidding in an additional MW into the FCA at $0 per kW-month price shifts the supply curve to the right and shifts out some smaller amount of capacity that would otherwise have cleared. As a result, the [PDF p. 408 | printed p. 390] amount of cleared supply increases by just a fraction of the additional supply. This value is determined by examining the percentage difference in slopes of the demand curve and supply curve at the point of the clearing price. A typical value might be 20 percent.
- Finally, we assume a decay effect. We use the same decay effect that is applied to cleared capacity and uncleared capacity due to similar expected dynamics in market response.

We then multiply these four values against one another to estimate the avoided cleared reliability cost in each year the resource is active. Cleared reliability benefits do not differ based on measure life. Using the same example as above (a 10-MW measure with an eight-year lifetime), we would expect cleared reliability benefits of about $0.1 million. Reliability benefits are much smaller than benefits provided by other avoided cost categories.

### Uncleared reliability

Resources that do not clear in the capacity market may still provide a reliability benefit. Some resources that do not clear the FCA will continue to operate as energy-only resources, adding to available reserves. While not obligated to do so, these resources are likely to operate at times of tight supply and high energy prices. They may also be available to assume the capacity obligations of resources that unexpectedly retire or otherwise become unavailable. In addition, resources that do not clear in the capacity market or immediately affect the load forecast will increase reserve margins and contribute to improved reliability.

To calculate uncleared reliability benefits, we first estimate five values:

- First, just as with cleared reliability, we utilize a VoLL. The VoLL in AESC 2024 is $61 per kWh.
- Second, just as with cleared reliability, we estimate the change in MWh of reliability benefits per MW of reserve. A typical value might be 0.2 MWh per MW.
- Third, we gross up benefits to reflect the reserve margin, as these resources are not resources bid into the capacity market and thus reduce supply.
- Fourth, we assume that reliability has a phased effect. Measures provide a reliability benefit as soon as they are installed. This benefit persists for a period of time then fades out. As with uncleared capacity and uncleared capacity DRIPE, we assume this schedule is shifted forward three years in the new market structure, as we assume a prompt market comes into effect.
- Fifth, we assume a separate decay effect that reflects the fact that after a period of time, all the of [sic] the reliability benefits will have been captured in the load forecast. This effect is also assumed to shift forward three years under the new market structure.

We then multiply these five values against one another to estimate avoided uncleared reliability costs. Uncleared reliability differs from the other uncleared avoided cost categories in two ways:

[PDF p. 409 | printed p. 391]

- Unlike uncleared capacity and uncleared capacity DRIPE, uncleared reliability benefits are summed over the years in which the measure is active, rather than the entire study period. This is similar to how avoided costs are summed for cleared reliability and most other avoided cost categories.
- Uncleared reliability benefits do not differ based on measure life.

Using the same example as above (a 10-MW measure with an eight-year lifetime), we would expect cleared [sic; the paragraph is about uncleared reliability] reliability benefits of about $0.8 million. Generally speaking, uncleared effects are greater than cleared effects because they are not impacted by the net increase in cleared supply variable (which only affects resources that clear the market).

### Applying these values

For a portfolio of measures, a program administrator may bid only a share of its capacity savings into the capacity market. In these situations, the program administrator should split the cleared and uncleared savings and calculate benefits accordingly. In our example, if a program administrator bids into the capacity market 50 percent of its 10-MW portfolio of measures, it would provide $960,000 in undiscounted cleared capacity benefits and $855,600 in uncleared capacity benefits (e.g., each of the values calculated above is halved). Likewise, the portfolio of measures provides $4.0 million in cleared capacity DRIPE benefits and $3.7 million in uncleared capacity DRIPE benefits (again, the above values are halved). Reliability benefits are much smaller: this example would yield cleared reliability benefits of $0.05 million and uncleared reliability benefits of $0.4 million.

In practice, (a) measures have different measure lives, (b) each of these avoided cost categories have different decay or LFE schedules, (c) values change over time, and (d) program administrators utilize a discount rate. As a result, program administrators must take a weighted average by measure-life year over the study period, not calendar year. Separate cost streams for cleared capacity, uncleared capacity, cleared capacity DRIPE, uncleared capacity DRIPE, cleared reliability, and uncleared reliability should be calculated independently for each cleared or uncleared MW (or share of MW).

### Capacity vs. capacity DRIPE

At first glance, capacity DRIPE benefits may appear surprisingly large relative to capacity benefits. But, changing the price of capacity is a high-value action, because it reduces the cost of procuring capacity for all resources in the system, not just the energy efficiency resources instigating the price change.

For example, assume total unhedged capacity cleared in New England is 20,000 MW, all of which clears at $2 per kW-month. This implies a total annual market value is $480 million. If our 10-MW measure were entirely bid into the capacity market, it would produce $0.24 million in capacity benefits in one year. This is about 0.05 percent of the market's total value and represents a one-for-one switch between one type of capacity (energy efficiency) for another kind (e.g., a conventional fossil resource).

But, because of price-shifting effects, the cleared measure also lowers the price that other market participants pay for the 20,000 MW. By lowering the price for all 20,000 MW, this measure produces [PDF p. 410 | printed p. 392] annual cleared capacity DRIPE benefits of $2.4 million, or 0.5 percent of the $480 million total market value (e.g., one order of magnitude larger than the capacity benefit).

These are both small numbers, relative to the size of the market. But because the DRIPE effect is multiplied across 20,000 MW, rather than just 10 MW, the final benefit is larger.

### Scaling factor for uncleared resources

Energy efficiency measures generally save energy according to a consistent pattern throughout a year (i.e., its load shape) because they perform the same functions as the less efficient technology while using less energy. Alternatively, demand response resources are designed to provide savings during specific time periods depending on grid characteristics that vary by year, day, and hour. Demand response resources are often subject to customer responsiveness, which can fluctuate with a customer's annual participation in a demand response program and with each demand response event called. As a result, demand response resources typically have shorter and more variable durations, both in terms of measure lives and annual hours of operation. Because of this variability, uncleared measures may not have a "full" effect on the load forecast. This implies that their uncleared benefits should be scaled according to how frequently the measure is expected to operate (and, as a result, impact the load forecast).

To account for demand response's limited impact on the load forecast, AESC recommends that program administrators apply a scaling factor that adjusts uncleared capacity, uncleared capacity DRIPE, and uncleared reliability benefits. The scaling factor is a measure-specific percentage multiplier that should be estimated based on a demand response program's design, implementation, and participant responsiveness. See text in the following section, Appendix K: _Scaling Factor for Uncleared Resources_, and the accompanying workbook titled "Appendix K.xlsx" for more information on how to calculate this scaling factor for different measures.

We note that the scaling factor should not be applied to reliability values. Because we expect ISO New England's use of the load regressions used for each individual year to be unchanged under the new market structure, we determine that the scaling effects described in Appendix K can be applied to benefits accruing under both the current market structure and the assumed new market structure that is effective in 2028.

[PDF pp. 411-436 not transcribed: Appendix K (scaling factor for uncleared resources), in the other files of this folder (see README.md)]
