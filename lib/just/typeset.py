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
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from lib.just import icml_crossrefs, icml_sidenotes

INDESIGN_MAX_WIDTH_PT = 504.0


# Pandoc's ICML writer emits a stray ``(a)`` subfigure label before the
# real ``Table N: …`` caption whenever a FloatRefTarget's content is a
# RawInline (which is exactly what ``icml_gt.lua`` produces to smuggle a
# native ``<Table>`` through the pipeline).  We strip those spurious
# labels after the fact: any ``ParagraphStyle/Caption`` paragraph whose
# only content is ``(a)`` is unambiguously the writer's subfigure label
# rather than something the author wrote.
_SUBFIGURE_LABEL_RE = re.compile(
    r"<ParagraphStyleRange AppliedParagraphStyle=\"ParagraphStyle/Caption\">\s*"
    r"<CharacterStyleRange AppliedCharacterStyle=\"\$ID/NormalCharacterStyle\">\s*"
    r"<Content>\([a-z]\)</Content>\s*"
    r"</CharacterStyleRange>\s*"
    r"</ParagraphStyleRange>\s*"
    r"<Br />\s*",
)


def _strip_subfigure_labels(icml_text: str) -> str:
    """Remove Pandoc's spurious ``(a)`` subfigure labels before GT captions."""
    return _SUBFIGURE_LABEL_RE.sub("", icml_text)


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


# File resources (SVGs, PNGs, …) that Pandoc links into the ICML appear as
# ``LinkResourceURI="file:<relative-path>"`` attributes.  Anything in the
# figure-icml tree that *isn't* in that set is a leftover — most commonly
# one of the 1x1 carrier SVGs that ``display_gt`` emits to smuggle native
# ICML ``<Table>`` XML through Quarto's embed pipeline (our ``icml_gt``
# filter reads them off disk, decodes the embedded XML, and replaces the
# link with a raw ICML block, leaving the SVG unreferenced on disk).
_LINK_RESOURCE_RE = re.compile(r'LinkResourceURI="file:([^"]+)"')


def _prune_orphan_figure_assets(out_dir: Path, icml_text: str) -> int:
    """Delete figure-icml assets not referenced by the final ICML.

    Returns the count deleted.  Safe: we only touch files under
    ``index_files/figure-icml/``; anything still referenced stays put.
    """
    fig_dir = out_dir / "index_files" / "figure-icml"
    if not fig_dir.is_dir():
        return 0

    referenced: set[Path] = set()
    for m in _LINK_RESOURCE_RE.finditer(icml_text):
        uri = m.group(1)
        try:
            referenced.add((out_dir / uri).resolve())
        except OSError:
            continue

    n_removed = 0
    for asset in fig_dir.iterdir():
        if not asset.is_file():
            continue
        try:
            resolved = asset.resolve()
        except OSError:
            continue
        if resolved in referenced:
            continue
        asset.unlink()
        n_removed += 1
    return n_removed


_SVG_WIDTH_RE = re.compile(r'(<svg\b[^>]*?)\bwidth="([0-9.]+)pt"')
_SVG_HEIGHT_RE = re.compile(r'(<svg\b[^>]*?)\bheight="([0-9.]+)pt"')


def _cap_oversized_svgs(out_dir: Path) -> int:
    """Shrink any figure SVG wider than the InDesign text column.

    Belt-and-suspenders for figures that escape the ``plt.subplots`` figsize
    cap (e.g. code that calls ``fig.set_size_inches`` after construction).
    Rewrites the root ``width``/``height`` attributes while leaving the
    ``viewBox`` untouched so content scales uniformly.  Text in these
    stragglers WILL scale down proportionally — the warning lets you
    chase down the offending ``figsize`` call and fix it at source.
    """
    n_fixed = 0
    for svg in out_dir.rglob("*.svg"):
        text = svg.read_text(encoding="utf-8")
        width_match = _SVG_WIDTH_RE.search(text)
        if width_match is None:
            continue
        width = float(width_match.group(2))
        if width <= INDESIGN_MAX_WIDTH_PT:
            continue

        scale = INDESIGN_MAX_WIDTH_PT / width
        height_match = _SVG_HEIGHT_RE.search(text)
        new_text = _SVG_WIDTH_RE.sub(
            lambda m: f'{m.group(1)}width="{INDESIGN_MAX_WIDTH_PT:g}pt"',
            text,
            count=1,
        )
        if height_match is not None:
            new_height = float(height_match.group(2)) * scale
            new_text = _SVG_HEIGHT_RE.sub(
                lambda m, h=new_height: f'{m.group(1)}height="{h:g}pt"',
                new_text,
                count=1,
            )

        svg.write_text(new_text, encoding="utf-8")
        n_fixed += 1
        print(
            f"⚠️  SVG wider than 504 pt — scaled ({width:.0f} → "
            f"{INDESIGN_MAX_WIDTH_PT:.0f} pt, text shrunk): {svg.relative_to(out_dir)}"
        )
    return n_fixed


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

    n_capped = _cap_oversized_svgs(out)
    if n_capped:
        print(f"📐 Capped {n_capped} oversized SVG(s) to {INDESIGN_MAX_WIDTH_PT:.0f} pt wide")

    _prune_quarto_intermediates(out)

    if output_path.exists():
        icml_text = output_path.read_text(encoding="utf-8")
        changed = False
        stripped = _strip_subfigure_labels(icml_text)
        if stripped != icml_text:
            icml_text = stripped
            changed = True
            print("📐 Stripped spurious (a) subfigure labels from GT tables")
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

        n_orphans = _prune_orphan_figure_assets(out, icml_text)
        if n_orphans:
            print(f"📐 Pruned {n_orphans} orphan figure asset(s) (GT table carriers, etc.)")

    print(f"✅ Typeset complete: {output_path}")


def main() -> None:
    qmd_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("index.qmd")

    if not qmd_path.exists():
        print(f"File not found: {qmd_path}", file=sys.stderr)
        sys.exit(1)

    typeset(qmd_path)


if __name__ == "__main__":
    main()
