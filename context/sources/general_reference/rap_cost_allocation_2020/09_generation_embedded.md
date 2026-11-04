# Part III: Embedded Cost of Service Studies

## 9. Generation in Embedded Cost of Service Studies

his chapter addresses the allocation of generation costs, including investment-related costs, operation **T** and maintenance costs and fuel costs. As noted in Section 6.1, equivalent changes in the allocation of a cost category among classes can be achieved by changing functionalization, classification or the choice of allocation factor.[^83] That section discusses the relevant issues at a high level, and this chapter delves more deeply into the underlying concepts and analytical techniques.

This chapter is not generally relevant to cost allocation for utilities that have restructured and no longer procure generation resources, as long as the generation prices suppliers offer (directly to customers or to the utility for default service) are differentiated by rate class. High-level cost allocation issues with respect to generation and default service are discussed in Section 7.2.

As discussed in Chapter 3, utilities acquire and maintain different types of generation resources, with distinct operating capabilities, to meet a range of needs including low-cost energy, reliability, **load following** and environmental compliance. Different classification and allocation methods may be necessary to equitably allocate the costs of different types of generation resources. In more recent years, energy efficiency, expanded demand response, distributed generation and energy storage — all of which can be located where load relief is most valuable — have expanded the utility’s options to meet load growth or reduce demands on aging assets without building transmission, distribution or central generation facilities.

Fuel costs, purchased power and dispatch O&M costs, such as the short-run variable cost of pollution controls, are typically classified as energy-related. The other categories of generation costs have generally been classified as being driven by some combination of energy (total energy requirements to serve customers, plus losses) and demand (some measure of loads in the hours that contribute to concerns about the

adequacy of generation supply to meet loads). Energy use is sometimes broken into TOU periods, so that different types of costs are spread over the hours in which they are used, as discussed further in Section 9.2 and Chapter 17.

When there are multiple cost-based approaches for estimating a classification or allocation factor, a compromise among the results may be appropriate. For example, various measures of reliability risk (emergency purchases, operation of peakers, interruption of load, inadequate operating reserve) may be distributed differently across the months, and the regulator may reasonably select a generation demand allocator averaging across the results of those measures. Similar conditions might apply for varying estimates of the firm-capacity equivalent for wind plants or other inputs.

Some cost of service studies identify other classifications of generation costs, such as ancillary services. These components are generally very small compared with total generation costs, and some ancillary services (automatic generation control, black start capability, uplift) can be difficult to relate to class load characteristics.

### 9.1 Identifying and Classifying Energy-Related Generation Costs

Many regulators have recognized that energy needs are a significant driver of generation capital investments and nondispatch O&M costs. In modern utility systems, generation facilities are built both to serve demand (i.e., to meet capacity and reliability requirements) and to produce energy economically. The amount of capacity is largely determined by reliability considerations, but the selection of generation technologies and thus the cost of the capacity are

[^83]: As mentioned previously, the third step is usually called allocation, which is the same as the name of the entire process . Some analysts refer to this third step as factor allocation in an attempt to prevent confusion .

largely determined by energy requirements.[^84] For variable renewables, particularly wind and solar, the effective capacity (in terms of the reliability contribution) of the generators is much smaller than their nameplate capacity, and the costs are mostly undertaken to provide energy without fuel costs or air emissions. Energy storage systems provide both energy benefits (by shifting energy from low-cost to high-cost hours) and reliability benefits, while demand response is used primarily to increase reliability.

As discussed in the text box on pages 78-79, some older cost of service studies classified a wide range of capital and nondispatch O&M costs as demand-related on the grounds that the costs were in some manner fixed, without regard for cost causation. This approach, known as **straight fixed/variable** , is anachronistic and does not reflect cost causation.[^85]

Table 12 shows the capital and O&M costs estimated for new conventional generation units from the 2018 Lazard’s _Levelized Cost of Energy Analysis_ report.[^86] Although the original costs and current plant in service and O&M costs of older units will vary, the general relationships have been consistent. This section first discusses the insights on this issue

Table 12. Cost components of conventional generation, 2018 midpoint estimates

| Technology             | Capital<br>cost<br>(per kW) | Fixed<br>operations and<br>maintenance<br>(per kW-year) | Variable<br>operations and<br>maintenance<br>(per MWh) |
| ---------------------- | --------------------------- | ------------------------------------------------------- | ------------------------------------------------------ |
| **Combustion turbine** | $825                        | $12 .50                                                 | $7 .40                                                 |
| **Combined cycle**     | $1,000                      | $5 .75                                                  | $2 .80                                                 |
| **Coal**               | $3,000                      | $40 .00                                                 | $2 .00                                                 |
| **Nuclear**            | $9,375                      | $125 .00                                                | $0 .80                                                 |

Source: Lazard. (2018). _Lazard’s Levelized Cost of Energy Analysis — Version 12.0_

[^84]: “Citing both past operating experience and future resource planning, the Division [the PSC intervention staff] notes that resources with higher energy availability are chosen over those with lower energy availability . Since energy plays a role in the selection of least-cost resources, the Division concludes that some weight needs to be given to energy in planning for new capacity, and the current weight of 25 percent is reasonable . We find the qualitative argument offered by the Division to be … convincing .” (Utah Public Service Commission, 1999, p . 82) . See also Washington Utilities and Transportation Commission (1993, pp . 8-9) .

[^85]: The term “straight fixed/variable” is imported from FERC’s rate design method for wholesale gas supply, where utilities, marketers and very large customers contract for capacity in a portfolio of individual pipeline and storage facilities . As is true for many electric wholesale purchased

from competitive wholesale markets. This is followed by four different classification approaches and two joint classification and allocation approaches, then a discussion of other technologies and issues.

#### 9.1.1 Insights and Approaches From Competitive Wholesale Markets

The ISOs/RTOs that operate energy (and in some cases, capacity) markets — specifically ISO-NE, NYISO, PJM, ERCOT, MISO and the SPP — provide examples of how the recovery of capital investment and nondispatch O&M costs naturally splits between energy and demand. The pricing in these markets can provide both a **competitive proxy** for classifying generation costs and a benchmark to check the reasonableness of other techniques.

ERCOT has no capacity market, and all costs are recovered through time-varying energy charges. Those energy charges are heavily weighted toward a small number of hours, which do not tend to have particularly high loads; the highestload hours are not the highest-cost hours. Figure 30 on the next page shows the hourly load and Houston Hub prices for 2017 (Electric Reliability Council of Texas, 2018, for load data; ENGIE Resources, n.d., for pricing data).

Prices generally trend upward with load, but the highestpriced hours are spread nearly evenly across load levels.

In 2017, the highest-priced 1% of hours (with prices over $160 per MWh) would have provided 18% of the annual net margin for a baseload plant with no variable cost, 53% of the margin for a plant with a variable cost of $20 per MWh (perhaps a combined cycle unit), and 77% of the margin for a plant with a $30-per-MWh variable cost (such as a recently built combustion turbine), assuming ideal dispatch and no

> power contracts, these gas contracts require that the buyers pay for investment-related costs regardless of how they use the resources and pay for variable costs in proportion to their usage . This approach is workable at the wholesale level but is not applicable to retail cost allocation, where the utility bundles a portfolio of generation assets for all of its customers .

[^86]: The coal cost in the table is Lazard’s low end, since the high-end cost “incorporates 90% carbon capture and compression” (Lazard, 2018, p . 2), which is in use on only one existing utility coal unit, SaskPower’s Boundary Dam . The $3,000/kW value is also consistent with the costs of the last three coal plants completed by U .S . regulated utilities (Turk, Virginia City and Rogers/Cliffside 6, all completed in 2012) . Actual current costs of various vintages of resources will vary for each utility .

##### Figure 30. ERCOT load and real-time prices in 2017

$2,250<br>$2,000<br>$1,750<br>$1,500<br>$1,250<br>$1,000<br>$750<br>$500<br>$250<br>$0<br>-$250<br>20,000 25,000 30,000 35,000 40,000 45,000 50,000 55,000 60,000 65,000 70,000<br>Hourly load in megawatts<br>Hourly price per megawatt-hour<br>

Sources: Electric Reliability Council of Texas. (2018). _2017 ERCOT Hourly Load Data_ ; ENGIE Resources. _Historical Data Reports_

outages. Those 88 hours representing the costliest 1% occurred in every month and almost the whole range of annual loads.

In contrast, the 1% of highest-load hours would have provided 5.1% of the margin for the baseload plant, 2.4% for the intermediate plant and 2% for the combustion turbine. This cost pattern suggests that, at least in some systems, generation costs should be time-differentiated but that load is not a good proxy for the highest-price periods. Classes with the ability to shape load to low-cost periods (with demand response or storage) may be much less expensive to serve than those with inflexible load patterns.

Regardless of how the top hours are chosen, the ERCOT data indicate that most of the long-term power supply costs are not recovered from the few peak hours and thus should not be considered demand-related. For a load shaped like the ERCOT average load, only about 3% of the generation costs were associated with the 1% of highest-load hours, and about 20% were associated with the 1% of highest-price hours.

In New England, the ISO-NE external market monitor

estimated that the net revenues available to pay the capital investment and nondispatch O&M costs of a typical recently built gas combined cycle unit would have been about 25% to 60% from the energy market and the remainder from the capacity market, depending on the year (Patton, LeeVanSchaick and Chen, 2017, p. 13). The comparable values for nuclear units were almost all from the energy market (Patton et al., 2017, p. 17).

The PJM independent market monitor reports the capacity revenues and the net energy revenues (i.e., energy revenue in excess of fuel and variable O&M) for a variety of plant types (Monitoring Analytics, 2014, pp. 219-222, 2019, pp. 335-339). These are the revenues available to pay for the capital investment and nondispatch O&M costs and thus represent the market allocation of these costs for the plants. Figure 31 on the next page shows the portion of these costs recovered through capacity payments for four types of new plants (gas-fired combustion turbine and combined cycle units, and hypothetical new coal and nuclear) in each year

##### Figure 31. Capacity revenue percentage in relation to capacity factor in PJM

100%<br>Combustion turbine<br>90% Combined cycle<br>Coal<br>80%<br>Nuclear<br>Trend<br>70%<br>60%<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>10% 20% 30% 40% 50% 60% 70% 80% 90% 100%<br>Capacity factor<br>Capacity revenue as percentage of total revenue<br>

Data sources: Monitoring Analytics. (2014 and 2019). _2013 State of the Market Report for PJM, 2018 State of the Market Report for PJM_

2009 through 2017 (Monitoring Analytics, 2014, 2019).[^87]

The concept displayed here is that units with a high **capacity factor** tend to make more of their revenue from energy markets instead of from the capacity market. In this set of PJM data, energy revenues cover 14% to 60% of the combustion turbine costs, 38% to 74% of combined cycle costs, 56% to 73% of baseload coal plant costs, about 34% of the costs of economically dispatched coal units, and 77% to 89% of nuclear costs over the nine-year period. The values for 2017 were 39% for modern combustion turbines, 87% for combined cycle units, 65% for coal and 20% for nuclear. Current values for PJM or the relevant load zones could be used as the demand classification percentages for vertically integrated utilities in PJM (e.g., IOUs in Kentucky, Virginia and West Virginia, and municipal and cooperative utilities in several states).

The market monitoring unit of the NYISO provided similar analyses for the various pricing zones of that RTO, as shown in Table 13 (Patton, LeeVanSchaick, Chen and Palavadi Naga, 2018, Table A-14, with additional calculations by the authors). The upstate zones have relatively low capacity

prices, while the Hudson Valley and New York City have very high capacity prices, and Long Island has intermediate prices. Both capacity and energy revenues vary among zones within each of these three areas, between load pockets within zones and among combustion turbine types.

Table 13. Energy portion of 2017 net revenue for New York ISO

| Zone                                       | Combustion<br>turbines<br>G | Combined<br>cycle<br>enerator type | Steam      |
| ------------------------------------------ | --------------------------- | ---------------------------------- | ---------- |
| **Upstate**                                | 72% to 80%                  | 71% to 79%                         | 42% to 55% |
| **Long Island**                            | 52% to 70%                  | 62% to 76%                         | 21% to 57% |
| **Hudson Valley and**<br>**New York City** | 31% to 49%                  | 34% to 55%                         | 6% to 29%  |

Sources: Patton, D., LeeVanSchaick, P., Chen, J., and Palavadi Naga, R. (2018). _2017 State of the Market Report for the New York ISO Markets;_ additional calculations by the authors

[^87]: The independent market monitor assumed that a nuclear plant would operate at a 75% capacity factor and made the same assumption for the coal plant through 2015; the capacity factors for the gas-fired plants and for coal in 2016 and 2017 are determined from the economic operation of the units .

#### 9.1.2 Classification Approaches

Many utilities and regulators acknowledge that a large portion of generation investment and nondispatch O&M costs is incurred to serve energy requirements. There are two categories of methods to classifying these costs as energyrelated and demand-related. First, average-and-peak is a top-down approach that uses high-level data on system loads and costs. Second, there is a range of bottom-up approaches that examine the drivers for costs on a plant-specific basis:

- Base-peak and related methods.

- Equivalent peaker method.

- **Operational characteristics methods** .

As a general matter, the bottom-up approaches are preferable for classifying generation costs. The average-andpeak approach is well suited for shared distribution system costs, as discussed in Section 11.2.

The system load factor, and hence the average-and-peak approach more generally, varies over time independent of the mix of the utility’s generation resources and does not respond to changes in that mix unless those changes are accompanied by retail pricing that follows the cost structure.

In addition to changing as loads change, the average-andpeak approach ignores the mix of resources and costs. This approach would produce the same classification of plant for a system that was entirely composed of gas-fired combustion turbines (with low capital costs and high fuel costs) or of coal-fired plants (with high capital costs to produce lower fuel costs).

Thus, while the average-and-peak method for generation costs may sometimes fall in the range of reasonable results, it is neither logical nor consistent.

###### Base-Peak Methods

###### Average-and-Peak Method

The average-and-peak approach can be applied in classification, when classifying a portion of costs as energy-related and the remainder as demand-related, or in developing a generation capacity allocator that reflects both energy and demand. When using this approach as a classification method, the **system load factor** percentage is classified as energy-related and the remainder as demandrelated.[^88] When used as an allocation factor, the averageand-peak factor for each class is:[^89]

Where A = annual average load = energy ÷ 8,760 P = peak load C = class S = system SLF = system load factor = (annual energy) ÷ (peak load × 8,760)

[^88]: This method is sometimes called the system load factor approach . It has also been called “average and excess” because a fraction of cost equal to the system load factor is allocated on energy and the excess of costs on a measure of peak loads (Coyle, 1982, pp . 51-52) .

Various utilities and other analysts have proposed to subfunctionalize generation resources (in the simplest case, between baseload and peaking plants) and classify each category of generation in a different manner. For example, peakers may be classified 100% as demand-related, while baseload resources are classified 75% to demand and 25% to energy, or some other location- and situation-specific ratio.

More advanced analyses have subfunctionalized generation among base, intermediate and peak categories, known as BIP classification. The base generation might be defined as all nuclear and coal plants, with the intermediate being gas-fired steam and combined cycle plants and the peak units being combustion turbines, storage and demand response. Alternatively, base plants might be any unit that operated at more than a certain capacity factor (for example, 60%), peakers those that ran at less than 5%, and intermediate anything between those 5% and 60% capacity factors. Or, rather than using capacity factor (which can be low due to forced outages, maintenance or economic dispatch), the

[^89]: This average-and-peak allocator should not be confused with the averageand-excess demand allocator described in the 1992 NARUC _Electric Utility Cost Allocation Manual,_ which allocates a portion of costs in proportion to average load and the excess in proportion to each class’s excess of peak load over its average use . That legacy average-and-excess allocator is essentially just a peak allocator (Meyer, 1981) .

generation classes can be defined using operating factor (the ratio of output to equivalent availability). At an extreme, each generation type, or even each unit, can be classified separately.

While the base-peak classification approach and related methods are highly flexible, that is both their greatest strength and a great weakness. The strength is that the method can be modified to accommodate the diversity of generation resources; the weakness is that the method requires a set of decisions about the definition of the generation classes and the classification percentage for each class. The base-peak method is connected to actual utility planning only at the highest conceptual level and provides limited guidance for the nitty-gritty details of traditional classification.

One of the challenges of the base-peak approach relates to the changing usage of generation resources. For example, several units that were built to burn coal in baseload operation have been converted to burn natural gas and thus run mostly on high-load summer days.[^90] These units operate as peak or intermediate resources (depending on the definitions used in the particular analysis), but most of the capital costs are attributable to the original baseload design. This problem may be ameliorated by removing those additional costs from the base-peak or BIP computation and directly classifying them as energy-related.

Recent technological changes pose additional challenges and opportunities for expanding the base-peak approach from two generation profiles, or the three profiles of the BIP method, to a full analysis of the use of generation resources. Decades ago, it was reasonably accurate to treat generation resources as being stacked neatly under the load duration curve in order of variable costs. The growing role of variable

[^90]: Some coal plants that once ran as baseload resources have been taken out of service in low-load months to reduce O&M costs . This includes Nova Scotia Power’s Lingan 1 and 2 (Barrett, 2012), Luminant’s Monticello and Martin Lake (Henry, 2012) and the Texas Municipal Power Agency’s Gibbons Creek (Institute for Energy Economics and Financial Analysis, 2019) .

output renewable resources, additional storage and economic demand response reduces the accuracy of those simple models. Resources like wind and solar do not fit neatly into the BIP categories, providing service in distinct time patterns that may not be related to system loads. At the same time, many utilities have access to much more granular detail on hourly consumption by customer.[^91] The BIP method can be expanded to reflect conditions (output by several classes of conventional generation, solar, wind and storage; energy use for storage; usage by class) in as many time periods (or load levels, or bins combining consumption and generation conditions) as desired, even down to an hourly allocation method. Usage and hence costs could thus be assigned directly to the classes using power at the times that each resource provides service.[^92]

###### Equivalent Peaker Method

The equivalent peaker method,[^93] discussed at length in the 1992 NARUC _Electric Utility Cost Allocation Manual,_ attributes as demand-related the portion of investment in each resource that would have been incurred to secure a peaking resource, such as demand response or a combustion turbine.[^94] Peaking resources are usually treated as 100% demand-related, while intermediate and baseload plants are classified as partly energy and partly demand.

If only peak load had been higher (and other needs were already satisfied) in the years in which the utility made the bulk of its generation construction decisions, it would have likely met that increased load by adding peaker capacity.[^95] Utilities historically have justified building baseload capacity by relying on these plants’ long hours of use and lower fuel

> way: 34% (the ratio of minimum to peak load) to energy; 36% (the 90% ratio of winter peak to summer peak, minus the 34% energy allocation, or 56%, times the 65% of the peak-period hours that occur in winter) to the winter peak demand; and the remaining 30% to the summer peak demand (Seelye, 2016, Exhibit WSS-11) . This approach has no cost basis .

[^93]: In some jurisdictions, this is called the peak credit method .

[^91]: Most utilities have long known the hourly generation by unit .

[^92]: Some utilities refer to their classification method as BIP, even though it does not reflect the differences in costs among the various types of generation . For example, the Louisville Gas & Electric and Kentucky Utilities 2018 “BIP” computation classified nondispatch generation costs this

[^94]: This approach is sketched out in Johnson (1980, pp . 33-35) and described in more detail in Chernick and Meyer (1982, pp . 47-65) .

[^95]: To some extent, the peakier load would likely allow for development of more demand response and load management . Estimating the potential and costs for these resources under hypothetical load shapes may be difficult .

costs.[^96] This incremental capital cost (often called capitalized energy or “steel for fuel”) is attributable to energy requirements, not demand. The investment-related costs of baseload resources above and beyond the cost of peaking units are incurred to serve energy load, not demand. Treating these costs as demand-related overstates the cost of meeting demand and understates the costs incurred to meet energy requirements. This phenomenon has been understood since the 1970s and 1980s:

[T]he extra costs of a coal plant beyond the cost necessary to build a combustion turbine should all be allocated [on] energy. The rationale for this allocation is that the marginal cost of capacity in the long run is just the lowest-cost technology required to meet peak load, which is typically a combustion turbine. Choosing to invest beyond this level [of combustion turbine capital cost] is justified not on capacity grounds, but on energy grounds. That is, the extra capital cost of a coal plant allows the utility to use a low-cost fuel and avoid higher-cost fuels (Kahn, 1988).

However, there are several additional issues with this concept in the modern electric system. First, the method does not adapt well to wind and solar, where the capital investment is primarily justified by avoiding fuel costs but the installed capital cost per nameplate MW may be little different from the cost of a peaker. An intermediate or baseload plant that is not much more expensive than a contemporaneous peaking resource would be classified as mostly demand-related, while very expensive plants are classified as mostly energy-related. And often, peaker units are used to provide energy when baseload units are not operating or to provide power for off-system sales.[^97]

Under the equivalent peaker method, the demand- or

[^96]: Similar reasoning applies to the decision to add renewable resources, substituting investment for fuel costs . See footnote 120 .

[^97]: During the 2000-2001 California energy crisis, oil-fired peakers in the Pacific Northwest operated at high monthly capacity factors because they were exempt from both gas supply constraints and California emissions regulations . U .S . Energy Information Administration Form 906 for 2000 and 2001 demonstrates the incremental oil burn in 2000 and 2001, particularly for Puget Sound Energy .

[^98]: In the future, the reference peaking capacity might be an increase in

reliability-related portion of the cost of each generation unit is estimated as the cost per kW of a peaker (usually a simplecycle combustion turbine) installed in the same period, times the effective capacity of that unit, adjusted for the equivalent availability of a peaker.[^98] The cost of the unit in excess of the equivalent gas turbine capacity is energy-related.

However, the simple version of this calculation typically will overstate the reliability-related portion of plant cost because it assumes a steam plant supports as much firm demand as would the same capacity of (smaller) combustion turbines. Due to higher forced outage rates, lengthy maintenance shutdowns and the size of units, a kilowatt of steam plant capacity typically supports less firm load than a kilowatt of capacity from a small peaker. A system with a peak load of about 6,500 MWs and a 65% load factor could achieve the same level of reliability with 80 units of 100 MWs (8,000 MWs, or a 23% reserve) or 19 units of 600 MWs (11,400 MWs, or a 75% reserve), assuming the units all have a 6% **equivalent forced outage rate** and that the load shape can accommodate all required maintenance off-peak. Increasing the equivalent forced outage rate to 10% would increase the required reserve for the 100-MW units to about 40% and for the 600-MW units to 90%. Even with the 6% equivalent forced outage rate, if the load factor were 96%, the reserve requirement would rise to 30% with 100-MW units and 90% with 600-MW units.

Figure 32 on the next page shows the gross plant per kW for combustion turbines as of 2011, from FERC Form 1 data (Federal Energy Regulatory Commission, n.d.). These values include the original cost of the units, plus capital additions since the plants entered service, minus the cost of any equipment retired. This tabulation includes all nonCHP simple-cycle combustion turbines for which cost data were available.[^99] Some of the later combustion turbines in this sample may not be pure peakers, since manufacturers

> demand response cost or storage peak output capacity, without an increase in energy generating capability . The reference peaker should always be the least-cost option for providing reliability .

[^99]: Municipal and cooperative utilities and non-utility generators (both those under contract with utilities and those operating in the merchant markets) do not file FERC Form 1 reports, so their units are not included in this analysis . The municipal and cooperative utilities typically retain financial and operating records that are compatible with the FERC system of accounts, allowing comparison of the data for a specific utility’s nonpeaking resources with national data on contemporaneous peaker costs .

Figure 32. Cost of combustion turbine plant in service in 2011<br>$600<br>Average for year<br>$500<br>Five-year rolling average<br>$400<br>$300<br>$200<br>$100<br>$0<br>1960 1965 1970 1975 1980 1985 1990 1995<br>Plant in-service year<br>Gross plant cost per kilowatt of capacity<br>

Data source: Federal Energy Regulatory Commission Form 1 database

developed more expensive and more efficient designs, including steam injection.

For comparison, coal plants built in this period generally cost from several hundred dollars per kW to more than $2,000 per kW; the latest vintage coal plants cost as much as $3,000 per kW. Steam plants fired by gas and oil (and not converted from coal) tend to have a wide range of gross plant costs, from the prices of contemporaneous combustion turbines to perhaps twice those costs. Nuclear plants generally have gross plant costs well above $1,000 per kW, up to $8,000 per kW. Combined cycle plants have usually been 20% to 50% more expensive than contemporaneous combustion turbines.[^100]

The capital costs of various types of generating capacity can be compared with the costs of peakers in several ways, including the following:

- Comparing recent or current gross plant costs for other generators with the corresponding cost of peakers, as discussed above.

- Comparing recent or current net plant (gross plant minus accumulated depreciation) costs for nonpeaking generators with the corresponding net plant costs of contemporaneous peakers. This comparison is theoretically the most appropriate basis for classifying generation rate base, which is based on net plant. Unfortunately, net plant is not generally publicly reported by plant or unit, so most cost analysts will have a difficult time implementing this approach. In addition, many utilities have depreciated peakers at a faster rate than steam plants, resulting in lower net plant for a peaker than for a steam plant with the same initial cost, additions and retirements. This results in a higher percentage of the steam plant costs being classified as energy-related based on net plant than gross plant. It is not obvious whether the additional classification to energy is more equitable than the result of the gross plant allocation.

- • Comparing the cost of building the actual mix of generation today with the cost of building a peaking-only system today.[^101] This approach avoids the problem of

[^100]: These cost ratios are provided to explain the importance of identifying the demand-related portion of generation investment . Any application of the equivalent peaker method should compare the costs of the utility’s existing plants to the costs of contemporaneous peakers, using the most

> comparable estimates of the costs of peakers, reflecting geographical and other differences .

[^101]: The peaking-only system might include combustion turbines, demand response and storage resources .

estimating the cost of building peakers at various times in the past. But many existing plants could not be built today as they currently exist — a new coal plant may require scrubbers, nitrogen oxide reduction, closedsystem cooling and other features that the existing coal plant does not have.[^102] Other plant types, such as oil- and gas-fired boiler units, no longer make economic sense and would not be built today. Determining the cost of building a new 1970s-style coal plant or a gas-fired steam plant may be much more difficult than determining the cost of peakers in the 1970s. And for some technologies, the costs of new construction do not meaningfully reflect the costs of the plants currently embedded in rates. For example, as expensive as the nuclear units of the 1980s were, the nuclear units currently under construction are much more expensive. Conversely, the costs of wind turbines have fallen dramatically since the 1980s. Comparing today’s costs for those resources to the costs of new peakers would probably overstate the energyrelated portion of the costs of an old nuclear unit and understate the energy-related portion of the costs of an old wind farm.

Whether the comparison uses gross plant in service, net plant in service or hypothetical new construction, the data sources should be as consistent as possible. It would not be appropriate to compare the current book value of an actual plant with the cost of a hypothetical plant in today’s dollars (Nova Scotia Utility and Review Board, 1995, p. 18).

Table 14 shows the equivalent peaker method analysis that Northern States Power Co.-Minnesota (a subsidiary of Xcel Energy) used in its 2013 rate case filing (Peppin, 2013, Schedule 2, p. 4).[^103] The capacity portion for each plant type is the ratio of the peaking cost ($770 per kW) to the plant type cost. For example, the peaking cost is 20.9% of the cost of the nuclear plant, so 20.9% of the nuclear investment is treated as capacity-related. The company uses its estimates of the replacement costs of each type of generation and applies the results to each capital cost component (gross plant, accumulated depreciation, deferred taxes, etc.).

[^102]: Many hydroelectric projects could not be licensed if they were proposed today .

Table 14. Equivalent peaker method analysis using replacement cost estimates

| Resource type      | Cost<br>per kW | Capacity-<br>related share<br>of cost | Energy-<br>related share<br>of cost |
| ------------------ | -------------- | ------------------------------------- | ----------------------------------- |
| **Peaking**        | $770           | 100%                                  | 0%                                  |
| **Nuclear**        | $3,689         | 20 .9%                                | 79 .1%                              |
| **Fossil***        | $1,976         | 39 .0%                                | 61 .0%                              |
| **Combined cycle** | $1,020         | 75 .4%                                | 24 .6%                              |
| **Hydro**          | $4,519         | 17 .0%                                | 83 .0%                              |

*The “fossil” resource type appears to be coal- or gas-fired steam.

Source: Peppin, M. (2013, November 4). Direct testimony on behalf of Northern States Power Co.-Minnesota. Minnesota Public Utilities Commission Docket No. E002/GR-13-868

This is not a very realistic comparison, for reasons discussed above. Many of the plants could not be built today, and some have complicated histories of retrofits and repowering. The nuclear replacement cost appears to be particularly optimistic compared with the cost of nuclear power plants under construction today.

Table 15 on the next page shows an alternative analysis based on the Xcel Energy Minnesota subsidiary’s actual investments in each plant type at the end of 2017, from Page 402 of its FERC Form 1 report (Federal Energy Regulatory Commission, n.d.).

The results of the two analyses are generally consistent, except for the classification of the combined cycle resources. These plants are of more recent vintage than the others; a fairer comparison, using peaker costs contemporaneous with the in-service dates of each of the other resources, probably would result in a lower energy classification of the combined cycle resources and higher energy classification for the coal and nuclear units.

The equivalent peaker method does have limitations. Perhaps most importantly, it requires cost comparisons of individual generation units with peakers of the same vintage. Utilities installed combustion turbines as far back as the early 1950s, but the technology was widely installed only in the late 1960s. The oldest remaining combustion turbine owned

[^103]: The company calls this a plant stratification analysis .

Table 15. Equivalent peaker method analysis using 2017 gross plant in service

|                        |                   | Plant in ser   | vice           | Excess over combus | tion turbine   |                                 |
| ---------------------- | ----------------- | -------------- | -------------- | ------------------ | -------------- | ------------------------------- |
| Resource type          | Capacity<br>(MWs) | Cost           | Cost<br>per kW | Cost               | Cost<br>per kW | Energy-related<br>share of cost |
| **Combustion turbine** | 1,114             | $291,000,000   | $261           | N/A                | N/A            | 0%                              |
| **Nuclear**            | 1,657             | $3,448,000,000 | $2,081         | $3,016,000,000     | $1,820         | 87%                             |
| **Coal**               | 2,390             | $2,156,000,000 | $902           | $1,532,000,000     | $641           | 71%                             |
| **Combined cycle**     | 1,266             | $939,000,000   | $742           | $609,000,000       | $481           | 65%                             |
| **All resources**      | 6,427             | $6,834,000,000 | $1,063         | $5,157,000,000     | $802           | 75%                             |

Data source: Federal Energy Regulatory Commission Form 1 database records for Northern States Power Co.-Minnesota

by a utility filing cost data (Madison Gas and Electric’s Nine Springs) entered service in 1964. The paucity of earlier data complicates the use of the equivalent peaker method for classifying the costs of older plants. This problem is gradually fading away, as all pre-1970 nuclear is gone and much of the pre-1970 fossil-fueled steam capacity has been retired or is nearing retirement, but the issue remains for classifying hydro plant costs and the few remaining old fossil fuel plants (U.S. Energy Information Administration, 1992).

One solution to the problem of classifying the investment in very old, little-used steam plants is to treat that cost as entirely demand-related. Since these units often represent a very small portion of generation rate base, this solution may be reasonable.

A full equivalent peaker analysis would compare the product of the actual depreciation charges for the nonpeaking plants with the product of the peaker depreciation rate and the peaker-equivalent gross investment for the same reliability contribution. Since the classification of rate base

usually ignores the higher accumulated depreciation of peakers compared with the accumulated depreciation for other generation resources of the same vintage (which tends to overstate the demand-related portion of generation rate base), it is also generally symmetrical to classify generation depreciation expense as proportional to the demand-related portion of gross plant (which will tend to understate the demand-related portion). If classification of one of these cost components is refined to reflect the difference in depreciation rates, the other cost component should be similarly adjusted.

As is true for plant in service, the nonfuel O&M costs of steam plants are generally much higher than the nonfuel O&M costs of combustion turbines. Typical O&M costs per kW-year are $1 to $10 for combustion turbines, $10 to $15 for combined cycle plants, $10 to $20 for oil- and gas-fired steam plants, $40 to $80 for coal plants and more than $100 for nuclear plants. Table 16 shows how the capacity-related O&M for conventional generation might be classified between energy and demand, using the utility’s actual nonfuel O&M

Table 16. Equivalent peaker method classification of nonfuel operations and maintenance costs

|                        |                   | Nonfuel ope  | rations             | Excess o     | ver                 |                                 |
| ---------------------- | ----------------- | ------------ | ------------------- | ------------ | ------------------- | ------------------------------- |
|                        |                   | and mainte   | nance               | combustion   | turbine             |                                 |
| Resource type          | Capacity<br>(MWs) | Cost         | Cost per<br>kW-year | Cost         | Cost per<br>kW-year | Energy-related<br>share of cost |
| **Combustion turbine** | 1,114             | $4,170,000   | $3 .74              | N/A          | N/A                 | 0%                              |
| **Nuclear**            | 1,657             | $215,880,000 | $130 .28            | $209,680,000 | $126 .54            | 97%                             |
| **Coal**               | 2,390             | $33,490,000  | $14 .01             | $24,550,000  | $10 .27             | 73%                             |
| **Combined cycle**     | 1,266             | $16,380,000  | $12 .94             | $11,650,000  | $9 .20              | 71%                             |

Data source: Federal Energy Regulatory Commission Form 1 database records for Northern States Power Co.-Minnesota

costs; the data are 2017 numbers from FERC Form 1, Page 402, for Northern States Power Co.-Minnesota (Federal Energy Regulatory Commission, n.d.).

Table 16 does not include the company’s wind resources, which average about $30 per kW-year in O&M, since MISO credits wind with unforced capacity value at only about 15% of rated capacity, or about 17% of the value of an installed MW of typical conventional generation. The demand-related portion of the wind capacity is thus less than $1 per kW-year, and the wind O&M is almost all energy-related.[^104]

###### Operational Characteristics Methods

The operational characteristics methods classify generation resources (units, resource types, purchases) based on their capacity factors or operating factors. Newfoundland Hydro classifies as energy-related a portion of the cost of each oil-fueled steam plant equal to the plant’s capacity factor (Parmesano, Rankin, Nieto and Irastorza, 2004, p. 22). At first blush, this approach appears to roughly follow the use of the resource, with plants that are used rarely being treated as primarily demand-related and those used in most hours classified as predominantly energy-related. Unfortunately, the use of capacity factor effectively classifies more of the cost to demand as the reliability of the resource declines.

A better approach would be to use the resource’s operating factor, which is the ratio of its output to its equivalent availability (that is, its potential output, if it were used whenever available). This approach would classify any resource that is dispatched whenever it is available (e.g., nuclear, wind and solar) as essentially 100% energy-related. That may be seen as an overstatement, since those resources generally provide some demand-related benefits and are sometimes built to increase generation reliability, as well as to produce energy with little or no fuel cost.

[^104]: The nonfuel O&M costs per kW for Northern States Power’s two small waste-burning plants and its small run-of-river hydro plant are even higher than the nuclear O&M and hence are effectively entirely energy-related, even if the hydro plant provides firm capacity .

[^105]: The Massachusetts Department of Public Utilities explained its preference for this method as follows: “The modified peaker POD results

#### 9.1.3 Joint Classification and Allocation Methods

Although most cost of service studies classify capital investments and capacity-related O&M as either demandrelated or energy-related, classify power and short-term variable costs as energy-related, and then allocate energy-related and demand-related costs in separate steps, two approaches accomplish both at once. These are the probability-of-dispatch (POD) and **decomposition** approaches.

###### Probability of Dispatch

The POD approach is the better of the two.[^105] Methods using this approach are generically referred to as probability of dispatch, even for versions that do not explicitly incorporate probability computations.[^106] A simplified illustrative example of power plant dispatch is shown in Figure 33 on the next page, under the utility load duration curve. The example uses only four types of generation: nuclear, coal, gas combined cycle and a peaking resource consisting of a mix of demand response, storage and combustion turbines. An actual POD analysis might break the generation data down to the plant or even unit level and may need to include load management and demand response as resources. This simplified example also does not illustrate maintenance, forced outages or ramping constraints.

Off-system sales and purchases can be added or subtracted from the load duration curve when they occur, or they can be subtracted or added to the generation available in each hour or period. Similar adjustments may be needed to reflect the charging of storage and operation of behind-themeter generation.

Figure 34 shows the composition of demand in each hour for the same illustrative system, divided among three customer classes. In this example, the residential class peak load occurs when load is high but not near the system peak.

> in a fair allocation of embedded capacity costs because this method recognizes the factors that cause the utility to incur power plant capital costs and because this method allocates to the beneficiaries of fuel savings the capitalized energy costs that produce those savings” (1989, p . 113) .

[^106]: For an example of the POD method, see La Capra (1992) .

Figure 33. Simplified generation dispatch duration illustrative example

7,000<br>Demand response/storage/combustion turbines<br>Combined cycle<br>6,000<br>Coal<br>5,000 Nuclear<br>4,000<br>3,000<br>2,000<br>1,000<br>0<br>1,000 2,000 3,000 4,000 5,000 6,000 7,000 8,000<br>Hour of the year, sorted by load<br>Higher load Lower load<br>This situation might arise for a winter-peaking residential industrial class might peak in the morning, the secondary<br>class in a summer-peaking system, or an evening-peaking commercial class at 1 p.m., and the residential class in the<br>residential class in a midday-peaking system. evening. Large commercial buildings typically experience<br>Note that the three customer classes need not peak at their peak load in the summer, since large buildings require<br>the same time. On a high-load summer day, the primary cooling in most climates. If a large percentage of home<br>Figure 34. Illustrative customer class load in each hour<br>7,000<br>Residential<br>Secondary commercial<br>6,000<br>Primary industrial<br>5,000<br>4,000<br>3,000<br>2,000<br>1,000<br>0<br>1,000 2,000 3,000 4,000 5,000 6,000 7,000 8,000<br>Hour of the year, sorted by load<br>System total megawatts<br>Total megawatts<br>

This situation might arise for a winter-peaking residential class in a summer-peaking system, or an evening-peaking residential class in a midday-peaking system.

Note that the three customer classes need not peak at the same time. On a high-load summer day, the primary

Higher load<br>

Lower load

Table 17. Class share of each generation type under probability-of-dispatch allocation

| Customer class           | Nuclear | Coal<br>Gener | Combined<br>cycle<br>ation source | <br>Peaking<br>resources |
| ------------------------ | ------- | ------------- | --------------------------------- | ------------------------ |
| **Residential**          | 34%     | 34%           | 32%                               | 31%                      |
| **Secondary commercial** | <br>28% | 29%           | 39%                               | 42%                      |
| **Primary industrial**   | 38%     | 37%           | 29%                               | 27%                      |

heating is electric, the residential class is likely to experience its highest load in the winter, even in places like Florida. The industrial class loads may peak in a variety of seasons, driven by vacation and maintenance schedules, variation in inputs (e.g., agricultural products) and demand, and other factors. The system peak may occur at a time different from all of the customer class NCP demands.

Table 17 shows how the costs of each generation resource would be allocated to the classes in the illustrative example in Figure 34. In the lowest-load hours, when nuclear is serving 80% of the energy load, the industrial class uses half the system energy and hence half the nuclear output; in the highest-load hours, when nuclear is serving about 29% of the load, the industrial class uses about 27% of the system energy. Averaged over the year, the industrial class uses 38% of the nuclear output. In the hours that the combustion turbines are running, the industrial class uses only 27% of the peaking resources’ output, since the residential and commercial classes dominate loads in that period.

The commercial class is responsible for the largest share of the summer peak and hence of the combustion turbine costs but the smallest part of the low-load hours and hence the lowest share of the nuclear and coal costs. Every class pays for a share of each type of generation.[^107]

The POD method has been applied with a wide range of detail. The generation “dispatch” over the year may represent historical or forecast operation, equivalent availability or capacity factor, seasonal variation (due to maintenance

[^107]: If this example had included a street lighting class, that class might not have been allocated any combustion turbine costs if the lights would not be on in the summer peak hours . In a more realistic example, including outages of the baseload plants, the combustion turbines probably would operate in some hours with street lighting loads and the lighting class would be allocated some combustion turbine costs .

outages, hydro output, natural gas price, off-system purchases and sales), actual hourly output (reflecting planned and random outages and unit ramping constraints) and other variants. The POD method is thus one approach to hourly allocation. Ideally, dispatch and class loads should use the available data to match costs with usage as realistically as possible.

The POD approach has some limitations. Most importantly, it does not consider the reason that investments were incurred, only the way they are currently used. The costs of an expensive coal plant no longer needed for baseload service and converted to burn natural gas and operating at a 10% capacity factor to meet peak loads might be allocated in exactly the same way as the costs of a much less expensive combustion turbine operating at 10% capacity factor.[^108] The excess costs of the converted coal plant are due to its historical role of providing large amounts of energy at then-attractive fuel costs; those costs were not incurred for the 10% of hours with highest demand. The same considerations arise for other steam plants that operate at much lower capacity factors than they were planned for and justified by. Some hydro plants have also changed operating patterns from their original use, either running for more hours to maintain downstream flow or for fewer hours due to reduced water supply. Peaking capacity is used to provide a range of ancillary services at many load levels, including upward ramping services (when load surges during the day or wind and solar output falls) and operating reserves (especially to back up large generation and transmission facilities). Reflecting these considerations may require modification of the inputs to the POD analysis, which considers only current use, not historical causation.

Second, the POD method spreads the cost of each resource equally to all hours or energy output, assigning the same cost of a totally baseload plant (with a 100% capacity factor) to the lowest-load off-peak hour as to the system peak hour. That approach comports with some concepts of equity and cost responsibility: The cost of each resource is allocated

[^108]: In the simpler forms of POD, the costs of both plants would be spread over the top 10% of hours . In more sophisticated approaches that map generation to actual operating hours, the steam plant would generate in many hours with load lower than the top 10%, while missing some of the top 10%, due to limits on load following .

proportionately to the classes that use it. On the other hand, it can be argued that the hours with higher marginal energy costs contribute more of the rationale for investing in that resource and that, in a sense, each kWh of usage at high-load times should bear more of the resource’s investment-related costs than should each kWh in the off-peak hours. This concern can be addressed by weighting the energy over the hours, such as in proportion to some measure of hourly market price.

Third, it is important that the load and dispatch data be representative of the cost causation or resource usage in the years for which the cost allocation will be in place. For example, a baseload plant may have operated at only 40% capacity factor in the most recent year because of major maintenance or availability of economic energy imports. Or load and dispatch in the last 12 months of data may be atypical because of an extremely cold winter and mild summer. The POD allocation should be based on weathernormalized dispatch and load, just as the rate case costs allowed by the regulator and included in the cost of service study should reflect weather-normalized load.

###### Decomposition

Class obligations for generation costs have occasionally been addressed by dividing the generation resource into separate generation systems serving hypothetical loads for portions of the utility’s customers, such as just the residential customers, just the commercial customers and just the industrial customers. For example, industrial customers in Nova Scotia have argued that their high-load-factor demands could be served by the capacity and energy of some set of baseload plants, where those costs are lower than the average generation cost per kWh (Drazen and Mikkelsen, 2013, pp. 11-16). The industrial advocates for this approach assume that the flat industrial load would be served exclusively by baseload plants and that all other costs should be allocated to other classes.[^109] A similar approach might inappropriately be suggested to justify allocating the highest-cost resources to customers with behind-the-meter solar generation and lower-cost resources to nonsolar customers whose load does not dip in midday. The method might also be used to test

whether classes are paying for enough capacity to cover their energy and reliability requirements.

In the context of resources stacked under a load duration curve, such as that shown in Figure 33 on Page 119, the decomposition approach allocates the resource mix horizontally, rather than the vertical allocation used in the POD method. Figure 35 on the next page illustrates the decomposition approach.

In essence, the decomposition method treats the utility as if it were multiple separate utilities. In the case of Figure 35, the utility system is decomposed into an all-nuclear system with enough capacity to meet the industrial peak load, and a utility with a little nuclear and all the other resources to serve all other load. Whether the industrial customers would support this allocation would usually depend on the cost of the nuclear resources compared with the system average.

The decomposition approach conflicts with reality in many ways, including:

1. The reserve requirements for the decomposed systems would be driven by their noncoincident class peaks or high loads (if they are assumed to be fully free-standing), requiring additional hypothetical capacity for utilities that are not already extensively overbuilt. If the decomposition assumes that the multiple class-specific systems would operate in a power pool, contribution to the system peaks would drive capacity requirements.

2. A system with a high load factor and relatively few large units would require a very high reserve margin (as discussed in Subsection 5.1.1) to cover fixed outages and even maintenance outages. The reserve units would operate in many hours (since the system load would always be near the allocated baseload capacity).

3. A baseload-only system would require a large amount of backup supply energy, either from hypothetical units or as purchases from the other classes.

4. The decomposition approach is usually designed to assign the lowest-cost resources to the industrial class,

[^109]: A decomposition method that accounts for all relevant factors may not show an advantage for industrial customers . In Alberta, a related method to the decomposition method was presented to demonstrate that baseload power for industrial customers would be considerably more expensive than the demand-based cost allocation of the existing system for the industrial class (Marcus, 1987) .

##### Figure 35. Illustration of decomposition approach to allocating resource mix

7,000 Demand response/storage/combustion turbines<br>Combined cycle<br>6,000 Coal<br>Nuclear<br>5,000 Maximum industrial load<br>Industrial load<br>4,000<br>3,000<br>2,000<br>1,000<br>0<br>1,000 2,000 3,000 4,000 5,000 6,000 7,000 8,000<br>Hour of the year, sorted by load<br>Higher load Lower load<br>allocation<br>Other-class generation<br>System total megawatts<br>allocation<br>Industrial generation<br>

shifting all the costs of mistakes and market changes onto the other classes. That includes excess capacity (even excess baseload and capacity made excess by decline in industrial loads), the costs of fuel conversion and the high costs of plants built as baseload but currently operated as peakers.

5. It is not clear how variable renewables and other unconventional resources would be incorporated into the decomposed utility systems.

It is possible (if not certain) that the decomposition approach could be expanded and revised to create a viable classification and allocation method, but at this point no such model has been developed.

#### 9.1.4 Other Technologies and Issues

Several types of generation costs do not fit neatly into the classification methods discussed in the previous sections. Some of those costs, such as hydro resources and purchased power, have been part of utility cost structures since before the development of formal cost of service studies. Others, such as excess capacity and uneconomic investments, became prominent in recent decades. More recently, utilities have

needed to deal with allocating nonhydro renewable costs; a few utilities already have significant costs for nonhydro storage (mostly batteries) and most will need to deal with those costs in the future. As technologies change, new cost allocation challenges will arise — for new resources, repurposed existing assets and newly obsolete resources.

###### Fuel Switching and Pollution Control Costs

Many fuel conversion investments have been undertaken to reduce fuel costs or increase the reliability of fuel supply for high-capacity-factor power plants. This category includes:

- Conversion of oil-fired steam plants to burn coal in the 1970s and 1980s (most of which have since been retired).

- Conversion of gas-fired plants to burn oil in the 1970s, when the supply of gas was limited.

- Conversion of oil-fired plants to co-firing or dual firing with gas since the 1990s to achieve environmental compliance and reduce fuel costs.

- Conversion of coal-fired plants to partial or full operation on gas to achieve environmental compliance.

- Conversion of coal-fired plants to partial or full

operation on biomass to achieve environmental compliance and RPS credit.[^110]

- Conversion of coal-fired plants to partial or full operation on petroleum coke, tire-derived fuel or other waste to reduce fuel costs.

These investments and resulting longer-term operating costs may reasonably be classified as 100% energy-related.

Most pollution control retrofit costs are incurred to comply with regulatory requirements to reduce the environmental effects of fossil-fueled plants and to allow them to continue burning low-cost fuel at high capacity factors. Peaking units that are needed only in a few high-load hours annually can afford to burn expensive clean fuels and are often allowed to have higher emissions rates since they operate so little. Hence, the need for the pollution control is driven primarily by the energy-serving function of the nonpeaking fossil plants. These environmental costs are most often related to emissions standards for air pollutants, but some substantial costs are driven by the need to protect water quality and aquatic life and to meet other health and environmental standards. As a result, the identifiable capital investment and nondispatch O&M costs of pollution controls may reasonably be classified as 100% energy-related or allocated in proportion to class usage of energy during the times that the plant is operated, to recognize the causes of the environmental retrofits.[^111]

###### Excess Capacity and Excess Costs

Utilities sometimes add generation that is not needed to maintain adequate reliability. Some of that excess capacity may result from the lumpiness of generation additions or declining load, with no clear connection to the classification of the additional costs. Other times the excess is the result of the long lead times for certain baseload generation (especially nuclear, but also some coal and hydro facilities), which can result in a plant being completed after the need for its

[^110]: In principle, biomass conversion might also reduce fuel costs, although that is not necessarily the case .

[^111]: Nova Scotia Power uses this adjustment to the average-and-peak approach (Nova Scotia Power, 2013a, p . 37) .

capacity has vanished and the value of its energy output has decreased dramatically. One or both of those outcomes befell many of the nuclear plants and some coal plants in the late 1970s and 1980s. The long lead times are generally the result of choices to build plants to produce large amounts of energy at low variable costs; in those cases, there is a reasonable presumption that the costs of the excess capacity are due to anticipated or actual energy requirements.[^112]

Excess capacity can be priced at the costs of contemporaneous peaking capacity and allocated among classes in proportion to the differences between projected class contribution to peak loads (at the time commitments were undertaken) and actual current class loads. Excess capitalized energy costs (net of equivalent peaking capacity costs and any fuel savings) similarly can be allocated in proportion to the differences between class projected energy requirements and their actual energy requirements.

Table 18 on the next page provides an illustration of the allocation of excess capacity among classes to reflect responsibility for the excess. In this illustration, the actual load in the rate case test year is 600 MWs lower than the load forecast at the time the utility committed to the excess capacity. Because of other adjustments in supply planning, the utility has about 480 MWs of excess capacity, which would support about 400 MWs more load than the actual need. That 400-MW excess is allocated among the classes in proportion to their shortfalls in load.[^113]

This adjusted peak load could be used in allocating peaking resources or the peaking-equivalent portion of all generation resource costs. A similar approach could be applied to allocate the additional costs of having a baseloadheavy resources mix resulting from actual energy use being lower than the forecast usage.

Another source of excess capacity is the addition of clean resources to allow the reduced use of dirty older generation, which thus allows the utility to meet environmental

[^112]: Accounting for a suboptimal system resource mix (and other inefficiencies) is also discussed in detail in Chapter 18 .

[^113]: Any load shortfall due to increased utility efficiency efforts since the commitment to build the capacity should generally be excluded from the shortfall .

##### Table 18. Allocation of 400 MWs excess capacity to reflect load risk

|                          | Forecast<br>load<br>(MWs) | Actual load<br>(MWs) | Load<br>differential | Share of load<br>shortfall | Allocated<br>excess<br>(MWs) | Load for<br>allocation<br>(MWs) |
| ------------------------ | ------------------------- | -------------------- | -------------------- | -------------------------- | ---------------------------- | ------------------------------- |
| **Residential**          | 1,400                     | 1,500                | +100                 | 0%                         | 0                            | 1,500                           |
| **Secondary commercial** | 2,300                     | 2,000                | -300                 | 43%                        | 171                          | 2,171                           |
| **Primary industrial**   | 2,700                     | 2,300                | -400                 | 57%                        | 229                          | 2,529                           |
| **Total**                | 6,400                     | 5,800                | +600                 | 100%                       | 400                          | 6,200                           |

requirements, reduce fuel costs or meet portfolio standards.[^114] Even though these new clean resources may raise the reliability of generation supply (usually above an existing adequate level), their costs were incurred as a result of energy loads; in these cases, the excess capacity should be recognized as energy-related.[^115]

Aside from excess capacity, changing economic, technological and regulatory conditions can result in a facility providing a service different from its original purpose. For example, a previously baseload generation plant may run on only a few days annually or may house a distribution service center. The plant may still have unrecovered capital costs, environmental cleanup obligations or other burdens. If the full cost of the repurposed facility exceeds its value in its new use, the excess costs should be allocated based on its former use as a baseload generating plant.[^116]

Finally, the amortization of a canceled generation plant is attributable to the reason the utility spent the money on

the plant, long before the plant’s costs and benefits were clear. Many nuclear plants were canceled after the utility spent more on the plant than the entire original expected cost, most recently the Summer plant in South Carolina. A number of coal plants were also canceled after the commitment of substantial funds.

###### Hydroelectric Generation

The classification of hydroelectric generation presents some issues that differ from those of thermal generation.[^117] First, many large generation facilities installed prior to 1960 are still in operation, so their costs are difficult to classify using the equivalent peaker method. Most of them could not be built today, given environmental siting constraints, so comparing new construction costs with new peaker costs may not be practical. Second, each conventional hydro facility consists of turbines and dams (and other civil works), which have different and varying effects on the energy and

[^114]: MidAmerican Energy, for example, will have added over 6,000 MWs of wind in the period 2004-2020 to reduce fuel costs to its retail customers but has kept most of its fossil generation in operation (Hammer, 2018) . This could result in a MISO-recognized reserve margin of 26% in unforced capacity terms in certain areas (Hammer, 2018, Table 3) . This is nearly three times the typical MISO-required unforced capacity reserve around 8% (Midcontinent Independent System Operator, 2018, p . 23) .

[^115]: Texas and Iowa established their initial renewable portfolio standards in terms of installed capacity, rather than the more common energy percentage requirement, and several jurisdictions have established targets for specific renewables (e .g ., solar, offshore wind) . See Texas Utilities Code § 39 .904 and Iowa Code Ch . 476 §§ 41-44 . The motivations for these targets, however they are formulated, have been primarily related to reducing fuel costs and emissions . Both Texas and Iowa have exceeded their requirements and continue to add renewables to reduce fuel and other energy costs .

[^116]: Excess costs can also be associated with underutilized or repurposed facilities . For example, a retired steam power plant may be used to warehouse distribution equipment; the generator may be operated as a synchronous condenser to support the transmission system; or a portion of the plant site may remain in service to house a combustion turbine, a transmission switching station or a control center . Sometimes this is intentionally done to avoid (or evade) a rate base disallowance for a unit retired prior to being fully depreciated . Most of those costs continue to be attributable to the original purpose of the steam plant and hence to energy and demand . Similarly, the utility may face cleanup costs for a former coal gasification site or any site contaminated by hazardous materials (e .g ., heavy metals, waste lubricating oil or PCB-contaminated transformer oil) . Regardless of how that site is used today or was most recently used, the cleanup costs are attributable to the activity that generated the contamination, not the current use .

- 117 The treatment of pumped storage, where water is pumped uphill off-peak and released to produce electricity during peak periods, is addressed with other storage technologies in Subsection 9 .1 .4 .

demand values of the facility. Adding a turbine may increase the facility’s capacity at peak load times without increasing energy output, since total energy output is limited by the amount of water flowing in the river. At another hydro facility, adding an additional turbine will not increase the output in periods of peak need (usually summer and winter) because there is not enough water to run the additional turbine, but it may increase energy output in the spring flood; this energy has value, even if it does not contribute to meeting peak load. Adding additional water storage (such as in an upstream reservoir to hold water from the spring flood) may allow the plant to operate longer hours each day but may not increase the contribution in peak hours. Increasing the height of a dam may increase capacity by raising the hydraulic head and also increase energy output because of both the greater head and the increased storage volume.

Hydro is distinct in that the fuel supply (water) is limited, and although the units usually can be dispatched to cover higher-cost hours, doing so precludes using the units at lower-cost hours. Utilities have often recognized this dual function of hydro investments by classifying hydro plant costs to both energy and capacity. For example:

- BC Hydro in British Columbia classifies hydro generation as 45% energy-related (BC Hydro, 2014, p. 9).

- Newfoundland and Labrador Hydro has proposed classification of 80% energy for a new hydro project (Newfoundland and Labrador Hydro, 2018, p. 6).

- Manitoba Hydro has long classified its generation as 100% energy-related, but this was modified in 2016 to an average-and-peak classification approach with a broad peak demand allocation measure (Manitoba Public Utility Board, 2016, pp. 47-53).

Other utilities, including Idaho Power, Hydro-Québec, and Newfoundland and Labrador Hydro, use the averageand-peak approach for legacy hydro.

[^118]: Many of these resources will also operate with little or no flexibility in the spring flood, with minimum flow constraints (which may change by season) and with requirements for flow variation for streambed maintenance, recreational activities, flood control and other factors .

[^119]: Many hydro resources bear the costs of providing services unrelated to electric generation, such as flood control, recreation, water supply

In selecting classification and allocation methods it is important to recognize the usage of each type of hydro resource. Some are run-of-river, with each hour’s output determined by the amount of water flowing through the system. Other hydro resources have limited flexibility in dispatch due to environmental constraints. Both of these categories of hydro resources should be treated as variable, similar to wind and solar.

Other categories of hydro resources have some storage capacity, allowing the operator to optimize dispatch over a day, a week or even a year.[^118] These resources are generally operated under a reliability-constrained economic dispatch regime, but since the variable cost is zero or minimal, they are dispatched to maximize the value of their limited energy supply rather than in merit dispatch order. For example, a hydro resource may be able to generate 100 MWhs in the hour ending at 2 a.m. at no cost, but the dispatcher is likely to prefer to keep the water in the reservoirs to be used for operating reserves, load following and avoidance of fuel costs in higher-cost hours later in the day.

The difference between the dispatch of hydro and thermal resources requires some adaptation in classification and allocation approaches. In some applications of the BIP classification approach, for example, resources are stacked under the load duration curve starting with the resources with the lowest variable costs. In a system with a significant hydro contribution, the method must be modified to reflect the value (not cost) in time periods (ideally hours) in which hydro energy is actually provided, whether that is due to run-of-river, minimum flow or economic dispatch.

It may be appropriate to recognize that some hydro resources are justified primarily by avoiding fuel costs in highload hours, resulting in allocation of the investment-related hydro costs in proportion to some measure of hourly market or marginal energy costs.[^119]

> and environmental protection . Other resources, especially those built in recent decades, may also bear the costs of endangered species protection, conservation easements, access to open space, aesthetic screening around a plant or payments in lieu of taxes . If the non-energy benefits are conditions of a license or permit, those are simply the costs of building or running the plant .

###### Renewable Energy

Renewable energy, generated from wind, solar, biomass, hydro, geothermal and other technologies, is becoming a larger part of the electric supply mix and hence the cost allocation challenge. Renewable resources may have very different cost characteristics than conventional resources, and the decision to invest in them may be driven by policy that may not consider peak demand at all.

As discussed in Subsection 7.1.2, renewable energy may be added — even though the utility does not need the capacity at peak hours — to reduce fuel costs, comply with portfolio requirements (which often require that a specified percentage of energy consumption is supplied by renewable generation) or meet environmental targets, particularly reducing the atmospheric effects of fossil energy generation. This substitution of capital investment for fuel is widely accepted as an important approach in 21st century utility planning, as shown in examples from Colorado, Iowa and Indiana.[^120]

In the classification of costs between capacity and energy, renewable costs that are driven by energy consumption, either directly or indirectly, should be classified as energyrelated. For renewable resources that provide some demandrelated benefits, the costs can be classified between demand and energy based on the equivalent peaker, average-and-peak or other methods, as long as the demand-related portion is discounted to reflect the effective load-carrying capacity of the renewable resource. Variable renewable resources fit well in a time-based allocation (such as a detailed POD allocation) because their costs can be allocated directly to the hours in which they provide energy to the system.

###### Purchased Power

Many power purchase agreements with utilities or nonutility generators (especially fossil-fueled generation) have been structured with two types of charges: predetermined monthly charges the utility must pay regardless of how

[^120]: Xcel Energy touted its renewable energy investments as “steel for fuel,” in which “capital recovery costs [are] offset by lower fuel and O&M costs” and wind “displaces coal and natural gas fuel,” resulting in “significant customer savings” (2018) . MidAmerican Energy justified its aggressive wind generation plan on eliminating exposure to fossil fuel costs (Hammer, 2018) . Northern Indiana Public Service Co . found that replacing its coal plants’ fuel and operating costs with wind and solar would reduce customer costs, uncertainty and risk (2018, p . 6) .

much energy it takes from the power producer, as long as the supplier meets contracted requirements for availability; and variable charges per MWh that the buyer pays for the energy it takes. The charges may reflect the projected cost of a single unit or plant (traditionally fossil fueled, increasingly renewable) at the time the contract was signed, or the actual cost of service for a unit or a portfolio of resources.

Another large set of power purchase agreements — including PURPA contracts, some dating back to the 1980s, and most 21st century renewable projects — pay the provider a rate per kWh delivered (perhaps with different rates by time of delivery). This cost structure fits well into an hourly allocation framework, although it is also possible to extract a demand component of the resource’s value for inclusion in a traditional demand/energy framework.

Many utilities classify the monthly guaranteed portion of payments to independent power producers as demand-related, using the archaic perspective that any generation cost that is committed for the rate year should be considered fixed and therefore demand-related, thus leading to great controversy in choosing the appropriate basis for allocation of demand-related costs. In reality, the utility may have agreed to the payment structure because of the low-cost energy provided by the deal, with that financial commitment having value to the resource owner in obtaining financing.

Others classify purchased power to mimic the classification of generation plant, as if the purchase were the equivalent of plant capital, without fuel.[^121] This treatment is similarly inconsistent with cost causation. Many power purchase agreements are structured to recover the costs of a baseload or intermediate resource, such as by charging a relatively high nonbypassable capacity charge and a low energy charge based on the usage of the resource. These contracts are typically not the lowest-cost way to meet peak loads. The only rational reason to enter into these contracts

[^121]: The contract may require the purchaser to take all of the available energy, so even a rate denominated in MWhs can be thought of as investmentrelated and thus similar to generation plant costs . In reality, the purchase contract replaces both the investment-related and variable costs of a comparable resource built by the purchasing utility .

would be to access lower-priced energy and higher efficiency. The classification process should look beyond the contract pricing terms to ascertain the true cost causation factors and where the benefits accrue.

Within the centrally dispatched power pools (such as the New England, New York, California and Midcontinent ISOs), utilities and other load-serving entities purchase energy on an hourly basis to meet their loads. The transactions are priced at the marginal costs of the supply bids to the system operator and cover some investment-related costs for most generators. The cost of those purchases should be classified as energy and allocated to loads on a time-differentiated basis.[^122]

Costs for purchased power can be classified in most of the same ways that the costs of utility-owned generation are classified, including the probability-of-dispatch, equivalent peaker and average-and-peak methods and many others. In many cases, the purchase will be from a specific plant whose investment and nondispatch O&M costs can be allocated in the same manner as the costs of similar resources the utility owns. In other cases, such as system power, the classification and allocation of power purchase costs will need to be based on the cost characteristics of the purchase.[^123] Where possible, the most straightforward classification approach would be to treat as energy-related the excess of the purchase costs over the capacity costs of a contemporaneous gas turbine peaking plant.

###### Energy Storage

Energy storage takes many forms, including:

- Water held in conventional hydro reservoirs.

- Pumped storage hydro facilities.

- A variety of battery technologies, which may be co-located with generation, transmission or distribution facilities or be behind the customer’s meter.

- A host of other electricity storage technologies, including

[^122]: Some utilities in these pools own generation, which is sold into the regional market . The revenue from those sales can be credited against the costs of the generator before those costs are allocated to classes .

[^123]: Since costs for purchased power may be recovered through both base rates and a power cost recovery mechanism, and the allocation of these costs may be reflected in both base rates and the power-cost mechanism, some care should be taken to ensure that the allocation is applied only once, just as the costs are recovered only once . For example, the costs for purchased power may be included in the cost of service study, with the anticipated purchased-power revenues from each class subtracted from

compressed air, flywheels and gravity (moving weights upward to store energy, using the potential energy to drive a generator as needed).

- Thermal storage as molten salt in solar thermal plants, ice or hot water at customer premises.

Batteries will be an increasingly important part of utility systems, and therefore of cost allocation studies, because of their flexibility and the rapid and continuing decline in their costs. Batteries can be installed (1) at the location of generation to stabilize or optimize output to the transmission system; (2) at substations to avoid transmission and distribution costs; or (3) throughout the system, on the utility or customer side of the meter to avoid transmission and distribution costs and to provide customer emergency power.

Batteries can provide a range of services, including contributing to bulk supply reliability, ancillary services (load following, reserves and automatic generator control), energy arbitrage, transmission load relief, distribution load relief and customer emergency supply. To the extent that the allocation study can reflect these various services, it should classify the costs of the batteries in proportion to their value. That classification may be based on the frequency with which the storage is used for each purpose, on the anticipated mix of benefits that justified the installation, or on the incremental cost incurred to achieve the additional purpose.[^124] Batteries may be very valuable for providing second-contingency support to the transmission system (avoiding the installation of redundant equipment), even if they may never actually be dispatched for that purpose. Where utilities purchase some attributes of behind-the meter batteries, such as ancillary services, the services they purchase should drive the cost allocation.

Storage operates as both a load and a supply resource and thus may operate at very different times than conventional generation. As a result, storage fits well into hourly allocation

> the allocated costs . Alternatively, the purchase costs may be excluded from the base rate cost of service study and allocated separately on an appropriate basis in the fuel and purchased power cost recovery mechanism .

[^124]: Renewable incentives and tax policy may encourage co-location of storage with centralized renewable generation . Moving the storage to support transmission, distribution or customer resilience would typically increase both the value and the cost of the resource; those incremental costs should be classified as due to the incremental service .

schemes. Storage usually delivers power into the grid at high-cost hours, so assigning the capital and operating costs, including the costs of charging storage, to those hours usually will result in an equitable tracking of costs to benefits.

But storage also provides some services while it is charging, including operating reserves. A 200-MW pumped storage unit can typically transition from being a 200-MW pumping load to a 200-MW supply within minutes, providing 400 MWs of net operating reserves at no incremental cost during low-cost hours, allowing avoidance of fuel costs for load-following resources. Storage may also provide other ancillary services while charging. If the cost of service study is sophisticated enough to classify and allocate ancillary services separately from demand and energy, some of the storage costs can be classified to ancillary service, reflecting the increased reserves available during charging.

In addition, some utility systems experience high ramp rates in net load at times that variable renewable generation is declining and load is rising, such as an evening-peaking utility with a large amount of solar generation in the midday period. To be able to ramp up output from other generation quickly enough to offset the drop in renewable output and meet the rising load, the system may require the construction of additional resources and the uneconomic operation of thermal generators at low-load times to ensure they are available when the ramping need arises. Storage-charging load in the period of minimum net load (which is also likely to be a period of low or even negative short-run marginal costs) raises the minimum load and reduces the ramp rate. These benefits flow to the loads during the ramping period, not just during the discharge period, so some of the costs of storage should be allocated to those loads.

###### System Control and Dispatch

The costs of scheduling, committing and dispatching generation units, recorded in FERC Account 556, are fixed in the short term but vary with the generation mix, load shapes and variability and other considerations. Costs of forecasting

[^125]: One possible complication with time differentiation is that some steam plants must be operated in low-load hours, when they are not really needed, so that they will be available when needed in higher-load hours . The costs of fuel and reagents used in low-load hours may be required to

load and supply and optimizing dispatch may vary depending on the amount of weather-related load, the existence of large loads and large generators that may suddenly trip off line, the extent of integration with other utilities, the length of time required for major plants to start up and the amount of variable renewable generation. Some dispatch costs would be required, even if the utility only needed to dispatch generation on a few peak hours, while others are required for multiday planning, 24-hour operation and other energyrelated factors.

These costs might most reasonably be classified as partly demand-related and partly energy-related. Reasonable approaches would include classification of dispatch costs in proportion to the classification of long-term generation costs, using the average-and-peak method or a 50/50 split between energy and demand.

#### 9.1.5 Summary of Generation Classification Options

Table 19 on the next page summarizes some attributes of the generation classification options described above. These descriptions are highly simplified and should be read in context of the discussion prior, including the discussion of special situations in Subsection 9.1.4.

### 9.2 Allocating Energy-Related Generation Costs

Energy-classified generation costs are often allocated to all classes in proportion to total annual class energy consumption. Alternatively, energy-related costs can be calculated by time period and allocated to classes in proportion to their usage in each time period. Assigning costs to time periods is usually straightforward for fuel and dispatch O&M.[^125] For systems with high penetration of variable renewables, such as wind and solar, then TOU or BIP allocation of energy-related costs is the most equitable.

The energy-related capital investment and nondispatch O&M costs can be allocated to classes in proportion to

> serve high-load hours, but the plants may also be supplying energy in the low-load hours; sorting out generation and fuel use among periods within a week or day can be very complicated .

Table 19. Attributes of generation classification options

| Method                                                                                            | Data and<br>computational<br>intensity | Accuracy<br>of cost<br>causality | Allows joint<br>classification/<br>allocation | Applicability                                                                          |
| ------------------------------------------------------------------------------------------------- | -------------------------------------- | -------------------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Straight fixed/variable**                                                                       | Very low                               | Very low                         | No                                            | Peaker-only systems                                                                    |
| **Competitive proxy**                                                                             | Low                                    | Medium                           | No                                            | In or near regional transmission<br>organizations that perform<br>revenue computations |
| **Average and peak**                                                                              | Low                                    | Low                              | No                                            | Hydro systems                                                                          |
| **Simple base-intermediate-peak**                                                                 | Low to medium                          | Medium                           | No                                            | Simple systems: limited hydro,<br>solar, wind, storage                                 |
| **Complex base-intermediate-peak**                                                                | High                                   | High                             | Yes                                           | Broad                                                                                  |
| **Equivalent peaker (peak credit)**                                                               | Low                                    | High                             | No                                            | Broad                                                                                  |
| **Operational characteristics**<br>**(capacity value, capacity factor,**<br>**operating factor)** | Generally low                          | Low to medium                    | No                                            | Limited                                                                                |
| **Probability of dispatch**                                                                       | Medium to high                         | Highest                          | Yes                                           | Broad                                                                                  |
| **Decomposition**                                                                                 | Very high                              | Low                              | Yes                                           | Rarely                                                                                 |

energy or assigned among time periods in proportion to the fuel and dispatch O&M. Table 20 provides an illustration of the development of energy-classified costs per MWh (both dispatch- and investment-related) over three time periods.

Table 21 on the next page shows an illustrative example applying these costs per MWh to usage for three customer classes by time period to allocate costs.

The comparable computation for most utilities could use

many more periods (perhaps even hourly data), include all resource types and compute usage by generation unit, rather than category.

Manitoba Hydro, which has an almost all-hydro system, assigns energy-classified capital investment costs among four seasons and three time periods (for a total of 12 periods) in proportion to the MISO market prices for exports in those periods, reflecting the reality that there are hours in which

Table 20. Illustrative example of energy-classified cost per MWh by time of use

|                           |                                |                   | Pe           | riod (and annual ho | urs)                |              |
| ------------------------- | ------------------------------ | ----------------- | ------------ | ------------------- | ------------------- | ------------ |
|                           | Energy-related<br>cost per MWh | Capacity<br>(MWs) | Peak<br>(50) | Midpeak<br>(2,000)  | Off-peak<br>(6,710) | Total        |
| **Resource type**         |                                |                   |              |                     |                     |              |
| Nuclear                   | $30                            | 500               | $750,000     | $28,500,000         | $90,585,000         | $119,835,000 |
| Coal                      | $40                            | 1,500             | $3,000,000   | $84,000,000         | $161,040,000        | $248,040,000 |
| Combined cycle            | $35                            | 1,000             | $1,750,000   | $35,000,000         | $0                  | $36,750,000  |
| Peaking                   | $100                           | 300               | $1,500,000   | $12,000,000         | $0                  | $13,500,000  |
| Demand response           | $250                           | 100               | $1,250,000   | $0                  | $0                  | $1,250,000   |
| Subtotal of all resources |                                |                   | $8,250,000   | $159,500,000        | $251,625,000        | $419,375,000 |
| **Consumption (MWhs)**    |                                |                   | 170,000      | 4,170,000           | 7,045,500           | 11,385,500   |
| **Cost per MWh**          |                                |                   | $48 .53      | $38 .25             | $35 .71             | $36 .83      |

Note: Numbers may not add up to total because of rounding. The illustration assumes that all resources are fully utilized in the peak period, with reductions in capacity factor between periods by 5 percentage points for nuclear, 30 points for coal, 50 points for combined cycle and 80 for peaking.

Table 21. Illustrative example of time-of-use allocation of energy-classified costs

|                        | Peak<br>(50) | Midpeak<br>(2,000)<br>Period (an | Off-peak<br>(6,710)<br>d annual hours) | Total        |
| ---------------------- | ------------ | -------------------------------- | -------------------------------------- | ------------ |
| **Consumption (MWhs)** | 170,000      | 4,170,000                        | 7,045,500                              | 11,385,500   |
| **Cost per MWh**       | $48 .53      | $38 .25                          | $35 .71                                | $36 .83      |
| **Class**              |              |                                  |                                        |              |
| Residential            |              |                                  |                                        |              |
| Consumption (MWhs)     | 69,250       | 2,080,000                        | 2,818,200                              | 4,967,450    |
| Allocated costs        | $3,360,662   | $79,558,753                      | $100,650,000                           | $183,569,415 |
| Commercial             |              |                                  |                                        |              |
| Consumption (MWhs)     | 85,000       | 1,460,000                        | 2,113,650                              | 3,658,650    |
| Allocated costs        | $4,125,000   | $55,844,125                      | $75,487,500                            | $135,456,625 |
| Industrial             |              |                                  |                                        |              |
| Consumption (MWhs)     | 15,750       | 630,000                          | 2,113,650                              | 2,759,400    |
| Allocated costs        | $764,338     | $24,097,122                      | $75,487,500                            | $100,348,961 |

Note: Numbers may not add up to total because of rounding.

transmission constraints preclude additional exports. That approach recognizes that using energy in some time periods is more expensive for Manitoba Hydro (in terms of lost export revenues) than consumption in other time periods.

- The class contributions to three or four seasonal peaks (3 CP or 4 CP).

- The average of the class contributions to multiple highload hours, such as:

  - The 12 monthly peaks (12 CP).

### 9.3 Allocating Demand-Related Generation Costs

As discussed in Subsection 9.1.3, some classification methodologies, such as probability of dispatch and more granular hourly variants, simultaneously develop cost by period and the associated allocation factors driven by use by period. This section describes methods for developing allocation factors for demand-related costs developed by legacy demand/energy classification methods.

Typically, utilities allocate demand-related generation based on some form of class contribution to system peak loads, referred to as coincident peak. The loads that determine how much capacity a utility requires may be concentrated in a few hours a year, a few hours in each month, the highest 50 or 100 hours in the year, or some other measure of the loads stressing system reliability.

Frequently used demand allocators include:

- The class contributions to the annual system coincident peak (1 CP).

- All hours with loads greater than a threshold, such as 80% to 95% of annual peak.

- **Peak capacity allocation factor** (PCAF), a technique developed in California that weights high-usage hours based on how close each hour is to the peak hour.

- Hours with some expectation for loss of energy.

- Hours in which the system is stressed

  - (e.g., operating reserves are below target levels).

As discussed in Chapter 5, generation capacity requirements have always been driven by more than a few hourly loads. Moreover, with peak loads being offset by solar generation and expanding demand response available to serve the highest-load or highest-cost hours, capacity requirements are driven by an even broader group of hours, which should be reflected in the development of the demand allocation factors. Broader allocation factors also have the virtue of limiting the instability resulting from the use of a limited number of peak hours. For example, ERCOT experienced an annual peak in 2017 at approximately

69,500 MWs on July 28 at 5 p.m. However, there were 13 other hours within 2% of that annual peak in 2017, in the hours ending at 3 p.m. to 7 p.m. (Electric Reliability Council of Texas, 2018, and calculations by the authors). Changes in temperature or cloud cover could shift the peak load to any of those hours. The peak timing in the load data can be very important in determining the allocators. The residential class typically will have a greater share of a peak load occurring at 7 p.m. than one occurring at 3 p.m. or 4 p.m.[^126]

Utilities have sometimes allocated generation demand costs on the class NCP at the system level.[^127] This approach may have been roughly appropriate for some utilities serving distinct classes with peak demands in different seasons, such as winter-peaking ski resorts and summer-peaking irrigation pumping, with both seasons contributing to the need for generation capacity. The class NCP would not recognize whatever load the ski resorts’ summer operations contribute to the pumping-dominated peaks and would allocate demand costs to other classes based on their summer or winter peaks — but not their contributions to either of the seasons’ high-load hours. Since reliability computations and the need for generation capacity are driven by combined system load, some measure of the combined loads on the system is relevant. With the hourly data collection technologies now available, this class NCP approximation is no longer necessary.

Traditionally, without access to the kind of sophisticated hourly data we can obtain today, utilities have tended to allocate demand costs on a single annual coincident peak,

[^126]: The range of loads in these 14 hours was only about 1,400 MWs, roughly the size of one large nuclear unit or two large coal units . The differences in loads over those hours are of little significance in terms of reliability .

[^127]: In some jurisdictions, the class NCP is referred to as the maximum class peak, maximum diversified demand or something similar, and “NCP” is used to designate the sum of the individual customer noncoincident peaks within each class . We refer to class NCP and customer NCP in this manual to distinguish between the two methods .

the average of the four monthly peaks in the high-load summer season, the average of some number of summer and winter monthly peaks, a defined number of peak hours when peaking resources are expected to operate, or the average of the 12 monthly peaks.[^128] The number of months included in the computations of the demand allocator often reflects the following factors:

- The number of months in which the system may experience its annual peak load.

- Whether high loads occur in both summer and the winter.

- Whether requirements for maintenance outages reduce available capacity in off-peak months enough that available reserves in those months are comparable to the reserves in the peak months.

A more comprehensive approach to these factors would develop the demand allocator from all the hours identified in a loss-of-energy expectation study, after accounting for maintenance scheduling. Depending on the system, that may be several hours or several hundred hours. If data are not available for a comprehensive loss-of-energy expectation analysis, a demand allocator based on all hours within a specified percentage of the peak (e.g., 80% to 95%) or based on a significant number of the highest hours in the year (e.g., 100) is preferable to a coincident peak analysis. In sum, averaging or weighting a small number of coincident peaks incorrectly assumes that the need for capacity is a simple function of the amount of the system monthly peak, even though capacity requirements are driven by many hours,

[^128]: FERC has a set of guidelines for determining whether wholesale demandclassified costs should be allocated on 3 CPs or 12 CPs (for example, see Federal Energy Regulatory Commission, 2008, pp . 30-35) . FERC’s approach does not contemplate that any other number of months (such as four or eight) might be responsible for the need for capacity .

Table 22. Attributes of generation demand allocation options

| Method                                                    | Data and<br>computational<br>intensity | Accuracy<br>of cost<br>causality | Allows joint<br>classification/<br>allocation | Applicability                                                                                          |
| --------------------------------------------------------- | -------------------------------------- | -------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **1 CP**                                                  | Very low                               | Very low                         | No                                            | Rare                                                                                                   |
| **3 CP; 4 CP**                                            | Low                                    | Low                              | No                                            | One-season peak; needle peaks                                                                          |
| **12 CP**                                                 | Low                                    | Low to medium                    | No                                            | Multiple seasonal peaks; extensive<br>maintenance requirements; class load<br>shapes near peak similar |
| **Multiple hours near peak**<br>**(e.g., top 100 hours)** | Low to medium                          | Medium                           | No                                            | Broad, but loss-of-energy expectation<br>gives more robust results if<br>data exist to calculate them  |
| **Loss-of-energy expectation**                            | High                                   | High                             | No                                            | Broad                                                                                                  |
| **Complex base-intermediate-peak**                        | High                                   | High                             | Yes                                           | Broad                                                                                                  |
| **Probability of dispatch**                               | Medium to high                         | High                             | Yes                                           | Broad                                                                                                  |

depending on load; the amount of generation capacity that is available, not just installed; and the scheduling of maintenance outages.

Table 22 summarizes some characteristics of the allocation methods described in this section, along with the POD method described in Subsection 9.1.3 and the more complex variants of the BIP method from Subsection 9.1.2.

### 9.4 Summary of Generation Allocation Methods and Illustrative Examples

As demonstrated in many ways in the previous sections, it is appropriate to classify some of the long-term investment and

O&M costs to energy usage rather than to demand. Table 23 presents a simplified view of appropriate classification results by plant type.

As variable renewable capacity (mostly wind and solar) on a system increases, the role for baseload capacity decreases. At some point, in hours with low load and high renewable output, traditional baseload resources will run only if they cannot shut down and restart on a timely basis.

Cost of service studies can also combine features of the various classification approaches, such as classifying peakers as 100% demand-related; classifying fuel conversion costs, environmental costs and generation without firm transmission as 100% energy-related; and applying the average-and-peak

Table 23. Summary of conceptual generation classification by technology

| Resource type                                                                   | Function                       | Classification                     |
| ------------------------------------------------------------------------------- | ------------------------------ | ---------------------------------- |
| **Nuclear, some hydro and best coal**                                           | Baseload                       | Primarily energy                   |
| **Modern combined cycle, best gas-fired steam and**<br>**mediocre coal**        | Intermediate                   | Energy and demand                  |
| **Combustion turbines, mediocre fossil-fueled steam**<br>**and combined cycle** | Peaking and operating reserves | Primarily demand or on-peak energy |
| **Storage and flexible hydro**                                                  | Peaking and energy shifting    | Demand or on-peak energy           |
| **Wind and solar**                                                              | Energy and some capacity       | Primarily energy                   |

Note: “Best” refers to resources with the lowest variable costs, “mediocre” to those with higher variable costs. Resources that are worse than mediocre are likely candidates for retirement. “Intermediate” refers to generation that is neither baseload nor peaking.

Table 24. Summary of generation allocation approaches

|                     |                                                                                              | Classification and allocation methods                                                                             | i                                                           |
| ------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Resource type       | Legacy                                                                                       | Modern                                                                                                            | Evolving                                                    |
| **Nuclear**         | Classification:Average and peak<br>Energy allocator:All energy<br>Demand allocator:12 CP     | Classification:Equivalent peaker<br>Energy allocator:All energy<br>Demand allocator:Loss-of-energy<br>expectation | All hours                                                   |
| **Baseload coal**   | Classification:Average and peak<br>Energy allocator:All energy<br>Demand allocator:12 CP     | Probability of dispatch                                                                                           | Hours dispatched                                            |
| **Combined cycle**  | Classification:Average and peak<br>Energy allocator:All energy<br>Demand allocator:12 CP     | Probability of dispatch                                                                                           | Hours dispatched or used for reserve                        |
| **Gas-fired steam** | Classification:Average and peak<br>Energy allocator:On-peak energy<br>Demand allocator:4 CP* | Probability of dispatch                                                                                           | Hours dispatched or used for reserve                        |
| **Peaker**          | Classification:100% demand<br>Demand allocator:4 CP or 12 CP                                 | Probability of dispatch                                                                                           | Hours dispatched or used for reserve                        |
| **Hydro**           | Classification:Average and peak<br>Energy allocator:All energy<br>Demand allocator:12 CP*    | Probability of dispatch                                                                                           | Hours dispatched or used for reserve                        |
| **Wind**            | Classification:100% energy<br>Energy allocator:All energy                                    | Classification:Equivalent peaker<br>Energy allocator:All energy<br>Demand allocator:Loss-of-energy<br>expectation | Hours of output                                             |
| **Solar**           | Classification:Average and peak<br>Energy allocator:On-peak energy<br>Demand allocator:4 CP  | Classification:Equivalent peaker<br>Energy allocator:All energy<br>Demand allocator:Loss-of-energy<br>expectation | Hours of output                                             |
| **Storage**         | Classification:Average and peak<br>Energy allocator:All energy<br>Demand allocator:12 CP     | Probability of dispatch                                                                                           | Hours dispatched, used for reserve<br>or reducing ramp rate |
| **Demand response** | Classification:100% demand<br>Demand allocator:3 CP to 12 CP**                               | Classification:100% demand<br>Demand allocator:3 CP to 12 CP**                                                    | Hours dispatched or used for reserve                        |

- Depends on use of resource

** Depends on program type and technology

approach to the remaining costs. A hybrid approach is only as equitable as the component techniques but may be useful where particular classification decisions can be made before the application of a generic approach to the residual costs. Table 24 summarizes examples of allocation factors

that might be applied to the capital and nondispatch O&M costs for various types of generation resources, whether utility-owned or purchased.[^129] This summary is, by its very nature, highly simplified, ignoring many of the complexities discussed in sections 9.1, 9.2 and 9.3.

129 The probability-of- dispatch and hourly approaches can also be applied to the short-run variable costs of the resources .

For simplicity, we show an illustration only for generation investment-related costs. Table 25 shows the amount of investment in each category, which we will then divide using multiple allocation methods.

Table 26 shows two currently used methods: a legacy 1 CP system measure and a more modern method, equivalent peaker, where 80% of baseload costs are considered to be energy-related. The illustrative load data and allocation factors are from tables 5 through 7 in Chapter 5.

Table 27 shows the calculation of an hourly allocation model, where baseload costs are apportioned to all hours, peaking and intermediate costs to midpeak hours, and storage only to the 2% of usage at the most extreme hours.

Table 25. Illustrative annual generation data

|                                              | Net<br>generation<br>(MWhs)      | Annual<br>nonfuel<br>revenue<br>requirement | Annual<br>nonfuel cost<br>per MWh |
| -------------------------------------------- | -------------------------------- | ------------------------------------------- | --------------------------------- |
| **Baseload**                                 | 1,860,000                        | $74,400,000                                 | $40                               |
| **Peaker**                                   | 534,000                          | $42,720,000                                 | $80                               |
| **Solar**                                    | 1,056,000                        | $31,680,000                                 | $30                               |
| **Storage**                                  | 62,000                           | $6,200,000                                  | $100                              |
| **Total**                                    | 3,512,000                        | $155,000,000                                | $44                               |
|                                              | Disposition<br>of net generation |                                             |                                   |
| **Storage input and**<br>**delivery losses** | 412,000                          |                                             |                                   |
| **Sales to customers**                       | 3,100,000                        |                                             |                                   |

Note: Numbers may not add up to total because of rounding.

Table 26. Allocation of generation capacity costs by traditional methods

|                       | Residential | Secondary<br>commercial | Primary<br>industrial | Street<br>lighting | Total        |
| --------------------- | ----------- | ----------------------- | --------------------- | ------------------ | ------------ |
| **1 CP (legacy)**     | $51,667,000 | $62,000,000             | $41,333,000           | $0                 | $155,000,000 |
| **Equivalent peaker** | $50,333,000 | $52,400,000             | $47,750,000           | $4,517,000         | $155,000,000 |

Note: Numbers may not add up to total because of rounding.

Table 27. Modern hourly allocation of generation capacity costs

|                             | Residential | Secondary<br>commercial | Primary<br>industrial | Street<br>lighting | Total        |
| --------------------------- | ----------- | ----------------------- | --------------------- | ------------------ | ------------ |
| **Baseload (all hours)**    | $24,000,000 | $24,000,000             | $24,000,000           | $2,400,000         | $74,400,000  |
| **Peaker (midpeak)**        | $14,424,000 | $15,735,000             | $12,326,000           | $236,000           | $42,720,000  |
| **Solar (daytime)**         | $10,560,000 | $12,320,000             | $8,800,000            | $0                 | $31,680,000  |
| **Storage (critical peak)** | $2,366,000  | $2,366,000              | $1,420,000            | $47,000            | $6,200,000   |
| **Total hourly allocation** | $51,350,000 | $54,421,000             | $46,545,000           | $2,683,000         | $155,000,000 |
| **Composite hourly factor** | 33%         | 35%                     | 30%                   | 2%                 | 100%         |

Note: Numbers may not add up to total because of rounding.
