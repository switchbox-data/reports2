"""Organization-name reconciliation for the library cleanup: extraction and candidate links.

``extract`` turns a snapshot into one :class:`OrgMention` per organization-looking string (creators
and the organization-bearing fields). ``group_mentions`` folds mentions that normalize identically
into :class:`OrgGroup` rows, and ``candidate_edges`` proposes links between groups (acronyms,
author-plus-publisher pairs, existing short forms, fuzzy matches). Edges are suggestions for the
reconcile-orgs agent pass and the human review, never final clusters.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field, replace
from typing import Any, Literal

from rapidfuzz import fuzz

from lib.sources import checks, citekeys, extra, snapshot

# Zotero fields that name an organization (publisher, issuing institution, venue, site owner).
ORG_FIELDS = (
    "publisher",
    "institution",
    "websiteTitle",
    "repository",
    "legislativeBody",
    "blogTitle",
    "company",
    "university",
    "court",
)
Kind = Literal["org", "person", "ambiguous"]
STRONG, WEAK, FUZZY_MIN_LEN = 92, 80, 6

US_STATES = {
    "alabama": "al", "alaska": "ak", "arizona": "az", "arkansas": "ar", "california": "ca", "colorado": "co",
    "connecticut": "ct", "delaware": "de", "district of columbia": "dc", "florida": "fl", "georgia": "ga",
    "hawaii": "hi", "idaho": "id", "illinois": "il", "indiana": "in", "iowa": "ia", "kansas": "ks",
    "kentucky": "ky", "louisiana": "la", "maine": "me", "maryland": "md", "massachusetts": "ma",
    "michigan": "mi", "minnesota": "mn", "mississippi": "ms", "missouri": "mo", "montana": "mt",
    "nebraska": "ne", "nevada": "nv", "new hampshire": "nh", "new jersey": "nj", "new mexico": "nm",
    "new york": "ny", "new york state": "nys", "north carolina": "nc", "north dakota": "nd", "ohio": "oh",
    "oklahoma": "ok", "oregon": "or", "pennsylvania": "pa", "rhode island": "ri", "south carolina": "sc",
    "south dakota": "sd", "tennessee": "tn", "texas": "tx", "utah": "ut", "vermont": "vt", "virginia": "va",
    "washington": "wa", "west virginia": "wv", "wisconsin": "wi", "wyoming": "wy",
}  # fmt: skip
_ACRONYM_SKIP = frozenset({"of", "and", "the", "for", "on", "in", "at", "to", "a", "an"})
_LEGAL_SUFFIX = re.compile(r"\b(inc|llc|ltd|corp|co|lp|llp|plc)\b\.?$")
_HARD_SPLIT = re.compile(r"\s*;\s*|\s*/\s*")
_SOFT_SPLIT = re.compile(r",\s*(?:and\s+)?|\s+and\s+|\s*&\s*")


@dataclass(frozen=True)
class OrgMention:
    item: str
    current_key: str | None
    role: str  # "creator:<creatorType>", "field:<zotero field>" or "key_author"
    text: str
    kind: Kind
    shape: str  # "single", "two" (firstName/lastName) or "-" for fields and key parts
    position: int  # creator index, 0 for fields
    cited: int  # citations of this item in reports
    shortauthor: str | None
    item_type: str
    title: str | None


@dataclass
class OrgGroup:
    id: str
    norm: str
    variants: Counter[str] = field(default_factory=Counter)
    roles: Counter[str] = field(default_factory=Counter)
    items: set[str] = field(default_factory=set)
    cited_items: set[str] = field(default_factory=set)
    shortauthors: Counter[str] = field(default_factory=Counter)
    kinds: Counter[str] = field(default_factory=Counter)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "norm": self.norm,
            "variants": dict(self.variants.most_common()),
            "roles": dict(self.roles.most_common()),
            "n_items": len(self.items),
            "n_cited_items": len(self.cited_items),
            "items": sorted(self.items),
            "shortauthors": dict(self.shortauthors.most_common()),
            "kinds": dict(self.kinds.most_common()),
        }


@dataclass(frozen=True)
class CandidateEdge:
    a: str
    b: str
    reason: str  # "acronym", "author_publisher", "shortauthor", "fuzzy_strong", "fuzzy_weak", "split_part"
    weight: int
    evidence: str


# --- normalization -------------------------------------------------------------------------------


def normalize(s: str) -> str:
    """Comparison form: ASCII, lowercase, "&" as "and", no punctuation, no leading "the" or legal suffix.

    >>> normalize("The Brooklyn Union Gas Company, Inc.")
    'brooklyn union gas company'
    >>> normalize("Orange & Rockland")
    'orange and rockland'
    """
    s = citekeys.ascii_fold(s).lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    s = re.sub(r"^the\s+", "", s)
    while (t := _LEGAL_SUFFIX.sub("", s).strip()) != s:
        s = t
    return re.sub(r"\s+", " ", s)


def _strip_state(norm: str) -> tuple[str | None, str]:
    for name in sorted(US_STATES, key=lambda s: -len(s)):
        if norm.startswith(name + " "):
            return US_STATES[name], norm[len(name) + 1 :]
    return None, norm


def acronyms(norm: str) -> set[str]:
    """Initialisms a full name may go by, with and without its state prefix.

    >>> sorted(acronyms("massachusetts department of public utilities"))
    ['dpu', 'madpu', 'mdpu']
    """
    words = norm.split()
    if len(words) < 2:
        return set()
    out = {"".join(w[0] for w in words if w not in _ACRONYM_SKIP)}
    state, rest = _strip_state(norm)
    if state and len(rest.split()) >= 2:
        core = "".join(w[0] for w in rest.split() if w not in _ACRONYM_SKIP)
        out |= {core, state + core}
    return {a for a in out if len(a) >= 2}


# --- extraction ----------------------------------------------------------------------------------


def classify_creator(creator: Mapping[str, str]) -> tuple[str, Kind, str]:
    """(display text, kind, shape) for a Zotero creator."""
    if "name" in creator:
        name = creator["name"].strip()
        if checks._PERSON_NAME.match(name) and not checks.ORG_CUES.search(name):
            return name, "person", "single"
        return name, "org", "single"
    first, last = (creator.get("firstName") or "").strip(), (creator.get("lastName") or "").strip()
    text = f"{first} {last}".strip() if first else last
    if not first or checks.ORG_CUES.search(last) or checks.ORG_CUES.search(first):
        return text, "org", "two"
    if last.isupper() and len(last) >= 2:
        return text, "ambiguous", "two"
    return text, "person", "two"


def _shortauthor(data: Mapping[str, Any]) -> str | None:
    try:
        return extra.get(data.get("extra"), extra.SHORTAUTHOR)
    except extra.ExtraError:
        return None


def extract(snap: snapshot.Snapshot, cite_counts: Mapping[str, int]) -> list[OrgMention]:
    """Every organization-looking string on items in Reports or Inbox.

    People are included (kind ``person``) so the person-split review can use the same table, but
    only ``org`` and ``ambiguous`` mentions are grouped. Items with no creator contribute their
    current key's author part as a ``key_author`` mention: it usually names the issuer.
    """
    summary = snapshot.summarize(snap)
    in_scope = {r.item: r for r in summary.rows if r.scope != "neither"}
    out: list[OrgMention] = []
    for it in snap["items"]:
        row = in_scope.get(it["key"])
        if row is None:
            continue
        data = it["data"]
        cited = sum(cite_counts.get(k, 0) for k in {row.key, row.native} if k)
        base = OrgMention(
            item=it["key"],
            current_key=row.key,
            role="",
            text="",
            kind="org",
            shape="-",
            position=0,
            cited=cited,
            shortauthor=_shortauthor(data),
            item_type=data["itemType"],
            title=citekeys.item_title(data),
        )
        for i, c in enumerate(data.get("creators", [])):
            text, kind, shape = classify_creator(c)
            if text:
                role = f"creator:{c.get('creatorType', 'author')}"
                out.append(replace(base, role=role, text=text, kind=kind, shape=shape, position=i))
        for f in ORG_FIELDS:
            if v := (data.get(f) or "").strip():
                out.append(replace(base, role=f"field:{f}", text=v))
        if not data.get("creators") and row.key and (parts := citekeys.split_key(row.key)) and parts[0]:
            out.append(replace(base, role="key_author", text=parts[0]))
    return out


def group_mentions(mentions: Iterable[OrgMention]) -> list[OrgGroup]:
    """One group per normalized string, over organization and ambiguous mentions."""
    by_norm: dict[str, OrgGroup] = {}
    for m in mentions:
        if m.kind == "person":
            continue
        norm = normalize(m.text) if m.role != "key_author" else m.text
        if not norm:
            continue
        g = by_norm.setdefault(norm, OrgGroup(id="", norm=norm))
        g.variants[m.text] += 1
        g.roles[m.role] += 1
        g.items.add(m.item)
        if m.cited:
            g.cited_items.add(m.item)
        if m.shortauthor and m.role.startswith("creator:"):
            g.shortauthors[m.shortauthor] += 1
        g.kinds[m.kind] += 1
    groups = sorted(by_norm.values(), key=lambda g: (-len(g.items), g.norm))
    for i, g in enumerate(groups, 1):
        g.id = f"G{i:03d}"
    return groups


# --- candidate edges -----------------------------------------------------------------------------


def split_parts(text: str, known: Mapping[str, OrgGroup]) -> list[tuple[str, OrgGroup]]:
    """Known organizations inside a string that may name several.

    ";" and "/" always separate names. "," and "and" separate only when every part is a known
    organization, so "Public Service Electric and Gas Company" stays whole.
    """
    hard = [p for p in _HARD_SPLIT.split(text) if p.strip()]
    if len(hard) > 1:
        return [(p, known[normalize(p)]) for p in hard if normalize(p) in known]
    soft = [p for p in _SOFT_SPLIT.split(text) if p.strip()]
    if len(soft) > 1 and all(normalize(p) in known for p in soft):
        return [(p, known[normalize(p)]) for p in soft]
    return []


def candidate_edges(groups: list[OrgGroup], mentions: Iterable[OrgMention]) -> list[CandidateEdge]:
    """Possible links between groups, each with a reason. Never merged automatically."""
    mentions = list(mentions)
    by_norm = {g.norm: g for g in groups}
    by_squash: dict[str, list[OrgGroup]] = defaultdict(list)
    for g in groups:
        by_squash[g.norm.replace(" ", "")].append(g)
    edges: dict[tuple[str, str, str], CandidateEdge] = {}

    def add(a: OrgGroup, b: OrgGroup, reason: str, weight: int, evidence: str) -> None:
        if a.id == b.id:
            return
        x, y = sorted((a.id, b.id))
        edges.setdefault((x, y, reason), CandidateEdge(x, y, reason, weight, evidence))

    for g in groups:
        for acr in acronyms(g.norm):
            for h in by_squash.get(acr, []):
                add(g, h, "acronym", 3, f"{h.norm!r} is an initialism of {g.norm!r}")
        for short in g.shortauthors:
            for h in by_squash.get(citekeys.squash(short), []):
                add(g, h, "shortauthor", 3, f"items authored {g.norm!r} carry tex.shortauthor {short!r}")
        for variant in g.variants:
            for part, h in split_parts(variant, by_norm):
                add(g, h, "split_part", 2, f"{part!r} is one of several names in {variant!r}")

    norm_of = {m: normalize(m.text) if m.role != "key_author" else m.text for m in mentions if m.kind != "person"}
    per_item: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for m, n in norm_of.items():
        per_item[m.item]["creator" if m.role.startswith("creator:") else m.role].add(n)
    for roles in per_item.values():
        for author in roles.get("creator", set()) | roles.get("key_author", set()):
            for f in ("field:publisher", "field:institution"):
                for other in roles.get(f, set()):
                    if author != other and author in by_norm and other in by_norm:
                        add(by_norm[author], by_norm[other], "author_publisher", 1, f"same item: author / {f[6:]}")

    long = [g for g in groups if len(g.norm) >= FUZZY_MIN_LEN]
    for i, g in enumerate(long):
        for h in long[i + 1 :]:
            score = fuzz.token_sort_ratio(g.norm, h.norm)
            if score >= STRONG:
                add(g, h, "fuzzy_strong", 2, f"token_sort_ratio {score:.0f}")
            elif score >= WEAK:
                add(g, h, "fuzzy_weak", 1, f"token_sort_ratio {score:.0f}")
    return sorted(edges.values(), key=lambda e: (e.a, e.b, e.reason))


def components(groups: list[OrgGroup], edges: Iterable[CandidateEdge], min_weight: int = 2) -> list[list[str]]:
    """Connected groups of group ids over edges of at least ``min_weight``, for batching the agent pass."""
    parent = {g.id: g.id for g in groups}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in edges:
        if e.weight >= min_weight:
            parent[find(e.a)] = find(e.b)
    comps: dict[str, list[str]] = defaultdict(list)
    for g in groups:
        comps[find(g.id)].append(g.id)
    return sorted(comps.values(), key=lambda c: (-len(c), c[0]))


def mention_dict(m: OrgMention) -> dict[str, Any]:
    return asdict(m)


def batches(comps: list[list[str]], size: int = 25) -> list[list[str]]:
    """Pack connected components into batches of about ``size`` groups, never splitting one."""
    out: list[list[str]] = []
    for comp in comps:
        if out and len(out[-1]) + len(comp) <= size:
            out[-1].extend(comp)
        else:
            out.append(list(comp))
    return out


def batch_payload(
    batch: list[str],
    groups: Mapping[str, OrgGroup],
    mentions: Iterable[OrgMention],
    edges: Iterable[CandidateEdge],
    snap: snapshot.Snapshot,
) -> dict[str, Any]:
    """Everything the reconcile-orgs agent needs for one batch: groups, their items and links."""
    ids = set(batch)
    data_by_item = {it["key"]: it["data"] for it in snap["items"]}
    norm_of_group = {g.norm: gid for gid, g in groups.items()}
    items: dict[str, dict[str, Any]] = {}
    for m in mentions:
        if m.kind == "person":
            continue
        gid = norm_of_group.get(normalize(m.text) if m.role != "key_author" else m.text)
        if gid not in ids:
            continue
        d = data_by_item[m.item]
        entry = items.setdefault(
            m.item,
            {
                "item": m.item,
                "current_key": m.current_key,
                "item_type": m.item_type,
                "title": m.title,
                "date": citekeys.item_date(d),
                "url": d.get("url") or None,
                "cited": m.cited,
                "creators": d.get("creators", []),
                "shortauthor": m.shortauthor,
                **{f: d[f] for f in ORG_FIELDS if d.get(f)},
                "mentions": [],
            },
        )
        entry["mentions"].append({"group": gid, "role": m.role, "text": m.text})
    return {
        "groups": [groups[g].as_dict() for g in batch],
        "edges": [asdict(e) for e in edges if e.a in ids or e.b in ids],
        "items": sorted(items.values(), key=lambda e: e["item"]),
    }
