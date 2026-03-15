#!/usr/bin/env python3
"""Diff all HTML pages between a baseline and current render.

Creates a temporary hub page linking to every common HTML file so that
website_diff's crawler discovers all pages — not just those reachable
from index.html. Past diffs are archived under .diff/diffs/.

Usage (from a report directory):
    uv run python -m lib.diff_report              # timestamped diff
    uv run python -m lib.diff_report my-label      # timestamped + label
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASELINE = Path(".diff/baseline")
DIFFS = Path(".diff/diffs")


def _find_html(directory: Path) -> set[str]:
    return {str(p.relative_to(directory)) for p in directory.rglob("*.html")}


def main() -> None:
    label = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else None

    if not BASELINE.is_dir():
        print(f"No baseline at {BASELINE}. Run 'just render' first to create one.", file=sys.stderr)
        sys.exit(1)

    docs = Path("docs")
    if not docs.is_dir():
        print("No rendered docs at docs/.", file=sys.stderr)
        sys.exit(1)

    old_files = _find_html(BASELINE)
    new_files = _find_html(docs)
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

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    diff_name = f"{timestamp}_{label}" if label else timestamp
    diff_dir = DIFFS / diff_name

    hub = "_diff_hub.html"
    links = "\n".join(f'<a href="{f}">{f}</a><br>' for f in common)
    hub_html = f"<html><head><title>diff hub</title></head><body>\n{links}\n</body></html>\n"
    (BASELINE / hub).write_text(hub_html)
    (docs / hub).write_text(hub_html)

    DIFFS.mkdir(parents=True, exist_ok=True)

    prerendered = [Path(f"prerendered_{name}") for name in ("old", "new")]

    try:
        subprocess.run(
            ["website_diff", "-o", str(BASELINE), "-n", str(docs), "-d", str(diff_dir), "-i", hub],
            check=True,
        )
    finally:
        (BASELINE / hub).unlink(missing_ok=True)
        (docs / hub).unlink(missing_ok=True)
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
