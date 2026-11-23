# NJ BPU site reference

Everything below was tested in November 2026 from the EC2 dev server
(us-west-2). The Public Document Search site uses Incapsula/Imperva WAF
but is otherwise accessible without login.

## URL patterns

| What                     | URL                                                                                          | Notes                                                  |
| ------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Public search home       | `https://publicaccess.bpu.state.nj.us/`                                                      | Same as Search.aspx                                    |
| Search page              | `https://publicaccess.bpu.state.nj.us/Search.aspx`                                           | ASP.NET WebForms with radio buttons                    |
| Search results (GET)     | `…/SearchResults.aspx?SearchType={type}&SearchText={query}`                                  | CaseNumber and PartyName only                          |
| Case summary             | `…/CaseSummary.aspx?case_id={case_id}`                                                       | Documents, parties, comments grids                     |
| Document download        | `…/DocumentHandler.ashx?document_id={document_id}`                                           | PDF with Content-Disposition header                    |
| Search guide             | `https://www.publicaccess.bpu.state.nj.us/SearchGuide.pdf`                                   | Official user guide                                    |
| Board orders             | `https://www.nj.gov/bpu/pdf/boardorders/{YYYY}/{YYYYMMDD}/{name}.pdf`                        | Static PDFs, no WAF                                    |
| Board agendas            | `https://www.nj.gov/bpu/pdf/boardagendas/{YYYY}/{YYYYMMDD}a.pdf`                             | Meeting agendas                                        |
| Board minutes            | `https://www.nj.gov/bpu/pdf/boardminutes/{YYYY}/{YYYYMMDD}/…`                                | Meeting minutes                                        |
| Board calendar           | `https://www.nj.gov/bpu/agenda/{YYYY}calendar/approved/calendar_archive.html`                | Lists meeting dates with links to order PDFs           |
| Meeting orders page      | `https://www.nj.gov/bpu/agenda/{YYYY}calendar/approved/{YYYYMMDD}.html`                      | Lists all orders for one meeting                       |
| Newly docketed           | `https://nj.gov/bpu/agenda/hearings/docksched/{YYYYMMDD}ndm.pdf`                             | Weekly new docket list                                 |
| e-Filing page            | `https://nj.gov/bpu/agenda/efiling/`                                                         | FAQs and instructions                                  |
| PSE&G electric tariffs   | `https://nj.pseg.com/AboutPSEG/regulatorypage/ElectricTariffs`                               | Utility-hosted, links to current and prior tariff PDFs |
| PSE&G current tariff PDF | `https://nj.pseg.com/-/media/pseg/public-site/documents/current-electric-tariff/{name}.ashx` | PDF via ASP.NET handler, no WAF                        |
| PSE&G prior tariff PDF   | `https://nj.pseg.com/-/media/pseg/public-site/documents/electric-prior-tariffs/{name}.ashx`  | Same pattern for archived tariff versions              |
| PSE&G regulatory filings | `https://nj.pseg.com/aboutpseg/regulatorypage/regulatoryfilings`                             | Chronological list of all PSE&G BPU filings            |

## Incapsula/Imperva WAF (publicaccess.bpu.state.nj.us)

The site uses Incapsula CDN/WAF. Bare requests (no User-Agent) get a 403
with a JavaScript challenge page.

**Cookie-warming pattern** (3 hops):

1. First request: 302 redirect to the same URL, sets `visid_incap_2396935`
   and `nlbi_2396935` cookies.
2. Second request: another 302, sets `incap_ses_*` cookies.
3. Third request: 200 with actual content.

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Warm the cookie jar
curl -s -c cookies.txt -o /dev/null -H "User-Agent: $UA" "$URL"
curl -s -b cookies.txt -c cookies.txt -o /dev/null -H "User-Agent: $UA" "$URL"
# Now the real request
curl -s -b cookies.txt -c cookies.txt -o result.html -H "User-Agent: $UA" "$URL"
```

The cookie jar must be reused across requests. `ASP.NET_SessionId` is also
set. The helper script (`fetch_njbpu.py`) handles this automatically via a
`requests.Session()`.

**nj.gov and nj.pseg.com** have no WAF — plain `curl` works.

## Search interface

### GET-based search (CaseNumber and PartyName)

```
https://publicaccess.bpu.state.nj.us/SearchResults.aspx?SearchType={type}&SearchText={query}
```

| SearchType      | GET works? | Notes                                         |
| --------------- | ---------- | --------------------------------------------- |
| `CaseNumber`    | Yes        | Partial matches; single result → 302 to case  |
| `PartyName`     | Yes        | Partial matches supported                     |
| `DocumentTitle` | No         | Requires POST with ViewState                  |
| `Keyword`       | No         | Requires POST with ViewState                  |
| `Advanced`      | No         | Combines criteria + date range; requires POST |

**ListType** parameter (optional): `Docket` (default) or `Document`.

**Single result** → 302 redirect to `CaseSummary.aspx?case_id={id}`.
**Multiple results** → 200 with HTML table: Docket #, Case Type, Open Date,
Caption, Party Name, Case Status.

### POST-based search (all types)

Required for DocumentTitle, Keyword, and Advanced Search. Steps:

1. GET `Search.aspx` to obtain `__VIEWSTATE`, `__VIEWSTATEGENERATOR`,
   `__EVENTVALIDATION`.
2. POST to `Search.aspx` with form fields:

| Field                                               | Value                             |
| --------------------------------------------------- | --------------------------------- |
| `__VIEWSTATE`                                       | From initial GET                  |
| `__VIEWSTATEGENERATOR`                              | `BBBC20B8`                        |
| `__VIEWSTATEENCRYPTED`                              | (empty)                           |
| `__EVENTVALIDATION`                                 | From initial GET                  |
| `ctl00$ContentPlaceHolder1$searchFilter$searchType` | `CaseNumber` / `PartyName` / etc. |
| `ctl00$ContentPlaceHolder1$searchFilter$SearchText` | Query text                        |
| `ctl00$ContentPlaceHolder1$searchFilter$btnSearch`  | `Search`                          |
| `ctl00$ContentPlaceHolder1$searchFilter$ListType`   | `Docket` or `Document`            |

**Advanced Search** additional fields:

| Field                                 | Value                       |
| ------------------------------------- | --------------------------- |
| `…$searchFilter$AdvanceCaseNumber`    | Docket number               |
| `…$searchFilter$AdvanceDocumentTitle` | Document title              |
| `…$searchFilter$AdvancePartyName`     | Party name                  |
| `…$searchFilter$AdvanceKeyword`       | Keyword in document content |
| `…$searchFilter$OpenDateFrom`         | MM/DD/YYYY                  |
| `…$searchFilter$OpenDateTo`           | MM/DD/YYYY                  |
| `…$searchFilter$btnAdvanceSearch`     | `Search`                    |

POST redirects to `/SearchResults.aspx`, which needs the same session.

**Pagination:** 30 results per page. Uses `__doPostBack` with targets like
`ctl00$ContentPlaceHolder1$gvSearchRs$ctl33$lbtnNum{N}` and `lbtnNext`.
Cannot paginate via URL parameters.

## Case summary page

**Grids:**

1. **Documents** (`gvDocuments`): checkbox, Docket #, Document Title
   (links to `DocumentHandler.ashx?document_id={id}`), Folder, Uploaded By,
   Description, Posted Date.
2. **Parties** (`gvParties`): Name, Type, Relationship.
3. **Comments** (`gvComments`): Posted By, Posted Date, Comments, Attachments.

**Sort controls:** `investigation_no` (docket), `name` (title), `folder`,
`doc_author`, `description`, `addon` (posted date).

**Batch download** via checkboxes + download button.

## Document download

```
https://publicaccess.bpu.state.nj.us/DocumentHandler.ashx?document_id={id}
```

- `Content-Type: application/pdf`
- `Content-Disposition: attachment;filename={TITLE}.PDF`
- No authentication; requires User-Agent (Incapsula)
- Average size: 1–7 MB for testimony/orders

## Document folder types

Observed in ER23120924 (79 documents total):

| Folder                         | Count | Contents                                    |
| ------------------------------ | ----- | ------------------------------------------- |
| CORRESPONDENCE                 | 18    | Cover letters, compliance filings, NDA      |
| MOTIONS                        | 17    | Intervention, participation, pro hac vice   |
| TESTIMONY                      | 16    | Direct testimony and schedules (P-2 … P-12) |
| COMMENTS                       | 15    | Public/stakeholder comments, exceptions     |
| PETITIONS                      | 5     | Rate case filings and updates (9+3, 12+0)   |
| ORDERS                         | 3     | Board orders                                |
| REPORTS                        | 2     | AMI final report, service extension report  |
| JOINT PROPOSALS / STIPULATIONS | 1     | Settlement agreement                        |
| NOTICES                        | 1     | Publication affidavits                      |
| INITIAL DECISIONS              | 1     | ALJ initial decision                        |

## Docket number format

```
{Classification}{CaseType}{YY}{MM}{NNNN}{Suffix}
```

| Part           | Values                                                                                  |
| -------------- | --------------------------------------------------------------------------------------- |
| Classification | E=Electric, G=Gas, A=All Utilities, C=Cable TV, T=Telecom, W=Water, Q=Clean Energy      |
| CaseType       | A=Audits, C=Complaint, D=Discontinuance, E=Franchise, F=Financing, M=Merger, R=Rates, … |
| YYMM           | 2-digit year + 2-digit month of filing                                                  |
| NNNN           | 4-digit sequence number within the month                                                |
| Suffix         | `-`=Case Management (most common), S=Slamming, U=Customer Assistance, K=One-Call        |

Example: `ER23120924-` = Electric (E) + Rates (R) + Dec 2023 (2312) + seq 0924 + Case Mgmt (-).

## Board order naming convention

Orders use agenda item numbering:

- `2A ORDER PS 23 BRC` = Agenda section 2 item A, PSE&G 2023 Base Rate Case
- Roman numerals (I–IX) for consent agenda sections
- Arabic numerals (1–9) for regular agenda sections
- Letters (A, B, C…) for sub-items within a section

The legacy "Search Board Orders" is a Google Custom Search Engine widget
(ID `012084561889324683733:trkpvkcunjo`), not API-friendly.

## Key document_ids — ER23120924 (PSE&G 2023 Rate Case)

**Case ID:** 2112583

| document_id | Folder                         | Posted     | Title                                                             |
| ----------- | ------------------------------ | ---------- | ----------------------------------------------------------------- |
| 1359943     | ORDERS                         | 10/10/2024 | 10-9-24-2A (Final Order)                                          |
| 1325663     | ORDERS                         | 01/11/2024 | 1-10-24-IIA (Rate Suspension Order)                               |
| 1344163     | ORDERS                         | 05/28/2024 | 5-22-24-IIA (Rate Suspension Extension)                           |
| 1359450     | JOINT PROPOSALS / STIPULATIONS | 10/04/2024 | Stipulation of Settlement                                         |
| 1359451     | INITIAL DECISIONS              | 10/04/2024 | ALJ Initial Decision                                              |
| 1324630     | PETITIONS                      | 12/29/2023 | P-1 - Petition Schedules 1-12                                     |
| 1324631     | TESTIMONY                      | 12/29/2023 | P-2 - McFadden Testimony and Schedules                            |
| 1324637     | TESTIMONY                      | 12/29/2023 | P-3 - Panel Testimony and Schedules                               |
| 1324638     | TESTIMONY                      | 12/29/2023 | P-4 - Pardo Testimony and Schedules                               |
| 1324639     | TESTIMONY                      | 12/29/2023 | P-5 - Bulkley Testimony and Schedules (ROE)                       |
| 1324640     | TESTIMONY                      | 12/29/2023 | P-6 - Adams Testimony and Schedules (Cost Allocation)             |
| 1324641     | TESTIMONY                      | 12/29/2023 | P-7 - Spanos Testimony and Schedules                              |
| 1324642     | TESTIMONY                      | 12/29/2023 | P-8 - Adams Testimony and Schedules                               |
| 1324632     | TESTIMONY                      | 12/29/2023 | P-9E - Swetz Testimony and Schedules (Electric Rate Design)       |
| 1324633     | TESTIMONY                      | 12/29/2023 | P-9G - Swetz Testimony and Schedules (Gas Rate Design)            |
| 1324634     | TESTIMONY                      | 12/29/2023 | P-10 - Faruqui Testimony and Schedules (TOU Rate Design)          |
| 1324635     | TESTIMONY                      | 12/29/2023 | P-11 - Reif Testimony and Schedules                               |
| 1324636     | TESTIMONY                      | 12/29/2023 | P-12 - Johnson Testimony and Schedules                            |
| 1342087     | TESTIMONY                      | 05/16/2024 | ChargeEVC TOU Rate Filing Testimony                               |
| 1359740     | COMMENTS                       | 10/08/2024 | Electrify America Exceptions and Comments to the Initial Decision |
| 1359741     | COMMENTS                       | 10/08/2024 | Electrify America Exceptions Cover Letter                         |
| 1371846     | COMMENTS                       | 02/03/2025 | Joint Industry Letter (Electrify America/EVgo/ChargePoint/Tesla)  |
| 1360143     | CORRESPONDENCE                 | 10/11/2024 | Compliance Filing                                                 |
| 1363515     | CORRESPONDENCE                 | 11/07/2024 | Revised Compliance Filing                                         |
| 1406068     | CORRESPONDENCE                 | 12/05/2025 | BGS RS-TOU 3P Compliance Filing                                   |
| 1424482     | CORRESPONDENCE                 | 05/28/2026 | BGS RS-TOU 3P Compliance Filing Update                            |
| 1370217     | REPORTS                        | 01/17/2025 | PSE&G AMI Program Final Report                                    |

## Data coverage

Per the BPU orders page (November 2026): "Public Document Search tool
currently provides all publicly-available documents from 2021 through 2015,
plus some 2014 documents." Content continues to be expanded.

The 2023 PSE&G rate case (ER23120924, filed December 2023) is fully
available with all 79 documents. Recent cases (2024–2026) are uploaded
promptly, typically within days of filing.
