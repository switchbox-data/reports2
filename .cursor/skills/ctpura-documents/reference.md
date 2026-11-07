# Connecticut PURA site reference

Notes on the PURA docket database at `https://www.dpuc.state.ct.us/`, a Lotus
Domino server. Everything here was checked against Docket 26-05-10 (the 2026
CL&P rate case). `scripts/fetch_pura_filing.py` implements it.

## Databases and entry points

| Database               | Contents                       |
| ---------------------- | ------------------------------ |
| `DOCKCURR.NSF`         | Current (active) dockets       |
| `2NDDOCKCURR.NSF`      | Second current-docket database |
| `dockhistpost2000.NSF` | Closed dockets since 2000      |

Domino URLs are case-insensitive (`dockcurr.nsf` and `DOCKCURR.NSF` both
work). The human entry point is the
[docketed and undocketed databases](https://portal.ct.gov/pura/docket/docketed-and-undocket-databases)
page on the PURA portal, which links to the views below. Other useful views:
`$FormWMV-AdditionsOnly-last14daysView` (new filings in the last 14 days) and
`$FormWMV-RevByDocketNumberView`.

## URL patterns

| What             | Pattern                                                          |
| ---------------- | ---------------------------------------------------------------- |
| Filing page      | `/dockcurr.nsf/All/<docID>?OpenDocument`                         |
| Same, via a view | `/DOCKCURR.NSF/<viewID>/<docID>?OpenDocument`                    |
| Attachment       | `/dockcurr.nsf/<viewID>/<docID>/$FILE/<url-encoded file name>`   |
| Docket view      | `/DOCKCURR.NSF/$FormDocketElectricRevView?OpenForm&CollapseView` |
| Expanded view    | `…?OpenForm&Start=1&Count=1000&Expand=<index>&Seq=1`             |

`<docID>` is a 32-hex-digit Domino document ID; any view ID (or `All`) in front
of it opens the same document. Single-quote all of these in the shell (see
"The `$FILE` pitfall" in `SKILL.md`).

## The Electric docket view

`$FormDocketElectricRevView` is a three-level outline. Each level is opened by
passing its outline index as `Expand=`; the HTML holds one `<tr>` per row,
with an `Expand=` link on rows that have children and an `?OpenDocument` link
to the row's own page.

| Level | Row text                                                                                                             | Index (26-05-10)    |
| ----- | -------------------------------------------------------------------------------------------------------------------- | ------------------- |
| 1     | `2026 Docket Numbers` (2026 is 1, 2025 is 2, …)                                                                      | `1`                 |
| 2     | `[26-05-10] Application of The Connecticut Light and Power Company …`                                                | `1.68`              |
| 3     | Filings: `Corres.`, `Motion No.`, `Notice`, `Prefiled testimony`, `Interrogs …`                                      | `1.68.<n>`          |
| 4     | Under an `Interrogs from X to Y a thru b-Issued <date>` row: `Question(s) Answered … (<company>) Date Filed: <date>` | `1.68.<n>` expanded |

The docket's index within its year changes as dockets are added, so look it up
each time rather than hard-coding it. Expanding a level-2 row returns the whole
year outline with that docket's filings inserted after its row; the docket's
filings end at the next `[YY-MM-NN]` row. Response filings appear **only**
under their interrogatory row (level 4), never as level-3 rows, so a search
for a response needs `--expand`. A large docket has hundreds of level-3 rows
(26-05-10 had 480 by November 2026); `Count=1000` returns them in one page.

Only the Electric view has been checked. Other industries (gas, water,
telecom) have their own `$FormDocket…RevView` views on the portal page; their
names are unverified.

## Filing page layouts

Filing pages come in at least two forms. The helper handles both.

**Responses (and most filings).** One `Label [hint]: value` per line:

```
Interrogs Responses for [ 26-05-10 ]  by Connecticut Light and Power Company dba Eversource Energy filed on 10/21/2026
Docket Number:  26-05-10
Official Filer(s) Name [On Behalf Of What Entity]:  CL&P
Filing Firm's Name [Submitter of Filing]:  Keegan Werlin LLP
Company Name [Pertains To What Entity]:  Connecticut Light and Power Company dba Eversource Energy
Date Filed:   10/21/2026 07:13:14 PM
All Files Attachment:   - CLF-SC-024_Final.pdf …
Interrogatories answered:  24 thru 35
Supplemental or Revision: No
```

**Interrogatories issued.** The value sits on the line after its label,
sometimes after a parenthetical hint (`(If different than Filing Firm)`), and
the page carries a large inline `<script>` that must be stripped first. Extra
fields: `Docket Title`, `Directed from`, `Directed to`, `Beginning Interrogatory
Number`, `Ending Interrogatory Number`, `Date Issued`, `Indicated Date Due`.

"Supplemental or Revision: Yes" marks a filing that revises an earlier
response; ingest it as its own source and say which response it replaces.

## Parsing notes

- Pages are Latin-1; decode with `latin-1`, then `html.unescape`.
- Attachment links are the `href`s containing `/$FILE/`; the same link can
  appear twice, so de-duplicate in order.
- No session, cookies or form posts are needed; plain GETs work.
- A URL whose `$FILE` was expanded away returns a small HTML page, "Error 400:
  Unknown Command Exception". `curl -o` without `-f` saves that page under the
  `.pdf` name, so check the `%PDF` header before trusting a download.
