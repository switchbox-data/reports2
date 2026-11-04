"""Post-draw optimization for plotnine/matplotlib SVG output.

Matplotlib's SVG backend renders continuous colorbars (the ``QuadMesh``
inside a ``Colorbar``) using Gouraud-shaded triangles.  In SVG this is
simulated with three ``<linearGradient>`` defs plus a ``colorMat``/
``colorAdd`` filter per triangle, producing ~24,000 lines / ~700 KB of
vector markup for a legend that's a few hundred pixels tall.  Every
plotnine figure with a continuous fill scale (e.g. ``scale_fill_gradient``)
pays this tax, and with the Switchbox pipeline that inlines every SVG
into ``index.html`` the tax compounds across the whole report.

The fix is a **two-step** process:

1. **Pre-save** — ``rasterize_colorbars()`` marks every ``QuadMesh``
   in the figure as rasterized.  Matplotlib's SVG backend then emits
   one small embedded PNG strip instead of thousands of Gouraud
   triangles.

2. **Post-save** — ``relocate_colorbar_images()`` parses the SVG
   string and fixes the ``<image>`` position.  Matplotlib's mixed-mode
   SVG renderer ignores the ``AnchoredOffsetbox`` transform that
   plotnine uses to position the legend, so the rasterized PNG ends up
   displaced into the data area.  The correct position is derived from
   the colorbar's ``LineCollection`` tick marks, which *are* placed
   correctly.

Together these reduce colorbar SVG from ~1.9 MB to ~35 KB while
keeping text and axes crisp vector.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from matplotlib.collections import QuadMesh

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def rasterize_colorbars(fig: Figure) -> None:
    """Mark every ``QuadMesh`` in *fig* as rasterized for SVG output.

    Run this on a drawn figure just before ``savefig(format="svg")``.
    The colorbar solids become a small embedded PNG inside the SVG,
    which trims ~700 KB per continuous-fill chart while keeping text
    and axes as crisp vector.

    Plotnine nests the colorbar ``QuadMesh`` inside an ``AuxTransformBox``
    inside the guide's ``AnchoredOffsetbox``, so a naive
    ``ax.get_children()`` walk misses it.  ``Figure.findobj`` recurses
    into offset boxes via each artist's ``get_children``, which finds
    the mesh no matter how deep it's nested.

    We intentionally do not change ``fig.dpi``: plotnine's colorbar
    placement (see ``plotnine.guides.guide_colorbar``) is sensitive to
    DPI, and matplotlib's rasterization resolution at the figure's
    native DPI is already fine for the small legend strip.

    **Important:** the rasterized ``<image>`` element will be
    *mispositioned* by matplotlib's SVG backend (it ignores the
    ``AnchoredOffsetbox`` transform).  Call
    ``relocate_colorbar_images()`` on the SVG string after
    ``savefig()`` to fix the placement.
    """
    for artist in fig.findobj(QuadMesh):
        artist.set_rasterized(True)


# ---------------------------------------------------------------------------
# SVG post-processing: fix mispositioned colorbar <image> elements
# ---------------------------------------------------------------------------

# Regex patterns compiled once at import time.
_RE_LINE_COLLECTION = re.compile(
    r'<g id="LineCollection_(\d+)">(.*?)</g>',
    re.DOTALL,
)
_RE_TICK_PATH = re.compile(
    r"M ([\d.]+) ([\d.]+)\s+L ([\d.]+) ([\d.]+)",
)
_RE_IMAGE = re.compile(
    r"(<image\b[^>]*/>)",
)
_RE_ATTR = re.compile(
    r'(\w+)="([^"]*)"',
)


def _parse_tick_positions(
    lc_content: str,
) -> tuple[float, float, float, float] | None:
    """Extract the colorbar rect bounds from a LineCollection's tick paths.

    Returns ``(x_left, x_right, y_top, y_bottom)`` for the inner edges
    of the tick marks, or ``None`` if the content doesn't look like
    colorbar ticks.
    """
    ticks = _RE_TICK_PATH.findall(lc_content)
    if len(ticks) < 2:
        return None

    xs: set[float] = set()
    ys: set[float] = set()
    for x1, y1, x2, _y2 in ticks:
        xs.update((float(x1), float(x2)))
        ys.add(float(y1))

    if len(xs) < 2 or len(ys) < 2:
        return None

    sorted_xs = sorted(xs)
    sorted_ys = sorted(ys)
    # Tick marks come in left/right pairs straddling the colorbar.
    # The inner edges (closest to center) bound the gradient rect.
    inner_left = sorted_xs[1]
    inner_right = sorted_xs[-2]
    return (inner_left, inner_right, sorted_ys[0], sorted_ys[-1])


def relocate_colorbar_images(svg: bytes) -> bytes:
    """Fix mispositioned colorbar ``<image>`` elements in a rasterized SVG.

    Matplotlib's mixed-mode SVG renderer computes the ``<image>``
    position from the artist's data-coordinate transform without
    accounting for the ``AnchoredOffsetbox`` that plotnine uses for
    legend placement.  The rasterized colorbar PNG ends up inside the
    data area instead of next to the tick marks.

    This function finds each ``LineCollection`` (colorbar ticks),
    derives the correct position, and relocates any ``<image>`` whose
    current position doesn't match.

    Parameters
    ----------
    svg :
        Raw SVG bytes from ``Figure.savefig(format="svg")``.

    Returns
    -------
    bytes
        SVG with colorbar images correctly positioned.  Returned
        unchanged if no colorbar tick marks are found.
    """
    text = svg.decode("utf-8")

    # 1. Collect colorbar target rectangles from LineCollection groups.
    targets: list[tuple[float, float, float, float]] = []
    for m in _RE_LINE_COLLECTION.finditer(text):
        bounds = _parse_tick_positions(m.group(2))
        if bounds is not None:
            targets.append(bounds)

    if not targets:
        return svg

    # 2. Find <image> elements that need relocation.
    #    A "mispositioned" image is one whose x does not fall within any
    #    target x-range (with a small tolerance).
    def _needs_relocation(img_tag: str) -> bool:
        attrs = dict(_RE_ATTR.findall(img_tag))
        x = float(attrs.get("x", "0"))
        return all(not (x_left - 1 <= x <= x_right + 1) for x_left, x_right, _yt, _yb in targets)

    # Collect images that need fixing, pairing each with its closest target.
    images_to_fix = []
    for m in _RE_IMAGE.finditer(text):
        img_tag = m.group(1)
        if _needs_relocation(img_tag):
            images_to_fix.append(m)

    if not images_to_fix:
        return svg

    # 3. Assign each image to the nearest target (by x proximity).
    #    In practice there's usually exactly one of each.
    used_targets: set[int] = set()

    def _pick_target(img_tag: str) -> tuple[float, float, float, float] | None:
        attrs = dict(_RE_ATTR.findall(img_tag))
        img_x = float(attrs.get("x", "0"))
        best_idx = -1
        best_dist = float("inf")
        for i, (xl, xr, _yt, _yb) in enumerate(targets):
            if i in used_targets:
                continue
            mid = (xl + xr) / 2
            dist = abs(img_x - mid)
            if dist < best_dist:
                best_dist = dist
                best_idx = i
        if best_idx >= 0:
            used_targets.add(best_idx)
            return targets[best_idx]
        return None

    # 4. Rewrite the SVG, replacing each mispositioned image.
    parts: list[str] = []
    last_end = 0
    relocated = False

    for m in images_to_fix:
        target = _pick_target(m.group(1))
        if target is None:
            continue

        x_left, x_right, y_top, y_bottom = target
        width = x_right - x_left
        height = y_bottom - y_top

        # Build a new <image> with corrected position.
        # The rasterized PNG has the low colour at row 0 (top) and the
        # high colour at the last row (bottom).  Colorbars display high
        # at top, so we flip vertically via scale(1 -1) translate(0 -h).
        #
        # SVG transform math for `scale(1 -1) translate(0 -h)`:
        #   Combined matrix maps local (x, y) → parent (x, -y + h).
        #   Image top-left at local y = -y_top maps to parent -(-y_top) + h
        #   = y_top + h = y_top + height = y_bottom (bottom of colorbar).
        #   Image bottom at local y = -y_top + height maps to parent
        #   -(-y_top + height) + height = y_top (top of colorbar).
        #   Row 0 (white/low) at local top → parent y_bottom (low) ✓
        #   Last row (dark/high) at local bottom → parent y_top (high) ✓
        img_y = -y_top

        attrs = dict(_RE_ATTR.findall(m.group(1)))
        attrs["x"] = f"{x_left}"
        attrs["y"] = f"{img_y}"
        attrs["width"] = f"{width}"
        attrs["height"] = f"{height}"
        attrs["transform"] = f"scale(1 -1) translate(0 -{height})"

        # Reconstruct the element preserving the href (image data).
        new_tag = "<image " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "/>"

        parts.append(text[last_end : m.start()])
        parts.append(new_tag)
        last_end = m.end()
        relocated = True

    if not relocated:
        return svg

    parts.append(text[last_end:])
    return "".join(parts).encode("utf-8")
