"""Switchbox plotnine package.

Importing this package registers brand fonts with matplotlib and
configures SVG text-as-text output.

It also installs a monkey-patch on ``plotnine.ggplot.save`` so that
any ``.save("file.svg")`` call automatically rasterizes colorbar
``QuadMesh`` artists and fixes their positioning in the SVG output.
This keeps plotnine's native save path (not just ``display_figure``)
producing compact SVGs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import plotnine
from plotnine.ggplot import mpl_save_view

from lib.plotnine.svg_optimize import rasterize_colorbars, relocate_colorbar_images
from lib.plotnine.switchbox_theme import SB_COLORS, theme_switchbox

__all__ = ["SB_COLORS", "theme_switchbox"]


def _is_svg_save(sv: mpl_save_view) -> bool:
    """Return True if this save view targets SVG output.

    plotnine infers format from the filename extension when ``format``
    is not passed explicitly, leaving ``sv.kwargs["format"]`` as
    ``None``.  We check both the explicit format and the filename.
    """
    fmt = sv.kwargs.get("format")
    if fmt is not None:
        return str(fmt).lower() == "svg"
    fname = sv.kwargs.get("fname")
    if fname is not None:
        return str(fname).lower().endswith(".svg")
    return False


# --- save_helper patch: rasterize colorbars pre-savefig ---

_original_save_helper = plotnine.ggplot.save_helper


def _save_helper_with_rasterize(
    self: plotnine.ggplot,
    *args: Any,
    **kwargs: Any,
) -> mpl_save_view:
    """Monkey-patched save_helper: mark QuadMesh as rasterized for SVG."""
    sv = _original_save_helper(self, *args, **kwargs)
    if _is_svg_save(sv):
        rasterize_colorbars(sv.figure)
    return sv


plotnine.ggplot.save_helper = _save_helper_with_rasterize  # type: ignore[assignment]


# --- save patch: relocate colorbar images post-savefig ---

_original_save = plotnine.ggplot.save


def _save_with_relocate(self: plotnine.ggplot, *args: Any, **kwargs: Any) -> None:
    """Monkey-patched save: after savefig, fix colorbar <image> position."""
    _original_save(self, *args, **kwargs)

    # Determine the output path from the same args save_helper would use.
    filename = kwargs.get("filename", args[0] if args else None)
    fmt = kwargs.get("format", args[1] if len(args) > 1 else None)
    path_dir = kwargs.get("path", args[2] if len(args) > 2 else "")

    if filename is None:
        return

    # Check if this is an SVG save.
    is_svg = (fmt is not None and str(fmt).lower() == "svg") or str(filename).lower().endswith(".svg")
    if not is_svg:
        return

    out = Path(path_dir) / filename if path_dir else Path(str(filename))
    if out.exists():
        svg_bytes = out.read_bytes()
        fixed = relocate_colorbar_images(svg_bytes)
        if fixed is not svg_bytes:
            out.write_bytes(fixed)


plotnine.ggplot.save = _save_with_relocate  # type: ignore[assignment]
