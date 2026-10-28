"""Consistency checks on the bibliography's organization names, dates and citation keys.

Checks only report; nothing is repaired. Fix the item in Zotero and regenerate. ``sync-bib``
runs them in ``warn`` mode (print and continue) or ``strict`` mode (errors block writing).
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any, Literal

from rapidfuzz import fuzz, process

from lib.sources import citekeys, extra

Level = Literal["error", "warning"]

ORG_CUES = re.compile(
    r"\b(company|corporation|corp|inc|llc|commission|department|authority|agency|administration|association|"
    r"institute|council|coalition|fund|board|bureau|office|university|laboratory|lab|group|utilities|utility|"
    r"energy|gas|electric|power|grid|state|city|county|foundation|center|centre|network|partners|alliance|"
    r"society|committee|services|operator|economics|research|cooperative|america|project|initiative)\b",
    re.IGNORECASE,
)
# Organizations whose legal name is itself an acronym (RMI, formerly Rocky Mountain Institute).
LEGAL_ACRONYM_NAMES = frozenset({"DNV", "GFT", "HEET", "ICF", "RMI"})
_BARE_ABBREVIATION = re.compile(r"^[A-Z0-9&.\-/ ]{2,10}$")
_PERSON_NAME = re.compile(r"^[A-Z][a-z'\u2019\-]+(?: [A-Z]\.?)?(?: [A-Z][a-z'\u2019\-]+){1,2}$")
# pandoc reads a bibliography id as Markdown: "_Foo_" becomes emphasis and can't be cited.
_EMPHASIS_IN_KEY = re.compile(r"(?<![A-Za-z0-9])_(?=[^_\s]).*?(?<=[^_\s])_(?![A-Za-z0-9])")
FUZZY_THRESHOLD = 92


@dataclass(frozen=True)
class Finding:
    level: Level
    code: str
    key: str
    message: str


def _orgs(data: Mapping[str, Any]) -> list[str]:
    return [c["name"] for c in data.get("creators", []) if "name" in c]


def _short(data: Mapping[str, Any]) -> str | None:
    try:
        return extra.get(data.get("extra"), extra.SHORTAUTHOR)
    except extra.ExtraError:
        return None


def chicago_join(parts: list[str]) -> str:
    """Chicago-style join: "A and B", "A, B, and C", "A et al." for four or more."""
    if len(parts) >= 4:
        return f"{parts[0]} et al."
    if len(parts) == 3:
        return f"{parts[0]}, {parts[1]}, and {parts[2]}"
    return " and ".join(parts)


def key_not_citable(key: str) -> bool:
    """Whether pandoc would read the key as Markdown emphasis, so citations can't find it."""
    return bool(_EMPHASIS_IN_KEY.search(key))


def run_checks(
    entries: Iterable[tuple[str, Mapping[str, Any]]],
    *,
    unpinned: Iterable[Mapping[str, str]] = (),
    literal_dates: Mapping[str, Mapping[str, str]] | None = None,
) -> list[Finding]:
    """Run every check on (citation key, Zotero item data) pairs in the bibliography."""
    entries = list(entries)
    findings: list[Finding] = []

    def add(level: Level, code: str, key: str, message: str) -> None:
        findings.append(Finding(level, code, key, message))

    single_org_short: dict[str, set[str]] = defaultdict(set)
    short_to_names: dict[str, set[str]] = defaultdict(set)
    for _, data in entries:
        orgs, short = _orgs(data), _short(data)
        if len(orgs) == 1 and len(data.get("creators", [])) == 1 and short:
            single_org_short[orgs[0]].add(short)
            short_to_names[short].add(orgs[0])
    all_shorts = set(short_to_names)

    for name, shorts in sorted(single_org_short.items()):
        if len(shorts) > 1:
            add("error", "FULL_NAME_SEVERAL_SHORT_FORMS", "", f"{name!r} has short forms {sorted(shorts)}")
    for short, names in sorted(short_to_names.items()):
        if len(names) > 1:
            add("error", "SHORT_FORM_SEVERAL_NAMES", "", f"short form {short!r} is used for {sorted(names)}")

    key_counts = Counter(key for key, _ in entries)
    for key, n in sorted(key_counts.items()):
        if n > 1:
            add("error", "DUPLICATE_KEY", key, f"pinned on {n} items")

    for key, data in entries:
        creators = data.get("creators", [])
        orgs, short = _orgs(data), _short(data)
        for name in orgs:
            if name in LEGAL_ACRONYM_NAMES:
                continue
            if _BARE_ABBREVIATION.match(name) or name in all_shorts:
                add("error", "AUTHOR_IS_ABBREVIATION", key, f"author {name!r} looks like an abbreviation")
            elif _PERSON_NAME.match(name) and not ORG_CUES.search(name):
                add("warning", "PERSON_IN_ONE_FIELD", key, f"single-field creator {name!r} looks like a person")
        for c in creators:
            if "lastName" in c:
                first, last = c.get("firstName", ""), c.get("lastName", "")
                if not first and "," in last:
                    add("warning", "PERSON_IN_ONE_FIELD", key, f"creator {last!r} is a whole name in the family field")
                elif not first or ORG_CUES.search(last):
                    add(
                        "error", "ORG_AS_TWO_FIELD_NAME", key, f"creator {last!r}, {first!r} looks like an organization"
                    )
                elif last.isupper() and len(last) > 1:
                    add(
                        "error",
                        "ORG_AS_TWO_FIELD_NAME",
                        key,
                        f"creator {last!r}, {first!r} has an all-caps family name",
                    )
        if len(orgs) > 1 and short:
            members = [next(iter(single_org_short[o])) for o in orgs if len(single_org_short.get(o, ())) == 1]
            if len(members) == len(orgs) and short != chicago_join(members):
                add("error", "MULTI_ORG_SHORT_FORM", key, f"short form {short!r} != {chicago_join(members)!r}")
        names = set(orgs) | ({short} if short else set())
        for field in ("publisher", "institution"):
            if (value := data.get(field)) and value in names:
                add("error", "PUBLISHER_REPEATS_AUTHOR", key, f"{field} {value!r} repeats the author")
        if not creators:
            add("warning", "NO_CREATOR", key, "item has no creator")
        elif not citekeys.conforms(key, data):
            add("warning", "KEY_NOT_CANONICAL", key, f"rule gives {citekeys.base_key(data)!r}")
        if key.endswith("_nd") or re.search(r"_nd[a-z]{0,2}$", key):
            add("warning", "UNDATED_KEY", key, "key year part is 'nd'")
        if (native := data.get("citationKey")) and native != key:
            add("warning", "PIN_DIFFERS_FROM_NATIVE_KEY", key, f"Zotero's native citationKey is {native!r}")
        if key_not_citable(key):
            add("error", "KEY_NOT_CITABLE", key, "pandoc reads this key as Markdown emphasis; citations can't find it")

    for item in unpinned:
        add("warning", "UNPINNED", item["zotero_item"], f"not yet processed (no pinned key): {item['title'][:80]!r}")
    for key, dates in (literal_dates or {}).items():
        for var, text in dates.items():
            add("warning", "INVALID_DATE", key, f"{var} {text!r} is not a valid date (written as literal)")

    names = sorted({n for _, d in entries for n in _orgs(d)})
    seen: set[frozenset[str]] = set()
    for name in names:
        if len(name) < 6:
            continue
        for other, score, _ in process.extract(name, names, scorer=fuzz.token_sort_ratio, limit=5):
            pair = frozenset((name, other))
            if other != name and score >= FUZZY_THRESHOLD and len(other) >= 6 and pair not in seen:
                seen.add(pair)
                add("warning", "SIMILAR_ORG_NAMES", "", f"{name!r} ~ {other!r} ({score:.0f})")
    return findings


def summarize(findings: list[Finding]) -> str:
    """Counts by level and code, then every finding, errors first."""
    counts = Counter((f.level, f.code) for f in findings)
    lines = [f"{n:5d}  {level:7s} {code}" for (level, code), n in sorted(counts.items())]
    for f in sorted(findings, key=lambda f: (f.level != "error", f.code, f.key)):
        lines.append(f"{f.level:7s} {f.code:30s} {f.key:55s} {f.message}")
    return "\n".join(lines)
