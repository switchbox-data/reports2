"""Turn aligned PDF occurrences into the document's Figure, Table and Number rows."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field

from rapidfuzz import fuzz

from lib.provenance.align import Occurrence, align_stream, match_footnotes
from lib.provenance.config import Link, ProvenanceConfig
from lib.provenance.pdf_index import PdfIndex, PdfToken
from lib.provenance.qmd import QmdDoc, clean_markdown
from lib.provenance.resolve import Notebook, cell_for_line, fig_caption, find_label_line, load_notebook, resolve_expr
from lib.provenance.text import join_tokens, md_escape, norm_tok, split_word

TABLE_HEADER_MIN_SCORE = 80
TABLE_HEADER_MAX_LINES = 3
MATH_GLYPH_RE = re.compile("[\U0001d400-\U0001d7ff]")
"""Equations extract as Mathematical Alphanumeric Symbols; a quote stops at them."""


@dataclass
class Row:
    type: str
    locations: list[tuple[int, int, str]]  # (page, sort_key, label)
    what: str  # markdown
    what_plain: str
    link: Link | None
    occurrences: list[Occurrence] = field(default_factory=list)


def format_locations(locs: list[tuple[int, int, str]]) -> str:
    by_page: dict[int, dict[str, list[int]]] = defaultdict(lambda: {"line": [], "footnote": [], "page": []})
    order: list[int] = []
    for page, key, kind in sorted(set(locs)):
        if page not in by_page:
            order.append(page)
        by_page[page][kind].append(key)

    def join(items: list[int]) -> str:
        items = sorted(set(items))
        if len(items) == 1:
            return str(items[0])
        if len(items) == 2:
            return f"{items[0]} and {items[1]}"
        return ", ".join(map(str, items[:-1])) + f", and {items[-1]}"

    parts = []
    for page in order:
        d = by_page[page]
        sub = []
        if d["line"]:
            sub.append(("line " if len(set(d["line"])) == 1 else "lines ") + join(d["line"]))
        if d["footnote"]:
            sub.append(("footnote " if len(set(d["footnote"])) == 1 else "footnotes ") + join(d["footnote"]))
        parts.append(f"p. {page}" + (", " + " and ".join(sub) if sub else ""))
    return "; ".join(parts)


ABBREVIATIONS = {"no.", "vs.", "e.g.", "i.e.", "etc.", "st.", "dr.", "mr.", "ms.", "approx.", "u.s.", "fig.", "p."}


def _ends_sentence(tok: PdfToken) -> bool:
    t = tok.text
    if t in {"•", "Q.", "A."}:
        return True
    return bool(re.search(r"[.?!:]”?$", t)) and t.lower() not in ABBREVIATIONS


def quote_for(occ: Occurrence) -> tuple[str, str]:
    stream, s, e = occ.stream, occ.start, occ.end
    lo = max(0, s - 12)
    while 0 < lo < s and not stream[lo].space:
        lo += 1
    before = stream[lo:s]
    lead = "" if lo == 0 else "…"
    for k in range(len(before) - 1, -1, -1):
        if _ends_sentence(before[k]):
            before, lead = before[k + 1 :], ""
            break
    hi = min(len(stream), e + 10)
    while e < hi < len(stream) and not stream[hi].space:
        hi -= 1
    after = stream[e:hi]
    trail = "" if e + len(after) >= len(stream) else "…"
    if _ends_sentence(occ.tokens[-1]):
        after, trail = [], ""
    for k, t in enumerate(after):
        if t.text in {"•", "Q.", "A."}:
            after, trail = after[:k], ""
            break
        if _ends_sentence(t):
            after, trail = after[: k + 1], ""
            break
    for k in range(len(before) - 1, -1, -1):
        if MATH_GLYPH_RE.search(before[k].text):
            before, lead = before[k + 1 :], ""
            break
    for k, t in enumerate(after):
        if MATH_GLYPH_RE.search(t.text):
            after, trail = after[:k], "…"
            break
    b, v, a = join_tokens(before), join_tokens(occ.tokens), join_tokens(after)
    m = re.match(r"^([(\[“\"]*)(.*?)([).,;:”\"\](\[“]*)$", v)
    assert m
    vpre, vcore, vpost = m.groups()
    sp1 = " " if before and occ.tokens[0].space else ""
    sp2 = " " if after and after[0].space else ""
    md = (
        f"{lead}{md_escape(b)}{sp1}{md_escape(vpre)}**{md_escape(vcore)}**{md_escape(vpost)}{sp2}{md_escape(a)}{trail}"
    ).strip()
    plain = f"{lead}{b}{sp1}{vpre}[{vcore}]{vpost}{sp2}{a}{trail}".strip()
    return md, plain


def location_of(occ: Occurrence) -> tuple[int, int, str]:
    t = occ.tokens[0]
    if t.footnote is not None:
        return (t.page, t.footnote, "footnote")
    assert t.line is not None
    return (t.page, t.line, "line")


def _split_norm(s: str) -> list[str]:
    return [norm_tok(p) for w in s.split() for p, _ in split_word(w)]


def _known_difference(cfg: ProvenanceConfig, pdf_value: str, cache_value: str) -> str | None:
    for kd in cfg.known_differences:
        if norm_tok(pdf_value) == norm_tok(kd.pdf_value) and norm_tok(cache_value) == norm_tok(kd.cache_value):
            return kd.explanation
    return None


def _rescue_known_difference(cfg: ProvenanceConfig, occ: Occurrence, cache_value: str) -> Occurrence | None:
    """Pin a weak alignment to the filed value of a known difference, if it sits in the matched span.

    A number edited after rendering often comes with edited words around it, which leaves the
    alignment unsure of the exact tokens even though it lands in the right place.
    """
    if not occ.tokens:
        return None
    for kd in cfg.known_differences:
        if norm_tok(cache_value) != norm_tok(kd.cache_value):
            continue
        val = _split_norm(kd.pdf_value)
        lo, hi = max(0, occ.start - len(val)), min(len(occ.stream), occ.end + len(val))
        sn = [norm_tok(t.text) for t in occ.stream]
        for j in range(lo, hi - len(val) + 1):
            if sn[j : j + len(val)] == val:
                return Occurrence(occ.expr_id, occ.stream[j : j + len(val)], occ.stream, j, j + len(val), "exact")
    return None


def _number_rows(
    cfg: ProvenanceConfig,
    doc: QmdDoc,
    idx: PdfIndex,
    notebooks: dict[str, Notebook],
    testimony: Notebook,
    review: list[dict[str, str]],
    baseline_text: str | None,
) -> list[Row]:
    rows: list[Row] = []
    occs = align_stream(doc.body, idx.body)
    fn_map = match_footnotes(doc, idx)
    for label, matches in fn_map.items():
        if not any(t.expr_id is not None for t in doc.footnotes[label]):
            continue
        if matches[0][1] < 80:
            review.append({"check": "footnote_match", "item": label, "detail": f"best score {matches[0][1]:.0f}"})
        for n, _ in matches:
            occs.extend(align_stream(doc.footnotes[label], idx.footnotes[n]))

    by_code: dict[str, list[Occurrence]] = defaultdict(list)
    for occ in occs:
        if occ.confidence == "low":
            occ = _rescue_known_difference(cfg, occ, doc.exprs[occ.expr_id].value) or occ
        by_code[doc.exprs[occ.expr_id].code].append(occ)
    for code, group in by_code.items():
        found = [o for o in group if o.tokens]
        for o in group:
            expr = doc.exprs[o.expr_id]
            if o.confidence in ("missing", "low"):
                review.append(
                    {
                        "check": f"match_{o.confidence}",
                        "item": code,
                        "detail": f"qmd line {expr.qmd_line}; value {expr.value!r}"
                        + (f"; pdf {join_tokens(o.tokens)!r}" if o.tokens else ""),
                    }
                )
                continue
            pdf_value = join_tokens(o.tokens)
            if o.confidence == "fallback":
                review.append(
                    {
                        "check": "match_fallback",
                        "item": code,
                        "detail": f"{format_locations([location_of(o)])}: found {pdf_value!r} by value search "
                        f"(qmd line {expr.qmd_line}); confirm it is the right occurrence",
                    }
                )
            if norm_tok(pdf_value) != norm_tok(clean_markdown(expr.value)):
                explanation = _known_difference(cfg, pdf_value, expr.value)
                detail = f"{format_locations([location_of(o)])}: pdf {pdf_value!r} vs cache {expr.value!r}"
                if explanation:
                    review.append({"check": "known_difference", "item": code, "detail": f"{detail}; {explanation}"})
                else:
                    if baseline_text is not None:
                        in_baseline = clean_markdown(expr.value) in baseline_text
                        detail += (
                            "; pre-filing render has the cache value"
                            if in_baseline
                            else ("; pre-filing render lacks the cache value")
                        )
                    review.append({"check": "pdf_vs_cache", "item": code, "detail": detail})
        if not found:
            continue
        res = resolve_expr(cfg, code, notebooks, testimony)
        if res.link is None:
            review.append({"check": "unresolved", "item": code, "detail": res.why})
        if res.other_cells:
            review.append(
                {
                    "check": "multi_cell",
                    "item": code,
                    "detail": f"linked to {res.link.text if res.link else '?'}; also uses "
                    + "; ".join(res.other_cells),
                }
            )
        first = min(found, key=lambda o: location_of(o)[:2])
        md, plain = quote_for(first)
        rows.append(Row("Number", [location_of(o) for o in found], md, plain, res.link, found))
    return rows


def _hardcoded_rows(cfg: ProvenanceConfig, idx: PdfIndex, review: list[dict[str, str]]) -> list[Row]:
    rows: list[Row] = []
    streams = [idx.body, *idx.footnotes.values()]
    for hc in cfg.hardcoded:
        ctx, val = _split_norm(hc.context), _split_norm(hc.value)
        offset = next((k for k in range(len(ctx) - len(val) + 1) if ctx[k : k + len(val)] == val), None)
        if offset is None:
            raise ValueError(f"hardcoded context {hc.context!r} does not contain {hc.value!r}")
        found: list[Occurrence] = []
        for stream in streams:
            sn = [norm_tok(t.text) for t in stream]
            for j in range(len(sn) - len(ctx) + 1):
                if sn[j : j + len(ctx)] == ctx:
                    s = j + offset
                    found.append(Occurrence(-1, stream[s : s + len(val)], stream, s, s + len(val), "exact"))
        if not found:
            review.append({"check": "hardcoded_missing", "item": hc.value, "detail": f"context {hc.context!r}"})
            continue
        if hc.review_note:
            review.append(
                {
                    "check": "hardcoded_note",
                    "item": hc.value,
                    "detail": f"{format_locations([location_of(found[0])])}: {hc.review_note}",
                }
            )
        first = min(found, key=lambda o: location_of(o)[:2])
        md, plain = quote_for(first)
        rows.append(Row("Number", [location_of(o) for o in found], md, plain, hc.link, found))
    return rows


def _figure_rows(
    cfg: ProvenanceConfig, doc: QmdDoc, idx: PdfIndex, notebooks: dict[str, Notebook], review: list[dict[str, str]]
) -> list[Row]:
    rows: list[Row] = []
    fig_caps = sorted((c for c in idx.captions if c["type"] == "Figure"), key=lambda c: c["number"])
    if len(fig_caps) != len(doc.embeds):
        review.append(
            {"check": "figure_count", "item": "", "detail": f"{len(doc.embeds)} embeds vs {len(fig_caps)} PDF figures"}
        )
    fig_rows: dict[str, Row] = {}
    for emb, cap in zip(doc.embeds, fig_caps, strict=False):
        nb = notebooks.get(emb["notebook"])
        if nb is None:
            nb = notebooks[emb["notebook"]] = load_notebook(cfg, emb["notebook"])
        label_line = find_label_line(nb, emb["label"])
        link = None
        if label_line is None:
            review.append({"check": "unresolved", "item": emb["label"], "detail": f"label not in {nb.name}.qmd"})
        else:
            link = cfg.notebook_link(nb.name, *cell_for_line(nb, label_line))
            nb_cap = clean_markdown(fig_caption(nb, label_line))
            score = fuzz.partial_ratio(norm_tok(nb_cap.lower()), norm_tok(cap["text"].lower()))
            if score < 80:
                review.append(
                    {
                        "check": "caption_mismatch",
                        "item": f"Figure {cap['number']} ({emb['label']})",
                        "detail": f"score {score:.0f}: notebook {nb_cap!r} vs pdf {cap['text']!r}",
                    }
                )
        loc = (cap["page"], 0, "page")
        title = f"Figure {cap['number']}: {cap['text']}"
        if emb["label"] in fig_rows:
            row = fig_rows[emb["label"]]
            row.locations.append(loc)
            row.what += f" (also shown as Figure {cap['number']})"
            row.what_plain += f" (also shown as Figure {cap['number']})"
        else:
            fig_rows[emb["label"]] = row = Row("Figure", [loc], md_escape(title), title, link)
            rows.append(row)
    return rows


def _locate_table(header: list[str], idx: PdfIndex, start: int) -> tuple[int, int] | None:
    """Find the PDF lines (after ``start``) that best match a table's header row.

    Header cells often wrap onto two or three PDF lines, so windows of up to three lines are
    scored. Returns the page and the index of the window's last line.
    """
    target = " ".join(_split_norm(" ".join(header)))
    best: tuple[float, int, int] | None = None
    for k in range(start, len(idx.lines)):
        for w in range(1, TABLE_HEADER_MAX_LINES + 1):
            if k + w > len(idx.lines):
                break
            text = " ".join(_split_norm(" ".join(ln["text"] for ln in idx.lines[k : k + w])))
            score = fuzz.token_sort_ratio(target, text)
            if score >= TABLE_HEADER_MIN_SCORE and (best is None or score > best[0]):
                best = (score, k, k + w - 1)
    if best is None:
        return None
    return idx.lines[best[1]]["page"], best[2]


def _table_rows(cfg: ProvenanceConfig, doc: QmdDoc, idx: PdfIndex, review: list[dict[str, str]]) -> list[Row]:
    rows: list[Row] = []
    testimony = cfg.testimony_key
    tbl_caps = sorted((c for c in idx.captions if c["type"] == "Table"), key=lambda c: c["number"])
    if tbl_caps:
        if len(tbl_caps) != len(doc.tables):
            review.append(
                {"check": "table_count", "item": "", "detail": f"{len(doc.tables)} qmd tables vs {len(tbl_caps)} PDF"}
            )
        for tbl, cap in zip(doc.tables, tbl_caps, strict=False):
            title = f"Table {cap['number']}: {cap['text']}"
            link = cfg.notebook_link(testimony, tbl["qmd_line"], tbl["end_line"])
            rows.append(Row("Table", [(cap["page"], 0, "page")], md_escape(title), title, link))
        return rows
    # Uncaptioned tables: number them in order and find each by its header row.
    pos = -1
    for k, tbl in enumerate(doc.tables, 1):
        hit = _locate_table(tbl["header"], idx, pos + 1)
        title = f"Table {k}: " + " / ".join(tbl["header"])
        if hit is None:
            review.append({"check": "table_not_found", "item": title, "detail": f"qmd line {tbl['qmd_line']}"})
            continue
        page, pos = hit
        review.append(
            {"check": "table_title", "item": title, "detail": f"uncaptioned table on p. {page}; review the wording"}
        )
        link = cfg.notebook_link(testimony, tbl["qmd_line"], tbl["end_line"])
        rows.append(Row("Table", [(page, 0, "page")], md_escape(title), title, link))
    return rows


def build_rows(
    cfg: ProvenanceConfig,
    doc: QmdDoc,
    idx: PdfIndex,
    review: list[dict[str, str]],
    baseline_text: str | None = None,
) -> list[Row]:
    notebooks = {name: load_notebook(cfg, name) for name in cfg.namespaces.values()}
    testimony = load_notebook(cfg, cfg.testimony_key)
    rows = _number_rows(cfg, doc, idx, notebooks, testimony, review, baseline_text)
    rows += _hardcoded_rows(cfg, idx, review)
    rows += _figure_rows(cfg, doc, idx, notebooks, review)
    rows += _table_rows(cfg, doc, idx, review)
    kind_order = {"page": 0, "line": 1, "footnote": 2}
    rows.sort(key=lambda r: min((p, kind_order[k], s) for p, s, k in r.locations))
    return rows
