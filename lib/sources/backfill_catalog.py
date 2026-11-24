"""Backfill Zotero ``abstract`` from extract front matter (or pending sentinels). ``just sources-backfill-catalog``."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from lib.sources import bib, catalog, frontmatter, zotero

EXAMPLES = 8


@dataclass
class CatalogPlanItem:
    item_key: str
    citekey: str
    new_abstract: str
    kind: str  # with_extract | zotero_only_pending | publisher_tail_kept | unchanged


@dataclass
class CatalogPlan:
    items: list[CatalogPlanItem] = field(default_factory=list)
    stats: Counter[str] = field(default_factory=Counter)

    def note(self, kind: str) -> None:
        self.stats[kind] += 1


def build_extract_index(root: Path | None = None) -> dict[str, tuple[str, str, str]]:
    """``citekey`` -> ``(context, contents, why_here)`` for extracts that define all three."""
    index: dict[str, tuple[str, str, str]] = {}
    for path in frontmatter.iter_extracts(root):
        fm = frontmatter.read(path)
        citekey = fm.get("citekey")
        if not citekey:
            continue
        c, co, w = fm.get("context"), fm.get("contents"), fm.get("why_here")
        if c and co and w:
            index[str(citekey)] = (str(c).strip(), str(co).strip(), str(w).strip())
    return index


def triple_for_citekey(citekey: str, index: Mapping[str, tuple[str, str, str]]) -> tuple[str, str, str]:
    if hit := index.get(citekey):
        return hit
    pending = catalog.PENDING_CATALOG
    return pending, pending, pending


def plan_item(
    item: Mapping[str, Any],
    index: Mapping[str, tuple[str, str, str]],
    plan: CatalogPlan,
) -> CatalogPlanItem | None:
    data = item["data"]
    citekey = bib.pinned_key(data)
    if not citekey:
        return None
    current = data.get("abstract") or ""
    c, co, w = triple_for_citekey(citekey, index)
    block = catalog.format_zotero_abstract(c, co, w)
    new_abstract = catalog.merge_with_existing(current or None, block)

    if new_abstract == (current or ""):
        plan.note("unchanged")
        return None

    if citekey in index:
        plan.note("with_extract")
        kind = "with_extract"
    else:
        plan.note("zotero_only_pending")
        kind = "zotero_only_pending"
    if catalog.publisher_tail(current):
        plan.note("publisher_tail_kept")
    return CatalogPlanItem(item["key"], citekey, new_abstract, kind)


def make_plan(
    items: Iterable[Mapping[str, Any]], reports_collections: set[str], root: Path | None = None
) -> CatalogPlan:
    index = build_extract_index(root)
    plan = CatalogPlan()
    for item in sorted(items, key=lambda it: it["key"]):
        data = item["data"]
        if data["itemType"] in zotero.NON_BIB_TYPES or data.get("deleted") or data.get("parentItem"):
            continue
        if not reports_collections & set(data.get("collections") or []):
            continue
        if bib.pinned_key(data) is None:
            continue
        if p := plan_item(item, index, plan):
            plan.items.append(p)
    return plan


def apply_plan(plan: CatalogPlan) -> list[str]:
    failures: list[str] = []
    for p in plan.items:
        try:
            zotero.set_abstract(p.item_key, p.new_abstract)
        except Exception as e:
            failures.append(f"{p.item_key} {p.citekey}: {type(e).__name__}: {e}"[:300])
    return failures


def report(plan: CatalogPlan, apply: bool) -> str:
    lines = [
        f"{len(plan.items)} items {'updated' if apply else 'would update'}",
        "  counts: " + ", ".join(f"{k} {plan.stats[k]}" for k in sorted(plan.stats)),
    ]
    if plan.items:
        lines.append(f"Examples (first {EXAMPLES}):")
        step = max(1, len(plan.items) // EXAMPLES)
        for p in plan.items[::step][:EXAMPLES]:
            lines.append(f"  {p.citekey} ({p.kind})")
    return "\n".join(lines)


def run(apply: bool = False, root: Path | None = None) -> tuple[CatalogPlan, list[str]]:
    items = zotero.all_items(refresh=True)
    reports = set(zotero.collection_tree(zotero.REPORTS))
    plan = make_plan(items, reports, root)
    if not apply or not plan.items:
        return plan, []
    return plan, apply_plan(plan)
