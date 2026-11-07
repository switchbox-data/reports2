---
name: ctpura-documents
description: >-
  Finds and fetches Connecticut PURA (CT PUC) docket filings from the
  dpuc.state.ct.us Lotus Domino database (filing pages, interrogatories,
  responses, testimony), then hands them to ingest-source. Use when working
  with Connecticut PURA, CT PUC, DPUC, dockcurr.nsf, a CT docket number like
  26-05-10, Eversource/CL&P or UI rate case discovery, or
  context/sources/ct_hp_rates/.
---

# Connecticut PURA documents

Find and download Connecticut Public Utilities Regulatory Authority filings
for the `context/sources/ct_hp_rates/` corpus. This skill covers **fetching
only**. Every source then enters the library through the **`ingest-source`
skill** (card, approval, `just sources-ingest`, extract, validate), which owns
Zotero, the public copy, the short link, the front matter and the index rows.

## Before you start

1. Identify what you have: a **filing page URL** (`…?OpenDocument`), a direct
   **attachment URL** (`…/$FILE/<name>.pdf`), or just a **docket number**
   (`YY-MM-NN`, e.g. `26-05-10`).
2. Check for duplicates before downloading anything:
   `rg -n "<docket or set name>" context/README.md context/sources/ct_hp_rates/`,
   then `just sources-dedupe` on the PDF (see `ingest-source`). Earlier sets in
   the same docket give the naming and citation-key precedent.
3. The PURA site is outside the sandbox allowlist: run fetch commands with
   `required_permissions: ["full_network"]`.

## The `$FILE` pitfall

Attachment URLs contain `$FILE`, and docket views contain `$Form…View`. The
shell and `just` both expand `$FILE` to an empty string, which silently turns
the URL into a 404 or the wrong page. **Always single-quote PURA URLs**, and
escape `$` as `\$` (shell) or `$$` (just) when one must go inside double
quotes. When a `just` recipe mangles one, call the underlying CLI directly
(e.g. `uv run python -m lib.sources.cli dedupe …`).

## Decision tree

```
Have a filing page URL (…?OpenDocument)?
├─ YES → fetch_pura_filing.py filing '<url>' -o DIR [--merge FILE]
│
└─ NO → Have a $FILE attachment URL?
         ├─ YES → Replace the "/$FILE/<name>" tail with "?OpenDocument" to get
         │        the filing page, then use `filing` as above (you need its
         │        metadata anyway)
         │
         └─ NO → Have a docket number?
                  └─ fetch_pura_filing.py docket <YY-MM-NN> --match '<text>' [--expand]
                     → pick the filing's URL → `filing`
```

## Fetching

The helper uses only the standard library (plus `pypdf` for `--merge`):

```bash
S=.cursor/skills/ctpura-documents/scripts/fetch_pura_filing.py

# One filing: metadata as JSON (filer, law firm, company, dates, interrogatory
# range answered or issued, attachments)
uv run python $S filing 'https://www.dpuc.state.ct.us/dockcurr.nsf/All/<ID>?OpenDocument'

# Download its PDFs (checks %PDF header and > 1 KB), merged into one file
uv run python $S filing '<filing URL>' -o /tmp/<slug> --merge /tmp/<slug>/<name>.pdf

# Find filings in a docket (Electric view). --expand lists the responses filed
# under each interrogatory set ("Question(s) Answered …").
uv run python $S docket 26-05-10 --match 'Sierra Club to CL&P' --expand
```

Download to `/tmp/` and let `ingest-source` place the file: PDFs under
`context/sources/` are gitignored and live on the Zotero item.

The JSON metadata maps straight onto the details card:

| Filing page field                       | Card use                                              |
| --------------------------------------- | ----------------------------------------------------- |
| `company` / `official_filer`            | Author organization (responses: the company only)     |
| `filing_firm`                           | Counsel; goes in the index row, not the author list   |
| `date_filed` (or `date_issued`)         | Date                                                  |
| `interrogatories_answered` / first–last | Title range (e.g. "Responses to CLF-SC-024 to …-035") |
| `docket_number`, `docket_title`         | Title prefix `Docket 26-05-10: …`; index row          |
| filing page URL                         | `source_url`                                          |

## Conventions for PURA sources

- **One source per set.** Responses are grouped by the request set they
  answer ("Information requests and their responses" in
  `context/code/source_metadata_conventions.md`). A response filing usually has
  one PDF per question (`CLF-SC-024_Final.pdf`, …); merge them with `--merge`,
  in question order, into one item.
- **Discovery compilations.** Eversource also files periodic "Discovery
  Compilations" correspondence (e.g. "ALLCO Set 11, CLF-SC Set 3, OCC Set 24")
  whose attachments (`<Party> Set <n>_COMBINED.pdf`) repackage responses
  already filed. Use a compilation as the item's file when it reproduces the
  set's answers exactly; it saves merging. If it carries answers from another
  set (the CLF-SC Set 1 compilation also holds CLF-SC-021 to 023), cut it to
  this set's pages. Date the item by the original response filing, not the
  compilation, and say in `context` that the file is the compilation.
- **File names:** `pura_<docket without dashes>_<slug>`, e.g.
  `pura_260510_eversource_resp_clf_sc_set3.md`,
  `pura_260510_ciec_ir1_to_clf_sc.md`.
- **Titles and keys** follow `context/code/source_metadata_conventions.md`:
  `Docket 26-05-10: Responses to CLF-SC-024 to CLF-SC-035`, author
  "Eversource Connecticut" (short form CL&P). Repeat sets in a docket collide
  on the key and take `a`, `b`, … suffixes (`clp_Docket260510Responses_2026a`).
- **Page numbers restart in each response.** Eversource responses print
  "Page n of N" per question. In a merged PDF the extract markers record that
  automatically (`[PDF p. 5 | printed p. 2]`), and citations use the response
  plus page: "CL&P Response to CLF-SC-027 at 2". Use `citation_scheme: page`
  and put one `## CLF-SC-0nn` section per response in the extract, so
  `just sources-cite` finds quotes per response.
- **Interrogatories issued** pages (questions, not answers) are authored by
  the issuing party (e.g. CIEC); the filing firm (e.g. Couch White LLP) is
  counsel.

## Worked examples

| Filing                                                                                                                                                           | Kind                   | Result                                                  |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------- |
| [CL&P responses CLF-SC-024 to 035](https://www.dpuc.state.ct.us/dockcurr.nsf/All/D0AF6A55310B9AC485258E9800474D25?OpenDocument), 10/21/2026                      | 12 PDFs, merged        | one source, 16 pages, `clp_Docket260510Responses_2026a` |
| [CIEC First Set to CLF-SC](https://www.dpuc.state.ct.us/DOCKCURR.NSF/5f3a36a996853741852588c600420c24/342fb8efd580d1b085258e9f00669a2b?OpenDocument), 10/29/2026 | Interrogatories issued | one source, `ciec_Docket260510First_2026`               |

## Additional resources

- [reference.md](reference.md): URL patterns, the docket views and how they
  expand, filing page layouts, and parsing notes.
- `scripts/fetch_pura_filing.py`: the tested helper above.
- `.cursor/skills/ingest-source/SKILL.md`: everything after the download.
