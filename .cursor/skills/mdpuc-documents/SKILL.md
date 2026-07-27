---
name: mdpuc-documents
description: >-
  Fetches Maryland PSC (MDPUC) regulatory PDFs from the DMS MailLog search or
  psc.maryland.gov uploads, then extracts them to high-quality markdown for the
  reports2 context corpus. Use when working with Maryland PSC, MDPUC, maillog,
  ML number, DMS, PC44, rate case filings, DRIVE Act orders, or
  context/sources/md_hp_rates/.
---

# Maryland PSC (MDPUC) Documents

Fetch and extract Maryland Public Service Commission filings for the reports2
`context/sources/md_hp_rates/` corpus. **Fetch and extract are two separate
phases** — never dump raw PDF text into the repo.

## Before you start

1. Identify what you have: **MailLog (ML) number**, **case number**, or a
   **psc.maryland.gov URL**.
2. Read quality references:
   - `context/sources/md_hp_rates/mdpuc_240945_pc44_tou_rate_design_work_group_report.md` — target extract quality
   - `rate-design-platform/.cursor/commands/extract-pdf-to-markdown.md` — extraction standards (read in full before extracting)
3. Check `context/README.md` for existing `md_hp_rates/` entries — avoid duplicates.

## Decision tree

```
Have a MailLog (ML) number?
├─ YES → Technique 1: MailLog search (PRIMARY)
│         Use scripts/fetch_maillog_pdf.py or manual workflow in reference.md
│
└─ NO → Have a direct psc.maryland.gov/wp-content/uploads/ URL?
         ├─ YES → Technique 2: PSC flat PDF fetch
         │         curl/wget the URL; verify %PDF header and size > 1 KB
         │
         └─ NO → Have case number only?
                  ├─ Browse case jacket (human/JS browser):
                  │    https://webpscxb.pscmaryland.com/DMS/case/{case_no}
                  │    Find ML numbers in filing list → retry Technique 1
                  │
                  └─ Web search psc.maryland.gov for order PDFs
                       (e.g. Order-91917_ML-323522-9761-1.pdf)
                       → Technique 2
```

**Default rule:** If you have an ML number, always use MailLog search. Never
guess a `pdfview/Public/...` DMS path from a filing index.

## Phase 1: Fetch PDF

### Technique 1 — MailLog search (PRIMARY)

**Search UI:** https://webpscxb.pscmaryland.com/DMS/maillogsearch

**Helper script (preferred):**

```bash
uv run python .cursor/skills/mdpuc-documents/scripts/fetch_maillog_pdf.py \
  <ML_NUMBER> \
  -o context/sources/md_hp_rates/mdpuc_<ML>_<slug>.pdf
```

**Workflow (if scripting manually):**

1. GET `maillogsearch` → extract `__VIEWSTATE`, `__VIEWSTATEGENERATOR`
2. POST with `ctl00$ContentPlaceHolder1$txtSearch=<ML#>` and
   `ctl00$ContentPlaceHolder1$btnSearch=Search`
3. Parse search results for `data-pdf` (single **or** double quotes) on
   `btnOpenPdf` → opens `/DMS/maillogpdfview/MailLog/0/0/{ML}/0`
4. GET maillogpdfview page → parse `data-pdf` on `btnOpenPdfFile` for the
   **actual** pdfview path
5. GET that pdfview URL → save PDF; verify `%PDF` magic bytes and size ≫ 1 KB

**Critical pitfall:** Direct DMS filing URLs like
`pdfview/Public/PC44/101/0/0/218934_D0121712~pdf` often return **0 bytes**.
MailLog resolves the real path (e.g. `218934_D0051941~pdf` under
`` `%60%60wportal%60Documents%60DMS%6021%608934%60/` `` with backtick-encoded
segments).

**Example:** ML 218934 → PC44 Rate Design Final Report (31 pages, ~368 KB).

Full curl/Python details: [reference.md](reference.md).

### Technique 2 — PSC flat PDF uploads

**Base:** https://psc.maryland.gov/wp-content/uploads/

Often organized by `YYYY/MM/`. Orders may be named like
`Order-91917_ML-323522-9761-1.pdf`.

```bash
curl -fsSL -o context/sources/md_hp_rates/mdpuc_9761_order_91917_drive_act.pdf \
  "https://psc.maryland.gov/wp-content/uploads/Order-91917_ML-323522-9761-1.pdf"
```

**Example straw proposal:**
`https://psc.maryland.gov/wp-content/uploads/2025/11/PSC-04.17.17-PC44-Rate-Design-straw-6-28-17-WG.pdf`

No VIEWSTATE needed. Always verify download size and `%PDF` header.

### Fallback — Case jacket browser

**URL:** https://webpscxb.pscmaryland.com/DMS/case/{case_no}

Useful for humans to find ML numbers and filing titles. Requires a
JavaScript-capable browser; headless direct PDF URLs from the jacket are
unreliable. When MailLog search fails, try psc.maryland.gov uploads or ask the
user to browse the case jacket and provide an ML number.

See also `context/domain/md_drive_act_tou.md` for case numbers, ML numbers, and
DMS navigation notes.

## Phase 2: Extract PDF → markdown

Extraction is **separate from fetch**. Follow
`rate-design-platform/.cursor/commands/extract-pdf-to-markdown.md` in full.

### Quality bar

Match `mdpuc_240945_pc44_tou_rate_design_work_group_report.md`:

- Flowing paragraphs (no mid-sentence line wraps from PDF columns)
- Proper `#` / `##` hierarchy matching source sections
- Markdown tables for tabular data
- Footnotes as `[^n]` with definitions at section end or in **Footnotes**
- `[DIAGRAM DESCRIPTION: ...]` blocks for figures/charts
- Front matter: Source, Pages, Date, Author(s), Maillog, Proceeding/Case

### Anti-patterns (explicitly rejected)

Do **not** ship any of these as final extracts:

| Anti-pattern                            | Why it fails                                                             |
| --------------------------------------- | ------------------------------------------------------------------------ |
| Raw `pdftotext` output                  | Broken mid-sentence wraps, column bleed                                  |
| Naive `page.get_text("text")` line dump | Duplicate letterhead, footnote text in body                              |
| Unjoined paragraph fragments            | Unreadable for agents and humans                                         |
| Duplicate table fragments               | PDF layout splits tables across pages                                    |
| Max-font-size footnote detection        | Footnote markers are often 6.5pt glued to 10pt body text (e.g. `AMI).6`) |

### Preferred extraction approach

1. Read the extract command; work **section by section** with structure in mind.
2. Use PyMuPDF `page.get_text("text")` or `get_text("dict")` for drafting only.
3. **Post-process:** join broken lines into paragraphs; strip repeated PSC
   letterhead blocks; move footnote bodies out of main text.
4. Convert footnotes manually — locate superscript numbers in PDF visually;
   do not rely on font-size heuristics alone.
5. Rebuild tables by hand when PDF layout breaks them; verify column counts.
6. Run the extract command's **Quality Checklist** before saving.

### Extraction checklist

Copy and complete before saving `.md`:

```
Extract quality:
- [ ] Front matter complete (Source, Pages, Date, Maillog/Case)
- [ ] Heading hierarchy matches source TOC
- [ ] Paragraphs flow (no PDF line-wrap artifacts)
- [ ] PSC letterhead/cover boilerplate stripped or minimized
- [ ] All tables in markdown table format
- [ ] Footnote ref count == footnote definition count (per chapter if reset)
- [ ] Figures have [DIAGRAM DESCRIPTION] blocks
- [ ] Hyperlinks converted to [label](URL)
- [ ] Minor typo blanket note in front matter (if corrections made)
- [ ] Compared spot-check against PDF (first page, one table, one footnote page)
```

## File naming and repo conventions

| Item        | Convention                                                                 |
| ----------- | -------------------------------------------------------------------------- |
| Directory   | `context/sources/md_hp_rates/`                                             |
| With ML#    | `mdpuc_{maillog}_{short_slug}.pdf` + matching `.md`                        |
| Without ML# | `mdpuc_{case}_{short_slug}` (e.g. `mdpuc_9761_order_91917_...`)            |
| Slug style  | lowercase, underscores, descriptive (e.g. `pc44_rate_design_final_report`) |

**After adding a source:** add a row to `context/README.md` under `sources/`.

**Do not:**

- Edit `reports/references.bib` (Zotero-managed)
- Add working plans or agent artifacts under `context/`
- Commit large PDFs without user request (PDFs in `context/sources/` are OK when part of the corpus)

## Worked examples

| Document                   | ML     | Fetch method    | Files                                                   |
| -------------------------- | ------ | --------------- | ------------------------------------------------------- |
| PC44 Final Report          | 218934 | MailLog search  | `mdpuc_218934_pc44_rate_design_final_report.*`          |
| PC44 TOU Work Group Report | 240945 | MailLog search  | `mdpuc_240945_pc44_tou_rate_design_work_group_report.*` |
| Order 91917 (DRIVE Act)    | 323522 | PSC flat upload | `mdpuc_9761_order_91917_drive_act_implementation.*`     |
| PC44 straw proposal        | —      | PSC flat upload | `mdpuc_pc44_rate_design_straw_proposal_20170627.*`      |

## Additional resources

- [reference.md](reference.md) — MailLog HTTP workflow, curl examples, HTML parsing notes
- `scripts/fetch_maillog_pdf.py` — tested helper for Technique 1
- `context/domain/md_drive_act_tou.md` — case jackets, ML numbers, DRIVE Act context
- `context/domain/bge_tou_rates.md` — BGE TOU / PC44 background
