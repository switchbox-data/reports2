"""Switchbox brand typography for Great Tables (Python).

Parallels ``lib/plotnine/switchbox_theme.py`` for charts:

- **Table title** — same as plotnine ``plot_title``: GT Planar **Bold**, 15px, black,
  **left-aligned** (tier 1).
- **Subtitle** — same as plotnine ``plot_subtitle``: GT Planar Regular, 13px, ``#333333``,
  left-aligned; extra bottom padding before the column-header rule.
- **Column spanners** — GT Planar **Bold**, 12px, ``#333333`` (slightly smaller than plotnine axis titles).
- **Column labels** (leaf headers under spanners) — GT Planar Regular, 12px, ``#333333``.
- **Stub (row labels)** — IBM Plex Sans **Bold**, 11px, ``#4D4D4D``.
- **Body cells, source notes** — IBM Plex Sans Regular, 11px, ``#4D4D4D``.

**Rules** (Switchbox report tables): thick black rule directly above the column-header block; thin black rule under headers; light gray horizontal rules between body rows; **no** vertical grid lines, **no** outer side borders or bottom table border, **no** row striping. Align per-cell formatting (e.g. ``cols_align``) is left to each table.

Font families match ``reports/.style/switchbox.scss`` (``GT-Planar``, ``GT-Planar-Bold``,
``IBM Plex Sans``). When tables are embedded in Quarto HTML, those ``@font-face`` rules
already load. For standalone HTML (e.g. cached notebook preview), pass
``include_font_faces=True`` to embed the same font URLs GitHub Pages uses.

Usage::

    from lib.great_tables import get_switchbox_gt_tab_options

    (
        GT(df)
        .tab_header(title="…", subtitle="…")
        .tab_options(**get_switchbox_gt_tab_options())
    )

    # Extra CSS (e.g. layout), optionally embed @font-face:
    opts = get_switchbox_gt_tab_options(
        extra_table_additional_css=[".gt_table { max-width: 100%; }"],
        include_font_faces=True,
    )
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

# Published report fonts (same base as switchbox.scss)
_FONTS_BASE = "https://switchbox-data.github.io/reports/fonts"

_COLOR_HEADER = "#333333"
_COLOR_DATA = "#4D4D4D"
_COLOR_RULE_BLACK = "#000000"
_COLOR_RULE_LIGHT = "#D8D8D8"
_COLOR_BG_WHITE = "#FFFFFF"
# Column headers: smaller than the former 13px default; still above 11px body.
_COLUMN_LABEL_PX = "12px"
# Space below subtitle before the column-label block (thick rule); GT default ~5px is tight.
_HEADING_SUBTITLE_PADDING_BOTTOM = "20px"


def _switchbox_gt_font_face_rules() -> list[str]:
    return [
        '@font-face { font-display: swap; font-family: "GT-Planar"; font-style: normal; '
        f'src: url("{_FONTS_BASE}/gt_planar/GT-Planar-Regular.otf") format("opentype"); }}',
        '@font-face { font-display: swap; font-family: "GT-Planar-Bold"; font-style: normal; '
        f'src: url("{_FONTS_BASE}/gt_planar/GT-Planar-Bold.otf") format("opentype"); }}',
        '@font-face { font-display: swap; font-family: "IBM Plex Sans"; font-style: normal; '
        f'src: url("{_FONTS_BASE}/ibm_plex_sans/IBMPlexSans-Regular.otf") format("opentype"); }}',
    ]


def _switchbox_gt_typography_rules() -> list[str]:
    """CSS appended after GT's compiled rules; use !important to beat #table_id table {...}."""
    return [
        ".gt_table .gt_heading .gt_title { "
        "font-family: 'GT-Planar-Bold', 'GT Planar', sans-serif !important; "
        "font-size: 15px !important; line-height: 1.2 !important; font-weight: normal !important; "
        "color: #000000 !important; text-align: left !important; }",
        ".gt_table .gt_heading .gt_subtitle { "
        "font-family: 'GT-Planar', 'GT Planar', sans-serif !important; "
        f"font-size: 13px !important; line-height: 1.35 !important; font-weight: normal !important; "
        f"color: {_COLOR_HEADER} !important; text-align: left !important; "
        f"padding-bottom: {_HEADING_SUBTITLE_PADDING_BOTTOM} !important; }}",
        ".gt_table .gt_heading { text-align: left !important; }",
        # Leaf column labels default to regular; bold overrides below for single-row tables and
        # spanner-row stub / rowspan headers (matches reference: spanners + stub head bold, "$/kWh" regular).
        ".gt_table .gt_col_heading { "
        "font-family: 'GT-Planar', 'GT Planar', sans-serif !important; "
        f"font-size: {_COLUMN_LABEL_PX} !important; line-height: 1.35 !important; "
        "font-weight: normal !important; "
        f"color: {_COLOR_HEADER} !important; }}",
        # Exactly one column-label row (title/subtitle rows may precede in thead) → all bold.
        ".gt_table thead:not(:has(tr.gt_col_headings ~ tr.gt_col_headings)) tr.gt_col_headings .gt_col_heading { "
        "font-family: 'GT-Planar-Bold', 'GT Planar', sans-serif !important; "
        f"font-size: {_COLUMN_LABEL_PX} !important; line-height: 1.35 !important; "
        "font-weight: normal !important; "
        f"color: {_COLOR_HEADER} !important; }}",
        ".gt_table thead tr.gt_spanner_row ~ tr.gt_col_headings .gt_col_heading { "
        "font-family: 'GT-Planar', 'GT Planar', sans-serif !important; "
        f"font-size: {_COLUMN_LABEL_PX} !important; line-height: 1.35 !important; "
        "font-weight: normal !important; "
        f"color: {_COLOR_HEADER} !important; }}",
        ".gt_table thead tr.gt_spanner_row .gt_col_heading { "
        "font-family: 'GT-Planar-Bold', 'GT Planar', sans-serif !important; "
        f"font-size: {_COLUMN_LABEL_PX} !important; line-height: 1.35 !important; "
        "font-weight: normal !important; "
        f"color: {_COLOR_HEADER} !important; }}",
        ".gt_table .gt_column_spanner_outer, .gt_table .gt_column_spanner { "
        "font-family: 'GT-Planar-Bold', 'GT Planar', sans-serif !important; "
        f"font-size: {_COLUMN_LABEL_PX} !important; line-height: 1.35 !important; "
        "font-weight: normal !important; "
        f"color: {_COLOR_HEADER} !important; }}",
        ".gt_table .gt_stub, .gt_table .gt_stub_row_group { "
        "font-family: 'IBM Plex Sans', 'IBM-Plex-Sans', sans-serif !important; "
        f"font-size: 11px !important; line-height: 1.4 !important; font-weight: bold !important; "
        f"color: {_COLOR_DATA} !important; }}",
        ".gt_table .gt_sourcenote { "
        "font-family: 'IBM Plex Sans', 'IBM-Plex-Sans', sans-serif !important; "
        f"font-size: 11px !important; line-height: 1.4 !important; color: {_COLOR_DATA} !important; }}",
        # No alternating row fill: SCSS uses #F4F4F4 for .gt_striped — force flat white even if
        # striping is toggled on elsewhere, and neutralize host page striping on tbody cells.
        ".gt_table tbody tr.gt_striped > th, .gt_table tbody tr.gt_striped > td { "
        f"background-color: {_COLOR_BG_WHITE} !important; color: {_COLOR_DATA} !important; }}",
        # No !important here: body cells need to respect GT `tab_style` fills (e.g. area column colors).
        ".gt_table tbody tr:not(.gt_striped) > th, .gt_table tbody tr:not(.gt_striped) > td { "
        f"background-color: {_COLOR_BG_WHITE}; }}",
    ]


def get_switchbox_gt_tab_options(
    *,
    extra_table_additional_css: Iterable[str] | None = None,
    include_font_faces: bool = False,
    **tab_option_overrides: Any,
) -> dict[str, Any]:
    """Build keyword arguments for :meth:`great_tables.GT.tab_options`.

    Parameters
    ----------
    extra_table_additional_css
        Extra rules appended after brand typography (e.g. widths, layout).
    include_font_faces
        If True, prepend ``@font-face`` rules so standalone HTML can load brand fonts.
    **tab_option_overrides
        Any other valid ``tab_options`` keys (e.g. ``table_width``, ``table_layout``) merged
        on top; use for table-specific layout. ``table_additional_css`` in overrides replaces
        the merged list unless you extend manually — prefer ``extra_table_additional_css``.
    """
    css: list[str] = []
    if include_font_faces:
        css.extend(_switchbox_gt_font_face_rules())
    css.extend(_switchbox_gt_typography_rules())
    if extra_table_additional_css is not None:
        css.extend(extra_table_additional_css)

    out: dict[str, Any] = {
        "table_font_names": ["IBM Plex Sans", "sans-serif"],
        "table_font_size": "11px",
        "table_font_weight": "normal",
        "table_font_color": _COLOR_DATA,
        "table_background_color": _COLOR_BG_WHITE,
        # Open frame: no outer top/bottom/side box; the strong rule sits on the header block.
        "table_border_top_style": "none",
        "table_border_top_width": "0px",
        "table_border_bottom_style": "none",
        "table_border_bottom_width": "0px",
        "table_border_left_style": "none",
        "table_border_left_width": "0px",
        "table_border_right_style": "none",
        "table_border_right_width": "0px",
        "heading_align": "left",
        "heading_title_font_size": "15px",
        "heading_title_font_weight": "normal",
        "heading_subtitle_font_size": "13px",
        "heading_subtitle_font_weight": "normal",
        "heading_border_bottom_style": "none",
        "heading_border_bottom_width": "0px",
        "column_labels_font_size": _COLUMN_LABEL_PX,
        "column_labels_font_weight": "normal",
        "column_labels_padding": "10px",
        "column_labels_padding_horizontal": "14px",
        "column_labels_vlines_style": "none",
        "column_labels_vlines_width": "0px",
        "column_labels_border_top_style": "solid",
        "column_labels_border_top_width": "3px",
        "column_labels_border_top_color": _COLOR_RULE_BLACK,
        "column_labels_border_bottom_style": "solid",
        "column_labels_border_bottom_width": "1px",
        "column_labels_border_bottom_color": _COLOR_RULE_BLACK,
        "column_labels_border_lr_style": "none",
        "column_labels_border_lr_width": "0px",
        "table_body_hlines_style": "solid",
        "table_body_hlines_width": "1px",
        "table_body_hlines_color": _COLOR_RULE_LIGHT,
        "table_body_vlines_style": "none",
        "table_body_vlines_width": "0px",
        "table_body_border_top_style": "none",
        "table_body_border_top_width": "0px",
        "table_body_border_bottom_style": "none",
        "table_body_border_bottom_width": "0px",
        "stub_font_size": "11px",
        "stub_font_weight": "bold",
        "stub_border_style": "none",
        "stub_border_width": "0px",
        "data_row_padding": "10px",
        "data_row_padding_horizontal": "14px",
        "row_striping_include_table_body": False,
        "row_striping_include_stub": False,
        # Same as table background so compiled .gt_striped rules never show gray (#F4F4F4).
        "row_striping_background_color": _COLOR_BG_WHITE,
        "source_notes_font_size": "11px",
        "source_notes_border_bottom_style": "none",
        "source_notes_border_bottom_width": "0px",
        "table_additional_css": css,
    }
    out.update(tab_option_overrides)
    return out
