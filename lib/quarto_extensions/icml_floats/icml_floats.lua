-- icml_floats.lua
-- Registers a FloatRefTarget renderer for ICML output so that figures and
-- tables render with captions instead of triggering Quarto's placeholder
-- warning ("Output format icml does not currently support FloatRefTarget
-- nodes.").  Modeled on the built-in IPYNB renderer in Quarto's main.lua.
--
-- Pandoc's ICML writer produces captions from specific AST structures:
--   • pandoc.Figure wrapping an Image  → ParagraphStyle/Figure + ParagraphStyle/Caption
--   • pandoc.Table with a caption      → ParagraphStyle/TableCaption
-- For content that doesn't match either pattern (e.g. GT tables rendered as
-- base64 HTML), we inject a RawBlock("icml", ...) with ParagraphStyle/Caption
-- so the caption text gets a proper InDesign paragraph style.
--
-- User filters run in a sandboxed env that exposes _G (the real global table)
-- but not _quarto directly.  We reach through _G to register the renderer.

local _quarto = _G._quarto
if _quarto == nil or _quarto.ast == nil or _quarto.ast.add_renderer == nil then
  return {}
end

--- Escape XML special characters in a string.
local function escape_xml(s)
  return s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;")
end

--- Build a RawBlock that produces a ParagraphStyle/Caption paragraph in ICML.
--- Handles only plain text (inline formatting is stripped).
local function raw_icml_caption(caption_inlines)
  local text = escape_xml(pandoc.utils.stringify(caption_inlines))
  local icml = '<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/Caption">\n'
    .. '  <CharacterStyleRange AppliedCharacterStyle="$ID/NormalCharacterStyle">\n'
    .. '    <Content>' .. text .. '</Content>\n'
    .. '  </CharacterStyleRange>\n'
    .. '</ParagraphStyleRange>'
  return pandoc.RawBlock("icml", icml)
end

_quarto.ast.add_renderer("FloatRefTarget", function(_)
  return FORMAT == "icml"
end, function(float)
  if float.content == nil then
    return pandoc.Null()
  end

  _G.decorate_caption_with_crossref(float)

  local caption_inlines = quarto.utils.as_inlines(float.caption_long) or {}
  local caption_blocks = {}
  if #caption_inlines > 0 then
    caption_blocks = {pandoc.Plain(caption_inlines)}
  end

  -- Case 1: Image content → pandoc.Figure for Figure/Caption paragraph styles
  local im = quarto.utils.match("Plain/[1]/Image")(float.content)
  if im and im ~= true then
    return pandoc.Figure(pandoc.Plain({im}), {long = caption_blocks})
  end

  -- Case 2: Top-level pandoc.Table → set the Table's own caption
  if float.content.t == "Table" then
    float.content.caption = {long = caption_blocks}
    return float.content
  end

  -- Case 3: Other content (GT tables, HTML divs, etc.)
  -- Emit the content followed by a raw ICML caption paragraph so it gets
  -- ParagraphStyle/Caption in InDesign.
  local blocks = pandoc.Blocks({float.content})
  if #caption_inlines > 0 then
    blocks:insert(raw_icml_caption(caption_inlines))
  end
  return pandoc.Div(blocks)
end)

return {}
