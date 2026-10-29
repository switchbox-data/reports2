---
description: Extract PDF to markdown preserving structure, formatting, tables, equations, and visual descriptions
argument-hint: <path-to-pdf-file>
---

# PDF to Markdown Extraction

You are extracting a technical PDF into a **standalone, fully-formatted markdown document** that preserves as much information as possible while remaining readable and useful without the original PDF.

## Core Principles

1. **Primary audience is LLMs/agents** consuming the markdown as context. Prefer clarity and completeness over brevity: keep equation labels, explicit section structure, and full figure descriptions. Human-friendly rendering is secondary but desirable (e.g. LaTeX for math, proper lists).
2. **Fidelity over brevity**: Preserve every meaningful piece of information
3. **Structure preservation**: Keep original document hierarchy, sections, subsections
4. **Formatting in markdown**: Use markdown formatting (bold, italics, code blocks, etc.) to mirror original emphasis
5. **Impossible content handling**: For diagrams, charts, images—provide detailed textual descriptions inline
6. **Standalone design**: A reader should be able to work from this markdown alone; the PDF is emergency reference only
7. **LLM-friendly markers**: Use clear, parseable markers when you must indicate "see PDF for visual"

### Long Documents (30+ pages)

For source PDFs longer than ~30 pages, **maintain the same fidelity throughout the entire document**. Do not allow quality to degrade in later sections — every chapter deserves the same level of verbatim transcription, footnote capture, and figure description as the first. Specifically:

- Work section by section at a consistent pace. If the Executive Summary was extracted near-verbatim, body chapters must be too.
- Do not switch from transcription to summarization partway through. If you find yourself writing "the section discusses X" instead of reproducing the actual text, stop and transcribe.
- For very long documents (80+ pages), it is acceptable to use multiple passes — extract the first half, save, then continue — rather than compressing later content.

## Extraction Instructions

### Structure & Hierarchy

- Preserve all heading levels (H1→H2→H3, etc.)
- Maintain table of contents structure if present
- Keep section numbers, subsection labels, and organizational schemes from original. **When the source has a table of contents**, verify that numbered section titles and counts in the extract match the TOC (e.g. the last numbered section in the extract should correspond to the last TOC entry; unnumbered headings on the same page as a numbered section may stay unnumbered).
- Preserve logical document sections with `---` between them if they marked distinct parts

### Text & Formatting

- **Bold** for emphasis (use `**text**`)
- _Italics_ for terms and citations; **preserve source italics**, especially in legal and regulatory documents: case names, signals (_See_, _See, e.g._, _Id._, _infra_), and any words the source emphasizes inside a quotation. When the text says "(emphasis added)" or "(emphasis in original)", the emphasized words **must** be italic in the extract, or the parenthetical is meaningless. Check font flags (e.g. PyMuPDF span flags / font names) rather than relying on plain text. For variable names and short math in prose use inline math `$...$` (see Equations below)
- `code` for technical terms, file paths, code snippets
- Preserve numbered and bulleted lists with correct nesting. **When the source has an inline numbered list** (e.g. "commissions should 1) … 2) … 5)" or "(1) … (2)" in one paragraph), **convert it to a markdown list** (numbered or bullet) unless that would break the flow of the paragraph.
- Keep paragraph structure and grouping exactly as in original
- Convert hyperlinks to markdown format: `[link text](URL)`. **Read hyperlink targets from the PDF's link annotations** (e.g. PyMuPDF `page.get_links()`), not just the printed text; never write that URLs are "not recoverable" without checking the annotations. If a target is an authenticated or session-specific URL (sign-in redirects), say so instead of reproducing a long token. When a URL appears as a bare link without surrounding descriptive text (common in footnotes of legal/regulatory documents), wrap it with a short descriptive label: `[Short Description](URL)` (e.g. `[2022 NYISO Gold Book](https://...pdf)`).
- **Sidebar boxes, callout panels, and inset text** (visually set apart from the main body — e.g., case studies, worked examples, "Challenge and Opportunity" boxes, marginal definitions): Preserve these in full. Format each as a blockquote or with a clear header indicating the sidebar title (e.g., `> **Remote Disconnection and Reconnection: Challenge and Opportunity**`). Do not silently drop sidebars; they often contain substantive content not duplicated in the main text.

### Source Errors, Typos, and Cross-References

Source PDFs often contain typos, missing words, or erroneous internal cross-references (e.g. "Section 4.1" when the content is clearly in Section 5.1). The goal is to make the extract easy for agents to reason about while preserving traceability to the original.

- **Minor typos** (misspellings, missing prepositions, obvious letter transpositions like "fro" for "for"): Correct them silently for readability, but add a blanket note in the front matter **only if you actually corrected any** (if the text is verbatim, say so instead, and never claim corrections that were not made): _"Note: Minor typographical errors in the source (e.g. "an" for "and", "fro" for "for") have been corrected for readability. Substantive corrections are annotated inline."_
- **Erroneous cross-references** (section numbers, figure numbers, or other internal references that are clearly wrong given the document's own structure): Correct the reference to what it clearly means, and add an inline bracketed annotation preserving the original: `Section 5.1 [source says "Section 4.1"]`. This lets agents follow the correct reference while knowing the source differed.
- **Truncated text** (e.g. a footnote or sentence cut off at a page break): Include whatever text is present, then add a bracketed note: `[text truncated at page break in source]`.
- **Ambiguous cases** (where it's unclear whether the source text is an error or intentional): Preserve the original text exactly and do not correct it. If warranted, add a bracketed note: `[sic]` or `[sic; possibly intended "X"]`.

### Extractor-Added Content (Non-Source)

Extracts are used as citable source context, so a reader must always be able to tell what the PDF says from what the extractor (human or agent) added.

- **Anything not printed in the PDF must be visibly marked as non-source.** This includes: metadata inferred from filenames, manifests, or other documents (docket numbers, filing dates, sponsoring witnesses, "Rate X / initial phase" glosses); interpretive comments, tags, or summaries (including hidden HTML comments); derived arithmetic (ratios, shares, recomputed totals); cross-document comparisons; and reading guides. Use an explicit label such as `_Extractor note (not source text): …_` or a front-matter field value like "not stated in the PDF; …". Do not put inferred values in front-matter fields as if they were printed (for example, write "Docket: not printed on the exhibit (extractor note: ICC Docket 24-0378)").
- **Do not state facts about other documents or pages the PDF does not support** (for example, "unchanged from the previous revision", "identical to the 2025 filing") unless you verified them and cite the file. Keep such claims in a labelled extractor note.
- **Summary or comparison tables that span periods or revisions** must put each value under the period it applies to, label every column with its billing period, and note when a printed value is not applicable in that period (for example, a "summer" rate printed in a table for months with no summer billing). Do not place a value under a header whose period it does not match.
- **Source inconsistencies are findings, not errors to fix**: when the source's own numbers do not reconcile (a printed percentage that disagrees with the printed counts, a total off by one, an empty cell in a calculation), keep the printed value and add a bracketed `[source discrepancy: …]` note with the arithmetic.

### Tables

- Convert **ALL** tables to markdown table format
- Preserve column headers and cell content exactly
- **Multi-column factor tables**: For tables with many numbered or lettered columns (e.g. (1)–(13), or A, B, C…), **verify column alignment for every row**, including the last. If one row has fewer or more populated cells than others (e.g. due to PDF layout or wrapping), ensure the extract preserves the same number of columns per row and does not drop or merge columns; add or align cells so each row matches the header.
- **When the PDF text layer scrambles a table** (spreadsheet-style pages, empty cells dropped, column order shuffled), render the page to an image and read row/column positions from it. Describe the method as "reconstructed" only if the rendered page cannot be read. Verify by arithmetic where possible (base × factor, row sums against printed totals).
- **Very long tables** (hundreds or thousands of rows, e.g. an 8,760-hour series): include a representative sample in the markdown, write the full table to a verified CSV alongside the markdown (diffed programmatically against the PDF), and state at the table location exactly which rows are omitted from the markdown and where the CSV is. Update `context/README.md` for the CSV.
- **When table content cannot be extracted** from the PDF (e.g. exhibit or appendix pages yield only titles or the table is image-based), do not invent cell data. Add an explicit note in the extract: _"Table content was not extractable from the PDF; description below is inferred from surrounding text. See original PDF for data."_ Then provide a short description of the table’s purpose and structure based on the narrative, and a "[→ See original PDF page X]" pointer.
- If a table is complex/wide, add a description before it explaining its structure
- Complex tables that don't render cleanly: provide both a prose description and the markdown version
- Keep alignment indicators if relevant (left, center, right aligned)
- **Table footnotes**: When the source has footnotes or notes tied to a table (e.g. superscripts in cells, "Notes:" or "Source:" below the table), handle them consistently: either (a) use markdown footnote refs in cells and `[^n]:` definitions below the table, or (b) fold the footnote text into the table caption or a single "Note:" or "Notes:" line immediately below the table. Choose one approach per document and apply it to all tables with footnotes.

### Equations & Mathematical Content

- **In running text**: Use **inline math** `$...$` for variable names and short expressions (e.g. $r_i$, $MC_h$, $\epsilon$, $ProposedRate_h$). This keeps math unambiguous for LLMs and renders well for humans.
- **Display equations**: Use **block math** `$$...$$` with LaTeX. Keep an optional label line above (e.g. `**Equation (1):**`) so the equation is tied to the text.
- Keep equations in original notation (LaTeX preferred). If equation is explained in surrounding text, include that text.
- For critical visual elements where the equation is unreadable in the PDF: `[EQUATION: describe what it shows]` before/after the transcribed formula.
- Reconstruct equations from surrounding prose and equation numbers when the PDF text extraction yields garbled symbols.

### Diagrams, Charts, Figures, Images

**First inventory every page for embedded images and vector charts** (e.g. PyMuPDF `page.get_images()` and `page.get_drawings()`, plus rendering each page and looking at it), including small charts on text-heavy pages and images that carry tables or bill excerpts. A chart caption must stay attached to its chart; never turn a figure caption into body text. Numbers read from rendered images (sample bills, screenshots, image-only tables) must be re-verified digit by digit at high DPI, since 6/8 and 1/7 misreads are common.

**For EVERY diagram/chart/figure in the PDF:**

1. **Provide a detailed, comprehensive verbal description** placed inline where the diagram appears in the original
2. **Use this format:**

```
   [DIAGRAM DESCRIPTION: <exact title from PDF>]

   <detailed prose description including:>
   - What type of diagram it is (flowchart, map, graph, schematic, etc.)
   - All labeled elements and components
   - Spatial relationships and connections between elements
   - For charts: axes labels, units, scale, data ranges, trend lines
   - For maps: geographic regions shown, color/pattern meanings, scale
   - Color coding, shading patterns, line styles if relevant to interpretation
   - What insight, relationship, or information the diagram conveys
   - Any legends or keys explained inline

   [→ See original PDF page X for visual rendering]
```

3. **Real example:**

```
   [DIAGRAM DESCRIPTION: Continental US Power Flow Coloring Scheme]

   A geographic map showing North America with transmission corridors overlaid.
   Transmission lines are color-coded by primary power flow direction: red
   indicates southward flow, blue indicates northward flow. Line thickness
   represents transmission capacity, with thicker lines indicating higher capacity.
   The diagram reveals regional patterns: Great Plains shows primarily north-to-south
   flows from wind generation, the Northeast shows complex multi-directional flows
   reflecting its interconnected grid, and the Southwest shows strong south-to-north
   flows. This visualization demonstrates how transmission constraints vary regionally
   and which directions are capacity-constrained.

   [→ See original PDF page 42 for visual rendering]
```

4. **For screenshots/UI mockups**: Describe layout, button locations, form fields, displayed data, visual hierarchy

5. **For flowcharts/process diagrams**: Describe flow path, decision points, inputs/outputs, process steps in order

6. **Preserve figure-referencing transitional sentences.** When the source text introduces a figure with a sentence like "Figure 3 shows the historical values for X" or "Figure 7 presents the projected installations," preserve that sentence as standalone text **before** the `[DIAGRAM DESCRIPTION]` block. Do not drop these sentences or fold them into the diagram description — they are part of the source prose and connect the narrative to the visual. The pattern is: transitional sentence → `[DIAGRAM DESCRIPTION]` block → any post-figure discussion.

### Citations & References

- Preserve citation format exactly: `(Author et al., Year)` or `[1]`, `[2]`, etc.
- Keep full reference entries at end of document in "References" section
- Maintain all URLs, DOIs, publication details
- If citation appears multiple times, keep it consistent throughout

### Footnotes & Endnotes

- **Locate and preserve every footnote** in the source. Do not drop footnote text, definitions, or URLs. Output each footnote either as a markdown footnote (`[^n]` in body with `[^n]: content` in a **Footnotes** section) or inlined at the reference point; in either case, the full content (including any URLs, citations, or definitions) must appear in the extract.
- Keep footnote text **verbatim**, including closing pointers such as "For more information, please refer to …"; do not paraphrase or shorten it.
- Preserve ALL footnote content—nothing drops. If a footnote reference triggers a linter (e.g. "unused reference definition"), you may **inline the footnote content** into the body at the reference point and remove the footnote definition, provided no content is lost.
- Keep numbering/order from original (or renumber from 1 if the source uses different numbering).

### OCR-Based Extractions

Some PDFs are scanned images with no embedded text, requiring OCR (e.g. via tesseract or PyMuPDF's `get_textpage_ocr`). When OCR is needed:

- **Note it in the front matter.** Add a line to the metadata block: `**Extraction method**: OCR (source PDF is image-based)`. Also include a blanket note: _"This document was extracted via OCR from a scanned PDF. Minor recognition errors may remain; low-confidence values are marked with `[?]`."_
- **Mark low-confidence values with `[?]`.** When OCR produces ambiguous or garbled text — especially in table cells, numbers, or proper nouns — include your best reconstruction followed by `[?]`. For example: `0.58 [?]` or `Smith [?]`. This signals to downstream consumers that the value may need manual verification against the original PDF.
- **Use the highest practical DPI** (300+ recommended) for OCR to maximize recognition quality.
- **For tables that OCR cannot extract** (e.g. complex spreadsheet images), do not invent cell data. Add: _"Table content was not extractable from the PDF; description below is inferred from surrounding text. See original PDF for data."_ Then describe the table's purpose and structure based on the narrative.

### Content You Cannot Fully Extract

**Logos/branding graphics**: Skip unless essential

**Decorative photographs**: Skip

**Letterhead/covers**: Extract text only

**Hand-drawn annotations**: Describe if meaningful

**Color-critical diagrams**: Provide description, note to see PDF for precise colors

**High-precision technical drawings**: Describe relationships and elements, note PDF shows exact proportions

### Output Structure

The extract starts with **flat YAML front matter**, then the document. Source ingest (`just sources-ingest`) writes the identifying fields (`citekey`, `zotero_item`, `public_url`, `short_url`, `source_url`, `md5`) once the source is in Zotero; you add or keep the descriptive ones. Everything in the front matter must be printed in the PDF or marked as not printed (see Extractor-Added Content).

```
---
source_file: <original filename>.pdf # always the PDF's own file name
citekey: <citation key, if ingest has already assigned one>
docket: <as printed, if any>
utility: <if relevant>
filing_date: <YYYY-MM-DD, if printed>
filer: <organization that filed or issued it>
document_type: <order | testimony | exhibit | tariff | report | paper | ...>
pages_total: <N>
extraction_scope: <full | partial: what is covered>
context: <why it exists: who made it, for whom, what it responds to or sets in motion>
contents: <what is in it, broadly>
why_here: <what we might use it for: the question it answers for us>
---

# [Document Title]

**Source**: [Original filename]
**Pages**: [X total pages]
**Date**: [Publication/modification date if present]
**Author(s)**: [Names; if the PDF has superscript numbers, list names with affiliations below]
**Author affiliations**: Extract from the first page: correspondence author (e.g. "Author for correspondence", email), and each numbered affiliation (institution, address). Omit only if the PDF has no affiliation block.

---

[Document content here, preserving original hierarchy]

---

## References

[Complete reference list]
```

When the source PDF contains them, include short back-matter sections such as **Acknowledgments**, **Funding**, **Author Contributions**, **Data Statement**, **Conflicts of interest**, or similar—preserve their headings and full text.

### Quality Checklist

- [ ] All heading levels preserved (H1, H2, H3, etc.)
- [ ] Text formatting (bold, italics, code, links) matches original emphasis
- [ ] **ALL tables extracted to markdown table format**
- [ ] **Every figure, diagram, and chart has detailed verbal description**
- [ ] Equations preserved in original notation
- [ ] All citations and references complete and linked
- [ ] All footnotes and endnotes preserved
- [ ] **Footnote count verified (mandatory)**: Before finalizing, count footnote **reference marks** in the source PDF (superscript numbers, symbols, or `[n]` markers in body text) and count footnote **definitions** in the extract (`[^n]:` lines or inlined equivalents). The counts **must** match. If the source has N footnotes, the extract must have exactly N footnote definitions. When footnotes are numbered per-chapter (resetting to 1 in each chapter), count per chapter and verify each. This is the single most commonly failed check — do not skip it.
- [ ] Source italics and "(emphasis added)" words preserved; hyperlink targets taken from link annotations; every page checked for images/charts
- [ ] Everything not printed in the PDF (inferred metadata, interpretation, derived numbers, hidden comments) is explicitly labelled as non-source
- [ ] Summary/comparison tables label each value with the period it applies to
- [ ] Source errors handled: minor typos corrected with blanket note in front matter (only if corrections were made); erroneous cross-references corrected with inline `[source says "…"]` annotations; truncated text noted
- [ ] No orphaned content (mentioned but not included)
- [ ] Section numbers, titles, labels preserved exactly
- [ ] Document reads as complete, standalone resource
- [ ] "See PDF" markers only for visual elements (colors, layouts, photos)
- [ ] Markdown syntax valid and renders cleanly
- [ ] List nesting correct

## When to Say "See PDF"

**DO reference for:**

- Color differentiation that's semantically important
- Precise visual layouts requiring exact positioning
- Photographic content (describe what's shown; see PDF for image)
- Hand-drawn elements
- Multi-layer overlapping visuals

**DO NOT reference for:**

- Any textual information (describe instead)
- Table content (extract it)
- Equation meaning (transcribe it)
- Document structure (recreate it)
- Citations (extract them)
- Text emphasis (apply markdown)
- Conceptual diagrams (describe in prose)

## Output filename and location

- **Filename**: The markdown file **must** use the same base name as the PDF, with a `.md` extension. Example: `bill_alignment_test.pdf` → `bill_alignment_test.md`.
- **Location**: `context/sources/<project>/`, where `<project>` is the project folder named on the source's details card (for example `ma_hp_rates`), or `context/sources/` itself for general reference. Never put a copy of the PDF in the repo: `context/sources/**/*.pdf` is gitignored, and the original lives in Zotero.
- **Index**: One row per file in the sources table of `context/README.md` (and in the project folder's README `File` table, if it has one). `just sources-ingest` adds these rows from the approved card; if you create an extract by hand, add them yourself.

## Process

The PDF file path or citation key is provided as: **$ARGUMENTS**

0. **Get the PDF.** If the argument is a citation key (e.g. `madpu_Docket2555Order_2025`), run `just fetch-source <citekey>`; it downloads the original from Zotero next to where the extract belongs and prints the path. If the argument is a file path, use it as given. If the source has not been ingested yet, ask the user to run the ingest-source skill first, so the extract gets its citation key.

1. Examine PDF structure first (TOC, sections, page count). From the first page, extract author affiliations and correspondence if present. If the document has a TOC, note the section numbers and page mapping so the extract’s heading numbers match (e.g. last numbered section = last TOC entry).
2. Preserve structure exactly in markdown (include **Author affiliations** in metadata when available). Verify section numbers against the TOC before finalizing.
3. Extract section by section, applying all rules (inline math in prose, markdown lists for inline-numbered lists, equation labels).
4. For visual elements: stop and write detailed description
5. For complex tables: show prose description + markdown version
6. Build complete References section
7. Do final quality check against checklist
8. Output complete markdown as ready-to-use document
9. **Save the file** under `context/sources/<project>/` using the **same base name as the PDF** (e.g. `foo.pdf` → `context/sources/<project>/foo.md`). Write the flat front matter above, then run `just sources-status <citekey>`: it reports the extract's front matter and index rows as done or missing.

**Save the extract in full with the matching filename, ready to commit.**
