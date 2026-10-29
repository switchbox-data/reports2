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

The ``--testimony`` flag (``just testimony``) renders an expert testimony in
the single testimony Word format (``lib/just/templates``): Times New Roman
12 pt, double-spaced, per-page line numbers, a witness running header and a
generated cover page. The docket details come from the ``testimony:`` block
in the .qmd frontmatter (see ``lib/just/testimony.py``); they are validated
first, so a missing field stops the render with a plain-English message.

Usage (from a report directory)::

    uv run python -m lib.just.draft                       # index.qmd
    uv run python -m lib.just.draft expert_testimony.qmd  # specific file
    uv run python -m lib.just.draft --testimony foo.qmd   # testimony format
"""

from __future__ import annotations

import argparse
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
from xml.sax.saxutils import escape

from lib.just.quarto_env import quarto_env
from lib.just.testimony import Testimony, TestimonyError, parse_file

# Word model file for expert testimony (Times New Roman 12 pt, double-spaced,
# per-page line numbers, witness header). Built by templates/build_expert_testimony.py.
TESTIMONY_TEMPLATE = Path(__file__).parent / "templates" / "expert_testimony.docx"
# Pandoc Lua filter for testimony-specific transforms (generated cover page,
# Q&A paragraphs, heading layout, table cell spacing).
TESTIMONY_LUA_FILTER = Path(__file__).parent / "templates" / "filters" / "testimony.lua"

# Tokens in the model file's header that hold the running-header text. The
# bracketed forms are the defaults baked into the on-disk template.
_HEADER_TOKENS = (
    (r"\[TESTIMONY TITLE\]|\{\{HEADER_LINE_1\}\}"),
    (r"\[PARTY\]|\{\{HEADER_LINE_2\}\}"),
    (r"\[CASE\]|\{\{HEADER_LINE_3\}\}"),
)


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


def _fill_header(header_xml: str, lines: tuple[str, str, str]) -> str:
    """Substitute the three running-header lines (XML-escaped) into header1.xml."""
    for pattern, line in zip(_HEADER_TOKENS, lines, strict=True):
        text = escape(line)
        header_xml = re.sub(pattern, lambda _m: text, header_xml)  # noqa: B023 - used immediately
    return header_xml


def _materialize_testimony_template(testimony: Testimony) -> Path:
    """Return a temp copy of the model file with the running header filled in.

    The on-disk template ships with placeholder header text. This writes the
    witness / party / case lines for this filing into ``word/header1.xml`` of
    a temp copy, so the shared on-disk template is never mutated.
    """
    tmp_dir = Path(tempfile.mkdtemp(prefix="switchbox_testimony_"))
    tmp_path = tmp_dir / "expert_testimony.docx"

    with zipfile.ZipFile(TESTIMONY_TEMPLATE) as src, zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/header1.xml":
                data = _fill_header(data.decode("utf-8"), testimony.header_lines).encode("utf-8")
            dst.writestr(item, data)

    print(f"📜 Testimony header → {' | '.join(testimony.header_lines)}", flush=True)
    return tmp_path


def draft(qmd_path: Path, *, testimony: bool = False) -> None:
    output_name = _output_name(qmd_path)
    is_non_article = qmd_path.name != "index.qmd"

    fields: Testimony | None = None
    if testimony:
        # Validate the `testimony:` frontmatter before doing any slow work.
        try:
            fields = parse_file(qmd_path)
        except TestimonyError as err:
            print(f"💥 {qmd_path}: the `testimony:` fields need attention:", file=sys.stderr)
            for line in err.problems:
                print(f"   {line}", file=sys.stderr)
            sys.exit(2)

    print(f"📄 Drafting {qmd_path} → {output_name}", flush=True)

    reference_doc: Path | None = None
    if fields is not None:
        if not TESTIMONY_TEMPLATE.exists():
            print(
                f"💥 Expert-testimony template not found: {TESTIMONY_TEMPLATE}",
                file=sys.stderr,
            )
            sys.exit(1)
        print(
            f"📜 Applying expert-testimony format: {TESTIMONY_TEMPLATE}",
            flush=True,
        )
        reference_doc = _materialize_testimony_template(fields)

    _clear_notebook_cache()

    env = quarto_env(SWITCHBOX_GT_AS_IMAGE="1")
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
    if fields is not None:
        # The Lua filter prints this on the cover (no zero-padded day).
        cmd += ["-M", f"testimony-date-long:{fields.date_long}"]
        if TESTIMONY_LUA_FILTER.exists():
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
        help="Render in the expert-testimony Word format (Times New Roman 12pt, double-spaced, "
        "per-page line numbers, running header, generated cover page). Requires a `testimony:` "
        "block in the frontmatter; see `just new-testimony`.",
    )
    args = parser.parse_args()

    qmd_path = Path(args.qmd_path)
    if not qmd_path.exists():
        print(f"File not found: {qmd_path}", file=sys.stderr)
        sys.exit(1)

    draft(qmd_path, testimony=args.testimony)


if __name__ == "__main__":
    main()
