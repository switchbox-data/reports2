"""Tests for lib.rates_analysis.seasonal_mc."""

from __future__ import annotations

import math

import polars as pl
import pytest

from lib.rates_analysis.seasonal_mc import (
    WINTER_MONTHS,
    build_seasonal_split_mc_8760,
    build_seasonal_split_mc_grid,
    cairo_8760_timestamps,
    winter_cost_share,
)


def _synthetic_load(year: int = 2025) -> pl.DataFrame:
    """Distinct hourly loads with a summer afternoon peak and a winter morning peak."""
    ts = cairo_8760_timestamps(year)
    loads = []
    for i, t in enumerate(ts.to_list()):
        seasonal = 1500 * math.cos(2 * math.pi * (t.timetuple().tm_yday - 200) / 365)
        daily = 400 * math.sin(2 * math.pi * (t.hour - 8) / 24)
        loads.append(3000 + abs(seasonal) + daily + i * 1e-6)
    return pl.DataFrame({"timestamp": ts, "load_mw": loads})


def _generator_top_n(load: pl.DataFrame, n_hours: int, annual: float) -> pl.Series:
    """The rate-design-platform rule: top-N hours, load / sum(top-N load)."""
    top = load.sort("load_mw", descending=True).head(n_hours)
    total = float(top["load_mw"].sum())
    peak = set(top["timestamp"].to_list())
    return pl.Series(
        [
            annual * v / total if t in peak else 0.0
            for t, v in zip(load["timestamp"].to_list(), load["load_mw"].to_list(), strict=True)
        ]
    )


def _max_abs_diff(a: pl.Series, b: pl.Series) -> float:
    return max(abs(x - y) for x, y in zip(a.to_list(), b.to_list(), strict=True))


def test_cairo_grid_drops_dec_31_in_leap_years():
    ts = cairo_8760_timestamps(2024)
    assert ts.len() == 8760
    last = ts.to_list()[-1]
    assert (last.month, last.day, last.hour) == (12, 30, 23)
    assert cairo_8760_timestamps(2025).len() == 8760


def test_no_winter_share_reproduces_generator_rule():
    load = _synthetic_load()
    profile = build_seasonal_split_mc_8760(load, 36.0, 100, None)
    expected = _generator_top_n(load, 100, 36.0)
    assert _max_abs_diff(profile["mc_per_kwh"], expected) < 1e-12


@pytest.mark.parametrize("split", ["cost", "hours"])
@pytest.mark.parametrize("x", [0.0, 0.4, 0.46, 1.0])
def test_annual_total_preserved(split, x):
    profile = build_seasonal_split_mc_8760(_synthetic_load(), 57.74, 150, x, split=split)
    assert profile.height == 8760
    assert profile["mc_per_kwh"].sum() == pytest.approx(57.74, rel=1e-12)


@pytest.mark.parametrize("x", [0.0, 0.4, 0.46, 1.0])
def test_cost_split_puts_exactly_x_of_cost_in_winter(x):
    profile = build_seasonal_split_mc_8760(_synthetic_load(), 36.0, 100, x)
    assert winter_cost_share(profile, "mc_per_kwh") == pytest.approx(x, abs=1e-12)
    winter = profile.filter(pl.col("timestamp").dt.month().is_in(list(WINTER_MONTHS)))
    summer = profile.filter(~pl.col("timestamp").dt.month().is_in(list(WINTER_MONTHS)))
    assert (winter["mc_per_kwh"] > 0).sum() == (100 if x > 0 else 0)
    assert (summer["mc_per_kwh"] > 0).sum() == (100 if x < 1 else 0)


def test_cost_split_is_linear_mix_of_seasonal_profiles():
    load = _synthetic_load()
    winter = build_seasonal_split_mc_8760(load, 36.0, 100, 1.0)["mc_per_kwh"]
    summer = build_seasonal_split_mc_8760(load, 36.0, 100, 0.0)["mc_per_kwh"]
    mixed = build_seasonal_split_mc_8760(load, 36.0, 100, 0.4)["mc_per_kwh"]
    assert _max_abs_diff(mixed, 0.4 * winter + 0.6 * summer) < 1e-12


def test_hours_split_uses_n_hours_with_rounded_winter_count():
    profile = build_seasonal_split_mc_8760(_synthetic_load(), 36.0, 100, 0.46, split="hours")
    nonzero = profile.filter(pl.col("mc_per_kwh") > 0)
    assert nonzero.height == 100
    assert nonzero.filter(pl.col("timestamp").dt.month().is_in(list(WINTER_MONTHS))).height == 46


def test_full_winter_identical_under_both_splits():
    load = _synthetic_load()
    by_cost = build_seasonal_split_mc_8760(load, 36.0, 100, 1.0, split="cost")
    by_hours = build_seasonal_split_mc_8760(load, 36.0, 100, 1.0, split="hours")
    assert _max_abs_diff(by_cost["mc_per_kwh"], by_hours["mc_per_kwh"]) < 1e-12


def test_winter_rank_load_moves_winter_hours_only():
    load = _synthetic_load()
    rank = load.with_columns(
        pl.when(pl.col("timestamp").dt.hour() == 3).then(pl.col("load_mw") * 10).otherwise(pl.col("load_mw"))
    )
    profile = build_seasonal_split_mc_8760(load, 36.0, 100, 0.5, winter_rank_load=rank)
    winter = profile.filter(
        pl.col("timestamp").dt.month().is_in(list(WINTER_MONTHS)),
        pl.col("mc_per_kwh") > 0,
    )
    assert set(winter["timestamp"].dt.hour().to_list()) == {3}
    base = build_seasonal_split_mc_8760(load, 36.0, 100, 0.5)
    summer = ~pl.col("timestamp").dt.month().is_in(list(WINTER_MONTHS))
    assert profile.filter(summer)["mc_per_kwh"].equals(base.filter(summer)["mc_per_kwh"])


def test_grid_stacks_one_block_per_share():
    grid = build_seasonal_split_mc_grid(_synthetic_load(), 36.0, 100, [0.4, 1.0])
    assert grid.height == 2 * 8760
    totals = grid.group_by("winter_share").agg(pl.col("mc_per_kwh").sum())
    assert totals["mc_per_kwh"].to_list() == pytest.approx([36.0, 36.0])


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"winter_share": 1.2}, "winter_share"),
        ({"winter_share": 0.4, "split": "peak"}, "split"),
        ({"winter_share": 0.4, "n_hours": 0}, "n_hours"),
        ({"winter_share": 0.4, "n_hours": 6000}, "eligible hours"),
    ],
)
def test_invalid_arguments_raise(kwargs, message):
    args = {"load": _synthetic_load(), "annual_cost_kw_yr": 36.0, "n_hours": 100} | kwargs
    with pytest.raises(ValueError, match=message):
        build_seasonal_split_mc_8760(**args)


def test_short_load_raises():
    with pytest.raises(ValueError, match="8760"):
        build_seasonal_split_mc_8760(_synthetic_load().head(100), 36.0, 10, 0.4)
