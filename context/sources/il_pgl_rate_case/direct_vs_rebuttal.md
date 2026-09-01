# Direct vs. Rebuttal vs. Direct on Rehearing — Form Differences

Structural and rhetorical differences between testimony forms, observed in the 10 exemplars in `reports/il_npa/sources/` (ICC Dkts. 23-0068 / 23-0069 cons.). The corpus is one consolidated docket with 10 filings: **3 Directs**, **6 Rebuttals**, **1 Direct on Rehearing**, **0 Surrebuttals**. Witness shorthand follows `_scratch/format_conventions.md`. Findings are corpus-bounded — claims describe what these 10 filings do, not what Illinois ICC practice universally requires.

## 1. Openings

`format_conventions.md` §2 documents the opening Q&A patterns in detail. The form-level pattern is:

- **Direct openings rebuild the witness from scratch.** The first 5–7 Qs ask name/employer, party, professional background, prior testimony before the ICC, prior testimony in other states, sponsorship of the testimony itself, and exhibits sponsored. Cebulko Direct walks through all seven; Schott and Dismukes use compressed variants of the same checklist (`format_conventions.md` §2 lines 70–77).
- **Rebuttal openings collapse to two Qs**: a name Q (or none at all — Rábago opens directly with `What is the purpose of your rebuttal testimony?`), then a one-line incorporation: `Are you the same [witness] who [filed direct testimony / previously filed testimony] in this proceeding…?` The standard answer is one word: `Yes.` This adoption-by-reference does the work of the full direct-style qualifications block. Elder is the only rebuttal witness in the corpus that repeats the full direct intro — she had not filed direct testimony in this docket, so she had nothing to incorporate.
- **Direct on Rehearing opens like a Direct, not a Rebuttal.** Effron rebuilds qualifications from scratch (name → occupation → educational background → prior testimony — `effron-rehearing` lines 55–83) even though the AG had previously filed direct testimony in the same docket from a different witness (Dismukes). The "are you the same…" shortcut requires same-witness continuity that a rehearing on a new issue, with a new witness, does not have.

## 2. How each form establishes scope

The three forms answer the "what is this testimony about" Q in mechanically different ways.

- **Direct establishes its own scope.** The Section II `Purpose of Testimony` Q is answered by listing the issues the witness will analyze — typically as a forecast of the testimony's substantive sections. There is no opposing testimony to bound against; the witness picks the issues. The Companies are the _subject_ of analysis, not the interlocutor.
- **Rebuttal establishes scope by naming the opposing witnesses and exhibits being responded to.** This shows up two ways:
  - **Section structure** is built around opposing witnesses. Walker §§ II–IV: `Response to NS/PGL Witness Zgonc`, `Response to NS/PGL Witnesses Eldringhoff & Eidukas`, `Response to NS/PGL Witness Weber`. Rábago §§ III–V: `Response to PGL Witness Egelhoff`, `Response to PGL Witness Nelson`, `Response to ICC Staff Witness Harden`. The architecture is witness-by-witness, not topic-by-topic.
  - **The scope-Q recital lists rebutted exhibits by number.** Cebulko Rebuttal responds to PGL/NS Exs. 12.0, 14.0, 17.0, 21.0, 22.0; Elder reviews NS-PGL Exs. 19.01–19.04; Leyko answers PGL Ex. 2.4 and NS Ex. 2.4. Cebulko Rebuttal §II is explicitly titled `Rebuttal Testimony Overview` and itemizes "areas of agreement / disagreement" with each rebutted witness.
- **Direct on Rehearing establishes scope by responding to a specific Commission order.** Effron's Section II opens by reciting the Commission's Amendatory Order of January 3, 2024 (which set a $1.005 billion total revenue requirement and authorized PGL to seek incremental relief) and naming the post-order PGL filing (Direct on Rehearing, February 6, 2024) the AG is responding to. The scope hook is the order, not the opposing testimony — though the substantive arithmetic does engage PGL's rehearing direct. Direct on Rehearing is structurally a hybrid: a Direct in opening form, a Rebuttal in scope-bounding logic.

Two stock Rebuttal devices that Direct does not use:

1. **The no-modification beat.** Cebulko Rebuttal: `Does anything in the direct testimony filed by Staff and other intervening parties, or the rebuttal testimony filed by Peoples Gas, cause you to modify the recommendations you made in direct testimony? — No.` (`cebulko-rebuttal` lines 57–59). This locks the witness's prior positions in place without re-litigating them.
2. **The silence-is-not-agreement disclaimer.** Leyko: `My silence with respect to any position taken by the Companies or any other party in this case should not be construed as agreement with that position` (`leyko-rebuttal` line 74). DeLeon footnote 1 and Rábago footnote 1 use the same boilerplate. A hedge against being deemed to have conceded by omission — a procedural concern that does not arise in Direct.

## 3. Length and density by form

Computed by averaging the verified Q-counts and footnote-counts in `format_conventions.md` §3 across the witnesses in each form. Page counts come from `_scratch/exemplar_inventory.md`.

| Form                | n | Mean pages | Mean Q-count | Mean footnotes | Footnotes per Q | Footnotes per source line |
| ------------------- | - | ---------: | -----------: | -------------: | --------------: | ------------------------: |
| Direct              | 3 |       65.7 |         93.0 |           95.0 |            1.02 |                     0.108 |
| Rebuttal            | 6 |       27.3 |         36.8 |           55.8 |            1.52 |                     0.141 |
| Direct on Rehearing | 1 |       10.0 |         19.0 |            0.0 |            0.00 |                     0.000 |

Two patterns:

- **Direct testimony is roughly 2.4× longer than Rebuttal** by page count and 2.5× longer by Q-count. This tracks the scope difference — Direct builds a full affirmative case across multiple issues, Rebuttal answers a defined set of opposing-testimony points.
- **Rebuttal is denser than Direct in citations per Q** (1.52 vs. 1.02) and per source line (14.1% vs. 10.8%). The shorter document footnotes more aggressively because every Rebuttal claim is fighting a specific record citation.
- **Direct on Rehearing (n=1) is roughly a third the length of an average Rebuttal**, with **zero footnotes**. Outlier — see §6.

These are means across small samples (Direct n=3, Rebuttal n=6) with substantial within-form variation: Cebulko Direct (118 pp, 158 Qs) and Cebulko Rebuttal (56 pp, 75 Qs) are both ≈2× their respective form means. The form distinction is a real signal but a weak constraint on individual filings.

## 4. Citation patterns by form

`format_conventions.md` §5 documents three coexisting footnote-citation formats: long form (full witness name + exhibit + locator), short form (`Ex. X.X at PAGE`), and page:line form (`Ex. X.X at PAGE:LINE-LINE`). `required_content.md` documents the regulatory authorities each filing leans on. Form-level patterns:

- **Direct testimony leans on primary regulatory authority and external evidence.** Cebulko Direct's footnote pool draws on the PUA (Sections 8-103B, 8-104), CEJA, the prior PGL/NS rate order (Docket 14-0224/14-0225), the QIP statute, the NARUC Gas Manual, and the IRA. Dismukes Direct centers on the QIP statute itself (220 ILCS 5/9-220.3) and PHMSA federal pipeline rules (49 CFR Parts 191/192/195). Schott Direct anchors equity recommendations in PUA Section 1-102(d) and Section 8-201.10(b). Statutes, federal regulations, prior dockets, third-party studies — affirmative authority for an affirmative case.
- **Rebuttal testimony leans on opposing-testimony page:line citations.** The page:line locator form (`Ex. X.X at PAGE:LINE-LINE`) appears only in Rebuttals in this corpus. Rábago Rebuttal alone uses it in multiple footnotes (e.g., `COC Ex. 2.0 at 10:196-198; 12:226 to 14:297; 26:527 to 28:548` at footnote 12), Walker Rebuttal uses it (`NS-PGL Ex. 13.0 at 21:383`), Cebulko Rebuttal uses the long-form `Rebuttal Testimony of [Witness], NS-PGL Ex. X.0 at PAGE` repeatedly. Rebuttals also cite primary authority where it scaffolds their argument (Leyko's incentive-comp dockets 20-0308, 18-0463, 18-1775, 19-0436; DeLeon's PUA just-and-reasonable hook), but the high-frequency citations are to the rebutted record itself. Witnesses also cite their own Direct for incorporation (`Rábago direct testimony, COC Ex. 2.0 at PAGE:LINE`; `DeLeon direct testimony, City Ex. 1.0 at 4:89 to 12:229`).
- **Direct on Rehearing uses inline prose citations.** Effron has zero footnotes. Citations to the Commission's Amendatory Order, to PGL's filings, and to the AG's own schedules appear in body prose: `In its Amendatory Order of January 3, 2024, the Commission found a total revenue requirement of $1.005 billion…` (`effron-rehearing` line 99). Schedules are cited by name (`AG Exhibit 9.01 Schedule 1P`) inside the Q&A text. This is a single-witness pattern, n=1; whether it generalizes to other rehearing testimony is unknown from this corpus.

## 5. Same-witness Direct → Rebuttal evolution (Cebulko, n=1)

Only Cebulko has both a Direct and a Rebuttal in this corpus, so this is illustrative rather than canonical. n=1 limits any generalization.

|                    | Cebulko Direct | Cebulko Rebuttal | Rebuttal / Direct |
| ------------------ | -------------: | ---------------: | ----------------: |
| Pages              |            118 |               56 |              0.47 |
| Q-count            |            158 |               75 |              0.47 |
| Source lines       |          1,428 |              684 |              0.48 |
| Footnotes          |            193 |              118 |              0.61 |
| Footnotes per Q    |           1.22 |             1.57 |              1.29 |
| Footnotes per line |          0.135 |            0.173 |              1.28 |

Observations within this single witness pair:

- The Rebuttal is roughly **half the length** of the Direct on every length axis (pages, Qs, source lines).
- Footnotes drop by less (61% retained) than length drops (47% retained), so **the Rebuttal is denser in citations** — about 28% more footnotes per Q and per source line.
- **Scope narrows from 8 substantive sections (Direct §§ III–X) to 1 (Rebuttal §III).** The Direct covers Background → Capex → Bill Impact → Gas System Planning → PBR → Rate Design. The Rebuttal collapses to a single substantive section on capital-spending strategy in the context of electrification, plus a brief Overview (§II) flagging areas of agreement/disagreement with five rebutted witnesses.
- **Citation mix shifts toward the rebutted record.** The Direct's footnote pool is statutes, prior orders, NARUC, IRA materials, and external studies. The Rebuttal's first 12 footnotes (`cebulko-rebuttal` lines 567–578) are almost entirely `Rebuttal Testimony of [Witness], NS-PGL Ex. X.0 at PAGE` — Eidukas, Graves, Eldringhoff, Egelhoff, Olsen — with primary authority appearing later when the legal frame is invoked.
- **Opening collapses**, per §1: where the Direct walks through 7 intro Qs, the Rebuttal opens with `Q. Please state your name.` → `Q. Are you the same Bradley Cebulko who sponsored direct testimony in this proceeding…?` → `A. Yes.` → `Q. What is the purpose of your rebuttal testimony?`

The substantive frame (declining throughput + aggressive capex = harm to remaining customers) carries over from Direct to Rebuttal. The Rebuttal does not introduce a new thesis — it concentrates the existing one and weaponizes it against specific opposing witnesses, most notably by using PGL witness Graves's own 2021 Brattle report (attached as PIO Ex. 4.1) as the load-bearing counter-evidence.

## 6. Effron's Direct on Rehearing as a distinct form (n=1)

Effron's testimony is the only Direct on Rehearing in the corpus and looks materially different from both Direct and Rebuttal:

- **Length**: 10 pages, 19 Qs, 147 source lines — roughly a third of an average Rebuttal and an eighth of Cebulko Direct.
- **Zero footnotes.** The only filing in the corpus with no footnotes at all (`format_conventions.md` §3 verifies). All citations are inline prose: the Commission's Amendatory Order is named and dated in the answer text, schedules are referenced by name (`AG Exhibit 9.01 Schedule 1P`), and PGL's rehearing filing is paraphrased rather than footnoted.
- **Narrow scope.** Three sections: I. Statement of Qualifications, II. Purpose of Testimony, III. Revenue Requirement of Incremental Plant. The substantive content is a single revenue-requirement calculation ($1.6M incremental, ≈0.16% above the Commission's $1.005B order) with arithmetic carried in two schedules.
- **Bounded by an order, not an opposing brief.** The scope hook is the Commission's January 3, 2024 Amendatory Order (which authorized incremental relief for emergency/safety/reliability work and 2023 work-in-progress) and the PGL rehearing filing of February 6, 2024. The testimony is structurally a Direct (full qualifications intro, no "are you the same…" shortcut) but functionally a narrow response to an order-defined question.
- **No statutes, no prior orders by docket number, no external authorities.** The filing was accepted with only the post-order procedural references in body prose.

This is a corpus-of-one observation. It documents what a procedurally focused rehearing testimony can look like in this docket, not a generalizable pattern for rehearing testimony across Illinois practice.

## 7. Surrebuttal — not in this corpus

**No surrebuttals appear in this corpus.** ICC procedural orders in major rate cases typically schedule a surrebuttal round after rebuttal, but the exemplar set was assembled around Direct, Rebuttal, and the post-order Rehearing filings; surrebuttal filings (if any were made in 23-0068 / 23-0069) were not pulled.

Any claim about surrebuttal form is therefore **speculative inference from regulatory practice, not corpus-derived.** Standard ICC practice is that surrebuttal is narrower than rebuttal — limited to responding to new material in the opposing party's rebuttal. Whether the cascade produces further opening compression (e.g., a one-line `Are you the same X who…` referencing both prior filings), further citation density (heavier reliance on page:line locators against the opposing rebuttal), or further scope narrowing is not testable from these 10 exemplars. Treat any surrebuttal-form questions as out of scope until exemplars are added.
