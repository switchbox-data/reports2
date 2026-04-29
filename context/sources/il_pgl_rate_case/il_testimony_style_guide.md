# Filing Expert Testimony Before the Illinois Commerce Commission: A Practical Guide

Based on **10 intervener testimonies in ICC Dockets 23-0068 / 23-0069 (cons.)** — the consolidated Peoples Gas Light & Coke Co. (PGL) and North Shore Gas Co. rate cases (2023–2024 rehearing). Witness coverage:

- **3 Direct testimonies** (May 9, 2023): Cebulko (PIO/Strategen), Schott (PIO/EEP), Dismukes (AG/Acadian).
- **6 Rebuttal testimonies** (July 17, 2023): Cebulko (PIO), Elder (PIO/Aspen), Leyko (CUB-PCR-COC/Brubaker), DeLeon (COC/Synapse), Rábago (COC/Rábago Energy), Walker (AG/Rod Walker & Associates).
- **1 Direct on Rehearing** (March 5, 2024): Effron (AG).

Frame everything below as **observed in this corpus** — 10 filings from one consolidated docket family, 9 distinct witnesses across 4 intervener parties — not universal Illinois ICC practice. A different docket, a different procedural posture, or a different witness scope could materially change what is appropriate.

This guide adapts the Switchbox Rhode Island testimony style guide (`context/methods/testimony_style_guide.md`); convergences with Rhode Island practice are noted inline, divergences are flagged and the Illinois practice is followed.

---

## Format basics

**Q&A format is mandatory.** Every sentence is framed as an answer to a question you asked yourself. Same convention as Rhode Island.

**There is no ICC-mandated Q/A style.** The Illinois corpus shows real per-witness variation along **three independent axes** (verified for all 10 filings; see `_scratch/format_conventions.md` §3 for the full table):

- **Punctuation**: `Q.` (period) vs. `Q:` (colon). Period dominates (8 of 10); colon appears in two PIO filings (Schott, Elder) but not the other two PIO filings (both Cebulko), so it is not a party convention.
- **Casing of question text**: sentence case vs. ALL CAPS. ALL CAPS appears in three filings (Dismukes/AG, Walker/AG, Leyko/CUB-PCR-COC); the AG's third filing (Effron) is sentence case, so the choice does not collapse to a party rule.
- **Bolding span**: label only (`**Q.** then plain text`), entire line bolded as one span (`**Q. text.**`), or label and text bolded as two adjacent spans (`**Q.** **text.**`).

Examples (each witness picks one combination and uses it consistently across the entire filing):

- **Label-only, sentence case, period** (Cebulko Direct line 50; Cebulko Rebuttal line 43; DeLeon line 60):
  > **Q.** Please state your name.
  >
  > **A.** My name is Bradley Cebulko.

- **Label-only, sentence case, colon** (Schott line 66):
  > **Q:** Please state your name, business name and address.
  >
  > **A:** ...

- **Label-only, ALL CAPS, period** (Dismukes line 77; Leyko line 64):
  > **Q.** PLEASE STATE YOUR NAME AND BUSINESS ADDRESS.
  >
  > **A.** ...

- **Entire-line bold, sentence case, colon, plain answer label** (Elder lines 63, 65 — Elder is the only filing with plain `A:`):
  > **Q: Please state your name and business address.**
  >
  > A: My name is Catherine Elder.

- **Entire-line bold, ALL CAPS** (Walker line 56):
  > **Q. PLEASE STATE YOUR FULL NAME AND OCCUPATION.**

- **Separately bolded label and text** (Effron line 55, the only filing in this style):
  > **Q.** **Please state your name and business address.**

The Rhode Island guide recommends picking the NERI label-only style "as the most modern and readable." Illinois practice does not converge on a single recommended style. Pick one combination of the three axes and use it consistently throughout the filing — whichever combination, the corpus shows it will look at home.

**Line numbers on every page.** The filed PDFs number every transcript line in the left margin (1–28 or so per page) — the standard locator for ICC testimony, used in `Ex. X.X at PAGE:LINE` cross-references (see Citations below). Per-line numbers were stripped during markdown extraction; restore them at typeset.

**Table of Contents** appears in every file in the corpus, immediately after the title block. A separate **Table of Exhibits** follows in some filings (Dismukes lines 53–71; Effron lines 46–49) but not all.

**Section headers.** Roman-numeral primary sections (`## I.`, `## II.`), uppercase-letter or Arabic-numeral subsections (`### A.`, `### 1.`). Section-header casing varies independently of Q-text casing — 2 of 10 filings use Title Case headers (Cebulko Direct, Walker Rebuttal), 8 of 10 use ALL CAPS. Cebulko Direct uses Title-case headers but sentence-case Qs; Cebulko Rebuttal uses ALL CAPS headers but sentence-case Qs (`format_conventions.md` §6).

---

## The cover page and consolidated-docket caption

This section has no Rhode Island analog — the RI corpus is one docket per filing.

Every Illinois filing in the corpus opens with the same fixed front matter:

1. Centered headers `STATE OF ILLINOIS` / `ILLINOIS COMMERCE COMMISSION`.
2. The docket caption, listing **both consolidated dockets in the same caption table**, stacked as separate rows.
3. Bold all-caps title block: `[DIRECT|REBUTTAL] TESTIMONY OF [WITNESS NAME]`, then `ON BEHALF OF`, then party (often broken across multiple lines for coalitions).
4. Exhibit identifier (e.g., `AG Exhibit 2.00`) and filing date.

The consolidated-caption pattern itself varies (`format_conventions.md` §1):

- **North Shore on top, PGL below, three-column table** (utility | `)` | docket): the dominant pattern, e.g., `cebulko-direct` lines 16–24, `schott-direct` lines 19–24, `cebulko-rebuttal` lines 19–24, `deleon-rebuttal` lines 20–23, `leyko-rebuttal` lines 23–31. Right-hand column carries `(consol.)` or `(cons.)` next to whichever docket is treated as consolidated.
- **PGL on top, North Shore-first ordering reversed**: Dismukes uses `Docket No. 23-0068 (consol.)` for North Shore, `Docket No. 23-0069` for PGL (`dismukes-direct` lines 20–26).
- **Two-column table**, parens column omitted, both utilities stacked in left cell and both dockets stacked in right cell with `(consol.)` between them: Effron (`effron-rehearing` lines 18–20).
- **Combined utility names then stacked dockets** with `(consol.)` on its own line: Walker (`walker-rebuttal` lines 19–26).

The corpus does not show one "correct" caption layout. The function is the same: list both dockets, mark the consolidation. Pick whichever layout matches the rest of your party's filings if there is one.

---

## Direct vs. Rebuttal vs. Direct on Rehearing

This section has no Rhode Island analog — the RI corpus is direct-only. Form-level differences in the Illinois corpus matter at the planning stage and shape every section that follows. Drawn from `_scratch/direct_vs_rebuttal.md` and verified against the source files.

| Form                | n | Mean pages | Mean Q-count | Mean footnotes | Footnotes per Q | Footnotes per source line |
| ------------------- | - | ---------: | -----------: | -------------: | --------------: | ------------------------: |
| Direct              | 3 |       65.7 |         93.0 |           95.0 |            1.02 |                     0.108 |
| Rebuttal            | 6 |       27.3 |         36.8 |           55.8 |            1.52 |                     0.141 |
| Direct on Rehearing | 1 |       10.0 |         19.0 |            0.0 |            0.00 |                     0.000 |

Means across small samples (Direct n=3, Rebuttal n=6) with substantial within-form variation; Cebulko Direct (118 pp, 158 Qs) and Cebulko Rebuttal (56 pp, 75 Qs) are both ≈2× their respective form means.

### Openings

- **Direct openings rebuild the witness from scratch.** The first 5–7 Qs ask name/employer, party, professional background, prior ICC testimony, prior testimony in other states, sponsorship of the testimony, and exhibits sponsored. Cebulko Direct walks through all seven; Schott and Dismukes use compressed variants. Same convention as Rhode Island's "canned questions."
- **Rebuttal openings collapse to two Qs.** A name Q (or none — Rábago opens with `What is the purpose of your rebuttal testimony?` at line 69), then a one-line incorporation:
  > **Q.** Are you the same Bradley Cebulko who sponsored direct testimony in this proceeding on behalf of …?
  >
  > **A.** Yes.

  Cebulko Rebuttal line 47; Walker line 60; Leyko line 68; DeLeon line 64. The standard answer is one word. This adoption-by-reference does the work of the full direct-style qualifications block.

  **Exception**: Elder filed Rebuttal but no Direct in this docket (she filed in the parallel Nicor 23-0066 case), so her Rebuttal opens with a full Direct-style qualifications block (`elder-rebuttal` lines 63–94). The abbreviated opening is a function of _prior filing in this proceeding_, not of the Rebuttal label itself.

- **Direct on Rehearing opens like a Direct, not a Rebuttal.** Effron rebuilds qualifications from scratch (`effron-rehearing` lines 55–83) even though the AG had previously filed Direct from a different witness (Dismukes). The "are you the same…" shortcut requires same-witness continuity that a rehearing on a new issue with a new witness does not have.

### Establishing scope

- **Direct establishes its own scope.** The Section II `Purpose of Testimony` Q is answered by listing the issues the witness will analyze. The Companies are the _subject_ of analysis, not the interlocutor.
- **Rebuttal establishes scope by naming the opposing witnesses and exhibits being responded to.** Section structure is built around opposing witnesses (Walker §§ II–IV `Response to NS/PGL Witness Zgonc`, `Response to NS/PGL Witnesses Eldringhoff & Eidukas`, `Response to NS/PGL Witness Weber`; Rábago §§ III–V `Response to PGL Witness Egelhoff`, `Response to PGL Witness Nelson`, `Response to ICC Staff Witness Harden`). The scope-Q recital lists rebutted exhibits by number (Cebulko Rebuttal: PGL/NS Exs. 12.0, 14.0, 17.0, 21.0, 22.0; Elder reviews NS-PGL Exs. 19.01–19.04). The architecture is witness-by-witness, not topic-by-topic.
- **Direct on Rehearing establishes scope by responding to a specific Commission order.** Effron's Section II opens by reciting the Commission's Amendatory Order of January 3, 2024 ($1.005 billion total revenue requirement) and naming the post-order PGL filing (Direct on Rehearing, February 6, 2024) the AG is responding to. Structurally a Direct (full intro), functionally a narrow response to an order-defined question.

### Two stock Rebuttal devices that Direct does not use

1. **The no-modification beat.** Cebulko Rebuttal: `Does anything in the direct testimony filed by Staff and other intervening parties, or the rebuttal testimony filed by Peoples Gas, cause you to modify the recommendations you made in direct testimony? — No.` (`cebulko-rebuttal` lines 57–59). Locks prior positions in place without re-litigating them.
2. **The silence-is-not-agreement disclaimer.** Leyko: `My silence with respect to any position taken by the Companies … should not be construed as agreement` (`leyko-rebuttal` line 74). Same boilerplate in DeLeon footnote 1 and Rábago footnote 1. Hedge against being deemed to have conceded by omission. Same device as the Rhode Island Tillman disclaimer.

### Same-witness Direct → Rebuttal evolution (Cebulko, n=1)

Only Cebulko has both forms in the corpus, so this is illustrative rather than canonical. The Rebuttal is roughly half the length on every length axis (47% of pages, Qs, and source lines), but the citation pool only shrinks to 61% — the Rebuttal is denser per Q (1.57 vs. 1.22) and per line. Scope narrows from 8 substantive sections (Direct §§ III–X) to 1 (Rebuttal §III). Citation mix shifts toward the rebutted record: the Rebuttal's first 12 footnotes (`cebulko-rebuttal` lines 567–578) are almost entirely `Rebuttal Testimony of [Witness], NS-PGL Ex. X.0 at PAGE`. The substantive frame carries over; the Rebuttal concentrates the existing thesis and weaponizes it against specific opposing witnesses.

### Effron's Direct on Rehearing as a distinct form (n=1)

10 pages, 19 Qs, **zero footnotes** — the only filing in the corpus with no footnotes. All citations are inline prose: `In its Amendatory Order of January 3, 2024, the Commission found a total revenue requirement of $1.005 billion…` (`effron-rehearing` line 99). Schedules referenced by name (`AG Exhibit 9.01 Schedule 1P`) inside Q&A text. Three sections only: Statement of Qualifications, Purpose of Testimony, Revenue Requirement of Incremental Plant. No statutes, no prior orders by docket number, no external authorities — and the filing was accepted. A corpus-of-one observation, not a generalizable pattern.

### Surrebuttal — not in this corpus

No surrebuttals appear. Standard ICC practice schedules a surrebuttal round after rebuttal, but the exemplar set was assembled around Direct, Rebuttal, and Rehearing. Any claim about surrebuttal form is speculative until exemplars are added.

---

## How long should things be?

**Total testimony.** The Illinois corpus is wider than the Rhode Island range:

| Form                | Page range (n) | Q-count range |
| ------------------- | -------------- | ------------- |
| Direct              | 39–118 (3)     | 49–158        |
| Rebuttal            | 11–56 (6)      | 10–75         |
| Direct on Rehearing | 10 (1)         | 19            |

Cebulko Direct (118 pp covering 8 substantive sections) sits at the top end; Leyko Rebuttal (11 pp, 10 Qs, single-issue scope) at the bottom. Effron's 10-page Rehearing is the absolute floor.

**Question count is roughly proportional to length but varies by analytical depth.** Verified counts (`format_conventions.md` §3):

| Witness          | Q count | Source lines | Footnotes |
| ---------------- | ------- | ------------ | --------- |
| Cebulko Direct   | 158     | 1428         | 193       |
| Schott Direct    | 49      | 544          | 40        |
| Dismukes Direct  | 72      | 661          | 52        |
| Cebulko Rebuttal | 75      | 684          | 118       |
| Elder Rebuttal   | 28      | 265          | 26        |
| Leyko Rebuttal   | 10      | 176          | 13        |
| DeLeon Rebuttal  | 47      | 477          | 66        |
| Rábago Rebuttal  | 31      | 365          | 68        |
| Walker Rebuttal  | 30      | 412          | 44        |
| Effron Rehearing | 19      | 147          | 0         |

**Answer length.** Same range as Rhode Island. One-word `Yes.` / `No.` answers are common for confirmation Qs (`cebulko-rebuttal` line 49 `Yes.`; line 59 `No.`; `effron-rehearing` line 147 `Yes.`). Single-paragraph answers (50–250 words) are the workhorse format. Multi-paragraph answers spanning several pages appear for substantive analytical answers (Schott's professional-experience answer at `schott-direct` lines 84–90; Cebulko's electrification response at `cebulko-rebuttal` lines 124–166).

**Multi-sentence framing Qs (50–150 words)** appear in rebuttal where the witness must summarize the opposing position before asking for response (Rábago line 85; Cebulko Rebuttal line 88). This is rebuttal-specific — Direct keeps Qs short.

The Rhode Island guide recommends "do not write essays … if an answer exceeds ~250 words, break it into multiple Q&A pairs." Illinois corpus practice is consistent with this advice; long uninterrupted answers are uncommon.

---

## How to structure a Q&A argument

The Rhode Island guide's two-pattern frame (a) responding to the Company's position vs. (b) advancing your own proposal applies in Illinois practice as well. The Illinois corpus adds a recurring **four-step rhetorical arc** specific to rebuttal-stage argument-building (drawn from `_scratch/tone_and_rhetoric.md` §7).

### The four-step arc within a single sustained argument

1. **Opening framing question.** "Please summarize your direct testimony regarding X" (Cebulko Rebuttal line 237; Rábago Rebuttal line 85) or "Please summarize [Company witness]'s concerns regarding your X" (Walker Rebuttal line 106). Anchors the section to the witness's existing record before engaging the Company.
2. **Evidentiary build.** 2–6 Qs that walk through the Company's response, the witness's allies, and any new evidence. Often introduced by Qs that quote the Company witness directly so the dispute is framed verbatim.
3. **Pivot to disagreement.** A Q ending `How do you respond?` or `Was the explanation sufficient?` The A typically opens with `No.` or `I disagree.`, then runs into legal terms of art only after laying out the substantive reasons. **`How do you respond?` is the workhorse Q for the pivot step** — across the four traced arcs in `_scratch/tone_and_rhetoric.md` §7, every transition from "here is the Company's position" to "here is why the Company is wrong" runs through it.
4. **Closing.** `What do you recommend?` or `Please restate your recommendation.` The closing A re-affirms the original ask, sometimes with a quantitative refinement (Walker's revised disallowance at line 198: `$1,689,222`), sometimes without (Cebulko, DeLeon). New rhetorical claims do not appear in the closing.

**Three of four traced arcs use the Company's own work as the rebuttal climax.** Cebulko quotes PGL witness Graves's 2021 Brattle report against Graves's rebuttal testimony; Rábago uses PGL's Company-generated Basic Customer Method ECOSS (produced in discovery between Direct and Rebuttal); DeLeon quotes Graves's "Future of Gas Utilities" presentation. Walker is the exception — his climax is fresh OGJ/EIA data the witness purchased and re-ran. The pattern: **let the opposing party convict itself with its own prior record where possible**.

**Footnote density is highest in the pivot step.** The Q&A doing the work of dismantling the Company's argument carries the densest footnote attribution to specific exhibit, page, and line numbers. Opening and closing steps tend to footnote prior testimony only.

### General principle, same as Rhode Island

**Finding first, methodology last.** Bury-the-lede is the most common mistake in technical testimony. Cebulko opens with `the Company has been aggressively spending` (line 262), not with how he measured spending. Rábago opens with `the price signals in rates to low users are distorted` (line 179), not with the ECOSS arithmetic.

---

## The opening sequence (canned questions)

Every Direct (and the one Rehearing Direct) walks through the same checklist (`format_conventions.md` §2 lines 70–77):

1. Name, business name, business address.
2. Employer and capacity / present occupation.
3. On whose behalf the testimony is submitted.
4. Professional experience and educational background.
5. Prior testimony before the Illinois Commerce Commission.
6. Prior testimony or comments in regulatory proceedings in other states.
7. Was the testimony prepared by you or directly under your supervision?
8. Are you sponsoring any exhibits?

Rebuttal collapses these to one or two Qs (`Are you the same X who…?` → `Yes.` → `What is the purpose of your rebuttal testimony?`).

The opening Q wording itself varies (the corpus uses six wordings — `format_conventions.md` §2). Pick whichever wording matches your party's usual style and run it consistently.

**Closing.** Every testimony ends with the same fixed Q&A (verified for all 10 in `format_conventions.md` §7):

> **Q.** Does this conclude your direct testimony?
>
> **A.** Yes, it does.

The testimony-type word matches the filing exactly: `direct testimony`, `rebuttal testimony`, or `Direct Testimony on Rehearing`. The answer is invariably `Yes.` or `Yes, it does.` — never elaborated. The closing Q's casing and bolding mirror the file's overall Q-formatting choice.

---

## Tone and voice

**First person, formal register, third person for the client.** Convergent with Rhode Island.

The Illinois corpus default is **formal, regulatory Q&A anchored in cost-of-service vocabulary** (`rate base`, `revenue requirement`, `used and useful`, `cost causation`, `ECOSS`, `imprudent`). Every witness drops into **plain-English summary mode** at least once per major section to keep the record legible — most often at the opening of a substantive section, before technical exposition, or at the close of a Q where a one-sentence takeaway is needed.

Plain-English moves embedded in formal testimony:

- `The bottom line is that the Company has been aggressively spending…` — Cebulko Direct line 262.
- `It isn't naïve to incorporate risk and trends into decision-making…` — Cebulko Rebuttal line 276.
- `Most disturbingly, customers with higher demands for gas pay less than their fair share…` — Rábago Rebuttal line 179.

### The "not a lawyer" disclaimer

A move common in the Illinois corpus that the Rhode Island guide does not flag: when the analysis touches statutory or order interpretation, witnesses **bound the scope of their expertise** with a "not a lawyer/attorney" disclaimer, then offer the witness's reading anyway.

- `While I am not a lawyer, I did not understand the Commission's order to be nearly as definitive…` — Cebulko Rebuttal line 517.
- `Although I am not a lawyer, I do not interpret the Commission's Final Order…` — Cebulko Direct line 1094.
- `While I am not an attorney, my understanding is that the burden of proof lies with the Company…` — Walker Rebuttal line 262.

### Pushing back on utility positions

Witnesses use a graduated ladder, almost never name-calling. The harshest language is reserved for **legal terms of art** (`unjust and unreasonable`, `imprudent`, `violates cost-causation principles`) or **structured findings** (`the studies do not demonstrate…`).

- **Soft disagreement** (acknowledging shared ground first): `The Company and I fundamentally disagree on several points…` — Cebulko Rebuttal line 77.
- **Hedged criticism** (`appears`, `seems`, `may`, `unclear`): `The Company's claim appears to be overstated.` — Cebulko Rebuttal line 333.
- **Direct contradiction** (`does not`, `fails to`, `is not the case`): `PGL fails to justify the magnitude of spending on these facilities.` — Elder Rebuttal line 100.
- **Strong condemnation** (legal terms of art, typically in section headers — `format_conventions.md` §6): Section II header `THE BASIC CUSTOMER METHOD ECOSS DEMONSTRATES THAT PGL'S PROPOSED FIXED CUSTOMER CHARGE IS UNJUST AND UNREASONABLE.` — Rábago Rebuttal line 83. Inline body prose stays one notch softer than the section heading.

`No.` as a standalone rhetorical pivot — a one-word `No.` answer followed by a multi-sentence justification — is a recurring move in rebuttal testimony (`cebulko-rebuttal` lines 227, 341, 353; `walker-rebuttal` line 88).

### Quantitative claims and qualifications

Numbers are bracketed by a **softening hedge** — `approximately`, `roughly`, `at least`, `no more than` — even when the figure comes straight from the utility's own data response. The hedge signals analytical care and pre-empts cross-examination on rounding or scope. The corpus does not show any unhedged round-number claims for material findings.

- `PGL proposes to add approximately $242.5 million dollars…` — Elder Rebuttal line 108.
- `Peoples Gas overspent approximately $20.4 million, or 11 percent…` — Dismukes Direct line 308.
- `At least 12 states have initiated 'future of gas' proceedings.` — DeLeon Rebuttal line 377.

When the benchmark is the witness's own analysis, the qualifier is replaced (or augmented) with a brief method-disclosure sentence (`The resulting figures were within 2% of each other, so I chose to utilize the weighted average…` — Walker Rebuttal line 171).

### Conceding points to maintain credibility

Standard concession move is **acknowledge → pivot**. Three recurring constructions:

1. `While I acknowledge X, … Y` (procedural fact → substantive challenge): `While I acknowledge the Commission has allowed recovery of RSUs in the past…` — Leyko Rebuttal line 112.
2. `It is true that X. However, Y` (prior orders or Company filings → insufficiency): `It is true that … PGL provided a description of additions to plant in service. However…` — DeLeon Rebuttal line 215.
3. `I agree with witness Z that X. However, Y` (single point to opposing witness → isolate the disputed point): `I agree with Witness Graves that policy-related issues … can take a considerable amount of time.` — Cebulko Rebuttal line 411.

**Conditional-disallowance fallback.** Where the primary recommendation is a 100% disallowance, pair it with a fallback conditioned on the Commission's rejection of the primary: `However, in the event that the Commission disagrees with my proposal to disallow one hundred percent…` — Walker Rebuttal line 364. Signals that the witness has thought through partial outcomes.

### Witness-level voice differences

Party-level groupings (PIO vs. AG vs. City vs. CUB-coalition) **mostly do not survive at the witness level** — most parties have only 1–2 witnesses and styles vary as much within parties as across them. The patterns below are individual-witness characterizations except where flagged.

- **PIO witnesses (Cebulko, Schott, Elder) — no shared voice.** Cebulko forward-looking and risk-framed (`I am concerned that…` Cebulko Direct line 152); Schott most willing to italicize for emphasis (`*unrecognized* by PGL as low-income…` Schott Direct line 156); Elder coolest and most empirical (`PGL fails to justify…` Elder Rebuttal line 100).
- **AG witnesses (Dismukes, Walker, Effron) — the one party-level pattern the corpus genuinely supports.** All three run **empirical, quantitative, comparative arguments**: Dismukes via peer-utility benchmarking (`Peoples Gas' distribution O&M expense per dekatherm was $1.29 compared to an average $0.67 for peer utilities` Dismukes Direct line 397), Walker via per-mile/inch-mile cost benchmarking, Effron via line-by-line revenue-requirement arithmetic. Cool, light on adjectives, heavy on tables.
- **City of Chicago witnesses (DeLeon, Rábago) — most assertive framing.** DeLeon ties findings to Chicago's Climate Action Plan and stranded-asset risk (`The threat of stranded assets and increased costs to consumers is real.` line 405); Rábago sharpest on rate design (`The price signals in rates to low users are distorted in favor of excess consumption…` line 179). Both willing to use legal-of-art labels in body prose.
- **CUB / PCR / City coalition (Leyko) — single witness.** Any tonal claim is a single-witness data point, not a party convention. The voice that does appear is narrowly scoped, financially disciplined, procedurally careful.

The Rhode Island guide says "measured and professional, never adversarial." Illinois practice converges on this. The Illinois ladder of pushback (soft → hedged → direct contradiction → legal-term-of-art in section headers) is more elaborate than the Rhode Island corpus shows because the Illinois corpus has six rebuttals to RI's none.

---

## How to cite things

Citations almost always live in **footnotes**, not inline body prose. Body names the witness (`Witness Eidukas testifies…`); the exhibit-number page locator drops to a footnote.

### Three coexisting footnote formats (`format_conventions.md` §5)

**Long form** (typically the first reference to a given witness):

> `Rebuttal Testimony of Theodore Eidukas, NS-PGL Ex. 12.0 at 16.` — `cebulko-rebuttal` line 567 (footnote 1).
> `*See* DeLeon direct testimony, City Ex. 1.0 at 4:89 to 12:229 (describing federal, state, and city initiatives that are driving electrification).` — `deleon-rebuttal` line 107 (footnote 2).

**Short form, page-only** (re-cites and informal):

> `NS-PGL Ex. 22.0 at 18` — `cebulko-rebuttal` line 578 (footnote 12).
> `*Id.*, at 8-9.` — `leyko-rebuttal` line 156 (footnote 3).
> `Docket No. 20-0308, Final Order, page 60.` — `leyko-rebuttal` line 152 (footnote 1) — orders use `page` instead of `at`.

**Page:line form** — the precision form for cross-testimony citations. `Ex. X.X at PAGE:LINE` or `Ex. X.X at PAGE:LINE-LINE`. Page:line locators only work because the original transcripts number every line.

> `COC Ex. 2.0 at 10:196-198` — `rabago-rebuttal` line 153 (footnote 12).
> `Nelson rebuttal testimony, NS-PGL Ex. 16.0 at 8:154` — `rabago-rebuttal` line 181 (footnote 17).

Multiple discontinuous ranges concatenated with semicolons:

> `COC Ex. 2.0 at 10:196-198; 12:226 to 14:297; 26:527 to 28:548` — `rabago-rebuttal` line 153 (footnote 12).

A range that spans pages uses `to` (with spaces):

> `COC Ex. 2.0 at 12:230 to 13:272` — `rabago-rebuttal` line 182 (footnote 18).

### Cross-docket citations

> `*See* ICC Docket 23-0066, Direct Testimony of Nicor Witness Joanne Mello, Nicor Exhibit 9.0.` — `cebulko-rebuttal` line 604 (footnote 38).
> `*See* Docket No. 23-0068-69, Direct Testimony of Justin Schott (May 9, 2023), p. 5.` — `cebulko-direct` line 1245 (footnote 193).

### Italics conventions

`*See*` and `*See, e.g.*` as introductory signals. `*Id.*` italicized with the trailing period inside the asterisks. Document titles in italics (`*The Future of Gas Utilities Series*`). `(emphasis added)` appended in parentheses, usually outside italics.

### Statutes and orders

> Public Utilities Act sections cited as `220 ILCS 5/1-102(d)`, `220 ILCS 5/8-103B`, `220 ILCS 5/9-220.3(b)`.
> Prior PGL/NS rate order: `Docket No. 14-0224/14-0225 (Consol.) Order (January 21, 2015) at 176` — `cebulko-rebuttal` footnote 117.
> Federal pipeline rules: `49 CFR Parts 191/192/195`.

### Form-specific citation patterns

(See the form-comparison section above for the underlying analysis.)

- **Direct typically leans on primary regulatory authority and external evidence** — statutes (PUA sections, CEJA, QIP statute), prior orders, the NARUC Gas Manual, the Inflation Reduction Act, federal regulations (PHMSA 49 CFR Parts 191/192/195). Brattle and EPRI are _not_ cited in any Direct in this corpus despite being substantively relevant to gas-transition arguments — they only appear in Rebuttals (Brattle in Cebulko Rebuttal and DeLeon Rebuttal; EPRI in Cebulko Rebuttal only).
- **Rebuttal typically leans on opposing-testimony page:line citations** — universal in the Rebuttals in this corpus. Rebuttals also cite primary authority where it scaffolds their argument (Leyko's incentive-comp dockets 20-0308, 18-1775, 19-0436, 18-0463; DeLeon's PUA just-and-reasonable hook), but the high-frequency citations are to the rebutted record itself.
- **Page:line citations are not strictly Rebuttal-bound.** Dismukes Direct uses page:line citations extensively (footnote 1: `Direct Testimony of Theodore Eidukas, PG Ex. 1.0 Rev. at 3:55-59`; footnote 3: `Direct Testimony of Joseph Zgonc, NS Ex. 2.0 Rev. at 5:101-104`) because his Direct is itself doing detailed factual rebuttal of the Companies' direct case. Cebulko Direct and Schott Direct, which are programmatic/affirmative rather than rebuttal-style, do not use the page:line form. The pattern that matches the citation form is **detailed point-by-point response to specific testimony**, not Rebuttal-form per se. All Rebuttals do this kind of response (so all use page:line); Direct filings use page:line when their substantive content does.
- **Direct on Rehearing uses inline prose citations.** Effron cites the Commission's Amendatory Order, PGL's filings, and AG schedules in body prose. Zero footnotes.

The Rhode Island guide's `[Witness] Direct, p. 25, lines 8–11` is the same locator-by-page-and-line idea in different syntax. Illinois practice uses `Ex. X.X at PAGE:LINE-LINE` instead, anchored to exhibit number rather than witness short name; the witness name comes in the lead-in (`Rebuttal Testimony of Theodore Eidukas, NS-PGL Ex. 12.0 at 16`).

---

## Exhibits

Pattern is `[PARTY PREFIX] [Ex.|Exhibit] [Major].[Minor]`. Each party uses its own prefix and minor-number padding style (`format_conventions.md` §4):

| Party / coalition         | Prefix in cover/lead                                                                         | Sub-exhibit minor                            | Examples                                                                                           |
| ------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| PIO                       | `PIO Exhibit` (cover); `PIO Ex.` (footnotes)                                                 | single-digit, no zero padding (`X.1`, `X.2`) | `PIO Exhibit 1.0` cover, sub `1.1`, `1.2`, `1.3`                                                   |
| AG                        | `AG Exhibit` (cover); `AG Ex.` (footnotes)                                                   | zero-padded two-digit (`X.01`, `X.02`)       | `AG Exhibit 2.00` cover, sub `2.01`–`2.17`                                                         |
| City of Chicago           | `City of Chicago Exhibit` or `COC Exhibit` (cover); body uses either `City Ex.` or `COC Ex.` | zero-padded two-digit                        | `City of Chicago Exhibit 3.0` cover (DeLeon); `City of Chicago ("COC") Exhibit 4.0` cover (Rábago) |
| CUB / PCR / Chicago joint | `CUB/PCR/Chicago Exhibit`                                                                    | (no sub-exhibits in the corpus)              | `CUB/PCR/Chicago Exhibit 4.0` cover                                                                |

**Intra-party prefix variation exists.** City witnesses do not converge on one short form: DeLeon uses `City Ex.` in the body while Rábago uses `COC Ex.`; both put the long form on the cover. Walker's footnotes alternate `AG Ex. 7.01` (line 124) with `AG Ex. 7.2` (line 224) in one filing.

**Cross-witness exhibit references.** Companies' exhibits cited as `NS-PGL Ex. X.0` for joint rebuttal exhibits; `PGL Ex. X.X` / `NS Ex. X.X` for company-specific direct exhibits. ICC Staff exhibits use `Staff Ex. X.0`. Revisions flagged with `REV`: `NS-PGL Ex. 17.0 REV at 14:250-251` (`rabago-rebuttal` footnote 15).

**Standard exhibit X.0 vs. X.1+ split.** The lead exhibit `[Party] Exhibit [Major].0` is the testimony itself. Sub-exhibits (`X.1`, `X.2` or `X.01`, `X.02`) are CV/qualifications, supporting data, discovery responses compiled into a single exhibit, attached studies. The CV is conventionally the first sub-exhibit (PIO Ex. 1.1, AG Ex. 2.17 for Dismukes — note Dismukes places the CV last, an exception). Compiled discovery responses are common (PIO Ex. 1.2 in Cebulko Direct; PIO Ex. 7.2 in Elder).

For a new Switchbox-sponsored intervener filing, pick a prefix that reads cleanly in the body cite syntax: `SB Ex. 1.0`, `SB Ex. 1.1`, etc. is consistent with existing party conventions.

---

## Tables and figures

**Tables appear inline in the markdown extracts** for compact tabular content embedded in the testimony body — the docket caption table itself; Rábago's `Table KRR-1` Basic Customer Method ECOSS results at lines 121–127; Walker's small exhibit index at lines 73–76. Larger or more complex tables are pushed to separate exhibits / schedules referenced by name (e.g., `AG Exhibit 9.01 Schedule 1P` in Effron).

**Diagrams that are not reproducible in markdown** are flagged in the extracts with `[DIAGRAM DESCRIPTION: …]` brackets followed by a transcribed approximation (`cebulko-rebuttal` lines 98–100). This is an extraction artifact, not a source convention.

The Rhode Island guide's "tables go inline, figures less common, charts go in exhibits" practice converges with what the Illinois corpus shows.

---

## Disclaimers and reservations

**The silence-is-not-agreement disclaimer** is the Illinois analog of the Rhode Island Tillman disclaimer. Used by Leyko (line 74), DeLeon (footnote 1, line 72), and Rábago (footnote 1, line 79), all in rebuttal. Verbatim:

> My silence with respect to any position taken by the Companies or any other party in this case should not be construed as agreement with that position. — Leyko Rebuttal line 74.

**Defensive framing of legal interpretation** with "not a lawyer/attorney" — see Tone and voice above.

---

## What to cite: scope-dependent expectations

The Rhode Island guide flags Docket 4600 Order 22851 as a mandatory citation. Illinois has no single comparable mandate — `required_content.md` verified that **no item in the corpus is cited by all 10 witnesses, and none reaches "near-universal" (8–9).** The "Frequently cited" tier (5–7 of 10) is the practical ceiling.

Frame citation expectations as **scope-dependent**, not universal. From `required_content.md` §"What this corpus suggests":

- **Capex-disallowance scope** (C-D, D-D, E-R, W-R, DL-R, Ef-DR): test-year revenue-requirement arithmetic is universal among witnesses doing this analysis (7/10); QIP-statute discussion (`220 ILCS 5/9-220.3`) is common where the disallowance touches QIP-funded plant; SMP discussion is common where it touches main replacement (5/10).
- **Rate-design scope** (C-D, C-R, R-R): cost-causation language and the prior PGL/NS rate order (`Docket No. 14-0224/14-0225`) are the shared anchors; ECOSS / Basic Customer Method appears in C-R and R-R (and underpins C-D's recommendation even where C-D does not use the term).
- **Energy-transition scope** (C-D, C-R, DL-R, partly D-D): CEJA (`Public Act 102-0662`), stranded-asset framing, and Brattle co-occur (Brattle in C-R and DL-R; EPRI is C-R-only and not a shared anchor).
- **Equity scope** (S-D only): `220 ILCS 5/8-201.10(b)`, `Section 1-102(d)`, the EEP four-pillar framework. S-D-unique in this corpus, so a new equity witness would be drawing fresh ground from a single precedent within the docket family.
- **Incentive-compensation scope** (L-R only): the four-docket incentive-comp line (Dockets `20-0308`, `18-1775`, `19-0436`, `18-0463`) is the entire authority base; a new witness on this issue would necessarily echo it.

Two general patterns:

1. **`Just and reasonable` (4/10) and `used and useful` (2/10) are invoked less often than ratemaking lore would predict.** Witnesses tend to do the underlying analysis and let the legal label sit in the introduction or framing rather than threading it through the body.
2. **Footnoting prior testimony in this docket** (using the `Witness Name, Party Ex. X.0 at PAGE:LINE` form) is more universal in this corpus than any specific external authority. The mechanical citation form is more reliably "expected" than the substantive citation list.

Effron's Rehearing testimony cites no statutes, no prior orders by docket number, and no external authorities — and was accepted. That is a corpus data point about what a focused rehearing testimony can look like, not a recommendation.

---

## Sections compressed or omitted from the Rhode Island guide

- **"Don't forget Docket 4600"** in the RI guide does not transfer. Illinois has no single equivalent omnibus rate-design principles order applied across all the corpus witnesses; the closest analog is the prior PGL/NS rate order (`14-0224/14-0225`) cited by 3/10. See the scope-dependent section above.
- **The Rhode Island guide's three-witness style table** (Acadia/Division, NERI, Walmart) is replaced by Illinois's three-axis variation table.
- **"Pick the NERI label-only style as the most modern and readable"** — the Illinois corpus does not converge on one preferred style. Pick a combination of the three axes and stay consistent.
- **The filing mechanics section** of the RI guide (cover letter, service list, ICC Clerk procedures) is left to the filing attorney — the Illinois corpus does not document filing mechanics any differently than RI's, and the cover letter / service list logic is procedurally similar enough that the RI guidance applies.

---

## Common mistakes to avoid

Convergent with Rhode Island, with Illinois-specific additions:

1. **Don't write prose and then shoehorn questions around it.** Write the questions first; they are the outline.
2. **Don't put argument in the questions.** Questions are neutral setups: `What did you find?` not `Isn't it true that the Company's proposal is unfair?`
3. **Don't assume the reader knows the background.** The ICC handles dozens of dockets.
4. **Don't skip the "so what."** After every analytical finding, connect it to a recommendation.
5. **Don't use footnotes for essential arguments.** Footnotes are for citations and tangential context.
6. **Don't mix Q-formatting axes mid-filing.** If the testimony opens `Q.` (period) sentence-case label-only, every Q in the file should follow the same pattern. The corpus shows internal consistency on the three axes (punctuation, casing, bolding span) for all 10 witnesses. Separately, watch for unforced terminal-punctuation inconsistencies in the question text itself: Dismukes inconsistently ends declarative-form Qs with `?` or `.` (lines 77 and 81 use `?`; line 85 uses `.`), the only such inconsistency in the corpus.
7. **Don't forget the consolidated caption.** Both PGL (Docket 23-0069) and North Shore (Docket 23-0068) must appear in the caption table, with one marked `(consol.)` or `(cons.)`. Filing under only one docket number when the proceeding is consolidated is a procedural error.
8. **Don't omit the silence-is-not-agreement disclaimer in Rebuttal.** It is consistently used in the corpus's Rebuttal filings to hedge against being deemed to have conceded by omission.
9. **Don't unhedge round numbers in material findings.** `approximately`, `roughly`, `at least`, `no more than` — every quantitative claim in the corpus uses one of these qualifiers, or a method-disclosure sentence in lieu.
10. **Don't bolt new arguments onto the closing Q.** `What do you recommend?` re-affirms the original ask, sometimes with a quantitative refinement; new rhetorical claims do not appear in the closing.

---

## The filing itself

Your attorney handles mechanical filing (cover letter, service list, ICC e-Docket submission, certificate of service). You produce the testimony in Word with line numbers and any exhibits as separate PDFs. Same as Rhode Island; the ICC e-Docket system is the procedural difference but does not change what the witness produces.
