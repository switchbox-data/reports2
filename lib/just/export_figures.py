"""Export all embedded figures and tables from a Quarto document as numbered PNGs.

Parses a .qmd file for ``{{< embed >}}`` directives, maps each to its
rendered output file (SVG or PNG), converts SVGs to high-res PNGs, and
copies everything into a flat output directory with filenames reflecting
their figure/table number in the document.

Usage::

    uv run python -m lib.just.export_figures <qmd_file> [--output-dir <dir>] [--dpi <dpi>]

Examples::

    # From report directory:
    uv run python -m lib.just.export_figures expert_testimony.qmd

    # Custom output and DPI:
    uv run python -m lib.just.export_figures expert_testimony.qmd --output-dir exhibits --dpi 600

    # "Figure 1.png" names that match the rendered document, one file per
    # embed instance (so numbers line up with the DOCX for manual replacement):
    uv run python -m lib.just.export_figures expert_testimony.qmd --name-style word --no-dedup

The script expects a prior ``just render`` so that rendered outputs exist
in ``docs/<stem>_files/figure-html/``.

**Colorbar workaround:** SVGs produced by the Switchbox plotnine pipeline
use ``rasterize_colorbars()`` to replace heavyweight Gouraud-shaded
gradient markup with a small embedded PNG.  This optimization works
perfectly for in-browser rendering, but the rasterized ``<image>``
element is sometimes dropped during the SVG save pipeline, leaving the
colorbar gradient invisible.  The script detects this (SVG has a
``LineCollection`` but no ``<image>`` element) and marks those figures
as needing manual PNG replacement.  Pass ``--warn-colorbars`` to see
which figures are affected without failing.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

EMBED_PATTERN = re.compile(
    r"\{\{<\s*embed\s+"
    r"(?P<notebook>[^\s#]+)"
    r"#(?P<label>(?:fig|tbl)-[^\s>]+)"
    r"\s*>\}\}"
)


def parse_embeds(qmd_path: Path, *, dedup: bool = True) -> list[dict[str, str]]:
    """Extract embed references in document order.

    Returns a list of dicts with keys: notebook, label, prefix (fig or tbl).

    With ``dedup=True`` (default) each label is emitted once, at its first
    appearance.  With ``dedup=False`` every ``{{< embed >}}`` instance is
    emitted, so a chart embedded twice yields two entries — this makes the
    per-type counter match Quarto's own float numbering (and therefore the
    numbers in the rendered DOCX/HTML), since Quarto numbers each embed
    instance separately.
    """
    embeds: list[dict[str, str]] = []
    seen: set[str] = set()
    text = qmd_path.read_text()

    for m in EMBED_PATTERN.finditer(text):
        label = m.group("label")
        if dedup and label in seen:
            continue
        seen.add(label)

        notebook = m.group("notebook")
        prefix = "fig" if label.startswith("fig-") else "tbl"
        embeds.append({"notebook": notebook, "label": label, "prefix": prefix})

    return embeds


def find_output_file(figure_dir: Path, notebook_stem: str, label: str) -> Path | None:
    """Find the rendered output file for a given embed label.

    Looks for ``notebooks-{notebook_stem}-{label}-output-1.{svg,png}``
    in the figure directory. Prefers SVG (higher quality source for
    conversion), falls back to PNG.
    """
    base = f"notebooks-{notebook_stem}-{label}-output-1"

    for ext in (".svg", ".png"):
        candidate = figure_dir / (base + ext)
        if candidate.exists():
            return candidate

    # Some tables may produce output-2 as the main image
    for ext in (".png", ".svg"):
        candidate = figure_dir / f"notebooks-{notebook_stem}-{label}-output-2{ext}"
        if candidate.exists():
            return candidate

    return None


def _svg_has_broken_colorbar(svg_path: Path) -> bool:
    """Detect SVGs where the colorbar gradient was stripped.

    The Switchbox ``rasterize_colorbars`` pipeline replaces matplotlib's
    Gouraud-shaded colorbar with an embedded ``<image>`` PNG.  If the
    ``<image>`` element is missing but colorbar tick marks are present,
    the colorbar gradient is invisible and the exported PNG will be
    broken.

    Colorbar ticks are short horizontal line pairs (dx < 20px) in a
    ``LineCollection`` group.  Long horizontal lines (dx > 100px) are
    dashed annotations, not colorbar ticks.
    """
    content = svg_path.read_text()
    if "<image" in content:
        return False

    lc_match = re.search(r'<g id="LineCollection_\d+">(.*?)</g>', content, re.DOTALL)
    if lc_match is None:
        return False

    ticks = re.findall(r"M ([\d.]+) [\d.]+\s+L ([\d.]+) [\d.]+", lc_match.group(1))
    return any(abs(float(x2) - float(x1)) < 20 for x1, x2 in ticks)


def svg_to_png(svg_path: Path, png_path: Path, *, dpi: int = 300) -> None:
    """Convert an SVG to a high-res PNG using rsvg-convert."""
    subprocess.run(
        [
            "rsvg-convert",
            "-d",
            str(dpi),
            "-p",
            str(dpi),
            "-o",
            str(png_path),
            str(svg_path),
        ],
        check=True,
        capture_output=True,
    )


def format_output_name(kind: str, n: int, *, name_style: str) -> str:
    """Build the output filename for a figure/table number.

    ``name_style="numbered"`` → ``Figure_01.png`` (zero-padded, underscore);
    ``name_style="word"`` → ``Figure 1.png`` (spaced, unpadded) to match the
    "Figure N" / "Table N" labels in the rendered document, so the files drop
    straight into a Word document during manual replacement.
    """
    if name_style == "word":
        return f"{kind} {n}.png"
    return f"{kind}_{n:02d}.png"


def export_figures(
    qmd_path: Path,
    output_dir: Path,
    *,
    dpi: int = 300,
    name_style: str = "numbered",
    dedup: bool = True,
) -> None:
    """Export all embedded figures/tables as numbered PNGs."""
    qmd_path = qmd_path.resolve()
    report_dir = qmd_path.parent
    qmd_stem = qmd_path.stem

    figure_dir = report_dir / "docs" / f"{qmd_stem}_files" / "figure-html"
    if not figure_dir.exists():
        print(f"ERROR: Rendered output directory not found: {figure_dir}")
        print("       Run 'just render' first to generate figure outputs.")
        sys.exit(1)

    embeds = parse_embeds(qmd_path, dedup=dedup)
    if not embeds:
        print(f"No {{{{< embed >}}}} directives found in {qmd_path.name}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    fig_counter = 0
    tbl_counter = 0
    exported = 0
    skipped: list[str] = []
    broken_colorbars: list[str] = []

    for embed in embeds:
        notebook = embed["notebook"]
        label = embed["label"]
        prefix = embed["prefix"]

        # Derive notebook stem: notebooks/representative_home.qmd -> representative_home
        notebook_stem = Path(notebook).stem

        source = find_output_file(figure_dir, notebook_stem, label)
        if source is None:
            skipped.append(label)
            continue

        if prefix == "fig":
            fig_counter += 1
            out_name = format_output_name("Figure", fig_counter, name_style=name_style)
        else:
            tbl_counter += 1
            out_name = format_output_name("Table", tbl_counter, name_style=name_style)

        out_path = output_dir / out_name

        if source.suffix == ".svg":
            if _svg_has_broken_colorbar(source):
                broken_colorbars.append(f"{out_name}  ←  {label}")
                svg_to_png(source, out_path, dpi=dpi)
                print(f"  {out_name}  ←  {label}  ⚠️  colorbar gradient missing")
            else:
                svg_to_png(source, out_path, dpi=dpi)
                print(f"  {out_name}  ←  {label}")
        else:
            shutil.copy2(source, out_path)
            print(f"  {out_name}  ←  {label}")

        exported += 1

    print(f"\n✅ Exported {exported} files to {output_dir}/")
    if broken_colorbars:
        print(
            f"\n⚠️  {len(broken_colorbars)} figures have broken colorbar gradients"
            " (SVG pipeline stripped the rasterized gradient)."
            "\n   Re-render these manually as PNG and copy into the output directory:"
        )
        for bc in broken_colorbars:
            print(f"     - {bc}")
    if skipped:
        print(f"\n⚠️  {len(skipped)} embeds not found (run 'just render' to generate):")
        for s in skipped:
            print(f"     - {s}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export embedded figures and tables from a Quarto document as numbered PNGs."
    )
    parser.add_argument(
        "qmd_file",
        type=Path,
        help="Path to the .qmd file (e.g. expert_testimony.qmd)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for PNGs (default: <qmd_stem>_figures/ in same directory)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="DPI for SVG-to-PNG conversion (default: 300)",
    )
    parser.add_argument(
        "--name-style",
        choices=["numbered", "word"],
        default="numbered",
        help=(
            "Output filename style: 'numbered' → Figure_01.png (default); "
            "'word' → 'Figure 1.png' to match the rendered document's labels."
        ),
    )
    parser.add_argument(
        "--no-dedup",
        action="store_true",
        help=(
            "Emit one file per {{< embed >}} instance instead of one per unique "
            "label, so the counter matches Quarto's float numbering (a chart "
            "embedded twice gets two files under its two numbers). Recommended "
            "with --name-style word for Word manual-replacement workflows."
        ),
    )

    args = parser.parse_args()

    qmd_path = args.qmd_file
    if not qmd_path.is_absolute():
        qmd_path = Path.cwd() / qmd_path

    if not qmd_path.exists():
        print(f"ERROR: File not found: {qmd_path}")
        sys.exit(1)

    output_dir = args.output_dir
    if output_dir is None:
        output_dir = qmd_path.parent / f"{qmd_path.stem}_figures"

    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir

    export_figures(
        qmd_path,
        output_dir,
        dpi=args.dpi,
        name_style=args.name_style,
        dedup=not args.no_dedup,
    )


if __name__ == "__main__":
    main()
