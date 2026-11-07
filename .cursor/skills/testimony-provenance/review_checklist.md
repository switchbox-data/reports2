# Review checklist for `provenance_review.csv`

Each row is `check, item, detail`. Work top to bottom; anything not resolved goes to the user.

## Placement

| Check                        | Meaning                                                                | What to do                                                                                                |
| ---------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `match_missing`, `match_low` | A rendered value was not found in the PDF, or only weakly              | Find it in the PDF. Edited in Word: add a `KnownDifference`. Cut from the filing: nothing. Otherwise ask. |
| `match_fallback`             | Found by searching for the value near similar words                    | Confirm the page and line; `extract_location` would flag a wrong one.                                     |
| `pdf_vs_cache`               | The PDF shows a different value than the cache at the tag              | Says whether the pre-filing render had the cache value. Ask the user, then record a `KnownDifference`.    |
| `known_difference`           | A recorded difference was seen                                         | Nothing; confirms the explanation applies.                                                                |
| `extract_not_found`          | The words around a number are not in the validated extract             | Usually extract layout (a figure description in between). Check by hand.                                  |
| `extract_location`           | The extract places the number elsewhere                                | Trust the extract unless it is wrong; fix the alignment or ask.                                           |
| `extract_checked`            | Count of locations checked and agreeing                                | All should agree.                                                                                         |
| `footnote_match`             | A qmd footnote matched its PDF footnote weakly                         | Check the footnote numbering.                                                                             |
| `excluded_prior_testimony`   | Inline expressions left out by `include_namespaces` or `exclude_codes` | Confirm each one repeats an earlier testimony's number.                                                   |

## Links

| Check               | Meaning                                                        | What to do                                                               |
| ------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `unresolved`        | No cell found for an expression or figure label                | Add a namespace, a resolver, or fix the label.                           |
| `multi_cell`        | The expression uses variables from several cells               | Linked to the first; usually fine. Check the link is the meaningful one. |
| `hardcoded_missing` | A `Hardcoded` context string is not in the PDF                 | Fix the context to match the filed wording.                              |
| `hardcoded_note`    | A review note on a hardcoded number                            | Tell the user (e.g. a methodology doc that rounds differently).          |
| `link_missing`      | A GitHub link does not resolve (`--check-links`)               | Push the tag (with approval), or fix the path.                           |
| `links_checked`     | Count of files and folders linked, and how many were not found | None should be missing.                                                  |

## Figures and tables

| Check                            | Meaning                                         | What to do                                                                         |
| -------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------- |
| `figure_count`                   | Embeds and PDF figure captions differ in number | Look for a commented-out embed or a caption the indexer missed (`pdf_lines.json`). |
| `caption_mismatch`               | Notebook caption and PDF caption differ         | Edited caption, or embeds out of order.                                            |
| `table_count`, `table_not_found` | A qmd table was not located in the PDF          | Check `pdf_lines.json` around where it should be.                                  |
| `table_title`                    | An uncaptioned table was titled from its header | Fine for the reader; mention it.                                                   |

## Cache and runs

| Check                                                 | Meaning                                                                      | What to do                                                                 |
| ----------------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `cache_file`                                          | A cache file read, with hash and time                                        | Record only.                                                               |
| `cache_missing`                                       | A cache file the setup cell needs is absent                                  | Render that notebook in the tag worktree.                                  |
| `cache_not_from_tag`                                  | The cache was written after the tag by other code                            | Rebuild from a worktree at the tag (`--path-exec-dir`).                    |
| `run_record_missing`, `run_file_missing`              | A run directory lacks an expected file                                       | Ask; the run may be incomplete.                                            |
| `run_tariff_vs_pin`                                   | A run's tariff differs from the pinned RDP commit                            | Ask; the pin may be wrong.                                                 |
| `mc_hash`, `mc_unrecorded`, `mc_unchanged_since_runs` | Marginal cost files: recorded hash, no record, or dated before the first run | `mc_unchanged_since_runs` is the evidence when runs did not record hashes. |
| `runs_checked`                                        | Summary of the run checks                                                    | Record only.                                                               |
