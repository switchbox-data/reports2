# Writing expert testimony: user guide

How to write expert testimony at Switchbox and turn it into the Word file that gets filed. It is written for anyone on the team who analyzes data and is asked to testify, so it assumes no knowledge of Quarto, Pandoc, or Word styles.

In short: you write the testimony as plain text in one file, fill in a short form at the top of that file (the docket details), and run one command. You get a finished Word document with a cover page, line numbers, page numbers, and the right fonts. Nobody has to reformat it by hand afterwards.

## The five steps

1. **Create the file:** `just new-testimony reports/<report>/expert_testimony.qmd`
2. **Fill in the form** at the top of the file (the `testimony:` block).
3. **Write the testimony** below it, as questions and answers.
4. **Check it** (optional): `just check-testimony reports/<report>/expert_testimony.qmd`
5. **Render it:** from the report folder, `just testimony`. The Word file appears in that folder.

Everything below explains these steps in order.

## Before you start: how testimony differs from a report

A Switchbox report talks to the public. Testimony talks to a commission, and it is evidence in a legal proceeding. Three things change:

- **Everything is a question and an answer.** You write both sides. The questions are an outline for the reader, not a cross-examination.
- **The register is more formal.** First person singular ("I find," "my analysis shows"), no contractions, and "CLF recommends" rather than "we recommend" when you speak for a client.
- **The finding comes first and the method comes last.** Lead with what you found and what you recommend; put the technical backup after.

The voice, structure and mistakes to avoid are covered in two places. Read them before you write your first testimony:

- **[`testimony_style_guide.md`](../methods/testimony_style_guide.md)** is the long version: how long answers should be, the opening and closing questions every testimony has, how to cite other witnesses, how to name exhibits, and common mistakes. It is drawn from witnesses in Rhode Island Docket 4770, but the conventions carry to other states.
- **The `expert-testimony` writing skill** ([`SKILL.md`](../../.cursor/skills/expert-testimony/SKILL.md)) is the same material in a form an AI agent in Cursor can follow. If you ask Cursor to "draft the introduction section of my testimony" or "edit my testimony for voice," it reads the skill first, along with the style guide and two example testimonies by other witnesses, so its draft matches Switchbox's voice and the genre. You are still the witness: read and rewrite everything an agent drafts, because you are the one who swears to it.

Two finished Switchbox examples to copy from:

- [`reports/md_hp_rates/expert_testimony.qmd`](../../reports/md_hp_rates/expert_testimony.qmd): Maryland, the most recent, and the model for the Word format.
- [`reports/ri_hp_rates/expert_testimony.qmd`](../../reports/ri_hp_rates/expert_testimony.qmd): Rhode Island.

The base Switchbox writing rules (numbers, bold, "would" for modeled outcomes) are in the "Writing conventions" section of [`AGENTS.md`](../../AGENTS.md).

## Step 1: Create the file

Testimony lives next to the report whose analysis it relies on, in `reports/<report>/`. From the root of the repo:

```bash
just new-testimony reports/md_hp_rates/expert_testimony.qmd
```

This creates a starter file with every field of the form already in place, each one filled with a `[PLACEHOLDER]` in square brackets, and a first question and answer. It will not overwrite a file that already exists.

## Step 2: Fill in the form

The form is a block at the top of the file called `testimony:`. Together these fields produce the cover page and the running header at the top of every page. You never type them anywhere else.

```yaml
testimony:
  commission: Maryland Public Service Commission
  commission_short: Maryland PSC
  case_number: "Case No. 9888"
  caption:
    - IN THE MATTER OF THE APPLICATION OF
    - BALTIMORE GAS & ELECTRIC COMPANY
    - FOR ADJUSTMENTS TO ITS ELECTRIC BASE RATES
  type: Direct
  and_exhibits: true
  witness: Juan-Pablo Velez
  witness_title: Executive Director, Switchbox
  on_behalf_of: Chesapeake Climate Action Network
  date: 2026-09-22
```

| Field              | Required | What to put                                                                                                      | Where it shows up                                     |
| ------------------ | -------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `commission`       | yes      | The commission's full name, e.g. `Maryland Public Service Commission`                                            | Cover page, in capitals, under "BEFORE THE"           |
| `commission_short` | yes      | A short name, e.g. `Maryland PSC` or `RIPUC`                                                                     | Page header, with the case number                     |
| `case_number`      | yes      | The docket exactly as it should print, e.g. `"Case No. 9888"` or `"Docket No. 26-05-10"`. Keep the quotes.       | Cover page caption, and page header                   |
| `caption`          | yes      | A list of lines naming the applicant and the subject of the proceeding. Copy them from the docket's own filings. | Left side of the cover-page caption, in capitals      |
| `type`             | yes      | One of `Direct`, `Rebuttal`, `Surrebuttal`, `Rejoinder`, `Supplemental Direct`, `Supplemental Rebuttal`          | Cover title ("DIRECT TESTIMONY OF …") and page header |
| `witness`          | yes      | The witness's name                                                                                               | Cover page, and page header                           |
| `on_behalf_of`     | yes      | The party you testify for, e.g. `Conservation Law Foundation`                                                    | Cover page, and page header                           |
| `date`             | yes      | The filing date, written `2026-09-22` or `September 22, 2026`                                                    | Bottom of the cover page                              |
| `and_exhibits`     | no       | `true` if exhibits are filed with the testimony. Defaults to no.                                                 | Adds "AND EXHIBITS" to the cover title                |
| `witness_title`    | no       | A line under the witness name, e.g. `Executive Director, Switchbox`. Delete the line if you do not want one.     | Cover page                                            |
| `version_label`    | no       | An extra cover line such as `PUBLIC VERSION`                                                                     | Cover page                                            |

Tips:

- **Take the caption, case number and commission name from the docket**, not from memory. The caption is the part most likely to be wrong, and it is on the cover of a legal filing.
- **Put quotes around a value that contains a colon or starts with a symbol**, as in `"Case No. 9888"`. When in doubt, quote it.
- The `title`, `subtitle`, and `author` lines at the top of the file are for the web preview only; they do not appear in the Word file.

If you leave something out, misspell a field name, or leave a `[PLACEHOLDER]`, the render stops before doing any work and tells you in plain English what to fix. For example:

```
💥 expert_testimony.qmd: the `testimony:` fields need attention:
   `testimony.caption` still has placeholder lines ([IN THE MATTER OF THE APPLICATION OF]): ...
   `testimony.date` is still a placeholder ([YYYY-MM-DD]): filing date, e.g. 2026-09-22.
```

The message also catches misspelled field names: "Unknown field `testimony.witnes`. Did you mean `witness`?"

## Step 3: Write the testimony

Everything below the form is the testimony itself, written in plain text (Markdown).

### Questions and answers

```markdown
**Q.** What is the purpose of your testimony?

**A.** The purpose of my testimony is to ...
```

- Bold only the `Q.` and `A.`; the question and answer text is plain.
- Leave a blank line between paragraphs. If an answer has several paragraphs, just write them one after another; the later paragraphs line up under the first.
- Put one extra blank line between question-and-answer pairs in the file, so each pair is visually set apart while you edit. Don't use `<br>` for spacing: the Word file spaces the pairs itself, and a `<br>` line would add an empty paragraph.
- Start with the usual opening questions (name and address, background, prior testimony, who you testify for, purpose, summary of recommendations, exhibits) and end with "Does this conclude your direct testimony?" The style guide lists them.

### Headings

Type the section numbers yourself, in the same way as the filed examples:

```markdown
## I. Introduction

### A. Qualifications

#### 1) The data we used
```

In the Word file, only the words are underlined ("I. **Introduction**" with the underline under "Introduction", not under "I."). The `##` level is the main heading; use `###` and `####` for sub-sections.

### Numbers come from the analysis, never from typing

Do not type statistics into the text. The analysis notebook saves its results, and the testimony pulls them in with inline code such as `` `{python} dollar(r.median_bill)` ``. This way the text and the analysis can never disagree. The pattern is described in the "Technical conventions" section of the [skill](../../.cursor/skills/expert-testimony/SKILL.md) and shown in full in the top of [`reports/md_hp_rates/expert_testimony.qmd`](../../reports/md_hp_rates/expert_testimony.qmd).

If the analysis has not been run on your machine, the testimony will fail to render with a "file not found" error for a `cache/...pkl` file. Run the analysis first (ask a teammate which notebook), or pull the cached results.

### Tables, figures, footnotes, and citations

- **Tables** go in the text, introduced by a sentence that tells the reader what to look for. They print single-spaced so they stay compact.
- **Figures** are drawn from the analysis notebook and inserted at print resolution. Use them sparingly in testimony; put the full set in an exhibit.
- **Footnotes** become real Word footnotes at the bottom of the page, in a smaller size. Use them for citations and side points, never for the main argument.
- **Citations** written as `@citation_key` are resolved against the shared bibliography and listed at the end of the document. Citation keys and how to add a source to the library are in [`sources_user_guide.md`](sources_user_guide.md).
- Don't use margin notes (`{.column-margin}`) or side-by-side layouts. A filed document has no margin column, so that content is placed in the body instead.

### Exhibits

Name them with your initials and a number (`JPV-1`, `JPV-2`). Exhibit 1 is your resume. The testimony text refers to the exhibits; the exhibits themselves are separate files that you attach when you file.

## Step 4: Check the form (optional)

```bash
just check-testimony reports/md_hp_rates/expert_testimony.qmd
```

This reads only the form and reports the same problems as the render would, in a second. Run it as often as you like. When everything is fine it prints a line such as `testimony fields OK (Direct testimony of Juan-Pablo Velez, Case No. 9888, September 22, 2026)`, which is also a quick way to check the cover details by eye.

## Step 5: Render the Word file

From inside the report's folder:

```bash
cd reports/md_hp_rates
just testimony
```

To render a differently named file, give its name: `just testimony my_rebuttal.qmd`. Rendering takes a minute or two, because it re-runs the figures at print quality.

The result is a Word file named after the testimony and the day you ran it, in the same folder, for example `expert_testimony_20260922.docx`. It is a build output, so don't commit it.

To read what you've written while you write it, run `just render expert_testimony.qmd` instead; it makes an HTML page in `docs/`. The page is set up for working, not filing: a Sections list on the left (click to jump), slightly smaller text, and each footnote and citation in the right margin next to the line that cites it. It has no line numbers or page breaks, since those only exist in the Word file. The styling is in `reports/.style/testimony.scss`; the settings are the `toc` and `reference-location` lines under `format: html:` at the top of the file, and `just new-testimony` includes them.

## What the Word file looks like

The format follows the Maryland PSC filing, and is the same for every commission.

**Cover page** (no line numbers, no header or footer): "BEFORE THE" and the commission name; the docket caption on the left with the case number on the right, and the rules around it; then "DIRECT TESTIMONY AND EXHIBITS OF", the witness name and title, "ON BEHALF OF" the party, any version label, and the date.

**Every page after the cover:**

- **Running header** in the top right, three lines: "Direct Testimony of Juan-Pablo Velez", the party, and "Maryland PSC Case No. 9888".
- **Line numbers** down the left margin, restarting at 1 on every page, so anyone can cite "page 12, lines 8 to 11."
- **Page numbers** centered at the bottom, starting at 1 on the first page after the cover.
- **Times New Roman 12 point**, double-spaced, one-inch margins, left-aligned (not justified).
- **Questions** in bold, with the `Q.` and `A.` hanging in the margin so the text lines up; answers in regular type. A small gap separates each question-and-answer pair.
- **Headings** bold, with the words underlined and the numeral not.
- **Footnotes** in 11 point, without line numbers.

## Handing it off

- **Send the `.docx` itself.** Don't open it in Google Docs and re-export it. Google Docs drops the fonts and may drop the line numbers, which is the problem this tool exists to solve.
- **Open it once in Word and look it over** before filing: check the cover page, flip through a few pages, and check that tables and figures sit where you expect. Small adjustments in Word (such as moving a page break) are fine; fix wording in the `.qmd` and re-render so the two stay in sync.
- Re-rendering always produces the whole file again. Edits made directly in Word are lost the next time you run `just testimony`.

## If something goes wrong

| What you see                             | What it means                                                   | What to do                                                     |
| ---------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------- |
| "the `testimony:` fields need attention" | The form is incomplete or has a typo                            | Fix the fields it lists and run again                          |
| "File not found: … .pkl"                 | The analysis results the testimony reads aren't on your machine | Run the analysis notebook that creates them, or ask a teammate |
| "File not found" for the `.qmd`          | Wrong folder or file name                                       | Run from the report's folder, or pass the file name            |
| "Quarto render failed"                   | An error in the text or the code cells, shown above that line   | Read the first error above the message; it points to the line  |
| The cover looks wrong                    | A field on the form is wrong                                    | Fix the form and re-render                                     |

## Where the pieces live

You don't need these to write testimony. They are for whoever maintains the tool.

- [`lib/just/testimony.py`](../../lib/just/testimony.py): the form's fields, the checks, `new-testimony`, `check-testimony`.
- [`lib/just/draft.py`](../../lib/just/draft.py): runs the render.
- [`lib/just/templates/filters/testimony.lua`](../../lib/just/templates/filters/testimony.lua): builds the cover page and lays out the questions, answers, and headings.
- [`lib/just/templates/build_expert_testimony.py`](../../lib/just/templates/build_expert_testimony.py): builds the Word model file (fonts, spacing, line numbers, header) that `expert_testimony.docx` in the same folder is saved from. Re-run it after changing the format, and commit the new `.docx`.
- [`tests/just/test_testimony.py`](../../tests/just/test_testimony.py): the tests.
- The writing skill: [`.cursor/skills/expert-testimony/SKILL.md`](../../.cursor/skills/expert-testimony/SKILL.md).
