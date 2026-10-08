## Chapter 10: Marginal Transmission, Distribution and Customer Costs

In contrast to marginal production costing methodology, analysts have devoted little attention to developing methodologies for costing marginal transmission, distribution and customer costs. An early evaluation noted: "... the determination of marginal costs for these functions, and especially distribution and customer costs, is much more difficult and less precise than for power supply, and it is not clear that the benefits are sufficient to justify the effort."[^10-1] The referenced study, therefore, used average embedded costs, because they were both more familiar to ratemakers and analysts, and a reasonable approximation to the marginal costs. It is still common for analysts to use some variation of a projected embedded methodology for these elements, rather than a strictly marginal approach. While marginal cost concepts have been applied to transmission and distribution for the purpose of investigating wheeling rates, little of this analysis has found its way into the cost studies performed for retail ratemaking. The basic research into marginal costing methodologies for transmission, distribution and customer costs for retail rates was done in connection with the 1979-1981 NARUC Electric Utility Rate Design Study and most current work and testimony still refer back to those results.

[^10-1]: W. Wilson, _Report for the Rhode Island Division of Public Utilities, Public Utilities Commission and Governor's Energy Office_ (1978), pp. B-27-8.

### I. Transmission

There are several basic approaches to the calculation of the marginal cost of transmission. However, the first step in any approach is the definition of the study period. Transmission investments are "lumpy" in that they usually occur in large amounts at intervals. Therefore, it is important to select a study horizon that is long enough to reflect the relationship between investments and load growth. To the extent that investments are related to load growth occurring outside the study period or there is a significant change in the level of system reliability, the analyst may wish to adjust the calculation of the load growth to identify the investment more closely with the load it is intended to serve. Given the desirability of a fairly long study period, analysts will typically select the utility's entire planning period augmented by historical data to the extent that the analyst believes that the historical relationships will continue to obtain in the future.

For purposes of a marginal cost study, investment in the transmission system is generally assumed to be driven by increments in system peak load. As the transmission system was actually constructed for a variety of reasons, the second step in the calculation of the marginal cost of transmission is to identify and eliminate those investments that are not related to load growth. The non-demand related transmission investments can be categorized as:

1. Those related to remote siting of generation units (which are costed as part of the generation cost).
2. Those related to system interconnections and pool requirements (whose benefits are manifested in reduced reserve requirements and, therefore, are again costed with generation).
3. Those associated with large loads of individuals (which are therefore charged to the particular customer concerned).
4. Replacement of existing facilities without adding capacity to serve additional load (assuming that the economic carrying charge formula incorporates an infinite series factor).

Costs that remain should be related only to system load growth or to maintenance of system reliability.

#### A. Costing Methodologies

There are two basic approaches to estimating marginal transmission costs, and they begin to diverge at this step in their methodology. The first approach is the **Projected Embedded Analyses** of which there are two variations: the **Functional Subtraction** approach, which relates total transmission investment additions to load growth, and the **Engineering** approach, which relates individual facilities (line miles, transformers, etc.) to load growth. The second methodology is the **System Planning** approach, which uses a base case/decrement analysis.

**1. Projected Embedded Analyses**

As the name suggests, Projected Embedded Analyses are often based on a simple projection of past costs and practices into the future. A disadvantage of this approach is that it may fail to capture important technological and business related developments and therefore result in the over or underestimation of marginal capacity cost.

_Functional Subtraction Approach_

The Functional Subtraction approach requires data in the form of annual load related investments in transmission and load growth for the same period. The period to be analyzed includes the transmission planner's planning period plus whatever historical period he believes appropriate. Transmission cost data must be sufficiently specific to enable the analyst to differentiate load growth related transmission expenditures from those more properly associated with either generation or a specific customer. Having chosen the study period and identified the load related investments in transmission by voltage level, the analyst performs the analysis in real dollars. This is done by converting the historical nominal data to current money values by applying either the Handy-Whitman plant costs indices or, if available, an inflation index particular to the utility. Projected investments are converted to real dollars by removing the inflation factor used by the planner in his computations.

The third step is to relate the real transmission investments to a measure of load growth at each voltage level; weather normalized if possible, stated in kilowatts. Non-coincident peak demand on the transmission system is the correct measure of load growth. However, given the system's integrated nature, for most purposes non-coincident peak demand on the transmission system is the same as the total system coincident peak.

The relationship between investment and load growth ($/KW) is usually obtained by simply dividing the sum of investments for the period by the growth in peak load. There have been some attempts at regressing annual investments against load growth, using the equation $\text{Transmission Costs} = a + b \times (\text{peak demand})$, but the $R^2$'s have been disappointingly low. However, given the assumption that transmission investments are "lumpy" and that one particular year's investment is not specifically related to that year's load growth, the lack of correlation should not be surprising. The best regression results are achieved by using least squares and regressing cumulative incremental investment against cumulative incremental load. Thus, the first year observation is the first year value of incremental investment and load, the second year observation is the sum of the first year and the second year values, the third year is the sum of the values for the first three years, and so on. See Table 10-1.

[TABLE DESCRIPTION: Table 10-1 — Computation of Marginal Demand Cost of Transmission: Transmission-Related Additions to Plant Per Added Kilowatt of Transmission System Peak Demand (Functional Subtraction Approach).

The table has four columns: (1) Year, (2) Growth Related Net Addition (1988 $M), (3) Cumulative Net Addition (1988 $M), (4) Growth In System Peak, and Cumulative System Peak. Data spans from 1976 through 1990, with partially readable values including years 1979 (147.9), 1981 (214.9, cumulative 322.7), 1982 (134.2, cumulative 454.3, peak 1685), 1986 (188.6, cumulative 791.2), 1987 (cumulative 862.6), 1989 (cumulative 1124.7, peak 5265), and 1990 (128.7, cumulative 1250.4, peak 5672). Most individual year data is garbled in the OCR.

The table concludes with two summary calculations:

**Simplified Approach:**
Marginal Transmission Investment Costs = Column 1 Total / Column 3 Total = $220.45/KW

**Regression Approach:**
Marginal Transmission Investment Costs = $249.40/KW
$Y = A + B \times X$
Where $Y$ is cumulative demand-related net additions to plant and $X$ is cumulative additions to coincident peak demand.
$A = -326.59$, $B = 0.2494$, $R^2 = 0.84$.]

[→ See original PDF page 146 for full data]

The fourth step is to convert the per kilowatt investment cost into an annualized transmission capacity cost by multiplying the former by a carrying charge rate. There are two forms in common use, the economic carrying charge and the standard annuity formula. During a period of zero inflation the two methods produce the same results, but during inflationary periods only the former takes due account of the impact of inflation on the value of plant assets.[^10-2]

[^10-2]: See Appendix 9-A for the derivation of the economic carrying charge.

Since the addition of transmission capacity occasions increased operation and maintenance expenses, the marginal O&M costs are calculated and added to the annualized transmission capacity costs. The expense per KW is usually found to be fairly constant and either the current year's expense or the average of the $/KW in current dollars over the historical portion of the study period is considered to be a good approximation of the marginal transmission operation and maintenance expense. The analyst takes the data from the FERC Form 1, again being careful to include only those costs related to load growth. For example, he may exclude rents or that portion of expenses related to load dispatching associated with generation trade-offs. Total transmission O&M expenses in current dollars are divided by system peak demand, and averaged if multiple years have been used. The result, either for the single current year or the average of several years, is then added to the annualized transmission capacity cost to obtain the total transmission marginal cost. Alternatively, O&M expenses can be regressed on load growth or transmission investments, in which case the O&M adjustment appears as a multiplier to the capacity cost rather than an adder.

The final step is to adjust the results for transmission's share of indirect costs including the marginal effect on general plant and working capital. See Table 10-2.

[TABLE DESCRIPTION: Table 10-2 — Computation of Marginal Demand Costs of Transmission (1988 $).

This table summarizes the annualization of transmission investment costs into a total marginal demand cost of transmission. The first row references the change in load from Table 10-1. The table applies the economic carrying charge, adds O&M expenses, adjusts for general plant loading, and applies loss adjustments to arrive at a total annual marginal cost per KW. The detailed numerical entries are largely unreadable in the OCR.]

[→ See original PDF page 147 for full data]

_Engineering Approach_

Like Functional Subtraction, the Engineering approach also relates changes in transmission investment to changes in system peak load. However, it first relates the addition of specific facilities (line miles, transformers, etc.) to growth in load over the chosen study period, and then computes the unit costs of each facility to derive the investment for transmission per added kilowatt of demand. The method has the advantage of more readily identifying those facilities added for the purpose of serving added load (and thereby excluding non-load related investment). It may be more difficult to apply, however, as it requires detailed records and distinctions that may come more easily to the utility company planner than to the outside observer.

Once the study period is selected, the analyst identifies the load growth related facilities that were or will be added each year at each voltage level. By either regression analysis or simple averages, the addition of facilities is related to the growth in coincident system peak. The result is expressed in line miles, transformers, etc. per added KW and monetized by applying a cost figure for each facility in real dollars. As with Functional Subtraction, the investment per added demand is annualized by a levelized carrying charge, or, more properly, an economic carrying charge (consistent with calculations for the other capacity components) and added to the associated annual operation and maintenance costs. The costs per KW for each facility are then totaled at each voltage level and adjusted for indirect costs.

**2. The System Planning Approach**

The System Planning approach is more nearly related to the marginal costing methodologies for generation than is the Projected Embedded approach. As such, it may be helpful to review what is meant by marginal capacity cost. The marginal cost of transmission or distribution capacity can be defined as the present worth of all costs, present and future, as they would be with a demand increment (decrement), less what they would be without the increment (decrement). This definition of marginal cost can be represented by a time-stream of discounted annual difference costs stretching to infinity. The stream of investments from this approach would be annualized by using an economic carrying charge.

Alternatively, the marginal capacity cost can be interpreted as the cost to the utility of bringing forward (delaying) by one year its future investments, including the stream of replacement investments, to meet the demand increment (decrement). Mathematically, this interpretation results in annual charges equal to the economic carrying charge on the marginal investments.

In order to simplify the calculation of marginal capacity cost it is common for the stream of difference costs to be truncated after a set number of years, usually the utility's planning period or the average economic life of the investments. However, if the period chosen is too short, truncation can result in serious underestimation of marginal capacity cost. In terms of the second definition this would be equivalent to neglecting the impact of the increment (decrement) on more distant investments. Truncating a component of the economic carrying charge as discussed in Appendix 9-A will mitigate some of those effects.

The System Planning approach is an application of the first incremental/decremental definition of marginal capacity cost and therefore the analyst should take care not to base his calculations on an unreasonably short planning horizon.

In contrast to the projected embedded studies for transmission cost, which may use some historical data, the study period for the system approach is forward-looking. As with the other methodologies, the relevant costs are those related to changes in load, and coincident system peak is the basic cost causation factor. The data required is thus the planner's base case of expected load growth and transmission investments, plus an incremental (decremental) case for the same period.

Planned transmission costs, investment and expenses, are identified and the marginal cost quantified by developing a differential time series of expenditures over the planning horizon using an increment or decrement to system peak load. A base case expansion plan is developed using the forecasted load over the future planning horizon. Investments are separated by voltage level where the utility has customers who take service directly from the high voltage lines. Those investments associated with load growth are identified and the total annual revenue requirements (including expense items) are derived in real or nominal dollars for each year at each voltage level.

The system planner is then asked to assume an increase or decrease in the coincident peak load and redesign transmission expenditures, still maintaining system reliability and continuing to meet the system planning criteria, and repeat the costing procedure. Thus, the marginal transmission capacity cost is the change in total costs associated with changes to budgeted transmission expenditures between the planner's base case and his incremental (decremental) case. The dollar stream representing the difference between the two cases is present worthed, aggregated and then annualized over the costing horizon. The resultant annualized figure is then divided by the amount of the increment (decrement) to obtain a $/KW marginal cost for transmission for each voltage level. The size of the increment (decrement) may vary according to the size of the utility and will certainly affect the result. A 50 MW change is often chosen as the smallest (most marginal) change that can be assumed and produce measurable differentiated cases.

**3. Adjustments**

_Loss Adjustment_

Electric utility transmission and distribution systems are not capable of delivering to customers all of the electricity produced at the generation bus bar. The difference between the amount of electricity generated and the amount actually delivered to customers is called "losses".

Losses can be broadly classified as copper losses, core losses and dielectric losses. They are caused, respectively, by the production of heat, the establishment of magnetic fields and the leakage of current. The first of these varies in proportion to the square of the current and is therefore included under marginal energy costs. The latter two are fixed losses associated with specific equipment and therefore covered by marginal capacity costs.

Marginal capacity loss factors are applied to marginal capacity-related costs per kilowatt. These factors account for the fact that when a customer demands an additional kilowatt at the meter, more than a kilowatt of distribution, transmission and generation capacity must be added.

_Energy Adjustment_

While most analysts assume that transmission is causally related to system peak and therefore is totally demand related, it has been argued, particularly in the literature concerning wheeling rates, that transmission embodies an energy component as well. For very small changes in load, transmission and generation are substitutes: additional generation can overcome the line losses in the transmission system, or extra transmission capacity can, by reducing losses, substitute for added generation. Thus, conceptually, it is proper to net out the energy savings from the marginal investment cost of transmission, leaving the residual to be demand related. There is no accepted methodology for quantifying this adjustment. One approach is to obtain a calculation of the energy loss/potential savings in $/period by multiplying the cost of 1 KW for each costing period times the energy loss in that period. Summing across the periods produces, in total dollars per kilowatt-year, the avoidable loss/potential savings. As some of this loss occurs at the generation level, it is appropriate to net out the portion of energy loss due to generation. The remainder is net energy savings in $/KW year attributable to increased transmission capacity that can then be capitalized into a $/KW computation.

#### B. Allocation of Costs to Time Periods

The attribution of marginal demand-related costs by time of use reflects the system planner's response to the goal of maintaining a target level of reliability in the generation, transmission and distribution components of the system. Thus, as the load varies according to time periods, so does the need to add capacity to maintain reliability.

System planners evaluate generation, transmission and distribution components separately for their reliability, and ideally the transmission capacity cost responsibility would reflect the planner's sensitivity to such factors as the likelihood of weather related service disruptions. For costing purposes, however, most analysts use the same methodologies, and often the same attribution factors, for transmission as they do for generation. The reasoning is that in general the load characteristics of the transmission system are identical to those of the generation system, both being driven by the system coincident peak. Therefore, it is not considered necessary to perform transmission specific load studies as the results of such studies should not differ significantly from those of the generation load studies. To the extent that the transmission and generation load characteristics do differ, the methodology discussed under "Distribution" can be employed.

The methods employed include attributing the costs uniformly across the peak period, or by means of transmission reliability indices or loss of load probability (LOLP). However, where the LOLP data are heavily influenced by seasonal generation availability (e.g., hydro facilities) or generation maintenance schedules, the generation LOLP factors are not a good measure of the need to add transmission capacity.

None of the generation-tied allocation methods recognize the seasonal variation in the capability of transmission facilities. Transmission facilities have a lower carrying capability when ambient temperatures are high (i.e., summer). Therefore, winter peaking utilities and summer peaking utilities with significant winter peaks need some method for adjusting seasonal assignment factors if they are going to rely on generation related costing allocators for transmission.

### II. Distribution

#### A. Costing Methodologies

The major issue in establishing the marginal cost of the distribution system is the determination of what portion of the costs, if any, should be classified as customer related rather than demand and energy related. The issue is a carry-over of the unresolved argument in embedded cost studies with the added query of whether the distribution costs usually identified as customer related are, in fact, marginal.

Most analysts agree that distribution equipment that is uniquely dedicated to individual customers or specific customer classes can be classified as customer rather than demand related. Customer premises equipment (meters and service drops) are generally functionalized as customer rather than distribution costs and, in reality, this is the only equipment that is directly assignable for all customers, even the smallest ones. Beyond the customers' premises, however, there are distribution costs that may be classified as customer related. For example, some jurisdictions classify line transformers as customer-related often using a proxy based on average load as the allocation factor when this equipment is not uniquely dedicated to individual customers. In addition, for very large customers, more than merely meters, services, and transformers are directly assignable. Some have entire substations dedicated to them. As noted above in "Transmission," distribution costs of equipment dedicated to individual customers can be directly assigned to them, thus reducing the common distribution costs assigned to the remainder of the class.

The major debate over the classification of the distribution system, however, concerns the jointly used equipment rather than the dedicated equipment. At the margin, there is symmetry between the cost of adding one customer and the cost avoided when losing one customer. A number of analysts have argued, and commissions have accepted, that the customer component of the distribution system should only include those features of the secondary distribution system located on the customer's own property. Portions of the distribution system that serve more than one customer cannot be avoided should one customer cancel service. Similarly, if the customer component of the marginal distribution cost is described as the cost of adding a customer, but no energy flows to the system, there is no reason to add to the distribution lines that serve customers collectively or to increase the optimal investment in the lines that are carrying the combined load of all customers. Therefore, the marginal customer cost of the jointly used distribution system is zero.

Those analysts who believe that there is a significant customer component to the marginal cost of the jointly used portion of the distribution system argue that the distribution system is causally related to increases in both the number of customers and the kilowatts of demand. (They may also note that distribution costs are influenced by the concentration of such non-demand, non-customer factors as load, geographic terrain, climatic conditions and local zoning ordinances. However, no analyst has attempted to introduce and quantify these elements in a marginal cost of service study and absent area-specific rates depending on density and distance from load centers, there is no reason to do so.) Because of the non-interconnected character of the distribution system, the relevant demand parameter is non-coincident peak, preferably measured at the individual substation or even at lower voltages, rather than the system peak used for generation and transmission. This reflects the fact that each portion of the distribution network must be planned to serve the maximum load occurring on it and the utility's investment reflects the need to provide capacity to each separate load center. As some customers receive service directly from the primary distribution system, calculations must be performed separately for the different voltage levels.

The measured relationship for each voltage level is expressed by the equation:

$$\text{Total Distribution Cost} = a + b \times \text{demand on distribution} + c \times \text{customers}$$

The statistical difficulty with this equation is that the demand is highly correlated with the number of customers (multicollinearity) and that therefore it is not possible to identify the separate marginal effects of changes in demand and customers on cost. The proposed estimation techniques resolve the statistical dilemma by computing the customer responsibility separately and then relating the residual cost to load growth. To the extent that the distribution system is sized in part to reduce energy losses, an energy component must also be netted out of marginal cost in order to obtain the demand component.

The two most common approaches to calculate the customer related component in marginal as well as embedded studies are the **zero intercept method** and the **minimum grid calculation**. The zero intercept method re-defines the original equation to read:

$$\text{Total Distribution Cost} = a + b \times \text{demand on distribution}$$

It solves the multicollinearity problem by eliminating the customer variable under the hypothesis that the constant "$a$" will then represent the non-variable, non-demand related portion of the costs, or the distribution facilities required when demand is zero. The method has been accused of "solving" the problem of multicollinearity by mis-specifying the equation. Statistically, removing a correlated variable (customers) from the equation will result in transferring some of the responsibility of the omitted variable to the coefficient of the remaining variable (demand). Application of the technique does not necessarily lead to results that make economic sense: negative constant terms are not uncommon. The approach is somewhat more successful when used to analyze cross-sectional data where the correlation is weaker or when applied to individual items of distribution equipment.

The **minimum grid** approach re-designs the distribution system to determine the cost in current year dollars of a hypothetical system that would serve all customers with voltage but not power (or with minimum demand of 0.5 KW), yet still satisfy the minimum standards for pole height and efficient conductor and transformer size. The calculations can be based either on the system as a whole or on a sample of areas reflecting different geographical, service and customer density characteristics.

When applying this approach, it is necessary to take care that the minimum size equipment being analyzed is, in fact, the minimum-sized equipment available, and not merely the minimum size stocked by or usually installed by the company. To the degree that the equipment being costed is larger than a true minimum, the minimum grid calculation will include costs more properly allocated to demand.

Figure 10-1 illustrates the results of the minimum grid approach for the marginal customer-related cost for a typical residential customer of the sample utility. In column 1 (Customer Specific Equipment) only line transformers, service and meters are functionalized to the customer category while all other distribution equipment is functionalized to the demand category. In column 2 (Minimum Distribution Method) all distribution equipment is first estimated at minimum size and functionalized as customer-related. The additional cost of equipment, sized to meet actual expected loads is functionalized as demand-related. For comparison, column 3 reflects the reconstruction cost for the as-built system. In the sample company, the minimum grid approach to determining the marginal customer-related cost of connecting an average customer produces a customer charge equal to 43 percent of costs of the distribution system (14 percent plus 29 percent) compared to the charge resulting from the alternative T-S-M approach, i.e., restricted to meter, service, line transformer and associated costs, which is only 28 percent of the distribution system costs.

[DIAGRAM DESCRIPTION: Figure 10-1 — Distribution Costs, Minimum Grid Approach.

A three-column bar chart comparing distribution cost allocations for a typical residential customer of the sample utility. Each column represents a different functionalization methodology, with costs shown in billions of dollars and broken into customer-related and demand-related components:

- **Column 1 — Customer Specific Equipment (T-S-M):** Only line transformers, service drops, and meters are functionalized as customer costs (28% of total distribution costs). All remaining distribution equipment is classified as demand-related.

- **Column 2 — Minimum Distribution Method (Minimum Grid):** All distribution equipment is first estimated at minimum size and classified as customer-related (43% of total: 14% from minimum-sized lines and substations, plus 29% from customer-specific equipment). The incremental cost above minimum size is classified as demand-related (57%).

- **Column 3 — Reconstruction Cost:** Shows the full reconstruction cost of the as-built distribution system for comparison, representing the total cost that is split between customer and demand components under the two methods.

The chart demonstrates that the minimum grid approach assigns a substantially larger share of distribution costs to the customer category (43%) than the customer-specific-equipment approach (28%).]

[→ See original PDF page 155]

The marginal demand related distribution costs are calculated in a manner similar to the marginal demand related transmission costs. The major differences are that, if considered appropriate, the marginal customer costs must be removed from the total costs incurred during the study period, and that the relevant load growth is non-coincident peak.

Removal of customer costs can be done in two ways. The cost of the minimum grid can be divided by the number of customers served to obtain a cost per customer to be included in the customer charge. The cost per customer at each voltage level can be multiplied by the number of customers added at each voltage level during the study period, and the sum subtracted from the total distribution investment in current year dollars. This residual is then considered the demand (or demand and energy) component of the marginal cost. Alternatively, the marginal customer costs can be removed by using a factor based on the ratio of investment in the minimum distribution grid to the investment in the total distribution system, calculated over the historical period. In the example, the customer related portion of the distribution system is 43 percent leaving a demand related portion of 57 percent. See Table 10-3, Column k footnote.

[TABLE DESCRIPTION: Table 10-3A — Demand Related Marginal Costs of Distribution: Minimum Grid Methodology.

A multi-column table spanning years 1976 through approximately 1990, with columns for: Year, Lines, T-M-S (Transformers-Meters-Service), Lines (replacement), Total Replacements, New Business Lines, Substations, TOTAL, Handy-Whitman Index, Reflated Additions, Demand Related Portion (cumulative), Non-Coincident Peak Load Additions (cumulative). The demand-related portion is derived by multiplying total reflated additions by 57% (since 43% is customer-related under the minimum grid methodology, derived from the average ratio of the minimum distribution system cost to total distribution system costs calculated in study workpapers).

The table concludes with regression results:
$Y = A + B \times X$
Where $Y$ is cumulative demand-related net additions to plant and $X$ is cumulative additions to distribution level peak demand.
$A = -134.608$
**Marginal demand costs of distribution = $159.13/KW**

Table footnotes:
(a) from study workpapers
(b) from study workpapers
(c) a + b
(d) from study workpapers: total replacements (repl.) portion of Lines and T-M-S
(e) c - d
(f) from study workpapers
(g) from study workpapers
(h) e + f + g
(i) Handy Whitman index
(j) h × i (reflated)
(k) j × 57% (43% customer related derived from the average ratio of the minimum distribution system cost to total distribution system costs calculated in study workpapers)
(l) cumulates k
(m) cumulates peak load additions in study workpapers]

[→ See original PDF page 156 for full data]

[TABLE DESCRIPTION: Table 10-3B — Demand Related Marginal Cost of Distribution: Customer Specific Equipment Methodology.

A multi-column table with the same structure and time period as Table 10-3A, but using the Customer Specific Equipment methodology instead of the Minimum Grid methodology. Columns include: Year, Lines, Lines (replacement), New Business Lines, Land, Substations, TOTAL, Handy-Whitman Index, Reflated Additions, Cumulative Demand Portion, Cumulative Non-Coincident Peak Load.

The table concludes with regression results:
$Y = A + B \times X$
Where $Y$ is cumulative demand-related net additions to plant and $X$ is cumulative additions to distribution level peak demand.
$A = -222.003$
$B = 0.203536$
**Marginal demand costs of distribution = $203.54/KW**

Table footnotes:
(a) from study workpapers
(b) from study workpapers
(c) a - b
(d) from study workpapers
(e) from study workpapers
(f) c + d + e
(g) Handy Whitman Index
(h) f × g
(i) cumulative h
(j) cumulative peak load additions in study workpapers]

[→ See original PDF page 157 for full data]

The functional subtraction method, in which it is possible to remove all non-demand related costs including the minimum grid, provides the most straightforward calculation. An analyst who employs the engineering method would have to determine individually for each facility which portion of the facility or the investment was incurred to serve customers and what proportion was incurred to serve demand. In both cases, the capacity costs are annualized and adjusted for operation and maintenance costs and for indirect costs. Absent special operation and maintenance studies, it is reasonable to divide O&M costs between customer and demand components on the assumption that they are proportional to the split in the distribution investment. Again, as in the transmission calculation, further adjustments can also be made to account for the losses and the energy component of the distribution cost using the methods outlined above. See Table 10-4.

**Table 10-4: Demand Related Marginal Cost of Distribution — Minimum Grid vs. Customer Specific Equipment Methodologies (1988 $)**

| Description                                                               | Minimum Grid ($/KW) | Customer Specific Equipment ($/KW) |
| ------------------------------------------------------------------------- | ------------------- | ---------------------------------- |
| Distribution Investment per KW change in Load (From Tables 10-3A & 10-3B) | 159.13              | 203.54                             |
| Annual Cost (× 13.08%)                                                    | 20.82               | 26.62                              |
| Demand Related O&M Expense                                                | —                   | —                                  |
| General Plant Loading                                                     | —                   | —                                  |
| Total Annual Costs of Distribution/KW                                     | 27.67               | 37.28                              |
| Loss Adjustment (1.107%)                                                  | 30.63               | 41.27                              |

#### B. Non-Coincident Peak Demand

To calculate the marginal demand related distribution cost for a particular customer class, the analyst needs to determine, using available load data, the increase in peak demand on the distribution system due to a 1 KW increase in the maximum demand of the class. The peak demand on the distribution system is referred to as the **non-coincident peak demand**.

Unfortunately, most load research studies have tended to focus on the structure of class demands at the generation and at the customer levels and, therefore, very little is known about the demands on the mid-stream components of the transmission and distribution systems. Consequently, analysts have resorted to various simplifying assumptions in order to determine transmission and distribution system non-coincident peaks. For power systems which depend for the most part on their own resources, it is often assumed that the class composition of the transmission system non-coincident peak demand is identical to the composition of the coincident peak demand at the generation level. This assumption may need to be amended for power systems with important interconnections with other systems.

Unlike the transmission system, however, secondary distribution systems are designed to meet load growth in particular localities. This means, of course, that the non-coincident peak on any portion of the secondary system reflects the combined load of the customers served from it. Because of zoning and land use regulations, load on any particular portion of the secondary system will generally be dominated by either residential or commercial customers. (Industrial customers are more likely to be served directly from the primary distribution system.) This suggests that a close relationship exists between an increase in the maximum demand of the residential or commercial class and the increase in the secondary non-coincident peak (i.e., coincident factor close to unity) for any particular locality. Where customer classes served from the secondary distribution system are mixed this result needs to be amended to take account of the diversity between the classes. As the residential class far out-numbers the commercial class on most systems, the secondary distribution system as a whole will be primarily responsive to residential loads.

Logically, the class demand at the time of peak on the primary distribution system must lie between the previously determined transmission and secondary distribution class demands and it is common to take the statistical average of the two demands.

Most analysts assume that the customer related marginal distribution costs do not vary by season or by time of day.

The method adopted to attribute marginal demand related distribution costs depends on the load characteristics of the distribution network. When distribution system components experience maximum demand during the peak costing period identified in the generation analysis, the allocation methods employed for generation (uniform allocation across peak period, probability of excess demand, loss of load probability), and sometimes simply the generation allocation factors themselves, can be used to attribute distribution costs to time periods. As noted above in the discussion on the allocation of transmission costs, if the generation allocators are used it may be necessary to adjust for the effect of the ambient temperature on line capacity and, therefore, on the seasonal allocation of costs. Load research at the distribution substation transformer level has indicated in a number of jurisdictions, however, that different segments of the distribution network peak at different times in the day and year, and are not closely related to the system peak. Those jurisdictions may find it more appropriate to adopt an equal allocation of distribution capacity costs or to allocate costs based on either the proportions of the number of substations that peak during the individual costing periods, or by relating the amount of distribution investment to the timing of the peak demand where the investment was made.

### III. Customer Costs

Marginal customer costs in the functionalization step of a marginal cost of service study are generally identified as those facilities and services that are specific to individual customers. These costs include the costs of the service drops, the costs of meters and metering and the customer accounts expenses. These costs are assumed to vary solely according to the number of customers on the utility's system, and are, therefore, classified 100 percent customer related as well. Jointly used facilities such as line transformers and interconnecting secondary conductors that have been functionalized as distribution costs and that the analyst may have classified as customer related, have been discussed above in the "Distribution" section.

#### A. Costing Methodologies

Most analysts assume that in current dollars there is little incremental change in the cost of customer related facilities and expenses. Since customer related facilities are added in small increments and exhibit little technological change, the effects of vintaging and technological change, which normally distinguish marginal and embedded costs, are reduced. Thus, while it would be possible to calculate over some planning horizon the change in customer related cost in constant dollars against the expected change in the number of customers, the analyst would not expect the resulting marginal cost to differ significantly from the average embedded cost. Therefore, most marginal cost studies adopt a form of embedded analysis to calculate the total investment cost which is then amortized using an economic carrying charge.

If the minimum grid methodology is used, the customer related investment cost is that calculated in the distribution portion of the study. Otherwise, the cost of meters and service drop investment is analyzed separately by the type of metering installation or by customer load class by determining the characteristics of the service required. While it would be possible to identify separate demand and customer components of meter costs assuming that the more complex metering can be identified with higher levels of demand, all metering costs are usually charged on a per customer basis and, therefore, there is no reason to distinguish between the two components. Annual costs of each type of equipment are calculated by multiplying the installed cost by an annual carrying charge, and adding a factor to reflect operation and maintenance expenses.

Customer accounts (meter reading and billing), service and informational expenses are usually analyzed over a recent historical period, with the expenses converted to current year dollars. The customers in each customer class are weighted based on an embedded study of costs per customer or on discussions with company personnel. The customer expenses are allocated to each load class based on the weighted number of customers. See Tables 10-5A and 10-5B.

#### B. Allocation of Costs to Time Periods

While a case could be made that there are seasonal variations to such customer accounts as meter reading and customer information, the data is typically not analyzed on a monthly basis and there is no attempt at seasonal differentiation in the cost studies.

[TABLE DESCRIPTION: Table 10-5A — Customer Related Marginal Costs: Minimum Grid.

A table showing customer-related marginal costs under the minimum grid methodology across customer classes: Residential, Commercial (GS-1, GS-P), Industrial (Sub-T, Primary), and Agricultural. Rows include:

- **Customer Related Investment Cost:** Residential $759.00; Commercial GS-1 $755.00, GS-P $2,723.00; Industrial Sub-T $2,416.00 / $8,290.00, $8,701.00 / $20,262.00; Agricultural $1,763.00.
- **Customer Related O&M:** Residential $17.00; Commercial GS-1 $17.00, GS-P $62.00; Industrial $189.00, $198.00, $462.00; Agricultural $40.00.
- **General Plant Loading:** Residential $3.82; values of $13.71, $12.17, $41.75, $43.82; Agricultural $8.88.
- **Customer Account Expenses:** Residential $42.00; Commercial $42.00; Industrial $886.00, $886.00, $886.00; Agricultural $79.00.
- **Total Customer Marginal Cost:** Residential $147.79; values of $163.23, $479.93, $430.55, $362.40 for other classes.

Some individual cell values are garbled or missing in the OCR.]

[→ See original PDF page 161 for full data]

[TABLE DESCRIPTION: Table 10-5B — Customer Related Marginal Costs: Customer Specific Equipment.

A table showing customer-related marginal costs under the customer specific equipment methodology across the same customer classes as Table 10-5A: Residential, Commercial (GS-1, GS-2, GS2-S), Industrial (Sub-T, Primary), and Agricultural. Rows include:

- **Customer Related Investment Cost:** Residential $309.09; Commercial GS-1 $476.37, GS-2 $2,007.83; Industrial Sub-T $5,209.66 / $8,473.46, $8,473.46 / $14,716.85; Agricultural $2,861.61.
- **Annualized Cost:** Various values including $202.00, $681.42, $1,083.33, $1,108.33, $1,924.96; Agricultural $374.30.
- **Customer Related O&M (Same % as MG):** Values of $10.73, $45.72, $118.60, $192.82; Agricultural $64.93.
- **Customer Install Equipment:** $0.47.
- **General Plant Loading:** Values of $2.40, $42.67, $42.67, $74.11; Agricultural $14.41.
- **Customer Account Expenses:** $886.00, $886.00, $886.00; Agricultural $79.00.
- **Total Customer Marginal Cost:** Residential $76.05; values of $118.97, $366.60, $881.33, $2,258.43, $2,254.11; Agricultural $540.09.
- **Weighted Average Class MC:** Residential $16.05; value of $285.75; Industrial $2,970.31; Agricultural $540.09.

Some individual cell values are garbled or missing in the OCR.]

[→ See original PDF page 162 for full data]
