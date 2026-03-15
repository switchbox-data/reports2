#!/usr/bin/env python3
"""Render a Quarto report with baseline snapshot for diffing.

Snapshots current docs/ to .diff/baseline/ before rendering,
then cleans up .ipynb artifacts from docs/ after rendering.

Usage (from a report directory):
    uv run python -m lib.report_render
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

BASELINE = Path(".diff/baseline")


def main() -> None:
    docs = Path("docs")

    if docs.is_dir():
        if BASELINE.exists():
            shutil.rmtree(BASELINE)
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(docs, BASELINE)

    result = subprocess.run(["quarto", "render", "."])
    if result.returncode != 0:
        sys.exit(result.returncode)

    for f in docs.rglob("*.ipynb"):
        f.unlink()


if __name__ == "__main__":
    main()
