"""Generate ``reports/chicago-author-date-switchbox.csl`` from pandoc's default CSL style.

Pandoc's default is Chicago Manual of Style 18th edition (author-date). Two patches:

- In-text citations print ``author-short`` (the organization's abbreviation, from
  ``tex.shortauthor`` in Zotero) instead of the author when it is set: "MA DPU (2024)".
- The bibliography appends it after the full name: "Massachusetts Department of Public
  Utilities (MA DPU). 2024. ..."

Items without ``author-short`` render exactly as in the default style. Rerun ``just make-csl``
after a pandoc (Quarto) upgrade; each patch point must match exactly once.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from lib.sources.zotero import REPO_ROOT

TITLE_OLD = "<title>Chicago Manual of Style 18th edition (author-date)</title>"
TITLE_NEW = "<title>Chicago Manual of Style 18th edition (author-date), Switchbox organization abbreviations</title>"

CITE_OLD = """        <names variable="composer">
          <name and="text" form="short" initialize-with=". "/>
          <substitute>
            <names variable="author"/>"""
CITE_NEW = """        <names variable="composer">
          <name and="text" form="short" initialize-with=". "/>
          <substitute>
            <text variable="author-short"/>
            <names variable="author"/>"""

BIB_OLD = """        <else>
          <text macro="author-bib"/>
          <text macro="date"/>"""
BIB_NEW = """        <else>
          <group delimiter=" ">
            <text macro="author-bib"/>
            <text variable="author-short" prefix="(" suffix=")"/>
          </group>
          <text macro="date"/>"""


def default_csl() -> str:
    return subprocess.run(
        ["quarto", "pandoc", "--print-default-data-file", "default.csl"], capture_output=True, text=True, check=True
    ).stdout


def make_csl(source: str) -> str:
    """Apply the patches, asserting each patch point occurs exactly once."""
    out = source
    for old, new in ((TITLE_OLD, TITLE_NEW), (CITE_OLD, CITE_NEW), (BIB_OLD, BIB_NEW)):
        n = out.count(old)
        if n != 1:
            raise RuntimeError(f"patch point found {n} times in pandoc's default.csl (expected 1):\n{old}")
        out = out.replace(old, new)
    return "".join(line.rstrip() + "\n" for line in out.splitlines())


def main() -> None:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    parser.add_argument("--path-output", default=str(REPO_ROOT / "reports" / "chicago-author-date-switchbox.csl"))
    args = parser.parse_args()
    Path(args.path_output).write_text(make_csl(default_csl()), encoding="utf-8")
    print(f"Wrote {args.path_output}")


if __name__ == "__main__":
    main()
