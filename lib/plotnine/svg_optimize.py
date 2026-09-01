"""Post-draw optimization for plotnine/matplotlib SVG output.

Matplotlib's SVG backend renders continuous colorbars (the ``QuadMesh``
inside a ``Colorbar``) using Gouraud-shaded triangles.  In SVG this is
simulated with three ``<linearGradient>`` defs plus a ``colorMat``/
``colorAdd`` filter per triangle, producing ~24,000 lines / ~700 KB of
vector markup for a legend that's a few hundred pixels tall.  Every
plotnine figure with a continuous fill scale (e.g. ``scale_fill_gradient``)
pays this tax, and with the Switchbox pipeline that inlines every SVG
into ``index.html`` the tax compounds across the whole report.

The fix is to call ``artist.set_rasterized(True)`` on the colorbar's
``QuadMesh`` *before* ``Figure.savefig(format="svg")``.  Matplotlib's
SVG backend then emits one small embedded PNG strip for the colorbar
(base64-encoded inside an ``<image>`` element) while everything else —
axes, text, tiles — stays vector.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from matplotlib.collections import QuadMesh

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def rasterize_colorbars(fig: Figure) -> None:
    """Mark every ``QuadMesh`` in ``fig`` as rasterized for SVG output.

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

    Parameters
    ----------
    fig :
        Drawn matplotlib figure (e.g. ``plotnine.ggplot.draw()`` output,
        or the figure wrapped by ``mpl_save_view``).
    """
    for artist in fig.findobj(QuadMesh):
        artist.set_rasterized(True)
