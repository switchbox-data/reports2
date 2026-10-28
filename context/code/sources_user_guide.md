# Source library: user guide

How to get a document into Switchbox's source library, and what happens when you do. For the design and failure handling, see `sources_architecture.md`; for how items are named, see `source_metadata_conventions.md`.

## What the library gives you

Every source (a commission order, testimony, a study, a paper, a workpaper workbook, a web page) ends up as:

- **A Zotero item** in the Switchbox group library, with the original file attached (the `.pdf`, the `.xlsx`, a `.pdf` snapshot of a web page, and so on). Zotero is the source of truth for all of our source files and their metadata. `reports/references.yaml` is a one-to-one export of Zotero's metadata that makes it easy to cite Zotero items from Quarto reports.
- **A public copy** readers can open: DocumentCloud for PDFs, Google Drive for workbooks, the live page plus a Wayback Machine capture for web pages. Papers with a DOI link to the DOI instead.
- **A short link**, `https://pub.switch.box/<citation_key>`, that forwards to the public copy. This is the link in citations, so it never changes even if the copy moves.
- **A markdown extract** in `context/sources/<project>/` that agents read as context (PDFs and web pages; workbooks get a short stub instead), listed in the sources index in `context/README.md`.

In other words, every source ends up:

1. properly captured and documented in Zotero for Switchboxers to use, in a form Quarto can pull from for citations in our reports;
2. in a user-friendly public web version, with a short link, for people outside Switchbox; and
3. as a lightweight markdown file (for PDFs and web pages) for agents to read. When an agent needs to see something the markdown can't show, like a chart, it pulls the original from Zotero.

## One-time setup

1. `just install` (it also installs the Chromium browser used to capture web pages).
2. Put the credentials in `reports2/.env` (gitignored). The shared ones are in the team password manager.
   - **Zotero:** `ZOTERO_API_KEY` (create it at [zotero.org/settings/keys](https://www.zotero.org/settings/keys) with **write and file access** to the group library) and `ZOTERO_GROUP_ID`.
   - **DocumentCloud:** `DOCUMENTCLOUD_USERNAME` and `DOCUMENTCLOUD_PASSWORD` (the pipeline account).
   - **Google Drive:** the Google OAuth app variables `G_CLIENT_ID`, `G_CLIENT_SECRET`, `G_PROJECT_ID`, `G_AUTH_URI` and `G_TOKEN_URI` (the same ones `lib/data/gsheets.py` uses), and `GDRIVE_PUBLIC_FOLDER_ID` (the ID of the public folder in the shared drive).
   - **Wayback Machine:** `IA_ACCESS_KEY` and `IA_SECRET_KEY` (optional; without them, captures use a slower anonymous route).
   - **Contact email:** `SOURCES_CONTACT_EMAIL` (your email, used for polite access to Crossref and Unpaywall when looking up DOIs).
3. `just google-login` once. It opens a browser to sign in with your Switchbox Google account and caches the token at `~/.config/gspread/authorized_user_reports2.json`; the Sheets helpers share it. On a machine without a browser (EC2), run it on your laptop and copy that file to the same path on the machine.
4. `just sources-doctor`. Every line should be green; each red or yellow line says how to fix it. You need push access to `switchbox-data/pub` (the short-link repo); doctor checks it.

**About the Google Drive copy.** Workbooks are uploaded as you: ingest uses your own Google login, not a shared key. They land in a folder in a Google shared drive, so Switchbox, not you, owns the files and they stay if you leave. Two things must be true: your Google account is a member of that shared drive, and the Workspace admin allows "anyone with the link" sharing for it (otherwise the public link asks for a sign-in, and `just sources-doctor` or the first upload will say so). If the OAuth consent screen is set to External with publishing status Testing, your cached login expires every 7 days and you must run `just google-login` again; an Internal app avoids this.

## Finding sources

There are two ways to find new sources: let an agent search for them, or find them yourself.

### Let an agent find them

Ask in Cursor, for example:

- "Find sources on seasonal heat pump rates for the ma_hp_rates project."
- "Find PURA's final decision in the Eversource rate case and any related compliance filings."

The `discover-sources` skill searches the web, downloads candidates to a scratch folder on your machine (`~/.cache/switchbox_sources/inbox/<date>_<topic>/`, never the repo), checks each one against the library, and shows you a table: what each document is, its length, whether we already have it, and a recommendation. Nothing goes into Zotero until you pick which ones to ingest (see "Adding a source").

### Find them yourself

- **On the web:** in the Zotero app, select the project's collection (for example `Reports > ma_hp_rates`), or the top-level **Inbox** if you're not sure where it belongs, then click the Zotero browser button. It saves the details and the PDF, including paywalled PDFs you can open.
- **A file you already have:** drag it into that Zotero collection or the Inbox, or just keep it on your machine and hand it to the agent (next section).

Items you save in Zotero this way aren't citable yet: they have no locked citation key, so `just sync-bib` leaves them out of `references.yaml`. When you next start a chat in Cursor, the agent tells you they're waiting, with an opening line like:

> 2 sources in Zotero are waiting for ingest: Eversource Connecticut 2026; U.S. Energy Information Administration 2018. Want me to process them?

Say "yes", or "not now" (it asks again next chat). Only items added since the pipeline went live are listed. `just sources-pending` shows the same list.

## Adding a source

How you start depends on where the source is:

- **You have the file or URL** (on your machine, or from an agent's search): attach the file or paste the URL and say "ingest this". For search results, say "ingest 1 and 3".
- **You saved it in Zotero** (the browser button, or dragged in): say "ingest my pending sources". The agent works from the item you saved, keeping its file, rather than creating a new one.

Either way, the agent then does the following.

1. **Reads the document and drafts a details card.**
   - **Authors.** For each author, it decides from the document (cover page, letterhead, "prepared by" line) whether it's a person or an organization. For a consultant's report, the consultant is the author and the client goes in as the institution.
   - **Organizations** are looked up in the library (in `references.yaml` and Zotero), by full name and by abbreviation, so the same agency never ends up with two spellings. If it finds a match, it reuses that exact full name and abbreviation. If not, it proposes a new name and abbreviation following the conventions doc, and flags it **NEW ORGANIZATION** on the card with where the abbreviation came from. Check that line carefully: once approved, it shows up in every citation of that organization.
   - **People** are entered as printed (family name, given name). There is no library lookup for people.
   - **Duplicates.** It checks the library for the same file, URL, DOI or title, and stops if the source is already there.
2. **Shows you the card** in plain words: title, authors, citation key, project, item type, date, DOI, where the public copy will live, the short link, and the index row. **Read it; this is the only checkpoint.** Tell the agent what to change.
3. **Runs ingest** (`just sources-ingest <card>`) when you approve. For every source, it creates the Zotero item (or updates the one you saved) with the card's details and a locked citation key, attaches the original file, files it in the project's collection (and out of the Inbox), sets the item's link to the citation link, and adds the short link. Then, by type:
   - **PDF:** uploads a public copy to DocumentCloud, and the short link points to it. A paper with a DOI skips DocumentCloud, and its citation links to the DOI.
   - **Web page:** captures the page in Chromium as a PDF snapshot plus its HTML (both attached in Zotero), saves it to the Wayback Machine, writes the markdown extract from the captured HTML, and points the short link at the live page. If the page later disappears, the short link can be repointed to the Wayback copy.
   - **Excel workbook:** uploads it to the shared Google Drive folder with "anyone with the link" access, and the short link points there. It copies the workbook into the repo if it's under the 600 KB limit (bigger ones only if you said so on the card), and writes a stub `.md` next to it saying what each sheet holds.

   It prints one line per document. If something fails (a network error, a service down), the same command can be rerun: it picks up where it stopped and never makes duplicates.
4. **Extracts PDFs** to markdown, validates the extract against the PDF, and reruns ingest, which writes the extract's front matter and adds the sources index row. Ingest then checks everything and tags the Zotero item **`processed`**. The tag means all of this is true:
   - the Zotero item has its locked citation key, sits in its project collection (not the Inbox), and has the original file attached;
   - the public copy exists and the short link forwards to it (or, for a DOI paper, the item links to the DOI);
   - for PDFs and web pages, the markdown extract is in the repo with front matter pointing back to the Zotero item (for workbooks, the stub and, if small enough, the workbook itself);
   - the source has its row in the sources index.

   `just sources-status <citation_key>` shows the same checklist.
5. **Refreshes the bibliography** with `just sync-bib` and lists the changed files for you to commit. The agent never commits. Commit:
   - the extract (or the workbook stub, and the workbook if it was copied in);
   - the index rows: `context/README.md` is the table of contents agents read to find sources, and each source gets one row there (its path and a sentence on what it is and when to read it); a folder with its own `README.md` gets a row in that README's file table too;
   - `reports/references.yaml`, always, since it's a one-to-one copy of Zotero and should stay current.

Several documents at once work the same way: one card each, approved together, one command, one push to the short-link repo.

You can also run ingest yourself (`just sources-ingest <card> --path-source <file>`, or `just sources-ingest-item <card> <zotero_item_key>` for a saved item), but the agent writes the card and checks it against the conventions for you, so let it.

## Getting an original file back

Original files are not stored in git. `just fetch-source <citation_key>` downloads the original from Zotero, whatever its type (PDF, workbook, web-page snapshot), and prints the path. It goes next to the extract when git ignores files there (PDFs, for example); anything git would track, like a workbook too big for the repo, goes to `~/.cache/switchbox_sources/fetched/<citation_key>/` instead, so it can't be committed by accident.

## Checking and cleaning up

| Task                                                                | Command                                                                  |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Is everything in place for a source?                                | `just sources-status <citation_key> [...]`                               |
| Is this source already in the library?                              | `just sources-dedupe --path-file x.pdf` (or `--url`, `--doi`, `--title`) |
| Is this a known organization, and what's its name and abbreviation? | `just sources-org "Massachusetts DPU"`                                   |
| Check credentials, access and tools                                 | `just sources-doctor`                                                    |
| What is waiting to be ingested?                                     | `just sources-pending`                                                   |

## When something goes wrong

- **A step says `failed`.** Read its message, fix the cause, run the same ingest command again. Nothing needs undoing.
- **"possible duplicate".** The library already has something that matches. Use the existing key, or re-run with `--force` only if it is truly a different document.
- **DocumentCloud takes a long time.** Large PDFs are processed after upload; ingest waits, and a re-run resumes the wait.
- **The short link gives "not found".** GitHub Pages updates a minute or two after the push. If it persists, `just sources-status <citation_key>` shows whether the link was recorded.
- **A bad write to Zotero.** Every write is logged in `~/.cache/switchbox_sources/logs/zotero_writes.jsonl` with the previous value, so an agent can restore it.
- **Web page capture is blocked.** Some sites refuse automated capture and the Wayback Machine; ingest reports the site as blocked. Save the page as a PDF by hand and ingest that file instead.
