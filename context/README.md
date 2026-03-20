# Context index

Reference docs, bug reports, and working notes for agents. **When you add or remove a file under `context/`, update this index.**

See **AGENTS.md → Reference context** for conventions. Top-level dirs: **tools/** (Quarto/plotting/tooling knowledge and known bugs).

## tools/

Documents that answer **"How does this tool work, and what are its pitfalls?"** — rendering pipelines, sizing mechanics, known Quarto bugs, and report-specific design decisions.

| File                                    | Use when working on …                                                                                                                                           |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| quarto_manuscript_embed_bug.md          | Embedding GT tables or matplotlib figures in `index.qmd` via `{{< embed >}}`. Documents the Lua filter crash and `text/html` truncation bugs, with workarounds. |
| plotnine_sizing_in_quarto.md            | Plotnine figure sizing, font consistency, or SVG rendering pipeline. Explains the full chain from `figure_size` to browser pixels.                              |
| ny_hp_rates_story_building_selection.md | Choosing or changing the "story building" profiled across the NY HP rates report's narrative charts.                                                            |
| illustrator_svg_infographics.md         | Illustrator SVGs (`infographic_*.svg`): CSS class scoping (color collisions), font-family names, nested `<tspan>` WebKit bug, white background rect.            |
