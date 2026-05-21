--! Pandoc Lua filter for ICC expert-testimony formatting.
--!
--! Applied by ``lib.just.draft`` when rendering with ``--testimony``.
--!
--! Responsibilities:
--!   1. Suppress the Pandoc YAML title block at the top of the docx.
--!      ICC testimony has its own bespoke cover page (handled in the
--!      QMD body / reference template), so the YAML-derived
--!      Title/Subtitle/Author/Date paragraphs would just clutter it.
--!      We keep ``title-meta`` etc. populated so docx properties and
--!      the witness header still resolve, but we erase the rendering
--!      metadata.
--!
--!   2. Reformat ``**Q.** ...`` / ``**A.** ...`` paragraphs into the
--!      ICC Q&A look:
--!         - Strip the trailing period from the marker.
--!         - Apply the ``Question`` paragraph style to questions, and
--!           the ``Answer`` paragraph style to answers (both defined
--!           in the reference template's ``styles.xml``); these
--!           styles set a hanging indent so the marker sits in the
--!           left gutter and the text wraps under the first word.
--!         - Uppercase + bold question text (ICC convention).  Footnote
--!           references, math, and emphasis inside the question survive
--!           the transform because we walk inlines tree-aware.
--!
--!   3. Insert a body-section break with a fresh line-number counter
--!      after the cover/TOC pages.  The cover pages live in section 1
--!      with line-numbering suppressed (via paragraph styles), and the
--!      body lives in section 2 where ``lnNumType`` restarts at 1.
--!      We mark the boundary with ``<!-- testimony-body-start -->`` in
--!      the QMD; the filter expands that comment-paragraph into a
--!      raw OOXML block carrying its own ``<w:sectPr>``.
--!
--!   4. Strip Quarto ``column-*`` div wrappers (HTML-only column
--!      classes such as ``::: {.column-page-inset-right}``).  In DOCX
--!      these classes have no meaning, and they break Pandoc's
--!      figure/crossref parsing whenever the QMD is missing the blank
--!      line above the opening fence — the literal ``:::`` markers
--!      survive into the docx and the image inside is never promoted
--!      to a Figure (so no caption, no working ``@fig-…`` reference).
--!
--!   5. Rewrite Quarto figure labels from ``Figure N`` to
--!      ``Figure JPV-N`` (author-initial scheme used in ICC
--!      testimony).  Quarto's crossref filter runs before this one and
--!      resolves ``@fig-foo`` references plus ``Figure: caption…``
--!      labels into ``[Str "Figure", Space, Str "1"]`` inline runs;
--!      we walk every Inlines list and substitute ``JPV-N`` for the
--!      bare number whenever it follows ``Figure``.
--!
--!   6. Use a blank header (``rIdTestimonyHeaderBlank``) on the cover
--!      section so page 1 doesn't show the witness running header.
--!      The TOC + body + appendix continue to use the witness header.
--!
--! Stage: Pandoc reads metadata first (Meta), then walks the document
--! body (Pandoc / Para).  We use Meta() to drop the title block, Para()
--! to rewrite Q&A paragraphs, Div() to strip column wrappers, Inlines()
--! to rewrite figure labels, and Pandoc() to expand the body-start
--! marker.

local function inlines_text(inlines)
  local buf = {}
  for _, el in ipairs(inlines) do
    if el.t == "Str" then
      table.insert(buf, el.text)
    elseif el.t == "Space" or el.t == "SoftBreak" or el.t == "LineBreak" then
      table.insert(buf, " ")
    elseif el.t == "Strong" or el.t == "Emph" or el.t == "Underline"
           or el.t == "SmallCaps" or el.t == "Span" or el.t == "Quoted"
           or el.t == "Link" then
      table.insert(buf, inlines_text(el.content))
    end
  end
  return table.concat(buf)
end

--! Detect a Q/A marker at the start of a paragraph.  We look for the
--! pattern ``Strong [Str "Q." or "Q"]`` (optionally followed by Space)
--! and report which marker matched plus the *remaining* inlines (with
--! the leading marker run + adjacent space stripped).
local function strip_qa_marker(inlines)
  if #inlines == 0 then return nil end

  local first = inlines[1]
  if first.t ~= "Strong" then return nil end

  local marker_text = inlines_text(first.content)
  marker_text = marker_text:gsub("^%s+", ""):gsub("%s+$", "")
  local marker
  if marker_text == "Q." or marker_text == "Q" then
    marker = "Q"
  elseif marker_text == "A." or marker_text == "A" then
    marker = "A"
  else
    return nil
  end

  local rest = {}
  local skipped_space = false
  for i = 2, #inlines do
    local el = inlines[i]
    if not skipped_space and (el.t == "Space" or el.t == "SoftBreak") then
      skipped_space = true
    else
      table.insert(rest, el)
    end
  end
  return marker, rest
end

--! Walk inlines and uppercase every Str token in place (used so
--! questions render in ALL CAPS while preserving footnote references,
--! inline math, links, and emphasis that mustn't be touched).
local function inlines_uppercase(inlines)
  local out = {}
  for _, el in ipairs(inlines) do
    if el.t == "Str" then
      table.insert(out, pandoc.Str(el.text:upper()))
    elseif el.t == "Strong" or el.t == "Emph" or el.t == "Underline"
           or el.t == "SmallCaps" or el.t == "Quoted" then
      el.content = inlines_uppercase(el.content)
      table.insert(out, el)
    elseif el.t == "Link" or el.t == "Span" then
      el.content = inlines_uppercase(el.content)
      table.insert(out, el)
    else
      table.insert(out, el)
    end
  end
  return out
end

--! Build a paragraph styled as a Q-row or A-row.  The marker stays
--! bold and is followed by a tab so Word lines up the question text
--! at the hanging-indent position defined by the Question/Answer
--! styles in the reference template.
local function qa_paragraph(marker, content_inlines)
  local style = (marker == "Q") and "Question" or "Answer"
  local marker_run = pandoc.Strong({ pandoc.Str(marker) })
  local body_inlines
  if marker == "Q" then
    body_inlines = { pandoc.Strong(inlines_uppercase(content_inlines)) }
  else
    body_inlines = content_inlines
  end

  -- Use a tab character so the hanging indent + tab stop in the
  -- Question/Answer styles produce a clean alignment column.
  local combined = { marker_run, pandoc.Str("\t") }
  for _, el in ipairs(body_inlines) do
    table.insert(combined, el)
  end

  local div = pandoc.Div(
    { pandoc.Para(combined) },
    pandoc.Attr("", { "qa", "qa-" .. marker:lower() }, { ["custom-style"] = style })
  )
  return div
end

function Meta(meta)
  if meta.title and not meta["title-meta"] then
    meta["title-meta"] = meta.title
  end
  if meta.author and not meta["author-meta"] then
    meta["author-meta"] = meta.author
  end
  if meta.date and not meta["date-meta"] then
    meta["date-meta"] = meta.date
  end
  meta.title = nil
  meta.subtitle = nil
  meta.author = nil
  meta.date = nil
  return meta
end

function Para(p)
  local stripped_marker, rest = strip_qa_marker(p.content)
  if stripped_marker and #rest > 0 then
    return qa_paragraph(stripped_marker, rest)
  end
  return nil
end

--! Strip Quarto ``column-*`` div wrappers (e.g. ``column-page-inset-right``,
--! ``column-margin``).  These layout classes are HTML-only and have no
--! analogue in DOCX.  Worse, when the QMD doesn't have a blank line
--! above the opening fence (``::: {.column-…}``) Pandoc treats the
--! literal ``:::`` markers as plain text — so the docx ends up with
--! stray ``::: {.column-page-inset-right}`` runs and, more painfully,
--! the wrapped image is never promoted to a Figure (no caption, no
--! working crossref).  Unwrapping the Div side-steps both problems
--! and means authors don't have to remember the blank-line discipline
--! the Pandoc fence parser enforces.
--!
--! We don't unwrap divs that carry an explicit ``custom-style`` (e.g.
--! ``::: {custom-style="Cover Page"}``) — those carry styling intent
--! and must reach the docx writer intact.
function Div(d)
  local has_custom_style = false
  if d.attr.attributes then
    for k, _ in pairs(d.attr.attributes) do
      if k == "custom-style" then has_custom_style = true end
    end
  end
  if has_custom_style then return nil end
  for _, c in ipairs(d.attr.classes) do
    if c:match("^column%-") then
      return d.content
    end
  end
  return nil
end

--! Rewrite figure labels from ``Figure N`` to ``Figure JPV-N``.
--!
--! Quarto's crossref filter (built into Quarto, runs before this one)
--! resolves ``@fig-foo`` cross-references and figure-caption prefixes
--! into the inline run [Str "Figure", Str "\xc2\xa0", Str "<arabic>"].
--! NOTE: Quarto uses a literal ``Str`` with a non-breaking space
--! (U+00A0, UTF-8 ``\xc2\xa0``) between "Figure" and the number — so
--! the rendered docx keeps them on the same line.  This is *not* a
--! Pandoc ``Space`` token and is *not* a regular ASCII space, so we
--! match all three forms (Pandoc Space, Str " ", Str NBSP) for safety.
--!
--! Walking every Inlines list lets us rewrite cross-references *and*
--! the auto-injected caption prefix without having to special-case
--! Link, Caption, Figure, Span, etc.
--!
--! We deliberately leave non-arabic numbers alone: appendix bullet
--! labels written as literal ``Figure JPV-1`` text contain
--! Str("JPV-1") which never matches the ``^%d+$`` guard, so they're
--! pass-through.  Likewise existing ``Figure IV-1`` style labels in
--! the original prose stay untouched.
-- Match Pandoc Space, ASCII " ", and UTF-8 non-breaking space ("\xc2\xa0").
-- Lua's %s pattern doesn't include NBSP so we test it explicitly.
local _NBSP = "\194\160"  -- U+00A0 in UTF-8 (decimal bytes 194, 160)
local function _is_separator(el)
  if el.t == "Space" then return true end
  if el.t ~= "Str" then return false end
  return el.text == " " or el.text == _NBSP
end

function Inlines(inlines)
  local out = {}
  local i = 1
  while i <= #inlines do
    local el = inlines[i]
    if i + 2 <= #inlines
       and el.t == "Str" and el.text == "Figure"
       and _is_separator(inlines[i + 1])
       and inlines[i + 2].t == "Str"
       and inlines[i + 2].text:match("^%d+$") then
      table.insert(out, pandoc.Str("Figure"))
      table.insert(out, inlines[i + 1])  -- preserve Space vs Str " "
      table.insert(out, pandoc.Str("JPV-" .. inlines[i + 2].text))
      i = i + 3
    else
      table.insert(out, el)
      i = i + 1
    end
  end
  return out
end

--! Body-section break: when the QMD contains the comment-marker
--! ``<!-- testimony-body-start -->`` we replace the corresponding
--! paragraph with a raw OOXML paragraph carrying its own <w:sectPr>.
--!
--! The OOXML semantics matter here: a <w:sectPr> inside a paragraph's
--! pPr describes the section that *ends* at that paragraph.  So this
--! sectPr governs section 1 (the cover/TOC pages above it), not the
--! body that follows.
--!
--! Section 1 (cover) properties:
--!   * <w:type w:val="nextPage"/> — the next section (body) starts on
--!     a new page, replacing the explicit {{< pagebreak >}} we used
--!     to need.
--!   * lnNumType is intentionally omitted — section 1 has no line
--!     numbering at all.  This kills the residual "1", "2" line-number
--!     stragglers Pandoc-inserted blank paragraphs would otherwise
--!     produce around the empty TOC field.
--!
--! Section 2 (body) properties live in word/document.xml's final
--! sectPr (built by build_expert_testimony.py) and that's where
--! lnNumType restart=newSection lives.
local body_section_break_xml = [[
<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:pPr>
    <w:suppressLineNumbers/>
    <w:sectPr>
      <w:headerReference w:type="default" r:id="rIdTestimonyHeader"/>
      <w:type w:val="nextPage"/>
      <w:pgSz w:w="12240" w:h="15840" w:code="1"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1728" w:header="720" w:footer="576" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:pPr>
</w:p>
]]

local BODY_MARKER_PATTERN = "{{<%s*testimony%-body%-start%s*>}}"

--! Pandoc's HTML comments survive as RawBlock("html", "<!-- ... -->").
--! Quarto shortcodes survive as Para containing a Str of the raw text
--! when there's no shortcode handler for them.  Match either form.
local function is_body_marker(blk)
  if blk.t == "RawBlock" and (blk.format == "html" or blk.format == "markdown") then
    local text = blk.text or ""
    return text:find("testimony%-body%-start") ~= nil
  end
  if blk.t == "Para" or blk.t == "Plain" then
    local txt = inlines_text(blk.content):gsub("^%s+", ""):gsub("%s+$", "")
    if txt == "<!-- testimony-body-start -->" then return true end
    if txt:match(BODY_MARKER_PATTERN) then return true end
  end
  return false
end

--! Static Table of Contents.
--!
--! Pandoc's --toc emits a TOC *field* that only populates once the
--! reader opens the doc in Word and accepts the "update fields"
--! prompt.  PDF previews and headless conversions show it as blank.
--!
--! Instead, we set ``toc: false`` in the QMD and place an explicit
--! ``<!-- testimony-toc -->`` marker.  The filter below walks the
--! document's Header tree and replaces the marker with a static
--! sequence of paragraphs styled ``TOC 1`` / ``TOC 2`` (which the
--! reference template's styles.xml maps to indented, non-line-numbered
--! TOC styles).
--!
--! We don't compute page numbers (impossible without running the docx
--! through a renderer); the reader gets an indented section list, and
--! the Word ``UPDATE FIELDS`` shortcut is no longer required.
local TOC_MARKER_PATTERN = "{{<%s*testimony%-toc%s*>}}"

local function is_toc_marker(blk)
  if blk.t == "RawBlock" and (blk.format == "html" or blk.format == "markdown") then
    local text = blk.text or ""
    return text:find("testimony%-toc%-here") ~= nil
       or text:find("testimony%-toc[^-]") ~= nil
  end
  if blk.t == "Para" or blk.t == "Plain" then
    local txt = inlines_text(blk.content):gsub("^%s+", ""):gsub("%s+$", "")
    if txt == "<!-- testimony-toc -->" or txt == "<!-- testimony-toc-here -->" then
      return true
    end
    if txt:match(TOC_MARKER_PATTERN) then return true end
  end
  return false
end

local function header_to_inlines(h)
  -- Strip the {custom-style="..."} attribute we added to appendix
  -- subsection headings; everything else (text, footnote refs, links)
  -- carries through.
  local copy = {}
  for _, el in ipairs(h.content) do
    table.insert(copy, el)
  end
  return copy
end

local function toc_para(level, inlines)
  -- Heading 2 → TOC 1; Heading 3 → TOC 2; Heading 4 → TOC 3.
  -- (We never go deeper in this codebase.)
  local style_name = "TOC " .. tostring(level - 1)
  return pandoc.Div(
    { pandoc.Para(inlines) },
    pandoc.Attr("", { "toc-entry" }, { ["custom-style"] = style_name })
  )
end

local function build_static_toc(blocks)
  -- Walk the body and collect all Header nodes at level 2 or 3.
  -- Skip the bibliography / refs block (Quarto auto-inserts a Heading
  -- for "References" we don't want to advertise in the TOC).
  local entries = {}
  for _, blk in ipairs(blocks) do
    if blk.t == "Header" and blk.level >= 2 and blk.level <= 3 then
      -- Skip headings that explicitly opt out via .unnumbered or that
      -- sit inside the appendix sub-listing (we still want the
      -- "## XI. APPENDIX" entry but the ### entries inside its body
      -- are already a flat list — keep them so the reader sees the
      -- appendix structure).
      local classes = blk.attr.classes or {}
      local skip = false
      for _, c in ipairs(classes) do
        if c == "unnumbered" then skip = true end
      end
      if not skip then
        table.insert(entries, toc_para(blk.level, header_to_inlines(blk)))
      end
    end
  end

  -- Heading row: "Table of Contents".  Use the ``TOC Heading`` style
  -- defined in the testimony template — it inherits the Heading 1
  -- visual (centered/bold/all-caps/underlined) and adds
  -- ``<w:suppressLineNumbers/>`` so the row doesn't pick up a stray
  -- gutter number.
  local title = pandoc.Div(
    {
      pandoc.Para({ pandoc.Str("Table of Contents") }),
    },
    pandoc.Attr("", {}, { ["custom-style"] = "TOC Heading" })
  )
  table.insert(entries, 1, title)
  return entries
end

--! Section break that pushes the TOC onto its own page.  This sectPr
--! describes section 1 (the cover) — its end is here, on the marker
--! paragraph.  The cover gets the *blank* header (rIdTestimonyHeaderBlank)
--! so page 1 doesn't show the witness running header; line numbering is
--! also omitted (the cover lives in section 1 where we don't number).
local toc_section_break_xml = [[
<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:pPr>
    <w:suppressLineNumbers/>
    <w:sectPr>
      <w:headerReference w:type="default" r:id="rIdTestimonyHeaderBlank"/>
      <w:type w:val="nextPage"/>
      <w:pgSz w:w="12240" w:h="15840" w:code="1"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1728" w:header="720" w:footer="576" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:pPr>
</w:p>
]]

--! Continuous section break used between major body sections to make
--! line numbering restart at 1.  ICC house style numbers each major
--! ``## SECTION`` independently (1..N within section II, fresh 1..N
--! within section III, …) rather than running 1..1220 through the
--! whole brief.
--!
--! ``<w:type w:val="continuous"/>`` keeps the new section on the same
--! page (no forced page break — that would push every Roman section
--! to its own page, which we *don't* want).  ``lnNumType
--! restart="newSection"`` tells Word to reset the counter at the start
--! of the section that ends at this paragraph.  ``<w:suppressLineNumbers/>``
--! on the marker paragraph keeps the marker itself out of the count.
local section_restart_break_xml = [[
<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:pPr>
    <w:suppressLineNumbers/>
    <w:sectPr>
      <w:headerReference w:type="default" r:id="rIdTestimonyHeader"/>
      <w:type w:val="continuous"/>
      <w:pgSz w:w="12240" w:h="15840" w:code="1"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1728" w:header="720" w:footer="576" w:gutter="0"/>
      <w:lnNumType w:countBy="1" w:restart="newSection" w:distance="240"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:pPr>
</w:p>
]]

--! Detect whether a Div produced by the Para() filter is a Q or an A.
--! Returns "Q", "A", or nil.
local function qa_div_marker(blk)
  if blk.t ~= "Div" or not blk.attr or not blk.attr.classes then return nil end
  for _, c in ipairs(blk.attr.classes) do
    if c == "qa-q" then return "Q" end
    if c == "qa-a" then return "A" end
  end
  return nil
end

--! Boundaries that reset the "we're inside a Q/A answer" state when
--! walking continuation paragraphs.  Anything that's not natural
--! flowing prose (headers, page breaks, our injected ``<br>``
--! separators, raw blocks, horizontal rules) ends the current answer.
local function is_continuation_boundary(blk)
  if blk.t == "Header" then return true end
  if blk.t == "HorizontalRule" then return true end
  if blk.t == "RawBlock" then
    local txt = blk.text or ""
    -- The QMD uses "<br>" between Q&A turns and includes our own
    -- "testimony-…" markers; treat both as boundaries so a continuation
    -- doesn't bleed across a turn change.
    if txt:match("<br") or txt:match("testimony%-") then return true end
    -- Foreign raw blocks (e.g. our injected sectPr paragraphs) also reset.
    return true
  end
  return false
end

--! Wrap a follow-up paragraph in a Div that picks up the
--! ``Question Continuation`` / ``Answer Continuation`` paragraph style
--! from styles.xml (defined in build_expert_testimony.py).  The style
--! holds the answer-column indent (left=720) plus a 0.25" first-line
--! indent so each wrapped paragraph lines up with the question/answer
--! text and reads as a clear new paragraph.
local function wrap_continuation(para, marker)
  local style = (marker == "Q") and "Question Continuation" or "Answer Continuation"
  local class_marker = "qa-cont-" .. marker:lower()
  return pandoc.Div(
    { para },
    pandoc.Attr("", { "qa-cont", class_marker }, { ["custom-style"] = style })
  )
end

--! Walk top-level blocks and apply continuation styling to follow-up
--! paragraphs that belong to a multi-paragraph Q or A.  We only style
--! plain ``Para`` blocks — lists, blockquotes, figures, code blocks
--! etc. inside an answer keep their default formatting (these don't
--! suffer from the indent-collapse bug; only the prose paragraphs do).
local function apply_continuation_styles(blocks)
  local out = {}
  local in_qa = nil  -- "Q" or "A" or nil
  for _, blk in ipairs(blocks) do
    local marker = qa_div_marker(blk)
    if marker then
      in_qa = marker
      table.insert(out, blk)
    elseif is_continuation_boundary(blk) then
      in_qa = nil
      table.insert(out, blk)
    elseif in_qa and blk.t == "Para" then
      table.insert(out, wrap_continuation(blk, in_qa))
    else
      -- BulletList / OrderedList / BlockQuote / Figure / Plain etc.
      -- Leave the block alone but stay "inside the answer" so any
      -- *further* prose paragraphs continue to be styled.
      table.insert(out, blk)
    end
  end
  return out
end

--! Detect a ``## ...`` (Heading level 2) that starts a major body
--! section and *not* the appendix's sub-section listings.  The
--! filter only counts the body Heading 2s; appendix sub-sections live
--! inside the ``## XI. APPENDIX`` section and don't need their own
--! line-number restart.
local function is_body_h2(blk)
  if blk.t ~= "Header" or blk.level ~= 2 then return false end
  local classes = blk.attr.classes or {}
  for _, c in ipairs(classes) do
    if c == "unnumbered" then return false end
  end
  return true
end

function Pandoc(doc)
  local toc_entries = build_static_toc(doc.blocks)

  -- First pass: expand cover/TOC/body markers and inject line-number
  -- restart breaks before each major Heading 2 in the body.  ``in_body``
  -- tracks whether we've passed the testimony-body-start marker;
  -- ``seen_first_body_h2`` makes us skip the *first* Heading 2 (which
  -- already has a fresh line counter from the body-start sectPr) and
  -- start injecting only on the second one onward.
  local out = {}
  local in_body = false
  local seen_first_body_h2 = false
  for _, blk in ipairs(doc.blocks) do
    if is_body_marker(blk) then
      table.insert(out, pandoc.RawBlock("openxml", body_section_break_xml))
      in_body = true
    elseif is_toc_marker(blk) then
      -- Push the TOC onto its own page (page 2 in the Walters
      -- exemplar): emit a section break, then the TOC heading and
      -- entries.  The follow-on body-start marker emits a second
      -- section break to push the body onto page 3+.
      table.insert(out, pandoc.RawBlock("openxml", toc_section_break_xml))
      for _, e in ipairs(toc_entries) do
        table.insert(out, e)
      end
    elseif in_body and is_body_h2(blk) then
      if seen_first_body_h2 then
        table.insert(out, pandoc.RawBlock("openxml", section_restart_break_xml))
      end
      seen_first_body_h2 = true
      table.insert(out, blk)
    else
      table.insert(out, blk)
    end
  end

  -- Second pass: wrap follow-up paragraphs of multi-paragraph Q&As in
  -- ``Question/Answer Continuation`` Divs so they keep the answer-
  -- column indent.
  out = apply_continuation_styles(out)

  doc.blocks = out
  return doc
end
