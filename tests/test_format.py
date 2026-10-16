"""Tests for the narrative formatting helpers in lib.format."""

from __future__ import annotations

from lib.format import month_list, pct


def test_pct_rounds_to_whole_percent_by_default() -> None:
    assert pct(0.43) == "43%"
    assert pct(0.625) == "62%"


def test_pct_honors_accuracy() -> None:
    assert pct(0.1234, accuracy=1) == "12.3%"


def test_month_list_three_months_uses_oxford_comma() -> None:
    assert month_list(["Jun", "Jul", "Aug"]) == "June, July, and August"


def test_month_list_two_months_uses_and() -> None:
    assert month_list(["Jul", "Aug"]) == "July and August"


def test_month_list_single_month() -> None:
    assert month_list(["Jul"]) == "July"
