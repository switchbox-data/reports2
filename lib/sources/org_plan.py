"""Proposed metadata for every in-scope item, from the reviewed organization clusters.

``build`` applies each item's per-item overrides and its groups' clusters to its creators and
organization fields, sets ``tex.shortauthor`` and computes every citation key from scratch with
:func:`citekeys.assign_keys` (no current key is kept). The result feeds the review sheet and,
after review, the Zotero apply step. Nothing here touches Zotero.
"""

from __future__ import annotations

import copy
import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from lib.sources import citekeys, docket_titles, extra, orgs, snapshot, title_case
from lib.sources.item_fixes import ItemFix
from lib.sources.org_proposals import ItemOverride, MergedCluster

# Primary creator type where "author" is not valid for the item type.
PRIMARY_CREATOR = {"bill": "sponsor", "presentation": "presenter", "computerProgram": "programmer"}


_MONTH_NAMES = {
    m: i
    for i, m in enumerate(
        [
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
        ],
        start=1,
    )
}
_MONTH_RE = "|".join(sorted({*_MONTH_NAMES, *(m[:3] for m in _MONTH_NAMES), "sept"}, key=lambda s: -len(s)))
_FILENAME_RE = re.compile(
    r"[0-9a-f]{16,}|\w_\w|^[a-z0-9]+(?:-[a-z0-9]+){2,}$|\.(?:pdf|docx?|xlsx?|csv)$", re.IGNORECASE
)


def looks_like_filename(title: str) -> bool:
    """Titles copied from a file name or URL slug ("mag-gas-adjustment-factors", "EUSS_ResRound1")."""
    return bool(_FILENAME_RE.search(title.strip()))


def _month(name: str) -> int:
    name = name.lower().rstrip(".")
    return next(v for k, v in _MONTH_NAMES.items() if k.startswith(name[:3]))


def normalize_date(s: str) -> str | None:
    """ISO form (YYYY, YYYY-MM or YYYY-MM-DD) of a US-style date, or None if it isn't one.

    >>> [normalize_date(x) for x in ("5/1/2025", "10/2023", "7-14-2026", "January 31, 2022", "Dec. 2022")]
    ['2025-05-01', '2023-10', '2026-07-14', '2022-01-31', '2022-12']
    """
    s = s.strip()
    if re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", s):
        return s
    # Timestamps, and ISO dates followed by a second copy ("2024-08-15 8/15/24").
    if m := re.match(r"(\d{4}-\d{2}-\d{2})(?:T[\d:.]+(?:Z|[+-]\d{2}:?\d{2})?|\s+\S+)$", s):
        return m[1]
    patterns: list[tuple[str, tuple[str, str, str]]] = [
        (r"(?P<y>\d{4})[/.-](?P<m>\d{1,2})[/.-](?P<d>\d{1,2})", ("y", "m", "d")),
        (r"(?P<m>\d{1,2})[/.-](?P<d>\d{1,2})[/.-](?P<y>\d{4})", ("y", "m", "d")),
        (r"(?P<m>\d{1,2})[/-](?P<y>\d{4})", ("y", "m", "")),
        (rf"(?P<mn>{_MONTH_RE})\.?,?\s+(?P<d>\d{{1,2}})(?:st|nd|rd|th)?,?\s+(?P<y>\d{{4}})", ("y", "mn", "d")),
        (rf"(?P<d>\d{{1,2}})\s+(?P<mn>{_MONTH_RE})\.?,?\s+(?P<y>\d{{4}})", ("y", "mn", "d")),
        (rf"(?P<mn>{_MONTH_RE})\.?,?\s+(?P<y>\d{{4}})", ("y", "mn", "")),
    ]
    for pat, (yk, mk, dk) in patterns:
        if not (m := re.fullmatch(pat, s, re.IGNORECASE)):
            continue
        y = int(m[yk])
        mo = _month(m[mk]) if mk == "mn" else int(m[mk])
        d = int(m[dk]) if dk else 0
        if not 1 <= mo <= 12 or d > 31:
            return None
        return f"{y:04d}-{mo:02d}" + (f"-{d:02d}" if d else "")
    return None


DATE_FIELDS = ("date", "dateDecided", "dateEnacted", "issueDate")
TITLE_FIELDS = ("title", "caseName", "nameOfAct", "subject")


@dataclass(frozen=True)
class Resolved:
    """A cluster's reviewed outcome: what every mention in its groups becomes."""

    cluster: str
    kind: str  # "organization", "person", "not_an_organization" or "split"
    full_name: str | None
    short_form: str | None
    split_into: tuple[str, ...] = ()


@dataclass
class ItemPlan:
    item: str
    scope: str
    item_type: str
    old_keys: list[str]
    cited: list[str]
    before: dict[str, Any]
    after: dict[str, Any]
    key: str | None = None
    action: str = "update"  # "update", "delete" or "duplicate" (trashed; old keys point at duplicate_of)
    duplicate_of: str | None = None
    changes: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)


def resolve(
    merged: Iterable[MergedCluster], decisions: Mapping[str, Mapping[str, Any]] | None = None
) -> dict[str, Resolved]:
    """Cluster id -> outcome. Defaults to the first proposal; ``decisions`` (from the sheet) override it."""
    out: dict[str, Resolved] = {}
    for m in merged:
        first = m.proposals[0]
        kind = "split" if m.split_into else first.kind
        res = Resolved(m.id, kind, first.canonical_full_name, first.short_form, tuple(m.split_into))
        if d := (decisions or {}).get(m.id):
            res = Resolved(
                m.id,
                d.get("kind", res.kind),
                d.get("full_name", res.full_name),
                d.get("short_form", res.short_form) or None,
                tuple(d.get("split_into", res.split_into)),
            )
        out[m.id] = res
    return out


def short_forms(resolved: Mapping[str, Resolved]) -> dict[str, str | None]:
    """Casefolded full name -> short form, for names an override assigns."""
    out: dict[str, str | None] = {}
    for r in resolved.values():
        if r.kind == "organization" and r.full_name:
            out.setdefault(r.full_name.casefold(), r.short_form)
    return out


def joined_short(forms: list[str]) -> str:
    """Chicago-style join: "A", "A and B", "A, B and C", "A et al." for four or more."""
    if len(forms) >= 4:
        return f"{forms[0]} et al."
    if len(forms) <= 2:
        return " and ".join(forms)
    return f"{', '.join(forms[:-1])} and {forms[-1]}"


def item_shortauthor(creators: Sequence[Mapping[str, str]], shorts: Mapping[str, str | None]) -> str | None:
    """The item's short form: its primary creators' short forms, joined; none if any is a person."""
    ordered = citekeys._ordered_creators(creators)
    if not ordered:
        return None
    primary = [c for c in ordered if c.get("creatorType") == ordered[0].get("creatorType")]
    if any(not citekeys._is_org(c) for c in primary):
        return None
    names = [c.get("name") or "" for c in primary]
    forms = [shorts.get(n.casefold()) for n in names]
    if not any(forms):
        return None
    return joined_short([f or n for f, n in zip(forms, names, strict=True)])


def _mention_group(m: Mapping[str, Any], norm_to_group: Mapping[str, str]) -> str | None:
    norm = m["text"] if m["role"] == "key_author" else orgs.normalize(m["text"])
    return norm_to_group.get(norm)


def _names_for(
    mention: Mapping[str, Any],
    group_cluster: Mapping[str, str],
    norm_to_group: Mapping[str, str],
    resolved: Mapping[str, Resolved],
    overrides: Mapping[tuple[str, str], list[tuple[str, ItemOverride]]],
    flags: list[str],
    sole_in_role: bool,
) -> tuple[list[str] | None, str | None]:
    """Replacement names for one mention (None = unchanged, [] = remove) and the reason.

    An override names an item and role but not a position, so it applies to the mention whose
    cluster proposed it, or to the only mention in that role.
    """
    gid = _mention_group(mention, norm_to_group)
    cid = group_cluster.get(gid or "")
    ovs = overrides.get((mention["item"], mention["role"]), [])
    mine = [o for c, o in ovs if c == cid]
    if not mine and sole_in_role:
        mine = [o for _, o in ovs]
    if mine:
        actions = {(o.action, tuple(o.to)) for o in mine}
        if len(actions) > 1:
            flags.append(f"conflicting overrides on {mention['role']}: {sorted(actions)}")
        o = mine[0]
        return ([] if o.action == "remove" else list(o.to)), f"override ({o.action}): {o.reason}"
    if cid is None:
        return None, None
    r = resolved[cid]
    if r.kind == "split":
        return list(r.split_into), f"{cid}: several organizations"
    if r.kind == "organization" and r.full_name:
        return [r.full_name], f"{cid}"
    if r.kind != "organization" and not mention["role"].startswith("field:"):
        flags.append(f"{mention['role']} {mention['text']!r} is {r.kind.replace('_', ' ')} ({cid}); no override")
    return None, None


def _person_split(name: str, known: Mapping[str, tuple[str, str]], comma_only: bool) -> tuple[str, str] | None:
    """(first, last) for a person stored as one field: "Last, First", or "First [Middle] Last"
    unless ``comma_only``."""
    if (hit := known.get(name.casefold())) is not None:
        return hit
    if name.count(",") == 1:
        last, first = (s.strip() for s in name.split(","))
        if first and last and orgs.classify_creator({"firstName": first, "lastName": last})[1] == "person":
            return first, last
        return None
    if comma_only or orgs.classify_creator({"name": name})[1] != "person" or " " not in name:
        return None
    first, last = name.rsplit(" ", 1)
    return first, last


def canonical_creator(
    c: Mapping[str, str],
    org_names: Mapping[str, str],
    known_people: Mapping[str, tuple[str, str]],
    *,
    from_zotero: bool,
    not_people: frozenset[str] = frozenset(),
) -> dict[str, str]:
    """A creator with a known organization's reviewed full name, or a single-field person split in two.

    Only names already in Zotero are split on looks alone; names the cleanup assigned are
    organizations unless written "Last, First".
    """
    if "name" not in c:
        return dict(c)
    name = c["name"].strip()
    if (full := org_names.get(orgs.normalize(name))) is not None:
        return {"creatorType": c["creatorType"], "name": full}
    if name.casefold() in not_people:
        return dict(c)
    if (split := _person_split(name, known_people, comma_only=not from_zotero)) is not None:
        return {"creatorType": c["creatorType"], "firstName": split[0], "lastName": split[1]}
    return dict(c)


def build(
    snap: snapshot.Snapshot,
    mentions: Iterable[Mapping[str, Any]],
    groups: Iterable[Mapping[str, Any]],
    merged: list[MergedCluster],
    key_rows: Iterable[Mapping[str, Any]],
    decisions: Mapping[str, Mapping[str, Any]] | None = None,
    fixes: Mapping[str, ItemFix] | None = None,
    today: tuple[int, int, int] = (9999, 12, 31),
    rulings: Mapping[str, Mapping[str, Any]] | None = None,
    not_people_names: Iterable[str] = (),
    dockets: Mapping[str, Mapping[str, Any]] | None = None,
    short_form_names: Mapping[str, str] | None = None,
) -> list[ItemPlan]:
    """``rulings`` (item key -> reviewer ruling) beat everything else: ``creators`` (names, or
    ``{"firstName", "lastName"}``), ``fields`` (Zotero field -> value) and ``action``
    (``delete``, or ``duplicate`` with ``duplicate_of``). ``not_people_names`` are single-field
    organizations whose names look like people's. ``dockets`` (item key -> ``{"docket", "title"}``)
    are researched docket numbers for proceeding documents whose metadata has none.
    ``short_form_names`` (organization full name -> short form) are the reviewer's short forms for
    organizations that have none, including ones outside any cluster."""
    resolved = resolve(merged, decisions)
    shorts = short_forms(resolved)
    shorts.update({name.casefold(): sf for name, sf in (short_form_names or {}).items()})
    norm_to_group = {g["norm"]: g["id"] for g in groups}
    group_cluster = {g: m.id for m in merged for g in m.groups}
    overrides: dict[tuple[str, str], list[tuple[str, ItemOverride]]] = defaultdict(list)
    for m in merged:
        for p in m.proposals:
            for o in p.item_overrides:
                overrides[(o.item, o.role)].append((m.id, o))
    by_item: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for mt in mentions:
        by_item[mt["item"]].append(mt)
    rows = {r["item"]: r for r in key_rows}
    items = {it["key"]: it["data"] for it in snap["items"]}
    org_names = {
        g["norm"]: r.full_name
        for g in groups
        if (cid := group_cluster.get(g["id"])) and (r := resolved[cid]).kind == "organization" and r.full_name
    }
    for m in merged:
        r = resolved[m.id]
        if r.kind == "organization" and r.full_name:
            for name in [r.full_name] + [p.canonical_full_name for p in m.proposals if p.canonical_full_name]:
                org_names[orgs.normalize(name)] = r.full_name
    not_people = frozenset(n.casefold() for n in not_people_names)
    title_names = {r.full_name for r in resolved.values() if r.full_name} | {
        c["name"] for d in items.values() for c in d.get("creators", []) if c.get("name")
    }
    title_acronyms = {r.short_form for r in resolved.values() if r.short_form and " " not in r.short_form}
    title_acronyms |= title_case.library_acronyms(
        d.get(f) or "" for d in items.values() for f in TITLE_FIELDS if isinstance(d.get(f), str)
    )
    known_people: dict[str, tuple[str, str]] = {}
    people_sources = [c for r in (rulings or {}).values() for c in r.get("creators", []) if isinstance(c, dict)]
    people_sources += [c for d in items.values() for c in d.get("creators", [])]
    for c in people_sources:
        if c.get("firstName") and c.get("lastName") and orgs.classify_creator(c)[1] == "person":
            known_people.setdefault(f"{c['firstName']} {c['lastName']}".casefold(), (c["firstName"], c["lastName"]))

    plans: list[ItemPlan] = []
    for item_key, row in rows.items():
        data = items[item_key]
        after = copy.deepcopy(data)
        p = ItemPlan(item_key, row["scope"], data["itemType"], row["old_keys"], row["cited"], data, after)
        mts = by_item.get(item_key, [])
        role_n = Counter(m["role"] for m in mts if m["kind"] != "person")
        by_pos = {mt["position"]: mt for mt in mts if mt["role"].startswith("creator:")}

        creators: list[dict[str, str]] = []
        for i, c in enumerate(data.get("creators", [])):
            mt = by_pos.get(i)
            names, why = (None, None)
            if mt is not None and mt["kind"] != "person":
                names, why = _names_for(
                    mt, group_cluster, norm_to_group, resolved, overrides, p.flags, role_n[mt["role"]] == 1
                )
            if names is None:
                creators.append(dict(c))
                continue
            new = [{"creatorType": c.get("creatorType", "author"), "name": n} for n in names]
            if [orgs.classify_creator(c)[0]] != names or "name" not in c:
                p.changes.append(f"{mt and mt['role']}: {orgs.classify_creator(c)[0]!r} -> {names} [{why}]")
            creators.extend(new)

        for f in orgs.ORG_FIELDS:
            if not (value := (data.get(f) or "").strip()):
                continue
            mt = next((m for m in mts if m["role"] == f"field:{f}"), None)
            names, why = (None, None)
            if mt is not None:
                names, why = _names_for(
                    mt, group_cluster, norm_to_group, resolved, overrides, p.flags, role_n[mt["role"]] == 1
                )
            if names is None:
                continue
            new_value = "; ".join(names)
            if new_value != value:
                after[f] = new_value
                p.changes.append(f"{f}: {value!r} -> {new_value!r} [{why}]")

        fix = (fixes or {}).get(item_key)
        if fix is not None and fix.action == "duplicate_of" and fix.duplicate_of not in rows:
            p.flags.append(f"duplicate of {fix.duplicate_of}, which is outside Reports and Inbox; kept this copy")
            fix = fix.model_copy(update={"action": "fix"})
        if fix is not None and fix.action != "fix":
            p.action = "delete" if fix.action == "delete" else "duplicate"
            p.duplicate_of = fix.duplicate_of
            p.changes.append(f"{p.action}{f' (of {fix.duplicate_of})' if fix.duplicate_of else ''}: {fix.notes}")
            plans.append(p)
            continue
        if fix is not None and (fix.organizations or fix.people):
            ctype = PRIMARY_CREATOR.get(data["itemType"], "author")
            suggested = [{"creatorType": ctype, "name": n} for n in fix.organizations] + [
                {"creatorType": ctype, "firstName": pp.first, "lastName": pp.last} for pp in fix.people
            ]
            names = [orgs.classify_creator(c)[0] for c in suggested]
            if creators:
                old = [orgs.classify_creator(c)[0] for c in creators]
                p.changes.append(f"authors {old} -> {names} (researched, {fix.confidence}): {fix.notes}")
            else:
                p.changes.append(f"author (researched, {fix.confidence}): {names}")
            creators = suggested
        if fix is not None and fix.title:
            tf = next((f for f in TITLE_FIELDS if f in data), "title")
            p.changes.append(f"{tf}: {data.get(tf)!r} -> {fix.title!r} (researched, {fix.confidence})")
            after[tf] = fix.title

        df = next((f for f in DATE_FIELDS if f in data), "date")
        if fix is not None and fix.date:
            p.changes.append(f"{df}: {data.get(df)!r} -> {fix.date!r} (researched, {fix.confidence})")
            after[df] = fix.date
        elif raw := (data.get(df) or "").strip():
            iso = normalize_date(raw)
            if iso is None:
                p.flags.append(f"date {raw!r} is not a date we can normalize")
            elif iso != raw:
                after[df] = iso
                p.changes.append(f"{df}: {raw!r} -> {iso!r}")
        if (d := citekeys.parse_date(after.get(df))) and d > today:
            p.flags.append(f"date {after.get(df)!r} is in the future")

        ka = None if creators else next((m for m in mts if m["role"] == "key_author"), None)
        if ka is not None:
            names, why = _names_for(ka, group_cluster, norm_to_group, resolved, overrides, p.flags, True)
            if names:
                ctype = PRIMARY_CREATOR.get(data["itemType"], "author")
                creators = [{"creatorType": ctype, "name": n} for n in names]
                p.changes.append(f"author (from old key {ka['text']!r}): {names} [{why}]")

        author_names = {c["name"].casefold() for c in creators if "name" in c}
        for f in orgs.ORG_FIELDS:
            v = (after.get(f) or "").strip()
            if v and v.casefold() in author_names:
                after[f] = ""
                p.changes.append(f"{f}: {v!r} removed (repeats the author)")

        if (rule := (rulings or {}).get(item_key)) is not None:
            why = rule.get("reason", "reviewer ruling")
            if rule.get("action") in ("delete", "duplicate"):
                p.action = rule["action"]
                p.duplicate_of = rule.get("duplicate_of")
                p.changes.append(f"{p.action}{f' (of {p.duplicate_of})' if p.duplicate_of else ''} [{why}]")
                plans.append(p)
                continue
            if "creators" in rule:
                ctype = PRIMARY_CREATOR.get(data["itemType"], "author")
                new = [
                    {"creatorType": ctype, "name": c} if isinstance(c, str) else {"creatorType": ctype, **c}
                    for c in rule["creators"]
                ]
                p.changes.append(
                    f"authors {[orgs.classify_creator(c)[0] for c in creators]} -> "
                    f"{[orgs.classify_creator(c)[0] for c in new]} [{why}]"
                )
                creators = new
            for f, v in rule.get("fields", {}).items():
                p.changes.append(f"{f}: {after.get(f)!r} -> {v!r} [{why}]")
                after[f] = v

        tf = next((f for f in TITLE_FIELDS if f in data), "title")
        if (found := (dockets or {}).get(item_key)) and found.get("docket"):
            new_title = f"Docket {found['docket']}: {found.get('title') or after.get(tf) or ''}".strip()
            if new_title != after.get(tf):
                p.changes.append(f"{tf}: {after.get(tf)!r} -> {new_title!r} (docket found, {found.get('confidence')})")
                after[tf] = new_title
        if (uncapped := title_case.uncap_title(after.get(tf) or "", title_names, title_acronyms)) is not None:
            p.changes.append(f"{tf}: {after.get(tf)!r} -> {uncapped!r} (was all caps)")
            after[tf] = uncapped
        if (docket := docket_titles.docket_title(after.get(tf) or "", after)) is not None:
            p.changes.append(f"{tf}: {after.get(tf)!r} -> {docket!r} (docket title)")
            after[tf] = docket

        originals = data.get("creators", [])
        normalized = [
            canonical_creator(c, org_names, known_people, from_zotero=c in originals, not_people=not_people)
            for c in creators
        ]
        for old, new in zip(creators, normalized, strict=True):
            if old != new:
                p.changes.append(f"creator {orgs.classify_creator(old)[0]!r} -> {new}")
        creators = normalized

        if creators != data.get("creators", []):
            after["creators"] = creators
        try:
            old_short = extra.get(data.get("extra"), extra.SHORTAUTHOR)
        except extra.ExtraError as e:
            p.flags.append(f"unreadable Extra: {e}")
            old_short = None
        new_short = item_shortauthor(creators, shorts)
        if new_short != old_short:
            after["extra"] = extra.set_field(data.get("extra"), extra.SHORTAUTHOR, new_short)
            p.changes.append(f"short form: {old_short!r} -> {new_short!r}")
        if not creators:
            p.flags.append("no author: needs one before it can have a key")
        plans.append(p)

    keyable = [{**p.after, "key": p.item} for p in plans if p.action == "update" and p.after.get("creators")]
    keys = citekeys.assign_keys(keyable, current_keys={})
    for p in plans:
        p.key = keys.get(p.item)
    return plans
