"""Switchbox brand theme for plotnine.

Applies Switchbox brand fonts, colors, and sizes to all chart text
elements, producing a consistent visual hierarchy across reports.

Typography guide
----------------
- **Title** (GT Planar Bold 15pt black, **left-aligned**): chart headline, echoes H3 headings.
- **Labeling layer** (GT Planar 13pt #333333): subtitle, axis titles, strip
  (facet) labels, legend title.  Title and subtitle are **left-aligned** (not centered);
  other labeling elements keep theme defaults.
- **Data-reference layer** (IBM Plex Sans 11pt #4D4D4D): axis tick labels,
  legend text — smallest text, for reading values off axes.

Usage::

    from lib.plotnine import theme_switchbox, SB_COLORS

    (
        ggplot(df, aes("x", "y"))
        + geom_col(fill=SB_COLORS["sky"])
        + theme_switchbox()
    )
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

import matplotlib as mpl
from matplotlib import font_manager
from plotnine import element_blank, element_line, element_rect, element_text, theme
from plotnine.themes.theme_minimal import theme_minimal

type _MarginKey = Literal["t", "b", "l", "r", "unit"]


def _render_as_raster() -> bool:
    """True when targeting DOCX/ICML (non-HTML) output."""
    return os.environ.get("SWITCHBOX_GT_AS_IMAGE") == "1" or os.environ.get("SWITCHBOX_TYPESET") == "1"


_FONT_DIR = Path(__file__).resolve().parent.parent.parent / "reports" / ".style" / "fonts"
_FONT_IBM_PLEX = "IBM Plex Sans"
_FONT_GT_PLANAR = "GT Planar"
_FONT_FARNHAM = "Farnham Text"
_FONTS_REGISTERED = False

_FONT_FILES: list[str] = [
    "ips-regular.otf",
    "ips-bold.otf",
    "gtp-regular.otf",
    "gtp-bold.otf",
    "gtp-black.otf",
    "ft-regular.otf",
    "ft-bold.otf",
]


def _register_fonts() -> None:
    """Register all brand fonts with matplotlib (idempotent)."""
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return

    for filename in _FONT_FILES:
        path = _FONT_DIR / filename
        if path.exists():
            font_manager.fontManager.addfont(str(path))

    mpl.rcParams["svg.fonttype"] = "none"
    _FONTS_REGISTERED = True
    _install_figsize_cap()


# Typeset-only figsize cap.  The InDesign text column is 504 pt = 7 in at
# the 72 pt-per-inch convention used by both SVG's ``pt`` unit and InDesign's
# layout.  Matplotlib SVGs embed an outer ``width="<fig_width_in * 72>pt"``,
# so a figure rendered at figsize=(12.5, h) imports 900 pt wide and has to
# be scaled down by hand — which shrinks the theme's 11 pt axis labels to
# ~6 pt.  Capping figsize at 7 in at render time lets matplotlib's layout
# reflow against the smaller frame while text stays at its native pt size.
_MAX_FIG_WIDTH_IN = 7.0
_FIGSIZE_CAP_INSTALLED = False


def _typeset_mode() -> bool:
    return os.environ.get("SWITCHBOX_TYPESET") == "1"


def _cap_figsize(figsize: Any) -> Any:
    if figsize is None:
        return figsize
    try:
        w, h = figsize
    except (TypeError, ValueError):
        return figsize
    if w > _MAX_FIG_WIDTH_IN:
        return (_MAX_FIG_WIDTH_IN, h * _MAX_FIG_WIDTH_IN / w)
    return figsize


def _install_figsize_cap() -> None:
    """Monkey-patch ``plt.figure``/``plt.subplots`` to cap width at 7 in.

    Only active when ``SWITCHBOX_TYPESET=1`` (set by ``just typeset``).
    Web (``just render``) and DOCX (``just draft``) output are unaffected.
    """
    global _FIGSIZE_CAP_INSTALLED
    if _FIGSIZE_CAP_INSTALLED or not _typeset_mode():
        return

    import matplotlib.pyplot as plt

    _orig_figure = plt.figure
    _orig_subplots = plt.subplots

    def figure(*args: Any, **kwargs: Any) -> Any:
        if "figsize" in kwargs:
            kwargs["figsize"] = _cap_figsize(kwargs["figsize"])
        return _orig_figure(*args, **kwargs)

    def subplots(*args: Any, **kwargs: Any) -> Any:
        if "figsize" in kwargs:
            kwargs["figsize"] = _cap_figsize(kwargs["figsize"])
        return _orig_subplots(*args, **kwargs)

    plt.figure = figure  # type: ignore[assignment]
    plt.subplots = subplots  # type: ignore[assignment]
    _FIGSIZE_CAP_INSTALLED = True


SB_COLORS: dict[str, str] = {
    "gray_light": "#E0E0E0",
    "gray": "#999999",
    "sky": "#68BED8",
    "midnight": "#023047",
    "carrot": "#FC9706",
    "saffron": "#FFC729",
    "pistachio": "#A0AF12",
    "black": "#000000",
    "white": "#FFFFFF",
    "midnight_text": "#0B6082",
    "pistachio_text": "#546800",
}


_COLOR_LABEL = "#333333"
_COLOR_DATA = "#4D4D4D"


class theme_switchbox(theme_minimal):
    """Switchbox brand theme for plotnine.

    Three-tier text hierarchy:

    ====  ====================  ==============================================
    Tier  Elements              Spec
    ====  ====================  ==============================================
    1     plot_title            GT Planar Bold · 15pt · black · left-aligned
    2     plot_subtitle         GT Planar · 13pt · #333333 · left-aligned
    2     axis titles,          GT Planar · 13pt · #333333
          strip text,
          legend title
    3     axis tick labels,     IBM Plex Sans · 11pt · #4D4D4D
          legend text
    ====  ====================  ==============================================
    """

    _RASTER_DPI = 300

    def __init__(self, base_size: int = 11):
        _register_fonts()
        super().__init__(base_size=base_size, base_family=_FONT_IBM_PLEX)
        if _render_as_raster():
            self += theme(dpi=self._RASTER_DPI)
        margin_title: dict[_MarginKey, Any] = {"b": 8, "unit": "pt"}
        margin_x: dict[_MarginKey, Any] = {"t": 8, "unit": "pt"}
        margin_y: dict[_MarginKey, Any] = {"r": 8, "unit": "pt"}
        self += theme(
            panel_background=element_rect(fill="white", color="white"),
            # Tier 1 — title
            plot_title=element_text(
                family=_FONT_GT_PLANAR,
                fontweight="bold",
                size=15,
                color="black",
                ha="left",
                margin=margin_title,
            ),
            # Tier 2 — labeling layer
            plot_subtitle=element_text(
                family=_FONT_GT_PLANAR,
                size=13,
                color=_COLOR_LABEL,
                ha="left",
            ),
            axis_title_x=element_text(
                family=_FONT_GT_PLANAR,
                size=13,
                color=_COLOR_LABEL,
                margin=margin_x,
            ),
            axis_title_y=element_text(
                family=_FONT_GT_PLANAR,
                size=13,
                color=_COLOR_LABEL,
                margin=margin_y,
            ),
            strip_text=element_text(
                family=_FONT_GT_PLANAR,
                size=13,
                color=_COLOR_LABEL,
            ),
            legend_title=element_text(
                family=_FONT_GT_PLANAR,
                size=13,
                color=_COLOR_LABEL,
            ),
            # Tier 3 — data-reference layer (explicit x/y so all axis tick labels match)
            axis_text=element_text(
                family=_FONT_IBM_PLEX,
                size=11,
                color=_COLOR_DATA,
            ),
            axis_text_x=element_text(
                family=_FONT_IBM_PLEX,
                size=11,
                color=_COLOR_DATA,
            ),
            axis_text_y=element_text(
                family=_FONT_IBM_PLEX,
                size=11,
                color=_COLOR_DATA,
            ),
            legend_text=element_text(
                family=_FONT_IBM_PLEX,
                size=11,
                color=_COLOR_DATA,
            ),
            # Structure: x-axis line and ticks visible; y-axis line and ticks hidden.
            # Horizontal grid lines (from theme_minimal) remain for y-axis reference;
            # vertical grid lines removed so the x-axis ticks are the only vertical cue.
            axis_line_x=element_line(size=0.5),
            axis_line_y=element_blank(),
            axis_ticks_x=element_line(color="black"),
            axis_ticks_y=element_blank(),
            panel_grid_major_x=element_blank(),
            panel_grid_minor_x=element_blank(),
        )
