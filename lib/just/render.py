#!/usr/bin/env python3
"""Render a Quarto report with baseline snapshot for diffing.

Snapshots current docs/ to .diff/baseline/ before rendering, inlines
any SVG figures into the HTML (removing the standalone .svg files),
and cleans up .ipynb artifacts from docs/ after rendering.

Usage (from a report directory):
    uv run python -m lib.just.render
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

BASELINE = Path(".diff/baseline")
INLINE_SVGS = Path("../.style/inline_svgs.py")


def main() -> None:
    docs = Path("docs")

    if docs.is_dir():
        print("📸 Snapshotting docs/ → .diff/baseline/")
        if BASELINE.exists():
            shutil.rmtree(BASELINE)
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(docs, BASELINE)

    print("📖 Rendering Quarto project...")
    result = subprocess.run(["quarto", "render", "."])
    if result.returncode != 0:
        print("💥 Quarto render failed!", file=sys.stderr)
        sys.exit(result.returncode)

    if INLINE_SVGS.exists():
        print("🖼️  Inlining SVGs into HTML...")
        result = subprocess.run([sys.executable, str(INLINE_SVGS), "docs"])
        if result.returncode != 0:
            sys.exit(result.returncode)
        svgs = list(docs.rglob("*.svg"))
        if svgs:
            for f in svgs:
                f.unlink()
            print(f"🗑️  Removed {len(svgs)} standalone SVG file(s)")

    ipynbs = list(docs.rglob("*.ipynb"))
    if ipynbs:
        for f in ipynbs:
            f.unlink()
        print(f"🗑️  Removed {len(ipynbs)} .ipynb artifact(s)")

    print("✅ Render complete!")


if __name__ == "__main__":
    main()
