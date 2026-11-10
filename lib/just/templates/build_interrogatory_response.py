#!/usr/bin/env python3
"""Build the interrogatory-response Word model file (Pandoc "reference doc").

Modelled on CLF and Sierra Club's filed CIEC-1 response in PURA Docket 26-05-10
(Nov. 4, 2026): Times New Roman 12 pt, single-spaced, 1" margins, a right-
aligned header block at the top of every page, then Date Filed / Witness /
Request from, "Question:" and "Response:".

* No cover page, no line numbers (unlike expert testimony).
* The header is written per response by ``lib.just.interrogatory`` after the
  render, so the header part baked in here is only a stand-in for the closing
  section.
* Every response is its own Word section that restarts page
  numbering at 1 (``pgNumType start=1`` in the closing section here and in the
  section breaks written by ``interrogatory.lua``).

Run via::

    uv run python -m lib.just.templates.build_interrogatory_response

This writes ``interrogatory_response.docx`` next to this script; commit the
result. ``lib.just.interrogatory`` hands it to Quarto as ``--reference-doc``.
Styles come from the testimony builder's helpers so the two formats share one
way of writing Word styles.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from lib.just.templates.build_expert_testimony import _NS, _TNR, _pandoc_cmd, _style

HERE = Path(__file__).parent
OUTPUT = HERE / "interrogatory_response.docx"

SECTPR_XML = """<w:sectPr>
    <w:headerReference w:type="default" r:id="rIdIRHeader"/>
    <w:pgSz w:w="12240" w:h="15840" w:code="1"/>
    <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    <w:pgNumType w:start="1"/>
    <w:cols w:space="720"/>
    <w:docGrid w:linePitch="360"/>
  </w:sectPr>"""

HEADER_XML = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr {_NS}>
  <w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr><w:r><w:t>[RESPONSE HEADER]</w:t></w:r></w:p>
</w:hdr>
"""

HEADER_FOOTER_PARTS = {"header1.xml": (HEADER_XML, "rIdIRHeader", "header")}

_SINGLE = '<w:spacing w:before="0" w:after="120" w:line="240" w:lineRule="auto"/>'


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
        '<w:style w:type="character" w:default="1" w:styleId="DefaultParagraphFont"><w:name w:val="Default Paragraph Font"/>'
        '<w:uiPriority w:val="1"/><w:semiHidden/></w:style>'
    )
    add(
        '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
        '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
        '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'
    )
    add(
        '<w:style w:type="numbering" w:default="1" w:styleId="NoList"><w:name w:val="No List"/>'
        '<w:uiPriority w:val="99"/><w:semiHidden/></w:style>'
    )

    # Body text: single-spaced with a 6 pt gap, as in the filed response.
    add(_style("BodyText", "Body Text", ppr=_SINGLE))
    add(_style("FirstParagraph", "First Paragraph", based_on="BodyText", next_style="BodyText", custom=True))
    add(
        _style(
            "Compact",
            "Compact",
            based_on="BodyText",
            custom=True,
            ppr='<w:spacing w:before="0" w:after="60" w:line="240" w:lineRule="auto"/>',
        )
    )

    # Date Filed / Witness / Request from: label, a tab, then the value; wrapped
    # lines hang under the value.
    add(
        _style(
            "IRMeta",
            "IR Meta",
            custom=True,
            ppr='<w:tabs><w:tab w:val="left" w:pos="1584"/></w:tabs>'
            '<w:spacing w:before="0" w:after="60" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:left="1584" w:hanging="1584"/>',
        )
    )
    # "Question:" and "Response:" labels.
    add(
        _style(
            "IRLabel",
            "IR Label",
            custom=True,
            next_style="BodyText",
            ppr='<w:keepNext/><w:spacing w:before="240" w:after="60" w:line="240" w:lineRule="auto"/>',
        )
    )
    add(
        _style(
            "IRTestimonyHeading",
            "IR Testimony Heading",
            custom=True,
            ppr='<w:spacing w:before="120" w:after="80" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:left="360" w:right="0"/>',
            rpr='<w:i/><w:iCs/><w:color w:val="595959"/><w:sz w:val="20"/><w:szCs w:val="20"/>',
        )
    )
    add(
        _style(
            "IRTestimonyPassage",
            "IR Testimony Passage",
            custom=True,
            ppr='<w:spacing w:before="160" w:after="40" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:left="360" w:right="0"/>',
            rpr='<w:b/><w:bCs/><w:color w:val="404040"/><w:sz w:val="20"/><w:szCs w:val="20"/>',
        )
    )
    # IRTestimonyLine kept for fallback; normal rows use a two-column OpenXML table in the Lua filter.
    add(
        _style(
            "IRTestimonyLine",
            "IR Testimony Line",
            based_on="BodyText",
            custom=True,
            ppr='<w:tabs><w:tab w:val="left" w:pos="1080"/></w:tabs>'
            '<w:spacing w:before="0" w:after="40" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:left="1080" w:hanging="1080" w:right="0"/>',
            rpr='<w:color w:val="404040"/><w:sz w:val="20"/><w:szCs w:val="20"/>',
        )
    )

    add(
        _style(
            "BlockText",
            "Block Text",
            next_style="BodyText",
            ppr='<w:spacing w:before="0" w:after="120" w:line="240" w:lineRule="auto"/><w:ind w:left="720" w:right="720"/>',
        )
    )
    add(_style("Figure", "Figure", next_style="ImageCaption", custom=True, ppr='<w:keepNext/><w:jc w:val="center"/>'))
    add(_style("CaptionedFigure", "Captioned Figure", based_on="Figure", next_style="ImageCaption", custom=True))
    add(
        _style(
            "Caption",
            "caption",
            next_style="BodyText",
            priority=35,
            ppr='<w:spacing w:before="60" w:after="120" w:line="240" w:lineRule="auto"/>',
            rpr="<w:i/><w:iCs/>",
        )
    )
    add(_style("ImageCaption", "Image Caption", based_on="Caption", custom=True))
    add(_style("TableCaption", "Table Caption", based_on="Caption", custom=True, ppr="<w:keepNext/>"))
    add(
        '<w:style w:type="table" w:customStyle="1" w:styleId="Table"><w:name w:val="Table"/>'
        '<w:basedOn w:val="TableNormal"/><w:uiPriority w:val="99"/><w:qFormat/><w:tblPr><w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        "</w:tblBorders></w:tblPr></w:style>"
    )

    # Footnotes (citations are written out in full in footnotes, as in testimony).
    add(
        _style(
            "FootnoteText",
            "footnote text",
            link="FootnoteTextChar",
            priority=99,
            ppr='<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>',
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

    # Header block: right-aligned, 11 pt.
    add(
        _style(
            "Header",
            "header",
            link="HeaderChar",
            priority=99,
            qformat=False,
            ppr='<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="right"/>',
            rpr='<w:sz w:val="22"/><w:szCs w:val="22"/>',
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
    add(_style("Footer", "footer", priority=99, qformat=False, ppr='<w:jc w:val="center"/>'))
    # Pandoc still references these for the (suppressed) YAML title block.
    for sid, nm in (("Title", "Title"), ("Subtitle", "Subtitle"), ("Author", "Author"), ("Date", "Date")):
        add(_style(sid, nm, next_style="BodyText", ppr='<w:jc w:val="center"/>', rpr="<w:b/><w:bCs/>"))
    add("</w:styles>")
    return "".join(s)


STYLES_XML = _build_styles_xml()


def _patch_document_xml(xml: str) -> str:
    """Replace the body's closing <w:sectPr> (Pandoc keeps it in every render)."""
    xml = re.sub(r"<w:sectPr\b[^>]*/>|<w:sectPr\b[^>]*>.*?</w:sectPr>", SECTPR_XML, xml, count=1, flags=re.DOTALL)
    if 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"' not in xml:
        xml = xml.replace(
            "<w:document ",
            '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ',
            1,
        )
    return xml


def _patch_rels(xml: str) -> str:
    inject = ""
    for part, (_xml, rid, kind) in HEADER_FOOTER_PARTS.items():
        rel = (
            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/{kind}" '
            f'Target="{part}"/>'
        )
        if rel not in xml:
            inject += rel
    return xml.replace("</Relationships>", inject + "</Relationships>", 1) if inject else xml


def _patch_content_types(xml: str) -> str:
    inject = ""
    for part, (_xml, _rid, kind) in HEADER_FOOTER_PARTS.items():
        override = (
            f'<Override PartName="/word/{part}" '
            f'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.{kind}+xml"/>'
        )
        if override not in xml:
            inject += override
    return xml.replace("</Types>", inject + "</Types>", 1) if inject else xml


def build(output: Path = OUTPUT) -> Path:
    """Build the model file by patching Pandoc's default reference doc."""
    base = Path(tempfile.mkdtemp(prefix="switchbox_pandoc_ref_")) / "_pandoc_default.docx"
    print(f"⚙️  Fetching Pandoc default reference doc → {base}")
    with base.open("wb") as fh:
        subprocess.run([*_pandoc_cmd(), "--print-default-data-file", "reference.docx"], check=True, stdout=fh)
    if output.exists():
        output.unlink()

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
                dst.writestr(item, _patch_rels(data.decode("utf-8")))
            elif name == "[Content_Types].xml":
                dst.writestr(item, _patch_content_types(data.decode("utf-8")))
            elif part in HEADER_FOOTER_PARTS:
                dst.writestr(item, HEADER_FOOTER_PARTS[part][0])
                seen.add(part)
            else:
                dst.writestr(item, data)
        for part, (xml, _rid, _kind) in HEADER_FOOTER_PARTS.items():
            if part not in seen:
                dst.writestr(f"word/{part}", xml)
    shutil.rmtree(base.parent, ignore_errors=True)
    print(f"✅ Wrote {output} ({output.stat().st_size:,} bytes)")
    return output


if __name__ == "__main__":
    try:
        build()
    except subprocess.CalledProcessError as exc:  # pragma: no cover - cli only
        print(f"💥 pandoc failed: {exc}", file=sys.stderr)
        sys.exit(1)
