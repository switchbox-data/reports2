-- icml_gt.lua
-- Promotes SVG carrier figures produced by ``lib.quarto.display_gt`` into
-- native ICML ``<Table>`` blocks when rendering a Quarto Manuscript for
-- the ICML (InDesign/InCopy) target.
--
-- **Why this filter exists.** Quarto's ``{{< embed >}}`` pipeline is picky
-- about which cell outputs it'll round-trip through the
-- ``.embed.ipynb → AST`` path for a non-HTML target:
--
-- * ``text/markdown`` outputs are stripped entirely for ``tbl-*`` cells.
-- * ``text/html`` outputs survive the ``.embed.ipynb`` step but Pandoc's
--   ICML writer emits "Unable to display output for mime type(s):
--   text/html" in their place.
-- * ``image/svg+xml`` outputs *do* survive end-to-end: Quarto writes
--   them to disk and Pandoc references them via ``pandoc.Image``.
--
-- So ``display_gt`` packages the ICML XML as base64 inside an
-- otherwise-empty 1×1 SVG carrier.  This filter intercepts
-- ``FloatRefTarget`` nodes (for ``tbl-*`` labelled cells, which
-- otherwise flow through ``icml_floats.lua``'s Figure path and end up
-- with a stray ``(a)`` subfigure label from Pandoc's writer) and plain
-- ``pandoc.Figure`` / ``pandoc.Image`` nodes (safety net for bare
-- ``display_gt`` calls not wrapped in a cross-ref) whose image content
-- is a carrier SVG, reads the payload off disk, decodes it, and emits
-- a ``pandoc.Div`` containing:
--
-- 1. ``RawBlock("icml", <decoded xml>)`` — the native table
-- 2. ``RawBlock("icml", "<ParagraphStyleRange.../Caption>...")`` — the
--    caption paragraph, preserved from ``caption_long``.
--
-- The renderer path avoids Pandoc's Figure writer entirely, so no
-- subfigure label leaks in.
--
-- Registration order matters: this file must precede
-- ``icml_floats.lua`` in ``_quarto.yml``'s ``filters`` list so our
-- ``add_renderer`` predicate runs first (Quarto dispatches to the
-- earliest-matching predicate).

if FORMAT ~= "icml" then
  return {}
end

local _DEBUG = os.getenv("SWITCHBOX_ICML_GT_DEBUG") == "1"

local function debug_log(msg)
  if _DEBUG then
    io.stderr:write("[icml_gt] " .. msg .. "\n")
  end
end

-- ---------------------------------------------------------------------------
-- Base64 decode (self-contained; avoids depending on a Lua library)
-- ---------------------------------------------------------------------------

local B64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
local B64_LOOKUP = {}
for i = 1, #B64_ALPHABET do
  B64_LOOKUP[B64_ALPHABET:sub(i, i)] = i - 1
end

local function b64_decode(data)
  if not data or data == "" then
    return ""
  end
  local stripped = data:gsub("%s", "")
  while stripped:sub(-1) == "=" do
    stripped = stripped:sub(1, -2)
  end
  local out = {}
  local buf, bits = 0, 0
  for i = 1, #stripped do
    local v = B64_LOOKUP[stripped:sub(i, i)]
    if v then
      buf = buf * 64 + v
      bits = bits + 6
      if bits >= 8 then
        bits = bits - 8
        local byte = math.floor(buf / (2 ^ bits))
        buf = buf - byte * (2 ^ bits)
        out[#out + 1] = string.char(byte)
      end
    end
  end
  return table.concat(out)
end

-- ---------------------------------------------------------------------------
-- Carrier detection (by reading the referenced SVG file)
-- ---------------------------------------------------------------------------

local MARKER = "switchbox-icml-gt"
local PAYLOAD_PATTERN = "data%-icml%-b64:%s*([A-Za-z0-9+/=%s]+)"

local cache = {}

local function strip_file_scheme(src)
  return (src:gsub("^file:", ""))
end

--- Read ``src`` and, if it's one of our carrier SVGs, return the
--- decoded ICML XML.  Returns ``nil`` otherwise.  Cached per path.
local function extract_xml_from_svg(src)
  if not src or src == "" then
    return nil
  end
  local path = strip_file_scheme(src)
  if cache[path] ~= nil then
    if cache[path] == false then return nil end
    return cache[path]
  end
  if not path:match("%.svg$") then
    cache[path] = false
    return nil
  end
  local f = io.open(path, "r")
  if not f then
    cache[path] = false
    return nil
  end
  local content = f:read("*a")
  f:close()
  if not content:find(MARKER, 1, true) then
    cache[path] = false
    return nil
  end
  local b64 = content:match(PAYLOAD_PATTERN)
  if not b64 or b64 == "" then
    cache[path] = false
    return nil
  end
  local xml = b64_decode(b64)
  if xml == "" then
    cache[path] = false
    return nil
  end
  debug_log("promoted carrier SVG " .. path .. " (" .. #xml .. " bytes ICML)")
  cache[path] = xml
  return xml
end

--- Find the first Image node inside a list of blocks (or a single
--- Plain/Para) — used to inspect ``FloatRefTarget.content`` and
--- ``pandoc.Figure.content``.
local function first_image_in(content)
  if content == nil then return nil end
  -- Normalise: Blocks coerces Plain/Image either way.
  local function walk_inline_list(inlines)
    for _, inline in ipairs(inlines) do
      if inline.t == "Image" then return inline end
    end
    return nil
  end
  local function walk_block(block)
    if block.t == "Plain" or block.t == "Para" then
      return walk_inline_list(block.content)
    elseif block.t == "Image" then
      return block
    end
    return nil
  end
  if content.t then
    return walk_block(content)
  end
  -- Blocks / plain-table-of-blocks:
  for _, b in ipairs(content) do
    local im = walk_block(b)
    if im then return im end
  end
  return nil
end

--- Escape ``&``, ``<``, ``>`` for ICML ``<Content>`` bodies.
local function escape_xml(s)
  return s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;")
end

--- Build a raw-ICML ``ParagraphStyle/Caption`` paragraph from inline text.
local function raw_icml_caption(caption_inlines)
  local text = escape_xml(pandoc.utils.stringify(caption_inlines))
  local icml = '<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/Caption">'
    .. '<CharacterStyleRange AppliedCharacterStyle="$ID/NormalCharacterStyle">'
    .. "<Content>" .. text .. "</Content>"
    .. "</CharacterStyleRange>"
    .. "</ParagraphStyleRange>"
  return pandoc.RawBlock("icml", icml)
end

-- ---------------------------------------------------------------------------
-- FloatRefTarget renderer (primary path for tbl-* labelled cells)
-- ---------------------------------------------------------------------------

local _quarto = _G._quarto

if _quarto ~= nil and _quarto.ast ~= nil and _quarto.ast.add_renderer ~= nil then
  --- Decide whether a given FloatRefTarget is one of ours — it has Image
  --- content whose ``.src`` points to a carrier SVG on disk.
  local function is_carrier_float(float)
    if not float or float.content == nil then return nil end
    local im = first_image_in(float.content)
    if not im then return nil end
    return extract_xml_from_svg(im.src)
  end

  _quarto.ast.add_renderer("FloatRefTarget", function(float)
    if FORMAT ~= "icml" then return false end
    return is_carrier_float(float) ~= nil
  end, function(float)
    local xml = is_carrier_float(float)
    if _G.decorate_caption_with_crossref ~= nil then
      _G.decorate_caption_with_crossref(float)
    end
    local caption_inlines = quarto.utils.as_inlines(float.caption_long) or {}
    local blocks = { pandoc.RawBlock("icml", xml) }
    if #caption_inlines > 0 then
      blocks[#blocks + 1] = raw_icml_caption(caption_inlines)
    end
    return pandoc.Div(blocks)
  end)
end

-- ---------------------------------------------------------------------------
-- Safety-net filters for carrier SVGs NOT wrapped in a FloatRefTarget
-- ---------------------------------------------------------------------------

local function on_figure(fig)
  local im = first_image_in(fig.content)
  if not im then return nil end
  local xml = extract_xml_from_svg(im.src)
  if not xml then return nil end
  debug_log("on_figure matched; replacing Figure")
  return { pandoc.RawBlock("icml", xml) }
end

local function on_image(image)
  local xml = extract_xml_from_svg(image.src)
  if not xml then return nil end
  debug_log("on_image matched; replacing Image")
  return pandoc.RawInline("icml", xml)
end

return {
  { Figure = on_figure, Image = on_image },
}
