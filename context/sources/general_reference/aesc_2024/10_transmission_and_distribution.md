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
extraction_scope: "partial: PDF pp. 288-336 (printed pp. 270-318), Chapter 10 Transmission and Distribution (10.1-10.5); the other files of this folder hold the rest of the report"
citation_scheme: page
context: "Prepared for the AESC 2024 Study Group (New England electric and gas program administrators, energy offices and regulators), the triennial study that sets the avoided costs used to screen energy efficiency and other demand-side programs in all six states. Released February 7, 2024 and amended May 24, 2024 to correct summer on-peak energy values; this is the amended release."
contents: "Chapter 10 of AESC 2024: a six-step general method for system-level avoided transmission and distribution (T&D) cost (10.1); the avoided pool transmission facilities (PTF) cost of $69 per kW-year (2024 dollars) derived from ISO New England's 2050 Transmission Study, with its carrying-charge assumptions, comparison with AESC 2018 ($112) and AESC 2021 ($95), and treatment of Regional Network Service (10.2, Table 129); a survey and assessment of how National Grid, United Illuminating, Eversource, Unitil, Vermont and Maine value avoided non-PTF T&D (10.3, Tables 130-136); the three-step localized (non-wires alternative) avoided T&D method and utility NWA screening criteria (10.4, Tables 137-144); and a pointer to Chapter 2 for avoided natural gas T&D (10.5)."
why_here: "Source for the AESC avoided PTF value ($69 per kW-year), the load-growth-based avoided T&D method (investment divided by actual peak load growth, real-levelized carrying charge, O&M and overheads), and the survey of New England utilities' avoided distribution values, which a New England heat pump rate design, marginal cost of service or cost allocation case may cite or contrast with its own marginal T&D costs; the chapter also addresses how electrification load on a winter peak is valued against T&D avoided costs."
---

_Extractor note (not source text): this file holds PDF pp. 288-336 (printed pp. 270-318) of AESC 2024, Chapter 10: Transmission and Distribution; the rest of the report is in the other files of this folder (see README.md), so those pages are marked not transcribed here. The text is transcribed verbatim; no source typos were corrected (apparent source errors are marked `[sic]` or `[source discrepancy: …]`). The source's running headers and footers are omitted, and the PDF's text layer drops some letters in several table captions (for example "Assess ent" for "Assessment"), which were read from the rendered pages. Superscript and subscript units in the source (for example "kW" with subscript "hardware") are written with `<sub>` tags. Headings are levelled by the source's typography: bold numbered headings `##`, bold headings `###`, bold-italic headings `####`, underlined headings `#####`._

[PDF pp. 1-287 not transcribed: front matter and Chapters 1-9 (executive summary through avoided costs of compliance with renewable portfolio standards), in the other files of this folder (see README.md)]

[PDF p. 288 | printed p. 270]

# 10. Transmission and Distribution

In addition to avoiding various types of generation costs (energy, capacity, and associated DRIPE), load reductions can contribute to deferring or avoiding the addition of load-related T&D facilities, due to reduced load growth and reduced loading of existing equipment.[^329] This chapter describes a methodological approach that program administrators can use to estimate avoidable T&D costs for planning and reporting of efficiency program benefits. It also quantifies avoided costs related to pool transmission facilities (PTF) transmission based on forward-going investments and identifies methodologies that could be used for estimating other categories of avoided T&D, including local T&D.

We estimate an avoided PTF cost of $69 per kW-year. For AESC 2024, we updated this value based on a recent ISO New England study that estimates future transmission investments through to 2050. AESC 2021 estimated a PTF avoided cost of $84 per kW-year in 2021 dollars ($95 per kW-year in 2024 dollars). We derived this value from the AESC 2018 avoided PTF value by applying an adjustment factor which represented the difference in future T&D spending relative to historical investments.

The Synapse Team also surveyed some of the sponsoring utilities (National Grid, United Illuminating, and Eversource Connecticut) for information on utility avoided T&D value estimates, along with the methods used to calculate those values, as part of AESC 2018. The common evaluation rubric was updated in 2021 and is again presented in AESC 2024. It includes:

1. Reviewing utility approaches to generic avoided cost values for non-PTF T&D and evaluating these approaches on a common evaluation rubric to facilitate cross-comparison and learning.
2. Reviewing utility approaches to calculating geographically localized avoided costs, such as for NWAs.
3. Developing an approach to the avoided cost of natural gas system T&D. See Section 2.4: _Avoided natural gas cost methodology_ for more information on the assumptions used in AESC with respect to natural gas T&D.

In addition to evaluating different approaches to geographically localized avoided costs for NWAs as a standalone aspect of analysis, AESC studies examine whether the appropriate treatment or calculation of T&D avoided costs differs for other specific technology types or program applications, such as distributed generation and electrification or other fuel-switching programs. AESC 2024 addresses the locational value of potential services provided by efficiency and other DERs; we do not address programmatic or other barriers to using DERs to address T&D costs.

[^329]: Many energy efficiency programs will be cost-effective without consideration of avoided T&D costs, and many load-control programs will not reliably reduce peak loads on T&D equipment. These will not be eligible to be credited with avoided T&D equipment. For some energy efficiency measures and programs, especially those with very peaky load shapes, the avoided T&D costs may be critical in demonstrating cost-effectiveness.

[PDF p. 289 | printed p. 271]

This section begins with an overview of the recommended approach for calculating avoided T&D costs, which can then be tailored to the specific situation for which costs are to be calculated. We then proceed through the different aspects and scales of such analysis in New England, beginning with regionwide PTF avoided costs. The subsequent two sections address avoided T&D at smaller scales: first for a utility service territory or other program-wide jurisdiction, and then for specific locations on areas within a service territory which may warrant location-specific avoided T&D values due to an existing constraint. For each of these scales, we present an evaluation of the relevant methods currently used by utilities within the region. The section concludes with an analysis of the equivalent structure for natural gas distribution (see Section 2.4: _Avoided natural gas cost methodology_ for more information).

## 10.1. General approach to estimating the value of system-level avoided T&D

The following steps, unchanged from AESC 2021, summarize a standardized approach to estimate generic system-level avoidable transmission or distribution costs:

- Step 1: Select a time period for the analysis, which may be historical, prospective, or a combination of the two.
- Step 2: Determine the actual or expected relevant load growth in the analysis period, in MW.[^330]
- Step 3: Estimate the load-related investments in dollars incurred to meet that load growth.
- Step 4: Divide the result of Step 3 by the result of Step 2 to determine the cost of load growth in $ per MW or $ per kW.
- Step 5: Multiply the results of Step 4 by a real-levelized carrying charge to derive an estimate of the avoidable capital cost in $ per kW-year.
- Step 6: Add an allowance for O&M of the equipment to derive the total avoidable cost in $ per kW-year.

The data for this approach may come from historical top-down accounting data, such as from page 206 of the utility's annual FERC Form 1 filing, or from bottom-up data based on past and future expenditures by project or budget line item.

These generic avoided T&D costs are not intended to represent the potential value of targeted load reductions, as part of NWAs to specific T&D projects. Analysis of targeted NWAs requires information about the cost and timing of the specific project to be avoided and the amount of load reduction

[^330]: The data could be for hypothetical growth levels, but the effort of determining the investments necessary to meet a hypothetical growth level is likely to be excessive. Hence, most analyses rely on actual investments (which are known) or fully developed investment projects for the relatively short-term future.

[PDF p. 290 | printed p. 272]

required to defer project need for one or more years. The methodology for localized value of avoided T&D is the subject of Section 10.4 below.

The goal of these generic avoided-cost computations is not to identify specific projects that can be avoided, but to estimate the overall, long-term ratio of T&D savings per kW of avoided load growth (and hence of a kW of peak savings).[^331]

The avoided T&D value is generally applied as if every kW of load reduction in any location will have the same value. This is a useful simplification, which is reasonable for widespread energy efficiency programs. In some places and times, even small load reductions that keep load below the capacity of existing equipment may defer or avoid very large incremental T&D investments. In other places and times, relatively large load reductions may have little effect on T&D investments. The location contributing to new T&D investments can vary from perhaps a dozen residential customers sharing a line transformer to thousands of customers sharing a substation or a transmission line. Since avoidable T&D costs are estimated as the ratio of actual or near-term expected investment to actual or expected load growth, the specific projects used in the analysis are not usually avoided.

Depending on the amount of excess capacity on the various levels of T&D equipment in a particular area, reducing load by any particular customer may defer or avoid the addition of a line transformer in the next year. It may also contribute to delaying or avoiding the reconfiguration of feeder, the upgrading of a substation, and the construction of transmission lines in following years. At another location, load reductions may have little effect on T&D investment for many years. Recognizing this complex dynamic, the general approach in this report computes the average ratio of all load-related investments to all load growth, rather than just the load growth that has the greatest effect on investment to develop avoided costs.[^332]

The methods and approach described here are generally independent of the technology or program that changes peak load. For example, the value of avoiding transmission investments does not depend on whether the peak was reduced by energy efficiency, demand response, or distributed generation—as long as the peak reductions are the same. It is also critical that the peaks in question are the same peaks: if transmission needs are driven by a summer system-wide peak, or distribution needs are driven by a winter morning, then the characteristics of a given measure or program at those times are what matter for avoiding expenditures. The marginal benefit of reduced peak should also be the same as the marginal cost of increased peak: electrification measures that increase a peak relevant for T&D infrastructure planning will, on the margin, create costs at the same rate (in $/kW) that load reduction measures reduce them. Note that time coincidence matters for electrification as well as energy

[^331]: Analysts do not generally have _ex post_ estimates of costs that have actually been (or are expected to be) avoided by energy efficiency; such analysis, if feasible, would usually be prohibitively expensive.

[^332]: Geographically targeted load reductions, such as part of an NWA to a transmission or distribution project, may have much higher values, depending on the magnitude and time of need, as discussed in more detail in Section 10.4.

[PDF p. 291 | printed p. 273]

efficiency: electrification measures that increase a winter peak do not cause T&D expenditures if those expenditures would be driven by the need to meet loads at a summer peak.

The remainder of this section provides an overview of background, context, and considerations to use as guidance in developing avoided T&D values. The following two subsections apply these lessons and guidance to PTF transmission (Section 10.2) and to evaluation of the methods used for generic avoided T&D in the region today (Section 10.3: _Survey of utility avoided costs for non-PTF transmission and distribution_).

### Criteria for avoided T&D estimation

The following considerations are useful in guiding the estimation of avoided T&D costs:

- **Time period.** In estimating the avoided T&D cost, any analysis should use data from complete, consistent, and reasonable time periods for both load and investment. It may be useful to align these timelines with those used for distribution planning and capital investment planning processes.
- **Investment plans and budgets for any future period must be reasonably complete.** It is important to capture all of the expected T&D costs along with all of the expected changes in load within the period selected for analysis. Investment plans that include only a portion of projected costs (for example, those associated with only larger projects with long lead times) should not be the only source of cost information.
- **The analysis period should provide a reasonable proxy for the long-term relationship between load and investment.** If the period starts with the system overbuilt due to unexpected load reductions, the analysis will tend to understate the cost per kilowatt and vice versa. The analysis should avoid or correct for unrepresentative conditions due to unexpected growth or deferred investments.

On a related point, adjusting the loads to account for weather conditions is likely to be more representative than actual loads in determining the amount of load growth in the analysis period, so weather adjustment may be necessary. Taking actual load growth between a hot summer with high loads and a subsequent mild summer with low loads would understate the amount of load growth driving the investment, and vice versa.

Some T&D investments are driven by load growth from new customers in areas that are not currently served, or are not served in a manner that would accommodate the growth, even with very aggressive energy efficiency efforts in new and existing loads in the area. For example, serving major commercial development in a previously residential exurban area or a 100-unit residential development in an agricultural area may require a new substation or feeder respectively, regardless of any conceivable load reduction. Analyses of avoided T&D costs generally omit these projects; where possible, the load growth served from these projects should also be omitted from the computation.

Even utility systems with little total load growth tend to have areas in which peak loads are growing, offset by areas in which peak loads are declining (due to some combination of energy efficiency

[PDF p. 292 | printed p. 274]

programs, other conservation, and economic and demographic trends). In those situations, the computation of avoided T&D costs should ideally represent the investments in the growing areas, divided by load growth in those same growing areas. This greater level of detail is rarely possible, especially on a feeder-specific or transformer-specific basis.

Investments should be converted to some common price basis (such as by adding or removing inflation) so that investments in differing years (e.g., 1997, 2007, 2017, and 2027) can be added together. Any projections or hypothetical adjustments to the historical periods should be handled consistently for load growth and investment.

The AESC avoided costs are based on hypothetical worlds in which no energy efficiency programs (and/or no other load management or electrification programs) are implemented going forward. For consistency in identifying the full T&D costs avoidable by energy efficiency programs, it would be desirable to start with the loads that would have occurred and the investments that would have been needed without energy efficiency efforts. Estimating the effect of the energy efficiency programs on historical and forecast loads may be feasible. Unfortunately, estimating the T&D investments that would have been needed without the energy efficiency programs is generally infeasible, requiring a large amount of engineering analyses to develop hypothetical needs at the feeder level.[^333]

If a fully consistent no-energy efficiency (no-EE) analysis could be performed, that would be ideal. But an analysis that combined loads from a "no-EE" premise with investments from the "with-EE" reality would understate avoidable costs.

### Disaggregation of growth

For each type of equipment, the computed load growth should reflect the load on that type of equipment. The T&D system consists of several types of equipment, which may be simplified into the following categories:

- high-voltage transmission lines (115 kV to 345 kV);
- transmission substations connecting transmission lines at different voltages;
- sub-transmission lines (e.g., 69 kV) that connect to distribution substations and some very large customers;
- bulk distribution substations that step transmission voltages down to generally high distribution voltages (mostly at 13.8 kV to 25 kV);
- high-voltage primary feeders that distribute power from the bulk substations to lower-voltage substations, some primary-voltage customers, and line transformers;

[^333]: The actual and projected energy efficiency may have avoided the planning and construction of more expensive T&D projects, but those costs are not generally available. The available data generally estimates the benefit of additional load reductions, on top of those that have occurred and are planned.

[PDF p. 293 | printed p. 275]

- lower-voltage substations that step down the power to lower (mostly legacy) voltages, in the 2 kV to 8 kV range;
- low-voltage primary feeders that distribute power to primary-voltage customers and line transformers;
- line transformers that step power down from the primary distribution voltages (2 kV to 35 kV) to secondary voltages (110 V to 500 V);
- secondary lines from the transformer customer service drops; and
- service drops from the street to customer meters.

Figure 58 illustrates the general design of T&D systems. The range of voltages considered to be sub-transmission varies among utility systems.

**Figure 58. Schematic of a T&D system**

[DIAGRAM DESCRIPTION: Figure 58. Schematic of a T&D system]

A black-and-white line-drawing schematic of an electric power system, drawn as a continuous serpentine loop of power lines that runs left-to-right across the top, down the right side, right-to-left across the second row, down the left side, left-to-right across the third row, down the right side and right-to-left along the bottom, so that power flows from the generating station at the top left through progressively lower voltages to end customers at the bottom. Labeled elements, in order along the path: (1) Top row: "Generating station" (a building with a smokestack) feeding "20,000 Volts" to a "Step-up transformer", which connects to lattice towers carrying the "138,000 Volts transmission" lines; a "Step-down transformer" on the transmission line steps down to "4000 Volts" to serve an "Industrial consumer" (a factory building). (2) Second row: the 138,000-volt line reaches a "Transmission substation" with a "Step-down transformer" (beside a lattice tower), from which a "34,500 Volt subtransmission" line runs back to the left; on this line a "Step-down transformer" serves an "Industrial consumer" at "440 Volts". (3) Third row: the 34,500-volt subtransmission line reaches a "Distribution substation" with a "Step-down transformer", which feeds "13,800 Volt distribution" lines on poles; along these lines a "Step-down transformer" connected through an "Underground vault" serves a "Commercial or industrial consumer 220/440 volts", and "Step-down transformers" serve a "Commercial consumer" at "120/240 Volts". (4) Bottom row: the "13,800 Volt distribution" line continues to "Step-down transformers" serving a "Farm-rural consumer" at "120/240 Volts" and a "Step-down transformer" serving a "Residential consumer" at "120/240 Volts". The figure has no numeric axes or data series; it conveys the voltage hierarchy of the system (generation at 20,000 V, transmission at 138,000 V, subtransmission at 34,500 V, distribution at 13,800 V, and service at 440 V, 220/440 V or 120/240 V) and which customer types connect at which level.

[→ See original PDF page 293 for visual rendering]

_Source: Electric Power Generation, Transmission and Distribution eTool. U.S. Department of Labor. Available at [https://www.osha.gov/SLTC/etools/electric_power/illustrated_glossary/](https://www.osha.gov/SLTC/etools/electric_power/illustrated_glossary/)._

[PDF p. 294 | printed p. 276]

Any load reduction may result in avoidance or delay of investments at one or more of these levels, in the near term or over many years.

All loads use transmission; primary and secondary loads use the primary distribution system; and only secondary loads use line transformers and secondary lines. Hence, T&D analyses should use the peak loads applicable to the transmission or distribution capacity appropriate to the particular analysis.

### Computation of T&D avoided costs

Generally, the computation of avoided costs in $/kW should use the same measure of load that will be used in screening. This criterion requires that the units of load reduction used to attribute avoided costs to programs be consistent with the units of load used to compute those avoided costs. The units should be consistent on a number of dimensions, including the timing of the load peaks, the treatment of seasonal load, the use of normal or extreme loads, and the treatment of losses.

Generation capacity avoided costs are driven by load at the time of the ISO New England peak, which has by convention been associated with an hour ending at 3 p.m. or 5 p.m. on a hot summer day. For simplicity, energy efficiency screening often uses these same peak conditions for estimating contribution to T&D peaks, in which case the avoided T&D costs should be computed per kilowatt of growth in contribution to regional peak. Since T&D assets reach their peak loads at different times, in both summer and winter, some utilities may use a different measure of peak load (e.g., sum of class peaks, sum of summer and winter peak) to derive the $/kW ratio, in which case that alternative measure of peak load should be used for valuing the T&D savings in the screening process.

If the avoided T&D costs are to be allocated between summer and winter peak contributions in screening, then the avoided-cost analysis should similarly reflect both summer and winter load growth. Assuming that winter peak growth equals summer peak growth is rarely realistic.

Transmission and some distribution facilities are designed for extreme weather (or other conditions), such as those in the ISO New England's 90/10 load forecasts. It may thus be tempting to divide investment by the growth in load that would occur under extreme conditions, rather than normal peak conditions (e.g., those that would be expected to be exceeded about half the time). If the analysis computes avoided T&D costs in $/kW<sub>extreme</sub>, screening must use estimates of load reduction under extreme conditions. For some end uses, load reductions will be very similar at normal and extreme peaks, but for others (air conditioning and solar in the summer, heating in the winter) the reductions under extreme conditions will exceed those at normal peaks.[^334] If screening assumptions cannot be developed for extreme conditions, analysts should avoid the use of extreme loads in the avoided-cost analyses. Note that this may mean using different weather for the purposes of demand-side measure evaluation than is used for T&D system planning, and tracking different "flavors" of peak load or developing equivalency relationships may be required.

[^334]: Something must use more energy at the extreme peak, or it would not be an extreme peak.

[PDF p. 295 | printed p. 277]

Similarly, if screening uses load reduction at the end use, the avoided T&D costs should use load growth at the end use. If this apples-to-apples structure is not possible (such as if load growth is measured at transmission level) the appropriate loss factor must be added to the avoided cost.

### Identifying load-related investments

The investment should include all identifiable load-related costs, but no more. AESC studies recommend using top-down accounting analyses to identify the accounts that are primarily load-related[^335] and net out an allowance for the costs of replacing retired equipment in kind. The FERC Form 1 data include both additions and retirements by account. Bottom-up analyses should be used to identify the projects and blanket accounts that are primarily load-related.[^336]

For the bottom-up analyses, we recognize that differentiating investments between those required by load growth from those required for other considerations can be complex. The non-load-related investments may include:

- Distribution assets (primarily meters and services) that are driven entirely or predominantly by the number of customers.[^337]
- Primary distribution projects that extend service into areas that have not previously been served, to connect new customers. New construction energy efficiency programs may avoid a small portion of the wire costs. However, most of the costs are related to the extension of supply to new areas.
- Some transmission projects that are required to integrate generation or allow targeted imports. Generation interconnection costs will generally be included in the generation market prices. Transmission projects supporting policy-driven imports of renewable energy from Canada or offshore wind are unlikely to be affected much by load reductions, at least in the short term.[^338]
- Some T&D investments simply replace old equipment. Other investments relocate facilities due to road widening, loss of easements, and similar factors. Neither type of investment is load-related.

[^335]: As the availability and granularity of data improves through technologies and planning advancements, we anticipate improvements in the methodology for identification of load-related investments that can be avoided through DERs and applicability to more feeders. The methodology described here is based on identifying load-related investments using current distribution system planning practices.

[^336]: A blanket account in the context of distribution utilities typically includes a large number of similar investments, such as substation upgrades or line-transformer replacements.

[^337]: Service drops are often sized or upgraded based on the end uses in a building. In principle, energy efficiency should reduce the required service size and cost. It is not clear how consistently utilities or contractors take building efficiency into account in determining the size of the service drop to be installed.

[^338]: Energy efficiency measures installed in the near term may (by reducing the use of fossil generation) reduce the motivation for further clean-import mandates and associated generation. Predicting the timing of future initiatives may be challenging.

[PDF p. 296 | printed p. 278]

In contrast, other investments are clearly required to accommodate load growth, including:

- Most new transmission lines and substations and additional transformers at existing substations;
- Additional feeders and line transformers in areas with existing service;
- Reconductoring of lines to increase capacity;
- Increasing the voltage of transmission or distribution lines; and
- Conversion of single-phase feeder branches to two-phase or three-phase operation.

A third set of investments is harder to characterize, including such situations as:

- Investments triggered by factors other than load, but whose cost are increased to accommodate higher load levels. For example, if rotting poles are being replaced with taller poles so that the feeder voltage can be increased in the future, the incremental cost of the taller poles is load-related. The cost of replacement may be unavoidable, but the load-related improvement may be avoidable.[^339]
- The costs of removing aging, but functional equipment to allow installation of higher-capacity equipment. The existing equipment might need to be replaced in another decade or two, even without the load growth, but most of the present value of the replacement cost would be due to the load-related timing of the project.
- Investments required to complete or modernize projects already in service, such as improved lightning arrestors or added SCADA equipment on existing feeders. These investments may be considered as a continuing cost of the original load-related projects (as post-operational capital additions are considered part of the cost of a power plant), and hence an adder to avoided cost (perhaps computed in dollars per MW of load, rather than dollars per MW of load growth). On the other hand, if the improvements are being driven by a one-time change in reliability or safety standards or technology, perhaps no similarly deferred improvements should be anticipated for equipment driven by future load growth.
- Replacement of equipment degraded by both age and loading levels. For example, high loads (especially high loads over many hours in a day) increase the rate at which insulation breaks down in underground lines, substation transformers, and line transformers. High loads on transmission lines also increase the line sag (possibly violating clearance requirements) and weaken the conductor. Replacements of load-carrying equipment will generally be at least partly driven by load levels, but the extent of this effect may be difficult to separate from the effects of time.

[^339]: In principle, the decision not to downsize the replacement may also be load-related, but the incremental component of project cost may be difficult to quantify.

[PDF p. 297 | printed p. 279]

- Investment driven by load-related energy considerations, including transmission congestion relief and reduction of line losses.[^340]

AESC studies recognize that these situations complicate the neat division of projects and accounts into load-related and non-load related categories. Classification of specific projects or accounts as avoidable or unavoidable by energy efficiency should be clearly documented and explained.

### Matching investment to load growth

Bottom-up analyses should include all the investment in load-related equipment entering service in the analysis period, including investment prior to the start of the analysis period. Any project costs that stretch beyond the in-service date of the equipment (e.g., for removal of retired equipment, environmental compliance, addition of communications or control equipment) should be included as well. Top-down accounting-based data will include all the costs of a project in the year that the project enters service but may count some deferred costs in the following year.

The load growth used in computing avoided distribution costs should reflect the loads at the distribution level, excluding loads served directly from transmission lines, for which the utility does not provide distribution equipment. Similarly, where the avoided cost of secondary distribution is computed separately from the primary distribution, the load growth should reflect only the loads served at the secondary distribution level.

While the load growth used in computing avoided distribution costs should reflect the loads of customers served at distribution, the growth in distribution loads may be stated in terms of MW at the transmission level, at the distribution level, or at the meter.[^341] Contribution of distribution loads to system or area peaks are highest when measured at the transmission level, lower at the distribution level, and still lower at the customer's meter. This is because the transmission-level loads include line losses from the meter to transmission, distribution-level loads include line losses from the meter to the feeder or substation, and loads at the meter include no losses. As a result, the avoided costs will be higher measured as $ per kW at the meter and lowest as $ per kW measured at transmission. Since energy efficiency program load reductions are generally estimated at the end use, the cost-benefit analysis must reflect avoided costs at the end use (or the customer meter, as a proxy for the end use). If the avoided cost is computed per kilowatt of load data at the transmission level, rather than using end-use load, losses from the meter to transmission must be added back to get the avoided cost in $/kW of load at the meter.[^342]

[^340]: Line losses should be computed on a marginal basis, where possible.

[^341]: Regardless of where load is measured, it should include only the contribution from the voltage levels driving the need for that type of equipment (i.e., all distribution load for substations and feeders, secondary load for transformers).

[^342]: Similarly, if the load growth is estimated at a distribution voltage, the avoided cost must be increased by the losses from the meter to that voltage.

[PDF p. 298 | printed p. 280]

Investments in T&D infrastructure to support load growth generally do not increase the capacity of the relevant portions of T&D system by only the exact amount of projected load growth. Instead, it is typical to use standard equipment (which may be larger than strictly necessary) or to design in an allowance for future growth over the multi-decade useful life of a piece of infrastructure. For example, the aggregate capacity of all of a utility's distribution infrastructure often far exceeds the sum of substation peak loads. When matching the load growth to the investment, it is therefore necessary to determine whether the relevant capacity is the increase in peak load, or the increase in capacity of the relevant portion of the T&D system.

The only choice that is consistent with an avoided cost formulation for demand-side measures is to use the actual growth in peak load, rather than the capacity of the new hardware. This is because the load avoided by a demand-side measure is the actual peak load. If the avoided T&D value were calculated by dividing the infrastructure cost by its additional peak capacity (that is, if the value were in units of $ per kW<sub>hardware</sub>) then when multiplying this value by the peak reduction produced by an energy efficiency program (kW<sub>end-use</sub>) the calculation would understate the value of efficiency by a ratio of kW<sub>hardware</sub> per kW<sub>end-use</sub>. In addition, the extent of overcapacity built into hardware once the decision is made to construct is entirely independent of the incremental peak capacity that caused the decision.

For example, take a load-growth-related investment with an annual carrying cost of $100,000 that is caused by an increase in load of 100 kW, but increases the capacity of the relevant portion of the grid by 1 MW. If the avoided cost value were based on the hardware installed, it would be $100 per kW<sub>hardware</sub>-year, while if it is based on the load, it would be $1,000 per kW<sub>end-use</sub>-year. If load were actually reduced by 100 kW through a demand-side intervention, these two avoided cost calculations would imply different values of the avoided cost: $100,000 per year in the end-use case and only $10,000 per year in the hardware case. Since we know that the $100,000 per year investment would have been avoided by the 100 kW load reduction, only the load-derived calculation can be correct.

While in theory a generic ratio of kW<sub>end-use</sub> to kW<sub>hardware</sub> could be used to adjust for this effect, when combining many such decisions across time and across a service territory, consistency and coherence in the meaning and scale of kW<sub>hardware</sub> would almost certainly be lost. Therefore, the calculation of avoided T&D costs should use the actual kW of load, rather than the kW of new hardware capacity.

### Dealing with absence of system load growth

As noted previously, some utilities have experienced little or no overall growth in total load for some years and may forecast little growth in peak loads for some years. Nonetheless, utilities can have load-related investments to address parts of their service territories that are experiencing load growth. Dividing the load-related investments by zero, a negative number, or even a small positive load growth will produce meaningless results. In those situations, a utility may either use historical data from a period with load growth or compute the avoided cost per kilowatt growth for the fraction of the system

[PDF p. 299 | printed p. 281]

that has experienced growth.[^343] Counterfactual 1 assumes a world with no new energy efficiency, no active demand management, and no building electrification programs, in which the avoided costs computed for the areas with growth would be applicable to the entire utility.

### Carrying cost

The annualization of the capital costs should reflect the utility's cost of capital, income taxes, property taxes, and insurance. The useful life used in determining the carrying charge should match the expected life of the equipment. If a transmission plant has a longer operating life than a distribution plant, the analysis should use a lower carrying charge for transmission than distribution. This is one reason that avoided transmission and distribution are usually computed separately.

The carrying charge should be computed in $/kW-year levelized in real terms. The real-levelized carrying charge is the first-year charge that, if escalated at the inflation rate, will have the same present value as the revenue requirements for the project or the nominally levelized charge. The real-levelized carrying charge in each year represents the present value benefit of a one-year delay in adding the investment, and hence a one-year reduction in load growth.

Annual revenue requirements, real-levelized costs, and nominally levelized costs have the same present value, but the revenue requirements are front-loaded. Nominally levelized costs are flat in nominal terms and real-levelized costs are flat in real terms, rising with inflation.

### Operation and maintenance

Most T&D plant additions (a new transmission line, substation, feeder, or line transformer) also incur additional O&M costs, such as for vegetation control, inspections, repairs, repainting of towers and structures, and the like. Some expenditures, such as reconductoring a feeder or replacing poles for a voltage upgrade, may not increase (and may actually decrease) O&M costs.

The best practice for extrapolating O&M from historical data would generally be to determine the unit O&M cost ($/MVA of substation operation and maintenance, $/mile of feeder) and apply that value to the avoided cost. That process is straightforward for additional substations and transmission lines, which have their own accounts in the FERC Form 1. But it would be more difficult for other distribution facilities for which O&M expenses are less clearly delineated. It is generally reasonable to assume that the ratio of O&M cost to gross plant for the avoidable capacity is the same as for the existing plant mix, although ideally the historical investments would be restated to include inflation.[^344] Any assumption that O&M associated with new equipment is less than the average O&M for similar existing equipment should be carefully considered and fully justified.

[^343]: We are unaware of any utilities that have estimated what capital expenditures would have been without historical DSM effects or what capital expenditures would be in the absence of future DSM effects.

[^344]: "Gross plant" is defined as the total capital assets dedicated to utility service and is used to determine rate base.

[PDF p. 300 | printed p. 282]

In addition to avoiding new facilities and their O&M, lower loads will also tend to reduce the rate of failures of existing equipment and thus the capital and O&M costs involved in repairing and replacing the damaged equipment.

### Overheads

Utilities generally allocate a range of overhead or administrative costs (e.g., senior management, legal, financial, human resources, purchasing and contracting, information technology, warehousing, office expense, vehicles) on labor or a similar broad measure of O&M and construction costs. Some of those overheads may not vary linearly with the number of personnel required to design, build, maintain and operate the assets, but increased construction will generally require more of the overheads as a whole.

The utility's overhead adders should be included in both the load-related investments and the associated O&M. Any exclusion of overhead costs from avoided T&D investment should be carefully considered and fully justified.

## 10.2. Avoided pool transmission facilities cost

All load in New England pays for PTFs. These costs are in addition to those that individual utilities pay to local facilities in the local networks. We rely on ISO New England research and analysis to estimate these avoided PTF costs.

In November 2023, ISO New England published its _2050 Transmission Study_, a first-of-its-kind long-term study that estimates transmission system investments needed by 2050 to ensure a reliable and smooth clean energy transition.[^345] The study incorporates New England's likely future resource mix and increasing demand associated with building and transportation electrification. The study outlines a range of investment costs for expected future peak loads in 2035, 2040, and 2050.[^346]

The study estimates total investment costs to provide reliable transmission in 2050 will range from $16 billion to $17 billion (in 2024 dollars) and assumes that roughly 80 to 85 percent of buildings are electrified, energy efficiency programs are in place, and 100 percent of transportation is electric by the middle of the century.[^347] These costs estimates are primarily load-related costs; the study did not include interconnection upgrade costs as well as the cost of upgrades related to voltage performance, transient stability performance, and short-circuit performance.

[^345]: ISO New England Inc. November 21, 2023. DRAFT 2050 Transmission Study. Available at: [https://www.iso-ne.com/system-planning/transmission-planning/longer-term-transmission-studies](https://www.iso-ne.com/system-planning/transmission-planning/longer-term-transmission-studies).

[^346]: ISO New England's _2050 Transmission Study_ serves as a roadmap to identify transmission needs beyond the current 10-year planning horizon and is designed to show generally how future transmission-related objectives can be accomplished over the next few decades. The Study is not intended as comprehensive or detailed plans for construction. Nonetheless, it estimates a range of likely future costs associated with upgrading the transmission system.

[^347]: ISO New England's _2050 Transmission Study_ also estimates transmission costs future [sic] a 2050 peak with 100 percent building and transportation electrification. For this scenario, costs range from $24 to $27 billion dollars (in 2024 dollars).

[PDF p. 301 | printed p. 283]

The _2050 Transmission Study_ predicts the transmission system will transition to a winter peaking system around 2035, with a 2020 annual peak of 51 GW (this is similar to the peak loads observed in the counterfactuals modeled in AESC 2024 that are inclusive of building electrification measures, such as Counterfactual #5). Based on the highest load observed on the New England system to date, seen in the summer of 2006, the region is expected to see total peak load growth of 23 GW by 2050. Dividing the load-related costs by the load growth driving these investments results in an expected range of $711 per kW to $756 per kW by 2050. Taking a mid-range value, this results in investment costs of $734 per kW.

We convert this investment value to an annual avoided cost value that incorporates depreciation of costs overtime and utility revenue requirements charged to ratepayers. To do this, we use a "carrying charge rate," a percentage we multiply by total costs to estimate the annual revenue requirement of an investment. For AESC 2024, we determine an average carrying charge rate of 9.4 percent. We assume a 50/50 debt-to-equity financing ratio, debt and equity rates of 4.5 percent and 10 percent, respectively, effective state and federal tax rate of 27 percent, and a 45-year transmission line life (consistent with previous AESC studies). We average the O&M expenses, property taxes, and insurance expenses across the three carrying charge calculations from Eversource and National Grid (provided in the 2018 T&D survey): property taxes total roughly 2 percent, insurance expenses represent less than 1 percent, and O&M expenses are roughly 1 percent. We multiply the average carrying charge rate by the value of investment ($/kW) to get a dollar per kW-year avoided cost value. The annualized avoided cost is thus $734 per kW times 9.4 percent, or $69 per kW-year (2024 dollars).

### Using avoided PTF values

#### Avoided and deferred PTF costs

An "avoided cost" of $69 per kW-year also represents the present value benefit of a one-year delay in making the PTF investment, or in other words, the cost of deferring the PTF investment by one year as a result of a one-year reduction in peak load. This is due to the treatment of the carrying charge rate within the calculation of the avoided PTF value. The real-levelized carrying charge is the first-year charge that, if escalated at the inflation rate, will have the same present value as the revenue requirements for the total costs expected to be incurred due to load growth.

#### Annual system peaks

Regional transmission needs related to load growth have typically been driven by summer peak loads. In its long-term transmission planning study, the ISO New England predicts that with electrification, the region's transmission system will shift to a winter peaking system by 2035. Similarly, all of AESC's counterfactuals scenarios have some level of electrification (all incorporate transportation electrification while many incorporate both building and transportation electrification). All counterfactuals have winter peaks that approach, or even exceed, the summer peaks in the mid-2030s or early 2040s. Regardless of whether the system peaks in the winter or the summer, the transmission system is built to reliably meet the total system peak, each year. Therefore, when evaluating measures, program administrators should apply this regional PTF value to a measure's impact on the regional annual system peak, regardless of

[PDF p. 302 | printed p. 284]

when the peak occurs. Reducing annual peak load through DERs will avoid or defer future upgrades to the transmission system, which is built to meet that annual peak.

#### Counterfactual scenarios

In its long-term transmission planning study, the ISO New England estimates transmission system needs in a future with high levels of electrification, energy efficiency, and significantly more renewable energy on the electric grid. It also estimates costs in a future with 100 percent building and transportation electrification by 2050. It does not, however, estimate future transmission investments for a future with no building electrification and no energy efficiency programs, such as AESC Counterfactual 1. ISO New England's _2050 Transmission Study_ is the only ISO-led study to date that attempts to holistically estimate long-term transmission requirements in New England. Furthermore, it includes transportation electrification, an element that is maintained across all AESC counterfactuals. It also assumes a winter peaking system within the next decade; all AESC counterfactuals have winter peaks that approach (or exceed) the summer peaks in the 2030s or 2040s. Without access to studies or information on potential transmission costs for a New England future without any additional DER measures, the ISO study serves as the best available source of data for this avoided cost category. As such, the avoided PTF value of $69 per kW-year should be applied to annual peak reductions in all counterfactual scenarios.

### Comparison of avoided PTF across years

Table 129 shows a comparison of each AESC avoided PTF value.

**Table 129. Comparison of avoided PTF costs**

| Study     | Avoided Costs (2024 $/kW-year) | Method                                                      |
| --------- | ------------------------------ | ----------------------------------------------------------- |
| AESC 2018 | $112                           | Historical data                                             |
| AESC 2021 | $95                            | Historical data (scaled to forward-looking PTF investments) |
| AESC 2024 | $69                            | Long-term forward-looking data                              |

AESC 2018 calculated avoided PTF costs on a historical basis, using then-current Transmission Cost Allocation (TCA) data to identify load-related investments in substations, new lines, voltage upgrades, and additional capacitors and transformers for projects for 2003 through 2024, and load projections for that period. AESC 2018 estimated avoided PTF cost as $94 per kW-year in 2018 dollars (equal to $112 per kW-year in 2024 dollars).

After the completion of AESC 2018, several stakeholders raised concerns that the analysis was backward-looking rather than prospective, so we updated AESC 2021 estimates to be forward-looking. We reviewed projects in the October 2020 Draft RSP Project List, which included projects planned through 2026. However, at that time, ISO New England peak loads were declining, due in part to the energy efficiency programs. Additionally, the RSP Project List lacked data on the amount of past and projected load growth driving these transmission expansion plans (despite loads in some areas growing that were driving the load-related RSP projects). As a result, in AESC 2021, we estimated avoided PTF costs using the historical-looking AESC 2018 avoided cost estimate, scaling it by the share of forward PTF

[PDF p. 303 | printed p. 285]

investments relative the [sic] historical PTF investments used in the AESC 2018 calculations. Specifically, RSP forward-looking costs were 85 percent of the historical TCA costs on an annualized basis, so we scaled the AESC 2018 avoided PTF costs by 85 percent to provide the estimate of $84 per kW-year ($94/kW year in 2024 dollars).

The AESC 2024 calculation is entirely forward-looking and based on the recent ISO New England study on long-term transmission needs for a reliable and smooth energy transition.

### Avoided PTF transmission costs and their relationship to Regional and Local Network Service

The avoided PTF costs derived in this section reflect avoidable future costs. As PTFs are built, the costs of those facilities are recovered through ISO New England's Regional Network Service (RNS) charge. RNS is recovered across the whole region, dictated by a formula that includes aggregate PTF revenue requirements and the monthly peak loads in each load zone. Local network service (LNS) charges are used to recover the cost of local transmission assets (rather than PTFs).

The avoided PTF costs presented in this section do not include any impact of changes in the cost or cost allocation of already-built regional transmission facilities. The cost of these facilities is unavoidable, from a regional perspective, because transmission owners need to recover the cost of their past investments. Reducing peak load on the bulk system has two effects: (1) it reduces the need to build more transmission, or defers future PTF investments, thus keeping future RNS costs lower; and (2) it shifts some of the existing RNS costs to others in the region who have not reduced their peaks by the same proportion. LNS costs for existing non-PTF transmission cannot be shifted to ratepayers in other areas, so only the first effect would exist for local avoided transmission value.

How one treats these two effects depends on one's cost-effectiveness test:

- When using a cost-effectiveness test that takes a regional perspective to transmission costs, the entirety of the avoided PTF cost would be included. No savings are possible for sunk transmission costs reflected in today's RNS rates. (That is, the second effect of reducing peak load identified above would cause a transfer within the region, rather than an avoided cost.)
- When using a cost-effectiveness test that takes a state-level perspective, only a portion of the avoided PTF cost would accrue to the benefit of the ratepayers within the state implementing the programs. As a result, the avoided PTF cost would be scaled down based on the state's share of RNS costs. At the same time, there would be some additional value to that state's ratepayers from shifting embedded RNS costs to ratepayers in other states, relative to the counterfactual in which other states operate programs but the state in question does not. Furthermore, load reductions at the annual peak reduce PTF investments, while the cost allocation of RNS depends on monthly peak loads. In theory, a state could reduce shoulder-season monthly peaks more so than other states but makes no impact on the annual peak driving the PTF spending. Since RNS is based on contributions to monthly peaks, this state's share of RNS costs could decrease relative to other states, despite doing little to reduce PTF investments. AESC 2024 does not model the state-level counterfactuals that would be required to quantify

[PDF p. 304 | printed p. 286]

a state-level avoided RNS value, nor does it quantify the monthly zonal peak values used in the RNS tariff.

### Low load considerations

Localized loads significantly below system averages can result in various issues for the transmission system, including disturbances to voltage levels due to back feed from the distribution system. Historically, load growth has driven a large amount of pooled transmission projects in New England. However, in recent years, increasing amounts of distributed generation and other DERs have resulted in low loads on the transmission system at certain times of the year. ISO New England is now beginning to develop projects that address these low load conditions, which account for 3 percent, or $7.9 million (in 2024 dollars), of its planned and proposed PTF projects.[^348] These types of investments may grow as more DERs are added to the system in the short to medium term. At the same time, their effect may be muted or eventually avoided altogether as New England adds load due to electrification.

AESC's avoided PTF cost is the value of avoiding or deferring projects associated with load growth. It represents the benefit of peak period load reductions from energy efficiency or other DERs. Conversely, low-load-related transmission projects are costs to the system that result from load reductions in certain areas or at certain times of the year. Since ISO New England does not currently publish forecasted load minimums, and there is limited information available on how low load will affect transmission costs in New England, we could not estimate a low-load PTF cost for AESC 2024. In future years, when more information on low-load projects is available, we can more explicitly incorporate low-load-related costs into AESC, which could inform a cost adder to apply to projects that reduce load at times not beneficial to the transmission grid.

## 10.3. Survey of utility avoided costs for non-PTF transmission and distribution

AESC 2021 included a new rubric to evaluate and compare the methodologies for non-PTF avoided T&D used by utilities in the Study Group. AESC 2018 included a discussion of methods used by several utilities (National Grid, United Illuminating, and Eversource Connecticut). The AESC 2024 Study Group members agreed that the information collected and evaluated in AESC 2018 and 2021 had not changed enough to warrant a new survey or evaluation of utility's non-PTF avoided cost approaches.

The non-PTF avoided T&D rubric is based on the parameters and areas detailed in Section 10.1 above. The key areas of evaluation rubric include:

1. Load (whether past, forecast, or a combination);

[^348]: This includes all in-service, under construction, planned, and proposed projects from 2021-2024. Regional system Plan and Related Analyses, ISO New England and Final RSP Project List – June 2023. Available at [https://www.iso-ne.com/system-planning/system-plans-studies/rsp](https://www.iso-ne.com/system-planning/system-plans-studies/rsp).

[PDF p. 305 | printed p. 287]

2. Identifying which expenditures are avoidable or deferable by changes in load (e.g., are "load-growth-related");
3. Matching the changes in load to the load-growth-related investments (e.g., in time);
4. Mapping lumpy investments to an annual value; and
5. Inclusion of other costs associated with T&D investments, such as O&M and overhead.

### Evaluation of current utility methods

The following section describes our review of data provided by participating utilities that informs the T&D avoided cost quantification approach. Below, we present summary tables of the evaluation rubric, applied to each utility that responded to the request for information about their current avoided T&D cost calculation methodologies. Table 130 summarizes the avoided T&D values currently in use. Table 131 provides a summary of the load forecast methodologies used in developing these avoided T&D cost values. Table 132 provides more detailed methodological considerations used in deriving the avoided cost values.

[PDF p. 306 | printed p. 288]

**Table 130. Summary of utility avoided T&D cost methodologies**[^349]

_Extractor note (not source text): the source prints one column per utility-state combination under the group headings Eversource (CT, MA, NH), National Grid (MA, RI), UI (CT), Vermont (VT), Maine (ME) and Unitil (MA); they are shown here as nine value columns, each headed "utility state"._

| Criterion                                                                                              | Eversource CT                                  | Eversource MA    | Eversource NH        | National Grid MA   | National Grid RI  | UI CT                | Vermont VT                                                   | Maine ME                                  | Unitil MA         |
| ------------------------------------------------------------------------------------------------------ | ---------------------------------------------- | ---------------- | -------------------- | ------------------ | ----------------- | -------------------- | ------------------------------------------------------------ | ----------------------------------------- | ----------------- |
| In evaluating or screening DSM, does utility have a method for valuation of avoided distribution costs | Yes                                            | Yes              | Yes                  | Yes                | Yes               | Yes                  | Yes                                                          | Yes                                       | Yes               |
| The existing value of avoided distribution costs used by utility in evaluating and screening DSM       | $14.05/kW (2018$)                              | $198/kW (2018$)  | $79.98/kW (2018$)    | $102.48/kW (2019$) | $80.24/kW (2019$) | $30.29/kW (2017$)    | $0/kW-Yr                                                     | Mid Value: $246.79 (nominal)              | $222.56 (2018$)   |
| The year in which avoided distribution cost was developed                                              | 2018                                           | 2018             | 2017                 | 2019               | 2019              | 2017                 | 2018                                                         | 2020                                      | No data available |
| Frequency at which avoided distribution cost is updated by utility                                     | No regular frequency                           | Every 3 years    | No regular frequency | Every 3 years      | With AESC Update  | No regular frequency | No regular frequency                                         | No regular frequency                      | No data available |
| In evaluating or screening DSM, does utility have a method for valuation of avoided transmission costs | Yes (PTF and Non-PTF)                          | Yes (PTF only)   | Yes (PTF only)       | Yes (PTF only)     | Yes (PTF only)    | Yes                  | Yes (PTF only)                                               | Yes                                       | Yes               |
| The existing value of avoided transmission costs currently used in evaluating and screening DSM        | Applies $1.03 $/kW-Yr in addition to $94/kW-yr | $94/kW-yr        | $94/kW-yr            | $94/kW-yr          | $94/kW-yr         | $0.84/kW-yr          | $94/kW-yr (Efficiency VT); $45/kW-yr (BED)                   | Mid Value: $56.88/kW-yr + PTF ($94/kW-yr) | $94/kW-yr         |
| The year in which avoided transmission costs were developed                                            | 2018                                           | 2018             | 2018                 | 2018               | 2018              | 2017                 | 2018 (Efficiency VT); 2012 (BED)                             | 2020                                      | 2018              |
| Frequency at which avoided transmission costs are updated                                              | No Regular Frequency                           | With AESC Update | With AESC Update     | With AESC update   | With AESC update  | No Regular Frequency | With AESC update (Efficiency VT); No Regular Frequency (BED) | PTF portion with AESC update              | With AESC Update  |

_Notes: Methodology for Maine represents EMT's proposed approach. For details on Unitil's approach, see D.P.U. 18-110 – D.P.U. 18-119 Three-Year Plan 2019-2021, October 31, 2018 Exhibit 1, Appendix C - Electric Page 36 of 43 <https://ma-eeac.org/wp-content/uploads/Exh.-1-Final-Plan-10-31-18-With-Appendices-no-bulk.pdf>._

[^349]: In 2022 after the completion of this survey, PPL Corporation acquired National Grid's Rhode Island service, which is now Rhode Island Energy.

[PDF p. 307 | printed p. 289]

**Table 131. Avoided T&D load forecast methodologies**[^350]

_Extractor note (not source text): column groups as in the source are Eversource (CT, MA, NH), National Grid (MA, RI), UI (CT), Vermont (VT) and Maine (ME). In the source, Maine's "Based on data available from CMP" is a single merged cell spanning the three "Operational" rows, and another single merged cell spanning the "Projected PV" and "Projected DR" rows (the Maine cell on the "Projected EE" row is blank); the text is repeated here in each row it spans. The source also prints the group labels "Inclusion of the following in load forecasts:" as shaded rows with no values._

| Criterion                                                                                | Eversource CT                      | Eversource MA                      | Eversource NH                      | National Grid MA                   | National Grid RI                   | UI CT              | Vermont VT                   | Maine ME                         |
| ---------------------------------------------------------------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ---------------------------------- | ------------------ | ---------------------------- | -------------------------------- |
| Load forecast granularity used in calculating avoided costs at a utility-wide level      | Transmission and Substation        | Transmission and Substation        | Transmission and Substation        | Transmission and Supply area level | Transmission and Supply area level | Transmission Level | Transmission (Based on AESC) | Based on data available from CMP |
| Inclusion of the following in load forecasts:                                            |                                    |                                    |                                    |                                    |                                    |                    |                              |                                  |
| Operational EE                                                                           | Yes                                | Yes                                | Yes                                | Yes                                | Yes                                | Yes                | Yes                          | Based on data available from CMP |
| Operational PV                                                                           | Yes                                | Yes                                | Yes                                | Yes                                | Yes                                | Yes                | Yes                          | Based on data available from CMP |
| Operational DR                                                                           | Yes                                | Yes                                | Yes                                | Yes                                | Yes                                | No                 | No                           | Based on data available from CMP |
| Inclusion of the following in load forecasts:                                            |                                    |                                    |                                    |                                    |                                    |                    |                              |                                  |
| Projected EE                                                                             | Yes                                | Yes                                | Yes                                | No                                 | No                                 | Yes                | Yes                          |                                  |
| Projected PV                                                                             | No                                 | No                                 | No                                 | Yes                                | Yes                                | Yes                | Yes                          | Based on data available from CMP |
| Projected DR                                                                             | Eversource-sponsored programs only | Eversource-sponsored programs only | Eversource-sponsored programs only | Yes                                | Yes                                | No                 | No                           | Based on data available from CMP |
| Inclusion of any electrification goals or mandates reflected in current policy           | No                                 | No                                 | No                                 | Yes                                | Yes                                | No                 | Yes                          | Based on data available from CMP |
| Existence of a process for identifying expenditures _avoidable_ through load reductions  | Yes                                | Yes                                | Yes                                | Yes                                | Yes                                | Yes                | No                           | Based on data available from CMP |
| Existence of a process for identifying expenditures _deferrable_ through load reductions | Yes                                | Yes                                | Yes                                | Yes                                | Yes                                | Yes                | No                           | Based on data available from CMP |

_Notes: In Massachusetts and Rhode Island, National Grid excludes projected energy efficiency beyond the current plan in its forecast for determining the value of avoided distribution costs for DSM. It does account for continued lifetime savings from the current and prior plan years with a decay rate over time. As of 2022, Rhode Island's National Grid's service territory is now served by Rhode Island Energy._

[^350]: In 2022 after the completion of this survey, PPL Corporation acquired National Grid's Rhode Island service, which is now Rhode Island Energy.

[PDF p. 308 | printed p. 290]

**Table 132. Detailed considerations for calculation of load-specific avoided T&D costs**[^351]

_Extractor note (not source text): column groups as in the source are Eversource (CT, MA, NH), National Grid (MA, RI), UI (CT), Vermont (VT) and Maine (ME)._

| Criterion                                                                                                                 | Eversource CT | Eversource MA | Eversource NH | National Grid MA | National Grid RI | UI CT       | Vermont VT                   | Maine ME                                                      |
| ------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------- | ------------- | ---------------- | ---------------- | ----------- | ---------------------------- | ------------------------------------------------------------- |
| Existence of a process for deciding years of expenditure that factor into avoided T&D costs                               | Yes           | Yes           | Yes           | Yes              | Yes              | Yes         | N/A - using AESC avoided PTF | Based on data available from CMP                              |
| Use of the following when calculating avoided T&D costs (past values/future values/combination of past and future)        | Combination   | Combination   | Combination   | Combination      | Combination      | Combination | N/A - using AESC avoided PTF | Based on data available from CMP                              |
| Existence of a process for matching load levels to load-growth-related investments                                        | No            | No            | No            | No               | No               | No          | N/A - using AESC avoided PTF | Range of values presented matching load levels to investments |
| Whether utility applies a carrying cost to these investments to annualize investment values when calculating avoided cost | Yes           | Yes           | Yes           | Yes              | Yes              | Yes         | N/A - using AESC avoided PTF | Yes                                                           |
| Whether utility applies avoided O&M costs associated with investments when calculating avoided cost                       | Yes           | Yes           | Yes           | Yes              | Yes              | Yes         | N/A - using AESC avoided PTF | Yes                                                           |
| Whether utility applies an avoided overhead cost associated with investments when calculating avoided cost                | Yes           | Yes           | Yes           | Yes              | Yes              | Yes         | N/A - using AESC avoided PTF | Yes                                                           |

[^351]: In 2022 after the completion of this survey, PPL Corporation acquired National Grid's Rhode Island service, which is now Rhode Island Energy.

[PDF p. 309 | printed p. 291]

The following sections present short descriptions of the methods used by each responding utility.

#### National Grid (Massachusetts and Rhode Island)

National Grid calculates its avoided distribution capacity values for both its Massachusetts and Rhode Island DSM programs using a workbook developed in 2005 by ICF International, Inc., updated with recommendations from the 2018 AESC Study.[^352] The company updates this workbook for each three-year planning cycle. The workbook calculates an annualized value of statewide avoided distribution capacity values from company-specific inputs that include historical and projected capital expenditures and peak loads, carrying charges, FERC Form 1 accounting data, and O&M costs.[^353] National Grid uses a combination of historical and forecasted values within the workbook and accounts for operational energy efficiency, PV, and demand response programs. The load forecast used to determine the value of avoided distribution only includes projected PV and continued lifetime energy efficiency savings from prior plans and the current plan. The analysis does not include forecasted savings from future energy efficiency plans.

National Grid determines the percentage of the total distribution investments that are load-growth-related but not associated with new business. The resulting percentage is then applied to the distribution investment forecast. For avoided transmission costs, National Grid uses the 2018 AESC PTF of $94 per kW-year (in 2018 dollars) in both Massachusetts and Rhode Island. It does not account for non-PTF transmission costs.[^354]

Table 133 summarizes the distribution methodology employed by National Grid, as well as recommendations for improvement.

[^352]: In 2022, after the completion of this survey, National Grid's Rhode Island service was acquired by PPL Corporation, and is now Rhode Island Energy.

[^353]: The Narragansett Electric Company d/b/a National Grid. Docket No. 5076 - 2021 Annual Plan. Attachment 4.

[^354]: The analysis in this section is based on National Grid MA and RI - 2018 Avoided T&D Workbooks, [text truncated at page break in source]

[PDF p. 310 | printed p. 292]

**Table 133. Assessment of National Grid's avoided distribution methodology and recommendations for improvement**

_Extractor note (not source text): in the source, a "-" in a cell marks no entry; multi-paragraph cells are separated here by `<br><br>`._

| Topic                                    | Overall Assessment                                                                                                                                                                                                                                                                                                                                                                                              | Recommendations on Improvement                                                                                                                                                                                                                                                                                                                                                                       | Recommendations on Clarity                                                                                                                                                                                                          |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Overall T&D Methodologies**            | The methodology is mostly consistent with recommended methodologies in its consideration of load-growth-related T&D investments.                                                                                                                                                                                                                                                                                | National Grid should account for non-PTF transmission costs.                                                                                                                                                                                                                                                                                                                                         | -                                                                                                                                                                                                                                   |
| **Categories of investments considered** | National Grid uses historical and forecasted T&D investments and assumes a percentage of that investment is related to load growth not associated with new business and is therefore avoidable with DSM.                                                                                                                                                                                                        | It is not clear how the percentage of avoidable distribution investments were calculated since they are significantly lower than the overall distribution investments. It is unclear whether this estimate of the avoidable investments reflects all load-growth-related projects, including any capacity-related projects undertaken for non-load growth purposes such as reliability improvements. | National Grid should provide more transparency regarding the calculation of percentages representing load growth and new business.<br><br>National Grid should use a more granular approach in the breakout of its T&D investments. |
| **Load Forecast Methodologies**          | National Grid includes the impact of historical adoption of energy efficiency measures but does not include the impact of forecasted energy efficiency adoption.                                                                                                                                                                                                                                                | National Grid should use a load forecast that includes future projected energy efficiency savings since the investment forecast assumes continued energy efficiency programs.                                                                                                                                                                                                                        | -                                                                                                                                                                                                                                   |
| **Detailed Considerations**              | National Grid uses a relatively short period of 11 years (5 years of historical data and 6 years of forecasted data) which may not be long enough to account for lumpiness associated with investments across the years.<br><br>National Grid applies a carrying cost to investments when calculating avoided costs.<br><br>National Grid includes both O&M and overhead costs in calculation of avoided costs. | National Grid should use a longer-term period for its analysis, in the range of 25–27 years.                                                                                                                                                                                                                                                                                                         | -                                                                                                                                                                                                                                   |

#### United Illuminating

United Illuminating developed estimates of the avoided T&D expenditures due to Conservation and Load Management (CLM) based on values from a 2017 Harbourfront Group study.[^355] The 2017 Harbourfront study uses principles of marginal cost of service in order to develop a marginal cost of transmission based on coincident peak demand and a marginal cost of service based on non-coincident

[PDF p. 311 | printed p. 293]

peak demand. The study calculated values for both historical years (2000–2016) and future years (2017–2026). The analysis assumed that non-coincident peak impacts resulted in substation and feeder demand reduction from all CLM measures, therefore resulting in the maximum estimate. The study also assumed that the T&D costs that are avoided by the implementation of a CLM load-reduction measure are the same as the marginal cost of T&D for adding or subtracting an increment of load. For the distribution system, the process involves identifying the T&D projects by separating out those that are load-growth-related from those that are not growth-related. For the transmission system, only projects undertaken to meet regional and national transmission and reliability standards were considered. The categories for the projects considered include transmission substation, transmission lines, distribution substations, and distribution feeders. The denominator for the marginal cost calculations is the added capacity or the load-serving capability of the capital project. The methodology used an economic carrying charge model and includes O&M expenses and overheads.

Table 134 summarizes the distribution methodology employed by United Illuminating, as well as recommendations for improvement.

**Table 134. Assessment of UI's avoided distribution methodology and recommendations for improvement**

_Extractor note (not source text): Table 134 runs across PDF pp. 311-313; the header row repeats on each page in the source and a single cell may be split at a page break (the continuation is shown at the top of the next page's part). Multi-paragraph cells are separated here by `<br><br>`._

| Topic                         | Overall Assessment                                                                                                                                                                                                                                                                                                                                                                    | Recommendations for Improvement                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Recommendations on Clarity                                                                                                                                                                                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Overall T&D Methodologies** | The methodology is broadly consistent with avoided T&D methodologies in its consideration of load-growth-related T&D investments.<br><br>The methodology is inconsistent with avoided T&D methodologies in its consideration of load growth. The study is a marginal cost-of-service study more suited for application for purposes of cost allocation across different rate classes. | The study provides a marginal cost which uses a different methodology compared with the avoided T&D cost methodologies suggested in this AESC. In the marginal cost development, the total investments identified for load growth projects were divided by the load-serving capability in developing the marginal costs. However, for an avoided T&D study we recommend dividing instead by the growth in peak demand during the timeframe identified.<br><br>The avoided costs were developed in context of the CLM | UI used a weighting construct where 20% of its avoided T&D value is combined with 80% of Eversource avoided T&D value at the distribution level and transmission level. Further information would be beneficial regarding the accuracy and rationale of these assumptions. |

[^355]: United Illuminating, Avoided Transmission and Distribution Cost Study 2000–2006.

[PDF p. 312 | printed p. 294]

| Topic                                    | Overall Assessment                                                                                                                                                                                                                                                                                                                                     | Recommendations for Improvement                                                                                                                                                                                                                                                                                                                                                        | Recommendations on Clarity                                                                                                                                                             |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _(continued: Overall T&D Methodologies)_ |                                                                                                                                                                                                                                                                                                                                                        | program and its applicability to other programs should be evaluated and updated accordingly.                                                                                                                                                                                                                                                                                           |                                                                                                                                                                                        |
| **Categories of investments considered** | UI includes all growth- and capacity-related projects in calculation of avoided T&D costs. This includes capacity-related investments associated with projects undertaken for reliability improvements.<br><br>UI considers both transmission and distribution investments at the substation and also considers feeder-level distribution investments. | -                                                                                                                                                                                                                                                                                                                                                                                      | UI should clarify how it considers and includes investments that may be harder to characterize as solely load-growth projects but may also contribute to alleviating load constraints. |
| **Load Forecast Methodologies**          | In evaluating investments, UI includes the impact of historical adoption of CLM measures but does not include this in forecasted CLM adoption. This methodology is accurate in quantifying the infrastructure costs that would be required without CLM provided that the investments and capital expenditure estimates also reflect growth             | UI should include the impacts of electrification and state policy goals when identifying avoided T&D investments.<br><br>Although UI has developed a load forecast for identification of load-growth-related investments, for an avoided T&D study we recommend dividing these investments by the growth in peak demand during the timeframe identified as opposed to the load-serving | The load forecast methodology is not clear in terms of other energy efficiency measures included in the load forecast and the applicability of these values across other programs.     |

[PDF p. 313 | printed p. 295]

| Topic                                      | Overall Assessment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Recommendations for Improvement      | Recommendations on Clarity |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------- |
| _(continued: Load Forecast Methodologies)_ | without CLM included for consistency.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | capacity of the projects identified. |                            |
| **Detailed Considerations**                | Although there is no process for matching investments to load growth years, application of the relatively long period of 27 years (17 years of historical data and 10 years of forecasted data) accounts for some of the lumpiness associated with investments across the years.<br><br>The analysis includes projects that could potentially be avoided or delayed by the implementation of CLM measures.<br><br>UI has applied a carrying cost to investments when calculating avoided costs.<br><br>UI has included both O&M and overhead costs in calculation of avoided costs. | -                                    | -                          |

#### Eversource (Connecticut, Massachusetts, and/or New Hampshire)

Eversource developed avoided or deferred T&D estimates using broadly similar methodologies across the three states it serves (Connecticut, Massachusetts, and New Hampshire) with some key differences in calculation of the percentage of avoidable or deferrable investments that could be considered in calculating the avoided costs. Its analysis in all three states considered both historical and forecasted

[PDF p. 314 | printed p. 296]

investments on the T&D system.[^356] For Massachusetts and New Hampshire, the methodology involved developing a value using the incremental investments and the incremental peak load growth over the same timeframe. In each of these states, Eversource assumed a certain percentage of the total T&D investments, respectively, were load-growth-related.

In the case of Connecticut, Eversource used a different approach. The methodology involved developing an additional regression analysis between historical investments and new customers to find the unavoidable investments associated with customer growth. Eversource does not consider these historical T&D investments that are related to customer growth avoidable/deferrable and therefore removed them from the analysis. Eversource used results of the regressions to evaluate the percentage of the T&D investments in Connecticut that are avoidable/deferrable, instead of the application of a percentage for Massachusetts and New Hampshire. Following this, Eversource conducted a regression analysis between incremental investments and peak load growth to assess the incremental investments associated with peak load growth in $/MW. The results of the two steps were combined to develop an annualized avoided T&D cost.

Table 135 summarizes the distribution methodology employed by Eversource, as well as recommendations for improvement.

**Table 135. Assessment of Eversource's avoided distribution methodology and recommendations for improvement**

_Extractor note (not source text): Table 135 runs across PDF pp. 314-315; the header row repeats on each page in the source and a single cell may be split at a page break. Multi-paragraph cells are separated here by `<br><br>`._

| Topic                                    | Overall Assessment                                                                                                                                                                                                                                                                                                                                                                  | Recommendations on Improvement                                                                                                                                                                                                                                                                                                                                    | Recommendations on Clarity                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Overall T&D Methodologies**            | Eversource's methodology is broadly consistent with avoided T&D methodologies in its consideration of load-growth-related T&D investments and load growth.<br><br>In the case of NH, the recommendations outlined are based on review of the workbooks used in developing the 2012 values. Eversource indicated that the methodology in subsequent updates has remained consistent. | Eversource does not currently estimate avoided/deferred T&D values for MA and NH. Synapse recommends calculating these values and updating at a consistent frequency.                                                                                                                                                                                             | Certain assumptions outlined below have not been supported with underlying sources and calculations. These should be provided in future updates.<br><br>For CT, both United Illuminating and Eversource have indicated the use of a 20/80 weighted average based on the respective customer base. Calculations outlining the weighting process should be provided to ensure consistency between both entities. |
| **Categories of investments considered** | Eversource does address the inclusion of growth- and capacity-related projects in calculation of avoided T&D costs, although it is unclear if these have been accurately estimated.                                                                                                                                                                                                 | In the case of NH and MA methodologies, it is not clear how the percentage of avoidable/deferrable investments were calculated and whether they are fully capturing all the avoidable load-growth-related investments. In the case of CT, the non-avoidable or deferrable T&D investments were derived using a top-down approach based on the number of customers | To increase transparency and ensure consistency with AESC methodologies in calculation of avoidable/deferrable investments, Eversource should identify underlying sources that specify the methodology and calculations applied in identifying the historical and forecasted capital investments.                                                                                                              |

[^356]: The analysis in this section is based on Eversource MA–2018 Avoided T&D Workbooks, Eversource CT–2018 Avoided T&D Workbooks and Eversource NH–2012 Avoided T&D Workbooks.

[PDF p. 315 | printed p. 297]

| Topic                                               | Overall Assessment                                                                                                                                                                                                                                                                                                                                                                                                        | Recommendations on Improvement                                                                                                                                    | Recommendations on Clarity                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _(continued: Categories of investments considered)_ |                                                                                                                                                                                                                                                                                                                                                                                                                           | added to the system. Eversource should consider looking at specific projects on a case-by-case basis that could be avoided or deferrable through load reductions. | This should include sources that outline the following:<br><br>1. The categories of investments considered (e.g., substation/feeder) and the inclusion of investments in the analysis that are incurred to address local load growth.<br><br>2. The analysis conducted in classification of investments as avoidable or deferrable including any calculations made to derive the avoidable/deferrable percentage estimates for both MA and NH Avoided D [sic] estimates.                                                                                                                                                                                                                                                                  |
| **Load Forecast Assumptions**                       | As of 2018, Eversource had not included the impacts of electrification in its forecast of T&D capital expenditures for the purpose of calculating avoided/deferred T&D costs. However, Eversource has indicated that future load and capital expenditure forecasting will include the impact of electrification.                                                                                                          | -                                                                                                                                                                 | The CT regression methodology for statewide T&D uses a presumed rate of load growth based on historical growth using data from the CT Siting Council. However, it is not clear if the load growth assumed for identifying the capital investments (typically done through T&D planning process) used this same estimate of load growth. These should be consistent.<br><br>For MA and NH, due to limited data availability underlying the development of the load forecasts and capital expenditures, further details are required to ensure consistency with methodologies outlined in AESC. Eversource has indicated that the load forecasts used for T&D investment planning are consistent with those used for Avoided T&D estimates. |
| **Detailed Considerations**                         | Although there is no process for matching investments to load growth years, application of the relatively long period of data accounts for some of the lumpiness associated with investments across the years.<br><br>Eversource has applied a carrying cost to investments when calculating avoided/deferred costs.<br><br>Eversource has included both O&M and overhead costs in calculation of avoided/deferred costs. | -                                                                                                                                                                 | -                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

#### Unitil (Massachusetts and/or New Hampshire)

No specific information was provided.

[PDF p. 316 | printed p. 298]

#### Vermont

For statewide energy efficiency programs administered through Efficiency Vermont, the state uses the 2018 AESC PTF of $94/kW-year as a proxy for both the statewide average avoided cost of distribution and transmission combined. This is because within Vermont loads are expected to remain on a flat-to-declining trajectory for the foreseeable future and there have been no geographic locations where targeted energy efficiency could defer needed T&D investments since 2012. In addition, Vermont is facing generation constraints where substations are at thermal loading capacity, as described in more detail in the section below. This means that energy efficiency could create additional costs instead of avoided costs.

Similarly, the City of Burlington Electric Department (BED) does not assume any avoided distribution costs because the system is overbuilt. BED uses a value of $45 per kW for avoided transmission costs that was originally developed and approved in 2012.

Table 136 summarizes the distribution methodology employed in Vermont, as well as recommendations for improvement.

[PDF p. 317 | printed p. 299]

**Table 136. Assessment of Vermont's avoided distribution methodology and recommendations for improvement**

_Extractor note (not source text): multi-paragraph cells are separated here by `<br><br>`._

| Topic                                    | Overall Assessment                                                                                                                                                                                                                                                                                                                                                              | Recommendations for Improvement                                                                                                                                                                                                                                                 | Recommendations on Clarity                                                                                                                                                                                                                            |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Overall T&D Methodologies**            | Vermont uses only the PTF value for the combination of PTF and non-PTF transmission and distribution. The PTF methodology is consistent with the recommendations of this chapter, by default.<br><br>The Burlington value does not reflect the regionwide nature of avoided PTF.<br><br>Vermont does not derive any value for avoided non-PTF transmission or for distribution. | Vermont should apply the same avoided PTF transmission costs across the state.<br><br>Vermont should consider tracking winter distribution peaks to identify whether electrification could cause the need for distribution upgrades and whether CLM could mitigate those costs. | Vermont should explicitly analyze and document the use of a $0 value for avoided non-PTF transmission and distribution costs, taking into account in-state differences in loads, distributed generation, and the impact of potential electrification. |
| **Categories of Investments Considered** | Because Vermont does not have a state-specific methodology for avoided T&D costs, it does not consider which investments are load-growth-related or whether to conduct analysis at the substation or feeder level.                                                                                                                                                              | -                                                                                                                                                                                                                                                                               | -                                                                                                                                                                                                                                                     |
| **Load Forecast Methodologies**          | Vermont Electric Power Company Long Range Transmission Plan (LRTP) includes load forecasts that account for EE, PV, DR, and adjusts for the amount of efficiency embedded in the actual data along with the amount of efficiency expected to occur in the future.                                                                                                               | -                                                                                                                                                                                                                                                                               | -                                                                                                                                                                                                                                                     |
| **Detailed Considerations**              | None                                                                                                                                                                                                                                                                                                                                                                            | -                                                                                                                                                                                                                                                                               | -                                                                                                                                                                                                                                                     |

#### Maine

Efficiency Maine Trust (EMT) engaged Synapse as a subcontractor to ERS to develop statewide avoided T&D costs in dollars per kilowatt-year ($/kW-year). The methodology used in developing the values is consistent with methodology outlined in AESC. The analysis used data provided by Central Maine Power (CMP). Based on this limited data availability, Synapse has assumed that the avoided T&D cost for CMP will serve as a proxy for the statewide avoided T&D cost.[^357] The developed avoided T&D value is based on the overall long-term ratio of T&D savings per kW of avoided growth using peak load forecasts and planned capital additions based on CMP data.

[^357]: Synapse did not have access to Versant data. While Synapse assumes the value for Versant will be nonzero, Synapse has no further information at this time and thus cannot include it in the statewide estimate.

[PDF p. 318 | printed p. 300]

In calculating the distribution expenditures, CMP uses forecasted load at the level of the service center as part of Chapter 330 filings.[^358] Synapse used the 50/50 load forecast from these filings. CMP provided Synapse with data for load-growth-related distribution capital expenditures. Some of the distribution capital expenditures were classified as both transmission and distribution; and in those cases, a portion of such projects were allocated to transmission avoided cost calculations. In addition to transmission investments related to distribution projects, CMP also provided similar load-growth-related investments associated with the non-PTF transmission costs. In estimating the avoided non-PTF cost, Synapse assumed these needs to be driven by the ISO New England CELT forecast. Synapse also applied a real levelized carrying charge and an avoided O&M allowance based on data provided by CMP. Since Synapse had limited data regarding matching of the CMP's capital investment time periods with the load growth, Synapse presented a range of values based on different assumptions of time periods for both the capital investments and the load growth. EMT chose to use the mid-point value across this range.

## 10.4. Localized value of avoided T&D

In addition to crediting demand-side measures with value for avoiding T&D costs across a service territory, it may also be necessary to estimate the value of these measures in a location-specific context. One example includes the evaluation of an NWA (or hybrid solution) as an alternative to a proposed or potential traditional infrastructure-based solution to a projected reliability issue. To comprehensively estimate the value that DERs, namely energy efficiency and demand response, provide to localized T&D systems, program administrators can develop and rely on localized T&D values. This section describes the approach developed in AESC Supplemental Study Part II: _Localized Transmission and Distribution Benefits Methodology_ (Supplemental Study) to AESC 2018 at the request of a subset of the AESC 2018 Study Group. The AESC 2024 Study Group members agreed that the information presented here was up to date. The section surveys the landscape of location-specific avoided T&D methods and approaches in the region.[^359]

### Summary of supplemental study approach to localized T&D value

The key aspects of the Supplemental Study methodology are to:

1. Identify target areas and required load reduction
2. Determine benefits of targeted load reductions by identified target area
3. Calculate avoided cost ($/kW) based on the present value of deferred expenditures and the required load reduction

[^358]: Central Maine Power Company Annual Filing of Schedule of Transmission Line Rebuild or Relocation Projects, 35-A M.R.S.A. §3132(3); and Schedule of Minor Transmission Line Construction Projects, 35-A M.R.S.A. §3132 (3-A).

[^359]: Chang, M., J. Hall, D. Bhandari, P. Knight. May 1, 2020. _AESC Supplemental Study, Part II. Localized Transmission and Distribution Benefits Methodology._ Synapse Energy Economics for AESC Supplemental Study Group. Available at [https://www.synapse-energy.com/sites/default/files/AESC_Supplemental_Study_Part_II_Localized_TD.pdf](https://www.synapse-energy.com/sites/default/files/AESC_Supplemental_Study_Part_II_Localized_TD.pdf)

[PDF p. 319 | printed p. 301]

The following sections detail the three-step process for determining localized T&D values. We also describe current practices followed by participating utilities when evaluating NWAs. We recognize that the decision process for evaluating NWAs relative to traditional engineering solutions is a different process from quantifying the avoided T&D costs for DSM planning. These three steps will require program administrators to obtain information from their respective planning groups.

#### Step 1: Identify target areas and required load reduction

The localized T&D value requires the identification of target projects and required load reduction and duration in order to calculate the avoided cost. This first step of identifying target projects utilizes a utility's planning processes that identify system contingencies at peak load levels under normal and contingency operations.

##### Build on existing T&D planning

The first step in identifying target locations for evaluation is based on the results from utilities' existing peak load forecasts at the transmission, sub-transmission, and distribution levels. The peak load forecasts should only account for program-related NWA components such as energy efficiency, PV, and demand response that are currently online and active.[^360] The peak load forecasts should be conducted in accordance with the utility's T&D planning practices and regulatory requirements (typical forecasts of five to 10 years in the future for distribution planning and 10 years for transmission and sub-transmission planning). This process may involve developing resource-specific forecasts. Stakeholders may consider evaluating peak load forecasts to include any state/local/regional electrification goals mandated by current policy, if not required by statute.

**Local transmission and sub-transmission:** After estimating peak load levels, the next step is to establish the system planning criteria and performance objectives. The system planning criteria should be based on the utility's local transmission system planning guidelines and regulatory obligations. This would involve designing the system in accordance with any relevant standards and/or design practices. For example, in New England this may include planning criteria for the bulk electric system as defined by ISO New England, NERC standards, and Northeast Power Coordinating Council (NPCC). In addition, local standards may also apply (e.g., Maine's local "safe harbor" reliability standards). An example of system planning criteria would involve establishing the voltage operating ranges and loading criteria for system components under normal and contingency operation—such as normal, long-term emergency and short-term emergency limit ratings for each type of equipment, i.e., the loading at which the equipment can operate in normal and emergency situations.

As part of the planning process, the planning group will run power flow simulations to identify the system contingencies and violations under varying system configurations. This may include understanding and applying the specific contingency standards (e.g., loss of element contingency such as N-0, N-1, N-1-1) that define the minimum infrastructure necessary to maintain security standards

[^360]: The load forecast should be the same for evaluating NWAs and traditional engineering solutions.

[PDF p. 320 | printed p. 302]

depending on the needs of the specific region. At a transmission level, this is typically done through load flow analysis software such as Siemens' PSS/E.[^361] The analysis should also estimate the required load reduction in order to mitigate the contingency.

**Distribution system:** The distribution system planning process will follow a similar process to transmission planning. Distribution planning requires projecting the peak load. This should include summer and winter peak load forecasts at a substation and circuit level. The peak load forecast should be done over a timeline that is consistent with the utility's distribution planning process. Depending on the utility, this forecast is typically done over a 10-year period.

The next step involves setting up the design criteria for planning of the distributions [sic] system. This includes establishing criteria for equipment loading, phase balancing, and ranges of system voltages, etc. Following this, a circuit analysis is conducted to identify where planning criteria and design threshold violations exist and where the system constraints are expected to occur. This is typically done using distribution system planning tools, e.g., Eaton's CYME software to assess the critical load levels, thermal, and voltage violations.[^362] This step would also involve estimating the load reduction required to mitigate any identified contingencies.

Distribution system analysis should also include a process to identify potential areas where there may be reliability concerns that could be mitigated through NWA solutions.

##### Considerations

To prioritize areas for targeted NWAs, utilities currently consider various additional factors before assessing the potential for an NWA option. For example, utilities may establish minimum threshold criteria to meet when addressing a system contingency or considering an NWA as a resource option.

Utilities also currently consider the timeline required for building the NWA and whether this can be done in time to avoid the identified contingency or violation that it is meant to address based on local conditions. There are issues that may not be considered imminent or immediate concerns (e.g., issues that may have been accepted for many years) and should also be addressed accordingly. For example, contingencies that have sufficient lead time could be considered for NWA solutions whereas projects with imminent needs may not be suitable for NWAs.

In addition, the severity and nature of the overload (e.g., the contingency number) are considerations for the NWA process. The conditions under which the constraint or planning violation has been identified should be factored in the analysis. This might include examining the degree to which the constraint is present in normal conditions or extreme conditions (such as hot weather). Utilities also consider the nature of the contingencies in terms of whether they are suitable applications for an NWA.

[^361]: Siemens. Last accessed March 10, 2021. "PSS®E – High Performance Transmission Planning and Analysis Software." _new.siemens.com._ Available at [https://new.siemens.com/global/en/products/energy/energy-automation-and-smart-grid/pss-software/pss-e.html](https://new.siemens.com/global/en/products/energy/energy-automation-and-smart-grid/pss-software/pss-e.html).

[^362]: CYME. Last Accessed March 10, 2021. "CYME International" _Cyme.com._ Available at <http://www.cyme.com/>

[PDF p. 321 | printed p. 303]

In identifying target areas where there are concerns about backing up critical loads, these areas should not be automatically disqualified from NWA consideration—instead hybrid solutions between the NWA and a wires solution could also be considered and evaluated by the planning group.[^363]

##### DSM planning and implementation

On the energy efficiency side, there is need to factor in the lead time for marketing, implementation, and verification of DSM under an NWA solution. As noted in the responses provided by the utilities and stated above, current NWA evaluation processes require a window of time prior to the need to start construction on T&D infrastructure. In their DSM planning processes, program administrators should also factor the amount of DSM that could be based on potential annual load reduction (percent) by class and projected overload, as well as estimates of distributed generation and storage capacity. Conversely, a conventional engineering solution will also take time, especially if it requires separate regulatory approval and other siting review.

##### Identifying expenditures avoidable by load reductions

This section describes an approach to identifying expenditures that are avoidable by load reductions. It incorporates ideas from existing methodologies used by utilities to identify regions suitable for NWAs.[^364]

In identifying the expenditures avoidable by load reductions, first it is necessary to identify the magnitude, duration, and coincidence of the load reduction compared to the location and the timing of the traditional utility solution that would solve any system contingencies. Any constraints identified should be listed as such based on the first year that the constraint is identified. As discussed above, this should be identified through the system power flow analysis. At minimum, most utilities consider load growth and reliability as the expenditures that can be avoided by NWAs.[^365] However, other projects may also have some suitability in replacing a wires solution.

If a project addresses both NWA-eligible constraints and also non-NWA-eligible constraints, the costs for such projects should be broken down between those that are NWA-eligible and non-NWA-eligible in estimating the avoided cost expenditures. The utility should clearly identify which investments are considered as avoidable or deferrable through an NWA and the expenditures identified should be estimated in accordance with the utility capital investment planning guidelines. The expenditures should include operating expenses (e.g., reconfiguration) and capital investments and O&M associated with new facilities (net of any savings from retiring old equipment).

[^363]: As the availability and granularity of data improves through technologies and planning advancements, we anticipate improvements in methodology and applicability to more feeders.

[^364]: This methodology does not comment on the accessibility of detailed load, engineering, and cost data for feeders and components.

[^365]: While overall system load growth may be flat or declining for a given utility, there still may be individual feeders that are experiencing load growth.

[PDF p. 322 | printed p. 304]

Utilities may establish a traditional engineering solution cost threshold before considering NWA solutions. Small projects that can be solved through traditional utility options (low-cost load transfers, etc.) may be less costly than procuring an NWA solution. Similarly, longer-term projects that do not have an imminent need and are above an established cost threshold may be more suitable projects for NWA consideration.

##### Identify type and period of required reduction

After identifying the expenditures that are avoidable by targeted load reductions, it is critical to identify the time at which the required load reduction is needed. This involves answering questions such as:

- Does the load reduction need to occur in a specific season?
- Does the load reduction need to occur in specific hours of the day?
- Over how many hours or days must the load reduction occur?

In addition, it is important to identify the number of years in which the reduction must occur. For example, if the goal is to defer an expenditure for three years, and the load is expected to exceed the system's capability for all three of those years, then an effective load reduction plan requires the load reduction to sustain for three years. Program administrators will need to coordinate with the utility's distribution planning group to ensure that localized demand reduction programs will meet the planning criteria as an appropriate solution.

#### Step 2: Determine benefits of targeted load reductions by identified target area

When calculating the avoided T&D costs, AESC users should quantify the reduced present value of deferred expenditures. The annualized present value should reflect the utility's cost of capital, income taxes, property taxes, and insurance over the life of the equipment. To do so, one must first calculate the real carrying charge (RCC) expressed as a percentage. In general, the RCC equals the weighted average cost of capital (WACC), plus income tax, property tax, associated insurance, and O&M:[^366]

**Equation (RCC):**

$$RCC = WACC + \mathit{Income\ Tax} + \mathit{Property\ Tax} + \mathit{Insurance} + \mathit{O\&M}$$

The RCC should then be used to calculate the reduced present value of the avoided expenditures. For example, if the utility's RCC is 15 percent, then a $10 million investment would have an annualized expenditure of $1.5 million per year ($10 million x 15 percent).

There may be situations where a DSM load reduction defers a specific project by some period of time. For those situations and for the purposes of simplifying a more complex process, we recommend that the deferral value represents the traditional engineering expenditure reduced by the RCC and then

[^366]: See Section 10.1 for a more detailed discussion of real carrying charge. The associated insurance and O&M costs may be expressed as a percentage of the deferred expenditure being analyzed.

[PDF p. 323 | printed p. 305]

discounted by the real discount rate.[^367] In our illustrative example, if the RCC is 15 percent and the real discount rate is 3.37 percent, a 1-year deferral would have an avoided cost value of 85.5 percent (0.855 = 1 – [0.15 * (1 – 0.0337)]).

#### Step 3: Calculate avoided cost ($ per kW)

The next step is to calculate the avoided cost in terms of dollar per kilowatt (measured in $ per kW) for each identified target area.[^368] To do so, program administrators must first compile:

1. The present value of the benefits from the deferral or avoidance of load-related expenditures identified in Step 2, above; and
2. The required load reduction, in kilowatts, required to achieve the deferral or avoidance of said expenditures.

Next, program administrators should divide the present value of the benefits from deferral or avoidance by the required load reduction to arrive at a localized avoided T&D value in dollars per kilowatt, by target area.

This value can serve as the conceptual average value for which to evaluate load-reduction resources and technologies between the planning and energy efficiency groups. In other words, the average cost of the load-reduction strategies used to achieve deferral or avoidance should be less than the calculated localized avoided T&D value, which is the value of the traditional engineering solution. If the average cost per kilowatt is greater than the localized avoided T&D value, then the avoidance or deferral portfolio costs more than the load-related expenditures that are targeted for deferral or avoidance. In these cases, alternative portfolios should be evaluated. If none are found to be cost-effective relative to the traditional engineering solution, the traditional engineering solution should be pursued.

Conceptually, it may be helpful to use the localized avoided T&D values as guidelines when compiling a portfolio to achieve the required load reduction. To the extent possible, program administrators should concentrate on achieving the required load reduction at lower costs per kilowatt than the avoided costs. However, specific resources may be less than or even greater than the average avoided cost, as long as the total portfolio cost is less than the localized avoided cost T&D value.

### Evaluation of current utility methods

AESC 2021 included a rubric, developed in Section 10.3: _Survey of utility avoided costs for non-PTF transmission and distribution_ above, to survey current utility methods for quantifying the value of demand-side measures in avoiding or deferring geographically localized investments. The evaluation

[^367]: For the purposes of this methodology, we do not address any probabilistic planning issues that may arise from the continued deferral or acceleration of specific distribution project due to changes in localized loads. A more detailed analysis would require the re-running of power flow analyses based on changed loads that may result in the determination of a different engineering solution.

[^368]: This methodology does not address issues regarding operational control or visibility associated with the T&D system.

[PDF p. 324 | printed p. 306]

rubric for localized T&D methods is built on a similar structure to the Supplemental Study, but it is more flexible (and more focused on the raw data sources and approaches to analysis) to reflect different approaches to calculating these values and the relative lack of maturity of this aspect of avoided cost analysis.

The Synapse Team surveyed the utilities in the Study Group regarding their approaches to localized avoided T&D values. The following section describes our review of data and methods provided by participating utilities. The AESC 2024 Study Group members agreed that the information collected and evaluated in AESC 2018 and 2021 had not changed enough to warrant a new survey or evaluation of current utility methods.

Below, we present summary tables of the evaluation rubric, applied to each utility that responded to the request for information about its methodology about the current locational valuation/NWA methodologies. Table 137 provides a general summary of methodologies related to identification of candidate locations for NWAs and the related load forecast methodologies. Table 138 provides specific criteria/thresholds for selection of a locations as an NWA. Table 139 and Table 140 provide a summary of specific design/engineering criteria applied at the T&D level.

[PDF p. 325 | printed p. 307]

**Table 137. Summary of location-specific evaluation methodologies and load forecast processes**[^369]

_Extractor note (not source text): the source's column groups are Eversource (MA/NH/CT), National Grid (MA, RI), United Illuminating (CT) and Vermont. The source also prints the group label "Inclusion of the following in the load forecasts:" as shaded rows with no values._

| Criterion                                                                                                                          | Eversource MA/NH/CT          | National Grid MA | National Grid RI | United Illuminating CT | Vermont       |
| ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ---------------- | ---------------- | ---------------------- | ------------- |
| Existence of a process to establish a location-specific value for avoided T&D costs in candidate locations for NWAs                | Yes                          | Yes              | Yes              | No                     | Yes           |
| Existence of a process to identify and/or select candidate locations for NWAs                                                      | Yes                          | Yes              | Yes              | No                     | Yes           |
| Existence of a process for quantification of the required load reduction from these locations for calculation of the avoided costs | Yes                          | Yes              | Yes              | No                     | Yes           |
| Whether the identification of these locations is based on utility load forecasts                                                   | Yes                          | Yes              | Yes              | No                     | Yes           |
| Granularity of load forecasts used by the utilities in identification of these locations                                           | Transmission and substation  | System Level     | System Level     | N/A                    | Circuit Level |
| Inclusion of the following in the load forecasts:                                                                                  |                              |                  |                  |                        |               |
| Operational EE                                                                                                                     | Yes                          | Yes              | Yes              | N/A                    | Yes           |
| Operational PV                                                                                                                     | Yes                          | Yes              | Yes              | N/A                    | Yes           |
| Operational DR                                                                                                                     | Only Eversource-sponsored DR | Yes              | Yes              | N/A                    | Yes           |
| Inclusion of the following in the load forecasts:                                                                                  |                              |                  |                  |                        |               |
| Projected EE                                                                                                                       | Yes                          | Yes              | Yes              | N/A                    | Yes           |
| Projected PV                                                                                                                       | Yes                          | Yes              | Yes              | N/A                    | Yes           |
| Projected DR                                                                                                                       | Only Eversource-sponsored DR | Yes              | Yes              | N/A                    | Yes           |
| Inclusion of any electrification goals or mandates reflected in current policy                                                     | Yes                          | Yes              | Yes              | N/A                    | Yes           |

_Notes: For Eversource, exact processes may vary across individual states between New Hampshire, Massachusetts, and Connecticut._

[^369]: In 2022, after the completion of this survey, National Grid's Rhode Island service was acquired by PPL Corporation, and is now Rhode Island Energy.

[PDF p. 326 | printed p. 308]

**Table 138. Summary of processes for identifying locations that would benefit from load reductions**[^370]

| Criterion                                                                                                                                                                       | Eversource MA/NH/CT | National Grid MA               | National Grid RI               | United Illuminating | Vermont |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------------------------ | ------------------------------ | ------------------- | ------- |
| Whether the load growth forecasts are conducted in concert with the utility's T&D planning                                                                                      | Yes                 | Forecasts feed into assessment | Forecasts feed into assessment | N/A                 | Yes     |
| Whether the utility applies a minimum threshold load criterion for qualification of a location in being considered for an NWA/used to calculate location-specific avoided costs | Yes                 | Yes                            | Yes                            | N/A                 | Yes     |
| The existence of threshold load criteria used by the utility in identifying the target locations                                                                                | Yes                 | Yes                            | Yes                            | N/A                 | Yes     |
| Whether the utility develops a specific timeline for qualification of a location in being considered for an NWA/used to calculate location-specific avoided costs               | Yes                 | Yes                            | Yes                            | N/A                 | Yes     |
| Is there a timeline established for identification of a targeted location                                                                                                       | Yes                 | Yes                            | Yes                            | N/A                 | Yes     |

[^370]: In 2022, after the completion of this survey, National Grid's Rhode Island service was acquired by PPL Corporation, and is now Rhode Island Energy.

[PDF p. 327 | printed p. 309]

**Table 139. Summary of processes for identifying target locations that would benefit from load reductions at the transmission level**[^371]

_Extractor note (not source text): the source's column groups are Eversource (no state label printed), National Grid (MA, RI), United Illuminating (no state label printed) and Vermont. The "Not applicable" cells for United Illuminating are single cells in the PDF, each centered on its row; they are shown here one per row._

| Criterion                                                                                                         | Eversource                                                                                                      | National Grid MA                                                    | National Grid RI                                                    | United Illuminating | Vermont                                                                                              |
| ----------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------- | ---------------------------------------------------------------------------------------------------- |
| Whether there is consistency with the utility's local transmission planning guidelines and regulatory obligations | Yes                                                                                                             | Not applicable, screening occurs for sub-transmission projects only | Not applicable, screening occurs for sub-transmission projects only | No                  | Yes                                                                                                  |
| Whether the targeted locations are identified through power flow simulations                                      | Yes                                                                                                             | Not applicable                                                      | Not applicable                                                      | No                  | Yes                                                                                                  |
| Tools used for power flow modeling for this purpose                                                               | PSS/E, TARA                                                                                                     | Not applicable                                                      | Not applicable                                                      | Not applicable      | Not specified                                                                                        |
| How far into the future are these locations identified                                                            | 10 years                                                                                                        | Not applicable                                                      | Not applicable                                                      | Not applicable      | 10 years                                                                                             |
| What specific contingency standards are applied                                                                   | NERC, NPCC, ISO-NE Planning Eversource SYSPLAN-01 – Eversource Energy Transmission System Reliability Standards | Not applicable                                                      | Not applicable                                                      | Not applicable      | ISO-NE, NERC, and other applicable reliability planning criteria                                     |
| Whether hybrid NWA solutions are considered                                                                       | Yes                                                                                                             | Not applicable                                                      | Not applicable                                                      | Not applicable      | Yes                                                                                                  |
| Cost threshold for the traditional solution                                                                       | Considered but details not specified                                                                            | Not applicable                                                      | Not applicable                                                      | Not applicable      | >$2.5M                                                                                               |
| Timeline criteria for the start of construction of the traditional solution                                       | Considered but details not specified                                                                            | Not applicable                                                      | Not applicable                                                      | Not applicable      | ≥2 years but <10 years                                                                               |
| Load reduction and/or off-setting generation requirement                                                          | Considered but details not specified                                                                            | Not applicable                                                      | Not applicable                                                      | Not applicable      | 1–3 yrs in future = 15% peak load; 5 yrs in future = 20% peak load; 10 yrs in future = 25% peak load |

[^371]: In 2022, after the completion of this survey, National Grid's Rhode Island service was acquired by PPL Corporation, and is now Rhode Island Energy.

[PDF p. 328 | printed p. 310]

**Table 140. Summary of processes for identifying target locations that would benefit from load reductions at the distribution level**[^372]

_Extractor note (not source text): the source's column groups are Eversource (no state label printed), National Grid (MA, RI), United Illuminating (no state label printed) and Vermont._

| Criterion                                                                                                                                                                  | Eversource                                                                                                                                                       | National Grid MA                          | National Grid RI                          | United Illuminating | Vermont                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ----------------------------------------- | ------------------- | ------------------------------------------------- |
| Whether the utility applies specific design criteria (for equipment loading, phase balancing, and ranges of system voltages, etc.) in identifying these locations?         | Yes                                                                                                                                                              | Yes                                       | Yes                                       | No                  | Yes                                               |
| The existing design criteria that are applied for this purpose                                                                                                             | Equipment Loading limits, reliability targets, voltage limits, resiliency goals; anti-islanding, flicker/transient limits, fault and short circuit, reverse flow | Yes                                       | Yes                                       | Not applicable      | Yes                                               |
| Consistency of the design criteria with utility distribution planning criteria that are applied in identifying traditional engineering solutions at the distribution level | Yes                                                                                                                                                              | Yes                                       | Yes                                       | Not applicable      | Yes                                               |
| Whether the targeted locations are identified through power flow simulations                                                                                               | Not initially                                                                                                                                                    | Yes, after initial assessment             | Yes, after initial assessment             | Not applicable      | Yes                                               |
| Tools used for power flow modeling for this purpose                                                                                                                        | Synergi, CYME, PSCAD                                                                                                                                             | Not specified                             | Not specified                             | Not applicable      | CYME                                              |
| Whether hybrid NWA solutions are considered                                                                                                                                | Yes                                                                                                                                                              | Yes                                       | Yes                                       | Not applicable      | Yes                                               |
| Cost threshold for the traditional solution                                                                                                                                | >$1M                                                                                                                                                             | ≥$500K                                    | >$1M                                      | Not applicable      | >$2M or >$250K if relieving a delivery constraint |
| Timeline criteria for the start of construction of the traditional solution                                                                                                | 2 years, less than 7 years from IRP filing date                                                                                                                  | 18 months                                 | 30 months                                 | Not applicable      | ≥2 years but <10 years                            |
| Load reduction and/or off-setting generation requirement                                                                                                                   | >30MW                                                                                                                                                            | Load reduction <20% of relevant peak load | Load reduction <20% of relevant peak load | Not applicable      | 25%                                               |

[^372]: In 2022, after the completion of this survey, National Grid's Rhode Island service was acquired by PPL Corporation, and is now Rhode Island Energy.

[PDF p. 329 | printed p. 311]

The following subsections present short descriptions of the methods used by each responding utility.

#### National Grid (Massachusetts and Rhode Island)

In both Massachusetts and Rhode Island, National Grid has a process to consider NWAs as part of its distribution planning process for distribution and sub-transmission capital projects and system needs.[^373] National Grid identifies system needs as a result of studies, operational issues, process safety issues, occupational safety issues, regulatory requirements, and/or customer requests.[^374] If the annual planning process identifies a system need, and that location passes the state-specific NWA screening criteria, then the project is shifted to an NWA analysis team for further review and analysis of the system need. The screening criteria for each state are shown in Table 141 below.

**Table 141. National Grid NWA screening criteria**[^375]

| Criteria                                  | Massachusetts                                                                                                                                                                     | Rhode Island                                                                                                                                                                                                  |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Project Type Suitability                  | Project types include Load Relief and Reliability. Other types have minimal suitability and will be reviewed as suitability changes due to state policy or technological changes. | Project types include Load Relief and Reliability. The need is not based on asset condition. If load reduction is necessary, then it will be less than 20% of the total load in the area of the defined need. |
| Timeline Suitability                      | Start of construction is at least 18 months in the future.                                                                                                                        | Start of construction is at least 30 months in the future.                                                                                                                                                    |
| Cost Suitability (Cost of Wires Solution) | Greater than or equal to $500K                                                                                                                                                    | Greater than $1M                                                                                                                                                                                              |

_Source: National Grid. Guidelines for Consideration of Non-Wires Alternatives in Distribution Planning. March 2020._

The avoided cost is based on a net-present-value calculation based upon costs and benefits of the NWA solution, as well as the avoided costs of not implementing some (in the case of a hybrid solution) or all of the traditional wires solution.

National Grid also considers hybrid NWA opportunities during screening. These are an NWA solution, or a combination of NWA solutions, that addresses part of a specified system need with the rest of the system need addressed by a wires solution.

Table 142 summarizes the NWA methodology employed by National Grid, as well as recommendations for improvement.

[^373]: In 2022, after the completion of this survey, National Grid's Rhode Island service was acquired by PPL Corporation, and is now Rhode Island Energy.

[^374]: National Grid. Guidelines for Consideration of Non-Wires Alternatives in Distribution Planning. March 2020.

[^375]: In 2022, after the completion of this survey, National Grid's Rhode Island service was acquired by PPL Corporation, and is now Rhode Island Energy.

[PDF p. 330 | printed p. 312]

**Table 142. Assessment of National Grid's avoided distribution methodology and recommendations for improvement**

_Extractor note (not source text): in the source, a "-" in a cell marks no entry; multi-paragraph cells are separated here by `<br><br>`._

| Topic                                           | Overall Assessment                                                                                                                                                                                                                                                                                                                                   | Recommendations on Improvement | Recommendations on Clarity                                                 |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------- |
| **Methodology for Identification of Locations** | National Grid has a documented process and guidelines for screening NWAs.                                                                                                                                                                                                                                                                            | -                              | Access to analysis and the NWA screening tool would increase transparency. |
| **Transmission-Specific NWA Criteria**          | -                                                                                                                                                                                                                                                                                                                                                    | -                              | -                                                                          |
| **Distribution-Specific NWA Criteria**          | National Grid has a documented process which outlines the types of projects that can replace traditional solutions for NWA consideration.<br><br>National Grid has criteria in place for the type of wires projects suitable for NWAs. These include criteria for type of project (load relief, reliability, non-asset condition), timing, and cost. | -                              | -                                                                          |

#### United Illuminating

Currently, United Illuminating does not have a regulatory-approved NWA process in place within the state of Connecticut.

#### Eversource (Connecticut, Massachusetts, and/or New Hampshire)

Eversource has a documented process and framework for identifying locations where DSM could be applied to meet a system need.[^376] The need for an investment at a particular location is identified as part of the distribution planning process which accounts for all planned and existing system upgrades including the DERs. The process involves using an in-house screening tool that looks at how NWA approaches can replace traditional solutions. The tool provides a comparison of the revenue requirements between an NWA and deferring a traditional solution in assessing the locational value of an NWA.

For use in the screening tool, Eversource develops a portfolio of possible solutions and technologies which involves market research and gathering information from vendors and suppliers through RFIs (Request for Information). Possible solutions are evaluated based on longevity, dependability, and the specific need identified. These technologies are integrated into the screening tool which is designed to provide a preliminary identification of the NWA solution and whether such a solution will meet the reliability and performance needs of the system.

In screening for NWAs, Eversource considers various criteria for identifying locations and selecting technologies including the magnitude of the need (applying N-0 and N-1 criteria to assess the required

[^376]: Survey To Evaluate Program Administrators Avoided T&D methodologies. Responses received on November 16, 2020.

[PDF p. 331 | printed p. 313]

capacity of the solution), duration of the need, the time of day of occurrence of the need, and the frequency at which the need occurs.

##### Distribution Planning Screening Criteria

Non-wires candidates include:[^377]

- Projects that are capacity-related
- Projects that can be deferred via deployment of NWAs
- Hybrid Solutions: combined deployment of NWAs paired with a traditional system

Some specific suitability criteria and threshold that are excluded from NWA consideration are:

- Upgrades that impact old or failing assets, or those scheduled to be replaced
- Upgrades below a financial threshold (have a projected cost of at least $1 million)
- Upgrades with immediate needs (less than 2 years). Projects must have a planned in-service date at least 3 years after the date of the Least Cost Integrated Resource Plan (LCIRP) filing.
- Projects require more than 30 MW of peak load relief within seven years of the latest LCIRP filing.

##### Transmission Planning Screening Criteria

Eversource is required to comply with the following reliability and planning standards when planning its transmission system:[^378]

- NERC TPL-001-04 - Transmission System Standards
- NPCC Regional Reliability Reference Director #1—Design and Operation of the Bulk Power System
- ISO New England Planning Procedure 3 (PP3)—Reliability Standards for the New England Area Bulk Power Supply System
- Eversource SYSPLAN-01—Eversource Energy Transmission System Reliability Standards

[^377]: New Hampshire Public Utility Commission. October 1, 2020. "Eversource Least Cost Integrated Resource Plan." _Puc.nh.gov._ Available at: [https://www.puc.nh.gov/Regulatory/Docketbk/2020/20-161/INITIAL%20FILING%20-%20PETITION/20-161_2020-10-01_EVERSOURCE_ATT_2020_LCIRP.PDF](https://www.puc.nh.gov/Regulatory/Docketbk/2020/20-161/INITIAL%20FILING%20-%20PETITION/20-161_2020-10-01_EVERSOURCE_ATT_2020_LCIRP.PDF). Appendix D.

[^378]: Massachusetts Department of Public Utilities. Last accessed March 11, 2021. "Petitions of Western Massachusetts Electric Company d/b/a Eversource Energy Pursuant to G.L. c. 164 72 and G.L. c. 40A 3."Available at [https://fileservice.eea.comacloud.net/FileService.Api/file/FileRoom/9164120#page=54](https://fileservice.eea.comacloud.net/FileService.Api/file/FileRoom/9164120#page=54). Pg. 54-57

[PDF p. 332 | printed p. 314]

Specific transmission suitability criteria for Non-Transmission Alternatives (NTA) also include response time to contingency conditions, minimum amount of operation time that resource is available for clearing of the contingency conditions, and land availability.[^379]

Table 143 summarizes the NWA/NTA methodology employed by Eversource, as well as recommendations for improvement.

**Table 143. Assessment of Eversource's avoided distribution methodology and recommendations for improvement**

_Extractor note (not source text): in the source, a "-" in a cell marks no entry; multi-paragraph cells are separated here by `<br><br>`._

| Topic                                           | Overall Assessment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Recommendations on Improvement                                                                                               | Recommendations on Clarity |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| **Methodology for Identification of Locations** | Eversource appears to have a documented process and standardized framework for identifying locations where NWAs could be applied to meet a system need on the distribution system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | For NWAs on the distribution system, access to the analysis (e.g., the NWA screening framework) would increase transparency. | -                          |
| **Transmission-Specific NWA Criteria**          | Targeted locations are identified through power flow simulations and reliability needs; the methodology for evaluation is consistent based on utility's local transmission planning guidelines and regulatory obligations.<br><br>Eversource uses specific criteria and thresholds to exclude locations where NTAs are not suitable (minimum response time to contingency conditions, development time, land requirements). These may vary depending on the specific requirements of the project.<br><br>Eversource focuses the NTA analysis on utility-scale resources; forecasted distributed generation, energy efficiency, and demand response are already used, where applicable, to reduce transmission system needs via inclusion in the ISO New England and Eversource load forecasts. | -                                                                                                                            | -                          |
| **Distribution-Specific NWA Criteria**          | Eversource has a documented process which outlines the types of projects that can replace traditional engineering solutions for NWA consideration; it also includes in a specific set of suitability criteria for qualification of a location suitable to NWA consideration including cost threshold, timeline, and the quantity of load reduction required.                                                                                                                                                                                                                                                                                                                                                                                                                                   | -                                                                                                                            | -                          |

#### Unitil (Massachusetts and New Hampshire)

Unitil has a documented process for identification of NWA opportunities. Per this process, Unitil applies design criteria for planning of the distribution and the transmission systems. At the distribution-system level, Unitil establishes a 90 percent planning threshold of seasonal rating for loads on substation

[^379]: "Non-Transmission Alternative" is the terminology used by Eversource in referring to NWAs at a transmission level.

[PDF p. 333 | printed p. 315]

transformers, stepdown transformers protective devices, and other distribution circuit elements.[^380] In addition, at the transmission and distribution levels, Until [sic] reviews NWA projects for any piece of major equipment that is expected to exceed 80 percent of its seasonal normal rating during the five-year study period and exceed 90 percent of its seasonal normal rating in year five of the study period during normal operating conditions.[^381] The company indicated that the 80 percent threshold accounts for lead times needed to implement NWA solutions.[^382] Unitil assumes a minimum of three years to receive, evaluate, and implement NWA proposals.[^383] In addition, Unitil typically considers NWAs to be suitable in addressing loading and/or voltage constraints but not suitable for condition-based replacement projects.[^384] Projects that address aging equipment may still be evaluated for NWAs, but this may not result in the issuance of an NWA RFP.

To estimate expenditures, Unitil has established a traditional engineering solution cost threshold before considering NWA solutions. Unitil has assessed that NWAs would generally not be evaluated if the recommended traditional option has an estimated cost of less than $250,000.[^385]

Should a traditional engineering project meet the above criteria, Unitil will then issue an RFP for NWA solutions. Proposed NWAs are then reviewed through an evaluation process to score relative options for the company.

#### Vermont

Vermont's planning process is split into two phases.

##### Transmission-Level Process

Every three years, the Vermont Electric Power Company (VELCO) publishes its LRTP. The LRTP analyzes the transmission system, identifies where the system does not meet design and reliability criteria, and describes the transmission alternatives to resolve the concerns.

Within the LRTP, VELCO applies the bulk transmission screening process originally adopted by the Vermont System Planning Committee (VSPC) and submitted to the Vermont Department of Public Service (PSD) in Docket 7081. This screening process helps to determine if there is potential for the deficiency to be resolved through energy efficiency and/or alternatives such as generation or demand response (or a hybrid of transmission with efficiency and/or generation). For any transmission deficiency that screens, the PSD requires a Reliability Plan. In Vermont, Reliability Plans are synonymous with NTAs.

[^380]: Unitil. Distribution Planning Guide. November 19, 2019. Page 8.

[^381]: Id. Page 8.

[^382]: Id. Section 4.3.

[^383]: Unitil. Project Evaluation Procedure, Page 3, July 2018.

[^384]: Unitil. Project Evaluation Procedure, Page 4, July 2018.

[^385]: Unitil. Project Evaluation Procedure, Page 3, July 2018.

[PDF p. 334 | printed p. 316]

Any affected distribution utility then drafts a project-specific action plan (PSAP) as required by the Docket 7081 Memorandum of Understanding. PSAPs describe a process for moving a deficiency from identification through to implementing a solution.

##### Sub-transmission and distribution process (geographic targeting)

Distribution utilities identify distribution-level constraints for consideration by VSPC and considers bulk/predominantly bulk transmission-level constraints once an LRTP is published, as described above.

Utilities typically identify distribution constraints in their IRPs or at any time in intervening years via the VSPC "Geotargeting" processes. As part of this process, the energy efficiency utility in consultation with the distribution utility and VELCO will determine the maximum achievable energy efficiency savings potential and costs. VSPC reviews the resulting recommendations for (1) areas needing new Reliability Plans, and (2) ending energy efficiency geographic targeting in any areas where analysis shows it is no longer cost-effective. The VSPC then makes a recommendation to the PSD. A Reliability Plan is required for distribution constraints identified by distribution utilities in their IRPs or otherwise that screen in for full analysis using the Distributed Utility Planning (DUP) screening tool from Docket 6290.

There have not been any geographic targeting locations identified since 2012. According to the survey response as part of AESC 2021, Vermont noted that 15 percent of Green Mountain Power's substations are at thermal loading capacity due to backflow of distributed generation. This means that energy efficiency in some cases could lead to increased costs on the system. For example, if a substation is at capacity, increased efficiency could result in the dumping of renewable generation (because customers would reduce the use of renewable generation on-site) or require increased investments to ensure reliability. While this issue is currently limited to a small number of hours, it is anticipated to worsen over the next decade as more renewable energy comes online to meet Vermont's clean energy goals.

Table 144 summarizes the NWA methodology employed by Vermont, as well as recommendations for improvement.

[PDF p. 335 | printed p. 317]

**Table 144. Assessment of Vermont's avoided distribution methodology and recommendations for improvement**

_Extractor note (not source text): in the source, a "-" in a cell marks no entry; multi-paragraph cells are separated here by `<br><br>`._

| Topic                                           | Overall Assessment                                                                                                                                                                                                                                                                                                                                                              | Recommendations on Improvement | Recommendations on Clarity |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | -------------------------- |
| **Methodology for Identification of Locations** | Vermont has a robust framework and criteria for identifying transmission, sub-transmission, and distribution-level NWAs.                                                                                                                                                                                                                                                        | -                              | -                          |
| **Transmission-Specific NWA Criteria**          | Targeted locations are identified through VELCO LRTP using power flow simulations and reliability.<br><br>The methodology for evaluation is consistent with transmission planning guidelines and regulatory obligations.<br><br>Vermont has criteria thresholds for excluding locations where NWAs are not suitable (regarding asset condition, cost thresholds, and timeline). | -                              | -                          |
| **Distribution-Specific NWA Criteria**          | Vermont has a screening tool specific to distribution-level NWAs.<br><br>The screening tool contains criteria for excluding locations where NWAs are not suitable (emergency or failing asset, cost and timing thresholds).                                                                                                                                                     | -                              | -                          |

#### Maine

In June 2019, the Maine Legislature enacted _An Act to Reduce Electricity Costs through Non-wires Alternatives_.[^386] This Act identified a non-wires coordinator position in the Office of Public Advocate. Based on this, the criteria and process for identification of NWAs within the state of Maine is currently underway.

### Consideration of location-specific costs and benefits in generation-constrained areas

Electrical systems have historically been designed for one-way flow of electrical power from central generators to distributed loads. However, the increased adoption of distributed generation resources is causing changes in that paradigm. This is particularly true in areas where generation can now approach or exceed load, but where the grid was designed and built to serve the load. Such locations have begun to appear in New England, including several locations in Vermont at both the transmission[^387] and distribution[^388] levels.

[^386]: Maine Legislature, An Act to Reduce Electricity Costs through Non-wires Alternatives. [http://www.mainelegislature.org/legis/bills/getPDF.asp?paper=HP0855&item=3&snum=129](http://www.mainelegislature.org/legis/bills/getPDF.asp?paper=HP0855&item=3&snum=129).

[^387]: See, for example, the discussion in Vermont Public Service Department. 2019. Vermont public Service Department. January 15, 2019. "Identifying and Addressing Electric Generation Constraints in Vermont." Vermont.gov. Available at [https://publicservice.vermont.gov/sites/dps/files/documents/2019%20Act%20139%20Generation%20Constraints%20Report%20final.pdf](https://publicservice.vermont.gov/sites/dps/files/documents/2019%20Act%20139%20Generation%20Constraints%20Report%20final.pdf).

[^388]: See Green Mountain Power. 2019. _Vergennes Generation Constrained Area_ available at [https://www.vermontspc.com/library/document/download/6603/VSPC%20Vergennes%20%285-21-1019%29%20%28002%29.pdf](https://www.vermontspc.com/library/document/download/6603/VSPC%20Vergennes%20%285-21-1019%29%20%28002%29.pdf) and Green Mountain Power. 2020. _Substation Generation Constraints: Hypothetical Constraint Review_ available at [PDF p. 336 | printed p. 318] [https://www.vermontspc.com/library/document/download/7092/GMP_Hypothetical%20Constraint%20Review.pdf](https://www.vermontspc.com/library/document/download/7092/GMP_Hypothetical%20Constraint%20Review.pdf) for discussions of issues in the vicinity of Vergennes, Vermont. Other presentations and notes from the Generation Constraints Committee of the Vermont System Planning Committee can be found here: [https://www.vermontspc.com/vspc-at-work/subcommittees](https://www.vermontspc.com/vspc-at-work/subcommittees). _(Extractor note (not source text): footnote 388 is printed across the bottom of PDF pp. 335 and 336; the body text of PDF p. 336 follows.)_

As part of its interconnection process, each generator is generally asked to pay for incremental changes in the grid that are required to interconnect safely and without impacting reliable service to customers. However, changes in load are not generally subject to the same type of analysis even though they could change the relationship between load and generation on a given circuit or other grid segment. Changes in end-use load that result in increased load during times when the distributed generation is producing could have the effect of mitigating reliability concerns, reducing strain on transformers or other grid hardware, or allowing more generation to interconnect (thereby potentially advancing state energy policies). On the other hand, changes in end-use load that result in decreased load during times when the distributed generation is producing could exacerbate reliability concerns, increase strain on grid hardware, or cause curtailment of generation.

Many of the general principles and considerations of localized avoided T&D costs could apply in the context of generation-constrained areas, just as they apply in the context of load-constrained areas. For example, the analysis would need to identify the specific costs corresponding to changes in the grid configuration that could be avoided or created by a change in end-use energy demand. With sufficient information regarding costs and the impacts on relevant peak loads (or exports), it would be possible to calculate a location-specific avoided T&D cost value for interventions that increase load, and a location-specific cost caused for interventions that decrease load, using the same approach to location-specific avoided T&D costs described earlier in this section.

The temporal and locational characteristics of the need should be carefully described. For example, if the issue of concern is created on sunny days during shoulder seasons when loads are otherwise low, then changes in an end use that operates only during the coldest days of winter would have no impact. The dynamic aspects of active demand management and load control measures that can respond to grid conditions (such as different behavior on sunny and cloudy days) should be considered. This would entail accounting for the contribution during peak and off-peak hours rather than only accounting for the average behavior across all hours. Hourly load profiles and load shapes for measures, including correlations with weather conditions where relevant, may be required to fully evaluate the impacts of traditional efficiency or electrification measures.

## 10.5. Avoided natural gas T&D costs

See Section 2.4: _Avoided natural gas cost methodology_ for more information on the assumptions used in AESC with respect to natural gas transmission and distribution.

[PDF pp. 337-436 not transcribed: Chapter 11 Value of Reliability (PDF pp. 337-347, in 11_value_of_reliability.md of this folder), Chapter 12 Sensitivity Analysis and Appendices A-K (PDF pp. 348-436, in the other files of this folder; see README.md)]
