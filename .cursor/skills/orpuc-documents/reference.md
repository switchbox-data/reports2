# Oregon PUC site reference

Everything below was tested in November 2026 with plain `curl` and a browser
User-Agent from the EC2 dev server (no cookies needed).

## URL patterns

| What                      | URL                                                                                              | Notes                                                                                                                                                                                                                                                                      |
| ------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Search page               | `https://apps.puc.state.or.us/edockets/search.asp`                                               | Plain GET forms to `srchlist.asp`                                                                                                                                                                                                                                          |
| Docket search             | `…/edockets/srchlist.asp?Prefix=UM++&DocketNumber=2377&submit1=GO`                               | `Prefix` is 4 chars, space-padded (`UM++` is `'UM  '`). The form offers ADV, AR, ARB, BP, CD, CP, DR, EA, ES, ETO, FA, IC, LC, NC, PCN, PL, RE, RG, RO, RT, RW, SA, UA, UCB, UD, UE, UF, UG, UI, UM, UNC, UP, UPN, UT, UW, UX, WA, WJ. Result links contain `DocketID=<n>` |
| Criteria search (dockets) | `…/edockets/srchlist.asp?SearchType=Docket&Category=UE++&Company=32&chkOpen=open&submit3=Submit` | Rows: docket, title, filed, final order and date. Optional `DateRange=usedate&StartMonth=&StartDay=&StartYear=&EndMonth=&EndDay=&EndYear=`                                                                                                                                 |
| Criteria search (tariffs) | `…/edockets/srchlist.asp?SearchType=Tariff&Company=32&chkPending=pending&submit3=Submit`         | Rows: advice no., ADV docket, PDF, title, filed, status, effective date. Same date parameters                                                                                                                                                                              |
| Company ids               | the `<select name="Company">` on `…/edockets/search.asp`                                         | PGE 32, Pacific Power (PacifiCorp) 33, Idaho Power 31, NW Natural 417, Avista 49, Cascade Natural Gas 50                                                                                                                                                                   |
| Docket page (actions)     | `…/edockets/docket.asp?DocketID=24470`                                                           | Summary plus the full ACTIONS list (245 actions for UM 2377)                                                                                                                                                                                                               |
| Order, by number          | `…/edockets/orders.asp?OrderNumber=26-154`                                                       | 302 to `/orders/2026ords/26-154.pdf` (or `1998ords/98-374.htm`)                                                                                                                                                                                                            |
| Order, direct             | `https://apps.puc.state.or.us/orders/<year>ords/<yy>-<nnn>.pdf`                                  | Older orders `.htm`                                                                                                                                                                                                                                                        |
| Filing, by link           | `…/edockets/edocs.asp?FileType=HTB&FileName=<f>&DocketID=<n>&numSequence=<k>`                    | 302 to the direct URL below                                                                                                                                                                                                                                                |
| Filing, direct            | `https://edocs.puc.state.or.us/efdocs/<FileType>/<FileName>`                                     | `FileName` = docket + lowercase FileType + digits, e.g. `um2377htb342431028.pdf`                                                                                                                                                                                           |
| Docket service list       | `…/edockets/docket_service_list.asp?DocketId=24470&Names=1`                                      | Semi-colon delimited emails                                                                                                                                                                                                                                                |
| Orders search page        | `https://apps.puc.state.or.us/orders/`                                                           | Order index by year                                                                                                                                                                                                                                                        |

`srchlist.asp?OrderNumber=26-154` is **not** a way to get the order: it returns
the docket and links the docket's latest filing. Use `orders.asp`.

The `DocketNoLayout.asp?DocketID=<n>` page (what web search tends to surface)
is a second view of the same actions; `docket.asp` is the one the script
parses.

## Docket page layout

Each action is a group of `<tr>` rows in this order:

1. date row: `<b>Date:`, the date, `Action:` type, and the document link
   (`edocs.asp?...` for filings, `orders.asp?OrderNumber=...` for orders)
2. for orders only: an `Order No:` row
3. a `Description` row: free text, sometimes with `TAGS:` lines
   (e.g. `Confidential to Agency Folder`)

The link belongs to the **date row above** its description. Newest action
first.

## FileType codes (the three letters in the file path)

Observed across UM 2377, UE 416, UE 457 and UM 827; one code per action type:

| Code | Action type                                | Code      | Action type                                          |
| ---- | ------------------------------------------ | --------- | ---------------------------------------------------- |
| HAA  | Initial (application, complaint, petition) | HDA       | Law judge ruling/memoranda                           |
| HAC  | Comments/response                          | HDB       | Commission ruling/memoranda                          |
| HAD  | Compliance                                 | HDF       | Intervention ruling                                  |
| HAE  | Protest/exception/objection                | HKK       | Appeal                                               |
| HAF  | Cross-exam statement                       | HNA       | Notice                                               |
| HAG  | Reconsideration                            | HPC       | Public comment                                       |
| HAH  | Other filing/pleading                      | HPD       | Other correspondence                                 |
| HAK  | Issue statement                            | HSA / HSB | GPO / MPO signatory page                             |
| HAN  | Signatory pages                            | HTB       | **Testimony and exhibits**                           |
| HAO  | Motion                                     | HUA–HUD   | Intervenor funding (notice, motion, budget, payment) |
| HAP  | Petition to intervene                      | UAA–UBH   | Utility filings / advice letters (tariff sheets)     |
| HAR  | Stipulation                                | UHR       | Advice                                               |
| HAU  | Staff report                               | HBC       | **Brief**                                            |
| HAW  | Huddle request                             | HCB / HCD | Hearing / conference                                 |

Orders are not in `efdocs`; they live under `/orders/<year>ords/`.

## Identifiers seen

| Docket  | DocketID | What                                               |
| ------- | -------- | -------------------------------------------------- |
| UM 2377 | 24470    | PGE large-load / marginal cost study investigation |
| UE 416  | 23617    | PGE general rate revision (2023)                   |
| UE 457  | 24618    | PGE power cost adjustment mechanism                |
| LC 73   | 21929    | PGE 2019 integrated resource plan                  |
| UM 827  | 5319     | Estimating marginal costs, electric (1998)         |

Docket prefixes seen in practice: **UE** electric rate cases and power cost
filings, **UM** miscellaneous investigations, **LC** least-cost plans (IRPs).
**UG** is gas and **UI** affiliated interest by convention, but those were
not tested.

## Citation formats in Oregon filings

- Testimony: `<Party>/<exhibit>, <Witness>/<page>`, e.g. `CUB/300, Jenks/15`,
  `PGE/400, Ferchland-Barrow-Jose/18`, `Staff/300, Stevens/25-26`. Party codes
  seen: CUB, Staff, PGE, AWEC, Coalition, DCC, CRITFC, Verrus, ADS (Amazon).
- Exhibit pages follow the exhibit's own PDF pagination, e.g. `CUB/116 Jenks/56`
  is PDF page 56 of the RAP Manual (printed page 54).
- Orders cite as `Order No. 23-386 at 14 (Oct. 30, 2023)`.
- Issue lists in orders are numbered ("16. Should data centers be charged the
  marginal cost of transmission?"), each with _Positions of the Parties_ and
  _Resolution_. The resolution is the holding.

## Docket categories (the `Category` / `Prefix` values)

ADV advice filings; AR administrative rule; ARB arbitration; CP competitive
provider; UCB consumer complaint (business); DR declaratory rulings; UE
electric rate case; EA/ES electricity service aggregator/supplier; ETO Energy
Trust presentations; UX exemption; FA fee assessment; UF financing; UG gas
rate case; IC interconnection complaint; LC least cost planning (IRP); UM
miscellaneous; NC/UNC notification center; UD/PL price list; UP/UPN property
transactions; PCN public convenience and necessity; RE/RG/RO/RT/RW reports;
UA service area allocation; UT telephone rate case; WA/WJ water; UW water rate
case. Values are four characters wide, space-padded.

## The newer eDocketsSearch app: no advantage

`https://apps.puc.state.or.us/edocketsSearch/eDocketsSearch/` is a server-rendered
form (ASP.NET, POST with an antiforgery token and cookie; it does not need
JavaScript to search). Every search type either redirects to the legacy
`srchlist*.asp` / `filelistNoLayout.asp` pages with query-string parameters, or
re-presents the same company/industry criteria form. Querying the legacy URLs
directly gives the same results with no token. Its one convenience, "New
Filings by week", is `filelistNoLayout.asp?StartDate=10%2f26%2f2026&EndDate=11%2f8%2f2026`
(all filings across all dockets in the window). A couple of weeks returns in
seconds; a 22-month window (Jan. 2025 to Nov. 2026) did return, but took about
100 seconds and a 2.1 MB page, so run it in the background or keep windows short.

## Tested behavior and limits

- Large PDFs work (34.6 MB order in a few seconds); no rate limiting seen.
- `orders.asp` for a nonexistent order returns a page, not a redirect; the
  script reports "not found".
- Old (1990s) dockets: filings are listed as text with no files, except
  orders.
- The "Go to specific Tariff Advice #" box (`srchlist.asp?TariffNumber=`)
  returned "no records" for every format tried (`26-43`, `2643`, `1911`,
  `ADV1911`), so tariff lookup goes through the company/date criteria search,
  or `docket "ADV <n>"` when the ADV number is known.
- Advice filing PDFs hold the letter and revised tariff sheets; work papers
  are usually on the Huddle Portal (not public).
- Not tested: public-comment portals, the hearings calendar, Oregon Court of
  Appeals filings (outside the OPUC site; see SKILL.md).
