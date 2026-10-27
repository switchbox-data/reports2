"""Rewrite citation keys in report sources after the library's keys change.

Only citations are touched (the same pandoc syntax :mod:`citations` reads): code blocks, inline
code, email addresses and Quarto cross-references are left alone. Each citation is renamed in
one pass, so an old key that is also some other item's new key is never renamed twice.

Such a key is *ambiguous* once the cleanup has run: in a file it may already be the new key.
The renames table marks it, and a rerun on a teammate's branch leaves it alone and lists where
it is cited, to be checked by hand.
"""

from __future__ import annotations

import csv
from collections.abc import Mapping
from pathlib import Path

from lib.sources import citations


def ambiguous(renames: Mapping[str, str]) -> set[str]:
    """Old keys that are also some item's new key."""
    return set(renames) & set(renames.values())


def unambiguous(renames: Mapping[str, str]) -> dict[str, str]:
    """The renames that are safe to apply to a file that may already be partly renamed."""
    skip = ambiguous(renames)
    return {old: new for old, new in renames.items() if old not in skip}


def rewrite(text: str, renames: Mapping[str, str]) -> tuple[str, int]:
    """``text`` with every cited old key renamed, and the number of citations changed."""
    lines = text.splitlines(keepends=True)
    n = 0
    for lineno, prose in citations._prose_lines(text):
        spans = []
        for m in citations.CITATION_RE.finditer(prose):
            group = "braced" if m.group("braced") else "key"
            spans.append(m.span(group))
        spans += [m.span("key") for m in citations.REF_LINK_RE.finditer(prose)]
        line = lines[lineno - 1]
        for start, end in sorted(spans, reverse=True):
            if (new := renames.get(line[start:end])) is not None:
                line = line[:start] + new + line[end:]
                n += 1
        lines[lineno - 1] = line
    return "".join(lines), n


def rewrite_reports(reports_dir: Path, renames: Mapping[str, str]) -> dict[Path, int]:
    """Rewrite every report source in place; returns citations changed per file."""
    changed = {}
    for path in citations.report_sources(reports_dir):
        text = path.read_text(encoding="utf-8")
        new, n = rewrite(text, renames)
        if n:
            path.write_text(new, encoding="utf-8")
            changed[path] = n
    return changed


def write_renames(renames: Mapping[str, str], path: Path) -> None:
    skip = ambiguous(renames)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["old_key", "new_key", "ambiguous"])
        w.writerows((old, new, "yes" if old in skip else "") for old, new in sorted(renames.items()))


def read_renames(path: Path) -> dict[str, str]:
    """The table's safe renames (ambiguous rows excluded)."""
    with path.open(newline="", encoding="utf-8") as f:
        return {r["old_key"]: r["new_key"] for r in csv.DictReader(f) if not r["ambiguous"]}


def read_ambiguous(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8") as f:
        return {r["old_key"] for r in csv.DictReader(f) if r["ambiguous"]}
