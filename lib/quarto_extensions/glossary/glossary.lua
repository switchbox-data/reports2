-- Glossary.lua
-- Author: Lisa DeBruine (modified by Switchbox)

-- Global glossary table
globalGlossaryTable = {}

-- Helper Functions

local function addHTMLDeps()
    quarto.doc.add_html_dependency({
    name = 'glossary',
    stylesheets = {'glossary.css'}
  })
end

local function kwExists(kwargs, keyword)
    for key, value in pairs(kwargs) do
        if key == keyword then
            return true
        end
    end
    return false
end

function sortByKeys(tbl)
    local sortedKeys = {}
    for key, _ in pairs(tbl) do
        table.insert(sortedKeys, key)
    end
    table.sort(sortedKeys)
    local sortedTable = {}
    for _, key in pairs(sortedKeys) do
        sortedTable[key] = tbl[key]
    end
    return sortedTable
end

local function glossaryDL(term, def)
  return "<dl class='glossary-dl'><dt>" .. term .. "</dt><dd>" .. def .. "</dd></dl>"
end

local function metaToHTML(metaValue)
  local blocks
  if type(metaValue) == "table" and #metaValue > 0 then
    blocks = metaValue
  else
    return pandoc.utils.stringify(metaValue)
  end
  local html = pandoc.write(pandoc.Pandoc(blocks), "html")
  html = html:gsub("^%s+", ""):gsub("%s+$", "")
  -- strip wrapping <p> tags for single-paragraph definitions so the
  -- result sits cleanly inside <dd> without extra vertical spacing
  if not html:find("</p>%s*<p") then
    html = html:gsub("^<p>", ""):gsub("</p>$", "")
  end
  return html
end

local function lookupDef(term, options)
  local metafile = io.open(options.path, 'r')
  if not metafile then
    io.stderr:write("Cannot open glossary file " .. options.path)
    return ""
  end
  local content = "---\n" .. metafile:read("*a") .. "\n---\n"
  metafile:close()
  local glossary = pandoc.read(content, "markdown").meta
  for key, value in pairs(glossary) do
    glossary[string.lower(key)] = value
  end
  if kwExists(glossary, term) then
    return metaToHTML(glossary[term])
  end
  return ""
end

---Merge user provided options with defaults
---@param userOptions table
local function mergeOptions(userOptions, meta)
  local defaultOptions = {
    path = "glossary.yml",
    popup = "hover",
    show = true,
    add_to_table = true
  }

  if meta.glossary ~= nil then
    for k, v in pairs(meta.glossary) do
      local value = pandoc.utils.stringify(v)
      if value == 'true' then value = true end
      if value == 'false' then value = false end
      defaultOptions[k] = value
    end
  end

  if userOptions ~= nil then
    for k, v in pairs(userOptions) do
      local value = pandoc.utils.stringify(v)
      if value == 'true' then value = true end
      if value == 'false' then value = false end
      defaultOptions[k] = value
    end
  end

  return defaultOptions
end


-- Shortcodes

return {

["glossary"] = function(args, kwargs, meta)
  local options = mergeOptions(kwargs, meta)
  local display = pandoc.utils.stringify(args[1])
  local term = string.lower(display)

  if kwExists(kwargs, "display") then
    display = pandoc.utils.stringify(kwargs.display)
  end

  if not quarto.doc.isFormat("html:js") then
    -- Wrap in a Span with class "GlossaryTerm" so the ICML writer emits a
    -- dedicated CharacterStyle/GlossaryTerm that the designer can style in
    -- one place. Nest Strong inside so terms default to bold until the
    -- designer defines the GlossaryTerm character style in InDesign.
    return pandoc.Span(
      pandoc.Strong(pandoc.Str(display)),
      pandoc.Attr("", {"GlossaryTerm"})
    )
  end

  addHTMLDeps()

  -- create glossary table
  if kwExists(kwargs, "table") then
    local gt = "<table class='glossary_table'>\n"
    gt = gt .. "<tr><th> Term </th><th> Definition </th></tr>\n"
    local sortedTable = sortByKeys(globalGlossaryTable)
    for key, value in pairs(sortedTable) do
        gt = gt .. "<tr><td>" .. key
        gt = gt .. "</td><td>" .. value .. "</td></tr>\n"
    end
    gt = gt .. "</table>"
    return pandoc.RawBlock('html', gt)
  end

  local def = ""
  if kwExists(kwargs, "def") then
    def = pandoc.utils.stringify(kwargs.def)
  else
    def = lookupDef(term, options)
  end

  if options.add_to_table then
    globalGlossaryTable[term] = def
  end

  local glosstext
  if options.popup == "hover" then
    glosstext = "<button class='glossary'><span class='def'>"
      .. glossaryDL(display, def)
      .. "</span>" .. display .. "</button>"
  elseif options.popup == "click" then
    glosstext = "<button class='glossary'><span class='def'>"
      .. glossaryDL(display, def)
      .. "</span>" .. display .. "</button>"
  elseif options.popup == "none" then
    glosstext = "<button class='glossary'>" .. display .. "</button>"
  end

  return pandoc.RawInline("html", glosstext)
end,

["glossary-def"] = function(args, kwargs, meta)
  local options = mergeOptions(kwargs, meta)
  local display = pandoc.utils.stringify(args[1])
  local term = string.lower(display)

  local def = ""
  if kwExists(kwargs, "def") then
    def = pandoc.utils.stringify(kwargs.def)
  else
    def = lookupDef(term, options)
  end

  if not quarto.doc.isFormat("html:js") then
    local defDoc = pandoc.read(def, "html")
    local termSpan = pandoc.Span(
      pandoc.Strong(pandoc.Str(display)),
      pandoc.Attr("", {"GlossaryTerm"})
    )
    local blocks = pandoc.Blocks({
      pandoc.Para({ termSpan })
    })
    for _, block in ipairs(defDoc.blocks) do
      blocks:insert(block)
    end
    return pandoc.Div(blocks, pandoc.Attr("", {"GlossaryDef"}))
  end

  addHTMLDeps()

  if options.add_to_table == nil or options.add_to_table then
    globalGlossaryTable[term] = def
  end

  return pandoc.RawBlock('html', glossaryDL(display, def))
end

}
