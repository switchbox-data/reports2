# nj_hp_rates

New Jersey: Jersey Central Power & Light's Rate RGT (Residential Geothermal & Heat Pump Service), the longest-running equipment-based heat pump rate in the Northeast. RGT is an equipment-eligibility rate, not a seasonal design, and JCP&L has no stand-alone cost study for it (it is combined with Rate RT in the class cost of service study). Useful as the example of a utility that has run a heat pump rate since 1999 without needing to identify customers beyond equipment attestation.

## Where the originals are

- The converted markdown and the raw workbooks are in this directory. **The original PDFs are not in the repo.** They are kept, unmodified, in a staging folder on the shared dev machine (not in git):
  `/ebs/home/jpv_switch_box/hp_rate_docket_staging/<folder>/` (path of each file is in its front matter as `original_pdf_path`). They are being uploaded to Zotero.
- Every converted markdown file has `source_url` (the URL we downloaded from, taken from our download manifest, not from the PDF) and `original_pdf_path` in its YAML front matter.
- One table with every document's URL, staged path and repo path: `/ebs/home/jpv_switch_box/hp_rate_docket_staging/PROVENANCE_FOR_ZOTERO.csv`.
- PDFs converted to markdown with the **extract-pdf-to-markdown** command (verbatim text, footnote counts checked, `<!-- PDF page N -->` markers so quotes can be cited by page). Where a file says _Partial_, only the pages relevant to the heat pump rate were extracted; the end of the file has an **Omitted pages index** saying what the other pages hold.

## Quick finder: which file answers which question

- **Why RGT exists / design:** no stand-alone RGT cost study. RGT is combined with RT in the class cost of service study ("RT/RGT"): see Lyons COSS (2026 petition JC-09, 2023 petition JC-8). Rate design for RT/RGT raises customer and distribution charges at the class increase (Peng, 2026 JC-10; 2023 JC-9).
- **Current rates (settled 2024):** BPU order and stipulation attachments (`..._bpu_order_approving_stipulation...md`): customer charge `$7.05` to `$8.07` (with 6.625% tax), summer on-peak `$0.060029`/kWh, off-peak `$0.028041`, all other months `$0.033061`; RGT 6,457 billing units, +`$55,341` (13.3%).
- **Proposed 2026 rates:** `..._jcpl_2026_base_rate_verified_petition...md` (RGT winter proposed equal to RS).
- **History:** 1999 tariff sheet (`..._19990801_..._rgt_original_sheet.md`) shows equipment-based eligibility.
- Not found in the retrieved record: why RGT was created.

## Files

### Testimony, reports and petitions

| File                                                                                                     | Docket / filed         | What it is and why it is here                                                                                                                                     | Scope                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `njbpu_ER26080420_20260806_jcpl_2026_base_rate_verified_petition_with_direct_testimony_and_schedules.md` | ER26080420; 2026-08-06 | 2026 base rate petition with testimony: RGT combined with RT in the cost study, proposed RGT winter rate set equal to RS; the newest and fullest RGT rate design. | Partial, 1432 pp. total. Extracted: PDF pages 1-2, 17, 20-21, 25-27, 81-83, 554-575, 586, 597-599, 779-803, 834, 876-879, 881-885, 922, 928, 949-950, 979, 1016-1019, 1021-1024, 1059, 1065, 1083-1084, 1092-1094, 1096-1097, 1108, 1111, 1119 of 1432 ()                    |
| `njbpu_ER23030144_20230316_jcpl_2023_base_rate_verified_petition_with_direct_testimony_and_schedules.md` | ER23030144; 2023-03-16 | 2023 petition: RT/RGT raised uniformly at the class increase; same cost-study treatment.                                                                          | Partial, 1362 pp. total. Extracted: PDF pp. 1-2 (cover letter); 15-16, 18-19 (petition: rate-change summary, tariff changes, witness/exhibit list); 513-521, 534-536, 541-542 (Exhibit JC-8, Lyons: cover, TOC, class definitions incl. RGT/RT combination, Figures 1-6, ... |
| `njbpu_ER23030144_20230807_jcpl_supplemental_testimony_12_plus_0_update_with_schedules.md`               | ER23030144; 2023-08-07 | Supplemental testimony with updated RT/RGT rates and RGT bill-impact schedules.                                                                                   | Partial, 394 pp. total. Extracted: PDF pp. 1-4 (Exhibit JC-2 Supplemental No. 1, Mader, complete); 7-11 (Exhibit JC-3 Supplemental No. 1, Pittavino, complete); 56-57, 142-143, 228-230 (Exhibit JC-8 Schedules TSL-1/TSL-2 12+0 COSS summary pages, ...                     |

### Tariffs and compliance filings

| File                                                                            | Docket / filed                                                       | What it is and why it is here                                                                                                                    | Scope                                                                                                                                                                           |
| ------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `njbpu_EO97070458_19990801_jcpl_tariff_bpu_no_9_part_iii_rgt_original_sheet.md` | EO97070458/EO97070459/EO97070460 (Board Order 5/24/1999); 1999-08-01 | Earliest RGT tariff text we could find (1999): equipment-based eligibility and the original rates; evidence that RGT predates the online record. | Partial, 66 pp. total. Extracted: PDF pages 1-11 of 66 (; cover, table of contents, Service Classifications RS, RT, RGT, and the first sheet of GS, which cross-references RGT) |

### Orders and decisions

| File                                                                               | Docket / filed         | What it is and why it is here                                                                               | Scope                                                                                                                                                                                   |
| ---------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `njbpu_ER23030144_20240214_bpu_order_approving_stipulation_jcpl_base_rate_case.md` | ER23030144; 2024-02-14 | BPU order approving the 2024 settlement with the settled RT/RGT rates (current rates before the 2026 case). | Partial, 418 pp. total. Extracted: Board Decision and Order PDF pp. 1-10 (pp. 11-13 service list omitted); OAL Initial Decision pp. 14-19 (incl. Cozen O'Connor transmittal letter, ... |
