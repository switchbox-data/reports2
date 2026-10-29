#!/usr/bin/env python3
"""The ``testimony:`` fill-in fields for expert-testimony Word output.

Every expert testimony renders with the same Word format
(``lib/just/templates``); only the docket details change from filing to
filing. Those details live in the testimony file's frontmatter, grouped
under one ``testimony:`` key::

    testimony:
      commission: Maryland Public Service Commission
      commission_short: Maryland PSC
      case_number: "Case No. 9888"
      caption:
        - IN THE MATTER OF THE APPLICATION OF
        - BALTIMORE GAS & ELECTRIC COMPANY
        - FOR ADJUSTMENTS TO ITS ELECTRIC BASE RATES
      type: Direct
      and_exhibits: true
      witness: Juan-Pablo Velez
      witness_title: Executive Director, Switchbox
      on_behalf_of: Chesapeake Climate Action Network
      date: 2026-09-22

Quarto passes unknown frontmatter fields straight through, so nothing here
breaks Quarto, but Quarto cannot *require* fields either. This module is the
safeguard: ``just testimony`` calls :func:`parse` before rendering and stops
with a plain list of what is missing, misspelled or still a placeholder, and
``just new-testimony`` writes a file with every field already present.

Usage::

    uv run python -m lib.just.testimony new reports/xx/expert_testimony.qmd
    uv run python -m lib.just.testimony check expert_testimony.qmd
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Field definitions
# ---------------------------------------------------------------------------

REQUIRED_FIELDS: tuple[str, ...] = (
    "commission",
    "commission_short",
    "case_number",
    "caption",
    "type",
    "witness",
    "on_behalf_of",
    "date",
)
OPTIONAL_FIELDS: tuple[str, ...] = ("and_exhibits", "witness_title", "version_label")
ALL_FIELDS: tuple[str, ...] = REQUIRED_FIELDS + OPTIONAL_FIELDS

# Plain-English meaning of each field; shown in error messages and the scaffold.
FIELD_HELP: dict[str, str] = {
    "commission": 'full commission name on the cover, e.g. "Maryland Public Service Commission"',
    "commission_short": 'short commission name for the page header, e.g. "Maryland PSC"',
    "case_number": 'docket as it should print, e.g. "Case No. 9888" or "Docket No. 26-01-03"',
    "caption": "list of caption lines naming the applicant and the subject of the proceeding",
    "type": "Direct, Rebuttal, Surrebuttal, ...",
    "witness": "witness name",
    "on_behalf_of": "the party the witness testifies for",
    "date": "filing date, e.g. 2026-09-22",
    "and_exhibits": "true adds AND EXHIBITS to the cover title (optional)",
    "witness_title": 'line under the witness name, e.g. "Executive Director, Switchbox" (optional)',
    "version_label": 'extra cover line such as "PUBLIC VERSION" (optional)',
}

TESTIMONY_TYPES: tuple[str, ...] = (
    "Direct",
    "Rebuttal",
    "Surrebuttal",
    "Rejoinder",
    "Supplemental Direct",
    "Supplemental Rebuttal",
)

_MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)

_YAML_FENCE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


class TestimonyError(ValueError):
    """Raised when the ``testimony:`` fields are missing or invalid.

    ``problems`` holds one plain-English line per problem.
    """

    __test__ = False  # not a pytest test class

    def __init__(self, problems: list[str]) -> None:
        self.problems = problems
        super().__init__("\n".join(problems))


@dataclass(frozen=True)
class Testimony:
    """Validated ``testimony:`` fields."""

    __test__ = False  # not a pytest test class

    commission: str
    commission_short: str
    case_number: str
    caption: tuple[str, ...]
    type: str
    witness: str
    on_behalf_of: str
    date: date
    and_exhibits: bool = False
    witness_title: str | None = None
    version_label: str | None = None

    @property
    def header_lines(self) -> tuple[str, str, str]:
        """The three right-aligned running-header lines on every body page."""
        return (
            f"{self.type} Testimony of {self.witness}",
            self.on_behalf_of,
            f"{self.commission_short} {self.case_number}",
        )

    @property
    def date_long(self) -> str:
        """Filing date without a leading zero, e.g. ``September 22, 2026``."""
        return long_date(self.date)


def long_date(d: date) -> str:
    """Format a date as ``September 2, 2026`` (no zero-padded day)."""
    return f"{_MONTHS[d.month - 1]} {d.day}, {d.year}"


# ---------------------------------------------------------------------------
# Reading and validating
# ---------------------------------------------------------------------------


def read_frontmatter(qmd_path: Path) -> dict[str, Any]:
    """Return the parsed YAML frontmatter of a .qmd, or ``{}`` if absent."""
    text = qmd_path.read_text(encoding="utf-8")
    match = _YAML_FENCE.match(text)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def _is_placeholder(value: str) -> bool:
    value = value.strip()
    return value.startswith("[") and value.endswith("]")


def _parse_date(value: Any) -> date | None:
    """Accept a YAML date, ``YYYY-MM-DD`` or ``Month D, YYYY``; else ``None``."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        s = value.strip()
        for fmt in ("%Y-%m-%d", "%B %d, %Y", "%B %d %Y"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue
    return None


def _normalize_type(value: str) -> str | None:
    """Match a testimony type case-insensitively; return its canonical form."""
    wanted = " ".join(value.split()).lower()
    for known in TESTIMONY_TYPES:
        if known.lower() == wanted:
            return known
    return None


def _bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str) and value.strip().lower() in {"true", "yes", "false", "no"}:
        return value.strip().lower() in {"true", "yes"}
    return None


def parse(meta: Mapping[str, Any]) -> Testimony:
    """Validate frontmatter and return the :class:`Testimony` fields.

    Raises :class:`TestimonyError` listing every problem at once, so one
    render attempt shows everything that needs fixing.
    """
    block = meta.get("testimony")
    if not isinstance(block, Mapping):
        raise TestimonyError(
            [
                "The frontmatter has no `testimony:` block. Fill in the block with these fields:",
                *[f"  {name}: {FIELD_HELP[name]}" for name in REQUIRED_FIELDS],
                "Tip: `just new-testimony <path>` writes a new file with every field in place.",
            ]
        )

    problems: list[str] = []

    for key in block:
        if key not in ALL_FIELDS:
            close = difflib.get_close_matches(str(key), ALL_FIELDS, n=1)
            hint = f" Did you mean `{close[0]}`?" if close else ""
            problems.append(f"Unknown field `testimony.{key}`.{hint}")

    def text_value(name: str) -> str | None:
        raw = block.get(name)
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            return None
        return str(raw).strip()

    values: dict[str, Any] = {}
    for name in REQUIRED_FIELDS:
        if name == "caption":
            continue
        if name == "date":
            continue
        value = text_value(name)
        if value is None:
            problems.append(f"Missing `testimony.{name}`: {FIELD_HELP[name]}.")
        elif _is_placeholder(value):
            problems.append(f"`testimony.{name}` is still a placeholder ({value}): {FIELD_HELP[name]}.")
        else:
            values[name] = value

    caption_raw = block.get("caption")
    if not isinstance(caption_raw, list) or not caption_raw:
        problems.append(f"Missing `testimony.caption`: {FIELD_HELP['caption']} (a YAML list, one line per item).")
    else:
        lines = [str(item).strip() for item in caption_raw if str(item).strip()]
        if not lines:
            problems.append("`testimony.caption` is empty.")
        placeholders = [line for line in lines if _is_placeholder(line)]
        if placeholders:
            problems.append(
                f"`testimony.caption` still has placeholder lines ({placeholders[0]}): {FIELD_HELP['caption']}."
            )
        values["caption"] = tuple(lines)

    if "type" in values:
        canonical = _normalize_type(values["type"])
        if canonical is None:
            problems.append(f"`testimony.type` is `{values['type']}`; use one of: {', '.join(TESTIMONY_TYPES)}.")
        else:
            values["type"] = canonical

    date_raw = block.get("date")
    if date_raw is None or (isinstance(date_raw, str) and not date_raw.strip()):
        problems.append(f"Missing `testimony.date`: {FIELD_HELP['date']}.")
    elif isinstance(date_raw, str) and _is_placeholder(date_raw):
        problems.append(f"`testimony.date` is still a placeholder ({date_raw}): {FIELD_HELP['date']}.")
    else:
        parsed = _parse_date(date_raw)
        if parsed is None:
            problems.append(f"`testimony.date` is `{date_raw}`; write it like 2026-09-22.")
        else:
            values["date"] = parsed

    and_exhibits = False
    if "and_exhibits" in block:
        flag = _bool(block["and_exhibits"])
        if flag is None:
            problems.append("`testimony.and_exhibits` must be true or false.")
        else:
            and_exhibits = flag

    optional: dict[str, str | None] = {}
    for name in ("witness_title", "version_label"):
        value = text_value(name)
        if value is not None and _is_placeholder(value):
            problems.append(f"`testimony.{name}` is still a placeholder ({value}); fill it in or delete the line.")
        optional[name] = value

    if problems:
        raise TestimonyError(problems)

    return Testimony(and_exhibits=and_exhibits, **values, **optional)


def parse_file(qmd_path: Path) -> Testimony:
    """Read a testimony .qmd and return its validated ``testimony:`` fields."""
    return parse(read_frontmatter(qmd_path))


# ---------------------------------------------------------------------------
# Scaffold
# ---------------------------------------------------------------------------

SCAFFOLD = """---
title: "Expert Testimony"
date: today
author:
  - name: "[WITNESS NAME]"
    affiliations:
      - Switchbox
toc: false
notebook-links: false
bibliography: ../references.yaml
csl: ../chicago-author-date-switchbox.csl
execute:
  echo: false
format:
  html:
    page-layout: article
    smooth-scroll: true
    theme:
      - ../.style/switchbox.scss

# Fill in every field below. They become the Word cover page and the running
# header; nothing else needs to be typed by hand. `just testimony` stops and
# lists anything still missing or still in [BRACKETS].
testimony:
  commission: "[COMMISSION NAME]"          # cover page, e.g. Maryland Public Service Commission
  commission_short: "[COMMISSION SHORT NAME]"  # page header, e.g. Maryland PSC
  case_number: "[CASE NUMBER]"             # e.g. Case No. 9888 or Docket No. 26-01-03
  caption:                                 # left side of the docket caption, one line per item
    - "[IN THE MATTER OF THE APPLICATION OF]"
    - "[APPLICANT NAME]"
    - "[SUBJECT OF THE PROCEEDING]"
  type: "[Direct]"                         # Direct, Rebuttal or Surrebuttal
  and_exhibits: false                      # true adds AND EXHIBITS to the cover title
  witness: "[WITNESS NAME]"
  witness_title: "[WITNESS TITLE]"         # optional: delete the line if not needed
  on_behalf_of: "[PARTY]"
  date: "[YYYY-MM-DD]"                     # filing date
  # version_label: PUBLIC VERSION          # optional extra cover line
---

## I. Introduction

**Q.** Please state your name, business address, and occupation.

**A.** My name is [WITNESS NAME].
"""


def write_scaffold(path: Path) -> Path:
    """Write a new testimony file with every ``testimony:`` field in place."""
    if path.exists():
        raise FileExistsError(f"{path} already exists; not overwriting it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(SCAFFOLD, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _print_problems(err: TestimonyError, qmd_path: Path) -> None:
    print(f"💥 {qmd_path}: the `testimony:` fields need attention:", file=sys.stderr)
    for line in err.problems:
        print(f"   {line}", file=sys.stderr)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Create or check the `testimony:` fields of a testimony .qmd.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="Write a new testimony .qmd with every field in place.")
    p_new.add_argument("path_qmd", help="Where to create the file, e.g. reports/xx/expert_testimony.qmd")

    p_check = sub.add_parser("check", help="Validate the `testimony:` fields without rendering.")
    p_check.add_argument("path_qmd", help="The testimony .qmd to check.")

    args = parser.parse_args(argv)
    path = Path(args.path_qmd)

    if args.command == "new":
        try:
            created = write_scaffold(path)
        except FileExistsError as exc:
            print(f"💥 {exc}", file=sys.stderr)
            sys.exit(1)
        print(
            f"✅ Created {created}. Fill in the `testimony:` fields at the top, then run `just testimony {created.name}`."
        )
        return

    if not path.exists():
        print(f"💥 File not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        t = parse_file(path)
    except TestimonyError as err:
        _print_problems(err, path)
        sys.exit(2)
    print(f"✅ {path}: testimony fields OK ({t.type} testimony of {t.witness}, {t.case_number}, {t.date_long}).")


if __name__ == "__main__":
    main()
