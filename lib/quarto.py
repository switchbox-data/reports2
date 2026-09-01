"""Helpers for Quarto Manuscript rendering.

Quarto Manuscript's ``{{< embed >}}`` shortcode breaks on certain cell
output types because Pandoc's ``--to ipynb`` conversion cannot round-trip
them faithfully.  The helpers here produce outputs that survive the
embed pipeline so ``{{< embed >}}`` can be used instead of file-based
workarounds.

* **``display_figure``** — for matplotlib figures: SVG for HTML and ICML,
  high-res PNG for DOCX (to dodge Pandoc's fuzzy 96-DPI rsvg-convert).
  ``display_svg`` is a backwards-compatible alias.
* **``display_gt``** — for Great Tables:

  * **HTML**: base64-decoded ``<div>`` (survives ``{{< embed >}}``).
  * **DOCX** (``SWITCHBOX_GT_AS_IMAGE=1``): high-res PNG screenshot.
  * **ICML** (``SWITCHBOX_TYPESET=1``): native InDesign ``<Table>`` XML
    (see :mod:`lib.great_tables.icml`), base64-packaged inside a 1x1
    placeholder SVG carrier and promoted to a raw ICML block by
    :file:`lib/quarto_extensions/icml_gt/icml_gt.lua` (the carrier dance
    is required because Quarto's embed pipeline strips
    ``text/markdown`` outputs from ``tbl-*`` cells and Pandoc's ICML
    writer refuses ``text/html`` — but ``image/svg+xml`` survives
    end-to-end).  The designer's InDesign document resolves the
    referenced named styles (``TableStyle/Table Inline``,
    ``CellStyle/Cell Header``, etc.), producing a native editable
    table that reflows with the layout instead of a placed SVG raster.
"""

from __future__ import annotations

import base64
import io
import os
import tempfile
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from great_tables import GT
    from matplotlib.figure import Figure


def _render_gt_as_icml() -> bool:
    """Return True when GT tables must be rendered as native ICML (ICML only).

    Set by ``lib.just.typeset`` via ``SWITCHBOX_TYPESET=1``.  ICML is
    placed in InDesign, which renders a native ``<Table>`` element as
    an editable table that reflows with the layout (text wraps
    properly when the designer resizes the frame) — unlike placed SVG,
    which shrinks text proportionally.
    """
    return os.environ.get("SWITCHBOX_TYPESET") == "1"


def _render_as_raster() -> bool:
    """Return True when GT tables must be rasterized to PNG (DOCX only).

    Set by ``just draft`` via ``SWITCHBOX_GT_AS_IMAGE=1``.  Word's Pandoc
    path doesn't handle SVG reliably (fuzzy 96-DPI ``rsvg-convert``), so
    GT tables for DOCX fall back to a high-res PNG screenshot.
    """
    return os.environ.get("SWITCHBOX_GT_AS_IMAGE") == "1"


def _render_figures_as_raster() -> bool:
    """Return True when matplotlib figures must be rasterized (DOCX only).

    Set by ``just draft`` via ``SWITCHBOX_GT_AS_IMAGE=1`` to work around
    Pandoc's default 96-DPI ``rsvg-convert`` pipeline into DOCX, which
    produces fuzzy figures.  ICML (``SWITCHBOX_TYPESET=1``) is intentionally
    excluded — InDesign places SVG natively at full fidelity, and the
    project-level ``fig-format: svg`` keeps raw Quarto figures as SVG too.
    """
    return os.environ.get("SWITCHBOX_GT_AS_IMAGE") == "1"


def display_figure(fig: Figure, *, dpi: int = 300) -> None:
    """Render a matplotlib figure as SVG (HTML/ICML) or high-res PNG (DOCX).

    Quarto Manuscript's ``{{< embed >}}`` breaks on cells that produce
    multi-MIME output (e.g. a raw matplotlib Figure emits both PNG and
    text/plain).  This helper produces a single MIME output that survives
    the embed pipeline.

    The output format depends on the target:

    * **HTML** (default) and **ICML**: ``image/svg+xml`` — sharp at any
      zoom, styled by CSS (HTML) or placed natively by InDesign (ICML).
    * **DOCX**: ``image/png`` at *dpi* (default 300) — avoids the fuzzy
      rasterization that happens when Pandoc converts SVG via
      ``rsvg-convert`` at its default 96 DPI.

    Format detection uses ``_render_figures_as_raster()``
    (``SWITCHBOX_GT_AS_IMAGE=1`` only).

    After saving, the figure is closed to free memory.
    """
    import matplotlib.pyplot as plt

    if _render_figures_as_raster():
        from IPython.display import Image, display

        fig.savefig(buf := io.BytesIO(), format="png", dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        display(Image(data=buf.getvalue(), format="png"))
    else:
        from IPython.display import SVG, display

        from lib.plotnine.svg_optimize import rasterize_colorbars

        rasterize_colorbars(fig)
        fig.savefig(buf := io.BytesIO(), format="svg", bbox_inches="tight")
        plt.close(fig)
        display(SVG(data=buf.getvalue()))


display_svg = display_figure


def display_gt(table: GT) -> None:
    """Display a Great Tables object so it works in HTML, DOCX, and ICML.

    Output format depends on environment:

    * **HTML** (neither var set): base64-encodes the GT HTML and wraps it
      in a ``<div>`` + ``<script>`` that decodes at page load.  Survives
      the Quarto Manuscript ``{{< embed >}}`` pipeline, which truncates
      raw ``text/html``.
    * **DOCX** (``SWITCHBOX_GT_AS_IMAGE=1``): renders the table as a
      high-res PNG (3x scale, ~300 DPI) using GT's headless Chrome
      screenshot.
    * **ICML** (``SWITCHBOX_TYPESET=1``): converts the GT to a native
      ``<Table>`` ICML fragment (via :mod:`lib.great_tables.icml`) and
      emits it as an HTML carrier div that the
      :file:`lib/quarto_extensions/icml_gt/icml_gt.lua` filter promotes
      to a raw ICML block.  The InDesign designer's template resolves
      the referenced named styles (``TableStyle/Table Inline``,
      ``CellStyle/Cell Header``, etc.), yielding a native editable table
      that reflows with the layout.  Any unexpected exception falls back
      to the PNG raster path so a single bad table can't break the whole
      ICML build.

    Usage in ``analysis.qmd``::

        from lib.quarto import display_gt

        my_table = GT(df).fmt_currency(...)
        display_gt(my_table)

    Then in ``index.qmd``::

        {{< embed notebooks/analysis.qmd#tbl-my-table >}}
    """
    if _render_gt_as_icml():
        _display_gt_as_icml(table)
    elif _render_as_raster():
        _display_gt_as_image(table)
    else:
        _display_gt_as_html(table)


def _display_gt_as_html(table: GT) -> None:
    """Base64-encode GT HTML for the browser-based embed pipeline."""
    from IPython.display import HTML, display

    html = table.as_raw_html()
    encoded = base64.b64encode(html.encode()).decode()
    uid = uuid.uuid4().hex[:8]
    display(
        HTML(
            f'<div id="gt-{uid}"></div>'
            f"<script>document.getElementById('gt-{uid}').innerHTML"
            f" = new TextDecoder().decode(Uint8Array.from(atob('{encoded}'),"
            f" c => c.charCodeAt(0)));</script>"
        )
    )


def _display_gt_as_image(table: GT, *, scale: float = 3.0) -> None:
    """Render GT to a high-res PNG and display as an IPython Image."""
    from IPython.display import Image, display

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmp_path = f.name
    try:
        table.save(tmp_path, scale=scale)
        with open(tmp_path, "rb") as f:
            png_bytes = f.read()
        display(Image(data=png_bytes, format="png"))
    finally:
        os.unlink(tmp_path)


def _display_gt_as_icml(table: GT) -> None:
    """Emit a GT as a native ICML ``<Table>`` fragment via an SVG carrier.

    Getting ICML out of Quarto's ``{{< embed >}}`` pipeline for ``tbl-*``
    labelled cells is surprisingly fiddly.  Candidates considered:

    * ``text/markdown`` — Quarto strips these outputs entirely before
      they reach the Pandoc AST (even when their content is a
      ``{=icml}`` raw block).
    * ``text/html`` — survives the ``.embed.ipynb`` step but Pandoc's
      ICML writer emits "Unable to display output for mime type(s):
      text/html" for it, because HTML isn't a first-class ICML media.

    What *does* survive the full pipeline is ``image/svg+xml``: Quarto
    writes it to a file, and Pandoc references it via
    ``pandoc.Image``.  So we smuggle the ICML XML out as base64 inside
    an otherwise-empty 1x1 SVG, and let the
    :file:`lib/quarto_extensions/icml_gt/icml_gt.lua` filter look for
    those carrier SVGs, read them back off disk, decode the embedded
    XML, and replace the Figure with ``pandoc.RawBlock("icml", xml)``
    before Pandoc writes the ICML Story.  On any exception we fall back
    to the PNG raster path so a single bad table can't break the whole
    ICML build.
    """
    from IPython.display import SVG, display

    try:
        from lib.great_tables.icml import render_gt_to_icml  # local import: keep HTML path light

        icml_xml = render_gt_to_icml(table)
    except Exception as exc:  # pragma: no cover — safety net for unexpected GT shapes
        import warnings

        warnings.warn(
            f"GT → ICML conversion failed ({type(exc).__name__}: {exc}); falling back to PNG raster for this table.",
            stacklevel=2,
        )
        _display_gt_as_image(table)
        return

    encoded = base64.b64encode(icml_xml.encode("utf-8")).decode("ascii")
    # The SVG itself is a 1x1 placeholder — InDesign never sees it; the
    # Lua filter unconditionally replaces the whole Figure before the
    # ICML writer runs.  Chunk the base64 payload into 76-char lines to
    # keep downstream tools happy with the SVG.
    lines = [encoded[i : i + 76] for i in range(0, len(encoded), 76)]
    payload = "\n".join(lines)
    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" width="1pt" height="1pt" version="1.1">\n'
        f"  <desc>switchbox-icml-gt\ndata-icml-b64:\n{payload}\n</desc>\n"
        "</svg>\n"
    )
    display(SVG(data=svg))
