"""Person lookup for the details card: lookup only, no stored registry.

Zotero stores each creator as plain text, so keeping a person consistent means typing them the same way every
time. :func:`find_person` returns every spelling of a matching person already in the library (``references.yaml``
plus Zotero), so a new item reuses it. A match needs the same family name and a compatible given name ("J." fits
"John", "Michael" fits "Michael J."); two names that only share a family name are different people.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from lib.sources import bib, env, extra


@dataclass
class PersonMatch:
    """One spelling of a person already in the library."""

    family: str
    given: str
    exact: bool
    count: int = 0
    example_keys: list[str] = field(default_factory=list)
    sources: set[str] = field(default_factory=set)  # "references", "zotero"

    def display(self) -> str:
        return f"{self.family}, {self.given}" if self.given else self.family


def fold(name: str) -> str:
    """Casefolded ASCII without punctuation, for comparing spellings ("Pérez-Arriaga" -> "perez arriaga").

    >>> fold("Pérez-Arriaga")
    'perez arriaga'
    """
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.casefold()).strip()


def _given_tokens(given: str) -> list[str]:
    # "J.H." and "J. H." both become ["j", "h"]
    return fold(given.replace(".", ". ")).split()


def _token_fits(a: str, b: str) -> bool:
    return a == b or (len(a) == 1 and b.startswith(a)) or (len(b) == 1 and a.startswith(b))


def given_compatible(a: str, b: str) -> bool:
    """Whether two given names could be the same person: first names agree (or one is its initial), and so do
    middle names where both have one. An empty given name fits anything.

    >>> given_compatible("Michael", "Michael J.")
    True
    >>> given_compatible("J.", "John")
    True
    >>> given_compatible("John", "Jane")
    False
    >>> given_compatible("Eric J.", "Eric R.")
    False
    """
    ta, tb = _given_tokens(a), _given_tokens(b)
    return all(_token_fits(x, y) for x, y in zip(ta, tb, strict=False))


def parse_name(query: str) -> tuple[str, str]:
    """(family, given) from "Family, Given" or "Given Family".

    >>> parse_name("Walsh, Michael J.")
    ('Walsh', 'Michael J.')
    >>> parse_name("Michael J. Walsh")
    ('Walsh', 'Michael J.')
    """
    if "," in query:
        family, given = query.split(",", 1)
        return family.strip(), given.strip()
    parts = query.split()
    return (parts[-1], " ".join(parts[:-1])) if parts else ("", "")


def references_people(path: Path | None = None) -> list[tuple[str, str, str]]:
    """(family, given, citation key) for every person author or editor in ``references.yaml``."""
    path = path or env.REFERENCES_YAML
    if not path.exists():
        return []
    refs = yaml.load(path.read_text(encoding="utf-8"), Loader=bib._Loader).get("references") or []
    out = []
    for r in refs:
        for role in ("author", "editor"):
            for a in r.get(role) or []:
                # A person has a given name; an organization is ``family`` (or ``literal``) alone.
                if "given" in a and "family" in a:
                    out.append((a["family"], a["given"], r["id"]))
    return out


def zotero_people(items: Iterable[Mapping[str, Any]]) -> list[tuple[str, str, str]]:
    """The same triples from Zotero items (``data`` dicts), for items not yet in ``references.yaml``."""
    out = []
    for it in items:
        d = it["data"]
        if d["itemType"] in ("attachment", "note", "annotation"):
            continue
        try:
            key = extra.get(d.get("extra"), extra.CITATION_KEY)
        except extra.ExtraError:
            continue
        for c in d.get("creators") or []:
            if c.get("lastName"):
                out.append((c["lastName"], c.get("firstName") or "", key or it["key"]))
    return out


def find_person(
    query: str,
    references: Path | None = None,
    items: Iterable[Mapping[str, Any]] | None = None,
) -> list[PersonMatch]:
    """Every spelling in the library of a person matching ``query``, exact spelling first, then most used."""
    family, given = parse_name(query)
    groups: dict[tuple[str, str], PersonMatch] = {}

    def consider(f: str, g: str, key: str, source: str) -> None:
        if fold(f) != fold(family) or not given_compatible(given, g):
            return
        exact = fold(g) == fold(given)
        m = groups.setdefault((f, g), PersonMatch(f, g, exact))
        m.sources.add(source)
        m.count += 1
        if len(m.example_keys) < 3:
            m.example_keys.append(key)

    seen_keys: set[str] = set()
    for f, g, key in references_people(references):
        seen_keys.add(key)
        consider(f, g, key, "references")
    if items is not None:
        for f, g, key in zotero_people(items):
            if key not in seen_keys:
                consider(f, g, key, "zotero")
    return sorted(groups.values(), key=lambda m: (not m.exact, -m.count, m.display()))


def describe(query: str, matches: list[PersonMatch]) -> str:
    """Human-readable lines for ``just sources-person``."""
    if not matches:
        return f"No match for {query!r}: a new person. Enter the name as printed (family name, given name)."
    lines = []
    for m in matches:
        where = "/".join(sorted(m.sources))
        tag = "same spelling" if m.exact else "compatible"
        lines.append(f"{m.display()}  |  {tag}  |  {m.count} items ({where}) e.g. {', '.join(m.example_keys)}")
    if len(matches) > 1 or not matches[0].exact:
        lines.append(
            "Possibly the same person spelled differently. If the document confirms it (same organization, same"
            " field), use the fullest spelling the document supports and say so on the card; otherwise enter the"
            " name as printed. Never merge on family name alone."
        )
    return "\n".join(lines)


def variant_spellings(people: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    """Pairs of distinct spellings ("Family, Given") that could be one person, for the ``sync-bib`` checks."""
    by_family: dict[str, set[tuple[str, str]]] = {}
    for f, g in people:
        by_family.setdefault(fold(f), set()).add((f, g))
    pairs = []
    for names in by_family.values():
        ordered = sorted(names)
        for i, (fa, ga) in enumerate(ordered):
            for fb, gb in ordered[i + 1 :]:
                if ga and gb and given_compatible(ga, gb):
                    pairs.append((f"{fa}, {ga}", f"{fb}, {gb}"))
    return pairs
