"""Quantile of a Gaussian KDE convolved with a normal."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import numpy as np
from scipy.stats import gaussian_kde


def _load() -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "reports" / "ct_hp_rates" / "ciec_requests" / "kde_sum.py"
    spec = importlib.util.spec_from_file_location("kde_sum_under_test", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


kde_sum = _load()


def test_zero_shift_matches_the_kde_cdf() -> None:
    sample = np.random.default_rng(0).normal(100.0, 15.0, size=80)
    kde = gaussian_kde(sample)
    q = kde_sum.added_normal_ppf(kde, 0.0, 0.0, 0.9)
    assert abs(float(kde.integrate_box_1d(-np.inf, q)) - 0.9) < 1e-4


def test_constant_shift_moves_the_quantile_by_the_shift() -> None:
    sample = np.random.default_rng(1).normal(50.0, 5.0, size=40)
    kde = gaussian_kde(sample)
    q0 = kde_sum.added_normal_ppf(kde, 0.0, 0.0, 0.9)
    q1 = kde_sum.added_normal_ppf(kde, 10.0, 0.0, 0.9)
    assert abs(q1 - q0 - 10.0) < 1e-6


def test_normal_approximation_is_close_when_the_added_sample_is_nearly_normal() -> None:
    rng = np.random.default_rng(2)
    system = rng.normal(0.0, 10.0, size=40)
    change = rng.normal(1.0, 0.5, size=60)
    exact = float(kde_sum.SumKDE(system, change).ppf(0.9))
    change_kde = gaussian_kde(change)
    points = np.asarray(change_kde.dataset, dtype=float).ravel()
    point_var = float(np.mean((points - points.mean()) ** 2))
    bandwidth_var = float(np.asarray(change_kde.covariance, dtype=float).reshape(-1)[0])
    approx = kde_sum.added_normal_ppf(gaussian_kde(system), float(points.mean()), point_var + bandwidth_var, 0.9)
    assert abs(approx - exact) < 0.05
