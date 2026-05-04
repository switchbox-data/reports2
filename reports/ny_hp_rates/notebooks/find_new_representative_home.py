"""Find a new representative home for the NY HP Rates one-pager.

Criteria from the user (one-pager messaging):

1. Overpays for delivery (under default rate after switching to HP) by ~$855
   (matches the headline statewide-average overpayment).
2. Total energy bills go up after switching to HP under default rates.
3. NG-heated home's delivery bill is BELOW its delivery cost of service
   (gas BAT < 0 — gas-heated home underpays for delivery).
4. HP customer on the dedicated HP rate has a delivery bill at or
   slightly above their delivery cost of service (HP-rate BAT >= 0, small).
5. Sizable increase in electricity costs (Syracuse home is ~2x kWh and bill).

Plus the existing constraints from analysis.qmd:

- Natural gas only (no oil/propane).
- Building must have no LMI credit applied (so energy_total = sum of components,
  matching the prose narrative).

Important: BAT for u02 (HP) and u02hprate (HP rate) scenarios uses the
baseline (run 1+2) residual_share_delivery, not the scenario's own residual.
This mirrors the workaround in analysis.qmd's cross-subsidy-example-data cell.
The scenario's own residual is calibrated for an unrealistic universe in which
the entire NY building stock has switched fuel/rate; for a "single customer
switches" thought experiment we hold the per-utility residual at the gas
baseline.

Run: uv run python notebooks/find_new_representative_home.py
"""

from __future__ import annotations

import sys

import polars as pl

# --- Paths (mirror analysis.qmd) ---
STATE = "NY"
BATCH = "ny_20260416a_r1-36"
S3_BASE = "s3://data.sb/switchbox/cairo/outputs/hp_rates"
_BILLS = f"{S3_BASE}/{STATE.lower()}/all_utilities/{BATCH}"

PATH_BILLS_BASELINE = f"{_BILLS}/run_1+2/comb_bills_year_target/"
PATH_BILLS_HP_DEFAULT = f"{_BILLS}/run_3+4/comb_bills_year_target/"
PATH_BILLS_HP_HPRATE = f"{_BILLS}/run_7+8/comb_bills_year_target/"
PATH_BAT_BASELINE = f"{_BILLS}/run_1+2/cross_subsidization_BAT_values/"
PATH_BAT_HP_DEFAULT = f"{_BILLS}/run_3+4/cross_subsidization_BAT_values/"
PATH_BAT_HP_HPRATE = f"{_BILLS}/run_7+8/cross_subsidization_BAT_values/"

ANNUAL_MONTH = "Annual"
TARGET_BAT = 855.0
RESSTOCK_META = "/ebs/data/nrel/resstock/res_2024_amy2018_2_sb/metadata/state=NY/upgrade=00/metadata-sb.parquet"

SYRACUSE_BLDG_ID = 328510


def _annual_bills(path: str, alias_prefix: str) -> pl.LazyFrame:
    return (
        pl.scan_parquet(path, hive_partitioning=True)
        .filter(pl.col("month") == ANNUAL_MONTH)
        .select(
            "bldg_id",
            "weight",
            "sb.electric_utility",
            "heats_with_natgas",
            "heats_with_oil",
            "heats_with_propane",
            "in.hvac_cooling_partial_space_conditioning",
            pl.col("elec_supply_bill").alias(f"{alias_prefix}_supply"),
            pl.col("elec_delivery_bill").alias(f"{alias_prefix}_delivery_vol"),
            pl.col("elec_fixed_charge").alias(f"{alias_prefix}_delivery_fixed"),
            pl.col("gas_total_bill").alias(f"{alias_prefix}_gas"),
            pl.col("oil_total_bill").alias(f"{alias_prefix}_oil"),
            pl.col("propane_total_bill").alias(f"{alias_prefix}_propane"),
            pl.col("elec_total_bill").alias(f"{alias_prefix}_elec_total"),
            pl.col("elec_total_bill_lmi_40").alias(f"{alias_prefix}_elec_total_lmi40"),
        )
        .with_columns(
            (
                pl.col(f"{alias_prefix}_supply")
                + pl.col(f"{alias_prefix}_delivery_vol")
                + pl.col(f"{alias_prefix}_delivery_fixed")
                + pl.col(f"{alias_prefix}_gas")
                + pl.col(f"{alias_prefix}_oil")
                + pl.col(f"{alias_prefix}_propane")
            ).alias(f"{alias_prefix}_energy_total"),
        )
    )


def _annual_bat(path: str, alias_prefix: str) -> pl.LazyFrame:
    return pl.scan_parquet(path, hive_partitioning=True).select(
        "bldg_id",
        pl.col("annual_bill_delivery").alias(f"{alias_prefix}_bill_delivery"),
        pl.col("economic_burden_delivery").alias(f"{alias_prefix}_mc_delivery"),
        pl.col("residual_share_delivery").alias(f"{alias_prefix}_residual_delivery"),
    )


def main() -> int:
    print("Loading bills + BAT for runs 1+2, 3+4, 7+8…", file=sys.stderr)

    bills_baseline = _annual_bills(PATH_BILLS_BASELINE, "u00")
    bills_hp = _annual_bills(PATH_BILLS_HP_DEFAULT, "u02")
    bills_hp_hprate = _annual_bills(PATH_BILLS_HP_HPRATE, "u02hprate")
    bat_baseline = _annual_bat(PATH_BAT_BASELINE, "u00")
    bat_hp = _annual_bat(PATH_BAT_HP_DEFAULT, "u02")
    bat_hp_hprate = _annual_bat(PATH_BAT_HP_HPRATE, "u02hprate")

    drop_dup_cols = [
        "weight",
        "sb.electric_utility",
        "heats_with_natgas",
        "heats_with_oil",
        "heats_with_propane",
        "in.hvac_cooling_partial_space_conditioning",
    ]
    bills_hp = bills_hp.drop(drop_dup_cols)
    bills_hp_hprate = bills_hp_hprate.drop(drop_dup_cols)

    joined = (
        bills_baseline.filter(pl.col("heats_with_natgas"))
        .join(bills_hp, on="bldg_id", how="inner")
        .join(bills_hp_hprate, on="bldg_id", how="inner")
        .join(bat_baseline, on="bldg_id", how="left")
        .join(bat_hp, on="bldg_id", how="left")
        .join(bat_hp_hprate, on="bldg_id", how="left")
    )

    base = joined.filter(
        (pl.col("u00_propane") == 0)
        & (pl.col("u00_oil") == 0)
        & (pl.col("u02_propane") == 0)
        & (pl.col("u02_oil") == 0)
    ).filter((pl.col("u00_elec_total") - pl.col("u00_elec_total_lmi40")).abs() < 1.0)

    # BAT computation:
    #   For u00 (gas baseline): use the run's own residual (no fix needed).
    #   For u02 (HP, default rates): mc + bill from u02; residual from u00.
    #   For u02hprate (HP, HP rate): mc + bill from u02hprate; residual from u00.
    base = base.with_columns(
        (pl.col("u00_bill_delivery") - pl.col("u00_mc_delivery") - pl.col("u00_residual_delivery")).alias("u00_bat"),
        (pl.col("u02_bill_delivery") - pl.col("u02_mc_delivery") - pl.col("u00_residual_delivery")).alias("u02_bat"),
        (pl.col("u02hprate_bill_delivery") - pl.col("u02hprate_mc_delivery") - pl.col("u00_residual_delivery")).alias(
            "u02hprate_bat"
        ),
        (pl.col("u00_mc_delivery") + pl.col("u00_residual_delivery")).alias("u00_cos"),
        (pl.col("u02_mc_delivery") + pl.col("u00_residual_delivery")).alias("u02_cos"),
        (pl.col("u02hprate_mc_delivery") + pl.col("u00_residual_delivery")).alias("u02hprate_cos"),
        (pl.col("u02_supply") / pl.col("u00_supply")).alias("supply_multiplier"),
        (
            (pl.col("u02_delivery_vol") + pl.col("u02_delivery_fixed"))
            / (pl.col("u00_delivery_vol") + pl.col("u00_delivery_fixed"))
        ).alias("delivery_multiplier"),
        (pl.col("u02_elec_total") / pl.col("u00_elec_total")).alias("elec_total_multiplier"),
        (pl.col("u02_energy_total") - pl.col("u00_energy_total")).alias("net_increase"),
        (pl.col("u02_gas") - pl.col("u00_gas")).alias("gas_bill_change"),
    ).with_columns(
        (pl.col("u02_bat") - TARGET_BAT).abs().alias("bat_distance"),
    )

    base_df = base.collect()
    print(f"\nBaseline natgas-only/no-LMI cohort: {base_df.height:,} buildings", file=sys.stderr)

    # --- Diagnostic on the existing Syracuse home ---
    print("\n=== Existing Syracuse home (bldg_id=328510) ===")
    syr = base_df.filter(pl.col("bldg_id") == SYRACUSE_BLDG_ID)
    if syr.is_empty():
        print("Syracuse home not in cohort")
    else:
        r = syr.row(0, named=True)
        for k in (
            "sb.electric_utility",
            "in.hvac_cooling_partial_space_conditioning",
            "u00_energy_total",
            "u02_energy_total",
            "net_increase",
            "u00_elec_total",
            "u02_elec_total",
            "elec_total_multiplier",
            "supply_multiplier",
            "delivery_multiplier",
            "gas_bill_change",
            "u00_bill_delivery",
            "u00_cos",
            "u00_bat",
            "u02_bill_delivery",
            "u02_cos",
            "u02_bat",
            "u02hprate_bill_delivery",
            "u02hprate_cos",
            "u02hprate_bat",
        ):
            v = r[k]
            if isinstance(v, float):
                print(f"  {k}: {v:,.2f}")
            else:
                print(f"  {k}: {v}")

    # --- Distribution diagnostics ---
    def _pcts(col: str, label: str) -> None:
        print(f"\n{label} percentiles:")
        for q in (0.05, 0.10, 0.25, 0.5, 0.75, 0.9, 0.95):
            print(f"  p{int(q * 100)}: {base_df[col].quantile(q):,.0f}")

    _pcts("u02_bat", f"u02_bat (target ${TARGET_BAT:.0f})")
    _pcts("u02hprate_bat", "u02hprate_bat (target ~$0)")
    _pcts("u00_bat", "u00_bat (gas, want negative)")
    _pcts("net_increase", "net_increase (want positive)")
    _pcts("elec_total_multiplier", "elec_total_multiplier (target ~2x)")

    # Stepwise filtering counts
    print("\n=== Stepwise filter counts ===")
    f1 = base_df.filter(pl.col("net_increase") > 0)
    print(f"after net_increase > 0:                     {f1.height:>7,}")
    f2 = f1.filter(pl.col("u00_bat") < 0)
    print(f"after u00_bat < 0 (gas underpays):          {f2.height:>7,}")
    f3 = f2.filter((pl.col("u02hprate_bat") >= -25) & (pl.col("u02hprate_bat") <= 100))
    print(f"after -25 <= u02hprate_bat <= 100:          {f3.height:>7,}")
    f4 = f3.filter(pl.col("in.hvac_cooling_partial_space_conditioning") == "100% Conditioned")
    print(f"after full cooling:                         {f4.height:>7,}")
    f5 = f4.filter(pl.col("bat_distance") <= 25)
    print(f"after |u02_bat - 855| <= 25:                {f5.height:>7,}")
    f6 = f4.filter(pl.col("bat_distance") <= 50)
    print(f"after |u02_bat - 855| <= 50:                {f6.height:>7,}")
    f7 = f4.filter(pl.col("bat_distance") <= 100)
    print(f"after |u02_bat - 855| <= 100:               {f7.height:>7,}")

    candidates = f4.with_columns(
        (pl.col("elec_total_multiplier") - 2.0).abs().alias("mult_distance"),
    ).with_columns(
        (pl.col("bat_distance") + 100 * pl.col("mult_distance")).alias("score"),
    )

    display_cols = [
        "bldg_id",
        "sb.electric_utility",
        "u00_energy_total",
        "u02_energy_total",
        "net_increase",
        "u00_elec_total",
        "u02_elec_total",
        "elec_total_multiplier",
        "supply_multiplier",
        "delivery_multiplier",
        "gas_bill_change",
        "u00_bill_delivery",
        "u00_cos",
        "u00_bat",
        "u02_bill_delivery",
        "u02_cos",
        "u02_bat",
        "u02hprate_bill_delivery",
        "u02hprate_cos",
        "u02hprate_bat",
        "bat_distance",
        "mult_distance",
        "score",
    ]
    pl.Config.set_tbl_cols(-1)
    pl.Config.set_tbl_rows(60)
    pl.Config.set_tbl_width_chars(420)
    pl.Config.set_fmt_float("mixed")

    print(f"\n{'=' * 80}")
    print(f"Top 25 by COMBINED score (bat distance + 100 * |mult-2|), within {f4.height} valid candidates")
    print(f"{'=' * 80}\n")
    by_score = candidates.sort("score").head(25)
    print(by_score.select(display_cols))

    print(f"\n{'=' * 80}")
    print(f"Top 25 by BAT proximity to ${TARGET_BAT}")
    print(f"{'=' * 80}\n")
    by_bat = candidates.sort("bat_distance").head(25)
    print(by_bat.select(display_cols))

    # Pull metadata for top union and show.
    top_ids = list(set(by_score["bldg_id"].head(15).to_list() + by_bat["bldg_id"].head(15).to_list()))
    if not top_ids:
        print("No candidates found. Exiting.")
        return 0
    print(f"\n{'=' * 80}")
    print(f"Detailed metadata for top {len(top_ids)} (union of two ranking views):")
    print(f"{'=' * 80}\n")

    META_COLS = [
        "bldg_id",
        "in.county",
        "in.geometry_floor_area",
        "in.bedrooms",
        "in.geometry_stories",
        "in.geometry_building_type_acs",
        "in.geometry_building_type_recs",
        "in.tenure",
        "in.vintage_acs",
        "in.vintage",
        "in.hvac_heating_efficiency",
        "in.hvac_cooling_efficiency",
        "in.hvac_cooling_partial_space_conditioning",
        "in.insulation_wall",
        "in.weather_file_city",
    ]
    meta = pl.scan_parquet(RESSTOCK_META).filter(pl.col("bldg_id").is_in(top_ids)).select(META_COLS).collect()

    top_rows = candidates.filter(pl.col("bldg_id").is_in(top_ids)).sort("score").join(meta, on="bldg_id", how="left")

    rows = top_rows.to_dicts()
    for i, r in enumerate(rows, start=1):
        print(f"--- Rank {i} (score={r['score']:.0f}): bldg_id={r['bldg_id']} | utility={r['sb.electric_utility']} ---")
        print(f"  City / county      : {r.get('in.weather_file_city')!s:<35} {r.get('in.county')}")
        print(
            f"  Building type      : {r.get('in.geometry_building_type_acs')!s} ({r.get('in.geometry_building_type_recs')})"
        )
        print(
            f"  Tenure / floor sqft: {r.get('in.tenure')!s:<10} {r.get('in.geometry_floor_area')!s} sqft, {r.get('in.bedrooms')} bed, {r.get('in.geometry_stories')} story"
        )
        print(f"  Vintage            : {r.get('in.vintage_acs')!s} ({r.get('in.vintage')})")
        print(f"  Heating eff (AFUE) : {r.get('in.hvac_heating_efficiency')}")
        print(
            f"  Cooling eff/share  : {r.get('in.hvac_cooling_efficiency')!s} ({r.get('in.hvac_cooling_partial_space_conditioning')})"
        )
        print(f"  Wall insulation    : {r.get('in.insulation_wall')}")
        print(
            f"  Energy total       : ${r['u00_energy_total']:>7,.0f}  ->  ${r['u02_energy_total']:>7,.0f}  (delta: ${r['net_increase']:+,.0f})"
        )
        print(
            f"  Electric total     : ${r['u00_elec_total']:>7,.0f}  ->  ${r['u02_elec_total']:>7,.0f}  (mult {r['elec_total_multiplier']:.2f}x; supply {r['supply_multiplier']:.2f}x; delivery {r['delivery_multiplier']:.2f}x)"
        )
        print(f"  Gas bill change    : ${r['gas_bill_change']:+,.0f}")
        print(
            f"  Delivery (NG dflt) : bill ${r['u00_bill_delivery']:>7,.0f}  COS ${r['u00_cos']:>7,.0f}  BAT ${r['u00_bat']:+,.0f}"
        )
        print(
            f"  Delivery (HP dflt) : bill ${r['u02_bill_delivery']:>7,.0f}  COS ${r['u02_cos']:>7,.0f}  BAT ${r['u02_bat']:+,.0f}  (target ~$855)"
        )
        print(
            f"  Delivery (HP rate) : bill ${r['u02hprate_bill_delivery']:>7,.0f}  COS ${r['u02hprate_cos']:>7,.0f}  BAT ${r['u02hprate_bat']:+,.0f}  (target ~$0)"
        )
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
