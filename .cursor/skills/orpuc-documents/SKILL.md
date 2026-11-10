---
name: orpuc-documents
description: >-
  Finds and fetches Oregon PUC (OPUC) orders and eDocket filings (testimony,
  briefs, orders, comments) from apps.puc.state.or.us and edocs.puc.state.or.us,
  as a fetch step for the discover-sources skill. Use when discover-sources (or
  the user) needs documents from the Oregon Public Utility Commission, OPUC, an
  Oregon docket number like UM 2377, UE 457 or LC 73, an Oregon order number
  like 26-154, eDockets, Oregon tariffs or advice filings (ADV dockets, "Advice
  No. 26-43"), PGE, PacifiCorp or NW Natural Oregon filings, or CUB/Staff/AWEC
  testimony in Oregon.
---

# Oregon PUC documents

Find and download Oregon Public Utility Commission orders and docket filings.
This skill is a **fetch subroutine of `discover-sources`**: use it when a
discovery run needs documents from the Oregon PUC. It downloads into the
discovery run's scratch inbox and nothing else. It does **not** ingest, and a
document it downloads is only a _candidate_: `discover-sources` de-duplicates
it, records it in `candidates.json`, and puts it in the triage table. The
user decides what is relevant, and only approved candidates go on to the
`ingest-source` skill. Never write to Zotero, DocumentCloud, Drive or the repo
from here.

Unlike Maryland (Cloudflare) and Connecticut (blocks the dev server), the
OPUC site needs **no login, no browser and no workaround**. Plain HTTP with a
browser-like User-Agent works from the dev server. The helper script does it
with the standard library.

## Before you start

1. You are normally here from step 2 or 3 of `discover-sources`, which has
   already pinned down the topic and what the sources are for. Keep that
   purpose in view: it decides which filings in a long docket are worth
   downloading.
2. Identify what you have: a **docket number** (`UM 2377`, `UE 457`, `LC 73`),
   an **order number** (`26-154`), a **FileName**
   (`um2377htb342431028.pdf`), or a topic only.
3. A topic with no docket number: web search finds the docket (searching
   "Oregon PUC UM 2377 CUB testimony" works), but never trust a search
   engine's summary of a filing. Download and read the PDF.

## Decision tree

```
Have an order number (26-154)?
├─ YES → fetch_orpuc.py order 26-154 -o DIR
│        (then ALWAYS check the docket for later orders; see "Subsequent history")
│
└─ NO → Have a docket number (UM 2377, ADV 1911)?
         ├─ YES → fetch_orpuc.py docket "UM 2377" [--match RE] [--action RE]
         │        → pick the file URL or order number
         │        → `fetch <FileName>` or `order <n>`
         │
         └─ NO → Looking for a tariff / rate schedule / advice filing?
                  ├─ YES → fetch_orpuc.py tariffs --company "<utility>" --since D
                  │        [--match "SCHEDULE 7"] → `fetch <FileName>`
                  │        (see "Tariffs and advice filings")
                  │
                  └─ NO → Know the utility and kind of docket (rate case, IRP)?
                           ├─ YES → fetch_orpuc.py dockets --category UE
                           │        --company "<utility>" [--since D]
                           └─ NO  → web search for the docket number, then as above
```

## Fetching

```bash
S=.cursor/skills/orpuc-documents/scripts/fetch_orpuc.py

# Docket number -> internal DocketID (via the site's own search form)
uv run python $S docket-id "UM 2377"                      # 24470

# Every action in the docket (date, type, description, direct file URL).
# --match is a regex on description/order number; --action on the action type.
uv run python $S docket "UM 2377" --action "ORDER"
uv run python $S docket "UM 2377" --match "Surrebuttal" --action "TESTIMONY"
uv run python $S docket "UM 2377" --since 2026-06-01 --json

# Download an order (PDF; pre-2000 orders are .htm)
uv run python $S order 26-154 -o ~/.cache/switchbox_sources/inbox/<run>

# Download one filing by FileName or URL
uv run python $S fetch um2377htb342431028.pdf -o ~/.cache/switchbox_sources/inbox/<run>
```

Download into the discovery run's inbox folder
(`~/.cache/switchbox_sources/inbox/<YYYY-MM-DD>_<topic>/`, `-o` on every
command), keeping the original file name. Every download is checked for a
`%PDF` header and size over 1 KB; an HTML error page that comes back with HTTP
200 is reported, not saved as a PDF.

**What to download.** A docket can have hundreds of actions, most of them
motions, notices and signatory pages. Use `docket --action` and `--match` to
narrow to what the purpose needs (usually `ORDER`, `TESTIMONY`, `BRIEF`) and
download only those; list the rest in the triage notes as seen but not taken.

**What goes in `candidates.json`.** Only facts seen on the document or the
docket page: `issuer` (the witness's party, or the Commission), `date` (the
action date, or an order's "ENTERED" date), `docket` (`UM 2377`),
`source_url` (the direct `edocs.puc.state.or.us` or `orders` URL that
`docket` prints), and `why_relevant`. Leave `doi` null. For a docket, one
candidate per file; do not merge a witness's exhibits.

**Reading before recommending.** Triage needs a judgment about relevance, so
read enough of each candidate to say what it contains (the order's issue list
and resolutions; a testimony's exhibit list). The "Reading PDFs" notes under
Pitfalls apply.

## Tariffs and advice filings

Oregon utilities change rates and tariff schedules by **advice filing**. Each
one is its own docket with prefix **ADV** (`ADV 1911`), carries the utility's
own advice number (`26-43`, "PGE Advice No. 26-43"), and sometimes also a
rate-case docket number (`UE 475`). The filing PDF is the advice letter plus
the revised tariff sheets (PGE 26-36 is 5 pages); work papers are often
"provided through the OPUC Huddle Portal" and are not public.

```bash
uv run python $S company "portland general"            # 32  PORTLAND GENERAL ELECTRIC
uv run python $S tariffs --company "portland general" --since 2025-01-01
uv run python $S tariffs --company "portland general" --match "SCHEDULE 7\b|RESIDENTIAL"
uv run python $S tariffs --company "pacific power" --pending --since 2026-01-01 --json
uv run python $S fetch uaa349185029.pdf -o <inbox>     # an advice filing PDF
uv run python $S docket "ADV 1911"                     # that filing's docket
```

Each result gives filed date, advice number, `ADV` docket, status (Pending,
Allowed, No action needed), effective date, title (which usually
names the schedule) and the direct PDF URL. Match on schedule names and numbers
in the title; the advice-number box on the site's own search page returned no
records for any format tried, so list by company and date instead.

- A **rate case** (UE for electric, UG for gas) has its own docket and tariff
  sheets in the compliance filings; find it with
  `dockets --category UE --company "<utility>"`.
- The advice filing shows the _change_ and the sheets filed; the full current
  tariff book is on the utility's own website. If the purpose needs the whole
  schedule, say so in the triage notes.
- `--since`/`--until` take `YYYY-MM-DD` and filter on the filed date.

## Subsequent history: always check

An order is rarely the last word. After fetching an order, run
`docket "<docket>" --since <order date>` and read the later `ORDER`,
`RECONSIDERATION` and `APPEAL` actions before characterizing the decision.
Example: Order 26-154 (UM 2377, May 7, 2026) was followed by Order 26-239
(compliance, July 10), Order 26-309 (rehearing and reconsideration granted in
part and denied in part, Aug. 31) and AWEC's petition for judicial review in
the Court of Appeals (Sept. 10). Read the reconsideration order for the
issue you rely on (26-309 left the Peak Growth Modifier and the RAP-study
directive in place), and say "subject to a pending petition for judicial
review" where that is so. Cite the docket, not a search summary, for status.

## Court of Appeals and other courts

Judicial review of OPUC orders (e.g. AWEC's petition on Order 26-309, listed
as an `APPEAL` action on UM 2377) happens in the Oregon Court of Appeals, whose
filings are **not** on the OPUC site and are not covered by this skill. If an
agent needs them, figure out how to get them (start from the appeal number on
the docket's `APPEAL` action), then **add that method to this skill** with a
tested script path and the pitfalls you hit.

## Pitfalls

- **Order search returns the wrong PDF.** `srchlist.asp?OrderNumber=26-154`
  returns the _docket_, whose `[PDF]` link is the docket's latest filing, not
  the order. Use `orders.asp?OrderNumber=` (the script's `order`), which
  redirects to `/orders/<year>ords/<number>.pdf`.
- **Docket number is not the DocketID.** The docket page URL uses an internal
  number (`DocketID=24470` for UM 2377). The script's `docket-id` finds it
  through the search form; the `Prefix` value must be four characters wide
  (`'UM  '`). Do not use the `DocketNoLayout.asp` URL that web search surfaces
  unless you already have the ID.
- **Link and description are on different table rows.** On the docket page
  the file link sits in the date row, above its description row. Hand-parsing
  by `<tr>` pairs links with the wrong filing; the script splits on the date
  marker.
- **Testimony is bundled by witness.** One PDF holds a witness's whole set
  (`CUB/300-311` is one 73-page file). The exhibit list at the front says what
  each exhibit is.
- **Company names are matched against a fixed list.** `--company` takes an
  id or part of a name and must match exactly one entry (`company <name>`
  lists matches); PGE is 32, Pacific Power 33, Idaho Power 31, NW Natural 417, Avista 49,
  Cascade Natural Gas 50.
- **Duplicate rows.** The same advice number can appear twice, once under an
  `ADV` docket and once under a rate-case docket (26-37 is `ADV 1900` and
  `UE 475`, each with its own PDF). Fetch the one whose docket the purpose
  needs, or both if unsure.
- **PacifiCorp is listed as "PACIFIC POWER" (id 33).** Search `company pacific`.
  Company names in the list are the OPUC's, not the common names.
- **Old dockets have almost no files.** 1990s dockets (e.g. UM 827) list
  filings as text only; the only downloadable items are the orders.
- **Confidential filings are not public.** The docket says "Confidential
  saved to Agency folder"; the PUBLIC or REDACTED version is what you get.
- **Reading PDFs.** `pypdf` and `pdfplumber` are in the reports2 environment
  (no `pdftotext` or PyMuPDF). `pypdf` takes about a minute on a 77-page
  order. The text layer has OCR errors (`A WEC` for AWEC, `I 00 MW`); check
  quoted words against the page image before quoting.
- **Pagination for citations.** For orders the printed page equals the PDF
  page and there are no line numbers, so cite `Order No. 26-154 at 34`. For
  testimony the cite is exhibit, witness and page (`CUB/300, Jenks/15`), and
  that page is _not_ the PDF page (Jenks/15 is PDF p. 17). Cite the printed
  exhibit page.

## Notes for the later ingest

These matter only after the user approves a candidate; `ingest-source` owns
them. Recorded here so the facts are captured at discovery time.

- **File names** at ingest: `orpuc_<docket without space>_<slug>` with the
  order or exhibit number in the slug, e.g. `orpuc_um2377_order_26_154`,
  `orpuc_um2377_cub300_jenks_surrebuttal`.
- **Titles and keys** follow `context/code/source_metadata_conventions.md`:
  `Docket UM 2377: Order No. 26-154`, author "Public Utility Commission of
  Oregon" for orders; for testimony the author is the witness, on behalf of
  the party.
- **Order captions** repeat the docket caption, e.g. "Investigation into
  Marginal Cost Study Treatment of Costs for Large Customers and Further
  Modifications to Portland General Electric Company's Rule C and Rule I."
- **Date an order by its "ENTERED" date** (May 7, 2026 for 26-154), not the
  commissioners' meeting date.

## Worked examples

| Document                                               | Fetch                          | Result                                                                          |
| ------------------------------------------------------ | ------------------------------ | ------------------------------------------------------------------------------- |
| Order No. 26-154 (UM 2377, large-load cost allocation) | `order 26-154`                 | 77 pp, 34.6 MB; Issue 17 directs a study of the RAP Manual's allocation methods |
| Order No. 26-309 (reconsideration)                     | `order 26-309`                 | 35 pp; PGM and Issue 17 undisturbed                                             |
| CUB surrebuttal, Jenks, CUB/300-311                    | `fetch um2377htb342431028.pdf` | 73 pp; cites the RAP Manual at Jenks/15-16                                      |
| Order No. 98-374 (UM 827, marginal cost methods)       | `order 98-374`                 | `.htm`, 47 KB                                                                   |

## Additional resources

- [reference.md](reference.md): URL patterns, redirects, the FileType codes,
  and how the docket page is laid out.
- `scripts/fetch_orpuc.py`: the tested helper above.
- `.cursor/skills/discover-sources/SKILL.md`: the parent workflow (purpose,
  inbox, `candidates.json`, de-duplication, triage table).
- `.cursor/skills/ingest-source/SKILL.md`: only for candidates the user approves.
