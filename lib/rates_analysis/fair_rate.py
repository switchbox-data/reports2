"""Derive fair delivery rates from CAIRO default-run overpayment data.

The "fair rate" sets the delivery volumetric rate so that the weighted-average
incremental delivery revenue from homes switching to heat pumps equals their
weighted-average incremental delivery marginal cost.  The fixed (customer)
charge is unchanged from the base rate.

Two variants:

- **Fair flat rate**: a single volumetric rate for all months.

    r' = avg(delta_MC) / avg(delta_kWh)

- **Fair seasonal rate**: summer rate unchanged at the base rate; winter rate
  set so the *annual* overpayment is zero (the full correction is concentrated
  in winter).

    r_win = (avg(delta_MC_annual) - r_base * avg(delta_kWh_summer))
            / avg(delta_kWh_winter)

Both rates can be decomposed into ``distribution + riders`` following the
tariff summary convention (riders are a pass-through, unchanged across rates).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FairFlatRate:
    """Result of deriving a fair flat delivery rate."""

    delivery_total: float
    """r' = avg(delta_MC) / avg(delta_kWh), in $/kWh."""

    distribution: float
    """delivery_total - riders, in $/kWh."""

    riders: float
    """Pass-through rider total, unchanged from the base rate, in $/kWh."""


@dataclass(frozen=True, slots=True)
class FairSeasonalRate:
    """Result of deriving a fair seasonal delivery rate."""

    winter_delivery_total: float
    """r_win that zeroes annual overpayment, in $/kWh."""

    winter_distribution: float
    """winter_delivery_total - riders, in $/kWh."""

    summer_delivery_total: float
    """Base rate, unchanged, in $/kWh."""

    summer_distribution: float
    """summer_delivery_total - riders, in $/kWh."""

    riders: float
    """Pass-through rider total, unchanged from the base rate, in $/kWh."""


# ---------------------------------------------------------------------------
# Derivation functions (pure math, no I/O)
# ---------------------------------------------------------------------------


def derive_fair_flat_rate(
    *,
    avg_delta_mc: float,
    avg_delta_kwh: float,
    base_delivery_rate: float,
    riders_total: float,
) -> FairFlatRate:
    """Derive a fair flat delivery volumetric rate.

    Parameters
    ----------
    avg_delta_mc
        Weighted-average incremental delivery marginal cost ($/yr) over the
        fair-rate population (pre-to-post HP retrofit).
    avg_delta_kwh
        Weighted-average incremental grid kWh (kWh/yr) over the same
        population.
    base_delivery_rate
        The current (Rate 1) delivery volumetric rate in $/kWh.  Used only for
        reference — the fair rate is derived independently.
    riders_total
        Shared riders total in $/kWh (pass-through, unchanged).

    Returns
    -------
    FairFlatRate
        The derived rate and its decomposition.

    Raises
    ------
    ValueError
        If ``avg_delta_kwh`` is zero (no incremental consumption to allocate
        costs over).
    """
    if avg_delta_kwh == 0.0:
        msg = "avg_delta_kwh must be non-zero (no incremental kWh to allocate costs over)"
        raise ValueError(msg)

    r_prime = avg_delta_mc / avg_delta_kwh

    return FairFlatRate(
        delivery_total=r_prime,
        distribution=r_prime - riders_total,
        riders=riders_total,
    )


def derive_fair_seasonal_rate(
    *,
    avg_delta_mc_annual: float,
    avg_delta_kwh_winter: float,
    avg_delta_kwh_summer: float,
    base_delivery_rate: float,
    riders_total: float,
) -> FairSeasonalRate:
    """Derive a fair seasonal delivery rate (summer unchanged, winter adjusted).

    The annual overpayment is recovered entirely in winter: the summer rate
    stays at the base (Rate 1) level, and the winter rate is set so that
    ``r_win * avg_delta_kwh_winter + r_base * avg_delta_kwh_summer == avg_delta_mc_annual``.

    Parameters
    ----------
    avg_delta_mc_annual
        Weighted-average incremental delivery marginal cost ($/yr), annual
        total, over the fair-rate population.
    avg_delta_kwh_winter
        Weighted-average incremental grid kWh during winter months (kWh/yr).
    avg_delta_kwh_summer
        Weighted-average incremental grid kWh during summer months (kWh/yr).
    base_delivery_rate
        The current (Rate 1) delivery volumetric rate in $/kWh, used as the
        summer rate.
    riders_total
        Shared riders total in $/kWh (pass-through, unchanged).

    Returns
    -------
    FairSeasonalRate
        The derived seasonal rates and their decomposition.

    Raises
    ------
    ValueError
        If ``avg_delta_kwh_winter`` is zero (cannot concentrate correction in
        winter with no incremental winter kWh).
    """
    if avg_delta_kwh_winter == 0.0:
        msg = (
            "avg_delta_kwh_winter must be non-zero "
            "(cannot concentrate annual correction in winter with no incremental winter kWh)"
        )
        raise ValueError(msg)

    r_winter = (avg_delta_mc_annual - base_delivery_rate * avg_delta_kwh_summer) / avg_delta_kwh_winter

    return FairSeasonalRate(
        winter_delivery_total=r_winter,
        winter_distribution=r_winter - riders_total,
        summer_delivery_total=base_delivery_rate,
        summer_distribution=base_delivery_rate - riders_total,
        riders=riders_total,
    )


# ---------------------------------------------------------------------------
# YAML output (custom-rate format compatible with create_custom_*_tariff.py)
# ---------------------------------------------------------------------------


def write_custom_rate_yaml(
    path: Path,
    rate: FairFlatRate | FairSeasonalRate,
    *,
    label: str,
    utility: str,
    fixed_charge: float,
    supply_rate: float,
    winter_months: list[int] | None = None,
    provenance: dict[str, str] | None = None,
) -> Path:
    """Write a custom-rate YAML file for conversion to URDB JSON.

    For a :class:`FairFlatRate`, writes a flat custom-rate YAML compatible with
    ``create_custom_flat_tariff.py``.  For a :class:`FairSeasonalRate`, writes a
    seasonal custom-rate YAML compatible with ``create_custom_seasonal_tariff.py``.

    Parameters
    ----------
    path
        Output file path.
    rate
        The derived rate (flat or seasonal).
    label
        Tariff label (e.g. ``icos_fair_flat``).
    utility
        Utility identifier (e.g. ``ct_eversource``).
    fixed_charge
        Customer charge in $/month, unchanged from the base rate.
    supply_rate
        Supply commodity rate in $/kWh.
    winter_months
        Required for seasonal rates; the 1-indexed month numbers for winter.
    provenance
        Optional dict of provenance metadata (batch, population, date) to
        include as a YAML comment header.

    Returns
    -------
    Path
        The written file path.
    """
    lines: list[str] = []

    if provenance:
        for key, val in provenance.items():
            lines.append(f"# {key}: {val}")
        lines.append("")

    if isinstance(rate, FairFlatRate):
        doc: dict[str, Any] = {
            "label": label,
            "utility": utility,
            "fixed_charge": round(fixed_charge, 2),
            "delivery": {
                "distribution": round(rate.distribution, 5),
                "riders": round(rate.riders, 5),
            },
            "supply_rate": round(supply_rate, 5),
        }
    elif isinstance(rate, FairSeasonalRate):
        if winter_months is None:
            msg = "winter_months is required for seasonal rates"
            raise ValueError(msg)
        summer_months = [m for m in range(1, 13) if m not in winter_months]
        doc = {
            "label": label,
            "utility": utility,
            "fixed_charge": round(fixed_charge, 2),
            "seasons": {
                "winter": {
                    "months": sorted(winter_months, key=lambda m: (m % 12, m)),
                    "delivery": {
                        "distribution": round(rate.winter_distribution, 5),
                        "riders": round(rate.riders, 5),
                    },
                },
                "summer": {
                    "months": sorted(summer_months),
                    "delivery": {
                        "distribution": round(rate.summer_distribution, 5),
                        "riders": round(rate.riders, 5),
                    },
                },
            },
            "supply_rate": round(supply_rate, 5),
        }
    else:
        msg = f"Unsupported rate type: {type(rate)}"
        raise TypeError(msg)

    path.parent.mkdir(parents=True, exist_ok=True)
    comment_header = "\n".join(lines)
    yaml_body = yaml.dump(doc, default_flow_style=False, sort_keys=False)
    content = f"{comment_header}{yaml_body}" if comment_header else yaml_body
    path.write_text(content, encoding="utf-8")
    return path
