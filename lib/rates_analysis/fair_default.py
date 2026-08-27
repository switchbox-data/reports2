"""Closed-form fair-default rate design (Strategy A: fixed_charge_only).

Implements the V^0-based Cramer system from
``rate-design-platform/context/methods/tou_and_rates/fair_default_rate_design.md``
(section 4, Strategy A).  The companion RDP solver
(``utils/mid/compute_fair_default_inputs.py::fixed_charge_only_rate_design``)
uses **kWh** in the same 2x2 system, which is equivalent only when the baseline
tariff is flat (V^0 = r * kWh, r cancels).  This module uses V^0 - the weighted
total of each customer's annual volumetric bill under the baseline tariff - so
the result is correct for seasonal, TOU, or any other baseline rate shape.

The two key constraints solved simultaneously are:

- **C1 (class revenue neutrality):** 12 F* N_cls + lambda V^0_cls = RR
- **C2 (subclass cross-subsidy elimination):** 12 F* N_hp + lambda V^0_hp = TC_hp

where lambda is the implied uniform scaling factor on all volumetric charges
and TC_hp = Bill_hp - X_hp is the heat-pump subclass's fair bill (current bill
minus cross-subsidy).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

MONTHS_PER_YEAR = 12.0
ZERO_TOLERANCE = 1e-12


@dataclass(frozen=True, slots=True)
class FairDefaultResult:
    """Output of the Strategy A (fixed_charge_only) closed-form solver."""

    fixed_charge: float
    """F* — the revenue-neutral, cross-subsidy-eliminating fixed charge ($/month)."""

    delta: float
    """F* - F_0 - change from the baseline fixed charge ($/month)."""

    implied_lambda: float
    """lambda* - the volumetric scaling factor (dimensionless).

    All baseline per-kWh charges are multiplied by lambda* to maintain C1.
    """

    feasible: bool
    """True when F* >= 0 and lambda* > 0 (the tariff has non-negative components)."""


def fair_default_fixed_charge_only(
    *,
    class_revenue: float,
    class_customers: float,
    subclass_revenue: float,
    subclass_customers: float,
    subclass_cross_subsidy: float,
    base_fixed_charge: float,
) -> FairDefaultResult:
    """Solve Strategy A: adjust F to eliminate subclass cross-subsidy, hold class revenue neutral.

    All monetary inputs are **weighted annual totals** (not per-customer averages).

    Parameters
    ----------
    class_revenue:
        RR — weighted sum of ``annual_bill_delivery`` for all customers.
    class_customers:
        N_cls — weighted customer count (all customers).
    subclass_revenue:
        Weighted sum of ``annual_bill_delivery`` for the HP subclass.
    subclass_customers:
        N_hp — weighted customer count (HP subclass).
    subclass_cross_subsidy:
        X_hp — weighted sum of ``BAT_percustomer_delivery`` for the HP subclass.
        Positive means the subclass is **overpaying**.
    base_fixed_charge:
        F_0 — the baseline tariff's monthly fixed charge ($/month).

    Returns
    -------
    FairDefaultResult
        Contains F*, delta, lambda*, and a feasibility flag.
    """
    v0_cls = class_revenue - MONTHS_PER_YEAR * base_fixed_charge * class_customers
    v0_hp = subclass_revenue - MONTHS_PER_YEAR * base_fixed_charge * subclass_customers

    tc_hp = subclass_revenue - subclass_cross_subsidy

    denominator = class_customers * v0_hp - subclass_customers * v0_cls
    if math.isclose(denominator, 0.0, abs_tol=ZERO_TOLERANCE):
        raise ValueError(
            "Degenerate system: N_cls * V^0_hp == N_hp * V^0_cls "
            "(subclass has the same per-customer volumetric bill as the class)."
        )

    fixed_charge = (class_revenue * v0_hp - tc_hp * v0_cls) / (MONTHS_PER_YEAR * denominator)

    implied_lambda = (class_revenue - MONTHS_PER_YEAR * fixed_charge * class_customers) / v0_cls

    return FairDefaultResult(
        fixed_charge=fixed_charge,
        delta=fixed_charge - base_fixed_charge,
        implied_lambda=implied_lambda,
        feasible=(fixed_charge >= 0.0 and implied_lambda > 0.0),
    )
