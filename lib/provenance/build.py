"""Command-line entry point shared by every testimony's ``build_provenance.py``."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from lib.provenance.config import ProvenanceConfig
from lib.provenance.document import rows_for_csv, write_csv, write_docx, write_markdown
from lib.provenance.extract_check import check_against_extract
from lib.provenance.links import check_links, find_urls
from lib.provenance.pdf_index import index_pdf
from lib.provenance.qmd import QmdDoc, evaluate_exprs, parse_qmd
from lib.provenance.resolve import git, git_show
from lib.provenance.review import Review, flag
from lib.provenance.rows import build_rows
from lib.sources import frontmatter

CACHE_PATH_RE = re.compile(r"""["']((?:\.\./)*cache/[^"']+\.pkl)["']""")


def check_cache(cfg: ProvenanceConfig, doc: QmdDoc, path_exec_dir: Path, review: Review) -> None:
    """Record which cache files the numbers came from, and flag ones written after the tag by other code."""
    tag_commit = git(cfg.path_repo, "rev-parse", f"{cfg.tag}^{{commit}}").stdout.strip()
    tag_time = datetime.fromisoformat(git(cfg.path_repo, "show", "-s", "--format=%cI", tag_commit).stdout.strip())
    exec_head = git(path_exec_dir, "rev-parse", "HEAD", check=False).stdout.strip()
    from_tag = exec_head == tag_commit
    for rel in sorted(set(CACHE_PATH_RE.findall(doc.setup_code))):
        path = path_exec_dir / rel
        if not path.exists():
            flag(review, "cache_missing", rel, str(path))
            continue
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        flag(review, "cache_file", rel, f"sha256 {sha[:12]}; written {mtime.isoformat(timespec='seconds')}")
        if not from_tag and mtime > tag_time:
            flag(
                review,
                "cache_not_from_tag",
                rel,
                f"written after {cfg.tag} by a checkout at {exec_head[:8] or '?'}; "
                "render the notebooks at the tag and set path_exec_dir to that checkout",
            )


def _docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode()
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", xml))


def main(cfg: ProvenanceConfig, default_output_dir: Path, description: str) -> None:
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--path-output-dir", type=Path, default=default_output_dir)
    ap.add_argument("--skip-s3", action="store_true", help="skip the checks against the simulation runs on S3")
    ap.add_argument(
        "--path-exec-dir",
        type=Path,
        default=None,
        help="report directory whose cache/ the testimony setup reads (e.g. a worktree rendered at the tag)",
    )
    ap.add_argument("--path-pdf", type=Path, default=None, help="the testimony as filed (overrides the config)")
    ap.add_argument(
        "--check-links",
        action="store_true",
        help="check that every GitHub link resolves (needs `gh`; run after pushing tags)",
    )
    args = ap.parse_args()
    out_dir: Path = args.path_output_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.path_exec_dir is not None:
        cfg.path_exec_dir = args.path_exec_dir.resolve()
    if args.path_pdf is not None:
        cfg.path_pdf = args.path_pdf.resolve()

    if not cfg.path_pdf.exists():
        raise SystemExit(
            f"{cfg.path_pdf} not found; fetch the filed PDF (`just fetch-source <citekey>`) and pass --path-pdf"
        )
    want_md5 = cfg.pdf_md5
    if cfg.path_extract is not None:
        extract_md5 = str(frontmatter.parse(cfg.path_extract.read_text()).get("md5") or "")
        if want_md5 and extract_md5 and extract_md5 != want_md5:
            raise SystemExit(f"{cfg.path_extract} is of a different PDF (md5 {extract_md5}, config {want_md5})")
        want_md5 = want_md5 or extract_md5 or None
    if want_md5 and hashlib.md5(cfg.path_pdf.read_bytes()).hexdigest() != want_md5:
        raise SystemExit(f"{cfg.path_pdf} is not the filed PDF (md5 differs from {want_md5})")
    idx = index_pdf(cfg.path_pdf)
    (out_dir / "pdf_lines.json").write_text(json.dumps(idx.lines, indent=1, ensure_ascii=False))
    doc = parse_qmd(git_show(cfg.tag, f"{cfg.report_rel}/{cfg.qmd_name}", cfg.path_repo))
    path_exec_dir = cfg.path_exec_dir or cfg.path_report
    evaluate_exprs(doc, path_exec_dir, cfg.qmd_name)

    review: Review = []
    baseline = _docx_text(cfg.path_baseline_docx) if cfg.path_baseline_docx else None
    rows = build_rows(cfg, doc, idx, review, baseline)
    if cfg.path_extract is not None:
        check_against_extract(rows, cfg.path_extract, review)
    check_cache(cfg, doc, path_exec_dir, review)
    if not args.skip_s3 and cfg.run_checks is not None:
        cfg.run_checks(review)

    path_md = out_dir / "provenance.md"
    write_markdown(cfg, rows, path_md)
    if args.check_links:
        check_links([*(r.link.url for r in rows if r.link), *find_urls(path_md.read_text())], review)
    write_csv(out_dir / "provenance.csv", rows_for_csv(rows))
    write_csv(out_dir / "provenance_review.csv", review)
    write_docx(path_md, out_dir / cfg.docx_name)
    counts: dict[str, int] = defaultdict(int)
    for r in rows:
        counts[r.type] += 1
    print(f"{len(rows)} rows ({dict(counts)}); {len(review)} review items -> {out_dir}")
