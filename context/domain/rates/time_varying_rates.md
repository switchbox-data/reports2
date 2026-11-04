# Time-varying residential rates: catalog of what we know (Northeast and Mid-Atlantic)

**Last updated:** 2026-10-27. **Scope:** residential time-of-use (TOU), seasonal-only, demand-charge, critical peak pricing, peak-time-rebate, and related rates and programs at investor-owned utilities from Maine to West Virginia, plus a few co-ops and municipals found along the way. It also lists legacy rates that NEEP files under time-varying (controlled water heating, battery demand response) and records "none found" where NEEP lists a rate we could not confirm.

This file answers three questions for each rate: what is it, **which docket defined it**, and **how do we know**. It starts from the NEEP survey ([`../../sources/general_reference/neep_modern_rate_design.md`](../../sources/general_reference/neep_modern_rate_design.md), Appendix A and E) but goes to the primary documents where it could. Electric heating and heat pump rates are in [`electric_heating_and_heat_pump_rates.md`](electric_heating_and_heat_pump_rates.md); some rows here (for example BGE Schedule RL, ConEd Rate III) also appear there. EV rates are in [`ev_rates.md`](ev_rates.md).

## How to read this catalog

**Category codes:** TOU-whole-home (time-varying delivery or supply on the whole bill); TOU-seasonal-only (seasonal, no time-of-day split); demand-charge; rebate-CPP / rebate-PTR / rebate-OPR (critical-peak, peak-time, and off-peak rebates); rebate-other; other (legacy or investigative).

In Pennsylvania the TOU rates are mostly **supply-side default service** offerings created in default-service-plan (P-) dockets, not delivery tariffs; NEEP does not make that distinction. Several NEEP "PTR" rows in NJ, NY, and WV turned out to be direct load control or device programs, not peak-time rebates; the entries say so.

- **Defining docket:** the proceeding that created or approved the offering. "Not found" means we have not located it, not that it does not exist.
- **Current governing docket:** the proceeding named on today's tariff footer or behind the current rate order, or where the offering is being changed. Tariff footers usually cite this one, which is why the defining docket is often hard to find.
- **Docket status** in the index table: _found_ = a defining docket is named; _partial_ = a revising or continuing docket is confirmed but the original creator is not; _unverified_ = named from a secondary source or inferred; _not found_.
- **Evidence level:** _Primary_ = the order, testimony, tariff text, or statute was read. _Official page_ = a utility or agency web page. _Search summary_ = only a search snippet or synthesis was seen; spot-check before relying on it.
- Research was done on 2026-10-27 by web search and page fetch. Where an order was cited but not opened, the entry says so. Open items for every region are in [`README.md`](README.md).

## Index

| State | Utility / offering                                                                     | Category          | Defining docket (short)                                                                                             | Docket status |
| ----- | -------------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------- | ------------- |
| ME    | CMP — A-TOU (residential time-of-use, Rate A-TOU)                                      | TOU-whole-home    | NOT FOUND for the original A-TOU creation (tariff revisions dated Jul 1 2012 and Jul 1 2018 exist). …               | not found     |
| ME    | CMP — A-Seasonal Heat Pump (SHP) pilot                                                 | TOU-seasonal-only | 2021-00325 (Commission-initiated rate design investigation; …                                                       | found         |
| ME    | CMP — Electric Technology (ET) rate                                                    | other             | 2021-00325 (pilot from Jan 1, 2023). Extension in 2022-00152 (Oct 1 2025 letter).                                   | found         |
| ME    | Versant — A-4 Home Eco time-of-use (Bangor Hydro District) and A-4M (Maine Public …    | TOU-whole-home    | 2021-00325 (Sept 27, 2022 Versant stipulation order approving A-4 Home Eco TOU).                                    | found         |
| ME    | Versant — A-20 Home Heating Eco rate (seasonal declining block)                        | other             | The HP/HPWH expansion came from 2021-00325; the original rate creation was NOT FOUND.                               | partial       |
| ME    | Maine PUC — time-of-use investigations (statewide)                                     | other             | 2023-00019, 2024-00231, 2025-00176.                                                                                 | found         |
| NH    | Eversource NH — Rate R-OTOD 2 (Residential Time-of-Day Delivery Service)               | TOU-whole-home    | DE 21-119 ("Eversource Energy's Proposed Tariff Amendment to Residential Time-of-Day Rate") …                       | found         |
| NH    | Eversource NH — Rate R-OTOD (original residential time-of-day)                         | TOU-whole-home    | NOT FOUND.                                                                                                          | not found     |
| NH    | Eversource NH — legacy controlled water heating, thermal storage (LCS) and space …     | other             | NOT FOUND (legacy, pre-restructuring).                                                                              | not found     |
| NH    | Eversource NH — residential battery demand response (ConnectedSolutions battery …      | other             | DE 23-068, Order No. 26,908 (Nov 30, 2023), which converted the active demand reduction pilot …                     | partial       |
| NH    | Liberty NH — Rate D-10 Optional Peak Load Pricing (residential time-of-day)            | TOU-whole-home    | NOT FOUND (predates the DE 19-064 tariff). (governing dockets only).                                                | not found     |
| NH    | Liberty NH — Rate D-11 Battery Storage Pilot (seasonal TOU)                            | TOU-seasonal-only | DE 17-189, Order No. 26,209, January 17, 2019 (up to 500 batteries; …                                               | found         |
| NH    | Unitil Energy Systems — Whole House TOU (TOU-D, now Schedule TOU-R)                    | TOU-whole-home    | DE 21-030 (Unitil rate case). Settlement Agreement of Feb 11, 2022, Section 6.6, requires a …                       | found         |
| VT    | GMP — Rate 14 Residential TOU + critical peak pricing ("Empower")                      | TOU-whole-home    | Docket 8525, Vermont Public Service Board, Final Order March 24, 2016: "approved two new …                          | found         |
| VT    | GMP — Rate 9 Residential critical peak pricing                                         | other             | Docket 8525, VT Public Service Board, Final Order March 24, 2016.                                                   | found         |
| VT    | GMP — Rate 11 Residential time-of-use                                                  | TOU-whole-home    | The original creating docket was NOT FOUND. Docket 8525 (Final Order 3/24/2016) integrated Rate 11 …                | not found     |
| VT    | GMP — Rate 22 Seasonal time-of-use                                                     | TOU-seasonal-only | NOT FOUND. Candidate: Case 18-2850-TF (rate-design proceeding for rates effective April 1, 2019; …                  | not found     |
| VT    | GMP — Rate 3 off-peak water heating                                                    | other             | NOT FOUND (not searched in depth; out of scope beyond noting existence).                                            | not found     |
| VT    | GMP — Battery demand response (Bring Your Own Device; …                                | other             | NOT FOUND. The only docket I saw in the add-on tariff PDFs is the Solar Energy Affordability …                      | not found     |
| MA    | Eversource MA (NSTAR Electric) — Residential Heat Pump Rates R1HP / R2HP (optional …   | TOU-seasonal-only | D.P.U. 25-55, MA DPU, order 2025-07-29 (approved with modifications NSTAR Electric's seasonal …                     | found         |
| MA    | National Grid MA (Massachusetts Electric / Nantucket Electric) — Residential Heat …    | TOU-seasonal-only | D.P.U. 23-150, MA DPU, base distribution rate case order 2024-09-30, printed pp. 492–513 (PDF page = printed + 18). | found         |
| MA    | Unitil (Fitchburg Gas & Electric) MA — Heat Pump Rate (R-1 / R-2 HP; …                 | TOU-seasonal-only | D.P.U. 23-80 / D.P.U. 23-81 (Fitchburg Gas and Electric Light Co. …                                                 | found         |
| MA    | All MA EDCs — Statewide default time-varying rate framework for basic service …        | other             | D.P.U. 14-04-C, MA DPU, "Order Adopting Policy Framework for Time Varying Rates" (final order …                     | found         |
| MA    | All MA EDCs — DOER-proposed default (opt-out) residential TOU rates (D.P.U. 26-62)     | TOU-whole-home    | D.P.U. 26-62 (opened on DOER's 2026-04-08 petition; …                                                               | found         |
| MA    | Eversource MA, National Grid MA, Unitil — ConnectedSolutions (residential …            | other             | D.P.U. 24-140 through 24-149, MA DPU, Order on the 2025–2027 Three-Year Energy Efficiency …                         | found         |
| RI    | Rhode Island Energy (RIE; The Narragansett Electric Co.) — Whole-home TOU / …          | TOU-whole-home    | PUC Docket 25-45-GE (RIE base distribution rate case, filed 2025-11-26, consolidated with …                         | found         |
| RI    | Rhode Island Energy — Residential seasonal volumetric distribution charge (A-16 …      | TOU-seasonal-only | PUC Docket 25-45-GE (open-meeting vote 39, 2026-08-21; written order NOT FOUND). …                                  | found         |
| RI    | Rhode Island Energy — Heat pump rate (CLF proposal resolved by settlement; …           | other             | PUC Docket 25-45-GE (Heat Pump Settlement filed 2026-05-26; updated signatures 2026-06-09).                         | found         |
| RI    | Rhode Island Energy — ConnectedSolutions residential demand response: Bring Your Own … | rebate-other      | PUC Docket 24-06-EE (System Reliability Procurement investment proposal for electric demand …                       | found         |
| CT    | Eversource CT (CL&P) — Residential Time-of-Day Electric Service, Rate 7 (whole-home …  | TOU-whole-home    | 05-10-03RE01, CT DPUC (now PURA), Decision dated 2007-12-19 — "Application of CL&P to Implement …                   | found         |
| CT    | Eversource CT (CL&P) — Variable Peak Pricing (VPP) Rider (daily-varying on-peak …      | TOU-whole-home    | 03-07-02RE10, CT DPUC, Letter Ruling dated 2008-06-26 (effective 2008-07-01); …                                     | found         |
| CT    | United Illuminating (UI) — Residential Time-of-Use Rate RT (C.P.U.C.A. No. 2526)       | TOU-whole-home    | 05-06-04, CT DPUC, final decision 2006 (UI rate-design decision, implementing PA 05-1 §13). …                       | found         |
| CT    | United Illuminating (UI) — Residential Load Control Rider RLC (C.P.U.C.A. No. 433)     | other             | 05-06-04 Supplemental Decision dated 2006-08-30 (per tariff footer).                                                | found         |
| CT    | Eversource CT — Rate 5 Residential Electric Heating Service (legacy electric-heating … | other             | NOT FOUND (a pre-2000 DPUC rate class; tried: Eversource filings, PURA LIDR decision, 26-05-10 …                    | not found     |
| CT    | Eversource CT — Proposed Rate 6 Optional Residential Space Heating (seasonal …         | TOU-seasonal-only | 26-05-10, PURA, filed 2026-07-14 — Application of CL&P to Amend its Rate Schedules (Presiding …                     | found         |
| CT    | Eversource CT / UI — Time-varying-rate education & engagement mandate (SB 4 §21, PA …  | other             | statute (Senate Bill 4 as enacted; sec. 21), implemented in 26-05-10; …                                             | found         |
| CT    | Eversource CT / UI — Smart-thermostat demand response: ConnectedSolutions …            | rebate-PTR        | Approved through DEEP's three-year Conservation & Load Management (C&LM) Plan — 2025–2027 C&LM …                    | found         |
| CT    | Eversource CT / UI — Energy Storage Solutions (ESS) program (battery demand …          | other             | 17-12-03RE03, PURA, Final Decision 2021-07-28 (PA 21-53). …                                                         | found         |
| NY    | Con Edison — SC 1 Rate II, Residential and Religious Voluntary Time-of-Day (P.S.C. …   | TOU-whole-home    | Case 13-E-0030, NY PSC, Order Approving Electric, Gas and Steam Rate Plans in Accord with Joint …                   | unverified    |
| NY    | Con Edison — SC 1 Rate III, Residential and Religious Voluntary Time-of-Day …          | TOU-whole-home    | Case 13-E-0030, NY PSC, Order Approving Electric, Gas and Steam Rate Plans in Accord with Joint …                   | found         |
| NY    | Con Edison — SC 1 Rate IV, Optional Demand-Based (Steady Use Rate) — cross-reference … | demand-charge     | Case 19-E-0065, NY PSC, Jan 16, 2020 (Select Pricing Plan). …                                                       | found         |
| NY    | Con Edison — SC 1 Rate VI (proposed, filed Jul 1, 2026) and Rider Z Innovative …       | demand-charge     | Case 18-E-0397, NY PSC, Order Approving Tariff Amendments with Modifications, Dec 13, 2018 …                        | found         |
| NY    | Con Edison — Rider AB, Smart Home Rate Demonstration Project (SC 1)                    | demand-charge     | NOT FOUND. Leaves are stamped "Order in Case 18-E-0130 dated 09/17/2020" (and 18-E-0130 et al. …                    | not found     |
| NY    | Con Edison — Smart Usage Rewards (residential event-based demand response)             | other             | Case 14-E-0423 (Proceeding on Motion of the Commission to Develop Dynamic Load Management …                         | found         |
| NY    | Central Hudson — SC 6, Residential Time-of-Use (12-hour and 5-hour peak options)       | TOU-whole-home    | NOT FOUND. SC 6 predates the cases I could read, and I did not locate an SC 6 leaf stamp. …                         | not found     |
| NY    | National Grid (Niagara Mohawk) — SC-1 Residential Optional Time-of-Use (SC1VTOU; …     | TOU-whole-home    | Special Provision L was already available to all residential customers as of Dec 1, 2016 (per …                     | found         |
| NY    | NYSEG — SC 12, Residential Service with Time-of-Use Metering (P.S.C. No. …             | TOU-whole-home    | Case 07-E-0479, NY PSC, order dated Aug 29, 2007 (leaf 295 stamp: "Issued in compliance …                           | found         |
| NY    | NYSEG — SC 8, Residential Day-Night Service (P.S.C. No. 120, leaf 256)                 | TOU-whole-home    | NOT FOUND. Leaf 256 rev. 5 effective Jan 1, 2010; case stamp not displayed in text I read; …                        | not found     |
| NY    | RG&E — SC 4, Residential Service Time-of-Use Rate (P.S.C. No. 19, leaf 174)            | TOU-whole-home    | Leaf 174.1.1 stamp: "Issued in Compliance with Order in Case 09-E-0228 issued and effective …                       | found         |
| NY    | O&R — SC 19, Residential Optional Time-of-Use Service (P.S.C. No. 3, leaf 341)         | TOU-whole-home    | Base SC 19 TOU: NOT FOUND (predates what I could trace). …                                                          | not found     |
| NY    | PSEG Long Island (LIPA) — Rate 194, Residential Time-of-Day (standard/default …        | TOU-whole-home    | Not a PSC case. LIPA is not generally subject to PSC rate jurisdiction. …                                           | found         |
| NY    | PSEG Long Island (LIPA) — Rate 180 flat residential rate (seasonal step above 250 …    | TOU-seasonal-only | Not a PSC case (LIPA tariff). Rate 180: referenced in DPS Matter 23-00071; creation NOT FOUND. …                    | found         |
| NY    | Central Hudson, National Grid, NYSEG, RG&E, O&R — Residential Direct Load Control / …  | other             | Case 14-E-0423, Proceeding on Motion of the Commission to Develop Dynamic Load Management …                         | found         |
| NY    | PSEG Long Island — Commercial System Relief Program (CSRP) and Distribution Load …     | other             | NOT FOUND (LIPA is outside the 14-E-0423 PSC framework).                                                            | not found     |
| NJ    | Atlantic City Electric (ACE) — Residential Service (RS) with seasonal inclining …      | TOU-seasonal-only | NOT FOUND (block structure is long-standing; the original ACE order that created the inclining …                    | not found     |
| NJ    | Atlantic City Electric (ACE) — Residential TOU option (RS "Residential TOU Option" …   | TOU-whole-home    | QO23120871, BPU (Triennium 2 energy efficiency / demand response stipulation, "Order Adopting …                     | found         |
| NJ    | Atlantic City Electric (ACE) — Direct Load Control demand response (consumer brand …   | other             | QO23120871, BPU, Order Adopting Stipulation, Oct 30, 2024 (PRIMARY, read). …                                        | found         |
| NJ    | Public Service Electric & Gas (PSE&G) — FlexPower / SmartFlex demand response …        | other             | UNVERIFIED for the demand response program approval. …                                                              | unverified    |
| NJ    | Jersey Central Power & Light (JCP&L) — Service Classification RT, Residential …        | TOU-whole-home    | NOT FOUND. RT predates restructuring; tariff footers only cite the latest rate case. …                              | not found     |
| NJ    | Jersey Central Power & Light (JCP&L) — Service Classification RS Residential Service … | TOU-seasonal-only | NOT FOUND (long-standing design). Most recent re-design inside ER23030144 (order Feb 14, 2024). …                   | not found     |
| NJ    | Jersey Central Power & Light (JCP&L) — Service Classification RGT, Residential …       | TOU-seasonal-only | NOT FOUND online; pre-1999. Current: ER23030144 / ER26080420.                                                       | not found     |
| NJ    | Public Service Electric & Gas (PSE&G) — Rate Schedule RS-TOU (two-period "2P" and …    | TOU-whole-home    | ER23120924 and GR23120925 (OAL PUC 00926-24), BPU, Order Adopting Stipulation, Oct 9, 2024 …                        | found         |
| NJ    | Public Service Electric & Gas (PSE&G) — Rate Schedule RLM, Residential Load …          | TOU-whole-home    | NOT FOUND (pre-restructuring/legacy rate). Current structure from ER23120924 (order Oct 9, 2024).                   | not found     |
| NJ    | Public Service Electric & Gas (PSE&G) — Rate Schedule RS summer inclining block and …  | TOU-seasonal-only | NOT FOUND for original design; re-set in ER23120924 (Oct 9, 2024).                                                  | not found     |
| NJ    | Rockland Electric Company (RECO) — SC 1 Residential Service (summer inclining block) … | TOU-whole-home    | NOT FOUND for SC 1 TOD (leaf footers cite ER09080668, May 12, 2010, for the older schedule leaves). …               | not found     |
| NJ    | Rockland Electric Company (RECO) — SC 3 Residential Time-of-Day Heating Service        | TOU-seasonal-only | NOT FOUND. Leaf 95 footer cited ER09080668 (May 12, 2010).                                                          | not found     |
| NJ    | New Jersey (all EDCs) — BGS TOU supply option for residential customers                | TOU-whole-home    | ER22030127 (BGS for period beginning June 1, 2023), BPU order Nov 9, 2022 (ordered EV BGS TOU …                     | found         |
| PA    | Duquesne Light — Time-of-Use Supply Rate (default service TOU; NEEP "TOU Pilot")       | TOU-whole-home    | P-2024-3048592, PA PUC, Opinion and Order Dec 5, 2024 (entered Jan 14, 2025; …                                      | found         |
| PA    | Duquesne Light — EV Time-of-Use Distribution Rate (RS / RH / RA add-on HP schedules)   | TOU-whole-home    | UNVERIFIED. The PUC EV page ties the Duquesne EV TOU pilot (three tiers, separate EV meter) to …                    | unverified    |
| PA    | Duquesne Light — Peak Saver Rewards (summer behavioral demand response; NEEP "PTR")    | rebate-PTR        | M-2020-3020818 (Duquesne Act 129 Phase IV EE&C Plan). …                                                             | found         |
| PA    | PECO — Default Service TOU (DSP-TOU)                                                   | TOU-whole-home    | P-2020-3019290, PA PUC, Opinion and Order Dec 3, 2020 (PECO DSP V; …                                                | found         |
| PA    | PECO — Rate RH (seasonal electric heating) and other legacy delivery rates             | TOU-seasonal-only | See local file.                                                                                                     | found         |
| PA    | PPL Electric — Time-of-Use default service (seasonal TOU, supply-only)                 | TOU-seasonal-only | P-2024-3047290, PA PUC, Order Nov 7, 2024 approving the Aug 27, 2024 settlement (retained the …                     | found         |
| PA    | FirstEnergy Pennsylvania (Met-Ed, Penelec, Penn Power, West Penn) — Rider K …          | TOU-whole-home    | P-2021-3030012 (Met-Ed), P-2021-3030013 (Penelec), P-2021-3030014 (Penn Power), P-2021-3030021 …                    | found         |
| DE    | Delmarva Power DE — Service Classification R-TOU-ND (optional residential TOU …        | TOU-whole-home    | NOT FOUND for the original optional TOU rate (likely an older Delmarva DE rate case; not located).                  | not found     |
| DE    | Delmarva Power DE — Rider "DP" Peak Energy Savings Credit (opt-out critical peak …     | rebate-CPP        | PSC Docket No. 09-311, Final Findings, Opinion and Order No. 8105, Jan 31, 2012. …                                  | found         |
| DE    | Delmarva Power DE — Docket 25-1554 "Affordability and Load Flexibility Portfolio" …    | other             | 25-1554 (Delaware PSC), filing Dec 2025. The docket number comes from the PSC public notice file …                  | found         |
| MD    | BGE — Schedule RL / RLH (optional residential TOU; electric-heat variant "RLH")        | TOU-whole-home    | NOT FOUND. The local doc `electric_heating_and_heat_pump_rates.md` (table at line 44) also says …                   | not found     |
| MD    | BGE — Schedule RD (whole-home TOU, from the PC44 pilot)                                | TOU-whole-home    | PC 44 (administrative docket "Transforming Maryland's Electric Distribution Systems"). …                            | found         |
| MD    | Pepco MD — Schedule R-TOU-P (residential TOU program, opt-in)                          | TOU-whole-home    | PC 44 (Letter Order May 7, 2018, pilot), per the local doc. …                                                       | found         |
| MD    | Delmarva Power MD — Schedule R-TOU-P (residential TOU program, opt-in)                 | TOU-whole-home    | PC 44 Letter Order (May 7, 2018), per the local doc. …                                                              | found         |
| MD    | Pepco MD — Schedule R-TM (time-metered residential; legacy)                            | TOU-whole-home    | NOT FOUND (pre-2000). Not attempted beyond the tariff text.                                                         | not found     |
| MD    | Potomac Edison MD — Schedule R-TOU (new residential TOU service)                       | TOU-whole-home    | Case 9761, Order 91917 (Oct 21, 2025), approving Potomac Edison's proposal (ML 320116). …                           | found         |
| MD    | SMECO — residential seasonal TOU (schedule id UNVERIFIED)                              | TOU-seasonal-only | NOT FOUND. I looked at SMECO's rates page and Phase II EV material, which only name Rider EV-TOU …                  | not found     |
| MD    | BGE — Rider 26 "Peak Time Rebate" (Smart Energy Rewards)                               | rebate-PTR        | Case 9208, Order 83531 (Aug 13, 2010), BGE's smart grid initiative (AMI plus dynamic pricing). …                    | found         |
| MD    | Pepco MD — Rider DP "Dynamic Pricing – Peak Energy Savings Credit"                     | rebate-PTR        | Case 9207, Order 83571 (Sept 2, 2010), Pepco's AMI plan and dynamic pricing (CPR) proposal. …                       | found         |
| MD    | Delmarva Power MD — Peak Energy Savings Credit (dynamic pricing rider)                 | rebate-PTR        | NOT FOUND for Delmarva MD. The 2010 PSC page says Delmarva's smart-grid initiative was handled …                    | not found     |
| MD    | SMECO — Peak Time Rebate (NEEP)                                                        | rebate-PTR        | NOT FOUND (searched SMECO rate pages and Phase II EV material).                                                     | not found     |
| MD    | Pepco MD — Rider "DRS" (Residential Direct Load Control)                               | other             | Case 9149, Order 82511 (cited in the tariff text; order not read).                                                  | found         |
| DC    | Pepco DC — no non-EV time-varying residential rate found                               | other             | not applicable.                                                                                                     | found         |
| WV    | Appalachian Power / Wheeling Power (WV) — Schedule R.S. …                              | TOU-seasonal-only | NOT FOUND (decades-old structure). Current rates: Case No. …                                                        | not found     |
| WV    | Appalachian Power / Wheeling Power (WV) — Schedule R.S.-T.O.D. …                       | TOU-whole-home    | NOT FOUND. Current rates: 24-0854-E-42T, Order dated Aug 28, 2025.                                                  | not found     |
| WV    | Appalachian Power / Wheeling Power (WV) — Residential Peak Reduction Program and …     | other             | EE/DR program authorized in Case No. 17-0401-E-P (per public notice and a PSC doc); …                               | unverified    |
| WV    | Appalachian Power / Wheeling Power (WV) — "Peak Time Rebate" (NEEP)                    | rebate-PTR        | NOT FOUND.                                                                                                          | not found     |
| WV    | Mon Power / Potomac Edison (WV) — no residential time-varying rates                    | other             | not applicable (nothing found).                                                                                     | found         |

## Maine

### CMP — A-TOU (residential time-of-use, Rate A-TOU)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active; enrollment about 0.77% per NEEP.
- **Design:** Weekdays: on-peak 7 am-12 pm and 4-8 pm; shoulder 12-4 pm; off-peak 8 pm-7 am. Weekends and holidays all off-peak. The on-peak/shoulder periods changed under the Stipulation in Docket 2022-00152 (order approving 6/6/2023; deliberations 1/17/2024; tariff stamped 1/29/2024; …
- **Defining docket:** NOT FOUND for the original A-TOU creation (tariff revisions dated Jul 1 2012 and Jul 1 2018 exist). The 2025 period change is **2022-00152**. _[not found]_
- **Current governing docket:** Tariff footer (Jul 1 2024): Dockets 2022-00039, 2022-00152, 2023-00230, 2024-00014, 2024-00015. Revisions Oct 1 2025 and Jul 1 2026. CMP's pending rate case: 2026-00043 (opened 2/17/2026).
- **Where we learned it:** Primary, partly search summary — local: `context/sources/me_hp_rates/cmp_final_report_2025_2022-152.md`
- **In NEEP:** yes (App A, CMP "TOU").
- **Notes:** A-TOU-OPTS was cancelled Jan 1 2023 (not in NEEP).

### CMP — A-Seasonal Heat Pump (SHP) pilot

- **Category:** TOU-seasonal-only (seasonal volumetric rate; low winter, high summer)
- **Status (Oct 2026):** Expired; CMP filed Docket 2026-00248 "Request for approval of A-Seasonal Heat Pump Rate (10/1/26)" (opened 8/25/2026, status Open).
- **Design:** 5,000-customer pilot, start January 1, 2023, very low winter and very high summer volumetric rates. Enrollment closed 12/31/2024. Expired January 2026.
- **Defining docket:** **2021-00325** (Commission-initiated rate design investigation; Sept 27, 2022 orders approved CMP and Versant stipulations). _[found]_
- **Current governing docket:** 2022-00152 follow-on (extension approved Jan 2024) and the open 2026-00248.
- **Where we learned it:** Primary, partly search summary — local: `context/sources/me_hp_rates/cmp_shp_rate_reconstructed.md`
- **In NEEP:** yes (App A, "seasonal HP pilot ending 2025").
- **Notes:** The pilot ended before the new request, so the offering was not available between January 2026 and 10/1/2026.

### CMP — Electric Technology (ET) rate

- **Category:** other (fixed-charge-heavy flat rate, not time-varying)
- **Status (Oct 2026):** Pilot extended through Jan 31 2027 (tariff stamped 10/31/2025). CMP's page says the rate ends Dec 31, 2026 and CMP asked MPUC to extend or make permanent.
- **Design:** $41.24 service charge and $0.088638/kWh flat (July 2026). Available to all residential customers; breakeven versus Rate A near 642 kWh/month.
- **Defining docket:** **2021-00325** (pilot from Jan 1, 2023). Extension in 2022-00152 (Oct 1 2025 letter). _[found]_
- **Current governing docket:** 2022-00152; pending extension request docket not identified.
- **Where we learned it:** Primary, partly search summary — local: `context/sources/me_hp_rates/cmp_et_rate_july_2026.md`
- **In NEEP:** yes (App A, "Intermittent-use electric tech" is an inaccurate label).
- **Notes:** The local file's header cites Docket 2022-00152 as the rate's docket.

### Versant — A-4 Home Eco time-of-use (Bangor Hydro District) and A-4M (Maine Public District)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active (BHD enrollment 591 per NEEP).
- **Design:** Whole house, including EV and storage. Weekday peak 7 am-12 pm and 4-8 pm; shoulder 12-4 pm; off-peak 8 pm-7 am; weekends shoulder 7 am-8 pm. Winter (Nov-Feb) and non-winter (Mar-Oct) rates are the same. Oct 2025 distribution: $21.59 customer charge; …
- **Defining docket:** **2021-00325** (Sept 27, 2022 Versant stipulation order approving A-4 Home Eco TOU). _[found]_
- **Current governing docket:** A-4 tariff footer Oct 1 2025: Docket 2024-00137 (sixteenth revision; the earlier April 2025 version cites 2023-00336). A-4M: Docket 2023-00336 in April 2025.
- **Where we learned it:** Primary, partly search summary — <https://www.versantpower.com/energy-solutions/eco-rates>
- **In NEEP:** yes (App A, "Seasonal TOU", an inaccurate label).
- **Notes:** Docket 2023-00336 is Versant's BHD distribution rate change; hearings Dec 2024; rates effective 3/31/2025 and Oct 2025.

### Versant — A-20 Home Heating Eco rate (seasonal declining block)

- **Category:** other (seasonal declining-block heating rate)
- **Status (Oct 2026):** Active.
- **Design:** Heating season Oct-Apr; declining block.
- **Defining docket:** The HP/HPWH expansion came from **2021-00325**; the original rate creation was NOT FOUND. _[partial]_
- **Current governing docket:** Tariff footer (Jan 1 2025): ER20-2054-000 (a FERC transmission docket, so not a retail rate order); also 2023-00336 and 2024-00137 for the retail rate base.
- **Where we learned it:** Primary
- **In NEEP:** yes (App A, "seasonal inclining block"; the tariff is declining block, which may be a NEEP error).
- **Notes:** A-2 water heating carries Docket 2024-00137 in the Oct 2025 footer; the origin of A-2 (closed to new customers per NEEP) was not found.

### Maine PUC — time-of-use investigations (statewide)

- **Category:** other (investigations, not a rate)
- **Status (Oct 2026):** 2023-00019 (inquiry on standard offer rate structure; opened 2/2/2023, closed); 2024-00231 (TOU inquiry; opened 8/19/2024, closed); 2025-00176 (formal TOU investigation; opened 6/5/2025, closed). …
- **Design:** Standard offer and delivery TOU structures.
- **Defining docket:** 2023-00019, 2024-00231, 2025-00176. _[found]_
- **Current governing docket:** Informal inquiry (docket not yet identified).
- **Where we learned it:** Primary, partly search summary — <https://www.maine.gov/mpuc/sites/maine.gov.mpuc/files/inline-files/TOU%20Report%20-%20Resolves%202023%20ch.%2079.pdf>
- **In NEEP:** partly (NEEP cites 2024-00231; mislabels another case as 2025-00152).
- **Notes:** The April 2025 TOU report in 2025-00176 was unreadable (empty HTML shell).

## New Hampshire

### Eversource NH — Rate R-OTOD 2 (Residential Time-of-Day Delivery Service)

- **Category:** TOU-whole-home (delivery only; the energy charge is flat)
- **Status (Oct 2026):** Active.
- **Design:** On-peak 1-7 pm weekdays, off-peak otherwise (all weekend/holiday hours off-peak). The June 15, 2021 proposal used noon-7 pm. Oct 2026 rates: $25.73 customer charge; distribution on-peak 8.101 cents/kWh, off-peak 5.943 cents/kWh; …
- **Defining docket:** **DE 21-119** ("Eversource Energy's Proposed Tariff Amendment to Residential Time-of-Day Rate"), Order No. 26,648, July 15, 2022. _[found]_
- **Current governing docket:** Tariff footer (Nov 1 2024): Order 26,648 in DE 21-119 and Order 26,768 in DE 22-039 (1/30/2023). Revenue requirement base: DE 19-057.
- **Where we learned it:** Primary, partly search summary — <https://www.puc.nh.gov/VirtualFileRoom/ShowDocument.aspx?DocumentId=098cbb5f-2686-454e-8ea3-c03bda612c9e>
- **In NEEP:** yes (App A, Eversource "TOU").
- **Notes:** A search synthesis said R-OTOD 2 was approved in DE 19-057; the tariff footers show DE 21-119, so I used that. DE 19-057 only supplies the revenue requirement.

### Eversource NH — Rate R-OTOD (original residential time-of-day)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active in tariff index.
- **Design:** Not analyzed (tariff page 44).
- **Defining docket:** NOT FOUND. _[not found]_
- **Current governing docket:** DE 19-057 (rate case, settlement Order 26,433, 12/15/2020) and DE 22-039.
- **Where we learned it:** Primary
- **In NEEP:** not separately (NEEP lists one Eversource "TOU").
- **Notes:** —

### Eversource NH — legacy controlled water heating, thermal storage (LCS) and space heating

- **Category:** other (load-controlled and off-peak legacy rates; all closed to new customers)
- **Status (Oct 2026):** Closed to new customers.
- **Design:** Rate R uncontrolled and controlled water heating (40-gallon minimum, closed); Rates R-LCS and G-LCS thermal storage (HEATSMART radio-controlled, 8/10/11-hour, switching options; closed); Rate G space heating.
- **Defining docket:** NOT FOUND (legacy, pre-restructuring). _[not found]_
- **Current governing docket:** DE 19-057.
- **Where we learned it:** Primary
- **In NEEP:** yes (App A, "WH (no new customers)" and "electric space heating").
- **Notes:** —

### Eversource NH — residential battery demand response (ConnectedSolutions battery storage; Clean Energy Fund battery rebate)

- **Category:** other (bring-your-own-device battery DR)
- **Status (Oct 2026):** Active.
- **Design:** Customers with batteries purchased after October 1, 2022 enroll through the manufacturer's app; about 40 June-September events, generally 3-8 pm; discharge to a floor of 20%. Plan incentive $275 per kW (residential, 2024-2026 plan). …
- **Defining docket:** **DE 23-068**, Order No. 26,908 (Nov 30, 2023), which converted the active demand reduction pilot into a full program for Eversource, Liberty, and Unitil (not NHEC). The Clean Energy Fund battery rebate came out of Order 26,577 (Feb 4, 2022) in DE 11-250 and DE 14-238, tracked in **DE 22-004** (Order 26,720). (pilot-origin docket for ADR not read). _[partial]_
- **Current governing docket:** DE 23-068 (2024-2026 plan); DE 22-004 for the Clean Energy Fund.
- **Where we learned it:** Primary — <https://www.puc.nh.gov/VirtualFileRoom/ShowDocument.aspx?DocumentId=196a3283-9edd-43c8-a40c-bcf73cd40efb>
- **In NEEP:** yes (App A, "Battery DR").
- **Notes:** The NHSaves ADR pilot predates the plan; its original docket (likely under DE 20-092) was not confirmed.

### Liberty NH — Rate D-10 Optional Peak Load Pricing (residential time-of-day)

- **Category:** TOU-whole-home (delivery-side peak/off-peak)
- **Status (Oct 2026):** Active.
- **Design:** Customer charge $14.74. Peak 8 am-9 pm weekdays (excluding holidays); off-peak otherwise. Distribution on-peak 14.054 cents/kWh, off-peak 0.186 cents/kWh. Includes an off-peak water-heating switch option.
- **Defining docket:** NOT FOUND (predates the DE 19-064 tariff). (governing dockets only). _[not found]_
- **Current governing docket:** Tariff footer (Apr 1 2025): Procedural Order in DE 23-039 (March 25, 2025). The original D-10 page footer cites Order 26,376 in DE 19-064 (June 30, 2020).
- **Where we learned it:** Primary
- **In NEEP:** yes (App A, Liberty "TOU" and "off-peak WH").
- **Notes:** No Liberty "WH DR" or PTR program was found (see Unresolved).

### Liberty NH — Rate D-11 Battery Storage Pilot (seasonal TOU)

- **Category:** TOU-seasonal-only (seasonal three-period TOU tied to behind-the-meter batteries)
- **Status (Oct 2026):** Active pilot; seasonal rates adjusted in Docket DE 25-027 (closed).
- **Design:** Leased Tesla Powerwall 2 batteries under Liberty control. Seasonal TOU: summer May-Oct, winter Nov-Apr; off-peak 8 pm-8 am, mid-peak 8 am-3 pm weekdays (8 am-8 pm weekends/holidays), critical peak 3-8 pm weekdays. Oct 2024: critical peak total $0.48875/kWh; …
- **Defining docket:** **DE 17-189**, Order No. 26,209, January 17, 2019 (up to 500 batteries; Phase 1 limited to 200 batteries/100 customers; Phase 2 conditional). _[found]_
- **Current governing docket:** Tariff footer cites Orders 26,376 and 26,377 in DE 19-064 (June 30, 2020); seasonal rate adjustments in DE 25-027; rate case DE 23-039.
- **Where we learned it:** Primary — <https://www.clf.org/wp-content/uploads/2019/01/26-209.pdf>
- **In NEEP:** yes (App A, "battery storage pilot w/ seasonal TOU").
- **Notes:** —

### Unitil Energy Systems — Whole House TOU (TOU-D, now Schedule TOU-R)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active (NH residential customers only).
- **Design:** Optional residential rate for regular use, EV charging, quick-recovery water heating, and space heating. Weekdays: mid-peak 6 am-3 pm, on-peak 3-8 pm, off-peak 8 pm-6 am; weekends and holidays off-peak. 12-month commitment. Not combinable with net metering.
- **Defining docket:** **DE 21-030** (Unitil rate case). Settlement Agreement of Feb 11, 2022, Section 6.6, requires a three-component (distribution, transmission, generation) time-differentiated whole-house TOU, effective by August 1, 2022 at the latest. The specific order number approving the permanent-rates settlement was not captured. (order number missing). _[found]_
- **Current governing docket:** **DE 25-025**, Order No. 28,225 (May 28, 2026), tariff NHPUC No. 3 ninth revised page 1, effective May 1, 2026.
- **Where we learned it:** Primary — <https://www.sec.gov/Archives/edgar/data/755001/000119312522154072/d344598dex993.htm>; <https://unitil.com/time-of-use>
- **In NEEP:** yes (App A, Unitil "TOU").
- **Notes:** The Dec 2025 rate sheet calls the schedule TOU-D; the May 2026 tariff index lists TOU-R.

## Vermont

### GMP — Rate 14 Residential TOU + critical peak pricing ("Empower")

- **Category:** TOU-whole-home (with critical peak pricing; not a rebate)
- **Status (Oct 2026):** Active; closed to nothing found. Launched August 2016.
- **Design:** Daily charge $0.876. Peak 1-9 pm Mon-Fri $0.35003/kWh; off-peak $0.14920/kWh. Critical peak 12-8 pm, up to 10 weekdays May 1-Sep 30 with day-ahead notice, $0.92529/kWh. Requires AMI and a one-year term. (Rates from the October 2026 GMP tariff PDF.)
- **Defining docket:** Docket 8525, Vermont Public Service Board, Final Order March 24, 2016: "approved two new residential critical peak pricing rate classes, Rate 9 and Rate 14". _[found]_
- **Current governing docket:** GMP multi-year regulation plan annual rate filings. FY26: 25-1069-TF (order 8/29/2025). FY27: 26-0096-TF (asked 7.5%, approved 5.51%, order 9/30/2026; the order date comes from a secondary site, `utilityratecalc.com`). …
- **Where we learned it:** Primary, partly search summary — <https://epuc.vermont.gov/?q=downloadfile%2F403417%2F144640>; <https://epuc.vermont.gov/?q=downloadfile%2F777060%2F204813>
- **In NEEP:** yes (App A, GMP "TOU+CPP"; NEEP's link points to Rate 9).
- **Notes:** A search synthesis attributed Rates 9 and 14 to "Docket 8794". The primary testimony says Docket 8525, which I used.

### GMP — Rate 9 Residential critical peak pricing

- **Category:** other (CPP rate, not a rebate)
- **Status (Oct 2026):** Active.
- **Design:** Daily charge $0.660. Critical-peak event price $0.92123/kWh; all other hours $0.21742/kWh. Requires AMI, one-year term.
- **Defining docket:** Docket 8525, VT Public Service Board, Final Order March 24, 2016. _[found]_
- **Current governing docket:** Same GMP annual tariff filings as Rate 14 (25-1069-TF, 26-0096-TF).
- **Where we learned it:** Primary
- **In NEEP:** yes (App A, "CPP").
- **Notes:** GMP's Rate 9 is the rate NEEP's CPP hyperlink resolves to.

### GMP — Rate 11 Residential time-of-use

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active.
- **Design:** Daily charge $0.876. Peak 1-9 pm weekdays $0.35949/kWh; off-peak $0.15322/kWh.
- **Defining docket:** The original creating docket was NOT FOUND. Docket 8525 (Final Order 3/24/2016) integrated Rate 11 and approved the current TOU periods, per the same Anderson testimony. (revision, not creation). _[not found]_
- **Current governing docket:** 25-1069-TF, then 26-0096-TF (annual MYRP tariff filings).
- **Where we learned it:** Primary
- **In NEEP:** yes (App A, "TOU").
- **Notes:** Tried searching ePUC and PSB for a pre-2016 Rate 11 order; nothing surfaced.

### GMP — Rate 22 Seasonal time-of-use

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** Active.
- **Design:** Same rates as Rate 11. Peak May-Oct 1-9 pm weekdays; Nov-Apr 7:30-11:30 am and 4:30-8:30 pm weekdays.
- **Defining docket:** NOT FOUND. Candidate: Case 18-2850-TF (rate-design proceeding for rates effective April 1, 2019; investigation opened 9/21/2018; final order 12/21/2018). I found no source stating Rate 22 was approved there. _[not found]_
- **Current governing docket:** 25-1069-TF, then 26-0096-TF.
- **Where we learned it:** Primary
- **In NEEP:** yes (App A, "seasonal TOU").
- **Notes:** The timing (absent in August 2018, present in February 2019) points to 18-2850-TF, but this is unverified.

### GMP — Rate 3 off-peak water heating

- **Category:** other (off-peak water heating; note only per assignment)
- **Status (Oct 2026):** Exists in GMP tariff book.
- **Design:** Not analyzed.
- **Defining docket:** NOT FOUND (not searched in depth; out of scope beyond noting existence). _[not found]_
- **Current governing docket:** GMP annual tariff filings (25-1069-TF, 26-0096-TF).
- **Where we learned it:** Official page
- **In NEEP:** yes (App A, "off-peak WH").
- **Notes:** —

### GMP — Battery demand response (Bring Your Own Device; Energy Storage Access Program Rider)

- **Category:** other (battery demand response; note only per assignment)
- **Status (Oct 2026):** Active.
- **Design:** Customer-owned battery dispatch for GMP peak events.
- **Defining docket:** NOT FOUND. The only docket I saw in the add-on tariff PDFs is the Solar Energy Affordability Program Pilot: Case 17-4894-INV (the 2017 Ratepayer Benefit Plan). The BYOD program docket was not located. _[not found]_
- **Current governing docket:** Unknown.
- **Where we learned it:** Primary
- **In NEEP:** yes (App A, "Battery DR").
- **Notes:** Worth a targeted ePUC search for "bring your own device" and the energy storage rider.

## Massachusetts

### Eversource MA (NSTAR Electric) — Residential Heat Pump Rates R1HP / R2HP (optional seasonal rate)

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** Active.
- **Design:** Optional rate for R-1/R-2 customers with an eligible heat pump (whole-home usage priced on the rate). Winter (Nov–Apr) distribution charge is lower than summer, and from the 2026–27 heating season the winter transmission charge is lower too. …
- **Defining docket:** **D.P.U. 25-55**, MA DPU, order 2025-07-29 (approved with modifications NSTAR Electric's seasonal heat pump rate and a marketing, education and outreach (MEO) plan). It was opened because the umbrella investigation **D.P.U. 25-08** (opened 2025-01-31 on a DOER petition; order 2025-03-21) directed Eversource to file a rate by 2025-05-15 like the National Grid/Unitil rates. _[found]_
- **Current governing docket:** **D.P.U. 25-08-A** (Order on Seasonal Heat Pump Rates, 2026-06-01: winter transmission charges; told National Grid and Unitil to match Eversource's design). …
- **Where we learned it:** Primary — <https://www.eversource.com/residential/account-billing/manage-bill/about-your-bill/rates-tariffs/electric-delivery-rates/ema>; <https://eeaonline.eea.state.ma.us/dpu/fileroom/#/dockets/docket/12533> — local: `context/sources/ma_hp_rates/madpu_25-08_order_seasonal_heat_pump_rates.md`, `context/domain/electric_heating_and_heat_pump_rates.md`
- **In NEEP:** yes — Appendix A: "MA Eversource: Seasonal heat pump" (Table 2 "Seasonal Only Rates").
- **Notes:** Docket 25-55 contains the workbooks (compliance Exh. ES-HP-2 Sch. 3 etc.). The 2025 order cites D.P.U. 25-55 at 23, 27 for the interim-rate rationale.

### National Grid MA (Massachusetts Electric / Nantucket Electric) — Residential Heat Pump Rate (R-1 HP / R-2 HP; optional seasonal rate)

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** Active (in place for the 2025–26 heating season).
- **Design:** Same structure as Eversource's: optional, whole-home, lower winter distribution charge, plus winter transmission charge from the 2026–27 heating season. DPU rejected National Grid's own "heating electrification pricing option" and told it to file a Unitil-style heat pump rate.
- **Defining docket:** **D.P.U. 23-150**, MA DPU, base distribution rate case order 2024-09-30, pp. 509–513. _[found]_
- **Current governing docket:** **D.P.U. 25-08-A** (2026-06-01) and compliance filing **D.P.U. 26-71** (winter transmission charge, stamped 2026-07-29).
- **Where we learned it:** Primary — local: `context/sources/ma_hp_rates/ngrid_26-71_residential_transmission_hp_rate_design.md`
- **In NEEP:** yes — Appendix A: "MA National Grid: Seasonal heat pump".
- **Notes:** none.

### Unitil (Fitchburg Gas & Electric) MA — Heat Pump Rate (R-1 / R-2 HP; optional seasonal rate)

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** Active.
- **Design:** Same structure. First MA heat-pump rate to be ordered. Unitil reported over 1,300 customers on the rate (Oct 2026, per our domain summary).
- **Defining docket:** **D.P.U. 23-80** (Fitchburg Gas and Electric Light Co. electric base rate case; D.P.U. 23-81 is the gas case decided in the same joint order; order dated Jun 28, 2024, heat pump section printed pp. 399–409). _[found]_
- **Current governing docket:** **D.P.U. 25-08-A** (2026-06-01) and compliance filing **D.P.U. 26-72** (winter transmission charge, stamped 2026-07-31).
- **Where we learned it:** Primary — <https://unitil.com/ma-discount-rate>
- **In NEEP:** yes — Appendix A: "MA Unitil: Seasonal heat pump".
- **Notes:** none.

### All MA EDCs — Statewide default time-varying rate framework for basic service (default TOU with critical peak price; opt-out to flat rate with peak time rebate)

- **Category:** other (adopted policy framework; no TVR is currently offered to MA residential customers). …
- **Status (Oct 2026):** Framework adopted; implementation deferred to a future order. Not in effect.
- **Design:** After AMI deployment, each EDC would offer basic-service customers (1) a default TOU rate with a CPP component, and (2) an opt-out to a flat rate with a peak time rebate. The framework was adopted without modification from the interim order.
- **Defining docket:** **D.P.U. 14-04-C**, MA DPU, "Order Adopting Policy Framework for Time Varying Rates" (final order in the DPU's own-motion investigation D.P.U. 14-04 opened 2014-01-23; the Interim Order preceded it). Order date NOT retrieved — it is a 2014 order (the repository record is dated 2014; the text cites a 2014-11-05 order in D.P.U. 12-76-C). _[found]_
- **Current governing docket:** **D.P.U. 26-62** (DPU's TVR investigation for default service, opened 2026-06-30 on DOER's 2026-04-08 petition — see next entry). Grid modernization plans in **D.P.U. 21-80 / 21-81 / 21-82** (Eversource / National Grid / Unitil; …
- **Where we learned it:** Primary, partly search summary — <https://archives.lib.state.ma.us/handle/2452/614487>; <https://www.mass.gov/info-details/grid-modernization-and-ami-resources>; <http://www.energychoicematters.com/stories/20260630aa.html>
- **In NEEP:** not as a rate. NEEP (line ~197) says MA "has proposals to create statewide default opt-out rates"; Table 2 shows no MA daily TVR except Unitil EV TOU.
- **Notes:** **Correction to the assignment's pointer:** D.P.U. 20-69 is the Grid Modernization Phase II docket, not a TVR docket. The TVR policy lives in D.P.U. 14-04-C, and the current TVR proceeding is D.P.U. 26-62. …

### All MA EDCs — DOER-proposed default (opt-out) residential TOU rates (D.P.U. 26-62)

- **Category:** TOU-whole-home (proposed)
- **Status (Oct 2026):** Investigation open (opened 2026-06-30); no rate approved.
- **Design:** DOER recommends default opt-out TOU rates that vary supply, transmission and distribution charges with a single consolidated 4–8 p.m. peak (HE 17–20) across all three load zones, plus shadow billing, bill stabilization and opt-out protections; …
- **Defining docket:** **D.P.U. 26-62** (opened on DOER's 2026-04-08 petition; the Interagency Rates Working Group's 2025 recommendation of opt-out seasonal TOU feeds it). _[found]_
- **Current governing docket:** **D.P.U. 26-62**; related **D.P.U. 25-200** (own-motion inquiry into gas and electric delivery charges and bill redesign, Vote and Order 2025-12-15).
- **Where we learned it:** Primary, partly search summary — <https://www.mass.gov/doc/doers-time-of-use-rate-proposal/download>; <https://www.mass.gov/info-details/massachusetts-electric-rate-task-force> — local: `context/sources/ma_hp_rates/madpu_25-08_order_seasonal_heat_pump_rates.md`
- **In NEEP:** not in NEEP's tables; mentioned in text as "proposals to create statewide default opt-out rates" (NEEP predates the filing).
- **Notes:** There is no MA EDC residential opt-in TOU tariff in force. In April 2025 testimony the Attorney General's expert wrote that National Grid "does not currently offer time-varying rates or other managed charging programs" (Synapse exhibit in D.P.U. 24-195/196/197) — SEARCH-SUMMARY of a primary exhibit.

### Eversource MA, National Grid MA, Unitil — ConnectedSolutions (residential smart-thermostat and battery demand response)

- **Category:** other (device-control demand response — NOT price-based PTR; note only)
- **Status (Oct 2026):** Active; DPU approved an improved ConnectedSolutions with modifications in the 2025–2027 plan order.
- **Design:** Mass Save program: customers enroll a smart thermostat or battery and the Program Administrators call peak events (the plan order describes control of "certain thermostats or battery storage systems to reduce energy usage during the system peak"). Incentive amounts not read. …
- **Defining docket:** **D.P.U. 24-140 through 24-149**, MA DPU, Order on the 2025–2027 Three-Year Energy Efficiency Plans, 2025-02-28 (electric: NSTAR Electric 24-149, National Grid 24-148, Fitchburg/Unitil 24-147, Cape Light Compact 24-146). The program's own original docket (earlier three-year plans, e.g. D.P.U. 18-110 to 18-119 for 2019–2021) was NOT verified. _[found]_
- **Current governing docket:** same (2025–2027 plan order; interim continuation beyond).
- **Where we learned it:** Primary — <https://www.mass.gov/info-details/energy-efficiency-dockets-and-filings>; <https://www.mass.gov/doc/2025-2027-three-year-energy-efficiency-plans-order/download>
- **In NEEP:** yes — Appendix A: "Eversource: PTR; Battery DR" and "National Grid: PTR; Battery DR" (NEEP labels the thermostat program a PTR in the events-based …
- **Notes:** NEEP's "PTR" for MA is this device-control program, not a bill-credit PTR tied to a tariff. User flagged as note-only.

## Rhode Island

### Rhode Island Energy (RIE; The Narragansett Electric Co.) — Whole-home TOU / time-varying rate (TVR): none in effect; development ordered

- **Category:** TOU-whole-home (not yet offered)
- **Status (Oct 2026):** Not offered. On 2026-08-21 the PUC rejected recovery of "Grid X" software costs tied to TOU development (vote 23) and, per the Attorney General, required RIE "to propose a schedule for Time of Use …
- **Design:** No residential TOU, CPP, demand-charge or other time-varying delivery rate exists in RI. RIE filed a "framework for development of time-varying rates and a TVR implementation plan" (Atrium Economics testimony, Book 5) in its 2025 rate case. …
- **Defining docket:** **PUC Docket 25-45-GE** (RIE base distribution rate case, filed 2025-11-26, consolidated with 25-33-GE; RI PUC; open-meeting decision 2026-08-21; written order NOT FOUND, not on the docket page as of my fetch). Background: **Docket 22-49-EL** (Advanced Metering Functionality business case; vote 2023-09-27, written **Order 25353**, dated 2025-05-20 per my earlier notes). … _[found]_
- **Current governing docket:** 25-45-GE (compliance filing 2026-08-27; tariffs effective 2026-09-01). The follow-on TOU schedule docket NOT FOUND (none opened as of the docket pages I read).
- **Where we learned it:** Primary, partly search summary — <https://ripuc.ri.gov/Docket-25-45-GE>; <https://ripuc.ri.gov/sites/g/files/xkgbur841/files/2026-10/Mins%20%2825-45-GE%2025-33-GE%29%20August%2021%202026.pdf>; <https://riag.ri.gov/press-releases/attorney-general-neronha-helps-secure-170-million-bill-credits-climate-mandates> — local: `context/sources/ri_hp_rates/ripuc_2545GE_rie_response_to_motions_to_intervene.md`
- **In NEEP:** consistent with NEEP. Appendix A and Tables 2–5 list "None" for RI on time-varying rates (RI row in Appendix A: "RI Energy | None | None | None").
- **Notes:** The AG release and the minutes are the only sources I read for the TOU direction; the minutes' motion list I extracted does not itself contain a TOU-schedule motion (the PUC says some items were given as direction in the order without a motion), so wait for the written order before citing the deadline.

### Rhode Island Energy — Residential seasonal volumetric distribution charge (A-16, Tariff No. 2313): ordered, not yet visible in tariff

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** Ordered 2026-08-21. The A-16 tariff (RIPUC No. 2313, issued 2025-11-26, effective 2026-09-01) and the Summary of Retail Delivery Rates (Tariff 2095, 9/1/26) that I read show a single A-16 …
- **Design:** Two seasons: winter = December–March usage; non-winter = April–November. Ratio of winter to non-winter base distribution volumetric charge equals the winter-peak to summer-peak ratio from RIE's response to PUC 2-2(b); the winter/non-winter gap may not exceed 1.5¢/kWh. …
- **Defining docket:** **PUC Docket 25-45-GE** (open-meeting vote 39, 2026-08-21; written order NOT FOUND). Origin of the idea: CLF's heat pump rate proposal in the same docket (see next entry). _[found]_
- **Current governing docket:** 25-45-GE compliance filing (2026-08-27) and tariff filings.
- **Where we learned it:** Primary, partly search summary — <https://ripuc.ri.gov/sites/g/files/xkgbur841/files/2026-08/Tariff%20No.%202313%20-%20Electric%20A-16%20Service%20Tariff%20-%20Effective%2009-01-2026.pdf>; <https://ripuc.ri.gov/sites/g/files/xkgbur841/files/2026-09/Compliance%20-%20RIPUC%20Nos.%202095%20%26%202096%20-%20PUC%209-29-26.pdf>; <https://www.rienergy.com/site/ways-to-save/rates-and-shopping/service-rates/residential-service-rates>
- **In NEEP:** not in NEEP (post-dates it).
- **Notes:** This is a seasonal rate on the _delivery_ volumetric charge only, not TOU, and applies to all residential customers rather than only heat pump customers. Our local domain file `context/domain/electric_heating_and_heat_pump_rates.md` describes RI-1 as a pending proposal; the docket now shows it was decided.

### Rhode Island Energy — Heat pump rate (CLF proposal resolved by settlement; no HP-specific rate adopted)

- **Category:** other (heat pump rate; proposal)
- **Status (Oct 2026):** No HP-specific rate. The PUC's formal action on the HP settlement is NOT VERIFIED: the minutes I read contain no "heat pump" motion. …
- **Design:** CLF proposed a separate lower winter volumetric delivery rate for electric heat pump customers. The 2026-05-26 Heat Pump Settlement (RIE, CLF, later Amtrak) replaces it with a commitment that RIE file a Demand Side Management (DSM) Investment Proposal under the Least Cost …
- **Defining docket:** **PUC Docket 25-45-GE** (Heat Pump Settlement filed 2026-05-26; updated signatures 2026-06-09). _[found]_
- **Current governing docket:** 25-45-GE; future DSM Investment Proposal docket NOT FOUND; LCP Standards docket **26-15-EE** (referenced only).
- **Where we learned it:** Primary — <https://ripuc.ri.gov/sites/g/files/xkgbur841/files/2026-06/25-45-GE-Heat%20Pump%20Settlement%20-%20Added%20Signatures%20%28PUC%206-9-2026%29.pdf>
- **In NEEP:** not in NEEP.
- **Notes:** Relevant to our heat pump rate work: RI has no HP rate and the seasonal delivery rate above is the closest outcome.

### Rhode Island Energy — ConnectedSolutions residential demand response: Bring Your Own Thermostat (BYOT) and RSB Battery (note only)

- **Category:** rebate-other (device-control demand response; NOT price-based PTR) — note only
- **Status (Oct 2026):** Active for program years 2024–2026; three-year budget `$28,567,600` (excluding OER allocations).
- **Design:** BYOT: `$50` upfront plus `$20` end-of-season incentive for allowing thermostat control during peak events. RSB Battery: per-kW incentives (`$225`/kW for batteries on or after 2024-06-01, `$200`/kW after a five-year look-back). Residential and C&I pathways.
- **Defining docket:** **PUC Docket 24-06-EE** (System Reliability Procurement investment proposal for electric demand response, 2024–2026 ConnectedSolutions). Open meetings 2024-07-01, 2024-07-16 (SRP factor, effective 2024-08-01) and 2024-07-30; **written Order 25306 issued 2025-04-22**. The order did not pre-approve incentive levels or design details. _[found]_
- **Current governing docket:** 24-06-EE (annual reports due February 15; final reconciliation due 2027-02-15). Parent three-year plan **Docket 23-35-EE** (Order 25092, 2024-07-03 per my earlier notes).
- **Where we learned it:** Primary
- **In NEEP:** NEEP's RI row lists no demand-flexibility offering. Not in NEEP.
- **Notes:** Included only because the user asked for PTR/ConnectedSolutions notes; NEEP's CT "PTR" entries have the same device-control character.

## Connecticut

### Eversource CT (CL&P) — Residential Time-of-Day Electric Service, Rate 7 (whole-home TOU)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active. Proposed for redesign in the pending Eversource rate case (customer charge `$9.62` → `$12.36` with Rate 1; TOD calculations in Exhibit CLP-RATES-2.8; …
- **Design:** Optional, opt-in; any residential customer, one-year commitment, requires a time-of-day meter installed free. On-peak = weekdays 12 noon–8 p.m.; off-peak = all other hours (~24% / ~76% of weekly hours). …
- **Defining docket:** **05-10-03RE01**, CT DPUC (now PURA), Decision dated 2007-12-19 — "Application of CL&P to Implement Time-of-Use, Interruptible Load Response, and Seasonal Rates" (implementing PA 05-1 §13 / CGS §16-243n). That decision directed redesigned _voluntary_ residential Rate 7 TOU effective 2008-01-01 (and phased mandatory residential TOU from 2009, later shelved). … _[found]_
- **Current governing docket:** Base-rate design of record is the last CL&P rate case, **17-10-46** (Eversource testimony in 26-05-10 calls it "the last rate case"; the exact 17-10-46 decision date was not retrieved — INFERRED, not read); …
- **Where we learned it:** Primary — <https://www.eversource.com/docs/default-source/rates-tariffs/ct-electric/rate-7-ct.pdf?sfvrsn=8b3bb93f_17>; <https://openei.org/w/images/b/bf/Utility_Rate_CPL_res_TOU_rate1.pdf>; <https://www.ehs.group/PDF/Connecticut/Dft%2005-10-03RE04%20CLP%20Mtr%20Deployment%20Plan-PURA.pdf> — local: `context/sources/ct_hp_rates/exhibit_clp_rates_1.md`
- **In NEEP:** yes — Appendix A row "CT / Eversource: Daily TVR = TOU – with variable peak pricing"; reference URL = the Rate 7 PDF above (Appendix E).
- **Notes:** NEEP Table 3 puts Eversource in "daily TVR" but Table 2 (tech-specific / daily-TVR column) shows CT = "None" for daily time varying rates; internal inconsistency in NEEP. Rate 7 is _not_ seasonal. Rate 7 is also subject to the LIDR (usage cap 1,200 kWh/mo, applied to on-peak first — see LIDR entry).

### Eversource CT (CL&P) — Variable Peak Pricing (VPP) Rider (daily-varying on-peak generation on top of Rate 7)

- **Category:** TOU-whole-home (variable peak pricing; closest NEEP category "TOU with variable peak pricing"; …
- **Status (Oct 2026):** Active (CL&P rider still in tariff); UI has the parallel Rider VPP (C.P.U.C.A. No. 934).
- **Design:** Opt-in rider for Standard Service customers already on a TOD rate (Rate 7 for residential) with interval metering. Replaces the fixed monthly on-peak generation charge with a daily price posted the prior day (day-ahead ISO-NE CT zone average + adder); off-peak priced monthly. …
- **Defining docket:** **03-07-02RE10**, CT DPUC, Letter Ruling dated 2008-06-26 (effective 2008-07-01); superseded by Decision dated 2011-09-21 in **03-07-02RE11** (effective 2012-01-01) which changed how VPP prices are set. Statutory driver: PA 07-242 §99 (voluntary CPP/RTP tariffs). UI's equivalent: **12-01-02** (Decision 2011-12-22), re-issued under **17-01-02 & 17-03-02** (Decision 2016-12-22) per UI tariff footer. _[found]_
- **Current governing docket:** none specific — rider revisions ride RAM/Standard Service dockets; I did not find the current CL&P rider footer (the PDF on eversource.com is the Jan-2012 version).
- **Where we learned it:** Primary, partly search summary — <https://www.eversource.com/clp/vpp/downloads/VPP_Rider.pdf>; <https://www.uinet.com/documents/d/uinet/0-1-schedule-of-rates-and-riders-1>; <https://www.eversource.com/residential/account-billing/manage-bill/about-your-bill/rates-tariffs/connecticut-variable-peak-pricing/connecticut-variable-peak-pricing-faqs>
- **In NEEP:** yes (Appendix A "TOU – with variable peak pricing"; Section 4 narrative ~line 477).
- **Notes:** NEEP states Eversource chose VPP "because of state legislation about real-time pricing" — consistent with PA 07-242 §99. Participation was only 14 C&I customers as of ~2010 per PURA's 2010s decision; residential VPP uptake not found.

### United Illuminating (UI) — Residential Time-of-Use Rate RT (C.P.U.C.A. No. 2526)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active (Sept 1, 2026 sheet). Earlier 2006 DPUC order had also mandated TOU for the highest-use UI residential customers on a 2007–2010 glide path (1,000–4,000+ kWh/mo thresholds); …
- **Design:** Optional, individually metered residential customers with TOU meter. Peak = weekdays 12 noon–8 p.m.; off-peak = all other hours. Standard-service generation 14.6194¢ peak vs 11.1194¢ off-peak (Jul–Dec 2026); transmission 17.0695¢ peak vs 0 off-peak (all year); …
- **Defining docket:** **05-06-04**, CT DPUC, final decision 2006 (UI rate-design decision, implementing PA 05-1 §13). Source for this is the OLR summary of the _draft_ decision (CGA 2006-R-0503) — SEARCH-SUMMARY; I did not open the 2006 decision. LIDR decision fn. 32 says the older UI electric-heating tariff "was subsumed into Rate RT in 2006", consistent with 05-06-04. … _[found]_
- **Current governing docket:** tariff sheet cites **26-01-04** (Decision 2026-08-19, eff. 2026-09-01) and **26-01-02** (Decision 2026-05-20), the semiannual RAM/standard-service dockets; …
- **Where we learned it:** Primary, partly search summary — <https://www.uinet.com/documents/d/uinet/0-1-schedule-of-rates-and-riders-1>; <https://www.uinet.com/documents/d/uinet/11-rate-rt>; <https://www.uinet.com/w/time-of-day-rate-rt>
- **In NEEP:** yes (Appendix A: UI "TOU"; Appendix E link to Rate RT page).
- **Notes:** UI is one of the few NE utilities where TOU is built on a mandatory-for-high-users history. Peak/off-peak delivery is flat; only supply and transmission are time-differentiated.

### United Illuminating (UI) — Residential Load Control Rider RLC (C.P.U.C.A. No. 433)

- **Category:** other (load control tied to Rate RT off-peak hours; note only)
- **Status (Oct 2026):** Active tariff, effective 2007-01-01.
- **Design:** Optional add-on for TOU customers; UI installs a load-control center (`$4.85`/month) that times designated loads (e.g., water heater) to Rate RT off-peak hours.
- **Defining docket:** **05-06-04** Supplemental Decision dated 2006-08-30 (per tariff footer). _[found]_
- **Current governing docket:** same.
- **Where we learned it:** Primary
- **In NEEP:** not in NEEP.
- **Notes:** Included for completeness; no evidence of significant enrollment.

### Eversource CT — Rate 5 Residential Electric Heating Service (legacy electric-heating rate; seasonal-only? — it is a flat electric-heating class, not seasonal)

- **Category:** other (technology-specific: electric heating; closed)
- **Status (Oct 2026):** Closed to new customers.
- **Design:** Legacy electric space-heating rate; closed to new customer enrollments. Used as LIDR "electric heating" proxy (6% energy burden target). Supply rate is identical to Rate 1 in standard service tables.
- **Defining docket:** NOT FOUND (a pre-2000 DPUC rate class; tried: Eversource filings, PURA LIDR decision, 26-05-10 testimony). _[not found]_
- **Current governing docket:** **26-05-10** (proposes replacing the growth path with optional Rate 6, below); until then RAM dockets (26-01-0x).
- **Where we learned it:** Primary — local: `context/sources/ct_hp_rates/exhibit_clp_rates_1.md`
- **In NEEP:** yes (Appendix A: "Electric heating service (no new customers)"; Table 2 "Technology Discount Rates: Eversource (EH)").
- **Notes:** NEEP labels this a "technology discount rate"; in the tariff it is its own residential class.

### Eversource CT — Proposed Rate 6 Optional Residential Space Heating (seasonal heat-pump rate) — PENDING

- **Category:** TOU-seasonal-only (proposed; winter-block structure)
- **Status (Oct 2026):** Proposed (filed 2026-07-14), rate year starting 2027-07-01; parties intervening (Acadia Center, CLF).
- **Design:** Optional rate for customers who adopt an air-source heat pump. Block 1 `$0.09431`/kWh up to ~700 kWh baseline; winter Block 2 `$0.07517`/kWh above 700 kWh (marginal-cost-based tail). Customer charge `$12.36` (Rate 1 and Rate 7 MRCC). Not mandatory for HP adopters.
- **Defining docket:** **26-05-10**, PURA, filed 2026-07-14 — Application of CL&P to Amend its Rate Schedules (Presiding Officer Thomas H. Wiehl). _[found]_
- **Current governing docket:** **26-05-10** (pending).
- **Where we learned it:** Primary — <https://www.eversource.com/residential/about/reliability/ct-electric-rate-review>; <https://egov.ct.gov/PMC/Agenda/Download/32432> — local: `context/sources/ct_hp_rates/exhibit_clp_rates_1.md`
- **In NEEP:** not in NEEP (NEEP predates the filing; Appendix A lists CT "Seasonal-only: None").
- **Notes:** Directly relevant to Switchbox's HP-rate work. Workbooks: Exhibit CLP-RATES-2 (xlsx), CLP-RATES-6 (xlsx), CLP-MCOS-*, CLP-ACOS-1 are in the docket.

### Eversource CT / UI — Time-varying-rate education & engagement mandate (SB 4 §21, PA 25-173)

- **Category:** other (policy driver; no rate)
- **Status (Oct 2026):** Statute effective 2025-10-01; Eversource plan pending in 26-05-10.
- **Design:** In any rate case initiated on/after 2025-07-01 each EDC must file an outreach/education plan on time-varying rates (consult OCC and DEEP). Eversource filed this as Exhibit CLP-RATES-8 in 26-05-10.
- **Defining docket:** statute (Senate Bill 4 as enacted; sec. 21), implemented in **26-05-10**; UI's equivalent would be in its next rate case (no docket on record — NOT FOUND). _[found]_
- **Current governing docket:** **26-05-10**.
- **Where we learned it:** Primary, partly search summary — local: `context/sources/ct_hp_rates/exhibit_clp_rates_1.md`
- **In NEEP:** not in NEEP.
- **Notes:** Eversource also has to respond to PURA's 22-08-06 direction to revisit the whole-house TOU rate.

### Eversource CT / UI — Smart-thermostat demand response: ConnectedSolutions (Eversource) and Smart Savers Rewards (UI)

- **Category:** rebate-PTR (closest: event-based pay-for-performance; NEEP labels it PTR)
- **Status (Oct 2026):** Active; Eversource has paused new ConnectedSolutions _battery_ enrollments in favour of ESS; thermostat program continues through 2027.
- **Design:** Opt-in, BYO-thermostat summer events (Jun–Sep, ~10–20 events, ≤3 hrs, ≤4°F setback, roughly 3–8 p.m.). Eversource: `$50` enrollment (`$100` income-eligible) + `$20`/yr; UI: `$35` enrollment + `$25`/season e-gift cards. …
- **Defining docket:** Approved through DEEP's three-year Conservation & Load Management (C&LM) Plan — **2025–2027 C&LM Plan**, DEEP Final Determination 2025-09-09 (budget Interim Decision 2024-12-20; 2026 Plan Update filed 2025-10-31/2026-03-01). This is a DEEP proceeding; the determination PDF did not print a docket number — docket NOT FOUND/UNVERIFIED. _[found]_
- **Current governing docket:** same (2026 Plan Update to 2025–2027 C&LM Plan).
- **Where we learned it:** Primary — <https://www.energizect.com/sites/default/files/documents/%235a_Draft%20Determination%20and%20Comment%20Request%202025_2027%20CLM.pdf>; <https://www.energizect.com/explore-solutions/smart-thermostat-demand-response>; <https://www.uinet.com/smartenergy/rebatesandprograms/ui-smart-savers-rewards>
- **In NEEP:** yes (Appendix A "PTR" for both CT utilities; Appendix E cites UI Smart Savers).
- **Notes:** This is a _device-control_ rebate, not a price-based peak-time rebate; PURA doesn't set it. The only CT pure PTR-style program I found is none.

### Eversource CT / UI — Energy Storage Solutions (ESS) program (battery demand response; note only)

- **Category:** other (battery storage DR; NEEP "Battery DR")
- **Status (Oct 2026):** Active; Year-5 changes effective 2026-04-01.
- **Design:** 9-year statewide program (2022–2030, 580 MW goal). From 2026-04-01 ("Construct 5"): performance-based active dispatch only — customers paid per kW delivered across ~50 summer and 5 winter events (≈`$300`/kW-yr standard residential per Tesla summary), plus a residential …
- **Defining docket:** **17-12-03RE03**, PURA, Final Decision 2021-07-28 (PA 21-53). Annual reviews: 21-08-05 (2021-12-08), 22-08-05 (2022-12-21), 23-08-05 (2023-11-29), 24-08-05 (2024-12-04), **25-08-05** (2025-12-17). _[found]_
- **Current governing docket:** **25-08-05** (Year 5) and open **26-08-05** (Year 6; presumed — not verified).
- **Where we learned it:** Primary — <https://portal.ct.gov/pura/electric/office-of-technical-and-regulatory-analysis/clean-energy-programs/energy-storage-solutions-program>; <https://portal.ct.gov/-/media/PURA/electric/Final-Decision-17-12-03RE03.pdf>; <https://energystoragect.com/wp-content/uploads/2026/02/ESS-Program-Manual-Revised-for-02112026-CLEAN.pdf>
- **In NEEP:** yes (Appendix A "Battery DR"; Appendix E).
- **Notes:** Eversource's ConnectedSolutions _battery_ (BYOD) program has had new enrollments paused since DEEP's 2023 C&LM Plan Update determination (2023-06-23 request for comment → later pause); existing customers may stay or move to ESS (DEEP 2025–2027 draft determination, read). …

## New York

### Con Edison — SC 1 Rate II, Residential and Religious Voluntary Time-of-Day (P.S.C. No. 10, leaf 389)

- **Category:** TOU-whole-home (seasonal peak/off-peak differentiation; legacy, closed to new customers)
- **Status (Oct 2026):** Closed to new customers (applications not accepted on or after March 1, 2014); existing customers remain.
- **Design:** Opt-in legacy TOD, **closed to new applicants since Mar 1, 2014**. Weekday 10 AM-10 PM on-peak; Jan 2024 tariff: summer (Jun-Sep) on-peak delivery 60.91 c/kWh vs off-peak 2.33 c/kWh (about 26:1); other months 22.09 vs 2.33 c/kWh (about 9.5:1). …
- **Defining docket:** Case 13-E-0030, NY PSC, Order Approving Electric, Gas and Steam Rate Plans in Accord with Joint Proposal, Feb 21, 2014 (replaced Rate II with Rate III for new elections from Mar 1, 2014; inferred from the leaf's Mar 1, 2014 date and the Rate III evidence below). The original creation of Rate II (pre-2014) is NOT FOUND. _[unverified]_
- **Current governing docket:** Case 25-E-0072 (order Jan 22, 2026) governs rates; the Jan 2024 leaf is stamped "Case 22-E-0064 dated 07/20/2023".
- **Where we learned it:** Primary — <https://www.coned.com/-/media/files/coned/documents/rates/electric/historical/psc-10/tariff/sc-202401.pdf>
- **In NEEP:** Yes, Appendix A row "NY / ConEd / Seasonal TOU" (does not distinguish Rate II vs Rate III).
- **Notes:** NEEP lumps Rate II and III as "Seasonal TOU".

### Con Edison — SC 1 Rate III, Residential and Religious Voluntary Time-of-Day (seasonal TOU) (P.S.C. No. 10, leaf 389.1)

- **Category:** TOU-whole-home (seasonal peak/off-peak differentiation; also ConEd's whole-home EV TOU)
- **Status (Oct 2026):** Active. Peak-period/seasonal-design study due **Nov 30, 2026** under the 2026 rate plan; changes to be filed by May 31, 2027. …
- **Design:** Opt-in, available to all SC 1 customers who elect it after Mar 1, 2014. On-peak every day 8 AM-midnight (incl. holidays), off-peak midnight-8 AM. Jan 2024 delivery: summer (Jun-Sep) on-peak 33.05 c/kWh vs off-peak 2.33 c/kWh (about 14:1); …
- **Defining docket:** **Case 13-E-0030**, NY PSC, Order Approving Electric, Gas and Steam Rate Plans in Accord with Joint Proposal, **Feb 21, 2014**. Basis: ConEd's Aug 21, 2014 Time-Sensitive Rate Pilot Plan (filed in compliance with Ordering Clause 10 of that order) says the pilot rate was modeled on "the SC 1 Rate III rate design approved in the Order". … _[found]_
- **Current governing docket:** **Case 25-E-0072** (and 25-G-0073), Order Adopting Terms of a Joint Proposal, Jan 22, 2026, JP filed Nov 5, 2025 (Rate III/IV continuation, study, price guarantee). …
- **Where we learned it:** Primary — <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=13-E-0030>; <https://www.coned.com/-/media/files/coned/documents/rates/electric/historical/psc-10/tariff/sc-202401.pdf>; <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=25-E-0072>
- **In NEEP:** Yes, Appendix A "NY / ConEd / Seasonal TOU" and "Seasonal EV TOU" (NEEP treats the EV TOU as Rate III with the EV provisions).
- **Notes:** There is no separate "EV TOU rate" tariff for ConEd. The EV option is Rate III plus Special Provisions E/F (I did not locate which order added Special Provisions E/F; UNVERIFIED). SmartCharge NY participants must be on a standard (non-TOU) rate.

### Con Edison — SC 1 Rate IV, Optional Demand-Based (Steady Use Rate) — cross-reference only

- **Category:** demand-charge
- **Status (Oct 2026):** Active; opened to all SC 1 customers.
- **Design:** See `reports2/context/domain/electric_heating_and_heat_pump_rates.md` (NY-1). Jan 2024 leaf 389.2: $29/month customer charge; summer on-peak (weekdays noon-8 PM) $23.55/kW, off-peak $6.95/kW; other months on-peak $18.12/kW.
- **Defining docket:** Case 19-E-0065, NY PSC, Jan 16, 2020 (Select Pricing Plan). Opened to all: Case 22-E-0064, Jul 20, 2023. _[found]_
- **Current governing docket:** Case 25-E-0072, Jan 22, 2026.
- **Where we learned it:** Primary
- **In NEEP:** Yes, Appendix A "NY / ConEd / Other: Select Pricing Plan (Demand Charge)"; Table 5 shows 776 customers (2025).
- **Notes:** not redone per instructions.

### Con Edison — SC 1 Rate VI (proposed, filed Jul 1, 2026) and Rider Z Innovative Pricing Pilot (P.S.C. No. 10)

- **Category:** demand-charge (Rate VI per its July 2026 filing; Rider Z pilot rate structures)
- **Status (Oct 2026):** Rate VI tariff leaves filed July 1, 2026 (proposed effective date in the cover letter; acceptance/suspension NOT checked). …
- **Design:** Rider Z = SC 1 Innovative Pricing Pilot (smart-meter customers; multiple pilot rate structures; I did not verify enrollment counts or the opt-out design). Rate VI, per ConEd's Jul 1, 2026 filing: elective; $21/month customer charge; …
- **Defining docket:** **Case 18-E-0397**, NY PSC, Order Approving Tariff Amendments with Modifications, **Dec 13, 2018** (Riders Z and AA; pilot began Apr 1, 2019, ended ~Q1 2022 plus later waves). Rate VI docket: NOT FOUND (I read the cover letter text only, no case number extracted). _[found]_
- **Current governing docket:** Case 25-E-0072 for base rates; Rate VI conversion docket UNVERIFIED.
- **Where we learned it:** Primary — <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=18-E-0397>
- **In NEEP:** Not in NEEP (NEEP lists only Rate IV as ConEd's demand charge option).
- **Notes:** 18-E-0397 is the docket to pull for pilot rate designs and reports (not opened).

### Con Edison — Rider AB, Smart Home Rate Demonstration Project (SC 1)

- **Category:** demand-charge (demonstration pilot)
- **Status (Oct 2026):** UNVERIFIED (pilot likely ended; not confirmed).
- **Design:** Opt-in demonstration with a daily demand charge on peak-window demand plus critical-peak event charges (parameters not verified; see leaves 327.12-327.14 in the ConEd tariff).
- **Defining docket:** NOT FOUND. Leaves are stamped "Order in Case 18-E-0130 dated 09/17/2020" (and 18-E-0130 et al. dated 04/16/2026), but 18-E-0130 is, to my knowledge, the energy storage proceeding; I did not read it, so I do not assert it created Rider AB. _[not found]_
- **Current governing docket:** UNVERIFIED.
- **Where we learned it:** Primary
- **In NEEP:** Not in NEEP.
- **Notes:** Included because it is the only critical-peak-event-charge element in NY residential tariffs I found.

### Con Edison — Smart Usage Rewards (residential event-based demand response)

- **Category:** other (event-based demand response; closest NEEP analogue is rebate-PTR)
- **Status (Oct 2026):** Active per NEEP/ConEd; not independently verified.
- **Design:** Residential customers with a smart meter enroll via ConEd's program partners for event-based rewards. Details not verified (web page not opened).
- **Defining docket:** **Case 14-E-0423** (Proceeding on Motion of the Commission to Develop Dynamic Load Management Programs); relevant orders read: Mar 14, 2019 (tariff filings 15-E-0186 et al. for each utility's DLM tariffs) and Mar 14, 2024. Which of these set ConEd's residential partner model is not confirmed. Case 09-E-0115 appeared only in a search snippet (UNVERIFIED). _[found]_
- **Current governing docket:** Case 14-E-0423 (annual reports each Nov 15; orders in 2024).
- **Where we learned it:** Primary, partly search summary — <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=14-E-0423>; <https://www.coned.com/en/save-money/rebates-incentives-tax-credits/rebates-incentives-tax-credits-for-residential-customers/smart-usage-rewards>
- **In NEEP:** NEEP lists ConEd "PTR" (Appendix A) and links this page.
- **Notes:** "Peak Time Rebate" is NEEP's label; I did not find a tariffed NY residential PTR.

### Central Hudson — SC 6, Residential Time-of-Use (12-hour and 5-hour peak options)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active. Rates per 24-E-0461 rate year 1 (July 1, 2025).
- **Design:** Opt-in; two options in the 2025 order's rate tables: "12 Hour on-peak" and "5 Hour on-peak" (peak-hour definitions not verified). Both customer charge $25.50 in rate year 1; delivery+supply rates differ by period (12-hour: on-peak $0.17851, off-peak $0.05950/kWh; …
- **Defining docket:** NOT FOUND. SC 6 predates the cases I could read, and I did not locate an SC 6 leaf stamp. PSL §66-o required eligible EV owners on SC 6 TOU as of Dec 1, 2017 to be able to register for a bill guarantee (per Central Hudson's Nov 8, 2018 letter in 18-E-0206). _[not found]_
- **Current governing docket:** **Case 24-E-0461** (electric) / 24-G-0462, NY PSC Order Adopting Terms of a Joint Proposal, Aug 14, 2025 (plan covers rate years starting Jul 1, 2025; exact JP filing date and plan end not verified). …
- **Where we learned it:** Primary, partly search summary — <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=24-E-0461>; <https://www.cenhud.com/en/my-energy/electric-vehicles/residential-charging-incentives/>
- **In NEEP:** Yes, Appendix A "NY / Central Hudson / TOU".
- **Notes:** The order calls it "SC 6 Residential TOU" (an "S.C. No. 6 Alt TOU" label also appears in the order's rate appendix); electric SC 6 in this order is the TOU class (gas SC 6 is separate).

### National Grid (Niagara Mohawk) — SC-1 Residential Optional Time-of-Use (SC1VTOU; Special Provision L to SC-1, P.S.C. No. 220, leaf 355)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active.
- **Design:** Opt-in; requires TOU meter ($3.36/month). Delivery: on-peak 7 AM-11 PM, off-peak 11 PM-7 AM. Commodity adds a summer super-peak 2-6 PM weekdays Jun-Aug (capacity charges concentrated into four hours). …
- **Defining docket:** Special Provision L was already available to all residential customers as of **Dec 1, 2016** (per the Nov 15, 2019 order in 18-E-0206); the case that created it is NOT FOUND. Leaves in the 2018 petition are stamped **Case 17-E-0238**, order issued **Mar 15, 2018**. EV one-year bill guarantee driver: PSL §66-o via **Case 18-E-0206** (Order of Nov 15, 2018; … _[found]_
- **Current governing docket:** **Case 24-E-0322** (electric) / 24-G-0323, Order Adopting Terms of Joint Proposal (session Aug 14, 2025, per summary of the order; I read only its front matter and did not confirm that the VTOU leaf was restated in it).
- **Where we learned it:** Primary — <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=17-E-0238>; <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=24-E-0322>
- **In NEEP:** Yes, Appendix A "NY / National Grid / TOU".
- **Notes:** The 2018 leaf has a one-time option for PEV owners: after a one-year term, a comparison of 12 months under Special Provision L vs standard SC-1, with a refund if SC-1 would have been cheaper (excluding the $3.36 incremental customer charge). Current (2025-26) leaf values not checked.

### NYSEG — SC 12, Residential Service with Time-of-Use Metering (P.S.C. No. 120, leaf 295)

- **Category:** TOU-whole-home (supply-only time differentiation; delivery flat)
- **Status (Oct 2026):** Active (leaf rev. 19, effective Jun 1, 2026).
- **Design:** Opt-in, customers using at least 35,000 kWh in 12 months (NEEP: "high energy users"). Seasonal three-period supply price: winter on-peak weekdays 7-10 AM and 5-10 PM; summer on-peak weekdays 10 AM-6 PM; off-peak 11:30 PM-7 AM; mid-peak otherwise; …
- **Defining docket:** **Case 07-E-0479**, NY PSC, order dated **Aug 29, 2007** (leaf 295 stamp: "Issued in compliance with order in Case No. 07-E-0479 dated 08/29/07"; effective Jan 1, 2008). _[found]_
- **Current governing docket:** **Case 25-E-0375** (leaf rev. 19 effective Jun 1, 2026, "Order in Case No. 25-E-0375, dated May 14, 2026", the temporary-rates order). Previous full rate plan: Case 22-E-0317, order Oct 12, 2023 (plan May 1, 2023-Apr 30, 2026).
- **Where we learned it:** Primary — <https://www.nyseg.com/documents/d/nyseg/psc120_serviceclassification-12>; <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=22-E-0317>
- **In NEEP:** Yes, Appendix A "NY / NYSEG / Seasonal TOU for high energy users (35000 kWh annually)".
- **Notes:** NEEP labels the NYSEG and RG&E TOU entries inconsistently (NYSEG: both rates; RG&E: only 1000 kWh). Verified below.

### NYSEG — SC 8, Residential Day-Night Service (P.S.C. No. 120, leaf 256)

- **Category:** TOU-whole-home (two-period, supply-only differentiation)
- **Status (Oct 2026):** Active (legacy).
- **Design:** Opt-in "Day-Night" metering for customers who opted in before May 27, 1988, new installations using 1,000 kWh or more per month, or existing SC 1 customers using 1,000 kWh or more per month. Night 11:30 PM-7 AM EST. …
- **Defining docket:** NOT FOUND. Leaf 256 rev. 5 effective Jan 1, 2010; case stamp not displayed in text I read; "opted prior to May 27, 1988" suggests a 1980s case (UNVERIFIED). _[not found]_
- **Current governing docket:** **Case 25-E-0375** (leaf stamp May 14, 2026 order); prior plan Case 22-E-0317.
- **Where we learned it:** Primary
- **In NEEP:** Yes, Appendix A "NY / NYSEG / TOU for above-average energy users (1000 kWh monthly)".
- **Notes:** NEEP's "above-average users 1000 kWh monthly" corresponds to SC 8 Day-Night, not SC 12.

### RG&E — SC 4, Residential Service Time-of-Use Rate (P.S.C. No. 19, leaf 174)

- **Category:** TOU-whole-home (supply-only differentiation)
- **Status (Oct 2026):** Active.
- **Design:** Voluntary for any customer who would otherwise be on SC 1. Schedule I (up to 24,750 kWh/yr) and Schedule II (above 24,750 kWh/yr). Peak 7 AM-9 PM Monday-Friday, off-peak all other hours. **Delivery charge identical in peak and off-peak** ($0.07115/kWh Sch. I, $0.08551 Sch. …
- **Defining docket:** Leaf 174.1.1 stamp: "Issued in Compliance with Order in Case 09-E-0228 issued and effective September 28, 2009" (RG&E rate order; effective Jan 1, 2010). Original creation date of SC 4 not determined (UNVERIFIED). _[found]_
- **Current governing docket:** **Case 25-E-0379** (leaves stamped May 14, 2026 temporary-rates order). Previous plan: Case 22-E-0319, order Oct 12, 2023 (not read; case number from assignment brief, UNVERIFIED).
- **Where we learned it:** Primary — <https://www.rge.com/documents/d/rge/psc19_serviceclassifications>
- **In NEEP:** Yes, Appendix A "NY / RG&E / Seasonal TOU for above-average energy users (1000 kWh monthly)" (NEEP's description does not match SC 4, which has no …
- **Notes:** RG&E has no seasonal TOU in this leaf.

### O&R — SC 19, Residential Optional Time-of-Use Service (P.S.C. No. 3, leaf 341)

- **Category:** TOU-whole-home (seasonal periods; delivery-based time differentiation; includes EV provisions)
- **Status (Oct 2026):** Active.
- **Design:** Optional residential TOU. Summer Jun-Sep weekdays: Period I peak noon-7 PM 44.651 c/kWh; Period II shoulder 10 AM-noon and 7-9 PM 15.976 c/kWh; Oct-May weekdays Period III 10 AM-9 PM 15.976 c/kWh; …
- **Defining docket:** Base SC 19 TOU: NOT FOUND (predates what I could trace). EV provisions (price guarantee, EV-only account, SC 1 customer charge for EV registrants): leaves 344/344.1 are stamped "Order in Case 18-E-0067 dated 3/14/2019" (O&R's 2018 rate case, effective Apr 1, 2019); … _[not found]_
- **Current governing docket:** **Case 24-E-0060** (electric), order dated **Mar 20, 2025** (SC 19 rate leaves effective Jan 1, 2026 stamped "Order in Case 24-E-0060 dated 3/20/2025"; gas companion case number not verified).
- **Where we learned it:** Primary — <https://cdne-dcxprod-sitecore.azureedge.net/-/media/files/oru/documents/rates/new-york/electric/ny-electric-tariff.pdf>
- **In NEEP:** Yes, Appendix A "NY / O&R / Seasonal TOU; Seasonal EV TOU" (both refer to SC 19).
- **Notes:** O&R's web page still showed $22.50 customer charge in the snippet; the current tariff leaf says $29.00 (SC 19) and SC 1 charge for EV registrants. Not reconciled.

### PSEG Long Island (LIPA) — Rate 194, Residential Time-of-Day (standard/default, opt-out) and Rate 195 Super Off-Peak (optional), Service Classification No. 1

- **Category:** TOU-whole-home (opt-out default)
- **Status (Oct 2026):** Active; migration through 2025.
- **Design:** Rate 194: peak weekdays 3-7 PM (excluding holidays), all other hours off-peak; **2:1 peak-to-off-peak ratio on both delivery and power supply**. Rate 195: same peak plus super off-peak 10 PM-6 AM daily; different delivery/supply ratios by season. …
- **Defining docket:** **Not a PSC case.** LIPA is not generally subject to PSC rate jurisdiction. Regulatory process: LIPA Board of Trustees vote **Mar 29, 2023** after DPS staff recommendations under the LIPA Reform Act, **DPS Matter 23-00071**, letter of Mar 28, 2023 ("Recommendations Regarding LIPA's Proposed Modifications to its Tariff for Electric Service"), recommending adoption with conditions. … _[found]_
- **Current governing docket:** LIPA Tariff for Electric Service (Board-approved). DPS Matter 23-00071 for the recommendation; later LIPA rate reviews (2025+) not examined.
- **Where we learned it:** Primary — <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=23-00071>
- **In NEEP:** Yes, Appendix A "NY / PSE&G Long Island / TOU (Opt-Out); TOU - with super off-peak" (and NEEP's heading "PSE&G" is a misnomer for PSEG Long Island; …
- **Notes:** DPS letter describes Rate 180 as flat with an increase in summer above 250 kWh. NEEP's "Technology-Specific: seasonal electric heating inclining/declining" is Rate 580 per local file `electric_heating_and_heat_pump_rates.md` (NY-3).

### PSEG Long Island (LIPA) — Rate 180 flat residential rate (seasonal step above 250 kWh) and Rate 580 residential electric heating (Service Classification No. 1)

- **Category:** TOU-seasonal-only (Rate 180: seasonal inclining step); other (Rate 580: electric-heating discount)
- **Status (Oct 2026):** Active (Rate 180 is the opt-out alternative to the default TOD Rate 194); Rate 580 per local doc.
- **Design:** Rate 180 is the flat residential rate; per the DPS Mar 28, 2023 letter it has a rate increase for usage over 250 kWh (NEEP: "seasonal inclining block rate (summer only)"). …
- **Defining docket:** Not a PSC case (LIPA tariff). Rate 180: referenced in DPS Matter 23-00071; creation NOT FOUND. Rate 580: NOT FOUND (local doc says "did not confirm the case number"). _[found]_
- **Current governing docket:** LIPA Tariff for Electric Service (Board-approved); NOT FOUND for the latest rate review.
- **Where we learned it:** Primary — <https://documents.dps.ny.gov/public/MatterManagement/CaseMaster.aspx?MatterCaseNo=23-00071>
- **In NEEP:** Yes, Appendix A (seasonal inclining block rate; seasonal electric heating inclining/declining block rate).
- **Notes:** NEEP describes Rate 580 as "inclining block rate in summer, declining in winter"; local doc describes a 40% winter delivery discount above 400 kWh/month. Not reconciled.

### Central Hudson, National Grid, NYSEG, RG&E, O&R — Residential Direct Load Control / Bring-Your-Own-Thermostat programs (Peak Perks; ConnectedSolutions; Smart Savings Rewards; Smart Savers)

- **Category:** other (event-based thermostat/battery demand response; NEEP labels these "PTR" or "Battery DR"; no bill-credit PTR tariff found)
- **Status (Oct 2026):** Active.
- **Design:** The Dynamic Load Management (DLM) programs include a **Direct Load Control (DLC) Program** targeting residential and small business customers, with a Bring Your Own Thermostat (BYOT) component whose upfront/seasonal incentive rates are set in each utility's DLM tariff (O&R …
- **Defining docket:** **Case 14-E-0423**, Proceeding on Motion of the Commission to Develop Dynamic Load Management Programs (originating order not retrieved: NOT FOUND); utility DLM tariff filings: **15-E-0186** (Central Hudson), **15-E-0188** (NYSEG), **15-E-0189** (National Grid), **15-E-0190** (RG&E), **15-E-0191** (O&R); ConEd's tariff case number NOT FOUND (15-E-0187 is a guess, UNVERIFIED). … _[found]_
- **Current governing docket:** Case 14-E-0423 (annual DR reports due Nov 15; Staff stakeholder session each Dec-Jan).
- **Where we learned it:** Primary, partly search summary
- **In NEEP:** Yes as "PTR" (Central Hudson, ConEd, National Grid, NYSEG, O&R, PSEG LI, RG&E) and "Battery DR" (National Grid); …
- **Notes:** The mapping of each brand to the DLC/BYOT tariff is my inference from the order text plus NEEP's URL titles; the brand names themselves are not in the orders I read.

### PSEG Long Island — Commercial System Relief Program (CSRP) and Distribution Load Relief — NOT residential

- **Category:** other
- **Status (Oct 2026):** UNVERIFIED.
- **Design:** NEEP Appendix E lists PSEG LI "System Relief Program" (CSRP) under peak-load programs; I did not verify any residential PTR.
- **Defining docket:** NOT FOUND (LIPA is outside the 14-E-0423 PSC framework). _[not found]_
- **Current governing docket:** NOT FOUND.
- **Where we learned it:** NEEP listing only; no independent source found
- **In NEEP:** Yes ("PTR" for PSEG LI in Appendix A).
- **Notes:** Listed in Unresolved.

## New Jersey

### Atlantic City Electric (ACE) — Residential Service (RS) with seasonal inclining block, Rate Schedule RS (BPU NJ No. 11, Section IV)

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** Active.
- **Design:** Default residential delivery rate. Summer (Jun–Sep) two blocks split at 750 kWh; winter (Oct–May) single flat rate. Rates approved in ER23020091 (with SUT, as in the order's rate-design exhibit): summer first 750 kWh $0.080587, over 750 kWh $0.094612; winter $0.073341 per kWh. …
- **Defining docket:** NOT FOUND (block structure is long-standing; the original ACE order that created the inclining block was not located). Last re-set in ER23020091, BPU, order Nov 17, 2023 (ACE 2023 base rate case, OAL PUC 02235-2023 S). _[not found]_
- **Current governing docket:** ER23020091 for base rates; quarterly/annual rider changes in other dockets (e.g. ER25070444 for Rider RGGI/TOU, order Sept 23, 2026).
- **Where we learned it:** Primary — <https://www.nj.gov/bpu/pdf/boardorders/2023/20231117/2A%20ORDER%20ACE%20Base%20Rate%20Case.pdf>; <https://nj.gov/bpu/pdf/boardorders/2026/20260923/2B%20ORDER%20ACE%2025%20Rider%20RGGI.pdf>
- **In NEEP:** Not in NEEP: Appendix A shows ACE Seasonal Only Rates = "None" (NEEP lists only an EV seasonal multifamily inclining block under technology-specific).
- **Notes:** Per the ER23020091 exhibit, ACE's default RS has a summer-only inclining block (and winter flat), which NEEP does not record. ACE RS tariff sheets are re-filed under many riders dockets, so the footer docket is rarely the defining one.

### Atlantic City Electric (ACE) — Residential TOU option (RS "Residential TOU Option", distribution) and BGS-TOU supply option

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active. Authorized Oct 30, 2024 as the "Time of Use Rate" demand-response program in Triennium 2; rate levels modified by the Sept 23, 2026 order (the order text says the TOU program is modified, not …
- **Design:** Opt-in. Distribution on-peak 4–9 pm weekdays (excl. holidays) all year; season-specific on-peak/off-peak distribution rates. As stipulated in ER25070444 (Sept 2026): summer peak $0.244459 / off-peak $0.065170 per kWh; …
- **Defining docket:** QO23120871, BPU (Triennium 2 energy efficiency / demand response stipulation, "Order Adopting Stipulation" Oct 30, 2024) — authorized the RS-TOU pilot (Triennium 2 budget line "Time of Use Rate" $3,600,000). _[found]_
- **Current governing docket:** ER25070444 (BPU order approving stipulation modifying TOU rates; order Sept 23, 2026).
- **Where we learned it:** Primary — <https://nj.gov/bpu/pdf/boardorders/2024/20241030/8D%20ORDER%20Atlantic%20City%20Electric%20Company%20Triennium%202.pdf>; <https://nj.gov/bpu/pdf/boardorders/2026/20260923/2B%20ORDER%20ACE%2025%20Rider%20RGGI.pdf>
- **In NEEP:** Not in NEEP (NEEP shows ACE "Daily Time Varying Rates: None").
- **Notes:** NEEP misses ACE's whole-home TOU entirely.

### Atlantic City Electric (ACE) — Direct Load Control demand response (consumer brand not verified; NEEP's "PTR – Summer" / "PTR – Winter pilot")

- **Category:** other (direct load control; NEEP files it under rebate-PTR)
- **Status (Oct 2026):** Authorized for Jan 2025–June 2027 (Triennium 2).
- **Design:** Utility-controlled thermostat/device load control with participation incentives. I could not retrieve a primary description of the incentive design or events. …
- **Defining docket:** QO23120871, BPU, Order Adopting Stipulation, Oct 30, 2024 (PRIMARY, read). Statewide framework: QO23030150 (order Jan 10, 2024 establishing T2 framework, per the order's citations). _[found]_
- **Current governing docket:** QO23120871.
- **Where we learned it:** Primary — <https://nj.gov/bpu/pdf/boardorders/2024/20241030/8D%20ORDER%20Atlantic%20City%20Electric%20Company%20Triennium%202.pdf>
- **In NEEP:** Appendix A NJ/ACE Rebates column: "EV OPR; PTR - Summer; PTR - Winter pilot".
- **Notes:** UNVERIFIED that these DLC programs equal NEEP's "PTR" rows; I found no ACE tariff or order using "peak time rebate". The customer-facing ACE program names and incentive amounts were not verified and are deliberately omitted.

### Public Service Electric & Gas (PSE&G) — FlexPower / SmartFlex demand response (NEEP's "PTR")

- **Category:** other (device-based demand response; NEEP lists as PTR)
- **Status (Oct 2026):** Active.
- **Design:** Opt-in. FlexPower (Direct Load Control pathway, launched June 2025): up-front incentive $50 per enrolled device category plus end-of-season participation incentive ($25 residential / $50 C&I per category, paid after Oct 31). …
- **Defining docket:** UNVERIFIED for the demand response program approval. The PSE&G PY4 report is captioned under EE framework dockets QO19010040, QO19060748 and QO17091004 together with PSE&G's CEF-EE petition. PSE&G Triennium 2 docket not confirmed (the Jan 10, 2024 T2 framework order lists QO23120868–QO23120875 for the utilities but I did not map which is PSE&G). _[unverified]_
- **Current governing docket:** UNVERIFIED (see above).
- **Where we learned it:** Primary — <https://flexpower.pseg.com/pages/home/landing>
- **In NEEP:** Appendix A NJ/PSE&G Rebates: "EV OPR; PTR".
- **Notes:** Not a classic peak time rebate. No PSE&G PTR tariff found.

### Jersey Central Power & Light (JCP&L) — Service Classification RT, Residential Time-of-Day Service

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Active.
- **Design:** Opt-in (optional alternative to RS). Delivery on-peak 8 am–8 pm Eastern Standard Time Mon–Fri; off-peak all other hours incl. weekends. Distribution (sheets effective May 1, 2025): on-peak $0.060029/kWh Jun–Sep and $0.044094 Oct–May; off-peak $0.028041; …
- **Defining docket:** NOT FOUND. RT predates restructuring; tariff footers only cite the latest rate case. Last set in ER23030144 / OAL PUC 3346-23 (BPU Decision and Order Adopting Initial Decision and Stipulation, Feb 14, 2024). _[not found]_
- **Current governing docket:** ER23030144 (base rates); the Feb 15, 2026 sheets also cite ER24120005 and ER25100556 in their footers (what those dockets decided was not verified).
- **Where we learned it:** Primary — <https://www.firstenergycorp.com/content/dam/customer/Customer%20Choice/Files/New%20Jersey/tariffs/BPU-14-Part-III-Eff-3-1-2026.pdf>; <https://www.nj.gov/bpu/pdf/boardorders/2024/20240214/2B%20ORDER%20JCP%26L%20Base%20Rate%20Case.pdf>
- **In NEEP:** Appendix A NJ/JCP&L "Daily Time Varying: Seasonal TOU".
- **Notes:** NEEP labels it "Seasonal TOU"; RT is whole-year TOU with a seasonally differentiated on-peak distribution rate (summer higher). It shares the 8 am–8 pm window with RGT.

### Jersey Central Power & Light (JCP&L) — Service Classification RS Residential Service (seasonal inclining block)

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** Active.
- **Design:** Default residential delivery rate. Summer (Jun–Sep): $0.020182/kWh first 600 kWh, $0.079810 over 600 kWh (4x tail ratio); winter (Oct–May): flat $0.033061/kWh. Opt-out (default).
- **Defining docket:** NOT FOUND (long-standing design). Most recent re-design inside ER23030144 (order Feb 14, 2024). Current tariff sheet footers also cite ER24120005 and ER25100556 (not verified what they decided). _[not found]_
- **Current governing docket:** ER23030144 (base rates).
- **Where we learned it:** Primary — <https://www.firstenergycorp.com/content/dam/customer/Customer%20Choice/Files/New%20Jersey/tariffs/BPU-14-Part-III-Eff-3-1-2026.pdf>
- **In NEEP:** Appendix A NJ/JCP&L "Seasonal Only: Seasonal inclining block rate".
- **Notes:** Confirms NEEP. Water-heating special provisions under RS (off-peak and controlled water heating) are NEEP's "Off-peak water heating; Controlled water heating".

### Jersey Central Power & Light (JCP&L) — Service Classification RGT, Residential Geothermal & Heat Pump Service

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** Active.
- **Design:** Cross-reference only; see `context/domain/electric_heating_and_heat_pump_rates.md` entry NJ-1. Summer (Jun–Sep) on-peak $0.060029 / off-peak $0.028041 distribution (8 am–8 pm weekdays); winter (Oct–May) flat $0.033061.
- **Defining docket:** NOT FOUND online; pre-1999. Earliest tariff text is the 1999 JCP&L tariff (BPU No. 9) issued under EO97070458/59/60, which did not create RGT. Footer cites ER25010024 (order Apr 23, 2025). _[not found]_
- **Current governing docket:** ER23030144 (2023 base rate case; order Feb 14, 2024) and ER26080420 (2026 base rate case, filed Aug 6, 2026, proposes RGT winter = RS winter). ER26030090 and ER25010024 are compliance dockets.
- **Where we learned it:** Primary — <https://www.firstenergycorp.com/content/dam/customer/Customer%20Choice/Files/New%20Jersey/tariffs/BPU-14-Part-III-Eff-3-1-2026.pdf>
- **In NEEP:** Appendix A NJ/JCP&L "Seasonal heat pump and geothermal systems TOU".
- **Notes:** Already documented locally; I did not search further.

### Public Service Electric & Gas (PSE&G) — Rate Schedule RS-TOU (two-period "2P" and three-period "3P" residential time-of-use)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** Authorized Oct 9, 2024 as a three-period "TOU Pilot" (stipulation para. 29: PSE&G may implement a three-period TOU option and defer up to $12.4M); …
- **Design:** Opt-in. 2P: on-peak 4–9 pm weekdays excluding PJM holidays, off-peak all other hours. 3P: on-peak 4–9 pm weekdays (excl. PJM holidays), off-peak 12–6 am, mid-peak all other times. …
- **Defining docket:** ER23120924 and GR23120925 (OAL PUC 00926-24), BPU, Order Adopting Stipulation, Oct 9, 2024 (stipulation paragraphs 29–31; $12.4M deferral for TOU implementation). _[found]_
- **Current governing docket:** ER23120924/GR23120925 for distribution; ER25040190 (BGS period beginning June 1, 2026) for the supply side of RS-TOU 3P (compliance filing Dec 5, 2025).
- **Where we learned it:** Primary — <https://www.nj.gov/bpu/pdf/boardorders/2024/20241009/2A%20ORDER%20PS%2023%20BRC.pdf>; <https://publicaccess.bpu.state.nj.us/DocumentHandler.ashx?document_id=1406072>
- **In NEEP:** Appendix A NJ/PSE&G "Daily Time Varying: Seasonal TOU". NEEP Table text says PSE&G ratio 1.0–5.7.
- **Notes:** NEEP refers to the existing RLM seasonal TOU (winter peak/off-peak rates equal, so winter ratio 1.0, summer 5.7). RS-TOU 2P/3P are the new rates; NEEP's Dec 2025 snapshot likely pre-dates them. I did not confirm exact go-live date for 2P/3P customers.

### Public Service Electric & Gas (PSE&G) — Rate Schedule RLM, Residential Load Management (legacy seasonal TOU)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** To be closed to new customers once RS-TOU is made available (stipulation para. 30).
- **Design:** Opt-in whole-house TOU (on-peak/off-peak distribution; summer peak rate high, winter peak equals off-peak per NEEP). Also the basis for the EV "RLM distribution only" credit under RS.
- **Defining docket:** NOT FOUND (pre-restructuring/legacy rate). Current structure from ER23120924 (order Oct 9, 2024). _[not found]_
- **Current governing docket:** ER23120924 / GR23120925.
- **Where we learned it:** Primary — <https://www.nj.gov/bpu/pdf/boardorders/2024/20241009/2A%20ORDER%20PS%2023%20BRC.pdf>
- **In NEEP:** Appendix A NJ/PSE&G "Seasonal TOU" (and Table 2 mention of 5.7 summer ratio).

### Public Service Electric & Gas (PSE&G) — Rate Schedule RS summer inclining block and RHS (closed) seasonal electric heating

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** RS active; RHS closed.
- **Design:** RS: summer two-block distribution rate (inclining block differential $0.0049/kWh retained in 2024 case), winter flat. RHS (Residential Heating Service): inclining summer / declining winter; closed to new customers. Cross-reference domain file entry NJ-2 for RHS.
- **Defining docket:** NOT FOUND for original design; re-set in ER23120924 (Oct 9, 2024). _[not found]_
- **Current governing docket:** ER23120924 / GR23120925.
- **Where we learned it:** Primary — <https://www.nj.gov/bpu/pdf/boardorders/2024/20241009/2A%20ORDER%20PS%2023%20BRC.pdf>
- **In NEEP:** Appendix A NJ/PSE&G "Seasonal inclining block rate (summer only)" and "Seasonal electric heating ... (no new customers)".
- **Notes:** Confirms NEEP.

### Rockland Electric Company (RECO) — SC 1 Residential Service (summer inclining block) and SC 1 Voluntary Time-of-Day

- **Category:** TOU-whole-home (SC 1 TOD) and TOU-seasonal-only (SC 1 inclining block)
- **Status (Oct 2026):** Active.
- **Design:** SC 1 default: summer first 600 kWh / over 600 kWh inclining block (tariff dated June 30, 2026: first 600 kWh 6.886 ¢, over 600 kWh 8.671 ¢ per kWh in the first column; 6.886 ¢ in the other column, which I read as non-summer months), other months flat. …
- **Defining docket:** NOT FOUND for SC 1 TOD (leaf footers cite ER09080668, May 12, 2010, for the older schedule leaves). EV price guarantee on the TOD rate came from EO20110730 (order Oct 12, 2022). _[not found]_
- **Current governing docket:** ER25060374 / OAL PUC 13561-2025 N (BPU order June 30, 2026).
- **Where we learned it:** Primary — <https://www.oru.com/-/media/files/oru/documents/rates/new-jersey/schedule-for-electric-service.pdf>; <https://nj.gov/bpu/pdf/boardorders/2026/20260630/2D%20ORDER%20RECO%20Base%20Rate%20Case.pdf>
- **In NEEP:** Appendix A NJ/RECO "Seasonal inclining block rate (summer only)", "Seasonal TOU", "EV TOU".
- **Notes:** RECO TOD and EV TOD are the same voluntary schedule; EV customers who register an EV get a first-year price guarantee.

### Rockland Electric Company (RECO) — SC 3 Residential Time-of-Day Heating Service

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** Active.
- **Design:** Cross-reference only (domain file entry NJ-3). Pilot change in June 30, 2026 order (stipulation para. 11): SC-3 summer peak/off-peak periods and ratios aligned with SC-1 Voluntary TOD; winter becomes a single flat volumetric rate; revenue neutral.
- **Defining docket:** NOT FOUND. Leaf 95 footer cited ER09080668 (May 12, 2010). _[not found]_
- **Current governing docket:** ER25060374 (order June 30, 2026).
- **Where we learned it:** Primary — <https://nj.gov/bpu/pdf/boardorders/2026/20260630/2D%20ORDER%20RECO%20Base%20Rate%20Case.pdf>
- **In NEEP:** Appendix A NJ/RECO "Seasonal electric water and space heating TOU".
- **Notes:** NEEP says RECO SC-3 is a seasonal TOU; the 2026 order removes winter TOD, making it a summer-only TOU for heating customers.

### New Jersey (all EDCs) — BGS TOU supply option for residential customers

- **Category:** TOU-whole-home (supply)
- **Status (Oct 2026):** Active.
- **Design:** Supply-side TOU is created in the annual BGS proceeding and implemented in each EDC tariff (ACE's EV BGS off-peak credit uses on-peak 8 am–8 pm Mon–Fri; PSE&G RS-TOU 3P has BGS on-peak/mid-peak/off-peak supply charges in the Dec 5, 2025 compliance tariff; …
- **Defining docket:** ER22030127 (BGS for period beginning June 1, 2023), BPU order Nov 9, 2022 (ordered EV BGS TOU solution); company-specific tariff dockets ER23040209 (ACE, order May 24, 2023) and ER23030131 (PSE&G, order May 24, 2023). Earlier: ER21030631 (BGS 2022, order Nov 17, 2021) first raised the EV TOU issue. _[found]_
- **Current governing docket:** ER25040190 (BGS for period beginning June 1, 2026; order Feb 12, 2026 per RECO tariff footer).
- **Where we learned it:** Primary — <https://nj.gov/bpu/pdf/boardorders/2023/20230524/2D%20ORDER%20ACE%20BGS%20EV%20TOU%20Tariff.pdf>; <https://www.nj.gov/bpu/pdf/boardorders/2023/20230524/2F%20ORDER%20PSE&G%20BGS%20EV%20TOU%20Tariff.pdf>
- **In NEEP:** Not in NEEP.
- **Notes:** I did not read the ER22030127 order itself; its content is as quoted in the two May 2023 orders.

## Pennsylvania

### Duquesne Light — Time-of-Use Supply Rate (default service TOU; NEEP "TOU Pilot")

- **Category:** TOU-whole-home (supply-only; delivery is not time-varying for non-EV customers)
- **Status (Oct 2026):** Active. Originally an EV-only pilot (DSP IX), expanded to all eligible residential/small commercial default service customers by PUC vote Apr 10, 2025; DSP X term June 1, 2025–May 31, 2029.
- **Design:** Voluntary, generation-only TOU in the default service plan for residential and small/medium commercial customers (<200 kW) with smart meters. Three periods: peak 3–9 pm non-holiday weekdays; off-peak 6 am–3 pm and 9–11 pm weekdays and 6 am–11 pm weekends/holidays; …
- **Defining docket:** P-2024-3048592, PA PUC, Opinion and Order Dec 5, 2024 (entered Jan 14, 2025; directed a supplemental TOU filing within 60 days) and Order approving the supplemental TOU rate Apr 10, 2025; compliance approval May 28, 2025. The EV-only supply pilot originated in P-2020-3019522 (Opinion and Order Jan 14, 2021, DSP IX). _[found]_
- **Current governing docket:** P-2024-3048592 (semiannual TOU reports/secretarial letters, latest Sept 16, 2026).
- **Where we learned it:** Primary, partly search summary — <https://www.puc.pa.gov/press-release/2025/puc-approves-expansion-of-duquesne-light-time-of-use-rate-04102025>; <https://www.puc.pa.gov/docket/P-2024-3048592>; <https://www.puc.pa.gov/pcdocs/1862250.pdf>
- **In NEEP:** Appendix A PA/Duquesne Daily Time Varying "TOU Pilot".
- **Notes:** NEEP calls it a pilot; since the Apr 2025 order it is generally available. I did not read the Apr 10, 2025 order PDF itself, only the docket sheet and PUC press release.

### Duquesne Light — EV Time-of-Use Distribution Rate (RS / RH / RA add-on HP schedules)

- **Category:** TOU-whole-home (delivery-only, EV owners)
- **Status (Oct 2026):** Active.
- **Design:** Residential distribution TOU for customers who own or lease an EV; whole-home usage is billed on it. Peak 3–9 pm non-holiday weekdays, off-peak all other times. Rates (Duquesne page): RS year-round standard 8.25¢ vs EV TOU peak 9.93¢ / off-peak 7.94¢ per kWh; …
- **Defining docket:** UNVERIFIED. The PUC EV page ties the Duquesne EV TOU pilot (three tiers, separate EV meter) to P-2020-3019522 (DSP IX), Jan 14, 2021; that is the supply pilot. I did not find the order that made the distribution TOU a tariff rate (candidate: R-2024-3046523, covered in the local HP-rates file for RA/RH). _[unverified]_
- **Current governing docket:** UNVERIFIED (R-2024-3046523 base rates likely).
- **Where we learned it:** Official page — <https://duquesnelight.com/energy-money-savings/home-energy-center/shift-and-save/ev-time-of-use-distribution-rate>; <https://www.puc.pa.gov/electricity/electric-vehicles/>
- **In NEEP:** Appendix A PA/Duquesne Technology-Specific "EV TOU Pilot; Heating with add-on heat pump (no new customers)" (RA cross-reference …
- **Notes:** See also the EV section (this is an EV-gated rate).

### Duquesne Light — Peak Saver Rewards (summer behavioral demand response; NEEP "PTR")

- **Category:** rebate-PTR
- **Status (Oct 2026):** Active (launched July 2025; enrollment reopened May 2026).
- **Design:** Voluntary, no device required. Up to five peak saver events per summer on weekdays, typically 3–9 pm for 2–3 hours; $1 in gift-card rewards per kWh reduced versus typical use. Limited to the first 7,500 eligible residential customers; …
- **Defining docket:** M-2020-3020818 (Duquesne Act 129 Phase IV EE&C Plan). The docket shows a Petition for Minor Changes filed Mar 19, 2025, a Secretarial Letter Apr 7, 2025 and a Revised Phase IV plan filed May 8, 2025; the order text approving the program was not read, so the approval date is UNVERIFIED. _[found]_
- **Current governing docket:** M-2020-3020818 (Phase IV); Phase V is M-2025-3052826 (Implementation Order June 18, 2025; Phase V runs June 1, 2026–May 31, 2031); Duquesne's Phase V plan docket not identified.
- **Where we learned it:** Official page — <https://www.puc.pa.gov/docket/M-2020-3020818>; <https://newsroom.duquesnelight.com/get-rewarded-for-smart-energy-use>; <https://newsroom.duquesnelight.com/save-energy-earn-rewards>
- **In NEEP:** Appendix A PA/Duquesne Rebates "PTR".
- **Notes:** This is an Act 129 pay-for-performance reward, not a rate. The $1/kWh reward is as described on Duquesne's pages.

### PECO — Default Service TOU (DSP-TOU)

- **Category:** TOU-whole-home (supply-only)
- **Status (Oct 2026):** Active (launched Sept 2021; continued in DSP VI through May 31, 2029).
- **Design:** Voluntary generation-price TOU for residential and small commercial default service customers with smart meters. Three year-round periods (peak, off-peak, super off-peak 12–6 am daily). …
- **Defining docket:** P-2020-3019290, PA PUC, Opinion and Order Dec 3, 2020 (PECO DSP V; approved the settlement creating TOU options). _[found]_
- **Current governing docket:** P-2024-3046008 (PECO DSP VI, June 1, 2025–May 31, 2029; Opinion and Order Nov 7, 2024; further Opinion and Order Jan 8, 2025 at the public meeting; PECO files annual DSP-TOU reports in P-2020-3019290).
- **Where we learned it:** Primary — <https://www.pecoprocurement.com/assets/files/PaPUC%20Order%20(December%203>; <https://www.puc.pa.gov/pcdocs/1855531.pdf>; <https://www.puc.pa.gov/pcdocs/1861692.pdf>
- **In NEEP:** Appendix A PA/PECO Daily Time Varying "TOU".
- **Notes:** Peak-period hours for DSP VI were in an image/table I did not capture; check Table 1 of the Nov 7, 2024 order.

### PECO — Rate RH (seasonal electric heating) and other legacy delivery rates

- **Category:** TOU-seasonal-only
- **Status (Oct 2026):** See local file.
- **Design:** Cross-reference only; see `context/domain/electric_heating_and_heat_pump_rates.md` entry PA-3 (PECO RH, docket R-2024-3046931 in that file).
- **Defining docket:** See local file. _[found]_
- **Current governing docket:** See local file.
- **Where we learned it:** NEEP listing only; no independent source found
- **In NEEP:** Appendix A PA/PECO Technology-Specific "Seasonal electric heating".
- **Notes:** Not re-researched per instructions.

### PPL Electric — Time-of-Use default service (seasonal TOU, supply-only)

- **Category:** TOU-seasonal-only (seasonal peak window; flat price by period)
- **Status (Oct 2026):** Active, program period June 1, 2025–May 31, 2029.
- **Design:** Voluntary supply-only TOU for most residential and small commercial customers (incl. net metering; excludes OnTrack/CAP). Summer (Jun 1–Nov 30 per PPL page; PUC order cites Jun–Aug summer) peak 2–6 pm weekdays; winter peak 4–8 pm weekdays; all other hours off-peak. …
- **Defining docket:** P-2024-3047290, PA PUC, Order Nov 7, 2024 approving the Aug 27, 2024 settlement (retained the existing TOU hours 2–6 pm summer / 4–8 pm winter instead of PPL's proposed redesign; PPL to evaluate TOU in next DSP). Earlier TOU: P-2020-3019356 (PPL DSP V, June 2021–May 2025; order date not retrieved). _[found]_
- **Current governing docket:** P-2024-3047290 (still active; new petitions in Sept–Oct 2026 relate to the DSP).
- **Where we learned it:** Primary — <https://www.puc.pa.gov/pcdocs/1855542.pdf>; <https://www.puc.pa.gov/pcdocs/1849611.pdf>; <https://www.pplelectric.com/site/ways-to-save/rates-and-shopping/time-of-use-plan>
- **In NEEP:** Appendix A PA/PPL Daily Time Varying "Seasonal TOU".
- **Notes:** Confirms NEEP. The PPL page lists summer as Jun 1–Nov 30; the EV rebate tariff uses Jun–Aug summer; I did not reconcile these.

### FirstEnergy Pennsylvania (Met-Ed, Penelec, Penn Power, West Penn) — Rider K Time-of-Use Default Service

- **Category:** TOU-whole-home (supply-only)
- **Status (Oct 2026):** Active; companies merged into FirstEnergy Pennsylvania Electric Company on Jan 1, 2024, keeping rate districts.
- **Design:** Optional generation-only TOU for smart-metered residential and small commercial customers (excludes CAP, budget billing, virtual net metering). Year-round periods: on-peak 2–9 pm Mon–Fri; super off-peak 11 pm–6 am daily; off-peak otherwise. Rates are multipliers on the PTC. …
- **Defining docket:** P-2021-3030012 (Met-Ed), P-2021-3030013 (Penelec), P-2021-3030014 (Penn Power), P-2021-3030021 (West Penn), PA PUC, Order Aug 4, 2022 approving the 2023–2027 DSP (DSP VI) with revised TOU riders. The Rider K TOU existed under the previous DSP (the 2022 order says the companies "currently offer" TOU riders); that earlier docket was not identified. _[found]_
- **Current governing docket:** same four dockets (DSP term June 1, 2023–May 31, 2027).
- **Where we learned it:** Primary — <https://www.puc.pa.gov/pcdocs/1750244.pdf>; <https://www.puc.pa.gov/pcdocs/1754636.pdf>; <https://www.puc.pa.gov/pcdocs/1779432.pdf>
- **In NEEP:** Appendix A PA/First Energy Daily Time Varying "TOU".
- **Notes:** Confirms NEEP. DSP VII for June 2027+ not yet found.

## Delaware

### Delmarva Power DE — Service Classification R-TOU-ND (optional residential TOU, non-demand)

- **Category:** TOU-whole-home (NEEP: seasonal TOU)
- **Status (Oct 2026):** active (August 2026 tariff).
- **Design:** Optional; limited to the first 5,000 customers; one-year minimum term and written contract; multi-register meter. On-peak 9 am-8 pm (EST) / 10 am-9 pm (EDT) weekdays including weekday holidays. Distribution `$0.093873` on-peak vs `$0.010914` off-peak per kWh; …
- **Defining docket:** NOT FOUND for the original optional TOU rate (likely an older Delmarva DE rate case; not located). _[not found]_
- **Current governing docket:** Docket 20-0149, Order No. 9770 (filed Sept 16, 2021, per the R-TOU-ND tariff footer). Delmarva's DE electric base rates were also set in Docket 22-0897, Order 10395 (Apr 18, 2024; application filed Dec 15, 2022). …
- **Where we learned it:** Primary — <https://www.delmarva.com/cdn/assets/v3/assets/blt47b6e332b18fb457/blt62f3e22e86bbad0a/67850d0ad19b5232ade02b59/2024.01.10_filing_DPL_DE_Electric_Primary_tar.pdf>; <https://depsc.delaware.gov/2024/04/11/delmarva-power-electric-rate-case-update/>; <https://depsc.delaware.gov/wp-content/uploads/sites/54/2024/04/Regular-Item-1f-Docket-22-0897-Order-10395-04-18-2024.pdf>
- **Notes:** A footer citing 20-0149 does not mean that docket defined the rate; it reflects a 2021 restatement. NEEP's "seasonal" label does not match the R-TOU-ND tariff text, which has no seasonal on-peak change in the distribution rates (SOS supply rates are seasonal).

### Delmarva Power DE — Rider "DP" Peak Energy Savings Credit (opt-out critical peak rebate)

- **Category:** rebate-CPP (critical peak rebate; default/opt-out)
- **Status (Oct 2026):** active (Rider DP in the Aug 2026 tariff). Delmarva's 25-1554 filing proposes a successor "Affordability and Load Flexibility Portfolio" for 2027-2029 (see below).
- **Design:** Customers are defaulted onto a critical peak rebate (CPR) with a customer baseline; they may opt out any time. NEEP Table 5 shows 93% participation in 2023.
- **Defining docket:** PSC Docket No. 09-311, Final Findings, Opinion and Order No. 8105, Jan 31, 2012. Delmarva's application to implement an advanced-metering-enabled dynamic pricing plan; it settled on CPR as the default. _[found]_
- **Current governing docket:** Docket 09-311 (initial order); the tariff footer for Rider DP was not separately traced.
- **Where we learned it:** Primary — <https://depsc.delaware.gov/wp-content/uploads/sites/54/2017/03/8105.pdf>
- **Notes:** Order 8105 text is a PDF where the page header reads "Order No. XXXX" but the running header reads Order No. 8105, dated "this 31st day of January, 2012". NEEP calls this a PTR; the order calls it a critical peak rebate.

### Delmarva Power DE — Docket 25-1554 "Affordability and Load Flexibility Portfolio" (proposed)

- **Category:** other (proposed EV-only TOU, whole-home TOU, DLC, BYOD thermostat, smart charge management)
- **Status (Oct 2026):** proposed. The Public Advocate moved to dismiss in April 2026; I did not confirm the outcome.
- **Design:** Application and direct testimony dated Dec 9, 2025 for a 2027-2029 portfolio costing about `$36.95` million, recovered through a new "Affordability and Load Flexibility Rider."
- **Defining docket:** 25-1554 (Delaware PSC), filing Dec 2025. The docket number comes from the PSC public notice file name; the testimony itself shows "25-XXXX". _[found]_
- **Current governing docket:** 25-1554, status UNVERIFIED.
- **Where we learned it:** Primary — <https://depsc.delaware.gov/wp-content/uploads/sites/54/2026/01/DKT-no.-25-1554-DPL-DSM-Public-Notice.pdf>; <https://publicadvocate.delaware.gov/2026/04/09/public-advocate-moves-to-dismiss-delmarva-powers-affordability-and-load-flexibility-docket/>
- **Notes:** Check this docket for any workbooks on proposed TOU designs.

## Maryland

### BGE — Schedule RL / RLH (optional residential TOU; electric-heat variant "RLH")

- **Category:** TOU-whole-home
- **Status (Oct 2026):** active on the tariff; marketing status ambiguous.
- **Design:** Opt-in whole-home TOU for residential customers. RLH is the electric-heating variant. Per local docs, RL dates to 1984 and its active/closed status is ambiguous (see Notes).
- **Defining docket:** NOT FOUND. The local doc `electric_heating_and_heat_pump_rates.md` (table at line 44) also says "Not found (RL dates to 1984)". I did not look for 1980s orders beyond that. _[not found]_
- **Current governing docket:** Case 9692 (BGE multi-year plan), Order 90948, Dec 14, 2023, per the local doc (not re-opened). Schedule RL is also an active marketing target in Case 9761, Order 91917 (local doc, line 464).
- **Where we learned it:** Primary — <https://azure-na-assets.contentstack.com/v3/assets/blt71bfe6e8a1c2d265/blte58f7cf25bd43b09/P3_SCH_RL.pdf> — local: `context/domain/electric_heating_and_heat_pump_rates.md`, `context/domain/bge_tou_rates.md`
- **Notes:** The local doc flags a conflict on whether RL is closed. The tariff sheet has no closed-to-new-customers language, but Order 91917 treats RL as an active target.

### BGE — Schedule RD (whole-home TOU, from the PC44 pilot)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** active. Permanent since 2022; revised tariff accepted May 20, 2026 (ML 330315).
- **Design:** Opt-in whole-home distribution and Standard Offer Service TOU. The DRIVE Act compliance filing lowered the all-in peak-to-off-peak ratio from 3.2:1 to 2.8:1 (per the local doc).
- **Defining docket:** PC 44 (administrative docket "Transforming Maryland's Electric Distribution Systems"). The Commission Letter Order of May 7, 2018 approved the opt-in pilot tariffs (BGE Schedule RD; PHI Schedule R-TOU-P). Per the local doc (line 139), not independently re-read. The Order No. 90298 (Jul 26, 2022) permanence step is also from the local doc (line 143). _[found]_
- **Current governing docket:** Case 9761 (DRIVE Act implementation), Order 91917, Oct 21, 2025.
- **Where we learned it:** Primary — <https://psc.maryland.gov/wp-content/uploads/Order-91917_ML-323522-9761-1.pdf> — local: `context/domain/bge_tou_rates.md`, `context/sources/md_hp_rates/mdpuc_9761_order_91917_drive_act_implementation.md`
- **Notes:** DRIVE-era Case 9761 order is the current anchor. The PC44 pilot docket identifier is PC 44, not a "Case No."

### Pepco MD — Schedule R-TOU-P (residential TOU program, opt-in)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** active.
- **Design:** Opt-in residential TOU. Summer on-peak 2-7 pm weekdays; winter on-peak 6-9 am and 5-9 pm weekdays. Rates effective Oct 1, 2026 per Pepco's page: summer `$0.41` on-peak and `$0.18` off-peak per kWh; …
- **Defining docket:** PC 44 (Letter Order May 7, 2018, pilot), per the local doc. DRIVE re-approval: Case 9761, Order 91917 (Oct 21, 2025). The Dec 1, 2025 effective date on the tariff page is consistent with implementation after that order. _[found]_
- **Current governing docket:** Case 9761 / Order 91917 for design. Pepco distribution rate levels are in Case 9702, Order 91181 (Jun 10, 2024), which granted only Rate Year 1 of the multi-year plan.
- **Where we learned it:** Primary — <https://www.pepco.com/cdn/assets/v3/assets/bltbb7c204688a1a6a8/blte8a580e4cc79e2c4/6a98797f82f57baf9e2f3917/2026-08-20_MASTER_MD_PEPCO_Tariff_Book_1.pdf>; <https://www.pepco.com/ways-to-save/for-your-home/maryland/time-of-use-rate>; <https://psc.maryland.gov/wp-content/uploads/Order-No.-91181-Order-on-Application-for-a-Multi-Year-Rate-Plan-9702.pdf>
- **Notes:** Delmarva MD uses the same R-TOU-P name.

### Delmarva Power MD — Schedule R-TOU-P (residential TOU program, opt-in)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** active (inferred from Order 91917 and the Order 91339 text that names Delmarva R-TOU-P).
- **Design:** Same PHI-family opt-in TOU as Pepco MD; I did not read Delmarva MD's own tariff sheet.
- **Defining docket:** PC 44 Letter Order (May 7, 2018), per the local doc. Order 91339 (Case 9478, Oct 1, 2024) names "R-TOU-P" as Delmarva's tariff. _[found]_
- **Current governing docket:** Case 9761 / Order 91917.
- **Where we learned it:** Primary — <https://www.rtoinsider.com/wp-content/uploads/2024/10/Order_EV-MUD-TOU-Schedules-9478.pdf>
- **Notes:** Delmarva MD tariff footer not read. A legacy Delmarva MD TOU schedule other than R-TOU-P may exist; not found.

### Pepco MD — Schedule R-TM (time-metered residential; legacy)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** closed to new customers.
- **Design:** Legacy TOU available only to customers on the schedule before Jul 1, 2000. Customer charge `$17.74`; kWh charge `$0.05296` summer and `$0.04493` winter (effective Apr 1, 2024; temporary rate swap Aug 2026).
- **Defining docket:** NOT FOUND (pre-2000). Not attempted beyond the tariff text. _[not found]_
- **Current governing docket:** Case 9702, Order 91181 (Jun 10, 2024) sets the customer charge year; rates in the tariff.
- **Where we learned it:** Primary
- **Notes:** User assignment listed R-TM; confirmed as a closed legacy schedule.

### Potomac Edison MD — Schedule R-TOU (new residential TOU service)

- **Category:** TOU-whole-home
- **Status (Oct 2026):** active as of Apr 20, 2026.
- **Design:** New opt-in residential TOU created under DRIVE Act Order 91917. Offered to eligible customers starting Apr 20, 2026.
- **Defining docket:** Case 9761, Order 91917 (Oct 21, 2025), approving Potomac Edison's proposal (ML 320116). A Letter Order of Jan 7, 2026 (ML 325593) approved the tariff pages. _[found]_
- **Current governing docket:** Case 9761.
- **Where we learned it:** Primary — <https://www.firstenergycorp.com/content/dam/customer/Customer%20Choice/Files/maryland/tariffs/pending-tariff-revisions/TOU-Tariff.pdf>
- **Notes:** PE's EV Charger TOU rider is a separate rate (see EV rates). The PE rate tariff was not read, so on-peak windows and ratios are not recorded here.

### SMECO — residential seasonal TOU (schedule id UNVERIFIED)

- **Category:** TOU-seasonal-only (per NEEP)
- **Status (Oct 2026):** UNVERIFIED.
- **Design:** NEEP lists a SMECO seasonal TOU; I did not read the tariff schedule. SMECO is a cooperative, and the DRIVE Act TOU obligation in Order 91917 applies to "investor-owned electric companies," so Case 9761 does not govern it.
- **Defining docket:** NOT FOUND. I looked at SMECO's rates page and Phase II EV material, which only name Rider EV-TOU, not a whole-home TOU. _[not found]_
- **Current governing docket:** NOT FOUND.
- **Where we learned it:** Official page — <https://www.smeco.coop/my-account/general-information/rates-fees/>
- **Notes:** SMECO files in its own rate cases (e.g. Case 9738 per a search summary — SEARCH-SUMMARY, not verified). I did not confirm any docket for SMECO's TOU.

### BGE — Rider 26 "Peak Time Rebate" (Smart Energy Rewards)

- **Category:** rebate-PTR
- **Status (Oct 2026):** active.
- **Design:** Event-based peak time rebate for residential smart-meter customers; per NEEP 77% enrolled in 2024. Listed in BGE tariff riders (e.g. Schedule EV rider list: "26. Peak Time Rebate").
- **Defining docket:** Case 9208, Order 83531 (Aug 13, 2010), BGE's smart grid initiative (AMI plus dynamic pricing). Source is the PSC smart-meter page and 2010 PSC annual report (secondary to the order itself); I did not read Order 83531. _[found]_
- **Current governing docket:** EmPOWER dockets 9494 / 9648 / 9705 (Order 90957, Dec 29, 2023). NEEP cites Case 9494 Item 151 (BGE semi-annual report, Aug 15, 2019).
- **Where we learned it:** Primary — <https://psc.maryland.gov/regulated-utilities/electricity/smart-grid-and-smart-meters/>; <https://psc.maryland.gov/wp-content/uploads/2025/11/MD-PSC-2010-Annual-Report.pdf>; <https://azure-na-assets.contentstack.com/v3/assets/blt71bfe6e8a1c2d265/bltbcb53d4782e3ba22/Rdrs_26_27.pdf>
- **Notes:** User assignment suggested "Case 9261?" for PTR; no evidence supports it. Case 9208 is the originating docket I found; 9494 is the later EmPOWER reporting docket.

### Pepco MD — Rider DP "Dynamic Pricing – Peak Energy Savings Credit"

- **Category:** rebate-PTR (peak-energy-savings credit; design details not read)
- **Status (Oct 2026):** active per the Aug 2026 tariff book (listed as applicable rider).
- **Design:** Residential rider listed in the Schedule R rider list ("Dynamic Pricing - Peak Energy Savings Credit"). I did not read the rider sheet itself.
- **Defining docket:** Case 9207, Order 83571 (Sept 2, 2010), Pepco's AMI plan and dynamic pricing (CPR) proposal. Source is the PSC smart-meter page; I did not read the order. _[found]_
- **Current governing docket:** EmPOWER dockets 9494 / 9648 / 9705.
- **Where we learned it:** Primary — <https://psc.maryland.gov/regulated-utilities/electricity/smart-grid-and-smart-meters/>
- **Notes:** Whether the credit is opt-in or default is not confirmed here.

### Delmarva Power MD — Peak Energy Savings Credit (dynamic pricing rider)

- **Category:** rebate-PTR (NEEP says opt-out)
- **Status (Oct 2026):** UNVERIFIED.
- **Design:** NEEP says Delmarva MD offers an opt-out PTR. I did not read Delmarva MD's rider.
- **Defining docket:** NOT FOUND for Delmarva MD. The 2010 PSC page says Delmarva's smart-grid initiative was handled differently (deferred) from Pepco's Case 9207. The related Delmarva case is probably Case 9294 (listed on the same PSC page), UNVERIFIED. _[not found]_
- **Current governing docket:** EmPOWER 9494 / 9648 / 9705 (UNVERIFIED for this specific credit).
- **Where we learned it:** Official page — <https://psc.maryland.gov/regulated-utilities/electricity/smart-grid-and-smart-meters/>
- **Notes:** The 93% opt-out figure in NEEP Table 5 is for Delmarva Delaware (2023), not Maryland.

### SMECO — Peak Time Rebate (NEEP)

- **Category:** rebate-PTR
- **Status (Oct 2026):** UNVERIFIED.
- **Design:** NEEP lists SMECO PTR; I found no tariff or order.
- **Defining docket:** NOT FOUND (searched SMECO rate pages and Phase II EV material). _[not found]_
- **Current governing docket:** NOT FOUND.
- **Where we learned it:** Official page
- **Notes:** SMECO's rider list on its rates page includes Rider DR-ST (Demand Response – Smart Temp), which is a device-based program, not a PTR.

### Pepco MD — Rider "DRS" (Residential Direct Load Control)

- **Category:** other (device-based demand response; included because it is on the Schedule R rider list)
- **Status (Oct 2026):** listed as an applicable rider; current enrollment unknown.
- **Design:** Residential direct-load-control rider. Tariff text says it is consistent with Order 82511 in Case 9149.
- **Defining docket:** Case 9149, Order 82511 (cited in the tariff text; order not read). _[found]_
- **Current governing docket:** EmPOWER lineage.
- **Where we learned it:** Primary
- **Notes:** Order 82511's date was not read.

## District of Columbia

### Pepco DC — no non-EV time-varying residential rate found

- **Category:** other
- **Status (Oct 2026):** none found.
- **Design:** NEEP lists only "whole-home EV TOU" for Pepco DC (see EV rates). I found no whole-home TOU for general residential customers, no PESC/PTR, and no CPP.
- **Defining docket:** not applicable. _[found]_
- **Current governing docket:** not applicable.
- **Where we learned it:** NEEP listing only; no independent source found
- **Notes:** PowerCentsDC pilot (c. 2008-2010) was a DC dynamic pricing pilot; I recall formal case 1056 but did not verify, so UNVERIFIED and not listed as an entry.

## West Virginia

### Appalachian Power / Wheeling Power (WV) — Schedule R.S. (seasonal declining-block residential)

- **Category:** TOU-seasonal-only (NEEP: "seasonal declining block")
- **Status (Oct 2026):** active (tariff effective Nov 17, 2025 base-case compliance; Sept 2026 ENEC update).
- **Design:** Basic service charge `$13.44` per month. Energy charge by season and block: Mar-Nov first 500 kWh `10.643¢`, over 500 kWh `9.189¢`; Jan, Feb and Dec has different blocks (read in the tariff). Default residential rate.
- **Defining docket:** NOT FOUND (decades-old structure). Current rates: Case No. 24-0854-E-42T, PSC Order dated Aug 28, 2025. _[not found]_
- **Current governing docket:** 24-0854-E-42T (reconsideration activity noted in Feb 2026; details not read).
- **Where we learned it:** Primary, partly search summary — <https://www.appalachianpower.com/lib/docs/ratesandtariffs/WestVirginia/2025_Base_Case_Tariff_11-17-2025.pdf>
- **Notes:** The 24-0854-E-42T case replaced a dismissed predecessor, 24-0669-E-42T. A 1984 special-reduced-rate order case number was not found.

### Appalachian Power / Wheeling Power (WV) — Schedule R.S.-T.O.D. (residential time-of-day)

- **Category:** TOU-whole-home (energy-only; no demand charge)
- **Status (Oct 2026):** active.
- **Design:** Optional whole-home TOU with single-phase multi-register meter. On-peak 7 am-9 pm weekdays `16.373¢`/kWh; off-peak `4.275¢`/kWh (about 3.8:1); `$13.44` basic service charge. …
- **Defining docket:** NOT FOUND. Current rates: 24-0854-E-42T, Order dated Aug 28, 2025. _[not found]_
- **Current governing docket:** 24-0854-E-42T.
- **Where we learned it:** Primary
- **Notes:** **NEEP discrepancy.** The tariff text I read shows an energy-only on-peak/off-peak schedule with no demand charge. NEEP's "with demand charge" label does not match the APCo residential tariff. The "battery storage TOU" is the Load Management Time-of-Day provision inside RS-TOD, not a separate schedule.

### Appalachian Power / Wheeling Power (WV) — Residential Peak Reduction Program and Load Management Water Heating provision

- **Category:** other (device-based load control; not a rate)
- **Status (Oct 2026):** active.
- **Design:** Peak Reduction Program: voluntary direct load control of central air or heat pump; capped at the first 6,000 customers registering per calendar year; up to 25 events/year; funded through the E.E./D.R. rider. …
- **Defining docket:** EE/DR program authorized in Case No. 17-0401-E-P (per public notice and a PSC doc); the 17-0401 attribution is from notices, not read from an order. Successor docket UNVERIFIED (I believe a "21-0332-E-P" EE/DR case exists but did not confirm). _[unverified]_
- **Current governing docket:** UNVERIFIED.
- **Where we learned it:** Primary, partly search summary — <https://wvlegals.com/psc-case-17-0401-e-p/>; <http://www.psc.state.wv.us/scripts/WebDocket/ViewDocument.cfm?CaseActivityID=574436&NotType=%27WebDocket%27>
- **Notes:** NEEP line 634 names "WH TOU, ES TOU, EV TOU" for APCo. WH is the load-management water-heating provision; ES is the energy-storage provision.

### Appalachian Power / Wheeling Power (WV) — "Peak Time Rebate" (NEEP)

- **Category:** rebate-PTR
- **Status (Oct 2026):** NOT CONFIRMED.
- **Design:** NEEP says APCo has a PTR. I found no PTR in the tariff texts I read.
- **Defining docket:** NOT FOUND. _[not found]_
- **Current governing docket:** NOT FOUND.
- **Where we learned it:** NEEP listing only; no independent source found
- **Notes:** Possibly NEEP is describing the Peak Reduction Program above. Treat as a NEEP discrepancy until shown otherwise.

### Mon Power / Potomac Edison (WV) — no residential time-varying rates

- **Category:** other
- **Status (Oct 2026):** UNVERIFIED.
- **Design:** NEEP says no rates. I did not read the Mon Power or Potomac Edison WV tariffs.
- **Defining docket:** not applicable (nothing found). _[found]_
- **Current governing docket:** not applicable.
- **Where we learned it:** NEEP listing only; no independent source found
- **Notes:** left as NEEP's claim.
