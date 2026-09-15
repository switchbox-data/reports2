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


@dataclass(frozen=True, slots=True)
class IncrementalFairDefaultResult:
    """Output of a default-rate redesign targeted to retrofit overpayment."""

    fixed_charge: float
    """F* — the revenue-neutral monthly fixed charge ($/month)."""

    delta: float
    """F* - F_0 — change from the baseline monthly fixed charge ($/month)."""

    implied_lambda: float
    """Uniform multiplier applied to the targeted volumetric charges."""

    retrofit_overpayment: float
    """Current incremental variable charge minus incremental marginal cost."""

    class_revenue_shift: float
    """Annual class revenue shifted from volumetric to fixed charges."""

    feasible: bool
    """True when F* >= 0 and lambda* > 0."""


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


def fair_default_incremental_fixed_charge(
    *,
    class_variable_revenue: float,
    class_customers: float,
    retrofit_incremental_variable_charge: float,
    retrofit_incremental_marginal_cost: float,
    base_fixed_charge: float,
) -> IncrementalFairDefaultResult:
    """Redesign a default rate around paired pre/post-retrofit overpayment.

    The same default tariff applies before and after the retrofit, so its fixed
    charge cancels from the retrofit bill difference. The required volumetric
    multiplier is therefore determined directly by:

    ``lambda * delta_variable_charge = delta_marginal_cost``.

    The fixed charge then rises enough to replace the class-wide revenue lost
    by applying ``lambda`` to the targeted volumetric charges. Inputs may be
    weighted annual totals; the two retrofit inputs must use the same
    population and weighting basis.
    """
    values = (
        class_variable_revenue,
        class_customers,
        retrofit_incremental_variable_charge,
        retrofit_incremental_marginal_cost,
        base_fixed_charge,
    )
    if not all(math.isfinite(value) for value in values):
        raise ValueError("All inputs must be finite.")
    if class_variable_revenue < 0.0:
        raise ValueError("class_variable_revenue must be non-negative.")
    if class_customers <= 0.0:
        raise ValueError("class_customers must be positive.")
    if math.isclose(retrofit_incremental_variable_charge, 0.0, abs_tol=ZERO_TOLERANCE):
        raise ValueError("retrofit_incremental_variable_charge must be non-zero.")

    implied_lambda = retrofit_incremental_marginal_cost / retrofit_incremental_variable_charge
    class_revenue_shift = (1.0 - implied_lambda) * class_variable_revenue
    fixed_charge = base_fixed_charge + class_revenue_shift / (MONTHS_PER_YEAR * class_customers)

    return IncrementalFairDefaultResult(
        fixed_charge=fixed_charge,
        delta=fixed_charge - base_fixed_charge,
        implied_lambda=implied_lambda,
        retrofit_overpayment=retrofit_incremental_variable_charge - retrofit_incremental_marginal_cost,
        class_revenue_shift=class_revenue_shift,
        feasible=(fixed_charge >= 0.0 and implied_lambda > 0.0),
    )
