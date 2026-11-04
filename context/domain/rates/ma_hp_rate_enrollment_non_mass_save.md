---
title: Massachusetts heat pump rate enrollment (non–Mass Save customers)
date: 2026-10-29
document_type: domain_synthesis
author: Switchbox
evidence_level: primary_sourced
scope: How Massachusetts IOUs enroll customers who do not receive a Mass Save heat pump rebate
citation_convention: |
  Switchbox synthesis—not a primary source. Each footnote gives (1) printed PDF page from the verbatim
  extract in context/sources/ma_hp_rates/ (see `<!-- PDF page N -->` markers), (2) line numbers in that
  extract (markdown link with `#L` line anchor, relative to this file under `../../sources/ma_hp_rates/`),
  and (3) a Switchbox short link to the primary PDF where one exists in reports/references.yaml.
extract_base: ../../sources/ma_hp_rates
---

# Massachusetts heat pump rate: enrolling without Mass Save

This note summarizes how Eversource (NSTAR Electric), National Grid, and Unitil enroll residential customers on the seasonal heat pump rate when the customer did **not** go through Mass Save. It is scoped to enrollment mechanics—not rate design.

**Primary extracts (repo):** [`context/sources/ma_hp_rates/`](../../sources/ma_hp_rates/)

**Consumer overview (no Switchbox short link):** [MA DPU, _Residential electric seasonal heat pump rates_](https://www.mass.gov/info-details/residential-electric-seasonal-heat-pump-rates) (`madpu_ResidentialElectricSeasonal_2025`). **This synthesis does not restate Mass.gov or IOU web enrollment steps**—verify operational URLs and forms there before testimony.

---

## Accuracy and open questions (read first)

Nothing below was invented without a filing, but several passages **infer, paraphrase, or combine** sources. Treat flagged items as **unverified** until checked against the primary PDF or live utility process.

| Issue                                        | What the doc says or implied                                                                                               | Risk                                                                                                                                                                                                                                                                                                                         | Status                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **A. Eversource Mass Save cutoff date**      | Jan 2026 reporting uses **Jan 1, 2019** for auto-enroll; D.P.U. 25-55 **order** references **Jan 1, 2022** (Exh. ES-HP-5). | We do **not** have a filing explaining the 2019 vs 2022 gap (compliance plan change, data availability, or informal expansion).                                                                                                                                                                                              | **Open—do not cite 2019 as “DPU-approved” without DPU-2-4 only.**                          |
| **B. Unitil attestation / annual review**    | Eligibility section cites D.P.U. **23-80** (2023) attestation + annual usage review.                                       | 25-08 Unitil responses describe **contact + affirm winter use + opt in** for non–Mass Save customers and do **not** repeat photo verification or the 23-80 CCHP attestation language. May still apply via tariff, but **23-80 enforcement text is not confirmed for the Nov 2025 seasonal program in the extracts we cite.** | **Open—confirm Unitil compliance tariff / current web process.**                           |
| **C. “Contacting the utility”**              | Summary once suggested phone contact for all IOUs.                                                                         | Eversource and National Grid filings specify **proactive apply** via **phone, website, or mobile app** (web/app need not be a phone call). Unitil 3-5 says **“contacting the Company.”**                                                                                                                                     | **Corrected in Summary; do not generalize across IOUs.**                                   |
| **D. Editorial inference**                   | Non–Mass Save uptake “depends on outreach and customer action—not utility data matching.”                                  | Logical summary of cannot-id responses; **not a utility or DPU statement.**                                                                                                                                                                                                                                                  | **Inference—remove or soften for testimony.**                                              |
| **E. National Grid “large share”**           | Paraphrase of post-launch auto-enroll.                                                                                     | Source text is **“significant majority,”** not “large share.”                                                                                                                                                                                                                                                                | **Use exact quote if citing.**                                                             |
| **F. “Same two intake paths as Eversource”** | Comparative framing for National Grid.                                                                                     | Substance matches NG Exhibit HP-1, but **wording is Switchbox comparison**, not NG language.                                                                                                                                                                                                                                 | **Paraphrase—cite NG exhibit directly.**                                                   |
| **G. Opt-out (Eversource)**                  | Opt-out section cites **April 2025 proposal** only for Eversource.                                                         | Post-launch opt-out mechanics for Eversource are **not** in the extracts indexed here (see D.P.U. 25-08-A directives on web opt-out info).                                                                                                                                                                                   | **Partial—Unitil letter cited; ES/NG post-launch opt-out not fully sourced in this note.** |
| **H. Live enrollment UX**                    | Implementation plans describe intended phone/portal/back-office flows (2024–2025 filings).                                 | **Not verified** against what customers see on utility sites in 2026.                                                                                                                                                                                                                                                        | **Open—check IOU pages before operational claims.**                                        |
| **I. Pre–Jan 1, 2019 Mass Save rebates**     | Unitil explicitly requires **self-enroll** for rebates before 1/1/2019.                                                    | Eversource bundles “prior to 2019” into **manual** enrollment with documentation; National Grid auto-enroll language in HP-1 is **broader** (“previously received” vs “since 2019” in adjacent paragraphs)—**do not assume identical cutoffs across IOUs without the exact NG compliance behavior.**                         | **Open for NG/Eversource vs Unitil alignment.**                                            |

---

## Summary

Massachusetts uses a **two-track** enrollment model (Switchbox label—not statutory language) at the three investor-owned electric utilities:

1. **Mass Save rebate track:** Auto-enrollment when the utility knows the customer received a qualifying heat pump incentive (with opt-out).[^unitil-auto][^es-post-launch][^ng-post-launch]
2. **All other eligible customers:** Must **proactively apply** (Eversource, National Grid) or **self-enroll** (Unitil). Eversource and National Grid: apply via **phone, website, or mobile app** with **documentary verification** as described in their implementation plans.[^es-proactive][^ng-proactive][^es-intake][^es-verify][^ng-intake][^ng-verify] Unitil (non–Mass Save): **contact the company**, **affirm** winter heat pump use, and **opt in** to the seasonal rate.[^unitil-self][^unitil-opt-in-process]

Utilities state they **cannot count or identify** all eligible heat pump customers who have not enrolled (especially outside Mass Save).[^unitil-cannot-id][^es-cannot-id][^ng-cannot-id]

---

## Eligibility (tariff availability)

The Eversource compliance tariff for Rate R-1HP ties service to an eligible heat pump used to heat or supplement heat for the home or part of the home, and to the customer **affirming ownership** of a heat pump at the service location.[^es-tariff-avail]

Unitil’s **D.P.U. 23-80** response (2023) describes enforcing HP-RES availability via customer **attestation** (cold-climate heat pump, primary or supplemental heat) and **annual usage review**.[^unitil-attest] **See open question B:** later D.P.U. 25-08 Unitil filings describe a different self-enrollment script for non–Mass Save customers and are the better source for that path.[^unitil-opt-in-process]

---

## Track 1: Mass Save auto-enrollment (context for the non–Mass Save path)

**Unitil:** Customers who receive a qualifying Mass Save heat pump rebate are auto-enrolled; they may self-enroll earlier using contractor leave-behind instructions; enrolled customers receive an opt-out letter.[^unitil-auto]

Customers with a Mass Save rebate **before January 1, 2019** are not on the auto-enroll path and **must self-enroll**.[^unitil-self]

**Eversource (as implemented, post-launch reporting):** Before the November 1, 2025 rate launch, Eversource auto-enrolled customers who received a heat pump from a Mass Save Sponsor after **January 1, 2019**; after launch, new Mass Save heat pump rebate recipients are auto-enrolled **weekly**.[^es-post-launch]

(Eversource’s April 2025 implementation **proposal** and the D.P.U. 25-55 **order** describe Mass Save auto-enrollment after **January 1, 2022**; January 2026 operational reporting describes auto-enrollment after **January 1, 2019**. **See open question A.**)[^es-proposal-auto-date][^es-post-launch][^es-order-2022]

**National Grid (post-launch reporting):** Before launch, auto-enrolled a **“significant majority”** of Mass Save sponsor heat pump customers after January 1, 2019; weekly auto-enrollment for new Mass Save rebates thereafter.[^ng-post-launch]

---

## Track 2: Non–Mass Save and legacy customers — how to opt in

### Eversource

- Customers **not** captured via Mass Save auto-enrollment must **proactively apply** for the heat pump rate.[^es-proactive]
- Intake channels: **inbound phone**, **website**, and **mobile app** self-service; enrollment requires **verification** with the application.[^es-intake]
- Acceptable verification: **photos of equipment serial numbers**; **proof of payment or purchase receipt**; **contractor invoice or installation receipt**. Eversource may audit and remove customers who cannot confirm verification.[^es-verify]
- Phone intake triggers a “solutions” email with requirements and an application to a back-office mailbox; web intake uses a portal with the same requirements; back-office confirms or denies enrollment.[^es-processing]
- As of January 23, 2026, nearly **12,000** customers not captured by Mass Save auto-enrollment (no Mass Save Sponsor rebate and/or install before 2019) had submitted documentation and been **manually enrolled**.[^es-manual-count]

### National Grid

- **All other customers** (outside Mass Save auto-enrollment) must **proactively apply**.[^ng-proactive]
- Mass Save auto-enroll vs **contact center / web / app** intake with **verification** (serial number photos, purchase proof, contractor invoice)—parallel structure to Eversource’s Exhibit ES-HP-5, per Exhibit HP-1.[^ng-intake][^ng-verify]
- National Grid states it has **no means** to count eligible heat pump customers who have not enrolled.[^ng-cannot-id]
- Identifying unenrolled heat pump customers is a “key challenge”; targeted outreach uses Mass Save data matched to customer records where possible—not a complete census of non–Mass Save installs.[^ng-meo-challenge]

### Unitil

- Customers who install **independent of Mass Save** must **self-enroll**.[^unitil-self]
- Non–Mass Save customers may enroll by **contacting Unitil**, **affirming** winter heat pump use, and **opting in** to the seasonal rate.[^unitil-opt-in-process]
- Unitil **cannot identify** non–Mass Save heat pump customers who do not opt in and therefore cannot report eligible-vs-enrolled percentages.[^unitil-cannot-id]
- Where data exist (e.g., Mass CEC incentives back to 2015), Unitil has used **automated phone and email** to reach customers not yet on the rate.[^unitil-outreach-cec]

---

## Opt-out

Mass Save auto-enrolled customers are to receive **opt-out instructions** in Eversource’s and National Grid’s **implementation plans** (as filed) and in Unitil’s **notification letter** (2025 response).[^es-proposal-opt-out][^unitil-auto][^ng-opt-out-proposal] Post-launch opt-out channels for all IOUs may also be described on Mass.gov and utility webpages; **not fully extracted here (open question G).**

---

## Source index (Switchbox short links)

| Citekey                                    | Short link                                                      | Repo extract                                                                                                                       |
| ------------------------------------------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `nstarelectric_Docket2555Residential_2025` | https://pub.switch.box/nstarelectric_Docket2555Residential_2025 | `context/sources/ma_hp_rates/madpu_25-55_20250417_exh_es_hp_5_marketing_and_outreach_final.md`                                     |
| `nstarelectric_Docket2508Response_2026`    | https://pub.switch.box/nstarelectric_Docket2508Response_2026    | `context/sources/ma_hp_rates/madpu_25-08_20260123_dpu_2_4_final.md`                                                                |
| `nstarelectric_Docket2555Compliance_2025a` | https://pub.switch.box/nstarelectric_Docket2555Compliance_2025a | `context/sources/ma_hp_rates/madpu_25-55_20250801_mdpu_85_eversource_r1hp_compliance.md`                                           |
| `meco_Docket23150Exhibit_2024`             | https://pub.switch.box/meco_Docket23150Exhibit_2024             | `context/sources/ma_hp_rates/madpu_23-150_20241230_ng_hp_rate_compliance_exh_hp_1_implementation.md`                               |
| `meco_Docket2508Information_2026`          | https://pub.switch.box/meco_Docket2508Information_2026          | `context/sources/ma_hp_rates/madpu_25-08_20260123_ng_dpu_common_3_5.md`                                                            |
| `meco_Docket2508Information_2025`          | https://pub.switch.box/meco_Docket2508Information_2025          | `context/sources/ma_hp_rates/madpu_25-08_20251114_ng_dpu_common_2_3.md`                                                            |
| `fge_Docket2508Response_2025`              | https://pub.switch.box/fge_Docket2508Response_2025              | `context/sources/ma_hp_rates/madpu_25-08_20251114_ir_response_unitil_dpu_common_2-3_auto_enroll_vs_self_enroll_identification.md`  |
| `fge_Docket2508Response_2026`              | https://pub.switch.box/fge_Docket2508Response_2026              | `context/sources/ma_hp_rates/madpu_25-08_20260123_ir_response_unitil_dpu_common_3-5_cannot_identify_non_mass_save_hp_customers.md` |
| `fge_Docket2380Response_2023`              | https://pub.switch.box/fge_Docket2380Response_2023              | `context/sources/ma_hp_rates/madpu_23-80_20230919_ir_response_dpu_2-04_hp_tariff_availability_enforcement_attestation.md`          |

---

## Footnotes

[^es-proactive]: NSTAR Electric (Eversource), _Residential Heat Pump Rate Implementation Plan_ (Exhibit ES-HP-5), D.P.U. 25-55, p. 3 (PDF p. 3), [extract L78](../../sources/ma_hp_rates/madpu_25-55_20250417_exh_es_hp_5_marketing_and_outreach_final.md#L78); [primary](https://pub.switch.box/nstarelectric_Docket2555Residential_2025).

[^es-proposal-auto-date]: Same, p. 3–4 (PDF pp. 3–4), [extract L78–86](../../sources/ma_hp_rates/madpu_25-55_20250417_exh_es_hp_5_marketing_and_outreach_final.md#L78-L86) (Mass Save auto-enroll proposed for rebates after January 1, 2022); [primary](https://pub.switch.box/nstarelectric_Docket2555Residential_2025).

[^es-order-2022]: Massachusetts DPU, Order (D.P.U. 25-55), discusses auto-enrollment for Mass Save rebates after January 1, 2022 (Exh. ES-HP-5 at 3–4); [extract L179](../../sources/ma_hp_rates/madpu_25-55_20250729_dpu_d_p_u_25_55_final_order_7_29_25.md#L179), [L351–355](../../sources/ma_hp_rates/madpu_25-55_20250729_dpu_d_p_u_25_55_final_order_7_29_25.md#L351-L355). **No Switchbox short link in `references.yaml` for this order extract—use repo extract or docket PDF.**

[^es-proposal-opt-out]: Same, p. 4 (PDF p. 4), [extract L86](../../sources/ma_hp_rates/madpu_25-55_20250417_exh_es_hp_5_marketing_and_outreach_final.md#L86) (auto-enrolled Mass Save customers notified with opt-out instructions); [primary](https://pub.switch.box/nstarelectric_Docket2555Residential_2025).

[^es-intake]: Same, p. 4 (PDF p. 4), [extract L88](../../sources/ma_hp_rates/madpu_25-55_20250417_exh_es_hp_5_marketing_and_outreach_final.md#L88) (contact center, website, and mobile app intake with verification); [primary](https://pub.switch.box/nstarelectric_Docket2555Residential_2025).

[^es-verify]: Same, pp. 4–5 (PDF pp. 4–5), [extract L92–98](../../sources/ma_hp_rates/madpu_25-55_20250417_exh_es_hp_5_marketing_and_outreach_final.md#L92-L98) (acceptable verification documents; audit and removal); [primary](https://pub.switch.box/nstarelectric_Docket2555Residential_2025).

[^es-processing]: Same, p. 5 (PDF p. 5), [extract L102–104](../../sources/ma_hp_rates/madpu_25-55_20250417_exh_es_hp_5_marketing_and_outreach_final.md#L102-L104) (solutions email, web portal, back-office confirmation or denial); [primary](https://pub.switch.box/nstarelectric_Docket2555Residential_2025).

[^es-post-launch]: NSTAR Electric (Eversource), Response to DPU-2-4, D.P.U. 25-08, p. 1 (PDF p. 1), [extract L52](../../sources/ma_hp_rates/madpu_25-08_20260123_dpu_2_4_final.md#L52) (auto-enroll after January 1, 2019; weekly enrollment post-launch); [primary](https://pub.switch.box/nstarelectric_Docket2508Response_2026).

[^es-manual-count]: Same, p. 1 (PDF p. 1), [extract L54](../../sources/ma_hp_rates/madpu_25-08_20260123_dpu_2_4_final.md#L54) (nearly 12,000 manual enrollments without Mass Save capture); [primary](https://pub.switch.box/nstarelectric_Docket2508Response_2026).

[^es-cannot-id]: Same, p. 1 (PDF p. 1), [extract L50](../../sources/ma_hp_rates/madpu_25-08_20260123_dpu_2_4_final.md#L50) (no means to count eligible but unenrolled heat pump customers); [primary](https://pub.switch.box/nstarelectric_Docket2508Response_2026).

[^es-tariff-avail]: NSTAR Electric (Eversource), Compliance Tariff R-1HP (M.D.P.U. No. 85), D.P.U. 25-55, Availability section (PDF p. 1), [extract L42](../../sources/ma_hp_rates/madpu_25-55_20250801_mdpu_85_eversource_r1hp_compliance.md#L42); [primary](https://pub.switch.box/nstarelectric_Docket2555Compliance_2025a).

[^ng-proactive]: National Grid, _Residential Heat-Pump Rate Implementation Plan_ (Exhibit HP-1), D.P.U. 23-150, p. 8 (PDF p. 8), [extract L154](../../sources/ma_hp_rates/madpu_23-150_20241230_ng_hp_rate_compliance_exh_hp_1_implementation.md#L154); [primary](https://pub.switch.box/meco_Docket23150Exhibit_2024).

[^ng-intake]: Same, pp. 8–9 (PDF pp. 10–11), [extract L164–168](../../sources/ma_hp_rates/madpu_23-150_20241230_ng_hp_rate_compliance_exh_hp_1_implementation.md#L164-L168) (contact center and self-service web/app intake with verification); [primary](https://pub.switch.box/meco_Docket23150Exhibit_2024).

[^ng-verify]: Same, p. 9 (PDF p. 11), [extract L172–174](../../sources/ma_hp_rates/madpu_23-150_20241230_ng_hp_rate_compliance_exh_hp_1_implementation.md#L172-L174) (verification documents; audit and removal); [primary](https://pub.switch.box/meco_Docket23150Exhibit_2024).

[^ng-post-launch]: National Grid, Response to DPU-Common-3-5-NG, D.P.U. 25-08, p. 1 (PDF p. 1), [extract L47](../../sources/ma_hp_rates/madpu_25-08_20260123_ng_dpu_common_3_5.md#L47) (“significant majority” auto-enrolled after January 1, 2019; weekly post-launch); [primary](https://pub.switch.box/meco_Docket2508Information_2026).

[^ng-opt-out-proposal]: National Grid, _Residential Heat-Pump Rate Implementation Plan_ (Exhibit HP-1), D.P.U. 23-150, [extract L162](../../sources/ma_hp_rates/madpu_23-150_20241230_ng_hp_rate_compliance_exh_hp_1_implementation.md#L162) (auto-enrolled customers notified with opt-out instructions); [primary](https://pub.switch.box/meco_Docket23150Exhibit_2024).

[^ng-cannot-id]: Same, p. 1 (PDF p. 1), [extract L49](../../sources/ma_hp_rates/madpu_25-08_20260123_ng_dpu_common_3_5.md#L49) (cannot report eligible-but-unenrolled counts); [primary](https://pub.switch.box/meco_Docket2508Information_2026).

[^ng-meo-challenge]: National Grid, Response to DPU-Common-2-3-NG, D.P.U. 25-08, p. 1 (PDF p. 1), [extract L53](../../sources/ma_hp_rates/madpu_25-08_20251114_ng_dpu_common_2_3.md#L53) (identification challenge; Mass Save cross-match for outreach); [primary](https://pub.switch.box/meco_Docket2508Information_2025).

[^unitil-auto]: Unitil, Response to DPU-Common 2-3, D.P.U. 25-08, p. 1 (PDF p. 1), [extract L48](../../sources/ma_hp_rates/madpu_25-08_20251114_ir_response_unitil_dpu_common_2-3_auto_enroll_vs_self_enroll_identification.md#L48) (Mass Save auto-enroll, leave-behind self-enroll, opt-out letter); [primary](https://pub.switch.box/fge_Docket2508Response_2025).

[^unitil-self]: Same, p. 1 (PDF p. 1), [extract L50](../../sources/ma_hp_rates/madpu_25-08_20251114_ir_response_unitil_dpu_common_2-3_auto_enroll_vs_self_enroll_identification.md#L50) (rebate before 1/1/2019 or install independent of Mass Save must self-enroll); [primary](https://pub.switch.box/fge_Docket2508Response_2025).

[^unitil-outreach-cec]: Same, p. 1 (PDF p. 1), [extract L50–51](../../sources/ma_hp_rates/madpu_25-08_20251114_ir_response_unitil_dpu_common_2-3_auto_enroll_vs_self_enroll_identification.md#L50-L51) (October automated phone/email to Mass CEC incentive recipients not yet on rate); [primary](https://pub.switch.box/fge_Docket2508Response_2025).

[^unitil-opt-in-process]: Unitil, Response to DPU-Common 3-5, D.P.U. 25-08, p. 1 (PDF p. 1), [extract L44–46](../../sources/ma_hp_rates/madpu_25-08_20260123_ir_response_unitil_dpu_common_3-5_cannot_identify_non_mass_save_hp_customers.md#L44-L46) (contact Company, affirm winter use, opt in); [primary](https://pub.switch.box/fge_Docket2508Response_2026).

[^unitil-cannot-id]: Same, p. 1 (PDF p. 1), [extract L46](../../sources/ma_hp_rates/madpu_25-08_20260123_ir_response_unitil_dpu_common_3-5_cannot_identify_non_mass_save_hp_customers.md#L46) (cannot identify non–Mass Save customers who did not opt in); [primary](https://pub.switch.box/fge_Docket2508Response_2026).

[^unitil-attest]: Unitil, Response to DPU 2-04, D.P.U. 23-80, p. 1 (PDF p. 1), [extract L45–49](../../sources/ma_hp_rates/madpu_23-80_20230919_ir_response_dpu_2-04_hp_tariff_availability_enforcement_attestation.md#L45-L49) (affirmation requirement; attestation; annual usage review); [primary](https://pub.switch.box/fge_Docket2380Response_2023).
