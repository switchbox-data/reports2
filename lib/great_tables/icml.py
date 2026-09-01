"""Render :class:`great_tables.GT` objects to native ICML ``<Table>`` XML.

The output is a *fragment* (no ``<?xml?>`` / ``<Document>`` wrapper) that
Pandoc embeds verbatim into a Quarto-generated ICML story via a
``{=icml}`` raw block.  When the designer opens the ICML in InDesign the
table drops in as a native editable table that reflows with the frame
— unlike placed SVG, which shrinks text when the frame resizes.

The converter walks GT's already-populated internal state
(``_boxhead``, ``_spanners``, ``_stub``, ``_body.body``, ``_heading``,
``_source_notes``, ``_styles``) instead of parsing rendered HTML so the
mapping stays semantic: we know "this column is right-aligned" rather
than guessing from CSS.

Named styles (``TableStyle/Table Inline``, ``CellStyle/Cell Header``,
``ParagraphStyle/TablePar > TableHeader``, etc.) are *referenced by
name* — they are defined in the designer's InDesign template and
survive the round-trip through Pandoc's ICML writer.  If a name does
not exist in the target document InDesign degrades gracefully to its
defaults without erroring.

Public API:

* :func:`render_gt_to_icml` — the only entry point; takes a ``GT``
  object and returns a string of ICML XML.
* :func:`set_icml_table_style` — optional per-table hook that overrides
  the default ``TableStyle/Table Inline`` used for memo-inline tables.
"""

from __future__ import annotations

import html as _html
import re
import secrets
import warnings
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from great_tables import GT


# =============================================================================
# Public API
# =============================================================================


DEFAULT_TABLE_STYLE = "Table Inline"
_ICML_TABLE_STYLE_ATTR = "_switchbox_icml_table_style"


def set_icml_table_style(gt: GT, style_name: str) -> GT:
    """Override the ICML ``TableStyle`` used when emitting *gt* as native ICML.

    By default :func:`render_gt_to_icml` references
    ``TableStyle/Table Inline`` — the designer's style for small tables
    that flow inline with memo body copy.  Pass ``"Table"`` (or any
    other style name defined in the target InDesign document) to pick a
    different named style per table.

    Returns the GT unchanged (mutated in place) so it's chainable.
    """
    setattr(gt, _ICML_TABLE_STYLE_ATTR, style_name)
    return gt


def render_gt_to_icml(gt: GT) -> str:
    """Serialize a ``GT`` object to a native ICML fragment.

    The returned string contains, in order:

    1. Optional ``ParagraphStyle/Caption`` paragraph for title + subtitle.
    2. A ``ParagraphStyle/Paragraph Table Anchor`` wrapper containing
       the ``<Table>`` element.
    3. One ``ParagraphStyle/Caption`` paragraph per source note.

    Raises
    ------
    ValueError
        If *gt* has no visible data columns.
    """
    built = gt._build_data(context="html")
    ast = _build_table_ast(built)
    return _serialize_ast(ast)


# =============================================================================
# AST — captures table structure + semantics before XML serialization.
# =============================================================================


@dataclass
class _Run:
    """A contiguous character-level run inside a paragraph."""

    text: str = ""
    bold: bool = False
    italic: bool = False
    color: str | None = None  # hex like "#RRGGBB"
    # ``break_before`` emits a ``<Br/>`` (forced line break) immediately
    # before this run.  Used by ``<br>`` inside markdown cells.
    break_before: bool = False


@dataclass
class _Cell:
    """One ``<Cell>`` of the table grid."""

    row: int
    col: int
    row_span: int = 1
    col_span: int = 1
    # AppliedCellStyle (e.g. "Cell", "Cell Header")
    cell_style: str = "Cell"
    # AppliedParagraphStyle (e.g. "TablePar", "TablePar > TableHeader")
    paragraph_style: str = "TablePar"
    runs: list[_Run] = field(default_factory=list)
    # Inline overrides from ``tab_style``.
    fill_color: str | None = None  # hex "RRGGBB" (no '#'); expands to Color/gt-XXXXXX
    # "merged_into" means the cell exists as a span-anchor somewhere else;
    # we still emit an empty ``<Cell>`` placeholder to keep the grid valid.
    merged_into: bool = False


@dataclass
class _Table:
    rows: int
    cols: int
    table_style: str
    column_widths_pt: list[float | None]  # per-column, None = let ICML default
    cells: dict[tuple[int, int], _Cell]
    heading_title: str | None = None
    heading_subtitle: str | None = None
    source_notes: list[str] = field(default_factory=list)


# =============================================================================
# Table walking
# =============================================================================


# Cell character style default size (pt). Matches the designer's
# consistent 8pt convention for in-table text in memo-inline tables.
_CELL_POINT_SIZE = "8"


def _build_table_ast(gt: GT) -> _Table:
    """Walk a built GT object and return a populated :class:`_Table`."""
    boxhead = gt._boxhead

    data_cols = [c for c in boxhead if c.type.name == "default" and c.visible]
    stub_cols = [c for c in boxhead if c.type.name == "stub" and c.visible]
    group_cols = [c for c in boxhead if c.type.name == "row_group" and c.visible]

    if not data_cols and not stub_cols:
        raise ValueError("GT object has no visible columns to render as ICML")

    has_stub = bool(stub_cols)
    has_groups = bool(group_cols)

    # Visible grid columns: optional stub + data columns.
    grid_cols: list[Any] = []
    if has_stub:
        grid_cols.append(stub_cols[0])
    grid_cols.extend(data_cols)
    col_count = len(grid_cols)

    # Spanner header rows — currently one level (nested spanners deferred).
    spanner_list = list(gt._spanners) if gt._spanners else []
    # Map spanner -> set of grid-col indices it spans.
    active_spanners: list[tuple[Any, list[int]]] = []
    for sp in spanner_list:
        # Find grid-col indices for each spanner variable.
        indices = []
        for var in sp.vars:
            for i, c in enumerate(grid_cols):
                if c.var == var:
                    indices.append(i)
                    break
        if indices:
            active_spanners.append((sp, sorted(indices)))

    has_spanner_row = bool(active_spanners)

    # Group row is a new row that spans all columns, inserted before the
    # first row of each distinct group.  We precompute those.
    group_breakpoints: list[tuple[int, str]] = []
    if has_groups:
        seen_groups: list[str] = []
        for row_info in gt._stub:
            g = row_info.group_id
            if g not in seen_groups:
                seen_groups.append(g)
                group_breakpoints.append((row_info.rownum_i, g))

    # Now compute total row count:
    #   [spanner row (maybe)] [column label row] [group row + body rows ...]
    n_header_rows = (1 if has_spanner_row else 0) + 1
    body_row_count = len(gt._stub) if gt._stub else len(gt._tbl_data)
    total_rows = n_header_rows + body_row_count + len(group_breakpoints)

    # Pre-compute column widths (px from GT → pt).
    column_widths_pt: list[float | None] = []
    for c in grid_cols:
        column_widths_pt.append(_parse_dimension_to_pt(c.column_width))

    cells: dict[tuple[int, int], _Cell] = {}

    cur_row = 0

    # Spanner row — each spanner anchors in its leftmost grid col with ColumnSpan.
    if has_spanner_row:
        # Track which grid-col indices in this row are covered by a spanner.
        covered: set[int] = set()
        for sp, indices in active_spanners:
            # Only handle contiguous spans (GT always produces contiguous ones).
            lo, hi = min(indices), max(indices)
            anchor_col = lo
            span = hi - lo + 1
            label = _extract_label(sp.spanner_label)
            anchor_cell = _Cell(
                row=cur_row,
                col=anchor_col,
                row_span=1,
                col_span=span,
                cell_style="Cell Header",
                paragraph_style="TablePar > TableHeader",
                runs=_text_to_runs(label),
            )
            cells[(cur_row, anchor_col)] = anchor_cell
            for k in range(anchor_col, anchor_col + span):
                covered.add(k)
                if k != anchor_col:
                    # Placeholder so ICML sees the grid cell even though it's part of the span.
                    cells[(cur_row, k)] = _Cell(
                        row=cur_row,
                        col=k,
                        cell_style="Cell Header",
                        paragraph_style="TablePar > TableHeader",
                        merged_into=True,
                    )
        # Empty cells (no spanner above) fill with "Cell Header" and blank content.
        for k in range(col_count):
            if k not in covered:
                cells[(cur_row, k)] = _Cell(
                    row=cur_row,
                    col=k,
                    cell_style="Cell Header",
                    paragraph_style="TablePar > TableHeader",
                    runs=[],
                )
        cur_row += 1

    # Column-label row.
    stub_offset = 1 if has_stub else 0
    # Stubhead in (cur_row, 0) if we have a stub.
    if has_stub:
        stubhead_label = _extract_label(gt._stubhead) if gt._stubhead else ""
        cells[(cur_row, 0)] = _Cell(
            row=cur_row,
            col=0,
            cell_style="Cell Header",
            paragraph_style="TablePar > TableHeader",
            runs=_text_to_runs(stubhead_label),
        )
    for i, c in enumerate(data_cols):
        col_idx = stub_offset + i
        para_style = _header_paragraph_style(c.column_align)
        cells[(cur_row, col_idx)] = _Cell(
            row=cur_row,
            col=col_idx,
            cell_style="Cell Header",
            paragraph_style=para_style,
            runs=_text_to_runs(_extract_label(c.column_label)),
        )
    cur_row += 1

    # Body rows.  Iterate GT's ``_stub`` if present (drives ordering +
    # groups); otherwise fall back to ``_tbl_data``.
    body_df = gt._body.body  # pandas or polars; we index by rownum_i
    raw_df = gt._tbl_data

    rowinfos = list(gt._stub) if gt._stub else None
    rowcount = len(rowinfos) if rowinfos is not None else len(raw_df)

    # Track which group each body row belongs to so we can insert group header rows.
    group_inserted: set[str] = set()

    # Pre-bin ``_styles`` by (rownum_i, colname) for O(1) lookup.
    style_index = _index_styles(gt._styles or [])

    for i in range(rowcount):
        if rowinfos is not None:
            ri = rowinfos[i]
            gid = ri.group_id
            rownum = ri.rownum_i
            rowname = ri.rowname or ""
        else:
            gid = None
            rownum = i
            rowname = ""

        # Group header row before first row of this group.
        if has_groups and gid is not None and gid not in group_inserted:
            group_inserted.add(gid)
            group_label = _extract_group_label(gt, gid, group_cols[0].var)
            # Anchor in col 0 with ColumnSpan=col_count.
            cells[(cur_row, 0)] = _Cell(
                row=cur_row,
                col=0,
                row_span=1,
                col_span=col_count,
                cell_style="Cell",
                paragraph_style="Table Row Header",
                runs=_text_to_runs(group_label),
            )
            for k in range(1, col_count):
                cells[(cur_row, k)] = _Cell(
                    row=cur_row,
                    col=k,
                    cell_style="Cell",
                    paragraph_style="Table Row Header",
                    merged_into=True,
                )
            cur_row += 1

        # Stub cell (row name).
        if has_stub:
            stub_runs = _text_to_runs(rowname)
            stub_styles = style_index.get((rownum, stub_cols[0].var))
            cells[(cur_row, 0)] = _apply_cell_styles(
                _Cell(
                    row=cur_row,
                    col=0,
                    cell_style="Cell",
                    paragraph_style="Table Row Header",
                    runs=stub_runs,
                ),
                stub_styles,
            )

        # Data cells.
        for di, c in enumerate(data_cols):
            col_idx = stub_offset + di
            val = _cell_value(body_df, raw_df, rownum, c.var)
            para_style = _body_paragraph_style(c.column_align)
            styles = style_index.get((rownum, c.var))
            cells[(cur_row, col_idx)] = _apply_cell_styles(
                _Cell(
                    row=cur_row,
                    col=col_idx,
                    cell_style="Cell",
                    paragraph_style=para_style,
                    runs=_cell_html_to_runs(val),
                ),
                styles,
            )

        cur_row += 1

    assert cur_row == total_rows, f"row-count mismatch: {cur_row} vs {total_rows}"

    # Resolve per-table ICML style override.
    override = getattr(gt, _ICML_TABLE_STYLE_ATTR, None)
    table_style = override or DEFAULT_TABLE_STYLE

    # Heading / source notes.
    title = _extract_label(gt._heading.title) if gt._heading and gt._heading.title else None
    subtitle = _extract_label(gt._heading.subtitle) if gt._heading and gt._heading.subtitle else None
    source_notes = [_extract_label(s) for s in (gt._source_notes or [])]

    return _Table(
        rows=total_rows,
        cols=col_count,
        table_style=table_style,
        column_widths_pt=column_widths_pt,
        cells=cells,
        heading_title=title,
        heading_subtitle=subtitle,
        source_notes=source_notes,
    )


def _index_styles(styles: list[Any]) -> dict[tuple[int, str], list[Any]]:
    """Bin GT ``StyleInfo`` entries by ``(rownum_i, colname)``."""
    out: dict[tuple[int, str], list[Any]] = {}
    for si in styles:
        if si.rownum is None or si.colname is None:
            # Locations without a specific cell (e.g. LocTitle) are skipped
            # — we handle title/subtitle separately as captions.
            continue
        key = (si.rownum, si.colname)
        out.setdefault(key, []).extend(si.styles)
    return out


def _apply_cell_styles(cell: _Cell, styles: list[Any] | None) -> _Cell:
    """Fold ``tab_style`` entries (fills + text) onto a cell."""
    if not styles:
        return cell
    for s in styles:
        cls = type(s).__name__
        if cls == "CellStyleFill":
            color = getattr(s, "color", None)
            if color:
                cell.fill_color = _normalize_hex(color)
        elif cls == "CellStyleText":
            weight = getattr(s, "weight", None)
            style = getattr(s, "style", None)
            color = getattr(s, "color", None)
            for run in cell.runs:
                if weight and weight.lower() in ("bold", "bolder", "700", "800", "900"):
                    run.bold = True
                if style and style.lower() == "italic":
                    run.italic = True
                if color:
                    run.color = color
        # CellStyleBorders, etc. — deferred (designer controls via named styles)
    return cell


def _cell_value(body_df: Any, raw_df: Any, rownum: int, col: str) -> str:
    """Pull formatted value from body; fall back to raw data if NA."""
    val = None
    try:
        val = body_df[col][rownum] if hasattr(body_df, "__getitem__") else None
    except Exception:
        val = None
    if val is None or (isinstance(val, float) and val != val):  # NaN check
        try:
            raw = raw_df[col][rownum] if hasattr(raw_df, "__getitem__") else None
        except Exception:
            raw = None
        if raw is None:
            return ""
        return str(raw)
    # Polars returns its Null sentinel as None already; pandas uses NaN
    try:
        import pandas as pd

        if pd.isna(val):
            try:
                raw = raw_df[col][rownum]
            except Exception:
                raw = None
            return "" if raw is None else str(raw)
    except Exception:
        pass
    return str(val) if val is not None else ""


def _extract_group_label(gt: GT, gid: str, group_var: str) -> str:
    """Grab the display label for a row group."""
    raw_df = gt._tbl_data
    try:
        for i in range(len(raw_df)):
            if str(raw_df[group_var][i]) == str(gid):
                return str(raw_df[group_var][i])
    except Exception:
        pass
    return str(gid)


def _header_paragraph_style(align: str | None) -> str:
    """Map column align → header paragraph style."""
    if align == "right":
        return "TablePar > TableHeader > RightAlign"
    if align == "center":
        return "TablePar > TableHeader > CenterAlign"
    return "TablePar > TableHeader"


def _body_paragraph_style(align: str | None) -> str:
    """Map column align → body paragraph style."""
    if align == "right":
        return "TablePar > RightAlign"
    if align == "center":
        return "TablePar > CenterAlign"
    return "TablePar"


def _extract_label(obj: Any) -> str:
    """Flatten GT's ``Md``/``Html``/``Text``/``str`` into a plain string.

    ``Md`` and ``Html`` are emitted as raw HTML — downstream
    :func:`_cell_html_to_runs` expands them into runs.  Raw ``str``
    passes through unchanged.
    """
    if obj is None:
        return ""
    # great_tables Md/Html have a .text field
    cls = type(obj).__name__
    if cls in ("Md", "Html", "Text"):
        return str(getattr(obj, "text", obj))
    return str(obj)


# =============================================================================
# HTML → runs (inline markdown + tab_header subtitle HTML)
# =============================================================================


class _RunParser(HTMLParser):
    """Tiny HTML → list[_Run] converter.

    Supports ``<br>`` (line break), ``<strong>``/``<b>``, ``<em>``/``<i>``,
    and ``<span>``. Anchors (``<a>``) pass through as plain text (ICML
    hyperlinks need a Story-level ``<HyperlinkDestination>`` block, which
    is out of scope for a table cell converter).  Any other tag is
    stripped — only its text content survives.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._bold = 0
        self._italic = 0
        self._color: str | None = None
        self._next_break = False
        self.runs: list[_Run] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            self._next_break = True
        elif tag in ("strong", "b"):
            self._bold += 1
        elif tag in ("em", "i"):
            self._italic += 1
        elif tag == "span":
            # Detect a handful of inline color hints; ignore the rest.
            for k, v in attrs:
                if k == "style" and v:
                    m = re.search(r"color\s*:\s*(#[0-9a-fA-F]{3,8}|rgb\([^)]+\))", v)
                    if m:
                        self._color = _normalize_css_color(m.group(1))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            self._next_break = True
        else:
            self.handle_starttag(tag, attrs)
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("strong", "b"):
            self._bold = max(0, self._bold - 1)
        elif tag in ("em", "i"):
            self._italic = max(0, self._italic - 1)
        elif tag == "span":
            self._color = None

    def handle_data(self, data: str) -> None:
        if not data:
            return
        self.runs.append(
            _Run(
                text=data,
                bold=self._bold > 0,
                italic=self._italic > 0,
                color=self._color,
                break_before=self._next_break,
            )
        )
        self._next_break = False


# Strip HTML comments (e.g. Quarto-inserted crossref comments) before parsing.
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def _cell_html_to_runs(text: str) -> list[_Run]:
    """Parse a cell's formatted HTML string into character runs."""
    if not text:
        return [_Run(text="")]
    if "<" not in text:
        # Fast path: raw text with no markup.
        return [_Run(text=_html.unescape(text))]
    cleaned = _HTML_COMMENT.sub("", text)
    parser = _RunParser()
    try:
        parser.feed(cleaned)
        parser.close()
    except Exception as exc:
        warnings.warn(f"ICML run-parse fell back to plain text: {exc}", stacklevel=2)
        return [_Run(text=_html.unescape(_strip_tags(cleaned)))]
    runs = parser.runs
    if not runs:
        return [_Run(text="")]
    return runs


def _text_to_runs(text: str) -> list[_Run]:
    """Convenience wrapper for paragraph-level labels that *may* be HTML."""
    return _cell_html_to_runs(text or "")


_TAG_STRIP = re.compile(r"<[^>]+>")


def _strip_tags(s: str) -> str:
    return _TAG_STRIP.sub("", s)


# =============================================================================
# Dimension + color helpers
# =============================================================================


def _parse_dimension_to_pt(val: Any) -> float | None:
    """Convert a CSS-style dimension to points.

    ``None`` / empty → None (ICML picks a default).  Percentages are
    skipped (warned): ICML column widths are absolute points, and we
    don't know the target frame width at emit time.
    """
    if val is None:
        return None
    s = str(val).strip().lower()
    if not s or s == "auto":
        return None
    m = re.match(r"^(-?\d*\.?\d+)\s*([a-z%]*)$", s)
    if not m:
        return None
    num = float(m.group(1))
    unit = m.group(2) or "px"
    if unit == "px":
        return num * 0.75  # 96px = 72pt
    if unit == "pt":
        return num
    if unit == "in":
        return num * 72
    if unit == "cm":
        return num * 28.3465
    if unit == "mm":
        return num * 2.83465
    if unit == "em":
        return num * 11  # rough: 1em ≈ 11pt in the theme
    if unit == "%":
        warnings.warn(
            "ICML column widths don't support percentages; letting InDesign auto-size",
            stacklevel=2,
        )
        return None
    return None


_HEX3 = re.compile(r"^#?([0-9a-fA-F]{3})$")
_HEX6 = re.compile(r"^#?([0-9a-fA-F]{6})$")


def _normalize_hex(color: str) -> str:
    """Normalize a hex color to uppercase 6 chars, no ``#``."""
    if not color:
        return "000000"
    s = color.strip()
    m = _HEX6.match(s)
    if m:
        return m.group(1).upper()
    m = _HEX3.match(s)
    if m:
        h = m.group(1)
        return (h[0] * 2 + h[1] * 2 + h[2] * 2).upper()
    # rgb()/named: best-effort fallback (designer can remap swatches).
    return "000000"


def _normalize_css_color(color: str) -> str:
    """Accept hex / rgb() / named → '#RRGGBB'."""
    s = color.strip()
    if s.startswith("#"):
        return "#" + _normalize_hex(s)
    m = re.match(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", s)
    if m:
        return f"#{int(m.group(1)):02X}{int(m.group(2)):02X}{int(m.group(3)):02X}"
    return s


# =============================================================================
# XML serialization
# =============================================================================


def _serialize_ast(tbl: _Table) -> str:
    """Serialize a :class:`_Table` to an ICML XML fragment."""
    parts: list[str] = []

    # Title + subtitle → Caption paragraph.
    caption = _format_caption(tbl.heading_title, tbl.heading_subtitle)
    if caption:
        parts.append(_wrap_caption(caption))

    # Table wrapper paragraph (Paragraph Table Anchor) → table.
    table_self = _gen_self_id()
    parts.append('<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/Paragraph Table Anchor">')
    parts.append('<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/Default">')

    # HeaderRowCount=0 matches the designer's convention for inline
    # memo tables: the first row is styled as header via CellStyle,
    # not marked as a repeating header.  Designers can toggle this
    # in InDesign later if the table spans pages.
    attrs = {
        "Self": table_self,
        "HeaderRowCount": "0",
        "BodyRowCount": str(tbl.rows),
        "FooterRowCount": "0",
        "ColumnCount": str(tbl.cols),
        "AppliedTableStyle": f"TableStyle/{tbl.table_style}",
        "TableDirection": "LeftToRightDirection",
        "TextTopInset": "4",
        "TextLeftInset": "4",
        "TextBottomInset": "4",
        "TextRightInset": "4",
    }
    parts.append("<Table " + _attr_str(attrs) + ">")

    # Column definitions
    for i, w_pt in enumerate(tbl.column_widths_pt):
        col_attrs = {
            "Self": f"{table_self}Col{i}",
            "Name": str(i),
        }
        if w_pt is not None:
            col_attrs["SingleColumnWidth"] = _fmt_float(w_pt)
        parts.append("<Column " + _attr_str(col_attrs) + "/>")

    # Row definitions — one <Row> per visual row, default height auto.
    for r in range(tbl.rows):
        parts.append(f'<Row Self="{table_self}Row{r}" Name="{r}"/>')

    # Cells
    for r in range(tbl.rows):
        for c in range(tbl.cols):
            cell = tbl.cells.get((r, c))
            if cell is None:
                # Missing cell — emit a blank placeholder for a valid grid.
                cell = _Cell(row=r, col=c, runs=[])
            parts.append(_serialize_cell(cell, table_self))

    parts.append("</Table>")
    parts.append("</CharacterStyleRange>")
    parts.append("</ParagraphStyleRange>")

    # Source notes → one Caption paragraph per note.
    for note in tbl.source_notes:
        parts.append(_wrap_caption(note))

    return "\n".join(parts)


def _serialize_cell(cell: _Cell, table_self: str) -> str:
    """Serialize one ``<Cell>`` with its ParagraphStyleRange content."""
    cell_attrs: dict[str, str] = {
        "Self": f"{table_self}i{cell.row}_{cell.col}",
        "Name": f"{cell.col}:{cell.row}",
        "RowSpan": str(cell.row_span),
        "ColumnSpan": str(cell.col_span),
        "AppliedCellStyle": f"CellStyle/{cell.cell_style}",
    }
    if cell.fill_color:
        cell_attrs["FillColor"] = f"Color/gt-{cell.fill_color}"
        cell_attrs["AppliedCellStylePriority"] = "1"
    inner = _serialize_cell_content(cell)
    return "<Cell " + _attr_str(cell_attrs) + ">" + inner + "</Cell>"


def _serialize_cell_content(cell: _Cell) -> str:
    """Render the ``<ParagraphStyleRange>`` payload inside a cell."""
    if cell.merged_into:
        # Placeholder cell absorbed by a span-anchor elsewhere — keep empty.
        return ""
    para_attrs = {"AppliedParagraphStyle": f"ParagraphStyle/{cell.paragraph_style}"}
    runs_xml = _serialize_runs(cell.runs or [_Run(text="")])
    return "<ParagraphStyleRange " + _attr_str(para_attrs) + ">" + runs_xml + "</ParagraphStyleRange>"


def _serialize_runs(runs: list[_Run]) -> str:
    """Serialize a list of runs to CharacterStyleRange elements."""
    # Each run becomes its own CharacterStyleRange so inline overrides
    # (bold, italic, color) stay local — matching InDesign's writer.
    chunks: list[str] = []
    for run in runs:
        attrs: dict[str, str] = {
            "AppliedCharacterStyle": "CharacterStyle/Default",
            "PointSize": _CELL_POINT_SIZE,
        }
        if run.bold and run.italic:
            attrs["FontStyle"] = "Bold Italic"
        elif run.bold:
            attrs["FontStyle"] = "Bold"
        elif run.italic:
            attrs["FontStyle"] = "Italic"
        if run.color:
            hexcolor = _normalize_hex(run.color.lstrip("#"))
            attrs["FillColor"] = f"Color/gt-{hexcolor}"
        body = ""
        if run.break_before:
            body += "<Br/>"
        if run.text:
            body += "<Content>" + _escape_xml(run.text) + "</Content>"
        if not body:
            body = "<Content></Content>"
        chunks.append("<CharacterStyleRange " + _attr_str(attrs) + ">" + body + "</CharacterStyleRange>")
    return "".join(chunks)


def _wrap_caption(text: str) -> str:
    """Wrap plain text in a ``ParagraphStyle/Caption`` paragraph."""
    esc = _escape_xml(text)
    return (
        '<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/Caption">'
        '<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/Default">'
        f"<Content>{esc}</Content>"
        "</CharacterStyleRange>"
        "</ParagraphStyleRange>"
    )


def _format_caption(title: str | None, subtitle: str | None) -> str:
    """Combine title + subtitle into a single caption string."""
    parts = []
    if title:
        parts.append(title)
    if subtitle:
        parts.append(subtitle)
    return " — ".join(parts) if parts else ""


def _gen_self_id() -> str:
    """Generate a random ICML Self ID (``u`` prefix, 8 hex chars)."""
    return "u" + secrets.token_hex(4)


def _attr_str(attrs: dict[str, str]) -> str:
    """Serialize an attribute dict with XML-escaped values, stable order."""
    parts = []
    for k, v in attrs.items():
        parts.append(f'{k}="{_escape_attr(v)}"')
    return " ".join(parts)


_ATTR_ESCAPES = {
    "&": "&amp;",
    '"': "&quot;",
    "<": "&lt;",
    ">": "&gt;",
}


def _escape_attr(text: str) -> str:
    return "".join(_ATTR_ESCAPES.get(c, c) for c in text)


def _escape_xml(text: str) -> str:
    """Escape ``&``, ``<``, ``>`` for element ``<Content>`` bodies."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _fmt_float(n: float) -> str:
    """Format a float for ICML attributes: 1 decimal place, no trailing zero."""
    s = f"{n:.2f}".rstrip("0").rstrip(".")
    return s or "0"
