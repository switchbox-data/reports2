from __future__ import annotations

from lib.great_tables.switchbox_theme import get_switchbox_gt_tab_options


def test_get_switchbox_gt_tab_options_has_typography_and_css() -> None:
    opts = get_switchbox_gt_tab_options()
    assert opts["table_font_names"] == ["IBM Plex Sans", "sans-serif"]
    assert opts["heading_align"] == "left"
    assert opts["heading_title_font_size"] == "15px"
    assert opts["column_labels_border_top_width"] == "3px"
    assert opts["column_labels_font_size"] == "12px"
    assert opts["table_body_vlines_width"] == "0px"
    assert opts["row_striping_include_table_body"] is False
    assert opts["row_striping_background_color"] == "#FFFFFF"
    assert opts["stub_font_weight"] == "normal"
    css = opts["table_additional_css"]
    assert isinstance(css, list)
    assert any("GT-Planar-Bold" in rule for rule in css)
    assert any("IBM Plex Sans" in rule for rule in css)
    assert any(":has(tr.gt_col_headings ~ tr.gt_col_headings)" in rule for rule in css)
    assert any("tbody tr.gt_striped" in rule for rule in css)
    assert any("gt_subtitle" in rule and "padding-bottom: 20px" in rule for rule in css)
    assert any("gt_sourcenote" in rule and "padding-top: 14px" in rule for rule in css)


def test_get_switchbox_gt_tab_options_merges_extra_css() -> None:
    opts = get_switchbox_gt_tab_options(extra_table_additional_css=[".gt_table { margin: 0; }"])
    css = opts["table_additional_css"]
    assert any("margin: 0" in rule for rule in css)


def test_get_switchbox_gt_tab_options_font_faces_optional() -> None:
    opts = get_switchbox_gt_tab_options(include_font_faces=True)
    css = opts["table_additional_css"]
    assert any("@font-face" in rule for rule in css)
    assert any("GT-Planar-Bold.otf" in rule for rule in css)


def test_get_switchbox_gt_tab_options_layout_overrides() -> None:
    opts = get_switchbox_gt_tab_options(table_width="800px")
    assert opts["table_width"] == "800px"
