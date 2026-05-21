#!/usr/bin/env python3
"""Build the expert-testimony Quarto reference DOCX.

Generates ``lib/just/templates/expert_testimony.docx`` by starting from
Pandoc's built-in default reference doc and rewriting its ``styles.xml``
(and, in later iterations, ``document.xml`` / header / settings) so the
resulting reference matches Illinois Commerce Commission (ICC) testimony
formatting conventions:

* Times New Roman 12 pt, double-spaced body
* Heading 2 (``## section``): TNR 12 pt bold ALL CAPS underlined, centered
  — used for ICC-style ``I. Introduction``-type section headers. (The
  source QMD uses ``##`` for top-level sections because the title comes
  from YAML, so Pandoc maps ``##`` → Heading 2.)
* Heading 3 (``### subsection``): TNR 12 pt bold, left-aligned —
  used for ``A.``/``B.`` subsections under each Roman-numeral section.
* Heading 1: kept available (TNR 12 pt bold underlined centered) for
  authors who want a higher level. Rare in ICC testimony.
* Block quote: TNR 12 pt single-spaced, indented (used for the docket
  caption / ``STATE OF ILLINOIS`` block at the top of the testimony).

Run via::

    uv run python -m lib.just.templates.build_expert_testimony

This writes ``expert_testimony.docx`` next to this script. The reference
doc is consumed by ``lib.just.draft`` when invoked with ``--testimony``.

Note: ICC testimony also requires line-numbering in the margin, witness
header, and a cover page. Those features are layered on in subsequent
iterations of this script (see TODOs).
"""

from __future__ import annotations

import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE / "expert_testimony.docx"

# ---------------------------------------------------------------------------
# Section properties — page size, margins, line numbering, header reference.
# ---------------------------------------------------------------------------
# All sizes are in twips (1/20 of a point; 1440 twips = 1 inch).
#
# This sectPr lives at the very end of word/document.xml (just before
# </w:body>) and governs the *body* section (section 2). The cover/TOC
# section (section 1) is governed by the sectPr the testimony.lua
# filter injects mid-document at the <!-- testimony-body-start --> marker.
#
# - pgSz: Letter (8.5" x 11")
# - pgMar: 1" top/right/bottom, 1.2" left (extra room for the line
#   numbers in the gutter). Header 0.5" from top; footer 0.4" from bottom.
# - lnNumType: countBy=1 (every line numbered), restart=newSection
#   (the body restarts at line 1 — the cover/TOC pages have no line
#   numbering at all because section 1's sectPr omits lnNumType).
#   distance=240 twips (~0.17") puts the numbers just outside the text.
# - headerReference: pulls in word/header1.xml (witness header).
SECTPR_XML = """<w:sectPr>
    <w:headerReference w:type="default" r:id="rIdTestimonyHeader"/>
    <w:pgSz w:w="12240" w:h="15840" w:code="1"/>
    <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1728" w:header="720" w:footer="576" w:gutter="0"/>
    <w:lnNumType w:countBy="1" w:restart="newSection" w:distance="240"/>
    <w:cols w:space="720"/>
    <w:docGrid w:linePitch="360"/>
  </w:sectPr>"""

# ---------------------------------------------------------------------------
# Header (top of every page) — three right-aligned lines:
#   1. Exhibit identifier (e.g. "CUB Exhibit 1.0")
#   2. Witness name (e.g. "Juan-Pablo Velez")
#   3. "Page <auto>"
# ---------------------------------------------------------------------------
# ``{{EXHIBIT}}`` and ``{{WITNESS_NAME}}`` are substituted at draft time
# by ``lib.just.draft`` from the QMD YAML frontmatter (title / author /
# optional ``exhibit``). The page number uses Word's PAGE field code so
# it stays live when the document is opened in Word.
HEADER_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Header"/>
      <w:jc w:val="right"/>
      <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr>
    </w:pPr>
    <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr><w:t>{{EXHIBIT}}</w:t></w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Header"/>
      <w:jc w:val="right"/>
      <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr>
    </w:pPr>
    <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr><w:t>{{WITNESS_NAME}}</w:t></w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Header"/>
      <w:jc w:val="right"/>
      <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr>
    </w:pPr>
    <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr><w:t xml:space="preserve">Page </w:t></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:noProof/><w:sz w:val="22"/></w:rPr><w:t>1</w:t></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:b/><w:sz w:val="22"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:hdr>
"""

# Default placeholders baked into the template, overridden by draft.py
# at render time when the QMD frontmatter provides a value.
DEFAULT_EXHIBIT = "[EXHIBIT NUMBER]"
DEFAULT_WITNESS_NAME = "[WITNESS NAME]"

# ---------------------------------------------------------------------------
# Blank header — used by the cover page section so the cover doesn't show
# the witness/exhibit/page-number block at the top. (ICC convention is for
# the cover to be unadorned; the running header starts on page 2.) Pandoc
# requires a header part to exist if a section references it, but Word
# will render the cover with no visible header text because the only
# paragraph is empty and styled with the (mostly empty) Header style.
# ---------------------------------------------------------------------------
BLANK_HEADER_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Header"/>
    </w:pPr>
  </w:p>
</w:hdr>
"""

# ---------------------------------------------------------------------------
# styles.xml — full replacement for the Pandoc default reference doc
# ---------------------------------------------------------------------------
# All sizes are in half-points (24 = 12 pt). Line spacing of 480 with
# lineRule="auto" is double-spaced.

STYLES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto"/>
        <w:jc w:val="both"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:latentStyles w:defLockedState="0" w:defUIPriority="0" w:defSemiHidden="0" w:defUnhideWhenUsed="0" w:defQFormat="0" w:count="276"/>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
  <!-- BodyText is what Pandoc applies to body paragraphs after the first. -->
  <w:style w:type="paragraph" w:styleId="BodyText">
    <w:name w:val="Body Text"/>
    <w:basedOn w:val="Normal"/>
    <w:link w:val="BodyTextChar"/>
    <w:qFormat/>
    <w:pPr>
      <w:spacing w:before="0" w:after="240" w:line="480" w:lineRule="auto"/>
      <w:jc w:val="both"/>
    </w:pPr>
  </w:style>
  <!-- ICC Q&A formatting.
       Both styles share a hanging indent of 0.5" with a tab stop at
       0.5" so the bold "Q" / "A" marker sits in the gutter and the
       question/answer text wraps under itself.  The Lua filter
       (testimony.lua) injects a literal tab character after the
       marker, which Word resolves to that 0.5" tab stop.

       Question — uppercase + bold question text (handled by the Lua
       filter; the style itself only owns spacing/indent).  Answer —
       sentence-case answer text. -->
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="Question">
    <w:name w:val="Question"/>
    <w:basedOn w:val="BodyText"/>
    <w:next w:val="QuestionContinuation"/>
    <w:qFormat/>
    <w:pPr>
      <w:tabs>
        <w:tab w:val="left" w:pos="720"/>
      </w:tabs>
      <w:spacing w:before="0" w:after="240" w:line="480" w:lineRule="auto"/>
      <w:ind w:left="720" w:hanging="720"/>
      <w:jc w:val="both"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="Answer">
    <w:name w:val="Answer"/>
    <w:basedOn w:val="BodyText"/>
    <w:next w:val="AnswerContinuation"/>
    <w:qFormat/>
    <w:pPr>
      <w:tabs>
        <w:tab w:val="left" w:pos="720"/>
      </w:tabs>
      <w:spacing w:before="0" w:after="240" w:line="480" w:lineRule="auto"/>
      <w:ind w:left="720" w:hanging="720"/>
      <w:jc w:val="both"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <!-- Continuation paragraphs of a multi-paragraph Q&A.  The first
       paragraph of an answer uses the ``Answer`` style with a hanging
       indent (so the ``A`` marker hangs in the left gutter); follow-on
       paragraphs of the same answer use this ``AnswerContinuation``
       style — same left indent (so the text stays aligned with the
       answer column), no hanging (no marker on continuation rows), and
       a 0.25" first-line indent for paragraph delineation, matching
       the ICC exemplar.  ``QuestionContinuation`` is identical;
       defined separately so a future divergence is one-style-edit
       away. -->
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="AnswerContinuation">
    <w:name w:val="Answer Continuation"/>
    <w:basedOn w:val="BodyText"/>
    <w:next w:val="AnswerContinuation"/>
    <w:qFormat/>
    <w:pPr>
      <w:spacing w:before="0" w:after="240" w:line="480" w:lineRule="auto"/>
      <w:ind w:left="720" w:firstLine="360"/>
      <w:jc w:val="both"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="QuestionContinuation">
    <w:name w:val="Question Continuation"/>
    <w:basedOn w:val="AnswerContinuation"/>
    <w:next w:val="QuestionContinuation"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="character" w:customStyle="1" w:styleId="BodyTextChar">
    <w:name w:val="Body Text Char"/>
    <w:basedOn w:val="DefaultParagraphFont"/>
    <w:link w:val="BodyText"/>
  </w:style>
  <!-- FirstParagraph is Pandoc's "first paragraph after a heading" style. -->
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="FirstParagraph">
    <w:name w:val="First Paragraph"/>
    <w:basedOn w:val="BodyText"/>
    <w:next w:val="BodyText"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="Compact">
    <w:name w:val="Compact"/>
    <w:basedOn w:val="BodyText"/>
    <w:qFormat/>
    <w:pPr>
      <w:spacing w:before="0" w:after="0" w:line="480" w:lineRule="auto"/>
    </w:pPr>
  </w:style>
  <!-- Cover page styles all use <w:suppressLineNumbers/> so the docket
       caption / docket title block / author / date don't get line
       numbers in the gutter — line numbers should start with the body. -->
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="BodyText"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:suppressLineNumbers/>
      <w:spacing w:before="240" w:after="240" w:line="276" w:lineRule="auto"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:bCs/>
      <w:caps/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/>
    <w:basedOn w:val="Title"/>
    <w:next w:val="BodyText"/>
    <w:qFormat/>
    <w:pPr>
      <w:suppressLineNumbers/>
      <w:spacing w:before="120" w:after="240" w:line="276" w:lineRule="auto"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:caps w:val="0"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="Author">
    <w:name w:val="Author"/>
    <w:next w:val="BodyText"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:suppressLineNumbers/>
      <w:jc w:val="center"/>
    </w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Date">
    <w:name w:val="Date"/>
    <w:next w:val="BodyText"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:suppressLineNumbers/>
      <w:jc w:val="center"/>
    </w:pPr>
  </w:style>
  <!-- TOC entries shouldn't get line numbers either. -->
  <w:style w:type="paragraph" w:styleId="TOC1">
    <w:name w:val="toc 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:uiPriority w:val="39"/>
    <w:pPr>
      <w:suppressLineNumbers/>
      <w:spacing w:before="0" w:after="100" w:line="276" w:lineRule="auto"/>
      <w:jc w:val="left"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TOC2">
    <w:name w:val="toc 2"/>
    <w:basedOn w:val="TOC1"/>
    <w:next w:val="Normal"/>
    <w:uiPriority w:val="39"/>
    <w:pPr>
      <w:suppressLineNumbers/>
      <w:ind w:left="220"/>
    </w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TOC3">
    <w:name w:val="toc 3"/>
    <w:basedOn w:val="TOC1"/>
    <w:next w:val="Normal"/>
    <w:uiPriority w:val="39"/>
    <w:pPr>
      <w:suppressLineNumbers/>
      <w:ind w:left="440"/>
    </w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="TOCHeading">
    <w:name w:val="TOC Heading"/>
    <w:basedOn w:val="Heading1"/>
    <w:next w:val="Normal"/>
    <w:uiPriority w:val="39"/>
    <w:qFormat/>
    <w:pPr>
      <w:suppressLineNumbers/>
    </w:pPr>
  </w:style>
  <!-- Cover Page — apply via `::: {custom-style="Cover Page"} ... :::` in
       QMD to wrap free-form bold paragraphs (e.g. "DIRECT TESTIMONY OF /
       JUAN-PABLO VELEZ / CUB Exhibit 1.0 / April 30, 2026") so they
       inherit centered bold formatting and skip line numbering. -->
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="CoverPage">
    <w:name w:val="Cover Page"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="BodyText"/>
    <w:qFormat/>
    <w:pPr>
      <w:suppressLineNumbers/>
      <w:spacing w:before="0" w:after="240" w:line="276" w:lineRule="auto"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <!-- Heading 1 — high-level banner (rarely used in ICC testimony; kept
       for authors who want a doc-wide top heading). Same visual as
       Heading 2 since QMD ## → Pandoc Heading 2 is the workhorse. -->
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="Heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="BodyText"/>
    <w:link w:val="Heading1Char"/>
    <w:uiPriority w:val="9"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="480" w:after="240" w:line="480" w:lineRule="auto"/>
      <w:jc w:val="center"/>
      <w:outlineLvl w:val="0"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:bCs/>
      <w:caps/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
      <w:u w:val="single"/>
    </w:rPr>
  </w:style>
  <w:style w:type="character" w:customStyle="1" w:styleId="Heading1Char">
    <w:name w:val="Heading 1 Char"/>
    <w:basedOn w:val="DefaultParagraphFont"/>
    <w:link w:val="Heading1"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:caps/>
      <w:sz w:val="24"/>
      <w:u w:val="single"/>
    </w:rPr>
  </w:style>
  <!-- Heading 2 (`## X` in QMD) — primary section header.
       ICC convention: TNR 12pt bold ALL CAPS underlined, centered. -->
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="Heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="BodyText"/>
    <w:link w:val="Heading2Char"/>
    <w:uiPriority w:val="9"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="480" w:after="240" w:line="480" w:lineRule="auto"/>
      <w:jc w:val="center"/>
      <w:outlineLvl w:val="1"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:bCs/>
      <w:caps/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
      <w:u w:val="single"/>
    </w:rPr>
  </w:style>
  <w:style w:type="character" w:customStyle="1" w:styleId="Heading2Char">
    <w:name w:val="Heading 2 Char"/>
    <w:basedOn w:val="DefaultParagraphFont"/>
    <w:link w:val="Heading2"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:caps/>
      <w:sz w:val="24"/>
      <w:u w:val="single"/>
    </w:rPr>
  </w:style>
  <!-- Heading 3 (`### X` in QMD) — sub-section header, used in this
       codebase exclusively inside the appendix (Figures & Tables Index)
       to label each section's figure list (e.g. "SECTION IV — SCOPE
       AND ANALYTICAL APPROACH").
       ICC convention requires the appendix sub-headings to look the
       same as the body section headings, so we reuse the Heading 2
       visual: TNR 12pt bold ALL CAPS underlined, centered.  If a
       future QMD uses ### in the body and wants a different look,
       attach {custom-style="Heading 3 Plain"} on those headers and
       define that as a separate style. -->
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="Heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="BodyText"/>
    <w:link w:val="Heading3Char"/>
    <w:uiPriority w:val="9"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:keepLines/>
      <w:spacing w:before="480" w:after="240" w:line="480" w:lineRule="auto"/>
      <w:jc w:val="center"/>
      <w:outlineLvl w:val="2"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:bCs/>
      <w:caps/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
      <w:u w:val="single"/>
    </w:rPr>
  </w:style>
  <w:style w:type="character" w:customStyle="1" w:styleId="Heading3Char">
    <w:name w:val="Heading 3 Char"/>
    <w:basedOn w:val="DefaultParagraphFont"/>
    <w:link w:val="Heading3"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:caps/>
      <w:sz w:val="24"/>
      <w:u w:val="single"/>
    </w:rPr>
  </w:style>
  <!-- Heading 4 — preserved for completeness; ICC testimony rarely uses it. -->
  <w:style w:type="paragraph" w:styleId="Heading4">
    <w:name w:val="Heading 4"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="BodyText"/>
    <w:uiPriority w:val="9"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:spacing w:before="200" w:after="0" w:line="480" w:lineRule="auto"/>
      <w:outlineLvl w:val="3"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="BlockQuote">
    <w:name w:val="Block Quotation"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="BodyText"/>
    <w:qFormat/>
    <w:pPr>
      <w:suppressLineNumbers/>
      <w:spacing w:before="120" w:after="240" w:line="276" w:lineRule="auto"/>
      <w:ind w:left="720" w:right="720"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <!-- BlockText is what Pandoc applies to top-level `>` blockquotes
       (e.g. the `> STATE OF ILLINOIS` caption block). Render it
       centered, single-spaced, bold — and skip line numbers so it can
       function as a cover-page banner without polluting the body
       line-number stream. -->
  <w:style w:type="paragraph" w:styleId="BlockText">
    <w:name w:val="Block Text"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="BodyText"/>
    <w:qFormat/>
    <w:pPr>
      <w:suppressLineNumbers/>
      <w:spacing w:before="0" w:after="0" w:line="276" w:lineRule="auto"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ImageCaption">
    <w:name w:val="Image Caption"/>
    <w:basedOn w:val="Caption"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableCaption">
    <w:name w:val="Table Caption"/>
    <w:basedOn w:val="Caption"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="Caption"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="BodyText"/>
    <w:qFormat/>
    <w:pPr>
      <w:keepNext/>
      <w:spacing w:before="120" w:after="120" w:line="240" w:lineRule="auto"/>
      <w:jc w:val="center"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="22"/>
      <w:szCs w:val="22"/>
    </w:rPr>
  </w:style>
  <!-- Footnote text: TNR 11pt, single spaced, first-line indent like ICC
       briefs. <w:suppressLineNumbers/> keeps footnotes out of the body
       line-number counter (otherwise Word numbers them in their own
       independent stream that confuses the reader). -->
  <w:style w:type="paragraph" w:styleId="FootnoteText">
    <w:name w:val="footnote text"/>
    <w:basedOn w:val="Normal"/>
    <w:link w:val="FootnoteTextChar"/>
    <w:pPr>
      <w:suppressLineNumbers/>
      <w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>
      <w:ind w:firstLine="360"/>
      <w:jc w:val="both"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="22"/>
      <w:szCs w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="character" w:customStyle="1" w:styleId="FootnoteTextChar">
    <w:name w:val="Footnote Text Char"/>
    <w:basedOn w:val="DefaultParagraphFont"/>
    <w:link w:val="FootnoteText"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="character" w:styleId="FootnoteReference">
    <w:name w:val="footnote reference"/>
    <w:basedOn w:val="DefaultParagraphFont"/>
    <w:rPr>
      <w:vertAlign w:val="superscript"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Header">
    <w:name w:val="header"/>
    <w:basedOn w:val="Normal"/>
    <w:link w:val="HeaderChar"/>
    <w:pPr>
      <w:tabs>
        <w:tab w:val="center" w:pos="4680"/>
        <w:tab w:val="right" w:pos="9360"/>
      </w:tabs>
      <w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>
      <w:jc w:val="right"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="22"/>
    </w:rPr>
  </w:style>
  <w:style w:type="character" w:customStyle="1" w:styleId="HeaderChar">
    <w:name w:val="Header Char"/>
    <w:basedOn w:val="DefaultParagraphFont"/>
    <w:link w:val="Header"/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Footer">
    <w:name w:val="footer"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr>
      <w:tabs>
        <w:tab w:val="center" w:pos="4680"/>
        <w:tab w:val="right" w:pos="9360"/>
      </w:tabs>
      <w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>
    </w:pPr>
  </w:style>
  <w:style w:type="character" w:styleId="DefaultParagraphFont" w:default="1">
    <w:name w:val="Default Paragraph Font"/>
  </w:style>
  <w:style w:type="table" w:styleId="TableNormal" w:default="1">
    <w:name w:val="Table Normal"/>
    <w:tblPr>
      <w:tblInd w:w="0" w:type="dxa"/>
      <w:tblCellMar>
        <w:top w:w="0" w:type="dxa"/>
        <w:left w:w="108" w:type="dxa"/>
        <w:bottom w:w="0" w:type="dxa"/>
        <w:right w:w="108" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
  </w:style>
  <w:style w:type="numbering" w:default="1" w:styleId="NoList">
    <w:name w:val="No List"/>
  </w:style>
</w:styles>
"""


def _patch_document_xml(xml: str) -> str:
    """Replace the body's empty <w:sectPr/> with our custom one.

    Pandoc preserves whatever <w:sectPr> sits at the end of the body of
    the reference doc, so this is how we inject page size, margins,
    line numbering, and header reference into every rendered draft
    without per-doc XML hacks.

    Also injects the ``r:`` namespace on the root <w:document> if
    missing, so the header reference's r:id attribute resolves.
    """
    if "<w:sectPr />" in xml:
        xml = xml.replace("<w:sectPr />", SECTPR_XML, 1)
    elif "<w:sectPr/>" in xml:
        xml = xml.replace("<w:sectPr/>", SECTPR_XML, 1)
    else:
        xml = re.sub(
            r"<w:sectPr\b[^>]*>.*?</w:sectPr>|<w:sectPr\b[^/]*/>",
            SECTPR_XML,
            xml,
            count=1,
            flags=re.DOTALL,
        )

    # Pandoc's default reference doc declares only the w: namespace on
    # <w:document>. Our SECTPR_XML uses an r:id attribute, so we need
    # the relationships namespace too.
    if 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"' not in xml:
        xml = xml.replace(
            "<w:document ",
            '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ',
            1,
        )
    return xml


def _patch_document_rels(xml: str) -> str:
    """Add the two header relationships our section breaks reference.

    ``rIdTestimonyHeader`` → ``header1.xml`` (witness/exhibit/page on body
    + appendix), ``rIdTestimonyHeaderBlank`` → ``header2.xml`` (empty,
    used by the cover/TOC sections so those pages have no header text).
    """
    body_rel = (
        '<Relationship Id="rIdTestimonyHeader" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships/header" Target="header1.xml"/>'
    )
    blank_rel = (
        '<Relationship Id="rIdTestimonyHeaderBlank" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships/header" Target="header2.xml"/>'
    )
    inject = ""
    if body_rel not in xml:
        inject += body_rel
    if blank_rel not in xml:
        inject += blank_rel
    if not inject:
        return xml
    return xml.replace("</Relationships>", inject + "</Relationships>", 1)


def _patch_content_types(xml: str) -> str:
    """Register the header content types so Word recognises both headers."""
    inject = ""
    for part in ("header1.xml", "header2.xml"):
        override = (
            f'<Override PartName="/word/{part}" '
            'ContentType="application/vnd.openxmlformats-officedocument.'
            'wordprocessingml.header+xml"/>'
        )
        if override not in xml:
            inject += override
    if not inject:
        return xml
    return xml.replace("</Types>", inject + "</Types>", 1)


def _patch_settings_xml(xml: str) -> str:
    """Tell Word to update all fields on first open.

    Without this, the TOC field that Pandoc emits stays as an empty
    placeholder until the user manually presses F9 / right-clicks
    "Update Field". With it, Word offers to update the TOC the moment
    the doc is opened, so distributing a freshly-rendered ICC docx
    actually shows the table of contents.
    """
    if "<w:updateFields" in xml:
        return xml
    inject = '<w:updateFields w:val="true"/>'
    # Insert near the start of <w:settings> so it's picked up by Word.
    return re.sub(
        r"(<w:settings\b[^>]*>)",
        r"\1" + inject,
        xml,
        count=1,
    )


def _patch_numbering_xml(xml: str) -> str:
    """Widen ``<w:hanging>`` on every list level so multi-character
    markers don't overflow the marker box.

    Pandoc's reference docx sets ``<w:ind w:left="720" w:hanging="360"/>``
    for ordered lists. The 360-twip (0.25") marker box fits ``(i)``,
    ``(ii)``, and most arabic markers, but **(iii)**, **(iv)**, and any
    longer roman/parenthesised marker overflow it. Word's behaviour
    when the marker is wider than the hanging indent is implementation
    -defined: sometimes the text wraps to the next default tab stop
    (a "huge gap"), sometimes it butts right up against the marker
    (no space), and the inconsistency is jarring inside a single list.

    Setting ``<w:hanging>`` equal to ``<w:left>`` for each level makes
    the marker hang back to the left margin of that level — there's
    always at least 0.5" between the start of the marker and the start
    of the text, so the longest reasonable marker still fits cleanly.
    """

    def _widen(match: re.Match) -> str:
        left = int(match.group("left"))
        # Cap hanging at left so the marker doesn't hang past the page
        # margin; for level 0 (left=720) that means hanging=720, for
        # level 1 (left=1440) hanging=720 stays, etc.
        return f'<w:ind w:left="{left}" w:hanging="{min(left, 720)}"/>'

    return re.sub(
        r'<w:ind w:left="(?P<left>\d+)" w:hanging="\d+"\s*/>',
        _widen,
        xml,
    )


def build() -> Path:
    """Build expert_testimony.docx by patching Pandoc's default ref doc."""
    # 1) Get Pandoc's default reference docx so we inherit its
    #    document.xml, settings.xml, _rels/, etc.
    base = HERE / "_pandoc_default.docx"
    print(f"⚙️  Fetching Pandoc default reference doc → {base}")
    with base.open("wb") as fh:
        subprocess.run(
            ["pandoc", "--print-default-data-file", "reference.docx"],
            check=True,
            stdout=fh,
        )

    if OUTPUT.exists():
        OUTPUT.unlink()

    header_xml = HEADER_XML.replace("{{EXHIBIT}}", DEFAULT_EXHIBIT).replace("{{WITNESS_NAME}}", DEFAULT_WITNESS_NAME)

    # 2) Copy file by file, patching as we go.
    print(f"⚙️  Writing patched template → {OUTPUT}")
    saw_header1 = False
    saw_header2 = False
    with zipfile.ZipFile(base) as src, zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/styles.xml":
                dst.writestr(item, STYLES_XML)
            elif item.filename == "word/document.xml":
                dst.writestr(item, _patch_document_xml(data.decode("utf-8")))
            elif item.filename == "word/_rels/document.xml.rels":
                dst.writestr(item, _patch_document_rels(data.decode("utf-8")))
            elif item.filename == "[Content_Types].xml":
                dst.writestr(item, _patch_content_types(data.decode("utf-8")))
            elif item.filename == "word/settings.xml":
                dst.writestr(item, _patch_settings_xml(data.decode("utf-8")))
            elif item.filename == "word/numbering.xml":
                dst.writestr(item, _patch_numbering_xml(data.decode("utf-8")))
            elif item.filename == "word/header1.xml":
                # Pandoc default doesn't ship one, but be safe.
                dst.writestr(item, header_xml)
                saw_header1 = True
            elif item.filename == "word/header2.xml":
                dst.writestr(item, BLANK_HEADER_XML)
                saw_header2 = True
            else:
                dst.writestr(item, data)

        if not saw_header1:
            dst.writestr("word/header1.xml", header_xml)
        if not saw_header2:
            dst.writestr("word/header2.xml", BLANK_HEADER_XML)

    base.unlink()  # cleanup
    print(f"✅ Wrote {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")
    return OUTPUT


if __name__ == "__main__":
    try:
        build()
    except subprocess.CalledProcessError as exc:  # pragma: no cover - cli only
        print(f"💥 pandoc failed: {exc}", file=sys.stderr)
        sys.exit(1)
