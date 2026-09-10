"""Post-draw optimization for plotnine/matplotlib SVG output.

**STATUS: DISABLED.**  The optimization described below is correct in
principle but broken in practice — matplotlib's mixed-mode SVG renderer
mispositions ``<image>`` elements that originate from artists inside
``AnchoredOffsetbox`` containers (which is exactly where plotnine nests
its colorbar ``QuadMesh``).  The rasterized PNG strip ends up inside the
data area instead of in the legend, leaving orphaned tick marks and
labels with no gradient bar.  See the ``rasterize_colorbars`` docstring
for the full diagnosis.

Background
----------
Matplotlib's SVG backend renders continuous colorbars (the ``QuadMesh``
inside a ``Colorbar``) using Gouraud-shaded triangles.  In SVG this is
simulated with three ``<linearGradient>`` defs plus a ``colorMat``/
``colorAdd`` filter per triangle, producing ~24,000 lines / ~700 KB of
vector markup for a legend that's a few hundred pixels tall.  Every
plotnine figure with a continuous fill scale (e.g. ``scale_fill_gradient``)
pays this tax, and with the Switchbox pipeline that inlines every SVG
into ``index.html`` the tax compounds across the whole report.

The *intended* fix was to call ``artist.set_rasterized(True)`` on the
colorbar's ``QuadMesh`` before ``Figure.savefig(format="svg")``.
Matplotlib's SVG backend would then emit one small embedded PNG strip
for the colorbar while everything else stayed vector.  Unfortunately
the backend computes the ``<image>`` element's ``x``/``y`` from the
artist's data-coordinate transform *without* accounting for the
``AnchoredOffsetbox`` positioning transform that plotnine uses to place
the legend to the right of the axes.  The result is a gradient blob
displaced into the data area and a legend that shows only ticks.

Until matplotlib fixes the mixed-mode renderer for offset-box children,
this optimization must stay disabled.  The function is kept as a no-op
so callers don't need to change, and the module docstring serves as a
record of the issue for future revisiting.

Potential future fixes:
  - Post-process the SVG: strip the Gouraud-triangle ``<g>`` for the
    colorbar and replace it with a single ``<rect>`` +
    ``<linearGradient>``.
  - Wait for a matplotlib release that fixes offset-box rasterization.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def rasterize_colorbars(fig: Figure) -> None:
    """No-op.  Colorbar rasterization is disabled.

    This function previously marked every ``QuadMesh`` in *fig* as
    rasterized for SVG output, trimming ~700 KB of Gouraud-triangle
    markup per continuous-fill chart.  It is now a no-op because
    matplotlib's SVG mixed-mode renderer mispositions ``<image>``
    elements for artists nested inside ``AnchoredOffsetbox`` —
    the container plotnine uses for its colorbar guide.

    The symptom: the colorbar gradient strip appears *inside* the data
    area (displaced by the offset-box anchor), while the legend region
    shows only tick marks and labels with no gradient bar.

    Callers (``display_figure``, the ``save_helper`` monkey-patch) are
    left in place so they don't need to change; this function simply
    returns without modifying *fig*.
    """
