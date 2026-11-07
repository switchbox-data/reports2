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
    append_all(out, s.question)
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
