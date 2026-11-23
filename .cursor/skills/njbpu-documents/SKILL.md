---
name: njbpu-documents
description: >-
  Finds and fetches New Jersey Board of Public Utilities (NJBPU) docket filings,
  board orders, and utility tariffs from publicaccess.bpu.state.nj.us and
  nj.gov/bpu. Use when working with NJ BPU, NJBPU, a NJ docket number like
  ER23120924, PSE&G rate cases, JCP&L, ACE, NJ Rate Counsel, NJ electric
  tariffs, or context/sources/nj_hp_rates/.
---

# New Jersey BPU documents

Find and download NJ Board of Public Utilities filings for the
`context/sources/nj_hp_rates/` corpus. This skill is a **fetch subroutine of
`discover-sources`**: use it when a discovery run needs documents from the
NJ BPU. It downloads into the discovery run's scratch inbox and nothing else.
It does **not** ingest; approved candidates go on to `ingest-source`.

## Before you start

1. Identify what you have: a **docket number** (`ER23120924`), a
   **document_id** (integer, e.g. `1359943`), a **board order date and agenda
   item** (`2024-10-09 2A`), or a topic/party name.
2. Check for duplicates before downloading:
   `rg -n "<docket or title>" context/README.md context/sources/nj_hp_rates/`,
   then `just sources-dedupe` on the PDF.
3. The NJ BPU site (`publicaccess.bpu.state.nj.us`) is **accessible from the
   dev server** — no Cloudflare blocks, no login required. It does use an
   **Incapsula/Imperva WAF** that requires a browser User-Agent header and a
   cookie-warming handshake (the helper script handles this automatically).
   Board orders on `nj.gov` and tariffs on `nj.pseg.com` have no WAF at all.

## Decision tree

```
Have a document_id?
├─ YES → fetch_njbpu.py fetch <id> -o DIR
│
└─ NO → Have a docket number (ER23120924)?
         ├─ YES → fetch_njbpu.py case <docket>
         │        → pick the document_id from the listing
         │        → fetch <id> -o DIR
         │
         └─ NO → Have a board order date + agenda item?
                  ├─ YES → fetch_njbpu.py order <YYYY-MM-DD> <item>
                  │
                  └─ NO → Looking for a tariff?
                           ├─ YES → PSE&G website (see "Tariffs" below)
                           │
                           └─ NO → Have a party name or topic?
                                    └─ fetch_njbpu.py search <query> --type party
                                       → pick the docket → case → fetch
```

## Fetching

```bash
S=.cursor/skills/njbpu-documents/scripts/fetch_njbpu.py

# List all documents in a docket (prints document_id, folder, date, title)
uv run python $S case ER23120924

# Download one document by document_id
uv run python $S fetch 1359943 -o ~/.cache/switchbox_sources/inbox/<run>

# Search by docket number or party name (GET-based, no ViewState needed)
uv run python $S search "PUBLIC SERVICE ELECTRIC" --type party
uv run python $S search ER23120924 --type docket

# Download a board order by meeting date and agenda item
uv run python $S order 2024-10-09 "2A ORDER PS 23 BRC"
```

Download into the discovery run's inbox folder
(`~/.cache/switchbox_sources/inbox/<YYYY-MM-DD>_<topic>/`, `-o` on every
command). Every download is checked for a `%PDF` header and size over 1 KB.

**What goes in `candidates.json`.** Only facts seen on the document or the
docket page: `issuer`, `date`, `docket`, `source_url` (the
`DocumentHandler.ashx?document_id=` URL or the `nj.gov` board order URL),
and `why_relevant`. Leave `doi` null.

## Three document systems

### 1. Public Document Search (primary)

**URL:** `https://publicaccess.bpu.state.nj.us/`

The main docket filing system. ASP.NET WebForms app with Incapsula WAF.
Documents from 2015–present (expanding). Supports search by docket number,
document title, party name, keyword, and advanced (combined criteria + date
range). Documents served as PDF via `DocumentHandler.ashx?document_id={id}`.

The helper script handles the WAF cookie-warming automatically. See
[reference.md](reference.md) for URL patterns, form fields, and pitfalls.

### 2. Board orders (nj.gov)

**URL:** `https://www.nj.gov/bpu/pdf/boardorders/{YYYY}/{YYYYMMDD}/{name}.pdf`

Static PDFs at predictable paths. No WAF, no auth. The order naming scheme
uses the agenda item number (e.g. `2A ORDER PS 23 BRC`). Calendar pages at
`/bpu/agenda/{YYYY}calendar/approved/` list each meeting's orders.

Board minutes: `/bpu/pdf/boardminutes/{YYYY}/{YYYYMMDD}/...`
Board agendas: `/bpu/pdf/boardagendas/{YYYY}/{YYYYMMDD}a.pdf`

### 3. Utility tariff pages

PSE&G hosts its own tariffs at:
`https://nj.pseg.com/AboutPSEG/regulatorypage/ElectricTariffs`

Tariff PDFs served via `.ashx` handlers:

- Current: `/-/media/pseg/public-site/documents/current-electric-tariff/{name}.ashx`
- Prior: `/-/media/pseg/public-site/documents/electric-prior-tariffs/{name}.ashx`

No WAF. Direct `curl -o` works. See [reference.md](reference.md) for the full
URL pattern and tariff history.

## Docket number format

```
{Classification}{CaseType}{YY}{MM}{NNNN}{Suffix}
```

| Part           | Values                                                                    |
| -------------- | ------------------------------------------------------------------------- |
| Classification | E=Electric, G=Gas, A=All, C=Cable, T=Telecom, W=Water, Q=Clean Energy     |
| CaseType       | R=Rates, O=Other, X=Generic, T=Tariff Revision, M=Merger, C=Complaint ... |
| YYMM           | 2-digit year + 2-digit month                                              |
| NNNN           | 4-digit sequence number                                                   |
| Suffix         | `-`=Case Management (most common)                                         |

Example: `ER23120924-` = Electric + Rates + Dec 2023 + case 0924.

## Conventions for NJ BPU sources

- **File names:** `njbpu_<docket without dashes>_<slug>`, e.g.
  `njbpu_er23120924_final_order.pdf`,
  `njbpu_er23120924_faruqui_tou_testimony.pdf`.
- **Titles and keys** follow `context/code/source_metadata_conventions.md`:
  `Docket ER23120924: Order Adopting Initial Decision and Stipulation`, author
  "New Jersey Board of Public Utilities" for orders; for testimony the author
  is the witness.

## Pitfalls

- **Incapsula WAF**: Bare `curl` without a User-Agent gets a 403 JavaScript
  challenge. The helper script handles cookie-warming automatically.
- **GET search only works for CaseNumber and PartyName**. Keyword and
  DocumentTitle searches require the full POST form flow with ViewState tokens.
  The helper script currently implements GET search only.
- **Pagination is POST-only**. The case summary page and search results show
  30 items per page; additional pages require `__doPostBack`. The helper
  script parses the first page only (sufficient for most cases; ER23120924
  has 79 documents and loads in one page).
- **Document naming is inconsistent**. Some use `YYYY-MM-DD - Utility -
  Description`, others use all-caps abbreviations, others use the BPU agenda
  item number (e.g. `10-9-24-2A`).
- **Board order filenames have spaces**. URL-encode spaces when constructing
  the path (or use the helper's `order` subcommand).
- **Cross-docket documents**. Some documents span electric and gas dockets
  (e.g. `ER23120924 & GR23120925`); they appear in both case summaries.

## Worked examples

| Document                         | Fetch                                   | Result                                  |
| -------------------------------- | --------------------------------------- | --------------------------------------- |
| PSE&G 2023 rate case final order | `fetch 1359943`                         | Board order, Oct 9, 2024                |
| Stipulation of Settlement        | `fetch 1359450`                         | Settlement terms, Oct 2, 2024           |
| Faruqui TOU testimony (P-10)     | `fetch 1324634`                         | Brattle Group rate design, Dec 29, 2023 |
| Swetz electric testimony (P-9E)  | `fetch 1324632`                         | PSE&G rate design/COSS, Dec 29, 2023    |
| Electrify America exceptions     | `fetch 1359740`                         | EV rate design objections, Oct 7, 2024  |
| ChargeEVC TOU testimony          | `fetch 1342087`                         | EV charging TOU advocacy, May 16, 2024  |
| Board order by date              | `order 2024-10-09 "2A ORDER PS 23 BRC"` | Same order via nj.gov path              |

## Additional resources

- [reference.md](reference.md): URL patterns, form fields, WAF details,
  docket format decoder, all 79 documents in ER23120924.
- `scripts/fetch_njbpu.py`: the tested helper above.
- `.cursor/skills/discover-sources/SKILL.md`: the parent workflow.
- `.cursor/skills/ingest-source/SKILL.md`: only for candidates the user
  approves.
