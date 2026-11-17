---
source_file: JPV-2.pdf
citekey: velez_Docket260510JPV2_2026
zotero_item: "7TKFRDEI"
public_url: https://drive.google.com/file/d/1czW4uIE1dXGjuhz7SCTKGWJbdfKit_KJ/view
short_url: https://pub.switch.box/velez_Docket260510JPV2_2026
source_url: https://www.dpuc.state.ct.us/DOCKCURR.NSF/5f3a36a996853741852588c600420c24/770ec45974af3d5a85258e97006011c7?OpenDocument
md5: "ed0707f1764199f4ec76bacc4a126511"
validated: 2026-11-16
docket: 26-05-10
utility: 'CL&P (The Connecticut Light and Power Company, d/b/a Eversource Energy); the exhibit refers to "CL&P" and "the Company"'
filing_date: 'not printed in the PDF (the exhibit is dated 2026-10-20 on its title block; extractor note, not source text: the requester gives the filing date as 2026-10-21)'
filer: Conservation Law Foundation and Sierra Club
document_type: exhibit
pages_total: 15
extraction_scope: full
citation_scheme: page
context: Exhibit JPV-2, filed by CLF and Sierra Club on Oct. 21, 2026 with the direct testimony of Juan-Pablo Velez (Switchbox).
contents: Six sections in Q&A form on data sources, representative home profiles, hourly marginal delivery costs, incremental cost and overpayment, Rate HP derivation, and the fixed-charge alternative.
why_here: The methodology the CIEC responses point to (e.g. Section 3 for hourly marginal costs, Section 6 for the fixed charge).
---

# Exhibit JPV-2: Data Sources and Methodology

**Source**: JPV-2.pdf
**Pages**: 15
**Date**: 2026-10-20 (as printed on the title block)
**Author(s)**: Juan-Pablo Velez
**Author affiliations**: The title block names no affiliation for the author beyond the testimony's sponsor: "Direct Testimony of Juan-Pablo Velez on Behalf of Conservation Law Foundation and Sierra Club — PURA Docket 26-05-10". No correspondence or affiliation block is printed.

_Extractor note (not source text): This extract follows the PDF's own pagination and has no printed page numbers or margin line numbers, so citations are by PDF page. Text is transcribed verbatim; no typographical corrections were made except where marked inline. Footnote reference marks (superscripts) are written as `[^n]`; the 12 footnote definitions sit on the pages where they are printed. Links in footnotes 5, 7, 8, 10 and 11 and in the references are taken from the PDF's link annotations. Equations were read from the rendered pages and written in LaTeX._

---

[PDF p. 1]

# Exhibit JPV-2: Data Sources and Methodology

Direct Testimony of Juan-Pablo Velez on Behalf of Conservation Law Foundation and Sierra Club — PURA Docket 26-05-10

Juan-Pablo Velez

2026-10-20

This exhibit describes the data sources and methodology behind the analysis presented in my Direct Testimony. It covers six topics:

1. The data sources I relied on.
2. How I constructed the representative home’s before-and-after electricity consumption profiles.
3. How I computed the hourly marginal costs of bulk transmission and distribution.
4. How I defined and computed the incremental cost, incremental revenue, fair annual bill, and overpayment of heat pump adoption.
5. How I derived the proposed Rate HP rates.
6. How I computed the fixed-charge alternative discussed in Section XIII of my Direct Testimony.

## 1. Data sources

**Q.** What data sources did you rely on for the analysis in your Direct Testimony?

**A.** My analysis draws on four categories of data:

1. **Proposed electric rates.** CL&P’s proposed Rate 1 and Rate 6 delivery rates from its rate case filing (Docket No. 26-05-10), and CL&P’s standard service generation rates, which I applied to the consumption data to compute electricity bills under each rate structure.
2. **Hourly transmission and distribution cost inputs.** The annualized cost of new bulk transmission and distribution capacity, allocated to specific hours of the year using a probability-of-peak methodology, which I used to identify when customer consumption drives new infrastructure investment.
3. **NREL ResStock building simulations.** A statistically representative sample of residential buildings in CL&P’s service territory, modeled under both current heating systems and a heat pump retrofit. I applied three load curve corrections and calibrated the sample’s customer weights before billing (see load curve adjustments below), then computed electricity bills from each building’s hourly
   [PDF p. 2]
   load profile using CAIRO (described below), and used the results both to construct the representative home (Section 2) and for the population-level bill-change analysis.
4. **Fossil fuel prices.** The filed residential gas rates of the gas utility serving each home (CT Natural Gas, Southern CT Gas, Yankee Gas, or Norwich Public Utilities), and the U.S. Energy Information Administration’s monthly residential heating oil and propane prices, which I used to compute the non-electric portions of households’ total energy bills.

**Q.** What rate data did you use?

**A.** All delivery rate inputs to my analysis are the Company’s proposed rates in Docket No. 26-05-10.

For **Rate 1**, I used the Company’s proposed Rate Year 1 customer charge of \$12.36 per month and distribution rate, both including the Gross Earnings Tax, together with the filed transmission rate and delivery riders, from Exhibit CLP-RATES-2.[^1] For generation, I used CL&P’s 2025 standard service rates, retrieved from the Arcadia (formerly Genability) tariff database.[^2]

For **Rate 6**, I used the rates filed by the Company in Exhibit CLP-RATES-6: a customer charge of \$30.95 per month, and a seasonal, tiered distribution rate. From November through March, consumption up to 700 kWh per month is billed at the Block 1 rate and consumption above 700 kWh at the discounted Block 2 rate. From April through October, all consumption is billed at the Block 1 rate.[^3]

For the **supply component** of Rate 6 bills, I used the same generation and transmission rates as Rate 1, consistent with the Company’s filing.

**Q.** What data did you use for the hourly transmission and distribution costs?

**A.** I constructed hourly marginal delivery costs from two inputs:

For **distribution**, I used the month-hour marginal costs the Company filed in response to OCC-863, Attachment 2 (“Docket 26-05-10: Response to OCC-863” 2026). Those costs take Table 3’s \$20.17/kW-year, gross it up for secondary losses to \$21.22/kW-year, and assign that annual amount to each month, hour, and day type. I placed that schedule on

[^1]: Exhibit CLP-RATES-2, Rate Year build, and Exhibit CLP-RATES-3, Docket No. 26-05-10 (Eversource 2026c, 2026d).

[^2]: Arcadia Signal API, CL&P residential standard service. Arcadia maintains a continuously updated database of U.S. electric utility tariffs sourced from utility filings.

[^3]: Exhibit CLP-RATES-6, Docket No. 26-05-10.

[PDF p. 3]

the 2025 calendar and scaled it so the year totals \$21.22/kW-year. The steps are in Section 3 of this exhibit.

For **bulk transmission**, I used the avoided Pool Transmission Facility cost of \$69/kW-year, in 2024 dollars, from the 2024 Avoided Energy Supply Components study (Synapse 2024). I inflated it to 2026 dollars (U.S. Bureau of Labor Statistics 2025) and spread it with the probability-of-peak method described in the Company’s response to OCC-733 (Eversource and Nieto 09-11-26), fit on ISO New England system load for 2022 through 2025 (ISO-NE n.d.). The steps are in Section 3 of this exhibit.

The resulting hourly cost profiles are shown in the bulk transmission and distribution marginal cost heatmaps in Section III of my Direct Testimony. These hourly costs also underlie the peak-hour overlays, seasonal marginal cost charts, and cost-versus-charge comparison in Section III.

**Q.** What is ResStock, and which figures did it produce?

**A.** ResStock is the End-Use Load Profiles dataset produced by the National Renewable Energy Laboratory (NREL), the U.S. Department of Energy’s primary laboratory for energy efficiency and renewable energy research (NREL 2024a, 2024b). I used the 2024.2 release of the dataset.

ResStock models a statistically representative sample of the U.S. housing stock. Each modeled dwelling has physical characteristics — square footage, insulation levels, HVAC equipment, and local climate — drawn from federal survey data. Its energy consumption is simulated hour-by-hour using the DOE’s EnergyPlus building energy simulation engine. For each home, ResStock provides a baseline scenario (with the home’s existing heating system) and a heat pump retrofit scenario (in which the home is equipped with a cold-climate air-source heat pump), each with a complete 8,760-hour energy consumption profile covering electricity, natural gas, heating oil, and propane.

Before running the bill analysis, I applied three corrections to ResStock’s simulated load curves, and separately calibrated the sample’s customer weights.

First, a **multifamily non-HVAC electricity correction.** ResStock systematically overstates electricity consumption for multifamily buildings, driven by inflated non-HVAC end uses (plug loads, lighting, appliances). The overstatement grows with a utility’s share of multifamily housing. I corrected this by scaling each multifamily building’s non-HVAC electricity consumption to match the single-family per-square-foot benchmark for each end use. HVAC loads were left unchanged.

Second, a **natural gas calibration.** I scaled every building’s hourly natural gas consumption by a single statewide factor, applied the same way to the baseline and the heat pump retrofit, so that ResStock’s weighted total matches the U.S. Energy Information
[PDF p. 4]
Administration’s reported residential natural gas deliveries for Connecticut (U.S. Energy Information Administration 2018).

Third, an **electricity sales calibration.** I scaled every building’s hourly electricity consumption by a single utility-wide factor so that the weighted total of the baseline, pre-retrofit profiles matches the residential electricity sales Eversource forecast for the rate year — 10,319,107,650 kWh across its residential class (Eversource 2026c). The same factor multiplies the heat pump retrofit profiles so the two scenarios stay on a consistent basis, but it pins only the pre-retrofit total to filed sales; the post-retrofit total is left free to reflect the added electricity a heat pump draws. For CL&P this factor was 0.995, a downward adjustment of roughly half a percent.

Separately, I calibrated the **customer weights.** ResStock assigns each modeled dwelling a weight representing the number of real households it stands for. I rescaled those weights so they sum to the residential customer count Eversource filed for the rate year — 1,212,520.95 customers, up from the 892,895.5 that ResStock natively assigns to CL&P territory, a factor of about 1.36 (Eversource 2026c). This ensures the modeled population represents the right number of customers when total class revenue and per-customer fixed charges are computed. Because the scaling is uniform, it does not change the share of households whose bills rise or fall; it affects only the population totals.

I used ResStock for the population-level bill-change analysis, in which I computed total energy bills for each of the 3,539 CL&P-territory buildings, under both their baseline heating system and a heat pump retrofit, and reported the share of households whose bills would increase or decrease. These results appear in the bill-change charts for natural-gas-heated and delivered-fuel-heated homes in Sections IV, V, VII, and XI of my Direct Testimony. I used CAIRO — the Customer Affordability, Incentives, and Rates Optimization model, a rate simulation engine developed by the National Laboratory of the Rockies (formerly NREL)[^4] — to compute each building’s electricity bills. CAIRO takes a building’s hourly electricity load profile and a tariff structure as inputs, and computes the resulting bill, including fixed charges, volumetric charges, and demand charges where applicable.

For the annual energy bill charts for natural-gas-heated and delivered-fuel-heated homes in Sections IV and XI of my Direct Testimony, both the electric and fossil fuel portions derive from ResStock consumption data, with bills computed by CAIRO. The representative-home analysis in Section III of my Direct Testimony also uses ResStock, as described in Section 2.

**Q.** What fossil fuel price data did you use?

**A.** For natural gas, I applied the filed residential gas rates of the gas utility serving each home (CT Natural Gas, Southern CT Gas, Yankee Gas, or Norwich Public Utilities) to each

[^4]: (NREL 2026).

[PDF p. 5]

household’s monthly gas consumption from ResStock. For heating oil and propane, I used the U.S. Energy Information Administration’s monthly residential price series (EIA 2024).

## 2. Representative home profiles

**Q.** How did you construct the before-and-after electricity consumption profiles used in Section III of your Direct Testimony?

**A.** I built both profiles from the ResStock simulations described in Section 1, using the hourly grid electricity consumption that CAIRO bills for each building, after the load curve corrections and after scaling ResStock’s residential consumption to the Company’s sales.[^5]

For the **“before” profile** — representing a typical home that heats with fossil fuels — I took every ResStock building in CL&P’s service territory that heats with natural gas, heating oil, or propane, in its baseline scenario, and computed the weighted average of their hourly electricity consumption, using ResStock’s sample weights.

For the **“after” profile** — representing a typical home after installing a heat pump — I took the same buildings, with the same weights, in ResStock’s heat pump retrofit scenario: a high-efficiency cold-climate air-source heat pump with electric resistance backup (Upgrade 2 in the ResStock 2024.2 release).

Because both profiles average the same buildings, the difference between them isolates the change in electricity consumption caused by the heat pump. The profiles are simulated, not metered. I relied on ResStock because the Company does not have this information for its own customers: it stated in discovery that it “does not track heating sources” and “does not employ AMI meters.”[^6]

The primary representative profile pools all fossil-fuel-heated homes together. For the fuel-specific total energy bill comparisons in Sections IV and XI of my Direct Testimony, I applied this exact same weighted-average construction separately to the natural-gas-heated and the delivered-fuel-heated (heating oil and propane) subcategories.

I summed each profile’s hourly consumption by month for the bill calculations and monthly load profile charts. I used the hourly profiles directly for the peak-hour overlays and for computing marginal transmission and distribution costs, which require hourly resolution.

[^5]: The notebook that builds these weighted-average before-and-after representative-home load and bill profiles is the report’s [representative-home notebook](https://github.com/switchbox-data/reports2/blob/main/reports/ct_hp_rates/notebooks/representative_home.qmd).

[^6]: Responses to CLF-SC-008 and CLF-SC-009, Docket No. 26-05-10 (Sept. 18, 2026) (Eversource, Davis, and Parsons 2026; Eversource, Parsons, and Davis 2026).

[PDF p. 6]

## 3. Hourly marginal delivery costs

**Q.** Can you walk through how you computed the hourly bulk transmission marginal costs shown in Section III of your Direct Testimony?

**A.** Yes. The annual cost is a regional avoided-cost figure for New England. The hourly shape comes from the probability-of-peak method the Company’s witness Amparo Nieto described in the response to OCC-733, which underlies the Company’s distribution marginal costs in OCC-863 Attachment 2 (Eversource and Nieto 09-11-26; “Docket 26-05-10: Response to OCC-863” 2026). I applied that method to New England system load, then placed the resulting rates on the analysis year’s calendar the same way I placed the distribution schedule. The calculation has three steps.[^7]

**Step 1: Annual bulk transmission cost.** Pool Transmission Facility cost is the cost of the regional transmission network that ISO New England plans and that every load-serving entity in New England pays for through Regional Network Service (ISO-NE 2026, sec. II.21.1). The Avoided Energy Supply Components study for 2024 estimates the long-run cost of that network, avoided when peak demand falls by one kilowatt, at \$69/kW-year in 2024 dollars. The same figure applies in all six New England states, because the network is pooled (Synapse 2024).

I inflated \$69/kW-year from 2024 dollars to 2026 dollars (U.S. Bureau of Labor Statistics 2025). 2026 is the dollar year of the Company’s marginal cost study, so the transmission and distribution schedules are in the same dollars (Eversource 2026b).

**Step 2: Probability of peak, following OCC-733.** OCC-733 describes how the Company turned four years of hourly load into a probability that the peak falls in each month, hour, and day type (Eversource and Nieto 09-11-26). I followed those steps, using ISO New England’s historical system load for 2022 through 2025, summed across the eight load zones (ISO-NE n.d.). These are the same four years the Company used for its own probability of peak. I used regional load because that is the load the AESC cost is measured against. AESC derives the \$69/kW-year from ISO New England’s estimate of the transmission investment needed to serve New England’s peak load growth, and it directs that the value be applied to a measure’s impact on the regional annual system peak, because the Pool Transmission Facilities are built to meet that peak (Synapse 2024, 283–84).

The steps are:

[^7]: The code that computes the hourly bulk-transmission marginal costs — spreading the AESC avoided-PTF value with the month-hour probability-of-peak method on ISO New England system load — is the rate-design platform’s [ISO-NE bulk-transmission module](https://github.com/switchbox-data/rate-design-platform/blob/main/utils/data_prep/marginal_costs/bulk_tx/bulk_tx_isone.py).

[PDF p. 7]

1. **Day type.** Each hour is labeled by month, hour beginning, and day type: weekday, or weekend-and-holiday. Saturday, Sunday, and the federal holidays take the weekend-and-holiday category.
2. **Normalize.** I divided each hour by the average hourly load of its own calendar year, which removes year-to-year load growth.
3. **Delimiter.** For each year, I took the highest month, hour, and day-type average of the normalized load, and averaged it over 2022 through 2025. An hour above this delimiter counts as a peak hour.
4. **Density in each cell.** For each of the 576 month, hour, and day-type cells (12 months × 24 hours × 2 day types), I fit a truncated Gaussian kernel density to the normalized loads in that cell (Eversource and Nieto 09-11-26).
5. **Probability of peak weighting.** The probability of peak for a cell is the share of its density above the delimiter. I divided those shares by their sum, so the 576 cells add to one.

**Step 3: Place the probabilities on the analysis calendar.** Following the Company’s approach in OCC-863 Attachment 2 (“Docket 26-05-10: Response to OCC-863” 2026), for each month and day type I divided the cell’s probability by the number of days of that type in the analysis year, and multiplied by the inflated annual cost:

$$MC_{m,d,h} = C \times \frac{PoP_{m,d,h}}{N_{m,d}}$$

$C$ is the inflated \$/kW-year. $N_{m,d}$ is the number of days of that type in that month. Each hour of 2025 then takes the weekday rate or the weekend-and-holiday rate, by the same rule as Step 2. This is the same last step as the distribution schedule: an annual cost, times a probability, divided by a day count, laid onto the calendar the residential loads are aligned to. A flat one-kilowatt load over the year pays back the inflated annual cost, which I verified. Hours whose probability is zero stay at zero. The resulting profile is the bulk transmission heatmap in Section III of my Direct Testimony.

**Q.** Can you walk through how you computed the hourly distribution marginal costs shown in Section III of your Direct Testimony?

**A.** Yes. I used the month-hour marginal costs the Company filed in response to OCC-863, Attachment 2 (“Docket 26-05-10: Response to OCC-863” 2026), and placed them on the 2025 analysis calendar. The calculation has three steps.[^8]

[^8]: The script that generates the hourly distribution and sub-transmission marginal-cost schedule from the Company’s OCC-863 Attachment 2 month-hour tables is the rate-design platform’s [distribution marginal-cost generator](https://github.com/switchbox-data/rate-design-platform/blob/main/utils/data_prep/marginal_costs/sub_tx_and_dist/generate_utility_tx_dx_mc.py).

[PDF p. 8]

**Step 1: The Company’s month-hour allocation.** Table 3 of Exhibit CLP-MCOS-2 states the system-wide marginal cost of distribution stations and trunkline feeders as \$20.17/kW-year, before losses, in 2026 dollars (Eversource 2026b). In Attachment 2 to its OCC-863 response (page 1, cell N3), the Company multiplies \$20.17 by the secondary loss factor 1.051845, which rounds to \$21.22/kW-year (“Docket 26-05-10: Response to OCC-863” 2026).

Attachment 2 then assigns that loss-adjusted annual cost to each month, hour, and day type. Page 3 is the probability that the distribution peak falls in that month, hour, and day type, measured on the Company’s substation loads (“Docket 26-05-10: Response to OCC-863” 2026). Each cell on page 1 is that probability times the loss-adjusted annual cost, divided by the number of days of that type in the month. Weekdays are one table. Weekends and public holidays are the other. I used those secondary \$/kWh values as the Company calculated them to represent the residential customers’ marginal costs at each hour.

**Step 2: Place the tables on the analysis calendar.** Attachment 2 is a set of average rates, not an 8,760-hour schedule for a specific calendar year. For each hour of 2025 I looked up the month and the hour. Saturday, Sunday, and the federal holidays take the weekend-and-holiday rate. A holiday that falls on Saturday is observed the Friday before, and one that falls on Sunday is observed the Monday after. Every other weekday takes the weekday rate. Those are the day types behind Attachment 2’s own weekend-and-holiday day counts, so the lookup reproduces the Company’s categories. I used 2025 because that is the calendar the residential load profiles are aligned to: a Monday in the marginal-cost file is a Monday in the load file.

**Step 3: Scale the year back to \$21.22/kW-year.** The day counts in Attachment 2 are not the exact number of each day type in 2025, so the looked-up 8,760 sums to \$21.35/kW-year rather than \$21.22. I multiplied every hour by 0.9939. Hours that were zero stay zero, and the ratio between any two hours is unchanged. After that scaling, the 8,760 hours sum to \$21.22/kW-year. I applied no CPI adjustment. The \$21.22 figure is already in the study’s 2026 dollars, and I used it as filed.

The resulting hourly profile is the distribution heatmap in Section III of my Direct Testimony. 2,039 hours carry a positive distribution marginal cost. The rest of the year is zero.

## 4. Incremental cost, incremental revenue, and overpayment

**Q.** What do you mean by the incremental cost of heat pump adoption?

**A.** The **incremental cost** is the change in the forward-looking marginal T&D costs that the transmission and distribution system incurs because of the customer’s heat pump
[PDF p. 9]
installation — the cost of capacity expansion triggered by consumption during the constrained hours identified in Section 3 of this exhibit.

I multiplied the representative home’s hourly electricity consumption by the hourly marginal-cost schedule described in Section 3, and summed across all 8,760 hours to get the total annual marginal T&D cost for that home. I performed this calculation for both the “before” and “after” consumption profiles. The incremental cost is the difference between the two annual totals:

$$\text{incremental cost} = \text{marginal T\&D cost after} - \text{marginal T\&D cost before}.$$

For the representative home, the incremental cost is the \$10 figure I cited in Section III of my Direct Testimony.

Because the marginal cost of every off-peak hour is zero, only consumption during the peak hours identified in Section 3 contributes to this total. Consumption in any other hour has no effect on it.

This is the same concept the Company uses as the floor for Rate 6’s discount: the discounted rate “is set to cover the incremental cost of serving the additional load the converting customer adds.”[^9] The Company does not report a dollar value for this incremental cost of the representative home. The figure above is my own estimate, computed as described in this section.

**Q.** What do you mean by incremental revenue?

**A.** The **incremental revenue** is the change in the customer’s annual delivery bill when they install a heat pump: the delivery bill after installation minus the delivery bill before.

$$\text{incremental revenue} = \text{delivery bill after} - \text{delivery bill before}.$$

The delivery bill includes three components: the fixed monthly customer charge, the distribution charges (the Distribution Energy Charge and its associated riders), and the transmission charges. It excludes generation charges, which are outside the scope of my overpayment analysis. The incremental revenue is therefore:

$$\begin{aligned}
\text{incremental revenue} \\
= \text{change in customer charge} + \text{change in distribution charges} \\

- \text{change in transmission charges}.
  \end{aligned}$$

Under Rate 1, the customer charge is the same before and after a customer installs a heat pump, so the incremental revenue comes entirely from the change in distribution and transmission charges. Including the customer charge matters when I evaluate a rate with a different customer charge. In every comparison, the “before” bill is the customer’s pre-

[^9]: Response to CLF-003(b), Docket No. 26-05-10 (Sept. 3, 2026) (Eversource 2026a).

[PDF p. 10]
installation bill under Rate 1. So when I evaluate Rate 6, which raises the customer charge from \$12.36 to \$30.95 per month, the difference in customer charges counts toward the incremental revenue, just as a change in volumetric charges would.

**Q.** What is the fair annual bill?

**A.** The **fair annual bill** is what a customer should pay for delivery service after installing a heat pump: the delivery bill they paid before the installation, plus the incremental cost.

$$\text{fair annual bill} = \text{delivery bill before} + \text{incremental cost}.$$

This is the standard of cost causation. A customer installing a heat pump is an existing customer, already paying their pre-installation bill toward the system’s existing costs. Their bill should change by exactly the change in T&D costs their new load profile causes.

**Q.** How do you define the overpayment caused by heat pump adoption?

**A.** Overpayment is the difference between a customer’s delivery bill after installing a heat pump and its fair annual bill. Equivalently, it is the incremental revenue minus the incremental cost:

$$\text{overpayment} = \text{delivery bill after} - \text{delivery bill before} - \text{incremental cost}.$$

A positive overpayment means the customer is overpaying: their bill changed by more than the costs their heat pump causes. A negative value means the customer is underpaying. Under a perfectly cost-reflective rate, every customer’s overpayment would be zero.

The theoretical “fair rate” benchmark shown in Sections IV, V, and VII of my Direct Testimony is defined directly from these quantities: it sets each customer’s post-heat-pump delivery bill equal to its fair annual bill, which is equivalent to removing each building’s individual delivery overpayment from its Rate 1 bill change.

**Q.** For which customers did you compute the overpayment?

**A.** I computed it in two ways, using the same formula.

For the **representative home** in Section III of my Direct Testimony, I applied the formula to the average fossil-fuel-heated home’s before-and-after consumption profiles described in Section 2. For that home, the result is an annual overpayment of \$1,040.

For the **distributions of overpayment** shown in Sections III, V, VII, and X of my Direct Testimony, I applied the formula to each fossil-fuel-heated ResStock building in the Company’s territory — homes heated with natural gas, heating oil, or propane —
[PDF p. 11]
individually. For each building, the “before” bill is CAIRO’s annual bill under Rate 1 for the building with its existing heating system, and the “after” bill is CAIRO’s annual bill under the rate being evaluated for the same building with a heat pump. Each building’s incremental revenue is the difference between those two bills. Its incremental cost is computed in exactly the same way as for the representative home: its own hourly grid consumption times the hourly marginal-cost schedule from Section 3, summed over the year, after minus before. I verified that this matches CAIRO’s per-building marginal-cost totals to within \$1 per building. Averages across buildings use ResStock’s sample weights.[^10]

The representative home applies the formula to an average consumption profile, while the distributions average the result of applying it to each home.

## 5. Rate HP derivation

**Q.** How did you derive the proposed Rate HP rates shown in Section X of your Direct Testimony?

**A.** Rate HP changes only two charges: the distribution and transmission volumetric rates during the winter months (November through March). The customer charge, the distribution riders, the generation rate, and the summer (April through October) distribution and transmission rates all stay at their proposed Rate 1 levels.[^11]

For each of the two components, I solved for the single winter rate at which the average fossil-fuel-heated customer’s overpayment, as defined in Section 4, is zero. In other words, the winter rate at which the representative home’s post-installation bill for that component equals its fair annual bill:

$$\text{fair annual bill} = \text{bill before} + \text{incremental cost},$$

where the bill before is computed under Rate 1, and the incremental cost is that component’s share of the incremental cost: the change in distribution marginal costs for distribution, and the change in bulk transmission marginal costs for transmission, using the hourly schedules in Section 3.

Under Rate HP, the representative home’s post-installation bill for each component is its summer consumption at the Rate 1 rate, plus its winter consumption at the Rate HP winter rate:

[^10]: The notebook that computes each building’s delivery overpayment and the weighted distributions shown across rate scenarios is the report’s [overpayment notebook](https://github.com/switchbox-data/reports2/blob/main/reports/ct_hp_rates/notebooks/overpayment.qmd).

[^11]: The script that derives these Rate HP winter delivery rates from the CAIRO overpayment results and writes the tariff files is the rate-design platform’s [ICOS tariff-derivation script](https://github.com/switchbox-data/rate-design-platform/blob/main/utils/mid/derive_icos_tariff.py).

[PDF p. 12]

$$\text{bill after}_{\text{R-HP}} = r_{\text{Rate 1}} \cdot \text{kWh}_{\text{after, summer}} + r_{\text{winter}} \cdot \text{kWh}_{\text{after, winter}}.$$

Setting this equal to the fair annual bill and solving for the winter rate gives:

$$r_{\text{winter}} = \frac{\text{fair annual bill} - r_{\text{Rate 1}} \cdot \text{kWh}_{\text{after, summer}}}{\text{kWh}_{\text{after, winter}}}.$$

Because the summer rate is unchanged, the entire correction falls on winter consumption. Equivalently, the winter rate is Rate 1’s winter bill for the post-installation profile, minus the overpayment under Rate 1, spread over the post-installation winter kWh. For the representative home, the result is a winter distribution rate of 2.622 ¢/kWh (including riders) and a winter transmission rate of 1.258 ¢/kWh. Because the riders are unchanged, the winter Distribution Energy Charge shown in the Rate HP table in Section X of my Direct Testimony is the winter distribution rate minus the riders.

The customer charge does not enter this calculation. It is the same before and after installation, and the same under Rate 1 and Rate HP, so it contributes nothing to the incremental revenue.

**Q.** How did you evaluate Rate HP across all fossil-fuel-heated customers?

**A.** The single Rate HP tariff is derived once, across all fossil-fuel-heated homes. Because the representative home’s load profile is the weighted average of all fossil-fuel-heated buildings, solving for the winter rate across all of those buildings gives the same result as solving it on the representative home — here applied to the combined delivery rate (distribution, riders, and transmission together) rather than to each component separately:

$$r_{\text{winter}} = \frac{r_{\text{Rate 1}} \cdot \overline{\text{kWh}_{\text{before}}} + \overline{\text{incremental cost}} - r_{\text{Rate 1}} \cdot \overline{\text{kWh}_{\text{after, summer}}}}{\overline{\text{kWh}_{\text{after, winter}}}},$$

where each bar denotes a weighted average across all fossil-fuel-heated buildings, using ResStock’s sample weights, and each building’s incremental cost is computed as described in Section 4. The resulting combined winter delivery rate is 3.880 ¢/kWh; the summer delivery rate and the customer charge are unchanged from Rate 1.

I then simulated this single tariff in CAIRO for every fossil-fuel-heated ResStock building in the Company’s territory. The resulting distribution of overpayments under Rate HP is reported across all fossil-fuel-heated homes in Section X of my Direct Testimony, and the resulting total energy bill impacts are disaggregated for natural-gas-heated and delivered-fuel-heated homes in Section XI.

## 6. Fixed-charge alternative

[PDF p. 13]

**Q.** In Section XIII of your Direct Testimony, you testified that eliminating the heat pump overpayment by redesigning Rate 1 would require raising the monthly customer charge from \$12.36 to \$121.49. How did you calculate that figure?

**A.** This is a redesign of Rate 1 itself, applied to every residential customer. It is not Rate HP. Rate HP, described in Section 5, keeps the customer charge at Rate 1 and lowers only the winter distribution and transmission rates, and only for heat pump customers. The alternative in Section XIII instead keeps a single default rate for the whole residential class and moves revenue from volumetric delivery charges onto the customer charge.

I solved for the version of Rate 1 that satisfies two conditions at the same time, for the representative fossil-fuel-heated home defined in Section 2.

The first condition is **cost reflectivity**. After the redesign, that home’s incremental revenue from the targeted volumetric charges must equal its incremental cost, so its overpayment, as defined in Section 4, is zero. The targeted charges are distribution (the Distribution Energy Charge and its riders) and transmission. I scaled both by one factor, the same in every month. I did not change generation charges.

The second condition is **revenue neutrality** for the residential class. The revenue held constant is the revenue collected through the charges the redesign touches: the monthly customer charge plus the targeted volumetric charges. Generation revenue is outside the redesign. Whatever revenue the lower volumetric rates give up must come back through the customer charge.

**Q.** How did you determine the factor by which the targeted volumetric rates would have to fall?

**A.** The factor does not depend on the customer charge. The redesigned rate applies both before and after a customer installs a heat pump, so the customer charge — whatever its level — is paid in both cases and contributes nothing to the incremental revenue. Only the targeted volumetric charges change. Setting the overpayment to zero therefore requires:

$$\lambda^* \times \text{incremental revenue} = \text{incremental cost},$$

where the incremental revenue is the change in the representative home’s distribution and transmission charges under proposed Rate 1, and the incremental cost is the change in its marginal T&D cost, both as defined in Section 4. Solving for the scaling factor $\lambda^*$ gives:

$$\lambda^* = \frac{\text{incremental cost}}{\text{incremental revenue}}.$$

Under proposed Rate 1, the representative home’s incremental revenue from the targeted charges is \$1,051 per year — \$726 in distribution charges and \$325 in transmission charges. Its incremental cost is \$10 per year. The difference is the \$1,040 annual overpayment I cited in Section III of my Direct Testimony.

_Extractor note (not source text): the printed components and totals do not reconcile exactly to the rounded figures: \$726 + \$325 = \$1,051, and \$1,051 − \$10 = \$1,041, against the printed \$1,040. The difference is consistent with rounding of the underlying values._

[PDF p. 14]

For CL&P, the factor is 1.0%. The targeted volumetric rates would have to be cut by approximately 99%, to 1.0% of their filed levels. At that level, the representative home’s post-installation distribution and transmission bill equals its fair annual bill for those charges. Generation charges are unchanged.

**Q.** How did you then determine the fixed charge?

**A.** From the revenue-neutrality condition. Cutting the targeted volumetric rates to 1.0% of their filed levels leaves 99% of the revenue those charges collect from the residential class to be recovered through the customer charge.

I computed that class revenue from the Company’s Rate Year residential billing determinants in Exhibit CLP-RATES-2: 1,076,695 residential customers, on average, and the class’s billed residential sales.[^12] I applied the filed distribution and transmission rates — which do not vary by month — to those sales. The two targeted charges collect approximately \$1,322 per residential customer per year. The redesign removes approximately \$1,310 of that amount per customer per year. Spread across twelve monthly bills, replacing it requires raising the customer charge by \$109.13 per month:

$$F^* = F_0 + \frac{(1 - \lambda^*)\,V_{\text{class}}}{12\,N_{\text{class}}}$$

where $F_0$ is the proposed Rate 1 customer charge, $V_{\text{class}}$ is the annual revenue the targeted volumetric charges collect from the residential class, and $N_{\text{class}}$ is the number of residential customers. Starting from \$12.36 per month, the result is a customer charge of \$121.49 per month.

Raising the customer charge does not itself reduce the overpayment. Because every customer pays the new charge both before and after installing a heat pump, it still contributes nothing to the incremental revenue. The charge rises only to keep the residential class’s delivery revenue unchanged after the volumetric rates are cut.

---

## References

“Docket 26-05-10: Response to OCC-863.” 2026.

EIA. 2024. “Heating Oil and Propane Update (Form EIA-877).” <https://www.eia.gov/petroleum/heatingoilpropane/>.

Eversource. 2026a. “Docket 26-05-10: Exhibit CLF-003_Final.”

[^12]: Exhibit CLP-RATES-2, Rate Year build: 12,920,344.76 annual bills rendered and 8,716,958.14 MWh of billed residential sales. The customer count is the annual bills divided by twelve. The starting customer charge is CL&P’s proposed Rate 1 charge, including the 6.8% Gross Earnings Tax.

[PDF p. 15]

———. 2026b. “Docket 26-05-10: Exhibit CLP-MCOS-2.” Connecticut Public Utilities Regulatory Authority.

———. 2026c. “Docket 26-05-10: Exhibit CLP-RATES-2.”

———. 2026d. “Docket 26-05-10: Exhibit CLP-RATES-3.”

Eversource, Edward Davis, and Kimberly Parsons. 2026. “Docket 26-05-10: CLF-SC-008_Final.”

Eversource, and Amparo Nieto. 09-11-26. “Docket No. 26-05-10 OCC-733.”

Eversource, Kimberly Parsons, and Edward Davis. 2026. “Docket 26-05-10: CLF-SC-009_Final.”

ISO-NE. 2026. “Open Access Transmission Tariff (OATT), Section II.” <https://www.iso-ne.com/static-assets/documents/regulatory/tariff/sect_2/oatt/sect_ii.pdf>.

———. n.d. “ISO-NE Web Serices [sic] API: Real-Time Hourly Demand by Load Zone.” Accessed October 16, 2026. <https://www.iso-ne.com/isoexpress/web/reports/load-and-demand/-/tree/demand-by-zone>.

NREL. 2024a. “End-Use Load Profiles for the U.S. Building Stock.” DOE Open Energy Data Initiative (OEDI); National Renewable Energy Laboratory (NREL). <https://doi.org/10.25984/1876417>.

———. 2024b. “ResStock 2024.2 Release: Technical Documentation.”

———. 2026. “Customer Affordability, Incentives, and Rates Optimization (CAIRO) Model.” NREL. <https://github.com/NatLabRockies/CAIRO>.

Synapse. 2024. “Avoided Energy Supply Components (AESC) in New England: 2024 Report.” Synapse Energy Economics.

U.S. Bureau of Labor Statistics. 2025. “Consumer Price Index for All Urban Consumers: All Items in U.S. City Average (CUUR0000SA0).” Federal Reserve Bank of St. Louis (FRED). <https://fred.stlouisfed.org/series/CUUR0000SA0>.

U.S. Energy Information Administration. 2018. “Form EIA-176: Annual Report of Natural and Supplemental Gas Supply and Disposition.” <https://www.eia.gov/naturalgas/data.php>.
