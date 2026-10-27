# Source metadata conventions (Zotero)

How items in the Switchbox Zotero group library are named and keyed. `reports/references.yaml` is a faithful mirror of the **Reports** collection (see the Bibliography section of `AGENTS.md`), so anything wrong in a citation is fixed here, in Zotero, and regenerated with `just sync-bib`. The library cleanup (`just orgs-*`) and source ingest both follow this document; the citation-key rule is implemented once, in `lib/sources/citekeys.py`.

## Storage

- **Organization author:** the full name as a single-field Zotero creator ("Massachusetts Department of Public Utilities").
- **Short form:** one line in Extra, `tex.shortauthor: MA DPU`. It renders in body citations ("MA DPU (2024)") and after the full name in the bibliography. Organizations that don't use one have no line.
- **Citation key:** one line in Extra, `Citation Key: madpu_Docket23150Order_2024`. Only items with this line reach `references.yaml`. Keys are assigned once (by the cleanup, or by ingest after the details card is approved) and never regenerated. Better BibTeX is not used; Zotero's native Citation Key field is left empty.
- **Publisher and institution:** full names, and only when they name a different organization from the author (the venue, the agency a filing went to, the lab that published a person's paper). A publisher that repeats the author is removed.
- **People:** two-field creators (last name, first name). A person stored as one field is split.

## Choosing the full name

- The **entity that issued the document**: the operating company that filed it, not its parent.
- Its **most recent name**, on every item regardless of publication date (NREL's 2018 reports and its 2026 CAIRO release are both "National Laboratory of the Rockies"). This applies to the same continuing organization under a new name; a document issued by a company later absorbed into a different company keeps its original issuer.
- A **subsidiary of a branded parent** is named **parent brand + territory** ("National Grid Upstate", "Eversource Connecticut") where the parent markets it that way; otherwise the company's own name, without "d/b/a". See the subsidiary table below.
- Drop a leading "The" and trailing "Inc.", "LLC", "Ltd." and "plc". Keep "Company" and "Corporation" when they are part of the name. Use "&" or "and" as the organization does.
- Correct typos and wrong names from the document or the organization's website, never from other spellings in the library.

## Choosing the short form (in priority order)

1. **The organization's own abbreviation**: its website, or the term the document defines ("Niagara Mohawk Power Corporation d/b/a National Grid ("NiMo" or the "Company")"). Record the evidence.
2. **Common usage** where it clearly serves readers better (ConEd).
3. **A state prefix** for generic agency abbreviations (DPU, PSC, PUC, DEP, DEC, DPS, BPU): "<state> <abbreviation>" with a space, as in MA DPU, NY PSC, RI PUC, MD PSC, NJ BPU, NY DEC. Distinctive names keep their own form (NYSERDA, NYISO, CT DEEP, ISO-NE). Bare "DPU", "PSC", "PUC", "DEC" and "DPS" are never valid.
4. **No short form** if the organization doesn't use one. Never invent one ("BGC" and "BUG" fail this test).
5. A short form may be a **short name** rather than an acronym ("Nicor Gas", "Peoples Gas", "National Fuel").
6. **One short form, one full name.** `sync-bib`'s checks enforce this.

## Sub-units, several organizations, organizations with people

- **Sub-units:** use the most specific unit named as author. ICC Staff is not the ICC; NY DPS is not NY PSC; EIA is not DOE. Series, programs and websites ("Today in Energy", "Mass Save", "Mass.gov") are not organizations.
- **Several organizations:** one creator per organization. The item's short form joins theirs Chicago-style ("NYSEG and RG&E"; "NYSERDA et al." for four or more).
- **Organizations plus people** (mostly testimony): normalize the organization's name and set no short form.
- **Known collisions:** MA DPU versus RI DPUC; NY PSC versus MD PSC; "MPSC" means Maryland here and Michigan elsewhere (use MD PSC).

## Subsidiaries

Separate legal companies stay separate, in the full name and the short form. The parent is the author only of its own documents (10-Ks, corporate sites, investor material). Joint filings by two companies get one creator per company. "(verify)" means the short form still needs evidence from a filing or the company's website.

| legal company                                                         | parent                         | full name                                  | short form              | key part                        |
| --------------------------------------------------------------------- | ------------------------------ | ------------------------------------------ | ----------------------- | ------------------------------- |
| Niagara Mohawk Power Corporation                                      | National Grid                  | National Grid Upstate                      | NiMo                    | `nimo`                          |
| The Brooklyn Union Gas Company                                        | National Grid                  | National Grid New York                     | KEDNY                   | `kedny`                         |
| KeySpan Gas East Corporation                                          | National Grid                  | National Grid Long Island                  | KEDLI                   | `kedli`                         |
| Massachusetts Electric Company                                        | National Grid                  | National Grid Massachusetts Electric       | Mass Electric (verify)  | `masselectric`                  |
| Nantucket Electric Company                                            | National Grid                  | National Grid Nantucket Electric           | (none)                  | `nationalgridnantucketelectric` |
| Boston Gas Company (incl. former Colonial Gas)                        | National Grid                  | National Grid Massachusetts Gas            | Boston Gas (verify)     | `bostongas`                     |
| New England Power Company                                             | National Grid                  | New England Power                          | NEP (verify)            | `nep`                           |
| The Narragansett Electric Company                                     | PPL (National Grid until 2022) | Rhode Island Energy                        | RIE                     | `rie`                           |
| National Grid USA, National Grid plc                                  |                                | National Grid                              | (none)                  | `nationalgrid`                  |
| The Connecticut Light and Power Company                               | Eversource                     | Eversource Connecticut                     | CL&P                    | `clp`                           |
| Yankee Gas Services Company                                           | Eversource                     | Eversource Connecticut Gas                 | Yankee Gas              | `yankeegas`                     |
| NSTAR Electric Company                                                | Eversource                     | Eversource Massachusetts                   | NSTAR Electric (verify) | `nstarelectric`                 |
| NSTAR Gas Company                                                     | Eversource                     | Eversource Eastern Massachusetts Gas       | NSTAR Gas (verify)      | `nstargas`                      |
| Eversource Gas Company of Massachusetts (formerly Columbia Gas of MA) | Eversource                     | Eversource Gas Company of Massachusetts    | EGMA (verify)           | `egma`                          |
| Eversource Energy                                                     |                                | Eversource                                 | (none)                  | `eversource`                    |
| Consolidated Edison Company of New York                               | Consolidated Edison            | Consolidated Edison Company of New York    | ConEd                   | `coned`                         |
| Orange and Rockland Utilities                                         | Consolidated Edison            | Orange and Rockland Utilities              | O&R                     | `or`                            |
| Consolidated Edison, Inc.                                             |                                | Consolidated Edison                        | (none)                  | `consolidatededison`            |
| New York State Electric & Gas Corporation                             | Avangrid                       | New York State Electric & Gas              | NYSEG                   | `nyseg`                         |
| Rochester Gas and Electric Corporation                                | Avangrid                       | Rochester Gas and Electric                 | RG&E                    | `rge`                           |
| Central Maine Power Company                                           | Avangrid                       | Central Maine Power                        | CMP                     | `cmp`                           |
| The United Illuminating Company                                       | Avangrid                       | United Illuminating Company                | UI                      | `ui`                            |
| Connecticut Natural Gas Corporation                                   | Avangrid                       | Connecticut Natural Gas                    | CNG                     | `cng`                           |
| The Southern Connecticut Gas Company                                  | Avangrid                       | Southern Connecticut Gas Company           | SCG                     | `scg`                           |
| The Berkshire Gas Company                                             | Avangrid                       | Berkshire Gas Company                      | Berkshire Gas (verify)  | `berkshiregas`                  |
| Avangrid, Inc.                                                        | Iberdrola                      | Avangrid                                   | (none)                  | `avangrid`                      |
| Public Service Electric and Gas Company                               | PSEG                           | Public Service Electric and Gas Company    | PSE&G                   | `pseg`                          |
| PSEG Long Island LLC                                                  | PSEG                           | PSEG Long Island                           | PSEG LI (verify)        | `psegli`                        |
| Public Service Enterprise Group                                       |                                | Public Service Enterprise Group            | PSEG                    | `pseg`                          |
| Baltimore Gas and Electric Company                                    | Exelon                         | Baltimore Gas and Electric Company         | BGE                     | `bge`                           |
| Potomac Electric Power Company                                        | Exelon                         | Potomac Electric Power Company             | Pepco                   | `pepco`                         |
| The Potomac Edison Company                                            | FirstEnergy                    | Potomac Edison Company                     | Potomac Edison          | `potomacedison`                 |
| Central Hudson Gas & Electric Corporation                             | Fortis                         | Central Hudson Gas & Electric              | Central Hudson          | `centralhudson`                 |
| Northern Illinois Gas Company                                         | Southern Company Gas           | Northern Illinois Gas Company              | Nicor Gas               | `nicorgas`                      |
| The Peoples Gas Light and Coke Company                                | WEC Energy Group               | Peoples Gas Light and Coke Company         | Peoples Gas             | `peoplesgas`                    |
| North Shore Gas Company                                               | WEC Energy Group               | North Shore Gas Company                    | North Shore Gas         | `northshoregas`                 |
| Ameren Illinois Company                                               | Ameren                         | Ameren Illinois                            | (none)                  | `amerenillinois`                |
| National Fuel Gas Distribution Corporation                            | National Fuel Gas Company      | National Fuel Gas Distribution Corporation | National Fuel           | `nationalfuel`                  |
| National Fuel Gas Company                                             |                                | National Fuel Gas Company                  | NFG                     | `nfg`                           |
| Liberty Utilities (St. Lawrence Gas) Corp.                            | Algonquin (Liberty)            | Liberty New York (verify)                  | (none)                  | `libertynewyork`                |
| Liberty Utilities (New England Natural Gas Company) Corp.             | Algonquin (Liberty)            | Liberty Massachusetts (verify)             | (none)                  | `libertymassachusetts`          |
| Fitchburg Gas and Electric Light Company                              | Unitil                         | Unitil Massachusetts (verify)              | FG&E (verify)           | `fge`                           |
| Unitil Corporation                                                    |                                | Unitil                                     | (none)                  | `unitil`                        |

## Renamed organizations

- **NREL** is now the **National Laboratory of the Rockies** (NLR, verify the short form).
- **The Narragansett Electric Company** (National Grid until 2022) is now **Rhode Island Energy** (RIE).
- **Columbia Gas of Massachusetts** is now **Eversource Gas Company of Massachusetts**.
- **Rocky Mountain Institute** is now **RMI**; **Gas Technology Institute** is now **GTI Energy**. Gannett Fleming merged into GFT (check whether that is a rename or a successor).

Report prose is not changed when an organization is renamed; only citations change.

## Citation keys

Format: `{author}_{title}_{year}{suffix}`, implemented in `lib/sources/citekeys.py` (`propose_key`, `assign_keys`).

- **Author part**, from the first creator (authors, then editors, then other types): an organization's short form, lowercased and stripped to `a-z0-9` (MA DPU gives `madpu`, ISO-NE `isone`, CL&P `clp`, O&R `or`); else its squashed full name (`bostongascompany`); for several organizations, the first one's part only; for a person, the family name, folded to ASCII with spaces, hyphens and apostrophes removed (Pérez-Arriaga gives `perezarriaga`). Every item needs a reviewed author; there is no anonymous fallback.
- **Title part:** Better BibTeX's `shorttitle(3,3)`: the first three words of the full title that aren't stop words, with "." and "&" removed between letters or digits, hyphens and apostrophes removed inside words, and each word's first letter uppercased ("Docket 23-150: Order" gives `Docket23150Order`).
- **Year part:** the 4-digit year of the item's date, or `nd` when no date can be found.
- **Collisions:** items with the same base key are ordered by date (missing dates last), then title, then Zotero item key, and take the base, then `a`, `b`, ..., `z`, `aa`. Once keys are locked, a new item takes the next free key; existing keys never shift.

The cleanup computes every key from scratch from the reviewed metadata, then locks it. After that, keys change only by a deliberate rename recorded in `reports/citekey_renames.csv`, applied to reports with `just rekey-refs`.
