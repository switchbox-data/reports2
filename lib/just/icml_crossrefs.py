#!/usr/bin/env python3
"""Post-process ICML: turn ``@sec-*`` hyperlinks into live InDesign cross-refs (page numbers).

Pandoc's ICML writer emits internal section refs as ``<HyperlinkTextSource>`` + a
``<Hyperlink>`` to ``<HyperlinkTextDestination/#sec-...>`` — a static jump link
with the resolved section *number* in the text (e.g. "Section 4.2.4"). For
InDesign we replace each such source with ``<CrossReferenceSource>`` plus a
``<CrossReferenceFormat>`` that uses a ``PageNumberBuildingBlock`` so the placed
ICML can show "p. N" and auto-update on reflow after the designer runs
**Update All Cross-References** once.

Only destinations whose anchor starts with ``#sec-`` are converted. Figure,
table, equation, and citation internal links are left unchanged.

See: https://github.com/jgm/pandoc/issues/5541
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# One CrossReferenceFormat shared by all @sec- refs: "p. " + page number
# ---------------------------------------------------------------------------

_CRF_SELF = "CrossReferenceFormat/sbx-page-p"

_CRF_INJECT = (
    f'  <CrossReferenceFormat Self="{_CRF_SELF}" Name="p. (page #)" '
    f'AppliedCharacterStyle="n">\n'
    f'    <BuildingBlock Self="{_CRF_SELF}-BB0" BlockType="CustomStringBuildingBlock" '
    f'AppliedCharacterStyle="n" CustomText="p. " '
    f'AppliedDelimiter="$ID/" IncludeDelimiter="false" />\n'
    f'    <BuildingBlock Self="{_CRF_SELF}-BB1" BlockType="PageNumberBuildingBlock" '
    f'AppliedCharacterStyle="n" CustomText="$ID/" '
    f'AppliedDelimiter="$ID/" IncludeDelimiter="false" />\n'
    f"  </CrossReferenceFormat>\n"
)

# A single <Hyperlink>...</Hyperlink> block (non-greedy; ICML does not nest these).
_HYPERLINK_WRAPPER = re.compile(r"<Hyperlink\s+[^>]+>.*?</Hyperlink>", re.DOTALL)


# Source id and destination anchor from the Hyperlink's Properties.
def _hyperlink_source_and_sec_anchor(block: str) -> tuple[str, str] | None:
    sm = re.search(r'Source="(htss-\d+)"', block)
    dm = re.search(
        r'<Destination\s+type="object">HyperlinkTextDestination/(#sec-[^<]+)</Destination>',
        block,
    )
    if sm and dm:
        return sm.group(1), dm.group(1)
    return None


# <HyperlinkTextSource Self="htss-N" ...> ... </HyperlinkTextSource>
_HTS_BLOCK = re.compile(
    r'<HyperlinkTextSource\s+Self="(htss-\d+)"([^>]*?)\s*>'
    r"([\s\S]*?)</HyperlinkTextSource>",
    re.DOTALL,
)


def _inject_crf(icml: str) -> str:
    """Inject the CrossReferenceFormat as a Document-level sibling of the style groups.

    CrossReferenceFormat must live at Document scope (not inside any
    RootStyleGroup), so we place it right after ``</RootCellStyleGroup>``
    and before the first ``<Story>``.
    """
    if _CRF_SELF in icml:
        return icml
    if "</RootCellStyleGroup>" not in icml:
        return icml
    return icml.replace(
        "</RootCellStyleGroup>",
        "</RootCellStyleGroup>\n" + _CRF_INJECT.rstrip("\n"),
        1,
    )


def _collect_sec_source_to_anchor(icml: str) -> dict[str, str]:
    """Map ``htss-N`` -> ``#sec-...`` for hyperlinks that target a section anchor."""
    out: dict[str, str] = {}
    for block in _HYPERLINK_WRAPPER.finditer(icml):
        m = _hyperlink_source_and_sec_anchor(block.group(0))
        if m:
            out[m[0]] = m[1]
    return out


def _rewrite_hts(
    m: re.Match[str],
    sec_map: dict[str, str],
) -> str:
    source_id = m.group(1)
    rest = m.group(2)
    body = m.group(3)

    if source_id not in sec_map:
        return m.group(0)

    anchor = sec_map[source_id]
    # Drop an existing empty/wrong Name= on the source; the Hyperlink's Name
    # should match the text-anchor id for a clean InDesign link list.
    rest_clean = re.sub(r"\s*Name=\"[^\"]*\"", "", rest)

    new_open = f'<CrossReferenceSource Self="{source_id}" AppliedFormat="{_CRF_SELF}" Name="{anchor}"{rest_clean}>'

    # Placeholder; InDesign replaces with "p. N" after Update All Cross-References.
    new_body = re.sub(
        r"<Content>[^<]*</Content>",
        "<Content>p. ??</Content>",
        body,
        count=1,
    )
    if new_body == body:
        new_body = re.sub(
            r"(<CharacterStyleRange[^>]+>)",
            r"\1<Content>p. ??</Content>\n    ",
            body,
            count=1,
        )

    return f"{new_open}{new_body}</CrossReferenceSource>"


def convert(icml: str) -> str:
    """Rewrite ICML: ``HyperlinkTextSource`` for ``#sec-*`` -> ``CrossReferenceSource``."""
    if "HyperlinkTextDestination/#sec-" not in icml:
        return icml

    sec_map = _collect_sec_source_to_anchor(icml)
    if not sec_map:
        return icml

    icml = _inject_crf(icml)
    if _CRF_SELF not in icml:
        return icml

    return _HTS_BLOCK.sub(
        lambda m: _rewrite_hts(m, sec_map),
        icml,
    )


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m lib.just.icml_crossrefs <path.icml>", file=sys.stderr)
        sys.exit(1)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)
    text = path.read_text(encoding="utf-8")
    n_before = text.count("<HyperlinkTextSource")
    text = convert(text)
    n_after = text.count("<CrossReferenceSource")
    path.write_text(text, encoding="utf-8")
    print(
        f"Wrote {path} (sec cross-refs: {n_after} CrossReferenceSource; "
        f"remaining HyperlinkTextSource: {text.count('<HyperlinkTextSource')})",
    )


if __name__ == "__main__":
    main()
