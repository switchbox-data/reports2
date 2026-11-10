# Data visualization design guide

Design rules for making charts that are honest and easy to read. This guide is about **what to draw**, not how to code it: it applies to plotnine, ggplot2, matplotlib, Datawrapper, D3, Excel, or a hand-drawn sketch. For how our plotting code works (theme, sizing, embedding), see the "Plotting and visualization" section of `AGENTS.md`, `plotnine_sizing_in_quarto.md`, and `quarto_manuscript_embed_bug.md`.

**How to use it.** Read §1 before choosing a chart, skim §2–§6 while building it, and run the checklist in §9 on the rendered image before calling the chart done. To pick a chart from the shape of the data (rows per group, ordering, nesting, additivity), with the reasoning for each choice, see the companion `dataviz_chart_selection.md`. The `chart-review` skill (`.cursor/skills/chart-review/`) wraps both.

**Source.** Distilled from Yan Holtz's [Data to Viz caveat collection](https://www.data-to-viz.com/caveats.html) (61 flashcards and their articles, MIT license, [source repo](https://github.com/holtzy/data_to_viz)), reorganized by decision and reconciled where the cards and articles disagree (§8). Items marked _(ours)_ are our additions, not from the source.

## 0. First decide: explanatory or exploratory?

Many rules below depend on this.

- **Explanatory** charts (anything in a report, testimony, slide or memo) make one point to a reader who gives the chart a few seconds. They need a message title, a highlight, annotation, and ruthless decluttering.
- **Exploratory** charts (in an analysis notebook, for us) show everything so we can find the point. Descriptive titles, all series in color, full gridlines and default orderings are acceptable. Distortions are never acceptable: the honesty rules (§2, §3) apply to both.

Before drawing an explanatory chart, write down in one sentence what the reader should take away. If you can't, you are not ready to choose a chart type.

## 1. Choose the chart type

Pick by the reader's task, not by what looks interesting. The table below is the quick version, organized by task. When you have the data, start from `dataviz_chart_selection.md` instead: it profiles the data, narrows the candidates by its shape, and explains why each candidate wins in which situation. Position along a common scale is read most accurately, followed by length. Angle, area, and color intensity are read poorly. Prefer the encodings near the top of that ranking for anything the reader must compare.

| Reader's task                                                                                               | Use                                                                                                                                           | Avoid                                                                            |
| ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Compare or rank values across categories                                                                    | Sorted bar chart (horizontal when labels are long), lollipop for many categories, dot plot when zero isn't meaningful                         | Pie, donut, radial bars, circular barplot, bubbles, choropleth map, radar        |
| Compare two values per category (before/after, two years, two groups) where the **difference** is the story | Dumbbell plot (two dots joined by a line), slope chart                                                                                        | Side-by-side paired bars                                                         |
| Part-to-whole, few parts                                                                                    | Sorted bars of shares, a single 100% stacked bar, or a pie with 2–3 clearly unequal slices                                                    | Pie with many or similar slices, multiple pies side by side, 3D or exploded pies |
| Part-to-whole, many parts                                                                                   | Sorted bars, treemap                                                                                                                          | Pie                                                                              |
| Composition over time                                                                                       | Stacked area/bars **only if** the total and overall composition is the message; otherwise lines (few groups) or small multiples (many groups) | Stacked chart when the reader must track a middle layer                          |
| Trend over time                                                                                             | Line chart on a true time axis                                                                                                                | Unconnected dots, bars at uneven time intervals drawn evenly spaced              |
| Many series over time                                                                                       | Highlight the 1–3 that matter (rest grey), or small multiples with the other series as grey context                                           | One panel with more than about 5 colored lines (spaghetti)                       |
| A derived quantity (difference, net flow, cumulative total, ratio)                                          | Plot the derived quantity itself, optionally aligned under the components                                                                     | Two component series that the reader must subtract or integrate mentally         |
| Two measures over time                                                                                      | Two aligned panels sharing the x-axis, or both indexed to a common base on one axis                                                           | Dual y-axes                                                                      |
| One distribution                                                                                            | Histogram with a deliberately chosen bin width (§3), density, ECDF                                                                            | Default bins without checking                                                    |
| Compare distributions                                                                                       | Boxplot with raw points (small/moderate n), violin or raincloud (large n), ridgeline (many ordered groups), small multiples                   | Bare boxplots, bar-of-mean with error bars, more than about 4 overlaid densities |
| Relationship between two variables                                                                          | Scatter plot; hexbin or 2D density when points overlap heavily                                                                                | Static 3D scatter                                                                |
| Third variable on a scatter                                                                                 | Color or size (bubble chart)                                                                                                                  | 3D                                                                               |
| Entity × variable matrix                                                                                    | Heatmap with rows and columns reordered by similarity                                                                                         | Alphabetically ordered heatmap                                                   |
| Profiles across many variables                                                                              | Faceted bars, parallel coordinates, heatmap                                                                                                   | Radar/spider chart (tolerable only for 1–2 series on a shared, labeled scale)    |
| Overlaps among 4+ sets                                                                                      | UpSet plot                                                                                                                                    | Venn/Euler diagram (fine for 2–3 sets)                                           |
| Geographic pattern (clusters, gradients, neighbors)                                                         | Choropleth of a normalized rate, proportional symbols for totals, tile map for equal-weight regions                                           | A map when the point is a ranking (use sorted bars)                              |

Never use 3D effects (depth, perspective, extruded bars, tilted pies) in a static chart. They distort lengths and angles, hide marks behind others, and encode no data. Interactive 3D is occasionally useful for exploration, and surface plots are fine for truly spatial data like terrain.

## 2. Scales and axes: don't distort

**Start length and area encodings at zero.** Bars, columns, lollipops and area charts encode value as length from the baseline, so a non-zero baseline breaks the ratio. 99 vs 80 drawn from 50 looks like 49 vs 30. Line charts and dot plots encode position, so you may zoom them to the data range. Tufte: "in a time-series, use a baseline that shows the data, not the zero point." If small differences between large values are the story, switch to a dot plot or line, or plot the difference directly. Never shorten the bars.

- _Spot it:_ a bar chart whose lowest value tick isn't 0, or an axis break symbol; pixel-height ratios that don't match the labeled value ratios.

**Share the value axis across panels the reader will compare.** With independent ranges, each panel stretches to fill its frame, and a series 5× larger looks the same as a small one. Free scales are legitimate only when panels show different measures, or when only the shape within each panel matters. In that case, say so ("y-axes differ").

- _Spot it:_ facets or tiles of the same metric whose top tick labels differ.

**Avoid dual y-axes.** The designer can choose either axis range freely, so the apparent crossing, slope and correlation of the two lines are arbitrary. Readers trust the lines and rarely read two scales. Use two aligned panels, or index both series (e.g., to 100 at the start). Exception: a secondary axis that is a fixed conversion of the first (°C/°F, kWh/MWh, count/percent of a fixed total) has no free parameter and is fine.

**Put time on a proportional time axis.** Unevenly spaced dates drawn at even spacing compress long gaps, and that invents jumps and plateaus. Treat dates as dates, not as category labels. Time runs left to right.

**Make date axes calendar-aligned.** Place ticks on whole days, months, quarters or years, chosen for the span. Show the year on the first tick and at each year change. Ticks at odd dates (4 Feb, 20 Jun) make readers do calendar arithmetic.

**Choose the aspect ratio deliberately.** Panel shape changes perceived slope, and with it perceived correlation. Scatter plots default to roughly square, and to exactly 1:1 when both axes share a unit (predicted vs actual, before vs after), with a y = x reference line where useful. For line charts, bank the slopes of interest toward 45°: long time series usually want wide, short panels. Don't stretch a panel to make a relationship look stronger or weaker.

**Size by area, never by radius.** If radius is proportional to value, area grows with the square, and a 2× value looks 4× bigger. Scale area (radius ∝ √value), include a size legend or direct labels, and prefer length when size would be the main encoding. Draw the largest marks first so small ones stay visible on top.

**Draw every shape from the data.** Arc angles, bar lengths and areas must be computed from the plotted values, never hand-drawn or typed in. When a label and a shape disagree, readers believe the shape.

**Follow visual conventions.** Up means more, time runs left to right, the highlighted segment of a ring is the share the label talks about. An inverted y-axis (the infamous "gun deaths" chart) is read backwards by most readers. Domain conventions that readers already expect (rank 1 at the top, depth increasing downward) are fine.

## 3. Statistical honesty

**Show the data behind summaries.** A box, or a bar with an error bar, reduces a distribution to a few numbers. Unimodal, bimodal, outlier-driven and tiny samples can all look identical. When raw observations are available, plot them: jittered points for small or moderate n, violin or raincloud for large n. Always state each group's **n** (e.g., in the label "Group A, n = 20"). For weighted survey data like ResStock, state the unweighted sample count, not the weighted population _(ours)_.

**Label every error bar.** SD, SE and confidence intervals differ by factors that depend on n (SE = SD/√n), so an unlabeled error bar can't be interpreted. Say which one it is, and at what level (e.g., 95% CI). If you only have summary statistics, error bars are acceptable, as long as they are labeled.

**Check bin widths.** Histogram defaults (30 bins, Sturges) are arbitrary. Try coarser and finer widths in natural units, and look for spikes (heaping at round numbers), gaps and second modes. Report the width that shows the real structure, and mention a feature that only finer bins reveal. Density plots have the same problem with bandwidth.

**Check for Simpson's paradox before showing a pooled trend.** If the data come from distinct subpopulations (utilities, heating types, years), the pooled correlation can have the opposite sign from every within-group trend. Color or facet by the group and fit a trend per group. Whether the pooled or within-group view answers the question depends on the causal structure, so pick groupings with a substantive reason, not every available column.

**Pick windows and subsets for the question, not the conclusion.** A short window in a long noisy series can show the opposite of the long-run trend while every point is accurate. Show the longer history, with the period of interest highlighted, or state why the window starts where it does. The same applies to choosing favorable subgroups or metrics.

**Normalize counts on maps.** Raw counts mostly map where people live (xkcd 1138). Map a rate (per capita, per customer, per household, per km²) and name the denominator in the legend. If totals really matter, use proportional symbols, not filled regions. Rates for small populations are noisy, so flag or smooth them.

**Show missing data as missing.** Give NA its own neutral style (grey or hatching, outside the color ramp) and a "No data" legend entry. Never let missing values fall into the lowest color class, never fill them with zero, and never drop the region from the map. The same goes for line charts (break the line rather than interpolating across gaps) and bar charts (missing is not zero).

**Make labels agree with the plotted data.** Compute every label from the same data that draws the geometry. Part-to-whole charts must sum to 100% (allow about ±1 point for rounding, and footnote it). Multi-select survey data sums to more than 100%, so it belongs in a bar chart, never a pie. Recheck every number in titles and annotations against the plotted values. The source collection's own examples contain mismatched annotations, which shows how easily this happens.

## 4. Color

**Decide what color's job is before choosing colors.** Color should do exactly one of these jobs:

| Job                                                            | Palette                                                                                 | Rule                                                                 |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Nothing (categories are already on an axis)                    | One neutral color                                                                       | Never color each bar differently just for decoration                 |
| Highlight                                                      | One accent color, everything else grey                                                  | The highlight should be the thing the title talks about              |
| Identity of unordered groups                                   | Distinct hues of similar prominence (qualitative)                                       | At most about 6–7. Never use shades of one hue, which imply an order |
| Ordered or numeric values                                      | Sequential, light (low) to dark (high), perceptually uniform                            | Never use distinct hues or rainbow/jet for ordered values            |
| Deviation from a meaningful midpoint (0, average, target, 50%) | Diverging: two hues, light neutral (light grey) at the midpoint, centered exactly on it | Never use a diverging palette on data without a meaningful midpoint  |

**Use few colors.** More than about 7 hues can't be matched to a legend, and no story emerges. Highlight the groups that matter, grey the rest, group minor categories into "Other", or use small multiples.

**Keep colors consistent across charts.** When several charts show the same categories, each category keeps one color everywhere. Assign colors by name, not by position, so a chart that drops a category doesn't shift the others.

**Make colors work for colorblind readers.** About 1 in 12 men of Northern European ancestry have red-green color vision deficiency. Don't distinguish series by red vs green. Pair hues that also differ in lightness (blue/orange is the classic safe pair). Label directly so identification doesn't depend on color alone. _Test:_ view the chart in grayscale or through a colorblindness simulator; if two series merge, change one.

**Keep contrast high.** Marks must differ in lightness from the background. Text must be dark: annotations in a pale tint of the data color are hard to read. Aim for a contrast ratio of at least 4.5:1 for small text and 3:1 for large text and thin marks (WCAG). Deliberately de-emphasized context (grey lines, gridlines) can be lighter, but text the reader must read should not be.

**Avoid pure, saturated primaries** (`#FF0000`, `#00FF00`, `"red"`, `"green"`, tool defaults). They vibrate, differ wildly in perceived lightness, and compete for attention. Use a designed palette.

**Use a white or near-white background.** Never put data on a saturated mid-tone background. In dark mode, use dark grey or navy, not pure black.

## 5. Text, labels and annotation

**Make the title say something** (explanatory charts). State the finding ("Heat pump homes save $600 a year on the default rate"), not the variables ("Annual bill by heating type"). Move the measure and units to the subtitle. Highlight the data the title refers to, so the eye can verify the claim at once, and label the key values the claim depends on. The title must be literally true of the chart. Exploratory and reference charts may keep descriptive titles.

**Label directly instead of using a legend.** Put series names at line ends, in the series color, or as colored words in the subtitle. A legend forces the reader to shuttle back and forth and hold a color key in memory. Keep a legend for continuous color scales, for many series, or for one shared legend across many small multiples. Never show a legend for a single series.

**Keep labels off the data.** Place labels in empty space next to what they describe (line ends, bar ends, whitespace with a short leader line), never on top of lines or points. Extend the axis limits to make room. White labels inside solid dark bars are fine.

**Keep labels horizontal.** If category labels would need rotating, flip to a horizontal bar chart. Keep vertical orientation for time and for ordinal sequences (age bands, income bins). For crowded date axes, thin the ticks rather than rotating the labels.

**Label fewer ticks.** Label round intervals only (every 5, 10, year, decade), about 4–8 labels per axis, with optional short unlabeled minor ticks between them. Categorical axes still need every category labeled.

**Round numbers to the precision that matters**, usually whole numbers, or one decimal when the differences are small. Extra digits are noise and imply false precision. Use one unit throughout (don't put a 0–1 axis next to % labels). Keep enough precision that distinct values don't look tied.

**Annotate explanatory charts.** Add short notes at key features (peaks, policy changes, crossings), shade relevant periods, label endpoints, and write out computed gaps ("+$420"). Anything the narrative refers to should be marked on the chart. Annotate the few points that carry the message, not everything.

**Use at most two typefaces**, and build hierarchy with size, weight and color. The title is the largest text.

**Size text for the final display.** Readable text should be at least about 14 px on screen, or about 9–11 pt in print, at the size the chart actually appears. Design at the embed width rather than scaling a large figure down. If labels don't fit at a readable size, show fewer labels; don't shrink the type.

## 6. Layout, ordering and decluttering

**Sort bars by value** unless the categories have an inherent order: months, hours, ordinal bins, or a fixed category order shared across a report's charts. Put the largest at the top of a horizontal bar chart, and pin "Other" and "Unknown" at the end regardless of value.

**Reorder heatmaps.** Order rows and columns by similarity (clustering) or by a summary value so blocks of similar cells form. Normalize columns first if they are on different scales. Keep inherent orders (hour of day, month) as they are. Don't over-interpret clusters found in noise.

**Group what belongs together.** Bars within a group should nearly touch, with wider gaps between groups. Never plot a concatenated "group - subgroup" factor at even spacing. Keep title, subtitle and their lines tight together, with more space between the header block, the plot and the caption. A label should be closer to its own mark than to any other.

**Declutter.**

- _Always remove:_ 3D, shadows, gradients, decorative color, the full box around the plot.
- _Usually remove:_ minor gridlines, gridlines on the category axis, legends that labels can replace, redundant axes.
- _Keep:_ a few light gridlines on the value axis, plus a baseline or zero line for bars.

Don't double-encode: either keep the value axis with light gridlines, or label every bar and drop the axis, not both.

**Use one alignment edge.** Snap the title, subtitle, labels and source note to one shared left edge, and minimize the number of distinct alignment lines.

**Multi-chart layouts.**

- Separate distinct charts with visible gutters, and pad each chart so marks don't touch its edges. Tight facets sharing an axis are the exception.
- Keep colors consistent and share axes across charts the reader will compare.
- In interactive output, link hovers across charts that share an x-axis.
- Avoid overplotting: when points pile into a solid blob, use smaller and transparent markers, hexbin or 2D density, or facets with grey context. Each fix has a cost: transparency hides outliers, sampling drops rare points, and density depends on bandwidth.

## 7. In Switchbox reports _(ours)_

- **What the house theme already handles.** `theme_switchbox` (Python) sets two type families, a three-tier size hierarchy, a left-aligned title and subtitle, no plot box, horizontal gridlines only, and a white background. Don't fight it with per-plot font or grid overrides. The R theme (`lib/ggplot/switchbox_theme.R`) does less: all text is 12 pt Plex, there are ticks on both axes, and minor gridlines stay on, so R charts need the decluttering in §6 by hand.
- **The brand palette is qualitative.** Sky, carrot, midnight, saffron and pistachio are for identity and highlights. For ordered values, build a sequential ramp of one hue (for example, light-to-dark midnight or sky). For signed changes (bill increase vs decrease), use carrot vs sky with a light grey midpoint, as `bill_delta_direction_by_cooling_coverage` in `lib/rates_analysis/hh_summary_funcs.py` does. Don't copy `QUADRANT_COLORS` in `rate_case_funcs.py`: it uses red/green, which fails §4 for colorblind readers and in grayscale.
- **Measured palette limits** (WCAG contrast against white; color distances under simulated color vision deficiency):
  - **Carrot vs pistachio** nearly merge for red-green colorblind readers. Never use them as the only distinction between two series.
  - **Carrot vs saffron** are close for everyone.
  - **Sky, carrot and pistachio** have almost the same lightness (L\* ≈ 68–73), so they merge in grayscale. Pair any of them with midnight, or rely on direct labels.
  - **Sky vs carrot** is a safe pair, and **midnight** contrasts with everything.
  - **Saffron** (contrast 1.6:1) and **gray_light** (1.3:1) are too faint for text, thin lines or small points. Use them only for fills and backgrounds.
  - For text in brand colors, use **midnight_text** and **pistachio_text**, which pass 4.5:1.
- **Heating types and other recurring categories** keep a fixed order (`HEATING_ORDER` in `lib/rates_analysis/rate_case_funcs.py`). Keep their colors fixed across a report too, and reuse an existing color dict rather than inventing a new mapping per notebook.
- **ResStock charts.** State the unweighted sample count when you show weighted results by small subgroups, and beware of Simpson's paradox when pooling utilities or heating types.

## 8. Where the sources disagree, and the position we take

| Question                           | Card says                              | Article says                                          | We do                                                                                    |
| ---------------------------------- | -------------------------------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Cut the y-axis?                    | Never when comparing groups            | Never for bars; no consensus for lines                | Zero for length and area encodings. Lines and dots may zoom, with a clearly labeled axis |
| Pie charts?                        | Acceptable for very simple cases       | Must be avoided                                       | Bars by default; a pie only for 2–3 clearly unequal parts of one whole                   |
| Highlight one bar?                 | Yes, one accent and the rest grey      | Author is "not a big fan"                             | Highlight when the title is about that item; otherwise one neutral color                 |
| Keep bars when showing error bars? | Keeps bars and error bars, adds points | Replace with boxplot + jitter or violin               | Show the raw points; drop the bars when the data is a distribution                       |
| Remove tick marks?                 | "Remove the box" card drops ticks      | "Don't label every tick" card keeps short minor ticks | Ticks are optional; if kept, they are short, with labels only at round steps             |
| Declutter the axis?                | Keeps the y-axis with light grid       | Final example drops the axis and labels every bar     | Either one, never both                                                                   |
| Small-multiple y scales            | "Share the y-axis"                     | Stacking article uses free y                          | Shared when magnitudes are compared; free only when stated                               |
| Aspect ratio                       | Square for scatter plots               | Wide for line charts (banking to 45°)                 | Both, by chart type                                                                      |
| Circular barplots                  | Use with care                          | "A good alternative" under conditions                 | Only for many bars with a cyclic or decorative purpose; never for precise comparison     |
| 3D                                 | Stick to 2D                            | Interactive scatter "perhaps", surfaces "why not"     | Never in static output                                                                   |

## 9. Review checklist (run on the rendered image)

Render the chart at its final size, look at the image, and answer each question. Fix every "no" or justify it in the chart's caption or in your report to the user.

**Message**

- [ ] Can I state the takeaway in one sentence, and does the chart type fit that task (§1)?
- [ ] Does the chart type fit the data's shape: one value vs several per group, ordered x, nesting, additivity, n (`dataviz_chart_selection.md` §1)?
- [ ] (Explanatory) Does the title state the finding, is it literally true of the plotted data, and is the supporting data highlighted?

**Honesty**

- [ ] Do bars and areas start at zero, and are compared panels on a shared axis (or labeled as differing)?
- [ ] No dual axes, 3D, radius-scaled bubbles, inverted axes, or evenly spaced uneven dates?
- [ ] Do shapes match their labels, do parts sum to 100%, and do title and annotation numbers match the data?
- [ ] Are sample sizes stated, raw data shown where a summary could hide it, and error bars labeled (SD/SE/CI)?
- [ ] Are counts on maps normalized, missing data shown as missing, and the time window justified?
- [ ] For pooled trends across subpopulations: did I check within-group trends?

**Color**

- [ ] Does color have exactly one job, with the right palette type for it (§4)?
- [ ] At most about 7 hues, consistent with the other charts in the same document?
- [ ] Still distinguishable in grayscale, and with no red/green-only distinctions?
- [ ] Is all text dark enough to read against its background?

**Text and layout**

- [ ] Direct labels instead of a legend where possible, with no labels sitting on the data?
- [ ] Horizontal labels, round tick intervals, numbers rounded sensibly, one unit throughout?
- [ ] All text readable at the final display size?
- [ ] Bars sorted (or in their natural order), heatmap rows and columns ordered meaningfully?
- [ ] No box, no heavy or minor gridlines, no redundant axis-plus-labels?
- [ ] No overplotted blobs, and small marks drawn on top of large ones?

## Source cards and articles

Each rule above traces to one or more of these:

- [All cards](https://www.data-to-viz.com/caveats.html)
- Articles:
  [cut y-axis](https://www.data-to-viz.com/caveat/cut_y_axis.html),
  [boxplot](https://www.data-to-viz.com/caveat/boxplot.html),
  [error bars](https://www.data-to-viz.com/caveat/error_bar.html),
  [dual axis](https://www.data-to-viz.com/caveat/dual_axis.html) (a stub; see [PolitiFact's example](http://www.politifact.com/truth-o-meter/statements/2015/oct/01/jason-chaffetz/chart-shown-planned-parenthood-hearing-misleading-/)),
  [3D](https://www.data-to-viz.com/caveat/3d.html),
  [counterintuitive](https://www.data-to-viz.com/caveat/counter_intuitive.html),
  [Simpson](https://www.data-to-viz.com/caveat/simpson.html),
  [pie](https://www.data-to-viz.com/caveat/pie.html),
  [radial bars](https://www.data-to-viz.com/caveat/circular_barplot_accordeon.html),
  [circular barplot](https://www.data-to-viz.com/caveat/circular_bar_yaxis.html),
  [color](https://www.data-to-viz.com/caveat/color_com_nothing.html),
  [declutter](https://www.data-to-viz.com/caveat/declutter.html),
  [horizontal labels](https://www.data-to-viz.com/caveat/hard_label.html),
  [annotation](https://www.data-to-viz.com/caveat/annotation.html),
  [consistency](https://www.data-to-viz.com/caveat/consistency.html),
  [order](https://www.data-to-viz.com/caveat/order_data.html),
  [bin size](https://www.data-to-viz.com/caveat/bin_size.html),
  [radius or area](https://www.data-to-viz.com/caveat/radius_or_area.html),
  [spaghetti](https://www.data-to-viz.com/caveat/spaghetti.html),
  [connect the dots](https://www.data-to-viz.com/caveat/connect_your_dot.html),
  [stacking](https://www.data-to-viz.com/caveat/stacking.html),
  [aspect ratio](https://www.data-to-viz.com/caveat/aspect_ratio.html),
  [overplotting](https://www.data-to-viz.com/caveat/overplotting.html),
  [heatmap](https://www.data-to-viz.com/graph/heatmap.html),
  [area](https://www.data-to-viz.com/caveat/area_hard.html),
  [calculation errors](https://www.data-to-viz.com/caveat/calculation_error.html),
  [grouped bars](https://www.data-to-viz.com/caveat/grouped_bar.html),
  [mental arithmetic](https://www.data-to-viz.com/caveat/mental_calculation.html),
  [multiple distributions](https://www.data-to-viz.com/caveat/multi_distribution.html),
  [radar](https://www.data-to-viz.com/caveat/spider.html)
- External:
  [Datawrapper on color](https://blog.datawrapper.de/colors/),
  [xkcd 1138](https://xkcd.com/1138/),
  [Cotgreave on wrapped bars and moiré](https://web.archive.org/web/20181226161528/http://gravyanecdote.com/uncategorized/wrappedbarsthoughts/)
