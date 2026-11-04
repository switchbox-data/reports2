#!/usr/bin/env python3
"""Build the expert-testimony Word model file (Pandoc "reference doc").

There is exactly one testimony format, used for every docket. It matches
the filed Maryland PSC testimony (CCAN, Case No. 9888): the measurements
below were taken from that filing's body pages.

    * Times New Roman 12 pt, left-aligned (ragged right), 1" margins.
    * Body text double-spaced (480). Every paragraph is followed by one
      9 pt gap (``after=180``); section headings also get 9 pt above.
    * ``Q.`` bold, ``A.`` regular; marker at the margin, text at 0.5",
      wrapped lines and follow-on paragraphs at 0.5" (no first-line indent).
    * Section headings (``I. Introduction``): bold, numeral right-aligned
      in its own 0.5" column, only the *words* underlined (the underline
      is applied to the text run by ``testimony.lua``, never to the numeral).
    * Line numbers restart at 1 on every page, 0.25" left of the text.
    * Header: three right-aligned lines (testimony title, party, case) at
      the top of every body page. Footer: centered page number, restarting
      at 1 on the first body page. The cover page has neither.
    * Figure captions italic 12 pt, single-spaced, indented 0.5".
      Footnotes 11 pt, single-spaced, not line-numbered.

The header text is filled in at render time (``lib.just.draft``), which
replaces the ``{{HEADER_LINE_n}}`` tokens in ``word/header1.xml``.

Run via::

    uv run python -m lib.just.templates.build_expert_testimony

This writes ``expert_testimony.docx`` next to this script; commit the
result. ``lib.just.draft`` hands it to Quarto as ``--reference-doc``.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT = HERE / "expert_testimony.docx"

# ---------------------------------------------------------------------------
# Page geometry (twips: 1/20 pt; 1440 twips = 1 inch)
# ---------------------------------------------------------------------------
# Footer sits ~0.7" above the page bottom edge (page number baseline at
# ~53 pt from the bottom in the filed example), inside the 1" bottom margin.
# Header sits 0.25" below the top edge; the fourth (blank) header paragraph
# pushes the first body line to ~76 pt, as in the example.
PAGE_SIZE = '<w:pgSz w:w="12240" w:h="15840" w:code="1"/>'
PAGE_MARGINS = (
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="360" w:footer="1000" w:gutter="0"/>'
)

# Section properties for the *body* section (the last section of the
# document, so it lives at the end of word/document.xml). The cover
# section's sectPr is injected mid-document by testimony.lua.
#   lnNumType restart="newPage": line numbers restart at 1 on every page.
#   distance=360: numbers sit 0.25" left of the text.
#   pgNumType start=1: the first body page is page 1 (the cover is unnumbered).
SECTPR_XML = f"""<w:sectPr>
    <w:headerReference w:type="default" r:id="rIdTestimonyHeader"/>
    <w:footerReference w:type="default" r:id="rIdTestimonyFooter"/>
    {PAGE_SIZE}
    {PAGE_MARGINS}
    <w:lnNumType w:countBy="1" w:restart="newPage" w:distance="360"/>
    <w:pgNumType w:start="1"/>
    <w:cols w:space="720"/>
    <w:docGrid w:linePitch="360"/>
  </w:sectPr>"""

# ---------------------------------------------------------------------------
# Headers and footers
# ---------------------------------------------------------------------------
_NS = (
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
)

# Three right-aligned lines plus one blank paragraph (the blank line is what
# gives the body its small gap below the header, as in the example).
HEADER_XML = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr {_NS}>
  <w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr><w:r><w:t xml:space="preserve">{{{{HEADER_LINE_1}}}}</w:t></w:r></w:p>
  <w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr><w:r><w:t xml:space="preserve">{{{{HEADER_LINE_2}}}}</w:t></w:r></w:p>
  <w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr><w:r><w:t xml:space="preserve">{{{{HEADER_LINE_3}}}}</w:t></w:r></w:p>
  <w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr></w:p>
</w:hdr>
"""

# Default placeholders baked into the on-disk template; replaced by draft.py.
DEFAULT_HEADER_LINES = ("[TESTIMONY TITLE]", "[PARTY]", "[CASE]")

# Cover pages show no header text and no page number.
BLANK_HEADER_XML = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr {_NS}>
  <w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr></w:p>
</w:hdr>
"""

FOOTER_XML = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr {_NS}>
  <w:p>
    <w:pPr><w:pStyle w:val="Footer"/></w:pPr>
    <w:r><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="separate"/></w:r>
    <w:r><w:rPr><w:noProof/></w:rPr><w:t>1</w:t></w:r>
    <w:r><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:ftr>
"""

BLANK_FOOTER_XML = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr {_NS}>
  <w:p><w:pPr><w:pStyle w:val="Footer"/></w:pPr></w:p>
</w:ftr>
"""

# part name -> (xml, relationship id, relationship type suffix)
HEADER_FOOTER_PARTS = {
    "header1.xml": (HEADER_XML, "rIdTestimonyHeader", "header"),
    "header2.xml": (BLANK_HEADER_XML, "rIdTestimonyHeaderBlank", "header"),
    "footer1.xml": (FOOTER_XML, "rIdTestimonyFooter", "footer"),
    "footer2.xml": (BLANK_FOOTER_XML, "rIdTestimonyFooterBlank", "footer"),
}

# ---------------------------------------------------------------------------
# styles.xml: full replacement for Pandoc's default reference doc
# ---------------------------------------------------------------------------
# Sizes are half-points (24 = 12 pt). line="480" lineRule="auto" is double
# spacing. A 9 pt paragraph gap is after="180".
#
# Spacing note: the filed example puts 9 pt between consecutive Q/A/body
# paragraphs, and 18 pt above each section heading (9 pt from the previous
# paragraph's "after" plus 9 pt from the heading's "before"). So every body
# style is before=0/after=180 and Heading 1 is before=180/after=180.
_TNR = '<w:rFonts w:ascii="Times New Roman" w:eastAsia="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
_BODY_SPACING = '<w:spacing w:before="0" w:after="180" w:line="480" w:lineRule="auto"/>'
# OOXML requires pPr children in schema order (spacing, then ind, then jc).
_BODY_PPR = _BODY_SPACING + '<w:jc w:val="left"/>'


def _style(
    style_id: str,
    name: str,
    *,
    based_on: str | None = "Normal",
    next_style: str | None = None,
    ppr: str = "",
    rpr: str = "",
    kind: str = "paragraph",
    custom: bool = False,
    default: bool = False,
    link: str | None = None,
    qformat: bool = True,
    priority: int | None = None,
) -> str:
    attrs = f'w:type="{kind}"'
    if default:
        attrs += ' w:default="1"'
    if custom:
        attrs += ' w:customStyle="1"'
    attrs += f' w:styleId="{style_id}"'
    parts = [f'<w:name w:val="{name}"/>']
    if based_on:
        parts.append(f'<w:basedOn w:val="{based_on}"/>')
    if next_style:
        parts.append(f'<w:next w:val="{next_style}"/>')
    if link:
        parts.append(f'<w:link w:val="{link}"/>')
    if priority is not None:
        parts.append(f'<w:uiPriority w:val="{priority}"/>')
    if qformat:
        parts.append("<w:qFormat/>")
    if ppr:
        parts.append(f"<w:pPr>{ppr}</w:pPr>")
    if rpr:
        parts.append(f"<w:rPr>{rpr}</w:rPr>")
    return f"<w:style {attrs}>{''.join(parts)}</w:style>"


def _build_styles_xml() -> str:
    s: list[str] = []
    add = s.append

    add(
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f"<w:styles {_NS}>"
        f'<w:docDefaults><w:rPrDefault><w:rPr>{_TNR}<w:sz w:val="24"/><w:szCs w:val="24"/>'
        '<w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
        '<w:pPrDefault><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
        '<w:jc w:val="left"/></w:pPr></w:pPrDefault></w:docDefaults>'
        '<w:latentStyles w:defLockedState="0" w:defUIPriority="0" w:defSemiHidden="0" '
        'w:defUnhideWhenUsed="0" w:defQFormat="0" w:count="276"/>'
    )
    add(_style("Normal", "Normal", based_on=None, default=True))
    add(
        '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/><w:uiPriority w:val="1"/><w:semiHidden/></w:style>'
    )
    add(
        '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
        '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
        '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
    )
    add(
        '<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/><w:uiPriority w:val="99"/><w:semiHidden/></w:style>'
    )

    # --- Body text -------------------------------------------------------
    # Pandoc applies BodyText to ordinary paragraphs, FirstParagraph to the
    # first one after a heading, and Compact to tight list items. All are
    # double-spaced with the 9 pt gap (the example's bullets are too).
    add(_style("BodyText", "Body Text", ppr=_BODY_PPR))
    add(_style("FirstParagraph", "First Paragraph", based_on="BodyText", next_style="BodyText", custom=True))
    add(_style("Compact", "Compact", based_on="BodyText", custom=True))

    # Q&A. Marker at the margin, a tab to 0.5", wrapped lines at 0.5".
    qa_ppr = (
        '<w:tabs><w:tab w:val="left" w:pos="720"/></w:tabs>'
        + _BODY_SPACING
        + '<w:ind w:left="720" w:hanging="720"/><w:jc w:val="left"/>'
    )
    add(
        _style(
            "Question",
            "Question",
            based_on="BodyText",
            next_style="Answer",
            custom=True,
            ppr="<w:keepNext/>" + qa_ppr,
            rpr="<w:b/><w:bCs/>",
        )
    )
    add(_style("Answer", "Answer", based_on="BodyText", next_style="AnswerContinuation", custom=True, ppr=qa_ppr))
    # Follow-on paragraphs of one answer: aligned at 0.5", no first-line indent.
    cont_ppr = _BODY_SPACING + '<w:ind w:left="720"/><w:jc w:val="left"/>'
    add(
        _style(
            "AnswerContinuation",
            "Answer Continuation",
            based_on="BodyText",
            next_style="AnswerContinuation",
            custom=True,
            ppr=cont_ppr,
        )
    )
    add(
        _style(
            "QuestionContinuation",
            "Question Continuation",
            based_on="AnswerContinuation",
            next_style="QuestionContinuation",
            custom=True,
            rpr="<w:b/><w:bCs/>",
        )
    )

    # --- Headings --------------------------------------------------------
    # H1: "I.<tab>Introduction". Numeral right-aligned at 0.25" (right tab at
    # 360), text at 0.5" (hanging indent). The underline is on the words only.
    add(
        _style(
            "Heading1",
            "heading 1",
            next_style="BodyText",
            link="Heading1Char",
            priority=9,
            ppr='<w:keepNext/><w:keepLines/><w:tabs><w:tab w:val="right" w:pos="360"/><w:tab w:val="left" w:pos="720"/></w:tabs>'
            '<w:spacing w:before="180" w:after="180" w:line="480" w:lineRule="auto"/><w:ind w:left="720" w:hanging="720"/>'
            '<w:jc w:val="left"/><w:outlineLvl w:val="0"/>',
            rpr="<w:b/><w:bCs/>",
        )
    )
    add(
        _style(
            "Heading1Char",
            "Heading 1 Char",
            based_on="DefaultParagraphFont",
            kind="character",
            custom=True,
            link="Heading1",
            qformat=False,
            rpr="<w:b/><w:bCs/>",
        )
    )
    # H2 ("A.<tab>Subheading") and H3 ("1)<tab>Sub-subheading"): italic, indented.
    add(
        _style(
            "Heading2",
            "heading 2",
            next_style="BodyText",
            priority=9,
            ppr='<w:keepNext/><w:keepLines/><w:spacing w:before="40" w:after="180" w:line="480" w:lineRule="auto"/>'
            '<w:ind w:left="1080" w:hanging="360"/><w:outlineLvl w:val="1"/>',
            rpr="<w:i/><w:iCs/>",
        )
    )
    add(
        _style(
            "Heading3",
            "heading 3",
            next_style="BodyText",
            priority=9,
            ppr='<w:keepNext/><w:keepLines/><w:spacing w:before="40" w:after="180" w:line="480" w:lineRule="auto"/>'
            '<w:ind w:left="1080" w:hanging="720"/><w:outlineLvl w:val="2"/>',
            rpr="<w:i/><w:iCs/>",
        )
    )
    add(
        _style(
            "Heading4",
            "heading 4",
            next_style="BodyText",
            priority=9,
            ppr='<w:keepNext/><w:spacing w:before="40" w:after="180" w:line="480" w:lineRule="auto"/><w:outlineLvl w:val="3"/>',
            rpr="<w:b/><w:bCs/>",
        )
    )

    # --- Block quotes, figures, tables, captions -----------------------
    add(
        _style(
            "BlockText",
            "Block Text",
            next_style="BodyText",
            ppr='<w:spacing w:before="0" w:after="180" w:line="240" w:lineRule="auto"/><w:ind w:left="720" w:right="720"/><w:jc w:val="left"/>',
        )
    )
    fig_ppr = '<w:keepNext/><w:suppressLineNumbers/><w:spacing w:before="180" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>'
    add(_style("Figure", "Figure", next_style="ImageCaption", custom=True, ppr=fig_ppr))
    add(_style("CaptionedFigure", "Captioned Figure", based_on="Figure", next_style="ImageCaption", custom=True))
    # Captions: italic, single-spaced, indented 0.5" (as in the example).
    add(
        _style(
            "Caption",
            "caption",
            next_style="BodyText",
            priority=35,
            ppr='<w:spacing w:before="60" w:after="180" w:line="240" w:lineRule="auto"/><w:ind w:left="720"/><w:jc w:val="left"/>',
            rpr="<w:i/><w:iCs/>",
        )
    )
    add(_style("ImageCaption", "Image Caption", based_on="Caption", custom=True))
    add(_style("TableCaption", "Table Caption", based_on="Caption", custom=True, ppr="<w:keepNext/>"))
    # Table cells: single-spaced and tight (Pandoc would otherwise use the
    # double-spaced Compact style that bullets need). testimony.lua applies this.
    add(
        _style(
            "TableText",
            "Table Text",
            custom=True,
            ppr='<w:spacing w:before="40" w:after="40" w:line="240" w:lineRule="auto"/>',
        )
    )
    add(
        '<w:style w:type="table" w:customStyle="1" w:styleId="Table"><w:name w:val="Table"/>'
        '<w:basedOn w:val="TableNormal"/><w:uiPriority w:val="99"/><w:qFormat/><w:tblPr><w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        "</w:tblBorders></w:tblPr></w:style>"
    )

    # --- Footnotes -------------------------------------------------------
    # 11 pt, single-spaced, no line numbers (footnotes are never numbered).
    add(
        _style(
            "FootnoteText",
            "footnote text",
            link="FootnoteTextChar",
            priority=99,
            ppr='<w:suppressLineNumbers/><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="left"/>',
            rpr='<w:sz w:val="22"/><w:szCs w:val="22"/>',
        )
    )
    add(
        _style(
            "FootnoteTextChar",
            "Footnote Text Char",
            based_on="DefaultParagraphFont",
            kind="character",
            custom=True,
            link="FootnoteText",
            qformat=False,
            rpr='<w:sz w:val="22"/><w:szCs w:val="22"/>',
        )
    )
    add(
        _style(
            "FootnoteReference",
            "footnote reference",
            based_on="DefaultParagraphFont",
            kind="character",
            qformat=False,
            rpr='<w:vertAlign w:val="superscript"/>',
        )
    )
    # Pandoc tags every link run with this style; without it, links render as plain text.
    add(
        _style(
            "Hyperlink",
            "Hyperlink",
            based_on="DefaultParagraphFont",
            kind="character",
            qformat=False,
            priority=99,
            rpr='<w:color w:val="0563C1"/><w:u w:val="single"/>',
        )
    )

    # --- Header, footer, cover -------------------------------------------
    hf_tabs = '<w:tabs><w:tab w:val="center" w:pos="4680"/><w:tab w:val="right" w:pos="9360"/></w:tabs>'
    add(
        _style(
            "Header",
            "header",
            link="HeaderChar",
            priority=99,
            qformat=False,
            ppr=hf_tabs + '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="right"/>',
        )
    )
    add(
        _style(
            "HeaderChar",
            "Header Char",
            based_on="DefaultParagraphFont",
            kind="character",
            custom=True,
            link="Header",
            qformat=False,
        )
    )
    add(
        _style(
            "Footer",
            "footer",
            priority=99,
            qformat=False,
            ppr=hf_tabs + '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/>',
        )
    )
    # Cover blocks: bold, centered, single-spaced, never line-numbered.
    add(
        _style(
            "CoverPage",
            "Cover Page",
            next_style="BodyText",
            custom=True,
            ppr='<w:suppressLineNumbers/><w:spacing w:before="0" w:after="240" w:line="276" w:lineRule="auto"/><w:jc w:val="center"/>',
            rpr="<w:b/><w:bCs/>",
        )
    )
    add(
        _style(
            "CoverCaption",
            "Cover Caption",
            custom=True,
            ppr='<w:suppressLineNumbers/><w:spacing w:before="0" w:after="0" w:line="276" w:lineRule="auto"/><w:jc w:val="left"/>',
        )
    )
    # Pandoc still references these for the (suppressed) YAML title block.
    for sid, nm in (("Title", "Title"), ("Subtitle", "Subtitle"), ("Author", "Author"), ("Date", "Date")):
        add(
            _style(
                sid,
                nm,
                next_style="BodyText",
                ppr='<w:suppressLineNumbers/><w:jc w:val="center"/>',
                rpr="<w:b/><w:bCs/>",
            )
        )

    add("</w:styles>")
    return "".join(s)


STYLES_XML = _build_styles_xml()

# ---------------------------------------------------------------------------
# Patches applied to the other parts of Pandoc's default reference doc
# ---------------------------------------------------------------------------


def _patch_document_xml(xml: str) -> str:
    """Replace the body's trailing <w:sectPr> with our body-section one.

    Pandoc preserves whatever <w:sectPr> sits at the end of the reference
    doc's body, so this is how page size, margins, line numbering, page
    numbering and the header/footer references reach every rendered file.
    Also declares the ``r:`` namespace so the ``r:id`` references resolve.
    """
    if "<w:sectPr />" in xml:
        xml = xml.replace("<w:sectPr />", SECTPR_XML, 1)
    elif "<w:sectPr/>" in xml:
        xml = xml.replace("<w:sectPr/>", SECTPR_XML, 1)
    else:
        xml = re.sub(
            r"<w:sectPr\b[^>]*>.*?</w:sectPr>|<w:sectPr\b[^/]*/>",
            SECTPR_XML,
            xml,
            count=1,
            flags=re.DOTALL,
        )
    if 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"' not in xml:
        xml = xml.replace(
            "<w:document ",
            '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ',
            1,
        )
    return xml


def _patch_document_rels(xml: str) -> str:
    """Add the relationships for our header and footer parts."""
    inject = ""
    for part, (_xml, rid, kind) in HEADER_FOOTER_PARTS.items():
        rel = f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/{kind}" Target="{part}"/>'
        if rel not in xml:
            inject += rel
    return xml.replace("</Relationships>", inject + "</Relationships>", 1) if inject else xml


def _patch_content_types(xml: str) -> str:
    """Register the header and footer content types."""
    inject = ""
    for part, (_xml, _rid, kind) in HEADER_FOOTER_PARTS.items():
        override = f'<Override PartName="/word/{part}" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.{kind}+xml"/>'
        if override not in xml:
            inject += override
    return xml.replace("</Types>", inject + "</Types>", 1) if inject else xml


def _pandoc_cmd() -> list[str]:
    """Return a command that runs Pandoc (standalone, or the one bundled with Quarto)."""
    if shutil.which("pandoc"):
        return ["pandoc"]
    return ["quarto", "pandoc"]


def build(output: Path = OUTPUT) -> Path:
    """Build the model file by patching Pandoc's default reference doc."""
    base = Path(tempfile.mkdtemp(prefix="switchbox_pandoc_ref_")) / "_pandoc_default.docx"
    print(f"⚙️  Fetching Pandoc default reference doc → {base}")
    with base.open("wb") as fh:
        subprocess.run([*_pandoc_cmd(), "--print-default-data-file", "reference.docx"], check=True, stdout=fh)

    if output.exists():
        output.unlink()

    header_xml = HEADER_XML
    for i, default in enumerate(DEFAULT_HEADER_LINES, start=1):
        header_xml = header_xml.replace(f"{{{{HEADER_LINE_{i}}}}}", default)

    print(f"⚙️  Writing patched template → {output}")
    seen: set[str] = set()
    with zipfile.ZipFile(base) as src, zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            name = item.filename
            data = src.read(name)
            part = name.removeprefix("word/")
            if name == "word/styles.xml":
                dst.writestr(item, STYLES_XML)
            elif name == "word/document.xml":
                dst.writestr(item, _patch_document_xml(data.decode("utf-8")))
            elif name == "word/_rels/document.xml.rels":
                dst.writestr(item, _patch_document_rels(data.decode("utf-8")))
            elif name == "[Content_Types].xml":
                dst.writestr(item, _patch_content_types(data.decode("utf-8")))
            elif part in HEADER_FOOTER_PARTS:
                xml = header_xml if part == "header1.xml" else HEADER_FOOTER_PARTS[part][0]
                dst.writestr(item, xml)
                seen.add(part)
            else:
                dst.writestr(item, data)
        for part, (xml, _rid, _kind) in HEADER_FOOTER_PARTS.items():
            if part not in seen:
                dst.writestr(f"word/{part}", header_xml if part == "header1.xml" else xml)

    shutil.rmtree(base.parent, ignore_errors=True)
    print(f"✅ Wrote {output} ({output.stat().st_size:,} bytes)")
    return output


if __name__ == "__main__":
    try:
        build()
    except subprocess.CalledProcessError as exc:  # pragma: no cover - cli only
        print(f"💥 pandoc failed: {exc}", file=sys.stderr)
        sys.exit(1)
