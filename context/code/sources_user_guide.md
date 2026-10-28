# Source library: user guide

How to get a document into Switchbox's source library, and what happens when you do. For the design and failure handling, see [`sources_architecture.md`](sources_architecture.md); for how items are named, typed and dated, see [`source_metadata_conventions.md`](source_metadata_conventions.md).

## What the library gives you

Every source (a commission order, testimony, a study, a paper, a workpaper workbook, a web page) ends up as:

- **A Zotero item** in the Switchbox group library, with the original file attached (the `.pdf`, the `.xlsx`, a `.pdf` snapshot of a web page, and so on). Zotero is the source of truth for all of our source files and their metadata. `reports/references.yaml` is a one-to-one export of Zotero's metadata that makes it easy to cite Zotero items from Quarto reports.
- **A public copy** readers can open: DocumentCloud for PDFs, Google Drive for workbooks, a Wayback Machine snapshot for web pages. Sources with a DOI link to the DOI instead.
- **A short link**, `https://pub.switch.box/<citation_key>`, that forwards to the public copy. This is the link in citations, so it never changes even if the copy moves.
- **A markdown extract** in `context/sources/<project>/` that agents read as context (PDFs and web pages; workbooks get a short stub instead), listed in the sources index in `context/README.md`.

In other words, every source ends up:

1. properly captured and documented in Zotero for Switchboxers to use, in a form Quarto can pull from for citations in our reports;
2. in a user-friendly public web version, with a short link, for people outside Switchbox; and
3. as a lightweight markdown file (for PDFs and web pages) for agents to read. When an agent needs to see something the markdown can't show, like a chart, it pulls the original from Zotero.

## One-time setup

1. `just install` (it also installs the Chromium browser used to capture web pages).
2. Put the credentials in `reports2/.env` (gitignored). They have most likely been created already: ask a teammate for the values rather than making new ones.
   - **Zotero:** `ZOTERO_API_KEY` (a key with **write and file access** to the group library; a new one can be made at [zotero.org/settings/keys](https://www.zotero.org/settings/keys)) and `ZOTERO_GROUP_ID`.
   - **DocumentCloud:** `DOCUMENTCLOUD_USERNAME` and `DOCUMENTCLOUD_PASSWORD` (the pipeline account).
   - **Google Drive:** the Google OAuth app variables `G_CLIENT_ID`, `G_CLIENT_SECRET`, `G_PROJECT_ID`, `G_AUTH_URI` and `G_TOKEN_URI` (the same ones `lib/data/gsheets.py` uses), and `GDRIVE_PUBLIC_FOLDER_ID` (the ID of the public folder in the shared drive).
   - **Wayback Machine:** `IA_ACCESS_KEY` and `IA_SECRET_KEY` (optional; without them, captures use a slower anonymous route).
   - **Contact email:** `SOURCES_CONTACT_EMAIL` (your email, used for polite access to Crossref and Unpaywall when looking up DOIs).
3. `just google-login` once. It opens a browser to sign in with your Switchbox Google account and caches the token at `~/.config/gspread/authorized_user_reports2.json`; the Sheets helpers share it. On a machine without a browser (EC2), run it on your laptop and copy that file to the same path on the machine.
4. `just sources-doctor`. Every line should be green; each red or yellow line says how to fix it. You need push access to [`switchbox-data/pub`](https://github.com/switchbox-data/pub) (the short-link repo); doctor checks it.

**About the Google Drive copy.** Workbooks are uploaded as you: ingest uses your own Google login, not a shared key. They land in a folder in a Google shared drive, so Switchbox, not you, owns the files and they stay if you leave. Two things must be true: your Google account is a member of that shared drive, and the Workspace admin allows "anyone with the link" sharing for it (otherwise the public link asks for a sign-in, and `just sources-doctor` or the first upload will say so). If the OAuth consent screen is set to External with publishing status Testing, your cached login expires every 7 days and you must run `just google-login` again; an Internal app avoids this.

## Finding sources

There are three ways to find new sources.

### 1. Have an agent find them

Ask in Cursor, for example:

- "Find sources on seasonal heat pump rates for the ma_hp_rates project."
- "Find PURA's final decision in the Eversource rate case and any related compliance filings."

The `discover-sources` skill searches the web, downloads candidates to a scratch folder on your machine (`~/.cache/switchbox_sources/inbox/<date>_<topic>/`, never the repo), checks each one against the library, and replies with a table like this:

| # | Title                                                       | Issuer        | Date       | Docket | Relevance                                                          | Recommendation                                       |
| - | ----------------------------------------------------------- | ------------- | ---------- | ------ | ------------------------------------------------------------------ | ---------------------------------------------------- |
| 1 | Order on Seasonal Heat Pump Rates                           | MA DPU        | 2026-06-01 | 25-08  | Directs National Grid and Unitil to file winter transmission rates | ingest                                               |
| 2 | Compliance Filing: Residential Heat Pump Rate Design        | National Grid | 2026-06-15 | 26-71  | Rate design workbook and tariff sheets implementing the order      | ingest                                               |
| 3 | Petition for an Investigation into Seasonal Heat Pump Rates | MA DOER       | 2025-01-31 | 25-08  | The petition that opened the case                                  | already in library as `doer_Docket2508Petition_2025` |

It also lists each file's path, says what it searched, and says what it couldn't reach. Nothing goes into Zotero until you pick which ones to ingest (see "Adding a source").

### 2. Find them yourself and give them to the agent

You found the document yourself (a link someone sent, a PDF on your machine). Attach the file in Cursor or paste the URL. It goes through the same ingest as the agent's finds; the only difference is that you found it.

### 3. Find them yourself and add them to Zotero

You can also put a source straight into Zotero. There are two choices to make.

**Where it goes:**

- **The project's collection** (for example `Reports > ma_hp_rates`, or `Reports > general_reference` for sources that serve no single report). Prefer this when you know the project.
- **The top-level Inbox**, when you're not sure where it belongs.

**How it gets there:**

- **The Zotero browser button:** select the target collection in the Zotero app, then click the button on the page. It saves the PDF (including paywalled PDFs you can open) and often fills in many of the details for you, especially for academic articles, where it pulls the publisher's official metadata.
- **By hand in the Zotero app:** drag a file into the collection. A dragged-in file doesn't need an item: the agent creates one when it ingests the file.

Either way, the source is now **pending**: it's in Zotero but hasn't been through ingest, so it has no locked citation key and `just sync-bib` leaves it out of `references.yaml`. Pending means anything in the Inbox, plus anything under `Reports` that isn't tagged `processed` (for `Reports`, only items added since the pipeline went live count). Nothing else is pending: items in other top-level collections, or in no collection, are general reading, not report sources, and ingest never touches them. To make one a source, move it into the Inbox or a project collection. When you next start a chat in Cursor, the agent tells you they're waiting, with an opening line like:

> 2 sources in Zotero are waiting for ingest: Eversource Connecticut 2026; U.S. Energy Information Administration 2018. Want me to process them?

Say "yes", or "not now" (it asks again next chat). `just sources-pending` shows the same list.

## Adding a source

How you start depends on how you found the source:

- **An agent found it:** say which ones to keep, for example "ingest 1 and 3".
- **You found it and gave it to the agent:** attach the file or paste the URL and say "ingest this".
- **You added it to Zotero:** say "ingest my pending sources".

In the first two cases, no Zotero item exists until ingest creates it. In the third, the source is already in Zotero, possibly as an item with some fields filled in (a lot of them, for an article saved with the browser button), or as a bare file. The agent still reads the document itself, downloading it from Zotero rather than reading it locally, and drafts a details card that builds on, and corrects, whatever fields are already there. Ingest then updates that item instead of creating a new one.

From there, the agent does the following.

1. **Reads the document and drafts a details card.**

   The details card is the Zotero entry, filled in for you. Instead of you typing each field into Zotero, the agent reads the document and fills them in following our conventions for names, titles, item types, dates and keys. Once you approve it, its contents become the Zotero item, and through `just sync-bib`, the entry in `references.yaml` that reports cite. Here is the card for a source already in the library, the Massachusetts DPU's order in docket 25-08:

   ```yaml
   item_type: document
   title: "Docket 25-08: Order on Seasonal Heat Pump Rates"
   creators:
     - name: Massachusetts Department of Public Utilities
   abbreviation: MA DPU
   date: "2026-06-01"
   docket: "25-08"
   projects: [ma_hp_rates]
   source_file: madpu_25-08_order_seasonal_heat_pump_rates.pdf
   source_url: https://eeaonline.eea.state.ma.us/DPU/Fileroom/dockets/bynumber/25-08
   extract_path: context/sources/ma_hp_rates/madpu_25-08_order_seasonal_heat_pump_rates.md
   index_row: Massachusetts DPU order on seasonal heat pump rates (June 1, 2026); read for the winter transmission charge directive.
   citekey: madpu_Docket2508Order_2026
   ```

   Here is how it fills each part:

   - **Duplicates first.** Before drafting anything, it checks the library for the same file (by its hash), URL, DOI or title, and stops if the source is already there.
   - **Authors.** For each author, it decides from the document (cover page, letterhead, "prepared by" line) whether it's a person or an organization. For a consultant's report, the consultant is the author and the client goes in as the institution.
     - **Organizations** are looked up in the library (in `references.yaml` and Zotero), by full name and by abbreviation, so the same agency never ends up with two spellings. If it finds a match, it reuses that exact full name and abbreviation. If not, it proposes a new name and abbreviation following the conventions doc, and flags it **NEW ORGANIZATION** on the card with where the abbreviation came from. Check that line carefully: once approved, it shows up in every citation of that organization.
     - **People** are entered as printed (family name, given name). There is no library lookup for people yet.
   - **Title.** The document's own title, in title case (never all caps). Documents filed in a utility proceeding start with the docket: `Docket 25-08: Order on Seasonal Heat Pump Rates`, with the commission's own number and no "D.P.U." or "Case". See [Titles](source_metadata_conventions.md#titles).
   - **Item type.** Chosen by the kind of document: commission documents (orders, testimony, exhibits, tariffs) are `document`, studies are `report`, workbooks are `dataset`, papers are `journalArticle` or `preprint`, web pages are `webpage`. The full list is in [Item types](source_metadata_conventions.md#item-types).
   - **Date.** The date the document took its present form, as printed on it: an order's issue date, testimony's filing date, a tariff's effective date, a report's publication date. It's written `YYYY-MM-DD` when the day is printed, else `YYYY-MM` or `YYYY`, and never taken from a filename. See [Which date to use](source_metadata_conventions.md#which-date-to-use).
   - **DOI.** Only one printed on the document itself (its first pages, its metadata or its landing page), and only after Crossref confirms the DOI belongs to a document with this title. DOIs in a reference list belong to other papers and are ignored. Most regulatory documents have none.
   - **Citation key.** Built by the pipeline from the card, not by Zotero: the author's short form, the first three significant words of the title, and the year. `madpu` + `Docket2508Order` + `2026` gives `madpu_Docket2508Order_2026`. If that key is taken, it adds `a`, `b`, and so on. Once ingested, the key is locked in Zotero and never changes. See [Citation keys](source_metadata_conventions.md#citation-keys).
   - **Project.** It maps the source to an existing project. A project exists in three places with the same name: the report folder (`reports/ma_hp_rates/`), the Zotero collection (`Reports > ma_hp_rates`) and the source folder (`context/sources/ma_hp_rates/`). If none fits, it suggests a new project for you to confirm, or `general_reference` for sources that serve no single report.
   - **Short link.** Derived from the citation key: `https://pub.switch.box/madpu_Docket2508Order_2026`. Sources with a DOI don't get one; they link to `https://doi.org/<doi>`.
   - **Index row.** One sentence on what the source is and when to read it. It becomes the source's row in `context/README.md` (see step 4).

2. **Shows you the card** in plain words: title, authors, citation key, project, item type, date, DOI, where the public copy will live, the short link, and the index row. **Read it; this is the only checkpoint.** Tell the agent what to change.

   Double-check that everything follows our conventions, and in particular that the item type is right: it decides how the source is cited, and it's the easiest field to get wrong. If you're not sure what the conventions are or which item type fits, see [`source_metadata_conventions.md`](source_metadata_conventions.md).

3. **Runs ingest** (`just sources-ingest <card>`) when you approve. For every source, it:
   - creates the Zotero item (or updates the one you saved) with the card's details and the locked citation key, attaches the original file, and files it in the project's collection (and out of the Inbox);
   - creates the short link, by adding a line (`"madpu_Docket2508Order_2026": "<public copy URL>"`) to `links.json` in the [`switchbox-data/pub`](https://github.com/switchbox-data/pub) repo, which GitHub Pages serves at `pub.switch.box`;
   - puts that short link in the Zotero item's URL field, so it's the link printed in citations.

   Then, by type:

   - **PDF:** uploads a public copy to DocumentCloud, and the short link points to it.
   - **Any source with a DOI** (most often a paper, but not only): skips DocumentCloud and the short link; the Zotero item's URL is the `https://doi.org/` link, which always resolves to the publisher's copy.
   - **Web page:** captures the page in Chromium as a PDF snapshot plus its HTML (both attached in Zotero), and asks the Wayback Machine to archive a snapshot of the page, getting back the snapshot's permanent URL. The short link points to that snapshot, so readers see the page as it was when we cited it, even if it later changes or disappears. (If the site blocks the Wayback Machine, the short link points to the live page instead, and ingest says so.) It writes the markdown extract from the captured HTML.
   - **Excel workbook:** uploads it to the shared Google Drive folder with "anyone with the link" access, and the short link points there. It copies the workbook into `context/sources/<project>/` if it's under the 600 KB limit (bigger ones only if you said so on the card). Next to it, it writes a stub `.md` with the same name: a workbook can't carry front matter or be read like prose, so the stub holds the front matter that points back to Zotero, lists each sheet with its size and column headers, and is what the sources index links to. An agent that needs the numbers opens the workbook itself.

   It prints one line per document. If something fails (a network error, a service down), the same command can be rerun: it picks up where it stopped and never makes duplicates.

4. **Extracts and validates PDFs, then reruns ingest.**
   - **Extract:** the [`/extract-pdf-to-markdown`](../../.cursor/commands/extract-pdf-to-markdown.md) command turns the PDF into markdown at the card's `extract_path`, keeping headings, tables, footnotes and equations, and describing figures in words.
   - **Validate:** the [`/validate-pdf-to-markdown-extraction`](../../.cursor/commands/validate-pdf-to-markdown-extraction.md) command compares the extract with the PDF and replies with a report. It grades eleven categories (equations, citations, headings, figures, tables, footnotes, lists, formatting, front matter, back matter, other) from A (complete and accurate) to D (missing or wrong), gives an overall score (Excellent, Good, Adequate or Needs work), and ends with a short summary, for example:

     > **Overall score: Good.** All categories A or B; tables and footnotes match the source.
     >
     > **Fix manually:** Table 3's last row is missing its total. Figure 2's description omits the y-axis units.

     **This is a decision point.** Read the summary and either ask the agent to fix what it lists, or accept the extract as it is and carry on.
   - **Rerun ingest.** The first run left this step pending because the extract didn't exist yet. The rerun:
     - **Writes the extract's front matter**, the block of fields between `---` lines at the top of the file. It ties the markdown back to its source, so an agent reading the extract knows which Zotero item and public copy it came from and can fetch the original:

       ```yaml
       ---
       source_file: madpu_25-08_order_seasonal_heat_pump_rates.pdf
       citekey: madpu_Docket2508Order_2026
       zotero_item: "ABCD1234"
       public_url: https://www.documentcloud.org/documents/12345678
       short_url: https://pub.switch.box/madpu_Docket2508Order_2026
       md5: "0320b78d428b697bb4401a3ecd6234b2"
       validated: 2026-10-28
       docket: "25-08"
       ---
       ```

     - **Adds the source's index row.** `context/README.md` is the table of contents agents read to find sources. Each source gets one row there, its path and the card's sentence on what it is and when to read it:

       ```markdown
       | ma_hp_rates/madpu_25-08_order_seasonal_heat_pump_rates.md | Massachusetts DPU order on seasonal heat pump rates (June 1, 2026); read for the winter transmission charge directive. |
       ```

       A folder with its own `README.md` gets a row in that README's file table too.

   Web pages skip the extract command (ingest writes their extract from the captured HTML), and workbooks get their stub instead.

5. **Verifies everything and tags the Zotero item `processed`.** This is the final check: ingest re-reads Zotero, the public copy, the short-link repo and the repo files, and only if all of it is in place does it add the `processed` tag in Zotero, which is how the pipeline records that a source is done. The tag means all of this is true:
   - the Zotero item has its locked citation key, sits in its project collection (not the Inbox), and has the original file attached;
   - the public copy exists and the short link forwards to it (or, for a source with a DOI, the item links to the DOI);
   - for PDFs and web pages, the markdown extract is in the repo with front matter pointing back to the Zotero item (for workbooks, the stub and, if small enough, the workbook itself);
   - the source has its row in the sources index.

   `just sources-status <citation_key>` shows the same checklist.

6. **Refreshes the bibliography**, `reports/references.yaml`, with `just sync-bib`, and lists the changed files for you to commit. The agent never commits. Commit:
   - the extract, for example `context/sources/ma_hp_rates/madpu_25-08_order_seasonal_heat_pump_rates.md` (or the workbook stub, and the workbook if it was copied in);
   - the index rows in `context/README.md` (and the folder README, if any);
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
