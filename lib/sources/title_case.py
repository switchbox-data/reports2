"""Title case for titles typed in ALL CAPS.

A title counts as all caps when every word of two or more letters is upper case, apart from
small words ("and", "of") and "d/b/a"; a run of three or more words in capitals inside a mixed
title ("NIAGARA MOHAWK POWER CORPORATION Direct Testimony") is rewritten too. It is rewritten in Chicago title case, keeping what must stay as is:

- organization names the library already spells in mixed case ("KeySpan Gas East Corporation"),
  matched case-insensitively, longest first;
- known acronyms and short forms (NY, PURA, LIHEAP) and codes without vowels or with digits
  (RSH, RMDS, R-3);
- "d/b/a" in lower case.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

# Chicago: articles, coordinating conjunctions and prepositions are lower case unless first or last.
SMALL_WORDS = frozenset(
    [
        "a",
        "an",
        "the",
        "and",
        "but",
        "or",
        "nor",
        "for",
        "so",
        "yet",
        "as",
        "at",
        "by",
        "in",
        "of",
        "off",
        "on",
        "per",
        "to",
        "up",
        "via",
        "into",
        "onto",
        "from",
        "with",
        "over",
        "upon",
        "than",
    ]
)
# Common acronyms in our sources; ``library_acronyms`` adds the ones the library itself uses.
ACRONYMS = frozenset(
    [
        "GAAP",
        "FERC",
        "NERC",
        "EIA",
        "EPA",
        "DOE",
        "HUD",
        "IRS",
        "SEC",
        "LIHEAP",
        "HEAP",
        "LMI",
        "AMI",
        "SMI",
        "FPL",
        "HVAC",
        "EV",
        "EVSE",
        "PV",
        "DER",
        "DERMS",
        "MCOS",
        "ECOS",
        "TOU",
        "IRP",
        "LTP",
        "LTGIP",
        "CLCPA",
        "AEBA",
        "NENY",
        "GHG",
        "CO2",
        "ESG",
        "CEO",
        "CFO",
        "ISO",
        "RTO",
        "NYISO",
        "PJM",
        "MISO",
        "ERCOT",
        "CAISO",
        "LDC",
        "NPA",
        "NPAS",
        "NWA",
        "UTEN",
        "GSHP",
        "ASHP",
        "CCASHP",
        "AMR",
        "AMS",
        "FAQ",
        "USA",
        "LLC",
        "LLP",
        "PLC",
        "DBA",
        "RFP",
        "RFI",
        "ACS",
        "PUMS",
        "FY",
        "YTD",
    ]
)
# Names spelled in mixed case that the library may only hold in capitals or plain title case.
SPELLINGS = ("KeySpan",)
STATE_CODES = frozenset(
    [
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "DC",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
        "US",
        "USA",
    ]
)
_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\u2019]*")
_LETTERS_RE = re.compile(r"[A-Za-z]{2,}")


def _is_caps(word: str) -> bool:
    letters = re.sub(r"[^A-Za-z]", "", word)
    return len(letters) >= 2 and letters.isupper()


def library_acronyms(titles: Iterable[str]) -> set[str]:
    """Standalone words in capitals inside titles that are mostly in lower case (a run of
    capitalized words is a name or a shouted phrase, not an acronym)."""
    found: set[str] = set()
    for t in titles:
        words = t.split()
        if not words or sum(_is_caps(w) for w in words) / len(words) >= 0.5:
            continue
        for i, w in enumerate(words):
            neighbors = words[max(i - 1, 0) : i] + words[i + 1 : i + 2]
            core = re.sub(r"^[^A-Za-z0-9]+|[^A-Za-z0-9]+$", "", w)
            if _is_caps(core) and not any(_is_caps(n) for n in neighbors) and core.lower() not in SMALL_WORDS:
                found.add(core)
    return found


def is_all_caps(title: str) -> bool:
    words = [w for w in _LETTERS_RE.findall(title.replace("d/b/a", "")) if w.lower() not in SMALL_WORDS or w.isupper()]
    spaced = [t for t in title.split() if re.search(r"[A-Za-z]{2,}", t)]
    return len(spaced) >= 2 and all(w.isupper() for w in words)


def _is_code(word: str, acronyms: frozenset[str]) -> bool:
    if word.upper() in acronyms:
        return True
    letters = re.sub(r"[^A-Za-z]", "", word)
    return bool(letters) and (not re.search(r"[AEIOUYaeiouy]", letters) or bool(re.search(r"\d", word)))


def _case_word(word: str, first: bool, last: bool, acronyms: frozenset[str]) -> str:
    if word.lower() == "d/b/a":
        return "d/b/a"
    if _is_code(word, acronyms):
        return word.upper()
    parts = word.split("-")
    out = []
    for i, part in enumerate(parts):
        low = part.lower()
        if (0 < i < len(parts) - 1 and low in SMALL_WORDS) or (
            not first and not last and len(parts) == 1 and low in SMALL_WORDS
        ):
            out.append(low)
        else:
            out.append(_WORD_RE.sub(lambda m: m.group(0)[:1].upper() + m.group(0)[1:].lower(), part, count=1))
    return "-".join(out)


MIN_CAPS_RUN = 3


def uncap_title(title: str, names: Iterable[str] = (), acronyms: Iterable[str] = ()) -> str | None:
    """``title`` in title case if it is in ALL CAPS, or with any run of three or more words in
    capitals rewritten; ``None`` if nothing changes."""
    acr = frozenset(a.upper() for a in acronyms) | STATE_CODES | ACRONYMS
    tokens = re.split(r"(\s+)", title.strip())
    words = [i for i, t in enumerate(tokens) if t.strip()]
    shouted = [_is_caps(tokens[i]) or tokens[i].lower() == "d/b/a" for i in words]
    if is_all_caps(title):
        selected = [True] * len(words)
    else:
        selected = [False] * len(words)
        n = 0
        while n < len(words):
            m = n
            while m < len(words) and shouted[m]:
                m += 1
            real = sum(not _is_code(tokens[words[k]], acr) for k in range(n, m))
            if real >= MIN_CAPS_RUN:
                selected[n:m] = [True] * (m - n)
            n = max(m, n + 1)
    if not any(selected):
        return None
    for n, i in enumerate(words):
        if not selected[n]:
            continue
        lead, core, trail = re.match(r"^([^A-Za-z0-9]*)(.*?)([^A-Za-z0-9/]*)$", tokens[i]).groups()  # type: ignore[union-attr]
        if core:
            after_colon = n > 0 and tokens[words[n - 1]].endswith(":")
            core = _case_word(core, n == 0 or after_colon, n == len(words) - 1, acr)
        tokens[i] = lead + core + trail
    out = "".join(tokens)
    spellings: set[str] = {n for n in [*names, *SPELLINGS] if n and not n.isupper()}
    for name in sorted(spellings, key=lambda n: (-len(n), n)):
        out = re.sub(rf"(?<![A-Za-z]){re.escape(name)}(?![A-Za-z])", name, out, flags=re.IGNORECASE)
    return out if out != title.strip() else None
