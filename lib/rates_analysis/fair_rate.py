"""Derive fair delivery rates from CAIRO default-run overpayment data.

The "fair rate" sets the delivery volumetric rate so that, for the average
fossil-fuel-heated building, the delivery bill after installing a heat pump
equals the delivery bill before the retrofit plus any incremental delivery
marginal cost.  The fixed (customer) charge is unchanged from the base rate.

    r_new * avg(kWh_after) = r_base * avg(kWh_before) + avg(delta_MC)

Two variants:

- **Fair flat rate**: a single volumetric rate for all months.

    r_new = (r_base * avg(kWh_before) + avg(delta_MC)) / avg(kWh_after)

- **Fair seasonal rate**: summer rate unchanged at the base rate; winter rate
  set so the *annual* constraint holds (the full adjustment is concentrated
  in winter).

    r_win = (r_base * avg(kWh_before) + avg(delta_MC_annual)
             - r_base * avg(kWh_after_summer)) / avg(kWh_after_winter)

Both rates are decomposed into ``distribution + transmission + other_riders``.
The discount (difference between the base rate and the fair rate) is applied
**proportionally** to distribution and transmission, leaving other riders
(CTA, SBC, CAM, RE, FMCC-Del) unchanged.
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
    """r_new = (r_base * avg(kWh_before) + avg(delta_MC)) / avg(kWh_after), in $/kWh."""

    distribution: float
    """Proportional share of the discountable portion, in $/kWh."""

    transmission: float
    """Proportional share of the discountable portion, in $/kWh."""

    other_riders: float
    """Non-discountable riders, unchanged from the base rate, in $/kWh."""


@dataclass(frozen=True, slots=True)
class FairSeasonalRate:
    """Result of deriving a fair seasonal delivery rate."""

    winter_delivery_total: float
    """r_win that satisfies the annual constraint, in $/kWh."""

    winter_distribution: float
    """Proportional share of the winter discountable portion, in $/kWh."""

    winter_transmission: float
    """Proportional share of the winter discountable portion, in $/kWh."""

    summer_delivery_total: float
    """Base rate, unchanged, in $/kWh."""

    summer_distribution: float
    """Base distribution rate, unchanged, in $/kWh."""

    summer_transmission: float
    """Base transmission rate, unchanged, in $/kWh."""

    other_riders: float
    """Non-discountable riders, unchanged from the base rate, in $/kWh."""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _proportional_decomposition(
    delivery_total: float,
    base_distribution: float,
    base_transmission: float,
    other_riders: float,
) -> tuple[float, float]:
    """Split the discountable portion of a delivery rate proportionally.

    Returns (new_distribution, new_transmission).
    """
    discountable = delivery_total - other_riders
    dist_share = base_distribution / (base_distribution + base_transmission)
    return dist_share * discountable, (1 - dist_share) * discountable


# ---------------------------------------------------------------------------
# Derivation functions (pure math, no I/O)
# ---------------------------------------------------------------------------


def derive_fair_flat_rate(
    *,
    avg_delta_mc: float,
    avg_kwh_before: float,
    avg_kwh_after: float,
    base_delivery_rate: float,
    base_distribution: float,
    base_transmission: float,
    other_riders: float,
) -> FairFlatRate:
    """Derive a fair flat delivery volumetric rate.

    The rate is set so that, on average over the fair-rate population:

        r_new * avg(kWh_after) = r_base * avg(kWh_before) + avg(delta_MC)

    The discount relative to the base rate is distributed proportionally
    across distribution and transmission; other riders pass through unchanged.

    Parameters
    ----------
    avg_delta_mc
        Weighted-average incremental delivery marginal cost ($/yr) over the
        fair-rate population (pre-to-post HP retrofit).
    avg_kwh_before
        Weighted-average annual grid kWh *before* the HP retrofit.
    avg_kwh_after
        Weighted-average annual grid kWh *after* the HP retrofit.
    base_delivery_rate
        The current (Rate 1) total delivery volumetric rate in $/kWh.
    base_distribution
        The current (Rate 1) distribution component in $/kWh.
    base_transmission
        The current (Rate 1) transmission component in $/kWh.
    other_riders
        Non-discountable riders total in $/kWh (pass-through, unchanged).

    Returns
    -------
    FairFlatRate
        The derived rate and its decomposition.

    Raises
    ------
    ValueError
        If ``avg_kwh_after`` is zero (no post-retrofit consumption to price).
    """
    if avg_kwh_after == 0.0:
        msg = "avg_kwh_after must be non-zero (no post-retrofit consumption to price)"
        raise ValueError(msg)

    r_new = (base_delivery_rate * avg_kwh_before + avg_delta_mc) / avg_kwh_after
    new_dist, new_tx = _proportional_decomposition(
        r_new,
        base_distribution,
        base_transmission,
        other_riders,
    )

    return FairFlatRate(
        delivery_total=r_new,
        distribution=new_dist,
        transmission=new_tx,
        other_riders=other_riders,
    )


def derive_fair_seasonal_rate(
    *,
    avg_delta_mc_annual: float,
    avg_kwh_before_annual: float,
    avg_kwh_after_winter: float,
    avg_kwh_after_summer: float,
    base_delivery_rate: float,
    base_distribution: float,
    base_transmission: float,
    other_riders: float,
) -> FairSeasonalRate:
    """Derive a fair seasonal delivery rate (summer unchanged, winter adjusted).

    The annual constraint is satisfied entirely via the winter rate: the summer
    rate stays at the base (Rate 1) level, and the winter rate is set so that:

        r_win * avg(kWh_after_winter) + r_base * avg(kWh_after_summer)
            = r_base * avg(kWh_before) + avg(delta_MC_annual)

    The discount on the winter rate is distributed proportionally across
    distribution and transmission; other riders pass through unchanged.

    Parameters
    ----------
    avg_delta_mc_annual
        Weighted-average incremental delivery marginal cost ($/yr), annual
        total, over the fair-rate population.
    avg_kwh_before_annual
        Weighted-average annual grid kWh *before* the HP retrofit.
    avg_kwh_after_winter
        Weighted-average grid kWh during winter months *after* the retrofit.
    avg_kwh_after_summer
        Weighted-average grid kWh during summer months *after* the retrofit.
    base_delivery_rate
        The current (Rate 1) delivery volumetric rate in $/kWh, used as the
        summer rate.
    base_distribution
        The current (Rate 1) distribution component in $/kWh.
    base_transmission
        The current (Rate 1) transmission component in $/kWh.
    other_riders
        Non-discountable riders total in $/kWh (pass-through, unchanged).

    Returns
    -------
    FairSeasonalRate
        The derived seasonal rates and their decomposition.

    Raises
    ------
    ValueError
        If ``avg_kwh_after_winter`` is zero (cannot concentrate adjustment in
        winter with no post-retrofit winter kWh).
    """
    if avg_kwh_after_winter == 0.0:
        msg = (
            "avg_kwh_after_winter must be non-zero "
            "(cannot concentrate annual adjustment in winter with no post-retrofit winter kWh)"
        )
        raise ValueError(msg)

    r_winter = (
        base_delivery_rate * avg_kwh_before_annual + avg_delta_mc_annual - base_delivery_rate * avg_kwh_after_summer
    ) / avg_kwh_after_winter

    win_dist, win_tx = _proportional_decomposition(
        r_winter,
        base_distribution,
        base_transmission,
        other_riders,
    )

    return FairSeasonalRate(
        winter_delivery_total=r_winter,
        winter_distribution=win_dist,
        winter_transmission=win_tx,
        summer_delivery_total=base_delivery_rate,
        summer_distribution=base_distribution,
        summer_transmission=base_transmission,
        other_riders=other_riders,
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

    Delivery is decomposed into ``distribution``, ``transmission``, and
    ``other_riders``.  The downstream tariff scripts sum all ``delivery`` dict
    values regardless of key names, so this is backward-compatible.

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
                "transmission": round(rate.transmission, 5),
                "other_riders": round(rate.other_riders, 5),
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
                        "transmission": round(rate.winter_transmission, 5),
                        "other_riders": round(rate.other_riders, 5),
                    },
                },
                "summer": {
                    "months": sorted(summer_months),
                    "delivery": {
                        "distribution": round(rate.summer_distribution, 5),
                        "transmission": round(rate.summer_transmission, 5),
                        "other_riders": round(rate.other_riders, 5),
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
