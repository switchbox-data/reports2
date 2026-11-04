"""Is this document (or URL) already in the repo or the library?

Searches, recursively under ``context/sources/``: ``md5:`` and normalized ``source_url:`` in extract front
matter; legacy ``MANIFEST.csv`` rows (sha256, computed only when a manifest exists, plus source URL); the
staging provenance CSV during the migration. Then Zotero: attachments by md5, items by URL, DOI and title.
Folder depth does not matter and nothing depends on a file's name.
"""

from __future__ import annotations

import csv
import hashlib
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from lib.sources import env, frontmatter, webpage, zotero


@dataclass(frozen=True)
class Match:
    kind: str  # md5, source_url, manifest_sha256, manifest_url, provenance_url, then Zotero's md5/url/doi/title
    where: str  # a repo path, or a Zotero web link
    detail: str = ""

    def line(self) -> str:
        return f"{self.kind}: {self.where}" + (f" ({self.detail})" if self.detail else "")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _rel(path: Path) -> str:
    try:
        return Path(path).resolve().relative_to(env.REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def local_matches(
    md5: str | None = None,
    sha256: str | None = None,
    source_url: str | None = None,
    root: Path | None = None,
    provenance_csv: Path | None = None,
) -> list[Match]:
    """Repo-side matches only (no network)."""
    root = Path(root) if root else env.SOURCES_DIR
    url = webpage.normalize_url(source_url) if source_url else None
    found: list[Match] = []
    for path in frontmatter.iter_extracts(root):
        data = frontmatter.read(path)
        if md5 and data.get("md5") == md5:
            found.append(Match("md5", _rel(path)))
        if url and data.get("source_url") and webpage.normalize_url(str(data["source_url"])) == url:
            found.append(Match("source_url", _rel(path)))
    for manifest in sorted(root.rglob("MANIFEST.csv")):
        with manifest.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if sha256 and row.get("sha256") == sha256:
                    found.append(Match("manifest_sha256", _rel(manifest), row.get("source_pdf", "")))
                elif url and row.get("source_url") and webpage.normalize_url(row["source_url"]) == url:
                    found.append(Match("manifest_url", _rel(manifest), row.get("source_pdf", "")))
    if provenance_csv and url:
        with Path(provenance_csv).open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("source_url") and webpage.normalize_url(row["source_url"]) == url:
                    found.append(Match("provenance_url", row.get("md_path", ""), f"row {row.get('n')}"))
    return found


def zotero_matches(
    md5: str | None = None,
    url: str | None = None,
    doi: str | None = None,
    title: str | None = None,
    items: list[dict[str, Any]] | None = None,
) -> list[Match]:
    found = []
    for d in zotero.find_duplicates(md5=md5, url=url, doi=doi, title=title, items=items):
        found.append(
            Match(f"zotero_{d.kind}", zotero.desktop_link(d.item_key), f"{d.citekey or 'no key'}: {d.title[:60]}")
        )
    return found


def check(
    path: Path | None = None,
    source_url: str | None = None,
    doi: str | None = None,
    title: str | None = None,
    root: Path | None = None,
    provenance_csv: Path | None = None,
    items: list[dict[str, Any]] | None = None,
    use_zotero: bool = True,
) -> list[Match]:
    """Every place ``path`` (a file), ``source_url``, ``doi`` or ``title`` already appears."""
    md5 = zotero.file_md5(path) if path else None
    root = Path(root) if root else env.SOURCES_DIR
    sha = sha256_of(path) if path and any(root.rglob("MANIFEST.csv")) else None
    found = local_matches(md5, sha, source_url, root, provenance_csv)
    if use_zotero:
        found += zotero_matches(md5, source_url, doi, title, items)
    return found


def summarize(matches: Iterable[Match]) -> str:
    lines = [m.line() for m in matches]
    return "\n".join(lines) if lines else "no matches"
