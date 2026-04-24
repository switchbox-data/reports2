# Switchbox house fonts

`GT Planar`, `IBM Plex Sans`, and `Farnham Text` (plus `ft-` / `gtp-` / `ips-` weights). Two copies of each weight ship here:

- **`*.otf`** — CFF/PostScript-flavored OpenType. What the web reports load via `@font-face` in `reports/.style/switchbox.scss`, also served at `https://switchbox-data.github.io/reports/fonts/…`.
- **`*.ttf`** — TrueType-flavored version of the same font, same internal family name. Needed for server-side rendering of GT tables to SVG via `lib/quarto.py::_display_gt_as_svg`. Chrome's `Page.printToPDF` embeds CFF-flavored OTFs as PDF Type 3 fonts, which Inkscape's native PDF importer mishandles (every `<text>` ends up with `font-size:1e-32px` — invisible). TrueType-flavored fonts get embedded as CID TrueType, which Inkscape decodes correctly with real font sizes and real `<text>` elements preserved for InDesign.

Provisioning installs the `*.ttf` copies into `/usr/local/share/fonts/switchbox/` (see `reports2/.devcontainer/Dockerfile` and `rate-design-platform/infra/user-data.sh`). No need to install the OTFs server-side — the web path fetches them from the CDN, and nothing on the server reads them.

## Regenerating the TTFs

If we ever update an OTF, regenerate its TTF sibling:

```bash
cd reports/.style/fonts
for f in *.otf; do uv run python otf2ttf.py "$f" "${f%.otf}.ttf"; done
```

The conversion uses `fontTools.pens.cu2quPen.Cu2QuPen` (cubic Béziers → quadratic, the same approximation used by `fontmake` / google/fonts tooling) with a max error of 1 font unit.
