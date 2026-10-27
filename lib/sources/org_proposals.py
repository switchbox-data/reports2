"""Schema and validation for the reconcile-orgs agent pass.

Each agent batch writes ``proposals/batch_NN.json``. ``load_proposals`` validates every file, merges
clusters that agents marked as the same organization across batches, and reports problems for the
review sheet. Nothing here touches Zotero.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from lib.sources import citekeys

GENERIC_AGENCY = frozenset({"dpu", "psc", "puc", "dep", "dec", "dps", "bpu", "dpuc", "pura"})


class Evidence(BaseModel):
    quote: str = Field(min_length=1)
    source: str = Field(min_length=1, description="citation key and page, or a URL")


class ItemOverride(BaseModel):
    item: str
    role: str
    action: Literal["assign", "remove", "split"]
    to: list[str] = Field(default_factory=list, description="full names (assign, split); empty for remove")
    reason: str = Field(min_length=1)
    evidence: list[Evidence] = Field(default_factory=list)


class Cluster(BaseModel):
    groups: list[str] = Field(min_length=1)
    same_as_groups: list[str] = Field(default_factory=list)
    kind: Literal["organization", "person", "not_an_organization"]
    canonical_full_name: str | None = None
    short_form: str | None = None
    short_form_source: Literal["own_usage", "common_usage", "state_prefix_rule", "none"] = "none"
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]
    flags: list[str] = Field(default_factory=list)
    item_overrides: list[ItemOverride] = Field(default_factory=list)
    needs_decision: bool = False
    notes: str = ""

    @model_validator(mode="after")
    def _consistent(self) -> Cluster:
        if self.kind == "organization" and not self.canonical_full_name:
            raise ValueError("an organization needs canonical_full_name")
        if self.short_form and self.short_form_source == "none":
            raise ValueError(f"short form {self.short_form!r} needs a short_form_source")
        if self.short_form and not self.evidence:
            raise ValueError(f"short form {self.short_form!r} needs evidence")
        if self.short_form and citekeys.squash(self.short_form) in GENERIC_AGENCY:
            raise ValueError(f"bare generic short form {self.short_form!r}: add the state prefix")
        if self.kind != "organization" and self.short_form:
            raise ValueError("only organizations have a short form")
        return self


class BatchProposal(BaseModel):
    batch: str
    clusters: list[Cluster]


class MergedCluster(BaseModel):
    id: str
    groups: list[str]
    batches: list[str]
    proposals: list[Cluster]
    split_into: list[str] = Field(
        default_factory=list, description="full names, when the name strings list several organizations"
    )


_JOINER_RE = re.compile(r"^(?:;\s*|,\s*(?:and\s+)?|\s+and\s+|\s*&\s*)")


def segment_names(name: str, known: Iterable[str]) -> list[str] | None:
    """Split ``name`` into two or more ``known`` full names joined by ';', ',', 'and' or '&'.

    Names may themselves contain "and" ("Rochester Gas and Electric"), so this matches known
    names rather than splitting on separators. Returns the canonical spellings, or None.

    >>> segment_names("NYSEG and Rochester Gas and Electric", ["NYSEG", "Rochester Gas and Electric"])
    ['NYSEG', 'Rochester Gas and Electric']
    """
    by_fold = {k.casefold(): k for k in known}
    longest_first = sorted(by_fold, key=lambda k: -len(k))

    def seg(s: str) -> list[str] | None:
        for k in longest_first:
            if not s.startswith(k):
                continue
            rest = s[len(k) :]
            if not rest:
                return [by_fold[k]]
            if (m := _JOINER_RE.match(rest)) and (tail := seg(rest[m.end() :])):
                return [by_fold[k], *tail]
        return None

    parts = seg(name.casefold().strip())
    return parts if parts and len(parts) > 1 else None


class Conflict(BaseModel):
    cluster: str
    field: Literal["canonical_full_name", "short_form"]
    options: list[str]
    batches: list[str]


def load_batches(paths: Iterable[Path]) -> tuple[list[BatchProposal], list[str]]:
    out, problems = [], []
    for p in sorted(paths):
        try:
            out.append(BatchProposal.model_validate(json.loads(p.read_text(encoding="utf-8"))))
        except Exception as e:  # report every bad file, not just the first
            problems.append(f"{p.name}: {e}")
    return out, problems


def merge(
    proposals: list[BatchProposal], expected_groups: dict[str, set[str]]
) -> tuple[list[MergedCluster], list[str]]:
    """Union clusters linked by ``same_as_groups`` and check coverage and uniqueness.

    ``expected_groups`` maps batch id to the group ids it was given; every one must be assigned
    exactly once in its own batch.
    """
    problems: list[str] = []
    assigned: dict[str, list[tuple[str, int]]] = defaultdict(list)
    clusters: list[tuple[str, Cluster]] = []
    for bp in proposals:
        given = expected_groups.get(bp.batch, set())
        seen: set[str] = set()
        for c in bp.clusters:
            idx = len(clusters)
            clusters.append((bp.batch, c))
            for g in c.groups:
                if g not in given:
                    problems.append(f"{bp.batch}: group {g} was not in this batch (use same_as_groups)")
                if g in seen:
                    problems.append(f"{bp.batch}: group {g} assigned twice")
                seen.add(g)
                assigned[g].append((bp.batch, idx))
        if missing := sorted(given - seen):
            problems.append(f"{bp.batch}: groups not assigned: {', '.join(missing)}")
    for batch in sorted(set(expected_groups) - {bp.batch for bp in proposals}):
        problems.append(f"{batch}: no proposal file")

    # A name that lists several known organizations is a split instruction, not an organization.
    known = {c.canonical_full_name for _, c in clusters if c.kind == "organization" and c.canonical_full_name}
    split: dict[int, tuple[str, ...]] = {}
    for idx, (_, c) in enumerate(clusters):
        if c.kind != "organization" or not c.canonical_full_name:
            continue
        if ";" in c.canonical_full_name:
            split[idx] = tuple(p.strip() for p in c.canonical_full_name.split(";") if p.strip())
        elif parts := segment_names(c.canonical_full_name, known - {c.canonical_full_name}):
            split[idx] = tuple(parts)

    parent = list(range(len(clusters)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    by_name: dict[str | tuple[str, ...], int] = {}
    for idx, (_, c) in enumerate(clusters):
        for g in c.same_as_groups:
            for _, other in assigned.get(g, []):
                if split.get(idx) == split.get(other):
                    parent[find(idx)] = find(other)
        if c.kind == "organization" and c.canonical_full_name:
            name: str | tuple[str, ...] = split.get(idx) or c.canonical_full_name.casefold()
            if name in by_name:
                parent[find(idx)] = find(by_name[name])
            else:
                by_name[name] = idx
    by_root: dict[int, list[int]] = defaultdict(list)
    for idx in range(len(clusters)):
        by_root[find(idx)].append(idx)
    merged: list[MergedCluster] = []
    for members in by_root.values():
        props = [clusters[i][1] for i in members]
        merged.append(
            MergedCluster(
                id="",
                groups=sorted({g for p in props for g in p.groups}),
                batches=sorted({clusters[i][0] for i in members}),
                proposals=props,
                split_into=list(split.get(members[0], ())),
            )
        )
    merged.sort(key=lambda m: m.groups[0])
    for i, m in enumerate(merged, 1):
        m.id = f"C{i:03d}"
    owners: dict[str, list[str]] = defaultdict(list)
    for m in merged:
        for g in m.groups:
            owners[g].append(m.id)
    for g, ids in sorted(owners.items()):
        if len(ids) > 1:
            problems.append(f"group {g} ended up in several clusters: {', '.join(ids)}")
    return merged, problems


def conflicts(merged: list[MergedCluster]) -> list[Conflict]:
    """Disagreements for the review sheet: names or short forms that batches proposed differently."""
    out: list[Conflict] = []
    short_owner: dict[str, set[str]] = defaultdict(set)
    for m in merged:
        if m.split_into:
            continue
        names = sorted({p.canonical_full_name for p in m.proposals if p.canonical_full_name})
        if len({n.casefold() for n in names}) > 1:
            out.append(Conflict(cluster=m.id, field="canonical_full_name", options=names, batches=m.batches))
        shorts = sorted({p.short_form for p in m.proposals if p.short_form})
        if len(shorts) > 1:
            out.append(Conflict(cluster=m.id, field="short_form", options=shorts, batches=m.batches))
        for s in shorts:
            short_owner[s].add(m.id)
    for s, ids in sorted(short_owner.items()):
        if len(ids) > 1:
            out.append(Conflict(cluster=", ".join(sorted(ids)), field="short_form", options=[s], batches=[]))
    return out
