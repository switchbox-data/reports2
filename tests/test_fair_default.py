"""Tests for the V^0-based fair-default fixed-charge-only solver.

Two cases:

1. **Flat baseline** — V^0 = r · kWh, so the V^0 formula must reproduce the
   RDP kWh-based result exactly.  Uses the same 4-building synthetic fixture as
   ``rate-design-platform/tests/test_compute_fair_default_inputs.py``.

2. **Seasonal baseline** — winter and summer rates differ, so V^0 and kWh are
   *not* proportional across subclasses with different load shapes.  The test
   verifies that F* from V^0 satisfies C1 and C2, and that the kWh shortcut
   would give a *different* (wrong) answer.
"""

from __future__ import annotations

import math

import pytest

from lib.rates_analysis.fair_default import fair_default_fixed_charge_only

MONTHS = 12.0


def test_flat_baseline_matches_rdp() -> None:
    """V^0 formula reproduces the RDP kWh-based result for a flat tariff."""
    f0 = 2.0
    rate = 0.50

    loads = {
        1: (100.0, 100.0, True, 20.0),
        2: (200.0, 100.0, True, 30.0),
        3: (100.0, 300.0, False, 0.0),
        4: (100.0, 500.0, False, 0.0),
    }

    class_revenue = 0.0
    hp_revenue = 0.0
    hp_cross_subsidy = 0.0
    n_cls = 0.0
    n_hp = 0.0

    for _bldg, (w_kwh, s_kwh, is_hp, bat) in loads.items():
        bill = MONTHS * f0 + rate * (w_kwh + s_kwh)
        class_revenue += bill
        n_cls += 1.0
        if is_hp:
            hp_revenue += bill
            hp_cross_subsidy += bat
            n_hp += 1.0

    result = fair_default_fixed_charge_only(
        class_revenue=class_revenue,
        class_customers=n_cls,
        subclass_revenue=hp_revenue,
        subclass_customers=n_hp,
        subclass_cross_subsidy=hp_cross_subsidy,
        base_fixed_charge=f0,
    )

    assert result.fixed_charge == pytest.approx(-4.25)

    rr = class_revenue
    tc_hp = hp_revenue - hp_cross_subsidy
    assert (MONTHS * result.fixed_charge * n_cls + result.implied_lambda * (rr - MONTHS * f0 * n_cls)) == pytest.approx(
        rr
    )
    assert (
        MONTHS * result.fixed_charge * n_hp + result.implied_lambda * (hp_revenue - MONTHS * f0 * n_hp)
    ) == pytest.approx(tc_hp)


def test_seasonal_baseline_differs_from_kwh_shortcut() -> None:
    """When rates differ by season, V^0-based F* != kWh-based F*."""
    f0 = 10.0
    r_winter = 0.10
    r_summer = 0.05

    loads = {
        1: (800.0, 200.0, True, 15.0),
        2: (600.0, 400.0, True, 10.0),
        3: (200.0, 800.0, False, -10.0),
        4: (100.0, 600.0, False, -15.0),
    }

    class_revenue = 0.0
    hp_revenue = 0.0
    hp_cross_subsidy = 0.0
    n_cls = 0.0
    n_hp = 0.0
    kwh_cls = 0.0
    kwh_hp = 0.0

    for _bldg, (w_kwh, s_kwh, is_hp, bat) in loads.items():
        bill = MONTHS * f0 + r_winter * w_kwh + r_summer * s_kwh
        kwh = w_kwh + s_kwh
        class_revenue += bill
        kwh_cls += kwh
        n_cls += 1.0
        if is_hp:
            hp_revenue += bill
            hp_cross_subsidy += bat
            kwh_hp += kwh
            n_hp += 1.0

    result = fair_default_fixed_charge_only(
        class_revenue=class_revenue,
        class_customers=n_cls,
        subclass_revenue=hp_revenue,
        subclass_customers=n_hp,
        subclass_cross_subsidy=hp_cross_subsidy,
        base_fixed_charge=f0,
    )

    rr = class_revenue
    tc_hp = hp_revenue - hp_cross_subsidy
    v0_cls = rr - MONTHS * f0 * n_cls
    v0_hp = hp_revenue - MONTHS * f0 * n_hp

    assert (MONTHS * result.fixed_charge * n_cls + result.implied_lambda * v0_cls) == pytest.approx(rr)
    assert (MONTHS * result.fixed_charge * n_hp + result.implied_lambda * v0_hp) == pytest.approx(tc_hp)

    kwh_denom = n_cls * kwh_hp - n_hp * kwh_cls
    f_kwh = (rr * kwh_hp - tc_hp * kwh_cls) / (MONTHS * kwh_denom)

    assert not math.isclose(result.fixed_charge, f_kwh, rel_tol=1e-6), (
        "V^0 and kWh formulas should differ for seasonal baselines"
    )

    c1_kwh = MONTHS * f_kwh * n_cls
    c2_kwh = MONTHS * f_kwh * n_hp
    lambda_kwh = (rr - c1_kwh) / v0_cls
    bill_hp_kwh = c2_kwh + lambda_kwh * v0_hp
    assert not math.isclose(bill_hp_kwh, tc_hp, rel_tol=1e-6), (
        "kWh formula should NOT satisfy C2 for seasonal baselines"
    )


def test_degenerate_raises() -> None:
    """Degenerate system (identical per-customer V^0) raises ValueError."""
    with pytest.raises(ValueError, match="Degenerate"):
        fair_default_fixed_charge_only(
            class_revenue=1200.0,
            class_customers=4.0,
            subclass_revenue=600.0,
            subclass_customers=2.0,
            subclass_cross_subsidy=0.0,
            base_fixed_charge=0.0,
        )
