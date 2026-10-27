"""Render citations against two bibliographies and compare them, key by key.

For a set of keys, a scratch document cites each key in its own paragraph and prints the
bibliography. It is rendered to HTML with pandoc's citeproc, once per bibliography (and
style), and each key's in-text citation and bibliography entry are extracted and compared.
Citing all of a report's keys together keeps year suffixes (2024a, 2024b) as in the report.
"""

from __future__ import annotations

import csv
import re
import subprocess
import tempfile
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup


@dataclass(frozen=True)
class Rendered:
    in_text: str
    bibliography: str


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def render_keys(keys: Iterable[str], bibliography: Path, csl: Path | None = None) -> dict[str, Rendered]:
    """Narrative in-text citation and bibliography entry for each key (missing keys omitted)."""
    keys = list(dict.fromkeys(keys))
    with tempfile.TemporaryDirectory() as tmp:
        doc = Path(tmp) / "cite.md"
        out = Path(tmp) / "cite.html"
        body = "\n\n".join(f"::: {{#k{i} .cite}}\n@{{{k}}}\n:::" for i, k in enumerate(keys))
        doc.write_text(f"{body}\n\n::: {{#refs}}\n:::\n", encoding="utf-8")
        cmd = ["quarto", "pandoc", str(doc), "--citeproc", "-t", "html", "-o", str(out)]
        cmd += ["--bibliography", str(bibliography)] + (["--csl", str(csl)] if csl else [])
        subprocess.run(cmd, check=True, capture_output=True)
        soup = BeautifulSoup(out.read_text(encoding="utf-8"), "html.parser")
    found: dict[str, Rendered] = {}
    for i, key in enumerate(keys):
        cite = soup.find(id=f"k{i}")
        entry = soup.find(id=f"ref-{key}")
        if cite is None or entry is None:
            continue
        found[key] = Rendered(_clean(cite.get_text(" ")), _clean(entry.get_text(" ")))
    return found


def compare(
    keys: Iterable[str],
    before: tuple[Path, Path | None],
    after: tuple[Path, Path | None],
    renames: Mapping[str, str] | None = None,
) -> list[dict[str, str]]:
    """One row per key: before/after in-text and bibliography, and whether either changed.

    ``renames`` maps old key -> new key, so a renamed item is compared with itself.
    """
    keys = list(dict.fromkeys(keys))
    renames = renames or {}
    old = render_keys(keys, *before)
    new = render_keys([renames.get(k, k) for k in keys], *after)
    rows = []
    for key in keys:
        b, a = old.get(key), new.get(renames.get(key, key))
        rows.append(
            {
                "key": key,
                "new_key": renames.get(key, key),
                "in_text_before": b.in_text if b else "(missing)",
                "in_text_after": a.in_text if a else "(missing)",
                "bibliography_before": b.bibliography if b else "(missing)",
                "bibliography_after": a.bibliography if a else "(missing)",
                "changed": str(b != a),
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["key"])
        writer.writeheader()
        writer.writerows(rows)
