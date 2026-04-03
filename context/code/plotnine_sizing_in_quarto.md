# How plotnine figure sizing works in Quarto

This document explains the rendering pipeline from plotnine code to what you see in the browser, why text sometimes appears tiny, and how to size figures correctly.

## The rendering pipeline

```
plotnine code                     Quarto                          Browser
─────────────                     ──────                          ───────
figure_size=(W, H) inches    →    Saves PNG at W×DPI × H×DPI  →  <img class="img-fluid">
font_size=12 pt (absolute)        pixels                          max-width: 100%
theme(dpi=300 from Quarto)        No width/height on <img>        Scales to container width
```

### Step 1: plotnine creates a figure in inches

`figure_size=(W, H)` in `theme()` sets the figure dimensions in **inches** (via matplotlib's `figure.set_size_inches()`). Font sizes in plotnine — whether from `element_text(size=12)` or `geom_text(size=9)` — are in **typographic points** (1 pt = 1/72 inch). These are absolute physical sizes within the figure's inch space: 12pt text is always 12/72 = 0.167 inches tall, regardless of figure size or DPI.

If no `figure_size` is set in the plotnine code, matplotlib's default is used. Quarto sets this default via its Python kernel setup (`/Applications/quarto/share/jupyter/lang/python/setup.py`):

```python
plt.rcParams['figure.figsize'] = (fig_width, fig_height)
plt.rcParams['figure.dpi'] = fig_dpi
plt.rcParams['savefig.dpi'] = "figure"
```

For HTML output with no `fig-width`/`fig-height` in `_quarto.yml`, the defaults are (7, 5) inches. `fig-dpi` comes from YAML (300 in ny_hp_rates).

### Step 2: Quarto saves the figure as a PNG

When a plotnine cell executes, the figure is saved as a PNG at the configured DPI. The pixel dimensions are:

```
pixel_width  = figure_width_inches × DPI
pixel_height = figure_height_inches × DPI
```

With `fig-dpi: 300` and `figure_size=(14, 6)`, the PNG is **4200 × 1800 pixels**.

Quarto's `fig-dpi` is set via `plt.rcParams['figure.dpi']`, which plotnine picks up. plotnine's own default DPI (100) is overridden by Quarto's setup.

Note: plotnine's default Jupyter display mode is `"retina"` (which doubles DPI), but Quarto's setup calls `set_matplotlib_formats("png")`, which overrides this. So in Quarto, DPI is exactly what `fig-dpi` says — no doubling.

### Step 3: the browser scales the image to fit the container

Quarto embeds the PNG as:

```html
<img src="..." class="img-fluid figure-img column-page-inset-right">
```

There is **no `width` or `height` attribute**. The `img-fluid` class (from Bootstrap) applies `max-width: 100%; height: auto;`, which means the image fills the container width and scales proportionally.

The container width is set by the Quarto column class:

| Class                      | Approximate width | Source                               |
| -------------------------- | ----------------- | ------------------------------------ |
| `.column-body`             | 750px             | `$grid-body-width` in switchbox.scss |
| `.column-page-inset-right` | ~1050px           | body + right margin                  |
| `.column-page-inset`       | ~1050px           | body + both margins (roughly)        |
| `.column-margin`           | ~300px            | right margin only                    |

Since the PNG pixel width (e.g. 4200px) is always larger than the container width (e.g. 1050px), the image is always **scaled down**. Everything in the image — bars, axes, text, annotations — scales by the same factor.

## The key equation (DPI cancels out)

The apparent size of text on screen is:

```
apparent_px = (font_pt / 72) × container_px / figure_width_inches
```

**DPI does not appear.** Higher DPI produces a larger PNG, but `img-fluid` scales it back to the container width, so the net effect on element size is zero. DPI only controls **image crispness** (sharpness of edges, readability when zooming in).

What matters is the **ratio of container width to figure width in inches**. Think of this as the "effective screen DPI":

```
effective_dpi = container_px / figure_width_inches
```

For 12pt text to appear at a comfortable ~17px on screen, you need `effective_dpi ≈ 100`.

## Worked examples

### Example: 12pt text at different figure widths in a 1050px container

| `figure_size` width | Effective DPI | 12pt text appears as | Verdict |
| ------------------- | ------------- | -------------------- | ------- |
| 7"                  | 150           | 25px                 | Large   |
| 10"                 | 105           | 17.5px               | Good    |
| 14"                 | 75            | 12.5px               | Small   |
| 17.5"               | 60            | 10px                 | Tiny    |

### Example: same chart in different containers

A chart with `figure_size=(10, 5)` and 12pt base text:

| Container                  | Width  | Effective DPI | 12pt text | Verdict |
| -------------------------- | ------ | ------------- | --------- | ------- |
| `.column-body`             | 750px  | 75            | 12.5px    | Small   |
| `.column-page-inset-right` | 1050px | 105           | 17.5px    | Good    |

This illustrates why the same chart can look fine in one container and have tiny text in another. The fix is to match `figure_size` to the container the chart will be displayed in.

## The correct mental model

**`figure_size` is the "design width" of your chart — it controls how large elements appear on screen.** It does NOT mean "make the chart bigger on the page." The page width is fixed by the CSS column class. Making `figure_size` wider just makes everything proportionally smaller.

Think of it this way: `figure_size` defines a canvas in inches. Plotnine lays out all elements at their point sizes within that canvas. The browser then squeezes (or stretches) that canvas to fit the container. If the canvas is much wider than the container's effective inches (container_px / 100), everything shrinks.

**Font sizes in points are absolute within the figure's inch space**, not relative to display. 12pt is always 0.167 inches in the figure. But if the figure is squeezed from 17.5 inches to a 1050px container (effective 60 DPI), those 0.167 inches become 10 pixels.

**DPI only controls crispness.** 300 DPI gives sharp text at any zoom level. 100 DPI gives slightly blurry text on retina screens. Neither changes the apparent size of anything on screen.

## How to size figures correctly

### Rule of thumb

Set `figure_width_inches` so that `container_px / figure_width_inches ≈ 100`:

- For `.column-body` (750px): **figure width ≈ 7–8"**
- For `.column-page-inset-right` (~1050px): **figure width ≈ 10–11"**

### When the aspect ratio demands a wider figure

If a chart genuinely needs more horizontal space (e.g. a multi-bar stacked chart or a wide faceted plot), you have two options:

1. **Increase font sizes proportionally.** If `figure_size=(17.5, ...)` in a 1050px container gives effective DPI of 60, you need fonts at `12 × (100/60) ≈ 20pt` to compensate.

2. **Reduce figure width and accept a different aspect ratio.** Most charts look fine at 10" wide — the aspect ratio change is often an improvement.

### What NOT to do

- Don't set `figure_size=(17, 4)` thinking it will make the chart banner-shaped on the page. It will be banner-shaped, but all text will be microscopic.
- Don't change DPI to fix sizing. DPI only affects crispness, not element size.
- Don't rely on Quarto's `fig-width`/`fig-height` YAML options for per-cell sizing — they are ignored for Jupyter cells. You must set size in the plotnine code itself via `theme(figure_size=(...))`.

## How to keep font size constant on screen while changing other things

The key equation is `apparent_px = (font_pt / 72) × container_px / figure_width_inches`. To hold `apparent_px` fixed, you need to compensate whenever you change one of the other variables.

### Scenario: changing the container class (e.g. `.column-body` → `.column-page-inset-right`)

You're widening the container from ~750px to ~1050px. The image stretches to fill the new container, so everything gets ~40% bigger — including text. To keep text the same size on screen, **widen `figure_size` by the same factor**:

```
new_figure_width = old_figure_width × (new_container_px / old_container_px)
```

Example: a chart at `figure_size=(7, 4)` in `.column-body` (750px) shows 12pt text at ~17.5px. Moving it to `.column-page-inset-right` (~1050px) without changes would show that text at ~25px. To keep it at ~17.5px, set `figure_size=(10, ...)` because `7 × (1050/750) ≈ 10`.

### Scenario: changing `figure_size` width (e.g. to fit more content horizontally)

You're widening the canvas from 10" to 14". The container stays the same, so everything shrinks by `10/14 ≈ 71%`. To keep text the same size on screen, **increase font sizes by the inverse factor**:

```
new_font_pt = old_font_pt × (new_figure_width / old_figure_width)
```

Example: at `figure_size=(10, 5)` in a 1050px container, 12pt text appears at ~17.5px. Widening to `figure_size=(14, 5)` shrinks it to ~12.5px. To restore ~17.5px, set `base_size` and `geom_text` sizes to `12 × (14/10) ≈ 17pt`.

In plotnine, override the base size on the theme:

```python
+ theme_switchbox(base_size=17)
+ theme(figure_size=(14, 5))
```

And scale `geom_text(size=...)` by the same factor.

### Scenario: changing `figure_size` height only

Height changes do **not** affect apparent text size. The browser scales the image based on width (the height follows proportionally). So you can freely adjust height to change the aspect ratio without worrying about text size.

### Scenario: changing DPI

DPI changes do **not** affect apparent text size. The PNG gets more or fewer pixels, but `img-fluid` scales it to the same container width regardless. Change DPI freely for crispness without worrying about text size.

### Scenario: changing `geom_text(size=...)` for a single annotation

`geom_text(size=...)` is in points, just like theme text. It follows the same equation. If you want an annotation to appear at the same screen size as 12pt theme text, set it to 12. If you want it smaller, set it lower. The ratio between `geom_text` size and `element_text` size is preserved through the scaling pipeline — whatever ratio you set in points is the ratio you'll see on screen.

### Quick reference table

| I want to...                     | What to change                                                      | What to hold constant             |
| -------------------------------- | ------------------------------------------------------------------- | --------------------------------- |
| Move chart to wider container    | Increase `figure_size` width proportionally                         | Font sizes in code                |
| Move chart to narrower container | Decrease `figure_size` width proportionally                         | Font sizes in code                |
| Fit more data horizontally       | Increase `figure_size` width AND increase font sizes by same factor | Container class                   |
| Make chart taller/shorter        | Change `figure_size` height                                         | Everything else (text unaffected) |
| Make chart crisper               | Increase DPI                                                        | Everything else (text unaffected) |
| Make one label bigger/smaller    | Change that label's `size=` in points                               | Everything else                   |

## Quarto configuration that affects this

### `_quarto.yml` settings

```yaml
format:
  html:
    fig-dpi: 300     # Controls PNG resolution (crispness), not display size
    fig-format: png  # Output format; also disables plotnine's retina doubling
```

`fig-width` and `fig-height` at the YAML level set defaults for charts that don't specify their own size. These are applied via `plt.rcParams['figure.figsize']` at kernel startup, so they're overridden by any explicit `theme(figure_size=...)` in plotnine code.

### Per-cell options

Quarto's `#| fig-width:` and `#| fig-height:` cell options **do not work for Jupyter/Python cells** — they only work for Knitr (R). For Python, always set size in code:

```python
+ theme(figure_size=(10, 5))
```

### Column classes in `index.qmd`

The column class on the embed determines the container width:

```markdown
:::{.column-page-inset-right}
{{< embed notebooks/analysis.qmd#fig-my-chart >}}
:::
```

If you move a chart from `.column-page-inset-right` (~1050px) to `.column-body` (~750px), text will shrink by ~30% unless you also reduce `figure_size` to match.

## Manuscript mode

The manuscript project type (`type: manuscript`) does **not** affect any of this. The figure sizing pipeline — DPI, PNG embedding, CSS scaling — is identical for manuscript and non-manuscript projects. The only manuscript-specific issue is the HTML truncation bug with `text/html` outputs (see the Quarto issue filed at quarto-dev/quarto-cli#14176), which affects GT tables, not plotnine figures.

## Source references

These findings come from reading the actual source code:

- **plotnine `figure_size`**: `plotnine/themes/themeable.py` — calls `figure.set_size_inches()`, units are inches
- **plotnine font sizes**: passed to matplotlib `Text` objects, units are points (1/72 inch)
- **plotnine DPI**: `plotnine/options.py` default is 100; theme's `dpi` sets `rcParams["figure.dpi"]`
- **plotnine Jupyter display**: `plotnine/ggplot.py` `_repr_mimebundle_` — defaults to "retina" (2× DPI PNG), but Quarto overrides to plain "png"
- **Quarto Python kernel setup**: `/Applications/quarto/share/jupyter/lang/python/setup.py` — sets `figure.figsize`, `figure.dpi`, `savefig.dpi`, and `set_matplotlib_formats()`
- **Quarto HTML embedding**: `<img class="img-fluid">` with no width/height attributes
- **Switchbox theme**: `reports/.style/switchbox.scss` — `$grid-body-width: 750px`
