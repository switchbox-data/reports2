--! Pandoc Lua filter for interrogatory-response Word output.
--!
--! Applied by ``lib.just.interrogatory`` when ``just interrogatories`` renders.
--! Every level-2 heading in the QMD is one response (its text is the response
--! label, e.g. "CIEC-1").  For each response this filter writes, in order:
--!
--!   Date Filed:  <date>
--!   Witness:     <witness>
--!   Request from: <requesting party>
--!   Question:    <the ``question`` block>
--!   Response:    <the ``response`` block>
--!
--! and then a Word section break, so every response is its own section.  The
--! per-response header (party, docket, set, date issued, label, "Page n of N")
--! is *not* written here: ``lib.just.interrogatory`` patches one header part
--! onto each section after Quarto finishes, because Pandoc cannot write
--! per-section headers.
--!
--! ``-M ir-only:<label>`` keeps just that one response (used by ``--split``);
--! a single response needs no section break, so it uses the model file's
--! closing section.
--!
--! ``[@key]`` citations are dropped: write every citation out in full in a
--! footnote, as in expert testimony.

local function xml_escape(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local function field(tbl, key)
  local v = tbl[key]
  if v == nil then return nil end
  local s = pandoc.utils.stringify(v):gsub("\194\160", " ")
  if s == "" then return nil end
  return s
end

local function tab()
  return pandoc.RawInline("openxml", "<w:r><w:tab/></w:r>")
end

local function styled(style, inlines)
  return pandoc.Div({ pandoc.Para(inlines) }, pandoc.Attr("", {}, { ["custom-style"] = style }))
end

--! Section break that ends one response: next page, page numbers restart at 1.
--! The header is added later by Python.  The paragraph is made as small as
--! Word allows so it never spills onto a page of its own.
local SECTION_BREAK = [[
<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:pPr>
    <w:spacing w:before="0" w:after="0" w:line="20" w:lineRule="exact"/>
    <w:rPr><w:sz w:val="2"/></w:rPr>
    <w:sectPr>
      <w:type w:val="nextPage"/>
      <w:pgSz w:w="12240" w:h="15840" w:code="1"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
      <w:pgNumType w:start="1"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:pPr>
</w:p>
]]

function Meta(meta)
  meta.title = nil
  meta.subtitle = nil
  meta.author = nil
  meta.date = nil
  return meta
end

--! Drop ``[@key]`` citations (and the space before them).
function Inlines(inlines)
  local out = pandoc.Inlines({})
  for _, el in ipairs(inlines) do
    if el.t == "Cite" then
      if #out > 0 and out[#out].t == "Space" then out:remove(#out) end
    else
      out:insert(el)
    end
  end
  return out
end

local function has_class(div, name)
  for _, c in ipairs(div.attr.classes) do
    if c == name then return true end
  end
  return false
end

local function append_blocks(dst, blocks)
  for _, b in ipairs(blocks) do table.insert(dst, b) end
end

--! Referenced-testimony lines.  ``lib.just.interrogatory_reftext`` writes one paragraph per passage, one line per
--! source line, each as ``<page:line><2 em spaces><text>`` joined by hard line breaks.  A list item's marker
--! (``1.``, ``2)``, a bullet) is preceded by non-breaking spaces, and its runon lines by more of them.  Each
--! line becomes one Word paragraph (style IR Testimony Line) with real tab stops and hanging indents, so the
--! text lines up after the line numbers, list numbers are indented, and runon text is indented further.
local NBSP = "\194\160"
local EM = "\226\128\131"
local FIGURE_SPACE = "\226\128\135"
local TEXT_COL = 1080 -- where unindented text starts (twips), as in the style
local MARKER_COL = 1440 -- where a list marker starts
local ITEM_COL = 1800 -- where a list item's text, and its runon lines, start

local function text_run(text, fmt)
  if text == "" then return "" end
  local rpr = (fmt.b and "<w:b/><w:bCs/>" or "") .. (fmt.i and "<w:i/><w:iCs/>" or "")
    .. (fmt.sup and '<w:vertAlign w:val="superscript"/>' or "")
  if rpr ~= "" then rpr = "<w:rPr>" .. rpr .. "</w:rPr>" end
  return string.format('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>', rpr, xml_escape(text))
end

local function with_fmt(fmt, key)
  local out = { b = fmt.b, i = fmt.i, sup = fmt.sup }
  out[key] = true
  return out
end

--! Footnote marks with no definition in the question stay literal text (``[^3]``); show them superscript.
local function str_runs(text, fmt)
  local out, pos = {}, 1
  while true do
    local a, b, num = text:find("%[%^(%w+)%]", pos)
    if not a then break end
    table.insert(out, text_run(text:sub(pos, a - 1), fmt))
    table.insert(out, text_run(num, with_fmt(fmt, "sup")))
    pos = b + 1
  end
  table.insert(out, text_run(text:sub(pos), fmt))
  return table.concat(out)
end

local function inline_runs(inlines, fmt)
  local out = {}
  for _, el in ipairs(inlines) do
    local t = el.t
    if t == "Str" then
      table.insert(out, str_runs(el.text, fmt))
    elseif t == "Space" or t == "SoftBreak" then
      table.insert(out, text_run(" ", fmt))
    elseif t == "Strong" then
      table.insert(out, inline_runs(el.content, with_fmt(fmt, "b")))
    elseif t == "Emph" then
      table.insert(out, inline_runs(el.content, with_fmt(fmt, "i")))
    elseif t == "Superscript" then
      table.insert(out, inline_runs(el.content, with_fmt(fmt, "sup")))
    elseif t == "Quoted" then
      local q = el.quotetype == "SingleQuote" and { "\u{2018}", "\u{2019}" } or { "\u{201C}", "\u{201D}" }
      table.insert(out, text_run(q[1], fmt) .. inline_runs(el.content, fmt) .. text_run(q[2], fmt))
    elseif t == "Link" or t == "Span" or t == "Underline" or t == "SmallCaps" then
      table.insert(out, inline_runs(el.content, fmt))
    elseif t == "Note" then
      -- a defined footnote: not expected inside a quotation
    else
      table.insert(out, text_run(pandoc.utils.stringify(el), fmt))
    end
  end
  return table.concat(out)
end

local function starts_with(s, prefix) return s:sub(1, #prefix) == prefix end

--! Split a Para's inlines into one list per source line (at hard line breaks).
local function split_lines(inlines)
  local lines, cur = {}, {}
  for _, el in ipairs(inlines) do
    if el.t == "LineBreak" then
      table.insert(lines, cur)
      cur = {}
    else
      table.insert(cur, el)
    end
  end
  table.insert(lines, cur)
  return lines
end

--! Pull the line reference (``6:13`` or ``83 n.75``) and the gap after it off the front of a line.
local function take_label(line)
  local first = line[1]
  if not first or first.t ~= "Str" then return nil end
  local rest = {}
  local label, tail
  local ref, after = first.text:match("^(%d+:%d+)(.*)$")
  if ref then
    label, tail = ref, after
    for i = 2, #line do table.insert(rest, line[i]) end
  elseif first.text:match("^%d+$") and line[2] and line[2].t == "Space"
    and line[3] and line[3].t == "Str" then
    local n, after_n = line[3].text:match("^(n%.%d+)(.*)$")
    if not n then return nil end
    label, tail = first.text .. " " .. n, after_n
    for i = 4, #line do table.insert(rest, line[i]) end
  else
    return nil
  end
  -- Tolerate the old tab separator, which pandoc turns into a plain space.
  while starts_with(tail, EM) or starts_with(tail, FIGURE_SPACE) do tail = tail:sub(#EM + 1) end
  if tail ~= "" then table.insert(rest, 1, pandoc.Str(tail)) end
  while rest[1] and rest[1].t == "Space" do table.remove(rest, 1) end
  return label, rest
end

--! Read the indentation shape of a line's text: ("marker", "1.") / ("runon") / ("plain").
local function classify(body)
  local nbsp = 0
  local first = body[1]
  if first and first.t == "Str" then
    local text = first.text
    while starts_with(text, NBSP) do
      nbsp = nbsp + 1
      text = text:sub(#NBSP + 1)
    end
    if nbsp > 0 then
      if text == "" then table.remove(body, 1) else body[1] = pandoc.Str(text) end
    end
  end
  first = body[1]
  if nbsp > 0 and first and first.t == "Str" and body[2] and body[2].t == "Space"
    and (first.text:match("^%d+[%.%)]$") or first.text == "\u{2022}") then
    local marker = first.text
    table.remove(body, 1)
    table.remove(body, 1)
    return "marker", marker
  end
  if nbsp > 0 then return "runon" end
  return "plain"
end

local function testimony_line(line)
  local label, body = take_label(line)
  if not label then return nil end
  local kind, marker = classify(body)
  local runs = inline_runs(body, {})
  local tab = "<w:r><w:tab/></w:r>"
  local ppr, lead
  if kind == "marker" then
    ppr = string.format(
      '<w:tabs><w:tab w:val="clear" w:pos="%d"/><w:tab w:val="left" w:pos="%d"/><w:tab w:val="left" w:pos="%d"/></w:tabs>'
        .. '<w:ind w:left="%d" w:hanging="%d"/>',
      TEXT_COL, MARKER_COL, ITEM_COL, ITEM_COL, ITEM_COL)
    lead = text_run(label, {}) .. tab .. text_run(marker, {}) .. tab
  elseif kind == "runon" then
    ppr = string.format(
      '<w:tabs><w:tab w:val="clear" w:pos="%d"/><w:tab w:val="left" w:pos="%d"/></w:tabs><w:ind w:left="%d" w:hanging="%d"/>',
      TEXT_COL, ITEM_COL, ITEM_COL, ITEM_COL)
    lead = text_run(label, {}) .. tab
  else
    ppr = ""
    lead = text_run(label, {}) .. tab
  end
  return pandoc.RawBlock(
    "openxml",
    string.format(
      '<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:pPr><w:pStyle w:val="IRTestimonyLine"/>%s</w:pPr>%s%s</w:p>',
      ppr, lead, runs
    )
  )
end

--! A passage paragraph (one or more source lines) as Word paragraphs.
local function testimony_lines(inlines)
  local out = {}
  for _, line in ipairs(split_lines(inlines)) do
    local blk = testimony_line(line)
    if blk then
      table.insert(out, blk)
    elseif #line > 0 then
      table.insert(out, styled("IR Testimony Line", line))
    end
  end
  return out
end

local function passage_title_para(para)
  local s = pandoc.utils.stringify(para)
  return s:match("^Velez Direct, printed") ~= nil
end

--! Style the nested ``referenced-testimony`` block inside a question.
local function format_referenced_testimony(div)
  local out = {}
  table.insert(
    out,
    styled(
      "IR Testimony Heading",
      { pandoc.Emph({ pandoc.Str("Referenced testimony (not part of the request)") }) }
    )
  )
  for _, blk in ipairs(div.content) do
    if blk.t == "Para" then
      if passage_title_para(blk) then
        table.insert(out, styled("IR Testimony Passage", blk.content))
      else
        append_blocks(out, testimony_lines(blk.content))
      end
    elseif blk.t == "Div" then
      for _, child in ipairs(blk.content) do
        if child.t == "Para" then
          if passage_title_para(child) then
            table.insert(out, styled("IR Testimony Passage", child.content))
          else
            append_blocks(out, testimony_lines(child.content))
          end
        else
          table.insert(out, child)
        end
      end
    else
      table.insert(out, blk)
    end
  end
  return out
end

local function normalize_question(blocks)
  local out = {}
  for _, blk in ipairs(blocks) do
    if blk.t == "Div" and has_class(blk, "referenced-testimony") then
      local inner = format_referenced_testimony(blk)
      for _, b in ipairs(inner) do
        table.insert(out, b)
      end
    else
      table.insert(out, blk)
    end
  end
  return out
end

local function append_all(dst, blocks)
  for _, b in ipairs(blocks) do table.insert(dst, b) end
end

function Pandoc(doc)
  local cfg = doc.meta["interrogatory_responses"]
  if type(cfg) ~= "table" then
    error("The frontmatter has no interrogatory_responses block.")
  end
  local requesting_party = field(cfg, "requesting_party") or ""
  local default_witness = field(cfg, "witness") or ""
  local date_filed = field(doc.meta, "ir-date-filed-long") or field(cfg, "date_filed") or ""
  local only = field(doc.meta, "ir-only")

  -- Gather the responses: each heading starts one; its question/response divs fill it.
  local sections = {}
  local cur = nil
  for _, blk in ipairs(doc.blocks) do
    if blk.t == "Header" then
      cur = {
        label = pandoc.utils.stringify(blk.content),
        witness = blk.attr.attributes["witness"],
        question = {},
        response = {},
      }
      table.insert(sections, cur)
    elseif blk.t == "Div" and cur then
      if has_class(blk, "question") then
        append_all(cur.question, blk.content)
      elseif has_class(blk, "response") then
        append_all(cur.response, blk.content)
      end
    end
  end

  if only then
    local kept = {}
    for _, s in ipairs(sections) do
      if s.label == only then table.insert(kept, s) end
    end
    if #kept == 0 then error("No response labelled " .. only) end
    sections = kept
  end

  local out = {}
  for i, s in ipairs(sections) do
    local witness = s.witness or default_witness
    table.insert(out, styled("IR Meta", { pandoc.Strong({ pandoc.Str("Date Filed:") }), tab(), pandoc.Str(date_filed) }))
    table.insert(out, styled("IR Meta", { pandoc.Strong({ pandoc.Str("Witness:") }), tab(), pandoc.Str(witness) }))
    table.insert(out, styled("IR Meta", { pandoc.Strong({ pandoc.Str("Request from:") }), tab(), pandoc.Str(requesting_party) }))
    table.insert(out, styled("IR Label", { pandoc.Strong({ pandoc.Str("Question:") }) }))
    append_all(out, normalize_question(s.question))
    table.insert(out, styled("IR Label", { pandoc.Strong({ pandoc.Str("Response:") }) }))
    if #s.response == 0 then
      table.insert(out, pandoc.Para({ pandoc.Emph({ pandoc.Str("[Response not yet written.]") }) }))
    else
      append_all(out, s.response)
    end
    if i < #sections then
      table.insert(out, pandoc.RawBlock("openxml", SECTION_BREAK))
    end
  end

  doc.blocks = out
  return doc
end
