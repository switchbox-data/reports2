# Dev-time notebook review links

How to get a stable, shareable GitHub Pages link to one notebook's rendered
output for internal review, separate from a report's final publish.

## Why this exists

Reports are Quarto Manuscript projects: only `index.qmd` (the finished
narrative) is meant to be reachable on the public site. Supporting notebooks
(`notebooks/analysis.qmd`, `notebooks/incremental_cos.qmd`, etc.) exist purely
as `{{< embed >}}` sources. `lib/just/publish.py` deletes their standalone
preview pages (`*-preview.html`, `.qmd`, `.ipynb`) on purpose when copying a
report's `docs/` to the root `docs/<project>/` that GitHub Pages serves, so
the public site only ever shows the finished article. See
[quarto_html_rendering_internals.md](quarto_html_rendering_internals.md) for
why manuscript notebooks produce a `-preview.html` in the first place.

Sometimes you want to share a notebook's rendered output for internal review
_before_ the report is finished — e.g. to get feedback on `incremental_cos.qmd`
without publishing the whole report yet. `just share` gives you a link for
that, without touching the final-publish behavior at all.

## How it works

`lib/just/share.py` does not render anything. A normal full `just render`
already produces a fully-styled, standalone `docs/notebooks/<name>-preview.html`
(+ `<name>_files/` sidecar) for every notebook in `project.render` — charts in
it are already CSS-styled inline SVGs, since `inline_svgs.py` already ran over
the whole `docs/` tree. `share.py`'s only job is to copy that already-correct
artifact into a `_review/` folder nested under the project's published
`docs/<project>/` tree:

```
docs/<project>/_review/notebooks/<name>-preview.html
docs/<project>/_review/notebooks/<name>_files/
```

Because `_review/` is nested inside `docs/<project>/`, `publish.py`'s existing
whole-tree `rmtree` + `copytree` (it replaces the entirety of
`docs/<project>/` on every real `just publish`) sweeps `_review/` away
automatically the next time this report is actually published. No pruning
rule was added to `publish.py` for this.

This only works for notebooks already listed in the report's
`project.render` in `_quarto.yml` — that's what makes Quarto produce a
`-preview.html` in the first place. If the notebook you want to share isn't
in `project.render`, add it there first.

## Usage

From the report directory:

```bash
just render                              # if you haven't already
just share notebooks/incremental_cos.qmd
```

This prints the resulting Pages URL and the exact git commands to make it
live:

```bash
cd ../..
git add -f docs/<project>/_review/
git commit -m "Add dev review link for incremental_cos.qmd"
git push
# then merge to main -- GitHub Pages only builds from main
```

Check the [Actions tab](https://github.com/switchbox-data/reports2/actions)
for the Pages build, then confirm the printed URL resolves.

## Caveats

- **Unlisted, not access-controlled.** Same as every other published report:
  `docs/` → GitHub Pages is this repo's only publishing pipeline, and it's
  public (just not linked from anywhere). Don't use this for anything that
  genuinely needs restricted access.
- **Ephemeral.** The review link disappears automatically the next time this
  report runs a real `just publish` — there's nothing to clean up manually,
  but also nothing to rely on long-term. If you need a link to stay up, that's
  a sign it should go through the real publish flow instead.
- **`.nojekyll` is required.** GitHub Pages' default "deploy from a branch"
  mode runs the published tree through Jekyll, which excludes any path
  starting with `_` (like `_review/`) unless a `.nojekyll` file sits at the
  Pages source root. This repo has `docs/.nojekyll` for exactly this reason —
  don't remove it.
- **Rollout scope.** As of this writing, only `reports/md_hp_rates/Justfile`
  has the `share` recipe. Adding it to other reports' Justfiles (and to the
  external `switchbox-data/report_template` repo, so `just new_report`
  scaffolds include it) is mechanical but hasn't been done yet.
