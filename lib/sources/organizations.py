"""Organization lookup for the details card: lookup only, no stored registry.

The Zotero library (as mirrored in ``reports/references.yaml``) and the subsidiary table in
``context/code/source_metadata_conventions.md`` are the source of truth. :func:`find_organization` takes a
full name or an abbreviation and returns every distinct (full name, short form) already in use, with a count
and example keys, so a new item reuses the library's exact spelling.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from rapidfuzz import fuzz

from lib.sources import bib, checks, env, extra

CONVENTIONS = env.REPO_ROOT / "context" / "code" / "source_metadata_conventions.md"
_LEGAL_SUFFIX = re.compile(r"[ ,]+(inc|llc|ltd|plc|corp|co)\.?$", re.IGNORECASE)
_NO_SHORT = re.compile(r"^\(none\)|^$", re.IGNORECASE)


@dataclass
class OrgMatch:
    """One distinct (full name, short form) already in the library or the subsidiary table."""

    full_name: str
    short_form: str | None
    score: float
    count: int = 0
    example_keys: list[str] = field(default_factory=list)
    sources: set[str] = field(default_factory=set)  # "references", "zotero", "conventions"
    legal_name: str | None = None  # the legal company, for subsidiary-table rows


def normalize(name: str) -> str:
    """Casefolded name without a leading "The", legal suffixes or punctuation ("The Foo Co., Inc." -> "foo co").

    >>> normalize("The Narragansett Electric Company, Inc.")
    'narragansett electric company'
    """
    s = re.sub(r"^the\s+", "", name.strip(), flags=re.IGNORECASE)
    s = _LEGAL_SUFFIX.sub("", s)
    return re.sub(r"[^a-z0-9]+", " ", s.casefold().replace("&", " and ")).strip()


_STOPWORDS = frozenset({"of", "the", "and", "for", "on"})


def _initialism_match(q: str, n: str) -> bool:
    """Whether ``q`` is ``n`` with a trailing run of words abbreviated ("massachusetts dpu" for the Department).

    >>> _initialism_match("massachusetts dpu", "massachusetts department of public utilities")
    True
    >>> _initialism_match("massachusetts dpu", "massachusetts electric company")
    False
    """
    qt, nt = q.split(), n.split()
    for k in range(len(qt)):
        if qt[:k] != nt[:k] or k >= len(nt):
            continue
        rest = [w for w in nt[k:] if w not in _STOPWORDS]
        if len(rest) > 1 and "".join(qt[k:]) == "".join(w[0] for w in rest):
            return True
    return False


def _score(query: str, candidates: Iterable[str | None]) -> float:
    """Best similarity of ``query`` to any candidate; exact matches (after normalizing) score 100."""
    q = normalize(query)
    best = 0.0
    for c in candidates:
        if not c:
            continue
        n = normalize(c)
        if n == q:
            return 100.0
        best = max(best, fuzz.token_sort_ratio(q, n))
        if _initialism_match(q, n):
            best = max(best, 92.0)
        # "DPU" should find "Massachusetts Department of Public Utilities" only through the short form
        if len(q) >= 5 and len(n) >= 5 and (q in n or n in q):
            best = max(best, 90.0)
    return best


def references_organizations(path: Path | None = None) -> list[tuple[str, str | None, str]]:
    """(full name, short form, citation key) for every organization author in ``references.yaml``."""
    path = path or env.REFERENCES_YAML
    if not path.exists():
        return []
    refs = yaml.load(path.read_text(encoding="utf-8"), Loader=bib._Loader).get("references") or []
    out = []
    for r in refs:
        authors = r.get("author") or []
        for a in authors:
            # Pandoc's CSL-YAML writer renders a single-field (organization) name as ``family`` alone.
            name = a.get("literal") or (a["family"] if "family" in a and "given" not in a else None)
            if name:
                out.append((name, r.get("author-short") if len(authors) == 1 else None, r["id"]))
    return out


def zotero_organizations(items: Iterable[Mapping[str, Any]]) -> list[tuple[str, str | None, str]]:
    """The same triples from Zotero items (``data`` dicts), for items not yet in ``references.yaml``."""
    out = []
    for it in items:
        d = it["data"]
        if d["itemType"] in ("attachment", "note", "annotation"):
            continue
        try:
            key = extra.get(d.get("extra"), extra.CITATION_KEY)
            short = extra.get(d.get("extra"), extra.SHORTAUTHOR)
        except extra.ExtraError:
            continue
        creators = d.get("creators") or []
        single = len(creators) == 1
        for c in creators:
            if "name" in c:
                out.append((c["name"], short if single else None, key or it["key"]))
    return out


def subsidiary_table(path: Path | None = None) -> list[dict[str, str]]:
    """Rows of the subsidiary table: legal company, parent, full name and short form."""
    path = path or CONVENTIONS
    rows: list[dict[str, str]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and len(cells) >= 5 and not set(cells[0]) <= {"-", " "} and cells[0] != "legal company":
            short = re.sub(r"\s*\(verify\)$", "", cells[3])
            rows.append(
                {
                    "legal": cells[0],
                    "parent": cells[1],
                    "full": cells[2],
                    "short": "" if _NO_SHORT.match(short) else short,
                }
            )
    return rows


def find_organization(
    query: str,
    references: Path | None = None,
    items: Iterable[Mapping[str, Any]] | None = None,
    conventions: Path | None = None,
    threshold: float = checks.FUZZY_THRESHOLD - 7,
    limit: int = 8,
) -> list[OrgMatch]:
    """Distinct organizations matching ``query`` (a full name or an abbreviation), best first.

    Looks in ``references.yaml``, then in ``items`` (Zotero data, when given), then in the subsidiary table.
    More than one result for the same organization means the library spells it two ways.
    """
    groups: dict[tuple[str, str | None], OrgMatch] = {}

    def consider(full: str, short: str | None, key: str | None, source: str, legal: str | None = None) -> None:
        score = _score(query, (full, short, legal))
        if score < threshold:
            return
        m = groups.setdefault((full, short or None), OrgMatch(full, short or None, score, legal_name=legal))
        m.score = max(m.score, score)
        m.sources.add(source)
        if key:
            m.count += 1
            if len(m.example_keys) < 3:
                m.example_keys.append(key)

    seen_keys: set[str] = set()
    for full, short, key in references_organizations(references):
        seen_keys.add(key)
        consider(full, short, key, "references")
    if items is not None:
        for full, short, key in zotero_organizations(items):
            if key not in seen_keys:
                consider(full, short, key, "zotero")
    for row in subsidiary_table(conventions):
        consider(row["full"], row["short"] or None, None, "conventions", legal=row["legal"])
    return sorted(groups.values(), key=lambda m: (-m.score, -m.count, m.full_name))[:limit]


def describe(matches: list[OrgMatch]) -> str:
    """Human-readable lines for ``just sources-org``, flagging organizations the library spells two ways."""
    if not matches:
        return (
            "No match: this looks like a NEW ORGANIZATION. Propose a full name and short form per the conventions doc."
        )
    lines = []
    for m in matches:
        short = m.short_form or "(no short form)"
        where = "/".join(sorted(m.sources))
        examples = f" e.g. {', '.join(m.example_keys)}" if m.example_keys else ""
        legal = f" [legal company: {m.legal_name}]" if m.legal_name else ""
        lines.append(f"{m.score:5.0f}  {m.full_name}  |  {short}  |  {m.count} items ({where}){examples}{legal}")
    exact = [m for m in matches if m.score >= 100]
    if len({(normalize(m.full_name), m.short_form) for m in exact}) > 1:
        lines.append(
            "Several spellings or short forms match: use the conventions-doc spelling; sync-bib will flag the others."
        )
    return "\n".join(lines)
