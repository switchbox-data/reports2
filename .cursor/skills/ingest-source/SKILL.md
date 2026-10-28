---
name: ingest-source
description: >-
  Bring a source (PDF, workbook, web page) into the Switchbox source library:
  draft the Zotero details card, get it approved, then run ingest so the item,
  file, public copy, short link, extract and index rows all exist. Use when the
  user adds, saves, ingests or extracts a source, says "pending sources", names a
  Zotero item to process, or the session-start reminder lists sources waiting.
---

# Ingest a source

**The agent decides; the CLI does.** You gather facts and draft a details card (YAML). The user approves it. `just sources-ingest` then performs every write (Zotero, DocumentCloud or Google Drive, short link, extract front matter, index rows) and can be re-run safely after any failure. Never write to Zotero, DocumentCloud, Drive or the `pub` repo any other way.

Read `context/code/source_metadata_conventions.md` before drafting (names, titles, item types, dates, keys) and `context/code/sources_user_guide.md` if the user asks how the pipeline works. If a command fails with a credentials error, run `just sources-doctor` and relay its fix hints.

## Steps

1. **Find the source.**
   - A file or URL from the user: use it. Check `just sources-dedupe --path-file <file>` (or `--url`, `--doi`, `--title`) first. If it is already in the repo or Zotero, say so and stop unless the user wants a new version.
   - "What's pending?" or a session-start reminder: `just sources-pending` lists Zotero items saved but not ingested. Each lists its Zotero item key, which ingest adopts with `--zotero-item` (the file you saved is already attached to it). Download that file from Zotero for reading, if you need it, with the item's attachment. A row whose reason is "file with no item" is a file dragged into Zotero that never got an item: draft the card from the file as usual and pass the file's key to `--zotero-item`; ingest creates the item and moves the file under it.
2. **Read enough of the source** to fill the card: issuer, title, date, docket (utility proceedings), pages, DOI if it has one. Use `uv run python -m lib.sources.cli find-doi --path-file <pdf>` for papers; only a DOI found on the document's own front pages, metadata or landing page counts, never one from a reference list.
3. **Organizations.** For every organization author or publisher run `just sources-org "<name as printed>"`. Use the existing full name and short form it returns. Only when it returns nothing, propose a new one following the conventions doc, set `new_organization: true`, and give the evidence in `abbreviation_source`. For every person author run `just sources-person "<Family, Given as printed>"`. If it lists spellings and the document confirms the same person (same organization or field), use the fullest spelling the document supports and say so when presenting the card; otherwise enter the name as printed. Never merge on family name alone.
4. **Project.** `uv run python -m lib.sources.cli projects` lists projects (report folders, Zotero collections, source folders). Pick one or more. A project that does not exist yet needs `new_project: true` and the user's confirmation. Sources that serve no single report (textbooks, manuals) go in the `general_reference` project.
5. **Item type** per the conventions doc: utility-commission documents are `document`; studies and MCOS are `report`; workpaper workbooks are `dataset`; papers are `journalArticle` or `preprint`; web pages are `webpage` (with `access_date`).
6. **Draft the card.** Write it to `/tmp/<citekey-or-slug>.yaml` (not into the repo). Fields:

   ```yaml
   item_type: document # one of: document, report, dataset, webpage, journalArticle, preprint, book, thesis,
   #   conferencePaper, presentation, blogPost, magazineArticle, newspaperArticle, hearing
   title: "Docket 25-55: Order on Seasonal Heat Pump Rates"
   creators:
     - name: Massachusetts Department of Public Utilities
   abbreviation: MA DPU
   date: "2025-06-01"
   docket: "25-55"
   projects: [ma_hp_rates]
   source_file: order.pdf
   source_url: https://example.org/files/order.pdf
   extract_path: context/sources/ma_hp_rates/madpu_25-55_order.md
   index_row: One sentence: what it is and when to read it.
   front_matter: { docket: "25-55", pages_total: 12, extraction_scope: full }
   citekey: placeholder
   ```

   Then `uv run python -m lib.sources.cli key /tmp/<card>.yaml` prints the citation key the rule gives; put it in `citekey`. `uv run python -m lib.sources.cli check-card /tmp/<card>.yaml` validates the card (titles, keys, organizations, duplicates) with no writes; fix everything it lists. A PDF with a DOI is not uploaded to DocumentCloud; override with `upload_documentcloud` only when the user asks. Workbooks that exceed the 600 KB file limit need `workbook_in_repo: false`.
7. **Show the card and wait for approval.** Present, in plain words: the Zotero title and creators, the citation key, the project(s), the item type (and that the user can pick another from the list in the card template) and date, the DOI (and where you found it), how the file will be shared (DocumentCloud, Drive, or a Wayback snapshot for web pages), the short link it will get, and the index row. List anything you were unsure about. **Do not ingest until the user approves.** Apply their corrections to the YAML.
8. **Ingest.** `just sources-ingest /tmp/<card>.yaml --path-source <file>`; for a Zotero Inbox item `just sources-ingest-item /tmp/<card>.yaml <ZOTERO_ITEM_KEY>`. For a web page, the CLI captures it (PDF and HTML) and saves it to the Wayback Machine. The command prints one JSON object per document. If it reports a problem, fix the cause and run the same command again; do not work around it by hand.
9. **Extract.** Only PDFs need this step: ingest writes web-page extracts from the captured HTML, and workbooks are not extracted (markdown would lose their formulas and structure; ingest writes a short stub `.md` next to them, and an agent that needs the numbers opens the workbook itself with polars for values or openpyxl for formulas).
   - **Delegate, one subagent per PDF.** By default, launch one subagent per PDF with the Task tool on the latest Sonnet model available (for example `claude-sonnet-5-5-high`), all in a single message so they run in parallel. Never split one PDF across agents. Delegate even a single PDF, which keeps the main context small. Extraction is mechanical transcription, where Sonnet is faster and cheaper; this split is a starting point, not a benchmarked result. If subagents are unavailable, extract the PDFs yourself, one after another.
   - **Make each prompt self-contained**, since subagents see none of this chat: the repo path (the user's checkout, where the extract must be written), the citekey, the exact `extract_path` from the card, and the local PDF path (the file you passed to ingest, or the path `just fetch-source <citekey>` prints). Tell it to follow `.cursor/commands/extract-pdf-to-markdown.md` exactly; not to run ingest, touch Zotero or commit; and to return the path it wrote, the page count, and any pages it had trouble with.
   - **Validate and finish each one yourself** as its subagent returns: run `/validate-pdf-to-markdown-extraction` on the extract, fix what it lists or ask the user, then run the same ingest command again for that document. The first run left the front matter step pending until the extract existed; the rerun writes it, adds the index row and tags the item `processed`.
10. **Verify.** `just sources-status <citekey>` must be all green. Ingest tags the Zotero item `processed` only after its own verification passes.
11. **Refresh the bibliography:** `just sync-bib`, so `references.yaml` matches Zotero. Then tell the user which files changed (the extract or stub, any workbook copy, the index rows, `references.yaml`) so they can commit them. **Never commit or push yourself**; the user always commits. Originals (PDFs) are gitignored and never committed.

## Rules

- The user approves the card before any write. Corrections after approval mean a new approval.
- Never invent a short form, DOI, docket number or date. Leave a field out and say it is missing.
- Never edit `reports/references.yaml` by hand and never create Zotero items with the Zotero tools directly.
- One citation key per document. If dedupe finds a match, reuse it.
- Drive uploads run as the signed-in user via the cached Google login. If ingest reports no cached Google login or an expired one, tell the user to run `just google-login` themselves (it needs a browser); never try to log in from the agent.
- Several documents at once: draft the cards yourself, one at a time, so keys and organization spellings stay consistent, and have the user approve them together. Pass all of them to a single `just sources-ingest` so the short links go out in one push. Only extraction runs in parallel (step 9).
- Recommend running the main session on Opus: drafting cards and validating extracts are judgment calls that get locked into Zotero and citations.
