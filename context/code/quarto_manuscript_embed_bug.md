# Quarto Manuscript `{{< embed >}}` bug with non-image outputs

## The bug

Quarto's Manuscript project type uses `{{< embed >}}` shortcodes to pull labeled outputs from analysis notebooks into `index.qmd`. This works for plotnine/ggplot2 figures (which produce `image/png` or `image/svg+xml` MIME outputs) but **fails for two known output types**:

1. **Great Tables (GT)** — Python's `GT()` objects produce `text/html` MIME output.
2. **Matplotlib figures** — Raw `matplotlib.figure.Figure` objects (not via plotnine).

### GT failure mode

Quarto's manuscript mode truncates `text/html` MIME outputs from Python cells to just `\n\n</div>`. This rogue `</div>` gets injected into `index.html`, prematurely closes a parent container, and cascades — breaking the page structure and pushing all subsequent content into or after the appendix.

### Matplotlib failure mode

Embedding a cell that **displays** a raw matplotlib `Figure` (e.g. the cell ends with `fig` or `plt.show()` so Jupyter emits the figure repr) causes a Lua filter crash during rendering:

```
Error running filter /Applications/quarto/share/filters/main.lua:
Block, list of Blocks, or compatible element expected, got table
        while retrieving function argument content
        while retrieving arguments for function Div
stack traceback:
        /Applications/quarto/share/filters/main.lua:22960: in field 'render'
        ...
```

This happens because matplotlib cells produce multiple MIME outputs (e.g., `text/plain` for the repr string + `image/svg+xml` or `image/png` for the figure). The embed filter expects a single block-level element but gets a table of mixed outputs.

Plotnine figures work because plotnine's `ggplot` object has a clean `_repr_svg_()` / `_repr_png_()` that Jupyter renders as a single image output, without an accompanying `text/plain` repr.

## The workaround

### Matplotlib: single-SVG output (preferred for `{{< embed >}}`)

Use **`lib.quarto.display_svg`** so the cell has **one** primary `image/svg+xml` output. This helper saves the figure as SVG, closes it, and displays it via `IPython.display.SVG`:

```python
from lib.quarto import display_svg

fig = my_plot.draw()  # or plt.subplots(...)
# ... any matplotlib post-processing ...
display_svg(fig)
```

This replaces the older inline three-liner (`savefig` / `plt.close` / `display(SVG(...))`) that was previously copy-pasted into each cell.

Give the cell `#| label: fig-my-chart` and `#| fig-cap: "..."`, then use `{{< embed notebooks/analysis.qmd#fig-my-chart >}}` in `index.qmd`. `just render` still runs `inline_svgs.py` on the built HTML.

### Great Tables and other HTML

For GT and similar, use **file-based inclusion** — save the output to `cache/` in the analysis notebook, then reference the file directly in `index.qmd`.

### GT tables

In `analysis.qmd`:

```python
from pathlib import Path
Path("../cache").mkdir(exist_ok=True)

_my_gt = GT(df).fmt_currency(...)
Path("../cache/my_table.html").write_text(_my_gt.as_raw_html())
_my_gt  # still display in notebook for preview
```

In `index.qmd`:

````markdown
:::{.column-page-inset-right}

```{r}
#| echo: false
htmltools::includeHTML("cache/my_table.html")
```

:::
````

### Matplotlib figures (fallback: static file + markdown image)

If you cannot use `display_svg` (e.g. a one-off script), save under `cache/` and use a markdown image in `index.qmd`; `inline_svgs.py` will still inline `.svg` assets when you run `just render`.

## Will switching away from Manuscripts fix this?

Possibly. The bug is in the Manuscript project type's embed filter (`main.lua`), which processes `{{< embed >}}` shortcodes. If we move to a non-Manuscript project type (e.g., a standard Quarto website or book), we would no longer use `{{< embed >}}` at all — notebooks would either be rendered inline or their outputs consumed via a different mechanism.

Key questions for the migration:

- Does the replacement approach handle multi-MIME notebook cell outputs gracefully?
- Does it preserve the analysis-narrative separation (keeping heavy computation out of `index.qmd`)?
- Do GT `text/html` outputs render correctly in the alternative project type?

Until the migration happens, use **`display_svg(fig)` + `{{< embed >}}`** for matplotlib charts where possible, and file-based workarounds for GT and other HTML.

## Affected reports

- `ny_hp_rates`: TOU rate table (GT) still uses file-based HTML; TOU schedule matplotlib charts and the bill-decomposition bar chart use `display_svg` + `{{< embed >}}`.
- `ri_hp_rates`: bill-decomposition bar chart and feeder/transformer peak analysis charts use `display_svg` + `{{< embed >}}`; optional TOU matplotlib cells exist behind `INCLUDE_TOU` for parity with NY (not embedded in `index.qmd` today).
