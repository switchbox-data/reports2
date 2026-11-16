"""Distribution of the sum of two independent Gaussian kernel densities.

X and Y are independent scalar random variables, each a Gaussian kernel
density on its own sample. The density of Z = X + Y is the convolution of
the two densities. For Gaussian kernels that convolution is a mixture with
one equally weighted component at every pairwise sum of sample points, and
with variance equal to the sum of the two bandwidths squared.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr
from scipy.stats import gaussian_kde

_SQRT_2PI = float(np.sqrt(2.0 * np.pi))
_Z_CHUNK = 512
_CENTER_CHUNK = 8_192


def _as_kde(obj: np.ndarray | gaussian_kde, bw_method: str | float | Callable | None) -> gaussian_kde:
    if isinstance(obj, gaussian_kde):
        if bw_method is not None:
            raise ValueError("bw_method applies only when SumKDE fits the samples itself")
        return obj
    x = np.asarray(obj, dtype=float).ravel()
    if x.size < 2:
        raise ValueError("a Gaussian KDE needs at least two observations")
    if bw_method is None:
        return gaussian_kde(x)
    return gaussian_kde(x, bw_method=bw_method)


def _point_moments(kde: gaussian_kde) -> tuple[float, float, float]:
    """Mean, population variance of the sample points, and kernel variance h^2."""
    x = np.asarray(kde.dataset, dtype=float).ravel()
    mean = float(x.mean())
    point_var = float(np.mean((x - mean) ** 2))
    bandwidth_var = float(np.asarray(kde.covariance, dtype=float).reshape(-1)[0])
    return mean, point_var, bandwidth_var


class SumKDE:
    """Distribution of Z = X + Y for independent Gaussian KDEs X and Y.

    Parameters
    ----------
    a, b:
        Sample arrays, or existing ``gaussian_kde`` objects. Arrays are fit
        with ``scipy.stats.gaussian_kde``. ``gaussian_kde.covariance`` is the
        bandwidth squared.
    bw_method:
        Passed through to ``gaussian_kde`` when ``a`` or ``b`` is an array.
    method:
        ``"exact"`` evaluates the pairwise mixture. ``"mc"`` draws ``mc_size``
        sums and fits a Gaussian KDE to them. ``"auto"`` uses the exact mixture
        when the number of pairs is at most ``pairwise_threshold``.
    """

    def __init__(
        self,
        a: np.ndarray | gaussian_kde,
        b: np.ndarray | gaussian_kde,
        *,
        bw_method: str | float | Callable | None = None,
        method: str = "auto",
        pairwise_threshold: float = 5e6,
        mc_size: int = 200_000,
        rng: np.random.Generator | int | None = None,
    ) -> None:
        if method not in {"auto", "exact", "mc"}:
            raise ValueError("method must be 'auto', 'exact', or 'mc'")
        if mc_size < 2:
            raise ValueError("mc_size must be at least 2")
        self._a = _as_kde(a, bw_method)
        self._b = _as_kde(b, bw_method)
        self._mean_a, self._point_var_a, self._h2_a = _point_moments(self._a)
        self._mean_b, self._point_var_b, self._h2_b = _point_moments(self._b)
        n = int(self._a.n)
        m = int(self._b.n)
        self._n_pairs = n * m
        if method == "auto":
            method = "exact" if self._n_pairs <= pairwise_threshold else "mc"
        self.method = method
        self._mc_size = int(mc_size)
        self._rng = np.random.default_rng(rng)
        self._centers: np.ndarray | None = None
        self._mc_kde: gaussian_kde | None = None
        self._component_std = float(np.sqrt(self._h2_a + self._h2_b))

    def mean(self) -> float:
        """Analytic mean, mean(X) + mean(Y)."""
        return self._mean_a + self._mean_b

    def var(self) -> float:
        """Analytic variance of Z.

        ``var(points of X) + var(points of Y) + h_X^2 + h_Y^2``. The point
        variances divide by the sample size, which is the variance of the
        equally weighted mixture of centers. Each kernel variance comes from
        ``gaussian_kde.covariance``.
        """
        return self._point_var_a + self._point_var_b + self._h2_a + self._h2_b

    def sample(self, size: int, rng: np.random.Generator | int | None = None) -> np.ndarray:
        """Draw ``size`` values of X + Y by sampling each density and adding."""
        if size < 0:
            raise ValueError("size must be non-negative")
        generator = np.random.default_rng(rng)
        return _sample_kde(self._a, size, generator) + _sample_kde(self._b, size, generator)

    def pdf(self, z: float | np.ndarray) -> float | np.ndarray:
        """Density of Z at scalar or array ``z``."""
        return self._evaluate(z, "pdf")

    def cdf(self, z: float | np.ndarray) -> float | np.ndarray:
        """P(Z <= z), the mean of the component normal cdfs."""
        return self._evaluate(z, "cdf")

    def prob_between(self, a: float, b: float) -> float:
        """P(a < Z < b). Zero when ``a`` is not below ``b``."""
        if b <= a:
            return 0.0
        return float(self.cdf(b) - self.cdf(a))

    def ppf(self, q: float | np.ndarray) -> float | np.ndarray:
        """Quantile, by inverting ``cdf`` with Brent's method."""
        values = np.asarray(q, dtype=float)
        scalar = values.ndim == 0
        flat = np.atleast_1d(values).ravel()
        out = np.array([self._ppf_one(float(one)) for one in flat], dtype=float)
        if scalar:
            return float(out[0])
        return out.reshape(values.shape)

    def _ppf_one(self, q: float) -> float:
        if not 0.0 < q < 1.0:
            raise ValueError("q must be strictly between 0 and 1")
        scale = float(np.sqrt(self.var()))
        if scale == 0.0:
            return self.mean()
        lo = self.mean() - 8.0 * scale
        hi = self.mean() + 8.0 * scale
        for _ in range(24):
            if float(self.cdf(lo)) < q < float(self.cdf(hi)):
                break
            lo -= 4.0 * scale
            hi += 4.0 * scale
        else:
            raise RuntimeError("could not bracket the quantile")
        return float(brentq(lambda t: float(self.cdf(t)) - q, lo, hi))

    def _evaluate(self, z: float | np.ndarray, kind: str) -> float | np.ndarray:
        values = np.asarray(z, dtype=float)
        scalar = values.ndim == 0
        flat = np.atleast_1d(values).astype(float, copy=False).ravel()
        if self.method == "mc":
            evaluated = np.asarray(self._fallback_kde().pdf(flat) if kind == "pdf" else self._fallback_cdf(flat), dtype=float)
        else:
            evaluated = self._exact(flat, kind)
        if scalar:
            return float(evaluated[0])
        return evaluated.reshape(values.shape)

    def _fallback_kde(self) -> gaussian_kde:
        if self._mc_kde is None:
            draws = self.sample(self._mc_size, rng=self._rng)
            self._mc_kde = gaussian_kde(draws)
        return self._mc_kde

    def _fallback_cdf(self, z: np.ndarray) -> np.ndarray:
        kde = self._fallback_kde()
        centers = np.asarray(kde.dataset, dtype=float).ravel()
        std = float(np.sqrt(np.asarray(kde.covariance, dtype=float).reshape(-1)[0]))
        return _mixture_stat(z, centers, std, "cdf")

    def _exact(self, z: np.ndarray, kind: str) -> np.ndarray:
        if self._component_std == 0.0:
            centers = self._pairwise_centers()
            if kind == "cdf":
                return np.array([float(np.mean(centers <= one)) for one in z], dtype=float)
            return np.zeros(z.shape, dtype=float)
        return _mixture_stat(z, self._pairwise_centers(), self._component_std, kind)

    def _pairwise_centers(self) -> np.ndarray:
        if self._centers is None:
            a = np.asarray(self._a.dataset, dtype=float).ravel()
            b = np.asarray(self._b.dataset, dtype=float).ravel()
            self._centers = (a[:, None] + b[None, :]).ravel()
        return self._centers


def _sample_kde(kde: gaussian_kde, size: int, rng: np.random.Generator) -> np.ndarray:
    x = np.asarray(kde.dataset, dtype=float).ravel()
    h = float(np.sqrt(np.asarray(kde.covariance, dtype=float).reshape(-1)[0]))
    drawn = x[rng.integers(0, x.size, size=size)]
    if h == 0.0 or size == 0:
        return drawn
    return drawn + rng.normal(0.0, h, size=size)


def added_normal_ppf(kde: gaussian_kde, loc: float, variance: float, q: float) -> float:
    """Quantile of a Gaussian KDE convolved with an independent normal.

    The normal has mean ``loc`` and variance ``variance``. A variance of zero
    shifts the KDE by ``loc``. The quantile is the exact inverse of the
    mixture cdf: each kernel, centered on one sample point, is widened by the
    added variance. This is the distribution of the KDE plus the sum of many
    independent copies of another KDE, once that sum is taken as normal with
    the other KDE's mean and variance.
    """
    if not 0.0 < q < 1.0:
        raise ValueError("q must be strictly between 0 and 1")
    if variance < 0.0:
        raise ValueError("variance must be non-negative")
    x = np.asarray(kde.dataset, dtype=float).ravel()
    h2 = float(np.asarray(kde.covariance, dtype=float).reshape(-1)[0])
    std = float(np.sqrt(h2 + variance))
    point_var = float(np.mean((x - x.mean()) ** 2))
    scale = float(np.sqrt(point_var + h2 + variance))
    center = float(x.mean() + loc)
    if scale == 0.0:
        return center

    def cdf(t: float) -> float:
        if std == 0.0:
            return float(np.mean(x + loc <= t))
        return float(ndtr((t - (x + loc)) / std).mean())

    lo = center - 8.0 * scale
    hi = center + 8.0 * scale
    for _ in range(24):
        if cdf(lo) < q < cdf(hi):
            break
        lo -= 4.0 * scale
        hi += 4.0 * scale
    else:
        raise RuntimeError("could not bracket the quantile")
    return float(brentq(lambda t: cdf(t) - q, lo, hi))


def _mixture_stat(z: np.ndarray, centers: np.ndarray, std: float, kind: str) -> np.ndarray:
    """Mean of the component normal pdfs or cdfs, evaluated in chunks."""
    out = np.empty(z.size, dtype=float)
    scale = centers.size * std * _SQRT_2PI if kind == "pdf" else float(centers.size)
    for start in range(0, z.size, _Z_CHUNK):
        zz = z[start : start + _Z_CHUNK]
        acc = np.zeros(zz.size, dtype=float)
        for c0 in range(0, centers.size, _CENTER_CHUNK):
            diff = (zz[:, None] - centers[c0 : c0 + _CENTER_CHUNK][None, :]) / std
            if kind == "pdf":
                acc += np.exp(-0.5 * diff * diff).sum(axis=1)
            else:
                acc += ndtr(diff).sum(axis=1)
        out[start : start + zz.size] = acc / scale
    return out
