# Writing interrogatory responses: user guide

How to answer another party's interrogatories or data requests and get Word files counsel can review and file. You write all the responses to one set in a single file, fill in a short form at the top, and run one command. Nobody retypes the header on each response.

## The steps

1. **Create the file:** `just new-interrogatory-responses reports/<report>/<name>.qmd`
2. **Fill in the form** at the top of the file (the `interrogatory_responses:` block).
3. **Add each question**, copied exactly, then **check** it: `just check-interrogatory-responses reports/<report>/<name>.qmd`
4. **Write the responses.**
5. **Render for review:** from the report folder, `just interrogatories` (Connecticut report: `ciec_responses.qmd`).
6. **Render for filing:** `just interrogatories-split`, which writes one Word file per response into `filing/`.

If you use an AI agent in Cursor, ask it to "set up responses to <the requests>": the `interrogatory-response` skill covers steps 1 to 3, including copying the questions out of the extract.

## The form

```yaml
interrogatory_responses:
  docket: PURA Docket No. 26-05-10
  responding_party: Conservation Law Foundation and Sierra Club
  requesting_party: Connecticut Industrial Energy Consumers
  set: Set CIEC-02
  date_issued: 2026-10-29
  date_filed: 2026-11-12
  witness: Juan-Pablo Velez
  file_prefix: CT 26-05-10
  source_extract: context/sources/ct_hp_rates/pura_260510_ciec_ir1_to_clf_sc.md
  expected_responses: 19
```

`docket`, `responding_party`, `requesting_party`, `set`, `date_issued`, `date_filed` and `witness` are required; they are printed in the header and caption of every response. The rest are optional:

- `file_prefix` starts each split file name (`CT 26-05-10_CIEC-1 Response.docx`).
- `source_extract` is the markdown extract of the requests. When it is set, `check` and every render confirm that each line of each question appears in it.
- `expected_responses` is how many responses the set has; the check fails if the file has a different number.
- `draft` defaults to true and prints DRAFT FOR COUNSEL REVIEW at the top of every page. Set it to `false` for the filing copy.

A value left in `[BRACKETS]`, a misspelled field name and a missing field are all reported together, before any rendering.

## The body

Each response is a level-2 heading carrying its label, then a `question` block and a `response` block:

```markdown
## CIEC-1

::: {.question}
Please refer to Velez Direct Testimony at page 6, lines 11-23.

a. Please provide Mr. Velez’s estimate of ...
b. Please provide Mr. Velez’s estimate of ...
:::

::: {.response}
a. ...
:::
```

- The label is printed exactly as you type it, in the header (`CIEC-1` or `CIEC-001`).
- A different witness for one response: `## CIEC-5 {witness="Name"}`.
- Do not nest blocks and do not put text outside them. Footnote definitions go inside the `response` block, right after the paragraph that uses them.
- An empty `response` block prints "[Response not yet written.]" in the review file.

## What the Word files look like

Every response is its own Word section that restarts at page 1. Its header has the responding party, docket, set, date issued, the response label and "Page n of N" counted within that response; the first page then shows Date Filed, Witness and Request from, followed by "Question:" and "Response:". The combined review file has all responses back to back; the split files have one each, in the same format. Open the combined review file in Word, not Google Docs or LibreOffice: only Word computes the per-response "of N" (the others show "of 1"). The split filing files work in all three.

Responses are separate PDFs on the PURA site, with attachments (Excel and the like) uploaded alongside, not embedded. See the `interrogatory-response` skill and its `connecticut.md` for filing details and for how the other parties' responses in the docket look.

Logic: `lib/just/interrogatory.py`, `lib/just/templates/filters/interrogatory.lua`, `lib/just/templates/build_interrogatory_response.py`.
