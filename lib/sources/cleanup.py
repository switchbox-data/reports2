"""One-off cleanup actions for the review sheet: likely duplicates and known library problems."""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from lib.sources import citekeys, orgs, snapshot


def normalize_url(url: str | None) -> str:
    """Comparison form of a URL; DocumentCloud links reduce to their document id."""
    u = (url or "").strip().lower()
    u = re.sub(r"^https?://(www\.)?", "", u)
    u = re.sub(r"[?#].*$", "", u).rstrip("/")
    if m := re.search(r"documentcloud\.org/documents/(\d+)", u):
        return f"documentcloud:{m[1]}"
    return u


def duplicate_sets(snap: snapshot.Snapshot, plans: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Sets of items that look like the same document.

    Strong: an identical attached file (md5). Medium: the same URL. Title matches count only when
    the new author part matches too, since utilities file same-titled studies in the same docket.
    """
    plans = {p["item"]: p for p in plans}
    files: dict[str, set[str]] = defaultdict(set)
    for it in snap["items"]:
        d = it["data"]
        if d.get("parentItem") in plans and d.get("md5"):
            files[d["md5"]].add(d["parentItem"])
    by: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for md5, items in files.items():
        by[("same attached file", md5)] |= items
    for k, p in plans.items():
        a = p["after"]
        if u := normalize_url(a.get("url")):
            by[("same URL", u)].add(k)
        title = orgs.normalize(citekeys.item_title(a) or "")
        author = (citekeys.split_key(p["key"]) or ("",))[0] if p["key"] else ""
        if len(title) > 12 and author:
            by[("same title, author and year", title, author, citekeys.year_part(citekeys.item_date(a)))].add(k)
    out: list[dict[str, Any]] = []
    seen: set[frozenset[str]] = set()
    for key, items in sorted(
        by.items(),
        key=lambda kv: ["same attached file", "same URL"].index(kv[0][0])
        if kv[0][0] != "same title, author and year"
        else 2,
    ):
        fs = frozenset(items)
        if len(fs) < 2 or fs in seen:
            continue
        seen.add(fs)
        ordered = sorted(fs, key=lambda i: (not plans[i]["cited"], -len(plans[i]["after"].get("creators", [])), i))
        out.append({"reason": key[0], "items": ordered, "keep": ordered[0]})
    return out


def actions(
    snap: snapshot.Snapshot, plans: Sequence[Mapping[str, Any]], unresolved: Iterable[str], summary: snapshot.Summary
) -> list[dict[str, Any]]:
    """Rows for the Cleanup tab."""
    by_item = {p["item"]: p for p in plans}

    def label(i: str) -> str:
        p = by_item[i]
        cited = f", cited as {', '.join(p['cited'])}" if p["cited"] else ""
        return f"{i} {p['key'] or p['old_keys']}: {(citekeys.item_title(p['after']) or '')[:70]}{cited}"

    rows: list[dict[str, Any]] = []
    for n, d in enumerate(duplicate_sets(snap, plans), 1):
        rows.append({
            "id": f"D{n:02d}",
            "type": f"possible duplicate ({d['reason']})",
            "items": [label(i) for i in d["items"]],
            "description": "These items may be the same document.",
            "proposed_action": f"keep {d['keep']}; move the others to the trash and point their old keys at its key"
            if d["reason"] == "same attached file"
            else "check: same document? If so keep the first listed",
        })  # fmt: skip
    for n, key in enumerate(sorted(unresolved), 1):
        rows.append({
            "id": f"U{n:02d}",
            "type": "citation with no item",
            "items": [key],
            "description": f"Reports cite @{key} but no item in Reports has this key.",
            "proposed_action": "find the item (or add it) so the citation resolves",
        })  # fmt: skip
    for n, (key, items) in enumerate(sorted(summary.duplicate_keys.items()), 1):
        rows.append({
            "id": f"K{n:02d}",
            "type": "two items with one key",
            "items": [label(i) for i in items if i in by_item],
            "description": f"Both items currently have the key {key}; the new keys separate them.",
            "proposed_action": f"say which item reports mean by @{key}; its new key replaces the old one in reports",
        })  # fmt: skip
    for n, i in enumerate(sorted(r.item for r in summary.empty), 1):
        rows.append({
            "id": f"E{n:02d}",
            "type": "empty item",
            "items": [label(i)] if i in by_item else [i],
            "description": "No title, creator or date.",
            "proposed_action": "move to the trash",
        })  # fmt: skip
    return rows
