# Rate catalogs: electric heating, time-varying, EV, and low-income rates

**Last updated:** 2026-10-27. This directory is our central knowledge base of retail electric rates and programs across the Northeast and Mid-Atlantic (Maine to West Virginia). For each rate or program it records what it is, **which docket defined it**, and **where we learned about it**. The goal is to let us find the defining docket for any rate and pull the workbooks and filings from it.

The starting point was NEEP's survey, [_Modern Rate Design in the Northeast_](../../sources/neep_modern_rate_design.md) (Appendix A, C, and E). NEEP gives almost no docket numbers, so the catalogs go to the orders, tariffs, and testimony themselves where we could reach them, and flag where we could not.

## Files

| File                                                                                   | Covers                                                                                                                                                   | Entries |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| [`electric_heating_and_heat_pump_rates.md`](electric_heating_and_heat_pump_rates.md)   | Heat pump rates, heat-pump-oriented rates open to all (ConEd Steady Use Rate), and legacy electric-heating rates                                         | 19      |
| [`time_varying_rates.md`](time_varying_rates.md)                                       | Whole-home TOU, seasonal-only, demand-charge, critical peak pricing, peak-time and other rebates, legacy water-heating and battery demand-response rates | 95      |
| [`ev_rates.md`](ev_rates.md)                                                           | Residential EV TOU, separately metered EV rates, off-peak charging rebates, managed charging, commercial EV demand-charge relief                         | 61      |
| [`low_income_and_affordability_programs.md`](low_income_and_affordability_programs.md) | Bill discounts, percentage-of-income plans, arrearage management, budget billing, customer-relief funds, LIHEAP and state assistance                     | 85      |

Each of the three newer files has an index table at the top (state, offering, category, short defining docket, docket status), then state sections with one entry per offering: category, status, design, defining docket, current governing docket, where we learned it, whether NEEP lists it, and notes.

## Conventions shared by all four files

- **Defining docket vs. current governing docket.** Utilities re-file tariffs in every rate case, so the docket on today's tariff footer is usually the current rate case, not the proceeding that created the rate. "Not found" means we have not located the defining docket, not that none exists. Many legacy rates (for example JCP&L RT, PSE&G RLM, BGE RL) predate the restructuring era and have no easily findable creating order.
- **Evidence levels.** _Primary_ (we read the order, testimony, tariff, or statute), _Official page_ (utility or agency web page), _Search summary_ (only a search snippet or synthesis; spot-check before relying on it).
- **Docket status** in the index tables: _found_, _partial_ (a revising docket is confirmed but not the original), _unverified_ (secondary source or inference), _not found_. Counts for the three newer files:

| File                                       | Found | Partial | Unverified | Not found |
| ------------------------------------------ | ----- | ------- | ---------- | --------- |
| `time_varying_rates.md`                    | 58    | 2       | 4          | 31        |
| `ev_rates.md`                              | 55    | 0       | 2          | 4         |
| `low_income_and_affordability_programs.md` | 51    | 4       | 4          | 26        |

- **Docket formats by regulator:** MA D.P.U. NN-NN; ME MPUC YYYY-NNNNN; NH DE YY-NNN; VT YY-NNNN-TF (tariff) or -PET (petition); CT PURA YY-MM-NN (older DPUC dockets use YY-MM-NNRENN suffixes); RI RIPUC numeric (4770) or YY-NN-GE/EL/EE; NY PSC YY-E-NNNN; NJ BPU ER/EO/QO + digits; PA PUC R- (rate case), P- (petition), M- (investigation) + year + digits; MD PSC Case NNNN or PC NN; DC Formal Case NNNN; DE PSC Docket YY-NNNN; WV PSC Case YY-NNNN-E-XX.

## Pulling documents from these dockets

Where the next step is to download workbooks and filings, note these access limits that the research ran into:

- **NY DPS** Matter Master pages do not render document lists without JavaScript. Browse `https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=<case>` interactively.
- **NH PUC** (`puc.nh.gov`) returns 403 to `curl`; order text was reachable only through search page capture.
- **Maine PUC** case pages did not render in WebFetch; `cmpco.com` timed out from the research host.
- **WV PSC**: no e-docket page was read; all WV case numbers come from tariffs, public notices, and one order PDF, so verify them in the WV PSC docket system.
- **Vermont ePUC** documents are reachable by `downloadfile` URLs, which are cited in the entries.
- Maryland PSC documents: see the [`mdpuc-documents` skill](../../../.cursor/skills/mdpuc-documents/SKILL.md).

## What NEEP covers that these files do not

NEEP also surveys water heating (controlled and off-peak water heating rates), battery demand response, and net metering. These are only incidental here: legacy controlled water heating and battery demand-response programs appear in `time_varying_rates.md` where we ran into them (GMP Rate 3, GMP and Eversource NH battery programs, Eversource NH LCS), but there is no systematic catalog. Outside the NEEP region we only have Illinois (see [`il_tou_rates.md`](../il_tou_rates.md)).

## Known corrections to NEEP and to our own earlier files

These came out of the research and are scattered in the entries; the most important:

- NJ Universal Service Fund: NEEP cites "Docket EX25040210", which is actually the June 18, 2025 `$30` summer bill reduction. The USF dockets are EX00020091 (original program) and ER25060371 (Sept 25, 2025 order setting current USF and Lifeline factors).
- NEEP omits ACE's TOU option (QO23120871), JCP&L EV Driven (EO21030630), PPL's EV TOU Charging Rebate (R-2025-3057164), and shows PPL's percent-of-income plan as "None" although PPL OnTrack exists.
- NEEP lists Duquesne's TOU as a "Pilot"; the PUC approved it as a regular default-service option on Dec 5, 2024 (P-2024-3048592).
- NEEP's NJ and NY "PTR" rows (ACE, PSE&G, ConEd and others) are device-based direct load control or demand response programs, not peak-time rebates; no tariff uses that term. NEEP's WV Appalachian Power "Peak Time Rebate" was not found in the tariff.
- NY: "Care&Share" is National Grid's, ConEd's is EnergyShare; "PSE&G Long Island" should be PSEG Long Island; RG&E SC 4 is a non-seasonal TOU, not "seasonal TOU for 1000 kWh users"; NEEP understates EAP coverage and omits National Grid EV managed charging and several NYSEG/RG&E/O&R EV TOU delivery rates.
- GMP Rates 9 and 14 trace to Vermont Docket 8525 (Final Order March 24, 2016), not "Docket 8794" as one search synthesis said. NEEP's GMP "EV PTR" is not a peak-time rebate; only Rate 72 (off-peak/managed charging) was found.
- **PECO base rate docket:** R-2024-3046931 is the electric case and R-2024-3046932 is the gas case (confirmed in the Duquesne/PECO follow-up research). The heat pump file was right.
- **Unitil D.P.U. 23-81** is Unitil's gas rate case, not part of the electric heat pump rate; the defining docket is 23-80. JCP&L RGT has a new rate-design docket, ER26080420. Duquesne Rate RA dates to the 1997 restructuring case R-00974104, not 2014.

## Open items by region

These are the research agents' own lists of what was NOT FOUND, UNVERIFIED, or INFERRED, left verbatim so we can tell what was and was not checked. None was filled from memory.

#### Maine, New Hampshire, Vermont

- **GMP:** original creation docket for Rate 11; defining docket for Rate 22 (18-2850-TF is circumstantial); docket authorizing the 2023 EAP changes; GMP budget billing; BYOD/battery DR program docket; Rate 3 origin.
- **NEEP's GMP "EV PTR":** I found only Rate 72 (off-peak/managed charging). No peak-time-rebate EV docket was located.
- **Maine:** original docket for CMP A-TOU; original Chapter 314 (LIAP/ELP) and Chapter 317 (AMP) rulemaking dockets; budget billing for CMP and Versant; the docket for the pending A-ET extension; Versant A-2 water heating origin; contents of the April 2025 TOU report in 2025-00176; whether the Oct 2026 informal inquiry has a docket number. CMP page text depends on search snippets because `cmpco.com` was unreachable.
- **Eversource NH:** defining docket for original R-OTOD, legacy water heating and thermal storage; no PTR program found (NEEP lists one); whether DE 22-004 Clean Energy Fund and DE 23-068 are the only battery DR authority; current Eversource distribution rate case docket (after DE 19-057) was not checked; Order 26,797 body was not read.
- **Liberty NH:** original D-10 docket; no water heater demand response or PTR program found despite NEEP rows; Liberty rate case DE 23-039 status as of October 2026 not checked.
- **Unitil NH:** order number approving permanent rates in DE 21-030; status of AMP implementation; Unitil budget billing terms.
- **NH EAP:** docket number for Order 23,980; whether an AMP was integrated into EAP after DE 22-043 Recommendation 5; NH DOE fuel assistance (LIHEAP) not fetched.
- **NHN:** docket DE 14-337 is from a search summary only.
- **Vermont secondary-source dependence:** the FY27 order date (9/30/2026) for 26-0096-TF comes from `utilityratecalc.com`.

#### Connecticut, Massachusetts, Rhode Island

Items below are NOT FOUND, UNVERIFIED or INFERRED. None was filled from memory.

##### Connecticut

- Origin docket and date of Eversource **Rate 7** (pre-2008 history) and of **Rate 5** (electric heating). The tariff footers I read cite only recent annual RAM dockets.
- Exact decision date of **17-10-46** (Eversource rate case) and of the **17-12-03RE11** reconsideration.
- Originating docket for Eversource **New Start** and the original statutory Matching Payment Program (the annual AFP dockets, 2020–2026, were found, but they renew a program that predates them).
- The authorizing docket for **budget billing / levelized payments** and winter-protection rules (utility terms and conditions; PURA rules).
- The DEEP conservation and load management docket number for the demand-response and storage programs.
- Whether **PA 25-173** is the same law as the "SB 4 §21" cited for the TVR education mandate (UNVERIFIED).
- CEAP (LIHEAP) and the RRES solar tariff have no PURA docket I could confirm.

##### Massachusetts

- **D.P.U. 14-04-C** order date (2014; text not dated in the copy I read).
- **D.P.U. 18-150** as National Grid's Phase II EV docket is INFERRED from a Mass.gov page; the order text I read truncated the number. Order date not retrieved.
- The docket that set Eversource's 42% and Unitil's 40% flat discount levels (D.P.U. 22-22 is a candidate; not verified).
- Compliance dockets for the tiered discount (D.P.U. 24-15 series) for Eversource and Unitil; only National Grid's (D.P.U. 26-132) was found.
- Annual AMP report dockets, and the authorizing dockets for all three **budget plans**.
- Unitil's next-phase EV docket; status of the proposed EV TOU dockets **D.P.U. 23-84 / 23-85**.
- Date of D.P.U. 24-15-C.

##### Rhode Island

- Written order in **25-45-GE** (open-meeting decision 2026-08-21): not on the docket page when I fetched it. Needed to confirm the due date of the TOU schedule, the start date of the seasonal residential delivery rate (the 2026-09-01 tariffs I read still show a single A-16 distribution charge), and the 2026-01-01 vs 2027-03-01 date for the five-tier A-60.
- Whether the PUC formally approved the **CLF heat pump settlement**; the minutes I read have no heat pump motion. The DSM Investment Proposal docket does not exist yet (LCP Standards docket 26-15-EE is referenced).
- Issue date of the 4770/4780 **Order 23823**; issue date of 22-49-EL **Order 25353** (2025-05-20 is from my earlier notes).
- Whether the **Off-Peak Charging Rebate** pilot has ended, and whether the ConnectedSolutions **EVDR** pathway launched; the EVDR incentive amount.
- The original authorizing docket for RIE **budget billing**, the outcome of review docket **25-20-GE**, and the docket for the pre-2016 AMP and the "standard/protected customer" payment-plan steps.
- Sale-approval docket for the PPL acquisition commitments (`$43.5` million low-income arrears discharge).
- The RI LIHEAP administering agency today (NEEP says OHHS) and the enhancement-plan annual-filing docket.
- The current A-60 discount percentages (25% / 30% come from the 2018 order).

#### New York

- **ConEd Rate II creation docket**: only the Mar 1, 2014 closure (Rate III replaced it) is documented; the original Rate II order (pre-2014) not found. Case 13-E-0030 order text (Feb 21, 2014) itself not read.
- **ConEd Rate VI (Smart Energy Plan) and Rider Z/Rider AB**: docket for Rate VI not extracted from the July 1, 2026 filing; whether the filing has been accepted not checked; 18-E-0130 stamp on Rider AB leaves left unexplained.
- **ConEd Special Provisions E/F** for EV on Rate III: which order created them not identified (18-E-0206 is the likely driver but unconfirmed).
- **National Grid VTOU origin**: available Dec 1, 2016, but the originating case was not found; 17-E-0238 (Mar 15, 2018) is only the leaf stamp in the petition I read. National Grid's EAP/EEAP leaves and EV Charge Smart Plan details (including whether the Feb 2024 petition was approved) not verified.
- **Central Hudson SC 6** origin docket; peak-hour definitions in SC 6 (12-hour vs 5-hour options) not verified; Central Hudson Aug 2025 order's permanent-tariff follow-up order not read.
- **NYSEG SC 8 Day-Night** origin (pre-1988 case) and **NYSEG SC 12** supply rate levels not found; SC 12 EV provision not checked (SC 8 Special Provision (p) applies to SC 1, 8, 12).
- **RG&E**: SC 4 creation docket (leaf stamp 09-E-0228 only); Case 22-E-0319 not read; RG&E EV peak window not verified; RG&E EAP leaf not opened.
- **NYSEG/RG&E 25-E-0375 / 25-E-0379 final order**: only the May 14, 2026 temporary-rates order was found; whether a final joint-proposal order issued by Oct 27, 2026 not checked. Also 22-E-0317/22-E-0319 (Oct 12, 2023 orders) contents not read.
- **O&R**: SC 19 creation docket; Case 24-E-0060 order not read (stamp only); O&R web page customer charge ($22.50) conflicts with tariff leaf ($29.00).
- **PSEG Long Island/LIPA**: no PSC dockets (tariffs are Board-approved; DPS "Matters" 23-00071 and 26-00346 are advisory); Rate 180, Rate 580 and HAP creation dockets NOT FOUND; HAP monthly amount conflict ($35 vs $45); EV-specific rate none found; PTR/CSRP not verified; LIPA EEAP status unknown.
- **Peak-time rebates**: no tariffed residential PTR found in NY; the programs NEEP labels PTR are DLC/thermostat programs under 14-E-0423; the originating DLM order(s) and ConEd's DLM tariff case number not found.
- **EAP discount dollar amounts** only partly extracted (NYSEG, Central Hudson EEAP, ConEd EEAC); ConEd Rider S, O&R, RG&E and National Grid statements not extracted.
- **Arrears Phase 1/2, Energy Bill Credit, Guarantee Pilot orders** not read directly (cited from the July 17, 2025 order's background); Phase 2 date (Jan 19 vs Jan 23, 2023) inconsistent in that order.
- **DPS Matter Master pages** do not render document lists without JavaScript; full docket document lists (workbooks) could not be browsed. Use `https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=<case>` interactively.
- **HEFPA citation** for budget billing from general knowledge, not verified.
- **NEEP errors noted:** understates EAP coverage; "Care&Share" attributed to ConEd (it is National Grid's; ConEd's is EnergyShare); labels "PSE&G Long Island" (PSEG Long Island); RG&E SC 4 shown as "seasonal TOU for 1000 kWh users" (tariff shows a non-seasonal TOU with a 24,750 kWh schedule split); Central Hudson Bill Discount shown in the "Seasonal Only" column; omits National Grid's EV managed charging and heating funds, NYSEG/RG&E/O&R EV TOU delivery rates, EEAP, and Rate VI.

#### New Jersey, Pennsylvania

##### Defining dockets NOT FOUND (legacy tariff provisions):

- JCP&L RT, RS (seasonal block) and RGT; PSE&G RS block, RLM and RHS; RECO SC 1 and SC 3; ACE RS seasonal block. These predate the restructuring era and their footers cite only current rate cases. A BPU docket search (or the Board's older order archive) is the next step.
- NJ Winter Termination Program rule (N.J.A.C. 14:3-3A.5): rulemaking docket not identified.
- NJ Lifeline: statutory program; annual rate set in the USF docket, no separate defining docket.
- NJ and PA budget billing / equal payment plans: tariff provisions only.
- PECO and ACE customer-relief funds: company-funded, no regulator docket found.
- PECO EVsmart (commercial only), FirstEnergy PA EV rate: none found.

##### Docket identified but approval or details UNVERIFIED:

- PSE&G FlexPower/SmartFlex DR: program approval docket (the Dec 1, 2025 PY4 letter is captioned QO19010040, QO19060748, QO17091004).
- Duquesne EV TOU distribution rate: docket UNVERIFIED (the EV TOU pilot supply rate traces to P-2020-3019522).
- Duquesne Peak Saver Rewards and Smart Charging Rewards: sit under M-2020-3020818; the approval order text was not read.
- PPL Optimized EV Charging: docket not identified.
- NJ PAGE: EO23050278 came from a search summary only; NJ SHARES: not found.
- PA CAP/hardship benefit levels for Duquesne's and FirstEnergy's 2026–2030 plans; Duquesne's new USECP docket; the Mar 14, 2024 FirstEnergy order; the June 13, 2024 PUC order on LIHEAP data sharing.
- JCP&L and RECO companions to the ACE/PSE&G BGS EV TOU credits: none found.
- PECO DSP VI peak hours and PPL DSP V order date.
- REAP rounds 1–2 (QO24020120) and the 2025 RUBC/$30 reduction orders: facts from earlier reading, URLs not retained.

##### Discrepancies with NEEP (`neep_modern_rate_design.md`) and the local HP file:

- NEEP cites "Docket EX25040210" for NJ USF. That docket is the June 18, 2025 $30 summer bill reduction. The USF dockets are EX00020091 (original program) and ER25060371 (Sept 25, 2025 order setting current USF and Lifeline factors).
- NEEP omits: ACE's TOU option (QO23120871), JCP&L EV Driven (EO21030630), PPL's EV TOU Charging Rebate (R-2025-3057164) and PPL's OnTrack CAP (Appendix C shows PPL's percent-of-income plan as "None").
- NEEP lists Duquesne's TOU as a "Pilot". The PUC approved it as a regular default-service option on Dec 5, 2024 (P-2024-3048592).
- NEEP's NJ "PTR" rows for ACE and PSE&G appear to be device-based demand response (direct load control, FlexPower), not peak time rebates. I found no tariff using that term.
- (Resolved) PECO's electric base-rate case is R-2024-3046931; R-2024-3046932 is gas.
- PA TOU is mostly supply-side default service TOU created in DSP (P-) dockets. NEEP does not make that distinction.

#### Maryland, DC, Delaware, West Virginia

##### Maryland

- BGE Schedule RL (1984), Pepco R-TM (pre-2000), Schedule EV's 2013 authorization (BGE says "permanent in 2016"), and the original Delmarva MD / Pepco MD dynamic-pricing orders for Delmarva: no defining docket found.
- Delmarva MD Peak Energy Savings Credit: authorizing order not found. Case 9294 is a guess.
- SMECO: TOU schedule id and docket, PTR, EV OPR, and the order authorizing Rider EV-TOU (Dec 1, 2023). Case 9738 appears only in a search summary.
- Order 92166 (Jan 29, 2026) not read for BGE, Pepco and Delmarva sections; Schedule EV's fate and PHI's Phase II decisions are unconfirmed.
- Order 90984 (Jan 17, 2024) not read directly.
- EmPOWER 2027-2029 cycle docket and current peak-rebate authority: not checked.
- EUSP: which docket sets the annual funding and class allocation. Not found.
- The nature of Case 9798 (named in PC 70 filings) was not checked; user guesses of Case 9695 and 9702 for low-income discounts are wrong for 9702 (Pepco multi-year plan, Order 91181); I did not verify 9695.
- Pepco MD Rider DP and Delmarva MD rider sheets, and Delmarva MD R-TOU-P tariff, were not read.
- PC 59 order's Jan 1, 2027 effective date was taken from the search summary, not the order text.

##### District of Columbia

- Orders 14712, 15986, 18059 and 18152 (RAD lineage) and Orders 19898 and 19983 (R-PIV) were cited but not opened.
- FC1155-2026-E-178 final-tariff notice not read, so the current R-PIV rates are not recorded.
- Pepco DC Customer Relief Fund, budget billing: not verified; no docket.
- Whether Pepco DC has any non-EV TOU, PTR or CPP: none found. PowerCentsDC case number not verified (I recall 1056, unconfirmed).

##### Delaware

- Original R-TOU-ND authorization: not found.
- Order No. 10129 (14-193, Nov 3, 2022): docketed as an Order but not read.
- Order dates for Order 9593 (17-1094) and Order 9198's exact issue date (docketed Mar 28, 2018).
- Delmarva DE base rate case filed Dec 2025: docket number not found.
- Status and outcome of 25-1554 after the Public Advocate's April 2026 motion to dismiss.
- Good Neighbor Energy Fund: not verified. Levelized budget billing: not found in the tariff.
- SB 187 / any Delaware EV statute: not found.

##### West Virginia

- No WV PSC e-docket page was read. All WV case numbers come from tariffs, public notices and one PSC order PDF.
- Defining dockets for RS (seasonal declining block), RS-TOD, the water heating and energy-storage provisions: not found (likely pre-2010 cases).
- 22-1082-E-PC: order date and outcome not read.
- EE/DR: 17-0401-E-P and the current successor docket: UNVERIFIED.
- Peak Time Rebate for APCo: none found in the tariff; treat as a NEEP error until shown otherwise.
- Implementing PSC order for the 20% discount (statute is §24-2A-1): not found.
- Mon Power / Potomac Edison WV tariffs and rate schedules: not read.
