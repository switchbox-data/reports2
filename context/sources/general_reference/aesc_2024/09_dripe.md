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
extraction_scope: "partial: PDF pp. 245-287 (printed pp. 227-269), Chapter 9 Demand Reduction Induced Price Effect; the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Chapter 9 explains and quantifies demand reduction induced price effects (DRIPE): the wholesale price reductions that follow a cut in demand for electric energy, electric capacity, natural gas and oil, plus the cross-fuel effects (gas-to-electric, electric-to-gas, electric-to-gas-to-electric). It gives the regression, hedging, decay and price-shift methods and the resulting zone-on-zone and zone-on-Rest-of-Pool values by state, with comparisons to AESC 2021."
why_here: "Switchbox does heat pump rate design, marginal cost of service and cost allocation in New England rate cases; this chapter supplies the approved New England DRIPE values (including the gas-to-electric and electric-to-gas-to-electric cross-DRIPE that matter for gas-to-heat-pump electrification) and the method behind them, to cite or to compare against our own marginal-cost assumptions."
---

_Extractor note (not source text): this file holds PDF pp. 245-287 (printed pp. 227-269) of AESC 2024, Chapter 9: Demand Reduction Induced Price Effect; the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. The text is transcribed verbatim, with no typographical corrections; where the source's own numbers or cross-references do not agree, the printed value is kept and flagged inline with `[sic]` or `[source discrepancy: …]`. Words the source underlines are marked with `<u>…</u>`._

[PDF pp. 1-244 not transcribed: front matter and Chapters 1-8, in the other files of this folder (see README.md)]

[PDF p. 245 | printed p. 227]

# 9. Demand Reduction Induced Price Effect

DRIPE refers to the reduction in prices in the wholesale markets for capacity and energy—relative to the prices forecast in a given counterfactual—resulting from the reduction in quantities of capacity and of energy required from those markets due to the impact of efficiency and/or demand response programs. Thus, DRIPE is a measure of the value of efficiency in terms of the reductions in wholesale prices seen by all retail customers in a given period. In some contexts, DRIPE maybe [sic] called “price suppression” or “price effect.”

This chapter describes our results, methodology, and assumptions for energy DRIPE, capacity DRIPE, natural gas DRIPE, fuel-oil DRIPE, and cross-DRIPE effects using a combination of quantitative analyses of national and New England data rather than modeling projected market conditions.

Generally speaking, compared to AESC 2021, we find (a) similar energy DRIPE values due to a number of factors (including changes in energy prices, changes in load, and changes in hedging assumptions) that largely offset one another, (b) similar trends capacity DRIPE values (although these values tend to be highly variable year-to-year in both AESC 2024 and AESC 2021), (c) lower gas supply and electric-to-gas DRIPE values due to decreases in price shifts, (d) higher gas-to-electric cross-DRIPE values due to increases in price shifts, and (e) higher oil DRIPE values, due to changes in the underlying projection of crude oil prices. See each of the subsections below for detailed comparisons of DRIPE values in AESC 2021 and AESC 2024.

## 9.1. Introduction

DRIPE is a measure of the value of efficiency in terms of the reductions in wholesale prices seen by all retail customers in a given period. It is a separate and distinct benefit from avoided energy, avoided capacity, avoided natural gas, and avoided oil. Figure 53 illustrates the impact of DRIPE. Whereas avoided energy (for example) describes the benefits associated with a quantity reduction, avoided energy DRIPE describes the benefits associated with a <u>price</u> reduction. These effects are not double-counting—in this Figure 53, each energy DRIPE and avoided energy (yellow arrows) are separate vector components of the aggregate effect (green arrow). The total cost at point (a) is equal to $p_1 \times q_1$, while the total cost at point (c) is equal to $p_2 \times q_2$. If DRIPE were uncounted, the total cost would incompletely be calculated as the cost at point (b), or $p_1 \times q_2$.

[PDF p. 246 | printed p. 228]

**Figure 53. Example figure depicting separate and non-overlapping avoided energy and energy DRIPE effects**

[DIAGRAM DESCRIPTION: Figure 53. Example figure depicting separate and non-overlapping avoided energy and energy DRIPE effects]

A conceptual supply-and-demand line graph. The x-axis is "Quantity (MWh)" with two marked quantities, $q_2$ (left) and $q_1$ (right); the y-axis is "Price ($/MWh)" with two marked prices, $p_2$ (lower) and $p_1$ (upper). A black upward-curving line labeled "Supply" starts nearly flat at the lower left and steepens to the upper right. Two vertical demand lines cross it: a dotted blue-grey vertical line at $q_1$ labeled "Demand without EE (MWh)" and a solid blue-grey vertical line at $q_2$ labeled "Demand with EE (MWh)". Three points are circled in red where lines meet the supply curve or demand lines: (a) where the "Demand without EE" line meets the supply curve (at price $p_1$); (b) where a horizontal dashed line at $p_1$ meets the "Demand with EE" line (at quantity $q_2$, price $p_1$, which is above the supply curve); and (c) where the "Demand with EE" line meets the supply curve (at price $p_2$). A horizontal gold arrow from (a) to (b), labeled "EE lowers demand (avoided energy)", shows the quantity effect at constant price $p_1$; a vertical gold arrow from (b) down to (c), labeled "EE lowers prices (energy DRIPE)", shows the price effect at quantity $q_2$; and a green arrow from (a) to (c) running along the supply curve, labeled "Total impact of both avoided energy and energy DRIPE", is the sum of the two gold arrows. The takeaway is that avoided energy (quantity reduction priced at the old price) and energy DRIPE (price reduction applied to the remaining quantity) are separate, non-overlapping components of the total cost reduction from point (a) to point (c).

Note: This example figure depicts impacts in the energy market, but the principles are the same for all other DRIPE categories. This figure also uses “EE” as an example measure. DR PE [sic] effects can be calculated for any measure (energy efficiency or otherwise), including measures that increase the demand of a commodity.

[→ See original PDF page 246 for visual rendering]

Broadly speaking, we model five categories of DRIPE in AESC.

- **Energy DRIPE:** The consumer savings from reducing load, resulting in the market price being set by a plant with a better heat rate or less expensive fuel (e.g., natural gas rather than oil). These computations hold gas prices constant, avoiding any overlap with the Electric-Gas-Electric cross-DRIPE discussed below.
- **Capacity DRIPE:** The change in state and regional electricity bills due to reductions in electric capacity prices.
- **Own-price natural gas DRIPE:** The value of reduced natural gas demand on both gas commodity prices (gas supply DRIPE) and transportation costs to New England from the production area (gas basis DRIPE).
- **Cross-DRIPE:** The value that gas reductions have on electricity prices and that electricity reductions have on natural gas prices. Cross-DRIPE is separate from, and in addition to, own-price DRIPE values. It does not double-count any benefits.
  - **Gas-to-Electric (G-E) cross-DRIPE**: The benefits to electricity consumers that result from lower gas demand reducing gas prices for electric generation.
  - **Electric-to-Gas (E-G) cross-DRIPE**: The benefits to gas consumers from a reduction in electricity demand and hence gas demand for generation.

[PDF p. 247 | printed p. 229]

- **Electric-to-Gas-to-Electric (E-G-E) cross-DRIPE**: The benefits of reductions in electricity demand on gas prices which in turn reduce electricity prices, even if the marginal generator does not change. E-G-E DRIPE measures the electric bill savings associated with reduction in the cost of gas for the marginal price-setting power plant, resulting from the decline in natural gas usage for electricity.
- **Own-price oil DRIPE:** The value of reduced demand for petroleum products (e.g., gasoline, diesel, residual) on petroleum prices.

The interactions of DRIPE effects are shown in Figure 54.

**Figure 54. DRIPE effect interactions**

[DIAGRAM DESCRIPTION: Figure 54. DRIPE effect interactions]

A flow diagram with three grey oval "source" nodes across the top, a row of yellow rounded-rectangle price nodes in the middle, and three green trapezoid retail-rate nodes at the bottom. Top row, left to right: "Gas Load Reduction", "Electric Load Reduction", "Oil Demand Reduction". Middle row, left to right: "Gas Delivery Prices", "Market Electric Energy Price", "Gas Supply Price", "Electric Capacity Price" (these four belong to the gas and electric branches), and, at the far right, "Oil Delivery". Bottom row: "Retail Gas Rates" (under Gas Delivery Prices), "Retail Electric Rates" (centered under the Market Electric Energy Price / Gas Supply Price / Electric Capacity Price nodes) and "Retail Oil Rates" (under Oil Delivery). A legend box at the lower left defines four arrow styles: solid blue arrow = "Direct Effects"; dashed blue arrow = "Direct Effects: Competitive Markets Only"; dotted blue arrow = "Direct Effects: Vertically-Integrated Utilities Only"; solid brown arrow = "Indirect Effects: Proportional to Percent Gas at Margin".

Arrows: Gas Load Reduction has a solid blue arrow down to Gas Delivery Prices and a long solid blue diagonal arrow to Gas Supply Price. Electric Load Reduction has a solid blue arrow to Market Electric Energy Price, a solid blue arrow to Electric Capacity Price, a solid brown (indirect) arrow straight down to Gas Supply Price, and a solid brown (indirect) diagonal arrow to Gas Delivery Prices. Gas Delivery Prices has a solid blue arrow to Market Electric Energy Price and a solid blue arrow down to Retail Gas Rates. Gas Supply Price has a solid blue arrow to Market Electric Energy Price. Market Electric Energy Price and Electric Capacity Price each have a dashed blue arrow (competitive markets only) to Retail Electric Rates, and Gas Supply Price has a dotted blue arrow (vertically-integrated utilities only) to Retail Electric Rates. Oil Demand Reduction has a solid blue arrow to Oil Delivery, which has a solid blue arrow to Retail Oil Rates. The diagram shows that gas-load reductions reach retail electric rates through gas supply and electric energy prices, and that electric-load reductions reach retail gas rates only indirectly, in proportion to how often gas is on the margin.

[→ See original PDF page 247 for visual rendering]

There are two elements to these estimates: magnitude and duration. The magnitude of DRIPE depends on market prices, market size, and the market price responsiveness. DRIPE benefits are unlikely to exist in perpetuity, however, so benefits are adjusted downward or decayed to reflect how other market participants respond to changes in market price over time.

Our estimates indicate that the DRIPE effects are very small when expressed in terms of an impact on market prices, i.e., reductions of a fraction of a percent. However, the DRIPE impacts are significant when expressed in absolute dollar terms for the state or region. Very small impacts on market prices, when applied to all energy and capacity being purchased in the market, translate into large absolute dollar amounts.

[PDF p. 248 | printed p. 230]

### General DRIPE methodology

In AESC, we estimate DRIPE according to the following steps:

1. First, we calculate a “price shift.” This shift represents the change in price (e.g., dollars per MWh) for a change in demand (e.g., MWh). Aggregated over many data points, this price shift represents the supply curve of a particular resource. For many DRIPE categories, this is calculated using a regression, where we observe many hundreds or thousands of historical datapoints to establish a relationship between prices and demand. For other DRIPE categories, these price shifts are based on an assumed supply curve. This most notably occurs for capacity DRIPE, where there is not enough information to develop a regression from historical data.
2. Second, we multiply these price shifts by total future market demand, so that we may then apply them to any generic <u>change</u> in demand. In other words, the price shift is expressed in terms of price-per-demand.2 [sic; the printed superscript "2" here is not a footnote reference] Multiplying the price shift by demand translates it into a price-per-demand value that can then be multiplied by a measure’s anticipated savings.[^290]
3. Finally, we adjust the price-per-demand value. This may include accounting for hedged demand which has, in theory, already been purchased and is not subject to price shifts. Or, it may involve reducing benefits to account for decays in effects, or “phasing in” of effects to describe a lag in the way the market realizes these impact [sic]. Importantly, only some categories of DRIPE have these shifts applied.

Depending on the DRIPE category, these steps may be more complex or performed in a different order (to facilitate computation).

Price effects impact the entire region because there is only one market each for electric energy, electric capacity, and natural gas. For all the DRIPE categories described in AESC, we estimate both intra-zonal DRIPE (i.e., the benefits that accrue within a zone from load impacts within that zone, sometimes called own-zone or zone-on-zone) and inter-zonally (i.e., the benefits that accrue beyond that zone’s borders in the “Rest of Pool”). We calculate Intra-zonal DRIPE by multiplying the price effect for a particular category of DRIPE by a single state’s projected demand (rather than the regional total). Meanwhile, inter-zonal DRIPE is calculated by subtracting the intra-zonal value from the regional total.[^291]

In some jurisdictions, only “intra-zonal” DRIPE benefits are used in cost-effectiveness testing. The reason may vary, but in some cases, there may be a regulatory directive to only count the benefits that accrue to a particular state’s ratepayers. However, we note that the inter-zonal benefits continue to exist even if

[^290]: Throughout this chapter, we frequently discuss DRIPE in terms of benefits relating from savings, but DRIPE is a non-directional value that can also describe price increases resulting from increased demand. Some measures that reduce the use of one kind of fuel (e.g., natural gas) but increase use of another fuel (e.g., electricity) may end up utilizing nearly all the DRIPE categories described in this chapter.

[^291]: An equivalent mathematical operation would be to multiply the price shift by the regional total demand <u>less</u> the demand for the state in question.

[PDF p. 249 | printed p. 231]

they are not counted in a measure’s cost-effectiveness test. We also note that no other states would count these benefits.

The remaining text of this chapter describes the specific methodology used to generate DRIPE benefits for each category of DRIPE.

## 9.2. Electric energy DRIPE

A reduction in electricity demand should reduce wholesale energy prices, which benefits all market participants. This section describes the AESC 2024 methodology and assumptions for electric energy DRIPE, discusses the benefits and detriments of various model forms, and presents our estimates of energy DRIPE. Energy DRIPE values are presented in two ways: first, by zone, month, and period; second for the “top” 100 load or price hours. The monthly values provide DRIPE estimates for programs targeting baseline reductions while the “top” hour assessments provide estimates for more targeted applications.

Our estimates of electric energy DRIPE follow the same approach used in previous AESC studies from 2009 to 2021. Generally speaking, we conduct a set of regressions of historical zonal hourly market prices against zonal and regional load to develop elasticities. Then, we estimate the timing and duration of benefits based upon the following market realities:

1. We assume the reductions in wholesale prices flow through to customers as existing contracts and other resources (legacy resources, renewable contracts, basic-service and other default contracts, direct contracts with marketers) expire.
2. Customers will respond to lower energy prices by using somewhat more energy.[^292]
3. The generation market will respond to sustained lower prices by some combination of retiring and de-rating existing generating capacity and delaying new resources that reduce market energy prices (such as gas combined-cycle units and high-efficiency combustion turbines).
4. Lower loads will tend to result in lower acquisition mandates under renewable and other alternative-energy standards that are stated as a percentage of energy sold.

### Regression model selection

AESC 2024, as with AESC 2021, estimates the magnitude of wholesale energy market DRIPE by year by conducting a set of regressions of historical zonal hourly market prices against regional load. This top-down approach assumes there is an underlying relationship between prices and loads which can be

[^292]: Other factors (e.g., purchases of renewables, transmission construction, grid modernization, recovery of energy-efficiency costs) may simultaneously raise prices. The energy DRIPE considers only the marginal effect on market energy prices on retail prices and hence usage.

[PDF p. 250 | printed p. 232]

represented using a single equation. This approach has the benefit that it is easy to understand and that it captures the key features of the system transparently.

Regressions also have the benefit of modeling the average relationship between price and demand and providing structure to heterogeneous data. Periods with similar demand often have very different prices. Price dispersion is a product of an uncertain system that contains dynamic unit commitment decisions as well as a host of other stochastics such as generator-forced outages or transmission constraints. By assessing all system price and demand data, it is possible to capture both structural trends as well as uncertain events that occurred in past years.

In prior AESC studies, we considered many functional forms to describe the relationship between zonal prices and loads. We tested the significance of variables related to ISO system performance (e.g., capacity surplus, maintenance), system implied heat rate, and zonal and regional loads. After considering these candidate variables and various functional forms, we settled on a polynomial model to characterize the relationship between zonal prices and loads. The model, described in Equation 4, relates zonal price to ISO-wide demand and to natural gas prices.

**Equation 4. Regression equation relating zonal electric energy prices to ISO demand and natural gas prices**

$$LMP_{Zone} = \beta_0 + \beta_1 Demand_{ISO} + \beta_2 Demand_{ISO}^2 + \beta_3 Demand_{ISO}^3 + \beta_4 Price_{NG}$$

Equation 4 describes a cubic function. A cubic function allows for a “hockey stick”-like profile where prices increase slowly at first, then quickly during high load periods. For example, at the extreme right side of the supply curve (e.g., when the market’s marginal unit might switch from a gas peaker to a natural gas-fired combined-cycle unit), prices will increase by approximately 30 percent even though demand might only increase a few MW. In the middle of the offer stack, by contrast, switching from a more efficient gas combined-cycle unit to a slightly less efficient one will only increase prices by a few percent. In Equation 4, changes in natural gas prices shift the overall curve up or down but do not skew the shape of the curve itself. This polynomial model offers five advantages over other assessed models:

1. **Non-linearity** that depicts very high prices at high load times and flatter prices under lower loads
2. **Explicit control for natural gas prices**, which is a major driver of winter price volatility
3. Significantly **better goodness-of-fit** compared to linear models (e.g., R<sup>2</sup> or sum-of-squared errors)
4. **Single functional form** for all zones, months, and periods
5. **Simple formulation**, where only key attributes are included

Note that the “ISO Demand” described Equation 4 [sic] is <u>not</u> the total ISO-wide demand for electricity. Instead, this variable is perhaps better described as “net demand,” which is calculated by subtracting hourly wind, solar, and nuclear output from gross demand reported by ISO New England. Wind and solar vary throughout the day predictably (especially for solar) and less predictably (as a function of weather).

[PDF p. 251 | printed p. 233]

Nuclear output is steady most days but is sometimes reduced or eliminated due to planned and unplanned outages. None of these generators are subject to load- or price-based dispatch, since they self-schedule or bid into ISO New England’s energy market at very low (in the case of wind, even negative) prices.[^293] As a result, we remove the MWh contribution of these non-price-responsive generators from our “ISO Demand” variable.

In AESC 2024, we use data from January 2018 through December 2022 as the basis for our regressions.[^294] Figure 55 plots actual price and demand data (in blue) against predicted data (in red) estimated using Equation 4 for one illustrative region and period. We perform a similar regression for nine regions (ISO-wide, Connecticut, Maine, New Hampshire, Rhode Island, Vermont, SEMA, NEMA, and WCMA), and for 24 time periods (one off-peak period and one on-peak period for each month).[^295]

[^293]: In earlier AESC studies, we also examined the impact of removing the hourly contribution of other resource types from the regression. Availability of other generation may also affect market energy prices, but the relationship between price and output is complicated. The dispatch of thermal plants is driven by loads and energy prices; commitment of steam and combined‐cycle plants is driven by forecast loads and prices; and hydro is scheduled within the week and the day to minimize costs of energy and reserves. It is therefore difficult to determine whether a plant is not running (1) because it is not available, (2) because energy price is below the plant’s energy bid, or (3) because it is being held back as reserve (especially in the case of hydro and fast-start combustion turbines) or to meet higher loads expected later in the hydro operating cycle. The output of most fossil units can be determined from EPA’s Air Market Programs dataset, and ISO New England provides total daily capacity that is unavailable due to outages or failure to commit in the day-ahead market, but these sources do not provide enough detail to determine why particular units are not operating. In any event, the regression results are similar whether gross net load is used in Equation 4, reducing the usefulness of additional complexity.

[^294]: This time period spans over 43,800 datapoints (for each of the nine modeled regions), which provides our regressions with sufficient detail to accurately predict the relationship between prices and loads. Previous AESC studies utilized shorter time periods; AESC 2024 broadens the time period examined in an attempt to include years both before and after the impacts of the COVID-19 pandemic and subsequent impacts on commodities markets. Hourly energy price data and gross load data was obtained from ISO New England (for example, see ISO New England. 2022. _ISO New England Public_. Available at [https://www.iso-ne.com/static-assets/documents/2022/02/2022_smd_hourly.xlsx](https://www.iso-ne.com/static-assets/documents/2022/02/2022_smd_hourly.xlsx)).

    Sub hourly data on ISO New England’s fuel mix was downloaded from ISO New England then averaged to produce hourly results for wind, solar, and nuclear generation. ISO New England. Last accessed September 30, 2023. “Dispatch Fuel Mix.” _ISO-NE.com_. Available at [https://www.iso-ne.com/isoexpress/web/reports/operations/-/tree/gen-fuel-mix](https://www.iso-ne.com/isoexpress/web/reports/operations/-/tree/gen-fuel-mix)

    Daily data on delivered prices to Algonquin Citygate were obtained from Natural Gas Intelligence’s (NGI’s) “Daily” subscription service. NYMEX Futures prices for Henry Hub were retrieved from NGI’s “Forward Look” subscription service. More details on each service can be found at: [https://www.naturalgasintel.com/](https://www.naturalgasintel.com/).

    For points with very low zonal LMPs, elasticities are very large. This is a byproduct of the modeling and elasticity calculation, not of any structural phenomenon. When LMPs are $0/MWh, the elasticity is infinite. We exclude calculated point elasticities when zonal prices are less than $5/MWh. These exclusions occur very rarely—for the ISO New England region, for example, there is one such hour.

[^295]: We use a similar approach to calculate regressions for “top” hours, for use in DSM measures that do not operate the entire year but are instead targeted at certain hours. Rather than 24 periods, we calculate regressions for 374 periods for all 9 regions. This includes 68 summer off-peak regressions, 58 summer on-peak regressions, 132 winter off-peak regressions, and 116 winter on-peak regressions. Each of these batches of regressions is divided in half into regressions that span “Top Load” and “Top LMP” hours. Within Summer, On-Peak, Top Load (for example), there exists regressions that cover the top 50 hours (sorted by ISO-wide demand), the top 100 hours, the top 150 hours, and so on. Asymmetry in number of regressions across different time slices (summer, winter, on-peak, and off-peak) is due to differences in the number of hours included within each time slice.

[PDF p. 252 | printed p. 234]

In general, the model produces a good fit ($R^2$ above 0.7) for 100 percent of the 216 regressions (24 periods X 9 regions). Periods with relatively lower $R^2$ values tend to be those in shoulder months (spring and fall) or off-peak periods.

**Figure 55. Illustrative regression for WCMA, February on-peak hours**

[DIAGRAM DESCRIPTION: Figure 55. Illustrative regression for WCMA, February on-peak hours]

A scatter plot with a fitted curve. The x-axis is "Net Day Ahead ISO-wide Demand (MW)", running from 0 to 16,000 in steps of 2,000. The y-axis is "Day Ahead LMP (2024 $/MWh)", running from $0 to $350 in steps of $50. Hundreds of semi-transparent blue-green dots, labeled "Hourly datapoints", form a dense cloud from about 6,000 MW to about 14,500 MW of net demand. At lower demand (about 6,000-9,000 MW) the points sit mostly between about $0 and $75 per MWh; the cloud widens and rises with demand, with most points between about $50 and $200 per MWh at 10,000-13,000 MW and a few reaching roughly $300 per MWh at about 12,000-13,000 MW. A red curve labeled "Regression line" starts near $25 per MWh at about 6,000 MW, stays nearly flat to about 9,000 MW, then bends upward, reaching about $200 per MWh at about 14,000 MW (the "hockey stick" shape of the cubic in Equation 4). The chart shows that prices are widely dispersed at any given demand but rise convexly with net demand, which is the relationship the elasticities are computed from.

Note: This chart is shown for illustrative purposes only. To plot the red, fitted line in the figure, we assume a daily price of $0 per MMBtu for natural gas (as multivariate regression cannot be displayed in a two-dimensional chart). This differs from our actual analysis in which we used different natural gas prices for each point. Final DRIPE calculations use monthly timeframes instead of quarterly; different zones have different price/load pairs.

[→ See original PDF page 252 for visual rendering]

### Calculating elasticities from the regression

After establishing a functional form to model the relationship between price and demand, we then estimate elasticities using these regressions. For each regression, we first calculate the derivative of the polynomial regression model (Equation 4) with respect to demand:

**Equation 5. Calculation of regression derivative**

$$\text{Instantaneous slope} = \frac{\partial LMP_{Zone}}{\partial Demand_{ISO}} = \beta_1 + 2\beta_2 Demand_{ISO} + 3\beta_3 Demand_{ISO}^2$$

For each hour within a regression, this derivative describes how price would change in each hour for a small change in demand. Next, we apply Equation 6 to describe the elasticity for each hourly data point (e.g., an estimate of the percent change in price per percent change in demand).

**Equation 6. Calculation of elasticity**

$$\text{Elasticity} = \frac{\%\ \text{change in price}}{\%\ \text{change in demand}} = \frac{\text{Instantaneous slope of price relative to demand}}{\text{Hourly electricity price}} \times \text{Hourly demand}$$

We then aggregated each of the resulting elasticities into a single load-weighted elasticity for each regression. This average elasticity represents the average price response to a small change in demand

[PDF p. 253 | printed p. 235]

for a given zone, season, and period. Table 101 presents electric energy DRIPE elasticities in by [sic] zone, month, and period.[^296]

**Table 101. Energy DRIPE elasticities**

| Period   | Month | ISO NE | ME  | NH  | VT  | CT  | RI  | SEMA | NEMA | WCMA |
| -------- | ----- | ------ | --- | --- | --- | --- | --- | ---- | ---- | ---- |
| Annual   |       | 1.3    | 1.4 | 1.4 | 1.4 | 1.3 | 1.3 | 1.4  | 1.3  | 1.3  |
| Off-peak | 1     | 2.1    | 2.1 | 2.1 | 2.1 | 2.1 | 2.1 | 2.1  | 2.1  | 2.1  |
| Off-peak | 2     | 1.5    | 1.6 | 1.6 | 1.5 | 1.5 | 1.5 | 1.5  | 1.5  | 1.5  |
| Off-peak | 3     | 1.4    | 1.5 | 1.4 | 1.4 | 1.3 | 1.4 | 1.4  | 1.4  | 1.4  |
| Off-peak | 4     | 0.9    | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 1.1  | 0.9  | 0.9  |
| Off-peak | 5     | 0.9    | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9  | 0.9  | 0.9  |
| Off-peak | 6     | 0.8    | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8  | 0.8  | 0.8  |
| Off-peak | 7     | 1.2    | 1.1 | 1.2 | 1.2 | 1.2 | 1.1 | 1.2  | 1.2  | 1.2  |
| Off-peak | 8     | 1.1    | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1  | 1.1  | 1.1  |
| Off-peak | 9     | 0.8    | 0.8 | 0.8 | 0.8 | 0.8 | 0.7 | 0.7  | 0.8  | 0.8  |
| Off-peak | 10    | 1.0    | 1.0 | 1.0 | 1.0 | 1.0 | 0.9 | 1.0  | 1.0  | 1.0  |
| Off-peak | 11    | 1.0    | 1.1 | 1.1 | 1.0 | 1.0 | 1.0 | 1.0  | 1.1  | 1.0  |
| Off-peak | 12    | 1.5    | 1.6 | 1.5 | 1.5 | 1.5 | 1.5 | 1.5  | 1.5  | 1.5  |
| On-peak  | 1     | 2.5    | 2.5 | 2.4 | 2.5 | 2.5 | 2.5 | 2.4  | 2.4  | 2.5  |
| On-peak  | 2     | 1.7    | 1.7 | 1.7 | 1.7 | 1.7 | 1.7 | 1.7  | 1.7  | 1.7  |
| On-peak  | 3     | 1.4    | 1.5 | 1.4 | 1.5 | 1.4 | 1.4 | 1.4  | 1.4  | 1.4  |
| On-peak  | 4     | 0.8    | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8  | 0.8  | 0.8  |
| On-peak  | 5     | 0.9    | 0.9 | 0.9 | 1.0 | 0.9 | 0.9 | 0.9  | 0.9  | 0.9  |
| On-peak  | 6     | 1.1    | 1.0 | 1.0 | 1.1 | 1.1 | 1.0 | 1.0  | 1.0  | 1.0  |
| On-peak  | 7     | 1.9    | 1.8 | 1.9 | 1.9 | 1.9 | 1.9 | 1.9  | 1.9  | 1.9  |
| On-peak  | 8     | 2.0    | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 2.1  | 2.0  | 2.0  |
| On-peak  | 9     | 1.0    | 0.9 | 0.9 | 1.0 | 1.0 | 1.0 | 1.1  | 1.0  | 1.0  |
| On-peak  | 10    | 1.3    | 1.2 | 1.3 | 1.3 | 1.3 | 1.3 | 1.4  | 1.3  | 1.3  |
| On-peak  | 11    | 1.2    | 1.3 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2  | 1.2  | 1.2  |
| On-peak  | 12    | 1.4    | 1.4 | 1.3 | 1.3 | 1.3 | 1.4 | 1.4  | 1.3  | 1.4  |

_Note:_ Elasticities for Connecticut subregions (Southwest CT and Other CT) are assumed to be equal to the Connecticut-wide elasticity. A Massachusetts-wide elasticity is calculated based on a weighted average of the demand for the three subregions. These values are available in the _AESC 2024 User Interface_.

The results are stable across zones but vary by month and period. The modest spread in elasticity values by zone indicates zonal prices are strongly correlated with system load. On an annual basis, a 1.0 percent reduction in demand yields a 1.3 percent reduction in price. Depending on the month, a 1.0 percent reduction in load throughout New England results in a 0.8 to 2.1 percent reduction in off‐peak price, and a 0.8 to 2.5 percent reduction in peak price.

[^296]: We also calculate elasticities for “top” hours (described in footnote 295) using an analogous methodology. These elasticities are not shown in this report due the [sic] large size of the table but may be found in the _AESC 2024 User Interface_.

[PDF p. 254 | printed p. 236]

#### Comparison with AESC 2021

Table 102 describes the summary statistics from Table 101 and compares the results with analogous values from AESC 2021. Elasticities in AESC 2024 are generally very similar to those in AESC 2021, due in part to the fact that three of the five years of input data overlap between the two datasets).

**Table 102. Comparison of energy DRIPE elasticities, AESC 2021 and 2024**

| Season | Period   | AESC 2021 Min | AESC 2021 Median | AESC 2021 Max | AESC 2024 Min | AESC 2024 Median | AESC 2024 Max |
| ------ | -------- | ------------- | ---------------- | ------------- | ------------- | ---------------- | ------------- |
| Annual |          | 1.35          | 1.36             | 1.40          | 1.34          | 1.35             | 1.37          |
| Winter | On-peak  | 0.87          | 1.38             | 2.71          | 0.75          | 1.34             | 2.50          |
| Winter | Off-peak | 0.72          | 1.18             | 2.35          | 0.86          | 1.23             | 2.13          |
| Summer | On-peak  | 0.65          | 1.50             | 2.22          | 0.92          | 1.48             | 2.06          |
| Summer | Off-peak | 0.72          | 1.00             | 1.21          | 0.73          | 0.92             | 1.17          |

### Calculating energy DRIPE

Next, we apply the above elasticities to hourly prices and loads to calculate the DRIPE benefit for any 1 MWh reduction in load. Conceptually, the value of DRIPE is equal to the change in price that results from a 1 MWh reduction in load, multiplied by the amount of load that benefits from that reduction in price.

We calculate the value of DRIPE both intra-zonally (i.e., the benefits that accrue within a zone from load impacts within that zone) and inter-zonally (i.e., the benefits that accrue beyond that zone’s borders in the “Rest of Pool”). Equation 7 describes the calculation for intra-zone DRIPE, while Equation 8 describes the calculation for inter-zone DRIPE. Intrazonal and interzonal values are added to determine the total DRIPE effect.

The first term in Equation 7 calculates the change in zonal price given a change in ISO demand. It is multiplied by the load in Zone Z to calculate the collective benefit of that price reduction. Equation 8 is similar but reflects how the demand reduction in Zone Z reduces prices in all other zones.

As in prior AESC studies, we assume the value of DRIPE is reduced in two ways:

- First, rather than relying on the full energy demand values, we instead rely only on the unhedged portion of demand to calculate energy DRIPE. This is the portion of demand that has not already been purchased through long-term contracts.
- Second, we assume that the DRIPE effect decays over time. This is a series that aggregates expected effects related to resources responding to changes in prices, demand elasticity, and binding RPS policies.

The next subsection describes each of these two effects.

Intrazonal DRIPE values are roughly proportional to the percentage of ISO load in a given zone. Zones with less load will have lower zone-on-zone energy DRIPE values than zones with higher load. For example, Maine accounts for roughly one-fifth as much load as Massachusetts and has a zone-on-zone

[PDF p. 255 | printed p. 237]

DRIPE value approximately one-fifth as large.[^297] Conversely, interzonal estimates are approximately proportional to the difference between ISO load and zonal load. Zones with lower load will have higher zone-on-Rest-of-Pool values.

**Equation 7. Value of intra-zonal electric energy DRIPE**

$$DRIPE_{\text{Zone Z} \,|\, \text{Zone Z},\ \text{Period P}} = \left[ \frac{\varepsilon_{\text{Zone Z, Period P}} \; P_{\text{Zone Z, Period P}}}{Q_{\text{ISO, Period P}}} \times Q_{\text{Zone Z, Period P}} \right] \times D$$

**Equation 8. Value of inter-zonal electric energy DRIPE**

$$DRIPE_{\text{Rest-of-Pool} \,|\, \text{Zone Z},\ \text{Period P}} = \frac{(1-\delta)_{\text{Period P}}}{Q_{\text{ISO, Period P}}} \sum_{x \in \text{Zones},\ x \neq \text{Zone Z}} \varepsilon_{x,\text{Period P}} \times P_{x,\text{Period P}} \times Q_{x,\text{Period P}}$$

Where:

- $\varepsilon$ is elasticity
- $P$ is the zonal market energy price ($/MWh)
- $Q_{\text{Zone Z}}$ is zonal load less hedged supply (i.e., “unhedged load”)
- $Q_{\text{ISO}}$ is ISO energy load
- $D$ is the aggregate decay effect

_Extractor note (not source text): the printed "Where:" list does not define $\delta$, which appears in Equation 8 as $(1-\delta)$; Equation 7 uses $D$ for the aggregate decay effect._

#### Energy DRIPE reductions

We assume the value of energy DRIPE is reduced due to (a) some portion of energy purchased being bought outside the spot market for energy (i.e., hedged) and (b) a decay factor. The following subsections describe the assumptions underlying each of these effects.

#### <u>Hedging assumptions</u>

Substantial energy is purchased months or up to several years in advance of delivery, through utility contracting for standard service or a third‐party contract. Hence, we assume energy DRIPE benefits are calculated only using the share of demand that is unhedged (i.e., the share that is purchased on the energy spot market). Our assumptions on energy hedging are based on four factors:

1. **Investor-owned utility contracts:** These contracts include pre‐restructuring legacy contracts, post‐restructuring reliability contracts in Connecticut, renewables purchases, and pending purchases from Hydro Québec.[^298]
2. **Hedging in Vermont.** Vermont is the sole remaining New England state that is vertically integrated statewide. Based on the 2021 IRP for Green Mountain Power, we assume

[^297]: There are subtle differences that make comparison inexact because DRIPE also depends on zonal elasticity and hedging estimates.

[^298]: We obtained data on these contracts from utility IRPs and FERC Form 1.

[PDF p. 256 | printed p. 238]

that all utilities in Vermont have about 50–90 percent of their energy hedged, depending on the year.[^299]
3. **Hedging of vertically integrated energy in the other five New England states**. We estimate the resources owned or under contract to the vertically integrated utilities (various mixes of municipals and coops in the other five states) based on data from EIA 861.[^300] Because exact data on hedged energy is difficult to compile, we assume that all load related to vertically integrated utilities (outside Vermont) are 50 percent hedged in all years.[^301]
4. **Short-term contracts.** In addition to long-term hedging, some load is also subject to short-term contracts. Based on our knowledge of the procurement policies for standard service, the length of third‐party contracts, and information provided by some of the participating utilities in previous AESC studies, we assume that 50 percent of energy is pre‐contracted for the year of measure installation, 20 percent in the following year, and 10 percent in the third year. Depending on the measure vintage selected, this assumption is shifted by one year or more.

Table 103 depicts the aggregate unhedged share of energy by year in Counterfactual #1.

[^299]: For more, see [https://greenmountainpower.com/wp-content/uploads/2021/12/2021-Integrated-Resource-Plan.pdf](https://greenmountainpower.com/wp-content/uploads/2021/12/2021-Integrated-Resource-Plan.pdf), Figure 7-5.

[^300]: EIA Form 861, 2015-2022. Available at [https://www.eia.gov/electricity/data/eia861/](https://www.eia.gov/electricity/data/eia861/).

[^301]: For example, we note that Belmont Light hedges up to 50 percent of its capacity and at least as much energy (see [https://www.belmontlight.com/wp-content/uploads/2019/07/BMLD-Power-Supply-Policy-Updated-July-2019.pdf](https://www.belmontlight.com/wp-content/uploads/2019/07/BMLD-Power-Supply-Policy-Updated-July-2019.pdf)). Few vertically integrated utilities outside Vermont publish precise information on the amount of energy and capacity that is hedged. Ipswich Electric Light Department, for example, notes a 30 percent hedging target in its annual report, but also includes separate, long-term clean energy power purchase agreements that increase the _de facto_ hedged percentage (see [https://www.ipswichma.gov/DocumentCenter/View/14930/ELD-Annual-Report---FY23-Budget](https://www.ipswichma.gov/DocumentCenter/View/14930/ELD-Annual-Report---FY23-Budget)). Likewise, Middleborough Department of Public utilities notes that about 50 percent of its power was purchased in 2021, which suggests that the remaining 50 percent was hedged ([https://www.mged.com/DocumentCenter/View/431/2021-DPU-Report-PDF](https://www.mged.com/DocumentCenter/View/431/2021-DPU-Report-PDF)).

[PDF p. 257 | printed p. 239]

**Table 103. Percent of load assumed to be unhedged in Counterfactual #1**

| Year | ISO | CT  | MA  | ME  | NH  | RI  | VT  |
| ---- | --- | --- | --- | --- | --- | --- | --- |
| 2024 | 38% | 23% | 42% | 46% | 46% | 40% | 26% |
| 2025 | 59% | 36% | 65% | 74% | 73% | 60% | 42% |
| 2026 | 74% | 51% | 82% | 92% | 92% | 63% | 53% |
| 2027 | 68% | 56% | 67% | 92% | 92% | 63% | 53% |
| 2028 | 70% | 59% | 68% | 92% | 92% | 64% | 53% |
| 2029 | 69% | 60% | 68% | 85% | 92% | 65% | 53% |
| 2030 | 70% | 68% | 68% | 79% | 92% | 66% | 53% |
| 2031 | 75% | 88% | 68% | 79% | 92% | 67% | 53% |
| 2032 | 76% | 89% | 69% | 80% | 92% | 68% | 53% |
| 2033 | 77% | 89% | 70% | 80% | 92% | 69% | 53% |
| 2034 | 77% | 89% | 71% | 81% | 92% | 70% | 53% |
| 2035 | 77% | 89% | 71% | 81% | 92% | 71% | 53% |
| 2036 | 78% | 89% | 72% | 82% | 92% | 71% | 53% |
| 2037 | 78% | 89% | 73% | 82% | 93% | 72% | 53% |
| 2038 | 79% | 90% | 73% | 83% | 93% | 73% | 53% |
| 2039 | 79% | 88% | 74% | 83% | 93% | 74% | 53% |
| 2040 | 78% | 83% | 74% | 83% | 93% | 74% | 53% |
| 2041 | 79% | 86% | 75% | 84% | 93% | 75% | 53% |
| 2042 | 80% | 90% | 75% | 84% | 93% | 76% | 53% |
| 2043 | 80% | 90% | 76% | 84% | 93% | 76% | 53% |
| 2044 | 81% | 91% | 76% | 85% | 93% | 76% | 53% |
| 2045 | 81% | 91% | 76% | 85% | 93% | 77% | 53% |
| 2046 | 81% | 91% | 76% | 85% | 93% | 77% | 53% |
| 2047 | 81% | 91% | 76% | 86% | 93% | 78% | 53% |
| 2048 | 81% | 91% | 76% | 86% | 93% | 78% | 53% |
| 2049 | 81% | 91% | 76% | 86% | 93% | 78% | 53% |
| 2050 | 82% | 91% | 77% | 86% | 93% | 78% | 53% |

Note: Because total energy demand varies for each counterfactual, and because assumptions on contracted MWh are fixed, these percentages vary for each counterfactual. See the _AESC 2024 User Interface_ for detail on each counterfactual.

#### <u>Decay assumptions</u>

We assume three factors tend to reduce energy DRIPE as time passes after the initial effect on market prices:

1. **Resources respond to changes in prices.** Owners of existing generating capacity would tend to allow their energy‐producing assets to become less efficient and less reliable as low energy prices make continued operation of the units less attractive, leading to more outages and higher market‐clearing prices.
2. **Demand elasticity.** Over time, customers might respond to lower energy prices by using somewhat more energy, pushing prices back up somewhat. We assume demand elasticities that start at 0.1 percent in 2024 and increase to 1 percent by 2036, where they are sustained through the study period.[^302]

[^302]: Elasticities are derived from Burke, Paul J. et al. "The price elasticity of electricity demand in the United States: A three-dimensional analysis." Center for Applied Macroeconomic Analysis, 2018. Available at [PDF p. 258 | printed p. 240] [https://cama.crawford.anu.edu.au/sites/default/files/publication/cama_crawford_anu_edu_au/2017-08/50_2017_burke_abayasekara_0.pdf](https://cama.crawford.anu.edu.au/sites/default/files/publication/cama_crawford_anu_edu_au/2017-08/50_2017_burke_abayasekara_0.pdf); and EIA Price Elasticity analysis, available at [https://www.eia.gov/analysis/studies/buildings/energyuse/pdf/price_elasticities.pdf](https://www.eia.gov/analysis/studies/buildings/energyuse/pdf/price_elasticities.pdf).

3. **Impact from binding RPS policies.** For every MWh not required due to energy efficiency, generation service providers will not need to procure a fraction of a REC from new renewable resources, assuming that these policies are “binding” (i.e., drive construction of new renewable resources in New England).[^303] We assume that reducing load under conditions where RPS policies are binding will generally result in fewer renewables being built, partially offsetting the reduction in energy load. This percentage varies by state, year, and counterfactual.

We calculate the aggregate decay effect in each year as the product of (a) one less the percent of load that is binding under the state’s RPS policies, (b) one less the demand elasticity factor, and (c) one less the resource fade-out factor. This effect is shown in Table 104, for Counterfactual #1, for measures installed in 2024.

**Table 104. Energy DRIPE decay factors for measures installed in 2024 in Counterfactual #1**

| Year | ISONE | CT  | MA  | ME  | NH  | RI  | VT  |
| ---- | ----- | --- | --- | --- | --- | --- | --- |
| 2024 | 95%   | 99% | 93% | 97% | 96% | 99% | 71% |
| 2025 | 94%   | 98% | 92% | 96% | 96% | 98% | 69% |
| 2026 | 93%   | 98% | 91% | 95% | 95% | 98% | 66% |
| 2027 | 92%   | 97% | 90% | 94% | 94% | 97% | 64% |
| 2028 | 91%   | 95% | 88% | 92% | 92% | 95% | 61% |
| 2029 | 88%   | 92% | 86% | 89% | 90% | 92% | 57% |
| 2030 | 84%   | 89% | 82% | 85% | 86% | 89% | 53% |
| 2031 | 79%   | 83% | 76% | 79% | 80% | 83% | 40% |
| 2032 | 70%   | 74% | 68% | 71% | 72% | 74% | 34% |
| 2033 | 58%   | 61% | 56% | 59% | 59% | 61% | 27% |
| 2034 | 40%   | 42% | 38% | 40% | 41% | 42% | 18% |
| 2035 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2036 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2037 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2038 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2039 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2040 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2041 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2042 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2043 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2044 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2045 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2046 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2047 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2048 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2049 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |
| 2050 | 0%    | 0%  | 0%  | 0%  | 0%  | 0%  | 0%  |

[^303]: For more discussion on binding RPS policies, see Chapter 7. _Avoided Cost of Compliance with Renewable Portfolio Standards and Related Clean Energy Policies_ and Section 8.2: _Applying non-embedded costs_.

[PDF p. 259 | printed p. 241]

Note: This decay schedule will vary for measures installed in other years, under other counterfactuals. See the _AESC 2024 User Interface_ for detail on each counterfactual.

#### Energy DRIPE values

After combining the effects of the price shifts, unhedged demand, and decay, we can calculate the energy DRIPE benefits. Table 105 provides 15-year levelized energy DRIPE benefits for efficiency measures installed in 2024 using Equation 7 and Equation 8, for values installed in Massachusetts. These values may be multiplied by a MWh quantity (e.g., energy savings from energy efficiency or energy increases from electrification) to estimate the resultant DRIPE impact in dollars. Values are shown for measures installed in 2024; values for measures installed in other years in other states may be calculated using the _AESC 2024 User Interface_.

_Extractor note (not source text): the text above calls the Table 105 values "15-year levelized", but the table lists a separate value for each year 2024-2034 under each period; the single 15-year levelized values by state are in Table 106._

**Table 105. Illustrative energy DRIPE values for 2024 installations (2024 $ per MWh) for Counterfactual #1, for Massachusetts**

| Period   | Year | Winter Intrazonal | Winter Interzonal | Summer Intrazonal | Summer Interzonal |
| -------- | ---- | ----------------- | ----------------- | ----------------- | ----------------- |
| Off-peak | 2024 | $18.41            | $18.25            | $6.19             | $5.89             |
| Off-peak | 2025 | $28.79            | $28.73            | $9.98             | $9.52             |
| Off-peak | 2026 | $29.04            | $29.07            | $10.00            | $9.60             |
| Off-peak | 2027 | $23.08            | $28.27            | $7.80             | $9.22             |
| Off-peak | 2028 | $23.09            | $28.05            | $8.10             | $9.45             |
| Off-peak | 2029 | $22.05            | $26.27            | $7.81             | $9.00             |
| Off-peak | 2030 | $20.51            | $25.00            | $7.56             | $9.00             |
| Off-peak | 2031 | $19.85            | $26.73            | $7.47             | $9.88             |
| Off-peak | 2032 | $16.77            | $22.28            | $6.87             | $8.98             |
| Off-peak | 2033 | $14.19            | $18.56            | $6.21             | $7.98             |
| Off-peak | 2034 | $9.83             | $12.69            | $4.43             | $5.60             |
| On-peak  | 2024 | $20.94            | $20.61            | $10.38            | $9.69             |
| On-peak  | 2025 | $32.86            | $32.54            | $16.91            | $15.81            |
| On-peak  | 2026 | $33.02            | $32.83            | $17.28            | $16.22            |
| On-peak  | 2027 | $26.16            | $31.87            | $13.35            | $15.46            |
| On-peak  | 2028 | $25.96            | $31.41            | $13.40            | $15.56            |
| On-peak  | 2029 | $25.01            | $29.69            | $13.07            | $14.92            |
| On-peak  | 2030 | $23.68            | $28.62            | $12.87            | $15.05            |
| On-peak  | 2031 | $22.79            | $30.64            | $12.81            | $16.69            |
| On-peak  | 2032 | $20.02            | $26.51            | $11.88            | $15.33            |
| On-peak  | 2033 | $16.88            | $22.04            | $10.45            | $13.33            |
| On-peak  | 2034 | $11.52            | $14.87            | $7.45             | $9.42             |

Note: Values differ across states because states vary in terms of size of unhedged electricity demand.

Table 106 provides the levelized value for energy DRIPE installed in each state, broken down between the value of price reductions in the state of installation (intrazonal) and in the Rest-of-Pool (interzonal). Intrazonal and interzonal values may be added to determine the total DRIPE effect. DRIPE values are broadly similar to those observed in AESC 2021 due to similarities in the DRIPE price shift component. Other factors that play a role in differences in DRIPE values include changes in energy prices (which are linked to changes in gas prices, clean energy deployment, and load), changes in load, and changes in hedging assumptions.

[PDF p. 260 | printed p. 242]

**Table 106. Seasonal energy DRIPE values for measures installed in 2024 (2024 $ per MWh)**

| Type       | Season | Period   | CT     | MA     | ME     | NH     | RI     | VT     |
| ---------- | ------ | -------- | ------ | ------ | ------ | ------ | ------ | ------ |
| Intrazonal | Summer | On-Peak  | $4.63  | $9.71  | $2.33  | $2.57  | $1.49  | $0.14  |
| Intrazonal | Summer | Off-Peak | $2.69  | $5.72  | $1.49  | $1.56  | $0.84  | $0.09  |
| Intrazonal | Winter | On-Peak  | $8.34  | $18.03 | $5.05  | $5.14  | $2.62  | $0.32  |
| Intrazonal | Winter | Off-Peak | $7.15  | $15.72 | $4.61  | $4.51  | $2.24  | $0.28  |
| Interzonal | Summer | On-Peak  | $16.44 | $10.87 | $18.65 | $18.34 | $19.45 | $20.66 |
| Interzonal | Summer | Off-Peak | $9.82  | $6.49  | $10.97 | $10.86 | $11.59 | $12.26 |
| Interzonal | Winter | On-Peak  | $31.50 | $20.90 | $34.65 | $34.42 | $36.99 | $39.01 |
| Interzonal | Winter | Off-Peak | $27.66 | $18.30 | $30.10 | $30.06 | $32.37 | $34.09 |

Note: Values shown are levelized over 15 years for Counterfactual #1.

## 9.3. Electric capacity DRIPE

This section describes our methodology and assumptions for capacity market DRIPE effects. If the capacity market were in equilibrium, and all the marginal sources of capacity had similar cost characteristics, reducing demand or adding capacity would not have much effect on capacity price. This observation is largely borne out by observations in the most recent capacity auctions (see discussion in Chapter 5: _Avoided Capacity Costs_). However, when looking out over the past 5–10 auctions, we observe that the marginal sources of capacity do seem to vary in price. The bid prices for individual units appear to have declined over time, as well. Hence, the clearing price of capacity continues to be sensitive to the amount of energy efficiency resources cleared in the FCM, and to the effect of uncleared energy efficiency resources on demand.[^304] As a result, we can be certain that capacity price effects are both real and material.

AESC estimates two varieties of capacity DRIPE effects:

- Cleared DRIPE benefits, which are benefits of measures that clear in the ISO New England FCM
- Uncleared DRIPE benefits, which are benefits of measures that are not submitted into or otherwise do not clear in the ISO New England FCM

This section describes the methodology we use to calculate both types of capacity DRIPE. We begin with a discussion of price shifts, then describe for which components of regional demand these price shifts are eligible for application, then describe the methodologies for calculating benefits in the two categories of capacity DRIPE.

[^304]: FCM prices will be determined to a large extent by the prices at which existing resources choose to delist. By delisting, existing resources in New England are able to: (1) sell into another market such as New York, (2) shut down, or (3) operate in the energy market without obligations in the capacity market. New resources can defer implementation or operate in the energy market. Resources that do not clear in one FCA can bid into the subsequent auctions, including Annual Reconfiguration Auctions, or sell capacity bilaterally, such as to assume the capacity obligation of a resource that cleared.

[PDF p. 261 | printed p. 243]

### Calculating price shifts in the capacity market

The “price shift” of capacity refers to how much the price of capacity (measures [sic] in $/kW-year per MW) changes in response to changes in demand. As in past AESC studies, for years utilizing the current capacity market structure (i.e., 2027 and prior years), we estimate price shifts for future years using the slope of the most recent capacity market auction (in the case of AESC 2024, this is FCA 17, conducted in February 2023), shifted to reflect the change in supply capacity that has occurred since that auction.

As an example, Figure 56 depicts the five known datapoints for supply and price in FCA 15.[^305] The line segment between each one of these points has a slope, which is effectively the price shift used in AESC 2021. Depending on where demand crosses the supply curve, the clearing price will have a different associated price shift. For example, in Figure 56, demand in Year 1 and Year 2 will produce the same price shift. Demand in Year 3, however, crosses at a different line segment and will yield a different price shift. Practically speaking, the shallower the line segment, the lower the price shift’s value is. Conversely, steeper line segments produce higher price shifts. See Table 107 for our estimates of the price shifts for each counterfactual.

**Figure 56. Supply curve for FCA 15 with illustrative demand lines**

[DIAGRAM DESCRIPTION: Figure 56. Supply curve for FCA 15 with illustrative demand lines]

A line graph of an auction supply curve with three vertical dashed demand lines. The x-axis is "Supply (MW)", running from 34,500 to 38,000 (ticks every 500 MW); the y-axis is "Price (2021 $/kW-month)", running from $0 to $12 (ticks every $2). Five red dots connected by a black line mark the known FCA 15 supply/price points, labeled (a) through (e) from left to right: (a) at about 35,000 MW and about $2.4; (b) at about 35,700 MW and about $2.8; (c) at about 37,100-37,200 MW and about $4.0; (d) at about 37,350 MW and about $6.9; (e) at about 37,600 MW and about $9.7. The curve is shallow between (a), (b) and (c) (rising only from about $2.4 to about $4), then very steep between (c), (d) and (e). Three dashed teal vertical lines are labeled "Demand, Year 1" (at about 36,000 MW), "Demand, Year 2" (at about 36,500 MW) and "Demand, Year 3" (at about 37,100 MW, just left of point (c) so that it crosses the steep part of the curve). Years 1 and 2 cross the same shallow segment between (b) and (c) and so share a price shift; Year 3 crosses a steeper segment and has a larger price shift. Values are read approximately from the rendered chart.

Note: Demand lines are illustrative and do not represent actual or projected demand in any year.

[→ See original PDF page 261 for visual rendering]

[^305]: ISO New England. Last accessed March 11, 2021. _Forward Capacity market (FCA 15) Result_. Available at [https://www.iso-ne.com/static-assets/documents/2018/05/fca-results-report.pdf](https://www.iso-ne.com/static-assets/documents/2018/05/fca-results-report.pdf).

[PDF p. 262 | printed p. 244]

**Table 107. Price shifts for capacity DRIPE (2024 $/kW-month per MW) in Rest-of-Pool region for current market structure**

| Year | FCA | CF# 1     | CF# 2     | CF# 3     | CF# 4     | CF# 5     | CF# 6     |
| ---- | --- | --------- | --------- | --------- | --------- | --------- | --------- |
| 2024 | 15  | $0.00062  | $0.00062  | $0.00062  | $0.00062  | $0.00062  | $0.00062  |
| 2025 | 16  | $0.00001  | $0.00001  | $0.00001  | $0.00001  | $0.00001  | $0.00001  |
| 2026 | 17  | <$0.00001 | <$0.00001 | <$0.00001 | <$0.00001 | <$0.00001 | <$0.00001 |
| 2027 | 18  | <$0.00001 | <$0.00001 | <$0.00001 | <$0.00001 | <$0.00001 | <$0.00001 |

Notes: Data on clearing prices for other counterfactuals and regions can be found in the _AESC 2024 User Interface_.

Under the new market structure (effective in 2028 and for all later years), we estimate price shifts based on the slopes of the demand curve and the modeled supply curve in the EnCompass model (see Table 108. [sic: no closing parenthesis in source] Given the slopes of these curves at the capacity market clearing point, we calculate how much the price of capacity would change in response to a 1 MW change in accredited energy efficiency capacity shifting the supply curve right by participating in the market (cleared) or shifting the demand curve left by reducing the load forecast (uncleared). Note the change in units in Table 108, relative to Table 107; because these prices represent the addition of any summer and winter values, it is more intuitive to approach them from an entire-year perspective, rather than a month-by-month perspective.

In general, price shifts tend to be higher in years and in counterfactuals with higher capacity prices, as both trends (high capacity prices and large price shifts) are indicators of a tight capacity market.

**Table 108. Price shifts for capacity DRIPE (2024 $/kW-month per MW) in Rest-of-Pool region for new market structure**

| Year | FCA | CF# 1    | CF# 2    | CF# 3    | CF# 4    | CF# 5    | CF# 6    |
| ---- | --- | -------- | -------- | -------- | -------- | -------- | -------- |
| 2028 | 19  | $0.00057 | $0.00059 | $0.00034 | $0.00367 | $0.00042 | $0.01111 |
| 2029 | 20  | $0.00056 | $0.00082 | $0.00092 | $0.00902 | $0.00526 | $0.01089 |
| 2030 | 21  | $0.00071 | $0.00117 | $0.00156 | $0.00998 | $0.00593 | $0.00927 |
| 2031 | 22  | $0.00070 | $0.00075 | $0.00140 | $0.00515 | $0.00055 | $0.00958 |
| 2032 | 23  | $0.00045 | $0.00365 | $0.01036 | $0.00954 | $0.00579 | $0.00819 |
| 2033 | 24  | $0.00057 | $0.00334 | $0.00457 | $0.00267 | $0.00583 | $0.00366 |
| 2034 | 25  | $0.01235 | $0.00106 | $0.00534 | $0.01504 | $0.00093 | $0.00694 |
| 2035 | 26  | $0.00043 | $0.00156 | $0.00190 | $0.00621 | $0.00255 | $0.00170 |
| 2036 | 27  | $0.00054 | $0.00408 | $0.00030 | $0.00039 | $0.00146 | $0.00556 |
| 2037 | 28  | $0.01166 | $0.00141 | $0.01041 | $0.00731 | $0.00416 | $0.00567 |
| 2038 | 29  | $0.01185 | $0.00132 | $0.00079 | $0.00588 | $0.00759 | $0.00388 |

Notes: Data on clearing prices for other counterfactuals and years can be found in the _AESC 2024 User Interface_.

During both capacity periods, the Rest-of-Pool price shift is used to estimate Rest-of-Pool capacity DRIPE impacts, except in cases where price separation occurs. See the next section for more information on these special cases.

#### Price separation

In two near-term years (FCA 15 and 16), AESC 2024 accounts for price separation. In these years, the auction had concluded prior to this study taking place. The results of both these auctions produced price separation in three regions. As they are modeled in AESC 2024, these regions include Northern New

[PDF p. 263 | printed p. 245]

England (Maine, New Hampshire, and Vermont), Southeast New England (SEMA, NEMA, and Rhode Island), and Rest-of-Pool (WCMA and Connecticut). In both of these years, the Northern New England region cleared at a price slightly lower than the Rest-of-Pool price, owing to it being export-constrained. Conversely, in both of these years, the Southeast New England region cleared at a price higher than the Rest-Of-Pool price, owing to it being import-constrained.

Due to limited available information on the auction supply curves of these three regions, we apply a different approach for estimating price shifts in these cases. First, to estimate the Rest-of-Pool price shift, we use the same methodology described in the above section, but incorporate the quantity of energy efficiency installed in just the Rest-of-Pool region to determine the price shift. Second, to estimate the price shifts in each of the other two regions, we examine how prices would have been different in each of these regions if the quantity of energy efficiency installed in these regions had been different by looking at the MRI curve specific to that region and auction.[^306] Then, we evaluate the difference in prices between the actual clearing price and the second hypothetical clearing price, and divide the result by the quantity of energy efficiency modeled in that region. This produces a dollar-per-kW-month price shift for each price-separated region.

Table 109 summarizes the results of these estimations. We observe that the estimated price shifts for Northern New England and Southeast New England are between 1.6 and 60 times higher than the Rest-of-Pool price shift, depending on the year. In particular, we observe that the estimated price shift for Southeast New England in FCA 15 is a particularly large one, especially compared to other observed price shifts in the period for which conducted auction data is available.[^307] This produces zone-on-zone capacity DRIPE values for FCA 15 (study year 2024, as modeled in FCA 2024 [sic]) to be unusually high, compared to other years.

Modeled capacity DRIPE values in FCA 15 and FCA 16 are assigned to the six states as follows: first, Maine, New Hampshire, and Vermont all inherit the Northern New England value. Second, Connecticut inherits the Rest-of-Pool value. Third, Rhode Island inherits the Southeast New England value. Fourth, Massachusetts inherits a weighed [sic] average blend of the Rest-of-Pool and Southeast New England values, based on the projected summer peak values of its three constituent regions (WCMA, NEMA, and SEMA). Each region (Northern New England, Southeast New England, and Rest-of-Pool) is segmented into their own modeled capacity region. Zone-on-zone and zone-on-region DRIPE effects are then estimated independently for each of the three regions.

Because of a lack of information suggesting otherwise, we do not model price separation in any other years.

[^306]: ISO New England publishes subregional MRI curves for auctions with price separation, but not supply curve results.

[^307]: More specifically, while variations in price shifts of these estimated magnitudes are not unusual (see Table 107 and Table 108) a price shift with a value above $0.001/kW-month per MW is unusual.

[PDF p. 264 | printed p. 246]

**Table 109. Price shifts in price-separated auctions (2024 $/kW-month per MW)**

| Price-separated region | FCA 15   | FCA 16   |
| ---------------------- | -------- | -------- |
| Northern New England   | $0.00099 | $0.00037 |
| Southeast New England  | $0.00620 | $0.00039 |
| Rest-of-Pool           | $0.00062 | $0.00001 |

Note: All counterfactuals utilize the same set of price shifts.

### Calculating capacity DRIPE

Price shifts are described in units of dollars-per-kW-month per MW (effectively, price per demand). To allow application of these numbers to any generic change in demand (e.g., from an energy efficiency measure), we multiply these values by the projected demand.

We calculate demand using two different sets of numbers. First, using the EnCompass model, we project future demand for each state and the region as a whole given the inputs described in Chapter 4: _Common Electric Assumptions_ and the methods described in Chapter 5: _Avoided Capacity Costs_. Second, we multiply this by the fraction of demand that is unhedged. Unhedged demand is the quantity of electricity that has not already been procured ahead of time and is thus subject to changes in the capacity market prices.

The unhedged percentage varies by state. Vermont utilities are vertically integrated and own (or have under long-term contract) a large portion of their capacity requirements. The same is also true for municipal utilities. The Connecticut utilities have contracts for differences with a number of generators built to relieve a transmission constraint, and all the restructured states have some legacy contracts and/or small post-restructuring contracts that provide capacity. In general, the long-term purchase of capacity has fallen out of favor, even where the utilities are purchasing energy long term.[^308] For Vermont, we estimate hedged demand percentages based on data from the most recently available Green Mountain Power IRP, and we assume hedged demand share in the rest of the state is similar.[^309] Specific data on hedged capacity for other states is less available. We rely on capacity contracts as published in FERC Form 1 and we assume half of all remaining vertically integrated demand is hedged as a proxy for the above-mentioned dynamics.

Table 110 describes the resulting unhedged capacity demand assumptions for Counterfactual #1. See the _AESC 2024 User Interface_ for detail on all counterfactuals.

[^308]: In addition, the generation-supply offers by the utilities, municipal aggregators, and third-party marketers provide short-term price certainty for a sizable portion of load. By the time those rates are locked in, the capacity price is generally known. For the small percentage of power-supply contracts for more than three years into the future, the capacity component is generally subject to market adjustment. Hence, retail power-supply contracts have little if any value in hedging capacity price risk.

[^309]: Green Mountain Power 2021, "2021 Integrated Resource Plan." Figure 7-5. Accessed December 18, 2023. Available at [https://greenmountainpower.com/wp-content/uploads/2021/12/2021-Integrated-Resource-Plan.pdf](https://greenmountainpower.com/wp-content/uploads/2021/12/2021-Integrated-Resource-Plan.pdf).

[PDF p. 265 | printed p. 247]

**Table 110. Unhedged capacity for Counterfactual #1 (MW)**

| Year | ISO    | CT    | MA     | ME    | NH    | RI    | VT  |
| ---- | ------ | ----- | ------ | ----- | ----- | ----- | --- |
| 2024 | 22,823 | 5,311 | 11,154 | 2,081 | 2,305 | 1,847 | 125 |
| 2025 | 23,608 | 5,371 | 11,445 | 2,076 | 2,330 | 1,904 | 482 |
| 2026 | 23,739 | 5,338 | 11,596 | 2,076 | 2,320 | 1,924 | 486 |
| 2027 | 25,381 | 5,654 | 12,521 | 2,187 | 2,434 | 2,064 | 520 |
| 2028 | 22,954 | 4,971 | 11,475 | 1,968 | 2,189 | 1,878 | 473 |
| 2029 | 23,578 | 5,075 | 11,823 | 2,021 | 2,239 | 1,934 | 487 |
| 2030 | 24,887 | 5,901 | 12,150 | 2,071 | 2,281 | 1,985 | 499 |
| 2031 | 25,014 | 5,861 | 12,264 | 2,085 | 2,293 | 2,007 | 504 |
| 2032 | 25,821 | 6,016 | 12,701 | 2,171 | 2,346 | 2,066 | 521 |
| 2033 | 25,926 | 6,044 | 12,560 | 2,246 | 2,435 | 2,073 | 568 |
| 2034 | 26,950 | 6,145 | 13,363 | 2,295 | 2,437 | 2,163 | 548 |
| 2035 | 27,540 | 6,231 | 13,697 | 2,354 | 2,485 | 2,210 | 563 |
| 2036 | 27,351 | 6,222 | 13,524 | 2,348 | 2,531 | 2,137 | 589 |
| 2037 | 28,114 | 6,143 | 14,086 | 2,470 | 2,575 | 2,214 | 627 |
| 2038 | 29,284 | 6,516 | 14,627 | 2,520 | 2,658 | 2,351 | 613 |
| 2039 | 29,204 | 6,320 | 14,649 | 2,574 | 2,699 | 2,301 | 661 |
| 2040 | 30,294 | 6,664 | 15,149 | 2,615 | 2,787 | 2,434 | 645 |
| 2041 | 30,947 | 6,769 | 15,481 | 2,673 | 2,868 | 2,491 | 665 |
| 2042 | 30,712 | 6,624 | 15,420 | 2,679 | 2,957 | 2,335 | 698 |
| 2043 | 31,284 | 6,637 | 15,693 | 2,775 | 2,973 | 2,480 | 726 |
| 2044 | 31,533 | 6,944 | 15,650 | 2,715 | 3,067 | 2,439 | 719 |
| 2045 | 32,594 | 7,063 | 16,184 | 2,871 | 3,118 | 2,649 | 709 |
| 2046 | 32,877 | 7,136 | 16,291 | 2,918 | 3,135 | 2,683 | 713 |
| 2047 | 33,148 | 7,206 | 16,396 | 2,964 | 3,149 | 2,716 | 717 |
| 2048 | 32,664 | 6,970 | 16,176 | 3,002 | 3,124 | 2,640 | 753 |
| 2049 | 33,660 | 7,345 | 16,600 | 3,044 | 3,173 | 2,773 | 725 |
| 2050 | 33,174 | 7,337 | 16,300 | 2,965 | 3,205 | 2,617 | 750 |

Notes: Data on hedged values for other counterfactuals can be found in the AESC 2021 [sic] User Interface.

Price shifts and unhedged capacity quantities are two of the primary inputs used to estimate capacity DRIPE. The following sections describe the methodologies used to translate these values into (a) cleared capacity benefits and (b) uncleared capacity benefits.

#### Calculating cleared capacity DRIPE

AESC 2024, as with previous AESC studies, utilizes a decay schedule for cleared capacity DRIPE. This schedule describes how these effects phase in and phase out.

First, we assume all cleared measures have full DRIPE benefits in the first year they are installed. However, we assume that this effect does not last indefinitely. Over time, customers will respond to lower prices by using somewhat more energy, including at the peak. In addition, lower capacity prices may result in the retirement of some generation resources and termination of some demand-response resources, which will result in these resources being removed from the supply curve. Further, some new proposed resources that have not cleared for several auctions may be withdrawn (if, for example, contracts and approvals expire, raising the cost of offering the resource into future auctions). As a result, we assume that the effects of DRIPE fade out over time. Based on expert judgement, we use the same

[PDF p. 266 | printed p. 248]

assumption used in prior AESC studies, wherein the phase-out is linear over time, reaching an effect of zero in the seventh year. We assume that measures with shorter lifetimes use the same decay schedule, rather than a compressed decay schedule or some other alternative. This is because the phase-out of DRIPE effects is based on market dynamics, rather than the features of individual measures.

Table 111 shows the decay schedule used for cleared capacity measures installed in 2024. Measures installed in later years have the same decay schedule, but shifted by one or more years. This structure of decay does not change between the current modeled structure (2027 and prior years) and the new market structure (2028 and later years).

**Table 111. Decay schedule used for cleared capacity for measures installed in 2024**

| Year              | Decay | 1- Decay |
| ----------------- | ----- | -------- |
| 2024              | 0%    | 100%     |
| 2025              | 17%   | 83%      |
| 2026              | 33%   | 67%      |
| 2027              | 50%   | 50%      |
| 2028              | 67%   | 33%      |
| 2029              | 83%   | 17%      |
| 2030 through 2050 | 100%  | 0%       |

After calculating this decay schedule, we calculate cleared capacity DRIPE as using [sic] the formulas described in Equation 9 (for interzonal DRIPE) and Equation 10 (for intrazonal). Interzonal DRIPE is calculated by multiplying the price shift for a given year by the unhedged capacity quantity for a given state, by one minus the decay percentage for that year. Meanwhile, intrazonal DRIPE uses the exact same calculation, except for replacing the unhedged capacity quantity for the given state with the unhedged capacity quantity for the rest of the region (less the state in question).

**Equation 9. Calculation of interzonal (zone-on-zone) cleared capacity DRIPE**

$$\text{Capacity DRIPE}_{\text{Zone Z} \,|\, \text{Zone Z},\ \text{Period P}} = \left[ \text{Price Shift} \times \text{Hedged Capacity}_{\text{Zone Z, Period P}} \right] \times (1 - \text{Decay})$$

**Equation 10. Calculation of intrazonal (zone-on-Rest-of-Pool) cleared capacity DRIPE**

$$\text{Capacity DRIPE}_{\text{ROP} \,|\, \text{Zone Z},\ \text{Period P}} = \left[ \text{Price Shift} \times \left( \text{Hedged Capacity}_{\text{ISO, Period P}} - \text{Hedged Capacity}_{\text{Zone Z, Period P}} \right) \right] \times (1 - \text{Decay})$$

_Extractor note (not source text): the equations are printed with the terms "Hedged Capacity", while the surrounding text describes the quantity as "unhedged capacity". Equation 9 is labeled "interzonal (zone-on-zone)" and Equation 10 "intrazonal (zone-on-Rest-of-Pool)", whereas elsewhere in this chapter zone-on-zone is called intrazonal and zone-on-Rest-of-Pool is called interzonal; the source's own labels are kept as printed. The "Decay" column of Table 111 is the share of the benefit that has faded out (the factor $(1-\text{Decay})$ is applied to the value)._

Table 112 shows cleared capacity DRIPE for each region for measures installed in 2024. In years with price separation, we use the Rest-of-Pool price shift to estimate Rest-of-Pool capacity DRIPE impacts,

[PDF p. 267 | printed p. 249]

regardless of whether a given region has price-separated in a particular auction.[^310] Capacity DRIPE values can vary widely year-to-year, based on the price shift produced by the model (e.g., a price shift change of an order of magnitude between years will yield approximately an order of magnitude difference in terms of cleared capacity DRIPE). This is the principle [sic] driver behind the differences in capacity DRIPE values in AESC 2021 and AESC 2024.

**Table 112. Cleared capacity DRIPE by year for measures installed in 2024 (2024 $ per kW-year)**

| Year              | Zone-on-Zone CT | Zone-on-Zone MA | Zone-on-Zone ME | Zone-on-Zone NH | Zone-on-Zone RI | Zone-on-Zone VT | Zone on Rest-of-Region CT | Zone on Rest-of-Region MA | Zone on Rest-of-Region ME | Zone on Rest-of-Region NH | Zone on Rest-of-Region RI | Zone on Rest-of-Region VT |
| ----------------- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| 2024              | $39             | $83             | $25             | $27             | $137            | $1              | $130                      | $87                       | $145                      | $142                      | $32                       | $168                      |
| 2025              | $0              | $1              | $8              | $9              | $7              | $2              | $1                        | $1                        | $0                        | $0                        | $0                        | $0                        |
| 2026              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2027              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2028              | $0              | $0              | $0              | $0              | $0              | $0              | $41                       | $26                       | $48                       | $47                       | $48                       | $51                       |
| 2029              | $0              | $0              | $0              | $0              | $0              | $0              | $21                       | $13                       | $25                       | $24                       | $25                       | $26                       |
| 2030              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2031              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2032              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2033              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2034              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2035              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2036              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2037              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2038              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 15-year levelized | $3              | $6              | $2              | $3              | $11             | $0              | $14                       | $9                        | $16                       | $16                       | $7                        | $18                       |

#### Calculating uncleared capacity DRIPE

Measures that are not bid into or do not clear the FCM also generate capacity DRIPE benefits, albeit with different timing and of different magnitudes.[^311] We calculate capacity DRIPE for uncleared resources analogously to that of cleared resources, but we adjust the decay schedule and market clearing prices to reflect different market features.

To calculate uncleared capacity DRIPE, we utilize a modified version of the same phase-in / phase-out schedule described above in Section 5.2: _Uncleared capacity calculations_. As with uncleared capacity, we assume that uncleared capacity DRIPE effects do not appear until several years after a measure is installed (five years when discussing measure impacts prior to 2028, and three years when discussing measure impacts that accrue in 2028 and later years), and that they persist at various magnitudes and

[^310]: In some circumstances, this yields a negative rest-of-region DRIPE effect, because the in-zone impacts are larger than the Rest-of-Pool impacts. In these circumstances, we assume a zero value for rest-of-region capacity DRIPE.

[^311]: These measures include energy efficiency measures that program administrators choose to not bid into the market due to administrative burden, demand response or load management measures that do not clear the capacity market but are nonetheless built for policy reasons, or building electrification measures which may produce demand increases (and therefore “negative savings").

[PDF p. 268 | printed p. 250]

lengths of time depending on the measure’s lifetime. However, uncleared capacity DRIPE differs in that we also assume that DRIPE effects decay over time, following the same decay schedule described in Table 111.

As with uncleared capacity, the calculations of uncleared capacity DRIPE also utilize estimates of reserved margin and scaling factors (also described above in Section 5.2: _Uncleared capacity calculations_).

To estimate uncleared capacity DRIPE, we use the following calculations:

- For intrazonal (zone-on-zone) uncleared capacity DRIPE in a particular state and year, we calculate the product of (a) the state’s unhedged demand, (b) the price shift for that year, (c) the effect-and-decay schedule that matches the measure’s lifetime, and (d) the scaling factor, if relevant. Unlike cleared capacity DRIPE, this value is then multiplied by one plus the reserve margin to reflect the fact that since the measure is uncleared, it is capable of avoiding some reserve margin.[^312]
- For interzonal (zone-on-Rest-of-Pool) uncleared capacity DRIPE for a particular state and year, we calculate the product of (a) regional unhedged demand minus the state’s unhedged demand, (b) the price shift for that year, (c) the effect-and-decay schedule that matches the measure’s lifetime, and (d) the scaling factor, if relevant. This value is then multiplied by one plus the reserve margin.

Table 113 [source says "Table 112"] shows uncleared capacity DRIPE for each region for measures installed in 2024, assuming a measure life of 10 years. As with cleared capacity DRIPE, uncleared capacity DRIPE values can vary widely year-to-year, based on the price shift produced by the model (e.g., a price shift change of an order of magnitude between years will yield approximately an order of magnitude difference in terms of cleared [sic] capacity DRIPE). Compared to cleared capacity DRIPE, uncleared capacity DRIPE values tend to be higher, but accrue later. This is due to higher capacity prices—and associated capacity price shifts—forecasted for the mid to long term.

[^312]: As the measure is uncleared, it is effectively “counted” in the demand side of the capacity auction (i.e., within the load forecast). In contrast, measures that are cleared are effectively treated the same as conventional power plants (i.e., supply), and through the auction effectively require the purchase of some extra amount of capacity to act as a reserve margin.

[PDF p. 269 | printed p. 251]

**Table 113. Uncleared capacity DRIPE by year for measures installed in 2024 (2024 $ per kW-year)**

| Year              | Zone-on-Zone CT | Zone-on-Zone MA | Zone-on-Zone ME | Zone-on-Zone NH | Zone-on-Zone RI | Zone-on-Zone VT | Zone on Rest-of-Region CT | Zone on Rest-of-Region MA | Zone on Rest-of-Region ME | Zone on Rest-of-Region NH | Zone on Rest-of-Region RI | Zone on Rest-of-Region VT |
| ----------------- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| 2024              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2025              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2026              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2027              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2028              | $20             | $47             | $8              | $9              | $8              | $2              | $74                       | $47                       | $86                       | $85                       | $86                       | $92                       |
| 2029              | $23             | $53             | $9              | $10             | $9              | $2              | $83                       | $53                       | $97                       | $96                       | $97                       | $104                      |
| 2030              | $30             | $63             | $11             | $12             | $10             | $3              | $98                       | $66                       | $118                      | $117                      | $118                      | $126                      |
| 2031              | $22             | $45             | $8              | $8              | $7              | $2              | $70                       | $47                       | $84                       | $84                       | $85                       | $90                       |
| 2032              | $9              | $18             | $3              | $3              | $3              | $1              | $28                       | $19                       | $34                       | $34                       | $34                       | $36                       |
| 2033              | $6              | $13             | $2              | $2              | $2              | $1              | $20                       | $14                       | $24                       | $24                       | $24                       | $26                       |
| 2034              | $60             | $130            | $22             | $24             | $21             | $5              | $202                      | $132                      | $240                      | $238                      | $241                      | $257                      |
| 2035              | $1              | $1              | $0              | $0              | $0              | $0              | $2                        | $1                        | $2                        | $2                        | $2                        | $2                        |
| 2036              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2037              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 2038              | $0              | $0              | $0              | $0              | $0              | $0              | $0                        | $0                        | $0                        | $0                        | $0                        | $0                        |
| 15-year levelized | $11             | $24             | $4              | $5              | $4              | $1              | $38                       | $25                       | $45                       | $45                       | $45                       | $48                       |

Note: This chart [sic] assumes a measure life of 10 years. Measures with other measure lives will have completely different uncleared capacity DRIPE effects. See the _AESC 2024 User Interface_ for more information.

#### <u>Important caveats for applying uncleared capacity DRIPE values</u>

Uncleared capacity DRIPE is different than many other avoided cost categories. Because uncleared capacity DRIPE describes an effect that fades out over time due to the market’s responses to that effect, users should sum avoided costs over the entire study period, regardless of any one measure’s lifetime. For example, the avoided costs of a 1 MW measured [sic] installed in 2024 would be equal to the sum of the values from 2024 through 2058, regardless of whether that measure had a 1-year measure life or a 30-year measure life.[^313]

Uncleared resources affect the load forecast only to the degree that these resources provide load reductions on the hours used in the load forecast regression. Some resources—such as demand response resources—may be active only on one or some of the hours used in the load forecast. As a result, these resources would provide a diminished uncleared capacity benefit. We recommend that program administrators apply a scaling factor to the benefits detailed in Table 113 to account for this effect. See _Appendix K: Scaling Factor for Uncleared Resources_ for more information on how this scaling factor is calculated and how it can be applied. Because we expect ISO New England’s use of the load regressions used for each individual year to be unchanged under the new market structure, we determine that the scaling effects described in _Appendix K: Scaling Factor for Uncleared Resources_ can be applied to benefits accruing under both the current market structure and the assumed new market structure that is effective in 2028.

[^313]: We note that this is the same approach used for summing avoided costs for uncleared capacity and uncleared capacity DRIPE, but no other avoided cost categories.

[PDF p. 270 | printed p. 252]

## 9.4. Natural gas DRIPE

Just as reducing electric load reduces electric energy prices, reducing natural gas usage reduces demand for natural gas in producing regions and therefore reduces the market price of that natural gas supply. This natural gas price reduction effect is natural gas DRIPE. The price for natural gas—and associated benefits—can be broken into two components:

1. The supply component, determined by North American demand and supply conditions on a largely annual basis.
2. Transportation costs or “basis,” determined by contract prices for LDCs and by the balance of regional demand and supply (mostly from pipelines) on a daily and seasonal basis for other users, especially electric generators.

Importantly, only the supply component of natural gas DRIPE is used in cost-effectiveness screening of gas measures. This is because LDCs and most other suppliers of gas to the end use rely primarily on firm long-term contracts for pipeline and storage capacity to allow for delivery of natural gas. As a result, the basis DRIPE effect benefits only electric customers.

### Natural gas supply DRIPE

This section focuses on the calculation of natural gas supply DRIPE. This is the DRIPE effect applied to end-use measures that produce natural gas savings.

#### Calculating elasticities

Elasticity describes how prices of a commodity respond to changes in demand. As in AESC 2021, AESC 2024 relies on a calculation of the implied response of natural gas prices to supply changes observed in different scenarios modeled in EIA’s AEO 2023.

Figure 57 compares annual data points from AEO 2023. Each data point represents the difference in both prices and demand for one AEO side-scenario relative to the price and demand for natural gas in the AEO 2023 Reference case for the same year. This figure includes datapoints from four different AEO side-scenarios: the High economic growth, Low economic growth, High Zero-Carbon Technology Cost, and Low Zero-Carbon Technology Cost. This analysis encompasses all years from 2022 through 2050. A linear regression of this dataset provides a slope that indicates how changes in price are related to changes in demand.

Overall, we find that reducing demand by one quadrillion Btu reduces EIA’s estimate of the market price by $0.067 per MMBtu in 2024 dollars. This is about three-quarters of the AESC 2021 value of $0.094/MMBtu per quadrillion Btu/year (in 2024 dollars).

[PDF p. 271 | printed p. 253]

**Figure 57. Effect of changing gas demand on gas price**

[DIAGRAM DESCRIPTION: Figure 57. Effect of changing gas demand on gas price]

A scatter plot with a linear trend line. The x-axis is "Change in Demand (Quadrillion Btu per year)", running from -6.0 to 4.0 in steps of 2.0 (axis range extends beyond the data on the left); the y-axis is "Change in Price (2024 $ per MMBtu)", running from -$0.50 to $0.50 in steps of $0.10, with a horizontal zero line and a vertical zero line at a change in demand of 0.0. About 100 blue dots, one per year per AEO 2023 side-scenario (relative to the Reference case), span roughly -4.1 to +3.4 quadrillion Btu on the x-axis. Most points cluster between about -2.5 and +3.4 quadrillion Btu, with price changes mostly between about -$0.15 and +$0.38; a few outlying points at the far left reach about -$0.42 (at about -4.1 quadrillion Btu), -$0.35 and -$0.30. A red upward-sloping regression line runs from about -$0.25 at -4.0 quadrillion Btu to about +$0.26 at +3.4 quadrillion Btu and is labeled "y = 0.0673x + 0.0275" and "R² = 0.6822". The slope, about $0.067 per MMBtu per quadrillion Btu, is the natural gas supply price shift used in this chapter: lower demand lowers price and higher demand raises it.

Note: Deltas compare annual prices and demand in four AEO 2023 scenarios versus the AEO 2023 Reference case.

[→ See original PDF page 253 for visual rendering]

#### Calculating natural gas supply DRIPE

As with electricity DRIPE effects, the price reduction per MMBtu saved is a very small portion of the price per MMBtu, but each MMBtu saved reduced prices for a very large number of MMBtus. According to AEO 2023, each year, New England is expected to consume about 0.6 quadrillion Btu for non-electric uses.[^314] Multiplying this quantity by the price shift ($0.067/MMBtu per quadrillion Btu) yields a natural gas supply DRIPE effect of $0.04 per MMBtu. The quantity of gas consumed for non-electric uses changes over time, and among states. Between 2024 and 2050, AEO 2023 estimates that non-electric gas demand will increase by about 6 percent. Demand in each state is projected based on recent historical observations from 2016 through 2021. Vermont, for example, is projected to consume about 0.01 quadrillion Btu while Massachusetts is projected to consume about 0.3 quadrillion Btu. These differences yield different DRIPE effects for each state.

We do not expect any decay in gas DRIPE; benefits should continue as long as the efficiency measure continues to reduce load. In contrast to intra‐month price variation driving the electric energy DRIPE, the studies and AEO gas-price forecasts reflect the full long‐term costs of gas development (at least after the first few years), not just the operation of existing wells. In addition, gas supply DRIPE is measuring

[^314]: Gas supply DRIPE is applied to gas efficiency measures which displace consumption of gas that has been purchased by LDCs. As a result, we use non-electric consumption for this calculation.

[PDF p. 272 | printed p. 254]

the effect of demand on the marginal cost of extraction for a finite resource. If anything, lower gas usage in 2024 will leave more low‐cost gas in the ground to meet demand in 2025, causing the DRIPE effect to accumulate over time.

However, we do assume that only a portion of consumption is responsive to DRIPE as a result of short-term contracts for gas. In Year 1, we assume that half of all gas demand is tied up in short-term contracts and is thus not impacted by DRIPE effects. This decreases to 20 percent in Year 2 and is assumed to fade away entirely in Year 3. Table 114 describes this impact schedule for measures installed in 2024. Measures installed in subsequent years would see these values shifted by one or more years. This is the same assumption used for short-term energy contracts for energy DRIPE (see Section 9.2: _Electric energy DRIPE_).

**Table 114. Share of demand that is responsive to natural gas supply DRIPE**

| Year           | Share of demand <u>not</u> impacted by DRIPE | Share of demand impacted by DRIPE |
| -------------- | -------------------------------------------- | --------------------------------- |
| 2024           | 50%                                          | 50%                               |
| 2025           | 20%                                          | 80%                               |
| 2026           | 0%                                           | 100%                              |
| …              | …                                            | …                                 |
| 2038 and later | 0%                                           | 100%                              |

Note: Values shown are for measures installed in 2024. Measures installed in 2025 would see these effects shifted by one year, measures installed in 2026 would see these effects shifted by two years, and so on.

#### Natural gas supply DRIPE values

Table 115 depicts the value of demand reduction for each state. We calculate this by obtaining the product of (a) the price shift (in 2024 $/MMBtu per quadrillion Btu), (b) the state’s non-electric natural gas consumption, and (c) the share of demand that is responsive to natural gas supply effects.[^315] Table 115 also shows the DRIPE effects for each state on the rest of the region. These values are calculated by subtracting the own-state value from the New England total in each year.

Using this table, we can see estimate [sic] the benefit for a reduction in gas use in each year. For example, a 1 MMBtu reduction in natural gas demand in 2025 yields a gas supply DRIPE benefit of $0.035 for New England as a whole. [source discrepancy: Table 115 prints $0.030 for "All" in 2025; $0.035 is the printed 15-year levelized value]

AESC 2024’s gas supply DRIPE estimates are lower than those found in AESC 2021, mostly due to lower price shift ($0.067/MMBtu per quadrillion Btu, down from $0.094/MMBtu per quadrillion Btu). Other changes are due to differences in historical gas consumption and projected gas consumption across the six states.

[^315]: Note that this consumption (and everything related to natural gas supply DRIPE) is independent of the natural gas price and avoided cost forecasts developed in Chapter 2: _Avoided Natural Gas Costs_.

[PDF p. 273 | printed p. 255]

**Table 115. Natural gas supply DRIPE benefit (2024 $ per MMBtu)**

| Year              | All   | Zone-on-Zone CT | Zone-on-Zone MA | Zone-on-Zone ME | Zone-on-Zone NH | Zone-on-Zone RI | Zone-on-Zone VT | Zone on Rest-of-Region CT | Zone on Rest-of-Region MA | Zone on Rest-of-Region ME | Zone on Rest-of-Region NH | Zone on Rest-of-Region RI | Zone on Rest-of-Region VT |
| ----------------- | ----- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| 2024              | 0.018 | 0.005           | 0.010           | 0.001           | 0.001           | 0.001           | 0.000           | 0.014                     | 0.008                     | 0.017                     | 0.018                     | 0.017                     | 0.018                     |
| 2025              | 0.030 | 0.007           | 0.016           | 0.002           | 0.001           | 0.002           | 0.001           | 0.022                     | 0.013                     | 0.028                     | 0.028                     | 0.027                     | 0.029                     |
| 2026              | 0.037 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.035                     | 0.034                     | 0.036                     |
| 2027              | 0.037 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.035                     | 0.034                     | 0.036                     |
| 2028              | 0.037 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.035                     | 0.034                     | 0.036                     |
| 2029              | 0.037 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.035                     | 0.034                     | 0.036                     |
| 2030              | 0.037 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.035                     | 0.034                     | 0.036                     |
| 2031              | 0.037 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.035                     | 0.034                     | 0.036                     |
| 2032              | 0.037 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.035                     | 0.034                     | 0.036                     |
| 2033              | 0.037 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.035                     | 0.035                     | 0.036                     |
| 2034              | 0.038 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.036                     | 0.035                     | 0.037                     |
| 2035              | 0.038 | 0.009           | 0.020           | 0.002           | 0.002           | 0.003           | 0.001           | 0.028                     | 0.017                     | 0.035                     | 0.036                     | 0.035                     | 0.037                     |
| 2036              | 0.038 | 0.009           | 0.021           | 0.002           | 0.002           | 0.003           | 0.001           | 0.029                     | 0.017                     | 0.035                     | 0.036                     | 0.035                     | 0.037                     |
| 2037              | 0.038 | 0.009           | 0.021           | 0.002           | 0.002           | 0.003           | 0.001           | 0.029                     | 0.017                     | 0.036                     | 0.036                     | 0.035                     | 0.037                     |
| 2038              | 0.038 | 0.009           | 0.021           | 0.002           | 0.002           | 0.003           | 0.001           | 0.029                     | 0.017                     | 0.036                     | 0.036                     | 0.035                     | 0.037                     |
| 15-year levelized | 0.035 | 0.009           | 0.019           | 0.002           | 0.002           | 0.003           | 0.001           | 0.027                     | 0.016                     | 0.033                     | 0.034                     | 0.033                     | 0.034                     |

Note: Values differ across states because states vary in terms of size of non-electric gas consumption.

### Natural gas basis DRIPE

Reductions in annual gas use will not only reduce the supply cost of natural gas, but also the basis. The basis is the price differential between the wholesale market price of gas in New England and the prices in the supply areas (sometimes called the “transportation” cost of natural gas). Since LDCs and most other suppliers of gas to the end use rely primarily on firm long-term contracts for pipeline and storage capacity to allow for delivery of natural gas, the basis DRIPE effect benefits only electric customers and is thus only used in G-E cross-DRIPE and below in E-G-E cross-DRIPE (see more below in Section 9.5: _Cross-fuel market price effects_).

#### Calculating elasticities

As in previous AESC studies, the majority of the price differential for natural gas in New England is assumed to be attributable to constraints on gas delivery capacity into New England from the Mid‐Atlantic region. As a result, our analysis focuses on the basis between the Texas Eastern Transmission Zone M‐3 (in Pennsylvania and New Jersey) and the Algonquin Gas Transmission citygates in Connecticut, Rhode Island, and eastern Massachusetts.[^316]

[^316]: To be clear, this calculation of DRIPE ignores effects from gas delivered to New England directly from Canada or from LNG.

[PDF p. 274 | printed p. 256]

Using data spanning three winters December 2020 through March 2023, we examine prices and demand for gas to determine price shifts over different periods of time.[^317] First, we utilize daily natural gas delivery data for the Algonquin Pipeline and Tennessee Gas Pipeline to determine the total amount of gas delivered to New England from the south.[^318] For each day, we calculate the aggregate surplus capacity for these two pipelines. Separately, we also estimate the price paid for gas flowing each day at both the TETCO M3 Hub and the Algonquin Citygate.[^319] The difference between these two values is the assumed basis for natural gas in New England.

Next, we assess a set of regressions of this surplus and basis data to determine what the price shift is at different times of the year. The slope of a linear regression describes the price shift. Table 116 describes the time periods and estimated price shifts. Note the use of two different “winter” periods and two different “summer” periods—one for electricity and one for gas. The seasonal assignments for the electric seasons are based on ISO New England’s definition, while the gas seasons are consistent with the analysis in Chapter 2: _Avoided Natural Gas Costs_.

**Table 116. Gas basis price shifts by season**

| Season           | Months included        | Basis price shift (2024 $/MMBtu per BBtu/day) |
| ---------------- | ---------------------- | --------------------------------------------- |
| Summer, electric | June through September | 0.00036                                       |
| Winter, electric | October through May    | 0.00447                                       |
| Summer, gas      | April through October  | 0.00032                                       |
| Winter, gas      | November through March | 0.00687                                       |
| Annual           | All months             | 0.00306                                       |

Over time, we assume that these basis price shifts decay as a result of a rebound effect (e.g., consumers using more gas given that it is cheaper), response of existing generation to price changes (i.e., gas units stay online longer and generate more electricity because of lower gas prices), and response of new generation to price changes (i.e., as prices remain low, there is less pressure to switch to newer, more efficient gas units). The combined effect of these drivers results in the decay schedule described in Table 117. Note that this schedule is for measures installed in 2024; measures installed in later years (e.g., 2025, 2026, and so on) use this same decay schedule but shifted by one year.

[^317]: We note that the time period analyzed for natural gas DRIPE purposes is narrower than the period evaluated for energy DRIPE purposes (i.e., three years versus five years). Reliance on this more limited dataset is due to data availability issues.

[^318]: Prices obtained from research performed by Natural Gas Intelligence (NGI). More details can be found at: [https://www.naturalgasintel.com/](https://www.naturalgasintel.com/)

[^319]: Prices obtained from Natural Gas Intelligence’s (NGI’s) “Daily” subscription service. More details on this service can be found at: [https://www.naturalgasintel.com/](https://www.naturalgasintel.com/).

[PDF p. 275 | printed p. 257]

**Table 117. Percent of gas basis decayed by year for measures installed in 2024**

| Year                         | Gas Basis Decay (%) |
| ---------------------------- | ------------------- |
| 2024                         | 1.3%                |
| 2025                         | 4.1%                |
| 2026                         | 6.8%                |
| 2027                         | 16.3%               |
| 2028                         | 25.4%               |
| 2029                         | 46.8%               |
| 2030                         | 67.0%               |
| 2031                         | 76.0%               |
| 2032                         | 84.5%               |
| 2033                         | 92.5%               |
| 2034 and all following years | 100.0%              |

We then apply these decay percentages to the price shifts described above. Table 118 shows the decayed basis values for a measure installed in 2024, with the supply gas DRIPE values (which are not decayed) for comparison. All values have been converted in to [sic] $/MMBtu per Quadrillion Btu terms, as these are otherwise very small numbers.

**Table 118. Decayed natural gas DRIPE values (2024 $/MMBtu per Quadrillion Btu reduced)**

| Year | Basis: Electricity Summer | Basis: Electricity Winter | Basis: Gas Summer | Basis: Gas Winter | Basis: Annual | Supply: Annual |
| ---- | ------------------------- | ------------------------- | ----------------- | ----------------- | ------------- | -------------- |
| 2024 | 0.0029                    | 0.0181                    | 0.0015            | 0.0449            | 0.0083        | 0.0001         |
| 2025 | 0.0028                    | 0.0176                    | 0.0014            | 0.0436            | 0.0080        | 0.0001         |
| 2026 | 0.0028                    | 0.0171                    | 0.0014            | 0.0424            | 0.0078        | 0.0001         |
| 2027 | 0.0025                    | 0.0154                    | 0.0012            | 0.0380            | 0.0070        | 0.0001         |
| 2028 | 0.0022                    | 0.0137                    | 0.0011            | 0.0339            | 0.0063        | 0.0001         |
| 2029 | 0.0016                    | 0.0098                    | 0.0008            | 0.0242            | 0.0045        | 0.0001         |
| 2030 | 0.0010                    | 0.0061                    | 0.0005            | 0.0150            | 0.0028        | 0.0001         |
| 2031 | 0.0007                    | 0.0044                    | 0.0004            | 0.0109            | 0.0020        | 0.0001         |
| 2032 | 0.0005                    | 0.0029                    | 0.0002            | 0.0071            | 0.0013        | 0.0001         |
| 2033 | 0.0002                    | 0.0014                    | 0.0001            | 0.0034            | 0.0006        | 0.0001         |
| 2034 | 0.0000                    | 0.0000                    | 0.0000            | 0.0000            | 0.0000        | 0.0001         |
| 2035 | 0.0000                    | 0.0000                    | 0.0000            | 0.0000            | 0.0000        | 0.0001         |
| 2036 | 0.0000                    | 0.0000                    | 0.0000            | 0.0000            | 0.0000        | 0.0001         |
| 2037 | 0.0000                    | 0.0000                    | 0.0000            | 0.0000            | 0.0000        | 0.0001         |
| 2038 | 0.0000                    | 0.0000                    | 0.0000            | 0.0000            | 0.0000        | 0.0001         |

In New England, basis benefits are significantly larger than supply benefits, for two reasons. First, New England demand is only a small portion of North American demand, so a percentage change in regional load has a much smaller percentage effect on continent-wide demand. Second, while gas producers can increase production from year to year, pipeline constraints are much less flexible, requiring years of planning, siting, permitting, and most importantly contracting.

[PDF p. 276 | printed p. 258]

Basis price shifts are not outright applied to any measures. Instead, we combine them with several other factors and use them to calculate cross-DRIPE. See “G-E cross-DRIPE” and “E-G-E cross-DRIPE” subsections below in Section 9.5: _Cross-fuel market price effects_. See these subsections for comparisons of AESC 2024 values with analogous values from AESC 2021.

## 9.5. Cross-fuel market price effects

The preceding sections calculated direct DRIPE effects where a reduction in demand for a given commodity reduced prices for that same commodity. DRIPE benefits also accrue indirectly through cross-DRIPE, which measures the impact that a reduction in one commodity has on a different commodity. We assess three kinds of cross-DRIPE:

1. **Gas-to-electric (G-E) cross-DRIPE ($/MWh)** measures the benefits to electricity consumers that result from a reduction in gas demand. Gas-fired generators set electric market prices in most hours, so reducing gas prices should reduce electricity prices.
2. **Electric-to-gas (E-G) cross-DRIPE ($/MMBtu)** measures the benefits to gas consumers from a reduction in electricity demand. Electric power accounts for about one-third of the region’s gas demand, so reducing electricity demand should reduce gas prices.
3. **Electric-to-gas-to-electric (E-G-E) cross-DRIPE ($/MWh)** combines the first two benefits. Reductions in electricity demand should reduce gas prices (E-G cross-DRIPE) which should, in turn, reduce electricity prices (G-E cross-DRIPE). E-G-E cross-DRIPE is separate from direct electric energy DRIPE and does not double-count any benefits. Reductions in electricity demand yield two benefits. First, lower demand levels will tend to switch the marginal unit to something lower cost, yielding a market price reduction through plant substitution. Second, lower electricity demand levels reduce the demand for, and price of, natural gas. Thus, natural gas power plants, which set prices in most hours, burn less expensive gas than they would have otherwise. Electric energy DRIPE captures the first benefit, while E-G-E cross-DRIPE captures the second benefit. In our energy DRIPE calculations, we explicitly control for natural gas prices, which means own-fuel energy DRIPE is only measuring the benefits of switching from a less efficient plant to a more efficient plant. For E-G-E DRIPE, we hold the powerplant constant, and reflect how a change in gas prices changes electric prices.

_Extractor note (not source text): the source labels the gas-to-electric and electric-to-gas-to-electric values in the list above in $/MWh and the electric-to-gas value in $/MMBtu, but the tables later in this section present G-E cross-DRIPE (Table 120) in $ per MMBtu, E-G cross-DRIPE (Table 119) in $ per MWh and E-G-E cross-DRIPE (Tables 122-123) in $ per MWh; the printed units are kept as printed._

### Electric-to-gas (E-G) cross-DRIPE

Electric-to-Gas (E-G) cross-DRIPE measures the benefits to gas consumers from a reduction in electricity demand. Electric power accounts for approximately one-third of the region’s gas demand, so reducing electricity demand should reduce gas prices, all else equal.

To calculate E-G cross-DRIPE, we utilize the supply gas price shift calculated in Section 9.4: _Natural gas DRIPE_: $0.067/MMBtu per quadrillion Btu. Next, we convert this price shift’s units into $-per-MWh per quadrillion Btu so that we can apply it to MWh savings. We do this by relying on data about the marginal

[PDF p. 277 | printed p. 259]

heat rate for emitting plants as reported by ISO New England.[^320] According to this data, the marginal emitting plant heat rate is 7.902 MMBtu per MWh.[^321] If we scale this to reflect the amount of time gas is expected to be on the margin in the energy market, we estimate a marginal gas heat rate of 6.56 MMBtu per MWh.[^322] We can then multiply this value by the price shift to produce an estimate of $0.54/MWh per quadrillion Btu (see Equation 11). [source discrepancy: Equation 11 prints $0.44 per MWh per quadrillion Btu; $0.067 × 6.56 = $0.4395]

**Equation 11. Price shift in dollar-per-MWh terms**

$$\text{Dollar per MWh price shift} = \text{dollar per MMBtu price shift} \times \text{marginal gas heat rate}$$

$$= \frac{\$0.067}{\dfrac{\text{MMBtu}}{\text{Quadrillion Btu}}} \times \frac{6.56\ \text{MMBtu}}{\text{MWh}} = \frac{\$0.44}{\dfrac{\text{MWh}}{\text{Quadrillion Btu}}}$$

To determine E-G DRIPE, we follow the same overall process used to estimate natural gas supply DRIPE. For each year and state, we calculate the product of (a) estimated natural gas consumption, (b) the estimated share of consumption that is DRIPE-responsive (see Table 114), and (c) the price shift.

[^320]: ISO New England. April 2023. _2021 Electric Generator Air Emissions Report_. Available at [https://www.iso-ne.com/static-assets/documents/2023/04/2021-air-emissions-report.pdf](https://www.iso-ne.com/static-assets/documents/2023/04/2021-air-emissions-report.pdf).

[^321]: Id, Section 5.3.1.2.

[^322]: According to ISO New England, from 2018 to 2021, natural gas plants and pumped storage plants (which are generally powered by marginal units) were marginal 83 percent of the time (see 2020 Air Emissions Report, Figure 4-9).

[PDF p. 278 | printed p. 260]

**Table 119. Electric-to-gas (E-G) cross-DRIPE benefit (2024 $ per MWh)**

| Year              | All   | Zone-on-Zone CT | Zone-on-Zone MA | Zone-on-Zone ME | Zone-on-Zone NH | Zone-on-Zone RI | Zone-on-Zone VT | Zone on Rest-of-Region CT | Zone on Rest-of-Region MA | Zone on Rest-of-Region ME | Zone on Rest-of-Region NH | Zone on Rest-of-Region RI | Zone on Rest-of-Region VT |
| ----------------- | ----- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| 2024              | 0.120 | 0.029           | 0.066           | 0.007           | 0.006           | 0.009           | 0.003           | 0.091                     | 0.055                     | 0.113                     | 0.114                     | 0.112                     | 0.117                     |
| 2025              | 0.193 | 0.047           | 0.105           | 0.012           | 0.010           | 0.014           | 0.005           | 0.146                     | 0.088                     | 0.181                     | 0.183                     | 0.179                     | 0.188                     |
| 2026              | 0.242 | 0.059           | 0.131           | 0.015           | 0.012           | 0.018           | 0.006           | 0.183                     | 0.110                     | 0.227                     | 0.229                     | 0.224                     | 0.236                     |
| 2027              | 0.241 | 0.059           | 0.131           | 0.015           | 0.012           | 0.018           | 0.006           | 0.182                     | 0.110                     | 0.226                     | 0.229                     | 0.223                     | 0.235                     |
| 2028              | 0.242 | 0.059           | 0.132           | 0.015           | 0.012           | 0.018           | 0.006           | 0.183                     | 0.110                     | 0.227                     | 0.230                     | 0.224                     | 0.236                     |
| 2029              | 0.242 | 0.059           | 0.132           | 0.015           | 0.012           | 0.018           | 0.006           | 0.183                     | 0.110                     | 0.227                     | 0.230                     | 0.224                     | 0.236                     |
| 2030              | 0.242 | 0.059           | 0.132           | 0.015           | 0.012           | 0.018           | 0.006           | 0.183                     | 0.110                     | 0.227                     | 0.230                     | 0.224                     | 0.236                     |
| 2031              | 0.243 | 0.059           | 0.132           | 0.015           | 0.012           | 0.018           | 0.006           | 0.183                     | 0.111                     | 0.227                     | 0.230                     | 0.225                     | 0.236                     |
| 2032              | 0.243 | 0.059           | 0.132           | 0.015           | 0.012           | 0.018           | 0.006           | 0.184                     | 0.111                     | 0.228                     | 0.231                     | 0.225                     | 0.237                     |
| 2033              | 0.244 | 0.060           | 0.133           | 0.015           | 0.012           | 0.018           | 0.006           | 0.184                     | 0.111                     | 0.229                     | 0.231                     | 0.226                     | 0.238                     |
| 2034              | 0.245 | 0.060           | 0.133           | 0.015           | 0.012           | 0.018           | 0.006           | 0.185                     | 0.111                     | 0.229                     | 0.232                     | 0.226                     | 0.238                     |
| 2035              | 0.245 | 0.060           | 0.133           | 0.015           | 0.012           | 0.018           | 0.006           | 0.185                     | 0.112                     | 0.230                     | 0.233                     | 0.227                     | 0.239                     |
| 2036              | 0.246 | 0.060           | 0.134           | 0.015           | 0.012           | 0.018           | 0.006           | 0.186                     | 0.112                     | 0.231                     | 0.234                     | 0.228                     | 0.240                     |
| 2037              | 0.247 | 0.060           | 0.134           | 0.015           | 0.012           | 0.018           | 0.006           | 0.187                     | 0.113                     | 0.232                     | 0.234                     | 0.229                     | 0.241                     |
| 2038              | 0.248 | 0.060           | 0.135           | 0.015           | 0.012           | 0.018           | 0.006           | 0.187                     | 0.113                     | 0.232                     | 0.235                     | 0.229                     | 0.241                     |
| 15-year levelized | 0.231 | 0.056           | 0.125           | 0.014           | 0.012           | 0.017           | 0.006           | 0.174                     | 0.105                     | 0.216                     | 0.219                     | 0.213                     | 0.225                     |

Note: Values differ across states because states vary in terms of size of non-electric gas consumption.

Using this table, we can estimate the benefit for a reduction in gas use in each year. For example, a 1 MWh reduction in electricity demand in 2024 yields an E-G cross-DRIPE benefit of $0.120 for New England as a whole. As with other DRIPE categories, zone-on-Rest-of-Region DRIPE benefits for each year are calculated for each state by subtracting the own-zone value for a given state from the New England-wide value.

As with gas supply DRIPE, AESC 2024’s electric-to-gas DRIPE estimates are lower than those found in AESC 2021, mostly due to lower price shift ($0.067/MMBtu per quadrillion Btu, down from $0.094/MMBtu per quadrillion Btu). Other changes are due to differences in historical gas consumption and projected gas consumption across the six states.

### Gas-to-electric (G-E) cross-DRIPE

Just as reductions in electricity demand can produce benefits to gas consumers, so too can reductions in gas demand benefit electric customers. Because this effect changes seasonally, we provide separate DRIPE benefits for annual and winter periods. Annual DRIPE benefits may be best applied to measures that provide savings throughout the year (such as hot water heating efficiency measures) while winter benefits may be best applied to measures that provide savings during the winter only (such as space heating efficiency measures).

To calculate G-E cross-DRIPE values, we first begin with the total price shifts described in Table 118. To calculate the price shift for each season, we add the supply price shift (which does not vary by season) to

[PDF p. 279 | printed p. 261]

the basis price shift (which does vary by season). Because the gas basis price shift decays but the gas supply price shift does not, by 2034, the “total” price shift for any seasons [sic] is equal to the supply price shift component.

Next, these values undergo a unit conversion. We multiply these price shifts (measured in dollar-per-MMBtu per quadrillion Btu) by the heat rate derived above in the E-G cross-DRIPE section (which is measured in MMBtu per MWh). This translation yields price shifts in dollar-per-MWh per MMBtu.

These price shifts are multiplied by each state’s unhedged energy to estimate total DRIPE benefits. For each state, the “energy” is the quantity of electricity demand (in MWh) in the state in question, consumed during the relevant period (e.g., winter, gas), under a particular counterfactual. We scale this total quantity of energy by the portion of energy assumed to be unhedged in each state (i.e., the portion of energy purchases not expected to be subject to the spot market). This unhedged assumption is the same used in energy DRIPE, described above in Table 103. Because system load changes across counterfactuals, the unhedged percentage also changes.

Table 120 summarizes the resulting G-E cross-DRIPE values. For annual effects, we utilize the annual price shift; for winter effects, we rely on gas winter period price shifts.

[PDF p. 280 | printed p. 262]

**Table 120. Gas-to-electric cross-fuel heating DRIPE, 2024 gas efficiency installations (2024 $ per MMBtu) for Counterfactual #1**

| Period                       | Year | NE    | Zone-on-Zone CT | Zone-on-Zone MA | Zone-on-Zone ME | Zone-on-Zone NH | Zone-on-Zone RI | Zone-on-Zone VT | Zone on Rest-of-Region CT | Zone on Rest-of-Region MA | Zone on Rest-of-Region ME | Zone on Rest-of-Region NH | Zone on Rest-of-Region RI | Zone on Rest-of-Region VT |
| ---------------------------- | ---- | ----- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| Annual (e.g., water heating) | 2024 | $2.30 | $0.36           | $1.15           | $0.30           | $0.30           | $0.17           | $0.01           | $1.94                     | $1.15                     | $2.00                     | $2.01                     | $2.13                     | $2.29                     |
| Annual (e.g., water heating) | 2025 | $3.58 | $0.56           | $1.79           | $0.48           | $0.47           | $0.26           | $0.03           | $3.02                     | $1.79                     | $3.10                     | $3.11                     | $3.32                     | $3.55                     |
| Annual (e.g., water heating) | 2026 | $4.49 | $0.78           | $2.24           | $0.58           | $0.58           | $0.27           | $0.04           | $3.71                     | $2.25                     | $3.91                     | $3.92                     | $4.23                     | $4.45                     |
| Annual (e.g., water heating) | 2027 | $3.87 | $0.78           | $1.73           | $0.54           | $0.53           | $0.26           | $0.03           | $3.09                     | $2.14                     | $3.33                     | $3.34                     | $3.61                     | $3.84                     |
| Annual (e.g., water heating) | 2028 | $3.57 | $0.74           | $1.60           | $0.48           | $0.47           | $0.24           | $0.03           | $2.83                     | $1.97                     | $3.09                     | $3.10                     | $3.33                     | $3.55                     |
| Annual (e.g., water heating) | 2029 | $2.55 | $0.54           | $1.16           | $0.32           | $0.34           | $0.18           | $0.02           | $2.02                     | $1.40                     | $2.23                     | $2.21                     | $2.38                     | $2.53                     |
| Annual (e.g., water heating) | 2030 | $1.61 | $0.37           | $0.72           | $0.18           | $0.21           | $0.11           | $0.01           | $1.23                     | $0.89                     | $1.42                     | $1.40                     | $1.49                     | $1.59                     |
| Annual (e.g., water heating) | 2031 | $1.21 | $0.34           | $0.51           | $0.13           | $0.15           | $0.08           | $0.01           | $0.87                     | $0.70                     | $1.08                     | $1.07                     | $1.13                     | $1.20                     |
| Annual (e.g., water heating) | 2032 | $0.73 | $0.20           | $0.31           | $0.08           | $0.09           | $0.05           | $0.01           | $0.53                     | $0.42                     | $0.65                     | $0.65                     | $0.69                     | $0.73                     |
| Annual (e.g., water heating) | 2033 | $0.32 | $0.09           | $0.14           | $0.04           | $0.04           | $0.02           | $0.00           | $0.23                     | $0.18                     | $0.29                     | $0.28                     | $0.30                     | $0.32                     |
| Annual (e.g., water heating) | 2034 | $0.02 | $0.01           | $0.01           | $0.00           | $0.00           | $0.00           | $0.00           | $0.02                     | $0.01                     | $0.02                     | $0.02                     | $0.02                     | $0.02                     |
| Annual (e.g., water heating) | 2035 | $0.00 | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Annual (e.g., water heating) | 2036 | $0.00 | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Annual (e.g., water heating) | 2037 | $0.00 | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Annual (e.g., water heating) | 2038 | $0.00 | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Winter (e.g., space heating) | 2024 | $5.09 | $0.80           | $2.54           | $0.68           | $0.67           | $0.37           | $0.03           | $4.29                     | $2.56                     | $4.41                     | $4.42                     | $4.72                     | $5.06                     |
| Winter (e.g., space heating) | 2025 | $7.91 | $1.23           | $3.93           | $1.08           | $1.06           | $0.55           | $0.06           | $6.68                     | $3.98                     | $6.83                     | $6.85                     | $7.36                     | $7.85                     |
| Winter (e.g., space heating) | 2026 | $9.96 | $1.72           | $4.94           | $1.33           | $1.30           | $0.58           | $0.10           | $8.25                     | $5.03                     | $8.64                     | $8.66                     | $9.38                     | $9.86                     |
| Winter (e.g., space heating) | 2027 | $8.58 | $1.72           | $3.82           | $1.22           | $1.19           | $0.56           | $0.07           | $6.86                     | $4.76                     | $7.36                     | $7.39                     | $8.02                     | $8.51                     |
| Winter (e.g., space heating) | 2028 | $7.92 | $1.63           | $3.54           | $1.10           | $1.07           | $0.52           | $0.06           | $6.29                     | $4.38                     | $6.82                     | $6.85                     | $7.40                     | $7.86                     |
| Winter (e.g., space heating) | 2029 | $5.64 | $1.18           | $2.55           | $0.73           | $0.76           | $0.38           | $0.05           | $4.47                     | $3.10                     | $4.91                     | $4.88                     | $5.26                     | $5.60                     |
| Winter (e.g., space heating) | 2030 | $3.53 | $0.81           | $1.57           | $0.42           | $0.46           | $0.24           | $0.03           | $2.71                     | $1.96                     | $3.11                     | $3.06                     | $3.29                     | $3.50                     |
| Winter (e.g., space heating) | 2031 | $2.65 | $0.73           | $1.11           | $0.29           | $0.32           | $0.17           | $0.02           | $1.92                     | $1.54                     | $2.36                     | $2.33                     | $2.48                     | $2.63                     |
| Winter (e.g., space heating) | 2032 | $1.59 | $0.43           | $0.67           | $0.18           | $0.19           | $0.10           | $0.01           | $1.15                     | $0.91                     | $1.41                     | $1.39                     | $1.48                     | $1.57                     |
| Winter (e.g., space heating) | 2033 | $0.67 | $0.18           | $0.28           | $0.07           | $0.08           | $0.04           | $0.01           | $0.49                     | $0.38                     | $0.59                     | $0.59                     | $0.62                     | $0.66                     |
| Winter (e.g., space heating) | 2034 | $0.01 | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.01                     | $0.01                     | $0.01                     | $0.01                     | $0.01                     | $0.01                     |
| Winter (e.g., space heating) | 2035 | $0.00 | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Winter (e.g., space heating) | 2036 | $0.00 | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Winter (e.g., space heating) | 2037 | $0.00 | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Winter (e.g., space heating) | 2038 | $0.00 | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |

Note: Values differ across states because states vary in terms of size of unhedged electricity demand.

This table indicates that the annual New England-wide value of G-E cross-DRIPE for 2024 is $1.72 per MMBtu. The winter value ($3.80 per MMBtu) is over twice as large because of the higher basis values in the winter months. [source discrepancy: Table 120 prints $2.30 (annual) and $5.09 (winter) for New England in 2024; $1.72 and $3.80 are the printed 15-year levelized values in Table 121] Importantly, since electricity generation everywhere in New England serves electricity demand throughout New England, the cross‐price effect on electric consumers in a given state is not dependent on the amount of gas burned for electric generation in that same state. For each state and year, the zone-on-Rest-of-Pool benefit equals the difference between the ISO-wide benefit and the zonal benefit.

Table 121 provides a comparison of gas-on-electric [sic] cross-DRIPE effects between AESC 2021 and AESC 2024. Gas-to-electric cross-DRIPE values in AESC 2024 are generally higher than in AESC 2021, largely as a result of changes in DRIPE coefficients and hedged energy assumptions.

[PDF p. 281 | printed p. 263]

**Table 121. Comparison of levelized gas-to-electric (G-E) cross-DRIPE benefits (2024 $ per MMBtu)**

| Period                 | Source         | ISO NE | CT   | MA   | ME   | NH   | RI   | VT    |
| ---------------------- | -------------- | ------ | ---- | ---- | ---- | ---- | ---- | ----- |
| Annual                 | AESC 2021      | 1.03   | 0.17 | 0.48 | 0.14 | 0.13 | 0.08 | 0.02  |
| Annual                 | AESC 2024      | 1.72   | 0.34 | 0.81 | 0.22 | 0.22 | 0.12 | 0.01  |
| Annual                 | Difference ($) | 0.70   | 0.17 | 0.33 | 0.09 | 0.09 | 0.03 | -0.01 |
| Annual                 | Difference (%) | 68%    | 99%  | 68%  | 64%  | 70%  | 41%  | -45%  |
| Winter / Space heating | AESC 2021      | 1.87   | 0.31 | 0.87 | 0.25 | 0.24 | 0.14 | 0.05  |
| Winter / Space heating | AESC 2024      | 3.80   | 0.74 | 1.78 | 0.51 | 0.51 | 0.25 | 0.03  |
| Winter / Space heating | Difference ($) | 1.94   | 0.43 | 0.90 | 0.26 | 0.26 | 0.11 | -0.01 |
| Winter / Space heating | Difference (%) | 104%   | 138% | 103% | 102% | 109% | 74%  | -32%  |

Note: All values are levelized over 15 years.

### Electric-to-gas-to-electric (E-G-E) cross-DRIPE

A reduction in electricity prices will reduce the price of natural gas; this reduction in natural gas prices will, in turn, reduce the price of electric energy. The magnitude of this reduction depends both on supply and on basis. E-G-E cross-DRIPE is separate from and offers benefits in addition to electric energy DRIPE.

To calculate E-G-E cross DRIPE, we begin with the price shifts described above in Table 118. As with G-E cross-DRIPE, to calculate the price shift for each season, we add the supply price shift (which does not vary by season) to the basis price shift (which does vary by season). Because the gas basis price shift decays but the gas supply price shift does not, by 2034, the “total” price shift for E-G-E cross-DRIPE is simply equal to the supply price shift component.

Next, these values undergo a unit conversion. Just as with G-E cross-DRIPE, we multiply these price shifts (measured in dollar-per-MMBtu per quadrillion Btu) by the heat rate derived above in the E-G cross-DRIPE section (which is measured in MMBtu per MWh). However, for this DRIPE category, we multiply this heat rate by the price shift twice. This translation yields price shifts in dollar-per-MWh per MWh (rather than dollar-per-MWh per MMBtu, as with G-E cross-DRIPE).

As with G-E cross-DRIPE, we then multiply these price shifts by each state’s unhedged energy to estimate total DRIPE benefits. For each state, the “energy” is the quantity of electricity demand (in MWh) in the state in question, consumed during the relevant period (e.g., winter, electric), under a particular counterfactual. This total quantity of energy is scaled by the portion of energy assumed to be unhedged in each state (i.e., the portion of energy purchases not expected to be subject to the spot market). As with G-E cross-DRIPE, this unhedged assumption is the same used in energy DRIPE, described above in Table 103.

Table 122 summarizes the E-G-E values for the annual period: these are the values that appear in the AESC 2024 User Interface and are applied by program administrators using Appendix B. Table 123 summarizes the summer and winter effects for historical comparison with AESC 2021. These values are not used in cost-effectiveness testing (except to the degree that the seasonal price shifts inform the annual price shift).

[PDF p. 282 | printed p. 264]

**Table 122. Annual electric-to-gas-to-electric cross-fuel heating DRIPE, 2024 gas efficiency installations (2024 $ per MWh)**

| Period | Year | NE     | Zone-on-Zone CT | Zone-on-Zone MA | Zone-on-Zone ME | Zone-on-Zone NH | Zone-on-Zone RI | Zone-on-Zone VT | Zone on Rest-of-Region CT | Zone on Rest-of-Region MA | Zone on Rest-of-Region ME | Zone on Rest-of-Region NH | Zone on Rest-of-Region RI | Zone on Rest-of-Region VT |
| ------ | ---- | ------ | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| Annual | 2024 | $15.02 | $2.37           | $7.53           | $1.96           | $1.94           | $1.12           | $0.10           | $12.65                    | $7.49                     | $13.06                    | $13.08                    | $13.90                    | $14.93                    |
| Annual | 2025 | $23.34 | $3.67           | $11.66          | $3.11           | $3.06           | $1.67           | $0.17           | $19.67                    | $11.68                    | $20.23                    | $20.28                    | $21.67                    | $23.17                    |
| Annual | 2026 | $29.30 | $5.09           | $14.61          | $3.81           | $3.75           | $1.74           | $0.29           | $24.21                    | $14.69                    | $25.49                    | $25.54                    | $27.56                    | $29.01                    |
| Annual | 2027 | $25.23 | $5.11           | $11.30          | $3.50           | $3.44           | $1.68           | $0.19           | $20.12                    | $13.93                    | $21.73                    | $21.79                    | $23.55                    | $25.04                    |
| Annual | 2028 | $23.29 | $4.84           | $10.46          | $3.16           | $3.09           | $1.56           | $0.18           | $18.45                    | $12.83                    | $20.13                    | $20.20                    | $21.73                    | $23.11                    |
| Annual | 2029 | $16.64 | $3.50           | $7.54           | $2.10           | $2.21           | $1.15           | $0.13           | $13.14                    | $9.10                     | $14.54                    | $14.43                    | $15.49                    | $16.51                    |
| Annual | 2030 | $10.46 | $2.44           | $4.67           | $1.20           | $1.36           | $0.72           | $0.07           | $8.03                     | $5.79                     | $9.26                     | $9.11                     | $9.74                     | $10.39                    |
| Annual | 2031 | $7.89  | $2.19           | $3.33           | $0.85           | $0.95           | $0.52           | $0.05           | $5.70                     | $4.57                     | $7.04                     | $6.95                     | $7.38                     | $7.84                     |
| Annual | 2032 | $4.78  | $1.32           | $2.03           | $0.52           | $0.57           | $0.32           | $0.03           | $3.47                     | $2.75                     | $4.26                     | $4.22                     | $4.47                     | $4.75                     |
| Annual | 2033 | $2.09  | $0.57           | $0.89           | $0.23           | $0.25           | $0.14           | $0.02           | $1.52                     | $1.20                     | $1.86                     | $1.84                     | $1.95                     | $2.07                     |
| Annual | 2034 | $0.14  | $0.04           | $0.06           | $0.02           | $0.02           | $0.01           | $0.00           | $0.10                     | $0.08                     | $0.13                     | $0.13                     | $0.13                     | $0.14                     |
| Annual | 2035 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Annual | 2036 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Annual | 2037 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Annual | 2038 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |

**Table 123. Seasonal electric-to-gas-to-electric cross-fuel heating DRIPE, 2024 gas efficiency installations (2024 $ per MWh)**

| Period          | Year | NE     | Zone-on-Zone CT | Zone-on-Zone MA | Zone-on-Zone ME | Zone-on-Zone NH | Zone-on-Zone RI | Zone-on-Zone VT | Zone on Rest-of-Region CT | Zone on Rest-of-Region MA | Zone on Rest-of-Region ME | Zone on Rest-of-Region NH | Zone on Rest-of-Region RI | Zone on Rest-of-Region VT |
| --------------- | ---- | ------ | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| Electric Summer | 2024 | $1.93  | $0.31           | $0.98           | $0.24           | $0.24           | $0.15           | $0.01           | $1.62                     | $0.96                     | $1.69                     | $1.69                     | $1.78                     | $1.92                     |
| Electric Summer | 2025 | $3.00  | $0.48           | $1.51           | $0.38           | $0.38           | $0.22           | $0.02           | $2.52                     | $1.49                     | $2.62                     | $2.62                     | $2.78                     | $2.98                     |
| Electric Summer | 2026 | $3.76  | $0.67           | $1.89           | $0.47           | $0.47           | $0.23           | $0.03           | $3.10                     | $1.87                     | $3.30                     | $3.29                     | $3.53                     | $3.73                     |
| Electric Summer | 2027 | $3.24  | $0.67           | $1.46           | $0.43           | $0.43           | $0.22           | $0.02           | $2.57                     | $1.78                     | $2.81                     | $2.81                     | $3.02                     | $3.22                     |
| Electric Summer | 2028 | $2.99  | $0.63           | $1.35           | $0.39           | $0.39           | $0.21           | $0.02           | $2.36                     | $1.64                     | $2.60                     | $2.60                     | $2.78                     | $2.97                     |
| Electric Summer | 2029 | $2.15  | $0.46           | $0.98           | $0.26           | $0.28           | $0.15           | $0.02           | $1.69                     | $1.17                     | $1.89                     | $1.87                     | $2.00                     | $2.13                     |
| Electric Summer | 2030 | $1.37  | $0.32           | $0.62           | $0.15           | $0.17           | $0.10           | $0.01           | $1.05                     | $0.76                     | $1.22                     | $1.20                     | $1.27                     | $1.36                     |
| Electric Summer | 2031 | $1.05  | $0.30           | $0.44           | $0.11           | $0.12           | $0.07           | $0.01           | $0.75                     | $0.61                     | $0.94                     | $0.93                     | $0.98                     | $1.04                     |
| Electric Summer | 2032 | $0.65  | $0.18           | $0.28           | $0.07           | $0.08           | $0.04           | $0.00           | $0.47                     | $0.37                     | $0.58                     | $0.58                     | $0.61                     | $0.65                     |
| Electric Summer | 2033 | $0.31  | $0.08           | $0.13           | $0.03           | $0.04           | $0.02           | $0.00           | $0.22                     | $0.17                     | $0.27                     | $0.27                     | $0.28                     | $0.30                     |
| Electric Summer | 2034 | $0.05  | $0.01           | $0.02           | $0.01           | $0.01           | $0.00           | $0.00           | $0.04                     | $0.03                     | $0.04                     | $0.04                     | $0.05                     | $0.05                     |
| Electric Summer | 2035 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Electric Summer | 2036 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Electric Summer | 2037 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Electric Summer | 2038 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Electric Winter | 2024 | $21.01 | $3.29           | $10.47          | $2.81           | $2.76           | $1.54           | $0.14           | $17.73                    | $10.54                    | $18.20                    | $18.26                    | $19.47                    | $20.87                    |
| Electric Winter | 2025 | $32.67 | $5.09           | $16.24          | $4.46           | $4.35           | $2.29           | $0.25           | $27.59                    | $16.43                    | $28.21                    | $28.32                    | $30.38                    | $32.43                    |
| Electric Winter | 2026 | $41.04 | $7.06           | $20.36          | $5.47           | $5.33           | $2.39           | $0.42           | $33.98                    | $20.68                    | $35.57                    | $35.70                    | $38.64                    | $40.62                    |
| Electric Winter | 2027 | $35.37 | $7.09           | $15.76          | $5.03           | $4.89           | $2.31           | $0.28           | $28.28                    | $19.61                    | $30.35                    | $30.48                    | $33.06                    | $35.09                    |
| Electric Winter | 2028 | $32.68 | $6.73           | $14.61          | $4.54           | $4.39           | $2.15           | $0.26           | $25.95                    | $18.07                    | $28.14                    | $28.29                    | $30.53                    | $32.42                    |
| Electric Winter | 2029 | $23.31 | $4.86           | $10.52          | $3.02           | $3.14           | $1.58           | $0.19           | $18.45                    | $12.78                    | $20.29                    | $20.17                    | $21.73                    | $23.11                    |
| Electric Winter | 2030 | $14.60 | $3.37           | $6.49           | $1.72           | $1.92           | $0.99           | $0.11           | $11.23                    | $8.10                     | $12.88                    | $12.68                    | $13.60                    | $14.49                    |
| Electric Winter | 2031 | $10.96 | $3.02           | $4.61           | $1.22           | $1.33           | $0.70           | $0.08           | $7.94                     | $6.35                     | $9.75                     | $9.63                     | $10.26                    | $10.89                    |
| Electric Winter | 2032 | $6.60  | $1.80           | $2.79           | $0.73           | $0.79           | $0.43           | $0.05           | $4.80                     | $3.80                     | $5.86                     | $5.80                     | $6.17                     | $6.55                     |
| Electric Winter | 2033 | $2.81  | $0.76           | $1.20           | $0.31           | $0.33           | $0.18           | $0.02           | $2.05                     | $1.61                     | $2.49                     | $2.47                     | $2.63                     | $2.79                     |
| Electric Winter | 2034 | $0.09  | $0.02           | $0.04           | $0.01           | $0.01           | $0.01           | $0.00           | $0.07                     | $0.05                     | $0.08                     | $0.08                     | $0.09                     | $0.09                     |
| Electric Winter | 2035 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Electric Winter | 2036 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Electric Winter | 2037 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |
| Electric Winter | 2038 | $0.00  | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00           | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     | $0.00                     |

Note: Values differ across states because states vary in terms of size of unhedged electricity demand.

This table indicates that the annual New England-wide value of G-E cross-DRIPE for 2024 is $11.23 per MMBtu. As with G-E cross-DRIPE, the winter value ($15.71 per MMBtu) is larger because of the higher basis values in the winter months, while the summer value ($1.46 per MMBtu is smaller) because of the

[PDF p. 283 | printed p. 265]

corresponding unimportance of the basis in these months. For each state and year, the zone-on-Rest-of-Pool benefit equals the difference between the ISO-wide benefit and the zonal benefit. Table 124 provides a comparison of gas-on-electric [sic] cross-DRIPE effects between AESC 2021 and AESC 2024. As with G-E cross-DRIPE, E-G-E cross-DRIPE values in AESC 2024 are generally higher than in AESC 2021, largely as a result of changes in DRIPE coefficients and hedged energy assumptions.

_Extractor note (not source text): the preceding paragraph (continued from p. 264) names "G-E cross-DRIPE" and "per MMBtu" for $11.23, $15.71 and $1.46, which are the printed 15-year levelized E-G-E values in Table 124 (in $ per MWh); Tables 122-123 print New England 2024 values of $15.02 (annual), $1.93 (summer) and $21.01 (winter). The printed wording is kept._

**Table 124. Comparison of 15-year levelized electric-to-gas-to-electric (E-G-E) cross-DRIPE benefits (2024 $ per MWh)**

| Period          | Source         | ISO NE | CT   | MA   | ME   | NH   | RI    | VT    |
| --------------- | -------------- | ------ | ---- | ---- | ---- | ---- | ----- | ----- |
| Electric Annual | AESC 2021      | 6.60   | 1.09 | 3.10 | 0.88 | 0.85 | 0.53  | 0.16  |
| Electric Annual | AESC 2024      | 11.23  | 2.20 | 5.27 | 1.46 | 1.47 | 0.76  | 0.09  |
| Electric Annual | Difference ($) | 4.63   | 1.11 | 2.17 | 0.58 | 0.62 | 0.23  | -0.07 |
| Electric Annual | Difference (%) | 70%    | 101% | 70%  | 66%  | 72%  | 43%   | -44%  |
| Electric Summer | AESC 2021      | 1.40   | 0.24 | 0.66 | 0.17 | 0.18 | 0.12  | 0.03  |
| Electric Summer | AESC 2024      | 1.46   | 0.29 | 0.69 | 0.18 | 0.19 | 0.10  | 0.01  |
| Electric Summer | Difference ($) | 0.06   | 0.05 | 0.03 | 0.01 | 0.01 | -0.02 | -0.02 |
| Electric Summer | Difference (%) | 4%     | 23%  | 4%   | 3%   | 6%   | -15%  | -67%  |
| Electric Winter | AESC 2021      | 7.12   | 1.16 | 3.33 | 0.98 | 0.93 | 0.55  | 0.18  |
| Electric Winter | AESC 2024      | 15.71  | 3.04 | 7.34 | 2.09 | 2.08 | 1.04  | 0.13  |
| Electric Winter | Difference ($) | 8.58   | 1.88 | 4.01 | 1.11 | 1.15 | 0.48  | -0.05 |
| Electric Winter | Difference (%) | 120%   | 161% | 120% | 114% | 123% | 88%   | -27%  |

## 9.6. Oil supply DRIPE

Reducing demand for petroleum and refined products should lead to a reduction in oil prices. Oil demand may be lessened by further electrifying the transportation sector (oil-electricity substitution effects) or by reducing electricity demand during high load winter periods when oil is on the margin (oil-gas substitution). This reduction in oil prices induced by a change in oil demand is termed oil DRIPE.

Oil’s global dimension makes modeling oil DRIPE more uncertain than the analysis of natural gas DRIPE. The analysis in Chapter 3: _Fuel Oil and Other Fuel Costs_ relies on analysis of oil supply fundamentals which, in turn, does not consider the impact of oil supply disruptions or other sources of short-term volatility in oil price. For AESC 2024, we conduct a relatively high-level model of oil DRIPE in the following steps:

1. Estimate the relevant elasticity (i.e., the percentage change in oil price per percentage change in demand for crude oil).
2. Calculate the crude oil DRIPE value.
3. Calculate refined product DRIPE values using the ratios of crude-to-refined-product price from EIA’s AEO 2023 for years 2024–2038.

[PDF p. 284 | printed p. 266]

### Estimating elasticities

Elasticity describes how prices of a commodity respond to changes in demand. We use oil play breakeven analysis to estimate elasticity for crude oil.

Oil play breakeven analysis models the price at which a given geological formation is revenue neutral (a specific oil field or formation is known in the industry as a “play”). Different plays have different breakeven points, and when considered in aggregate, a supply curve can be made to show the prices at which various sources of new supply would enter the market. This curve can be thought of as analogous to an electric market’s power plant offer stack.

By examining a set of these supply curves, we can assess the average relationship between price and supply for a marginal barrel of oil. Table 125 presents elasticities from five different breakeven analyses. Two of these curves display a supply curve with a very steep right tail. The Wood Mackenzie supply curve, for example, indicates that an additional million barrels per day of oil supply would increase breakeven price by about $8.6 per barrel. In other words, it indicates that a 1.0 percent increase in cumulative oil production in this region would increase costs by 0.86 percent.

**Table 125. Percent change in crude oil price for a 1.0 percent change in global demand**

| Forecast                              | Curve Segment | Date Published | Elasticity | Sources |
| ------------------------------------- | ------------- | -------------- | ---------- | ------- |
| Wood Mackenzie                        | Entire curve  | 2019           | 0.86       | (A)     |
| Rystad Energy                         | Entire curve  | 2022           | 1.45       | (B)     |
| Goldman Sachs                         | Low only      | 2023           | 0.57       | (C)     |
| Goldman Sachs                         | High only     | 2023           | 3.07       | (C)     |
| BP/PIRA                               | Low only      | 2015           | 0.88       | (D)     |
| BP/PIRA                               | High only     | 2015           | 3.60       | (D)     |
| S&P Global                            | Entire Curve  | 2021           | 0.63       | (E)     |
| **Average (All)**                     |               |                | **1.58**   |         |
| **Average (Low Only + Entire Curve)** |               |                | **0.88**   |         |

_Sources: (A) [https://www.woodmac.com/reports/upstream-oil-and-gas-global-oil-cost-curves-and-pre-fid-breakevens-updated-h2-2018-211878/](https://www.woodmac.com/reports/upstream-oil-and-gas-global-oil-cost-curves-and-pre-fid-breakevens-updated-h2-2018-211878/), (B) [https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/863800/fossil-fuel-supply-curves.pdf](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/863800/fossil-fuel-supply-curves.pdf), (C) [http://crudeoilpeak.info/oil-price-analysis](http://crudeoilpeak.info/oil-price-analysis), (D) [https://www.bp.com/content/dam/bp/business-sites/en/global/corporate/pdfs/news-and-insights/speeches/new-economics-of-oil-spencer-dale.pdf](https://www.bp.com/content/dam/bp/business-sites/en/global/corporate/pdfs/news-and-insights/speeches/new-economics-of-oil-spencer-dale.pdf), and (E) [https://www.spglobal.com/commodityinsights/en/ci/research-analysis/global-crude-oil-curve-shows-projects-break-even-through-2040.html](https://www.spglobal.com/commodityinsights/en/ci/research-analysis/global-crude-oil-curve-shows-projects-break-even-through-2040.html)._

A simple average of all elasticities yields a value of 1.58. If the two “High only” slopes are removed, the resulting average elasticity is 0.88. Given the uncertain nature of this analysis, AESC 2024 models oil supply as unit elastic in the relevant region study [sic], so a 1 percent change in demand would yield a 1

[PDF p. 285 | printed p. 267]

percent change in price.[^323] Critically, demand in this context is _global demand_ (currently 101 million barrels/day, of which the United States consumes about one-fourth.[^324]

This estimate is similar to our estimate of elasticity of supply for natural gas. This is expected given the similarities between the two hydrocarbons, their disposition, and their extraction.

Next, we convert this elasticity into a “price shift” which represents how the price (in dollars per MMBtu) changes in response to changes in demand (measured in quadrillion Btu per year). To do this, we multiply the elasticity by a forecast for WTI crude oil prices ($16 to $18 per MMBtu, depending on the year) and divide the result by a forecast of crude oil consumption (estimated to be about 240 quadrillion Btu worldwide per year).[^325] This yields an average price shift of about $0.07/MMBtu per quadrillion Btus for any given year.

### Calculating oil DRIPE

As with the electric and natural gas DRIPE effects, the price reduction per MMBtu of oil saved is very tiny compared to the price per MMBtu. But each MMBtu saved reduced prices for a very large number of MMBtus. That said, given the modest size of New England oil demand in comparison to the entire global market (about 0.76 percent of worldwide consumption), the overall value of DRIPE remains modest.[^326]

According to the latest EIA SEDS database, in 2014 through 2021, New England consumed approximately 1.4 quadrillion Btu of petroleum products yearly.[^327] Over time, AEO 2023 forecasts demand gradually falling, averaging about 1.04 quadrillion Btu of petroleum products yearly between 2024 and 2050.

As a result, a 1 MMBtu reduction in crude oil demand yields an average regional benefit of about $0.07 per MMBtu (i.e., $0.07/MMBtu per quadrillion Btu multiplied by 1.04 quadrillion Btu). The value for each state, presented in Table 126, are [sic] proportionally smaller, ranging from about $0.005 per MMBtu to

[^323]: The assumption of unit elasticity may overstate price effects because estimates of shale resources have increased in the past years and estimates of shale extraction costs have fallen—both effects reduce the slope of the supply curve, and its corresponding elasticity.

[^324]: For more information, see [https://www.iea.org/oilmarketreport/omrpublic/](https://www.iea.org/oilmarketreport/omrpublic/).

[^325]: Crude oil prices are based on WTI prices from AEO 2023 and worldwide crude oil consumption is based on values in EIA’s 2021 edition of the International Energy Outlook.

    EIA. Last accessed August 10, 2023. “Petroleum and Other Liquids Prices.” _Eia.org_. Available at [https://www.eia.gov/outlooks/aeo/excel/aeotab_12.xlsx](https://www.eia.gov/outlooks/aeo/excel/aeotab_12.xlsx).

    EIA. 2021. “Liquids Consumption: OECD: OECD Americas.” _EIA.gov_. Available at [https://www.eia.gov/outlooks/aeo/data/browser/#/?id=5-IEO2019&sourcekey=0](https://www.eia.gov/outlooks/aeo/data/browser/#/?id=5-IEO2019&sourcekey=0).

[^326]: Calculated based on data from 2014 to 2021 using data from EIA. 2021. “State Energy Data System: Updates by Energy Source.” _Eia.gov_. Available at [https://www.eia.gov/state/seds/seds-data-fuel.php?sid=US#DataFiles](https://www.eia.gov/state/seds/seds-data-fuel.php?sid=US#DataFiles)

[^327]: See [https://www.eia.gov/state/seds/seds-data-fuel.php?sid=US#DataFiles](https://www.eia.gov/state/seds/seds-data-fuel.php?sid=US#DataFiles) for more information.

[PDF p. 286 | printed p. 268]

$0.033 per MMBtu per 1 MMBtu reduction.[^328] Zone-on-zone values are calculated based on each state’s share of oil consumption relative to the New England-wide total. Meanwhile, zone-on-region values are equal to the New England total minus the value from each respective state.

**Table 126. Crude oil DRIPE by state (2024 $ per MMBtu)**

| Year                      | NE    | Zone-on-Zone CT | Zone-on-Zone MA | Zone-on-Zone ME | Zone-on-Zone NH | Zone-on-Zone RI | Zone-on-Zone VT | Zone on Rest-of-Region CT | Zone on Rest-of-Region MA | Zone on Rest-of-Region ME | Zone on Rest-of-Region NH | Zone on Rest-of-Region RI | Zone on Rest-of-Region VT |
| ------------------------- | ----- | --------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- | ------------------------- |
| 2024                      | 0.096 | 0.022           | 0.040           | 0.012           | 0.011           | 0.006           | 0.006           | 0.074                     | 0.057                     | 0.084                     | 0.085                     | 0.091                     | 0.091                     |
| 2025                      | 0.088 | 0.020           | 0.036           | 0.011           | 0.010           | 0.005           | 0.005           | 0.068                     | 0.052                     | 0.077                     | 0.078                     | 0.083                     | 0.083                     |
| 2026                      | 0.086 | 0.020           | 0.035           | 0.011           | 0.010           | 0.005           | 0.005           | 0.066                     | 0.051                     | 0.075                     | 0.076                     | 0.081                     | 0.081                     |
| 2027                      | 0.085 | 0.019           | 0.035           | 0.011           | 0.010           | 0.005           | 0.005           | 0.065                     | 0.050                     | 0.074                     | 0.075                     | 0.080                     | 0.080                     |
| 2028                      | 0.083 | 0.019           | 0.034           | 0.011           | 0.010           | 0.005           | 0.005           | 0.064                     | 0.049                     | 0.073                     | 0.074                     | 0.078                     | 0.079                     |
| 2029                      | 0.082 | 0.019           | 0.034           | 0.011           | 0.009           | 0.005           | 0.005           | 0.063                     | 0.048                     | 0.071                     | 0.073                     | 0.077                     | 0.077                     |
| 2030                      | 0.080 | 0.018           | 0.033           | 0.010           | 0.009           | 0.005           | 0.005           | 0.062                     | 0.047                     | 0.070                     | 0.071                     | 0.076                     | 0.076                     |
| 2031                      | 0.079 | 0.018           | 0.032           | 0.010           | 0.009           | 0.005           | 0.005           | 0.061                     | 0.046                     | 0.069                     | 0.070                     | 0.074                     | 0.074                     |
| 2032                      | 0.078 | 0.018           | 0.032           | 0.010           | 0.009           | 0.005           | 0.004           | 0.060                     | 0.046                     | 0.067                     | 0.069                     | 0.073                     | 0.073                     |
| 2033                      | 0.076 | 0.017           | 0.031           | 0.010           | 0.009           | 0.004           | 0.004           | 0.059                     | 0.045                     | 0.066                     | 0.068                     | 0.072                     | 0.072                     |
| 2034                      | 0.075 | 0.017           | 0.031           | 0.010           | 0.009           | 0.004           | 0.004           | 0.058                     | 0.044                     | 0.065                     | 0.067                     | 0.071                     | 0.071                     |
| 2035                      | 0.074 | 0.017           | 0.030           | 0.010           | 0.008           | 0.004           | 0.004           | 0.057                     | 0.043                     | 0.064                     | 0.065                     | 0.070                     | 0.070                     |
| 2036                      | 0.073 | 0.017           | 0.030           | 0.009           | 0.008           | 0.004           | 0.004           | 0.056                     | 0.043                     | 0.064                     | 0.065                     | 0.069                     | 0.069                     |
| 2037                      | 0.072 | 0.016           | 0.030           | 0.009           | 0.008           | 0.004           | 0.004           | 0.056                     | 0.042                     | 0.063                     | 0.064                     | 0.068                     | 0.068                     |
| 2038                      | 0.071 | 0.016           | 0.029           | 0.009           | 0.008           | 0.004           | 0.004           | 0.055                     | 0.042                     | 0.062                     | 0.063                     | 0.067                     | 0.067                     |
| 2039                      | 0.070 | 0.016           | 0.029           | 0.009           | 0.008           | 0.004           | 0.004           | 0.054                     | 0.041                     | 0.061                     | 0.062                     | 0.066                     | 0.066                     |
| 2040                      | 0.069 | 0.016           | 0.029           | 0.009           | 0.008           | 0.004           | 0.004           | 0.054                     | 0.041                     | 0.060                     | 0.061                     | 0.065                     | 0.065                     |
| 2041                      | 0.069 | 0.016           | 0.028           | 0.009           | 0.008           | 0.004           | 0.004           | 0.053                     | 0.040                     | 0.060                     | 0.061                     | 0.065                     | 0.065                     |
| 2042                      | 0.068 | 0.016           | 0.028           | 0.009           | 0.008           | 0.004           | 0.004           | 0.053                     | 0.040                     | 0.059                     | 0.060                     | 0.064                     | 0.064                     |
| 2043                      | 0.067 | 0.015           | 0.028           | 0.009           | 0.008           | 0.004           | 0.004           | 0.052                     | 0.040                     | 0.059                     | 0.060                     | 0.063                     | 0.063                     |
| 2044                      | 0.067 | 0.015           | 0.028           | 0.009           | 0.008           | 0.004           | 0.004           | 0.052                     | 0.039                     | 0.058                     | 0.059                     | 0.063                     | 0.063                     |
| 2045                      | 0.066 | 0.015           | 0.027           | 0.009           | 0.008           | 0.004           | 0.004           | 0.051                     | 0.039                     | 0.058                     | 0.059                     | 0.062                     | 0.062                     |
| 2045 [sic; 2046 expected] | 0.066 | 0.015           | 0.027           | 0.009           | 0.008           | 0.004           | 0.004           | 0.051                     | 0.039                     | 0.057                     | 0.058                     | 0.062                     | 0.062                     |
| 2047                      | 0.066 | 0.015           | 0.027           | 0.009           | 0.008           | 0.004           | 0.004           | 0.051                     | 0.039                     | 0.057                     | 0.058                     | 0.062                     | 0.062                     |
| 2048                      | 0.066 | 0.015           | 0.027           | 0.008           | 0.007           | 0.004           | 0.004           | 0.051                     | 0.039                     | 0.057                     | 0.058                     | 0.062                     | 0.062                     |
| 2049                      | 0.065 | 0.015           | 0.027           | 0.008           | 0.007           | 0.004           | 0.004           | 0.051                     | 0.038                     | 0.057                     | 0.058                     | 0.062                     | 0.062                     |
| 2050                      | 0.065 | 0.015           | 0.027           | 0.008           | 0.007           | 0.004           | 0.004           | 0.050                     | 0.038                     | 0.057                     | 0.058                     | 0.061                     | 0.062                     |
| 15-year levelized         | 0.080 | 0.018           | 0.033           | 0.010           | 0.009           | 0.005           | 0.005           | 0.062                     | 0.047                     | 0.070                     | 0.071                     | 0.076                     | 0.076                     |

Note: Values differ across states because states vary in terms of size of oil consumption.

[^328]: The United States consumes about 37 quads of petroleum products annually, compared with 1.4 quads consumed in New England. The value of a 1 MMBtu reduction in oil demand anywhere within the United States has a U.S.-wide DRIPE value of $2.25 per MMBtu.

[PDF p. 287 | printed p. 269]

As with natural gas supply DRIPE, oil DRIPE are [sic] not decayed. Because oil DRIPE is not decayed, the values in the preceding table reflect the actual value of a demand reduction in each year (e.g., a regionwide demand reduction in 2024 is worth $0.096 per MMBtu and a reduction in 2028 is worth $0.083 per MMBtu). Oil DRIPE benefits are low because of the relatively modest amounts of demand in New England states compared to the size of the global oil market.

In order to apply oil DRIPE values to specific commodities (e.g., gasoline, home heating fuel), we multiply the values in Table 126 by the refined-price to crude-price ratio found in Table 127. For example, the levelized value of gasoline DRIPE across New England is worth $0.1454 per MMBtu reduced ($0.084 per MMBtu x 1.51). [source discrepancy: Table 126 prints a New England 15-year levelized value of $0.080, and $0.084 × 1.51 = $0.1268; $0.1454 ÷ 1.51 = $0.0963, which matches the printed 2024 New England value of $0.096]

**Table 127. AEO 2023 prices of crude oil and refined petroleum products**

| Product           | 2023–2035 Avg Price (2022 $ per gallon) | Ratio of product price to WTI price |
| ----------------- | --------------------------------------- | ----------------------------------- |
| WTI Crude Oil     | 2.49                                    | -                                   |
| Home heating oil  | 4.15                                    | 1.67                                |
| Residual fuel oil | 2.40                                    | 0.96                                |
| Motor gasoline    | 3.75                                    | 1.51                                |
| Motor diesel      | 4.58                                    | 1.84                                |

Source: EIA AEO 2023 Table: “Petroleum and Other Liquids Prices.” Available at [https://www.eia.gov/outlooks/aeo/excel/aeotab_12.xlsx](https://www.eia.gov/outlooks/aeo/excel/aeotab_12.xlsx).

This analysis assumes that oil supply drives the price of refined products and that a reduction in the demand of any petroleum product impacts the price of all other crude products. In reality, there may not be a one-to-one price benefit for reductions in gasoline on fuel oil (for example). This simplifying assumption is reasonable given the small magnitude of oil DRIPE effects and the high-level analysis undertaken.

Table 128 illustrates the differences between crude oil DRIPE calculated in AESC 2021 and AESC 2024. In AESC 2024, oil DRIPE values for New England as a whole are 9 percent higher than in the previous study. This change is primarily due to increases in forecasts of crude oil prices.

**Table 128. Comparison of oil DRIPE values (2024 dollars per MMBtu)**

|                | New England | CT    | MA    | ME    | NH    | RI    | VT    |
| -------------- | ----------- | ----- | ----- | ----- | ----- | ----- | ----- |
| AESC 2021      | 0.074       | 0.017 | 0.031 | 0.010 | 0.008 | 0.004 | 0.004 |
| AESC 2024      | 0.080       | 0.018 | 0.033 | 0.010 | 0.009 | 0.005 | 0.005 |
| Difference ($) | 0.007       | 0.002 | 0.002 | 0.001 | 0.001 | 0.000 | 0.000 |
| Difference (%) | 9%          | 11%   | 8%    | 7%    | 13%   | 9%    | 10%   |

Note: Values shown are levelized over 15 years. AESC 2021 uses a discount rate of 0.81 percent while AESC 2024 values use a discount rate of 1.74 percent.

[PDF pp. 288-436 not transcribed: Chapters 10-12 and Appendices A-K, in the other files of this folder (see README.md)]
