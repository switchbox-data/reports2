"""The canonical citation-key rule: ``{author}_{title}_{year}{suffix}``.

Single implementation shared by ``just sync-bib`` checks, the one-time library cleanup and
source ingest. Functions take a Zotero item's ``data`` dict (``creators``, ``title``,
``shortTitle``, ``date``, ``extra``, ``key``) and need no Zotero access.

- **Author part.** First creator (authors, then editors, then other types). An organization
  (single-field creator) uses the item's short form (``tex.shortauthor`` in Extra) if it has
  one, else its full name; a person uses the family name. The result is ASCII-folded,
  lowercased and reduced to ``a-z0-9`` ("MA DPU" -> ``madpu``, "O&R" -> ``or``,
  "Pérez-Arriaga" -> ``perezarriaga``).
- **Title part.** Better BibTeX's ``shorttitle(3,3)``: the first three non-stop words of the
  full title, each with its first character uppercased.
- **Year part.** The 4-digit year of the item's date, or ``nd`` when there is none.
- **Collisions.** Items sharing a base key are ordered by date, title and Zotero item key;
  the first takes the bare key, the next ``a``, ``b``, ... (as in Better BibTeX). Items whose
  current key already conforms keep it, suffix included.
"""

from __future__ import annotations

import re
import string
import unicodedata
from collections.abc import Iterable, Mapping
from itertools import count, product
from typing import Any

from lib.sources import extra as extra_mod

Item = Mapping[str, Any]

# Better BibTeX's skip words for title-based key parts.
_STOP_WORDS_TEXT = """
a ab aboard about above across after against al along amid among an and anti around as at before behind below
beneath beside besides between beyond but by d da das de del dell dello dei degli della delle dem den der des
despite die do down du during ein eine einem einen einer eines el en et except for from gli i il in inside
into is l la las le les like lo los near nor of off on onto or over past per plus round save since so some sur
than the through to toward towards un una unas under underneath une unlike uno unos until up upon versus via
von while with within without yet zu zum
"""
STOP_WORDS = frozenset(_STOP_WORDS_TEXT.split())

_NAME_SUFFIX_RE = re.compile(r",?\s+(jr\.?|sr\.?|ii|iii|iv|v)$", re.IGNORECASE)
_MULTI_SHORT_SPLIT_RE = re.compile(r",\s*(?:and\s+)?|\s+and\s+|\s+et al\.?$")
_KEY_RE = re.compile(r"^(?P<author>.*?)_(?P<title>.*)_(?P<year>\d{4}|nd)(?P<suffix>[a-z]{0,2})$")
_MONTHS = {
    m: i
    for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)
}


class NoCreatorError(ValueError):
    """Raised when an item has no creator to build the author part from."""


def ascii_fold(s: str) -> str:
    """Fold diacritics to ASCII ("Rábago" -> "Rabago"); other non-ASCII punctuation becomes a space."""
    s = s.replace("\u2019", "'")
    s = "".join(" " if ord(ch) > 127 and unicodedata.category(ch)[0] in "PZS" else ch for ch in s)
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def squash(s: str) -> str:
    """ASCII-fold, lowercase and keep only ``a-z0-9`` ("ISO-NE" -> "isone")."""
    return re.sub(r"[^a-z0-9]", "", ascii_fold(s).lower())


def _ordered_creators(creators: Iterable[Mapping[str, str]]) -> list[Mapping[str, str]]:
    creators = list(creators)
    rank = {"author": 0, "editor": 1}
    return sorted(creators, key=lambda c: rank.get(c.get("creatorType", "author"), 2))


def _is_org(creator: Mapping[str, str]) -> bool:
    return "name" in creator or "literal" in creator


def _person_part(creator: Mapping[str, str]) -> str:
    family = creator.get("lastName") or creator.get("family") or ""
    family = _NAME_SUFFIX_RE.sub("", family.strip())
    particle = creator.get("non-dropping-particle", "")
    return squash(f"{particle}{family}")


def author_part(creators: Iterable[Mapping[str, str]], short_form: str | None = None) -> str:
    """Author part from Zotero creators (``name`` or ``firstName``/``lastName``).

    ``short_form`` is the item's ``tex.shortauthor``. For several organizations it is the
    joined form ("NYSEG and RG&E"), of which only the first member is used.

    >>> author_part([{"creatorType": "author", "name": "Massachusetts Department of Public Utilities"}], "MA DPU")
    'madpu'
    >>> author_part([{"creatorType": "author", "firstName": "José Ignacio", "lastName": "Pérez-Arriaga"}])
    'perezarriaga'
    """
    ordered = _ordered_creators(creators)
    if not ordered:
        raise NoCreatorError("item has no creator; every item needs a reviewed author")
    first = ordered[0]
    if not _is_org(first):
        return _person_part(first)
    if short_form:
        n_orgs = sum(1 for c in ordered if _is_org(c))
        first_short = _MULTI_SHORT_SPLIT_RE.split(short_form)[0] if n_orgs > 1 else short_form
        return squash(first_short)
    return squash(first.get("name") or first.get("literal") or "")


def title_part(title: str | None, n_words: int = 3) -> str:
    """Better BibTeX ``shorttitle(3,3)`` title part.

    >>> title_part("Should 'Energy Hogs' Shoulder More of the Utility Cost Burden?")
    'ShouldEnergyHogs'
    >>> title_part("Docket 23-150: Order")
    'Docket23150Order'
    """
    t = ascii_fold(title or "")
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"(?<=[A-Za-z0-9])[.&](?=[A-Za-z0-9])", "", t)
    words = re.findall(r"[A-Za-z0-9]+(?:[-'\u2019][A-Za-z0-9]+)*", t)
    out: list[str] = []
    for w in words:
        if w.lower() in STOP_WORDS:
            continue
        w = re.sub(r"[-'\u2019]", "", w)
        out.append(w[0].upper() + w[1:])
        if len(out) == n_words:
            break
    return "".join(out)


def parse_date(date: str | None) -> tuple[int, int, int] | None:
    """Best-effort (year, month, day) from a Zotero date string; 0 for unknown parts."""
    s = (date or "").strip()
    if m := re.match(r"^(\d{4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?", s):
        return int(m.group(1)), int(m.group(2) or 0), int(m.group(3) or 0)
    if m := re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", s):
        return int(m.group(3)), int(m.group(1)), int(m.group(2))
    if not (y := re.search(r"\b(1[5-9]\d\d|2[01]\d\d)\b", s)):
        return None
    month = next((v for k, v in _MONTHS.items() if re.search(rf"\b{k}", s, re.IGNORECASE)), 0)
    day = re.search(r"\b(\d{1,2})(?:st|nd|rd|th)?\b,", s)
    return int(y.group(1)), month, int(day.group(1)) if day and month else 0


def year_part(date: str | None) -> str:
    """4-digit year of the item's date, or ``nd``.

    >>> year_part("2024-06-24"), year_part("June 2024"), year_part("")
    ('2024', '2024', 'nd')
    """
    parsed = parse_date(date)
    return f"{parsed[0]:04d}" if parsed else "nd"


def item_title(item: Item) -> str | None:
    """Zotero's title, or its type-specific equivalent (cases, statutes, emails)."""
    return item.get("title") or item.get("caseName") or item.get("nameOfAct") or item.get("subject")


def item_date(item: Item) -> str | None:
    """Zotero's date, or its type-specific equivalent (cases, statutes, patents)."""
    return item.get("date") or item.get("dateDecided") or item.get("dateEnacted") or item.get("issueDate")


def short_form(item: Item) -> str | None:
    """The item's ``tex.shortauthor`` from Extra, if any."""
    return extra_mod.get(item.get("extra"), extra_mod.SHORTAUTHOR)


def base_key(item: Item) -> str:
    """Rule-generated key without a collision suffix."""
    author = author_part(item.get("creators", []), short_form(item))
    return f"{author}_{title_part(item_title(item))}_{year_part(item_date(item))}"


def split_key(key: str) -> tuple[str, str, str, str] | None:
    """Split a key into (author, title, year, suffix), or None if it isn't in the pattern."""
    m = _KEY_RE.match(key)
    return (m["author"], m["title"], m["year"], m["suffix"]) if m else None


def conforms(key: str, item: Item) -> bool:
    """Whether an existing key follows the rule (ignoring a collision suffix).

    Author and year parts must equal the rule's; the title part may come from the title or
    the short title and is compared case-insensitively, so keys Better BibTeX built from a
    short title or with other capitalization are kept.
    """
    parts = split_key(key)
    if parts is None:
        return False
    author, title, year, _ = parts
    try:
        rule_author = author_part(item.get("creators", []), short_form(item))
    except NoCreatorError:
        return False
    titles = {title_part(item_title(item)).casefold(), title_part(item.get("shortTitle")).casefold()}
    return author == rule_author and year == year_part(item_date(item)) and title.casefold() in titles


def suffixes() -> Iterable[str]:
    """'', 'a', ..., 'z', 'aa', 'ab', ..."""
    yield ""
    for n in count(1):
        for letters in product(string.ascii_lowercase, repeat=n):
            yield "".join(letters)


def propose_key(item: Item, taken: set[str]) -> str:
    """First free key for ``item``: the base key, then base + 'a', 'b', ...

    Does not modify ``taken``. Raises NoCreatorError for an item without a creator.
    """
    base = base_key(item)
    return next(base + s for s in suffixes() if base + s not in taken)


def _collision_order(item: Item) -> tuple:
    parsed = parse_date(item_date(item))
    return (parsed is None, parsed or (0, 0, 0), item_title(item) or "", item.get("key") or "")


def assign_keys(items: Iterable[Item], current_keys: Mapping[str, str], reserved: Iterable[str] = ()) -> dict[str, str]:
    """Canonical key for every item, resolving collisions deterministically.

    ``current_keys`` maps Zotero item key -> current citation key. ``reserved`` holds keys
    that must not be reused (for example, other items' locked keys). Returns item key ->
    citation key.

    1. Items whose current key conforms keep it, suffix included (first come, if two
       items claim the same key).
    2. The rest are ordered by date (missing last), title and Zotero item key.
    3. Each takes the first free key in base, base + 'a', 'b', ...
    """
    items = list(items)
    taken = set(reserved)
    result: dict[str, str] = {}
    for item in sorted(items, key=_collision_order):
        current = current_keys.get(item["key"])
        if current and current not in taken and conforms(current, item):
            result[item["key"]] = current
            taken.add(current)
    for item in sorted(items, key=_collision_order):
        if item["key"] in result:
            continue
        key = propose_key(item, taken)
        result[item["key"]] = key
        taken.add(key)
    return result
