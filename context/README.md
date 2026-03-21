# Context index

Reference docs, bug reports, and working notes for agents. **When you add or remove a file under `context/`, update this index.**

See **AGENTS.md → Reference context** for conventions. Top-level dirs: **tools/** (Quarto/plotting/tooling knowledge and known bugs).

## domain/

Documents that answer **"How does this work in the real world?"** — policy explainers, program guides, regulatory and institutional background. Subdirs group by theme.

| File                                               | Use when working on …                                                                                                                                                                |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| rie_distribution_planning_and_thermal_screening.md | RIE feeder/transformer capacity analysis: how the annual thermal screening works (normal rating + N-1 contingency load at risk), what triggers an area study, and what happens next. |

## methods/

Documents that answer **"How do we justify and operationalize this?"** — conceptual framing, formulas, literature, design choices that feed our methodology writeup. Will be implemented in code.

| File                                    | Use when working on …                                                                                |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| ny_hp_rates_story_building_selection.md | Choosing or changing the "story building" profiled across the NY HP rates report's narrative charts. |

## code/

Documents that answer **"How does this tool work? What are its pitfalls and work arounds? How do I run this?"** — rendering pipelines, sizing mechanics, known Quarto bugs, and report-specific design decisions.

| File                            | Use when working on …                                                                                                                                           |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| quarto_manuscript_embed_bug.md  | Embedding GT tables or matplotlib figures in `index.qmd` via `{{< embed >}}`. Documents the Lua filter crash and `text/html` truncation bugs, with workarounds. |
| plotnine_sizing_in_quarto.md    | Plotnine figure sizing, font consistency, or SVG rendering pipeline. Explains the full chain from `figure_size` to browser pixels.                              |
| illustrator_svg_infographics.md | Illustrator SVGs (`infographic_*.svg`): CSS class scoping (color collisions), font-family names, nested `<tspan>` WebKit bug, white background rect.            |

## sources/

Primary sources like academic articles and documents, mostly extracted from PDFs via the **extract-pdf-to-markdown** slash command.

| File                                       | Use when working on …                                                                                                                                                                          |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| rie_2024_peak_forecast_2025-2039.md        | Rhode Island Energy's 15-year electric peak (MW) forecast (2025–2039). Peak demand projections, key uncertainty scenarios (EE, PV, EV, DR, ES, heat pumps), weather assumptions.               |
| rie_distribution_planning_guide.md         | Rhode Island Energy distribution planning criteria: N-1 contingency limits, equipment ratings (Normal/LTE/STE), load at risk thresholds, feeder/transformer/sub-tx planning.                   |
| rie_distribution_planning_study_process.md | Rhode Island Energy integrated planning study process: milestones (scoping → sanctioning), annual planning screening, study team composition, report template, DER/EV/HE forecast integration. |
