"""Tooling for the one-time migration of the existing extracts into the pipeline (Phase 5).

* ``read_provenance`` / ``source_for_extract`` / ``draft_cards``: the staging folder's ``PROVENANCE_FOR_ZOTERO.csv``
  lists each original (``src``), its public source URL, and the extract (``md_path``) already in the repo.
  Drafts pre-fill a card from a row; a person (or the agent) adds the creators, key, index row and approves it.
* ``convert_frontmatter``: legacy extracts (``source:`` and ``original_pdf_path:``) to the flat schema, editing only
  the lines that change.
* ``convert_manifest_folder``: a folder described by ``MANIFEST.csv`` gets the same fields in each extract's
  front matter (``source_file``, ``source_url``, and ``md5`` when the PDF is on disk). Deleting ``MANIFEST.csv``
  afterwards is left to the person.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import polars as pl
import yaml

from lib.sources import env, frontmatter, zotero

SEPARATOR = " :: "  # the provenance CSV's titles read "<filing title> :: <exhibit file name>"


def read_provenance(path: Path) -> pl.DataFrame:
    return pl.read_csv(path, infer_schema_length=0)


def _stem_key(path: str) -> str:
    return Path(path).with_suffix("").as_posix()


def source_for_extract(provenance: pl.DataFrame, extract_path: str) -> dict[str, Any] | None:
    """The provenance row whose extract (or workbook) is ``extract_path``; workbooks match on the stem."""
    want = _stem_key(extract_path)
    for row in provenance.iter_rows(named=True):
        if _stem_key(row["md_path"]) == want:
            return row
    return None


def draft_cards(provenance: pl.DataFrame, out_dir: Path, repo_root: Path | None = None) -> list[Path]:
    """Write one draft card per row, with what the CSV knows. Drafts are deliberately not valid yet:
    ``creators``, ``citekey`` and ``index_row`` need a person or the agent, so ingest rejects them until filled.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for row in provenance.iter_rows(named=True):
        md = Path(row["md_path"])
        workbook = row["type"].upper().startswith("XLS")
        extract = md.with_suffix(".md") if workbook else md
        title = row["title"].split(SEPARATOR)[0].strip()
        card = {
            "item_type": "dataset" if workbook else "document",
            "title": f"Docket {row['docket']}: {title}",
            "docket": row["docket"],
            "date": row["filing_date"],
            "source_file": Path(row["src"]).name,
            "source_url": row["source_url"],
            "extract_path": extract.as_posix(),
            "projects": [md.parts[2]] if len(md.parts) > 2 else [],
            "front_matter": {k: row[k] for k in ("docket", "utility", "rate", "filing_date", "filer") if row.get(k)}
            | {"document_type": row["doc_type"]},
        }
        path = out_dir / f"{row['n']:0>3}_{extract.stem[:60]}.yaml"
        path.write_text(yaml.safe_dump(card, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")
        paths.append(path)
    return paths


@dataclass(frozen=True)
class Change:
    path: Path
    detail: str


def _parses(lines: list[str]) -> bool:
    try:
        yaml.safe_load("\n".join(lines))
    except yaml.YAMLError:
        return False
    return True


def quote_invalid_values(text: str) -> tuple[str, list[str]]:
    """``text`` with each one-line value that is not valid YAML (e.g. a plain value containing ``: ``) single-quoted.

    Returns the new text and the fields that were quoted.
    """
    front, rest = frontmatter.split(text)
    if front is None or _parses(front):
        return text, []
    quoted = []
    out = []
    for line in front:
        m = frontmatter._KEY_LINE.match(line)
        if m and not _parses([line]):
            value = line[m.end() :].strip()
            line = f"{m.group(1)}: '{value.replace(chr(39), chr(39) * 2)}'"
            quoted.append(m.group(1))
        out.append(line)
    return frontmatter._join(out, rest), quoted


def convert_frontmatter(root: Path | None = None, dry_run: bool = True) -> list[Change]:
    """Rename ``source`` to ``source_file`` and drop ``original_pdf_path`` in every legacy extract under ``root``.

    Legacy fields are found from the front matter's lines rather than a YAML parse, because some legacy blocks are
    not valid YAML; those values are quoted so the converted block parses.
    """
    changes = []
    for path in frontmatter.iter_extracts(root):
        text = path.read_text(encoding="utf-8")
        front, _ = frontmatter.split(text)
        if front is None:
            continue
        keys = {b.key for b in frontmatter._blocks(front)}
        what = [f for f in ("source", "original_pdf_path") if f in keys]
        if not what:
            continue
        new, quoted = quote_invalid_values(frontmatter.to_flat(text))
        if new == text:
            continue
        if not dry_run:
            path.write_text(new, encoding="utf-8")
        detail = "converted " + ", ".join(what)
        if quoted:
            detail += "; quoted " + ", ".join(quoted)
        changes.append(Change(path, detail))
    return changes


def convert_manifest_folder(folder: Path, dry_run: bool = True) -> list[Change]:
    """Copy each ``MANIFEST.csv`` row's facts into its extract's front matter (columns as in the legacy manifests).

    An extract without front matter gets a new block. When several rows name the same extract (a PDF and the
    workbook CSVs pulled from it), the first row is the source.
    """
    folder = Path(folder)
    manifest = folder / "MANIFEST.csv"
    if not manifest.exists():
        raise FileNotFoundError(manifest)
    changes = []
    with manifest.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    seen: set[Path] = set()
    for row in rows:
        extract = (folder / row["md_path"]).resolve() if row.get("md_path") else None
        if extract is None or not extract.exists() or extract in seen:
            continue
        seen.add(extract)
        fields: dict[str, Any] = {"source_file": Path(row["source_pdf"]).name}
        if row.get("source_url"):
            fields["source_url"] = row["source_url"]
        pdf = folder / row["source_pdf"]
        if pdf.exists():
            fields["md5"] = zotero.file_md5(pdf)
        text = extract.read_text(encoding="utf-8")
        if frontmatter.split(text)[0] is None:
            text_with_block = frontmatter._join([], "---\n\n" + text.lstrip("\n"))
            new = frontmatter.to_flat(text_with_block, fields)
        else:
            new = frontmatter.to_flat(text, fields)
        if new != text:
            if not dry_run:
                extract.write_text(new, encoding="utf-8")
            changes.append(Change(extract, "set " + ", ".join(fields)))
    return changes


def manifest_folders(root: Path | None = None) -> list[Path]:
    return sorted(p.parent for p in (Path(root) if root else env.SOURCES_DIR).rglob("MANIFEST.csv"))
