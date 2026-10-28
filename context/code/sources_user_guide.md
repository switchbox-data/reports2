# Source library: user guide

How to get a document into Switchbox's source library, and what happens when you do. For the design and failure handling, see `sources_architecture.md`; for how items are named, see `source_metadata_conventions.md`.

## What the library gives you

Every source (a commission order, testimony, a study, a paper, a workpaper workbook, a web page) ends up as:

- **A Zotero item** in the Switchbox group library, with the original file attached. This is the record that `reports/references.yaml` is built from, and where the original PDF lives.
- **A public copy** readers can open: DocumentCloud for PDFs, Google Drive for workbooks, the live page plus a Wayback Machine capture for web pages. Papers with a DOI link to the DOI instead.
- **A short link**, `https://pub.switch.box/<citation_key>`, that forwards to the public copy. This is the link in citations, so it never changes even if the copy moves.
- **A markdown extract** in `context/sources/<project>/` that agents read as context (PDFs and web pages; workbooks get a short stub), with a row in the index of `context/README.md`.

## One-time setup

1. `just install` (it also installs the Playwright browser used to capture web pages).
2. Put the credentials in `reports2/.env` (gitignored): `ZOTERO_API_KEY` (create it at [zotero.org/settings/keys](https://www.zotero.org/settings/keys) with **write and file access** to the group library) and `ZOTERO_GROUP_ID`; `DOCUMENTCLOUD_USERNAME` and `DOCUMENTCLOUD_PASSWORD`; `GDRIVE_SERVICE_ACCOUNT_JSON` (path to the service account key file) and `GDRIVE_PUBLIC_FOLDER_ID`; `IA_ACCESS_KEY` and `IA_SECRET_KEY` (optional; the Wayback Machine works anonymously but with lower limits); `SOURCES_CONTACT_EMAIL` (your email, used for polite access to Crossref and Unpaywall).
3. `just sources-doctor`. Every line should be green; each red or yellow line says how to fix it. You need push access to `switchbox-data/pub` (the short-link repo); doctor checks it.

## Adding a source

Ask the agent in Cursor: "ingest this PDF" (attach the file or give a URL), or save the item in Zotero's **Inbox** collection (with Zotero's browser connector, which attaches the PDF) and say "ingest my pending sources".

1. The agent reads the document, looks up the organization's existing name, checks the library for a duplicate, and drafts a **details card**.
2. It shows you the card in plain words: title, authors, citation key, project, item type, date, DOI, where the public copy will live, the short link, and the index row. **Read it; this is the only checkpoint.** Tell the agent what to change.
3. When you approve, the agent runs `just sources-ingest <card>`. This writes everything and prints one JSON line per document. If something fails (a network error, a service down), run the same command again; it picks up where it stopped and never makes duplicates.
4. The agent extracts PDFs to markdown, validates the extract, and runs `just sources-status <citation_key>`, which must be all green. Ingest marks the Zotero item with the `processed` tag only at the end.
5. Commit the extract, the index rows and (if a report cites it) `reports/references.yaml` after `just sync-bib`.

Several documents at once work the same way: one card each, one command, one push to the short-link repo.

## Items you saved by hand

At the start of each Cursor session you may see "N sources saved in Zotero are waiting to be ingested." `just sources-pending` lists them. Say "ingest them" and the agent drafts a card for each, using the item you saved (`just sources-ingest-item <card> <zotero_item_key>` adopts it instead of creating a new one). Only items added since the pipeline went live are listed.

## Finding sources

Ask for it: "find sources on seasonal heat pump rates for the ma_hp_rates project." The `discover-sources` skill searches, downloads to `~/.cache/switchbox_sources/inbox/<date>_<topic>/`, checks each file against the library, and gives you a table of candidates to keep or skip. Nothing is added to Zotero until you approve ingest for a candidate.

## Getting a PDF back

PDFs are not stored in git. `just fetch-source <citation_key>` downloads the original from Zotero next to its extract and prints the path (the file is gitignored).

## Checking and cleaning up

| Task                                        | Command                                                                  |
| ------------------------------------------- | ------------------------------------------------------------------------ |
| Is everything in place for a source?        | `just sources-status <citation_key> [...]`                               |
| Is this file or URL already in the library? | `just sources-dedupe --path-file x.pdf` (or `--url`, `--doi`, `--title`) |
| What is this organization already called?   | `just sources-org "Massachusetts DPU"`                                   |
| Check credentials, access and tools         | `just sources-doctor`                                                    |
| What is waiting to be ingested?             | `just sources-pending`                                                   |

## When something goes wrong

- **A step says `failed`.** Read its message, fix the cause, run the same ingest command again. Nothing needs undoing.
- **"possible duplicate".** The library already has something that matches. Use the existing key, or re-run with `--force` only if it is truly a different document.
- **DocumentCloud takes a long time.** Large PDFs are processed after upload; ingest waits, and a re-run resumes the wait.
- **The short link gives "not found".** GitHub Pages updates a minute or two after the push. If it persists, `just sources-status <citation_key>` shows whether the link was recorded.
- **A bad write to Zotero.** Every write is logged in `~/.cache/switchbox_sources/logs/zotero_writes.jsonl` with the previous value, so an agent can restore it.
- **Web page capture is blocked.** Some sites refuse automated capture and the Wayback Machine; ingest reports the site as blocked. Save the page as a PDF by hand and ingest that file instead.
