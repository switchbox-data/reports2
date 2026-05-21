#!/usr/bin/env python3
"""Render a Quarto report to DOCX for content review.

Handles the full pipeline that ``just draft`` needs:

1. For non-article files in a Manuscript project (anything other than
   ``index.qmd`` when ``_quarto.yml`` exists), temporarily moves the
   project config so Quarto treats the file as standalone.
2. Purges the freeze cache and rendered notebook outputs so embedded
   notebooks re-execute with raster settings (PNG figures, GT-as-image).
3. Sets ``SWITCHBOX_GT_AS_IMAGE=1`` so ``display_gt`` and
   ``theme_switchbox`` produce high-res PNGs instead of HTML/SVG.
4. Runs ``quarto render`` with ``--to docx``, ``fig-dpi:300``, and
   ``fig-format:png`` for print-quality output.

Optional ``--testimony`` flag applies an expert-testimony reference
template (Times New Roman 12pt, double-spaced body, line numbering,
formal headings) located at ``lib/just/templates/expert_testimony.docx``.

Usage (from a report directory)::

    uv run python -m lib.just.draft                       # index.qmd
    uv run python -m lib.just.draft expert_testimony.qmd  # specific file
    uv run python -m lib.just.draft --testimony foo.qmd   # apply template
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import date
from pathlib import Path

import yaml

# Reference template for expert testimony formatting (ICC-style: Times
# New Roman 12pt, double-spaced, line-numbered, witness header).
TESTIMONY_TEMPLATE = Path(__file__).parent / "templates" / "expert_testimony.docx"
# Pandoc Lua filter for testimony-specific transforms (suppress YAML
# title block, tabular Q&A, body-section break for line-number reset).
TESTIMONY_LUA_FILTER = Path(__file__).parent / "templates" / "filters" / "testimony.lua"


def _output_name(qmd_path: Path) -> str:
    """Generate a date-stamped DOCX filename from the source .qmd."""
    stem = qmd_path.stem if qmd_path.stem != "index" else "report_draft"
    return f"{stem}_{date.today():%Y%m%d}.docx"


@contextmanager
def _hide_quarto_yml() -> Iterator[None]:
    """Temporarily move _quarto.yml out of the way, restoring on exit.

    Quarto Manuscript projects only produce DOCX for the main article
    (``index.qmd``).  For other files (e.g. ``expert_testimony.qmd``),
    the project config must be absent so Quarto renders standalone.
    """
    quarto_yml = Path("_quarto.yml")
    backup = Path("_quarto.yml.draft_bak")

    if not quarto_yml.exists():
        yield
        return

    quarto_yml.rename(backup)
    try:
        yield
    finally:
        if backup.exists():
            backup.rename(quarto_yml)


def _clear_notebook_cache() -> None:
    """Purge freeze cache and rendered notebook outputs.

    Ensures embedded notebooks re-execute with ``SWITCHBOX_GT_AS_IMAGE=1``
    active, producing high-res PNGs instead of reusing stale SVG/HTML
    outputs from a previous ``just render`` (HTML) build.
    """
    cleared = []

    freeze_root = Path(".quarto/_freeze")
    if freeze_root.is_dir():
        shutil.rmtree(freeze_root)
        cleared.append(str(freeze_root))

    nb_docs = Path("docs/notebooks")
    if nb_docs.is_dir():
        shutil.rmtree(nb_docs)
        cleared.append(str(nb_docs))

    if cleared:
        print(f"📄 Cleared cached outputs: {', '.join(cleared)}", flush=True)


_YAML_FENCE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _read_yaml_frontmatter(qmd_path: Path) -> dict:
    """Return the parsed YAML frontmatter of a .qmd, or {} if absent."""
    text = qmd_path.read_text(encoding="utf-8")
    match = _YAML_FENCE.match(text)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _testimony_header_values(meta: dict) -> tuple[str, str]:
    """Pick exhibit / witness name out of QMD YAML, with sensible fallbacks.

    YAML conventions supported (in order of precedence):

    * Top-level ``exhibit`` / ``witness`` strings.
    * A ``testimony:`` block with ``exhibit:`` and/or ``witness:`` keys.
    * ``author[0].name`` for the witness name when not otherwise set.
    """
    testimony_block = meta.get("testimony") or {}
    if not isinstance(testimony_block, dict):
        testimony_block = {}

    exhibit = meta.get("exhibit") or testimony_block.get("exhibit") or "[EXHIBIT NUMBER]"

    witness = meta.get("witness") or testimony_block.get("witness")
    if not witness:
        authors = meta.get("author")
        if isinstance(authors, list) and authors:
            first = authors[0]
            if isinstance(first, dict):
                witness = first.get("name")
            elif isinstance(first, str):
                witness = first
        elif isinstance(authors, dict):
            witness = authors.get("name")
        elif isinstance(authors, str):
            witness = authors
    if not witness:
        witness = "[WITNESS NAME]"

    return str(exhibit), str(witness)


_MONTH_NAMES = "January|February|March|April|May|June|July|August|September|October|November|December"


def _fix_caption_alignment(xml: str) -> str:
    """Force figure captions to be centred (Issue 6).

    Pandoc's docx writer wraps figures in a 1x1 table and emits the
    caption paragraph with **two** ``<w:pPr>`` blocks in a single
    ``<w:p>``: an outer one with ``<w:jc w:val="center"/>`` (the table
    cell's default) and an inner one carrying the ``ImageCaption``
    pStyle plus an explicit ``<w:jc w:val="left"/>``.  Two ``pPr`` in
    one paragraph is invalid OOXML — Word picks the second, so the
    inline ``jc="left"`` overrides the style's ``jc="center"`` and the
    caption renders left-aligned.

    Drop the redundant outer ``pPr`` (it's the table-cell context the
    caption already inherits) and strip the inline ``jc="left"`` so
    the ``ImageCaption`` style's centring takes effect.  Done by raw
    regex against ``document.xml`` because the AST walker can't see the
    duplicate ``pPr`` — Pandoc writes it directly during AST→OOXML.
    """
    # 1) Drop the redundant outer <w:pPr><w:jc w:val="center"/></w:pPr>
    #    (only when it directly precedes another <w:pPr> on the same
    #    paragraph — that's the duplicate-pPr signature).
    xml = re.sub(
        r'<w:pPr>\s*<w:jc w:val="center"\s*/>\s*</w:pPr>(?=\s*<w:pPr>)',
        "",
        xml,
    )

    # 2) For every <w:pPr> that styles a caption, drop the inline
    #    jc="left" so the style's jc="center" is the only alignment
    #    directive left.
    def _strip_left_jc(match: re.Match) -> str:
        block = match.group(0)
        if '<w:pStyle w:val="ImageCaption"' in block or '<w:pStyle w:val="Caption"' in block:
            block = re.sub(r'<w:jc w:val="left"\s*/>', "", block)
        return block

    return re.sub(r"<w:pPr>.*?</w:pPr>", _strip_left_jc, xml, flags=re.DOTALL)


def _fix_zero_padded_dates(xml: str) -> str:
    """Drop the leading zero from days in dates like "May 05, 2026".

    The cover-page date is generated via R inline code in the QMD
    (``format(.., "%B %d, %Y")`` — ``%d`` is zero-padded).  Switchbox
    house style — and the ICC exemplar — write single-digit days
    without the leading zero (e.g. "May 5, 2026").  We can't fix this
    without editing the QMD's R format string, so we do the cosmetic
    fix here at the OOXML layer.  Matches only the month-name + day
    pattern, so we don't accidentally touch substrings like ``2026 05 05``.
    """
    return re.sub(
        rf"\b({_MONTH_NAMES})\s+0(\d)\b",
        r"\1 \2",
        xml,
    )


def _fix_numbering_indents(xml: str) -> str:
    """Widen ``<w:hanging>`` to match ``<w:left>`` for every list level.

    Pandoc generates new abstract-num definitions in
    ``word/numbering.xml`` for each list style it encounters; those
    inherit a 360-twip hanging indent that's too narrow for
    parenthesised roman markers like ``(iii)`` and ``(viii)``.
    Build-time we patch the reference docx's pre-existing definitions,
    but Pandoc-generated ones still need fixing — do it here, after
    the docx exists.  See ``_patch_numbering_xml`` in the build script
    for the rationale.
    """

    def _widen(match: re.Match) -> str:
        left = int(match.group("left"))
        return f'<w:ind w:left="{left}" w:hanging="{min(left, 720)}"/>'

    return re.sub(
        r'<w:ind w:left="(?P<left>\d+)" w:hanging="\d+"\s*/>',
        _widen,
        xml,
    )


def _postprocess_testimony_docx(output_path: Path) -> None:
    """Apply OOXML-layer fixes that Pandoc/AST filters can't reach.

    Three targeted rewrites:

    * ``document.xml`` — fix figure-caption alignment (Issue 6) and
      zero-padded cover dates (Issue 7).
    * ``word/numbering.xml`` — widen hanging indents on all list
      levels so multi-character markers stop colliding with the text
      column (Issue 4).

    Idempotent and safe to run on any docx (the regexes only fire on
    the patterns Pandoc actually emits).
    """
    if not output_path.exists():
        return

    tmp_path = output_path.with_suffix(".docx.postproc")

    fixes_applied: list[str] = []

    with (
        zipfile.ZipFile(output_path) as src,
        zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as dst,
    ):
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/document.xml":
                xml = data.decode("utf-8")
                before = xml
                xml = _fix_caption_alignment(xml)
                if xml != before:
                    fixes_applied.append("caption-alignment")
                before = xml
                xml = _fix_zero_padded_dates(xml)
                if xml != before:
                    fixes_applied.append("date-format")
                dst.writestr(item, xml.encode("utf-8"))
            elif item.filename == "word/numbering.xml":
                xml = data.decode("utf-8")
                before = xml
                xml = _fix_numbering_indents(xml)
                if xml != before:
                    fixes_applied.append("list-indents")
                dst.writestr(item, xml.encode("utf-8"))
            else:
                dst.writestr(item, data)

    tmp_path.replace(output_path)

    if fixes_applied:
        print(
            f"🩹 Post-processed testimony docx ({', '.join(fixes_applied)})",
            flush=True,
        )


def _materialize_testimony_template(qmd_path: Path) -> Path:
    """Return a temp copy of the template with header placeholders substituted.

    The on-disk template ships with ``{{EXHIBIT}}`` / ``{{WITNESS_NAME}}``
    in ``word/header1.xml``. This rewrites those tokens for the witness
    declared in the QMD's YAML and writes the patched template to a temp
    file so we don't mutate the shared on-disk template.
    """
    meta = _read_yaml_frontmatter(qmd_path)
    exhibit, witness = _testimony_header_values(meta)

    tmp_dir = Path(tempfile.mkdtemp(prefix="switchbox_testimony_"))
    tmp_path = tmp_dir / "expert_testimony.docx"

    with zipfile.ZipFile(TESTIMONY_TEMPLATE) as src, zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/header1.xml":
                hdr = data.decode("utf-8")
                # Replace bracketed defaults *and* mustache tokens so
                # this works whether the template was last built with
                # placeholders or with leftover values from a previous
                # render (idempotent).
                hdr = re.sub(r"\[EXHIBIT NUMBER\]|\{\{EXHIBIT\}\}", exhibit, hdr)
                hdr = re.sub(r"\[WITNESS NAME\]|\{\{WITNESS_NAME\}\}", witness, hdr)
                dst.writestr(item, hdr)
            else:
                dst.writestr(item, data)

    print(
        f"📜 Testimony header → exhibit={exhibit!r}, witness={witness!r}",
        flush=True,
    )
    return tmp_path


def draft(qmd_path: Path, *, testimony: bool = False) -> None:
    output_name = _output_name(qmd_path)
    is_non_article = qmd_path.name != "index.qmd"

    print(f"📄 Drafting {qmd_path} → {output_name}", flush=True)

    reference_doc: Path | None = None
    if testimony:
        if not TESTIMONY_TEMPLATE.exists():
            print(
                f"💥 Expert-testimony template not found: {TESTIMONY_TEMPLATE}",
                file=sys.stderr,
            )
            sys.exit(1)
        print(
            f"📜 Applying expert-testimony template: {TESTIMONY_TEMPLATE}",
            flush=True,
        )
        reference_doc = _materialize_testimony_template(qmd_path)

    _clear_notebook_cache()

    env = {**os.environ, "SWITCHBOX_GT_AS_IMAGE": "1"}
    cmd = [
        "quarto",
        "render",
        str(qmd_path),
        "--to",
        "docx",
        "-M",
        "fig-dpi:300",
        "-M",
        "fig-format:png",
        "--output",
        output_name,
    ]
    if reference_doc is not None:
        cmd += ["--reference-doc", str(reference_doc.resolve())]
    if testimony and TESTIMONY_LUA_FILTER.exists():
        cmd += ["--lua-filter", str(TESTIMONY_LUA_FILTER.resolve())]

    if is_non_article and Path("_quarto.yml").exists():
        with _hide_quarto_yml():
            result = subprocess.run(cmd, env=env)
    else:
        result = subprocess.run(cmd, env=env)

    if reference_doc is not None:
        # Clean up the temp reference doc (and its parent tmp dir).
        shutil.rmtree(reference_doc.parent, ignore_errors=True)

    if result.returncode != 0:
        print("💥 Quarto render failed!", file=sys.stderr)
        sys.exit(1)

    if testimony:
        _postprocess_testimony_docx(Path(output_name))

    print(f"✅ Draft complete: {output_name}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a Quarto report to DOCX (with optional expert-testimony formatting)."
    )
    parser.add_argument(
        "qmd_path",
        nargs="?",
        default="index.qmd",
        help="Path to the .qmd file to render (default: index.qmd).",
    )
    parser.add_argument(
        "--testimony",
        action="store_true",
        help="Apply the expert-testimony reference template "
        "(Times New Roman 12pt, double-spaced, line-numbered, witness header).",
    )
    args = parser.parse_args()

    qmd_path = Path(args.qmd_path)
    if not qmd_path.exists():
        print(f"File not found: {qmd_path}", file=sys.stderr)
        sys.exit(1)

    draft(qmd_path, testimony=args.testimony)


if __name__ == "__main__":
    main()
