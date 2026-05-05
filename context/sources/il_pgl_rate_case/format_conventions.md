# Illinois ICC Expert Testimony — Mechanical Format Conventions

Conventions observed across the 10 exemplar testimonies in `reports/il_npa/sources/` (ICC Docket Nos. 23-0068 / 23-0069, PGL & North Shore Gas rate cases, 2023–2024). Witness shorthand follows `_scratch/exemplar_inventory.md`.

> **Note on line numbers.** The original PDFs number every transcript line (1–28 or so per page) — the standard locator for ICC testimony. Those per-line numbers were stripped during extraction (each source file's front-matter calls this out). Citations below give the **markdown line number** of the source file, not the original PDF page or line. Page boundaries appear in the markdown as `---` horizontal rules.

Filename shorthand used in citations (suffix `.md` omitted):

| Short tag          | File                                                      |
| ------------------ | --------------------------------------------------------- |
| `cebulko-direct`   | `icc_23-0069_direct_testimony_pio_cebulko.md`             |
| `schott-direct`    | `icc_23-0069_direct_testimony_pio_schott.md`              |
| `dismukes-direct`  | `icc_23-0069_direct_testimony_ag_dismukes.md`             |
| `cebulko-rebuttal` | `icc_23-0069_rebuttal_testimony_pio_cebulko.md`           |
| `elder-rebuttal`   | `icc_23-0069_rebuttal_testimony_pio_elder.md`             |
| `leyko-rebuttal`   | `icc_23-0069_rebuttal_testimony_cub_pcr_chicago_leyko.md` |
| `deleon-rebuttal`  | `icc_23-0069_rebuttal_testimony_chicago_deleon.md`        |
| `rabago-rebuttal`  | `icc_23-0069_rebuttal_testimony_chicago_rabago.md`        |
| `walker-rebuttal`  | `icc_23-0069_rebuttal_testimony_ag_walker.md`             |
| `effron-rehearing` | `icc_23-0069_rehearing_direct_testimony_ag_effron.md`     |

## 1. Cover page and docket caption

Every filing opens with the same fixed front matter, in this order:

1. Centered headers `STATE OF ILLINOIS` / `ILLINOIS COMMERCE COMMISSION`.
2. The docket caption — usually a **three-column table** (utility + brief description of the proceeding | closing parenthesis `)` | docket number). Both consolidated dockets are listed in the **same caption table**, stacked as separate rows. The right-hand column carries `(consol.)` or `(cons.)` next to whichever docket is treated as the consolidated one.
3. A bold all-caps title block: `[DIRECT|REBUTTAL] TESTIMONY OF [WITNESS NAME]`, then `ON BEHALF OF`, then party (often itself broken into multiple lines for coalitions).
4. The exhibit identifier (e.g., `AG Exhibit 2.00`) and filing date.

How both utilities are represented in a single caption (verbatim two-row pattern):

- North Shore on top with `Docket No. 23-0068`, PGL below with `Docket No. 23-0069 (cons.)` — `cebulko-direct` (lines 16–24 in the source after extraction; same shape in `schott-direct` lines 19–24, `cebulko-rebuttal` lines 19–24, `deleon-rebuttal` lines 20–23, `leyko-rebuttal` lines 23–31).
- North Shore on top with `Docket No. 23-0068 (consol.)`, PGL below with `Docket No. 23-0069` — `dismukes-direct` lines 20–26.
- Effron's caption uses a **two-column table** — the parens column is omitted entirely. Both utility-name/description blocks are stacked within the left cell, and both docket numbers (with `(consol.)` between them) are stacked within the right cell — `effron-rehearing` lines 18–20.
- Walker combines both utility names into adjacent rows then stacks the two dockets in the right column with `(consol.)` on its own line — `walker-rebuttal` lines 19–26.

Title-block examples (bold, all-caps, witness name on its own line):

- `**REBUTTAL TESTIMONY OF KARL R. RÁBAGO** ... **ON BEHALF OF** ... **THE CITY OF CHICAGO**` — `rabago-rebuttal` lines 30–38.
- `**DIRECT TESTIMONY OF** ... **DAVID E. DISMUKES, PH.D.** ... **ON BEHALF OF** ... **THE PEOPLE OF THE STATE OF ILLINOIS**` — `dismukes-direct` lines 28–34.
- `**REBUTTAL TESTIMONY OF** **CATHERINE ELDER**` — `elder-rebuttal` lines 32–33.

A Table of Contents follows the title block in every file (e.g., `cebulko-direct` lines 16–44; `dismukes-direct` lines 42–51), occasionally followed by a separate Table of Exhibits (`dismukes-direct` lines 53–71; `effron-rehearing` lines 46–49).

## 2. Witness self-introduction

Every Section I opens with a Q&A sequence that establishes name, employer, party, qualifications, and exhibits. The exact opening question wording varies; the underlying checklist is identical.

### Opening-question variants for the very first Q

The corpus uses six wordings for the opening Q. They sort along three orthogonal axes (purpose of the Q, exact noun list, casing) — see §3 for the casing/bolding axes:

| Opening Q wording (sentence order preserved)                                        | Witness                      | Citation                   |
| ----------------------------------------------------------------------------------- | ---------------------------- | -------------------------- |
| `Please state your name, business name and address.`                                | Cebulko (Direct)             | `cebulko-direct` line 50   |
| `Please state your name, business name and address.`                                | Schott (Direct)              | `schott-direct` line 66    |
| `Please state your name and business address.`                                      | Elder (Rebuttal)             | `elder-rebuttal` line 63   |
| `Please state your name and business address.`                                      | Effron (Direct on Rehearing) | `effron-rehearing` line 55 |
| `PLEASE STATE YOUR NAME AND BUSINESS ADDRESS?`                                      | Dismukes (Direct)            | `dismukes-direct` line 77  |
| `PLEASE STATE YOUR NAME AND BUSINESS ADDRESS.`                                      | Leyko (Rebuttal)             | `leyko-rebuttal` line 64   |
| `PLEASE STATE YOUR FULL NAME AND OCCUPATION.`                                       | Walker (Rebuttal)            | `walker-rebuttal` line 56  |
| `Please provide your name, title, and business address.`                            | DeLeon (Rebuttal)            | `deleon-rebuttal` line 60  |
| `Please state your name.`                                                           | Cebulko (Rebuttal)           | `cebulko-rebuttal` line 43 |
| (No name Q — opens directly with `What is the purpose of your rebuttal testimony?`) | Rábago (Rebuttal)            | `rabago-rebuttal` line 69  |

Note Dismukes's terminal `?` on what is grammatically an imperative — Dismukes's filing inconsistently ends declarative-form Qs with `?` or `.`: lines 77 and 81 (`...PLACE OF EMPLOYMENT?`) use `?`, while line 85 (`...AREAS OF EXPERTISE.`) uses `.`. This intra-witness inconsistency appears nowhere else in the corpus.

The "name and occupation" wording (Walker) is the only variant that asks about job role in the first Q rather than a separate follow-up. Most witnesses follow with the standard sequence:

1. By whom are you employed and in what capacity? (Cebulko Direct line 54; Schott line 70; Elder line 67)
2. On whose behalf are you submitting testimony? (Cebulko Direct line 58; Schott line 74)
3. Please summarize your professional experience / educational background. (Cebulko Direct line 62; Effron lines 63, 81)
4. Have you previously testified before the Illinois Commerce Commission? (Cebulko Direct line 68; Dismukes line 93; Schott line 92)
5. Have you testified or provided comments in regulatory proceedings in other states? (Cebulko Direct line 72; Schott line 96; Elder line 85)
6. Was this testimony prepared by you or directly under your supervision? (Cebulko Direct line 76)
7. Are you sponsoring any exhibits? (Cebulko Direct line 80; Schott line 100; Elder line 89; DeLeon line 80)

### Rebuttal openings

Rebuttal-witness openings collapse to two questions: name (or no name Q at all), then "Are you the same X who…":

- `Q. Are you the same Bradley Cebulko who sponsored direct testimony in this proceeding on behalf of …?` — `cebulko-rebuttal` line 47.
- `Q. ARE YOU THE SAME ROD WALKER WHO FILED DIRECT TESTIMONY IDENTIFIED AS AG EXHIBIT 3.00 IN THIS CONSOLIDATED DOCKET ON MAY 9, 2023?` — `walker-rebuttal` line 60.
- `Q. ARE YOU THE SAME JAMES A. LEYKO WHO PREVIOUSLY FILED TESTIMONY IN THIS PROCEEDING?` — `leyko-rebuttal` line 68.
- `Q. Are you the same Dr. Sol DeLeon who provided direct testimony on behalf of the City of Chicago … on May 9, 2023 in this consolidated proceeding?` — `deleon-rebuttal` line 64.

Then a `What is the purpose of your rebuttal testimony?` Q immediately after (`cebulko-rebuttal` line 51; `leyko-rebuttal` line 72; `deleon-rebuttal` line 68; `rabago-rebuttal` line 69 as the very first Q). Elder is the only rebuttal witness in the corpus who repeats the full direct-style qualifications block (`elder-rebuttal` lines 63–94) — she had not filed direct testimony in this docket. Effron's rehearing direct also uses the full direct-style intro (`effron-rehearing` lines 55–83).

The standard answer to "Are you the same…?" is one word: `Yes.` (`cebulko-rebuttal` line 49; `walker-rebuttal` line 62; `deleon-rebuttal` line 66).

## 3. Q&A format mechanics

### The three independent dimensions of Q formatting

Q lines vary along three orthogonal axes. Each witness picks one combination and uses it consistently across the entire filing.

- **Punctuation**: `Q.` (period) vs. `Q:` (colon).
- **Casing of the question text**: sentence case vs. ALL CAPS.
- **Bolding span**: label only (`**Q.**` then plain text) vs. entire line bolded as one span (`**Q. text.**`) vs. label and text bolded as two adjacent spans (`**Q.** **text.**`).

Per-witness combination (verified by reading the witness's intro and one body Q):

| Witness                   | Punct. | Casing   | Bolding span                                          | A. label-bolded?                | Example Q line                       |
| ------------------------- | ------ | -------- | ----------------------------------------------------- | ------------------------------- | ------------------------------------ |
| Cebulko (Direct)          | `Q.`   | sentence | label-only                                            | yes (`**A.**`)                  | `cebulko-direct` line 50             |
| Schott (Direct)           | `Q:`   | sentence | label-only                                            | yes (`**A:**`)                  | `schott-direct` line 66              |
| Dismukes (Direct)         | `Q.`   | ALL CAPS | label-only                                            | yes                             | `dismukes-direct` line 77            |
| Cebulko (Rebuttal)        | `Q.`   | sentence | label-only                                            | yes                             | `cebulko-rebuttal` line 43           |
| Elder (Rebuttal)          | `Q:`   | sentence | entire-line bold                                      | **no** (plain `A:`)             | `elder-rebuttal` line 63; A: line 65 |
| Leyko (Rebuttal)          | `Q.`   | ALL CAPS | label-only                                            | yes                             | `leyko-rebuttal` line 64             |
| DeLeon (Rebuttal)         | `Q.`   | sentence | label-only                                            | yes                             | `deleon-rebuttal` line 60            |
| Rábago (Rebuttal)         | `Q.`   | sentence | entire-line bold                                      | yes (`**A.**`, label-only bold) | `rabago-rebuttal` line 69            |
| Walker (Rebuttal)         | `Q.`   | ALL CAPS | entire-line bold                                      | yes (label-only bold)           | `walker-rebuttal` line 56            |
| Effron (Rehearing Direct) | `Q.`   | sentence | separately-bolded label and text (`**Q.** **text.**`) | yes                             | `effron-rehearing` line 55           |

The three axes do not collapse to a party-level rule:

- **Punctuation**: `Q.` is the dominant choice (8 of 10). `Q:` appears in two PIO filings (Schott, Elder) but the other two PIO filings (both Cebulko) use `Q.` — so it is not a PIO convention.
- **Casing**: ALL CAPS appears in three filings — Dismukes (AG), Walker (AG), Leyko (CUB/PCR/COC). The third AG filing (Effron) is sentence case, so even within the AG witnesses there is no uniform party rule.
- **Bolding span**: the four "fancy" bolding choices (entire line, separately bolded, plain answer label) appear once or twice each across different parties, with no party clustering.

### Question and answer length

- Most Q lines are a single short sentence, 5–15 words: `Please state your name.` (`cebulko-rebuttal` line 43); `What is your present occupation?` (`effron-rehearing` line 59).
- Multi-sentence framing Qs (50–150 words) appear in rebuttal testimony where the witness must summarize the opposing position before asking for response: see `rabago-rebuttal` line 85 (a single Q that runs ~75 words), and `cebulko-rebuttal` line 88 (a Q ending in "How do you respond?" after a long restatement of the Company's claim).
- One-word answers (`Yes.` / `No.`) are common for confirmation Qs: `cebulko-rebuttal` line 49 (`Yes.`), `cebulko-rebuttal` line 59 (`No.`), `effron-rehearing` line 147 (`Yes.`), `walker-rebuttal` line 62 (`Yes.`).
- Single-paragraph answers (50–250 words) are the workhorse format — see most A. blocks in `cebulko-rebuttal` lines 53–166.
- Multi-paragraph answers spanning several pages appear for substantive analytical answers. Examples: Schott's professional-experience answer at `schott-direct` lines 84–90 (four paragraphs); Cebulko's response on electrification at `cebulko-rebuttal` lines 124–166 (multiple paragraphs across several Qs).

### Volume

Q-count is roughly proportional to length but varies by analytical depth. Counted via `grep -cE '^\*\*Q[\.:]'`:

| Witness          | Q count | Source lines | Footnote count |
| ---------------- | ------- | ------------ | -------------- |
| Cebulko Direct   | 158     | 1428         | 193            |
| Schott Direct    | 49      | 544          | 40             |
| Dismukes Direct  | 72      | 661          | 52             |
| Cebulko Rebuttal | 75      | 684          | 118            |
| Elder Rebuttal   | 28      | 265          | 26             |
| Leyko Rebuttal   | 10      | 176          | 13             |
| DeLeon Rebuttal  | 47      | 477          | 66             |
| Rábago Rebuttal  | 31      | 365          | 68             |
| Walker Rebuttal  | 30      | 412          | 44             |
| Effron Rehearing | 19      | 147          | **0**          |

Effron's rehearing testimony is the only filing in the corpus with **zero footnotes** — citations are inlined as prose ("In its Amendatory Order of January 3, 2024, the Commission found a total revenue requirement of $1.005 billion…"; `effron-rehearing` line 99). Every other filing footnotes citations.

## 4. Exhibit numbering

Pattern is `[PARTY PREFIX] [Ex.|Exhibit] [Major].[Minor]`. Each party uses its own prefix and minor-number padding style.

| Party / coalition             | Prefix in cover/lead                                                                         | Sub-exhibit minor                            | Examples                                                                                                                                                                                                                                                                                                                                                                                                     |
| ----------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Public Interest Organizations | `PIO Exhibit` (cover); `PIO Ex.` (footnotes)                                                 | single-digit, no zero padding (`X.1`, `X.2`) | `PIO Exhibit 1.0` cover (`cebulko-direct` line 9), sub `PIO Exhibit 1.1`, `1.2` (lines 84–85). `PIO Exhibit 4.0` cover (`cebulko-rebuttal` line 10), sub `PIO Exhibit 4.1`–`4.4` (lines 124, 162, 166). `PIO Exhibit 7.0` cover (`elder-rebuttal` line 8), sub `PIO Exhibit 7.1`, `7.2` (lines 93–94). Schott `PIO Exhibit 3.0` cover (`schott-direct` line 5), sub `PIO Exhibit 3.1`–`3.5` (lines 104–108). |
| People of IL / Illinois AG    | `AG Exhibit` (cover); `AG Ex.` (footnotes)                                                   | zero-padded two-digit (`X.01`, `X.02`)       | `AG Exhibit 2.00` cover (`dismukes-direct` line 36), sub `AG Exhibit 2.01`–`2.17` (lines 55–71). `AG Exhibit 7.00` cover (`walker-rebuttal` line 36), sub `AG Ex. 7.01`–`7.03` (lines 74–76). `AG Exhibit 9.00` cover (`effron-rehearing` line 30), sub `AG Exhibit 9.01`, `9.02` (lines 48–49).                                                                                                             |
| City of Chicago               | `City of Chicago Exhibit` or `COC Exhibit` (cover); body uses either `City Ex.` or `COC Ex.` | zero-padded two-digit (`X.01`, `X.02`)       | `City of Chicago Exhibit 3.0` cover (`deleon-rebuttal` line 31), sub `City Exhibit 3.01`–`3.04` (lines 51–54). `City of Chicago ("COC") Exhibit 4.0` cover (`rabago-rebuttal` line 40), sub `COC Exhibit 4.01`–`4.08`, plus `COC Group Exhibit 4.04` for grouped attachments (lines 56–63).                                                                                                                  |
| CUB / PCR / Chicago joint     | `CUB/PCR/Chicago Exhibit`                                                                    | (no sub-exhibits in this file)               | `CUB/PCR/Chicago Exhibit 4.0` cover (`leyko-rebuttal` line 18).                                                                                                                                                                                                                                                                                                                                              |

**Intra-party prefix variation.** The City of Chicago witnesses do not pick one short form: DeLeon uses `City Ex.` in the body (`deleon-rebuttal` lines 51–54, 107) while Rábago uses `COC Ex.` throughout (`rabago-rebuttal` lines 56–63, 99–105). Both files put the long form `City of Chicago [("COC")] Exhibit X.0` on the cover. The AG corpus has a single observed inconsistency: Walker's footnotes alternate `AG Ex. 7.01` (`walker-rebuttal` line 124) with `AG Ex. 7.2` (line 224) — same exhibit number, two different minor-padding styles in one filing.

**Cross-witness exhibit references.** Companies' exhibits are cited as `NS-PGL Ex. X.0` for joint rebuttal exhibits and as `PGL Ex. X.X` / `NS Ex. X.X` for company-specific direct exhibits:

- `NS-PGL Ex. 12.0 at 16` (`cebulko-rebuttal` line 567, footnote 1).
- `PGL Ex. 2.4 at 17 and NS Ex. 2.4 at 17` (`leyko-rebuttal` line 162, footnote 6).

ICC Staff exhibits use `Staff Ex. X.0`. Revisions are flagged with the `REV` suffix: `NS-PGL Ex. 17.0 REV at 14:250-251` (`rabago-rebuttal` line 174, footnote 15).

## 5. Citations to other testimony

Citations almost always live in **footnotes**, not inline. Body prose names the witness ("Witness Eidukas testifies…"); the exhibit-number page locator is dropped to a footnote. Three formats coexist.

### Long form (typically the first reference to a given witness)

> `Rebuttal Testimony of Theodore Eidukas, NS-PGL Ex. 12.0 at 16.` — `cebulko-rebuttal` line 567 (footnote 1).
> `Rebuttal Testimony of Frank C. Graves, NS-PGL Ex. 22.0 at 5-6.` — `cebulko-rebuttal` line 568 (footnote 2).
> `*See* DeLeon direct testimony, City Ex. 1.0 at 4:89 to 12:229 (describing federal, state, and city initiatives that are driving electrification).` — `deleon-rebuttal` line 107 (footnote 2).

### Short form, page-only locator (for re-cites and informal references)

> `NS-PGL Ex. 22.0 at 18` — `cebulko-rebuttal` line 578 (footnote 12).
> `PIO Ex. 1.0 at 13` — `cebulko-rebuttal` line 595 (footnote 29).
> `*Id.*, at 8-9.` — `leyko-rebuttal` line 156 (footnote 3) — `Id.` for the immediately preceding citation.
> `Docket No. 20-0308, Final Order, page 60.` — `leyko-rebuttal` line 152 (footnote 1) — uses `page` instead of `at` for orders.

### Page:line locator (the precision form for cross-testimony citations)

The full form is `Ex. X.X at PAGE:LINE` or `Ex. X.X at PAGE:LINE-LINE`. Page:line locators only work because the original transcripts number every line; they do not work in the extracted markdown:

> `COC Ex. 2.0 at 10:196-198` — `rabago-rebuttal` line 153 (footnote 12).
> `NS-PGL Ex. 17.0 REV at 14:250-251` — `rabago-rebuttal` line 174 (footnote 15).
> `Nelson rebuttal testimony, NS-PGL Ex. 16.0 at 8:154` — `rabago-rebuttal` line 181 (footnote 17).
> `NS-PGL Ex. 13.0 at 21:383` — `walker-rebuttal` line 90 (footnote 1).

Multiple discontinuous ranges are concatenated with semicolons inside one citation:

> `COC Ex. 2.0 at 10:196-198; 12:226 to 14:297; 26:527 to 28:548` — `rabago-rebuttal` line 153 (footnote 12).
> `Rábago direct testimony, COC Ex. 2.0 at 21:421-427; 24:485-495; 34:664-674` — `rabago-rebuttal` line 194 (footnote 21).

A range that spans pages uses `to` (with spaces) between the two `page:line` endpoints:

> `COC Ex. 2.0 at 12:230 to 13:272` — `rabago-rebuttal` line 182 (footnote 18).
> `City Ex. 1.0 at 4:89 to 12:229` — `deleon-rebuttal` line 107 (footnote 2).

### Cross-docket citations

Citations to testimony in other ICC dockets lead with the docket number, then the standard testimony locator:

> `*See* ICC Docket 23-0066, Direct Testimony of Nicor Witness Joanne Mello, Nicor Exhibit 9.0.` — `cebulko-rebuttal` line 604 (footnote 38).
> `*See* Docket No. 23-0068-69, Direct Testimony of Justin Schott (May 9, 2023), p. 5.` — `cebulko-direct` line 1245 (footnote 193 — note `p. 5` instead of `page:line` because cross-testimony was filed on the same date and the line-numbered transcript wasn't yet standard between PIO witnesses).

### Italics conventions in citations

`*See*` and `*See, e.g.*` are used as introductory signals (`rabago-rebuttal` line 153; `deleon-rebuttal` line 107). `*Id.*` italicized with the trailing period inside the asterisks (`leyko-rebuttal` line 156; `walker-rebuttal` line 91). Document titles use italics: `*The Future of Gas Utilities Series*` (`deleon-rebuttal` line 193). `(emphasis added)` is appended in parentheses, usually outside italics (`rabago-rebuttal` line 174).

## 6. Section headers and document structure

Every testimony divides into Roman-numeral sections followed by uppercase-letter subsections (and occasionally Arabic-numeral sub-subsections). Casing of the section header text varies independently of casing of Q text.

```
I.   [Introduction / Witness Identification and Qualifications / Statement of Qualifications / Purpose and Scope]
II.  Purpose of Testimony  (often combined with I in shorter rebuttals)
III. [Substantive section 1]
...
N.   Conclusion  (omitted in some short rebuttals; the closing Q. then sits inside the last substantive section)
```

### Section-header casing per file

- **Title case** (2 of 10): Cebulko Direct (`## I. Witness Identification and Qualifications` — `cebulko-direct` line 48), Walker Rebuttal (`## I. Introduction` — `walker-rebuttal` line 54).
- **ALL CAPS** (8 of 10): Schott (`## I. WITNESS IDENTIFICATION AND QUALIFICATIONS` — `schott-direct` line 64), Dismukes (`## I. INTRODUCTION` — `dismukes-direct` line 75), Cebulko Rebuttal (`## I. INTRODUCTION` — `cebulko-rebuttal` line 41), Elder (`## I. INTRODUCTION AND WITNESS QUALIFICATIONS` — `elder-rebuttal` line 61), Leyko (`## I. INTRODUCTION` — `leyko-rebuttal` line 62), DeLeon (`## I. INTRODUCTION AND PURPOSE OF TESTIMONY` — `deleon-rebuttal` line 58), Rábago (`## I. PURPOSE AND SCOPE OF REBUTTAL TESTIMONY` — `rabago-rebuttal` line 67), Effron (`## I. STATEMENT OF QUALIFICATIONS` — `effron-rehearing` line 53).

(Section-header casing does not match Q-text casing within a witness — Cebulko Direct uses Title case headers but sentence-case Qs; Cebulko Rebuttal uses ALL CAPS headers but sentence-case Qs.)

### Subsection style

- Uppercase-letter subsections: `### A. Transmission Pipeline Benchmarking & the Clavey Rd. Project` (`walker-rebuttal` line 104), `### A. Safety Modernization Program` (in `cebulko-direct` ToC, line 24).
- Arabic-numeral sub-points: `1.`, `2.`, `3.` under `V.D.` in `cebulko-direct` (ToC lines 28–30), and `1.` through `6.` under section III in `schott-direct` (ToC lines 47–52 — note that Schott uses Arabic numerals for first-level subsections, skipping uppercase letters entirely).

### Standard opening sections

- Section I is always either `Introduction`, `Witness Identification and Qualifications`, `Introduction and Purpose of Testimony`, or `Statement of Qualifications`. Wording varies; the function (witness intro Q&A) is identical.
- Section II is most often `Purpose of Testimony` (Cebulko Direct, Schott, Cebulko Rebuttal as "REBUTTAL TESTIMONY OVERVIEW", Elder, Effron). When section I already contains the purpose Q, section II is the first substantive section (DeLeon, Rábago).
- A `Summary of Recommendations` or `Summary of Conclusions and Recommendations` section often appears second or third — `dismukes-direct` line 45 (Section II); `deleon-rebuttal` line 41 (Section II).

### Standard closing section

A final section explicitly titled `Conclusion` appears in: `schott-direct` (Section VII), `dismukes-direct` (Section VIII "CONCLUSIONS AND RECOMMENDATIONS"), `cebulko-direct` (Section X), `elder-rebuttal` (Section IV — `elder-rebuttal` line 257). Short rebuttals (Leyko, Walker, DeLeon, Rábago, Cebulko Rebuttal, Effron) skip a separate Conclusion section — the closing Q lives at the end of the last substantive section.

## 7. Closing — "Does this conclude your testimony?"

Every testimony ends with the same fixed Q&A. The closing Q's casing and bolding mirror the file's overall Q-formatting choice (§3); the testimony-type word matches the filing type exactly.

| File               | Closing Q (verbatim, with bolding markers)                          | Closing A              | Source line |
| ------------------ | ------------------------------------------------------------------- | ---------------------- | ----------- |
| `cebulko-direct`   | `**Q.** Does this conclude your direct testimony?`                  | `**A.** Yes, it does.` | line 1228   |
| `schott-direct`    | `**Q:** Does this conclude your direct testimony?`                  | `**A:** Yes, it does.` | line 458    |
| `dismukes-direct`  | `**Q.** DOES THIS CONCLUDE YOUR DIRECT TESTIMONY?`                  | `**A.** Yes.`          | line 627    |
| `cebulko-rebuttal` | `**Q.** Does this conclude your rebuttal testimony?`                | `**A.** Yes, it does.` | line 559    |
| `elder-rebuttal`   | `**Q: Does this conclude your rebuttal testimony?**`                | `A: Yes, it does.`     | line 263    |
| `leyko-rebuttal`   | `**Q.** DOES THIS CONCLUDE YOUR REBUTTAL TESTIMONY?`                | `**A.** Yes.`          | line 142    |
| `deleon-rebuttal`  | `**Q.** Does this conclude your rebuttal testimony?`                | `**A.** Yes.`          | line 469    |
| `rabago-rebuttal`  | `**Q. Does this conclude your rebuttal testimony?**`                | `**A.** Yes.`          | line 363    |
| `walker-rebuttal`  | `**Q. DOES THIS CONCLUDE YOUR REBUTTAL TESTIMONY?**`                | `**A.** Yes.`          | line 410    |
| `effron-rehearing` | `**Q.** **Does this conclude your Direct Testimony on Rehearing?**` | `**A.** Yes.`          | line 145    |

The answer is invariably `Yes.` or `Yes, it does.` — never elaborated.

The phrase `[testimony type] testimony` tracks the filing type exactly: `direct testimony`, `rebuttal testimony`, or `Direct Testimony on Rehearing`. The Effron file is the one place the testimony-type words are themselves bolded as part of the Q text.

## 8. Other observed conventions

- **A. label bolding follows Q. label bolding within each file**, with one exception: Elder bolds the entire Q line as a single span (`**Q: ...**`) but leaves the A. label and text plain (`A: My name is...` — `elder-rebuttal` lines 63 and 65). Every other file bolds both labels.
- **Footnote density** is high in substantive testimony but not uniform — see the Q/footnote count table in §3. Cebulko Direct (193 footnotes over 1,428 source lines) and Cebulko Rebuttal (118 over 684) sit at the high end; Effron (0) at the low end. Leyko's compact 11-page rebuttal still carries 13 footnotes.
- **Inline emphasis** uses italics sparingly: case names, statute names, term-of-art definitions, and citation signals (`*See*`, `*Id.*`). For example: `*i.e.*, Chicago` (`leyko-rebuttal` line 70); `*could* benefit … *will* benefit` (`leyko-rebuttal` line 132); `*therefore preserve the availability of such services to all citizens*` (`schott-direct` line 452).
- **Quoted regulatory text** is set as a Markdown blockquote (`> …`) often spanning multiple paragraphs, with citation in the trailing footnote. See `leyko-rebuttal` lines 90–94 (nested blockquote citing the ICC Order in Docket 20-0308 quoting Docket Nos. 19-0436/18-0463/18-1775); `cebulko-rebuttal` regulatory-text patterns; `schott-direct` line 452 quoting the Public Utilities Act.
- **Tables** appear inline in the markdown extracts for compact tabular content embedded in the testimony body (e.g., the docket caption itself; the `KRR-1` Basic Customer Method ECOSS results table at `rabago-rebuttal` lines 121–127; Walker's small exhibit index at `walker-rebuttal` lines 73–76). Larger or more complex tables are pushed to separate exhibits / schedules referenced by name (e.g., `AG Exhibit 9.01 Schedule 1P` — `effron-rehearing` line 103).
- **Diagrams** that are not reproducible in markdown are flagged with `[DIAGRAM DESCRIPTION: …]` brackets followed by a transcribed approximation (`cebulko-rebuttal` lines 98–100). This is an extraction artifact, not a source convention.
- **Typeset output should restore line numbers.** Page:line citation requires it, and the corpus is built around it. Each source file's "Notes on extraction" front-matter explicitly flags that per-line numbering was dropped during extraction.
