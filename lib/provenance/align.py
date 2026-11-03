"""Locate each rendered qmd value in the PDF's token streams."""

from __future__ import annotations

import difflib
from dataclasses import dataclass

from rapidfuzz import fuzz

from lib.provenance.pdf_index import PdfIndex, PdfToken
from lib.provenance.qmd import QmdDoc, QToken
from lib.provenance.text import norm_tok

CONTEXT = 6  # qmd tokens on each side compared when a value has to be searched for
MIN_CONTEXT_OVERLAP = 2


@dataclass
class Occurrence:
    expr_id: int
    tokens: list[PdfToken]
    stream: list[PdfToken]
    start: int
    end: int
    confidence: str  # exact | anchored | fallback | low | missing


def _search_value(qn: list[str], s: int, e: int, pn: list[str], estimate: int | None) -> int | None:
    """Find the value's tokens verbatim in the PDF, preferring matching neighbors, then proximity.

    Rescues values whose surrounding text was reworded after rendering, which throws the
    sequence alignment off even though the number itself is printed unchanged.
    """
    value, n = qn[s:e], e - s
    if not value or not any(value):
        return None
    q_ctx = {t for t in qn[max(0, s - CONTEXT) : s] + qn[e : e + CONTEXT] if t}
    best: tuple[int, int, int] | None = None
    for j in range(len(pn) - n + 1):
        if pn[j : j + n] != value:
            continue
        p_ctx = set(pn[max(0, j - CONTEXT - 2) : j] + pn[j + n : j + n + CONTEXT + 2])
        overlap = len(q_ctx & p_ctx)
        dist = abs(j - estimate) if estimate is not None else 0
        if best is None or (overlap, -dist) > (best[0], -best[1]):
            best = (overlap, dist, j)
    if best is None or best[0] < MIN_CONTEXT_OVERLAP:
        return None
    return best[2]


def align_stream(q_tokens: list[QToken], p_tokens: list[PdfToken]) -> list[Occurrence]:
    qn = [norm_tok(t.text) for t in q_tokens]
    pn = [norm_tok(t.text) for t in p_tokens]
    sm = difflib.SequenceMatcher(None, qn, pn, autojunk=False)
    q2p: list[int | None] = [None] * len(qn)
    exact = [False] * len(qn)
    block_of: list[tuple[int, int, int, int] | None] = [None] * len(qn)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                q2p[i1 + k] = j1 + k
                exact[i1 + k] = True
        elif tag == "replace":
            for k in range(i2 - i1):
                q2p[i1 + k] = j1 + min(int(k * (j2 - j1) / (i2 - i1)), j2 - j1 - 1)
                block_of[i1 + k] = (i1, i2, j1, j2)

    out: list[Occurrence] = []
    i = 0
    while i < len(q_tokens):
        eid = q_tokens[i].expr_id
        if eid is None:
            i += 1
            continue
        s = i
        while i < len(q_tokens) and q_tokens[i].expr_id == eid:
            i += 1
        e = i
        mapped = [q2p[k] for k in range(s, e) if q2p[k] is not None]
        before_ok = s == 0 or exact[s - 1]
        after_ok = e >= len(qn) or exact[e]
        if all(exact[s:e]):
            js, je, conf = q2p[s], q2p[e - 1], "exact"
        elif mapped and before_ok and after_ok:
            blk = block_of[s]
            if blk and blk[0] == s and blk[1] == e:
                js, je = blk[2], blk[3] - 1
            else:
                js, je = min(mapped), max(mapped)
            conf = "anchored"
        else:
            estimate = min(mapped) if mapped else next((q2p[k] for k in range(s, -1, -1) if q2p[k] is not None), None)
            found = _search_value(qn, s, e, pn, estimate)
            if found is not None:
                js, je, conf = found, found + (e - s) - 1, "fallback"
            elif mapped:
                js, je, conf = min(mapped), max(mapped), "low"
            else:
                out.append(Occurrence(eid, [], p_tokens, -1, -1, "missing"))
                continue
        assert js is not None and je is not None
        out.append(Occurrence(eid, p_tokens[js : je + 1], p_tokens, js, je + 1, conf))
    return out


def match_footnotes(doc: QmdDoc, idx: PdfIndex) -> dict[str, list[tuple[int, float]]]:
    """Map each qmd footnote label to the PDF footnote number(s) carrying its text."""
    p_text = {n: " ".join(norm_tok(t.text) for t in toks) for n, toks in idx.footnotes.items()}
    out: dict[str, list[tuple[int, float]]] = {}
    for label, toks in doc.footnotes.items():
        q = " ".join(norm_tok(t.text) for t in toks)
        scores = sorted(((fuzz.ratio(q, p), n) for n, p in p_text.items()), reverse=True)
        best = scores[0][0]
        out[label] = [(n, s) for s, n in scores if s >= max(85.0, best - 2.0)] or [(scores[0][1], best)]
    return out
