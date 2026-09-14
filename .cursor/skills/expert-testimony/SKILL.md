---
name: expert-testimony
description: >-
  Write or edit expert testimony in Q&A format for regulatory proceedings
  (PUC/PSC/ICC rate cases, docket filings). Use when the user asks to write,
  draft, edit, or review expert testimony, testimony outlines, or testimony
  exhibits.
---

# Expert Testimony

Write or edit expert testimony for regulatory proceedings (PUC/PSC/ICC rate cases). This skill teaches the voice, structure, and conventions through a deliberate reading sequence.

## Reading sequence (order matters)

Before writing or editing any testimony, read these files **in order**. Each step builds on the prior one — do not skip or reorder.

### Step 1: Learn the Switchbox voice

Read the **Writing Conventions** section of this project's `CLAUDE.md` (already auto-loaded via workspace rules). This is the base voice: clear, direct, evidence-driven, policy-oriented, accessible to non-technical readers. Internalize the voice, tone, sentence-level style, number formatting, and rhetorical structures described there.

The testimony voice IS the Switchbox report voice, but adapted for regulatory proceedings:

- **More formal register.** No contractions. First person singular ("I find," "I recommend," "my analysis shows"), not first person plural.
- **Q&A scaffolding.** Every sentence lives inside a question-and-answer pair. The questions are rhetorical — you write both sides.
- **Third person for the client.** "CLF recommends..." or "On behalf of CLF, I recommend..." — not "we recommend."
- **Measured disagreement.** When disagreeing with the utility: state what they propose, state why it is wrong, state the fix. No sarcasm. Use the graduated ladder: soft disagreement → hedged criticism → direct contradiction → legal terms of art (reserved for section headers).
- **Conditional "would" for modeled outcomes.** Same as Switchbox reports. "X% of homes **would** save money," never "will save."
- **Confident findings.** "I find that..." "My analysis demonstrates..." — no hedging with "may" or "might" when you have data.
- **Hedged round numbers.** Bracket quantitative claims with "approximately," "roughly," "at least," "no more than" — even when the figure comes from the utility's own data.

### Step 2: See how experienced intervenor witnesses write testimony

Read these two third-party exemplars to absorb the genre conventions — Q&A format, exhibit references, opening boilerplate, citation style, how experienced witnesses structure arguments:

1. **Rábago direct testimony** — `context/sources/ri_hp_rates/ripuc_4770_direct_testimony_neri_rabago.md`. The best third-party exemplar: 75 pages covering 8 topics, modern label-only Q&A style, strong analytical voice on rate design and cost causation.
2. **LeBel direct testimony** — `context/sources/ri_hp_rates/ripuc_4770_direct_testimony_acadia_lebel.md`. Concise (28 pages), policy-forward intervenor testimony with a rate design vision.

After reading these, you know what expert testimony _looks like_.

### Step 3: Learn the structural conventions

Read the **testimony style guide** — `context/methods/testimony_style_guide.md`. This codifies the patterns you just saw in Rábago and LeBel: argument structures, answer length tiers, opening/closing sequences, citation conventions, exhibit naming, common mistakes. The guide makes the implicit patterns explicit.

### Step 4: Read the Switchbox exemplar

Read **`reports/ri_hp_rates/expert_testimony.qmd`** — Switchbox's only finished testimony. This is the synthesis: how Switchbox balances the base voice (step 1) with the testimony genre (steps 2–3). Note that Switchbox's testimony is more accessible than Rábago's, more data-forward than LeBel's, and uses inline computed values via the Quarto pipeline.

**Match this voice, not the third-party exemplars.**

---

## Condensed testimony conventions

These conventions are always available without file reads. They are distilled from the RI testimony style guide and the Switchbox exemplar.

### Q&A format

Every sentence of testimony is framed as an answer to a question you wrote. The questions are rhetorical scaffolding, not cross-examination.

Switchbox uses the **NERI label-only style** (bold Q./A. prefix, plain text):

```
**Q.** What is the purpose of your testimony?

**A.** The purpose of my testimony is to...
```

Pick one style and be consistent throughout the filing. Use `<br>` between Q&A pairs for visual spacing in HTML output.

### Opening sequence (canned questions)

Every testimony starts with ~6 mandatory questions:

1. Name, title, employer, business address.
2. Education and work experience (career chronology in prose; resume is a separate exhibit).
3. Prior testimony before this PUC and before other state regulatory commissions.
4. On whose behalf you are testifying.
5. Purpose of testimony (one tight paragraph — this is the thesis statement).
6. Summary of recommendations (numbered list — the most important answer in the testimony).
7. Sponsored exhibits ("I am sponsoring Exhibits JPV-1 through JPV-X").

The closing is always:

```
**Q.** Does this conclude your direct testimony?

**A.** Yes, it does.
```

### Argument structure

Two patterns, depending on whether you are reacting or proposing:

**(a) Responding to the Company's position** (~5 sections per topic):

1. State the Company's position.
2. State your position ("Do you support this proposal?" → "No.").
3. Build the argument ("Why not?" → the substance).
4. Provide evidence (numerical example, table, or exhibit reference).
5. State your recommendation.

**(b) Advancing your own proposal** (~6 sections per topic):

1. Establish the problem — lead with the finding, not the methodology.
2. Explain why it matters — connect to principles the Commission cares about.
3. Present the remedy — your proposal, stated clearly and specifically.
4. Show it works — quantify the impact (bill changes, cross-subsidy elimination).
5. Anticipate objections — state the likely counterargument fairly, then dismantle it.
6. Explain the methodology — technical backup comes _after_ the finding and proposal.

**General principle: finding first, methodology last.** Bury-the-lede is the most common mistake in technical testimony.

### Answer length

| Type     | Words              | When to use                                                     |
| -------- | ------------------ | --------------------------------------------------------------- |
| One-word | 1 ("Yes." / "No.") | Factual yes/no questions (prior testimony, sponsoring exhibits) |
| Short    | 10–50              | Narrow factual questions with clear answers                     |
| Medium   | 80–250             | The workhorse. Most substantive answers.                        |
| Long     | 300–600            | Major summaries, overall assessments, conceptual arguments      |

If an answer exceeds ~250 words, break it into multiple Q&A pairs. The questions give the reader handholds.

### Citations

**Other witnesses in the same docket:**

First reference establishes the short name:

> See Pre-filed Direct Testimony of Howard S. Gorman ("Gorman Direct"), p. 25, lines 8–11.

Subsequent references: `Gorman Direct, p. 39, lines 17–19.`

**Prior docket orders:** Full citation on first use, then short name.

**Statutes:** Cite by section (e.g., `R.I. Gen. Laws § 39-1-1(b)`).

**External sources:** Go in footnotes, not body text.

**Data request responses:** `Company response to CLF 2-9` (format: `[Responding party] response to [Requesting party] [Set]-[Question]`).

### Exhibits

Naming convention: witness initials + number (`JPV-1`, `JPV-2`, etc.).

- Exhibit 1 is always the resume/qualifications statement.
- Subsequent exhibits: supporting data tables, the full Switchbox report, schedules of calculations.
- Tables can be both inline (summary version in the Q&A) and in an exhibit (full version).

### Tables and figures

Tables go inline in the Q&A. Introduce with prose, then show immediately:

> The cost-of-service and bill comparison is shown in Table 1 below.
>
> [TABLE]
>
> As Table 1 shows, heat pump customers overpay by...

Figures (charts) are less common in testimony — they appear more in exhibits. Key summary figures can be inline; the full set of charts should be in an exhibit.

Number tables and figures sequentially: Table 1, Table 2, Figure 1, Figure 2.

### Disclaimers

Include a disclaimer near the top (after the summary of recommendations):

> **Q.** Does the fact that you may not address an issue or position advocated by the Company indicate CLF's support?
>
> **A.** No. The fact that an issue is not addressed in this testimony should not be construed as an endorsement of any position taken by the Company or any other party.

### Common mistakes

1. Do not write prose and then shoehorn questions around it. Write the questions first — they are the outline.
2. Do not put argument in the questions. Questions are neutral setups: "What did you find?" — not "Isn't it true that the Company's proposal is unfair?"
3. Do not assume the reader knows the background. Explain the context before diving into the analysis.
4. Do not skip the "so what." After every analytical finding, connect it to a recommendation.
5. Do not use footnotes for essential arguments. Footnotes are for citations and tangential context.
6. Do not mix up "cost of service" and "rate design." ACOSS/COSS determines revenue per class (cost allocation); rate design determines how that revenue is collected (fixed, volumetric, demand charges).

---

## Technical conventions (Quarto)

Testimony `.qmd` files follow the same Quarto Manuscript data flow as reports:

- Analysis notebooks export `report_vars` to `cache/` via pickle.
- The testimony file loads them in a setup cell and uses inline `{python}` expressions.
- **Never hardcode numbers in testimony prose.** All computed values must come from inline code.

### Setup cell pattern

```python
import pickle
from types import SimpleNamespace

v = SimpleNamespace(**pickle.loads(Path("cache/report_variables.pkl").read_bytes()))

def dollar(x, accuracy=0):
    return f"${x:,.{accuracy}f}"

def pct(x, accuracy=0):
    return f"{x * 100:,.{accuracy}f}%"
```

### Rendering

From the report directory:

- `just draft expert_testimony.qmd` — Renders to DOCX with testimony formatting (TNR 12pt, double-spaced, line numbering, Q/A paragraph styles).
- `just typeset expert_testimony.qmd` — Renders to ICML for InDesign.

The `--testimony` flag in `just draft` applies `lib/just/templates/filters/testimony.lua` (Pandoc Lua filter) and the testimony reference DOCX built by `lib/just/templates/build_expert_testimony.py`.
