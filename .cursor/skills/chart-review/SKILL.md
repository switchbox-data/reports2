---
name: chart-review
description: >-
  Choose, design and review data visualizations using Switchbox's dataviz
  guides: profile the data and pick the chart type from its shape and the
  reader's question (with the reasoning for why it fits), avoid distortions,
  pick palettes by color's job, title and label for the message, then render
  the chart, look at the image and run the checklist. Use whenever creating,
  modifying, choosing or reviewing a chart, figure, plot or map in any tool
  (plotnine, ggplot2, matplotlib, Datawrapper, Excel), when the user asks
  which chart to use for some data, or asks for a chart critique or dataviz
  audit.
---

# Chart review

Two guides hold the rules; this skill is the workflow.

- `context/code/dataviz_chart_selection.md`: **which chart** to use, from the shape of the data and the reader's question, and why each chart fits where it fits.
- `context/code/dataviz_design_guide.md`: **how to draw it** honestly and readably, plus the review checklist (§9).

For plotting-code mechanics (never guess an API, test in a standalone script, plotnine pitfalls, sizing), follow the "Plotting and visualization" section of `AGENTS.md`. That section gets the code right; this skill gets the chart right.

## When making or changing a chart

1. **Read the guides.** Once per session, before your first chart, read the selection guide (§1–§3, plus the §4 entry for any chart you're considering) and the design guide (at least §0 and §9).
2. **Write the message.** Decide whether the chart is explanatory (report, testimony, slides) or exploratory (analysis notebook). For explanatory charts, write the one-sentence takeaway before writing code. If the user hasn't given one and it isn't clear from the surrounding narrative, ask.
3. **Profile the data.** Run the selection guide's §1 checks on the actual data: column roles, distinct values, rows per group, total n, crossed vs nested, additivity, shared units, skew, grid completeness, sign, weights. Don't infer them from column names. If you can't see the data, ask the user the questions whose answers would change the choice.
4. **Choose the chart type.** Match the profile to a shape (selection guide §2), read the candidates and reasoning for it (§3), and check the chosen chart's "when not" in §4 and §5. Pick the candidate whose most accurate encoding carries the message. For exploratory work, try two or three candidates. When you suggest a chart to the user, give the reason in terms of their data ("each heating type has thousands of homes, so a boxplot hides the bimodal bills; a violin shows them").
5. **Decide color's job** (design guide §4): none, highlight, group identity, ordered value, or diverging. Choose the palette type to match. In reports2, check design guide §7 for the brand palette's limits and for existing color maps to reuse.
6. **Build it**, following the `AGENTS.md` test-plot workflow.
7. **Render at the final size and look at the image.** Read the PNG or SVG with the Read tool. Never review a chart from its code alone: overlapping labels, unreadable text, blobs and color clashes only show up in the image.
8. **Run the design guide's §9 checklist** against the image, and against the code for things the image can't show (n, error-bar type, the data behind labels). Fix each failure and re-render. Repeat until every item passes or has a stated reason.
9. **Report** to the user: the takeaway, the chart, why this chart type fits the data, and any checklist items you deliberately left unmet, with the reason.

## When auditing existing charts

1. Render the document, or the notebook cells that produce the figures. Then view each figure image.
2. For each figure, check whether the chart type fits the data's shape (selection guide §1–§3), then run the design guide's §9 checklist. Record only the failures. For each failure, give:
   - the figure label,
   - the rule (with its guide and section),
   - what you see,
   - a concrete fix,
   - a severity:
     - **misleading**: a reader would draw a wrong conclusion (design guide §2–§3 failures, or a chart type that hides what the data shows, such as a bare boxplot over a tiny group),
     - **hard to read**: the reader can get the point, but slowly or not at all,
     - **polish**: everything else.
3. Present misleading items first. Don't edit the charts unless the user asks.
4. Don't flag house-theme choices (design guide §7) as failures. If a house-theme default itself conflicts with the guides, list it separately as a house-style question for the user.

## Judgment calls

- The rules are defaults, not laws. Design guide §8 and selection guide §5 record where the sources disagree and the position we take. When a rule conflicts with the message, the honesty rules (design guide §2, §3) win over the readability and polish rules (§4–§6).
- The selection guide's thresholds (about 2,000 points, about 7 colors, about 20–30 rows per group) are prompts to look at the rendered chart, not cutoffs.
- Exploratory notebook charts only need the honesty rules. Don't spend effort polishing them unless they will be embedded in a report.
- If a fix would change a number or a claim in the narrative (for example, normalizing a map, or splitting a pooled trend), stop and tell the user. Don't silently change what the chart says.
