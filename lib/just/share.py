#!/usr/bin/env python3
"""Publish an already-rendered manuscript notebook preview as a stable dev-review link.

This script does not render anything. Quarto's manuscript project type already
produces a fully-styled, standalone ``<name>-preview.html`` (+ ``<name>_files/``
sidecar) for every notebook in ``project.render`` on a normal full ``just
render`` -- charts in that page are already CSS-styled inline SVGs, since
``inline_svgs.py`` already ran over the whole ``docs/`` tree. This script just
copies that already-correct artifact into a ``_review/`` folder nested under
this project's published ``docs/<project>/`` tree, so that ``publish.py``'s
existing whole-tree ``rmtree`` + ``copytree`` sweeps it away automatically the
next time this report is really published -- no changes to publish.py.

Only works for notebooks already listed in this project's ``project.render``
(that's what produces the ``-preview.html`` this script copies). If it's
missing, run a full ``just render`` first.

Usage (from a report directory):
    uv run python -m lib.just.share notebooks/incremental_cos.qmd
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

PAGES_BASE_URL = "https://switchbox-data.github.io/reports2"


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: uv run python -m lib.just.share <path/to/notebook.qmd>", file=sys.stderr)
        sys.exit(1)

    qmd_path = Path(sys.argv[1])
    docs = Path("docs")

    preview_html = docs / qmd_path.parent / f"{qmd_path.stem}-preview.html"
    files_dir = docs / qmd_path.parent / f"{qmd_path.stem}_files"

    if not preview_html.exists():
        print(
            f"❌ {preview_html} not found.\n"
            "   share.py doesn't render anything -- run `just render` (full project)\n"
            "   first so Quarto produces the notebook preview page.",
            file=sys.stderr,
        )
        sys.exit(1)

    project = Path.cwd().name
    pub_root = (Path("../..") / "docs" / project).resolve()
    dest_dir = pub_root / "_review" / qmd_path.parent
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_html = dest_dir / preview_html.name
    shutil.copy2(preview_html, dest_html)
    print(f"📄 Copied {preview_html} → {dest_html}")

    if files_dir.exists():
        dest_files = dest_dir / files_dir.name
        if dest_files.exists():
            shutil.rmtree(dest_files)
        shutil.copytree(files_dir, dest_files)
        print(f"📦 Copied {files_dir} → {dest_files}")

    # The preview page references ../site_libs/... (shared Bootstrap/JS/CSS).
    # That only exists at the project's published root after a real `just
    # publish`. If this report has never been published, seed it here so the
    # review link isn't missing its styling -- harmless either way, since a
    # future real publish overwrites site_libs/ wholesale regardless.
    local_site_libs = docs / "site_libs"
    dest_site_libs = pub_root / "site_libs"
    if not dest_site_libs.exists() and local_site_libs.exists():
        shutil.copytree(local_site_libs, dest_site_libs)
        print(f"📦 Seeded {dest_site_libs} (this report hasn't been published yet)")

    rel_url_path = Path(project) / "_review" / qmd_path.parent / preview_html.name
    url = f"{PAGES_BASE_URL}/{rel_url_path}"
    rel_publish_dir = Path("docs") / project

    print()
    print(f"🔗 Review link (live once merged to main): {url}")
    print()
    print("Next steps to make it live:")
    print("  cd ../..")
    print(f"  git add -f {rel_publish_dir}/")
    print(f'  git commit -m "Add dev review link for {qmd_path.name}"')
    print("  git push")
    print("  # then merge to main -- GitHub Pages only builds from main")
    print()
    print(
        "Note: this link is unlisted but public, same as the rest of the site.\n"
        "It will be swept away automatically the next time this report's\n"
        "`just publish` runs for real -- no manual cleanup needed."
    )


if __name__ == "__main__":
    main()
