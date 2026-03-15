#!/usr/bin/env python3
"""Clean all generated caches and artifacts from a report directory.

Usage (from a report directory):
    uv run python -m lib.report_clean
"""

from __future__ import annotations

import shutil
from pathlib import Path


def main() -> None:
    for name in [".quarto", ".diff", "prerendered_old", "prerendered_new"]:
        p = Path(name)
        if p.is_dir():
            shutil.rmtree(p)

    for d in Path("docs").glob("*_files"):
        if d.is_dir():
            shutil.rmtree(d)

    notebooks = Path("notebooks")
    if notebooks.is_dir():
        for pattern in ["*.html", "*.ipynb", "*.rmarkdown"]:
            for f in notebooks.glob(pattern):
                f.unlink()
        for d in notebooks.glob("*_files"):
            if d.is_dir():
                shutil.rmtree(d)


if __name__ == "__main__":
    main()
