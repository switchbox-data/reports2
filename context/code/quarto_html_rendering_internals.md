# Quarto HTML rendering internals

How Quarto turns `.qmd` files into HTML, what caches it uses, and how the behavior
differs between project renders and single-file renders (and between manuscript
projects and other project types). Based on reading the Quarto 1.9.36 source
(`quarto.js`) and empirical testing.

## The rendering pipeline

Rendering a `.qmd` file with Python code cells is a two-stage process: **execute**
(run the code) then **pandoc** (convert to HTML). Understanding this split is key
to understanding everything else in this document.

```
┌─────────────┐       ┌────────────────────────────────┐       ┌──────────────────────┐
│  a.qmd      │       │  1. EXECUTE                    │       │  2. PANDOC           │
│             │       │                                │       │                      │
│ - yaml      │──────▶│  Quarto converts the .qmd's    │──────▶│  Quarto feeds pandoc │
│ - markdown  │       │  code cells into a temporary   │       │  the original .qmd   │
│ - code cells│       │  .ipynb notebook, starts a     │       │  markdown + the cell │
│             │       │  Jupyter kernel, and executes  │       │  outputs from step 1 │
└─────────────┘       │  each cell. Outputs:           │       │                      │
                      │   • cell outputs (text, tables)│       │  Pandoc converts the │
                      │   • figure files on disk       │       │  combined document   │
                      │     (SVG or PNG)               │       │  to HTML.            │
                      └────────────────────────────────┘       └──────┬───────────────┘
                                                                      │
                                                                      ▼
                                                              ┌──────────────────────┐
                                                              │  Output              │
                                                              │   • a.html           │
                                                              │   • a_files/         │
                                                              │     └ figure-html/   │
                                                              │       └ fig-*.svg    │
                                                              └──────────────────────┘
```

In more detail:

1. **Parse**: Quarto reads the `.qmd` and separates the YAML front matter, markdown
   prose, and code cells (fenced with ````{python}`).
   _No console output._
2. **Convert to notebook**: Quarto converts the code cells into a temporary Jupyter
   notebook (named `<stem>.quarto_ipynb` in the same directory). This notebook is
   transient — created for execution and cleaned up afterward. The markdown prose is
   not included; only the code cells go into the notebook.
   _No console output._
3. **Execute**: Quarto starts a Jupyter kernel and sends each cell for execution.
   The kernel produces cell outputs: text, display data (figures, tables), errors.
   Figures are written to disk as image files (SVG or PNG, controlled by
   `fig-format`) in a temporary `_files/figure-html/` directory. The `fig-format`
   option is passed to the kernel via Jupyter's inline backend configuration, so
   matplotlib (and plotnine, which wraps it) produce figures in the requested format
   at execution time. Console output:
4. **Merge**: Quarto takes the original `.qmd` markdown and annotates it with the
   cell outputs from step 3. Each code cell's output (including references to the
   figure files on disk) is spliced back into the document at the position of the
   code fence that produced it. The result is a self-contained markdown document
   ready for pandoc.
   _No console output._
5. **Pandoc**: Quarto feeds the annotated markdown to pandoc, which converts it to
   the target format (HTML, DOCX, etc.). For HTML, pandoc produces the `.html` file.
   Figure files are copied into the final `_files/` companion directory.
   Console output:

The freeze cache, embed mechanism, and embed cache described below all operate on
the boundary between these stages — they store or reuse intermediate results so
that one or both stages can be skipped on subsequent renders.

## HTML output structure

When rendering completes, Quarto produces:

- `**<name>.html`** — the rendered page.
- `**<name>_files/`** — a companion directory containing everything the HTML
  references: figures, CSS, JS libraries, font files. The HTML uses relative
  paths into this directory (e.g., `<name>_files/figure-html/fig-a-output-1.svg`).

In a **project render** (`quarto render .`), the `output-dir` setting in
`_quarto.yml` (typically `docs`) controls where these land. Site-wide assets
(Bootstrap CSS/JS, Quarto runtime, syntax highlighting) are deduplicated into a
shared `docs/site_libs/` directory. Each rendered page's `_files/` directory
contains only page-specific assets (mostly figures).

In a **single-file render** (`quarto render foo.qmd`), Quarto still reads
`_quarto.yml` if it exists and respects `output-dir`. However, the CLI flag
`--output-dir` is rejected for single-file renders — only the project config
controls the output directory.

## The freeze cache

The freeze cache stores the results of **step 3 (Execute)** — the raw cell
outputs and figure files — so that the expensive Jupyter kernel execution can be
skipped on subsequent renders. It lives at:

```
.quarto/_freeze/<notebook-path>/
├── execute-results/html.json   # cell outputs (text, display_data, errors)
└── figure-html/                # figure files produced by cell execution
    └── fig-a-output-1.svg
```

### What it stores

The `html.json` file contains the serialized outputs of each code cell — the same
data structure Jupyter would store in a notebook's `outputs` array. The
`figure-html/` directory contains the actual image files that cell execution wrote
to disk.

### Cache validity

The freeze cache is **all-or-nothing at the file level**. Quarto computes an MD5
hash of the entire `.qmd` source file and stores it alongside the cached outputs.
On the next render, it re-hashes the source and compares. If a single character
has changed anywhere — a code cell, prose, YAML front matter, a comment — the
hash changes and **all cells re-execute from scratch**. There is no per-cell
granularity: changing cell 7 of 10 re-executes all 10.

When the hash matches (the `.qmd` is unchanged), Quarto skips steps 2–3 entirely
(no temporary notebook, no kernel) and jumps straight to step 4 (Merge) using
the cached outputs. Only the Pandoc conversion (step 5) runs.

### What it doesn't do

The freeze cache does **not** provide per-cell caching within a notebook. If you
change one cell in a 10-cell notebook that takes 5 minutes to execute, all 10
cells re-execute — even if cells 1–6 and 8–10 are identical to the last run.

For example, suppose `analysis.qmd` has 10 cells. You fix a typo in the caption
of cell 7 and re-render. You might expect Quarto to skip cells 1–6 (unchanged)
and only re-run cell 7 onward. It doesn't. Because the file hash changed, the
entire freeze cache is invalidated and all 10 cells execute from scratch.

This means the freeze cache doesn't help when you're **iterating on the notebook
you're rendering**. Every edit invalidates it. Its value is entirely in skipping
notebooks you _aren't_ editing — i.e., speeding up project-wide renders where
some notebooks are unchanged.

### When it's useful

The freeze cache's main value is in **project renders where some notebooks
haven't changed**. A typical workflow: you're iterating on `index.qmd` (prose
only, no code cells) while `notebooks/analysis.qmd` hasn't been touched. On each
`just render`, the analysis notebook's freeze cache is still valid — its cells
aren't re-executed, and only the Pandoc pass runs for it. This can save minutes
on notebooks with expensive computations.

The cache is written in both project and single-file renders, as long as Quarto
recognizes a project context (i.e., `_quarto.yml` exists in a parent directory).

### Project render vs. single-file render

In practice, the freeze cache behaves the same in both modes. Both write to and
read from `.quarto/_freeze/`. If you run a full project render, every notebook's
execution results are cached. A subsequent single-file render of one of those
notebooks will find and reuse the cache (or update it if the source changed),
assuming you haven't changed the notebook before rendering it (unlikely, or
why would you be single-file rendering it, but there you have it.)

The reverse is also true—if you're working on a particular notebook and you single-file
render it, its outputs are added to the freeze cache, and they'll be picked up
by a subsequent project render.

## How `{{< embed >}}` works

The `{{< embed >}}` shortcode lets one `.qmd` file pull a labeled output (a
figure, table, etc.) from another `.qmd` file. For example, `index.qmd` might
contain:

```
{{< embed notebooks/analysis.qmd#fig-energy-savings >}}
```

This tells Quarto: "find the cell labeled `fig-energy-savings` in
`notebooks/analysis.qmd`, grab its output, and insert it here." The key thing
to understand is that this requires **rendering the referenced notebook through
a separate pipeline** — it can't just read the `.qmd` source, because the
figure doesn't exist until the code runs.

### The embed render pipeline

To produce the `.embed.ipynb`, Quarto renders the referenced notebook through
the same Execute → Merge → Pandoc pipeline from the top of this document. The
only difference is the final step: instead of Pandoc converting to HTML, it
converts to **ipynb format** (`--to ipynb`).

Compare the two:

```
Normal render (produces HTML)
──────────────────────────────────────────────────────────────────────────

┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  a.qmd      │────▶│ 1. EXECUTE   │────▶│ 2. MERGE     │────▶│ 3. PANDOC        │
│             │     │ Jupyter      │     │              │     │    --to html     │
│             │     │ runs cells,  │     │ Splice cell  │     │                  │
│             │     │ produce      │     │ outputs into │     │ → a.html         │
│             │     │ figures      │     │ markdown     │     │ → a_files/       │
└─────────────┘     └──────────────┘     └──────────────┘     └──────────────────┘


Embed render (produces .embed.ipynb)
──────────────────────────────────────────────────────────────────────────

┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  a.qmd      │────▶│ 1. EXECUTE   │────▶│ 2. MERGE     │────▶│ 3. PANDOC        │
│             │     │ Jupyter      │     │              │     │    --to ipynb    │
│             │     │ runs cells,  │     │ Splice cell  │     │                  │
│             │     │ produce      │     │ outputs into │     │ → a.embed.ipynb  │
│             │     │ figures      │     │ markdown     │     │   (cell outputs  │
└─────────────┘     └──────────────┘     └──────────────┘     │    baked in)     │
                                                              └──────────────────┘
```

The `.embed.ipynb` is a Jupyter notebook with all cell outputs baked into its
cell output arrays. Quarto opens it, finds the cell whose label matches
`#fig-a`, and extracts the figure data.

### Where this fits in the parent's pipeline

Embed resolution happens **during the parent's Pandoc stage** — after the
parent's own code cells have already executed. Quarto pauses the parent's Pandoc
pass, obtains the `.embed.ipynb` (via the embed render above, or from the embed cache
we will discuss below), extracts the labeled output, injects it into the parent's
Pandoc stream, and resumes.

```
index.qmd rendering pipeline
──────────────────────────────────────────────────────────────────────────

 ┌──────────────┐     ┌──────────────┐     ┌─────────────────────────────┐
 │ 1. EXECUTE   │────▶│ 2. MERGE     │────▶│ 3. PANDOC (index → HTML)    │
 │              │     │              │     │                             │
 │ Run index's  │     │ Splice cell  │     │ Processing markdown...      │
 │ own code     │     │ outputs into │     │                             │
 │ cells        │     │ markdown     │     │ ┌─────────────────────────┐ │
 └──────────────┘     └──────────────┘     │ │ Encounters {{< embed    │ │
                                           │ │ analysis.qmd#fig-a >}}  │ │
                                           │ └───────────┬─────────────┘ │
                                           │             │ PAUSE         │
                                           │             ▼               │
                                           │  ┌────────────────────────┐ │
                                           │  │ Obtain .embed.ipynb    │ │
                                           │  │ (from cache or by      │ │
                                           │  │  running the embed     │ │
                                           │  │  render pipeline above)│ │
                                           │  └───────────┬────────────┘ │
                                           │              │              │
                                           │              ▼              │
                                           │  ┌────────────────────────┐ │
                                           │  │ Extract #fig-a from    │ │
                                           │  │ .embed.ipynb, inject   │ │
                                           │  │ into index's HTML      │ │
                                           │  └───────────┬────────────┘ │
                                           │              │ RESUME       │
                                           │              ▼              │
                                           │  ...continues processing    │
                                           │  rest of index.qmd...      │
                                           └──────────────┬──────────────┘
                                                          │
                                                          ▼
                                                docs/index.html
                                                docs/index_files/
                                                  figure-html/
                                                    fig-a.svg
```

This is expensive: to embed one figure, Quarto must render the _entire_
referenced notebook (all cells, not just the one being embedded). The embed
cache exists to avoid paying this cost repeatedly.

### Does the embedded notebook get executed twice?

Consider this scenario. You have `analysis.qmd` and `index.qmd` in your project
render list. Without embeds, a project render executes `analysis.qmd` (producing
`analysis.html`) and then executes `index.qmd` (producing `index.html`). If the
freeze cache is warm for `analysis.qmd`, its execution is skipped — only its
Pandoc-to-HTML pass runs. So far, so good.

Now you add `{{< embed notebooks/analysis.qmd#fig-a >}}` to `index.qmd`. The
embed pipeline needs an `.embed.ipynb` — not the `.html` that the project render
already produced. Does `analysis.qmd` get _executed_ a second time to produce
this different output format? In other words, we know we need to change the
pandoc step to produce an ipynb that index can pull embeds from, but do
we also have to repeat the jupyter compute for the analysis notebook?

**No — the cells never execute twice.** The Execute stage for `analysis.qmd` produces
format-agnostic cell outputs (text, display data, figure files) and stores these
in the freeze cache. These results can feed into _any_ Pandoc output format.
What the embed pipeline adds is an additional Pandoc pass (`--to ipynb`) that
converts those same results into a different format. The expensive part (cell execution)
is shared; only the cheap part (Pandoc conversion) is repeated.

In other words, as long as `analysis.qmd` has been rendered before the render
pipeline for `index.qmd` goes looking for `analysis.embed.ipynb`, it will
skip the Execute step of `analysis.embed.ipynb`'s render pipeline and skip
straight to telling Pandoc to produce `.embed.ipynb` from the same cell
outputs that already produced `analysis.html`.

Here's what this all looks like in a project render. The Execute stage for `analysis.qmd`
runs once (or is skipped via freeze cache), and the results fan out into multiple Pandoc
passes:

```
analysis.qmd in a project render (with embeds)
──────────────────────────────────────────────────────────────────────────

                                              ┌──────────────────┐
                                         ┌───▶│ PANDOC → HTML    │───▶ analysis.html
                                         │    └──────────────────┘
┌──────────────┐     ┌──────────────┐    │
│  EXECUTE     │────▶│  MERGE       │────┤
│              │     │              │    │    ┌──────────────────┐
│ (or freeze   │     │ Splice cell  │    └───▶│ PANDOC → ipynb   │───▶ analysis.embed.ipynb
│  cache hit)  │     │ outputs into │         │ (for embeds)     │
│              │     │ markdown     │         └──────────────────┘
└──────────────┘     └──────────────┘
```

Only the HTML Pandoc pass happens when `analysis.qmd` is rendered.
Later, when `index.qmd` encounters the embed shortcode, Quarto triggers the
embed pipeline for `analysis.qmd`. The Execute
stage is skipped (the results are in memory or in the freeze cache), and only
the Pandoc-to-ipynb pass runs — effectively appending the second arrow to the
diagram above on demand.

But there's a twist! In a **manuscript project**, both Pandoc passes happen
automatically when `analysis.qmd` is first rendere — the
`.embed.ipynb` is produced speculatively alongside the HTML. By
the time `index.qmd` encounters the embed shortcode, the `.embed.ipynb` is
already in memory. (And actually, it does _three_ Pandoc passes, because it also
produces an `analysis.out.ipynb`, which is meant to be a standalone Jupyter
notebook containing all the outputs embedded that users can download from
the manuscript website and play with.)

Either way, the cells _execute_ once. The difference between manuscript and
non-manuscript projects is just _when_ the Pandoc-to-ipynb pass happens
(eagerly in manuscript, lazily in non-manuscript).

What about **in a single-file render** of `index.qmd` (or any other stand-alone notebook
that embeds from others?) unlike a project render, when `analysis.qmd`
get rendered before `index.qmd`, `analysis.qmd` not been rendered in this
session — there's nothing in memory. Quarto must produce the `.embed.ipynb`
from scratch. The freeze cache can still skip execution, leaving only the
Pandoc-to-ipynb pass. If the freeze cache is also cold, `analysis.qmd` is
fully executed and then converted to `.embed.ipynb`. Either way, this extra
work happens transparently during the parent's Pandoc stage. So a single-file
render basically works like a project render, there's just no guarantee that
you can skip the execution of the `analysis.qmd` notebook, becaused the
freeze cache may be empty or invalidated.

Okay, so no, embedded notebooks don't get executed twice. But so far,
it seems like you still need to do the Pandoc-to-ipynb pass. But what
if you're just working on `index.qmd`, and nothing has changed in `analysis.qmd`?

Is there a way to skip even the Pandoc-to-ipynb pass? Yes — that's
the embed cache, covered next.

## The embed cache

The embed cache stores the `.embed.ipynb` files produced by the process above,
so that the referenced notebook doesn't need to be re-rendered every time a
document embeds from it. It lives at:

```
.quarto/embed/<notebook-path>/
└── <name>.embed.ipynb
```

### Cache lookup

When Quarto encounters `{{< embed notebooks/a.qmd#fig-a >}}`, it checks for a
cached `.embed.ipynb` before running the full pipeline described above:

1. **In-memory**: has `a.embed.ipynb` already been produced in this render
   session? (This happens in full project renders where `analysis.qmd` is
   rendered before `index.qmd`.)
2. **On disk**: does `.quarto/embed/notebooks/a.embed.ipynb` exist and is it
   newer than the source `a.qmd`? If so, load it.
3. **Render**: if neither, run the full Execute → Merge → Pandoc-to-ipynb
   pipeline to produce a fresh `.embed.ipynb`, then cache it to `.quarto/embed/`.

Once the `.embed.ipynb` is in hand (from any of these three paths), Quarto
extracts the labeled cell output and injects it into the parent document.

### When it's useful

We showed above that the freeze cache already prevents _double execution_ — if
`analysis.qmd`'s cells have run once (either earlier in the same project render
or in a prior render), the Execute stage is skipped and only the Pandoc-to-ipynb
pass runs. The embed cache goes one step further: it skips that Pandoc pass too.

**Scenario: iterating on `index.qmd` prose while analysis is unchanged.** You're
editing the narrative in `index.qmd` and re-rendering repeatedly. Each render
encounters `{{< embed analysis.qmd#fig-a >}}`. Without the embed cache, every
render would need to produce a fresh `.embed.ipynb` — even with a freeze cache
hit on `analysis.qmd`, that still means loading the cached cell outputs, running
Lua filters, and doing the full Pandoc-to-ipynb conversion. Not as expensive as
re-executing cells, but not free either.

With the embed cache, none of that happens. The `.embed.ipynb` from the last
render is already on disk. Quarto loads it, extracts `#fig-a`, and continues —
no Execute, no Pandoc, just a file read.

If `analysis.qmd` _has_ changed, the embed cache is stale (the source is newer
than the cached `.embed.ipynb`). Quarto falls back to the full pipeline:
Execute (unless the freeze cache is still valid — it won't be, since the source
changed) then Pandoc-to-ipynb, producing a fresh `.embed.ipynb` and updating the
cache.

**Scenario: single-file render of a document with embeds.** You run
`just render testimony_outline.qmd` to iterate on a standalone document that
embeds figures from `analysis.qmd`. In a single-file render, `analysis.qmd` was
not rendered in this session — there are no in-memory results. Without the embed
cache, Quarto would need to render `analysis.qmd` from scratch (Execute +
Pandoc-to-ipynb), or at best skip execution via the freeze cache and still do
the Pandoc pass. With the embed cache warm from a prior project render, Quarto
loads the cached `.embed.ipynb` directly — no rendering of `analysis.qmd` at
all.

**Manuscript projects keep the cache warm by default.** In a manuscript project,
the embed cache is populated speculatively for every notebook (see "Manuscript
project specifics" below). After a full project render, every notebook's
`.embed.ipynb` is cached, so both scenarios above are fast without any manual
cache management.

### Relationship to the freeze cache

We already covered this above, but just to be extra explicit: these are independent caches that capture different stages of the pipeline:

| Cache                       | Stores                                                | Pipeline stage | Purpose                                          |
| --------------------------- | ----------------------------------------------------- | -------------- | ------------------------------------------------ |
| Freeze (`.quarto/_freeze/`) | Raw execution results (cell outputs + figure files)   | After Execute  | Skip re-executing notebook cells                 |
| Embed (`.quarto/embed/`)    | Rendered `.embed.ipynb` (execution + pandoc to ipynb) | After Pandoc   | Skip re-rendering notebooks for embed extraction |

The embed pipeline _reads_ from the freeze cache when it renders a notebook: if
a notebook's execution results are already frozen, the embed rendering skips the
Execute stage and goes straight to the Pandoc-to-ipynb stage. So a populated
freeze cache speeds up embed rendering, but the two caches don't share files or
depend on each other structurally.

## Manuscript project specifics

We also already covered this, but just to be extra explicit:
manuscript projects (`type: manuscript` in `_quarto.yml`) add behavior on top of
the general rendering pipeline. Specifically, for every `.qmd` notebook in the
project's render list, the manuscript framework produces three additional
artifacts — regardless of whether any document uses `{{< embed >}}` to reference
the notebook.

### The three manuscript notebook artifacts

When a `.qmd` notebook is rendered within a manuscript project, Quarto runs three
parallel rendering passes from the same executed notebook:

| Render type      | Output file           | Purpose                                                        |
| ---------------- | --------------------- | -------------------------------------------------------------- |
| `kQmdIPynb`      | `<name>.embed.ipynb`  | Pre-built embed artifact, ready for `{{< embed >}}` extraction |
| `kRenderedIPynb` | `<name>.out.ipynb`    | Downloadable executed notebook (for readers)                   |
| `kHtmlPreview`   | `<name>-preview.html` | HTML preview page linked from the manuscript sidebar           |

These are independent Pandoc passes — none depends on the output of another. They
all start from the same Execute-stage results (either freshly executed or loaded
from the freeze cache) and each runs its own Pandoc conversion to a different
output format.

The key implication: in a manuscript project, `.embed.ipynb` is created
**speculatively** for every notebook. The framework doesn't check whether any
document actually embeds from it. This means the embed cache is always populated
after a full manuscript project render, and subsequent single-file renders of
`index.qmd` (or any document with `{{< embed >}}` shortcodes) will find cached
embeds without needing to re-render the notebooks.

### Non-manuscript projects

In a non-manuscript project (e.g., `type: website`), no `.embed.ipynb`,
`.out.ipynb`, or `-preview.html` files are produced. Notebooks are rendered
directly to `.html`. The embed cache is only populated on demand — when a
document containing `{{< embed >}}` is rendered and triggers the embed pipeline.

### Side-by-side: what a project render produces

For a project with one notebook (`notebooks/a.qmd`) and one article
(`index.qmd`), rendering the project produces:

**Manuscript project:**

| File                                                         | Category                          |
| ------------------------------------------------------------ | --------------------------------- |
| `.quarto/_freeze/notebooks/a/execute-results/html.json`      | Freeze cache                      |
| `.quarto/_freeze/notebooks/a/figure-html/fig-a-output-1.svg` | Freeze cache                      |
| `.quarto/embed/notebooks/a.embed.ipynb`                      | Embed cache                       |
| `docs/index.html`                                            | Output: rendered article          |
| `docs/notebooks/a-preview.html`                              | Output: notebook preview page     |
| `docs/notebooks/a.embed.ipynb`                               | Output: published embed notebook  |
| `docs/notebooks/a.out.ipynb`                                 | Output: published output notebook |
| `docs/notebooks/a_files/figure-html/fig-a-output-1.svg`      | Output: figure for preview page   |

**Website project:**

| File                                                         | Category                                  |
| ------------------------------------------------------------ | ----------------------------------------- |
| `.quarto/_freeze/notebooks/a/execute-results/html.json`      | Freeze cache                              |
| `.quarto/_freeze/notebooks/a/figure-html/fig-a-output-1.svg` | Freeze cache                              |
| `.quarto/embed/notebooks/a.embed.ipynb`                      | Embed cache (only if index embeds from a) |
| `docs/index.html`                                            | Output: rendered article                  |
| `docs/notebooks/a.html`                                      | Output: rendered notebook page            |
| `docs/notebooks/a_files/figure-html/fig-a-output-1.svg`      | Output: figure for notebook page          |

(Both also produce `docs/site_libs/` with shared JS/CSS assets, omitted for
clarity.)

## When to render one file vs. the whole project

A full project render (`just render`) renders every file in the render list. A
single-file render (`just render foo.qmd`) renders only that file, resolving
embeds from cache or on demand. Understanding when each is appropriate requires
understanding what work a full project render does that you might not need.

### What a full project render always does

Even when only one file has changed, a full project render:

1. **Runs the Pandoc pass for every file in the render list.** The freeze cache
   skips Execute (cell execution), but the Pandoc conversion always runs. For a
   project with 5 notebooks and an index, that's 6 Pandoc passes minimum — more
   if any of those documents contain `{{< embed >}}` shortcodes that trigger
   additional Pandoc-to-ipynb passes (and more still in manuscript projects where
   each notebook gets three Pandoc passes (HTML, `.embed.ipynb`, `.out.ipynb`))
   though the embed cache can prevent these Pandoc-to-ipynb passes when the
   referenced notebook hasn't changed.
2. **Produces all output artifacts for every file.** Each notebook gets its
   `.html` output (and in manuscript projects, also `.embed.ipynb` and
   `.out.ipynb`).

This is correct and desirable when you want everything up to date. But most of
the time, you're iterating on one file and don't need the rest.

### Comparison: two scenarios

The following tables compare what work happens in a full project render vs. a
single-file render, for a project with `analysis.qmd`, `index.qmd`, and
`testimony.qmd` in the render list (in that order). Both `index.qmd` and
`testimony.qmd` embed figures from `analysis.qmd`.

**Scenario 1: only testimony changed.**

You've been editing `testimony.qmd`. `analysis.qmd` and `index.qmd` are
unchanged.

|                                        | Full project render        | Single-file render        |
| -------------------------------------- | -------------------------- | ------------------------- |
| `analysis.qmd` Execute                 | Skipped (freeze cache hit) | Skipped (embed cache hit) |
| `analysis.qmd` Pandoc → HTML           | Runs                       | Skipped (not rendered)    |
| `analysis.qmd` Pandoc → `.embed.ipynb` | Runs                       | Skipped (embed cache hit) |
| `index.qmd` Execute                    | Skipped (freeze cache hit) | Skipped (not rendered)    |
| `index.qmd` Pandoc → HTML              | Runs (resolves embeds)     | Skipped (not rendered)    |
| `testimony.qmd` Execute                | Runs (freeze cache miss)   | Runs (freeze cache miss)  |
| `testimony.qmd` Pandoc → HTML          | Runs                       | Runs                      |

The single-file render does only the last two rows. The full project render does
the Pandoc passes for analysis and index — not expensive individually, but they
add up across multiple notebooks.

**Scenario 2: analysis changed, testimony embeds from it.**

You changed a cell in `analysis.qmd` that `testimony.qmd` embeds. `index.qmd`
also embeds from `analysis.qmd` (different figures) but hasn't changed itself.

|                                        | Full project render                                         | Single-file render                        |
| -------------------------------------- | ----------------------------------------------------------- | ----------------------------------------- |
| `analysis.qmd` Execute                 | Runs (freeze cache miss)                                    | Runs (freeze cache miss)                  |
| `analysis.qmd` Pandoc → HTML           | Runs                                                        | Skipped (embed pipeline only needs ipynb) |
| `analysis.qmd` Pandoc → `.embed.ipynb` | Runs                                                        | Runs (embed pipeline)                     |
| `index.qmd` Execute                    | Skipped (freeze cache hit)                                  | Skipped (not rendered)                    |
| `index.qmd` Pandoc → HTML              | Runs (picks up fresh analysis embeds)                       | Skipped (not rendered)                    |
| `testimony.qmd` Execute                | Skipped (freeze cache hit — testimony itself didn't change) | Skipped (freeze cache hit)                |
| `testimony.qmd` Pandoc → HTML          | Runs (picks up fresh analysis embeds)                       | Runs (picks up fresh analysis embeds)     |

In the full project render, `index.qmd`'s Pandoc pass runs and picks up the
fresh analysis output — correct behavior, since index embeds from analysis. But
if you're just iterating on testimony and don't need index updated right now,
the single-file render avoids that work. It also skips analysis's HTML Pandoc
pass, since the embed pipeline only needs the `.embed.ipynb`.

The tradeoff: `index.html` is now stale (it still has the old analysis figures),
and `analysis.html` (the preview page) wasn't re-rendered either — both stay as
they were until the next full project render.

### In manuscript projects

Everything above applies, with one addition: manuscript projects produce three
Pandoc passes per notebook (HTML preview, `.embed.ipynb`, `.out.ipynb`) instead
of one. This makes the "wasted work" in a full project render larger — each
unchanged notebook still gets three Pandoc passes instead of one. It also means
the embed cache is always warm after a full project render (`.embed.ipynb` is
produced speculatively for every notebook), which makes single-file renders
particularly effective: embeds resolve from cache without any work on the
referenced notebooks.

### When to use each

**Use `just render` (full project)** when:

- You want all outputs up to date (e.g., before publishing or reviewing).
- You've changed a notebook that multiple documents embed from and want all of
  them to pick up the changes.
- You haven't rendered in a while and want to rebuild everything cleanly.

**Use `just render foo.qmd` (single-file)** when:

- You're iterating on one document and don't need the rest updated.
- You want the fastest possible feedback loop — only the work needed for that
  one file.
- You're working on a document that embeds from notebooks that haven't changed
  (the embed cache makes this nearly free).
