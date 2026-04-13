"""Helpers for Quarto Manuscript rendering.

Quarto Manuscript's ``{{< embed >}}`` shortcode breaks on certain cell
output types because Pandoc's ``--to ipynb`` conversion cannot round-trip
them faithfully.  The helpers here produce outputs that survive the
embed pipeline so ``{{< embed >}}`` can be used instead of file-based
workarounds.

* **``display_figure``** — for matplotlib figures: SVG for HTML, high-res
  PNG for DOCX/ICML.  ``display_svg`` is a backwards-compatible alias.
* **``display_gt``** — for Great Tables (``text/html`` → base64-decoded HTML
  for HTML output; high-res PNG for ICML/non-HTML output).
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


def _render_as_raster() -> bool:
    """Return True when targeting a non-HTML format (DOCX, ICML).

    Checks for ``SWITCHBOX_GT_AS_IMAGE=1`` or ``SWITCHBOX_TYPESET=1``.
    Set by ``lib.just.typeset`` (ICML) and by the ``just draft`` recipe
    (DOCX).  Used by both ``display_figure`` (SVG → PNG) and
    ``display_gt`` (HTML → PNG) to produce raster output that embeds
    cleanly in Word and InDesign.
    """
    return os.environ.get("SWITCHBOX_GT_AS_IMAGE") == "1" or os.environ.get("SWITCHBOX_TYPESET") == "1"


def display_figure(fig: Figure, *, dpi: int = 300) -> None:
    """Render a matplotlib figure as SVG (HTML) or high-res PNG (DOCX/ICML).

    Quarto Manuscript's ``{{< embed >}}`` breaks on cells that produce
    multi-MIME output (e.g. a raw matplotlib Figure emits both PNG and
    text/plain).  This helper produces a single MIME output that survives
    the embed pipeline.

    The output format depends on the target:

    * **HTML** (default): ``image/svg+xml`` — sharp at any zoom, styled by
      CSS, inlined by ``just render``'s post-processing.
    * **DOCX / ICML**: ``image/png`` at *dpi* (default 300) — avoids the
      fuzzy rasterization that happens when Pandoc converts SVG via
      ``rsvg-convert`` at its default 96 DPI.

    Format detection reuses ``_render_as_raster()`` (env vars
    ``SWITCHBOX_GT_AS_IMAGE`` / ``SWITCHBOX_TYPESET``).

    After saving, the figure is closed to free memory.
    """
    import matplotlib.pyplot as plt

    if _render_as_raster():
        from IPython.display import Image, display

        fig.savefig(buf := io.BytesIO(), format="png", dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        display(Image(data=buf.getvalue(), format="png"))
    else:
        from IPython.display import SVG, display

        fig.savefig(buf := io.BytesIO(), format="svg", bbox_inches="tight")
        plt.close(fig)
        display(SVG(data=buf.getvalue()))


display_svg = display_figure


def display_gt(table: GT) -> None:
    """Display a Great Tables object so it works in both HTML and ICML.

    **HTML output** (default): base64-encodes the GT HTML and wraps it in a
    ``<div>`` + ``<script>`` that decodes at page load.  This survives the
    Quarto Manuscript ``{{< embed >}}`` pipeline (which truncates raw
    ``text/html``).

    **ICML output** (detected via ``QUARTO_EXECUTE_INFO``): renders the table
    to a high-res PNG (3x scale, ~300 DPI at full width) using GT's headless
    Chrome screenshot and displays it via ``IPython.display.Image``.  Quarto
    treats this like any other figure — saving it to
    ``docs/index_files/figure-icml/`` and wiring up the ICML ``<Link>``
    reference automatically.

    Usage in ``analysis.qmd``::

        from lib.quarto import display_gt

        my_table = GT(df).fmt_currency(...)
        display_gt(my_table)

    Then in ``index.qmd``::

        {{< embed notebooks/analysis.qmd#tbl-my-table >}}
    """
    if _render_as_raster():
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
