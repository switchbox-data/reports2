"""Schema for the second agent pass: authors, dates and titles for items still missing them.

Each batch writes ``item_fixes/batch_NN.json``. Every field is a suggestion with evidence; the
review sheet shows it next to the current value and nothing reaches Zotero without review.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from lib.sources.org_proposals import Evidence

ISO_DATE_RE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")


class Person(BaseModel):
    first: str = ""
    last: str = Field(min_length=1)


class ItemFix(BaseModel):
    item: str
    organizations: list[str] = Field(default_factory=list, description="author full names, in order")
    people: list[Person] = Field(default_factory=list, description="person authors, in order, after organizations")
    date: str | None = Field(default=None, description="ISO: YYYY, YYYY-MM or YYYY-MM-DD")
    title: str | None = None
    evidence: list[Evidence] = Field(min_length=1)
    confidence: Literal["high", "medium", "low"]
    action: Literal["fix", "delete", "duplicate_of"] = "fix"
    duplicate_of: str | None = None
    notes: str = ""

    @model_validator(mode="after")
    def _consistent(self) -> ItemFix:
        if self.date and not ISO_DATE_RE.match(self.date):
            raise ValueError(f"date {self.date!r} is not YYYY, YYYY-MM or YYYY-MM-DD")
        if self.action == "duplicate_of" and not self.duplicate_of:
            raise ValueError("duplicate_of needs the other item's key")
        if self.action == "fix" and not (self.organizations or self.people or self.date or self.title):
            raise ValueError("a fix needs an author, date or title")
        return self


class FixBatch(BaseModel):
    batch: str
    fixes: list[ItemFix]


def load(paths: Iterable[Path], expected: dict[str, set[str]]) -> tuple[dict[str, ItemFix], list[str]]:
    """Item key -> fix, and problems (bad files, items missing from or foreign to their batch)."""
    out: dict[str, ItemFix] = {}
    problems: list[str] = []
    for p in sorted(paths):
        try:
            fb = FixBatch.model_validate(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:  # report every bad file, not just the first
            problems.append(f"{p.name}: {e}")
            continue
        given = expected.get(fb.batch, set())
        seen = {f.item for f in fb.fixes}
        if extra := sorted(seen - given):
            problems.append(f"{fb.batch}: items not in this batch: {', '.join(extra)}")
        if missing := sorted(given - seen):
            problems.append(f"{fb.batch}: items with no fix: {', '.join(missing)}")
        for f in fb.fixes:
            out[f.item] = f
    return out, problems
