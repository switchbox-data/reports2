--! Pandoc Lua filter: mark each testimony question for the HTML preview.
--!
--! Questions are written ``**Q.** ...``. Pandoc turns those into plain
--! paragraphs with no class, so CSS cannot tell a question from an answer
--! or from any other paragraph that starts with bold text. This filter
--! wraps each question paragraph in ``<div class="qa-question">`` so
--! ``reports/.style/testimony.scss`` can put space above every new pair.
--!
--! Only the question paragraph is wrapped. Answers (and the figures,
--! tables and lists inside them) are left where they are, because Quarto's
--! page grid positions wide figures as direct children of the page and
--! would stop doing so if they were nested in a wrapper.
--!
--! HTML only: it is listed under ``format: html: filters:`` in a testimony
--! file, so the Word export (``lib/just/templates/filters/testimony.lua``)
--! never sees it.

local function is_question(p)
  local first = p.content[1]
  if first == nil or first.t ~= "Strong" then
    return false
  end
  local label = pandoc.utils.stringify(first):gsub("%s+", "")
  return label == "Q."
end

function Para(p)
  if is_question(p) then
    return pandoc.Div({ p }, pandoc.Attr("", { "qa-question" }))
  end
end
