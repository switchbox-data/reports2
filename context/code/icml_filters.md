# ICML export filters

Quarto/Pandoc's ICML writer has two gaps that our custom Lua filters fix:

1. **FloatRefTarget nodes** (figures, tables with cross-references) produce warnings and empty output.
2. **Complex LaTeX math** (fractions, underbraces, summations) is dumped as raw TeX text instead of rendered equations.

Both filters live in `lib/quarto_extensions/` and activate only for `FORMAT == "icml"` — they are no-ops for HTML and DOCX.

## Filters

### `icml_floats/icml_floats.lua`

Registers a custom `FloatRefTarget` renderer for ICML output. Without it, Quarto emits "Output format icml does not currently support FloatRefTarget nodes" for every figure and table.

- **Timing**: `at: pre-quarto` (must register the renderer before Quarto processes the AST).
- **Mechanism**: Accesses `_G._quarto.ast.add_renderer` (user filters run in a sandboxed env that doesn't expose `_quarto` directly). Decorates captions with cross-reference prefixes (e.g., "Figure 1:") and emits `Para(Image)` for image floats or `Div(content, caption)` for other floats.

### `icml_math/icml_math.lua`

Pre-renders every `Math` node (both inline `$...$` and display `$$...$$`) to SVG using `latex` + `dvisvgm`, then replaces the Math node with an `Image` element. Pandoc's ICML writer never sees the math, so there are no "Could not convert TeX math" warnings and equations appear as correctly typeset SVG images in InDesign.

- **Timing**: Default (runs during Pandoc's filter phase, after Quarto).
- **Prerequisites**: `latex` and `dvisvgm` on PATH (from TinyTeX), `ghostscript` (system package for dvisvgm's PostScript processing).
- **Caching**: Hash-based. Each unique expression is rendered once and cached in `cache/icml_math/`. Subsequent renders reuse the cache (~1s for 74 equations vs ~18s cold).
- **Output**: SVGs are placed in `math/` relative to CWD during rendering (so Pandoc can resolve dimensions), then `just typeset` copies them to `docs/math/` alongside the ICML.

## Prerequisites

### TinyTeX

Both the devcontainer Dockerfile and EC2 `user-data.sh` install TinyTeX + required packages:

```bash
quarto install tinytex --no-prompt
tlmgr install dvisvgm standalone mathtools amsfonts
```

On EC2, TinyTeX is installed to `/opt/TinyTeX/` with symlinks in `/usr/local/bin/` for multi-user access. In the devcontainer (root user), it's at `/root/.TinyTeX/`.

### Ghostscript

Required by `dvisvgm` for PostScript special processing (standalone class bounding box). Installed via apt: `ghostscript`.

## How `just typeset` works

The typeset pipeline is implemented in `lib/just/typeset.py` and invoked via `just typeset` from any report directory. It:

1. Runs `quarto render <file> --to icml --output <stem>_YYYYMMDD.icml`.
2. During rendering, Quarto runs both Lua filters from `_quarto.yml`:
   - `icml_floats.lua` handles FloatRefTarget nodes (figures, tables).
   - `icml_math.lua` renders each Math node to SVG in `math/`, replacing with Image.
3. Moves `math/*.svg` to `docs/math/` and removes the temp `math/` directory.
4. Runs `icml_sidenotes` to convert footnotes to anchored margin notes if the ICML contains footnotes.

The designer receives `docs/<stem>_YYYYMMDD.icml` + `docs/math/` directory.

The module also supports typesetting non-`index.qmd` files (e.g. `just typeset expert_testimony.qmd`), generating a filename from the source stem.

## Adding to a new report

In `_quarto.yml`:

```yaml
filters:
  - at: pre-quarto
    path: ../../lib/quarto_extensions/icml_floats/icml_floats.lua
  - path: ../../lib/quarto_extensions/icml_math/icml_math.lua
```

In `Justfile`:

```just
typeset path_qmd="":
    uv run python -m lib.just.typeset {{ path_qmd }}
```

## Troubleshooting

- **"latex not found"**: Install TinyTeX with `quarto install tinytex --no-prompt`, then `~/.TinyTeX/bin/*/tlmgr install dvisvgm standalone mathtools amsfonts`.
- **"dvisvgm not found"**: Run `tlmgr install dvisvgm`.
- **"PostScript specials ignored"**: Install ghostscript (`apt install ghostscript`). Without it, SVGs render but bounding boxes may be slightly off.
- **LaTeX compilation fails for a specific expression**: Check the TeX packages. If math uses a symbol not in `amsmath`/`amssymb`/`mathtools`, install the needed package via `tlmgr install <package>`.
- **Cache stale after editing math**: Delete `cache/icml_math/` to force re-render.
