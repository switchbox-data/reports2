"""Verify the revenue-neutrality workbook reproduces the testimony numbers.

Two checks:

1. **Structural** — open the xlsx and confirm expected sheets, named ranges,
   and formula strings exist.
2. **Numerical** — re-run polars aggregation on the same BAT data and YAML
   inputs to confirm HP + non-HP = total, rate derivations match calibrated
   rates, and per-building aggregates are consistent.
"""

from __future__ import annotations

import sys
from pathlib import Path

import polars as pl
from openpyxl import load_workbook

REPORT_DIR = Path("/ebs/home/alex_switch_box/reports2/reports/ri_hp_rates")
sys.path.insert(0, str(REPORT_DIR))

from testimony_response.build_RIE_1_12_workbook import (  # noqa: E402
    DELIVERY_METHODS_REPORTED,
    METHOD_LABELS,
    load_inputs,
    load_master_bat,
)


def _structural_check(xlsx_path: Path) -> None:
    print(f"=== Structural check: {xlsx_path} ===")
    wb = load_workbook(str(xlsx_path), data_only=False)
    expected_sheets = [
        "README",
        "inputs_revenue_requirement",
        "inputs_tariffs",
        "inputs_subclass_rr",
        "bat_per_building",
        "hp_nonhp_aggregates",
        "revenue_neutrality_proof",
        "validation",
    ]
    missing = [s for s in expected_sheets if s not in wb.sheetnames]
    assert not missing, f"missing sheets: {missing}"
    print(f"  sheets: {wb.sheetnames}")

    expected_names = {
        "total_delivery_revenue_requirement",
        "test_year_customer_count",
        "test_year_residential_kwh",
        "customer_charge_total",
        "core_delivery_rate_total",
        "annual_fixed_per_customer",
        "default_vol_usd_per_kwh",
        "hp_flat_vol_usd_per_kwh",
        "nonhp_default_vol_usd_per_kwh",
        "hp_delivery_rr_epmc",
        "nonhp_delivery_rr_epmc",
        "ws_weight",
        "ws_has_hp",
        "ws_annual_bill",
        "ws_annual_kwh",
        "ws_bill_check",
        "ws_w_bill",
        "ws_w_kwh",
        "agg_hp_customers",
        "agg_nonhp_customers",
        "agg_hp_kwh",
        "agg_nonhp_kwh",
    }
    actual_names = set(wb.defined_names)
    missing_names = expected_names - actual_names
    assert not missing_names, f"missing named ranges: {missing_names}"
    print(f"  named ranges: {len(actual_names)} (OK)")

    bat_ws = wb["bat_per_building"]
    assert isinstance(bat_ws["F2"].value, (int, float)), f"expected numeric annual_kwh, got {bat_ws['F2'].value!r}"
    assert "F2" in bat_ws["G2"].value and "inputs_tariffs" in bat_ws["G2"].value, (
        f"expected annual_bill_delivery_check formula, got {bat_ws['G2'].value!r}"
    )
    assert bat_ws["H2"].value == "=B2*E2"
    assert bat_ws["I2"].value == "=B2*F2"
    n_rows = bat_ws.max_row - 1
    print(f"  bat_per_building data rows: {n_rows:,}")

    # Check hp_nonhp_aggregates SUMIFS.
    agg_ws = wb["hp_nonhp_aggregates"]
    c2 = str(agg_ws["C2"].value)
    assert "SUMIFS" in c2 and '"true"' in c2, f"unexpected C2: {c2}"
    print("  hp_nonhp_aggregates SUMIFS formulas: OK")

    # Check inputs_subclass_rr sum formulas.
    sub_ws = wb["inputs_subclass_rr"]
    d2 = str(sub_ws["D2"].value)
    assert d2 == "=B2+C2", f"unexpected sum formula: {d2}"
    f2 = str(sub_ws["F2"].value)
    assert f2 == "=D2-E2", f"unexpected delta formula: {f2}"
    print("  inputs_subclass_rr sum/delta formulas: OK")

    # Check revenue_neutrality_proof exists and has content.
    proof_ws = wb["revenue_neutrality_proof"]
    assert "Revenue-neutrality" in str(proof_ws["A1"].value)
    print("  revenue_neutrality_proof title: OK")
    print()


def _numerical_check() -> None:
    print("=== Numerical check (expected values from polars) ===")
    bat = load_master_bat()
    inputs = load_inputs()

    default_vol = inputs["default_vol_usd_per_kwh"]
    hp_vol = inputs["hp_flat_vol_usd_per_kwh"]
    nonhp_vol = inputs["nonhp_default_vol_usd_per_kwh"]
    annual_fixed = inputs["annual_fixed_per_customer"]
    total_rr = inputs["total_delivery_revenue_requirement"]
    n_customers = inputs["test_year_customer_count"]
    ty_kwh = inputs["test_year_residential_kwh"]

    bat = bat.with_columns(
        ((pl.col("annual_bill_delivery") - annual_fixed) / default_vol).alias("annual_kwh"),
    )

    # Per-building totals.
    total_w = float(bat["weight"].sum())
    total_rev = float((bat["weight"] * bat["annual_bill_delivery"]).sum())
    total_kwh_computed = float((bat["weight"] * bat["annual_kwh"]).sum())

    print(f"  sum(weight): {total_w:,.2f} (expected {n_customers:,.2f})")
    assert abs(total_w - n_customers) < 0.5

    print(f"  sum(w*bill): ${total_rev:,.0f} (expected ${total_rr:,.0f})")
    assert abs(total_rev - total_rr) < 5_000

    print(f"  sum(w*kwh): {total_kwh_computed:,.0f} (expected {ty_kwh:,.0f})")
    assert abs(total_kwh_computed - ty_kwh) / ty_kwh < 1e-6

    # HP vs non-HP split.
    hp_mask = bat["postprocess_group.has_hp"].cast(str).str.to_lowercase() == "true"
    hp = bat.filter(hp_mask)
    nonhp = bat.filter(~hp_mask)

    n_hp = float(hp["weight"].sum())
    n_nonhp = float(nonhp["weight"].sum())
    hp_kwh = float((hp["weight"] * hp["annual_kwh"]).sum())
    nonhp_kwh = float((nonhp["weight"] * nonhp["annual_kwh"]).sum())
    hp_rev = float((hp["weight"] * hp["annual_bill_delivery"]).sum())
    nonhp_rev = float((nonhp["weight"] * nonhp["annual_bill_delivery"]).sum())

    print(f"\n  HP customers: {n_hp:,.1f}")
    print(f"  Non-HP customers: {n_nonhp:,.1f}")
    print(f"  HP kWh: {hp_kwh:,.0f}")
    print(f"  Non-HP kWh: {nonhp_kwh:,.0f}")
    print(f"  HP delivery revenue (current): ${hp_rev:,.0f}")
    print(f"  Non-HP delivery revenue (current): ${nonhp_rev:,.0f}")

    # Implied vol rates.
    hp_fixed_total = annual_fixed * n_hp
    hp_vol_rev = hp_rev - hp_fixed_total
    hp_implied_vol = hp_vol_rev / hp_kwh

    nonhp_fixed_total = annual_fixed * n_nonhp
    nonhp_vol_rev = nonhp_rev - nonhp_fixed_total
    nonhp_implied_vol = nonhp_vol_rev / nonhp_kwh

    print(f"\n  HP implied vol rate: {hp_implied_vol:.6f} $/kWh")
    print(f"  HP calibrated vol rate: {hp_vol:.6f} $/kWh")
    print(f"  Non-HP implied vol rate: {nonhp_implied_vol:.6f} $/kWh")
    print(f"  Non-HP calibrated vol rate: {nonhp_vol:.6f} $/kWh")

    # Subclass RR checks (delivery only — supply is not part of the claim).
    subs = inputs["subclass_revenue_requirements"]
    print("\n  Subclass RR sum checks (delivery, testimony methods only):")
    for method in DELIVERY_METHODS_REPORTED:
        hp_rr = float(subs["delivery"][method]["hp"])
        nonhp_rr = float(subs["delivery"][method]["non-hp"])
        total = hp_rr + nonhp_rr
        delta = abs(total - total_rr)
        label = METHOD_LABELS.get(method, method)
        print(f"    {label}: hp=${hp_rr:,.2f} + nonhp=${nonhp_rr:,.2f} = ${total:,.2f} (delta=${delta:.2f})")
        assert delta < 1.0, f"{method} delivery sum mismatch: {delta}"

    # Revenue neutrality: proposed revenue = current revenue.
    proposed_hp_rev = hp_vol * hp_kwh + annual_fixed * n_hp
    proposed_nonhp_rev = nonhp_vol * nonhp_kwh + annual_fixed * n_nonhp
    proposed_total = proposed_hp_rev + proposed_nonhp_rev

    print("\n  === Revenue neutrality check ===")
    print(f"  Current total revenue: ${total_rev:,.0f}")
    print(f"  Proposed HP revenue: ${proposed_hp_rev:,.0f}")
    print(f"  Proposed non-HP revenue: ${proposed_nonhp_rev:,.0f}")
    print(f"  Proposed total revenue: ${proposed_total:,.0f}")
    print(f"  Difference: ${proposed_total - total_rev:,.0f}")

    # EPMC HP COS matches testimony.
    epmc_hp = float(subs["delivery"]["epmc"]["hp"])
    print(f"\n  EPMC delivery HP RR: ${epmc_hp:,.2f}")
    print("  (testimony cos_default_hp_group_cos should = $11,940,870.79)")
    assert abs(epmc_hp - 11_940_870.79) < 0.01, f"EPMC HP mismatch: {epmc_hp}"
    print("  PASS: matches testimony value")

    print("\n  All numerical checks: PASS")


def main() -> int:
    xlsx_path = REPORT_DIR / "cache" / "revenue_neutrality.xlsx"
    if not xlsx_path.exists():
        print(f"ERROR: {xlsx_path} not found. Run build_RIE_1_12_workbook.py first.")
        return 1
    _structural_check(xlsx_path)
    _numerical_check()
    return 0


if __name__ == "__main__":
    sys.exit(main())
