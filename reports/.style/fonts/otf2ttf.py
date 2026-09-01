#!/usr/bin/env python3
"""Convert CFF-flavored OTF fonts to TrueType-flavored TTF.

The Switchbox house fonts (GT Planar, IBM Plex Sans, Farnham Text) ship as
OTFs with CFF/PostScript outlines. That's fine for browsers, but Chrome's
``Page.printToPDF`` (used by ``lib/quarto.py::_display_gt_as_svg`` for the
ICML render path) embeds CFF-flavored OTFs as **PDF Type 3 fonts** — a
per-glyph drawing-operator format that Inkscape's native PDF importer
cannot decode for font size. The resulting SVG has ``font-size:1e-32px``
on every ``<text>`` element and the text is invisible.

TrueType-flavored fonts (``glyf`` table, quadratic Bézier curves) get
embedded as CID TrueType, which Inkscape handles correctly, preserving
editable ``<text>`` elements at the right size. So we pre-convert each
OTF to a TTF with the same internal family name. fontconfig sees both
and resolves ``GT Planar`` / ``IBM Plex Sans`` to the TTF on the server.

Regenerate with::

    cd reports/.style/fonts
    for f in *.otf; do uv run python otf2ttf.py "$f" "${f%.otf}.ttf"; done

Requires ``fonttools`` (already a transitive dep via ``matplotlib``).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, cast

from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable

# Max CFF → TrueType curve approximation error in font units.
# 1.0 is the standard used by google/fonts and fontmake tooling.
MAX_ERR = 1.0


def otf_to_ttf(otf_path: Path, ttf_path: Path) -> None:
    font = TTFont(str(otf_path))
    if "CFF " not in font:
        raise SystemExit(f"{otf_path} has no CFF table — is it already TrueType?")

    glyph_order = font.getGlyphOrder()
    cff_glyphs = font["CFF "].cff[font["CFF "].cff.fontNames[0]].CharStrings

    # fontTools dispatches newTable(tag) and font[tag] to concrete subclasses
    # at runtime, but the stubs return the opaque ``DefaultTable`` base class,
    # so we cast to ``Any`` to access the tag-specific attributes below.
    glyf_table = cast(Any, newTable("glyf"))
    glyf_table.glyphs = {}
    glyf_table.setGlyphOrder(glyph_order)

    for glyph_name in glyph_order:
        pen = TTGlyphPen(None)
        cu2qu_pen = Cu2QuPen(pen, max_err=MAX_ERR, reverse_direction=True)
        cff_glyphs[glyph_name].draw(cu2qu_pen)
        glyf_table[glyph_name] = pen.glyph()

    del font["CFF "]
    font["glyf"] = glyf_table

    font["loca"] = newTable("loca")
    head = cast(Any, font["head"])
    head.indexToLocFormat = 1

    # maxp 0.5 (CFF) → 1.0 (TrueType). fontTools recomputes the counts at
    # compile time; we just need the non-None defaults in place.
    maxp = cast(Any, font["maxp"])
    maxp.tableVersion = 0x00010000
    for attr, default in [
        ("maxPoints", 0),
        ("maxContours", 0),
        ("maxCompositePoints", 0),
        ("maxCompositeContours", 0),
        ("maxZones", 2),
        ("maxTwilightPoints", 0),
        ("maxStorage", 0),
        ("maxFunctionDefs", 0),
        ("maxInstructionDefs", 0),
        ("maxStackElements", 0),
        ("maxSizeOfInstructions", 0),
        ("maxComponentElements", 0),
        ("maxComponentDepth", 0),
    ]:
        setattr(maxp, attr, default)

    # sfnt version → TrueType magic.
    font.sfntVersion = "\x00\x01\x00\x00"

    for tag in ("VORG",):
        if tag in font:
            del font[tag]

    ttf_path.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(ttf_path))
    print(f"{otf_path.name} → {ttf_path.name} ({ttf_path.stat().st_size} bytes)")


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: otf2ttf.py <in.otf> <out.ttf>", file=sys.stderr)
        sys.exit(2)
    otf_to_ttf(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
