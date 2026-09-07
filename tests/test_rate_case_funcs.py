"""Unit tests for lib.rates_analysis.rate_case_funcs."""

from __future__ import annotations

import polars as pl
import pytest

from lib.rates_analysis.rate_case_funcs import quadrant_pcts, weighted_range_pcts


def test_weighted_range_pcts_partitions_known_weights() -> None:
    df = pl.DataFrame(
        {
            "bill_change": [-1500.0, -500.0, 500.0, 1500.0],
            "weight": [1.0, 1.0, 2.0, 1.0],
        }
    )
    pct = weighted_range_pcts(
        df,
        value_col="bill_change",
        low_end={"savings > $1k": -1000.0},
        middle=[
            ("savings $0-1k", -1000.0, 0.0),
            ("losses $0-1k", 0.0, 1000.0),
        ],
        high_end={"losses > $1k": 1000.0},
    )
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
        low_end={"low": 0.0},
        middle=[("mid", 0.0, 200.0)],
        high_end={"high": 200.0},
    )
    assert pct == {"low": 0.0, "mid": 0.0, "high": 0.0}


def test_weighted_range_pcts_rejects_duplicate_labels() -> None:
    df = pl.DataFrame({"bill_change": [1.0], "weight": [1.0]})
    with pytest.raises(ValueError, match="duplicates: \\['same'\\]"):
        weighted_range_pcts(
            df,
            value_col="bill_change",
            low_end={"same": 0.0},
            middle=[("same", 0.0, 1.0)],
            high_end={"high": 1.0},
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


def test_weighted_range_pcts_accepts_three_middle_ranges() -> None:
    df = pl.DataFrame(
        {
            "bill_change": [-2500.0, -1500.0, -500.0, 500.0, 1500.0],
            "weight": [1.0, 1.0, 1.0, 1.0, 1.0],
        }
    )
    pct = weighted_range_pcts(
        df,
        value_col="bill_change",
        low_end={"save > $2k": -2000.0},
        middle=[
            ("save $1k-2k", -2000.0, -1000.0),
            ("save $0-1k", -1000.0, 0.0),
            ("lose $0-1k", 0.0, 1000.0),
        ],
        high_end={"lose > $1k": 1000.0},
    )
    assert list(pct) == [
        "save > $2k",
        "save $1k-2k",
        "save $0-1k",
        "lose $0-1k",
        "lose > $1k",
    ]
    assert all(v == pytest.approx(20.0) for v in pct.values())
