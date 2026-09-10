"""Switchbox plotnine package.

Importing this package registers brand fonts with matplotlib and
configures SVG text-as-text output.

History: this module previously installed a monkey-patch on
``plotnine.ggplot.save_helper`` to rasterize colorbar ``QuadMesh``
artists before SVG save, trimming ~700 KB of Gouraud-triangle markup per
chart.  That optimization is now disabled because matplotlib's SVG
mixed-mode renderer mispositions ``<image>`` elements for artists inside
``AnchoredOffsetbox`` (plotnine's legend container).  See
``svg_optimize.py`` for the full diagnosis.
"""

from __future__ import annotations

from lib.plotnine.switchbox_theme import SB_COLORS, theme_switchbox

__all__ = ["SB_COLORS", "theme_switchbox"]
