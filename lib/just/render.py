#!/usr/bin/env python3
"""Render a Quarto report — full project or a single .qmd file.

Full-project mode (no arguments):
    Snapshots current docs/ to .diff/baseline/ before rendering, runs
    ``quarto render .``, inlines SVG figures into the HTML, and cleans
    up .ipynb artifacts.

Single-file mode (one argument):
    Runs ``quarto render <file>``, forwards fig-format from _quarto.yml
    via ``-M`` (Quarto does not inherit project-level format settings for
    single-file renders), moves the output into docs/, inlines SVGs, and
    cleans up artifacts.  No baseline snapshot is taken.

    Note on ``{{< embed >}}``: Quarto's embed pipeline re-executes the
    embedded notebook with its own format (ipynb, hardcoded to PNG) and
    ignores both project-level and ``-M`` fig-format.  Embedded figures
    will be SVG only if a freeze cache from a prior full project render
    exists.  If embedded figures appear as PNG, run ``just render`` (no
    arguments) first to build the cache.

Usage (from a report directory):
    uv run python -m lib.just.render                  # full project
    uv run python -m lib.just.render foo.qmd          # single file
"""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

BASELINE = Path(".diff/baseline")
INLINE_SVGS = Path("../.style/inline_svgs.py")


def _clean_quarto_artifacts(docs: Path) -> None:
    """Remove Quarto-generated intermediates from the source and docs trees."""
    removed = 0

    for pattern in ("**/*.out.ipynb", "**/*.embed.ipynb"):
        for f in Path(".").glob(pattern):
            # Keep `.quarto/embed/**/*.embed.ipynb`: Quarto needs these to resolve
            # `{{< embed >}}` when rendering standalone docs (e.g. testimony_outline.qmd).
            if f.parts[0] == ".quarto":
                continue
            f.unlink()
            removed += 1

    for f in docs.rglob("*.ipynb"):
        f.unlink()
        removed += 1

    if removed:
        print(f"🗑️  Removed {removed} .ipynb artifact(s)")


def _get_project_fig_format() -> str | None:
    """Read format.html.fig-format from _quarto.yml, if present."""
    quarto_yml = Path("_quarto.yml")
    if not quarto_yml.exists():
        return None
    with quarto_yml.open() as f:
        cfg = yaml.safe_load(f)
    try:
        return cfg["format"]["html"]["fig-format"]
    except (KeyError, TypeError):
        return None


def _move_to_docs(qmd_path: Path, docs: Path) -> Path:
    """Move rendered HTML and _files/ directory into docs/.

    Returns the destination HTML path.
    """
    src_html = qmd_path.with_suffix(".html")
    src_files = qmd_path.with_suffix("").parent / (qmd_path.with_suffix("").name + "_files")

    dest_html = docs / src_html
    dest_files = docs / src_files

    dest_html.parent.mkdir(parents=True, exist_ok=True)

    if dest_html.exists():
        dest_html.unlink()
    if dest_files.exists():
        shutil.rmtree(dest_files)

    if src_html.exists():
        shutil.move(str(src_html), str(dest_html))
    if src_files.exists():
        shutil.move(str(src_files), str(dest_files))

    return dest_html


def _inline_svgs() -> bool:
    """Run SVG inlining on docs/. Returns True on success."""
    if not INLINE_SVGS.exists():
        return True
    print("🖼️  Inlining SVGs into HTML...")
    result = subprocess.run([sys.executable, str(INLINE_SVGS), "docs"])
    return result.returncode == 0


def _open_or_hint(html_path: Path) -> None:
    """Open the rendered HTML on macOS, or print a hint otherwise."""
    if html_path.exists():
        if platform.system() == "Darwin":
            subprocess.Popen(["open", str(html_path)])
        else:
            print(f"👉 Open {html_path} to view")


def _render_project() -> None:
    """Full-project render with baseline snapshot."""
    docs = Path("docs")

    if docs.is_dir():
        print("📸 Snapshotting docs/ → .diff/baseline/")
        if BASELINE.exists():
            shutil.rmtree(BASELINE)
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(docs, BASELINE)

    render_failed = False
    print("📖 Rendering Quarto project...")
    try:
        result = subprocess.run(["quarto", "render", "."])
        if result.returncode != 0:
            render_failed = True
            print("💥 Quarto render failed!", file=sys.stderr)

        if not render_failed and not _inline_svgs():
            render_failed = True
    finally:
        _clean_quarto_artifacts(docs)

    if render_failed:
        sys.exit(1)

    print("✅ Render complete!")
    _open_or_hint(docs / "index.html")


def _has_embeds(qmd_path: Path) -> bool:
    """Check whether a .qmd file contains ``{{< embed >}}`` shortcodes."""
    try:
        return "{{< embed " in qmd_path.read_text(encoding="utf-8")
    except OSError:
        return False


def _render_single(qmd_path: Path) -> None:
    """Single-file render with fig-format forwarding and move to docs/."""
    docs = Path("docs")

    if _has_embeds(qmd_path) and not Path(".quarto/_freeze").exists():
        print(
            "⚠️  This file embeds figures from other notebooks, but no freeze\n"
            "   cache exists. Embedded figures will render as PNG instead of SVG.\n"
            "   Run `just render` (full project) first to build the cache.",
            file=sys.stderr,
        )

    cmd: list[str] = ["quarto", "render", str(qmd_path)]
    fig_format = _get_project_fig_format()
    if fig_format:
        cmd.extend(["-M", f"fig-format:{fig_format}"])

    render_failed = False
    print(f"📖 Rendering {qmd_path}...")
    try:
        result = subprocess.run(cmd)
        if result.returncode != 0:
            render_failed = True
            print("💥 Quarto render failed!", file=sys.stderr)

        if not render_failed:
            dest_html = _move_to_docs(qmd_path, docs)
            print(f"📦 Moved output to {dest_html}")

            if not _inline_svgs():
                render_failed = True
    finally:
        _clean_quarto_artifacts(docs)

    if render_failed:
        sys.exit(1)

    print("✅ Render complete!")
    _open_or_hint(docs / qmd_path.with_suffix(".html"))


def main() -> None:
    if len(sys.argv) > 1:
        _render_single(Path(sys.argv[1]))
    else:
        _render_project()


if __name__ == "__main__":
    main()
