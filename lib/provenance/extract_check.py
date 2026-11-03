"""Cross-check each number's page and line against the filed PDF's validated source extract.

The extract's ``[PDF p. N | printed p. M]`` markers and ``{n}`` line prefixes were checked against the PDF
when it was ingested (``just sources-check-pages``), so ``lib.sources.pagelines.cite`` gives an independent
answer to "where is this passage?". A disagreement points at a bad alignment or a mis-read line number.
"""

from __future__ import annotations

import re
from pathlib import Path

from lib.provenance.align import Occurrence
from lib.provenance.rows import Row, format_locations, location_of
from lib.provenance.text import join_tokens
from lib.sources.pagelines import Citation, cite

CONTEXT_WINDOWS = ((5, 5), (3, 3), (5, 0), (0, 5), (1, 1))
"""(words before, words after) the value to search the extract for, widest first; one-sided windows
cover a value next to a figure or table, whose description the extract places in between."""


def _covers(c: Citation, page: int, key: int, kind: str) -> bool:
    s, e = c.start, c.end
    if kind == "footnote":
        return (
            c.footnote is not None and re.sub(r"\D", "", c.footnote) == str(key) and str(page) in {s.printed, e.printed}
        )
    if c.footnote is not None or s.line is None or e.line is None:
        return False
    if s.printed == e.printed:
        return s.printed == str(page) and s.line <= key <= e.line
    return (s.printed == str(page) and key >= s.line) or (e.printed == str(page) and key <= e.line)


def _citations(md_text: str, occ: Occurrence) -> tuple[str, list[Citation]]:
    quote = ""
    for before, after in CONTEXT_WINDOWS:
        quote = join_tokens(occ.stream[max(0, occ.start - before) : occ.end + after])
        hits = cite(md_text, quote)
        if hits:
            return quote, hits
    return quote, []


def check_against_extract(rows: list[Row], path_extract: Path, review: list[dict[str, str]]) -> None:
    md_text = path_extract.read_text()
    checked = agree = 0
    for row in rows:
        for occ in row.occurrences:
            page, key, kind = location_of(occ)
            where = format_locations([(page, key, kind)])
            quote, hits = _citations(md_text, occ)
            checked += 1
            if not hits:
                review.append({"check": "extract_not_found", "item": row.what_plain, "detail": f"{where}: {quote!r}"})
            elif any(_covers(c, page, key, kind) for c in hits):
                agree += 1
            else:
                review.append(
                    {
                        "check": "extract_location",
                        "item": row.what_plain,
                        "detail": f"{where} here; extract has {quote!r} at " + "; ".join(str(c) for c in hits),
                    }
                )
    review.append(
        {
            "check": "extract_checked",
            "item": str(checked),
            "detail": f"number locations; {agree} agree with {path_extract.name}",
        }
    )
