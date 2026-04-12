#!/usr/bin/env python3
"""Render a Quarto report to ICML for InDesign typesetting.

Runs ``quarto render`` with ``--to icml``, then handles post-processing:
- Moves math SVGs (rendered by the icml_math Lua filter) from the temp
  ``math/`` directory to ``docs/math/`` alongside the ICML.
- Runs icml_sidenotes conversion if the ICML contains footnotes.

Usage (from a report directory):
    uv run python -m lib.just.typeset                       # index.qmd
    uv run python -m lib.just.typeset expert_testimony.qmd  # specific file
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from lib.just import icml_sidenotes


def _output_name(qmd_path: Path) -> str:
    """Generate a date-stamped ICML filename from the source .qmd."""
    stem = qmd_path.stem if qmd_path.stem != "index" else "report"
    return f"{stem}_{date.today():%Y%m%d}.icml"


def _move_math_svgs(docs: Path) -> int:
    """Move math SVGs from temp math/ to docs/math/. Returns count moved."""
    src = Path("math")
    if not src.is_dir():
        return 0

    dest = docs / "math"
    dest.mkdir(parents=True, exist_ok=True)

    svgs = list(src.glob("*.svg"))
    for svg in svgs:
        shutil.copy2(svg, dest / svg.name)

    shutil.rmtree(src)
    return len(svgs)


def typeset(qmd_path: Path) -> None:
    docs = Path("docs")
    output_name = _output_name(qmd_path)
    output_path = docs / output_name

    print(f"📐 Typesetting {qmd_path} → {output_path}")

    cmd = ["quarto", "render", str(qmd_path), "--to", "icml", "--output", output_name]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("💥 Quarto render failed!", file=sys.stderr)
        sys.exit(1)

    n_svgs = _move_math_svgs(docs)
    if n_svgs:
        print(f"📐 Moved {n_svgs} math SVGs to {docs / 'math'}/")

    if output_path.exists():
        icml_text = output_path.read_text(encoding="utf-8")
        if "<Footnote>" in icml_text:
            converted = icml_sidenotes.convert(icml_text)
            output_path.write_text(converted, encoding="utf-8")
            print(f"📐 Converted footnotes to sidenotes in {output_path}")

    print(f"✅ Typeset complete: {output_path}")


def main() -> None:
    qmd_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("index.qmd")

    if not qmd_path.exists():
        print(f"File not found: {qmd_path}", file=sys.stderr)
        sys.exit(1)

    typeset(qmd_path)


if __name__ == "__main__":
    main()
