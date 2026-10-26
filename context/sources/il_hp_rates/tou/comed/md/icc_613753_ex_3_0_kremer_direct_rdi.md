# ComEd Ex. 3.0 — Direct Testimony of Kathleen E. Kremer (Residential TOU Distribution Rate Design; Initial RDI Filing)

**Source**: `icc_613753_ex_3_0_kremer_direct_rdi.pdf` (ICC e-docket file id / filing id 613753)
**Pages**: 47 PDF pages (cover, 1 page of table of contents, 45 pages of testimony numbered "Page 1 of 45" through "Page 45 of 45")
**Date**: Filed May 23, 2024 (initial rate design investigation filing; the PDF itself carries no date, and the docket caption still reads "Docket No. 24-_____")
**Docket**: ICC Docket No. 24-0378 (Commonwealth Edison Co., revenue-neutral tariff changes related to rate design — Rate BEST / DTOU) — initial RDI phase (direct testimony)
**Author(s)**: Kathleen E. Kremer, Principal Rate Analyst, Retail Rates, Commonwealth Edison Company
**Document type**: Direct testimony (Q&A format)
**ComEd exhibit no.**: ComEd Ex. 3.0 (attachments: ComEd Exs. 3.01–3.06; Ex. 3.03 and Ex. 3.04 are extracted separately in this directory)
**Extraction method**: Embedded PDF text (PyMuPDF), tables/equations/figures verified against rendered page images
**Extraction notes**:

- _Minor typographical errors in the source (e.g. "the the", "initally", "Distrubution", "categaries", "paring") have been corrected for readability. Substantive corrections are annotated inline._
- The running header on every page ("Docket No. 24-____ / ComEd Ex. 3.0 / Page N of 45") and the cover-page caption block are omitted after being stated once here. The per-line margin numbers (1–763) are stripped. Page references use **`[p. N]`** markers placed where each page of the testimony begins; **N is the testimony page number ("Page N of 45")**, which is the PDF page number minus 2. Citations of the form "Ex. 3.0 at 20:339" refer to testimony page 20, line 339.
- The Q/A structure and original headings (I., A., etc.) are preserved. In the source, the answer to the question about nonresidential DFC structure (p. 11) lacks an "A." label; it is supplied here without annotation.
- Figures 1–10 are images; each is described below and all legible numeric callouts inside them are transcribed. Tables 1–11 are reproduced as markdown tables. The three footnotes are collected under **Footnotes** at the end.
- Dollar signs are escaped as `\$`.
- Section numbering was verified against the table of contents (I–X, with the subsection letters listed there). In the source, section VI.A's title ("TOU Distribution Rate Low-Income Impacts") appears after the first Q/A of the section rather than directly under the VI heading; here it is reproduced in that source position.

---

## Cover Page

STATE OF ILLINOIS
ILLINOIS COMMERCE COMMISSION

COMMONWEALTH EDISON COMPANY

Revenue-neutral tariff changes related to rate design.

Docket No. 24-_____

**Direct Testimony of KATHLEEN E. KREMER**
Principal Rate Analyst, Retail Rates
Commonwealth Edison Company

ComEd Ex. 3.0

---

## Table of Contents

[p. i]

| Section | Title                                                               | Page |
| ------- | ------------------------------------------------------------------- | ---- |
| I.      | INTRODUCTION AND BACKGROUND                                         | 1    |
| A.      | Witness Identification                                              | 1    |
| B.      | Purpose of Direct Testimony                                         | 1    |
| C.      | Background and Qualifications                                       | 2    |
| D.      | Summary of Recommendations                                          | 2    |
| E.      | Attachments                                                         | 3    |
| II.     | FILING REQUIREMENT BACKGROUND                                       | 4    |
| A.      | Commission Directives                                               | 4    |
| B.      | ComEd's Current Rate Options                                        | 5    |
| C.      | Stakeholder Meetings                                                | 11   |
| D.      | ComEd's Proposal                                                    | 12   |
| III.    | RESIDENTIAL TOU DISTRIBUTION RATE DESIGN                            | 15   |
| A.      | TOU Distribution Rate Development                                   | 15   |
| B.      | Computation Details                                                 | 20   |
| IV.     | TARIFF REVISIONS REQUIRED TO IMPLEMENT TOU distribution rates       | 26   |
| V.      | TOU DISTRIBUTION RATE IMPACT ON EXISTING RESIDENTIAL RRTP CUSTOMERS | 27   |
| VI.     | TOU Rate IMPACT on LOW-INCOME Customers                             | 32   |
| A.      | TOU Distribution Rate Low-Income Impacts                            | 33   |
| B.      | Time-Variant Supply Low-Income Impacts                              | 38   |
| VII.    | NONRESIDENTIAL TOU DISTRIBUTION RATE DESIGN                         | 41   |
| VIII.   | ELECTRIC VEHICLE CREDITS FOR TOU ENROLLMENT                         | 44   |
| IX.     | SUPPLY TOU RATES                                                    | 45   |
| X.      | CONCLUSION                                                          | 45   |

---

[p. 1]

## I. INTRODUCTION AND BACKGROUND

### A. Witness Identification

**Q.** Please state your name and business address.

**A.** My name is Kathleen E. Kremer. My business address is Commonwealth Edison Company ("ComEd"), Three Lincoln Centre, Oakbrook Terrace, Illinois 60181.

**Q.** By whom are you employed and in what capacity?

**A.** I am employed by ComEd as a Principal Rate Analyst, Retail Rates.

### B. Purpose of Direct Testimony

**Q.** What is the purpose of your testimony?

**A.** The purpose of my testimony is to:

<!-- EPON: goal — stated purposes of Ex. 3.0: TOU-based delivery charges methodology for residential customers, tariff terms, low-income impact, Rider EVEN -->

- Present a methodology and provide an illustrative example for the determination of time of use ("TOU") based delivery charges for ComEd's residential customers;
- Discuss the terms and conditions of implementing delivery TOU and present the tariff revisions necessary for the implementation;
- Provide information on the impact of TOU rates on low-income customers; and
- Discuss ComEd's proposed Rider EVEN - Electric Vehicle Elective Notification ("Rider EVEN").

[p. 2]

### C. Background and Qualifications

**Q.** Please summarize your duties and responsibilities in your current position.

**A.** As a Principal Rate Analyst in the Retail Rates department, my primary duties are the development, implementation, and administration of ComEd's retail tariffs and policies.

**Q.** What is your professional experience?

**A.** I have been employed by ComEd since 1998 in various positions, including, in sequence: Accountant, Load Profiling Analyst, Energy Acquisition Analyst, Principal Regulatory Specialist, and my current position as Principal Rate Analyst, Retail Rates.

**Q.** What is your educational background?

**A.** I have a Bachelor of Science degree in Accounting from Northeastern Illinois University, from which I graduated magna cum laude in 1998.

**Q.** Have you submitted testimony to the Illinois Commerce Commission ("ICC" or "Commission") in prior proceedings?

**A.** Yes. I presented testimony in ICC Docket No. 21-0850 in support of proposed revisions to Rider DG REBATE – Renewable Energy Distributed Generation Rebate ("Rider DG Rebate") to expand eligibility and set new rates, and also in ICC Docket No. 23-0773 in support of proposed Rider IMUD – Interval Meter Usage Data ("Rider IMUD").

### D. Summary of Recommendations

**Q.** What are the principal recommendations in your direct testimony?

<!-- EPON: goal,bundling,ev-hp,bill-comparison — summary of recommendations: four-period kWh-based DTOU paired with time-variant supply; Rider EVEN for EV owners; claim that residential and low-income customers on time-variant supply would benefit on average -->

**A.** First, should the Commission direct ComEd to offer TOU distribution charges, the four-period kWh-based methodology I present is fair and reasonable, and should be paired with

[p. 3]

existing and future time-variant supply rates in order to further incentivize customers to shift load. Second, proposed Rider EVEN provides a fair and reasonable additional incentive for residential customers that are electric vehicle ("EV") owners to enroll in a time-variant supply rate that is paired with a TOU distribution rate. Third, I present data demonstrating that residential customers and low-income residential customers on a time-variant supply rate, on average, would benefit from a TOU distribution rate.

### E. Attachments

**Q.** What are the attachments to your direct testimony?

**A.** The following Exhibits ("Exs.") are attached to my testimony:

- ComEd Ex. 3.01 is a copy of the tariff sheets containing ComEd's proposed revisions to Rate BESH – Basic Electric Service Hourly Pricing ("Rate BESH"), Rate RDS – Retail Delivery Service ("Rate RDS"), Rate RESS – Retail Electric Supplier Service ("Rate RESS"), and Rate MRPP – Multi-Year Rate Plan Pricing ("Rate MRPP") to implement TOU distribution rates to residential retail customers;
- ComEd Ex. 3.02 is a copy of the same tariff sheets showing ComEd's proposed revisions to Rate BESH, Rate RDS, Rate RESS, and Rate MRPP as shown in ComEd Ex. 3.01, but in redline format;
- ComEd Ex. 3.03 is a copy of the proposed Informational Sheets showing the TOU Distribution Facilities Charges ("DFCs");
- ComEd Ex. 3.04 presents an illustrative example showing the determination of the TOU DFCs;

[p. 4]

- ComEd Ex. 3.05 is a copy of the proposed Rider EVEN tariff; and
- ComEd Ex. 3.06 is a copy of the proposed Informational Sheet supplement to Rider EVEN.

## II. FILING REQUIREMENT BACKGROUND

### A. Commission Directives

**Q.** Why is ComEd proposing TOU distribution rates for residential customers?

<!-- EPON: goal — origin of DTOU: 2023 BE Final Order (Dockets 22-0432/22-0442) required ComEd to propose a TOU distribution rate in its next RDI -->

**A.** The Final Order in ComEd's Beneficial Electrification Plan proceeding, ICC Docket Nos. 22-0432 / 22-0442 (Cons.) ("2023 BE Final Order"), requires ComEd to develop and propose a TOU distribution rate in its next rate design investigation proceeding, and included a requirement for ComEd to work with the ICC Staff and stakeholders to develop proposed TOU distribution rates as part of ComEd's 2024 Rate Design Investigation ("RDI") filing. _Commonwealth Edison Co._, ICC Docket Nos. 22-0432 / 22-0442 (cons), Final Order (Mar. 23, 2023) at 258.

**Q.** What does the Commission require of a TOU distribution rate proposal?

<!-- EPON: goal,midday-peak,ev-hp — the three Commission requirements: significant on/off-peak differential, periods coinciding with distribution system peaks, and an EV-owner incentive (rate not exclusive to EV owners) -->

**A.** The Commission's directive in the 2023 BE Final Order identified three core requirements:

- A TOU rate must contain differences between on-peak and off-peak periods that are significant enough to encourage customers to shift usage without deterring customers from signing up for the rate;
- The rate's on-peak and off-peak periods should coincide with the distribution system on-peak and off-peak periods; and

[p. 5]

- ComEd's rate proposal should include an incentive for EV owners (e.g., monthly/annual bill credits) to go on the rate, though the rate should not be available exclusively to EV owners. _Id._

**Q.** Is it your understanding that the Commission must adopt TOU distribution rates in this proceeding?

**A.** No. Although I am not an attorney, it is my understanding that the Commission required the development of a TOU distribution rate methodology for consideration. In the 2023 BE Final Order, the Commission stated: "Whether or not the TOU rate as proposed in the future rate design investigation proceeding is appropriate and should be adopted will be determined in that proceeding. However, the Commission directs ComEd to work with Staff and stakeholders in the development of the new proposed distribution TOU rate." _Id._ at 263. Whether or not such rates should be adopted as proposed, modified, or rejected entirely, will be up to the Commission.

### B. ComEd's Current Rate Options

**Q.** Can you describe the categories of charges that appear on a ComEd customer's bill?

**A.** Yes. There are three categories shown on a customer's ComEd bill: Supply, Delivery, and Taxes & Fees. These categories are shown in Figure 1.

[p. 6]

**Figure 1: ComEd Bill Categories**

[DIAGRAM DESCRIPTION: Figure 1: ComEd Bill Categories]

An image of a sample ComEd residential monthly bill (page 1 of 3, issued 4/11/24, account # 1234567890; "SERVICE FROM 3/13/24 THROUGH 4/11/24", "Residential - Single"; customer name and address are placeholders). A banner reads "Payment Deducted on 5/3/24 — $104.31" with "Thank you for your payments totaling $117.49." Left panel: "TOTAL USAGE (kWh)" bar chart of monthly usage from April 2023 through April 2024 (summer months highest, current month bar highlighted as an actual read). Right panel: "AVERAGE DAILY USE (monthly usage/days in period)" showing Current Month 19.2 kWh/day (+11% from last year, 43.2° avg. temp), Last Month 18.4 kWh (43.9° avg. temp), Last Year 17.3 kWh (41.2° avg. temp), with the note "Ten 100W light bulbs for 1 hour = 1 kWh". Bottom: a "CURRENT CHARGES SUMMARY" donut chart of current charges "$104.31" split into three categories, each boxed in red by the testimony's author: **SUPPLY $35.41** ("ComEd provides your energy."), **DELIVERY $43.22** ("ComEd delivers electricity to your home."), and **TAXES & FEES $25.68**. (The figure is the testimony's illustration that a bill has three categories: Supply, Delivery, Taxes & Fees.)

[→ See original PDF page 8 for visual rendering]

Charges that are shown in the Supply category include electric power and energy provided by either ComEd or a Retail Electric Supplier ("RES") and are typically based upon the volume of kilowatt-hours ("kWhs") that a customer uses in a monthly billing period. If a customer elects to have their Supply provided by ComEd, ComEd provides that customer electric power and energy as a direct pass-through cost, without markup. In order to deliver the electric power and energy (_i.e._, Supply), ComEd builds and maintains the distribution

[p. 7]

power grid, along with measuring and billing customers for the power and energy delivered. ComEd incurs costs to do all of this. The charges related to those costs appear on a customer's bill in the Delivery category and reflect the portion of those costs for which the customer is responsible. Charges that appear in the Taxes & Fees category are costs related to state requirements or programs that ComEd administers.

**Q.** Which line item under Delivery costs is relevant to a TOU rate?

<!-- EPON: fixed-vs-volumetric — DFC is the delivery line item recovering distribution costs; residential DFCs are today a flat per-kWh rate -->

**A.** The DFC line item is the cost within the Delivery category for which the Commission is directing the development of a TOU distribution rate. This line item recovers distribution costs. These costs are generally related to the purchase and maintenance of equipment like poles, conduit, wire and cable, and transformers. Today, the DFCs are charged to residential customers at a flat per-kWh rate, multiplied by the volume of kWhs that customer uses in a monthly billing period.

**Q.** Can you explain what is meant by the terms "time-variant," "TOU," and "hourly" in relation to electricity pricing and rates?

**A.** Yes. Under the broad umbrella of time-variant rates, TOU and hourly are different types of pricing models. As the name implies, under time-variant rates, the price a customer pays for electricity varies based upon when the customer uses electricity. Generally, a customer on a time-variant rate will pay more at times when system demand is high and less at times when system demand is low. Thus, time-variant pricing differs from more traditional utility rate models, where the customer pays the same amount per unit of electricity regardless of when the customer's usage occurs. Because time-variant rates incorporate information about demand for electricity, they are generally understood to provide better

[p. 8]

price signals than traditional rate models. Customers are financially incentivized to shift energy usage from periods when prices are high to periods when prices are low.

Within the broad category of time-variant rates, there is a wide range of rate structures. TOU rates typically divide each 24-hour day into two or more pricing periods, and a specific, pre-determined price applies to all consumption within each period. They vary in the number of pricing periods, the hours included in each pricing period, and the methodology for determining the price applied in each period. Hourly pricing is another type of time-variant rate. Under a typical hourly pricing rate, the charge is determined at the hour the energy is consumed, with higher prices corresponding to increased electricity demand.

**Q.** Can ComEd's customers choose their provider of Supply?

**A.** Yes. With the exception of those residential customers who receive a DG Rebate for storage, which requires those customers to take service under ComEd's hourly supply rate (Rate BESH), all of ComEd's customers can elect to take supply from a RES.[^1]

**Q.** Can customers choose their supply rate when they elect to take service from a RES?

**A.** Yes. While ComEd cannot speak to the types of RES supply offerings specifically, ComEd understands that there are numerous supply products offered by RESs. A listing of currently available RES offerings can be found at www.plugin.illinois.gov.

[p. 9]

**Q.** Do residential and small commercial customers have different supply rate options when they elect to take service from ComEd?

<!-- EPON: bundling,profile — status quo supply options: default flat Rate BES, hourly Rate BESH via Rider RRTP (1.1% of residential customers), 1,900-participant RTOUPP three-period pilot sunsetting June 2024 -->

**A.** Yes. Except for those exclusions discussed above, all residential and small commercial customers who choose to take supply service from ComEd will default to ComEd's flat rate supply pricing, under Rate BES – Basic Electric Service ("Rate BES"). Those customers can elect ComEd's hourly supply pricing, available under Rate BESH since 2007 (note that residential customers take Rate BESH supply under Rider RRTP – Residential Real Time Pricing Program ("Rider RRTP" or "RRTP")). As of the December 2023 Public ICC Switching Report for ComEd, 1.1% and 1.3% of residential and small commercial customers, respectively, choose to take supply service under Rate BESH. ComEd also offers a residential time of use supply pilot rate with three pricing periods under Rate RTOUPP – Residential Time of Use Pricing Pilot ("Rate RTOUPP" or "RTOUPP"). The pilot, which is capped at 1,900 participants, started in June 2020 and is scheduled to sunset in June 2024.

**Q.** Can customers choose their provider of delivery service, shown in the Delivery category on their bill?

**A.** No. ComEd delivers power and energy to all customers from the supplier that each customer has elected (either ComEd or a RES). ComEd recovers the costs related to this delivery service, shown in the Delivery section of a customer's bill, based upon the customer's assigned delivery class.

[p. 10]

**Q.** Can customers choose their delivery service class under existing tariffs?

<!-- EPON: profile — delivery class is assigned, not chosen (customer type or billing kW); class DFC set from ECOSS revenue requirement; only exception is separately metered nonresidential EV charging in Watt-Hour class -->

**A.** No. With one exception, all customers are assigned a delivery class based upon the type of customer (e.g., residential single family, residential multi-family, dusk to dawn lighting, etc.) or level of billing kilowatt ("kW") demand (e.g., Small Load (0-100 kW), Medium Load (100-400 kW) etc.) and cannot elect a different delivery service class. The exception is that nonresidential customers that have dedicated (i.e. separately metered) EV charging facilities have the ability to elect delivery service under the Watt-Hour Delivery Class. A customer's delivery class determines the DFC applicable in the customer's Delivery section of the bill.

**Q.** What are ComEd's DFCs?

**A.** ComEd's DFCs are listed beginning in the Delivery Service Charge Informational Sheet No. 64 et. seq., supplement to Rate MRPP in ComEd's Schedule of Rates. The DFCs are designed to recover delivery service costs related to purchase and maintenance of equipment like poles, conduit, wire and cable, transformers, and other facilities required to maintain a reliable distribution system. The DFCs vary by delivery class and are set to recover the revenue requirement allocated to each delivery class for such distribution services. The assigned revenue requirement is determined in ComEd's embedded cost of service study ("ECOSS") (ComEd Ex. 2.01) and determination of the charges is provided in the rate design (ComEd Ex. 2.02) attached to the direct testimony of ComEd witness Leick (ComEd Ex. 2.0).

[p. 11]

**Q.** How are ComEd's DFCs currently structured for residential customers?

<!-- EPON: fixed-vs-volumetric — status quo: all residential DFCs are a flat per-kWh charge with no time-of-day distinction -->

**A.** For all residential customers, DFCs are a per kWh charge which are multiplied by the total kWh usage during the month without any distinction based on day or time when the kWhs are delivered.

**Q.** How are ComEd's DFCs currently structured for nonresidential customers?

<!-- EPON: fixed-vs-volumetric,midday-peak — nonresidential DFC is a kW demand charge on Maximum Kilowatts Delivered (MKD) in a 9:00 A.M.–6:00 P.M. weekday window; ComEd characterizes this as already a TOU distribution rate -->

**A.** For all nonresidential customers except those in the Watt-Hour Delivery Class, DFCs are a per kW charge for that customer's Maximum Kilowatts Delivered ("MKD") as defined on the 2nd Revised Sheet No. 129.1 in the General Terms and Conditions section of ComEd's Schedule of Rates. The MKD is the highest thirty (30) minute demand for electric power and energy in each monthly billing period established by the customer and delivered by ComEd during the periods, known as the "MKD window" from 9:00 A.M. until 6:00 P.M. on Monday through Friday, except on days designated as holidays by the North American Electric Reliability Corporation ("NERC"). To the extent that ComEd delivers electric power and energy to the customer outside of the MKD window, the customer does not pay a DFC for that measured kW. This inherently makes the current DFC structure for nonresidential customers, including small commercial customers, a TOU distribution rate. Therefore, ComEd is not proposing another TOU distribution rate for small commercial customers.

### C. Stakeholder Meetings

**Q.** How did ComEd gather input from ICC Staff and other stakeholders?

**A.** ComEd hosted a meeting on December 11, 2023. Fourteen parties attended that meeting: ICC Staff, Advanced Energy United, Ameren Illinois, the City of Chicago, Constellation,

[p. 12]

the Citizens Utility Board ("CUB"), the Environmental Defense Fund ("EDF"), Metra, the Environmental Law and Policy Center ("ELPC"), the Illinois Competitive Energy Association ("ICEA"), Legal Action Chicago, the Office of the Illinois Attorney General ("AG"), Nicor Gas, IGS Energy, and ChargePoint. During the meeting, ComEd presented information related to both supply and distribution TOU rates and solicited feedback. ComEd requested additional feedback via survey and held a follow-up meeting on April 12, 2024. Fourteen parties attended that meeting: ICC Staff, Advanced Energy United, Ameren Illinois, the City of Chicago, the AG, CUB, EDF, ELPC, ICEA, Generac, GridX, Metra, Constellation, and The Ad Hoc Group. ComEd considered feedback from these meetings and parties in the development of the current proposal.

### D. ComEd's Proposal

**Q.** How does ComEd's proposed methodology satisfy the Commission's core requirements as discussed in Section II. A. of your testimony?

<!-- EPON: goal,midday-peak,ev-hp — how the proposal claims to meet the three Commission requirements: kWh-based DFCs track historical usage, periods coincide with distribution on/off-peak, Rider EVEN incentive for EV owners enrolling in a time-variant supply rate for 2 years -->

**A.** First, under ComEd's methodology, ComEd will determine varying kWh-based DFCs that correspond with distribution system usage. This means that DFCs will be lower during periods of historically lower usage and higher during periods of historically higher usage. Second, as I discuss below, the rate's on-peak and off-peak periods coincide with the distribution system on-peak and off-peak periods, again, aligning the proposed charges with distribution costs. Third, this proposal includes financial incentives, through the introduction of Rider EVEN, for residential EV owners to enroll in a time-variant supply rate (which will be paired with the TOU distribution rate) and to remain enrolled for 2 years. See ComEd Exs. 3.05 and 3.06.

[p. 13]

**Q.** What are the key components of ComEd's proposed TOU rate methodology?

<!-- EPON: profile,fixed-vs-volumetric — revenue-neutral design: TOU DFCs collect the same class DFC revenue as the single flat DFC if ALL residential customers in the class were on the new rate -->

**A.** The TOU DFCs for each residential delivery class are developed using what is commonly known as a "revenue neutral rate design." In other words, the TOU DFC rates are designed to collect the same amount of DFC revenue for the residential delivery class as are currently being collected with the single, non-time-variant DFC rate if all residential customers were on the new rate.

**Q.** Is enrollment in the TOU distribution rates dependent on election of a time-variant supply rate?

<!-- EPON: bundling,stacking — DTOU is not a standalone choice: it is automatically "paired" with any elected time-variant supply rate (ComEd Rider RRTP or RES) for AMI-metered residential customers -->

**A.** Yes. See ComEd Ex. 3.01. All residential customers with an AMI meter taking service under ComEd's default supply rate, Rate BES, can voluntarily choose to take supply service under ComEd's Rider RRTP or a RES time-variant rate. If a residential customer elects a time-variant supply rate, whether offered by ComEd or a RES, the TOU distribution rate will be "paired" with that customer's elected supply rate as the applicable TOU distribution rate. A RES would need to notify ComEd that a customer is on a time-variant supply rate and then the TOU distribution rate would apply.

**Q.** Why does ComEd require the residential TOU distribution rate be paired with a time-variant supply rate?

<!-- EPON: bundling,goal — rationale for pairing: minimize election points and administrative burden; a flat distribution option would be "counterintuitive" alongside a time-variant supply election -->

**A.** Having only one distribution rate option will minimize the election points that customers face when enrolling in RRTP. If the rates are not paired, a customer selecting their time-variant supply rate would additionally need to decide between a Fixed Distribution Rate or a TOU Distribution Rate. If a customer would like to find a rate that rewards shifting their energy usage, it would be counterintuitive for ComEd to offer a non-time-variant

[p. 14]

distribution option to go with the time-variant supply election the customer just made. The most straightforward and customer-friendly offering for a time-variant rate is one where our customers can maximize the effects of any actions they will take to shift load. Pairing time-variant supply rates with a time-variant distribution rate accomplishes this goal. Without this pairing, ComEd would need to program its systems to allow for several different rate combinations (i.e., RRTP supply with flat distribution vs RRTP with TOU distribution; BES with flat distribution vs BES with TOU distribution; RES-supplied flat rate with flat rate distribution vs RES supplied flat rate with TOU distribution; and RES-supplied time-variant rate with flat rate distribution vs RES-supplied flat rate with TOU distribution) [sic; the final comparison is likely intended to read "RES-supplied time-variant rate with TOU distribution"], rather than assigning each supply election to one corresponding distribution election. ComEd would also need to develop marketing materials explaining all of the combinations, also resulting in substantial additional costs. Together, we believe these would be unnecessary administrative burdens that would conflict with the core purpose of offering a time-variant rate: to help customers manage their energy usage and by extension, their energy bills.

**Q.** Will residential customers who have taken certain rebates be required to take their applicable TOU distribution rate?

<!-- EPON: bundling,ev-hp,lockout — customers who took a DG Rebate for storage (must take Rate BESH) or a Beneficial Electrification rebate for an EV charger/installation (must take a time-variant supply rate) are required onto the paired DTOU rate -->

**A.** Yes. As described previously in my testimony, residential customers who have taken a DG Rebate for storage are required to take supply service under Rate BESH, which, under the proposed methodology, will be paired with the TOU distribution rate corresponding to their delivery class. In addition, in the 2023 BE Final Order, the ICC approved the requirement for residential customers who receive a BE rebate for an EV charger and installation to

[p. 15]

take supply service under a time-variant rate. _Commonwealth Edison Co._, ICC Docket Nos. 22-0432 / 22-0442 (cons.), Final Order (Mar. 23, 2023) at 257. Since those customers are required to take supply service under a time-variant rate, either offered by ComEd or by a RES, ComEd will pair their time-variant supply service with the applicable TOU distribution rate.

**Q.** When would these rates go into effect?

**A.** If approved, these residential TOU distribution rates will go into effect beginning with the January 2026 monthly billing period. This is the same time as any revisions to Delivery Service Charges adopted by the Commission in this revenue neutral RDI proceeding as discussed in ComEd witness Leick's direct testimony, ComEd Ex. 2.0.

## III. RESIDENTIAL TOU DISTRIBUTION RATE DESIGN

### A. TOU Distribution Rate Development

**Q.** What is ComEd's TOU distribution rate design proposal?

<!-- EPON: profile,fixed-vs-volumetric — four-period revenue-neutral kWh DFC; revenue neutrality holds only "if usage profiles remain unchanged from the class average profile" -->

**A.** ComEd proposes a revenue neutral rate design that includes different DFCs for four TOU periods, designed to recover the same amount of revenue that the fixed-price DFC would recover for all of the customers in each residential delivery class if usage profiles remain unchanged from the class average profile.

**Q.** What are the four time periods and how are these time periods determined?

<!-- EPON: midday-peak — Table 1 / Figure 2: Mid-Day Peak = 1:00 PM–7:00 PM, "High" system loading, 76% of feeder peaks; periods chosen by share of feeders peaking in each period -->

**A.** The time periods are presented in Table 1. These time periods correspond closely with the percentage of distribution feeders that experience peak loading during the day as shown in Table 1 and Figure 2, and which I will describe in greater detail later in my testimony.

[p. 16]

ComEd chose the names of the periods to be intuitive, using common terms that customers can easily remember.

**Table 1: Time Periods**

<!-- EPON: midday-peak — the four DTOU periods and their feeder-peak shares: Morning 6am–1pm 17%, Mid-Day Peak 1pm–7pm 76%, Evening 7pm–11pm 5%, Overnight 11pm–6am 2% -->

| Period Name  | Start Time | End Time | System Loading | % of Feeder Peaks |
| ------------ | ---------- | -------- | -------------- | ----------------- |
| Morning      | 6:00 AM    | 1:00 PM  | Moderate       | 17%               |
| Mid-Day Peak | 1:00 PM    | 7:00 PM  | High           | 76%               |
| Evening      | 7:00 PM    | 11:00 PM | Moderate       | 5%                |
| Overnight    | 11:00 PM   | 6:00 AM  | Base           | 2%                |

**Figure 2: System Loading and Feeder Peak**

[DIAGRAM DESCRIPTION: Figure 2: System Loading and Feeder Peak]

A bar chart of the number of distribution feeders reaching their annual peak in each hour of the day (y-axis "Feeder Count", ticks 0–1200 in steps of 200; x-axis labeled by clock time, running 11pm | 6am for the Overnight block, 6am–1pm, 1pm | 7pm, and 7pm–11pm), overlaid with four color-shaded vertical blocks, one per TOU period: a green **Overnight** block (11pm–6am) labeled "2% of feeders peak in Overnight Period" with almost no bars (tiny bars only just before 6am); a yellow **Morning** block (6am–1pm) labeled "17% of feeders peak in Morning Period" with small bars rising gradually from about 40 to about 220 feeders toward 1pm; a red **Mid-Day Peak** block (1pm–7pm) labeled "76% of feeders peak in Mid-Day Peak Period" with bars rising from about 400 and 480, to about 730, a maximum of about 1,130 and about 1,030 in the 5–7pm hours, and about 420 in the last hour (the peak bar heights are approximate readings from the chart); and an orange **Evening** block (7pm–11pm) labeled "5% of feeders peak in Evening Period" with bars of about 160, 90 and 30 feeders tapering to zero (consistent with the hourly averages 160.5, 92.5 and 33.0 in ComEd Ex. 3.04, tab 3_Feeder Peak). Beneath the chart, three horizontal bands map TOU periods to system-loading cost categories: a red band **System High** ("Costs related to shared distribution lines and substations based upon a heavily loaded grid") spanning only the Mid-Day Peak block; an orange band **System Moderate** ("Costs related to shared distribution lines and substations based upon a moderately loaded grid") spanning the Morning through Evening blocks (6am–11pm); and a green band **System Base** ("Costs related to the baseline equipment required to deliver power, including all secondary voltage transformers and distribution lines, in addition to a portion of costs related to shared facilities") spanning all 24 hours.

[→ See original PDF page 18 for visual rendering; the exact bar heights are in the source data at ComEd Ex. 3.04, tab 3_Feeder Peak]

[p. 17]

**Q.** What are the three categories of the System Loading shown in Table 1 and Figure 2?

**A.** These categories represent the types of distribution equipment that are needed to support different loading scenarios.

- System Base Loading describes the time periods during which the loads on ComEd's grid are historically low and only baseline distribution equipment (e.g. poles, crossarms, trenching, conduit, and local distribution equipment like transformers) is required to deliver electricity. This type of equipment needs to be in place whether the load is 1 kW or 1,000 kW.
- System Moderate Loading describes the time periods during which the loads on ComEd's grid are historically moderate, requiring larger conductors and distribution equipment to deliver electricity.
- System High Loading describes the time periods during which the loads on ComEd's grid are historically higher, requiring larger sized or more distribution equipment, including conductors and substation equipment, to deliver electricity.

**Q.** How are the revenue neutral TOU DFCs determined?

**A.** An illustrative example of the determination of revenue neutral TOU DFCs is provided in ComEd Ex. 3.04. The first tab of this exhibit, 1_DTOU DFC Rates, shows the computation of the TOU DFCs. For convenience, some of the computation results from this tab are included as the tables in my testimony.

First, the total amount of kWhs for each of the residential delivery classes is identified by the TOU time periods and then included in each of the applicable System

[p. 18]

Loading categories. Tables 2, 3 and 4 below provide illustrative examples.

<!-- EPON: ev-hp,profile — the four residential delivery classes distinguish homes WITH vs WITHOUT electric space heat (SFNH, MFNH, SFH, MFH); heat-pump/electric-heat homes are a separate delivery class for DTOU rate design -->

The residential delivery classes are: Single Family Without Electric Space Heat ("SFNH"), MultiFamily Without Electric Space Heat ("MFNH"), Single Family With Electric Space Heat ("SFH"), and MultiFamily With Electric Space Heat ("MFH"). The applicable TOU period kWhs for each System Loading category are shown in Table 4 below (and previously in Figure 2):

<!-- EPON: stacking,midday-peak — cost layering: System Base cost spread over all four periods, System Moderate over all but Overnight, System High over Mid-Day Peak kWh only -->

System Base cost is allocated to all four TOU periods; System Moderate Cost is allocated to all but the Overnight period; and System High cost is allocated to only the Mid-Day Peak period.

**Table 2: Forecasted 2026 Annual Billed kWh by Distribution TOU Period**

<!-- EPON: profile,midday-peak — Mid-Day Peak billed kWh by class (SF no heat 6.13 billion, MF no heat 1.42 billion, SF heat 0.178 billion, MF heat 0.416 billion kWh) are the divisor for System High rates -->

| TOU Period   | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- |
| Morning      | 5,306,933,486                     | 1,370,864,294                    | 201,417,739                    | 465,266,160                   |
| Mid-Day Peak | 6,129,549,262                     | 1,420,394,572                    | 177,787,988                    | 416,019,068                   |
| Evening      | 4,026,635,272                     | 993,077,851                      | 120,921,719                    | 291,317,516                   |
| Overnight    | 4,592,622,074                     | 1,247,167,105                    | 174,617,202                    | 406,333,685                   |
| Total        | 20,055,740,094                    | 5,031,503,822                    | 674,744,648                    | 1,578,936,429                 |

**Table 3: Applicable kWh for each System Loading Category**

The table maps each System Loading category (rows) to the TOU periods whose kWh it applies to (columns, in order Morning, Mid-Day Peak, Evening, Overnight):

| System Category | Morning | Mid-Day Peak | Evening | Overnight |
| --------------- | ------- | ------------ | ------- | --------- |
| System High     |         | Mid-Day Peak |         |           |
| System Moderate | Morning | Mid-Day Peak | Evening |           |
| System Base     | Morning | Mid-Day Peak | Evening | Overnight |

[p. 19]

**Table 4: Forecasted 2026 Annual Billed kWh by System Loading Category**

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- |
| System High             | 6,129,549,262                     | 1,420,394,572                    | 177,787,988                    | 416,019,068                   |
| System Moderate         | 15,463,118,020                    | 3,784,336,717                    | 500,127,446                    | 1,172,602,744                 |
| System Base             | 20,055,740,094                    | 5,031,503,822                    | 674,744,648                    | 1,578,936,429                 |

Next, the DFC revenue responsibilities for each delivery class from the result of the rate design provided in ComEd Ex. 2.02 are allocated to each of the three System Loading categories. Table 5 provides this illustrative example.

**Table 5: DFC Revenue Responsibility by System Loading Category**

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- |
| System High             | \$400,184,224                     | \$77,604,096                     | \$5,769,596                    | \$12,367,350                  |
| System Moderate         | \$118,051,203                     | \$22,892,691                     | \$1,699,967                    | \$3,642,506                   |
| System Base             | \$598,468,181                     | \$113,241,496                    | \$10,458,402                   | \$23,874,078                  |
| Total                   | \$1,116,703,608                   | \$213,738,283                    | \$17,927,965                   | \$39,883,934                  |

The per kWh DFC revenue responsibility for each System Loading category is the result of dividing the DFC revenue responsibility for the System Loading category by the applicable kWhs of the System Loading category. See Table 6, below:

**Table 6: Per kWh DFC Revenue Responsibility**

<!-- EPON: ev-hp,midday-peak,stacking — per-kWh System High/Moderate/Base cost layers by class; space-heat classes have markedly lower layers (System High: SF no heat $0.06529 vs SF heat $0.03245; MF no heat $0.05464 vs MF heat $0.02973 per kWh) -->

| System Loading Category | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat |
| ----------------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- |
| System High             | \$0.06529                         | \$0.05464                        | \$0.03245                      | \$0.02973                     |
| System Moderate         | \$0.00763                         | \$0.00605                        | \$0.00340                      | \$0.00311                     |
| System Base             | \$0.02984                         | \$0.02251                        | \$0.01550                      | \$0.01512                     |

[p. 20]

<!-- EPON: stacking,midday-peak — the three system-loading price layers are "stacked": Mid-Day Peak = High + Moderate + Base ($0.06529 + $0.00763 + $0.02984 = $0.10276/kWh for SFNH); Morning/Evening = Moderate + Base; Overnight = Base only -->

To determine the final rates, the three System Loading periods are stacked for the corresponding period. Meaning the System High includes all three prices, or for SFNH, the Mid-Day Peak price is \$0.06529 + \$0.00763 + \$0.02984 = \$0.10276/kWh. The Morning and Evening DFCs stack the System Moderate and System Base, while the Overnight DFC is only the System Base price. The result of the application is shown in the illustrative example in Table 7.

<!-- EPON: profile,fixed-vs-volumetric — revenue-neutrality check: class kWh shares per period times TOU prices reproduce the flat class DFC (Ex. 2.02), which holds only at the class-average load shape -->

The last line of Table 7 shows the base DFC for comparison. In the corresponding calculation in this first tab of ComEd Ex. 3.04, a computation is done to confirm that the corresponding share of the kWhs billing determinants in each TOU period times the TOU distribution rate prices result in the same base fixed DFC shown in ComEd Ex. 2.02 (slight rounding difference may occur), confirming the revenue neutrality of the rate design.

**Table 7: Per kWh DFC by Distribution TOU Period**

<!-- EPON: ev-hp,midday-peak,stacking,fixed-vs-volumetric — final DTOU rates by delivery class; electric-space-heat classes pay lower per-kWh rates in every period: about 50% of the no-heat rate for single family and 58–67% for multi family (Mid-Day Peak SF heat $0.05135 vs SF no heat $0.10276; MF heat $0.04796 vs MF no heat $0.08320) and a lower flat DFC (SF heat $0.02657 vs SF no heat $0.05568); Mid-Day Peak is about 3.4x Overnight for SFNH and about 3.3x for SFH -->

| Period           | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat |
| ---------------- | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- |
| Morning          | \$0.03747                         | \$0.02856                        | \$0.01890                      | \$0.01823                     |
| Mid-Day Peak     | \$0.10276                         | \$0.08320                        | \$0.05135                      | \$0.04796                     |
| Evening          | \$0.03747                         | \$0.02856                        | \$0.01890                      | \$0.01823                     |
| Overnight        | \$0.02984                         | \$0.02251                        | \$0.01550                      | \$0.01512                     |
| (Flat) Fixed DFC | \$0.05568                         | \$0.04248                        | \$0.02657                      | \$0.02526                     |

### B. Computation Details

**Q.** Can you discuss the other information is presented in ComEd Ex. 3.04?

**A.** Yes. I will walk you through the calculations presented in ComEd Ex. 3.04. Tabs 2 through 5 of ComEd Ex. 3.04 provide computation details:

[p. 21]

- Tab 2_DTOU DFC RevResp shows the allocation of the DFC revenue responsibilities for each residential delivery class to three DFC revenue responsibilities, one for each System Loading category, by identifying distribution costs by sub-function and the factor used to allocate each of the sub-function costs to the three System Loading categories.
- Tab 3_Feeder Peak shows the development of the Feeder Peak allocation factor.
- Tab 4_Shared Distribution Lines [source says "Distrubution"] shows the development of the Plant/Feeder Peak allocation factor.
- Tab 5_DTOU kWhs shows the development of kWhs by TOU periods from a single annual amount of billed kWh for each delivery class shown in ComEd Ex. 2.02.

**Q.** How does ComEd develop the DFC revenue responsibilities?

<!-- EPON: stacking,midday-peak,fixed-vs-volumetric — cost-allocation logic: secondary wires/transformers 100% System Base; high-voltage lines and substations by feeder-peak frequency; shared distribution lines by plant-in-service plus feeder-peak -->

**A.** ComEd develops the DFC revenue responsibility for each System Loading category by allocating the Distribution Facilities Costs by sub-function from ComEd's ECOSS provided by ComEd witness Leick (ComEd Ex. 2.01) through allocation factors shown in ComEd Ex. 3.04. ComEd allocates the costs for distribution sub-functions to System Loading categories by one of the three sets of allocation factors: costs related to secondary voltage wires and transformers are allocated 100% to System Base Loading; costs related to High Voltage Lines and Substations of all voltages are allocated to three System Loading categories based on Feeder Peak Data; and costs related to Shared Distribution Lines are allocated to three System Loading categories based on a combination of Plant in Service Cost Data and Feeder Peak Data, both of which I describe below.

[p. 22]

The illustrative example provided in ComEd Ex. 3.04 presents, on the 2_DTOU DFC RevResp tab, the development of the 2026 DFC revenue responsibility by System Loading categories. In this tab, we show the following:

- The DFC revenue responsibilities by delivery class are shown in the table in section A. This is the amount that needs to be allocated to System Loading categories for each delivery class.
- The allocation process starts with the Distribution Facilities Cost by sub-function table in section B, and the three System Loading categories are shown in section C.
- The three sets of allocation factors used to allocate the Distribution Facilities Cost by sub-function to the three System Loading categories described earlier are shown next to each sub-function in the Allocation Factors table in section D.
- Finally, the Distribution Facilities Costs by System Loading table in section E shows the result of applying the allocation factors by sub-function to the Distribution Facilities Costs by sub-function.
- The DFC Revenue Responsibility by System Loading table in section F presents the result of allocating the DFC Revenue Responsibility for each delivery class table in section A by the percentages determined from the table in section E. These results are also provided in Table 5 of my testimony, above.

**Q.** What is Feeder Peak Data?

<!-- EPON: profile,midday-peak — Feeder Peak Data: date/hour/load at each of ~5,500 feeders' annual peak in 2022 and 2023, i.e., system (feeder) peak hours drive the 76/22/2 System High/Moderate/Base cost split -->

**A.** Feeder Peak Data is the data set that contains the date, hour, and corresponding load for each distribution feeder at the point that it reached its highest loading in 2022 and 2023. A

[p. 23]

distribution feeder is a term used to describe a distribution line (ComEd had approximately 5,500 distribution feeders in service in 2022 and 2023). In the illustrative example provided in ComEd Ex. 3.04, the 3_Feeder Peak tab presents the development of the average frequency of distribution feeders reaching peak during the three System Loading periods in 2022 and 2023. Columns (A), (B), and (C) of the table in section B provide the count of feeders reaching their highest feeder loading in 2022 and 2023 for each of the 24 hours, while the average count and percentage of the 2022 and 2023 feeders reaching peak feeder loading are computed in Columns (D) and (E). The computed percentages of the feeder peak for the four TOU periods are presented in Column (F) of this table.

<!-- EPON: midday-peak,stacking — mapping of TOU periods to System Loading categories: Morning+Evening = Moderate, Mid-Day Peak = High, Overnight = Base; allocation factors 76% / 22% / 2% -->

The result shown in Table 1 is developed through the assignment of the TOU periods to the System Loading categories presented in the table in section C: Morning and Evening periods are assigned to System Moderate; Mid-Day Peak period is assigned to System High; and the Overnight period is assigned to System Base. The allocation result for the three System Loading categories is shown in the row with the title "Allocation Factors" in this assignment table: 76%, 22%, and 2%. This corresponds to Table 1, presented earlier in my testimony, which shows the average frequency of distribution feeders reaching peak during the three System Loading periods in 2022 and 2023.

**Q.** What is Plant in Service Cost Data and how is the Feeder Peak data used to allocate the costs of Shared Distribution Lines?

**A.** Plant in Service Cost Data is the estimated 2026 total plant in service cost for Federal Energy Regulatory Commission ("FERC") Accounts 364-367, the accounts related to Shared Distribution Lines, from ComEd's 2026 ECOSS. See ComEd Ex. 2.01. The table

[p. 24]

in section A of the 4_Shared Distribution Lines tab in ComEd Ex. 3.04 provides the following:

- The cost data together with each account as a percentage of the total Accounts 364-367 is provided in columns (A) through (D) of the table.
- Columns (E) and (F) of this table show the allocation of the plant in service costs of each account to two System Loading groups: System Loaded (i.e., System Moderate and High), and System Base. The costs for Accounts 364 and 366 are allocated to System Base; the cost for Account 365 is allocated 24% to System Loaded and 76% to System Base; and the cost for Account 367 is allocated 67% to System Loaded and 33% to System Base. For each of these FERC accounts, allocation factors for System Loaded and System Base are developed by reviewing the description of each cost component in the account to determine a reasonable assignment.
- The allocation results, provided in the last row of columns (G) and (H) of the table in section A, show that for the Shared Distribution Line total cost, 39% is allocated to System Loaded and 61% is allocated to System Base. The cost of each FERC account as a percentage of the total Shared Distribution Line costs and the 39% and 61% allocation results shown in the table in section A are also provided in Table 8 below.

The table in section B shows the further allocation of the 39% System Loaded to the System High category and the System Moderate category based on 77% to 23% feeder

[p. 25]

peak of these two periods. The allocation result for the three System Loading Categories is shown in the table in section C: 30%, 9%, and 61%.

**Table 8: Shared Distribution Line Allocation**

| FERC Account             | Account Description                | % of Total Costs | System Loaded | System Base |
| ------------------------ | ---------------------------------- | ---------------- | ------------- | ----------- |
| 364                      | Poles, Towers, and Fixtures        | 18.4%            | 0%            | 18.4%       |
| 365                      | Overhead Conductors and Devices    | 27.1%            | 6.5%          | 20.6%       |
| 366                      | Underground Conduit                | 6.2%             | 0%            | 6.2%        |
| 367                      | Underground Conductors and Devices | 48.3%            | 32.4%         | 15.9%       |
| Shared Distribution Line |                                    | 100%             | 39%           | 61%         |

**Q.** How did you develop the kWhs by TOU distribution period in Table 2?

<!-- EPON: profile,bill-comparison — period kWh shares come from the 2021 hourly load profile of the AVERAGE customer in each delivery class (8,760 hours), scaled to 2026 billed kWh; no profile for individual electrified homes -->

**A.** The kWhs by TOU distribution period for each residential delivery class is developed by grouping hourly kWhs of the average customers in the delivery class for the 8,760 hours in the TOU periods, computing the percentages, and allocating the annual amount of kWh billing units in the TOU periods based on the computed percentages. An illustrative example of the development of kWhs by distribution periods is provided in the 5_DTOU kWhs tab of ComEd Ex. 3.04. In this tab, the 2026 annual billed kWhs by delivery class from ComEd Ex. 2.02 are presented in the table starting in section A, the 2021 average per customer kWhs for the TOU distribution periods by delivery class are presented in the table starting in section B, and the result of the computed 2026 kWhs by TOU distribution period are presented in the table starting in section C.

[p. 26]

## IV. TARIFF REVISIONS REQUIRED TO IMPLEMENT TOU DISTRIBUTION RATES

**Q.** What tariff revisions does ComEd propose in order to implement TOU distribution rates?

<!-- EPON: bundling — tariff mechanics: BESH/RDS/RESS/MRPP revisions; RES must notify ComEd when a customer takes time-variant supply so DTOU is applied -->

**A.** ComEd proposes to revise Rate BESH, Rate RDS, Rate RESS, and Rate MRPP to implement TOU distribution rates. The revisions to Rate BESH describe: (1) that the applicable DFCs in the Monthly Charges section for residential customers are determined on a \$/kWh basis and differentiated by TOU period; (2) the distribution TOU periods; and (3) the informational sheets listing the TOU DFCs. See Sheet No. 32.1 in ComEd Exs. 3.01 and 3.02. The revisions to Rate RDS describe the same information for residential customers taking service from RESs under terms that include TOU or hourly pricing provisions. See Sheet No. 61 in ComEd Exs. 3.01 and 3.02. The revisions to Rate RESS describe a new continuing obligation for RESs to inform ComEd that a customer is taking or terminating service under terms that include the TOU or hourly pricing provisions. See Sheet No. 88.1 in ComEd Exs. 3.01 and 3.02. The revisions to Rate MRPP describe that each time ComEd makes an informational filing updating delivery service charges, ComEd must concurrently make a filing of the Time of Use Distribution Facilities Charges Informational Sheets corresponding to such changes in the delivery service charges. See Sheet No. 627 in ComEd Exs. 3.01 and 3.02.

[p. 27]

## V. TOU DISTRIBUTION RATE IMPACT ON EXISTING RESIDENTIAL RRTP CUSTOMERS

**Q.** Under ComEd's proposed methodology to make the residential delivery TOU applicable to customers that elect RRTP, approximately how many residential customers would be impacted?

<!-- EPON: bill-comparison,bundling,ev-hp — existing RRTP customers (41,270 as of March 2024, incl. 1,141 SFH and 2,424 MFH space-heat accounts) would be transferred to DTOU automatically -->

**A.** Customers on Rider RRTP would be transferred to TOU distribution rates under ComEd's proposed tariff changes, and as of March, 2024, the following number of residential delivery customers were enrolled in Rider RRTP[^2]:

| Delivery Class | Number of RRTP Customers |
| -------------- | ------------------------ |
| SFNH           | 31,234                   |
| MFNH           | 6,471                    |
| SFH            | 1,141                    |
| MFH            | 2,424                    |
| Total          | 41,270                   |

**Q.** Did ComEd perform an analysis to determine bill impacts to these customers had they been on a distribution TOU rate? If so, how was the impact analysis performed?

<!-- EPON: bill-comparison,profile — bill-impact methodology: for each RRTP customer, average monthly DFC computed twice (flat DFC on 2023 average monthly kWh vs. TOU DFC on 2023 average monthly kWh per period); no behavior change assumed; sample limited to customers on RRTP all of 2023 -->

**A.** Yes. ComEd performed a TOU distribution rate impact analysis for the 34,624 customers that had been on RRTP for all of 2023. For each customer, ComEd computed an average monthly DFC portion of the bill twice: (1) using the current flat DFC for the average monthly kWh usage in 2023; and (2) using the presented TOU distribution rate by applying the DFC for each TOU distribution period to the average monthly kWh usage for that period in 2023. Both sets of DFC values are provided in Table 7.

[p. 28]

**Q.** How were the bill impacts determined?

<!-- EPON: bill-comparison — impact = TOU-DFC amount minus flat-DFC amount per customer; negative = savings -->

**A.** To determine the bill impacts, ComEd calculated the average monthly bill difference by subtracting the computed amount under the flat DFC from the computed amount under the TOU DFCs for each RRTP customer. A negative difference means the RRTP customer would have had savings (i.e., would have paid less) under the TOU distribution rate as compared to the current flat rate offering, and a positive difference means the customer would have paid more under the TOU distribution rate, again, as compared to the current flat rate offering.

**Q.** What bill impacts did ComEd observe when applying the TOU distribution rates from Table 7 to the RRTP customers?

**A.** The analysis showed that the vast majority of the customers would have had savings under ComEd's proposed methodology for the TOU rate design. Figures 3 through 6 below show that, had the rate been in effect in 2023, the frequency of the average monthly bill amount difference, in \$1 increments, for the customers taking service under RRTP, the number of accounts with and without savings, and the average per bill impact (negative value means savings, positive value means losses) by delivery class.

[p. 29]

**Figure 3: Hypothetical Average Monthly DFC Bill Impact for SFNH Customers on RRTP**

[DIAGRAM DESCRIPTION: Figure 3: Hypothetical Average Monthly DFC Bill Impact for SFNH Customers on RRTP]

A blue histogram of the number of SFNH RRTP customers (y-axis, count) by range of average monthly DFC (savings) or losses (x-axis "Range of DFC (Savings) or Losses", bins in \$1 increments from an open-ended lowest bin through to an open-ended "> \$5.0" bin; the small rotated tick labels are only partly legible). The distribution is roughly bell-shaped with a long left tail of larger savings, a peak in the bins just on either side of \$0 (the tallest bar sits immediately left of the red line), and a vertical red line marking the class average. An inset summary box reads:

| **Customers on RRTP all of 2023** | Count  | % of Total |
| --------------------------------- | ------ | ---------- |
| Total # of Customers =            | 25,983 |            |
| # of Customers w DTOUR Savings =  | 18,736 | 72%        |
| # of Customers w DTOUR Losses =   | 7,175  | 28%        |
| # of Customers No Change =        | 72     | 0%         |

| **Average Per Bill:**           |             |
| ------------------------------- | ----------- |
| kWh =                           | 842         |
| DFC with DTOUR =                | \$44.57     |
| Fixed DFC =                     | \$46.88     |
| **DFC (Savings) or Losses =**   | **-\$2.31** |
| **% DFC (Savings) or Losses =** | **-5.2%**   |

[→ See original PDF page 31 for visual rendering]

**Figure 4: Hypothetical Average Monthly DFC Bill Impact for MFNH Customers on RRTP**

[DIAGRAM DESCRIPTION: Figure 4: Hypothetical Average Monthly DFC Bill Impact for MFNH Customers on RRTP]

A blue histogram of MFNH RRTP customers by range of average monthly DFC (savings) or losses (same x-axis and \$1 bins as Figure 3). The distribution is tightly concentrated: the two tallest bars are the bins immediately either side of \$0 (savings of \$0–\$1 and losses of \$0–\$1), with a vertical red line at the class average. Summary box:

| **Customers on RRTP all of 2023** | Count | % of Total |
| --------------------------------- | ----- | ---------- |
| Total # of Customers =            | 5,456 |            |
| # of Customers w DTOUR Savings =  | 3,219 | 59%        |
| # of Customers w DTOUR Losses =   | 2,197 | 40%        |
| # of Customers No Change =        | 40    | 1%         |

| **Average Per Bill:**           |             |
| ------------------------------- | ----------- |
| kWh =                           | 388         |
| DFC with DTOUR =                | \$16.15     |
| Fixed DFC =                     | \$16.50     |
| **DFC (Savings) or Losses =**   | **-\$0.35** |
| **% DFC (Savings) or Losses =** | **-2.2%**   |

[→ See original PDF page 31 for visual rendering]

[p. 30]

**Figure 5: Hypothetical Average Monthly DFC Bill Impact for SFH Customers on RRTP**

[DIAGRAM DESCRIPTION: Figure 5: Hypothetical Average Monthly DFC Bill Impact for SFH Customers on RRTP]

A blue histogram of SFH (single family with electric space heat) RRTP customers by range of average monthly DFC (savings) or losses (\$1 bins, same axis as Figure 3). The distribution is roughly symmetric around \$0 with the tallest bar in the bin immediately left of the red average line and a vertical red line at the class average. Summary box:

| **Customers on RRTP all of 2023** | Count | % of Total |
| --------------------------------- | ----- | ---------- |
| Total # of Customers =            | 1,021 |            |
| # of Customers w DTOUR Savings =  | 676   | 66%        |
| # of Customers w DTOUR Losses =   | 344   | 34%        |
| # of Customers No Change =        | 1     | 0%         |

| **Average Per Bill:**           |             |
| ------------------------------- | ----------- |
| kWh =                           | 1,678       |
| DFC with DTOUR =                | \$43.89     |
| Fixed DFC =                     | \$44.58     |
| **DFC (Savings) or Losses =**   | **-\$0.69** |
| **% DFC (Savings) or Losses =** | **-1.6%**   |

[→ See original PDF page 32 for visual rendering]

**Figure 6: Hypothetical Average Monthly DFC Bill Impact for MFH Customers on RRTP**

[DIAGRAM DESCRIPTION: Figure 6: Hypothetical Average Monthly DFC Bill Impact for MFH Customers on RRTP]

A blue histogram of MFH (multi family with electric space heat) RRTP customers by range of average monthly DFC (savings) or losses (\$1 bins). Tightly concentrated, with the two tallest bars the bins immediately either side of \$0 and a vertical red line at the class average. Summary box (note the source labels the first row "Total # of Customers in the Sample"):

| **Customers on RRTP all of 2023**    | Count | % of Total |
| ------------------------------------ | ----- | ---------- |
| Total # of Customers in the Sample = | 2,164 |            |
| # of Customers w DTOUR Savings =     | 1,173 | 54%        |
| # of Customers w DTOUR Losses =      | 981   | 45%        |
| # of Customers No Change =           | 10    | 0%         |

| **Average Per Bill:**           |             |
| ------------------------------- | ----------- |
| kWh =                           | 817         |
| DFC with DTOUR =                | \$20.53     |
| Fixed DFC =                     | \$20.64     |
| **DFC (Savings) or Losses =**   | **-\$0.11** |
| **% DFC (Savings) or Losses =** | **-0.5%**   |

[→ See original PDF page 32 for visual rendering]

[p. 31]

**Q.** Does the data above show that most customers on RRTP would have a lower monthly bill on a TOU distribution rate?

<!-- EPON: bill-comparison,ev-hp — results by class: SFNH 72% save (avg $2.31/mo savings), MFNH 59% ($0.35), SFH (electric space heat) 66% ($0.69), MFH 54% ($0.11); savings shrink and the share of losers grows for the electric-heat classes; sample is RRTP hourly-supply self-selectors with 2023 load, not typical or newly electrified homes -->

**A.** Yes. If ComEd's proposed TOU distribution rates had been applicable to the RRTP customers' usage in 2023, our analysis of this hypothetical shows that most RRTP customers would have had a slightly lower monthly bill under the TOU distribution rate. For RRTP customers in our single-family delivery class who do not use electricity for whole-house heating (i.e., SFNH), 72% would have saved and 28% would have seen losses or no change for a net average savings of \$2.31 per month for all RRTP customers in this delivery class. For those RRTP customers in our multi-family delivery class (i.e., MFNH), 59% would have seen savings and 41% would have seen losses or no change for a net average savings of \$0.35 per month for all RRTP customers in this delivery class. When it comes to customers who use electricity for whole-house heating, 66% of those RRTP customers who are part of the single-family delivery class, SFH, would have seen savings and 34% would have seen losses or no change for a net average savings of \$0.69 per month for all RRTP customers in this delivery class. When we look at those RRTP customers who are part of the multifamily space heat delivery class, 54% would have seen savings and 46% would have seen losses or no change for a net average savings of \$0.11 per month.

<!-- EPON: bill-comparison — aggregate: about $900,000/year net savings to RRTP customers (calculation shown), to be recovered through Rider RBA from the delivery class -->

Overall, based upon these average savings and using the number of RRTP customers for each delivery class in the March 2024 switching report, the net savings for RRTP customers for the four delivery classes for an annual period would be about \$900,000 ((\$2.31 x 31,234 + \$0.35 x 6,471 + \$0.69 x 1,141 + \$0.11 x 2,424) x 12 = \$905,632). Savings or losses such as this, under the application of the TOU distribution

[p. 32]

DFCs, would be recovered under the corresponding delivery service classes' reconciliation under Rider RBA – Revenue Balancing Adjustment ("Rider RBA").

**Q.** Was ComEd able to conduct an analysis on residential customers served by a RES under a time-variant supply rate who would be transferred to the distribution TOU rate?

**A.** No. ComEd does not have data on which RES-supplied customers are currently taking service under a time-variant supply rate.

**Q.** Will residential customers be notified before their distribution rate changes?

**A.** Yes. ComEd will work with its Marketing Team, Elevate Energy, and RESs to develop a plan to notify customers of the change before it would become effective on January 2026 monthly bills. Each RES will need to identify those customers that will be transferred to the new rate.

## VI. TOU RATE IMPACT ON LOW-INCOME CUSTOMERS

**Q.** What is the Commission's directive on the impacts of time-variant rates for low-income customers?

**A.** In the 2023 BE Final Order, the Commission expressed concern about the potential impacts of time-variant rates on low-income customers and directed ComEd to work with Staff and stakeholders to gather more information on the impacts of TOU rates for low-income customers. _Commonwealth Edison Co._, Final Order (Mar. 23, 2023) at 257-258.

[p. 33]

**Q.** How did you define low-income for the purposes of your analyses?

**A.** I used the same information on the population of low-income customers initially presented in ComEd's Low Income Discount proposal, ICC Docket No. 24-0163.

### A. TOU Distribution Rate Low-Income Impacts

**Q.** Did ComEd perform an analysis of the impact of the TOU distribution rate on low-income customers?

**A.** Yes. ComEd performed this analysis, as directed by the Commission, and included this as a topic in the stakeholder workshop process described previously in my testimony.

**Q.** What data did ComEd use to analyze the TOU distribution rate impact on low-income customers?

<!-- EPON: bill-comparison,profile — low-income analysis population: 2023 interval data; ~185,000 income-qualified premises, ~156,000 after exclusions; only ~1,930 on RRTP and ~40 on RTOUPP -->

**A.** ComEd used interval data for the 2023 annual period in the low-income impact analysis. ComEd recently estimated that about 185,000 premises are enrolled in income qualified programs.[^3] From those initially identified, ComEd excluded premises occupied by multiple customers of record (i.e., customers moved in or moved out of the premises) over the course of 2023 or by customer(s) that changed service from a ComEd time-variant rate to another rate or vice versa. ComEd also excluded customers that had unusually long or short billing months in 2023. After making these exclusions, ComEd then analyzed about 156,000 premises occupied by low-income customers. Of these, ComEd determined that, in 2023, about 1,930 low-income customers were taking service under Rate RRTP, about

[p. 34]

40 customers were taking service under Rate RTOUPP, and the other customers were taking service under Rate BES or Rate RDS with a RES.

**Q.** How did ComEd perform the impact analysis?

<!-- EPON: bill-comparison — low-income method: 1,930 RRTP low-income customers; average monthly DFC computed under 2026 flat DFC vs 2026 DTOU rates (Table 7), both applied to 2023 average monthly kWh by period -->

**A.** ComEd performed the TOU distribution rate impact analysis using the data for the 1,930 low-income customers taking service under RRTP by computing an average monthly DFC portion of the bill twice: (1) using the 2026 flat DFC shown in Table 7 applied to the 2023 average monthly kWh usage; and (2) using the proposed 2026 TOU distribution rates from Table 7 applied to the 2023 average monthly kWh usage in each period. This analysis presents two alternative views of 2023 customer usage in order to assess what customer savings would have been, had these rates been in effect.

**Q.** How did ComEd determine the bill impacts?

**A.** To determine the bill impacts, the average monthly bill difference is calculated by subtracting the computed amount under the flat DFC from the computed amount under the TOU DFCs for each low-income customer. A negative difference means the low-income customer would have had savings (i.e., paid less) under the TOU distribution rate as compared to a flat rate, and a positive difference means the customer would have paid more under the TOU distribution rate, again as compared to a flat rate. The blue bars in Figures 7-10 below show the frequency of the average monthly bill amount difference, in \$1 increments, for the low-income customers taking service under RRTP in 2023. A separate figure is provided for each delivery class.

[p. 35]

**Q.** Did ComEd perform the same impact analysis for low-income customers on a non-time-variant rate?

<!-- EPON: bill-comparison — comparison group: equal-sized random sample of low-income customers on flat-supply Rate BES in each delivery class, same DFC calculation (orange bars labeled "BES") -->

**A.** Yes. For each delivery class, ComEd performed the same analysis for an equal number of randomly selected low-income customers from the pool of low-income customers in that delivery class taking service under Rate BES (a non-time-variant rate). Their results are labeled under "BES." The orange bars in Figures 7-10, below, show the frequency of the average monthly DFC amount difference, in the same \$1 increments, for low-income customers taking service under Rate BES in 2023. A separate figure is provided for each delivery class.

**Figure 7: Hypothetical Average Monthly DFC Bill Impact for SFNH Low-Income Customers on RRTP vs. BES**

[DIAGRAM DESCRIPTION: Figure 7: Hypothetical Average Monthly DFC Bill Impact for SFNH Low-Income Customers on RRTP vs. BES]

A clustered bar chart (y-axis count 0–300; x-axis "Range of DFC (Savings) or Losses" in \$1 bins from "< -\$10" to "> \$5.0"), with blue bars for low-income RRTP customers and orange bars for a random sample of low-income Rate BES customers (legend: blue RRTP, orange BES) and a red vertical line near \$0. Both distributions peak around the \$0 to \$1 savings bins (about 240–300 customers per bin) with RRTP shifted slightly toward savings. Inset summary table:

| **Low-income Customers on RRTP or BES all of 2023** | RRTP        | BES (Random Sample) | RRTP (% of Total) | BES (Random Sample) (% of Total) |
| --------------------------------------------------- | ----------- | ------------------- | ----------------- | -------------------------------- |
| Total # of Customers =                              | 1,102       | 1,102               |                   |                                  |
| # of Customers w DTOUR Savings =                    | 836         | 742                 | 76%               | 67%                              |
| # of Customers w DTOUR Losses =                     | 262         | 358                 | 24%               | 32%                              |
| # of Customers No Change =                          | 4           | 2                   | 0%                | 0%                               |
| **Average Per Bill:**                               |             |                     |                   |                                  |
| kWh =                                               | 658         | 636                 |                   |                                  |
| DFC with Distribution TOU Rate =                    | \$35.21     | \$34.68             |                   |                                  |
| Fixed DFC =                                         | \$36.61     | \$35.43             |                   |                                  |
| **DFC (Savings) or Losses =**                       | **-\$1.40** | **-\$0.75**         |                   |                                  |
| **% DFC (Savings) or Losses =**                     | **-4.0%**   | **-2.2%**           |                   |                                  |

[→ See original PDF page 37 for visual rendering]

[p. 36]

**Figure 8: Hypothetical Average Monthly DFC Bill Impact for MFNH Low-Income Customers on RRTP vs. BES**

[DIAGRAM DESCRIPTION: Figure 8: Hypothetical Average Monthly DFC Bill Impact for MFNH Low-Income Customers on RRTP vs. BES]

Clustered bar chart (y-axis count 0–250; same x-axis and legend as Figure 7; blue = RRTP, orange = BES) with a red vertical line near \$0. Both distributions are tightly concentrated in the \$0-to-\$1 savings and \$0-to-\$1 loss bins (about 175–215 customers per bin). Inset summary table:

| **Low-income Customers on RRTP or BES all of 2023** | RRTP        | BES (Random Sample) | RRTP (% of Total) | BES (Random Sample) (% of Total) |
| --------------------------------------------------- | ----------- | ------------------- | ----------------- | -------------------------------- |
| Total # of Customers =                              | 530         | 530                 |                   |                                  |
| # of Customers w DTOUR Savings =                    | 310         | 287                 | 58%               | 54%                              |
| # of Customers w DTOUR Losses =                     | 215         | 243                 | 41%               | 46%                              |
| # of Customers No Change =                          | 5           | -                   | 1%                | 0%                               |
| **Average Per Bill:**                               |             |                     |                   |                                  |
| kWh =                                               | 369         | 369                 |                   |                                  |
| DFC with Distribution TOU Rate =                    | \$15.38     | \$15.57             |                   |                                  |
| Fixed DFC =                                         | \$15.67     | \$15.66             |                   |                                  |
| **DFC (Savings) or Losses =**                       | **-\$0.29** | **-\$0.09**         |                   |                                  |
| **% DFC (Savings) or Losses =**                     | **-1.9%**   | **-0.6%**           |                   |                                  |

[→ See original PDF page 38 for visual rendering]

**Figure 9: Hypothetical Average Monthly DFC Bill Impact for SFH Low-Income Customers on RRTP vs. BES**

[DIAGRAM DESCRIPTION: Figure 9: Hypothetical Average Monthly DFC Bill Impact for SFH Low-Income Customers on RRTP vs. BES]

Clustered bar chart (y-axis count 0–25 approximately, small sample; blue = RRTP, orange = BES) with a red vertical line near \$0. RRTP bars peak in the \$0.01-to-\$1.00 savings bin (about 23 customers); BES bars are more dispersed, including bars out to the \$4–\$5 loss bins. Inset summary table:

| **Low-income Customers on RRTP or BES all of 2023** | RRTP        | BES (Random Sample) | RRTP (% of Total) | BES (Random Sample) (% of Total) |
| --------------------------------------------------- | ----------- | ------------------- | ----------------- | -------------------------------- |
| Total # of Customers =                              | 65          | 65                  |                   |                                  |
| # of Customers w DTOUR Savings =                    | 44          | 36                  | 68%               | 55%                              |
| # of Customers w DTOUR Losses =                     | 21          | 29                  | 32%               | 45%                              |
| # of Customers No Change =                          | -           | -                   | 0%                | 0%                               |
| **Average Per Bill:**                               |             |                     |                   |                                  |
| kWh =                                               | 1,570       | 1,471               |                   |                                  |
| DFC with Distribution TOU Rate =                    | \$41.10     | \$38.90             |                   |                                  |
| Fixed DFC =                                         | \$41.71     | \$39.09             |                   |                                  |
| **DFC (Savings) or Losses =**                       | **-\$0.61** | **-\$0.19**         |                   |                                  |
| **% DFC (Savings) or Losses =**                     | **-1.5%**   | **-0.5%**           |                   |                                  |

[→ See original PDF page 38 for visual rendering]

[p. 37]

**Figure 10: Hypothetical Average Monthly DFC Bill Impact for MFH Low-Income Customers on RRTP vs. BES**

[DIAGRAM DESCRIPTION: Figure 10: Hypothetical Average Monthly DFC Bill Impact for MFH Low-Income Customers on RRTP vs. BES]

Clustered bar chart (y-axis count 0–120; blue = RRTP, orange = BES) with a red vertical line near \$0. Both series are tightly concentrated in the \$0-to-\$1 savings and \$0-to-\$1 loss bins (about 80–108 customers per bin), with small tails. Inset summary table (the percentage row is faint in the source; values below were read at high zoom):

| **Low-income Customers on RRTP or BES all of 2023** | RRTP          | BES (Random Sample) | RRTP (% of Total) | BES (Random Sample) (% of Total) |
| --------------------------------------------------- | ------------- | ------------------- | ----------------- | -------------------------------- |
| Total # of Customers =                              | 234           | 234                 |                   |                                  |
| # of Customers w DTOUR Savings =                    | 137           | 124                 | 59%               | 53%                              |
| # of Customers w DTOUR Losses =                     | 96            | 107                 | 41%               | 46%                              |
| # of Customers No Change =                          | 1             | 3                   | 0%                | 1%                               |
| **Average Per Bill:**                               |               |                     |                   |                                  |
| kWh =                                               | 811           | 766                 |                   |                                  |
| DFC with Distribution TOU Rate =                    | \$20.30       | \$19.33             |                   |                                  |
| Fixed DFC =                                         | \$20.47       | \$19.34             |                   |                                  |
| **DFC (Savings) or Losses =**                       | **-\$0.17**   | **-\$0.01**         |                   |                                  |
| **% DFC (Savings) or Losses =**                     | **-0.8% [?]** | **-0.1% [?]**       |                   |                                  |

[→ See original PDF page 39 for visual rendering]

**Q.** What do you conclude from this analysis?

<!-- EPON: bill-comparison,ev-hp — conclusion: low-income customers would see slightly lower DFC bills under DTOU without changing usage (SFNH RRTP $1.40/mo and 76% saving vs BES $0.75 and 67%; MFNH RRTP $0.29 and 58% vs BES $0.10 and 54%); the text reports only the two no-electric-heat classes even though Figures 9–10 cover SFH/MFH -->

**A.** I conclude that the 2023 usage profile data shows that the majority of low-income customers could benefit from this TOU distribution rate without changing the way they use energy. On average, low-income customers taking service under a TOU distribution rate would have a slightly lower monthly bill without changing usage patterns. In the SFNH delivery class, the computed average monthly savings for the RRTP customers would have been \$1.40 per month, with 76% of those customers saving, and \$0.75 per month for the BES customers, with 67% of those customers saving. In the MFNH delivery class, the computed average monthly savings for the TVR customers would have been \$0.29 per month, with 58% of those customers saving, and \$0.10 [sic; Figure 8 shows -\$0.09] for BES customers, with 54% of those customers saving. Based upon these findings, I conclude that low-income customers do not need to be treated, and should not be treated, differently when it comes

[p. 38]

to making a TOU distribution rate the default rate when a customer elects a time-variant supply rate.

### B. Time-Variant Supply Low-Income Impacts

**Q.** Does ComEd have data related to the impact of Rate RTOUPP on low-income customers?

**A.** Yes. In ComEd's Rate RTOUPP Semi-Annual Compliance Filing #8, filed on April 12, 2024, ComEd provided data on the savings or loss to low-income customers. _See Commonwealth Edison Co._, ICC Docket Nos. 18-1725 / 18-1824 (cons.), Residential Time of Use Pricing Pilot Semi-Annual Compliance Filing #8, [sic; the citation ends here in the source, with no page or exhibit reference]. As shown on page 28 of that report and in Table 9, below, from June 2020 through mid-February 2024 the total customer savings was \$18,892 (negative number in table) for the 117 low-income customers, out of the 1,900 participants. Low-income customers were not restricted from participating in RTOUPP; therefore they should not be restricted from participating in RRTP with the TOU distribution rate.

**Table 9 – Rate RTOUPP (Savings)/Loss for Low Income Customers**

The table is an image in the source (reproduced from the RTOUPP compliance filing). Values read from the rendered image at high zoom; parentheses denote savings (negative values). The "Bills" column is blank in the "Jul 20 – Sep 23" row, and for SFH in Feb-24 both the (savings)/loss cell and the bills cell are blank in the source.

| Month/Year      | SF (Savings)/Loss | SF Bills | MF (Savings)/Loss | MF Bills | SFH (Savings)/Loss | SFH Bills | MFH (Savings)/Loss | MFH Bills | Total (Savings)/Loss | Total Bills |
| --------------- | ----------------- | -------- | ----------------- | -------- | ------------------ | --------- | ------------------ | --------- | -------------------- | ----------- |
| Jul 20 – Sep 23 | \$ (10,451.94)    |          | \$ (3,272.78)     |          | \$ (133.98)        |           | \$ 188.74          |           | \$ (13,669.96)       |             |
| Oct-23          | \$ (1,866.02)     | 88       | \$ (276.75)       | 23       | \$ (9.00)          | 1         | \$ (18.62)         | 2         | \$ (2,170.39)        | 114         |
| Nov-23          | \$ 302.82         | 88       | \$ 32.24          | 23       | \$ 1.51            | 1         | \$ 6.17            | 2         | \$ 342.74            | 114         |
| Dec-23          | \$ (3.81)         | 89       | \$ (16.35)        | 23       | \$ (0.50)          | 1         | \$ 3.30            | 2         | \$ (17.36)           | 115         |
| Jan-24          | \$ (1,544.06)     | 91       | \$ (288.44)       | 23       | \$ (8.97)          | 1         | \$ (13.15)         | 2         | \$ (1,854.62)        | 117         |
| Feb-24          | \$ (1,285.44)     | 57       | \$ (229.32)       | 11       |                    |           | \$ (7.36)          | 1         | \$ (1,522.12)        | 69          |
| Totals          | \$ (14,848.45)    |          | \$ (4,051.40)     |          | \$ (150.94)        |           | \$ 159.08          |           | \$ (18,891.71)       |             |

[→ See original PDF page 40 for visual rendering]

[p. 39]

**Q.** Does ComEd have data related to the impact of Rider RRTP on low-income customers?

<!-- EPON: capacity-mdppec,bill-comparison — contrast of capacity recovery: RRTP/BESH participants pay capacity on kW Peak Load Contribution; RTOUPP and Rate BES recover capacity per kWh -->

**A.** Yes. As indicated earlier in my testimony, ComEd's RRTP program is offered to residential customers that elect to take hourly supply service under Rate BESH. Under this rate option, the participant's \$/kWh supply prices can change each hour based upon the wholesale market price, and the participant pays for their capacity costs based upon their kW-based Peak Load Contribution, consistent with how their capacity costs are incurred. (In contrast, under Rate RTOUPP and Rate BES the capacity costs are recovered based upon a per-kWh rate.)

<!-- EPON: bill-comparison — RRTP low-income supply-side outcome in 2023: 1,683 low-income RRTP participants saved ~$403,000 vs Rate BES; 96.50% saved in an average month (73.29% in January) vs 96.42% (73.09%) for non-low-income; caveat that results track PJM prices and may not predict the future -->

1,683 RRTP participants were identified as low-income customers out of a total average of approximately 40,000 residential customers participating in 2023. Those participants saved approximately \$403,000 when compared to Rate BES. An average of 96.50% of low-income participants saved each month in 2023, with January being the lowest month with 73.29% saving. These percentages are very similar to those seen for non-low-income RRTP participants, with 96.42% of participants saving, on average, throughout all of 2023 and 73.09% saving in January 2023.

I note that ComEd's time-variant supply prices are tied to the PJM wholesale hourly energy market and those prices fluctuate with market conditions and may go extremely low, including even negative, or extremely high for short periods of time. Therefore, previous outcomes may not be indicative of future savings/losses.

[p. 40]

**Q.** Based upon this data, do you conclude that low income customers should be treated similar to non-low-income customers for the proposed TOU distribution rate?

<!-- EPON: profile,ev-hp,midday-peak — Tables 10–11: share of kWh by DTOU period by class; electric-space-heat homes have a flatter shape (Mid-Day Peak 26.16% / 26.18% of kWh vs 30.06% / 27.96% for no-heat homes; Overnight 26.04% / 25.85% vs 23.57% / 25.07%); low-income shapes close to the class averages -->

**A.** Yes. We see that low-income customer energy usage is not noticeably different from non-low-income customer energy usage for time-variant rate purposes. Table 10 provides the percentage of kWhs in the four TOU periods for the entire delivery class population. Table 11 below provides the percentage of kWhs in each period for the roughly 156,000 premises occupied by low-income customers discussed previously in the TOU distribution rate bill impact section of my testimony. There are no dramatic differences.

**Table 10: kWh Distribution by Distribution TOU Period and Delivery Class**

| TOU Period   | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- |
| Morning      | 26.15%                            | 27.09%                           | 29.69%                         | 29.34%                        |
| Mid-Day Peak | 30.06%                            | 27.96%                           | 26.16%                         | 26.18%                        |
| Evening      | 20.22%                            | 19.88%                           | 18.11%                         | 18.63%                        |
| Overnight    | 23.57%                            | 25.07%                           | 26.04%                         | 25.85%                        |
| Total        | 100.00%                           | 100.00%                          | 100.00%                        | 100.00%                       |

**Table 11: kWh Distribution by Distribution TOU Period Low-income Customers**

| TOU Period   | Single Family No Elec. Space Heat | Multi Family No Elec. Space Heat | Single Family Elec. Space Heat | Multi Family Elec. Space Heat |
| ------------ | --------------------------------- | -------------------------------- | ------------------------------ | ----------------------------- |
| Morning      | 26.41%                            | 27.38%                           | 29.60%                         | 29.69%                        |
| Mid-Day Peak | 28.65%                            | 27.50%                           | 25.74%                         | 26.18%                        |
| Evening      | 19.57%                            | 19.15%                           | 18.05%                         | 18.08%                        |
| Overnight    | 25.37%                            | 25.97%                           | 26.61%                         | 26.05%                        |
| Total        | 100.00%                           | 100.00%                          | 100.00%                        | 100.00%                       |

[p. 41]

## VII. NONRESIDENTIAL TOU DISTRIBUTION RATE DESIGN

**Q.** How does ComEd define "small commercial customers" for purposes of considering a TOU distribution rate?

**A.** ComEd defines "small commercial customers" to mean the Small Load Delivery Class, which includes customers with demands less than 100 kW, and the Watt-Hour Delivery Class, which generally includes customers that use less than 2,000 kWhs per month. Note that the Watt-Hour Delivery Class is being phased-out and no new metered customers are allowed in the class except for service points that are exclusively for EV charging stations and those accounts can exceed 100 kW. _Commonwealth Edison Co._, ICC Docket No. 20-0832, Final Order (May 27, 2021) at 23-24. Currently there are 85 accounts utilizing the Watt-Hour Delivery Class for EV charging.

**Q.** Are these Small Load Delivery Class customers currently being billed with a TOU distribution rate?

<!-- EPON: fixed-vs-volumetric,midday-peak — nonresidential MKD window (9:00 A.M.–6:00 P.M. weekdays, ex-NERC holidays) is a demand-charge TOU distribution rate; load outside the window costs $0/kW -->

**A.** Yes. As discussed earlier, the MKD is the highest 30 minute demand for electric power and energy in each monthly billing period established by the customer and delivered by ComEd during the periods, known as the "MKD window" from 9:00 A.M. until 6:00 P.M. on Monday through Friday, except on days designated as holidays by the NERC.

**Q.** Does this TOU distribution rate design already incentivize Small Load customers to shift load outside of the MKD demand window?

**A.** Yes. Apart from the Watt-Hour delivery class, this demand-based MKD billing is applicable to all nonresidential customers, who can minimize their delivery costs by shifting load outside of the MKD demand window, where the kW-demand charge is \$0 for

[p. 42]

the demand level set during that "off peak" period. ComEd has observed several situations where larger nonresidential customers clearly adjust their usage patterns to avoid the MKD demand window. For the Small Load Delivery Class customers, an annual review of the demands found that 53% of these customers had their highest demand level in the MKD period, 40% of these customers had their highest demand outside of the MKD period, and 7% of these customers had the same demand level in both periods. This shows that 40% of the small commercial customers benefited from this TOU distribution rate design.

**Q.** Does ComEd have a proposal for modifying its current TOU distribution rate for small commercial customers or creating another TOU distribution rate for them?

**A.** Not at this time. ComEd does not know what type of rate design small commercial customers may benefit from and be interested in. Because standing up such a program will require investment in billing and marketing, it would be imprudent to develop another time-variant rate prior to obtaining additional feedback from these customers.

**Q.** Can you explain the notification requirement contained in the proposed revisions to Rate RESS?

**A.** Yes. There is currently no way for ComEd to know if a RES-supplied customer, residential or nonresidential, is taking service under a time-variant rate. ComEd's proposed revisions to Rate RESS will require notification from RESs for both residential and nonresidential customers supplied by the RES under time-variant supply rates. See ComEd Ex. 3.01. Requiring notifications for nonresidential customers in addition to residential customers will allow ComEd to have data on the number of time-variant nonresidential customers that may be interested in alternative TOU distribution rates. This information will enable

[p. 43]

ComEd to potentially query these customers regarding their desire for alternative TOU distribution rates as part of collecting the feedback that I mentioned above.

**Q.** Should ComEd follow the same rate design methodology for small commercial customers as presented for the residential delivery classes with a kWh-based DFC?

<!-- EPON: fixed-vs-volumetric,goal — ComEd's rationale that kW-based charges are the right cost-causation measure for nonresidential customers (equipment is built for maximum kW demand, not kWh), yet kWh-based DFCs are used for residential TOU -->

**A.** No. Changing to a kWh-based DFC would conflict with prior Commission order to recognize that the kW-based demand is the most appropriate use of the delivery system for these nonresidential customers with the phasing out of most customers in the Watt-hour Delivery Class. It is clear that the kW-based rate is the most appropriate way to measure a customer's use of the system since the distribution equipment (e.g., distribution transformer, feeder or substation) is built to accommodate the maximum demand on the system, which is based upon kW demand, and not the volume or usage over time on the system, which is measured in kWh usage. Since the vast majority of nonresidential customers are already billed that way, moving to a kWh-based charge would be regressive. With the exception of EV charging stations, the Commission already adopted a plan in the 2020 RDI to move all metered nonresidential customers to kW-based delivery charges with the phase-out of metered customers in the Watt-Hour Delivery Class. _Commonwealth Edison Co._, ICC Docket No. 20-0832, Final Order (May 27, 2021) at 23-24; _Commonwealth Edison Co._, ICC Docket Nos. 22-0432 / 22-0442 (cons.), Final Order (Mar. 23, 2023) at 246.

[p. 44]

**Q.** Can ComEd use its existing TOU distribution rate to better educate its nonresidential customers regarding the MKD demand window and potentially encourage load shifting and lower bills?

**A.** Yes. In order to help customers understand that only usage during the MKD billing window (i.e., peak period) is used to calculate a nonresidential customer's DFCs, ComEd proposes to:

- Expand the description in the bill line item providing the calculation supporting the DFC charge and clearly identifying the peak time period to which the charge is applicable; and
- Add a new line to the bill for all nonresidential customers (other than Watt-Hour, which has a kWh DFC) showing their Off-Peak Period kW demand, which would reflect that customer's kW-based demand during the period 6 pm – 9 am, Monday through Friday, excluding holidays, and all day on weekends, multiplied by a rate of \$0/kW. This would more clearly show that only the usage during the MKD billing window (i.e., peak period) is used to bill the customer for use of the delivery system and higher demand levels in the off-peak will not have additional costs.

## VIII. ELECTRIC VEHICLE CREDITS FOR TOU ENROLLMENT

**Q.** How does ComEd propose to provide incentives to residential EV owners?

<!-- EPON: ev-hp,lockout,goal — Rider EVEN: $2/month enrollment credit for up to 24 monthly billing periods when an EV owner signs up for a supply rate paired with DTOU (ends if customer leaves eligible rate or moves) -->

**A.** ComEd is proposing Rider EVEN (ComEd Ex. 3.06), which would provide for monthly enrollment incentive credits of \$2 per month, for up to 24 monthly billing periods, when a residential customer signs up for a supply rate paired with the TOU distribution rate and

[p. 45]

identifies themself as an EV owner. The incentive credit would end if the customer ceases to take service under an eligible rate or moves from the premises they initially enrolled in.

<!-- EPON: ev-hp — Rider EVEN additional $2/month credit (24 months) per additional EV registered at the address while on the paired rate; credits appear as a Miscellaneous Credit and flow through Rider RBA as other revenues -->

Rider EVEN also provides for additional monthly incentive credits of \$2 per month, for up to 24 monthly billing periods, when the residential customer registers an additional EV at their address while on a supply rate paired with the TOU distribution rate. The credits would appear on a customer's regular monthly bill as a Miscellaneous Credit and flow through the Revenue Balancing Adjustment Amount as other revenues in Rider RBA.

**Q.** If a customer moves to a new premises within the ComEd service territory, can the customer subsequently receive another incentive for the same EV at the new premises?

**A.** Yes. A customer could receive an additional 24-monthly billing period credits if they enroll in, and remain enrolled in, an eligible supply rate paired with the TOU distribution rate at the new premises. This is to incentivize customers to continue to charge their vehicle under a time-variant rate at the new premises.

## IX. SUPPLY TOU RATES

**Q.** Is ComEd proposing a new residential supply TOU tariff at this time?

**A.** No, this is a delivery proceeding and ComEd is not introducing a supply tariff.

## X. CONCLUSION

**Q.** Does that conclude your direct testimony?

**A.** Yes, it does.

---

## Footnotes

[^1]: The requirement to take service under Rate BESH is described in Sheet Nos. 248.1 and 248.4 of Rider DG REBATE – Renewable Energy Distributed Generation Rebate in ComEd's Schedule of Rates. (Testimony p. 8.)

[^2]: The ICC switching report is available at [ICC Electric Switching Statistics](https://www.icc.illinois.gov/industry-reports/electric-switching-statistics). (Testimony p. 27.)

[^3]: Verified Petition for Approval of Low-Income Discount Proposal Under Section 9-241 of the Public Utilities Act. ICC Docket No. 24-0163. (filed on March 11, 2024) (ComEd's low-income discount filing; direct testimony of G. Michael Martin, ComEd Ex. 2.0, at 5:83-6:95). (Testimony p. 33.)
