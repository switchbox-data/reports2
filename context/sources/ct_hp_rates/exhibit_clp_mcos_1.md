---
source_file: "Eversource - 2026 - Docket 26-05-10 Exhibit CLP-MCOS-1.pdf"
citekey: clp_Docket260510Exhibit_2026d
docket: "26-05-10"
utility: The Connecticut Light and Power Company d/b/a Eversource Energy
filer: The Connecticut Light and Power Company d/b/a Eversource Energy
document_type: testimony
filing_date: 2026-07-14
pages_total: 21
extraction_scope: full
citation_scheme: page_line
---

# Exhibit CLP-MCOS-1 — Direct Testimony of Amparo Nieto (Marginal Cost of Service Study)

**Source**: `Exhibit CLP-MCOS-1.pdf`
**Pages**: 21 total (cover + TOC + 19 numbered testimony pages)
**Date**: July 14, 2026
**Author(s)**: Amparo Nieto
**Author affiliations**: Director, Energy Practice, Berkeley Research Group (BRG); testimony on behalf of The Connecticut Light and Power Company d/b/a Eversource Energy
**Docket**: Connecticut PURA Docket No. 26-05-10 — Application of The Connecticut Light and Power Company d/b/a Eversource Energy to Amend Its Rate Schedules
**Exhibit**: CLP-MCOS-1 (Marginal Cost of Service Study testimony)
**Companion schedules**: Exhibit CLP-MCOS-2 (`exhibit_clp_mcos_2.md`) — Schedule E-6.0 / MCOS summary tables (2026–2031)

**Extraction method**: `pdftotext -layout`, then structured into markdown; Q&A and section headings normalized and soft hyphenation at line breaks rejoined. Figures are described inline; see the PDF for diagrams. Page and line markers were added afterwards from the PDF's text layer (`just sources-page-skeleton`; checked with `just sources-check-pages`).

**Page and line markers**: Each PDF page begins with a `[PDF p. N | printed p. M]` marker (PDF pages 1-2, the cover and table of contents, print no page number; printed pages 1-19 are PDF pages 3-21). Every numbered testimony line keeps its margin line number as `{n}` and its own markdown line, so `just sources-cite` can give page and line. Markdown joins the lines back into paragraphs. Running headers and footers (docket, exhibit, "Page N of 19") are omitted; the page markers record them. Words hyphenated across two lines stay split as printed (for example `long-` / `term`). The three bullets in the answer on printed pp. 3-4 and the three numbered items on printed p. 8 are marked up as markdown lists.

Note: Minor typographical errors in the source (e.g. “REGUATORY” on the cover, “Berkley” for “Berkeley”, missing “I” in “am a Director”) have been corrected for readability where unambiguous. Other source typos in the testimony (e.g. “MCS study”, “BENEFITIAL”, “TOU period. as per”) are kept as printed. Substantive corrections are annotated inline.

Note (repair from the PDF): the earlier extract read printed p. 10, line 8 as “added. We used the Company’s FERC Form 1 reports”; the PDF prints “added wed the Company’s FERC Form 1 reports”, which is now reproduced with a `[sic; …]` note. The older ad hoc `_Testimony page N_` notes are replaced by the standard page markers. Stray margin line numbers “2 3” that had been captured inside the Figure 2 chart text were removed.

---

## Cover

[PDF p. 1]

STATE OF CONNECTICUT\
PUBLIC UTILITIES REGULATORY AUTHORITY

**Docket No. 26-05-10**

APPLICATION OF THE CONNECTICUT LIGHT AND POWER COMPANY\
D/B/A EVERSOURCE ENERGY\
TO AMEND ITS RATE SCHEDULES

**DIRECT TESTIMONY OF**\
AMPARO NIETO

Marginal Cost of Service Study

On behalf of\
The Connecticut Light and Power Company\
d/b/a Eversource Energy

July 14, 2026

---

## Table of Contents

[PDF p. 2]

| Section | Title                                      | Page |
| ------- | ------------------------------------------ | ---- |
| I.      | INTRODUCTION                               | 1    |
| II.     | SUMMARY OF TESTIMONY                       | 3    |
| III.    | METHODS USED IN THE COMPANY’S RATE CASE    | 7    |
| IV.     | RATE DESIGN IMPLICATIONS OF MARGINAL COSTS | 14   |

**Exhibits**

- Exhibit CLP-MCOS-2 — Marginal Cost of Service Study Summary (Schedule E-6.0)

---

[PDF p. 3 | printed p. 1]

## {1} I. INTRODUCTION

{2} **Q.** PLEASE STATE YOUR NAME AND CURRENT POSITION.

{3} **A.** My name is Amparo Nieto. I am a Director at the Energy Practice of Berkeley Research
{4} Group (BRG), where I lead the electricity tariff and cost of service practice.

{5} **Q.** PLEASE SUMMARIZE YOUR EDUCATION AND PROFESSIONAL
{6} EXPERIENCE.

{7} **A.** I am an economist with 30 years of consulting experience in the energy industry. I
{8} extensively advise and testify on behalf of electric and natural gas utilities in the United
{9} States, Canada and overseas, on innovative retail rates for all customers in the context
{10} of decarbonization and electrification, electricity and natural gas marginal cost studies,
{11} improvements to embedded cost allocation methods, evaluation of demand response
{12} programs and interruptible rates, reform of Net Energy Metering (“NEM”) and electric
{13} vehicle rates, and other pricing and regulatory matters. I have supported the design of
{14} multi-part rate structures and time of use (“TOU”) rate options that provide more
{15} efficient price signals as customers have access to distributed energy resources
{16} (“DERs”) such as behind-the-meter solar, energy storage, electric vehicles. In
{17} California, I advised the California Public Utilities Commission (CPUC) during the [PDF p. 4 | printed p. 2]
{1} state comprehensive reform of NEM that adopted net billing and time of use rates along
{2} with avoided cost compensation. In New York and Illinois, I led the system-wide and
{3} locational marginal cost distribution studies that supported the development of
{4} compensation to DERs for their value to the grid. For many years, I have directed a
{5} membership-based utility working group that discusses rate innovation and regulatory
{6} policy strategies. I also advise ISOs and regulatory commissions in the United States,
{7} Spain, Australia, and Ireland in wholesale and retail market design. I hold a Masters’
{8} degree in Economic Analysis from the Institute for Fiscal Studies of Madrid, Spain,
{9} and a BA in Economics from the University of Carlos III of Madrid. My curriculum
{10} vitae is set forth in Exhibit CLP-ACOS-3, accompanying my testimony submitted as
{11} Exhibit CLP-ACOS-1 in the Application in this proceeding.

{12} **Q.** WHAT IS THE PURPOSE OF YOUR TESTIMONY?

{13} **A.** The purpose of my testimony is to present the Marginal Cost of Distribution Service
{14} (“MCOS) study that I prepared for the Company in the present rate case, to be used as
{15} a guide for rate design. In my testimony, I describe the principles behind using
{16} marginal costs for rate design, the methods employed for the study, and a summary of
{17} the results by rate class. I also provide opinion on the use of the study results in making
{18} informed rate design decisions that enhance the efficiency and equity properties of the
{19} Company’s existing distribution rates. A more detailed summary of the 2026 MCOS
{20} results is submitted along with this testimony in Exhibit CLP-MCOS-2.

[PDF p. 5 | printed p. 3]

{1} **Q.** HAVE YOU SEPARATELY PROVIDED TESTIMONY IN THIS RATE CASE?

{2} **A.** Yes. I also directed the development of the Company’s Allocated Cost of Service
{3} Study (“ACOS”) and have submitted separate testimony in this proceeding, in Exhibit
{4} CLP-ACOS-1.

---

## {5} II. SUMMARY OF TESTIMONY

{6} **Q.** PLEASE SUMMARIZE THE KEY ROLE OF A MARGINAL COST STUDY IN
{7} RATE DESIGN.

{8} **A.** Rate designs that use marginal cost information and follow marginal cost principles are
{9} best suited to support three of the major ratemaking objectives:

- {10} Fostering economically-efficient energy usage decisions that lead to a more
  {11} efficient expansion of the distribution grid; customers are able to make more
  {12} informed decisions that align with the provision of reliable service at the lowest
  {13} possible cost when the corresponding rates signal the true underlying cost impact
  {14} to from incremental usage. The marginal cost study is also useful to determine the
  {15} appropriate time of use periods for distribution time of use (TOU rates),
- {16} Ensuring equitable rates or mitigating intra-class cross-subsidies over time;
  {17} marginal-cost based tariffs help prevent increases in inter and intra-class cross
  {18} subsidies as individual customers change their consumption because these rates
  {19} generally help tracking ongoing changes in the incremental cost to serve,
  {20} particularly when differentiating by season and by time of usage. [PDF p. 6 | printed p. 4]
- {1} Preserving customer affordability in the transition to a decarbonized sector. When
  {2} energy charges are set well above marginal unit costs, customers that add usage
  {3} will tend to experience disproportionally higher bills that exceed the incremental
  {4} cost of incremental service.

{5} **Q.** COULD YOU FURTHER EXPLAIN THE PREMISE OF MARGINAL COST
{6} RATE DESIGNS BEING BENEFITIAL FOR AFFORDABILITY GOALS?

{7} **A.** Yes. Marginal-cost based rate designs tend to bring usage charges lower and closer to
{8} marginal usage cost, while rising existing monthly customer charges towards marginal
{9} customer and connection-related costs. This design can largely mitigate increasingly
{10} affordability concerns of customers who wish to actively support decarbonization by
{11} acquiring electric vehicles or adopting efficient heat pumps for electric space heating
{12} and would otherwise be disproportionally burdened. In addition, this rate design also
{13} avoids harming affordability in the longer-term for low to moderately low-income
{14} customers, who generally have a limited ability to undertake hedging strategies like
{15} adding rooftop solar or shifting consumption away from the highest-cost hours with
{16} battery storage. When rates are not appropriately structured to mirror marginal cost, it
{17} is more likely that these customers ultimately shoulder the Company net revenue losses.

{18} **Q.** PLEASE EXPLAIN HOW RATES CAN MIRROR MARGINAL COST
{19} STRUCTURE, OTHER THAN BY SIMPLY RELYING.

{20} **A.** Ideally, an efficient distribution rate would be a 3-part rate that reflects the underlying
{21} structure of marginal costs of service, by adding a monthly subscription charge or
{22} facility charge, to differentiate cost by customer size, as well as to collect a share of the [PDF p. 7 | printed p. 5]
{1} revenue requirement for existing plant outside of usage charges. Currently, efforts are
{2} being implemented across the country to reduce the over-reliance of fixed distribution
{3} cost recovery through usage charges and increase fixed charges to increase equity
{4} across customers within the class. Such rate rebalancing process also reduces the
{5} distortion in price signal (i.e., increments of usage lead to a lower grid cost impact than
{6} the existing kWh charges appear to indicate) and the existing cross-subsidies within the
{7} class (higher usage customers disproportionally paying more than cost of service).

{8} **Q.** PLEASE BRIEFLY SUMMARIZE THE SCOPE OF THE MARGINAL COST
{9} ANALYSIS.

{10} **A.** The MCOS that I conducted for the Company evaluates all elements of marginal
{11} distribution costs of service, from upstream distribution grid to the local equipment
{12} needed to serve each customer and associated services. The study involves identifying
{13} the local and system-wide incremental cost of expanding the distribution system based
{14} on a detailed review of growth-related capacity expansion projects that will go into
{15} service during the study period 2026 – 2031 and the corresponding Company’s peak
{16} load forecasts driving those investments. This analysis produces forward-looking unit
{17} costs and establishes the appropriate basis for efficient usage-related price signals.
{18} Additionally, the study estimates marginal cost incurred by the Company to provide
{19} customer access to the grid, as well as other customer-related services. These costs vary
{20} with customer type (by service class, phase of service and installation type). The last
{21} two cost components represent the share of marginal costs of service that do not vary
{22} with on-going usage over time.

[PDF p. 8 | printed p. 6]

{1} **Q.** WHAT ARE THE MAIN FINDINGS FOR THE UPSTREAM DISTRIBUTION
{2} SYSTEM?

{3} **A.** One key finding of the study is that about 24 percent of the total system load expected
{4} at the end of the study period (year 2031) is located in distribution substation areas that
{5} will require capacity expansion to meet peak load reliably during the six-year period.
{6} The system-wide marginal distribution unit cost calculation reflects this finding. The
{7} MCOS also time-differentiates the system-wide marginal costs and allocates it to hours
{8} of the day and months that are more likely to trigger capacity needs when customers
{9} increase their consumption. The analysis of the Company’s distribution substation
{10} hourly load patterns, after considering the expected trend in PV, heat pump and EV
{11} adoption, revealed that the Company will continue to be summer-peaking through year
{12} 2031, which is the study period covered by the analysis, and there is a very small
{13} probability of peak falling on the coldest winter months as I will explain later in my
{14} testimony.

{15} **Q.** PLEASE SUMMARIZE TO WHAT EXTENT MARGINAL COST RESULTS
{16} CAN GUIDE THE COMPANY CLASS REVENUE ALLOCATION.

{17} **A.** The Company rate revenue targets are decided primarily on the basis of the Company’s
{18} allocated cost of service study (ACOS), subject to other objectives such as gradualism
{19} in changes. While the Company continues to rely on ACOS results for setting class
{20} revenue targets in this rate case, it is important to ensure that each rate class is paying
{21} at least the corresponding marginal costs of service, using the MCOS results. This
{22} includes economic development rates. I compared the results of the ACOS allocations
{23} and they are directionally aligned with the results of marginal cost-based allocations, [PDF p. 9 | printed p. 7]
{1} as shown in Exhibit MCOS-2. Additionally, the direction of changes in class revenue
{2} requirement suggested by the ACOS for the major rate classes is consistent with those
{3} suggested by the MCOS results, in terms of moving towards cost parity by rate class.

---

## {4} III. METHODS USED IN THE COMPANY’S RATE CASE

{5} **Q.** PLEASE DEFINE MARGINAL COSTS.

{6} **A.** Marginal cost is the cost of the additional resources needed to produce and/or deliver
{7} the next small increment of output (or the costs avoided when consumers reduce their
{8} demand by a small amount). In perfectly competitive conditions, a market-clearing
{9} price is defined by the intersection of the total suppliers’ marginal supply cost curve
{10} and the aggregated demand curve. In presence of natural monopolies, such as the
{11} regulated distribution business, prices equal to marginal cost would fail to produce the
{12} required revenue to recover all costs, because distribution stations and feeders exhibit
{13} large economies of scale and investment is lumpy. Marginal costs are still relevant to
{14} determine the apportionment of costs between the different rate components and rate
{15} design, and to ensure that all customers pay no less than marginal cost plus an equitable
{16} share of existing (sunk) costs.

{17} **Q.** PLEASE DESCRIBE THE ELEMENTS OF THE MCOS STUDY.

{18} **A.** The MCOS study a forward-looking exercise over a six-year horizon (2026 - 2031).
{19} This timeframe represents a reasonable period to ensure that rates reasonably reflect
{20} the expected capacity conditions and system needs during the period the rates will be [PDF p. 10 | printed p. 8]
{1} in effect. Using a shorter period would affect marginal cost stability for pricing
{2} purposes.
{3} The MCOS covers the following elements of delivery service:

1. {4} Marginal, time-related upstream delivery costs, including costs of bulk and non-
   {5} bulk distribution stations, and trunk-line primary feeders that connect these
   {6} substations to the more local primary lines. These are time-related costs as they
   {7} are closely related to the growth in expected station peak loads. Only load
   {8} increases (or reductions) in hours coincident with the station peak hours have a
   {9} bearing on the marginal costs of this component of service.
2. {10} Local distribution facilities costs, including transformers and conductors local
   {11} to the customer premises (primary and secondary). These costs vary with
   {12} customer type (by service class, phase of service and installation type). When
   {13} a new customer begins to receive service, marginal facilities cost involves local
   {14} transformer and local line capacity to accommodate the customer’s expected
   {15} long-term maximum demand.
3. {16} Other components of distribution equipment are strictly customer-related, such
   {17} as the cost of meters and service drops, and costs required to administer and
   {18} process meter reads and billing, and other services.

{19} **Figure 1 is a simplified diagram of the Company’s electric distribution system.**

[PDF p. 11 | printed p. 9]

{1} **Figure 1. Simplified CL&P’s Electric Delivery System Diagram**

[See original PDF p. 11 (printed p. 9) for the diagram]

{3} **Q.** PLEASE DESCRIBE THE COMPUTATION OF THE MARGINAL
{4} DISTRIBUTION SUBSTATION AND PRIMARY FEEDER COSTS.

{5} **A.** The MCS study estimates the marginal growth-related capacity investment, stated in
{6} $ per kW of added peak load carrying capability. The starting point of the marginal
{7} high-voltage distribution cost analysis is a review of the Company’s budgeted
{8} investments in bulk substations during the study period. The annualized bulk
{9} substation marginal costs are averaged across all the capacity-expansion areas where
{10} the corresponding projects are located. Since the distribution rate design is not
{11} geographically differentiated, a system-wide marginal cost analysis ultimately needs to [PDF p. 12 | printed p. 10]
{1} be produced, by accounting for the share of the system peak load that is served in areas
{2} of effectively zero marginal costs as they can reliably accommodate load without
{3} requiring expansion. The system-wide marginal cost was annualized using the
{4} appropriate economic carrying charge. The final step of the computation of marginal
{5} distribution substation cost required using marginal operation and maintenance
{6} (“O&M”) expenses and loading factors to account for administrative and general
{7} (“A&G”) expenses. Marginal distribution station and line O&M expenses were then
{8} added wed [sic; possibly intended “added. We used”] the Company’s FERC Form 1 reports to identify annual distribution O&M
{9} expenses in recent years. Upon review of the annual expense per kW (in constant
{10} dollars) in these years, divided by total non-coincident distribution station peak demand
{11} for the Company, the most recent four-year average expense was selected to represent
{12} future marginal O&M expenses per kW of station peak load.

{13} **Q.** WHAT INVESTMENT TYPES WERE REVIEWED IN THE CALCULATION
{14} OF UPSTREAM DISTRIBUTION MARGINAL COSTS?

{15} **A.** The investments adding capacity that are selected for the study address deficiencies
{16} from the point of view of meeting load during base loading conditions (N-0), as well
{17} as in contingency scenarios (N-1). The Company will generally expand a substation
{18} transformer when the peak load is expected to be at or above 75 percent (bulk stations)
{19} assuming zero transfers, or when peak load may begin to approach the transformer’s
{20} load carrying capability. The study excludes projects that are driven by the need to
{21} modernize the grid, improvements of asset condition, or replacement of aging facilities [PDF p. 13 | printed p. 11]
{1} over the study period, since these are necessary investments to address substandard
{2} design, or other reliability-related issues that are unrelated to growth in peak load.

{3} **Q.** WHAT INFORMATION WAS USED TO RELY ON THE SHARES OF THE
{4} SYSTEM THAT ARE GROWING?

{5} **A.** The ratio of forecasted substation peak loads of planned substation areas to total system
{6} peak load forecast determines the share of the system that requires capacity addition
{7} over the six-year period, which is about 24% for the distribution substations and about
{8} 14% for distribution feeders. The Company provided annual substation and feeder peak
{9} demands along with summer forecasted peak load by planning area that includes a
{10} combination of organic load growth, electrification, and step load additions due to
{11} commercial and industrial activity. This information was used to estimate the total peak
{12} load at the substation level that will be located in areas that require capacity expansion
{13} investments to serve station peak demand reliably during the six-year study period. A
{14} system-wide marginal cost was calculated by multiplying the distribution substation
{15} cost by this share, and an equivalent calculation was performed for the primary
{16} trunkline feeders. The sum of the weighted average cost of the distribution substation
{17} and the weighted marginal cost of the primary feeder results in the total upstream
{18} marginal per-kW investment through the six-year study period. This calculation is
{19} provided in Attachment MCOS-2.

[PDF p. 14 | printed p. 12]

{1} **Q.** DID YOU TIME-DIFFERENTIATE THE ANNUALIZED MARGINAL
{2} DISTRIBUTION COST?

{3} **A.** Yes. The annualized marginal distribution costs must be allocated to those hours in
{4} the year that are most likely to trigger a need for investment when load increases.
{5} Thus, the MCOS study used an hourly probability of peak analysis that calculates the
{6} standard deviation of hourly loads across day types and months, using recent years of
{7} distribution hourly load profiles (2022 through 2025). The probability of peak
{8} statistically calculates the likelihood that each hour of each day type may reach or
{9} exceed the annual peak load. The hourly loads are normalized to isolate the effect of
{10} customer growth which leads to overall changes of peak demand year to year. Further
{11} analysis is undertaken to account for expected modifications of the historical hourly
{12} load shapes at the substation, using projections of behind the meter solar growth, as
{13} well as heat pump load adoption as the system approaches year 2031. The results of
{14} the analysis were used to allocate the annual marginal substation costs to hours and
{15} months, which ultimately are summarized by TOU period. as per existing TOU rates.
{16} These results by TOU period are provided in Exhibit CLP-MCOS-2, Table 2.

{17} **Q.** PLEASE EXPLAIN THE COMPUTATION OF LOCAL MARGINAL
{18} DISTRIBUTION FACILITIES COSTS.

{19} **A.** The MCOS estimates the cost that is incurred when the Company connects the most
{20} typical (average customer) in a given rate class to the grid. The Company is responsible
{21} for providing customer access in perpetuity, unless the site is permanently abandoned.
{22} The design demand for customers to be connected affects the sizing of the line
{23} transformer and local lines and it is expected to be sufficient to serve the expected long- [PDF p. 15 | printed p. 13]
{1} term maximum load that the customers over the service life of the facilities. This
{2} concept of demand is local in nature and distinctly different from the upstream
{3} diversified peak demands considered when sizing the upstream distribution
{4} infrastructure. The local distribution facilities costs may vary depending on whether
{5} facilities are overhead or underground, as well as whether they are single-phase or poly-
{6} phase, and customer density. To estimate the typical installed cost of distribution
{7} facilities, an extensive sample of work orders associated with customer connection jobs
{8} in the most recent four years (2022-2025), representative of the different mix of
{9} connections in the Company’s service territory were reviewed. The study computes
{10} the typical per-kW installed cost of connection by customer class, net of customer
{11} contributions. Appropriate class-weighted local facilities costs were calculated, in
{12} 2026$, based on the approximate mix of overhead vs underground connections and
{13} single and three-phase facilities within each customer class.

{14} **Q.** DESCRIBE THE METHOD USED TO ESTIMATE MARGINAL CUSTOMER
{15} COSTS.

{16} **A.** The marginal customer-related costs refer to costs unrelated to energy, peak demand,
{17} or design demand at the time of connection. These include the installed cost of the
{18} meter and service drop, customer accounts and customer service and informational
{19} expenses. Once the annualized installed costs of these assets for all customer categories
{20} are estimated, marginal O&M and marginal customer service expenses are added to
{21} obtain the total marginal customer cost by class. The marginal customer service and
{22} informational expenses, and the marginal customer account expenses incorporate [PDF p. 16 | printed p. 14]
{1} information from the ACOS, based on relative customer class requirements and
{2} frequency of each activity by customer class. As per other components of the study,
{3} loading factors were applied to reflect non-plant A&G expenses and general plant.

---

## {4} IV. RATE DESIGN IMPLICATIONS OF MARGINAL COSTS

{5} **Q.** WHAT KEY RATE DESIGN CHANGES ARE SUGGESTED BY THE
{6} RESULTS OF THE MCOS?

{7} **A.** The main rate design implication from the results of the 2026 MCOS study is that
{8} customers are currently paying significantly more than the underlying marginal per-
{9} kW and per-kWh costs across the board, when comparing marginal unit cost per kW
{10} or per kWh with the existing charges. The marginal unit cost per kW of peak load
{11} growth is relatively low on a system-wide average basis, recognizing that the majority
{12} of the system can accommodate load growth over the next six-year planning period.
{13} While the current per-kWh charges in distribution rates exceed the per-kWh marginal
{14} costs of upstream distribution service to recover other non-marginal cost associated
{15} with the existing revenue requirement, the large differential suggests an excessive
{16} incentive to conserve that can be moderated to bring rates closer to optimal, more
{17} efficient price signals, particularly for classes when the monthly fixed charge remains
{18} lower than the marginal customer and facilities costs. Thus, I recommend lowering the
{19} usage charges for these classes, and allocating more costs to the fixed component of
{20} the rate, and when the rate has blocked charges, to the first block of usage. Reconciling
{21} marginal cost-based revenue with the class revenue requirement this way minimizes
{22} distortions in price signals. Table 1 below illustrates the marginal unit cost for each [PDF p. 17 | printed p. 15]
{1} component of the service using the existing time of day periods and the year-round
{2} construct of the existing rates. Marginal local distribution facilities costs are shown
{3} separately, in two alternative ways – per customer and per kW of monthly design or
{4} contract demand. Marginal primary costs are also shown in two alternative ways – per
{5} kW of monthly metered demand and per kWh of usage. The marginal unit cost figures
{6} have not been marked up to reconcile class marginal cost revenues with the Company
{7} proposed class revenue targets, but they are still useful to assess the efficiency of the
{8} price signals in the current rates.

[PDF p. 18 | printed p. 16]

{1} **Table 1. Marginal Unit Cost by Rate Component, using existing TOU Periods**

| Service   | Customer cost ($/mo) | Local facilities ($/cust-mo) | Local facilities ($/kW-mo design) | Period   | Primary demand ($/kW-mo) | Primary energy ($/kWh) |
| --------- | -------------------: | ---------------------------: | --------------------------------: | -------- | -----------------------: | ---------------------: |
| Rate 1    |                28.98 |                        24.51 |                              3.06 | All      |                        — |                0.00242 |
| Rate 5    |                36.14 |                        34.09 |                              3.06 | All      |                        — |                0.00242 |
| Rate 7    |                59.74 |                        24.51 |                              3.06 | On-Peak  |                        — |                0.00727 |
| Rate 7    |                      |                              |                              3.06 | Off-Peak |                        — |                0.00099 |
| Rate 18   |                47.29 |                        15.32 |                              3.06 | All      |                        — |                0.00241 |
| Rate 27   |               113.54 |                       342.03 |                              1.90 | All      |                     1.76 |                0.00241 |
| Rate 27A  |               111.53 |                       342.03 |                              1.90 | All      |                     1.76 |                0.00241 |
| Rate 30   |                39.10 |                        47.76 |                              2.39 | All      |                     1.76 |                0.00241 |
| Rate 30A  |                41.50 |                        59.70 |                              2.39 | All      |                     1.76 |                0.00241 |
| Rate 35   |                73.61 |                       149.73 |                              1.25 | All      |                     1.76 |                0.00241 |
| Rate 37   |               118.70 |                       361.58 |                              1.45 | All      |                     1.76 |                0.00241 |
| Rate 39   |               816.84 |                     4,537.10 |                              1.47 | All      |                     1.76 |                0.00241 |
| Rate 40   |                52.38 |                        56.30 |                              1.88 |          |                     1.76 |                0.00241 |
| Rate 41   |               181.64 |                       801.11 |                              1.50 | On-Peak  |                     1.20 |                0.00723 |
| Rate 41   |                      |                              |                                   | Off-Peak |                     0.55 |                0.00098 |
| Rate 55   |               182.83 |                       766.10 |                              1.21 | On-Peak  |                     1.20 |                0.00723 |
| Rate 55   |                      |                              |                                   | Off-Peak |                     0.55 |                0.00098 |
| Rate 56   |               208.84 |                       899.03 |                              1.30 | On-Peak  |                     1.20 |                0.00723 |
| Rate 56   |                      |                              |                                   | Off-Peak |                     0.55 |                0.00098 |
| Rate 57   |               135.93 |                     2,810.54 |                              1.03 | On-Peak  |                     1.20 |                0.00723 |
| Rate 57   |                      |                              |                                   | Off-Peak |                     0.55 |                0.00098 |
| Rate 58   |               135.96 |                     4,426.86 |                              1.03 | On-Peak  |                     1.20 |                0.00723 |
| Rate 58   |                      |                              |                                   | Off-Peak |                     0.55 |                0.00098 |
| Rate EV-S |                68.29 |                       168.95 |                              2.48 |          |                     1.76 |                 0.0024 |
| Rate EV-M |                79.05 |                       192.84 |                              1.30 |          |                     1.76 |                 0.0024 |
| Rate EV-L |               149.33 |                       807.82 |                              1.30 |          |                     1.76 |                 0.0024 |

[PDF p. 19 | printed p. 17]

{1} **Q.** IN YOUR OPINION, DO THE RATE DESIGNS PROPOSED BY THE
{2} COMPANY OVERALL ALIGN WITH MARGINAL COST STUDY RESULTS?

{3} **A.** I have reviewed the Company’s rate proposals and in my opinion the direction of
{4} changes proposed aligns with what the MCOS suggests. This measure will help avoid
{5} intra-class cross subsidies, while considering and avoiding extreme bill impacts. In my
{6} opinion, the proposals recognize that rates should gradually be rebalanced to seek
{7} improved economic efficiency and equity.

{8} **Q.** DID YOU EVALUATE THE SUITABILITY OF THE EXISTING TIME OF
{9} USE PERIODS?

{10} **A.** Yes. Time-differentiated distribution rates must keep in mind the system-wide
{11} distribution hourly marginal cost patterns. Current peak period is defined as noon to
{12} 8pm, year-round. There is significantly lower probability of peak from noon to 3 pm
{13} relative to hours 3 pm to 8 pm, which recognizes the impact of solar PV penetration
{14} in early to mid-afternoon. This suggests that a modification to introduce a shorter
{15} peak period that starts at 4 pm and ends at 9 pm would increase cost-reflectiveness of
{16} the distribution rate. This revision would align with the prevailing marginal unit cost
{17} profile. The addition of a shoulder period would optimize the time of use price
{18} signals. The largest beneficial impacts of customer adoption of TOU rates will
{19} materialize once the Company experiences higher enrollment in TOU rates and at that
{20} point it will be particularly critical to include only the core peak hours in the peak
{21} period. Figure 2 below shows the hourly probability of peak for a typical summer
{22} day.

[PDF p. 20 | printed p. 18]

{1} **Figure 2. Hourly probability of peak, typical Summer Weekday and Weekend**

[See original PDF p. 20 (printed p. 18) for the chart]

14.00%
12.00%
10.00%
8.00%
6.00%
4.00%
2.00%
0.00%
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
Weekday Weekend/Holiday

{4} **Q.** IS SEASONAL DIFFERENTIATION NECESSARY TO IMPROVE PRICE
{5} SIGNALS IN RATE DESIGN?

{6} **A.** Yes. A decision to keep the same TOD charges year-round does not strictly align with
{7} the underlying seasonality in peak-related costs. About 80 percent of the annual
{8} probability of peak falls in two months, July and August, and the remaining 19.5
{9} percent falls in the months of June and September, with less than 1 percent falling in
{10} the coldest winter months of December through January. Only a very small number of
{11} bulk substations experience a peak load in the winter months of December or January,
{12} and even then, there is higher substation load-carrying capability in the winter relative
{13} to the summer. Continuing with year-round distribution TOU periods would not
{14} support efficient adoption of heat pump rates, and therefore I recommend the
{15} Company’s proposal to set seasonal rates for heat pump use. TOU rates that are also [PDF p. 21 | printed p. 19]
{1} seasonally-differentiated would be advisable eventually, particularly when considering
{2} growth of DERs and impact on the distribution station load profile in the future. In the
{3} longer-term, additional electrification will shift more cost responsibility to the winter
{4} evening hours.

{5} **Q.** DOES THIS CONCLUDE YOUR TESTIMONY?

{6} **A.** Yes, it does.
