---
name: interrogatory-response
description: >-
  Write responses to interrogatories or data requests in a rate case (PUC/PSC
  discovery), then render them to Word for counsel to review and file. Use when
  the user is answering another party's requests, e.g. CIEC's questions to
  CLF-SC in Connecticut PURA Docket 26-05-10, or asks how a response should be
  formatted or filed.
---

# Interrogatory responses

All the responses to one set of requests live in **one `.qmd`**. One command renders a combined
Word file for counsel to review; another renders one Word file per response for filing. The
witness's voice, citation rules and number conventions are the testimony ones (see
`expert-testimony` and its `citations.md`); this skill covers what is different.

State and docket specifics live next to this file: [`connecticut.md`](connecticut.md) holds what we
know about PURA (header layouts seen in the docket, the web filing form, file names, due dates).
Another state may differ (combined file, no running header, different caption), so read its filings
before assuming the Connecticut format, and add a `<state>.md` here when you learn one.

## Workflow

1. **Find the requests.** They should be an extract under `context/sources/` (use `ingest-source`,
   and `ctpura-documents` for Connecticut, if not). Read the instructions at the top of the requests:
   they can change what the response must contain (native Excel, sworn statements, supplementation).
2. **Create the file.** `just new-interrogatory-responses reports/<report>/<name>.qmd` writes the
   `interrogatory_responses:` block with every field a `[PLACEHOLDER]`. Fill it in (fields are
   explained in `context/code/interrogatory_responses_user_guide.md`). Set `source_extract` to the
   extract and `expected_responses` to the count.
3. **Copy in the questions, verbatim.** For each question add `## <label>` (the label as the
   requester printed it, e.g. `CIEC-1`), then a `::: {.question}` block with the question text and
   an empty `::: {.response}` block. Lettered parts go one per line as `a. ...`, `b. ...`. Join a
   sentence the PDF broke across a page; change nothing else, not even a typo or a hyphen. Do **not**
   paraphrase or tidy. Then run `just check-interrogatory-responses <qmd>`: it confirms every line of
   every question appears in the extract and tells you exactly where a line diverges. Fix the QMD
   until it passes; never "fix" the extract.
4. **Write the responses** (conventions below), with final citations from the first draft on.
   `just check-interrogatory-responses` lists how many are still unwritten and fails on citation
   problems it can detect.
5. **Render for review.** From the report folder, `just interrogatories` writes
   `<name>_<date>.docx`: every response on its own pages with the filed header. Send that to counsel.
   Fold their comments into the QMD and re-render; the QMD is the source of truth.
6. **Render for filing.** Set `date_filed` to the real date and `draft: false`, then
   `just interrogatories-split` writes one `.docx` per response into `filing/`. Counsel (or we) save
   each as PDF from Word and upload them, with any attachments, using the state's filing form.
   Word fills in the "Page n of N" fields on opening; check one file's header before sending.

## Writing a response

- **Answer exactly what is asked, part by part.** Use the question's own letters: `a.`, `b.` as
  paragraphs starting with the letter. A yes/no confirmation starts with "Confirmed." or "Not
  confirmed." and then explains. Do not argue beyond the question.
- **Voice.** Same as the testimony: the Switchbox report voice (step 1 of the `expert-testimony`
  skill) in the testimony's formal register. First person singular ("I did not prepare," "my
  analysis shows"), no contractions, "CLF and Sierra Club" in the third person, exact numbers,
  "would" for modeled outcomes, no hedge words. Be shorter than the testimony: answer the question
  in the fewest sentences that fully do so, then stop. No restating the question, no background the
  testimony already gives (cite it instead), no advocacy. Say what was and was not done: if the
  request asks for an estimate the witness did not prepare, say so and why (the requests often ask
  this directly).
- **Every citation goes in a footnote, in the testimony's paralegal format** (read
  `expert-testimony/citations.md` before writing one). That includes the witness's own testimony,
  the Company's exhibits and its data responses, not only outside documents. The response text says
  what the source shows; the footnote says where. In each response, cite a source in full the first
  time (with its date and its `pub.switch.box` short link) and in short form or `_Id._` after that,
  with `[@key]` once per footnote (Word drops the tags, so the footnote must read completely without
  them). Pinpoints are `at 14`, `at 14:5–7`, `at 14 n.8` or `at 20 ¶ 54`, never "p." or "PDF p.".
- **Drafts get final citations too**, including a first pass written as bullet points. Never leave
  a citation key, a "p. 21" or an inline "(Velez Direct at …)" to tidy later: write the footnote in
  full now. If a pinpoint cannot be verified yet, write the footnote anyway and flag the gap inside
  it, e.g. `**[NOT INGESTED]**` or `**[TK: no public copy to link yet]**`. Discussion and counsel
  blocks (`> **[DISCUSSION FOR JPV]**`, `**[COUNSEL]**`) are notes to the witness and may cite inline.
- **Get every pinpoint from `just sources-cite`**, never by counting or from memory, and quote the
  source's exact words in a parenthetical where the response relies on its wording. A set of data
  responses often reprints earlier answers word for word, so the same passage can turn up several
  times: read every hit `sources-cite` prints, check which response each is in, and cite the
  original.
- **Put derivations in footnotes.** The response text gives the number and what it is ("CL&P's share
  of ISO New England's forecast"); the footnote gives the arithmetic, its inputs and their sources,
  with the inputs computed inline.
- **Footnote mechanics.** Put the definition right after the paragraph or bullet that uses it,
  indented to that item's text (3 spaces under `a.`, 5 under a `-` bullet inside it), with a blank
  line before and after; without the blank line after, Pandoc folds a following paragraph into the
  note. Give every use its own footnote: Pandoc prints a note again for each reference to it.
- **`just check-interrogatory-responses` enforces the mechanical parts**: it fails on an inline
  citation in the response text, a citation key used as a citation, a "p." pinpoint, a footnote
  without a blank line after it, and a footnote that is undefined, unused, or used twice. Run it after
  every drafting pass, not just before rendering.
- **Never hardcode a number.** If a number comes from the analysis, compute it inline like testimony.
  A number that is also in the filed testimony must match it.
- **Attachments are separate files, not embedded.** Excel workbooks (build them with the
  `calculation-workbook` skill, formulas intact), CSVs and similar are uploaded next to the response
  PDF. Name each `<label> Attachment <n>.<ext>` and refer to it by that name in the response
  ("See CIEC-3 Attachment 1."). If no workbook exists because the analysis is in Python, say so and
  point to the code, as CLF-SC did for CIEC-1 (a provenance table; see `testimony-provenance`).
  Keep a list of each response's attachments for the filing note.
- **Objections and privilege.** State the basis in the response. A privilege claim needs a sworn
  statement filed with the responses if the requests' instructions say so (CIEC's do).
- **Duty to supplement.** Requests usually require correcting or supplementing a response until the
  decision. Note it in your handoff to counsel.
- **Do not guess at facts about the Company, other parties or the record.** Check the extracts, and
  mark what you cannot support for counsel.

## Rendering internals

`lib/just/interrogatory.py` (fields, checks, render, header patching),
`lib/just/templates/filters/interrogatory.lua` (caption block and section breaks),
`lib/just/templates/build_interrogatory_response.py` (the Word model file; rebuild with
`uv run python -m lib.just.templates.build_interrogatory_response` and commit the `.docx`).

Pandoc cannot write a different header for each Word section, so each response ends with a section
break and the Python step patches a header part onto each section afterwards. The header uses the
`PAGE` and `SECTIONPAGES` Word fields, so each response restarts at "Page 1 of N" with its own N.
LibreOffice and Google Docs do not support `SECTIONPAGES` (they show "of 1"), so the combined review file
should be opened in Word. `--split` runs the same render once per response with `-M ir-only:<label>` and
uses `NUMPAGES` instead (one section per file, same count), which works in Word and LibreOffice.
