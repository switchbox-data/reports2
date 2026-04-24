"""Switchbox plotnine package.

Importing this package registers brand fonts with matplotlib and installs
a monkey-patch on ``plotnine.ggplot.save_helper`` that rasterizes the
``QuadMesh`` inside every continuous-fill colorbar before SVG save.  Without
the patch, matplotlib emits ~700 KB of Gouraud-shaded-triangle markup per
colorbar; see ``svg_optimize.py`` for the full story.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import plotnine

from lib.plotnine.svg_optimize import rasterize_colorbars
from lib.plotnine.switchbox_theme import SB_COLORS, theme_switchbox

if TYPE_CHECKING:
    from plotnine.iapi import mpl_save_view

__all__ = ["SB_COLORS", "theme_switchbox"]


_original_save_helper = plotnine.ggplot.save_helper


def _save_helper_with_svg_optimize(self: plotnine.ggplot, *args: Any, **kwargs: Any) -> mpl_save_view:
    """Drop-in replacement that rasterizes QuadMesh artists on SVG saves.

    Plotnine's ``_repr_mimebundle_`` -> ``save`` -> ``save_helper`` pipeline
    is the sole path for figures rendered as the last expression in a cell
    (the common Quarto pattern).  Wrapping ``save_helper`` here means every
    plotnine chart that goes to SVG picks up the colorbar optimization
    without any change at the call site.
    """
    view = _original_save_helper(self, *args, **kwargs)
    if view.kwargs.get("format") == "svg":
        rasterize_colorbars(view.figure)
    return view


plotnine.ggplot.save_helper = _save_helper_with_svg_optimize  # ty: ignore[invalid-assignment]
