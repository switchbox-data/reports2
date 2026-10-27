"""Command-line entry points for the bibliography tooling (run via the root Justfile).

    uv run python -m lib.sources.cli zotero-verify
    uv run python -m lib.sources.cli sync-bib [--checks warn|strict] [--force]
    uv run python -m lib.sources.cli check-citekeys

None of these write to Zotero.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

import yaml

from lib.sources import bib, checks, citations, extra, zotero

REPO_ROOT = zotero.REPO_ROOT
DEFAULT_REFERENCES = REPO_ROOT / "reports" / "references.yaml"
REPORTS_DIR = REPO_ROOT / "reports"
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
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
