# Illinois Time-of-Use Rates: ComEd Rate BEST / DTOU and Ameren Rider STOU

Reference for agents working on Illinois heat pump rate design, testimony, or CAIRO inputs that touch time-of-use (TOU) rates. It consolidates what the Illinois sources in `context/sources/il_hp_rates/tou/` say about the TOU rates that exist (or were ordered) in Illinois, in a form you can look facts up in without re-reading ~1 MB of orders and tariffs.

**How to use this file.** Section 1 is a fact sheet (tables and one YAML block) you can lift values from. Sections 2–5 explain each offering and why it is designed the way it is. Section 6 lists what is **not** in the sources, so you do not invent it. Every number below is tagged with its source file; if a value is derived or inferred rather than quoted, the text says so. Do not treat illustrative rates (Section 4.4) as tariffed rates.

**Source files** (all under `context/sources/il_hp_rates/tou/`):

| Short name         | File                                                                     | What it is                                                                                 |
| ------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| Statute            | `il_statute_220_ilcs_5_16-107_8_time_of_use_pricing.md`                  | Statute requiring utilities to offer a market-based TOU supply rate                        |
| Final Order        | `icc_24-0378_final_order_part_1.md`, `icc_24-0378_final_order_part_2.md` | ICC Docket 24-0378 order (Jan 16, 2025); Part 2 §VI.E is the DTOU, §VI.F the STOU question |
| Order on Rehearing | `icc_24-0378_order_on_rehearing.md`                                      | Approves ComEd Rate BEST (Jul 17, 2025)                                                    |
| McCann Ex. 1.0     | `icc_24-0378_direct_testimony_cub_edf_mccann_ex_1_0.md`                  | CUB/EDF direct on DTOU design (Jul 24, 2024)                                               |
| McCann Ex. 4.0     | `icc_24-0378_rehearing_testimony_cub_edf_mccann_ex_4_0.md`               | CUB/EDF rehearing testimony on STOU design (Apr 29, 2025)                                  |
| Ameren filing      | `icc_erm_26-175_ameren_rider_stou_compliance_tariff.md`                  | Ameren Illinois Rider STOU compliance tariff (filed Sep 29, 2026)                          |
| ComEd filing       | `icc_erm_26-176_comed_rate_best_nonresidential_compliance_tariff.md`     | ComEd Rate BEST nonresidential-availability tariff sheets (filed Sep 29, 2026)             |

---

## 1. Fact sheet

### 1.1 What offerings exist

| Offering                                                             | Utility         | Time-varies                                                              | Status (per sources)                                                                                                                         | Primary source                    |
| -------------------------------------------------------------------- | --------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| **DTOU** (Distribution Time of Use)                                  | ComEd           | Delivery only (the Distribution Facilities Charge, DFC)                  | Approved Jan 16, 2025 as a separate **opt-in** rate; implemented by changing DFCs inside existing rates, not as a separate tariff            | Final Order Pt. 2 §VI.E           |
| **Rate BEST** (Basic Electric Service Time of Use Pricing)           | ComEd           | Supply **and** delivery (bundled STOU + DTOU)                            | Approved Jul 17, 2025; residential from the **June 2026** billing period; eligible nonresidential from the **January 2028** billing period   | Order on Rehearing; ComEd filing  |
| **Rider STOU** (Supply Time-of-Use), service classes STOU-1 / STOU-2 | Ameren Illinois | Supply only (energy, capacity, and transmission, all in the supply rate) | Tariff filed Sep 29, 2026, effective **Nov 13, 2026**, opt-in                                                                                | Ameren filing                     |
| Rate BESH (hourly pricing) / Rider RTP                               | ComEd / Ameren  | Real-time supply price                                                   | Existing; **not** TOU, but the benchmark TOU is compared with and shares pricing machinery with                                              | Order on Rehearing; Ameren filing |
| RTOUPP (Residential TOU Pricing Pilot)                               | ComEd           | Supply                                                                   | Four-year pilot, limited to about 1,900 customers at a time; **expired**; its results are the empirical basis for CUB/EDF's design arguments | McCann Ex. 4.0                    |

### 1.2 ComEd TOU periods (DTOU and Rate BEST use the same four periods)

All times are **Central Prevailing Time (CPT)**, **every day** (the tariff does not distinguish weekdays from weekends or holidays), `icc_erm_26-176_comed_rate_best_nonresidential_compliance_tariff.md` sheet 484 and Order on Rehearing §IV.B.1.

| Period           | Hours (CPT)                      | Hours per day | Relative price (all seasons)                                 |
| ---------------- | -------------------------------- | ------------- | ------------------------------------------------------------ |
| Morning          | 6:00 a.m. – 1:00 p.m.            | 7             | Shoulder                                                     |
| **Mid-Day Peak** | 1:00 p.m. – 7:00 p.m.            | 6             | **Highest**; also carries 100% of capacity cost in Rate BEST |
| Evening          | 7:00 p.m. – 9:00 p.m.            | 2             | Shoulder                                                     |
| Overnight        | 9:00 p.m. – 6:00 a.m. (next day) | 9             | **Lowest**                                                   |

History of the period boundaries: ComEd first proposed Overnight 11 p.m.–6 a.m., moved it to 10 p.m. on rebuttal, and the Commission adopted Staff's 9 p.m. start, citing ComEd data that only 0.6% of feeders reach maximum load in the 9 p.m. hour (Final Order Pt. 2 §VI.E.2). The Commission rejected CUB/EDF's request to move the 1 p.m. hour into the Morning period to match RTOUPP.

### 1.3 Seasons

| Utility                          | Summer                                                                     | Non-summer    | Notes                                                                                                                                                                                                                                                                                                                      |
| -------------------------------- | -------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ComEd (DTOU)                     | none                                                                       | none          | The DTOU has **no seasonal variation**; the Commission rejected CUB/EDF's seasonal proposal "in the interest of simplicity and fairness"                                                                                                                                                                                   |
| ComEd (Rate BEST supply charges) | defined in ComEd's General Terms and Conditions (**not in these sources**) | same          | Electricity Charges (MPEC, MDPPEC, EPEC, OPEC) are set separately for summer and non-summer, but the **ordering of periods is the same in both seasons** (Mid-Day Peak highest, Overnight lowest). CUB/EDF testimony uses summer = June–September, non-summer = October–May; assume ComEd matches, but this is unconfirmed |
| Ameren (Rider STOU)              | June – September                                                           | October – May | Defined in the tariff; MISO Planning Year runs June 1 for 12 months                                                                                                                                                                                                                                                        |

### 1.4 Quick-reference YAML

```yaml
comed_dtou:
  decided: 2025-01-16   # ICC Docket 24-0378 Final Order
  time_varies: delivery_only   # the Distribution Facilities Charge (DFC)
  enrollment: opt_in
  seasonal: false
  periods_cpt:
    morning:  {start: "06:00", end: "13:00"}
    mid_day_peak: {start: "13:00", end: "19:00"}
    evening:  {start: "19:00", end: "21:00"}
    overnight: {start: "21:00", end: "06:00"}
  revenue_neutral_within_delivery_class: true
  ev_credit: {rider: EVEN, usd_per_month: 2, max_months: 24, second_ev_extra_usd_per_month: 2}
comed_rate_best:
  approved: 2025-07-17   # Order on Rehearing
  residential_start_billing_period: 2026-06
  nonresidential_start_billing_period: 2028-01   # non-competitively declared customers only
  tariff_sheets_effective: 2026-11-13   # compliance filing, ERM 26-176
  bundled_with: DTOU   # every Rate BEST customer is also a DTOU customer
  periods_cpt: same_as_dtou
  supply_charges: [MPEC, MDPPEC, EPEC, OPEC]   # per season
  capacity_recovery: 100_percent_in_mid_day_peak_kwh_charge   # no demand (kW) charge
  transmission_and_pjm_misc_recovery: separate_flat_kwh_line_item   # see 4.3 for the Jan 2028 change
  price_setting_basis: historical_pjm_real_time_residual_lmp_comed_zone_x_participant_illustrative_profile
  reenrollment_lockout_billing_periods: 12
  requires_ami_interval_meter: true
ameren_rider_stou:
  tariff_effective: 2026-11-13
  classes: {STOU-1: DS-1_residential, STOU-2: DS-2_small_general}
  ineligible: DS-5
  enrollment: opt_in
  periods: [off_peak, intermediate, on_peak]   # hours NOT in tariff; set in informational filings
  seasons: {summer: Jun-Sep, non_summer: Oct-May}
  rate_formula: energy_plus_capacity_plus_transmission_plus_supply_cost_adjustment
  differentiated_by: [rate_class, delivery_voltage]
  informational_filing_cadence: before_June_and_before_October_effective_dates
  period_changes_allowed: annually_with_2_weeks_notice
  reenrollment_lockout_months: 12
  requires_interval_meter: true
```

### 1.5 Price points found in the sources

These are the only dollar values in the sources. **None is the final tariffed Rate BEST or Rider STOU rate** (those are in informational sheets not in the sources; see Section 6).

| Item                                                                            | Value                                                                | Source and caveat                                                                      |
| ------------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| ComEd flat residential DFC, single-family, no electric space heat               | 5.568 ¢/kWh                                                          | Final Order Pt. 2 §VI.E.2 (Staff table, "Fixed DFC")                                   |
| ComEd approved DTOU, same class: Mid-Day Peak                                   | 10.712 ¢/kWh                                                         | McCann Ex. 4.0 §4.2 (describes the approved DTOU)                                      |
| ComEd approved DTOU, same class: Evening                                        | 3.747 ¢/kWh                                                          | Staff table; also consistent with McCann's "186% higher" statement                     |
| ComEd approved DTOU, same class: Overnight                                      | 2.984 ¢/kWh                                                          | Staff table; consistent with "259% higher"                                             |
| ComEd approved DTOU, same class: Morning                                        | about 4.01 ¢/kWh (**derived**)                                       | Back-calculated from McCann's "167% higher than the Morning rate"; not stated directly |
| DTOU Mid-Day Peak vs. other periods                                             | 2.67× Morning, 2.86× Evening, 3.59× Overnight                        | McCann Ex. 4.0 (167% / 186% / 259% higher)                                             |
| ComEd's estimated DTOU savings                                                  | 2.31 dollars per month (about 5% of delivery cost)                   | ELPC/VS/UCS's account of ComEd witness testimony, Final Order Pt. 2 §VI.E.1.c          |
| ComEd direct-case Rate BEST summer Mid-Day Peak (before capacity moved into it) | 4.787 ¢/kWh                                                          | McCann Ex. 4.0; superseded by the compromise proposal                                  |
| PJM capacity charge ComEd proposed for BESH-style recovery                      | 8.37511 dollars per kW-month vs. 0.91048 currently                   | McCann Ex. 4.0; shows the size of the capacity cost now in the Mid-Day Peak charge     |
| Rider EVEN credit                                                               | 2 dollars per month for up to 24 months (+2 dollars for a second EV) | Final Order Pt. 2 §VI.E.7                                                              |
| Rate BEST outreach/education cost impact                                        | about 0.007 dollars per customer per month                           | Order on Rehearing §VI.E                                                               |

---

## 2. The statute: 220 ILCS 5/16-107.8

Enacted by P.A. 104-458 §90-35 (the CRGA Act), effective **June 1, 2026**. Both the Ameren and ComEd filings were made on Sep 29, 2026, which is 120 days after that date, matching the statute's filing deadline.

What it requires of an electric utility with more than 100,000 customers (subsection (h) exempts smaller ones):

- Offer **at least one market-based TOU supply rate** to eligible customers who take supply from the utility, including net-metering customers (whose energy credits are valued at the TOU price for the same period).
- **If more than one tariff is proposed**, at least one has at least three blocks: a **peak** block of consecutive hours best reflecting the highest average system use, an **off-peak** block reflecting the next-highest demand, and a **super-off-peak** block of all other hours. Blocks reflect the hour **and weekday** for which costs are charged.
- Prices come from a stated methodology using **average zonal and capacity prices of PJM and MISO**, with capacity costs set to recover the capacity obligation the utility incurs.
- The rate **includes transmission costs** (network integration transmission service, transmission enhancement, locational reliability).
- Charges may be adjusted **monthly** and time blocks **annually**, with at least **two weeks' notice** to customers.
- A **purchased energy adjustment** fully recovers supply costs; the utility procures in the **day-ahead market**.
- Commission approval within 240 days; **annual report by April 1** (customers by type, usage changes, value to participants and non-participants, recommended modifications); modification investigations capped at 180 days; prudent compliance costs recoverable from eligible retail customers.

Two points worth knowing when you compare the statute to the tariffs: ComEd uses **four** periods and Ameren **three**, so the statute's three-block minimum is met in different ways. ComEd's tariff also sets prices using **historical real-time residual** PJM prices (Section 4.2) while the statute describes day-ahead procurement; the tariff trues up through the purchased electricity adjustment. This file notes the difference but does not take a position on it.

---

## 3. ComEd DTOU (delivery TOU)

**What it is.** A rate structure in which the per-kWh Distribution Facilities Charge varies by the four periods in Section 1.2 instead of being one flat per-kWh number. It does not change supply pricing. Collectively the four DFCs recover the same revenue the flat DFC would for each delivery class, based on average usage for that class.

**Why those periods.** ComEd built the periods from **feeder-peak data** (the share of feeders at their maximum load in each hour), not from customer-behavior analysis. ComEd chose intuitive names (Morning, Mid-Day Peak, Evening, Overnight) over CUB/EDF's price-based names (Off-Peak, Peak, Super-Peak).

**Commission's three design tests** (from the earlier BE Plan 1 Order, restated in the Final Order): (1) the peak/off-peak price difference must be big enough to shift usage without deterring sign-up; (2) rate periods must coincide with the distribution system's on-peak and off-peak periods; (3) there must be an incentive for EV owners, but the rate cannot be EV-only.

**Key rulings in the Final Order (Pt. 2 §VI.E):**

| Issue                                | Ruling                                                                                                                                                                                                                | Main opposing view                                                                                                                                                                                                         |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Overnight start time                 | **9 p.m.**, with other period rates adjusted to stay revenue neutral (Staff's method: spread the difference across Morning and Mid-Day Peak, keeping Morning below the flat DFC)                                      | ComEd proposed 10 p.m.; CUB/EDF supported 10 p.m. and called Staff's 9 p.m. unsupported by analysis                                                                                                                        |
| 1 p.m. hour                          | Stays in Mid-Day Peak                                                                                                                                                                                                 | CUB/EDF and the AG wanted it in Morning to match RTOUPP                                                                                                                                                                    |
| Seasonality                          | **None**                                                                                                                                                                                                              | CUB/EDF: summer Super Peak only, since non-summer loads never approach summer peaks. ComEd and Staff: distribution costs are not seasonal, and a seasonal DTOU would unfairly benefit rooftop-solar net-metering customers |
| Period names and number of rates     | ComEd's four names; four rates                                                                                                                                                                                        | CUB/EDF: three rates (shoulders share one) and cost-based names                                                                                                                                                            |
| Pairing with time-variant supply     | DTOU is a **separate opt-in offering**; it is **not** mandatory for customers who take a time-variant supply rate from an ARES or ComEd                                                                               | ComEd and Staff wanted mandatory pairing; CUB/EDF, the AG and ICEA/RESA opposed it, citing conflicting price signals and low-income risk                                                                                   |
| Revenue allocation to DTOU customers | ComEd must use **actual** post-implementation usage data to determine avoided or deferred distribution investment attributable to DTOU load shifting and pass those savings to customers                              | CUB/EDF wanted forecast savings deducted from the DTOU revenue requirement up front; ComEd said it cannot isolate DTOU effects                                                                                             |
| Tariff structure                     | Update existing rates' DFCs; **no separate DTOU tariff**                                                                                                                                                              | CUB/EDF and ICEA/RESA wanted a separate tariff                                                                                                                                                                             |
| EV incentive (Rider EVEN)            | 2 dollars per month for up to 24 monthly billing periods, plus 2 dollars for a second EV; only condition is staying on the DTOU. The Commission told ComEd to re-examine the level in its next rate design proceeding | CUB/EDF: 463 dollars per year for two years or 9 dollars per month, based on the value of avoided PJM capacity                                                                                                             |

**Education and outreach.** The Final Order directed ComEd to convene stakeholders by Aug 31, 2025 and finish materials by Nov 1, 2025, with advance copies to ARES and Staff, and specific materials for net-metering customers who could enroll in both a flat supply rate and the DTOU.

---

## 4. ComEd Rate BEST (supply + delivery TOU)

### 4.1 What it is and how it came about

Rate BEST is ComEd's **bundled** residential STOU. A customer on Rate BEST pays time-differentiated **supply** charges (Section 4.2) **and** time-differentiated **delivery** (DTOU) charges, both using the same four periods, so the customer tracks one set of time blocks. It is available only as the bundle: every Rate BEST customer is a DTOU customer, but a customer can take DTOU without Rate BEST by pairing it with another supply option.

ComEd did not propose an STOU in the original case. After the Final Order told ComEd to develop a "strawman," ComEd applied for rehearing and **voluntarily proposed Rate BEST** for approval. That is why the Commission found §16-103(e) inapplicable. The Commission approved the **Compromise Proposal** (the version revised after stakeholder input) on Jul 17, 2025.

### 4.2 Charges on a Rate BEST bill

From `icc_erm_26-176_comed_rate_best_nonresidential_compliance_tariff.md` (sheets 487–492.1) and the Order on Rehearing:

| Component                                                        | How it works                                                                                                                                                                                                                                                                                                                                                           |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Customer Charge; Standard Metering Service Charge                | Same as the customer's delivery class                                                                                                                                                                                                                                                                                                                                  |
| Distribution Facilities Charge                                   | **Residential:** TOU-differentiated, four periods (the DTOU). **Nonresidential:** the delivery class's ordinary DFC (per kWh for Watt-hour class; per kW of Maximum Kilowatts Delivered, by voltage level, for Demand class), plus the Primary Voltage Transformer Charge where applicable. Nonresidential delivery is **not** time-differentiated in the filed sheets |
| Illinois Electricity Distribution Tax Charge                     | Per kWh, by delivery class                                                                                                                                                                                                                                                                                                                                             |
| **Electricity Charges** (supply): MPEC, MDPPEC, EPEC, OPEC       | Per-kWh price for Morning, Mid-Day Peak, Evening and Overnight, each set separately for summer and non-summer. Updated each June for the June–May year, and revisable if ComEd finds a better cost match                                                                                                                                                               |
| **PJM Services and Miscellaneous Procurement Components Charge** | Recovers PJM transmission and ancillary costs (including NITS), uncollectible costs, and customer-service and collection-agency costs not in the Electricity Charges. Shown as a separate bill line                                                                                                                                                                    |
| **BEST Purchased Electricity Adjustment Factor (TPEA)**          | True-up in ¢/kWh for over/under-recovery of procurement costs; applied to every kWh                                                                                                                                                                                                                                                                                    |

**Electricity Charge formulas** (`icc_erm_26-176_comed_rate_best_nonresidential_compliance_tariff.md` sheets 488–490). For customer class C (residential or nonresidential), period P, and season S or N:

$$
HENC_{C,P,S/N} = \frac{\sum_{\text{hours in } P}\left[HkW_C \times HLMP\right] \times \frac{1\ \text{MWh}}{1{,}000\ \text{kWh}} \times \left(1 + DLF_C\right)}{E_{C,P,S/N}}
$$

$$
EC_{C,P,S/N} = \left(HENC_{C,P,S/N} + A_{C,P,S/N}\right) \times 100¢/\$ \times SBUF \times ISUF
$$

In plain terms: take the participants' **aggregate illustrative hourly load profile** ($HkW_C$) and the **historical PJM real-time residual locational marginal price for the ComEd Zone** ($HLMP$), multiply hour by hour, gross up for distribution losses ($DLF_C$), and divide by the profile's energy in that period ($E$). That gives the energy cost per kWh the class **would have paid** historically in that period and season. Then add an adjustment ($A$) so the price reflects current or future market conditions and any TPEA true-up, convert to cents, and apply the base and incremental supply **uncollectible factors** ($SBUF$, $ISUF$). For every hourly interval in the **Mid-Day Peak** period, $HENC$ also includes ComEd's PJM **capacity costs**.

**TPEA** (`icc_erm_26-176_comed_rate_best_nonresidential_compliance_tariff.md` sheet 492.1), with accrued expenses AE, accrued revenues AR, automatic balancing AB, adjustment A, and usage U (the amortized quantity may run up to 12 billing periods):

$$
TPEA = \frac{\left[AE - AR + AB + A\right]_{\text{amortized}} + \sum ATPEA}{U} \times \frac{100¢}{\$1}
$$

### 4.3 Design decisions that shaped the final rate

The initial ComEd proposal recovered capacity and part of transmission through **fixed monthly per-kW demand charges** locked in for 12 months based on prior-year peak-hour usage. CUB/EDF (McCann) and ELPC/VS/UCS argued these were opaque, backdoor fixed charges that muted the price signal. The Compromise Proposal, adopted by the Commission, changed three things:

1. **No demand charge for capacity.** 100% of capacity cost is recovered in the **Mid-Day Peak kWh charge** (every ComEd supply rate except BESH already recovers capacity per kWh). McCann argued this also gives an apples-to-apples comparison with the default rate (Rate BES), whose per-kWh price already contains capacity.
2. **Transmission and miscellaneous procurement charges become volumetric.** Per the Order on Rehearing, a **flat, separate per-kWh line item**, not spread into the period prices (spreading them would have added administrative cost).
3. **Mid-Day Peak is the peak all year.** CUB/EDF had wanted the Mid-Day Peak price only in summer (every recent PJM and ComEd system peak fell in summer, 1–7 p.m.). They accepted year-round application as a compromise. Seasonal price **levels** still differ because the supply charges are set by season, but the relative ordering does not change.

**Change written into the Sep 2026 tariff sheets that is not in the Order on Rehearing.** Sheet 492 says that **beginning with the January 2028 billing period**, the kW-based costs for transmission service and other kW-based PJM expenses will be recovered through a **kWh charge applied only to Mid-Day Peak kWh**, shown as its own bill line, while the other kWh-based transmission and PJM costs are recovered through a charge on **all four periods**. The sheet words this for "retail customers" generally (it accompanies nonresidential availability). Whether it also changes residential recovery is **not stated** in the sources; treat the residential treatment after January 2028 as an open question before modeling it.

### 4.4 Illustrative rates (not tariffed)

McCann's Ex. 4.0 design uses a heuristic **3.0 / 1.5 / 1.0** ratio (the same family of ratios the Regulatory Assistance Project and Burbank and Sacramento utilities use) and rolls capacity into the Mid-Day price. It is CUB/EDF's illustration, not what ComEd filed:

| Season and period                    | Rate (¢/kWh) | Ratio |
| ------------------------------------ | -----------: | ----: |
| Summer Mid-Day                       |       12.450 |   3.0 |
| Summer Morning, Evening              |        6.225 |   1.5 |
| Non-summer Mid-Day, Morning, Evening |        6.225 |   1.5 |
| Overnight (both seasons)             |        4.150 |   1.0 |

McCann's Ex. 1.0 also gives illustrative **DTOU** rates under his own (not adopted) periods, in dollars per kWh, by housing class: Peak–Morning and Peak–Evening 0.03860 (single-family, no electric space heat), Super Peak–Mid-day 0.24323, Off-Peak–Overnight 0.02984. Those predate the Commission's final periods and Staff's revenue-neutrality adjustment; use the approved values in Section 1.5 instead.

### 4.5 Eligibility, enrollment and customer protections

- **Residential** customers from the June 2026 billing period; **nonresidential** customers in the Watt-hour or Demand customer groups from the January 2028 billing period. **Competitively declared** customers are excluded.
- Requires an **AMI interval meter** at every metered point. Customers on **Rider NAM (non-AMI metering)** are ineligible.
- **Net metering:** the tariff text excludes customers served under Rider POGNM classifications NM1–NM4 (residential) or NM1–NM6, NM11, NM12 (nonresidential). The Order on Rehearing describes the same issue as a **legacy vs. non-legacy** distinction: **legacy** customers (interconnected on or before Dec 31, 2024, with full retail-rate netting) must move to **non-legacy** status to take Rate BEST, while non-legacy customers (interconnected on or after Jan 1, 2025) are eligible and receive supply credits by period. The sources do not map the NM classifications to legacy status. The Statute separately values net-metering energy credits at the TOU period price.
- **Low Income Discount** customers can take Rate BEST. McCann argues the discount applied to the combined bill preserves the cents-per-kWh gaps between periods and so preserves the price signal.
- After terminating, a customer cannot return for **12 monthly billing periods** (an anti-arbitrage rule that matches BESH and RTOUPP).
- Enrollment goes through ComEd's enrollment process; to leave, the customer enrolls in the other tariff.

### 4.6 Cost recovery and other directives

- **Administrative costs** (mainly IT) are recovered through the **delivery services rate** across all customers, not from Rate BEST participants alone; the Commission reasoned that peak-load reduction benefits all customers and that charging early adopters would deter enrollment. **Supply procurement costs** pass through directly to STOU customers.
- Because the Integrated Distribution Company (IDC) Rules restrict utility marketing of supply, ComEd had to petition to modify its **IDC Implementation Plan** (or seek clarification that no change is needed) by **Jan 1, 2026**, once its consumer materials were developed, and make a **compliance filing within 25 business days** of the Order on Rehearing.
- The Commission is separately reviewing how ComEd allocates costs between supply and delivery (Staff report due January 2026); that review could force changes to Rate BEST and other tariffs.
- **Annual report** by April 1 in Docket 24-0378, beginning in **2028**; an annual audit and a proceeding to reconcile errors also begin in 2028.
- **Retail competition:** RESs began receiving interval data in June 2025 and had about 12 months to develop their own STOUs; ICEA/RESA's tying and competition objections were rejected.

---

## 5. Ameren Illinois Rider STOU

Source: `icc_erm_26-175_ameren_rider_stou_compliance_tariff.md`. Filed Sep 29, 2026; effective **Nov 13, 2026**. The filing also updates Customer Terms and Conditions, Rider PER (purchased electricity), Rider EUA (uncollectibles) and Rider TS (transmission) to support the STOU.

### 5.1 Availability and switching

- Available to **DS-1** (residential) and **DS-2** (small general) customers with the **necessary interval metering**; classes are **STOU-1** (DS-1) and **STOU-2** (DS-2). **DS-5** is not eligible.
- A customer who ends service under STOU, or under Rider RTP, cannot return to that rider for **12 months**. Customers may switch BGS (default basic generation service) ↔ STOU and RTP ↔ STOU subject to notice, with a 10-calendar-day rescission window when moving from STOU or RTP back to BGS.
- A customer who defaults or switches to BGS has until the end of the second full billing month to elect RTP, STOU or a RES, or must stay on BGS for 12 months.
- New DS-1 and DS-2 applicants may choose BGS, RTP or STOU, or a RES.
- Delivery rates are the customer's ordinary DS-1 or DS-2 rates. The filing describes STOU "in combination with" the DS and TS tariffs as a bundled option; **no time-varying delivery rate is described** in the filed sheets (unlike ComEd).

### 5.2 Periods and seasons

Three periods: **off-peak, intermediate, on-peak**. The tariff does **not** state the hours. They are published in the **Rider STOU informational filing**, which Ameren must file at least two weeks before the June effective date and again before October (and may revise if it improves cost matching). Ameren may **change the periods annually** to better reflect system peaks, with two weeks' notice. Seasons: Summer = June–September; Non-Summer = October–May. Rates are differentiated by **rate class and delivery voltage** (secondary, primary, high voltage).

### 5.3 How the rate is built

For period P, voltage V, season S or N (¢/kWh, rounded to the thousandth of a cent):

$$
ESTOUR_{P,V,S/N} = EP_{P,S/N} \times DLA_V
$$

$$
CSTOUR_{P,S/N} = \frac{CC_{S/N} \times PLC_{S/N} \times \text{Seasonal Days}_{S/N}}{PkWh_{S/N}}
$$

$$
STOUR_{P,V,S/N} = ESTOUR_{P,V,S/N} + CSTOUR_{P,S/N} + TSC_{STOU}
$$

| Term         | Meaning                                                                                                                                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| $EP$         | **Estimated price:** average of the **forecast day-ahead market** price for the season and period, plus applicable MISO revenue sufficiency guarantee, revenue neutrality uplift, ancillary and other market settlement costs |
| $DLA_V$      | Distribution loss adjustment by voltage level                                                                                                                                                                                 |
| $CC$         | Capacity cost, as a **daily** cost per unit of PLC demand, procured through MISO markets                                                                                                                                      |
| $PLC$        | Peak Load Contribution demand. **Initially the sum for all customers in the delivery class** (not just enrollees); later set to the customers assumed to take STOU service in the MISO Planning Year                          |
| $PkWh$       | Forecast **peak-period** energy (kWh) for those customers in the season                                                                                                                                                       |
| $TSC_{STOU}$ | Transmission charge, **applied to all kWh in the on-peak block**                                                                                                                                                              |

The capacity formula divides by **peak-period** kWh, so capacity cost is evidently recovered on on-peak kWh; the tariff text does not say so explicitly, so treat this as an inference. A **Supply Cost Adjustment** (procurement, working capital, uncollectibles) and the monthly **Purchased Electricity Adjustment (PEA)** from Rider PER also apply to STOU kWh.

**Transmission** (Rider TS section D): $TSC_{STOU} = TSC_n \times TM$, where $TSC_n$ is the Transmission Service Charge for non-interval-metered customers and $TM$ is the **Transmission Multiplier**: the ratio of total kWh among STOU-eligible DS-1 (and, separately, DS-2) customers to forecast **on-peak** kWh. This concentrates transmission cost recovery into the on-peak period.

**PEA** (Rider PER), in ¢/kWh: $PEA = \frac{\{[AE - AR + AB + A]_{\text{amortized}} + SA\}}{U} \times \frac{100¢}{\$1}$, with a settlement adjustment SA that currently includes a 33,530,000 dollar refund tied to FERC Docket ER25-3069.

### 5.4 Reporting and review

- **Annual report by April 1**, starting the first calendar year STOU is in effect for a full year, with the same four items as the statute.
- Within **three years**, Ameren must report on whether to keep setting prices from **all** customers in the delivery class or to use **actual enrolled-customer data**, and file conforming tariffs if it recommends a change.
- Ameren may recover all prudent costs of complying with §16-107.8, including market participation costs.

---

## 6. Side-by-side comparison

| Feature                | ComEd Rate BEST (+ DTOU)                                                                                                                                          | Ameren Rider STOU                                                                        |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Wholesale market       | PJM                                                                                                                                                               | MISO                                                                                     |
| Periods                | 4: Morning, Mid-Day Peak, Evening, Overnight (fixed in the tariff)                                                                                                | 3: off-peak, intermediate, on-peak (hours in informational filings; may change annually) |
| Seasonal rates         | Supply prices by season; period ordering unchanged; DTOU not seasonal                                                                                             | Summer (Jun–Sep) and non-summer (Oct–May)                                                |
| Delivery rate          | TOU for residential (DTOU, bundled)                                                                                                                               | Ordinary DS-1 / DS-2 delivery rates                                                      |
| Capacity recovery      | 100% in Mid-Day Peak per-kWh charge; no demand charge                                                                                                             | Daily capacity cost × PLC × days ÷ peak kWh, in the capacity component                   |
| Transmission recovery  | Flat per-kWh line item; from Jan 2028 a Mid-Day-Peak-kWh charge for kW-based costs plus an all-period charge for the rest (residential treatment to be confirmed) | On-peak kWh only, via transmission multiplier                                            |
| Energy price basis     | Historical PJM real-time residual LMP × illustrative participant profile × losses, plus adjustments                                                               | Forecast day-ahead price by season and period × loss factor                              |
| Price update cadence   | Annual (June), revisable                                                                                                                                          | Informational filings before June and October, revisable                                 |
| Eligible customers     | Residential (June 2026); nonresidential, non-competitively declared (Jan 2028)                                                                                    | DS-1 and DS-2 only; DS-5 excluded                                                        |
| Re-entry after leaving | 12 monthly billing periods                                                                                                                                        | 12 months                                                                                |
| Admin cost recovery    | Delivery rates (all customers)                                                                                                                                    | Costs recoverable through the rider and PEA                                              |
| Annual report          | April 1, starting 2028                                                                                                                                            | April 1, starting first full year in effect                                              |

---

## 7. What is not in the sources (do not guess)

- **Ameren STOU period hours and rates.** Only the formula and the three period names are filed; the hours and ¢/kWh values are in the informational filing, which is not in `context/`.
- **ComEd's final tariffed Rate BEST ¢/kWh values** by period and season, and the final **DTOU rates for classes other than single-family, no electric space heat** (multi-family and the two electric-space-heat classes). McCann's tables are illustrative only.
- **ComEd's own definition of summer and non-summer** for Rate BEST (it is in ComEd's General Terms and Conditions).
- **Whether the January 2028 transmission change in sheet 492 applies to residential customers.**
- Any **enrollment counts or bill-impact estimates** for either utility; ComEd's only quantified DTOU savings figure is the 2.31 dollars per month cited in the record.
- The **Staff report** on supply/delivery cost allocation (due January 2026) and any resulting changes to Rate BEST.

---

## 8. Modeling notes for rate-design-platform and report work

- A ComEd TOU tariff for CAIRO needs **4 periods × 2 seasons of supply charges plus 4 DTOU delivery charges**, a flat per-kWh transmission/PJM line item, and the TPEA. Period boundaries are on **every day**; convert CPT consistently ("Central Prevailing Time" follows daylight saving). The tariff does not exclude weekends or holidays.
- Because capacity sits entirely in the Mid-Day Peak price, ComEd's Mid-Day price carries both energy and capacity signals; do not add a separate capacity term when pricing a Rate BEST bill.
- For Ameren, you cannot build a complete STOU tariff from the sources alone. You can state the formula structure and cite that the hours come from the informational filing.
- DTOU is **revenue neutral within each delivery class**, designed on average class usage. CUB/EDF's characterization is that ComEd's allocation assumes **no load shifting**; ComEd's position was that it cannot isolate DTOU effects and that customers already get the benefit through lower period charges. On those terms, a DTOU customer who does not shift pays roughly what a flat-rate customer pays, and one who shifts out of Mid-Day Peak pays less. CUB/EDF argues this overcharges DTOU customers as a group; the Commission instead ordered a later true-up from actual data.
- The price signal is strongest in the supply charge: the Illinois record (ELPC/VS/UCS) notes delivery is only about one-third of the bill, which is why a supply-side STOU bundled with DTOU matters for the size of the incentive.

---

## 9. Glossary

| Term                     | Meaning                                                                                                                                                                                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DTOU                     | ComEd Distribution Time of Use rate (time-varying DFC)                                                                                                                                                                                                                      |
| STOU                     | Supply time-of-use rate                                                                                                                                                                                                                                                     |
| BEST                     | ComEd Rate BEST, Basic Electric Service Time of Use Pricing (bundled STOU + DTOU)                                                                                                                                                                                           |
| BES / BESH               | ComEd's default fixed supply rate / its hourly (real-time) supply rate                                                                                                                                                                                                      |
| RTOUPP                   | ComEd's expired Residential TOU Pricing Pilot                                                                                                                                                                                                                               |
| BGS / RTP / HSS          | Ameren Basic Generation Service (default) / Real-Time Pricing / Hourly Supply Service                                                                                                                                                                                       |
| DFC                      | Distribution Facilities Charge                                                                                                                                                                                                                                              |
| MPEC, MDPPEC, EPEC, OPEC | Morning, Mid-Day Peak, Evening, Overnight Period Electricity Charges                                                                                                                                                                                                        |
| HENC, EC                 | Historical Energy Charge, and the resulting Electricity Charge                                                                                                                                                                                                              |
| TPEA / PEA               | ComEd BEST / Ameren Purchased Electricity Adjustment true-ups                                                                                                                                                                                                               |
| PLC                      | Peak Load Contribution (a customer's share of the system peak that sets capacity obligation)                                                                                                                                                                                |
| TSC, TM                  | Ameren Transmission Service Charge and Transmission Multiplier                                                                                                                                                                                                              |
| NITS                     | Network Integration Transmission Service                                                                                                                                                                                                                                    |
| AMI                      | Advanced metering infrastructure (interval meter)                                                                                                                                                                                                                           |
| ARES / RES               | Alternative retail electric supplier                                                                                                                                                                                                                                        |
| LID                      | ComEd Low Income Discount                                                                                                                                                                                                                                                   |
| IDC                      | Integrated Distribution Company (83 Ill. Adm. Code 452). ComEd operates as an IDC, and the IDC Rules limit a utility's promotion and marketing of electricity supply, which is why ComEd's TOU outreach materials needed an IDC Implementation Plan filing or clarification |
| CPT                      | Central Prevailing Time                                                                                                                                                                                                                                                     |
| CUB/EDF                  | Citizens Utility Board and Environmental Defense Fund (witness Richard McCann)                                                                                                                                                                                              |
| ELPC/VS/UCS              | Environmental Law & Policy Center, Vote Solar, Union of Concerned Scientists                                                                                                                                                                                                |
| ICEA/RESA                | Illinois Competitive Energy Association / Retail Energy Supply Association                                                                                                                                                                                                  |
