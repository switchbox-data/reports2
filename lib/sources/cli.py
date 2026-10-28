"""Command-line entry points for the bibliography and source-ingest tooling (run via the root Justfile).

Read-only (never write to Zotero or any public host):

    zotero-verify, sync-bib [--checks warn|strict] [--force], check-citekeys,
    pending [--brief], status, dedupe, org, doctor (read-only checks), fetch, projects, key,
    check-card, find-doi, draft-cards, convert-frontmatter (dry run unless --apply)

Writing (after the person approves the details card):

    ingest CARD... [--zotero-item KEY] [--extract] [--no-publish]

``ingest`` prints one JSON object per document, so an agent formats the report instead of reconstructing links.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

from lib.sources import bib, checks, citations, env, extra, zotero

REPO_ROOT = env.REPO_ROOT
DEFAULT_REFERENCES = env.REFERENCES_YAML
REPORTS_DIR = env.REPORTS_DIR
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
    result = bib.build_references(items)
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
    result = bib.build_references(items)
    data_by_key = {bib.pinned_key(i["data"]): i["data"] for i in zotero.bibliographic(items)}
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
    cited = _cited_keys(Path(args.path_reports).resolve())
    missing = {k: v for k, v in sorted(cited.items()) if k not in ids}
    for key, uses in missing.items():
        where = ", ".join(f"{c.path.relative_to(REPO_ROOT)}:{c.line}" for c in uses[:3])
        print(f"missing: @{key}  ({where}{', ...' if len(uses) > 3 else ''})")
    print(f"{len(cited)} cited keys, {len(cited) - len(missing)} resolve, {len(missing)} missing.")
    return 1 if missing else 0


# --- source ingest ------------------------------------------------------------------------------


def _out(text: str = "") -> None:
    print(text)


def _find_source(card, args: argparse.Namespace, provenance) -> Path | None:
    """The original file for a card: ``--path-source``, the provenance CSV, or ``--path-source-dir/<source_file>``."""
    from lib.sources import migrate

    if args.path_source and len(args.path_cards) == 1:
        return Path(args.path_source)
    if provenance is not None and card.extract_path:
        row = migrate.source_for_extract(provenance, card.extract_path)
        if row and Path(row["src"]).exists():
            return Path(row["src"])
    if args.path_source_dir and card.source_file:
        hits = sorted(Path(args.path_source_dir).rglob(card.source_file))
        if hits:
            return hits[0]
    return None


def cmd_ingest(args: argparse.Namespace) -> int:
    """Ingest approved cards: Zotero item and files, public copies, short links, front matter, indexes."""
    from lib.sources import ingest, metadata, migrate

    provenance = migrate.read_provenance(Path(args.path_provenance_csv)) if args.path_provenance_csv else None
    if args.zotero_item and len(args.path_cards) != 1:
        print("--zotero-item applies to exactly one card.", file=sys.stderr)
        return 2
    entries = []
    for path in args.path_cards:
        try:
            card = metadata.load(Path(path))
        except Exception as e:
            print(f"{path}: {e}", file=sys.stderr)
            return 2
        extract = None
        if args.extract:
            if not card.extract_path or not (REPO_ROOT / card.extract_path).exists():
                print(
                    f"{path}: --extract needs an existing extract at extract_path ({card.extract_path})",
                    file=sys.stderr,
                )
                return 2
            extract = REPO_ROOT / card.extract_path
        entries.append((card, _find_source(card, args, provenance), args.zotero_item, extract))
    reports = ingest.ingest_batch(entries, force=args.force, publish=not args.no_publish)
    for report in reports:
        _out(json.dumps(report.to_dict()))
        marks = {"done": "+", "already": "=", "skipped": "-", "pending": "~", "failed": "!"}
        for step in report.steps:
            print(
                f"  {marks.get(step.status, '?')} {report.citekey}: {step.name} {step.status} {step.detail}",
                file=sys.stderr,
            )
        if not report.ok:
            print(f"  rerun: just sources-ingest {path_for(args, report.citekey)}", file=sys.stderr)
    return 0 if all(r.ok for r in reports) else 1


def path_for(args: argparse.Namespace, citekey: str) -> str:
    return next((p for p in args.path_cards if Path(p).stem == citekey), " ".join(args.path_cards))


def cmd_check_card(args: argparse.Namespace) -> int:
    """Validate a drafted card against the conventions and the library (no writes)."""
    from lib.sources import metadata

    try:
        card = metadata.load(Path(args.path_card))
    except Exception as e:
        print(f"invalid card: {e}")
        return 1
    taken = zotero.pinned_keys()
    if args.zotero_item and taken.get(card.citekey) == args.zotero_item:
        taken.pop(card.citekey)  # the item being adopted may already carry the key
    problems = card.problems(set(taken))
    for p in problems:
        print(f"- {p}")
    print("card is valid" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


def cmd_key(args: argparse.Namespace) -> int:
    """The citation key the rule gives a draft card (``citekey`` may be empty or missing in the YAML)."""
    from lib.sources import citekeys, metadata

    raw = yaml.safe_load(Path(args.path_card).read_text(encoding="utf-8"))
    card = metadata.SourceMetadata.model_validate({**raw, "citekey": raw.get("citekey") or "placeholder"})
    print(citekeys.propose_key(card.zotero_data(), set(zotero.pinned_keys())))
    return 0


def cmd_fetch(args: argparse.Namespace) -> int:
    """Download a source's original file from Zotero next to its extract; print the path."""
    from lib.sources import frontmatter

    item_key = zotero.pinned_keys().get(args.citekey)
    if item_key is None:
        print(f"No Zotero item has the pinned key {args.citekey}.", file=sys.stderr)
        return 1
    extract = frontmatter.find_by_citekey(args.citekey)
    if args.path_output_dir:
        out_dir = Path(args.path_output_dir)
    elif extract:
        out_dir = extract.parent
    else:
        out_dir = env.cache_dir() / "fetched" / args.citekey
    wanted = frontmatter.read(extract).get("md5") if extract else None
    if wanted:
        for existing in out_dir.glob("*"):
            if existing.is_file() and existing.suffix != ".md" and zotero.file_md5(existing) == wanted:
                print(existing.resolve())
                return 0
    path = zotero.download_attachment(item_key, out_dir)
    print(path.resolve())
    return 0


def cmd_pending(args: argparse.Namespace) -> int:
    """Zotero items waiting for ingest. ``--brief`` is the session-start hook's one-liner and never fails."""
    try:
        items = zotero.pending_items()
    except Exception as e:
        if args.brief or args.hook:
            return 0  # missing credentials or no network: say nothing
        print(f"Could not read Zotero: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    if args.brief or args.hook:
        if items:
            shown = "; ".join(f"{i.author[:40]} {i.year}" for i in items[:4])
            more = f" (+{len(items) - 4} more)" if len(items) > 4 else ""
            line = f"{len(items)} source(s) in Zotero waiting for ingest: {shown}{more}"
            if args.hook:
                note = f"{line}. Open your first reply with a one-line list of these and offer to process them with the ingest-source skill."
                print(json.dumps({"additional_context": note}))
            else:
                print(line)
        return 0
    if not items:
        print("Nothing is waiting for ingest.")
        return 0
    for i in items:
        print(f"{i.key}  {i.label():45.45}  {i.reason:20}  {i.title[:70]}")
    return 0


def cmd_dedupe(args: argparse.Namespace) -> int:
    """Where a file, URL, DOI or title already appears in the repo or the library."""
    from lib.sources import dedupe

    if not any((args.path_file, args.url, args.doi, args.title)):
        print("Give --path-file, --url, --doi or --title.", file=sys.stderr)
        return 2
    prov = Path(args.path_provenance_csv) if args.path_provenance_csv else None
    matches = dedupe.check(
        Path(args.path_file) if args.path_file else None,
        args.url,
        args.doi,
        args.title,
        provenance_csv=prov,
        use_zotero=not args.no_zotero,
    )
    print(dedupe.summarize(matches))
    return 0


def cmd_org(args: argparse.Namespace) -> int:
    """Existing spellings and short forms of an organization."""
    from lib.sources import organizations

    items = None if args.no_zotero else zotero.bib_items()
    print(organizations.describe(organizations.find_organization(args.name, items=items)))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Per-step checklist for each citation key, or for every row of a provenance CSV."""
    from lib.sources import frontmatter, migrate, status

    keys = list(args.citekeys)
    if args.path_provenance_csv:
        for row in migrate.read_provenance(Path(args.path_provenance_csv)).iter_rows(named=True):
            md = REPO_ROOT / row["md_path"]
            stub = md.with_suffix(".md") if md.suffix != ".md" else md
            key = frontmatter.read(stub).get("citekey") if stub.exists() else None
            if key:
                keys.append(str(key))
            else:
                print(f"[FAIL] row {row['n']}: no citekey in front matter of {stub.name}")
                keys.append("")
    bad = 0
    for key in [k for k in keys if k] or []:
        checks_ = status.source_status(key)
        print(f"== {key}")
        for c in checks_:
            print("  " + c.line().replace("\n", "\n  "))
        bad += not status.all_green(checks_)
    return 1 if bad or "" in keys else 0


def cmd_doctor(_: argparse.Namespace) -> int:
    from lib.sources import doctor

    results = doctor.run_all()
    for r in results:
        print(r.line())
    failed = [r for r in results if r.level == doctor.FAIL]
    print(
        f"\n{len(results) - len(failed)} of {len(results)} checks passed"
        + (f"; {len(failed)} failed" if failed else "")
    )
    return 1 if failed else 0


def cmd_projects(_: argparse.Namespace) -> int:
    """Projects (report folders, Zotero subcollections and source folders), and where each exists."""
    from lib.sources import projects

    try:
        names = list(zotero.project_collections())
    except Exception:
        names = None
    for p in projects.list_projects(zotero_projects=names):
        where = ", ".join(
            label
            for label, present in (
                ("report", p.report_folder),
                ("zotero", p.zotero_collection),
                ("sources", p.source_folder),
            )
            if present
        )
        print(f"{p.name}\t{where}{'\t(planned)' if p.planned else ''}")
    return 0


def cmd_find_doi(args: argparse.Namespace) -> int:
    from lib.sources import doi

    result = doi.find_doi(
        args.title, Path(args.path_file) if args.path_file else None, args.url, args.zotero_doi, args.author
    )
    if result is None:
        print("no DOI found")
        return 1
    print(f"{result.doi}\t{result.source}\t{'verified at Crossref' if result.verified else 'NOT verified'}")
    return 0


def cmd_draft_cards(args: argparse.Namespace) -> int:
    """Pre-fill draft cards from the staging provenance CSV (creators, key and index row are left to fill in)."""
    from lib.sources import migrate

    paths = migrate.draft_cards(migrate.read_provenance(Path(args.path_provenance_csv)), Path(args.path_output_dir))
    print(f"Wrote {len(paths)} draft cards to {args.path_output_dir}")
    return 0


def cmd_convert_frontmatter(args: argparse.Namespace) -> int:
    """Legacy front matter to the flat schema; MANIFEST.csv folders too. Dry run unless ``--apply``."""
    from lib.sources import migrate

    root = Path(args.path_root) if args.path_root else None
    changes = migrate.convert_frontmatter(root, dry_run=not args.apply)
    for folder in migrate.manifest_folders(root):
        changes += migrate.convert_manifest_folder(folder, dry_run=not args.apply)
    for c in changes:
        print(f"{c.path.relative_to(REPO_ROOT) if c.path.is_relative_to(REPO_ROOT) else c.path}: {c.detail}")
    print(f"{len(changes)} file(s) {'changed' if args.apply else 'would change (pass --apply)'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lib.sources.cli", description=(__doc__ or "").split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("zotero-verify", help="read-only Zotero API checks").set_defaults(func=cmd_zotero_verify)
    p = sub.add_parser("sync-bib", help="regenerate reports/references.yaml from Zotero")
    p.add_argument("--path-output", default=str(DEFAULT_REFERENCES))
    p.add_argument("--checks", choices=("warn", "strict"), default="warn")
    p.add_argument("--force", action="store_true", help="regenerate even if up to date; allow dropping cited keys")
    p.add_argument("--verbose", action="store_true", help="print every finding")
    p.set_defaults(func=cmd_sync_bib)
    p = sub.add_parser("check-citekeys", help="confirm every cited key exists in references.yaml")
    p.add_argument("--path-references", default=str(DEFAULT_REFERENCES))
    p.add_argument("--path-reports", default=str(REPORTS_DIR))
    p.set_defaults(func=cmd_check_citekeys)

    p = sub.add_parser("ingest", help="ingest approved card(s) into Zotero, public hosts, short links and the repo")
    p.add_argument("path_cards", nargs="+", metavar="PATH_CARD")
    p.add_argument("--path-source", help="the original file (only with a single card)")
    p.add_argument("--path-source-dir", help="folder searched recursively for each card's source_file")
    p.add_argument(
        "--path-provenance-csv", help="staging PROVENANCE_FOR_ZOTERO.csv: finds each card's original by extract path"
    )
    p.add_argument(
        "--zotero-item", help="adopt this existing Zotero item (e.g. one added to the Inbox) instead of creating one"
    )
    p.add_argument("--extract", action="store_true", help="reuse the existing extract at the card's extract_path")
    p.add_argument("--force", action="store_true", help="create the item even if possible duplicates exist")
    p.add_argument(
        "--no-publish", action="store_true", help="queue short links locally; do not push to pub or tag processed"
    )
    p.set_defaults(func=cmd_ingest)
    p = sub.add_parser("check-card", help="validate a drafted card (no writes)")
    p.add_argument("path_card", metavar="PATH_CARD")
    p.add_argument("--zotero-item")
    p.set_defaults(func=cmd_check_card)
    p = sub.add_parser("key", help="the citation key the rule gives a draft card")
    p.add_argument("path_card", metavar="PATH_CARD")
    p.set_defaults(func=cmd_key)
    p = sub.add_parser("fetch", help="download a source's original file from Zotero; prints the path")
    p.add_argument("citekey")
    p.add_argument("--path-output-dir")
    p.set_defaults(func=cmd_fetch)
    p = sub.add_parser("pending", help="Zotero items waiting for ingest")
    p.add_argument(
        "--brief", action="store_true", help="one line, silent when nothing is waiting or Zotero is unreachable"
    )
    p.add_argument(
        "--hook", action="store_true", help="session-start hook output: JSON with additional_context, silent when empty"
    )
    p.set_defaults(func=cmd_pending)
    p = sub.add_parser("dedupe", help="is this file, URL, DOI or title already in the repo or library?")
    p.add_argument("--path-file")
    p.add_argument("--url")
    p.add_argument("--doi")
    p.add_argument("--title")
    p.add_argument("--path-provenance-csv")
    p.add_argument("--no-zotero", action="store_true", help="search the repo only")
    p.set_defaults(func=cmd_dedupe)
    p = sub.add_parser("org", help="existing spellings and short forms of an organization")
    p.add_argument("name")
    p.add_argument(
        "--no-zotero",
        action="store_true",
        help="skip the Zotero library (references.yaml and the conventions doc only)",
    )
    p.set_defaults(func=cmd_org)
    p = sub.add_parser("status", help="step checklist per citation key")
    p.add_argument("citekeys", nargs="*")
    p.add_argument("--path-provenance-csv", help="check the extract of every row")
    p.set_defaults(func=cmd_status)
    sub.add_parser("doctor", help="check credentials, access and tools").set_defaults(func=cmd_doctor)
    sub.add_parser("projects", help="list projects").set_defaults(func=cmd_projects)
    p = sub.add_parser("find-doi", help="find and verify a document's DOI")
    p.add_argument("--title")
    p.add_argument("--path-file")
    p.add_argument("--url")
    p.add_argument("--zotero-doi")
    p.add_argument("--author")
    p.set_defaults(func=cmd_find_doi)
    p = sub.add_parser("draft-cards", help="pre-fill draft cards from the staging provenance CSV")
    p.add_argument("--path-provenance-csv", required=True)
    p.add_argument("--path-output-dir", required=True)
    p.set_defaults(func=cmd_draft_cards)
    p = sub.add_parser("convert-frontmatter", help="legacy extract front matter to the flat schema")
    p.add_argument("--path-root")
    p.add_argument("--apply", action="store_true")
    p.set_defaults(func=cmd_convert_frontmatter)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
