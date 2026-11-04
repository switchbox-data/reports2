"""The internal review list: checks a person should look at, written only to ``provenance_review.csv``."""

from __future__ import annotations

Review = list[dict[str, str]]


def flag(review: Review, check: str, item: str = "", detail: str = "") -> None:
    review.append({"check": check, "item": item, "detail": detail})
