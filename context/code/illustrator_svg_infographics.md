# Illustrator-exported SVG infographics in reports

Heat-pole infographics (`img/infographic_*.svg`) and other Illustrator-exported charts are used as inline SVGs in report HTML. Several things break when Illustrator SVGs are inlined. This document lists each issue and its fix.

## Checklist: after exporting a new SVG from Illustrator

1. **Font family names** — find-and-replace Illustrator's PostScript names with web names (see below).
2. **`text` default font** — add `text { font-family: 'GT Planar', sans-serif; }` to the SVG's `<style>`.
3. **`@font-face` declarations** — add them inside `<defs><style>` so the SVG works both standalone and inlined (copy from an existing infographic).
4. **CSS class scoping** — run the `scope_svg_classes` script to prefix `.cls-N` names with the file stem.
5. **White background** — add a white `<rect>` after `</defs>` matching the viewBox dimensions.
6. **Nested `<tspan>` wrappers** — remove any redundant outer `<tspan>` that wraps positioned children without adding `x`/`y`.
7. **ViewBox sizing** — if the viewBox is small (< ~750px wide), scale the content up so `inline_svgs.py` renders it at a reasonable width.
8. **Sync NY ↔ RI** — copy shared infographics between report `img/` directories.
9. **Render** — `just render` from the report directory to re-inline.

Each step is explained in detail below.

## Font family names

Illustrator emits internal PostScript-style names (`GTPlanar-Bold`, `GTPlanar-Regular`, `GTPlanar-Black`). Those do **not** match the `@font-face` names in `reports/.style/switchbox.scss` (`GT Planar` with weights, `GT-Planar-Black`). Unmatched names → fallback font → **broken layout** because copy uses per-glyph `<tspan x="…">` positioning tuned for GT Planar.

**Fix:** In the SVG `<style>`, use `'GT Planar', sans-serif` (keep existing `font-weight` on classes) and `'GT-Planar-Black', 'GT Planar', sans-serif` where Black was used.

## Inherited body font on `<text>` (report HTML only)

In the Quarto HTML page, `main div { font-family: Farnham; font-size: 1.07em }` applies to figure wrappers. Inlined SVG `<text>` nodes often have classes that set **fill** and **font-size** but **not** `font-family`. Only some `<tspan>`s carry `font-family: 'GT Planar'`. **Classless tspans inherit from `<text>`**, which then inherits **Farnham** from the HTML — so one line mixes two fonts and absolute `tspan x` values no longer match glyph widths (gaps, overlaps, "missing" letters).

**Fix:** In each SVG `<style>`, add a default:

```css
text {
  font-family: 'GT Planar', sans-serif;
}
```

## CSS class name collisions (colors)

Illustrator exports SVGs with generic class names (`.cls-1`, `.cls-2`, …). Each SVG defines its own `.cls-N → fill/stroke` mapping. When multiple Illustrator SVGs are inlined on the same HTML page, their `<style>` blocks all share the DOM's CSS scope — the last SVG's `.cls-12 { fill: #f8981d }` overrides an earlier SVG's `.cls-12 { fill: #dcddde }`, **scrambling colors across all infographics on the page**.

**Fix:** Prefix every `.cls-N` class name with the file stem so they're unique per SVG (e.g. `.infographic_2_cls-12`). Apply the renaming to both CSS rules and `class="…"` attributes:

```python
import re
from pathlib import Path

def scope_svg_classes(svg_path: Path) -> None:
    prefix = svg_path.stem.replace("-", "_").replace(" ", "_") + "_"
    text = svg_path.read_text(encoding="utf-8")
    for cls in sorted(set(re.findall(r'\bcls-\d+\b', text))):
        text = re.sub(r'\b' + re.escape(cls) + r'\b', prefix + cls, text)
    svg_path.write_text(text, encoding="utf-8")
```

Run this on every Illustrator SVG after export. The current infographic SVGs have already been scoped.

## White background

These SVGs are transparent. The report's SVG lightbox uses a dark overlay (`reports/.style/inline_svgs.py`); white label fills and `mix-blend-mode: multiply` assume a **white** plate.

**Fix:** After `</defs>`, add `<rect width="W" height="H" fill="#ffffff"/>` where `W`×`H` match the root `viewBox`.

## Nested `<tspan>` wrappers

Some blocks wrap a run of absolutely positioned tspans in an outer `<tspan class="…">` that adds no `x`/`y`. Chromium/WebKit mishandle this; text can scatter as overlapping "floating" letters.

**Fix:** Remove the redundant outer `<tspan>…</tspan>` so each positioned `<tspan>` is a **direct child** of `<text>`.

## ViewBox sizing

`inline_svgs.py` sets the inlined SVG's display `width` to the viewBox width. Illustrator sometimes exports at small canvas sizes (e.g. 504×226 for the NYISO peak load chart). If the viewBox is narrower than the report column (~830px for `column-body-outset`), the chart renders too small and left-aligned.

**Fix:** Scale the viewBox and content up. For example, to widen a 504×226 SVG to 900px:

1. Change `viewBox="0 0 504 226"` → `viewBox="0 0 900 404"` (preserving aspect ratio: `226 × 900/504 ≈ 404`).
2. After `</defs>`, wrap all content in `<g transform="scale(1.7857)">…</g>` (where `1.7857 = 900/504`).

This scales the visual content to fill the wider coordinate space. Text, strokes, and shapes all scale proportionally.

## `@font-face` declarations

Each SVG should embed `@font-face` rules inside `<defs><style>` pointing to the GitHub Pages–hosted font files. This ensures fonts load correctly both when the SVG is served standalone (e.g. `<img src="…svg">` in preview) and when inlined. Copy the `@font-face` block from an existing infographic SVG.

## NY vs RI report assets

`reports/ny_hp_rates/img/` and `reports/ri_hp_rates/img/` use the **same** infographic filenames (`infographic_1.svg`–`3.svg`). They should stay **byte-identical** unless a report intentionally forks art. After changing NY, sync RI with:

```bash
cp reports/ny_hp_rates/img/infographic_*.svg reports/ri_hp_rates/img/
```

After changing sources, run `just render` from the report directory so `inline_svgs.py` re-inlines the SVG into `docs/`.
