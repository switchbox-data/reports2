## 17. Future of Embedded Cost Allocation

hange is inevitable as the electric industry adapts to new technology. Part III of this manual, on **C** embedded cost of service studies, has attempted to address many common situations the cost analyst will face in determining an equitable allocation of costs among customer classes. But new technologies and changing loads will dictate new issues and perhaps new methods.

Historically, power has flowed from central generators, through transmission, to primary distribution and then secondary distribution. Customers served at the transmission level have not paid for distribution, and those served at primary have not paid for line transformers or secondary lines. This situation is beginning to change. In some places, the development of distributed solar capacity already causes power to flow from secondary to primary and even onto the transmission system. At some point, all customers may receive service through all levels of the delivery system, requiring a substantial rethinking of the allocation of distribution costs.

In addition to the increased complexity of system operations, utilities have more data about system operations and

customer loads than they had a few decades ago. As the costs of electronics decline, more data will become available to more utilities. Thus, methods that were the best available in the 1980s can now (or soon) be superseded by more accurate and realistic allocations. Computations that would have been unwieldy on the computers of the 1980s are trivial today.

For example, as utilities acquire data on the hourly load of each class, many costs can be allocated on an hourly basis, rather than on such summary values as annual energy use and contribution to a few peak load hours. The costs of baseload generation resources (nuclear, biomass, geothermal) may be assigned to all hours; costs of wind and solar resources to the hours they provide service; storage to the hours in which it exports energy and provides other benefits;[^206] and demand response costs to the hours these resources are deployed or the hours in which they reduce costs by supplying operating reserves. In a sense, this is an evolution and refinement of the base-intermediate-peak traditional method, described in Section 9.1.

To illustrate this approach, Figure 45 provides a day’s

Figure 45. Daily dispatch for illustrative hourly allocation example

2,500<br>Peaker Storage<br>Solar Charging of storage<br>2,000 Base<br>1,500<br>1,000<br>500<br>0<br>-500<br>1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24<br>Hour of day<br>Megawatts<br>

206 Among other things, charging storage in hours with low net loads will raise minimum load levels and reduce ramp rates, benefiting the hours in which net load rises rapidly .

##### Figure 46. Class loads for illustrative hourly allocation example

2,500<br>Street lighting<br>Industrial<br>Commercial<br>2,000<br>Residential<br>1,500<br>1,000<br>500<br>0<br>1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24<br>Megawatts<br>

Hour of day

worth of hourly dispatch of four resources: a baseload resource (perhaps nuclear), solar, a peaker (perhaps a combustion turbine) and storage (both as charging load below the axis and generation above the line). In this example, the storage charges from excess base capacity in the early morning and then from solar, and discharges in the evening to replace the waning solar. The actual application of hourly allocation would include 8,760 hours from an actual or typical year, with a wide range of load levels, availability of the base resource and solar output patterns.

Figure 46 provides hourly energy requirements by class (including losses) for the same day as in Figure 45.

Table 39 on the next page provides two types of data from Figure 45 and Figure 46: each class’s share of the load in each hour, and the portion of each resource’s daily generation that occurs in the hour.

The generation cost allocation for a class would be:

Where Lh = class share of load in hour _h_

Sr,h = share of resource _r_ output that occurred in hour _h_

for the day)

Table 40 shows the result of this computation for the data in Table 39. The lighting class, for example, would pay for 1.8% of the base resource, 2.2% of the peakers and just 0.6% of the solar. Table 40 also shows each class’s share of total load, for reference.

Table 39. Hourly class load share and resource output

| Hour          | Residential | Commercial<br>Class shar | e of load<br>Industrial | Street<br>lighting | Reso<br>Base | urce output: Perce<br>Peaking | ntage occurring<br>Solar | by hour<br>Storage |
| ------------- | ----------- | ------------------------ | ----------------------- | ------------------ | ------------ | ----------------------------- | ------------------------ | ------------------ |
| **1**         | 39 .0%      | 35 .3%                   | 22 .5%                  | 3 .2%              | 4%           | 0%                            | 0%                       | 0%                 |
| **2**         | 37 .0%      | 36 .2%                   | 23 .5%                  | 3 .3%              | 4%           | 0%                            | 0%                       | 0%                 |
| **3**         | 36 .4%      | 36 .7%                   | 23 .5%                  | 3 .4%              | 4%           | 0%                            | 0%                       | 0%                 |
| **4**         | 36 .7%      | 37 .0%                   | 23 .1%                  | 3 .3%              | 4%           | 0%                            | 0%                       | 0%                 |
| **5**         | 37 .5%      | 36 .6%                   | 22 .7%                  | 3 .2%              | 4%           | 0%                            | 0%                       | 0%                 |
| **6**         | 38 .4%      | 37 .2%                   | 21 .4%                  | 3 .0%              | 4%           | 0%                            | 3%                       | 0%                 |
| **7**         | 39 .7%      | 37 .1%                   | 20 .6%                  | 2 .6%              | 4%           | 0%                            | 8%                       | 0%                 |
| **8**         | 39 .8%      | 39 .2%                   | 19 .5%                  | 1 .6%              | 4%           | 0%                            | 9%                       | 0%                 |
| **9**         | 38 .8%      | 42 .6%                   | 18 .4%                  | 0 .2%              | 4%           | 0%                            | 9%                       | 0%                 |
| **10**        | 36 .7%      | 44 .8%                   | 18 .2%                  | 0 .2%              | 4%           | 0%                            | 8%                       | 0%                 |
| **11**        | 36 .6%      | 45 .1%                   | 18 .1%                  | 0 .2%              | 4%           | 0%                            | 11%                      | 0%                 |
| **12**        | 35 .9%      | 45 .8%                   | 18 .1%                  | 0 .2%              | 4%           | 0%                            | 10%                      | 0%                 |
| **13**        | 36 .7%      | 44 .8%                   | 18 .3%                  | 0 .2%              | 4%           | 0%                            | 7%                       | 1%                 |
| **14**        | 37 .5%      | 44 .0%                   | 18 .2%                  | 0 .2%              | 4%           | 0%                            | 13%                      | 0%                 |
| **15**        | 36 .3%      | 44 .7%                   | 18 .8%                  | 0 .2%              | 4%           | 0%                            | 12%                      | 0%                 |
| **16**        | 37 .4%      | 43 .5%                   | 18 .8%                  | 0 .2%              | 4%           | 0%                            | 7%                       | 0%                 |
| **17**        | 41 .5%      | 40 .6%                   | 17 .4%                  | 0 .4%              | 4%           | 5%                            | 1%                       | 25%                |
| **18**        | 44 .7%      | 37 .3%                   | 16 .1%                  | 2 .0%              | 4%           | 13%                           | 0%                       | 25%                |
| **19**        | 45 .2%      | 35 .8%                   | 16 .8%                  | 2 .2%              | 4%           | 13%                           | 0%                       | 18%                |
| **20**        | 44 .2%      | 36 .1%                   | 17 .4%                  | 2 .3%              | 4%           | 15%                           | 0%                       | 12%                |
| **21**        | 44 .4%      | 35 .4%                   | 17 .8%                  | 2 .3%              | 4%           | 15%                           | 0%                       | 10%                |
| **22**        | 45 .9%      | 33 .8%                   | 17 .9%                  | 2 .4%              | 4%           | 19%                           | 0%                       | 5%                 |
| **23**        | 42 .8%      | 35 .1%                   | 19 .4%                  | 2 .6%              | 4%           | 12%                           | 0%                       | 1%                 |
| **24**        | 41 .6%      | 35 .5%                   | 20 .1%                  | 2 .8%              | 4%           | 6%                            | 0%                       | 3%                 |
| **All hours** | 39 .7%      | 39 .6%                   | 19 .1%                  | 1 .6%              | 100%         | 100%                          | 100%                     | 100%               |

Note: Percentages may not add up to 100 because of rounding.

##### Table 40. Class shares of resource cost responsibilities and load

|                                      | Residential | Secondary<br>commercial | Primary<br>industrial | Street<br>lighting |
| ------------------------------------ | ----------- | ----------------------- | --------------------- | ------------------ |
| **Resource type**                    | .           | .                       | .                     | .                  |
| Base                                 | 39 .6%      | 39 .2%                  | 19 .4%                | 1 .8%              |
| Peaker                               | 44 .3%      | 35 .8%                  | 17 .7%                | 2 .2%              |
| Solar                                | 37 .5%      | 43 .1%                  | 18 .7%                | 0 .6%              |
| Storage                              | 43 .8%      | 37 .4%                  | 17 .2%                | 1 .7%              |
| **Class share**<br>**of total load** | 39 .7%      | 39 .6%                  | 19 .1%                | 1 .6%              |
