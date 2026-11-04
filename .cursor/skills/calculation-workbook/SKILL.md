---
name: calculation-workbook
description: >-
  Export intermediate calculations and cited results to an Excel workbook with
  formulas intact, then upload it to a Google Drive folder. Use when the user
  asks for a workpaper, exhibit, calculation workbook, Google Sheet, or Excel
  file of testimony or report numbers with formulas intact.
---

# Calculation workbook

Build an `.xlsx` a reviewer can audit, upload it to the proceeding's Drive folder, and check every formula step against the number the narrative prints.

The narrative file (testimony or `index.qmd`) only loads finished variables. Export from the notebook that still has the inputs in memory.

## Stop if the file would be huge

Before writing one 8,760-hour profile per building, or any other file of that size, stop and ask the user.

The usual answer is the weighted-average representative home: one 8,760 before and one 8,760 after. Record the building count and the weight sum. Do not describe the sample on the sheet.

A weighted share (the percent of homes whose bill falls) is a different file: one row per building, with annual bills as inputs and the share as a formula. Still ask before writing that, unless the user has already asked for it.

## What is an input, and what is a formula

Source data is values: metered kWh, a tariff's rates, an hourly marginal-cost schedule, a CAIRO annual bill. Ratios, sums, products, deltas, and rates derived from those are formulas.

Do not add a note that restates the workbook: which schedules, which riders, which files, or how timestamps were aligned. The notebook prose should not explain the workbook either. A sheet note is one sentence, and only when a step cannot be a formula.

## Steps

1. List each cited number and the notebook variable it comes from.
2. One workbook per data source. A testimony table with two columns becomes two workbooks.
3. Assert the formula steps against the report variables before writing. After writing, read the workbook back. Assert the stored inputs against the notebook frames, and assert each intermediate evaluated from those stored cells against the notebook variable. Those asserts live in the notebook. Upload only after they pass.
4. Upload with `upload_xlsx` from `lib.data.gsheets`. That trashes any file of the same name in the folder and uploads an Excel file, so the formulas survive download. `xlsx_to_gsheet` writes into a native Google Sheet; do not use it for this.
5. Print the Drive link. Delete the local cache copy only after the upload succeeds.

`upload_xlsx(path, folder_id)` needs a cached Google login (`just google-login`). It raises `GoogleLoginRequired` when the login is missing, and leaves the xlsx in place.

Worked examples:

- Connecticut representative home, section "Excel workbook exports" in `reports/ct_hp_rates/notebooks/representative_home.qmd`.
- Maryland surrebuttal Table 1: `lib.workbooks.representative_overcharge`, called from `reports/md_hp_rates/notebooks/representative_home.qmd` and `representative_home_rebuttal.qmd`.
- Maryland surrebuttal bill-decrease share: `lib.workbooks.bill_decrease_share`, called from `reports/md_hp_rates/notebooks/analysis_bills_only.qmd`.
