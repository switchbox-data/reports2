"""Helpers for Quarto Manuscript rendering.

Quarto Manuscript's ``{{< embed >}}`` shortcode breaks on certain cell
output types because Pandoc's ``--to ipynb`` conversion cannot round-trip
them faithfully.  The helpers here produce outputs that survive the
embed pipeline so ``{{< embed >}}`` can be used instead of file-based
workarounds.

* **``display_svg``** — for matplotlib figures (multi-MIME → single SVG).
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


def _render_gt_as_image() -> bool:
    """Return True if GT tables should be rendered as images (for ICML).

    Checks for ``SWITCHBOX_TYPESET=1``, set by ``lib.just.typeset`` before
    running Quarto.  This is more reliable than ``QUARTO_EXECUTE_INFO``
    because embedded notebooks may not receive the ICML format info — they
    get re-executed generically when their cached ``.out.ipynb`` is removed.
    """
    return os.environ.get("SWITCHBOX_TYPESET") == "1"


def display_svg(fig: Figure) -> None:
    """Render a matplotlib figure as SVG and display it via IPython.

    Quarto Manuscript's ``{{< embed >}}`` breaks on cells that produce
    multi-MIME output (e.g. a raw matplotlib Figure emits both PNG and
    text/plain).  Finishing the cell with a single ``IPython.display.SVG``
    object avoids this by producing only an ``image/svg+xml`` MIME type.

    After saving to SVG the figure is closed to free memory.
    """
    import matplotlib.pyplot as plt
    from IPython.display import SVG, display

    fig.savefig(buf := io.BytesIO(), format="svg", bbox_inches="tight")
    plt.close(fig)
    display(SVG(data=buf.getvalue()))


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
    if _render_gt_as_image():
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
