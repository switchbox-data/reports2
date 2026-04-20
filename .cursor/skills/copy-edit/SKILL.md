---
name: copy-edit
description: Perform a full professional copy edit of a Quarto report following Chicago Manual of Style (17th ed.) conventions adapted for Switchbox house style. Use when the user asks for a copy edit, proofread, style check, grammar review, or editorial pass on an index.qmd or other .qmd narrative file.
---

# Copy Edit

Perform a thorough copy edit of a Switchbox report `.qmd` file, the way a professional copy editor working on technical and scientific publications would, grounded in the **Chicago Manual of Style, 17th edition** (CMOS 17) with Switchbox house style overrides noted below.

## Before you start

1. Read the target `.qmd` file in full.
2. Read the project's `CLAUDE.md` (already in context) for Switchbox voice, tone, and writing conventions — the copy edit must not fight those.
3. Identify all **protected zones** (see below) so you never modify them.

## Protected zones — do not edit

These constructs must pass through untouched. Never modify content inside them.

- **Inline computed values**: `` `{python} ...` ``, `` `r ...` ``
- **Code cells**: Fenced blocks starting with `` ```{python} ``, `` ```{r} ``
- **YAML frontmatter**: The `---` delimited block at the top of the file
- **Quarto shortcodes**: `{{< embed ... >}}`, `{{< glossary ... >}}`, `{{< glossary-def ... >}}`
- **Cross-references**: `@fig-...`, `@tbl-...`, `@sec-...`, `@citation_key`
- **LaTeX math**: `$...$` inline and `$$...$$` display blocks
- **Column/layout divs**: `:::` / `:::::` fenced div syntax
- **Chunk options**: Lines beginning with `#|`
- **HTML comments**: `<!-- ... -->`
- **Markdown links and images**: `[text](url)`, `![alt](path)`
- **Footnote markers**: `[^label]` — you may edit the _prose_ inside a footnote definition, but not the marker syntax itself

## Switchbox house style overrides to CMOS

Where Switchbox conventions differ from CMOS defaults, **house style wins**:

| Item               | CMOS default                       | Switchbox house style                                                          |
| ------------------ | ---------------------------------- | ------------------------------------------------------------------------------ |
| Em dash spacing    | Unspaced (word—word)               | **Spaced** (word — word)                                                       |
| Percent            | Spell out in nontechnical text     | **Always digits + %** (e.g., 40%, not "forty percent")                         |
| Dollar amounts     | Varies                             | **Always $digits with commas** (`$1,107`, not "about a thousand dollars")      |
| Bold               | Sparingly                          | **Bold key statistics and defined terms** per CLAUDE.md conventions            |
| Modeled outcomes   | Indicative ("will") or conditional | **Always conditional "would"** for simulation results                          |
| Voice for findings | Varies                             | **Active first person plural** ("We find that …," never "It was found that …") |
| Serial comma       | Required (CMOS 6.19)               | **Required** (aligned)                                                         |

Do **not** "fix" these to standard CMOS. They are intentional.

## What to check

Work through the file **systematically**, section by section. For each issue found, make the correction via `StrReplace` with enough surrounding context for a unique match.

### 1. Grammar and syntax

- Subject–verb agreement (watch for long prepositional phrases between subject and verb)
- Dangling and misplaced modifiers ("After switching to heat pumps, the bill drops" — whose bill?)
- Sentence fragments (acceptable occasionally for rhetorical punch; flag only unclear ones)
- Run-on sentences and comma splices
- Pronoun–antecedent agreement and clarity of reference

### 2. Punctuation

- **Serial comma**: Required before "and"/"or" in a series (CMOS 6.19)
- **Em dash** ( — ): Spaced, for parenthetical asides and abrupt changes. Two hyphens (`--`) in source should be en dash (`–`) for ranges or proper em dash (`—`) for parentheticals.
- **En dash** (–): For number and date ranges ("2021–2035"), score-like combinations ("cost–benefit"), and compound adjectives where one element is itself a compound ("New York–based"). In markdown source, use `–` directly or `--` only for ranges.
- **Hyphens**: Compound modifiers before a noun ("cost-of-service study," "low-income households"). No hyphen after an -ly adverb ("highly energy burdened," not "highly-energy-burdened"). Suspended hyphens in parallel compounds ("single- and multi-family").
- **Comma after introductory elements**: Required after introductory clauses, long prepositional phrases, and transitional adverbs (CMOS 6.25–6.30).
- **Comma in compound sentences**: Required before coordinating conjunction joining independent clauses (CMOS 6.22).
- **Semicolons**: Between independent clauses not joined by a conjunction; in complex series with internal commas.
- **Colons**: Lowercase after a colon unless what follows is a complete sentence (CMOS 6.61) or a proper noun. (Switchbox frequently uses the "colon-as-pivot" — follow the existing pattern.)
- **Possessives**: Singular nouns ending in _s_ take _'s_ (CMOS 7.15–7.22): "the business's costs." Exception: "its" (never "it's" for possessive).
- **Quotation marks**: Double quotes for direct quotations; periods and commas inside closing quotes (American style).

### 3. Spelling and word choice

- Correct commonly confused words: affect/effect, principal/principle, complement/compliment, ensure/insure, comprise/compose, fewer/less, farther/further, that/which
- **That** for restrictive clauses (no comma); **which** for nonrestrictive clauses (with comma) (CMOS 6.27)
- Consistent spelling of technical terms throughout (check against first occurrence): e.g., "heat pump" (not "heatpump"), "cost of service" vs. "cost-of-service" (hyphenated when used as a modifier)
- No double spaces after periods

### 4. Number style

- **Percentages**: Digits + % always (house style).
- **Dollar amounts**: Digits with $ and commas always (house style).
- **Other numbers in running text**: Spell out whole numbers one through one hundred and any number beginning a sentence (CMOS 9.2–9.3). Exception: keep digits in technical contexts (dimensions, multipliers, data values) and wherever mixing spelled-out and digit forms in the same passage would be inconsistent.
- **Thousands separator**: Commas in numbers of four or more digits ($1,107; 8,760 hours).
- **Ranges**: En dash between numbers ("15–25 words"), no spaces.
- **Decimal precision**: Flag inconsistent decimal precision within a single comparison (e.g., mixing "$3.48" and "$3.5" for the same type of price).

### 5. Consistency and terminology

- Verify term consistency: if "heat pump customer" is used, do not later switch to "HP customer" without abbreviation established (unless abbreviation was introduced earlier).
- Check that abbreviations/acronyms are defined on first use in the _main text_ (not just in a footnote or appendix).
- Consistent capitalization of proper nouns, program names, and technical terms: "Bill Alignment Test" (not "bill alignment test"), "Rhode Island Energy" (not "RI Energy" unless introduced as abbreviation).
- Table and figure references: "as shown in @fig-..." (not "as shown in Figure X" inconsistently).

### 6. Parallel structure

- Items in a bulleted or numbered list must be grammatically parallel (all noun phrases, all imperative verbs, all complete sentences — not a mix).
- Items in a series within a sentence should be parallel: "loading data, computing statistics, and generating figures" (not "loading data, computation of statistics, and to generate figures").

### 7. Clarity and concision

- Cut filler: "in order to" → "to"; "the fact that" → "that"; "it should be noted that" → cut entirely
- Remove redundancies: "currently existing," "past history," "each and every"
- Break sentences over ~40 words if they can be split without losing meaning
- Flag ambiguous pronoun references ("This shows…" — this what?)
- Prefer concrete subjects over vague ones ("The analysis shows" over "It can be seen that")

### 8. Formatting and structure

- Consistent heading capitalization (sentence case for questions: "How does a home's income affect its energy bills?"; title case is also acceptable if consistent throughout)
- No orphan headings (a heading with no content before the next heading)
- Consistent use of horizontal rules (`---`) as section breaks
- Footnote definitions placed immediately after the paragraph that first invokes them (not grouped at end of section)

## Output approach

- Make all corrections directly via `StrReplace`, one at a time.
- For each edit, state the issue category (e.g., "punctuation — missing serial comma") and the specific CMOS reference or house style rule.
- Group nearby edits into a single `StrReplace` when the old_string can be made unique.
- If a passage has an issue you're **uncertain** about (e.g., ambiguous sentence that might be intentional), note it in your response text as a **query** rather than making the change. Professional copy editors query the author on judgment calls.
- After all edits, provide a brief **summary** listing the categories of changes made and their counts.
