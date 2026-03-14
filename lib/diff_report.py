#!/usr/bin/env python3
"""Diff all HTML pages between a baseline and current render.

Creates a temporary hub page linking to every common HTML file so that
website_diff's crawler discovers all pages — not just those reachable
from index.html.

Usage (from a report directory):
    uv run python -m lib.diff_report docs-baseline docs .diff
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def _find_html(directory: Path) -> set[str]:
    return {str(p.relative_to(directory)) for p in directory.rglob("*.html")}


def main() -> None:
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <old_dir> <new_dir> <diff_dir>", file=sys.stderr)
        sys.exit(1)

    old_dir = Path(sys.argv[1])
    new_dir = Path(sys.argv[2])
    diff_dir = Path(sys.argv[3])

    if not old_dir.is_dir():
        print(f"No baseline at {old_dir}. Run 'just render' first to create one.", file=sys.stderr)
        sys.exit(1)
    if not new_dir.is_dir():
        print(f"No rendered docs at {new_dir}.", file=sys.stderr)
        sys.exit(1)

    old_files = _find_html(old_dir)
    new_files = _find_html(new_dir)
    added = sorted(new_files - old_files)
    removed = sorted(old_files - new_files)
    common = sorted(old_files & new_files)

    if added:
        print(f"New pages (not in baseline): {', '.join(added)}")
    if removed:
        print(f"Removed pages (not in new render): {', '.join(removed)}")
    if not common:
        print("No common HTML files to diff.")
        sys.exit(1)

    hub = "_diff_hub.html"
    links = "\n".join(f'<a href="{f}">{f}</a><br>' for f in common)
    hub_html = f"<html><head><title>diff hub</title></head><body>\n{links}\n</body></html>\n"
    (old_dir / hub).write_text(hub_html)
    (new_dir / hub).write_text(hub_html)

    if diff_dir.exists():
        shutil.rmtree(diff_dir)

    prerendered = [Path(f"prerendered_{name}") for name in ("old", "new")]

    try:
        subprocess.run(
            ["website_diff", "-o", str(old_dir), "-n", str(new_dir), "-d", str(diff_dir), "-i", hub],
            check=True,
        )
    finally:
        (old_dir / hub).unlink(missing_ok=True)
        (new_dir / hub).unlink(missing_ok=True)
        (diff_dir / hub).unlink(missing_ok=True)
        for d in prerendered:
            if d.exists():
                shutil.rmtree(d)

    index = diff_dir / "index.html"
    if platform.system() == "Darwin":
        os.execlp("open", "open", str(index))
    else:
        print(f"Diff ready at {index}")


if __name__ == "__main__":
    main()
