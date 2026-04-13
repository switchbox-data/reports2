-- icml_math.lua
-- Pre-renders LaTeX math to SVG for ICML output using latex + dvisvgm.
-- Replaces Math nodes with Image elements so Pandoc's ICML writer never
-- encounters math it can't convert (eliminating "Could not convert TeX math"
-- warnings and producing correct equations in InDesign).
--
-- Requires: TinyTeX or TeX Live (latex, dvisvgm on PATH or in ~/.TinyTeX/).
-- Requires: ghostscript (for dvisvgm PostScript special processing).
--
-- Usage: add to _quarto.yml:
--   filters:
--     - path: ../../lib/quarto_extensions/icml_math/icml_math.lua

if FORMAT ~= "icml" then
  return {}
end

local pandoc_path = require("pandoc.path")

-- ---------------------------------------------------------------------------
-- Find binaries
-- ---------------------------------------------------------------------------

local function find_binary(name)
  local handle = io.popen("command -v " .. name .. " 2>/dev/null")
  if handle then
    local result = handle:read("*a"):gsub("%s+$", "")
    handle:close()
    if result ~= "" then
      return result
    end
  end

  local home = os.getenv("HOME") or "/root"
  local locations = {
    home .. "/.TinyTeX/bin/x86_64-linux/" .. name,
    home .. "/.TinyTeX/bin/aarch64-linux/" .. name,
    "/root/.TinyTeX/bin/x86_64-linux/" .. name,
    "/opt/TinyTeX/bin/x86_64-linux/" .. name,
    "/opt/TinyTeX/bin/aarch64-linux/" .. name,
  }
  for _, path in ipairs(locations) do
    local f = io.open(path, "r")
    if f then
      f:close()
      return path
    end
  end
  return nil
end

local latex_bin = find_binary("latex")
local dvisvgm_bin = find_binary("dvisvgm")

if not latex_bin then
  io.stderr:write(
    "[icml_math] WARNING: 'latex' not found on PATH or in TinyTeX. "
      .. "Install TinyTeX with: quarto install tinytex\n"
      .. "Math will remain as raw TeX in the ICML output.\n"
  )
  return {}
end

if not dvisvgm_bin then
  io.stderr:write(
    "[icml_math] WARNING: 'dvisvgm' not found. "
      .. "Install with: tlmgr install dvisvgm\n"
      .. "Math will remain as raw TeX in the ICML output.\n"
  )
  return {}
end

-- ---------------------------------------------------------------------------
-- Output and cache directories
-- ---------------------------------------------------------------------------

-- Place SVGs in math/ relative to the CWD (the Quarto project directory).
-- Pandoc resolves Image paths relative to CWD, so it can read the SVGs to get
-- real dimensions for the ICML output. The typeset recipe then copies math/ to
-- docs/math/ (alongside the ICML) so InDesign can find them.
local math_dir = "math"
os.execute("mkdir -p '" .. math_dir .. "'")

local cache_dir = "cache/icml_math"
os.execute("mkdir -p '" .. cache_dir .. "'")

-- ---------------------------------------------------------------------------
-- LaTeX rendering
-- ---------------------------------------------------------------------------

local TEX_PREAMBLE = table.concat({
  "\\documentclass[border=1pt]{standalone}",
  "\\usepackage{amsmath}",
  "\\usepackage{amssymb}",
  "\\usepackage{mathtools}",
  "\\begin{document}",
}, "\n")

local TEX_POSTAMBLE = "\n\\end{document}\n"

local function make_tex(math_text, display)
  local wrapped
  if display then
    wrapped = "$\\displaystyle " .. math_text .. "$"
  else
    wrapped = "$" .. math_text .. "$"
  end
  return TEX_PREAMBLE .. "\n" .. wrapped .. TEX_POSTAMBLE
end

local function render_to_svg(math_text, display)
  local mode_tag = display and "D" or "I"
  local hash = pandoc.utils.sha1(mode_tag .. math_text)
  local svg_name = "eq_" .. hash:sub(1, 16) .. ".svg"
  local svg_output = pandoc_path.join({ math_dir, svg_name })
  local svg_cache = pandoc_path.join({ cache_dir, svg_name })

  -- Serve from cache if available
  local cached = io.open(svg_cache, "r")
  if cached then
    cached:close()
    os.execute("cp '" .. svg_cache .. "' '" .. svg_output .. "'")
    return svg_name
  end

  -- Create temp directory
  local tmpdir = os.tmpname() .. "_icml_math"
  os.execute("mkdir -p '" .. tmpdir .. "'")

  local tex_path = pandoc_path.join({ tmpdir, "eq.tex" })
  local tex_file = io.open(tex_path, "w")
  if not tex_file then
    io.stderr:write("[icml_math] ERROR: cannot write " .. tex_path .. "\n")
    os.execute("rm -rf '" .. tmpdir .. "'")
    return nil
  end
  tex_file:write(make_tex(math_text, display))
  tex_file:close()

  -- latex -> DVI
  local latex_cmd = "'" .. latex_bin .. "'"
    .. " -interaction=nonstopmode"
    .. " -output-directory='" .. tmpdir .. "'"
    .. " '" .. tex_path .. "'"
    .. " >/dev/null 2>&1"
  local latex_ok = os.execute(latex_cmd)
  if not latex_ok then
    io.stderr:write(
      "[icml_math] WARNING: latex failed for: " .. math_text:sub(1, 80) .. "...\n"
    )
    os.execute("rm -rf '" .. tmpdir .. "'")
    return nil
  end

  -- DVI -> SVG
  local dvi_path = pandoc_path.join({ tmpdir, "eq.dvi" })
  local dvisvgm_cmd = "'" .. dvisvgm_bin .. "'"
    .. " --no-fonts"
    .. " '" .. dvi_path .. "'"
    .. " -o '" .. svg_output .. "'"
    .. " >/dev/null 2>&1"
  local svg_ok = os.execute(dvisvgm_cmd)
  if not svg_ok then
    io.stderr:write(
      "[icml_math] WARNING: dvisvgm failed for: " .. math_text:sub(1, 80) .. "...\n"
    )
    os.execute("rm -rf '" .. tmpdir .. "'")
    return nil
  end

  -- Verify output exists
  local verify = io.open(svg_output, "r")
  if not verify then
    io.stderr:write("[icml_math] WARNING: SVG not produced for: " .. math_text:sub(1, 80) .. "\n")
    os.execute("rm -rf '" .. tmpdir .. "'")
    return nil
  end
  verify:close()

  -- Cache for next render
  os.execute("cp '" .. svg_output .. "' '" .. svg_cache .. "'")
  os.execute("rm -rf '" .. tmpdir .. "'")
  return svg_name
end

-- ---------------------------------------------------------------------------
-- Pandoc filter
-- ---------------------------------------------------------------------------

local eq_count = 0

return {
  {
    Math = function(el)
      local display = el.mathtype == "DisplayMath"
      local svg_name = render_to_svg(el.text, display)

      if not svg_name then
        return el
      end

      eq_count = eq_count + 1
      local alt_text = el.text:sub(1, 120)
      local img = pandoc.Image(alt_text, "math/" .. svg_name)
      if display then
        img.classes:insert("display-math")
      else
        img.classes:insert("inline-math")
      end
      return img
    end,
  },
  {
    Pandoc = function(doc)
      if eq_count > 0 then
        io.stderr:write("[icml_math] Rendered " .. eq_count .. " equations to SVG in " .. math_dir .. "/\n")
      end
      return doc
    end,
  },
}
