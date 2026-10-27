"""Thin pyzotero wrapper for the Switchbox Zotero group library.

Credentials come from ``ZOTERO_API_KEY`` and ``ZOTERO_GROUP_ID`` in the repo's ``.env``
(or the environment). The key is never printed.
"""

from __future__ import annotations

import os
from collections import defaultdict
from collections.abc import Iterable
from functools import cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pyzotero import zotero

REPO_ROOT = Path(__file__).resolve().parents[2]
NON_BIB_TYPES = frozenset({"attachment", "note", "annotation"})


@cache
def client() -> zotero.Zotero:
    """Zotero client for the group library, loading ``.env`` from the repo root."""
    load_dotenv(REPO_ROOT / ".env")
    missing = [v for v in ("ZOTERO_API_KEY", "ZOTERO_GROUP_ID") if not os.environ.get(v)]
    if missing:
        raise RuntimeError(f"Set {' and '.join(missing)} in {REPO_ROOT / '.env'}")
    return zotero.Zotero(os.environ["ZOTERO_GROUP_ID"], "group", os.environ["ZOTERO_API_KEY"])


def library_version() -> int:
    """Current library version (``Last-Modified-Version``)."""
    return client().last_modified_version()


def collections() -> list[dict[str, Any]]:
    """Every collection in the library."""
    z = client()
    return z.everything(z.collections())


def collection_tree(name: str, all_collections: list[dict[str, Any]] | None = None) -> list[str]:
    """Keys of the top-level collection ``name`` and all its subcollections, recursively."""
    cols = all_collections if all_collections is not None else collections()
    roots = [c["key"] for c in cols if c["data"]["name"] == name and not c["data"]["parentCollection"]]
    if len(roots) != 1:
        raise RuntimeError(f"Expected one top-level collection named {name!r}, found {len(roots)}")
    children: dict[str, list[str]] = defaultdict(list)
    for c in cols:
        if c["data"]["parentCollection"]:
            children[c["data"]["parentCollection"]].append(c["key"])
    tree, stack = [], [roots[0]]
    while stack:
        key = stack.pop()
        tree.append(key)
        stack.extend(children.get(key, []))
    return tree


def items_in_collections(collection_keys: Iterable[str], include: str = "data,csljson") -> list[dict[str, Any]]:
    """Top-level items in the given collections, de-duplicated by item key, trash excluded."""
    z = client()
    items: dict[str, dict[str, Any]] = {}
    for key in collection_keys:
        for item in z.everything(z.collection_items_top(key, include=include)):
            if not item["data"].get("deleted"):
                items[item["key"]] = item
    return sorted(items.values(), key=lambda it: it["key"])


def bibliographic(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop standalone attachments and notes, which are not bibliography entries."""
    return [it for it in items if it["data"]["itemType"] not in NON_BIB_TYPES]
