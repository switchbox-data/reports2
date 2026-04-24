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

### Matplotlib: `display_figure` (preferred for `{{< embed >}}`)

Use **`lib.quarto.display_figure`** (or its alias **`display_svg`**) so the cell has **one** primary image output. The helper is format-aware:

- **HTML** (`just render`): emits `image/svg+xml` — sharp at any zoom, inlined by post-processing.
- **DOCX** (`just draft`): emits `image/png` at 300 DPI — avoids the fuzzy rasterization that happens when Pandoc converts SVG via `rsvg-convert` at 96 DPI.
- **ICML** (`just typeset`): emits `image/svg+xml` — InDesign places SVG natively at full fidelity, and the project-level `fig-format: svg` keeps raw Quarto figures SVG too. GT tables also get SVG for ICML (see `display_gt` below).

Format detection: figures rasterize on `SWITCHBOX_GT_AS_IMAGE=1` only (set by `just draft`); GT tables rasterize to PNG on `SWITCHBOX_GT_AS_IMAGE=1`, render as vector SVG on `SWITCHBOX_TYPESET=1` (set by `just typeset`), and otherwise base64-encode as HTML.

```python
from lib.quarto import display_figure  # or display_svg (alias)

fig = my_plot.draw()  # or plt.subplots(...)
# ... any matplotlib post-processing ...
display_figure(fig)
```

This replaces the older inline three-liner (`savefig` / `plt.close` / `display(SVG(...))`) that was previously copy-pasted into each cell.

Give the cell `#| label: fig-my-chart` and `#| fig-cap: "..."`, then use `{{< embed notebooks/analysis.qmd#fig-my-chart >}}` in `index.qmd`. `just render` still runs `inline_svgs.py` on the built HTML.

### Great Tables: `display_gt` (preferred for `{{< embed >}}`)

Use **`lib.quarto.display_gt`** so the cell has a single output whose GT markup survives Pandoc's `--to ipynb` round-trip. The output format is chosen by environment:

- **HTML** (`just render`): base64-encodes the GT HTML inside a `<div>` + `<script>`; JavaScript decodes and injects the markup at page load. Pandoc cannot parse opaque base64, so the full table survives. No iframe — the table participates in the host page's CSS cascade (Switchbox fonts, colors).
- **DOCX** (`just draft`, `SWITCHBOX_GT_AS_IMAGE=1`): emits a high-res PNG screenshot (GT's headless-Chrome `save()` at 3× scale). GT's HTML + web fonts don't survive Pandoc's DOCX writer reliably.
- **ICML** (`just typeset`, `SWITCHBOX_TYPESET=1`): emits a vector SVG with real `<text>` / `<tspan>` elements. Pipeline: GT HTML → headless Chrome via Selenium → `Page.printToPDF` (CDP) produces a vector PDF → `inkscape --export-plain-svg` (native importer, **not** `--pdf-poppler`, which outlines text) produces an editable-text SVG → `IPython.display.SVG`. Quarto writes the SVG to `icml/index_files/figure-icml/<label>-output-N.svg` and Pandoc's ICML writer emits a `<Link LinkResourceURI="file:...">`. Requires `inkscape` on `PATH` (provisioned by `rate-design-platform/infra/user-data.sh` and `reports2/.devcontainer/Dockerfile`).

```python
from lib.quarto import display_gt

my_table = GT(df).fmt_currency(...)
display_gt(my_table)
```

Give the cell `#| label: tbl-my-table` and `#| tbl-cap: "..."`, then use `{{< embed notebooks/analysis.qmd#tbl-my-table >}}` in `index.qmd`. Captions, cross-references, and column classes all work normally.

#### Why this works

Pandoc's `--to ipynb` parses raw `text/html` cell outputs and only retains the outermost closing tag (`</div>`). By encoding the GT HTML as a base64 string inside a `<script>`, the markup is opaque to Pandoc's HTML parser — the `<div>` and `<script>` elements are simple enough to survive, and the encoded payload passes through as an attribute value.

#### Legacy workaround: file-based inclusion

The older pattern — saving to `cache/` and including via `htmltools::includeHTML()` — still works but has drawbacks: no Quarto cross-referencing, no `tbl-cap` captions, requires R in Python reports, and the `cache/` file must be kept in sync manually. Prefer `display_gt` for new tables.

### Matplotlib figures (fallback: static file + markdown image)

If you cannot use `display_figure` (e.g. a one-off script), save under `cache/` and use a markdown image in `index.qmd`; `inline_svgs.py` will still inline `.svg` assets when you run `just render`.

## Affected reports

- `ny_hp_rates`: TOU rate table (GT) and BAT summary tables use `display_gt` + `{{< embed >}}`; TOU schedule matplotlib charts and the bill-decomposition bar chart use `display_figure` + `{{< embed >}}`.
- `ri_hp_rates`: bill-decomposition bar chart and feeder/transformer peak analysis charts use `display_figure` + `{{< embed >}}`; optional TOU matplotlib cells exist behind `INCLUDE_TOU` for parity with NY (not embedded in `index.qmd` today).
