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

Usage (from a report directory)::

    uv run python -m lib.just.draft                       # index.qmd
    uv run python -m lib.just.draft expert_testimony.qmd  # specific file
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import date
from pathlib import Path


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


def draft(qmd_path: Path) -> None:
    output_name = _output_name(qmd_path)
    is_non_article = qmd_path.name != "index.qmd"

    print(f"📄 Drafting {qmd_path} → {output_name}", flush=True)

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

    if is_non_article and Path("_quarto.yml").exists():
        with _hide_quarto_yml():
            result = subprocess.run(cmd, env=env)
    else:
        result = subprocess.run(cmd, env=env)

    if result.returncode != 0:
        print("💥 Quarto render failed!", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Draft complete: {output_name}", flush=True)


def main() -> None:
    qmd_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("index.qmd")

    if not qmd_path.exists():
        print(f"File not found: {qmd_path}", file=sys.stderr)
        sys.exit(1)

    draft(qmd_path)


if __name__ == "__main__":
    main()
