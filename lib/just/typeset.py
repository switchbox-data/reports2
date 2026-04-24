#!/usr/bin/env python3
"""Render a Quarto report to ICML for InDesign typesetting.

Outputs to ``icml/`` (not ``docs/``) so the designer gets a standalone folder
that can be dropped onto Google Drive.  Post-processing steps:

- Moves math SVGs (rendered by the icml_math Lua filter) from the temp
  ``math/`` directory to ``icml/math/`` alongside the ICML.
- Runs icml_sidenotes conversion if the ICML contains footnotes.
- Runs icml_crossrefs conversion to turn ``@sec-*`` links into live InDesign
  cross-references (page numbers). After placing the ICML, the designer runs
  **Update All Cross-References** from the Cross-References panel once per
  document; page numbers fill in automatically and stay live on reflow.

Usage (from a report directory)::

    uv run python -m lib.just.typeset                       # index.qmd
    uv run python -m lib.just.typeset expert_testimony.qmd  # specific file
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from lib.just import icml_crossrefs, icml_sidenotes


def _output_name(qmd_path: Path) -> str:
    """Generate a date-stamped ICML filename from the source .qmd."""
    stem = qmd_path.stem if qmd_path.stem != "index" else "report"
    return f"{stem}_{date.today():%Y%m%d}.icml"


def _move_math_svgs(out_dir: Path) -> int:
    """Move math SVGs from temp math/ into the output directory. Returns count moved."""
    src = Path("math")
    if not src.is_dir():
        return 0

    dest = out_dir / "math"
    dest.mkdir(parents=True, exist_ok=True)

    svgs = list(src.glob("*.svg"))
    for svg in svgs:
        shutil.copy2(svg, dest / svg.name)

    shutil.rmtree(src)
    return len(svgs)


def _clear_notebook_cache() -> None:
    """Delete Quarto's freeze cache and .out.ipynb files so notebooks re-execute.

    GT tables use ``display_gt`` which checks ``SWITCHBOX_TYPESET`` to decide
    whether to emit HTML (for web) or PNG (for ICML).  The cached outputs
    from the HTML render contain HTML, so the freeze cache must be removed
    to force re-execution with the env var set.
    """
    freeze_dir = Path(".quarto/_freeze/notebooks")
    if freeze_dir.is_dir():
        shutil.rmtree(freeze_dir)
        print(f"📐 Cleared freeze cache: {freeze_dir}")

    for out_nb in Path("docs").rglob("*.out.ipynb"):
        out_nb.unlink()
    for out_nb in Path(".").glob("*.out.ipynb"):
        out_nb.unlink()


def _prune_quarto_intermediates(out_dir: Path) -> None:
    """Remove Quarto intermediates the designer doesn't need."""
    for pattern in ("*.out.ipynb", "*.embed.ipynb", "*.qmd"):
        for f in out_dir.rglob(pattern):
            f.unlink()


def typeset(qmd_path: Path) -> None:
    out = Path("icml")
    output_name = _output_name(qmd_path)
    output_path = out / output_name

    print(f"📐 Typesetting {qmd_path} → {output_path}")

    _clear_notebook_cache()

    env = {**os.environ, "SWITCHBOX_TYPESET": "1"}
    cmd = [
        "quarto",
        "render",
        "--to",
        "icml",
        "--execute",
        "--output-dir",
        "icml",
    ]
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        print("💥 Quarto render failed!", file=sys.stderr)
        sys.exit(1)

    # Project-level render outputs index.icml; rename to date-stamped name.
    default_icml = out / "index.icml"
    if default_icml.exists() and default_icml != output_path:
        default_icml.rename(output_path)

    n_svgs = _move_math_svgs(out)
    if n_svgs:
        print(f"📐 Moved {n_svgs} math SVGs to {out / 'math'}/")

    _prune_quarto_intermediates(out)

    if output_path.exists():
        icml_text = output_path.read_text(encoding="utf-8")
        changed = False
        if "<Footnote>" in icml_text:
            icml_text = icml_sidenotes.convert(icml_text)
            changed = True
            print(f"📐 Converted footnotes to sidenotes in {output_path}")
        if "HyperlinkTextDestination/#sec-" in icml_text:
            before = icml_text.count("<CrossReferenceSource")
            icml_text = icml_crossrefs.convert(icml_text)
            added = icml_text.count("<CrossReferenceSource") - before
            if added:
                changed = True
                print(
                    f"📐 Converted {added} @sec refs to live cross-references in {output_path}",
                )
        if changed:
            output_path.write_text(icml_text, encoding="utf-8")

    print(f"✅ Typeset complete: {output_path}")


def main() -> None:
    qmd_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("index.qmd")

    if not qmd_path.exists():
        print(f"File not found: {qmd_path}", file=sys.stderr)
        sys.exit(1)

    typeset(qmd_path)


if __name__ == "__main__":
    main()
