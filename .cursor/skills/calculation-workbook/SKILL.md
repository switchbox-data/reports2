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

The usual answer is the weighted-average representative home: one 8,760 before and one 8,760 after. Say on the sheet that the average across buildings was computed in the notebook, and that those hourly kWh are inputs.

A weighted share (the percent of homes whose bill falls) is a different file: one row per building, with annual bills as inputs and the share as a formula. Still ask before writing that, unless the user has already asked for it.

## What is an input, and what is a formula

Source data is values: metered kWh, a tariff's rates, an hourly marginal-cost schedule, a CAIRO annual bill.

Every step a reviewer would recompute is an Excel formula: a ratio, a sum, a product, a delta, a rate derived from those.

When a step cannot be a formula, say so in a note on the sheet. A weighted average over a building sample is the usual case. The sheet then starts from that average.

## Steps

1. List each cited number and the notebook variable it comes from.
2. One workbook per data source. A testimony table with two columns becomes two workbooks.
3. Recompute each formula step in Python from the same inputs. Assert it against the report variable the narrative prints. Write the file only after the asserts pass.
4. Upload with `upload_xlsx` from `lib.data.gsheets`. That trashes any file of the same name in the folder and uploads an Excel file, so the formulas survive download. `xlsx_to_gsheet` writes into a native Google Sheet; do not use it for this.
5. Print the Drive link. Delete the local cache copy only after the upload succeeds.

`upload_xlsx(path, folder_id)` needs a cached Google login (`just google-login`). It raises `GoogleLoginRequired` when the login is missing, and leaves the xlsx in place.

Worked examples:

- Connecticut representative home, section "Excel workbook exports" in `reports/ct_hp_rates/notebooks/representative_home.qmd`.
- Maryland surrebuttal Table 1: `lib.workbooks.representative_overcharge`, called from `reports/md_hp_rates/notebooks/representative_home.qmd` and `representative_home_rebuttal.qmd`.
- Maryland surrebuttal bill-decrease share: `lib.workbooks.bill_decrease_share`, called from `reports/md_hp_rates/notebooks/analysis_bills_only.qmd`.
