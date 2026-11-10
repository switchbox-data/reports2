# Choosing a chart from the data

How to go from a dataset to the right chart type, and why each chart fits the situations it fits. The companion `dataviz_design_guide.md` covers how to draw a chart honestly once you've picked it (axes, color, labels, the review checklist). This guide covers which chart to pick. Both are tool-agnostic.

**How to use it.** Profile the data (§1), recognize its shape (§2), read the candidates and the reasoning for that shape (§3), then look up the chosen chart in the catalog (§4) for when not to use it. If you can inspect the data, run the §1 checks rather than guessing from column names. If you can't, ask the user the §1 questions whose answers would change the choice.

**Source.** Distilled from Yan Holtz's [From Data to Viz](https://www.data-to-viz.com/) (MIT license, [source repo](https://github.com/holtzy/data_to_viz)): its decision tree, its 35 chart pages and its 19 worked "story" pages, which take one real dataset through several charts and show what each one reveals or hides. Where the site lists charts that the design guide restricts, or contradicts itself, §5 records the position we take. Items marked _(ours)_ are our additions.

**The principle.** The data's shape narrows the field to a handful of feasible charts. The reader's question, and properties of the data like sample size, number of groups, and whether values add up to a whole, pick among them. The site's advice is to "identify and try all feasible chart types" and keep the one that best suits both the data and the point. For exploratory work, try two or three. For an explanatory chart, write the message first (design guide §0), then pick the candidate whose most accurately read encoding (position, then length) carries that message.

## 1. Profile the data first

Each check below changes which chart is right. Run them on the actual data. A column's name or dtype is not its role: a numeric column with four distinct values is a category, and a string column of dates is a time axis.

| Check                                                                                              | Why it matters                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Role of each column**: numeric value, category, ordered (time, sequence, ordinal), geography, ID | Decides the family in §2. Ordered columns become the x-axis; IDs become labels, not data                                                                                                                                      |
| **Distinct values** of each numeric column                                                         | A numeric column with few distinct values (codes, flags, counts 1–5) is a category; color or facet by it. Low distinct-to-row ratio in a continuous measure means heaping at round values, which bin width can hide or reveal |
| **Rows per entity or group**                                                                       | One row per level means you're showing an amount (bars, lollipops). Several rows per level means you're showing a distribution (boxplots, violins, ridgelines). This is the single most common wrong turn                     |
| **Total rows** and duplicate (x, y) pairs                                                          | Above about 2,000 points, scatter plots overplot into blobs; switch to hexbin, 2D histogram or density. Heavy duplication overplots at any n                                                                                  |
| **Rows per group, minimum and spread**                                                             | Below roughly 20–30 per group, violins and densities invent shape: use boxplots with the raw points, and print n. Very unequal group sizes must be shown                                                                      |
| **Number of levels** of each category                                                              | Decides color vs axis vs facet. More than about 7 needs highlighting, an "Other" group, or small multiples. Overlaid densities stop working above about 4 groups; ridgelines suit many                                        |
| **Crossed or nested** categories                                                                   | Crossed (every utility × every heating type) leads to grouped bars, heatmaps, lines. Nested (each child has exactly one parent) leads to treemaps and grouped-sorted bars                                                     |
| **Additivity**: do the values sum to a meaningful whole?                                           | Gate for every part-to-whole chart: stacked bars and areas, treemaps, pies, waffles. Rates, averages, medians and percentages of different bases don't add, so they get bars, dots or lines                                   |
| **Shared units and scale** across numeric columns                                                  | Same units allow one shared axis (boxplots side by side). Different units need separate panels, standardizing, or indexing to a base                                                                                          |
| **Range and skew** (max vs 99th percentile, max/min ratio)                                         | Heavy right skew suggests a log axis (for position encodings only, never for bars) or truncating with a note. A few giants next to many near-zero values make area charts and circular bars unreadable                        |
| **Regular, complete grid**: is every combination present, at even spacing?                         | A complete regular x × y grid suits a heatmap (or a surface). Missing combinations break dodged bars, stacked areas and lines; decide whether to filter or show gaps. Irregular time steps need a true time axis              |
| **Sign and midpoint**                                                                              | Values that cross a meaningful zero (bill changes) need a diverging palette or a reference line, and rule out area-based encodings like bubble size                                                                           |
| **Weights** _(ours)_                                                                               | ResStock and survey data carry sample weights. Histograms, shares and summaries must be weighted; state the unweighted n for small subgroups (design guide §3)                                                                |
| **Missing values and catch-alls**                                                                  | NA, "Other" and "Unknown" need their own treatment, not a rank among real categories (design guide §3, §6)                                                                                                                    |

In polars, most of these are one line each (the tool-agnostic checks above are what matter; this is just a shortcut):

```python
df.schema                                                    # roles start here, but verify them
df.select(pl.all().n_unique())                               # distinct values per column
df.group_by(group_cols).len().describe()                     # rows per group: one, or several?
df.group_by(child).agg(pl.col(parent).n_unique().alias("k")).filter(pl.col("k") > 1).height == 0  # nested?
df.select(pl.struct(a, b).n_unique()).item() == df[a].n_unique() * df[b].n_unique()            # complete grid?
```

## 2. Recognize the data's shape

Most datasets fall into one of these shapes (the site counts about 20; some are merged here). Find yours, then go to the matching part of §3.

| Shape                                                                       | How to recognize it                                                     | §3   |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ---- |
| One numeric variable                                                        | One measure, no grouping or order that matters                          | 3.1  |
| Two numeric variables, not ordered                                          | Two measures per entity, neither is an index                            | 3.2  |
| One series over an ordered x                                                | One measure against time or a sequence, one value per step              | 3.3  |
| Several series over an ordered x                                            | As above, plus a category (long format) or several value columns (wide) | 3.4  |
| Three numeric variables                                                     | Three measures per entity, or a value on a regular x × y grid           | 3.5  |
| Several numeric variables                                                   | Many measures per entity (four or more)                                 | 3.6  |
| One category, one value per level                                           | Category column is unique; one number per level                         | 3.7  |
| One category, several values per level                                      | Category repeats; many observations per level                           | 3.8  |
| Two crossed categories, one value per cell                                  | Every combination possible, one row per combination                     | 3.9  |
| Two crossed categories, several values per cell                             | As above, but many rows per combination                                 | 3.10 |
| Nested categories with a value                                              | Each child has exactly one parent (region > utility > rate class)       | 3.11 |
| Independent lists or sets                                                   | Items belonging to several lists; question is overlap                   | 3.12 |
| Relationships: adjacency matrix, edge list, flows                           | Pairs of entities with a link, maybe a weight and a direction           | 3.13 |
| Hierarchy plus extra links                                                  | A tree, and separate links between its leaves                           | 3.13 |
| Points, points with a value, regions with a value, origin–destination pairs | Lat/lon columns, or a region ID that joins to boundaries                | 3.14 |

## 3. Candidates by shape, and how to choose among them

Each subsection gives the candidates (the first listed is our usual default for explanatory charts), the questions that pick among them, and why. Story links point to the site's worked example.

### 3.1 One numeric variable: what does the distribution look like?

**Candidates:** histogram, density, ECDF _(ours)_, strip or dot plot for small n _(ours)_. Story: [OneNum](https://www.data-to-viz.com/story/OneNum.html).

- **Histogram** by default. Its y-axis is a count the reader can quote ("about 500 homes"), and fine bins show discreteness honestly.
- **Density** when the message is the overall shape, or when you will overlay a few groups. Its y-axis is abstract, it implies continuity, and it can spill past natural bounds (negative kWh).
- **ECDF** when the reader needs percentiles or shares ("what fraction of homes save money?"). It has no bin width to choose. _(ours)_
- With small n (under about 50–100), histograms and densities are unstable; show the points.

**Why bin width is a decision, not a default.** In the story, Airbnb prices look like a smooth skewed curve at 10-euro bins; finer bins reveal spikes at round prices. Compare a coarse and a fine view before choosing, and say what the spikes mean. With heaped or discrete data, a smooth density at a large bandwidth is the most misleading option because it invents a shape that isn't there.

**Interrogate:** distinct-to-row ratio (heaping), max vs 99th percentile (truncate with a note, or log axis), whether there is a hidden grouping column (if so, this is §3.8) or an ordering column (§3.3).

### 3.2 Two numeric variables, not ordered: how are they related?

**Candidates:** scatter; hexbin or 2D histogram; 2D density; scatter with marginal distributions; binned boxplots _(ours, from the site's tree)_. Story: [TwoNum](https://www.data-to-viz.com/story/TwoNum.html).

- **Scatter** first, for "are they related?". Add a trend line only if it says something, and know that a loess or linear fit can be bent by a couple of outliers (the story shows two points dragging a loess curve down).
- **Above about 2,000 points**, or with many duplicate pairs, the scatter becomes a blob. **Hexbin or 2D histogram** keep both the dense core and the outliers, and their color is a count. **2D density** shows modes in the core best (the story finds two hidden peaks) but silently drops sparse regions and outliers.
- **Binned boxplots**: for very large n, bin x into classes (deciles, size bands) and show y's distribution per class. This reads more precisely than color intensity. _(inference)_
- **Marginal distributions** when the reader also needs each variable's own shape.

**Interrogate:** n and duplicates; whether either column is really an index (then §3.3); outliers beyond the 99th percentile on either axis (label them, or note that a density hides them); skew (log axes); a third variable or group (then §3.5, or color by group and check for Simpson's paradox, design guide §3).

### 3.3 One series over an ordered x: how does it change?

**Candidates:** line, area, connected scatter, bar or lollipop for few discrete periods; for time series, also boxplots or violins per period (seasonality). Story: [TwoNumOrdered](https://www.data-to-viz.com/story/TwoNumOrdered.html).

- **Line** for many points. The slope carries the change, and position can be zoomed to the data range.
- **Connected scatter** (line plus markers) for few points (under about 20–50), so the reader sees which values are observed and which are interpolated. Also when steps are irregular.
- **Area** only when the baseline is a meaningful zero and the magnitude matters. The fill implies "amount from zero", so never cut the axis of an area chart.
- **Bars** for a few discrete periods whose totals the reader compares (monthly bills). Bars say "separate amounts"; lines say "a continuous process".
- **Distribution per period** (boxplot per month, ridgeline per season) when the question is the spread within each period rather than the level.
- If the range spans orders of magnitude and the question is relative change, use a log axis or plot percent change. A linear axis over a 100× range hides the early moves.

**Interrogate:** is x truly an order with one value per step (duplicates mean §3.2); how many points; regular spacing; is zero meaningful; is there a threshold in the question (draw it as a reference line or threshold fill).

### 3.4 Several series over an ordered x: how do groups evolve?

**Candidates:** line chart, highlighted line chart, small multiples, stacked area, percent stacked area, heatmap (group × time), streamgraph (interactive only). Story: [OneCatSevOrderedNum](https://www.data-to-viz.com/story/OneCatSevOrderedNum.html).

The number of groups and whether their sum means something decide this:

- **2–5 groups:** overlaid lines, labeled directly.
- **More than about 5, or one group the story is about:** highlight the 1–3 that matter and grey the rest, or use small multiples with the other series as grey context. One panel of many colored lines is spaghetti.
- **Dozens to hundreds of groups:** a heatmap of group × time (rows ordered by a summary or clustering) shows patterns across all of them. _(ours)_ The site suggests PCA or clustering to find groups of similar trajectories.
- **Stacked area** only when the total is the message and the groups are additive parts of it, and **percent stacked** when shares are. Every band except the bottom one sits on a moving baseline, so readers can't track a middle group; streamgraphs make this worse (no band has a flat baseline).
- **Small multiples:** a shared y-axis for comparing magnitudes; free y-axes for comparing shapes and timing, stated in the caption. Free axes make every peak look equally tall.

**Interrogate:** number of groups; is the sum meaningful; do magnitudes differ by orders of magnitude (a stacked chart is then dominated by the largest group); are time steps shared across groups; do missing group-periods mean zero or unknown.

### 3.5 Three numeric variables

**Candidates:** bubble chart, scatter with color, heatmap or contour for a regular grid, small multiples of scatters. Story: [ThreeNum](https://www.data-to-viz.com/story/ThreeNum.html).

- **Bubble chart:** readers judge size far less precisely than position, so the encodings rank the variables. Put the relationship you want read on x and y, and give size to a non-negative amount (population, total customers) that is the least related to the others. Size by area, never radius.
- **Color for the third variable** when it can be negative or has a midpoint (bill change), since negative sizes are meaningless.
- **Regular x × y grid** (hour × day of year, temperature × size): check `rows == distinct x × distinct y`. Then use a heatmap; a 3D surface is the one case the site accepts 3D, and we still prefer the heatmap for static output.
- Thousands of bubbles overlap; facet or switch to color.

### 3.6 Several numeric variables per entity

**Candidates:** per-variable distributions (boxplots, violins or ridgelines on a shared axis, or faceted histograms), scatterplot matrix (correlogram), correlation heatmap, clustered heatmap with a dendrogram, PCA, parallel coordinates. Story: [SeveralNum](https://www.data-to-viz.com/story/SeveralNum.html).

First decide whether the question is about the **variables** or about the **entities**:

- **Variables: how is each distributed?** One shared axis only if they share units; otherwise faceted histograms with free scales.
- **Variables: how do they relate?** A scatterplot matrix for 3 to about 8–10 variables; beyond that, a correlation heatmap (k variables means k² panels).
- **Entities: which are similar?** Hierarchical clustering shown as a dendrogram, with a heatmap of the standardized values to explain why entities cluster. Standardize first when units differ, or the clustering just sorts by the largest-unit column (the story's dendrogram does exactly that).
- **Entities: profiles across variables.** Parallel coordinates (scaled axes, ordered to reduce crossings, one group highlighted), or faceted bars for few entities. Not radar charts (§5).
- **Summarize many variables in two dimensions:** PCA, labeled with what the components mean.

**Interrogate:** number of numeric columns; shared units; numeric columns that are really codes; rows (decides whether entity labels are readable); an ID column; a category to color by.

### 3.7 One category, one value per level: amounts and rankings

**Candidates:** sorted bar, sorted lollipop, dot plot; for parts of a whole: share bars, single 100% stacked bar, treemap, waffle, and (rarely) pie. Story: [OneNumOneCat](https://www.data-to-viz.com/story/OneNumOneCat.html).

- **Sorted bar or lollipop** by default: length or position on a common baseline answers "who is biggest, and by how much?". Sort by value unless the levels have a natural order (months, income bins, a report-wide fixed order). Go horizontal when labels are long or numerous.
- **Lollipop over bar** when there are many levels or the values are close together, where a wall of bars is heavy and differences vanish. **Dot plot** when zero isn't meaningful and small differences matter (bars must start at zero; dots may zoom).
- **Part of a whole** only if the values are additive parts of a meaningful total. Sorted bars of shares still read best. A treemap gives an overview of how the whole divides but weak comparisons. A pie or waffle only for 2–3 clearly unequal parts (§5).
- **Extreme skew** (two giants and a long tail near zero) degrades every chart here: split top N from "the rest", label values directly, or use a log axis on a dot plot.

**Interrogate:** is the category column unique (if not, §3.8); number of levels; natural order; how different the values are; do they sum to a whole; catch-all rows.

### 3.8 One category, several values per level: comparing distributions

**Candidates:** boxplot with raw points, violin, ridgeline, overlaid densities, small-multiple histograms, raincloud _(ours)_. Story: [OneNumOneCatSeveralObs](https://www.data-to-viz.com/story/OneNumOneCatSeveralObs.html).

Rows per group and the number of groups decide this:

- **Small groups (under about 20–30 rows):** boxplot plus jittered points, or just the points. A violin or density at that size invents shape. Print n.
- **Large groups, up to about 7:** violin or raincloud shows the shape a box hides (bimodality, heaping).
- **About 4 or fewer groups that don't overlap much:** overlaid densities.
- **Many groups (10 or more) with enough rows each:** ridgeline, sorted by median. The story's 17-group example works only as a ridgeline.
- **Shape of each group matters more than comparison:** small multiples with a shared x-axis (free y-axes stated).
- **Bounded or heaped data** (integer percentages, round bills): histograms are more honest than densities.

Never show a bar of the mean with an error bar when you have the observations (design guide §3). Sort groups by median unless they have a natural order.

### 3.9 Two crossed categories, one value per cell

**Candidates:** grouped bars, heatmap, dumbbell or slope chart, scatter of one level against the other, line or parallel plot when one category is ordered, small multiples, stacked bars (only if additive). Story: [OneNumSevCatSubgroupOneObsPerGroup](https://www.data-to-viz.com/story/OneNumSevCatSubgroupOneObsPerGroup.html).

- **Grouped bars:** put the category with fewer levels inside each group (as fill), at most about 7, and the many-level category on the axis. The outer grouping decides which comparison is easy: grouping by utility makes "compare rates within a utility" easy; grouping by rate makes "rank utilities within a rate" easy. Choose for the message.
- **One category has exactly two levels** (before/after, two years, two scenarios): a dumbbell or slope chart shows the difference and the ranking for every entity. A scatter of level 1 against level 2, with a y = x line, scales to many more entities.
- **One category is ordered** (years, months): lines or a parallel plot show each entity's trajectory. Grouped bars are for unordered categories.
- **Many levels on both axes:** a heatmap, with rows and columns ordered meaningfully.
- **Stacked bars** only if the values sum to a meaningful total across the inner category, and then the total is what reads well; inner segments don't.

**Interrogate:** crossed or nested (nested is §3.11); exactly one row per cell (several is §3.10); levels of each category; is one ordered or two-level; is the grid complete; is there an aggregate row (an average shown as a peer) that should be a reference line instead.

### 3.10 Two crossed categories, several values per cell

**Candidates:** grouped boxplots with points and n, grouped violins (large cells only), small-multiple grid of histograms. Story: [OneNumSevCatSubgroupSevObsPerGroup](https://www.data-to-viz.com/story/OneNumSevCatSubgroupSevObsPerGroup.html).

Check the smallest cell first. The story's "women tip more on Fridays" rests on 9 and 10 observations, which a box drawn without points or n hides completely. Put the comparison that matters adjacent (inner), fix any ordinal order explicitly, and facet by a third category rather than adding more colors. Never clip outliers with axis limits that also drop them from the box statistics; zoom the view instead.

### 3.11 Nested categories with a value

**Candidates:** bars or lollipops sorted within groups (colored or faceted by parent), treemap, circle packing, sunburst (interactive), dendrogram (structure only). Story: [SevCatOneNumNestedOneObsPerGroup](https://www.data-to-viz.com/story/SevCatOneNumNestedOneObsPerGroup.html).

- First check that each child has exactly one parent and that leaf values add up to parent totals. Area-based hierarchy charts are only valid if they do.
- **"How is the whole divided?"** Treemap: space-efficient, shows which top-level groups dominate and which branches drive them, weak for exact comparison. Circle packing shows the grouping more clearly but wastes space and compares worse.
- **"Which leaf is biggest?"** Sorted bars or lollipops of the leaves, with the hierarchy reintroduced by color, faceting, or sorting by group then value. This is the better default for explanatory charts.
- **Several values per leaf:** boxplots or violins per leaf, grouped by parent.
- Non-additive leaf values (rates, averages) rule out treemaps and sunbursts.

### 3.12 Independent lists or sets: what overlaps?

**Candidates:** Venn or Euler diagram (2–3 sets), UpSet plot (more sets, or when intersection sizes must be compared), pairwise overlap heatmap; sorted lollipop for frequencies within a list. Story: [SeveralIndepLists](https://www.data-to-viz.com/story/SeveralIndepLists.html).

When list sizes differ a lot, raw intersection counts mostly reflect list size; normalize (share of each list, Jaccard index) before comparing. Standard Venn regions aren't area-proportional; print counts in each region. Clean the items first: the story's top "words" include scraping junk, which the lollipop exposed.

### 3.13 Relationships, flows and hierarchies with links

**Candidates:** heatmap of the matrix, Sankey, chord, network graph, arc diagram, dendrogram, hierarchical edge bundling. Stories: [AdjacencyMatrix](https://www.data-to-viz.com/story/AdjacencyMatrix.html) (the site's NestedValueForLinks and NestedValueForConnection pages are broken copies of another story; this section uses their chart pages).

- **Is the matrix symmetric?** No means directed flows: Sankey (origins left, destinations right) or a directed chord. Yes means undirected: Sankey's left/right split is meaningless.
- **Weighted or 0/1?** Chord diagrams need weights. Weighted networks with variable edge widths clutter; prefer a heatmap or Sankey.
- **How many nodes, how dense?** About 10 dense, weighted nodes: chord or Sankey. About 100 sparse nodes: network (for structure: components, hubs, bridges) or arc (when labels must be readable). Many dense nodes: heatmap, which scales as N² cells no matter how many edges and makes a dominant diagonal (within-node flows) obvious.
- **Flows that split or merge through stages and are conserved** (inflow equals outflow at each node): Sankey, so widths add up visually. Drop weak links and order nodes to cut crossings. If flows aren't conserved, label totals.
- **Hierarchy only:** dendrogram for structure; §3.11 charts if leaves carry values. A node with several parents rules out a dendrogram; use a Sankey.
- **Hierarchy plus many leaf-to-leaf links:** edge bundling shows which branches talk to which, at the cost of tracing any single link. For lookups, use a heatmap of leaves ordered by the hierarchy.
- Circular, arc and heatmap layouts all depend on node order; order by community or clustering.

### 3.14 Maps

**Candidates:** dot map, dot density, hexbin or 2D histogram of points, bubble map, choropleth, tile (hexbin) map of regions, cartogram, connection map; and often no map at all. Stories: [GPSCoordWithoutValue](https://www.data-to-viz.com/story/GPSCoordWithoutValue.html), [GPSCoordWithValue](https://www.data-to-viz.com/story/GPSCoordWithValue.html), [MapConnection](https://www.data-to-viz.com/story/MapConnection.html) (the site's RegionWithValue page is a broken copy; this section uses its chart pages).

First ask whether geography is the message (clusters, gradients, neighbors). If the point is a ranking of regions, use sorted bars; a map makes ranking hard.

- **Points without a value:** few points, plain dots (interactive if each has details); thousands, dot density with small transparent dots; heavy overlap, bin into hexagons or squares with a log color scale and readable breaks. Zoom to the region of interest so bins mean something.
- **Points with a value:** a bubble map, area proportional to a non-negative total, small bubbles drawn on top, capped size range. Rates and signed values go to color, not size.
- **Regions with a value:** a choropleth, but only for a normalized rate (per customer, per capita) and regions of broadly similar size. The eye integrates area times color, so large rural regions dominate. With very unequal regions (utility territories, US states), use a labeled tile map, a cartogram, or a choropleth paired with a sorted bar chart. For totals, bubbles at centroids.
- **Origin–destination pairs:** great circles split at the dateline, identical pairs grouped into counts, high-volume routes drawn on top. If the message is how much flows rather than where, aggregate to regions and use a chord, Sankey or origin × destination heatmap.

**Interrogate:** do you have boundaries keyed to your IDs; total or rate; how unequal region areas and populations are; how many points and how much they overlap; how skewed the values are (classed vs continuous palette); whether the audience will recognize distorted shapes.

## 4. Chart catalog: when, why and when not

Each entry gives what carries the value (which decides how accurately it's read), when the chart is the right choice, and when it isn't, with the alternative. Links go to the site's chart page.

**Distributions**

- [**Histogram**](https://www.data-to-viz.com/graph/histogram.html) (bar height = count per bin). Use for one numeric variable's distribution, or a few groups as small multiples. Not with untested default bins, unequal bins, or more than about 3 overlaid groups (use ridgeline or small multiples). Not to be confused with a bar chart, which has one bar per category.
- [**Density**](https://www.data-to-viz.com/graph/density.html) (curve height, smoothed). Use for shape with many points; overlay up to about 3–4 groups. Not with small n, heaped or bounded data (use a histogram), and never trust one bandwidth.
- **ECDF** _(ours)_ (position: cumulative share). Use when the reader needs percentiles or "share of homes below X", or to compare a few groups without binning. Less intuitive for lay readers; annotate the key share.
- **Boxplot** ([caveat](https://www.data-to-viz.com/caveat/boxplot.html); position of median and quartiles). Use for quick median and spread comparison across many groups. It hides n and multimodality: add jittered points for small groups, use a violin or raincloud for large ones, and show n.
- [**Violin**](https://www.data-to-viz.com/graph/violin.html) (width = density). Use for large samples per group and few-to-moderate groups. Not for small samples (boxplot with points). Order by median and show n.
- [**Ridgeline**](https://www.data-to-viz.com/graph/ridgeline.html) (stacked densities). Use for many groups (about 6 or more) with a clear pattern across them, especially ordered groups. Not for few groups or groups without a pattern (violin or boxplot). Overlap hides the tops of some curves.

**Relationships between numeric variables**

- [**Scatter**](https://www.data-to-viz.com/graph/scatter.html) (position on both axes). Use for the relationship between two unordered numerics. Above about 2,000 points, switch to hexbin, 2D density or marginal plots. Color subgroups to check Simpson's paradox.
- [**2D density, hexbin, 2D histogram**](https://www.data-to-viz.com/graph/density2d.html) (color = count). Use when a scatter overplots. Not for small samples (scatter). Hexbins keep outliers; smooth 2D density drops them. Check bin size or bandwidth.
- [**Bubble**](https://www.data-to-viz.com/graph/bubble.html) (position plus area). Use for three numerics when the x–y relationship is the message. Not when size is the main variable (area is read poorly); size by area; draw small bubbles on top.
- [**Connected scatter**](https://www.data-to-viz.com/graph/connectedscatter.html) (position, joined in order). Use for an ordered series with few points, or two series with different units over time (instead of a dual axis: plot one against the other, labeled by date). Label dates and add direction cues when the path doubles back.
- [**Correlogram**](https://www.data-to-viz.com/graph/correlogram.html) (scatterplot matrix). Use for a first look at all pairs of 3 to about 10 numeric variables. Beyond that, a correlation heatmap.
- [**Parallel coordinates**](https://www.data-to-viz.com/graph/parallel.html) (position on parallel axes). Use for many entities across several scaled numerics, to find groups and trade-offs. Too many lines: highlight one group. Reorder axes to cut crossings; scale each axis.
- **PCA** (position on component axes). Use to summarize many numerics in two dimensions, or to cluster trajectories. Standardize first; label what the components mean; readers need an explanation.

**Amounts and rankings**

- [**Bar**](https://www.data-to-viz.com/graph/barplot.html) (length from zero). Use for one value per category, sorted. Not with several observations per group (boxplot or violin). Never cut the axis.
- [**Lollipop**](https://www.data-to-viz.com/graph/lollipop.html) (position of the dot, line to zero). Use like a bar, especially with many levels or close values. Unsorted, a bar reads better; not for distributions.
- **Dot plot** _(ours)_ (position only). Use when zero isn't meaningful and small differences between large values matter; may zoom.
- **Dumbbell and slope chart** _(ours)_ (two positions per entity). Use when two values per entity (before/after, two scenarios) and the difference is the story. Not for more than two points per entity (lines).
- **Grouped and stacked bars** (length; stacked segments sit on moving baselines). Grouped for one value per combination of two categories, with few bars per group. Stacked only when the total matters; only the bottom segment and the total read accurately.
- [**Circular barplot**](https://www.data-to-viz.com/graph/circularbarplot.html) (length on a radial axis). Only for many bars (about 40 or more) with an obvious pattern, or decoration. Not for precise comparison; outer bars look bigger.

**Parts of a whole**

- **Pie** ([caveat](https://www.data-to-viz.com/caveat/pie.html); angle and area) and [**donut**](https://www.data-to-viz.com/graph/donut.html) (arc length). Only for 2–3 clearly unequal parts of one whole, annotated directly. Never several side by side, never 3D. Default to sorted bars of shares.
- **Waffle** (count of cells). For a countable share of a few categories ("3 in 10 homes"). Not for many categories or precise comparison. The site gives no guidance; this is ours.
- [**Treemap**](https://www.data-to-viz.com/graph/treemap.html) (area). Use for how a whole divides across a hierarchy of up to about 3 levels. Not for precise comparison (bars).
- [**Circle packing**](https://www.data-to-viz.com/graph/circularpacking.html) (area, nesting). Use to show how groups nest. Wastes space and compares worse than a treemap.
- [**Sunburst**](https://www.data-to-viz.com/graph/sunburst.html) (angle by ring). Interactive only, for hierarchies or sequences. Angles are hard to read and outer rings look bigger; treemap for static output.

**Over time**

- [**Line**](https://www.data-to-viz.com/graph/line.html) (position and slope). Use for the trend of a few series over an ordered x. Many series: highlight or small multiples. Never a dual axis. Irregular steps need a true time axis and markers.
- [**Area**](https://www.data-to-viz.com/graph/area.html) (filled length from zero). Use for one series when magnitude from zero matters. Never with a cut axis; not for many overlapping series.
- [**Stacked area**](https://www.data-to-viz.com/graph/stackedarea.html) (band thickness on a moving baseline). Use for the evolution of an additive total and the composition of it. Not for tracking one group's trend (lines or small multiples).
- [**Streamgraph**](https://www.data-to-viz.com/graph/streamgraph.html) (band thickness, no baseline). Only interactive "who dominates when" views with strongly shifting shares. Otherwise stacked area, lines or small multiples.
- [**Heatmap**](https://www.data-to-viz.com/graph/heatmap.html) (color). Use for an overview of a matrix: entities × features, adjacency, or regular time patterns like hour × day. Normalize, and order rows and columns by clustering or a summary (keep natural orders like hours). Not for reading exact values unless numbers are printed in the cells.

**Relationships and flows**

- [**Sankey**](https://www.data-to-viz.com/graph/sankey.html) (band width). Use for weighted flows between stages or from sources to uses. Drop weak links; order nodes to cut crossings.
- [**Chord**](https://www.data-to-viz.com/graph/chord.html) (ribbon width around a circle). Use for weighted flows among a few entities. Not for bipartite data (Sankey) or many links (heatmap); needs explanation for lay readers.
- [**Network**](https://www.data-to-viz.com/graph/network.html) (node-link layout). Use for structure (clusters, hubs, bridges) of unweighted, sparse relations. Avoid hairballs; weighted directed flows go to Sankey or chord. The layout algorithm changes what the reader sees.
- [**Arc diagram**](https://www.data-to-viz.com/graph/arc.html) (nodes on a line). Use when every node label must be readable. Needs a good node order; for overall structure, a network.
- [**Dendrogram**](https://www.data-to-viz.com/graph/dendrogram.html) (tree). Use for an explicit hierarchy or clustering results, with a heatmap. State the distance and linkage; horizontal for long labels.
- [**Edge bundling**](https://www.data-to-viz.com/graph/edge_bundling.html) (bundled links over a hierarchy). Use for a hierarchy plus many leaf-to-leaf links, when the pattern between branches matters more than any single link.
- [**Venn**](https://www.data-to-viz.com/graph/venn.html) (overlapping regions). 2–3 sets, with counts in each region. More sets: UpSet plot.

**Maps**

- [**Choropleth**](https://www.data-to-viz.com/graph/choropleth.html) (color per region). Use for one normalized value per region with boundaries. Not for raw counts or very unequal regions (tile map, cartogram, bubble map).
- [**Bubble map**](https://www.data-to-viz.com/graph/bubblemap.html) (area at a location). Use for totals at points or region centroids. Size by area; transparency and a size legend.
- [**Hexbin map**](https://www.data-to-viz.com/graph/hexbinmap.html) (equal tiles, or binned points). Use for equal-weight regions or many points. Label tiles; readers lose geographic landmarks.
- [**Cartogram**](https://www.data-to-viz.com/graph/cartogram.html) (region size = weight). Use to correct or show the region-size bias of a choropleth. Only if the audience recognizes the distorted shapes, ideally with the real map alongside.
- [**Connection map**](https://www.data-to-viz.com/story/MapConnection.html) (great-circle lines). Use when where the routes go matters. Aggregate identical pairs; for how much flows, a chord, Sankey or heatmap.

## 5. Where we depart from the site

The site's tree lists every chart that can technically draw a shape, including several that the design guide restricts. When a leaf offers one of these, skip it unless its narrow condition holds:

| Chart                 | Site lists it for                   | We use it only when                                                                              |
| --------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------ |
| Pie, donut            | One category with values            | 2–3 clearly unequal parts of one whole (design guide §8)                                         |
| Word cloud            | One category with values; lists     | Never for data; word length and area distort. Sorted lollipop instead                            |
| Spider or radar       | Two crossed categories              | 1–2 series on a shared, labeled scale. Otherwise faceted bars, dumbbell, or parallel coordinates |
| 3D scatter or surface | Three numerics                      | Never static. Heatmap or contour for grids, color or size for scatters                           |
| Circular barplot      | Variation of bar charts             | Many bars with a cyclic or decorative purpose, never for precise comparison                      |
| Streamgraph, sunburst | Several ordered series; hierarchies | Interactive output only                                                                          |
| Waffle                | One category with values            | A countable share of a few categories                                                            |

The site's thresholds (about 2,000 points, about 4 overlaid densities, about 7 colors, about 6 groups for ridgelines) are rules of thumb, and some pages contradict each other (the violin page says ridgelines suit "a few groups"; the ridgeline page says many). Treat thresholds as prompts to check the rendered chart, not as cutoffs.

## 6. Shapes that recur in Switchbox data _(ours)_

- **Per-building results** (bills, bill changes, BAT values) are one numeric with several observations per group (heating type, utility, income band), with sample weights. Use weighted histograms or ECDFs for one group, weighted boxplots or violins by group (§3.8), and bars of shares for "what fraction save money". The shared helpers in `lib/rates_analysis/rate_case_funcs.py` cover several of these (`plot_weighted_bill_change_hist`, `plot_weighted_hist_by_group`, `plot_ratedesign_cdf`, `plot_bill_change_quadrants`).
- **Bill changes** are signed with a meaningful zero: diverging color centered at zero, or a zero reference line. Not bubble sizes.
- **Hourly 8760 series** (loads, marginal costs) form a complete regular grid of day × hour: a heatmap shows seasonal and daily structure at once (`plot_mc_heatmap`). Use lines for an average day or a peak week, and boxplots by month for spread.
- **Monthly bill components** (delivery, supply, fixed) are additive, so stacked bars of one building or a median household are valid; the total and the bottom segment read accurately.
- **Rate scenarios × heating types** are two crossed categories (§3.9). With two scenarios (default vs reform), a dumbbell or slope chart beats paired bars. With more, decide which comparison the outer group should make easy.
- **Utility territories** vary enormously in area. Choropleths of utility-level rates overweight large rural utilities; pair them with sorted bars, or skip the map when the point is a ranking.
