"""Give old library items the same citation links that ingest gives new ones (``just sources-backfill-links``).

Ingest sets an item's Zotero ``url`` to the DOI link (``https://doi.org/<doi>``) or, when there is a public
copy, to the short link ``https://pub.switch.box/<citation key>``. Items added before ingest existed carry
whatever URL they were saved with. This module brings them in line, for every item under ``Reports``:

- **DOI:** ``url`` becomes ``https://doi.org/<doi>``; the old ``url`` is kept as an "Original source" link attachment.
- **DocumentCloud link** (in ``url`` or in a link attachment): the document is added to ``links.json`` in
  ``switchbox-data/pub`` (one commit, one push for the whole run), ``url`` becomes the short link, the old
  ``url`` is kept as a link attachment, and the ``DocumentCloud ID`` line is written to Extra.
- **Both:** the DOI wins for ``url`` and there is no short link (as in ingest: DOI items link to doi.org and get
  no copy), but the existing DocumentCloud copy is still recorded (Extra ID and a link attachment).
- **Neither:** skipped.

A dry run (the default) only reads and reports. ``apply`` writes, in an order that makes a rerun safe: the short
links are published first, then for each item the link attachments and Extra, and ``url`` last, because the
URL is the one field a rerun can no longer recover the old value from. A finished item plans no actions, so a
second run writes nothing to Zotero and makes no commit to ``pub``. Zotero writes go through
:mod:`lib.sources.zotero_write`, so they are logged with the previous values and can be rolled back.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlsplit

from lib.sources import extra, metadata, shortlinks, zotero
from lib.sources.ingest import DOCUMENTCLOUD_TITLE, ORIGINAL_TITLE

DOCUMENTCLOUD_HOST = "documentcloud.org"
PUBLIC_HOST = "www.documentcloud.org"
LINK_MODES = ("linked_url", "imported_url")  # attachments that are a URL (not a stored file)
EXAMPLES = 10

# Action names, in the order they are reported.
SET_DOI_URL = "set url to doi.org link"
ADD_SHORT_LINK = "add short link to pub"
SET_SHORT_URL = "set url to short link"
KEEP_OLD_URL = "keep old url as link attachment"
ATTACH_DOCUMENTCLOUD = "attach DocumentCloud link"
WRITE_DOCUMENTCLOUD_ID = "write DocumentCloud ID to Extra"
ACTIONS = (
    SET_DOI_URL,
    ADD_SHORT_LINK,
    SET_SHORT_URL,
    KEEP_OLD_URL,
    ATTACH_DOCUMENTCLOUD,
    WRITE_DOCUMENTCLOUD_ID,
)


@dataclass(frozen=True)
class DocumentCloudRef:
    """A DocumentCloud document, however the library happened to link to it."""

    doc_id: str
    canonical: str  # the document page without annotations, query or fragment
    public_page: bool  # a www.documentcloud.org page, not a file on s3.documentcloud.org


def parse_documentcloud(url: str | None) -> DocumentCloudRef | None:
    """The document behind a DocumentCloud URL, or ``None`` for any other URL.

    Handles page URLs (``/documents/<id>-<slug>/``, with ``#document/p4/a12``, ``?mode=``, or page and
    annotation path suffixes) and the file URLs on ``s3.documentcloud.org`` (``/documents/<id>/<name>.pdf``,
    possibly signed).

    >>> parse_documentcloud("https://www.documentcloud.org/documents/123-a-b/#document/p4/a9").canonical
    'https://www.documentcloud.org/documents/123-a-b'
    >>> parse_documentcloud("https://s3.documentcloud.org/documents/123/a-b.pdf?X-Amz=1").doc_id
    '123'
    >>> parse_documentcloud("https://example.org/documents/123-a") is None
    True
    """
    if not url:
        return None
    parts = urlsplit(url.strip())
    host = (parts.hostname or "").lower()
    if host != DOCUMENTCLOUD_HOST and not host.endswith("." + DOCUMENTCLOUD_HOST):
        return None
    segments = [s for s in parts.path.split("/") if s]
    if "documents" not in segments[:-1]:
        return None
    rest = segments[segments.index("documents") + 1 :]
    m = re.fullmatch(r"(\d+)(?:-(.+))?", rest[0])
    if not m:
        return None
    doc_id, slug = m.group(1), m.group(2)
    if slug is None and len(rest) > 1 and host != PUBLIC_HOST:
        slug = re.sub(r"\.pdf$", "", rest[1], flags=re.IGNORECASE)  # s3 file URLs name the file, not the slug
    canonical = f"https://{PUBLIC_HOST}/documents/{doc_id}" + (f"-{slug}" if slug else "")
    return DocumentCloudRef(doc_id, canonical, host == PUBLIC_HOST)


def doi_link(doi: str) -> str:
    """``https://doi.org/<doi>`` for a DOI as stored in Zotero (bare, or already a doi.org URL)."""
    bare = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi.strip(), flags=re.IGNORECASE)
    return f"https://doi.org/{bare}"


@dataclass
class ItemPlan:
    """What backfill will do for one item. ``actions`` maps an action name to its detail."""

    item_key: str
    citekey: str
    title: str
    kind: str  # "doi", "documentcloud" or "doi+documentcloud"
    actions: dict[str, str] = field(default_factory=dict)
    new_url: str | None = None
    keep_url: tuple[str, str] | None = None  # (url, title) of the old url to attach
    attach_documentcloud: str | None = None  # url of the DocumentCloud link attachment to ensure
    documentcloud_id: str | None = None
    short_link_target: str | None = None  # DocumentCloud URL to add to links.json

    def summary(self) -> str:
        return f"{self.item_key}  {self.citekey}  [{self.kind}]  " + "; ".join(self.actions)


@dataclass
class Plan:
    items: list[ItemPlan] = field(default_factory=list)
    skipped: int = 0  # in Reports, but neither DOI nor DocumentCloud
    problems: list[str] = field(default_factory=list)  # items backfill will not touch, with the reason
    notes: list[str] = field(default_factory=list)

    def counts(self) -> Counter[str]:
        c: Counter[str] = Counter()
        for p in self.items:
            c.update(p.actions.keys())
        return c


def _children_by_parent(items: Iterable[Mapping[str, Any]]) -> dict[str, list[Mapping[str, Any]]]:
    out: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for it in items:
        if parent := it["data"].get("parentItem"):
            out[parent].append(it)
    return out


def _documentcloud_refs(data: Mapping[str, Any], kids: list[Mapping[str, Any]]) -> list[DocumentCloudRef]:
    """Distinct DocumentCloud documents the item links to: its ``url`` first, then its link attachments."""
    urls = [data.get("url")] + [
        k["data"].get("url") for k in kids if k["data"].get("linkMode") in LINK_MODES and not k["data"].get("deleted")
    ]
    refs: dict[str, DocumentCloudRef] = {}
    for url in urls:
        ref = parse_documentcloud(url)
        if ref and ref.doc_id not in refs:
            refs[ref.doc_id] = ref
    return list(refs.values())


def plan_item(
    item: Mapping[str, Any], kids: list[Mapping[str, Any]], links: Mapping[str, str], plan: Plan
) -> ItemPlan | None:
    """The plan for one top-level item, or ``None`` when there is nothing (or nothing safe) to do."""
    data = item["data"]
    label = f"{item['key']} {data.get('title', '')[:60]!r}"
    try:
        citekey = extra.get(data.get("extra"), extra.CITATION_KEY)
        known_id = extra.get(data.get("extra"), extra.DOCUMENTCLOUD_ID)
    except extra.ExtraError as e:
        plan.problems.append(f"{label}: {e}")
        return None
    doi = (data.get("DOI") or "").strip()
    refs = _documentcloud_refs(data, kids)
    if not doi and not refs:
        plan.skipped += 1
        return None
    if not citekey:
        plan.problems.append(f"{label}: no pinned citation key")
        return None
    if known_id and refs and not any(r.doc_id == known_id for r in refs):
        plan.problems.append(
            f"{citekey}: Extra records DocumentCloud ID {known_id} but the item links to other documents"
        )
        return None
    ref = next((r for r in refs if r.doc_id == known_id), None) or (refs[0] if refs else None)
    if len(refs) > 1 and ref:
        plan.notes.append(f"{citekey}: links to {len(refs)} DocumentCloud documents; using {ref.doc_id}")

    old_url = (data.get("url") or "").strip()
    kind = "doi+documentcloud" if doi and ref else "doi" if doi else "documentcloud"
    p = ItemPlan(item["key"], citekey, data.get("title", ""), kind)

    if doi:
        want_url = doi_link(doi)
    else:
        try:
            shortlinks.check_key(citekey)
        except shortlinks.ShortLinkError as e:
            plan.problems.append(f"{citekey}: {e}")
            return None
        want_url = f"{metadata.SHORT_LINK_BASE}/{citekey}"

    if ref and not doi:
        have = links.get(citekey)
        if have is None:
            p.short_link_target = ref.canonical
            p.actions[ADD_SHORT_LINK] = f"{citekey} -> {ref.canonical}"
        elif (mapped := parse_documentcloud(have)) is None or mapped.doc_id != ref.doc_id:
            plan.problems.append(f"{citekey}: pub already maps it to {have}, not {ref.canonical}; left alone")
            return None

    if old_url != want_url:
        p.new_url = want_url
        p.actions[SET_DOI_URL if doi else SET_SHORT_URL] = f"{old_url or '(empty)'} -> {want_url}"
        if old_url and not (
            doi and _same_doi_link(old_url, want_url)
        ):  # an http/dx variant of the DOI link adds nothing
            old_ref = parse_documentcloud(old_url)
            p.keep_url = (old_url, DOCUMENTCLOUD_TITLE if old_ref else ORIGINAL_TITLE)
            if not _has_link(kids, old_url):
                p.actions[KEEP_OLD_URL] = old_url

    if ref:
        p.documentcloud_id = ref.doc_id
        # A public-page link to the document (an attachment, or the old url kept above) already serves as the copy.
        old = parse_documentcloud(old_url)
        covered = bool(old and old.doc_id == ref.doc_id and old.public_page and p.keep_url) or any(
            (r := parse_documentcloud(k["data"].get("url"))) and r.doc_id == ref.doc_id and r.public_page
            for k in kids
            if k["data"].get("linkMode") == "linked_url"
        )
        if not covered:
            p.attach_documentcloud = ref.canonical
            p.actions[ATTACH_DOCUMENTCLOUD] = ref.canonical
        if known_id != ref.doc_id:
            p.actions[WRITE_DOCUMENTCLOUD_ID] = ref.doc_id
    return p if p.actions else None


def _same_doi_link(url: str, want: str) -> bool:
    """Whether ``url`` is the DOI link ``want`` up to scheme, ``dx.`` prefix and case."""

    def norm(u: str) -> str:
        return re.sub(r"^https?://(dx\.)?", "", u.strip(), flags=re.IGNORECASE).casefold()

    return norm(url) == norm(want)


def _has_link(kids: list[Mapping[str, Any]], url: str) -> bool:
    return any(k["data"].get("linkMode") == "linked_url" and k["data"].get("url") == url for k in kids)


def make_plan(items: Iterable[Mapping[str, Any]], reports_collections: set[str], links: Mapping[str, str]) -> Plan:
    """Plan every non-deleted, top-level bibliographic item under ``Reports`` (``items`` is the whole library)."""
    items = list(items)
    kids = _children_by_parent(items)
    plan = Plan()
    for item in sorted(items, key=lambda it: it["key"]):
        data = item["data"]
        if data["itemType"] in zotero.NON_BIB_TYPES or data.get("deleted") or data.get("parentItem"):
            continue
        if not reports_collections & set(data.get("collections") or []):
            continue
        if p := plan_item(item, kids.get(item["key"], []), links, plan):
            plan.items.append(p)
    return plan


def apply_plan(plan: Plan, batch: shortlinks.Batch | None) -> tuple[int, list[str]]:
    """Write the plan: publish the short links once, then each item's attachments, Extra and, last, ``url``.

    Returns ``(items_done, failures)``. An item that fails is reported and left for a rerun; the rest continue.
    """
    failures: list[str] = []
    todo = list(plan.items)
    if batch is not None:
        adds = [p for p in plan.items if p.short_link_target]
        for p in adds:
            assert p.short_link_target
            try:
                batch.add(p.citekey, p.short_link_target)
            except shortlinks.ShortLinkError as e:
                failures.append(f"{p.item_key} {p.citekey}: {e}")
                todo.remove(p)
        if batch.ops:
            batch.message = f"Add {len(batch.ops)} short links for existing DocumentCloud sources"
            batch.publish()
    done = 0
    for p in todo:
        try:
            if p.keep_url:
                zotero.attach_link(p.item_key, *p.keep_url)
            if p.attach_documentcloud:
                zotero.attach_link(p.item_key, p.attach_documentcloud, DOCUMENTCLOUD_TITLE)
            if p.documentcloud_id and WRITE_DOCUMENTCLOUD_ID in p.actions:
                zotero.set_extra_fields(p.item_key, {extra.DOCUMENTCLOUD_ID: p.documentcloud_id})
            if p.new_url:
                zotero.set_url(p.item_key, p.new_url)
            done += 1
        except Exception as e:  # keep going; the failing item is listed and a rerun picks it up
            failures.append(f"{p.item_key} {p.citekey}: {type(e).__name__}: {e}"[:300])
    return done, failures


def report(plan: Plan, apply: bool) -> str:
    """Counts per action, a few examples, and anything left alone."""
    lines = [
        f"{len(plan.items)} items {'changed' if apply else 'would change'}; {plan.skipped} skipped (no DOI, no DocumentCloud link)"
    ]
    kinds = Counter(p.kind for p in plan.items)
    lines.append("  by kind: " + (", ".join(f"{k} {n}" for k, n in sorted(kinds.items())) or "none"))
    counts = plan.counts()
    for name in ACTIONS:
        lines.append(f"  {name}: {counts.get(name, 0)}")
    if plan.items:
        lines.append(f"Examples (first {EXAMPLES}):")
        step = max(1, len(plan.items) // EXAMPLES)
        for p in plan.items[::step][:EXAMPLES]:
            lines.append("  " + p.summary())
            for name, detail in p.actions.items():
                lines.append(f"      {name}: {detail}")
    for note in plan.notes:
        lines.append(f"note: {note}")
    for problem in plan.problems:
        lines.append(f"left alone: {problem}")
    return "\n".join(lines)


def run(apply: bool = False) -> tuple[Plan, list[str]]:
    """Plan (and with ``apply``, write) the backfill for the whole library. Returns the plan and failures."""
    items = zotero.all_items(refresh=True)
    reports = set(zotero.collection_tree(zotero.REPORTS))
    repo = shortlinks.ensure_clone()
    links = shortlinks.load_links(repo)
    plan = make_plan(items, reports, links)
    if not apply or not plan.items:
        return plan, []
    _done, failures = apply_plan(plan, shortlinks.Batch(repo))
    return plan, failures
