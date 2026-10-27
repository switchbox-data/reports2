"""Command-line entry points for the bibliography tooling (run via the root Justfile).

    uv run python -m lib.sources.cli zotero-verify
    uv run python -m lib.sources.cli sync-bib [--checks warn|strict] [--force]
    uv run python -m lib.sources.cli check-citekeys
    uv run python -m lib.sources.cli orgs-snapshot [--path-work-dir DIR] [--no-s3]

None of these write to Zotero.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict
from datetime import date
from pathlib import Path

import yaml

from lib.sources import (
    bib,
    checks,
    citations,
    citekeys,
    cleanup,
    extra,
    item_fixes,
    org_apply,
    org_plan,
    org_proposals,
    orgs,
    render_diff,
    review_sheet,
    snapshot,
    zotero,
)

REPO_ROOT = zotero.REPO_ROOT
DEFAULT_REFERENCES = REPO_ROOT / "reports" / "references.yaml"
REPORTS_DIR = REPO_ROOT / "reports"
CONVENTIONS_DOC = REPO_ROOT / "context" / "code" / "source_metadata_conventions.md"
COLLECTION = "Reports"


def _bibliography_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    refs = yaml.load(path.read_text(encoding="utf-8"), Loader=bib._Loader).get("references") or []
    return {r["id"] for r in refs}


def _cited_keys(reports_dir: Path) -> dict[str, list[citations.Citation]]:
    cited: dict[str, list[citations.Citation]] = {}
    for path in citations.report_sources(reports_dir):
        for c in citations.find_citations(path.read_text(encoding="utf-8", errors="ignore"), path):
            cited.setdefault(c.key, []).append(c)
    return cited


def cmd_zotero_verify(_: argparse.Namespace) -> int:
    """Read-only checks of the API key, the Reports tree and the data shapes code relies on."""
    z = zotero.client()
    access = z.key_info().get("access", {})
    group_access = access.get("groups", {})
    print("Key access (groups):", group_access or "none")
    cols = zotero.collections()
    tree = zotero.collection_tree(COLLECTION, cols)
    top = sorted(c["data"]["name"] for c in cols if not c["data"]["parentCollection"])
    print(f"Library version {zotero.library_version()}; {len(cols)} collections; top level: {', '.join(top)}")
    items = zotero.items_in_collections(tree)
    bibl = zotero.bibliographic(items)
    print(f"{COLLECTION} (recursive): {len(tree)} collections, {len(items)} top-level items, {len(bibl)} bibliographic")
    print("  item types:", dict(Counter(i["data"]["itemType"] for i in bibl).most_common()))
    shapes = Counter("name" if "name" in c else "firstName/lastName" for i in bibl for c in i["data"]["creators"])
    print("  creator shapes:", dict(shapes))
    pinned = [i for i in bibl if bib.pinned_key(i["data"])]
    native = [i for i in bibl if i["data"].get("citationKey")]
    shorts = [i for i in bibl if extra.get(i["data"].get("extra"), extra.SHORTAUTHOR)]
    print(f"  keys: {len(pinned)} pinned in Extra, {len(native)} in Zotero's native citationKey field")
    print(f"  tex.shortauthor in Extra: {len(shorts)}")
    mismatched = [i for i in pinned if i["data"].get("citationKey") not in (None, "", bib.pinned_key(i["data"]))]
    for i in mismatched:
        print(f"  Extra pin {bib.pinned_key(i['data'])!r} != native {i['data']['citationKey']!r} ({i['key']})")
    if sample := next(iter(shorts), None):
        csl = sample["csljson"]
        print(f"  CSL-JSON keeps Extra in note: {'note' in csl}; has citation-key: {'citation-key' in csl}")
    result = bib.build_references(items, include_unpinned=True)
    for key, dates in result.literal_dates.items():
        print(f"  invalid date: {key} {dates}")
    return 0


def cmd_sync_bib(args: argparse.Namespace) -> int:
    """Regenerate references.yaml from Zotero."""
    path = Path(args.path_output)
    version = zotero.library_version()
    if not args.force and bib.header_version(path) == version:
        print(f"{path} is up to date with library version {version}.")
        return 0
    items = zotero.items_in_collections(zotero.collection_tree(COLLECTION))
    result = bib.build_references(items, include_unpinned=args.include_unpinned)
    data_by_key = {
        (bib.pinned_key(i["data"]) or i["data"].get("citationKey")): i["data"] for i in zotero.bibliographic(items)
    }
    findings = checks.run_checks(
        [(r["id"], data_by_key[r["id"]]) for r in result.records],
        unpinned=result.unpinned,
        literal_dates=result.literal_dates,
    )
    print(checks.summarize(findings) if args.verbose else "\n".join(checks.summarize(findings).splitlines()[:40]))
    print(f"\n{len(result.records)} entries; {len(result.unpinned)} items not yet processed (no pinned key).")
    errors = [f for f in findings if f.level == "error"]
    if args.checks == "strict" and errors:
        print(f"strict: {len(errors)} errors; not writing {path}. Fix the items in Zotero and rerun.")
        return 1
    new_ids = {r["id"] for r in result.records}
    dropped = sorted(k for k in _cited_keys(REPORTS_DIR) if k in _bibliography_ids(path) and k not in new_ids)
    if dropped and not args.force:
        print(f"Not writing {path}: {len(dropped)} cited keys would disappear: {', '.join(dropped[:10])}")
        print("Pin their keys in Zotero (or pass --force).")
        return 1
    bib.write_references_yaml(result, path, version, REPO_ROOT)
    print(f"Wrote {path} (library version {version}).")
    return 0


def cmd_check_citekeys(args: argparse.Namespace) -> int:
    """Every key cited in reports/**/*.qmd and *.md must exist in references.yaml."""
    ids = _bibliography_ids(Path(args.path_references))
    cited = _cited_keys(Path(args.path_reports))
    missing = {k: v for k, v in sorted(cited.items()) if k not in ids}
    for key, uses in missing.items():
        where = ", ".join(f"{c.path.relative_to(REPO_ROOT)}:{c.line}" for c in uses[:3])
        print(f"missing: @{key}  ({where}{', ...' if len(uses) > 3 else ''})")
    print(f"{len(cited)} cited keys, {len(cited) - len(missing)} resolve, {len(missing)} missing.")
    return 1 if missing else 0


def cmd_orgs_snapshot(args: argparse.Namespace) -> int:
    """Back up the whole library (local + S3) and write today's key map. Read-only."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    if args.path_snapshot:
        path = Path(args.path_snapshot)
        snap = snapshot.load(path)
    else:
        snap = snapshot.fetch()
        path = snapshot.write(snap, work_dir)
    s = snapshot.summarize(snap)
    print(f"Snapshot: Switchbox group library version {s.library_version}")
    print(f"  bibliographic items (excluding notes, attachments, trash): {s.bibliographic}")
    sc = s.scope_counts
    print(
        f"    in Reports (recursive): {sc['reports'] + sc['both']}   in Inbox: {sc['inbox'] + sc['both']}"
        f"   in both: {sc['both']}   in neither: {sc['neither']}"
    )
    print(f"  attachments and notes: {s.children}   in trash: {s.trashed}")
    print(f"  wrote {path} ({path.stat().st_size / 1e6:.1f} MB)")
    if args.no_s3 or args.path_snapshot:
        print("  S3 copy skipped")
    else:
        uri = snapshot.s3_uri(snap)
        snapshot.upload(path, uri)
        print(f"  copied to {uri}")
    cited = _cited_keys(REPORTS_DIR)
    rows = snapshot.key_map(s, cited)
    (work_dir / "key_map.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    ks = s.key_sources
    print(f"Current keys (Reports and Inbox): {len(rows)} items")
    print(f"  pinned in Extra: {ks['extra']}   native field only: {ks['native']}   no key: {ks['none']}")
    print(f"  cited in reports: {sum(bool(r['cited']) for r in rows)} items; ", end="")
    mapped = {k for r in rows for k in r["old_keys"]}
    unresolved = sorted(k for k in cited if k not in mapped)
    print(f"cited keys with no item: {len(unresolved)} ({', '.join(unresolved)})")
    for key, items in s.duplicate_keys.items():
        print(f"  duplicate key: {key} -> {len(items)} items ({', '.join(items)})")
    for item, pin, native in s.pin_differs:
        print(f"  Extra pin differs from native key: {item} {pin!r} vs {native!r}")
    if s.empty:
        print(f"  empty items (no title, creator or date): {', '.join(f'{r.item} ({r.key})' for r in s.empty)}")
    print(f"  wrote {work_dir / 'key_map.json'}")
    return 0


def cmd_orgs_extract(args: argparse.Namespace) -> int:
    """Extract organization names from the latest snapshot, link candidates, and batch them. Read-only."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    snaps = sorted(work_dir.glob("snapshot_v*.json"), key=lambda p: int(p.stem.removeprefix("snapshot_v")))
    if not snaps:
        print(f"No snapshot in {work_dir}; run just orgs-snapshot first.")
        return 1
    snap = snapshot.load(snaps[-1])
    cite_counts = {k: len(v) for k, v in _cited_keys(REPORTS_DIR).items()}
    mentions = orgs.extract(snap, cite_counts)
    groups = orgs.group_mentions(mentions)
    edges = orgs.candidate_edges(groups, mentions)
    comps = orgs.components(groups, edges)
    packed = orgs.batches(comps, args.batch_size)
    by_id = {g.id: g for g in groups}
    out = work_dir / "extract"
    (out / "batches").mkdir(parents=True, exist_ok=True)
    for old in (out / "batches").glob("batch_*.json"):
        old.unlink()
    with (out / "mentions.jsonl").open("w", encoding="utf-8") as f:
        for m in mentions:
            f.write(json.dumps(orgs.mention_dict(m), ensure_ascii=False) + "\n")
    (out / "groups.json").write_text(
        json.dumps([g.as_dict() for g in groups], ensure_ascii=False, indent=1), encoding="utf-8"
    )
    (out / "edges.json").write_text(
        json.dumps([e.__dict__ for e in edges], ensure_ascii=False, indent=1), encoding="utf-8"
    )
    with (out / "groups_index.tsv").open("w", encoding="utf-8") as f:
        batch_of = {g: f"B{i:02d}" for i, b in enumerate(packed, 1) for g in b}
        f.write("group\tbatch\tn_items\tvariants\troles\n")
        for g in groups:
            variants = " | ".join(v for v, _ in g.variants.most_common(4))
            roles = ",".join(r for r, _ in g.roles.most_common(3))
            f.write(f"{g.id}\t{batch_of[g.id]}\t{len(g.items)}\t{variants}\t{roles}\n")
    for i, batch in enumerate(packed, 1):
        payload = orgs.batch_payload(batch, by_id, mentions, edges, snap)
        payload["batch"] = f"B{i:02d}"
        (out / "batches" / f"batch_{i:02d}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
        )
    kinds = Counter(m.kind for m in mentions)
    print(f"Snapshot {snaps[-1].name}: {len(mentions)} name strings on Reports and Inbox items")
    print(f"  organization: {kinds['org']}   person: {kinds['person']}   ambiguous: {kinds['ambiguous']}")
    print(f"  distinct organization names (after normalizing): {len(groups)}")
    print(f"  candidate links: {len(edges)} ({dict(Counter(e.reason for e in edges).most_common())})")
    print(f"  linked sets: {len(comps)} ({sum(len(c) > 1 for c in comps)} with more than one name)")
    print(f"  agent batches: {len(packed)} in {out / 'batches'}")
    return 0


def cmd_orgs_evidence(args: argparse.Namespace) -> int:
    """Print an item's metadata and the opening of its documents' text, for checking names. Read-only."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    snaps = sorted(work_dir.glob("snapshot_v*.json"), key=lambda p: int(p.stem.removeprefix("snapshot_v")))
    snap = snapshot.load(snaps[-1])
    by_key = {it["key"]: it for it in snap["items"]}
    z = zotero.client()
    for item_key in args.items:
        it = by_key.get(item_key)
        if it is None:
            print(f"== {item_key}: not in the snapshot\n")
            continue
        d = it["data"]
        print(f"== {item_key}  {d['itemType']}  key={snapshot.current_key(d)[0]}")
        for f in ("title", "date", "url", "extra", *orgs.ORG_FIELDS):
            if d.get(f):
                print(f"  {f}: {d[f]}")
        for c in d.get("creators", []):
            print(f"  creator ({c.get('creatorType')}): {c}")
        kids = [k for k in snap["items"] if k["data"].get("parentItem") == item_key]
        for k in kids:
            kd = k["data"]
            if kd["itemType"] == "note":
                print(f"  note: {kd.get('note', '')[:300]!r}")
                continue
            print(
                f"  attachment {k['key']}: {kd.get('title')} ({kd.get('contentType')}, {kd.get('linkMode')}) {kd.get('url', '')}"
            )
            try:
                ft = z.fulltext_item(k["key"])
            except Exception:  # no indexed text for this attachment
                continue
            text = " ".join(ft.get("content", "").split())
            print(
                f"  --- text ({ft.get('indexedPages') or ft.get('indexedChars')} indexed) ---\n  {text[: args.chars]}"
            )
        print()
    return 0


def cmd_orgs_proposals(args: argparse.Namespace) -> int:
    """Validate the reconcile-orgs proposal files and merge them into clusters. Read-only."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    extract_dir = work_dir / "extract"
    expected = {}
    for p in sorted((extract_dir / "batches").glob("batch_*.json")):
        b = json.loads(p.read_text(encoding="utf-8"))
        expected[b["batch"]] = {g["id"] for g in b["groups"]}
    paths = sorted((work_dir / "proposals").glob("batch_*.json"))
    if args.batch:
        paths = [p for p in paths if p.stem == f"batch_{int(args.batch):02d}"]
        expected = {k: v for k, v in expected.items() if k == f"B{int(args.batch):02d}"}
    proposals, problems = org_proposals.load_batches(paths)
    merged, merge_problems = org_proposals.merge(proposals, expected)
    problems += merge_problems
    found = org_proposals.conflicts(merged)
    if not args.batch:
        (work_dir / "clusters.json").write_text(
            json.dumps([m.model_dump() for m in merged], ensure_ascii=False, indent=1), encoding="utf-8"
        )
        (work_dir / "conflicts.json").write_text(
            json.dumps([c.model_dump() for c in found], ensure_ascii=False, indent=1), encoding="utf-8"
        )
    kinds = Counter("split" if m.split_into else m.proposals[0].kind for m in merged)
    conf = Counter(p.confidence for m in merged for p in m.proposals[:1])
    print(f"{len(paths)} proposal files, {len(merged)} clusters ({dict(kinds)}); confidence {dict(conf)}")
    print(f"  needs your decision: {sum(any(p.needs_decision for p in m.proposals) for m in merged)}")
    for c in found:
        print(f"  for the review sheet: {c.cluster} {c.field}: {' | '.join(c.options)}")
    for msg in problems:
        print(f"  problem: {msg}")
    print("OK" if not problems else f"{len(problems)} problems")
    return 1 if problems else 0


def cmd_orgs_plan(args: argparse.Namespace) -> int:
    """Apply the merged clusters to every in-scope item and compute keys from scratch. Read-only."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    snaps = sorted(work_dir.glob("snapshot_v*.json"), key=lambda p: int(p.stem.removeprefix("snapshot_v")))
    snap = snapshot.load(snaps[-1])
    extract_dir = work_dir / "extract"
    mentions = [json.loads(line) for line in (extract_dir / "mentions.jsonl").open(encoding="utf-8")]
    groups = json.loads((extract_dir / "groups.json").read_text(encoding="utf-8"))
    merged = [
        org_proposals.MergedCluster.model_validate(m)
        for m in json.loads((work_dir / "clusters.json").read_text(encoding="utf-8"))
    ]
    key_rows = json.loads((work_dir / "key_map.json").read_text(encoding="utf-8"))
    path_decisions = work_dir / "decisions.json"
    decisions = json.loads(path_decisions.read_text(encoding="utf-8")) if path_decisions.exists() else {}
    rulings = review_sheet.load_json(work_dir / "rulings.json", {})
    decisions = {**rulings.get("clusters", {}), **decisions}
    fixes_dir = work_dir / "item_fixes"
    fixes, _ = item_fixes.load(fixes_dir.glob("batch_*.json"), {})
    today = date.today()
    plans = org_plan.build(
        snap,
        mentions,
        groups,
        merged,
        key_rows,
        decisions,
        fixes,
        (today.year, today.month, today.day),
        rulings.get("items", {}),
        rulings.get("not_people", []),
        {
            d["item"]: d
            for path in sorted((work_dir / "docket_titles").glob("batch_*.json"))
            for d in json.loads(path.read_text(encoding="utf-8"))["items"]
        },
        {
            **org_plan.table_short_forms(CONVENTIONS_DOC.read_text(encoding="utf-8")),
            **rulings.get("short_forms", {}),
            **review_sheet.load_json(work_dir / "answers.json", {}).get("short_forms", {}),
        },
    )
    (work_dir / "plan.json").write_text(
        json.dumps([asdict(p) for p in plans], ensure_ascii=False, indent=1), encoding="utf-8"
    )
    changed = sum(bool(p.changes) for p in plans)
    keyed = [p for p in plans if p.key]
    same = sum(p.key in p.old_keys for p in keyed)
    print(f"{len(plans)} items: {changed} with metadata changes, {sum(bool(p.flags) for p in plans)} flagged")
    print(
        f"  keys: {len(keyed)} assigned ({same} unchanged, {len(keyed) - same} new); "
        f"{sum(p.action != 'update' for p in plans)} to the trash; "
        f"{sum(p.action == 'update' and not p.key for p in plans)} still need an author"
    )
    cited_changed = sum(1 for p in keyed if p.cited and p.key not in p.old_keys)
    print(f"  cited items whose key changes: {cited_changed}")
    print(f"  wrote {work_dir / 'plan.json'}")
    return 0


def cmd_orgs_dry_run(args: argparse.Namespace) -> int:
    """Render every report's citations before and after the plan, and write the differences. Read-only."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    snaps = sorted(work_dir.glob("snapshot_v*.json"), key=lambda p: int(p.stem.removeprefix("snapshot_v")))
    snap = snapshot.load(snaps[-1])
    plans = {p["item"]: p for p in json.loads((work_dir / "plan.json").read_text(encoding="utf-8"))}
    items = [it for it in snap["items"] if it["key"] in plans]
    after_items = []
    for it in items:
        p = plans[it["key"]]
        if (data := org_apply.target_data(p)) is not None:
            csl = org_apply.preview_csl(it["csljson"], p["before"], p["after"])
            after_items.append({**it, "data": data, "csljson": csl})
    out_dir = work_dir / "dry_run"
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, its, unpinned in (("before", items, True), ("after", after_items, False)):
        paths[name] = out_dir / f"references_{name}.yaml"
        result = bib.build_references(its, include_unpinned=unpinned)
        paths[name].write_text(bib.to_yaml(result, snap["library_version"]), encoding="utf-8")
    renames = {}
    for p in plans.values():
        key = p["key"] if p["action"] == "update" else (plans.get(p["duplicate_of"] or "") or {}).get("key")
        for old in p["old_keys"]:
            if key and old != key:
                renames[old] = key
    csl_path = REPORTS_DIR / "chicago-author-date-switchbox.csl"
    rows = []
    for report in sorted(d for d in REPORTS_DIR.iterdir() if d.is_dir() and d.name != "templates"):
        keys = sorted(_cited_keys(report))
        if not keys:
            continue
        diff = render_diff.compare(keys, (paths["before"], csl_path), (paths["after"], csl_path), renames)
        rows += [{"report": report.name, **r} for r in diff]
        print(
            f"{report.name}: {len(diff)} cited, "
            f"{sum(r['in_text_before'] != r['in_text_after'] for r in diff)} in-text changes, "
            f"{sum(r['bibliography_before'] != r['bibliography_after'] for r in diff)} bibliography changes, "
            f"{sum(r['in_text_after'] == '(missing)' for r in diff)} missing after "
            f"({sum(r['in_text_before'] == '(missing)' for r in diff)} missing before)"
        )
    render_diff.write_csv(rows, out_dir / "render_diff.csv")
    print(f"wrote {out_dir / 'render_diff.csv'}")
    return 0


def _needs_fix(p: dict) -> list[str]:
    """What an item in plan.json still lacks: author, date or a real title."""
    after = p["after"]
    title = citekeys.item_title(after) or ""
    out = []
    if not p["key"]:
        out.append("author")
    if citekeys.parse_date(citekeys.item_date(after)) is None:
        out.append("date")
    if not title.strip() or org_plan.looks_like_filename(title):
        out.append("title")
    return out


def cmd_orgs_fix_batches(args: argparse.Namespace) -> int:
    """Write input batches for the second agent pass (authors, dates, titles). Read-only."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    plans = json.loads((work_dir / "plan.json").read_text(encoding="utf-8"))
    merged = json.loads((work_dir / "clusters.json").read_text(encoding="utf-8"))
    names = sorted(
        {
            (p["canonical_full_name"], p["short_form"] or "")
            for m in merged
            for p in m["proposals"][:1]
            if p["canonical_full_name"] and not m["split_into"]
        }
    )
    todo = [(p, need) for p in plans if (need := _needs_fix(p))]
    out = work_dir / "item_fixes" / "inputs"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("batch_*.json"):
        old.unlink()
    n = 0
    for i in range(0, len(todo), args.batch_size):
        n += 1
        chunk = todo[i : i + args.batch_size]
        payload = {
            "batch": f"F{n:02d}",
            "organizations": [{"full_name": f, "short_form": s} for f, s in names],
            "items": [
                {
                    "item": p["item"],
                    "needs": need,
                    "cited_as": p["cited"],
                    "item_type": p["item_type"],
                    "current": {
                        k: v for k, v in p["after"].items() if v and k not in ("relations", "collections", "tags")
                    },
                }
                for p, need in chunk
            ],
        }
        (out / f"batch_{n:02d}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(todo)} items need an author, date or title: {dict(Counter(x for _, need in todo for x in need))}")
    print(f"  {n} batches in {out}")
    return 0


def cmd_orgs_fixes(args: argparse.Namespace) -> int:
    """Validate the second agent pass's fix files. Read-only."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    fixes_dir = work_dir / "item_fixes"
    expected = {}
    for p in sorted((fixes_dir / "inputs").glob("batch_*.json")):
        b = json.loads(p.read_text(encoding="utf-8"))
        expected[b["batch"]] = {it["item"] for it in b["items"]}
    paths = sorted(fixes_dir.glob("batch_*.json"))
    if args.batch:
        paths = [p for p in paths if p.stem == f"batch_{int(args.batch):02d}"]
        expected = {k: v for k, v in expected.items() if k == f"F{int(args.batch):02d}"}
    fixes, problems = item_fixes.load(paths, expected)
    print(f"{len(paths)} fix files, {len(fixes)} items: {dict(Counter(f.action for f in fixes.values()))}")
    print(f"  confidence {dict(Counter(f.confidence for f in fixes.values()))}")
    for msg in problems:
        print(f"  problem: {msg}")
    print("OK" if not problems else f"{len(problems)} problems")
    return 1 if problems else 0


def cmd_orgs_sheet_push(args: argparse.Namespace) -> int:
    """Build the review tabs, save CSV copies and create or refresh the Google Sheet. No Zotero access."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    rd = review_sheet.load_json
    snaps = sorted(work_dir.glob("snapshot_v*.json"), key=lambda p: int(p.stem.removeprefix("snapshot_v")))
    snap = snapshot.load(snaps[-1])
    plans = rd(work_dir / "plan.json", [])
    known = {k for p in plans for k in p["old_keys"]} | {p["key"] for p in plans if p.get("key")}
    unresolved = [k for k in _cited_keys(REPORTS_DIR) if k not in known]
    actions = cleanup.actions(snap, plans, unresolved, snapshot.summarize(snap))
    (work_dir / "cleanup.json").write_text(json.dumps(actions, ensure_ascii=False, indent=1), encoding="utf-8")
    tabs = review_sheet.build_tabs(
        plans=plans,
        merged=rd(work_dir / "clusters.json", []),
        groups=rd(work_dir / "extract" / "groups.json", []),
        conflicts=rd(work_dir / "conflicts.json", []),
        questions=rd(work_dir / "questions.json", []),
        cleanup=actions,
    )
    path_meta = work_dir / "review_sheet.json"
    meta = rd(path_meta, {})
    if meta.get("spreadsheet_id") and not args.csv_only:
        tabs = review_sheet.carry_answers(tabs, review_sheet.pull(meta["spreadsheet_id"]))
    tabs = review_sheet.carry_answers(
        tabs,
        review_sheet.answers_as_tabs(rd(work_dir / "decisions.json", {}), rd(work_dir / "answers.json", {})),
    )
    review_sheet.write_csvs(tabs, work_dir / "review_csv")
    if args.csv_only:
        print(f"wrote {work_dir / 'review_csv'}")
        return 0
    url = review_sheet.push(tabs, args.title, meta.get("spreadsheet_id"))
    meta = {"spreadsheet_id": url.rstrip("/").split("/d/")[1].split("/")[0], "url": url}
    path_meta.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    for name, rows in tabs.items():
        print(f"  {name}: {len(rows) - 1} rows")
    print(f"Review sheet: {url}")
    return 0


def cmd_orgs_sheet_pull(args: argparse.Namespace) -> int:
    """Read the reviewer's answers into decisions.json and answers.json. No Zotero access."""
    work_dir = Path(args.path_work_dir) if args.path_work_dir else snapshot.default_work_dir()
    meta = review_sheet.load_json(work_dir / "review_sheet.json", {})
    if not meta:
        print("no review sheet yet; run orgs-sheet-push first")
        return 1
    tabs = review_sheet.pull(meta["spreadsheet_id"])
    decisions, other = review_sheet.answers_from(tabs)
    previous = review_sheet.load_json(work_dir / "answers.json", {})
    for section in ("short_forms", "long_key_comments"):
        other[section] = {**previous.get(section, {}), **other[section]}
    (work_dir / "decisions.json").write_text(json.dumps(decisions, ensure_ascii=False, indent=1), encoding="utf-8")
    (work_dir / "answers.json").write_text(json.dumps(other, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(decisions)} cluster decisions, {len(other['items'])} item verdicts, ", end="")
    print(f"{len(other['questions'])} question answers, {len(other['cleanup'])} cleanup answers")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lib.sources.cli", description=(__doc__ or "").split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("zotero-verify", help="read-only Zotero API checks").set_defaults(func=cmd_zotero_verify)
    p = sub.add_parser("sync-bib", help="regenerate reports/references.yaml from Zotero")
    p.add_argument("--path-output", default=str(DEFAULT_REFERENCES))
    p.add_argument("--checks", choices=("warn", "strict"), default="warn")
    p.add_argument("--force", action="store_true", help="regenerate even if up to date; allow dropping cited keys")
    p.add_argument(
        "--include-unpinned",
        action="store_true",
        help="pre-cleanup only: also include items without a pinned key, using Zotero's native citationKey",
    )
    p.add_argument("--verbose", action="store_true", help="print every finding")
    p.set_defaults(func=cmd_sync_bib)
    p = sub.add_parser("check-citekeys", help="confirm every cited key exists in references.yaml")
    p.add_argument("--path-references", default=str(DEFAULT_REFERENCES))
    p.add_argument("--path-reports", default=str(REPORTS_DIR))
    p.set_defaults(func=cmd_check_citekeys)
    p = sub.add_parser("orgs-snapshot", help="back up the whole Zotero library and write today's key map")
    p.add_argument("--path-work-dir", default="", help="default: ~/.cache/switchbox_sources/org_cleanup/<date>")
    p.add_argument("--no-s3", action="store_true", help="skip the S3 copy")
    p.add_argument("--path-snapshot", default="", help="summarize an existing snapshot instead of fetching")
    p.set_defaults(func=cmd_orgs_snapshot)
    p = sub.add_parser("orgs-extract", help="extract organization names from the snapshot and batch them")
    p.add_argument("--path-work-dir", default="", help="default: ~/.cache/switchbox_sources/org_cleanup/<date>")
    p.add_argument("--batch-size", type=int, default=25)
    p.set_defaults(func=cmd_orgs_extract)
    p = sub.add_parser("orgs-evidence", help="print items' metadata and the opening of their documents' text")
    p.add_argument("items", nargs="+", help="Zotero item keys")
    p.add_argument("--chars", type=int, default=2500)
    p.add_argument("--path-work-dir", default="")
    p.set_defaults(func=cmd_orgs_evidence)
    p = sub.add_parser("orgs-proposals", help="validate reconcile-orgs proposals and merge them into clusters")
    p.add_argument("--batch", default="", help="validate one batch only (e.g. 3)")
    p.add_argument("--path-work-dir", default="")
    p.set_defaults(func=cmd_orgs_proposals)
    p = sub.add_parser("orgs-plan", help="apply clusters to every item and compute citation keys from scratch")
    p.add_argument("--path-work-dir", default="")
    p.set_defaults(func=cmd_orgs_plan)
    p = sub.add_parser("orgs-dry-run", help="render every report's citations before and after the plan")
    p.add_argument("--path-work-dir", default="")
    p.set_defaults(func=cmd_orgs_dry_run)
    p = sub.add_parser("orgs-fix-batches", help="write batches of items that still need an author, date or title")
    p.add_argument("--batch-size", type=int, default=23)
    p.add_argument("--path-work-dir", default="")
    p.set_defaults(func=cmd_orgs_fix_batches)
    p = sub.add_parser("orgs-fixes", help="validate the author/date/title agent pass")
    p.add_argument("--batch", default="")
    p.add_argument("--path-work-dir", default="")
    p.set_defaults(func=cmd_orgs_fixes)
    p = sub.add_parser("orgs-sheet-push", help="create or refresh the cleanup review Google Sheet")
    p.add_argument("--title", default="Zotero cleanup review")
    p.add_argument("--csv-only", action="store_true", help="only write the CSV copies")
    p.add_argument("--path-work-dir", default="")
    p.set_defaults(func=cmd_orgs_sheet_push)
    p = sub.add_parser("orgs-sheet-pull", help="read the reviewer's answers from the review sheet")
    p.add_argument("--path-work-dir", default="")
    p.set_defaults(func=cmd_orgs_sheet_pull)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
