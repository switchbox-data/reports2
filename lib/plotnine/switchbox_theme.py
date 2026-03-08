"""Switchbox brand theme for plotnine.

Applies Switchbox brand fonts (GT Planar for titles, Farnham Text for
subtitles/legend/strip text, IBM Plex Sans for axes), white panel
background, visible axis lines/ticks, and Switchbox brand colors.

Usage::

    from lib.plotnine import theme_switchbox, SB_COLORS

    (
        ggplot(df, aes("x", "y"))
        + geom_col(fill=SB_COLORS["sky"])
        + theme_switchbox()
    )
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from matplotlib import font_manager
from plotnine import element_line, element_rect, element_text, theme
from plotnine.themes.theme_minimal import theme_minimal

type _MarginKey = Literal["t", "b", "l", "r", "unit"]

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

    _FONTS_REGISTERED = True


SB_COLORS: dict[str, str] = {
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


class theme_switchbox(theme_minimal):
    """Switchbox brand theme for plotnine.

    Font assignment:
    - **GT Planar Bold**: plot title
    - **Farnham Text**: plot subtitle, legend title, strip (facet) text
    - **IBM Plex Sans**: axis text, axis titles, legend text (base family)

    Parameters
    ----------
    base_size
        Base font size in points. All text sizes scale from this.
    """

    def __init__(self, base_size: int = 12):
        _register_fonts()
        super().__init__(base_size=base_size, base_family=_FONT_IBM_PLEX)
        margin_x: dict[_MarginKey, Any] = {"t": 3, "unit": "pt"}
        margin_y: dict[_MarginKey, Any] = {"r": 3, "unit": "pt"}
        self += theme(
            panel_background=element_rect(fill="white", color="white"),
            plot_title=element_text(family=_FONT_GT_PLANAR, fontweight="bold"),
            plot_subtitle=element_text(family=_FONT_FARNHAM),
            legend_title=element_text(family=_FONT_FARNHAM, ha="center"),
            strip_text=element_text(family=_FONT_FARNHAM),
            axis_line=element_line(size=0.5),
            axis_ticks=element_line(color="black"),
            axis_title_x=element_text(margin=margin_x),
            axis_title_y=element_text(margin=margin_y),
        )
