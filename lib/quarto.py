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
  * **ICML** (``SWITCHBOX_TYPESET=1``): vector SVG with real ``<text>``
    elements, via Chrome's CDP ``Page.printToPDF`` → Inkscape's native
    PDF importer.  Requires ``inkscape`` on ``PATH`` (provisioned in
    ``infra/user-data.sh`` and ``.devcontainer/Dockerfile``).
"""

from __future__ import annotations

import base64
import io
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from great_tables import GT
    from matplotlib.figure import Figure


def _render_gt_as_svg() -> bool:
    """Return True when GT tables must be rendered as vector SVG (ICML only).

    Set by ``lib.just.typeset`` via ``SWITCHBOX_TYPESET=1``.  ICML is placed
    in InDesign, which handles SVG natively with full vector fidelity and
    editable text; rasterizing at 300 DPI loses both.
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
    * **ICML** (``SWITCHBOX_TYPESET=1``): renders the table as a vector
      SVG with real ``<text>`` elements.  The pipeline is Chrome CDP
      ``Page.printToPDF`` (vector) → Inkscape's native PDF importer
      (``inkscape --export-plain-svg``).  InDesign places the SVG
      natively with editable text.  Requires ``inkscape`` on ``PATH``
      (provisioned in ``infra/user-data.sh`` and
      ``.devcontainer/Dockerfile``).

    Usage in ``analysis.qmd``::

        from lib.quarto import display_gt

        my_table = GT(df).fmt_currency(...)
        display_gt(my_table)

    Then in ``index.qmd``::

        {{< embed notebooks/analysis.qmd#tbl-my-table >}}
    """
    if _render_gt_as_svg():
        _display_gt_as_svg(table)
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


def _display_gt_as_svg(table: GT, *, scale: float = 1.0) -> None:
    """Render GT to a vector SVG with real ``<text>`` and display it.

    Pipeline: GT HTML → headless Chrome (``Page.printToPDF``) → vector
    PDF → Inkscape (``--export-plain-svg``, native importer) → SVG.

    The native Inkscape importer preserves PDF text as ``<text>`` /
    ``<tspan>`` elements; the ``--pdf-poppler`` backend would convert
    them to outlined paths, which is why we don't pass it.

    The Switchbox house fonts must be installed as TrueType-flavored
    ``*.ttf`` (not CFF-flavored ``*.otf``) in the server's fontconfig.
    Chrome embeds CFF-OTFs as PDF Type 3 fonts, which Inkscape's native
    importer can't decode for font size — every ``<text>`` ends up with
    ``font-size:1e-32px`` (invisible). TrueType-flavored fonts get
    embedded as CID TrueType and decode correctly. See
    ``reports/.style/fonts/README.md`` for the OTF → TTF conversion.

    InDesign places the resulting SVG natively with editable text.
    """
    from great_tables._utils_selenium import _get_web_driver
    from IPython.display import SVG, display

    if shutil.which("inkscape") is None:
        raise RuntimeError(
            "Inkscape not found on PATH. GT → SVG for ICML requires "
            "`apt-get install inkscape` (see infra/user-data.sh and "
            ".devcontainer/Dockerfile)."
        )

    html = table.as_raw_html(make_page=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        html_path = tmp / "table.html"
        html_path.write_text(html, encoding="utf-8")
        pdf_path = tmp / "table.pdf"
        svg_path = tmp / "table.svg"

        wdriver_cls = _get_web_driver("chrome")
        with wdriver_cls() as driver:
            driver.set_window_size(6000, 6000)
            driver.get(f"file://{html_path}")

            # Kill body margin/padding/centering so the table is flush to
            # (0,0), apply zoom, force a reflow.
            driver.execute_script(
                "var s=document.createElement('style');"
                "s.innerText='html,body{margin:0!important;padding:0!important;}"
                " body>div{margin:0!important;padding:0!important;}';"
                "document.head.appendChild(s);"
                "var el=document.getElementsByTagName('table')[0];"
                f"el.style.zoom='{scale}';"
                "el.parentNode.style.display='none';"
                "el.parentNode.style.display='';"
            )
            time.sleep(0.1)

            # Shrink window to the table's intrinsic width so the browser
            # doesn't center or soft-wrap it.
            table_w = driver.execute_script("return document.getElementsByTagName('table')[0].scrollWidth;")
            driver.set_window_size(int(table_w * scale + 20), 6000)
            time.sleep(0.1)

            dims = driver.execute_script(
                "var t=document.getElementsByTagName('table')[0];"
                "var r=t.getBoundingClientRect();"
                "return [t.scrollWidth, t.scrollHeight, r.left, r.top,"
                " document.body.scrollHeight];"
            )
            client_w, scroll_h, left, top, body_h = dims

            pad = 8
            width_px = client_w * scale + max(left, 0) * 2 + pad * 2
            height_px = max(scroll_h * scale, body_h) + max(top, 0) * 2 + pad * 2
            width_in = width_px / 96.0
            height_in = height_px / 96.0

            # ``Page.printToPDF`` paginates by default; ``preferCSSPageSize``
            # plus an explicit ``@page`` matching our page dims keeps the
            # whole table on one page so Inkscape emits a single SVG.
            driver.execute_script(
                "var s=document.createElement('style');"
                f"s.innerText='@page {{ size: {width_in}in {height_in}in;"
                " margin: 0; }}';"
                "document.head.appendChild(s);"
            )

            pdf_result = driver.execute_cdp_cmd(
                "Page.printToPDF",
                {
                    "printBackground": True,
                    "preferCSSPageSize": True,
                    "paperWidth": width_in,
                    "paperHeight": height_in,
                    "marginTop": 0,
                    "marginBottom": 0,
                    "marginLeft": 0,
                    "marginRight": 0,
                    "scale": 1.0,
                },
            )
            pdf_path.write_bytes(base64.b64decode(pdf_result["data"]))

        # Do NOT pass --pdf-poppler: the native Inkscape importer keeps
        # text as <text>/<tspan>; the poppler backend outlines it.
        subprocess.run(
            [
                "inkscape",
                "--export-type=svg",
                "--export-plain-svg",
                "-o",
                str(svg_path),
                str(pdf_path),
            ],
            check=True,
            timeout=120,
            capture_output=True,
        )

        svg_bytes = svg_path.read_bytes()

    display(SVG(data=svg_bytes))
