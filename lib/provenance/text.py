"""Token helpers shared by the PDF index, the qmd parser and the aligner."""

from __future__ import annotations

import re
from typing import Any

SUBTOKEN_RE = re.compile(r"\$?[-\u2212]?\d[\d,]*(?:\.\d+)?%?|[A-Za-z][\w'\u2019]*|\S")


def norm_tok(t: str) -> str:
    t = t.lower().replace("\u2019", "'").replace("\u2018", "'").replace("“", '"').replace("”", '"')
    t = t.replace("\u2212", "-").replace("\u2013", "-")
    return t.strip(".,;:()[]\"'!?*")


def split_word(word: str) -> list[tuple[str, bool]]:
    """Split a whitespace word into number/word pieces, flagging which follow a space.

    Punctuation-only pieces stay glued to a neighbor so quotes keep their punctuation.
    """
    pieces: list[list[Any]] = []
    pending = ""
    for k, p in enumerate(SUBTOKEN_RE.findall(word)):
        if norm_tok(p):
            pieces.append([pending + p, k == 0 or (bool(pending) and len(pieces) == 0)])
            pending = ""
        elif pieces:
            pieces[-1][0] += p
        else:
            pending += p
    if pending:
        pieces.append([pending, True])
    if pieces:
        pieces[0][1] = True
    return [(p, s) for p, s in pieces]


def norm_words(s: str) -> list[str]:
    """``s`` split and normalized the way PDF and qmd tokens are, for comparing runs of words."""
    return [norm_tok(p) for w in s.split() for p, _ in split_word(w)]


def find_runs(hay: list[str], needle: list[str]) -> list[int]:
    """Start positions of every occurrence of ``needle`` as a contiguous run in ``hay``."""
    n = len(needle)
    if n == 0:
        return []
    return [j for j in range(len(hay) - n + 1) if hay[j : j + n] == needle]


def join_tokens(tokens: list[Any]) -> str:
    return "".join((" " if t.space and k else "") + t.text for k, t in enumerate(tokens))


def md_escape(s: str) -> str:
    return re.sub(r"([\\*_$\[\]<>|#`])", r"\\\1", s)
