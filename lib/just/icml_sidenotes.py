#!/usr/bin/env python3
"""Post-process ICML to convert footnotes to anchored margin notes (sidenotes).

Pandoc/Quarto exports footnotes as standard ICML ``<Footnote>`` elements, which
InDesign renders as page-bottom footnotes.  Our reports use margin notes instead,
requiring the designer to manually convert each footnote to an inline superscript
reference + an anchored text frame in the margin.

This script automates that conversion.  For each ``<Footnote>`` it produces:

1. An inline superscript reference number (CharacterStyle/SidenoteRef)
2. An anchored TextFrame positioned in the outer page margin
3. A separate Story for the frame's content (ParagraphStyle/Sidenote)

The designer can adjust frame dimensions and positioning by modifying the
``Sidenote`` object style or the ``AnchoredObjectSetting`` attributes after
import.  Frame height auto-sizes to fit content.

Usage (from a report directory)::

    uv run python -m lib.just.icml_sidenotes docs/report.icml

The file is modified in place.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — tweak these to match the InDesign template
# ---------------------------------------------------------------------------
FRAME_WIDTH_PT = 144  # 2 inches
FRAME_HEIGHT_PT = 54  # initial height; auto-sizes via HeightOnly
ANCHOR_X_OFFSET = 12  # points gap between text column edge and note frame
ANCHOR_Y_OFFSET = 0  # vertical offset from baseline (0 = aligned)

# ---------------------------------------------------------------------------
# Regex patterns (Pandoc's ICML output is machine-generated and regular)
# ---------------------------------------------------------------------------

# The full CharacterStyleRange wrapping a Footnote.
# Pandoc always emits:  <CharacterStyleRange ... Position="Superscript">\n  <Footnote>...\n  </CharacterStyleRange>
_FOOTNOTE_BLOCK = re.compile(
    r"<CharacterStyleRange\s+"
    r'AppliedCharacterStyle="\$ID/NormalCharacterStyle"\s+'
    r'Position="Superscript"\s*>'
    r"\s*<Footnote>"
    r"(.*?)"
    r"</Footnote>"
    r"\s*</CharacterStyleRange>",
    re.DOTALL,
)

# Content ParagraphStyleRanges inside a footnote (skip the auto-number one).
# The auto-number para has NO AppliedParagraphStyle attribute; content paras do.
_CONTENT_PARAS = re.compile(
    r"(<ParagraphStyleRange\s+AppliedParagraphStyle="
    r'"ParagraphStyle/Footnote[^"]*"'
    r">.*?</ParagraphStyleRange>)",
    re.DOTALL,
)

# Leading tab in the first <Content> of a footnote paragraph.
# Pandoc prepends \t to separate the auto-number from text; we strip it.
_LEADING_TAB = re.compile(r"(<Content>)\t")


# ---------------------------------------------------------------------------
# Style definitions to inject into the ICML
# ---------------------------------------------------------------------------

_CHAR_STYLE_SIDENOTE_REF = (
    '      <CharacterStyle Self="CharacterStyle/SidenoteRef" '
    'Name="SidenoteRef" Position="Superscript">\n'
    "        <Properties>\n"
    '          <BasedOn type="object">$ID/NormalCharacterStyle</BasedOn>\n'
    "        </Properties>\n"
    "      </CharacterStyle>"
)

_PARA_STYLE_SIDENOTE = (
    '      <ParagraphStyle Self="ParagraphStyle/Sidenote" '
    'Name="Sidenote" LeftIndent="0" PointSize="9">\n'
    "        <Properties>\n"
    '          <BasedOn type="object">$ID/NormalParagraphStyle</BasedOn>\n'
    "        </Properties>\n"
    "      </ParagraphStyle>"
)


def _inject_styles(icml: str) -> str:
    """Add SidenoteRef character style and Sidenote paragraph style."""
    if "CharacterStyle/SidenoteRef" not in icml:
        icml = icml.replace(
            "</RootCharacterStyleGroup>",
            f"{_CHAR_STYLE_SIDENOTE_REF}\n    </RootCharacterStyleGroup>",
        )
    if "ParagraphStyle/Sidenote" not in icml:
        icml = icml.replace(
            "</RootParagraphStyleGroup>",
            f"{_PARA_STYLE_SIDENOTE}\n    </RootParagraphStyleGroup>",
        )
    return icml


# ---------------------------------------------------------------------------
# Builders for replacement XML fragments
# ---------------------------------------------------------------------------


def _inline_ref(n: int) -> str:
    """Superscript reference number in the main text flow."""
    return (
        "<CharacterStyleRange AppliedCharacterStyle="
        '"CharacterStyle/SidenoteRef" Position="Superscript">\n'
        f"    <Content>{n}</Content>\n"
        "  </CharacterStyleRange>"
    )


def _anchored_frame(n: int) -> str:
    """Anchored TextFrame that InDesign places in the outer page margin."""
    w = FRAME_WIDTH_PT
    h = FRAME_HEIGHT_PT
    return (
        '  <CharacterStyleRange AppliedCharacterStyle="$ID/NormalCharacterStyle">\n'
        f'    <TextFrame Self="sidenote_frame_{n}" '
        f'ParentStory="sidenote_story_{n}" '
        'ContentType="TextType" '
        'ItemTransform="1 0 0 1 0 0">\n'
        "      <Properties>\n"
        "        <PathGeometry>\n"
        '          <GeometryPathType PathOpen="false">\n'
        "            <PathPointArray>\n"
        f'              <PathPointType Anchor="0 0" '
        f'LeftDirection="0 0" RightDirection="0 0" />\n'
        f'              <PathPointType Anchor="0 {h}" '
        f'LeftDirection="0 {h}" RightDirection="0 {h}" />\n'
        f'              <PathPointType Anchor="{w} {h}" '
        f'LeftDirection="{w} {h}" RightDirection="{w} {h}" />\n'
        f'              <PathPointType Anchor="{w} 0" '
        f'LeftDirection="{w} 0" RightDirection="{w} 0" />\n'
        "            </PathPointArray>\n"
        "          </GeometryPathType>\n"
        "        </PathGeometry>\n"
        "      </Properties>\n"
        '      <AnchoredObjectSetting AnchoredPosition="Anchored"\n'
        '        SpineRelative="true"\n'
        '        LockPosition="false"\n'
        '        PinPosition="true"\n'
        '        AnchorPoint="TopLeftAnchor"\n'
        '        HorizontalAlignment="LeftAlign"\n'
        '        HorizontalReferencePoint="PageMargins"\n'
        '        VerticalAlignment="TopAlign"\n'
        '        VerticalReferencePoint="LineBaseline"\n'
        f'        AnchorXoffset="{ANCHOR_X_OFFSET}"\n'
        f'        AnchorYoffset="{ANCHOR_Y_OFFSET}" />\n'
        '      <TextFramePreference AutoSizingType="HeightOnly"\n'
        '        AutoSizingReferencePoint="TopCenterPoint"\n'
        '        UseMinimumHeightForAutoSizing="false"\n'
        '        MinimumHeightForAutoSizing="0" />\n'
        "    </TextFrame>\n"
        "  </CharacterStyleRange>"
    )


def _sidenote_story(n: int, content_xml: str) -> str:
    """Standalone Story element for a sidenote's anchored frame content."""
    return (
        f'  <Story Self="sidenote_story_{n}" TrackChanges="false" '
        'StoryTitle="" AppliedTOCStyle="n" AppliedNamedGrid="n">\n'
        '    <StoryPreference OpticalMarginAlignment="false" '
        'OpticalMarginSize="12" />\n'
        '    <InCopyExportOption IncludeGraphicProxies="true" '
        'IncludeAllResources="false" />\n'
        f"{content_xml}\n"
        "  </Story>"
    )


# ---------------------------------------------------------------------------
# Footnote content extraction
# ---------------------------------------------------------------------------


def _extract_and_restyle(footnote_inner: str, n: int) -> str:
    """Extract content paragraphs from a footnote, restyle for sidenote.

    Returns the ParagraphStyleRange XML for the sidenote story, with
    the style changed from ``Footnote > Paragraph`` to ``Sidenote``
    and a superscript number prepended.
    """
    paras = _CONTENT_PARAS.findall(footnote_inner)
    if not paras:
        return (
            '<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/Sidenote">\n'
            "      <CharacterStyleRange AppliedCharacterStyle="
            '"$ID/NormalCharacterStyle">\n'
            f"        <Content>{n}.</Content>\n"
            "      </CharacterStyleRange>\n"
            "    </ParagraphStyleRange>"
        )

    result_parts: list[str] = []
    for i, para in enumerate(paras):
        # Change the paragraph style from Footnote > Paragraph to Sidenote
        restyled = re.sub(
            r'AppliedParagraphStyle="ParagraphStyle/Footnote[^"]*"',
            'AppliedParagraphStyle="ParagraphStyle/Sidenote"',
            para,
        )

        # Strip leading tab from the first <Content> in each paragraph
        restyled = _LEADING_TAB.sub(r"\1", restyled)

        if i == 0:
            # Prepend the note number to the first paragraph
            num_csr = (
                "<CharacterStyleRange AppliedCharacterStyle="
                '"$ID/NormalCharacterStyle" Position="Superscript">\n'
                f"        <Content>{n}</Content>\n"
                "      </CharacterStyleRange>\n"
                "      <CharacterStyleRange AppliedCharacterStyle="
                '"$ID/NormalCharacterStyle">\n'
                "        <Content> </Content>\n"
                "      </CharacterStyleRange>\n"
                "      "
            )
            # Insert the number right after the opening ParagraphStyleRange tag
            restyled = re.sub(
                r"(ParagraphStyle/Sidenote\">)\s*",
                r"\1\n      " + num_csr,
                restyled,
                count=1,
            )

        result_parts.append(restyled)

    return "\n    <Br />\n    ".join(result_parts)


# ---------------------------------------------------------------------------
# Main conversion
# ---------------------------------------------------------------------------


def convert(icml: str) -> str:
    """Convert all footnotes in *icml* to anchored margin notes."""
    stories: list[str] = []
    note_num = 0

    def _replace(m: re.Match[str]) -> str:
        nonlocal note_num
        note_num += 1
        content_xml = _extract_and_restyle(m.group(1), note_num)
        stories.append(_sidenote_story(note_num, content_xml))
        return _inline_ref(note_num) + "\n" + _anchored_frame(note_num)

    result = _FOOTNOTE_BLOCK.sub(_replace, icml)
    result = _inject_styles(result)

    # Insert sidenote stories immediately after the main pandoc_story's
    # closing </Story>, BEFORE the document-level <Hyperlink> declarations
    # block.  InDesign wires <Hyperlink Source="htss-N"> to its source by
    # forward reference at parse time: every htss-N must already have
    # appeared in some Story by the time the parser hits its Hyperlink.
    # Pandoc's template emits all hyperlinks after the single main story,
    # so if we appended sidenote stories at end-of-document the 50+ htss
    # sources living inside them would be unreachable, and outbound URL
    # links in footnotes would silently fail to import as live links.
    # Cross-refs aren't affected because <CrossReferenceSource> encodes
    # its destination inline (no Hyperlink declaration needed).
    if stories:
        stories_block = "\n".join(stories)
        # Use re.sub with a function so the replacement is treated as a
        # literal string (avoids accidental backreference expansion if
        # any URL or content contains a "\1" sequence).
        result, n_subs = re.subn(
            r"</Story>",
            lambda m: "</Story>\n" + stories_block,
            result,
            count=1,
        )
        if n_subs == 0:
            result = result.replace(
                "</Document>",
                f"{stories_block}\n</Document>",
            )

    return result


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m lib.just.icml_sidenotes <path.icml>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    original = path.read_text(encoding="utf-8")

    if "<Footnote>" not in original:
        print(f"No footnotes found in {path}, nothing to do.")
        return

    converted = convert(original)

    footnote_count = len(_FOOTNOTE_BLOCK.findall(original))
    path.write_text(converted, encoding="utf-8")
    print(f"Converted {footnote_count} footnotes to sidenotes in {path}")


if __name__ == "__main__":
    main()
