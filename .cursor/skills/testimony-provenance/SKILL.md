---
name: testimony-provenance
description: >-
  Build a provenance document for filed expert testimony: a Word table listing every figure, table
  and computed number in the filed PDF with its page and line, each linked to the notebook cell
  (or rate-design-platform file) that produced it, at a frozen git tag. Use when the user asks for a
  provenance table, a "where do the numbers come from" exhibit, a document linking testimony to code,
  or an interrogatory response like CT CIEC-1.
---

# Testimony provenance

The engine is `lib/provenance/`; each testimony has a thin `build_provenance.py` that builds a
`ProvenanceConfig` and calls `lib.provenance.build.main`. Two working examples, the second the
template to copy:

- `reports/ct_hp_rates/provenance/build_provenance.py` (CT CIEC-1, tag `ct_eversource_submission`)
- `reports/md_hp_rates/provenance/direct/build_provenance.py` (MD BGE direct, tag `md_bge_submission`)

The reader is a non-technical regulator or paralegal. The Word document says only where each item is
and where its code is. Every internal check (mismatches, cache dates, run verification) goes to
`provenance_review.csv`, which is never sent.

## What the build does

1. Indexes the filed PDF by printed page, margin line number, footnote and caption. Page and line numbers
   come from `lib.sources.pagelines.read_pdf`, the reader behind source extracts' markers; the testimony
   is the run of pages whose printed numbers increase (attachments restart at 1 and are skipped).
2. Reads the testimony `.qmd` **at the tag** (`git show`), evaluates its setup cell in `path_exec_dir`, and
   renders each inline `{python}` expression to its value.
3. Aligns the qmd text with the PDF text to place every value on its page and line (exact, anchored,
   fallback value search, or low/missing for review).
4. Links each expression to the notebook cell that sets its variable (via `namespaces`), each embedded
   figure to its labeled cell, and each table to the testimony lines that define it.
5. Cross-checks every number's location against the validated extract with `pagelines.cite`.
6. Optionally verifies the CAIRO runs on S3: run records, tariffs vs. the pinned RDP commit, and the
   marginal cost files' hashes and dates.
7. Writes `provenance.md`, the `.docx` (landscape), `provenance.csv`, `provenance_review.csv` and
   `pdf_lines.json`.

## Steps

1. **Get the filed PDF and its extract.** The testimony must be in the source library with a validated
   extract under `context/sources/<project>/` (`citation_scheme: page_line`, an `md5`). If it is not, ingest
   it first with the `ingest-source` skill. Fetch the PDF with `just fetch-source <citekey>`; it lands next
   to the extract. Set `path_pdf` to that path and `path_extract` to the extract; the build checks the
   PDF's md5 against the extract's.
2. **Fix the tag.** Ask the user which commit the filed testimony was rendered from. Create an annotated
   tag there in reports2 (`git tag -a <name> <commit> -m ...`), and one with the same name in
   rate-design-platform on the commit pinned by the runs (`RDP_REF` in the batch config). **Do not push
   tags without the user's approval.** Every permalink points at the tag, so it must not move.
3. **Render the cache at the tag.** The setup cell reads `cache/*.pkl`; a later render gives later numbers.
   Make a worktree at the tag, `uv sync --frozen`, render the notebooks the setup cell loads, and pass that
   report directory as `--path-exec-dir` (see the MD script's docstring for the commands).
4. **Write the config.** Copy the MD script into `reports/<project>/provenance/<testimony>/` and edit:
   `TAG`, `namespaces` (setup-cell prefix to notebook), `notebook_blurbs` (plain-language title and one
   sentence per notebook), `intro`, `title`/`subtitle`, `docx_name`, `platform_links` (RDP code and
   methodology docs at the tag), and `run_checks` (batch prefix, RDP pin, marginal cost types). Copy the
   `.gitignore` too. Add a Justfile recipe like `provenance-direct path_exec_dir:`.
5. **Run and triage.** Run the recipe, then work through `provenance_review.csv` with
   `review_checklist.md`. Fix what the config can fix: `hardcoded` rows for numbers typed into the
   testimony (link them to the RDP doc or code that derives them), `known_differences` for numbers edited
   in Word after rendering (with the explanation), `resolvers` for unusual expressions. Never edit the
   document by hand.
6. **Ask, don't guess.** When a number differs from the code, a value is hardcoded with no source, or a
   run check fails, report it to the user with the evidence and ask how to record it.
7. **Deliver.** Run `just check` and `just test`, open the `.docx` to spot-check a few links, and hand
   it over with a short summary of the review items that needed a decision.

## Reuse, don't rebuild

- PDF pages and lines: `lib.sources.pagelines.read_pdf` (never a second PDF reader).
- Quote locations: `lib.sources.pagelines.cite` against the extract.
- The filed PDF: `just fetch-source <citekey>`; new sources: the `ingest-source` skill.
- Pinpoint citations inside the testimony itself are the `expert-testimony` skill's job, not this one.
