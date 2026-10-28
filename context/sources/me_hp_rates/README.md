# me_hp_rates

Maine heat pump and beneficial-electrification rates: Central Maine Power's A-Seasonal / Seasonal Heat Pump (SHP) rate and Electric Technology (ET) rate (dockets 2021-00325, 2022-00152, 2026-00248) and Versant Power's heat pump rate (2021-00325). Includes the rate design workbooks, the Demand Side Analytics evaluation of what CMP knew about participants, and the orders.

## Where the originals are

- The converted markdown and the raw workbooks are in this directory. **The original PDFs are not in the repo.** They are kept, unmodified, in a staging folder on the shared dev machine (not in git):
  `/ebs/home/jpv_switch_box/hp_rate_docket_staging/<folder>/` (path of each file is in its front matter as `original_pdf_path`). They are being uploaded to Zotero.
- Every converted markdown file has `source_url` (the URL we downloaded from, taken from our download manifest, not from the PDF) and `original_pdf_path` in its YAML front matter.
- One table with every document's URL, staged path and repo path: `/ebs/home/jpv_switch_box/hp_rate_docket_staging/PROVENANCE_FOR_ZOTERO.csv`.
- PDFs converted to markdown with the **extract-pdf-to-markdown** command (verbatim text, footnote counts checked, `<!-- PDF page N -->` markers so quotes can be cited by page). Where a file says _Partial_, only the pages relevant to the heat pump rate were extracted; the end of the file has an **Omitted pages index** saying what the other pages hold.

## Quick finder: which file answers which question

**CMP and Versant.** CMP identified participants by self-attestation ("verbally affirming heat pump ownership"), capped enrollment at 5,000, and the evaluator (Demand Side Analytics) held the rebate records; the evaluation is the best account of what data the utility did and did not have.

- **Design workbooks:** `mepuc_2026-00248_..._cmp_attachment_1_2026.xlsx` (A-Seasonal design, model-home bills of about `$1,854`); `mepuc_2021-00325_20220421_cmp_attachment_2.xlsx` (marginal-cost fixed-charge workbook).
- **CMP testimony and filings:** `mepuc_2022-00152_..._rate_design_and_revenue_allocation_testimony...md` (RD-16 to RD-19); request for approval of Rate A-Seasonal (2021-00325, Oct 11, 2022); request to reinstate (2026-00248).
- **Evaluation:** `mepuc_2026-00248_20260904_dsa_final_report_et_and_hp_rates.md`: bill and load results and what data CMP had.
- **Versant (A-20 heating rate, Bangor Hydro District):** comments, stipulation (Section F), ratebook and rate design order from 2021-00325.
- **Orders:** CMP rate design order and stipulation approval (2021-00325).
- **History:** `mepuc_2012-00343_..._emera_maine_heat_pump_pilot_final_report...md` (rebate pilot, not a rate).
- Pre-existing CMP files in this directory (Rate A tariff, Section 44 transmission, ET rate, SHP reconstruction, final report 2022-00152) are listed at the bottom.

## Files

### Workbooks (raw `.xlsx`, not converted)

| File                                                   | Docket / filed         | What it is and why it is here                                                                                                                | Scope                  |
| ------------------------------------------------------ | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `mepuc_2026-00248_20260825_cmp_attachment_1_2026.xlsx` | 2026-00248; 2026-08-25 | CMP's A-Seasonal design workbook (model home bill `$1,854.21` versus `$1,854.17` on the ET rate); the best surviving derivation of the rate. | Raw workbook, 203.0 KB |
| `mepuc_2021-00325_20220421_cmp_attachment_2.xlsx`      | 2021-00325; 2022-04-21 | CMP's marginal-cost fixed-charge workbook supporting its response to the Staff straw proposal.                                               | Raw workbook, 49.0 KB  |

### Testimony, reports and petitions

| File                                                                                        | Docket / filed         | What it is and why it is here                                                                                                                   | Scope         |
| ------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `mepuc_2026-00248_20260904_dsa_final_report_et_and_hp_rates.md`                             | 2026-00248; 2026-09-04 | Demand Side Analytics evaluation: what data CMP had (rebate data held only by the evaluator, plus interval data) and the bill and load results. | Full (48 pp.) |
| `mepuc_2022-00152_20220909_rate_design_and_revenue_allocation_testimony_updated_version.md` | 2022-00152; 2022-09-09 | CMP's only sworn testimony on the optional beneficial-electrification rates (pp. RD-16 to RD-19).                                               | Full (37 pp.) |
| `mepuc_2012-00343_20141120_emera_maine_heat_pump_pilot_final_report_111714.md`              | 2012-00343; 2014-11-20 | Evaluation of the earlier Bangor Hydro heat pump pilot that Versant cites as the origin of its heat pump rate experience.                       | Full (65 pp.) |

### Settlements, stipulations and requests

| File                                                                             | Docket / filed         | What it is and why it is here                                                                                                              | Scope         |
| -------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------- |
| `mepuc_2021-00325_20221011_cmp_request_for_approval_of_rate_a_seasonal_final.md` | 2021-00325; 2022-10-11 | CMP's filing: price points, revenue neutrality against A-TOU-OPTS, the 5,000 cap and 'verbally affirming heat pump ownership' eligibility. | Full (2 pp.)  |
| `mepuc_2026-00248_20260825_cmp_request_to_reinstate_a_seasonal_rate_2026.md`     | 2026-00248; 2026-08-25 | CMP's own account of the design logic in asking to reinstate the cancelled rate.                                                           | Full (2 pp.)  |
| `mepuc_2021-00325_20220926_cmp_revised_stipulation_draft_geo_signed.md`          | 2021-00325; 2022-09-26 | Revised stipulation; para. 9 creates the pilot heat pump rate.                                                                             | Full (11 pp.) |
| `mepuc_2021-00325_20211201_vp_comments_120121.md`                                | 2021-00325; 2021-12-01 | Versant comments describing A-20's structure (above-700-kWh block cut to 3.228 cents/kWh in Oct-Apr) and eligibility.                      | Full (83 pp.) |
| `mepuc_2021-00325_20220801_stipulation_2021_00325_080122.md`                     | 2021-00325; 2022-08-01 | Versant stipulation Section F: keeps A-20 with the 50% heating test and adds heat pump water heaters.                                      | Full (24 pp.) |

### Tariffs and compliance filings

| File                                                                                               | Docket / filed         | What it is and why it is here                              | Scope         |
| -------------------------------------------------------------------------------------------------- | ---------------------- | ---------------------------------------------------------- | ------------- |
| `mepuc_2021-00325_20221018_bhd_ratebook_2022_ev_battery_storage_heating_filed_10_18_2022_clean.md` | 2021-00325; 2022-10-18 | Bangor Hydro District rate book with the A-20 tariff text. | Full (15 pp.) |

### Orders and decisions

| File                                                                               | Docket / filed         | What it is and why it is here                                                                       | Scope        |
| ---------------------------------------------------------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------------- | ------------ |
| `mepuc_2021-00325_20221026_cmp_rate_design_order_rate_a_seasonal_no_2021_00325.md` | 2021-00325; 2022-10-26 | Commission order approving A-Seasonal (the defining order).                                         | Full (3 pp.) |
| `mepuc_2021-00325_20220927_2021_00325_order_approving_stipulation_cmp.md`          | 2021-00325; 2022-09-27 | Sept 27, 2022 order approving CMP's stipulation in the rate design investigation (opens the pilot). | Full (7 pp.) |
| `mepuc_2021-00325_20221213_versant_rate_design_order_no_2021_00325.md`             | 2021-00325; 2022-12-13 | Commission order on Versant's rate design (approval of the heating rate changes).                   | Full (4 pp.) |

### Files that were already in this directory

| File                                      | Notes                                                                                                                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `a-seasonal.xlsx`                         | CMP rate bulletin for Rate A-Seasonal (Oct 1, 2025 revision). A tariff bulletin, not the 2026 rate design workbook (`mepuc_2026-00248_..._cmp_attachment_1_2026.xlsx`). |
| `cmp_rate_a_tariff_july_2026.md`          | CMP Rate A tariff and MPUC component breakdown.                                                                                                                         |
| `cmp_section_44_transmission_services.md` | CMP Section 44 transmission charges.                                                                                                                                    |
| `cmp_et_rate_july_2026.md`                | CMP ET rate.                                                                                                                                                            |
| `cmp_shp_rate_reconstructed.md`           | Reconstruction of the SHP rate across 8 revisions.                                                                                                                      |
| `cmp_final_report_2025_2022-152.md`       | CMP final report (Docket 2022-00152, Dec 5, 2025) with the DSA evaluation as Attachment 6 (raw extraction). Not re-extracted from staging.                              |
