"""Helpers for Quarto Manuscript rendering.

Quarto Manuscript's ``{{< embed >}}`` shortcode breaks on certain cell
output types because Pandoc's ``--to ipynb`` conversion cannot round-trip
them faithfully.  The helpers here produce outputs that survive the
embed pipeline so ``{{< embed >}}`` can be used instead of file-based
workarounds.

* **``display_svg``** — for matplotlib figures (multi-MIME → single SVG).
* **``display_gt``** — for Great Tables (``text/html`` → base64-decoded HTML).
"""

from __future__ import annotations

import base64
import io
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from great_tables import GT
    from matplotlib.figure import Figure


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
    """Display a Great Tables object so it survives ``{{< embed >}}``.

    Pandoc's ``--to ipynb`` conversion truncates raw ``text/html`` cell
    outputs, reducing GT tables to a stray ``</div>``.  This helper
    base64-encodes the HTML and wraps it in a ``<div>`` + ``<script>``
    that decodes at page load.  Because the GT markup is opaque to Pandoc
    (hidden inside a base64 string attribute), it passes through the
    embed pipeline intact.

    The decoded HTML includes GT's scoped ``<style>`` block, so all
    formatting is preserved.  Unlike an iframe approach, the table
    participates in the host page's CSS cascade (fonts, colors).

    Usage in ``analysis.qmd``::

        from lib.quarto import display_gt

        my_table = GT(df).fmt_currency(...)
        display_gt(my_table)

    Then in ``index.qmd``::

        {{< embed notebooks/analysis.qmd#tbl-my-table >}}
    """
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
