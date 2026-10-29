--! Pandoc Lua filter for expert-testimony Word output.
--!
--! Applied by ``lib.just.draft`` when rendering with ``--testimony``
--! (``just testimony``).  There is one testimony format for every docket
--! (see ``build_expert_testimony.py`` for the measurements); the only
--! things that change per filing are the ``testimony:`` fields in the
--! QMD frontmatter, which this filter turns into the cover page.
--!
--! Responsibilities:
--!   1. Drop the Pandoc YAML title block (the cover replaces it).
--!   2. Generate the cover page from ``testimony:`` metadata: "BEFORE THE
--!      <COMMISSION>", the docket caption (applicant lines, a column of
--!      ``)`` marks, the case number at right), the testimony title block
--!      and the filing date.  The cover is its own Word section with no
--!      header, page number or line numbers; the body section that follows
--!      restarts page numbering at 1.
--!   3. Format ``**Q.**`` / ``**A.**`` paragraphs: marker at the margin, a
--!      tab, text at 0.5".  Follow-on paragraphs of the same Q or A sit at
--!      0.5" with no first-line indent (styles live in the reference doc).
--!   4. Format headings.  The shallowest heading level in the document
--!      becomes the top level ("I. Introduction": bold, numeral right-
--!      aligned in its own column, only the *words* underlined).  Deeper
--!      levels are italic ("A. ...", "1) ...").  Numerals are typed in the
--!      QMD and kept as typed (so cross-references like "Section X.B.1"
--!      stay valid); the filter only re-lays them out.
--!   5. Strip Quarto ``column-*`` div wrappers (HTML-only layout classes
--!      that otherwise leave literal ``:::`` text and break figure parsing).
--!   6. Keep table cells single-spaced (bullets need double-spaced "Compact").
--!   7. Drop legacy ``<!-- testimony-body-start -->`` / ``testimony-toc``
--!      markers from older QMDs.

local text = pandoc.text

local function inlines_text(inlines)
  return pandoc.utils.stringify(pandoc.Inlines(inlines))
end

-- A tab as a raw Word run: robust regardless of how the writer treats "\t".
local function tab()
  return pandoc.RawInline("openxml", "<w:r><w:tab/></w:r>")
end

local function xml_escape(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

--! ---------------------------------------------------------------------
--! Q / A paragraphs
--! ---------------------------------------------------------------------

--! Detect a Q/A marker at the start of a paragraph: Strong [Str "Q." or "Q"]
--! optionally followed by a space.  Returns the marker ("Q"/"A") and the
--! remaining inlines, or nil.
local function strip_qa_marker(inlines)
  if #inlines == 0 then return nil end
  local first = inlines[1]
  if first.t ~= "Strong" then return nil end

  local marker_text = inlines_text(first.content):gsub("^%s+", ""):gsub("%s+$", "")
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

--! Build a paragraph styled as a Q-row or A-row: bold marker, a tab, then
--! the text.  Questions are bold via the ``Question`` style.
local function qa_paragraph(marker, content_inlines)
  local style = (marker == "Q") and "Question" or "Answer"
  local combined = { pandoc.Strong({ pandoc.Str(marker .. ".") }), tab() }
  for _, el in ipairs(content_inlines) do
    table.insert(combined, el)
  end
  return pandoc.Div(
    { pandoc.Para(combined) },
    pandoc.Attr("", { "qa", "qa-" .. marker:lower() }, { ["custom-style"] = style })
  )
end

function Meta(meta)
  if meta.title and not meta["title-meta"] then meta["title-meta"] = meta.title end
  if meta.author and not meta["author-meta"] then meta["author-meta"] = meta.author end
  if meta.date and not meta["date-meta"] then meta["date-meta"] = meta.date end
  meta.title = nil
  meta.subtitle = nil
  meta.author = nil
  meta.date = nil
  return meta
end

function Para(p)
  local marker, rest = strip_qa_marker(p.content)
  if marker and #rest > 0 then
    return qa_paragraph(marker, rest)
  end
  return nil
end

--! Strip Quarto ``column-*`` div wrappers; keep Divs that carry an explicit
--! ``custom-style`` (they carry styling intent).
function Div(d)
  if d.attr.attributes and d.attr.attributes["custom-style"] then return nil end
  for _, c in ipairs(d.attr.classes) do
    if c:match("^column%-") then return d.content end
  end
  return nil
end

--! Table cells: single-spaced "Table Text" instead of the double-spaced
--! "Compact" style Pandoc would pick (the example's bullets use Compact).
--! Pandoc's docx writer hard-codes the "Compact" style for ``Plain`` blocks
--! in table cells, ignoring a wrapping custom-style; a ``Para`` honors it.
local function to_table_text(blk)
  return pandoc.Div({ pandoc.Para(blk.content) }, pandoc.Attr("", {}, { ["custom-style"] = "Table Text" }))
end

function Table(tbl)
  -- Walk the whole table, then put the caption back untouched (its Plain
  -- block must keep the caption style).
  local caption = tbl.caption
  local walked = tbl:walk({ Plain = to_table_text, Para = to_table_text })
  walked.caption = caption
  return walked
end

--! ---------------------------------------------------------------------
--! Continuation paragraphs
--! ---------------------------------------------------------------------

local function qa_div_marker(blk)
  if blk.t ~= "Div" or not blk.attr or not blk.attr.classes then return nil end
  for _, c in ipairs(blk.attr.classes) do
    if c == "qa-q" then return "Q" end
    if c == "qa-a" then return "A" end
  end
  return nil
end

--! Anything that is not flowing prose ends the current answer: headings,
--! rules and raw blocks (the QMD's ``<br>`` separators, section breaks).
local function is_continuation_boundary(blk)
  return blk.t == "Header" or blk.t == "HorizontalRule" or blk.t == "RawBlock"
end

--! A line holding only ``<br>`` (the QMD's visual separator between Q&A
--! turns) parses as a paragraph of raw inlines.  Word would render it as an
--! empty double-spaced line, breaking the uniform 9 pt gap, so drop it.
local function is_br_only(blk)
  if blk.t ~= "Para" and blk.t ~= "Plain" then return false end
  local saw_br = false
  for _, el in ipairs(blk.content) do
    if el.t == "RawInline" and el.format:match("html") and el.text:match("^<br%s*/?>$") then
      saw_br = true
    elseif el.t ~= "Space" and el.t ~= "SoftBreak" and el.t ~= "LineBreak" then
      return false
    end
  end
  return saw_br
end

local function wrap_continuation(para, marker)
  local style = (marker == "Q") and "Question Continuation" or "Answer Continuation"
  return pandoc.Div(
    { para },
    pandoc.Attr("", { "qa-cont", "qa-cont-" .. marker:lower() }, { ["custom-style"] = style })
  )
end

--! Follow-up paragraphs of a multi-paragraph Q or A keep the 0.5" column.
--! Lists, block quotes, figures etc. inside an answer keep their own style.
local function apply_continuation_styles(blocks)
  local out = {}
  local in_qa = nil
  for _, blk in ipairs(blocks) do
    local marker = qa_div_marker(blk)
    if is_br_only(blk) then
      in_qa = nil -- separator: drop it, and end the current answer
    elseif marker then
      in_qa = marker
      table.insert(out, blk)
    elseif is_continuation_boundary(blk) then
      in_qa = nil
      table.insert(out, blk)
    elseif in_qa and blk.t == "Para" then
      table.insert(out, wrap_continuation(blk, in_qa))
    else
      table.insert(out, blk)
    end
  end
  return out
end

--! ---------------------------------------------------------------------
--! Headings
--! ---------------------------------------------------------------------

--! Lua patterns for a typed label at each relative level.
local LABEL_PATTERNS = {
  [1] = "^[IVXLCDM]+%.$", -- I.  II.  III.
  [2] = "^%a%.$",         -- A.  B.
  [3] = "^%d+[%.%)]$",    -- 1)  2.
}

local function format_heading(h, level)
  h.level = level
  local content = h.content
  local label, rest
  local pattern = LABEL_PATTERNS[level]
  if pattern and #content >= 2 and content[1].t == "Str" and content[1].text:match(pattern)
     and content[2].t == "Space" then
    label = content[1].text
    rest = {}
    for i = 3, #content do table.insert(rest, content[i]) end
  else
    rest = {}
    for i = 1, #content do table.insert(rest, content[i]) end
  end

  local new = {}
  if level == 1 then
    -- "\tI.\tIntroduction": the first tab right-aligns the numeral against
    -- the 0.25" right tab stop, the second tab jumps to the 0.5" text column.
    if label then
      table.insert(new, tab())
      table.insert(new, pandoc.Str(label))
      table.insert(new, tab())
    end
    if #rest > 0 then table.insert(new, pandoc.Underline(rest)) end
  else
    if label then
      table.insert(new, pandoc.Str(label))
      table.insert(new, tab())
    end
    for _, el in ipairs(rest) do table.insert(new, el) end
  end
  h.content = new
  return h
end

--! Shift heading levels so the shallowest heading is level 1, then format.
--! (Testimony QMDs use ``##`` for sections because the title lives in YAML.)
local function format_headings(doc)
  local min_level = 99
  doc:walk({ Header = function(h) if h.level < min_level then min_level = h.level end end })
  if min_level == 99 then return doc end
  return doc:walk({
    Header = function(h)
      local level = h.level - min_level + 1
      if level > 4 then level = 4 end
      return format_heading(h, level)
    end,
  })
end

--! ---------------------------------------------------------------------
--! Cover page
--! ---------------------------------------------------------------------

--! Read one string field from a metadata map (YAML booleans arrive as Lua
--! booleans, everything else is stringified).
local function field(tm, key)
  local v = tm[key]
  if v == nil then return nil end
  local s
  if type(v) == "boolean" then
    s = tostring(v)
  else
    s = pandoc.utils.stringify(v)
  end
  -- Pandoc's markdown reader turns "No. 9888" into "No.<nbsp>9888"; use a
  -- plain space so the cover text matches the running header exactly.
  s = s:gsub("\194\160", " ")
  if s == "" then return nil end
  return s
end

local function cover_para(style, content, extra_ppr)
  local run = ""
  if content and content ~= "" then
    run = '<w:r><w:t xml:space="preserve">' .. xml_escape(content) .. "</w:t></w:r>"
  end
  return '<w:p><w:pPr><w:pStyle w:val="' .. style .. '"/>' .. (extra_ppr or "") .. "</w:pPr>" .. run .. "</w:p>"
end

local function cover_cell(width, content)
  return '<w:tc><w:tcPr><w:tcW w:w="' .. width .. '" w:type="dxa"/></w:tcPr>'
    .. cover_para("CoverCaption", content) .. "</w:tc>"
end

--! The docket caption: one row per caption line, ``)`` in the middle column,
--! and the case number in the right column of the last row.
local function caption_table(lines, case_number)
  local rows = {}
  for i, line in ipairs(lines) do
    local right = (i == #lines) and case_number or ""
    table.insert(rows,
      "<w:tr>" .. cover_cell(5760, line) .. cover_cell(360, ")") .. cover_cell(3240, right) .. "</w:tr>")
  end
  return '<w:tbl><w:tblPr><w:tblW w:w="9360" w:type="dxa"/><w:tblInd w:w="0" w:type="dxa"/>'
    .. '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="0" w:type="dxa"/>'
    .. '<w:right w:w="0" w:type="dxa"/></w:tblCellMar></w:tblPr>'
    .. '<w:tblGrid><w:gridCol w:w="5760"/><w:gridCol w:w="360"/><w:gridCol w:w="3240"/></w:tblGrid>'
    .. table.concat(rows) .. "</w:tbl>"
end

local RULE_PPR = '<w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="auto"/></w:pBdr>'

--! Section break ending the cover section (no header text, no page number,
--! no line numbers).  The body section's properties live at the end of the
--! reference doc's document.xml.
local COVER_SECTION_BREAK = [[
<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:pPr>
    <w:suppressLineNumbers/>
    <w:sectPr>
      <w:headerReference w:type="default" r:id="rIdTestimonyHeaderBlank"/>
      <w:footerReference w:type="default" r:id="rIdTestimonyFooterBlank"/>
      <w:type w:val="nextPage"/>
      <w:pgSz w:w="12240" w:h="15840" w:code="1"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="360" w:footer="1000" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:pPr>
</w:p>
]]

local function build_cover(meta)
  -- Metadata maps are plain Lua tables in this Pandoc version (no ``.t`` tag).
  local tm = meta.testimony
  if type(tm) ~= "table" then return nil end

  local commission = field(tm, "commission") or ""
  local case_number = field(tm, "case_number") or ""
  local kind = field(tm, "type") or ""
  local witness = field(tm, "witness") or ""
  local witness_title = field(tm, "witness_title")
  local on_behalf_of = field(tm, "on_behalf_of") or ""
  local version_label = field(tm, "version_label")
  -- ``lib.just.draft`` supplies a long-form date ("September 22, 2026");
  -- fall back to the raw value for anyone running the filter directly.
  local date = field(meta, "testimony-date-long") or field(tm, "date") or ""

  local caption = {}
  if tm.caption and pandoc.utils.type(tm.caption) == "List" then
    for _, item in ipairs(tm.caption) do
      table.insert(caption, pandoc.utils.stringify(item))
    end
  end

  local flag = (field(tm, "and_exhibits") or "false"):lower()
  local and_exhibits = (flag == "true" or flag == "yes")
  local title_line = text.upper(kind) .. " TESTIMONY" .. (and_exhibits and " AND EXHIBITS" or "") .. " OF"

  local x = {}
  table.insert(x, cover_para("CoverPage", "BEFORE THE", '<w:spacing w:after="0"/>'))
  table.insert(x, cover_para("CoverPage", text.upper(commission)))
  table.insert(x, cover_para("CoverCaption", ""))
  if #caption > 0 then
    table.insert(x, caption_table(caption, case_number))
  end
  table.insert(x, cover_para("CoverCaption", ""))
  table.insert(x, cover_para("CoverCaption", "", RULE_PPR))
  table.insert(x, cover_para("CoverCaption", "", RULE_PPR))
  table.insert(x, cover_para("CoverCaption", ""))
  table.insert(x, cover_para("CoverCaption", ""))
  table.insert(x, cover_para("CoverPage", title_line))
  table.insert(x, cover_para("CoverPage", witness))
  if witness_title then table.insert(x, cover_para("CoverPage", witness_title)) end
  table.insert(x, cover_para("CoverPage", "ON BEHALF OF"))
  table.insert(x, cover_para("CoverPage", text.upper(on_behalf_of)))
  if version_label then table.insert(x, cover_para("CoverPage", text.upper(version_label))) end
  table.insert(x, cover_para("CoverCaption", ""))
  table.insert(x, cover_para("CoverCaption", ""))
  table.insert(x, cover_para("CoverPage", date))

  local blocks = {}
  for _, chunk in ipairs(x) do
    table.insert(blocks, pandoc.RawBlock("openxml", chunk))
  end
  table.insert(blocks, pandoc.RawBlock("openxml", COVER_SECTION_BREAK))
  return blocks
end

--! ---------------------------------------------------------------------
--! Whole-document pass
--! ---------------------------------------------------------------------

--! Legacy markers from older QMDs; the cover is generated now.
local function is_legacy_marker(blk)
  local txt
  if blk.t == "RawBlock" then
    txt = blk.text or ""
  elseif blk.t == "Para" or blk.t == "Plain" then
    txt = inlines_text(blk.content)
  else
    return false
  end
  return txt:find("testimony%-body%-start") ~= nil or txt:find("testimony%-toc") ~= nil
end

function Pandoc(doc)
  doc = format_headings(doc)

  local out = {}
  for _, blk in ipairs(doc.blocks) do
    if not is_legacy_marker(blk) then table.insert(out, blk) end
  end
  out = apply_continuation_styles(out)

  local cover = build_cover(doc.meta)
  if cover then
    local combined = {}
    for _, b in ipairs(cover) do table.insert(combined, b) end
    for _, b in ipairs(out) do table.insert(combined, b) end
    out = combined
  end

  doc.blocks = out
  return doc
end
