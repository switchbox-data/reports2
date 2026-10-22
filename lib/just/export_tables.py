"""Export native Markdown tables from a rendered Quarto document as PNGs.

Some documents (e.g. the CT ``expert_testimony.qmd``) author their tables as
native Markdown pipe tables directly in the ``.qmd`` — with a
``: caption {#tbl-...}`` attribute — rather than ``{{< embed >}}``-ing a
rendered table from a notebook.  Such tables have *no* standalone image
output for :mod:`lib.just.export_figures` to pick up.

This script fills that gap: it opens the report's rendered HTML in headless
Chrome (via selenium, the same engine ``great_tables`` uses) and screenshots
each table element, preserving the report's Switchbox CSS and fonts.  Files
are named after the table's "Table N" number so they line up with the
rendered document (and the DOCX), which makes manual replacement in Word
straightforward.

Each table float in the Quarto HTML is a ``<div id="tbl-...">`` wrapping a
``<figcaption>Table&nbsp;N: ...</figcaption>`` and a ``<table>``.  We
screenshot the inner ``<table>`` (table-only, no caption — matching how
figures export the plot without its Quarto caption).  To capture the caption
too, screenshot the ``#tbl-...`` div instead (see ``--include-caption``).

Usage::

    # From the report directory (after `just render`):
    uv run python -m lib.just.export_tables expert_testimony.qmd

    # "Table 1.png" names, 3x device scale, custom output dir:
    uv run python -m lib.just.export_tables expert_testimony.qmd \
        --name-style word --scale 3 --output-dir expert_testimony_figures

Requires a Chrome/Chromium binary on the system; selenium's Selenium Manager
auto-provisions the matching driver (needs network access on first run).
"""

from __future__ import annotations

import argparse
import contextlib
import re
import sys
import time
from pathlib import Path

from lib.just.export_figures import format_output_name

# {#tbl-...} caption attributes, in document order.
TBL_ID_PATTERN = re.compile(r"\{#(tbl-[A-Za-z0-9_-]+)\}")

# "Table 1", "Table&nbsp;1", etc. (\s matches the NBSP for str patterns).
CAPTION_NUM_PATTERN = re.compile(r"Table\s*(\d+)")


def parse_table_ids(qmd_path: Path) -> list[str]:
    """Return ``tbl-`` ids in document order, from ``{#tbl-...}`` captions."""
    text = qmd_path.read_text()
    ids: list[str] = []
    seen: set[str] = set()
    for m in TBL_ID_PATTERN.finditer(text):
        tid = m.group(1)
        if tid in seen:
            continue
        seen.add(tid)
        ids.append(tid)
    return ids


def _extract_between(html: str, open_prefix: str, close_tag: str) -> str:
    """Return ``html[start:end]`` spanning ``open_prefix`` .. ``close_tag`` (inclusive)."""
    start = html.find(open_prefix)
    if start < 0:
        return ""
    end = html.find(close_tag, start)
    if end < 0:
        return ""
    return html[start : end + len(close_tag)]


def _body_open_tag(html: str) -> str:
    """Return the ``<body ...>`` opening tag (to preserve its classes)."""
    start = html.find("<body")
    if start < 0:
        return "<body>"
    end = html.find(">", start)
    return html[start : end + 1]


def _extract_div(html: str, elem_id: str) -> str | None:
    """Return the full ``<div id="elem_id" ...>...</div>`` node by depth-matching.

    Quarto's HTML is well-formed, so we can balance ``<div>``/``</div>`` from
    the target's opening tag to find its matching close.
    """
    start = html.find(f'<div id="{elem_id}"')
    if start < 0:
        return None
    i = start
    depth = 0
    while i < len(html):
        nxt_open = html.find("<div", i)
        nxt_close = html.find("</div>", i)
        if nxt_close < 0:
            return None
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open + 4
        else:
            depth -= 1
            i = nxt_close + 6
            if depth == 0:
                return html[start:i]
    return None


def _build_minimal_page(html_path: Path, tbl_ids: list[str], *, width: int) -> tuple[str, list[str]]:
    """Assemble a lightweight HTML page containing only the table nodes.

    Reuses the report's ``<head>`` (theme CSS, fonts) and ``<body>`` classes so
    the tables render with their real Switchbox styling, but omits the ~38
    inlined figures that make the full page too heavy for headless Chrome.
    """
    html = html_path.read_text()
    head = _extract_between(html, "<head", "</head>")
    body_open = _body_open_tag(html)

    blocks: list[str] = []
    found: list[str] = []
    for tid in tbl_ids:
        node = _extract_div(html, tid)
        if node is None:
            continue
        found.append(tid)
        # Constrain width to match the report's body column so the tables wrap
        # exactly as they do in the published document.
        blocks.append(f'<div style="max-width:{width}px;margin:24px;">{node}</div>')

    page = f"<!DOCTYPE html><html>{head}{body_open}{''.join(blocks)}</body></html>"
    return page, found


def _make_driver(scale: float):
    """Headless Chrome with a high device-scale-factor for crisp screenshots."""
    from selenium import webdriver

    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--hide-scrollbars")
    opts.add_argument(f"--force-device-scale-factor={scale}")
    # Large enough that wide tables are never wrapped onto extra lines.
    opts.add_argument("--window-size=2400,3000")
    # Robustness on headless servers / containers: avoid the small /dev/shm
    # that triggers "Timed out receiving message from renderer", and disable
    # the GPU/sandbox that aren't available in these environments.
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    return webdriver.Chrome(options=opts)


def _caption_number(driver, tbl_id: str) -> int | None:
    """Read the "Table N" number from a table float's caption, if present."""
    from selenium.webdriver.common.by import By

    try:
        cap = driver.find_element(By.CSS_SELECTOR, f"#{tbl_id} figcaption")
    except Exception:
        return None
    m = CAPTION_NUM_PATTERN.search(cap.text)
    return int(m.group(1)) if m else None


def export_tables(
    qmd_path: Path,
    output_dir: Path,
    *,
    scale: float = 3.0,
    name_style: str = "numbered",
    include_caption: bool = False,
    width: int = 700,
) -> None:
    """Screenshot every ``{#tbl-...}`` table from the rendered HTML as a PNG.

    Rather than loading the full report HTML (too heavy for headless Chrome
    once ~38 figures are inlined), this extracts just the table nodes into a
    lightweight standalone page that reuses the report's ``<head>`` styling,
    then screenshots each table at a high device-scale-factor.
    """
    qmd_path = qmd_path.resolve()
    report_dir = qmd_path.parent
    html_path = report_dir / "docs" / f"{qmd_path.stem}.html"
    if not html_path.exists():
        print(f"ERROR: Rendered HTML not found: {html_path}")
        print("       Run 'just render' first to generate the HTML.")
        sys.exit(1)

    tbl_ids = parse_table_ids(qmd_path)
    if not tbl_ids:
        print(f"No {{#tbl-...}} table definitions found in {qmd_path.name}")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    page, found = _build_minimal_page(html_path, tbl_ids, width=width)
    skipped = [t for t in tbl_ids if t not in found]

    # Write the minimal page alongside the real HTML so its relative CSS/font
    # references (site_libs/, *_files/) still resolve.
    tmp_path = html_path.parent / f"_{qmd_path.stem}_tables_tmp.html"
    tmp_path.write_text(page)

    from selenium.webdriver.common.by import By

    driver = _make_driver(scale)
    driver.set_page_load_timeout(120)
    exported = 0
    try:
        driver.get(tmp_path.resolve().as_uri())
        # Let webfonts settle so text metrics (and thus table widths) are final.
        with contextlib.suppress(Exception):
            driver.execute_script("return document.fonts.ready")
        time.sleep(0.8)

        for i, tbl_id in enumerate(found, start=1):
            selector = f"#{tbl_id}" if include_caption else f"#{tbl_id} table"
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
            except Exception:
                skipped.append(tbl_id)
                continue

            number = _caption_number(driver, tbl_id) or i
            out_name = format_output_name("Table", number, name_style=name_style)
            out_path = output_dir / out_name

            element.screenshot(str(out_path))
            print(f"  {out_name}  ←  {tbl_id}")
            exported += 1
    finally:
        driver.quit()
        tmp_path.unlink(missing_ok=True)

    print(f"\n✅ Exported {exported} tables to {output_dir}/")
    if skipped:
        print(f"\n⚠️  {len(skipped)} tables not found in the rendered HTML (run 'just render' to regenerate):")
        for s in skipped:
            print(f"     - {s}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export native Markdown tables from a rendered Quarto document as PNGs."
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
        "--scale",
        type=float,
        default=3.0,
        help="Device scale factor for high-res screenshots (default: 3.0)",
    )
    parser.add_argument(
        "--name-style",
        choices=["numbered", "word"],
        default="numbered",
        help=(
            "Output filename style: 'numbered' → Table_01.png (default); "
            "'word' → 'Table 1.png' to match the rendered document's labels."
        ),
    )
    parser.add_argument(
        "--include-caption",
        action="store_true",
        help="Capture the Quarto caption above the table, not just the table itself.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=700,
        help="Body column width (px) the tables are laid out in (default: 700, the report body width).",
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

    export_tables(
        qmd_path,
        output_dir,
        scale=args.scale,
        name_style=args.name_style,
        include_caption=args.include_caption,
        width=args.width,
    )


if __name__ == "__main__":
    main()
