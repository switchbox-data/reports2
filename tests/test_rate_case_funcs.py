"""Unit tests for lib.rates_analysis.rate_case_funcs."""

from __future__ import annotations

import math

import polars as pl
import pytest

from lib.rates_analysis.rate_case_funcs import quadrant_pcts, weighted_range_pcts

QUADRANTS = [
    ("savings > $1k", -math.inf, -1000.0),
    ("savings $0-1k", -1000.0, 0.0),
    ("losses $0-1k", 0.0, 1000.0),
    ("losses > $1k", 1000.0, math.inf),
]


def test_weighted_range_pcts_partitions_known_weights() -> None:
    df = pl.DataFrame(
        {
            "bill_change": [-1500.0, -500.0, 500.0, 1500.0],
            "weight": [1.0, 1.0, 2.0, 1.0],
        }
    )
    pct = weighted_range_pcts(df, value_col="bill_change", ranges=QUADRANTS)
    assert list(pct) == [
        "savings > $1k",
        "savings $0-1k",
        "losses $0-1k",
        "losses > $1k",
    ]
    assert pct["savings > $1k"] == pytest.approx(20.0)
    assert pct["savings $0-1k"] == pytest.approx(20.0)
    assert pct["losses $0-1k"] == pytest.approx(40.0)
    assert pct["losses > $1k"] == pytest.approx(20.0)
    assert sum(pct.values()) == pytest.approx(100.0)


def test_weighted_range_pcts_zero_weight() -> None:
    df = pl.DataFrame({"bill_change": [100.0], "weight": [0.0]})
    pct = weighted_range_pcts(
        df,
        value_col="bill_change",
        ranges=[
            ("low", -math.inf, 0.0),
            ("mid", 0.0, 200.0),
            ("high", 200.0, math.inf),
        ],
    )
    assert pct == {"low": 0.0, "mid": 0.0, "high": 0.0}


def test_weighted_range_pcts_rejects_duplicate_labels() -> None:
    df = pl.DataFrame({"bill_change": [1.0], "weight": [1.0]})
    with pytest.raises(ValueError, match="duplicates: \\['same'\\]"):
        weighted_range_pcts(
            df,
            value_col="bill_change",
            ranges=[
                ("same", -math.inf, 0.0),
                ("same", 0.0, 1.0),
                ("high", 1.0, math.inf),
            ],
        )


def test_quadrant_pcts_wrapper_uses_delta_column() -> None:
    df = pl.DataFrame(
        {
            "delta": [-1500.0, -500.0, 500.0, 1500.0],
            "weight": [1.0, 1.0, 2.0, 1.0],
        }
    )
    pct = quadrant_pcts(df)
    assert pct["savings > $1k"] == pytest.approx(20.0)
    assert pct["losses $0-1k"] == pytest.approx(40.0)


def test_weighted_range_pcts_five_bins() -> None:
    df = pl.DataFrame(
        {
            "bill_change": [-2500.0, -1500.0, -500.0, 500.0, 1500.0],
            "weight": [1.0, 1.0, 1.0, 1.0, 1.0],
        }
    )
    pct = weighted_range_pcts(
        df,
        value_col="bill_change",
        ranges=[
            ("save > $2k", -math.inf, -2000.0),
            ("save $1k-2k", -2000.0, -1000.0),
            ("save $0-1k", -1000.0, 0.0),
            ("lose $0-1k", 0.0, 1000.0),
            ("lose > $1k", 1000.0, math.inf),
        ],
    )
    assert list(pct) == [
        "save > $2k",
        "save $1k-2k",
        "save $0-1k",
        "lose $0-1k",
        "lose > $1k",
    ]
    assert all(v == pytest.approx(20.0) for v in pct.values())
