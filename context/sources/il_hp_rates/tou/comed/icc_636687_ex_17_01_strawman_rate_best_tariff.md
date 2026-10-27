# ComEd Ex. 17.01 — Strawman Rate BEST (Basic Electric Service Time of Use Pricing) Tariff (Rehearing)

**Source**: `icc_636687_ex_17_01_strawman_rate_best_tariff.pdf` (ICC e-docket file id / filing id 636687)
**Pages**: 20 (tariff draft sheets, one sheet per page)
**Date**: Draft; all dates left blank in the source ("Date Effective: XXX YY, 2025"; "Issued pursuant to the Illinois Commerce Commission Order on Rehearing dated XXX YY, 2025, in Docket No. 24-0378"). Filed as an exhibit to ComEd's rehearing direct testimony (ComEd Ex. 17.0, Kremer) in 2025.
**Docket**: ICC Docket No. 24-0378 (Commonwealth Edison Co., revenue-neutral tariff changes related to rate design — Rate BEST / DTOU), on Rehearing
**Author(s)**: Commonwealth Edison Company (tariff text); "Issued by David R Perez, EVP and COO"
**Document type**: Strawman (illustrative draft) tariff sheets — Word-exported, sheet numbers left as placeholders
**ComEd exhibit no.**: ComEd Ex. 17.01
**Extraction method**: Embedded PDF text (PyMuPDF), equations verified against rendered page images
**Extraction notes**:

- _Minor typographical errors in the source have been corrected for readability. Substantive corrections are annotated inline._
- **Draft status**: every sheet is headed "xth Revised Sheet No. xx / (Canceling xth Revised Sheet No. xx)". These placeholders are kept as written (`x`, `xx`); they are not real sheet numbers. The "(Continued from Sheet No. x+n) / (Continued on Sheet No. x+n)" lines are given at each page marker below as printed. They are not strictly sequential in the source (pp. 9 and 10 both print "Continued from Sheet No. x+7" / "Continued on Sheet No. x+9"; p. 19 says "Continued on Sheet No. x+18" although the final page, p. 20, says "Continued from Sheet No. x+17").
- **Boilerplate omitted** (stated once here): the page-top exhibit stamp "ICC Docket No. 24-0378 (on Rehearing) / ComEd Ex. 17.01"; and on every sheet the header block "ILL. C. C. No. 10 / Commonwealth Edison Company / ELECTRICITY / xth Revised Sheet No. xx / (Canceling xth Revised Sheet No. xx)", the title "RATE BEST / BASIC ELECTRIC SERVICE TIME OF USE PRICING", and the footer "Filed with the Illinois Commerce Commission on XXX YY, 2025. Issued pursuant to the Illinois Commerce Commission Order on Rehearing dated XXX YY, 2025, in Docket No. 24-0378. / Date Effective: XXX YY, 2025 / Issued by David R Perez, EVP and COO / Post Office Box 805379, Chicago, Illinois 60680-5379 / Asterisk (\*) indicates change."
- **Change markers**: every sheet carries a single asterisk in the left margin beside the title block (the entire draft is new/changed, so no paragraph-level change markers are used). Not reproduced per page.
- Page markers `[p. N]` give the PDF page (one tariff sheet per page). Section headings are printed in the source in capitals; kept.
- Dollar signs in units are escaped as `\$`. The source contains no data tables or diagrams; it contains three display formulas (Formula 1, Formula 2 on p. 7; the MCC equation on p. 9; the TPEA equation on p. 13), transcribed as LaTeX.
- Underscores/subscripts: the source writes subscripts as small text such as "HENC P S or N"; transcribed as $\mathrm{HENC}_{P,\,S\text{ or }N}$ where $P$ = period (Morning, Mid-Day Peak, Evening, Overnight) and $S$/$N$ = summer / nonsummer.

---

[p. 1] _(Continued on Sheet No. x+1)_

## APPLICABILITY.

Retail customers may begin taking service under this tariff beginning with the June 2026 monthly billing period.

This tariff is available to residential retail customers for which (a) the Company will be providing bundled electric service, (b) service is not taken under Service Classifications NM1, NM2, NM3, or NM4 of Rider POGNM – Parallel Operation of Retail Customer Generating Facilities with Net Metering (Rider POGNM), or Rider NAM – Non AMI Metering (Rider NAM), (c) successfully enrolls for service under this tariff using the enrollment process established by the Company, and (d) advanced metering infrastructure (AMI) meter capable of providing interval usage is installed.

## PURPOSE.

<!-- EPON: goal,ev-hp,midday-peak — stated purposes: shift use away from high-price wholesale periods and from distribution/transmission peaks; purpose (c) explicitly encourages EV charging in early-morning hours -->

The purpose of this tariff is to provide retail customers with a supply rate option that (a) encourages less electricity usage, or a shift in electricity usage, from periods when electricity prices are typically higher in the hourly wholesale electricity market, (b) encourages less electricity use during the periods when the distribution and transmission systems incur their peak demands, (c) encourages electric vehicle owners to charge their electric vehicles in the early morning hours when hourly wholesale electricity prices are typically lower, and (d) increases customers' satisfaction with their electric service with a new supply rate option.

---

[p. 2] _(Continued from Sheet No. x; Continued on Sheet No. x+2)_

## DEFINITIONS.

Generally, definitions of terms used in this tariff are provided in the Definitions part of the General Terms and Conditions of the Company's Schedule of Rates. The following acronyms and terms are defined for use in this tariff:

**Basic Electric Service Time of Use Pricing (BEST)**
Basic Electric Service Time of Use Pricing means the residential electric supply rate provided under the provisions of this tariff.

**BEST Purchased Electricity Adjustment Factor**
BEST Purchased Electricity Adjustment Factor (TPEA) means a unit credit or charge that, through its application, periodically equalizes applicable revenues from retail customers taking service hereunder for electric power and energy procured for them by the Company and the expenses incurred by the Company related to the procurement of such electric power and energy, thereby ensuring that the Company does not over or under recover its costs related to the procurement of electric power and energy for its retail customers.

**Capacity Costs**
Capacity costs means capacity obligation costs incurred by the Company to procure electric power and energy directly from PJM-administered markets for customers receiving service hereunder.

**Capacity Obligation**
Capacity Obligation means the retail customer's share, in kilowatts (kW), of the annual peak electric load assigned to the Company by PJM Interconnection, L.L.C. (PJM). The Capacity Obligation for a retail customer is determined by the Company based on the retail customer's Peak Load Contribution (PLC) and PJM's Reliability Pricing Model methodology.

**Evening Period**
Evening Period is the period where energy is measured for billing purposes every day from 7:00 p.m. to 9:00 p.m. CPT.

**Evening Period Electricity Charge**
Evening Period Electricity Charge (EPEC) means an electric supply service unit price applicable to energy provided to a retail customer during the Evening Period. There are Summer and Nonsummer EPECs for the Summer and Nonsummer Periods defined in the Definitions part of General Terms and Conditions of the Company's Schedule of Rates.

<!-- EPON: midday-peak,stacking — Mid-Day Peak Period defined as every day 1:00 p.m.–7:00 p.m. CPT (same window used for the DTOU delivery charge, see Distribution Facilities Charges on p. 6); separate summer and nonsummer MDPPECs -->

**Mid-Day Peak Period**
Mid-Day Peak Period is the period where energy is measured for billing purposes every day from 1:00 p.m. to 7:00 p.m. CPT.

**Mid-Day Peak Period Electricity Charge**
Mid-Day Peak Period Electricity Charge (MDPPEC) means an electric supply service unit price applicable to energy provided to a retail customer during the Mid-Day Peak Period. There are Summer and Nonsummer MDPPECs for the Summer and Nonsummer Periods defined in the Definitions part of General Terms and Conditions of the Company's Schedule of Rates.

---

[p. 3] _(Continued from Sheet No. x+1; Continued on Sheet No. x+3)_

## DEFINITIONS (CONTINUED).

<!-- EPON: capacity-mdppec — strawman recovers capacity through a kW-based Monthly Capacity Charge (MCC) on the customer's PJM capacity obligation, not in Mid-Day Peak kWh -->

**Monthly Capacity Charge**
Monthly Capacity Charge (MCC) means a kW-based electric supply service unit price that, through its application, allows the Company to recover certain costs incurred by the Company related to the demand for electric power and energy procured directly from PJM-administered markets for retail customers receiving service hereunder.

**Morning Period**
Morning Period is the period where energy is measured for billing purposes every day from 6:00 a.m. to 1:00 p.m. CPT.

**Morning Period Electricity Charge**
Morning Period Electricity Charge (MPEC) means an electric supply service unit price applicable to energy provided to a retail customer during the Morning Period. There are Summer and Nonsummer MPECs for the Summer and Nonsummer Periods as defined in the Definitions part of General Terms and Conditions of the Company's Schedule of Rates.

**NITS**
NITS means Network Integration Transmission Service.

<!-- EPON: tmc,capacity-mdppec — NSPLC (network service peak load contribution, kW) is the billing determinant for the kW-based transmission/PJM services charge -->

**NSPLC**
NSPLC means network service peak load contribution, in kW. The retail customer's NSPLC is determined by the Company for the period of twelve (12) consecutive monthly billing periods beginning with the applicable January monthly billing period and extending through the following December monthly billing period. For a situation in which insufficient historical electric power and energy consumption data exist for a retail customer, the Company determines such retail customer's NSPLC based upon the Company's judgment and knowledge of the retail customer's electric power and energy requirements and contribution to such peak demand for electricity on the ComEd Zone.

**Overnight Period**
Overnight Period is the period where energy is measured for billing purposes every day from 9:00 p.m. to 6:00 a.m. Central Prevailing Time (CPT).

**Overnight Period Electricity Charge**
Overnight Period Electricity Charge (OPEC) means an electric supply service unit price applicable to energy provided to a retail customer during the Overnight Period. There are Summer and Nonsummer OPECs for the Summer and Nonsummer Periods as defined in the Definitions part of General Terms and Conditions of the Company's Schedule of Rates.

---

[p. 4] _(Continued from Sheet No. x+2; Continued on Sheet No. x+4)_

## DEFINITIONS (CONTINUED).

<!-- EPON: tmc — PJM Services and Misc. Procurement Components Charge has two parts: a kW-based unit price and a separate kWh-based unit price -->

**PJM Services and Miscellaneous Procurement Components Charge**
PJM Services and Miscellaneous Procurement Components Charge is comprised of two separate components: a kW-based unit price and a separate kWh-based unit price, that, through their application, allow the Company to recover from retail customers applicable costs the Company incurs for transmission service and in procuring certain services from PJM Interconnection L.L.C. (PJM)-administered markets, including but not limited to, NITS and other PJM-associated expenses in accordance with applicable tariffs on file with the Federal Energy Regulatory Commission (FERC) and also other costs that are not recovered through the application of the Electricity Charges and Monthly Capacity Charges.

**PLC**
PLC means peak load contribution, in kW. The retail customer's PLC is determined by the Company based on PJM's Reliability Pricing Model methodology for a period of twelve (12) monthly billing periods beginning with the June monthly billing period and extending through the following May monthly billing period. For a situation in which insufficient historical electric power and energy consumption data exist for a retail customer, the Company determines such retail customer's PLC based upon, in the Company's judgment, the retail customer's expected electric power and energy requirements and its expected contribution to such peak electric load on the PJM electric system region.

## PREREQUISITES OF SERVICE.

For a situation in which a retail customer requests service hereunder, capable AMI meter-related facilities must be installed at such retail customer's premises prior to commencement of service hereunder.

For a situation in which a retail customer requesting service hereunder is currently receiving service from the Company under a different tariff, such retail customer must fulfill all obligations, except timely payment for service, for which it is responsible under such other tariff prior to terminating service under such other tariff and commencing service hereunder.

A retail customer enrolling in service hereunder must successfully enroll for service under this tariff using the enrollment process established by the Company.

---

[p. 5] _(Continued from Sheet No. x+3; Continued on Sheet No. x+5)_

## NATURE OF SERVICE.

### Bundled Electric Service

<!-- EPON: bundling,stacking — supply TOU is only available bundled with ComEd delivery under DTOU; no component may be provided by a third party or separately -->

Bundled electric service provided to retail customers receiving service with time of use pricing satisfies the Company's requirements to provide bundled electric power and energy service in accordance with the terms of this Bundled Electric Service subsection. Such provision includes (1) direct procurement through PJM-administered markets of all the component services the Company requires to meet retail customer instantaneous electric power and energy requirements at any given time under the Company's tariffs, applicable tariffs on file with the FERC, and other applicable laws, including, without limitation, all required electric energy, energy to satisfy losses, electric generation capacity, volumetric risk management, transmission services, ancillary transmission services, administrative services, and other necessary services procured by the Company; (2) delivery of the electric power and energy via the Company's distribution facilities, including the provision of reactive power and voltage support using distribution facilities, provided under time of use differentiated Distribution Facilities Charges (Distribution Time Of Use Pricing – DTOU) rates and subject to the terms, conditions, and limitations provided for in the Company's tariffs on file with the Illinois Commerce Commission (ICC); and (3) the Company's standard metering and billing that are necessary to permit retail customers to receive service hereunder as permitted by law and by tariffs approved by the ICC and the FERC. No component of bundled electric service may be provided to a retail customer by a third party, and components of this bundled electric service are not available separately from the Company under this tariff.

### Electrical Characteristics of Service

The electrical characteristics of the bundled electric service provided to a retail customer served hereunder are comparable to the electrical characteristics of the electric power and energy provided or delivered to other retail customers taking service under other tariffs included in the Company's Schedule of Rates. Such characteristics are described in the Electrical Characteristics section of the Nature of Service part of the General Terms and Conditions of the Company's Schedule of Rates.

### Service and Facilities

Standard service and distribution and meter-related facilities provided by the Company for a retail customer served hereunder are determined in accordance with the provisions of the General Terms and Conditions and other applicable tariffs in the Company's Schedule of Rates.

In the provision of electric service hereunder, the Company furnishes, installs, owns, operates, replaces, and maintains meter-related facilities associated with capable AMI metering adequate to measure the kilowatt-hours (kWhs) delivered to the retail customer and the rate at which such electricity is delivered to such retail customer in each half hour in the monthly billing period. To the extent that such meter-related facilities are larger, more, or different from facilities provided in a standard metering installation, such meter-related facilities are provided in accordance with the provisions for providing nonstandard services and facilities.

---

[p. 6] _(Continued from Sheet No. x+4; Continued on Sheet No. x+6)_

## NATURE OF SERVICE (CONTINUED).

### Service and Facilities (Continued)

Notwithstanding the preceding provisions of this Service and Facilities subsection, if larger, more, or different services or distribution or meter-related facilities than those needed to provide standard electric service to the retail customer are in place, required or requested by the retail customer, and such services or facilities are reasonably and technically feasible, and can be furnished, installed, operated, replaced, and maintained with no significant adverse impact on the Company's system with respect to reliability or efficiency, such services or facilities are furnished, installed, owned, operated, replaced, and maintained by the Company, provided the Company is allowed to recover from the retail customer the costs of furnishing, installing, owning, operating, replacing, and maintaining such services or facilities in accordance with its provisions for providing nonstandard services and facilities in the Company's Schedule of Rates, including but not limited to the provisions of the General Terms and Conditions, Rider DE - Distribution System Extensions (Rider DE), Rider NS - Nonstandard Services and Facilities (Rider NS), and Rider ML - Meter-Related Facilities Lease (Rider ML).

For a situation in which the Company relocates or removes Company facilities in accordance with a retail customer's requirements or request, such relocation or removal is performed in accordance with the provisions for providing nonstandard services and facilities, as applicable.

## MONTHLY CHARGES.

A retail customer served hereunder is subject to each charge described in this Monthly Charges section for each monthly billing period.

### Customer Charge

<!-- EPON: fixed-vs-volumetric — fixed customer charge is the delivery-class customer charge from the Delivery Service Charges Informational Sheets -->

The Customer Charge is applicable to the retail customer for the monthly billing period and is equal to the applicable Customer Charge listed in the Delivery Service Charges Informational Sheets of the Company's Schedule of Rates for the delivery class applicable to the retail customer for the monthly billing period.

### Standard Metering Service Charge

The Standard Metering Service Charge is applicable to the retail customer for the monthly billing period and is equal to the applicable Standard Metering Service Charge listed in the Delivery Service Charges Informational Sheets of the Company's Schedule of Rates for the delivery class applicable to the retail customer for the monthly billing period.

### Distribution Facilities Charges

<!-- EPON: stacking,midday-peak — delivery (DFC) charges use the same four TOU periods as the supply charges: Morning 6am–1pm, Mid-Day Peak 1pm–7pm, Evening 7pm–9pm, Overnight 9pm–6am; both delivery and supply peak prices apply to the 1–7 p.m. window -->

The Distribution Facilities Charges are provided on a \$/kWh basis and differentiated by four TOU periods (shown in Central Prevailing Time, CPT): the Morning Period from 6:00 a.m. to 1:00 p.m., the Mid-Day Peak Period from 1:00 p.m. to 7:00 p.m., the Evening Period from 7:00 p.m. to 9:00 p.m., and the Overnight Period from 9:00 p.m. to 6:00 a.m. of the subsequent day. The TOU Distribution Facilities Charges are listed in the Time of Use Distribution Facilities Charges Informational Sheets of the Company's Schedule of Rates for the delivery class applicable to such residential retail customer for the monthly billing period. Each TOU Distribution Facilities Charge for the monthly billing period is applicable to the kWhs provided to the residential retail customer during the corresponding TOU period of the monthly billing period.

---

[p. 7] _(Continued from Sheet No. x+5; Continued on Sheet No. x+7)_

## MONTHLY CHARGES (CONTINUED).

### Illinois Electricity Distribution Tax Charge

The Illinois Electricity Distribution Tax Charge (IEDT) provided on a \$/kWh basis is applicable to the kWhs provided to the retail customer during the monthly billing period and is equal to the applicable IEDT listed in the Delivery Service Charges Informational Sheets of the Company's Schedule of Rates for the delivery class applicable to the retail customer for the monthly billing period.

### Electricity Charges

Each year after the initial implementation of the Electricity Charges, the Electricity Charges are updated and will be applicable beginning with that year's June monthly billing period and extending through the following May monthly billing period. Notwithstanding such periodic update, the Electricity Charges may be revised by the Company if the Company determines such revision results in a better match between the Company's applicable expected costs and its recovery of those costs.

<!-- EPON: profile,midday-peak — core design: Formula 1 prices each period using historical PJM RT residual LMPs weighted by the "participants' aggregate illustrative profile" (hourly kW) and distribution losses, separately for summer and nonsummer; the same aggregate profile sets all period charges for every customer -->

Electricity Charges are applicable to each kWh provided to the retail customer during the corresponding Morning Period, Mid-Day Peak Period, Evening Period or Overnight Period in the summer or nonsummer monthly billing period for which such charge is determined. Each such summer and nonsummer MPEC, MDPPEC, EPEC and OPEC is determined in the following two steps and formulas: (1) the first step, Formula 1, determines the residential energy charge per kWh that would have been recovered with the historical PJM real time residual locational marginal prices for the ComEd Zone and distribution losses for the participants' aggregate illustrative profile for each of the summer and nonsummer price periods, and (2) the second step, Formula 2, takes the corresponding per kWh energy charges and adds any associated per kWh adjustments to make the charges reflective of current or future market prices for each period, converts the charges to cents/kWh and applies the uncollectible factors to determine the resultant charge:

**Formula 1:**

$$
\mathrm{HENC}_{P,\,S\text{ or }N} \;=\; \left(\sum_{\text{Start Hour}}^{\text{End Hour}}\left[\,\mathrm{HkW}\times\mathrm{HLMP}\,\right]\times\frac{1\ \mathrm{MWh}}{1{,}000\ \mathrm{kWh}}\times\left(1+\mathrm{DLF}\right)\right)\Big/\ \mathrm{kWh}_{P,\,S\text{ or }N}
$$

**Formula 2:**

$$
\mathrm{EC}_{P,\,S\text{ or }N} \;=\; \left(\mathrm{HENC}_{P,\,S\text{ or }N} + \mathrm{A}_{P,\,S\text{ or }N}\right)\times 100\,¢/\$ \times \mathrm{SBUF}\times\mathrm{ISUF}
$$

---

[p. 8] _(Continued from Sheet No. x+6; Continued on Sheet No. x+8)_

## MONTHLY CHARGES (CONTINUED).

### Electricity Charges (Continued)

Where:

| Term                                |   | Definition                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------------- | - | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| $\mathrm{HENC}_{P,\,S\text{ or }N}$ | = | Historical Energy Charge, in \$/kWh, is the computed charge using the corresponding HkW and HLMP for each period (P), where P is the summer or nonsummer Morning, Mid-Day Peak, Evening or Overnight Period, and S or N is the corresponding summer or nonsummer charge for specific charges, adjusted for the corresponding DLF and divided by the total corresponding kWh for each period. |
| HkW                                 | = | Historical kilowatt (kW), in kW, is the historical hourly interval kW demand data for the participants' aggregate illustrative profile for each period P.                                                                                                                                                                                                                                    |
| HLMP                                | = | The historical PJM real time hourly residual locational marginal price for the ComEd Zone, in \$/MWh, for each hourly interval for each period P.                                                                                                                                                                                                                                            |
| DLF                                 | = | Distribution Loss Factor, in decimal format, to adjust for losses on the distribution system located in the Company's service territory and equal to the computed participants average DLF using DLFs in Informational Sheet No. 33.                                                                                                                                                         |
| $\mathrm{EC}_{P,\,S\text{ or }N}$   | = | Electricity Charge, in Cents/kWh, applied to each kWh provided to the retail customer during the corresponding summer or nonsummer period P for which such charge is determined.                                                                                                                                                                                                             |
| $\mathrm{E}_{P}$                    | = | Energy, in kWh, equal to the energy from the participants' aggregate illustrative hourly interval profile for each corresponding period P for which such charge is determined.                                                                                                                                                                                                               |
| SBUF                                | = | Base Uncollectible Cost Factor, in decimal format, equal to the residential Supply BUF (SBUFR) listed in or determined in accordance with the provisions of Rider UF - Uncollectible Factors (Rider UF), as applicable.                                                                                                                                                                      |

[source note: the term list prints "EP" for energy, where Formula 1 divides by the total kWh for each period and does not itself contain an $E_P$ symbol; Formula 2 prints the adjustment term as "A" with subscript P S or N while the definition (p. 9) defines "A" without subscripts. Both are preserved as printed.]

---

[p. 9] _(Continued from Sheet No. x+7; Continued on Sheet No. x+9)_

## MONTHLY CHARGES (CONTINUED).

### Electricity Charges (Continued)

| Term |   | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---- | - | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ISUF | = | Incremental Supply Uncollectible Cost Factor, in decimal format, equal to ISUFR determined in accordance with the provisions of Rider UF.                                                                                                                                                                                                                                                                                                                                                                                                                 |
| A    | = | Adjustments, in \$/kWh, to raise or lower the corresponding EC for over or under collections from the application of the TPEA or other Commission approved changes that allow for raising or lowering the EC to more accurately recover all of the supply related costs. Costs related to the recovery of the TPEA may include a cumulative balance of deferrals associated with the computation of previous TPEA factors existing at the end of the most recent month for which applicable data are available prior to the date such ECs are determined. |

### Capacity Charge

<!-- EPON: capacity-mdppec — capacity cost recovered through a kW-based Monthly Capacity Charge (MCC) = PJM Net Load Price converted to $/kW-month, applied to the customer's Capacity Obligation (PLC-based); not embedded in the Mid-Day Peak kWh price in this strawman -->

The Company determines capacity charges in a manner that recovers the capacity obligation costs incurred by the Company to procure electric power and energy directly from PJM-administered markets for retail customers receiving service under Rate BEST. Such capacity charges equal the applicable PJM Net Load Price (NLP), in \$/MW-Day, for the PJM Planning Year, adjusted by uncollectible factors, and are applicable for the period that extends from the beginning of the June monthly billing period through the end of the following May monthly billing period corresponding to such PJM Planning Year.

The Monthly Capacity Charge (MCC) is applicable to the Capacity Obligation, as defined in the Definitions part of General Terms and Conditions, established by the retail customer for the monthly billing period. Such MCC is determined in accordance with the following equation:

**MCC equation:**

$$
\mathrm{MCC} \;=\; \mathrm{NLP}\times\frac{1\ \mathrm{MW}}{1{,}000\ \mathrm{kW}}\times\frac{365\ \mathrm{Days}}{12\ \mathrm{Months}}\times\mathrm{BUF}\times\mathrm{ISUF}
$$

Where:

| Term |   | Definition                                                                                                                                                                                                              |
| ---- | - | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MCC  | = | Monthly Capacity Charge, in \$/kW-Month, applied to the Capacity Obligation established by the retail customer for the monthly billing period.                                                                          |
| NLP  | = | Applicable PJM Net Load Price, in \$/MW-Day, for the period of time corresponding to the monthly billing periods during which the MCC is applied.                                                                       |
| BUF  | = | Base Uncollectible Cost Factor, in decimal format, equal to the residential Supply BUF (SBUFR) listed in or determined in accordance with the provisions of Rider UF - Uncollectible Factors (Rider UF), as applicable. |
| ISUF | = | Incremental Supply Uncollectible Cost Factor, in decimal format, equal to the residential ISUFR determined in accordance with the provisions of Rider UF.                                                               |

---

[p. 10] _(Continued from Sheet No. x+7 [as printed]; Continued on Sheet No. x+9 [as printed])_

Notwithstanding the preceding provisions for the computation of MCC, for computations that pertain to leap years, the number of days in the year is 366 rather than 365.

### PJM Services and Miscellaneous Procurement Components kW Charge

<!-- EPON: tmc,capacity-mdppec — kW-based transmission (NITS) and misc. PJM charge billed on NSPLC, shown as "Trans & Misc Component kW Charge"; at-cost, no mark-up -->

The Company determines kW-based PJM Services and Miscellaneous Procurement Components Charges in a manner that allows the Company to recover from retail customers receiving electric service under Rate BEST the costs it incurs in procuring certain services from PJM, including but not limited to, NITS and other kW-based PJM-associated expenses incurred in accordance with applicable tariffs on file with the FERC, and other applicable law. The Company is not allowed to mark-up or include a return on such costs. The PJM Services and Miscellaneous Procurement Components kW Charge is applicable to the NSPLC established by the retail customer for the monthly billing period. The PJM Services and Miscellaneous Procurement Components kW Charge is shown as a separate line item on the retail customer's monthly bill for electric service and designated as the Transmission and Miscellaneous Procurement Components kW Charge (Trans & Misc Component kW Charge).

The PJM Services and Miscellaneous Procurement Components kW Charge is determined by the Company each year and is generally applicable for the period that extends from the beginning of the June monthly billing period through the end of the following May monthly billing period. Included in the determination of the PJM Services and Miscellaneous Procurement Components kW Charge are applicable system losses, base uncollectible costs, and incremental uncollectible costs incurred by the Company.

Notwithstanding the previous provisions of this PJM Services and Miscellaneous Procurement Components kW Charge subsection, in the event that the Company (a) recomputes the PJM Services Price (PSP) and revises the Retail PJM Services Charge in accordance with the provisions of Rider PE or (b) revises base uncollectible costs or incremental uncollectible costs included in the determination of the PJM Services Charge, then the PJM Services and Miscellaneous Procurement Components kW Charge must be correspondingly revised.

---

[p. 11] _(Continued from Sheet No. x+8; Continued on Sheet No. x+10)_

## MONTHLY CHARGES (CONTINUED).

### PJM Services and Miscellaneous Procurement Components kWh Charge

<!-- EPON: tmc — kWh-based TMC recovers PJM costs not recovered through Electricity Charges or the kW charge (ancillary expenses, uncollectibles, customer-service, collection, working capital, procurement costs), applied to every kWh regardless of period -->

The kWh-based PJM Services and Miscellaneous Procurement Components is applicable to each kWh provided to the retail customer during the monthly billing period. The Company determines a PJM Services and Miscellaneous Procurement Components kWh Charge in a manner that allows the Company to recover the costs it incurs related to the procurement of electric power and energy directly from PJM-administered markets for retail customers receiving electric service under Rate BEST which are not recovered through the application of the Electricity Charges and the PJM Services and Miscellaneous Procurement Components kW Charge.

The PJM Services and Miscellaneous Procurement Components kWh Charge is determined by the Company each year and is generally applicable for the period that extends from the beginning of the June monthly billing period through the end of the following May monthly billing period. The following costs expected to be incurred by the Company may be included in the determination of the PJM Services and Miscellaneous Procurement Components kWh Charge:

- (a) kWh-based PJM Transmission Ancillary Expenses and credits;
- (b) base and incremental uncollectible costs;
- (c) customer service related costs allocated to only retail customers taking service hereunder in accordance with the ICC's order in the Company's most recent general rate case in accordance with Article IX or Section 16-108.18 of the Act as applicable;
- (d) collection agency costs allocated to only retail customers taking service hereunder in accordance with the ICC's order in the Company's most recent general rate case in accordance with Article IX or Section 16-108.18 of the Act, as applicable;
- (e) costs of working capital used to arrange or procure electric power and energy directly from PJM-administered markets, with such costs determined in a manner consistent with the methodology used to determine costs of working capital approved by the ICC in its order in the Company's most recent general rate case in accordance with Article IX or Section 16-108.18 of the Act, or as otherwise provided by law, as applicable; and

_(item (f) continues on the next sheet)_

---

[p. 12] _(Continued from Sheet No. x+9; Continued on Sheet No. x+11)_

## MONTHLY CHARGES (CONTINUED).

### PJM Services and Miscellaneous Procurement Components kWh Charge (Continued)

- (f) costs associated with arranging or procuring electric power and energy directly from PJM-administered markets, which are identified through the use of a wages and salaries allocator calculated as initially directed by the ICC in its Order in Docket No. 11-0721, dated May 29, 2012, with any subsequent value of such allocator as approved by the ICC in its order in the Company's most recent general rate case in accordance with Article IX or Section 16-108.18 of the Act, or as otherwise provided by law, as applicable, and taking into account reconciliation adjustments made in accordance with Section 16-108.5(d) of the Act, as applicable, whereby such costs are equal to the portion of the Company's overall costs to which such allocator is applied that are (i) not recovered through the application of delivery service charges, (ii) not recovered through the application of the PJM Services and Miscellaneous Procurement Components kW Charge determined in accordance with the PJM Services and Miscellaneous Procurement Components kW Charge subsection of this Monthly Charges section, and (iii) not costs incurred by the Company in association with arranging and providing for the supply of electric power and energy in accordance with the Procurement Obligations section of Rider PE or the Monthly Charges section of Rate BESH.

Including costs of working capital in the determination of the PJM Services and Miscellaneous Procurement Components kWh Charge provides for the recovery of costs the Company incurs for working capital used to arrange or procure electric power and energy supply directly from PJM-administered markets, such as the funds required to finance the lag between the purchase of electric power and energy supply resources and the recovery of the costs of such resources from retail customers. Such costs are determined in a manner consistent with the methodology used to determine costs of working capital approved by the ICC in its order in the Company's most recent general rate case in accordance with Article IX or Section 16-108.18 of the Act, or as otherwise provided by law, as applicable. Such methodology is applied using a cost of capital equal to that established by the ICC in its order in such most recent case or as otherwise provided by law, as applicable. All other data, including applicable leads and lags, are updated annually to reflect current electric power and energy supply procurement working capital costs. Company representatives must review such calculated costs with personnel from the Accounting Department of the ICC Staff in accordance with the provisions of the Reporting and Annual Audit section of this tariff. A cost of capital established by the ICC in its order in such most recent case or as otherwise provided by law, as applicable, is applied in determining the costs of working capital component of the PJM Services and Miscellaneous Procurement Components kWh Charge only for PJM Services and Miscellaneous Procurement Components kWh Charges that become applicable after the date of such order or law, as applicable.

---

[p. 13] _(Continued from Sheet No. x+10; Continued on Sheet No. x+12)_

## MONTHLY CHARGES (CONTINUED).

### PJM Services and Miscellaneous Procurement Components kWh Charge (Continued)

Applicable system losses are reflected in the determination of the PJM Services and Miscellaneous Procurement Components kWh Charge. Notwithstanding the previous provisions of this PJM Services and Miscellaneous Procurement Components kWh Charge subsection, the PJM Services and Miscellaneous Procurement Components kWh Charge must be recomputed in accordance with directives in ICC orders in Company's most recent general rate case in accordance with Article IX or Section 16-108.18 of the Act, or as otherwise provided by law, as applicable. Moreover, the PJM Services and Miscellaneous Procurement Components kWh Charge must be recomputed in the event that the Company revises base uncollectible costs or incremental uncollectible costs included in the determination of the PJM Services and Miscellaneous Procurement Components kWh Charge. In the event that the Company revises the PJM Services and Miscellaneous Procurement Components kWh Charge in accordance with the provisions in the PJM Services and Miscellaneous Procurement Components kWh Charge subsection of this Monthly Charges section, or at such time that FERC approved or accepted changes in charges related to costs recovered through the application of the PJM Services and Miscellaneous Procurement Components kWh Charge become effective, the PJM Services and Miscellaneous Procurement Components kWh Charge for service under this tariff may be required to be correspondingly revised.

The PJM Services and Miscellaneous Procurement Components kWh Charge is shown as a separate line item on the retail customer's monthly bill for electric service and designated as the Transmission and Miscellaneous Components kWh Charge (Trans & Misc Component kWh Charge).

### BEST Purchased Electricity Adjustment Factor

The BEST Purchased Electricity Adjustment Factor (TPEA) periodically equalizes the revenues from retail customers receiving electric service under this tariff for electric power and energy procured for them by the Company and the expenses incurred by the Company related to the procurement of such electric power and energy as provided in this Monthly Charges section.

A TPEA, in ¢/kWh rounded to the thousandths of a cent, is determined and applied to each kWh provided to the retail customer during a given effective period. The TPEA is shown as a separate line item on the retail customer's monthly bill for electric service and designated as the Purchased Electricity Adjustment. The TPEA is determined and applied in such effective period in accordance with the following equation:

**TPEA equation:**

$$
\mathrm{TPEA} \;=\; \frac{\left[\mathrm{AE}-\mathrm{AR}+\mathrm{AB}+\mathrm{A}\right]_{\text{amortized}} + \sum \mathrm{ATPEA}}{\mathrm{U}}\times\frac{100\,¢}{\$1}
$$

Where:

| Term |   | Definition                                                                                                                                                                                                                                |
| ---- | - | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TPEA | = | BEST Purchased Electricity Adjustment Factor, in ¢/kWh rounded to the thousandths of a cent, applied as a credit or charge to kWhs provided to retail customers receiving electric service under this tariff during the effective period. |

_(definitions of the remaining terms continue on the next sheet)_

---

[p. 14] _(Continued from Sheet No. x+11; Continued on Sheet No. x+13)_

## MONTHLY CHARGES (CONTINUED).

### BEST Purchased Electricity Adjustment Factor (Continued)

| Term          |   | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------- | - | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AE            | = | Accrued Expenses, in \$, equal to the sum of all the accrued net expenses incurred by the Company related to the direct procurement of electric power and energy from PJM-administered markets for retail customers receiving service hereunder during the determination period(s). Accrued Expenses may reflect the amortization of certain expenses, such as legal and consultative fees associated with the procurement of electric power and energy and ICC proceedings concerning the procurement of electric power and energy, over multiple determination periods.                                                                                                                                                                                                                  |
| AR            | = | Accrued Revenues, in \$, equal to the accrued net revenues recognized for retail customers receiving service hereunder during the determination period(s) through the application of the Energy Charges, PJM Services and Miscellaneous Procurement Components kW Charge and kWh Charge, and Monthly Capacity Charge, as applicable. Accrued Revenues may reflect the amortization of certain revenues over multiple determination periods.                                                                                                                                                                                                                                                                                                                                                |
| AB            | = | Automatic Balancing Factor, in \$, equal to the cumulative debit or credit balance resulting from the application of the TPEA through the determination period(s). Such balance includes interest at the rate established by the ICC in accordance with 83 Illinois Administrative Code Section 280.40(g).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| A             | = | Adjustment, in \$, equal to an amount (a) ordered by the ICC, or (b) determined by the Company, that is to be refunded to or collected from retail customers receiving electric service under Rate BEST to correct for errors associated with the computation of a previously applied TPEA in accordance with this tariff. Such amount includes interest at the rate established by the ICC in accordance with 83 Illinois Administrative Code Section 280.40(g). Such interest is calculated for the period of time beginning on the first day of the effective period during which such TPEA was applied and extending through the day prior to the start of the effective period in which the A is applied. Such amount may be amortized over multiple effective periods with interest. |
| [ ] amortized | = | Amortization of the quantity included in the brackets, as necessary, for a period not to exceed twelve (12) effective monthly billing periods. For a situation in which amortization is not necessary, there is no amortization period.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ATPEA         | = | Amortized BEST Purchased Electricity Adjustment Amount, in \$, equal to a previously amortized quantity (AE - AR + AB + A). Each such TPEA includes interest at the rate established by the ICC in accordance with 83 Illinois Administrative Code Section 280.40(g), and such interest is calculated for an amortization period not to exceed twelve (12) effective periods, beginning on the first day of the effective period during which such TPEA is applied and extending through the day prior to the start of the last effective period during which such TPEA is applied. Each such TPEA is applied only during effective periods that correspond to such TPEA's amortization period.                                                                                            |

---

[p. 15] _(Continued from Sheet No. x+12; Continued on Sheet No. x+14)_

## MONTHLY CHARGES (CONTINUED).

### BEST Purchased Electricity Adjustment Factor (Continued)

| Term |   | Definition                                                                                                                             |
| ---- | - | -------------------------------------------------------------------------------------------------------------------------------------- |
| U    | = | Usage, in kWh, forecasted to be provided to retail customers receiving electric service under this tariff during the effective period. |

For the purpose of determining the TPEA, (a) a determination period means the calendar month for which a TPEA is determined for retail customers receiving electric service under Rate BEST, and (b) an effective period means the monthly billing period during which such TPEA is applied to kWhs provided to such retail customers. The effective period is the first monthly billing period beginning no earlier than fifteen (15) calendar days after the final reconciliation of the PJM-conducted settlement process for electric supply for the determination period(s).

### Nonstandard Services and Facilities Charge

If the Company provides services or distribution facilities for the retail customer served hereunder that are different from or in addition to a standard service or distribution facilities installation, certain of such services or distribution facilities are provided and charged for through a monthly amount applicable to such retail customer for the monthly billing period and computed in accordance with the provisions of Rider NS.

### Nonstandard Meter-Related Facilities Charge

If the Company provides meter-related facilities to the retail customer served hereunder that are different from or in addition to facilities included in a standard metering installation, such meter-related facilities are provided and charged for through a rental amount applicable to such retail customer for the monthly billing period and computed in accordance with the provisions of Rider ML.

### Other Generally Applicable Charges

The Company's Schedule of Rates of which this tariff is a part includes General Terms and Conditions and riders that include other generally applicable charges. Service hereunder is subject to such General Terms and Conditions, riders, and other generally applicable charges.

Notwithstanding the previous provisions for the calculation of the Energy Charges, PJM Services and Miscellaneous Procurement Components kW Charge and kWh Charge, Monthly Capacity Charge, and TPEA, certain costs related to the administration, legal, mandated adjustments or other project costs along with cash working capital expense for the procurement of these supply charges may be allocated with the corresponding charges developed in Rate BESH based upon the energy provided under each rate or other equitable methodology. Furthermore, the costs recovered with these charges will not also be recovered through the application of similar charges in Rate BES, Rate BESH or other supply charges collected by the Company.

---

[p. 16] _(Continued from Sheet No. x+13; Continued on Sheet No. x+15)_

## OTHER CHARGES.

### Late Payment Charge

The Late Payment Charge as described in the Billing and Payment part of the General Terms and Conditions of the Company's Schedule of Rates is applicable to all charges applied in accordance with the provisions of this tariff.

## MEASUREMENT OF POWER AND ENERGY PROVIDED.

Electric power and energy provided to a retail customer served hereunder are measured in accordance with the provisions of the Measurement of Energy and Demand subsection of the Continuing Electric Service section of the Billing and Payment part of the General Terms and Conditions of the Company's Schedule of Rates. However, if a customer has unmetered fixtures receiving service under the Fixture-included Lighting Delivery Class, the kWhs delivered during the monthly billing period are determined using the Company's standard practice for such lighting fixtures.

## TERM OF SERVICE.

<!-- EPON: lockout — enrollment through the Company's enrollment process; prerequisites must be satisfied before service commences -->

For a retail customer requesting service hereunder, such service does not commence until the retail customer fulfills all applicable prerequisites of service provided in the General Terms and Conditions of the Company's Schedule of Rates and the retail customer fulfills all applicable prerequisites of service provided in the Prerequisites of Service section of this tariff. The customer must successfully enroll for service under this tariff using the enrollment process established by the Company.

<!-- EPON: lockout — 12-billing-period re-enrollment lockout after terminating service under Rate BEST -->

Following a termination of service hereunder, such residential retail customer is not eligible to receive service hereunder for a period of at least twelve (12) monthly billing periods following the billing period of such termination.

A retail customer's term of service hereunder commences when the Company begins to provide service hereunder.

---

[p. 17] _(Continued from Sheet No. x+14; Continued on Sheet No. x+16)_

## TERM OF SERVICE (CONTINUED).

Notwithstanding the provisions of the previous paragraphs, to terminate service hereunder and elect service under another tariff, the customer must follow the enrollment requirements of the other tariff, as applicable.

Otherwise, in the event that (a) the retail customer terminates service from the Company under this tariff and (b) does not elect to obtain service from the Company under any other tariffed service at its premises due to the fact that such retail customer is vacating the premises, the Company has the option of discontinuing electric service at the premises if a successor customer does not provide an application at such premises.

## INFORMATIONAL FILINGS.

PJM Services and Miscellaneous Procurement Components kW Charge, PJM Services and Miscellaneous Procurement Components kWh Charge, and TPEAs are revised periodically in accordance with the provisions of the PJM Services and Miscellaneous Procurement Components kW Charge subsection, PJM Services and Miscellaneous Procurement Components kWh Charge subsection, and BEST Purchased Electricity Adjustment Factor subsection, respectively, of the Monthly Charges section of this tariff. The Company must file such revised charges and adjustments with the ICC for informational purposes in accordance with the provisions of this Informational Filings section which follow the same filing requirements as the provisions for the corresponding Monthly Capacity Charges, PJM Services Charges, Miscellaneous Procurement Components Charges, and Hourly Purchased Electricity Adjustment Factor provided in the Informational Filing section of Rate BESH. Electricity Charges are updated as provided in the Electricity Charges section of this tariff.

---

[p. 18] _(Continued from Sheet No. x+15; Continued on Sheet No. x+17)_

## REPORTING AND ANNUAL AUDIT.

Each year beginning in 2028, if sufficient data exists, at least thirty (30) calendar days prior to the start of the June monthly billing period, internal administrative and operational costs and costs of working capital expected to be incurred by the Company as a result of its electric power and energy supply procurement activities for retail customers for which the Company is to provide service hereunder during the PJM Planning Period beginning on the June 1 corresponding to such June monthly billing period must be reviewed by Company representatives with personnel from the Accounting Department of the ICC Staff.

Each year beginning in 2028, if sufficient data exists, the Company must conduct an audit of its costs for the previous PJM Planning Year and recoveries of such costs pursuant to this tariff. The Company must also prepare a report each year that summarizes the results of such audit. Such report must be submitted to the ICC in an informational filing, with copies of such report provided to the Manager of the Staff's Accounting Department and the Director of the Staff's Financial Analysis Division within sixty (60) calendar days after the end of the effective period associated with the May determination period of such PJM Planning Year. Such report must be verified by an officer of the Company.

The audit described in the previous paragraph of this Reporting and Annual Audit section must examine (a) costs recovered pursuant to this tariff to verify that such costs are recovered only pursuant to this tariff and to confirm that any such costs are not also being recovered inappropriately through charges imposed under other tariffs, (b) charges and adjustments determined pursuant to this tariff that are included in retail customers' bills for electric service provided hereunder to verify that such charges and adjustments are properly applied, (c) revenues resulting from the application of this tariff to verify that such revenues are correctly stated, (d) the Company's internal administrative and operational costs associated with the procurement of electric power and energy for retail customers served hereunder to verify that such costs are reasonable, and (e) the Company's costs of working capital associated with expenditures for electric power and energy supply to ensure such costs were determined in a manner consistent with the methodology used to determine costs of working capital approved by the ICC in its order in the then most recent general rate case in accordance with Article IX or Section 16-108.18 of the Act, or as otherwise provided by law, as applicable, using the cost of capital established by the ICC in its order in such most recent case or as otherwise provided by law, as applicable.

---

[p. 19] _(Continued from Sheet No. x+16; Continued on Sheet No. x+18)_

## ANNUAL RECONCILIATION.

Each year beginning in 2028, if sufficient data exists, no earlier than ninety (90) calendar days after the end of the effective period associated with the May determination period of a PJM Planning Year and concurrent with the annual reconciliation filings for Rate BESH and Rider PE, a proceeding must commence to provide for the correction of any errors that may have occurred in the application of the provisions of this tariff. Any such proceeding may also provide for the determination of the reasonableness of the Company's internal administrative and operational costs associated with the procurement of electric power and energy for retail customers served hereunder. With respect to the costs of working capital incurred by the Company, the actual costs of working capital must be calculated based upon a methodology consistent with the methodology used to determine costs of working capital approved by the ICC in its order in the then most recent general rate case in accordance with Article IX or Section 16-108.18 of the Act, or as otherwise provided by law, as applicable. The actual costs of working capital must be calculated based upon the cost of capital established by the ICC in its order in such most recent case or as otherwise provided by law, as applicable using actual expenses to arrange or procure electric power and energy directly from PJM-administered markets and applicable updated lead and lag days. Such calculated costs of working capital are subject to review and adjustment in the annual proceeding described in this Annual Reconciliation section. To the extent that any such error is identified or any such reviewable cost is found to be unreasonable by the ICC, an applicable adjustment is determined and applied in accordance with lawful orders issued by the ICC in such proceeding and effectuated through the Adjustment (A) component of the TPEA in accordance with the provisions of the BEST Purchased Electricity Adjustment Factor subsection of the Monthly Charges section of this tariff.

---

[p. 20] _(Continued from Sheet No. x+17)_

## MISCELLANEOUS GENERAL PROVISIONS.

Provisions regarding credit requirements, deposits, billing, and payment for service provided hereunder are included in the General Terms and Conditions of the Company's Schedule of Rates.

Provisions regarding the disconnection and reconnection of electric service provided hereunder for safety or other reasons are included in the Disconnection and Reconnection part of the General Terms and Conditions of the Company's Schedule of Rates.

Provisions addressing the resolution of disputes between the Company and a retail customer that involve the performance, breach, or alleged breach of any obligation under this tariff, or under any rider applicable to this tariff, or under any contract entered into under this tariff or applicable rider, are included in the Dispute Resolution part of the General Terms and Conditions of the Company's Schedule of Rates.

Nothing in this tariff precludes a residential entity that shares occupancy of a nonresidential retail customer's premises from being served as a separate retail customer under a tariff applicable or available to residential retail customers.

Nothing in this tariff precludes a nonresidential entity that shares occupancy of a residential retail customer's premises from being served as a separate retail customer under a tariff applicable or available to nonresidential retail customers.

The Company's Schedule of Rates of which this tariff is a part includes General Terms and Conditions and riders. Service hereunder is subject to the General Terms and Conditions and the riders applicable to this tariff.
