#!/usr/bin/env python3
"""Publish rendered docs to the root docs/ directory for GitHub Pages.

Copies docs/ to ../../docs/<project_name>/, runs SVG inlining on the copy,
then prunes Quarto intermediates (index_files/, *-preview.html, .qmd, .ipynb)
while keeping site_libs/, img/, and all non-preview HTML.

Usage (from a report directory):
    uv run python -m lib.just.publish
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

INLINE_SVGS = Path("../.style/inline_svgs.py")


def _prune_published_site(pub_path: Path) -> None:
    """Remove cruft not needed on GitHub Pages; keep img/ and static SVGs."""
    index_dirs = [p for p in pub_path.rglob("index_files") if p.is_dir()]
    for p in sorted(index_dirs, key=lambda x: len(x.parts), reverse=True):
        shutil.rmtree(p)
    if index_dirs:
        print(f"🗑️  Removed {len(index_dirs)} index_files/ tree(s)")

    removed_files = 0
    for f in sorted(pub_path.rglob("*-preview.html")):
        f.unlink()
        removed_files += 1
    for f in sorted(pub_path.rglob("*.qmd")):
        f.unlink()
        removed_files += 1
    for f in sorted(pub_path.rglob("*.ipynb")):
        f.unlink()
        removed_files += 1
    if removed_files:
        print(f"🗑️  Removed {removed_files} intermediate file(s) (preview HTML, .qmd, .ipynb)")


def main() -> None:
    docs = Path("docs")
    if not docs.is_dir():
        print("❌ No docs/ directory. Run 'just render' first.", file=sys.stderr)
        sys.exit(1)

    project = Path.cwd().name
    pub_path = (Path("../..") / "docs" / project).resolve()

    print(f"📦 Publishing docs/ → {pub_path}", flush=True)
    if pub_path.exists():
        shutil.rmtree(pub_path)
    shutil.copytree(docs, pub_path)

    if INLINE_SVGS.exists():
        print("🖼️  Inlining SVGs into published HTML...", flush=True)
        result = subprocess.run(
            [sys.executable, str(INLINE_SVGS.resolve()), str(pub_path)],
        )
        if result.returncode != 0:
            print("💥 inline_svgs failed!", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"⚠️  Skipping SVG inline: {INLINE_SVGS} not found", file=sys.stderr)

    _prune_published_site(pub_path)
    print(f"✅ Published to {pub_path}", flush=True)


if __name__ == "__main__":
    main()
