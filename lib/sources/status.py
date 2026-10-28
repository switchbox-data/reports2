"""``just sources-status``: the step checklist for one source, read from the real systems.

For each citation key: the Zotero item (key pinned, citation url, project, stored file, ``processed`` tag), the
DocumentCloud / Drive / Wayback copies recorded on it, the short link in ``pub``, and the repo (front matter,
index row). Green on every line means the staging copy can be deleted.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from lib.sources import documentcloud, extra, frontmatter, indexes, metadata, shortlinks, zotero
from lib.sources.doctor import FAIL, OK, WARN, Check

SHORT_LINK_BASE = metadata.SHORT_LINK_BASE


def _line(name: str, ok: bool, detail: str = "", hint: str = "", soft: bool = False) -> Check:
    return Check(name, OK if ok else (WARN if soft else FAIL), detail, hint)


def source_status(citekey: str, root: Path | None = None) -> list[Check]:
    """Checklist for ``citekey``; stops after the first line when the key is not in Zotero."""
    item_key = zotero.pinned_keys().get(citekey)
    if item_key is None:
        return [
            Check("Zotero item with pinned key", FAIL, citekey, "run just sources-ingest, or pin the key in Zotero")
        ]
    item = zotero.get_item(item_key)
    data: dict[str, Any] = item["data"]
    checks = [Check("Zotero item with pinned key", OK, zotero.web_link(item))]
    doi = data.get("DOI")
    want_url = f"https://doi.org/{doi}" if doi else f"{SHORT_LINK_BASE}/{citekey}"
    checks.append(
        _line(
            "Zotero url is the citation link",
            data.get("url") == want_url,
            f"{data.get('url')!r}",
            f"expected {want_url}",
        )
    )
    names = {key: name for name, key in zotero.project_collections().items()}
    in_projects = sorted(names[c] for c in data.get("collections", []) if c in names)
    checks.append(
        _line(
            "in a project subcollection",
            bool(in_projects),
            ", ".join(in_projects),
            "add the item to Reports > <project>",
        )
    )
    stored = zotero.stored_attachments(item_key)
    checks.append(
        _line(
            "file stored in Zotero",
            bool(stored),
            ", ".join(c["data"].get("filename", "") for c in stored),
            "attach the file in Zotero",
        )
    )
    ex = data.get("extra")
    if dc := extra.get(ex, zotero.DOCUMENTCLOUD_ID):
        try:
            doc = documentcloud.client().documents.get(int(dc))
            checks.append(
                _line(
                    "DocumentCloud copy public and processed",
                    doc.status == "success" and doc.access == "public",
                    f"{doc.status}, {doc.access}",
                )
            )
        except Exception as e:
            checks.append(Check("DocumentCloud copy public and processed", FAIL, f"{type(e).__name__}: {e}"[:200]))
    else:
        checks.append(
            Check(
                "DocumentCloud copy",
                OK if doi else WARN,
                "none (DOI item)" if doi else "none recorded",
                "" if doi else "fine for web pages and workbooks",
            )
        )
    if not doi:
        target = shortlinks.resolve(citekey)
        checks.append(
            _line("short link in pub", target is not None, target or "", "rerun just sources-ingest for this card")
        )
    checks.append(
        _line("tagged processed", zotero.is_processed(data), "", "rerun ingest; the tag goes on after all steps verify")
    )
    path = frontmatter.find_by_citekey(citekey, root)
    if path is None:
        checks.append(
            Check("extract with this citekey in the repo", WARN, "none", "fine for sources that are not extracted")
        )
        return checks
    fm = frontmatter.read(path)
    checks.append(
        _line("front matter zotero_item matches", fm.get("zotero_item") == item_key, str(fm.get("zotero_item")))
    )
    if not doi:
        checks.append(
            _line(
                "front matter short_url matches",
                fm.get("short_url") == f"{SHORT_LINK_BASE}/{citekey}",
                str(fm.get("short_url")),
            )
        )
    sources = root or indexes.GLOBAL_README.parent / "sources"
    rel = path.resolve().relative_to(Path(sources).resolve()).as_posix()
    checks.append(_line("row in context/README.md", indexes.has_global_row(rel), rel, "rerun ingest to add the row"))
    return checks


def all_green(checks: list[Check]) -> bool:
    return all(c.level != FAIL for c in checks)
