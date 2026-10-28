"""Titles of utility-commission proceeding documents: ``Docket <number>: <title>``.

The number is the commission's own, without "Case", "D.P.U." or "No." (``Docket 24-E-0165``,
``Docket 25-08``, ``Docket 26-05-10``, ``Docket 4770``). A document filed in several dockets
uses the first one. ``docket_title`` moves a docket reference found anywhere in a title (or in
the item's number fields) to the front, and leaves titles without one alone.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

# A docket number: NY "22-E-0317", MA "25-55", CT "26-05-10", RI "4770" / "25-45-GE",
# IL "25-0084", MN "CI-23-117", ME "2022-00152".
_NUM = r"(?:[A-Z]{1,3}-)?\d{1,5}(?:-(?:[A-Z]{1,3}|\d{1,5}))*"
# "Rate Case 25-E-0072" keeps "Case": there it is part of the title, not the docket label.
_INTRO = r"(?i:Dockets?|(?<!Rate )Cases?|D\.\s?P\.\s?U\.|DPU)(?:\s+(?i:Nos?)\.?)?"
_REF = re.compile(rf"\b{_INTRO}\s*:?\s*(?P<num>{_NUM})\b")
# NY case numbers are distinctive enough to recognize without "Case".
_NY_NUM = re.compile(r"\b(?P<num>\d{2}-[A-Z]-\d{4,5})\b")
# A list of further numbers after the first ("…, 22-G-0318, 22-E-0319 and 22-G-0320").
_MORE = rf"(?:\s*(?:,|;|&|and|,\s*and)\s*(?:{_INTRO}\s*)?{_NUM})*"
_LIST = re.compile(rf"(?:\b{_INTRO}\s*:?\s*)?{_NUM}{_MORE}")
_CONFORMING = re.compile(rf"^Docket {_NUM}: \S")

NUMBER_FIELDS = ("docketNumber", "reportNumber", "number", "billNumber")


def _docket(text: str) -> re.Match[str] | None:
    return _REF.search(text) or _NY_NUM.search(text)


def _strip_reference(title: str, m: re.Match[str]) -> str:
    """``title`` without the docket list that starts at ``m``, tidied."""
    lst = _LIST.match(title, m.start())
    end = lst.end() if lst else m.end()
    before, after = title[: m.start()], title[end:]
    # "(Case 23-G-0627)" or "(Exh LU-NWA-1, D.P.U. 25-08)": drop the reference inside the parentheses.
    before = re.sub(r"(?:,\s*|\s+)(?:for|on|in|of)\s*$", "", before)
    before = re.sub(r",\s*$", "", before)
    out = before + after
    out = re.sub(r"\(\s*[,;]?\s*\)", "", out)
    out = re.sub(r"\(\s*[,;]\s*", "(", out)
    out = re.sub(r"\s*[,;]\s*\)", ")", out)
    out = re.sub(r"\s{2,}", " ", out).strip()
    out = re.sub(r"^(?:[-\u2013\u2014:,]\s*)+", "", out)
    out = re.sub(r"(?:\s*[-\u2013\u2014:,])+$", "", out)
    out = re.sub(r"\s+:", ":", out)
    return out.strip()


def docket_title(title: str, data: Mapping[str, Any] | None = None) -> str | None:
    """The title in ``Docket <number>: …`` form, or ``None`` if it has no docket (or already conforms)."""
    title = title.strip()
    if not title or _CONFORMING.match(title):
        return None
    m = _docket(title)
    if m is not None:
        rest = _strip_reference(title, m)
        number = m.group("num")
    else:
        found = next((mm for f in NUMBER_FIELDS if (mm := _docket(str((data or {}).get(f) or "")))), None)
        if found is None:
            return None
        rest, number = title, found.group("num")
    # "(Gas IRP): Order …" right after the number becomes "Order … (Gas IRP)".
    if lead := re.match(r"^\(([^()]+)\):\s*(.+)$", rest):
        rest = f"{lead.group(2)} ({lead.group(1)})"
    rest = rest[:1].upper() + rest[1:]
    return f"Docket {number}: {rest}" if rest else None
