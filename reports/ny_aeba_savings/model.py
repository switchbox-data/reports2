"""Heat pump cost savings model for New York new construction.

Migrated from Excel workbook to polars. This module contains data loading
functions that read YAML configuration files and return polars DataFrames
or dicts ready for computation, plus computation functions that replicate
the Excel Model sheet formulas.
"""

from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import polars as pl
import yaml

# Type alias for scenario overrides used in testing.
# Keys are (fuel, zone) tuples; values are dicts of param_name -> value.
Overrides = dict[tuple[str, str], dict[str, Any]] | None

DATA_DIR = Path(__file__).parent / "data"

# Year range for fuel price averaging. The Excel model uses a 6-year window
# of winter months (Jan-Mar, Oct-Dec) from 2020 through 2025.
_FUEL_PRICE_START_YEAR = 2020


def _load_yaml(filename: str) -> Any:
    """Read and parse a YAML file from the data directory."""
    path = DATA_DIR / filename
    with open(path) as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Scalar / dict loaders
# ---------------------------------------------------------------------------


def load_model_params() -> dict:
    """Load flat dict of financial/analysis scalars.

    Returns keys: mortgage_rate, mortgage_term_years, discount_rate,
    analysis_period_years, indoor_design_temp_f, sizing_scale_up_factor,
    internal_heat_gains_btu, epa_hdd_adjustment, propane_tank_cost.
    """
    return _load_yaml("model_params.yaml")


def load_operating_params() -> dict:
    """Load maintenance costs, efficiency ratings, fuel content conversions.

    Returns a nested dict with top-level keys: maintenance, efficiency,
    gas_water_heater, hpwh, fuel_content.
    """
    return _load_yaml("operating_params.yaml")


# ---------------------------------------------------------------------------
# DataFrame loaders
# ---------------------------------------------------------------------------


def load_building_params() -> pl.DataFrame:
    """Load building parameters, merging defaults into each zone.

    yaml.safe_load resolves YAML anchors and merge keys automatically,
    so each zone dict already contains all default fields plus its overrides.

    Returns one row per zone (3 rows) with columns for every building
    parameter plus a 'zone' identifier.
    """
    data = _load_yaml("building_params.yaml")
    zones = data["zones"]
    return pl.DataFrame(zones)


def load_equipment() -> pl.DataFrame:
    """Load equipment specs and prices.

    Each record has a 'prices' list and a pre-computed 'avg_price'.
    The prices list is dropped since we only need the average for modeling.
    The 'zones' field (present on zone-dependent devices like ccASHP) is
    kept as a list column for downstream filtering.

    Returns one row per device entry.
    """
    records = _load_yaml("equipment.yaml")

    # Build flat rows, dropping the raw prices list
    rows = []
    for rec in records:
        row = {k: v for k, v in rec.items() if k != "prices"}
        # Verify avg_price is consistent with prices if both present
        if "prices" in rec and "avg_price" not in row:
            prices = rec["prices"]
            row["avg_price"] = sum(prices) / len(prices)
        rows.append(row)

    return pl.DataFrame(rows)


def load_fuel_prices(*, start_year: int = _FUEL_PRICE_START_YEAR) -> pl.DataFrame:
    """Load fuel price records and compute winter averages.

    Reads all monthly winter price records, filters to years >= start_year,
    and returns one row per fuel with the mean price across all winter months
    in that period.

    Columns returned: fuel, avg_price, n_months (count of observations).

    Units are as stored in the YAML:
      - electricity: cents/kWh
      - natural_gas: $/mcf
      - propane: cents/gallon
    """
    records = _load_yaml("fuel_prices.yaml")
    all_prices = pl.DataFrame(records)

    avg_prices = (
        all_prices.filter(pl.col("year") >= start_year)
        .group_by("fuel")
        .agg(
            pl.col("price").mean().alias("avg_price"),
            pl.col("price").count().alias("n_months"),
        )
        .sort("fuel")
    )

    return avg_prices


def load_counties() -> pl.DataFrame:
    """Load 62 county records.

    Each row contains: county, population, electric_utility, gas_utility,
    zone, design_temp_f, new_construction_share.

    Counties with no gas service have gas_utility = null.
    """
    records = _load_yaml("counties.yaml")
    return pl.DataFrame(records)


def load_utility_rebates() -> pl.DataFrame:
    """Load utility rebate records in long format.

    Each row is one utility x technology combination with columns:
    utility, technology, amount, unit, source, source_notes.
    """
    records = _load_yaml("utility_rebates.yaml")
    return pl.DataFrame(records)


def load_service_line_costs() -> pl.DataFrame:
    """Load gas utility service line costs.

    Each row has: gas_utility, avg_service_line_length_ft,
    avg_per_foot_cost, avg_service_line_cost, source.
    """
    records = _load_yaml("service_line_costs.yaml")
    return pl.DataFrame(records)


def load_heating_survey() -> pl.DataFrame:
    """Load heating system type counts by zone.

    Each row is one system type with count and percentage columns
    for zones 4, 5, and 6.
    """
    records = _load_yaml("heating_survey.yaml")
    return pl.DataFrame(records)


# ---------------------------------------------------------------------------
# Helper: apply scenario-level overrides
# ---------------------------------------------------------------------------


def _apply_overrides(df: pl.DataFrame, overrides: Overrides) -> pl.DataFrame:
    """Apply per-scenario parameter overrides to a DataFrame.

    The overrides dict maps (fuel, zone) tuples to dicts of column_name -> value.
    Only columns already present in `df` are overridden; unknown keys are ignored
    so that overrides for later computation stages pass through harmlessly.
    """
    if not overrides:
        return df

    for (fuel, zone), params in overrides.items():
        for col_name, value in params.items():
            if col_name not in df.columns:
                continue
            # Build a conditional expression: where fuel & zone match, use override
            df = df.with_columns(
                pl.when((pl.col("fuel") == fuel) & (pl.col("zone") == zone))
                .then(pl.lit(value))
                .otherwise(pl.col(col_name))
                .alias(col_name)
            )
    return df


# ---------------------------------------------------------------------------
# Computation: weighted-average design temperature per zone
# ---------------------------------------------------------------------------


def _compute_zone_design_temps() -> pl.DataFrame:
    """Compute weighted-average coldest day design temp per zone.

    Weights are new_construction_share within each zone (normalized to sum
    to 1 within zone). This replicates the County information!J66:J68
    values that the Excel Model sheet references for rows 49.

    Returns a DataFrame with columns: zone, coldest_day_temp_f.
    """
    counties = load_counties()
    return (
        counties.with_columns(
            # Weight = share within zone (shares already sum to ~1 statewide,
            # but we normalize within each zone)
            zone_total=pl.col("new_construction_share").sum().over("zone"),
        )
        .with_columns(
            zone_weight=pl.col("new_construction_share") / pl.col("zone_total"),
        )
        .group_by("zone")
        .agg(
            (pl.col("design_temp_f") * pl.col("zone_weight")).sum().alias("coldest_day_temp_f"),
        )
    )


# ---------------------------------------------------------------------------
# Computation stage 1: build_scenario_table
# ---------------------------------------------------------------------------


def build_scenario_table(overrides: Overrides = None) -> pl.DataFrame:
    """Build the 6-row scenario table: 3 zones x 2 fuels.

    Each row represents one scenario with building params, model params,
    and fuel prices joined in. The overrides dict allows tests to modify
    specific input values per scenario.
    """
    # Create the 6 scenario rows: cross join of fuels x zones
    fuels = pl.DataFrame({"fuel": ["natural_gas", "propane"]})
    zones = pl.DataFrame({"zone": ["4", "5", "6"]})
    scenarios = fuels.join(zones, how="cross")

    # Join building params by zone (R-values, HDD, ACH50, etc.)
    building = load_building_params()
    scenarios = scenarios.join(building, on="zone")

    # Join model-level params (scalars broadcast to all rows)
    model_params = load_model_params()
    for key, value in model_params.items():
        scenarios = scenarios.with_columns(pl.lit(value).alias(key))

    # Join operating params (flatten the nested dict)
    op = load_operating_params()
    scenarios = scenarios.with_columns(
        pl.lit(op["efficiency"]["furnace_afue"]).alias("furnace_afue"),
        pl.lit(op["efficiency"]["ccashp_hspf2"]).alias("ccashp_hspf2"),
        pl.lit(op["maintenance"]["furnace"]).alias("furnace_maintenance_cost"),
        pl.lit(op["maintenance"]["ac"]).alias("ac_maintenance_cost"),
        pl.lit(op["maintenance"]["gas_water_heater"]).alias("gwh_maintenance_cost"),
        pl.lit(op["maintenance"]["ccashp"]).alias("ccashp_maintenance_cost"),
        pl.lit(op["maintenance"]["hpwh"]).alias("hpwh_maintenance_cost"),
        pl.lit(op["fuel_content"]["natural_gas_btu_per_mcf"]).alias("natural_gas_btu_per_mcf"),
        pl.lit(op["fuel_content"]["propane_btu_per_gallon"]).alias("propane_btu_per_gallon"),
        pl.lit(op["hpwh"]["daily_kwh"]).alias("hpwh_daily_kwh"),
    )

    # Gas water heater fuel usage rate depends on fuel type
    scenarios = scenarios.with_columns(
        pl.when(pl.col("fuel") == "natural_gas")
        .then(pl.lit(op["gas_water_heater"]["fuel_usage_rate_nat_gas"]))
        .otherwise(pl.lit(op["gas_water_heater"]["fuel_usage_rate_propane"]))
        .alias("gwh_fuel_usage_rate"),
        pl.lit(op["gas_water_heater"]["daily_operating_hours"]).alias("gwh_daily_operating_hours"),
    )

    # Join fuel prices: electricity (same for all), and fuel-specific price
    fuel_prices = load_fuel_prices()
    elec_price_row = fuel_prices.filter(pl.col("fuel") == "electricity")
    # Electricity price: convert cents/kWh to $/kWh
    elec_price = elec_price_row["avg_price"][0] * 0.01
    scenarios = scenarios.with_columns(
        pl.lit(elec_price).alias("electricity_price"),
    )

    # Natural gas price: $/mcf (already in dollars)
    natgas_price = fuel_prices.filter(pl.col("fuel") == "natural_gas")["avg_price"][0]
    # Propane price: convert cents/gallon to $/gallon
    propane_price = fuel_prices.filter(pl.col("fuel") == "propane")["avg_price"][0] * 0.01

    scenarios = scenarios.with_columns(
        pl.when(pl.col("fuel") == "natural_gas")
        .then(pl.lit(natgas_price))
        .otherwise(pl.lit(propane_price))
        .alias("fuel_price"),
    )

    # Apply overrides before returning
    return _apply_overrides(scenarios, overrides)


# ---------------------------------------------------------------------------
# Computation stage 2: building geometry (Model rows 12-24)
# ---------------------------------------------------------------------------


def compute_building_geometry(overrides: Overrides = None) -> pl.DataFrame:
    """Compute building geometry columns matching Excel rows 12-24.

    Formulas (using E column as reference):
      Row 12: wall_length = sqrt(floor_area / stories)
      Row 14: wall_surface_area = (wall_length * 4) * (stories * wall_height)
      Row 15: attic_floor_area = floor_area / stories
      Row 17: wall_area_excl_windows = wall_surface_area * (1 - window_door_pct)
      Row 18: window_door_area = wall_surface_area * window_door_pct
      Row 21: above_grade_basement_wall_area = 4 * above_grade_height * wall_length
      Row 22: below_grade_basement_wall_area = 4 * below_grade_height * wall_length
      Row 23: basement_floor_perimeter = wall_length * 4
      Row 24: volume = floor_area*wall_height + (above+below)*floor_area/stories
    """
    scenarios = build_scenario_table(overrides)

    return (
        scenarios.with_columns(
            # Row 12: wall_length = sqrt(floor_area / stories)
            (pl.col("floor_area_sf") / pl.col("stories")).sqrt().alias("wall_length_ft"),
        )
        .with_columns(
            # Row 14: wall_surface_area = (wall_length * 4) * (stories * wall_height)
            (pl.col("wall_length_ft") * 4 * pl.col("stories") * pl.col("wall_height_ft")).alias("wall_surface_area_sf"),
            # Row 15: attic_floor_area = floor_area / stories
            (pl.col("floor_area_sf") / pl.col("stories")).alias("attic_floor_area_sf"),
        )
        .with_columns(
            # Row 17: wall_area_excl_windows = wall_surface_area * (1 - window_pct)
            (pl.col("wall_surface_area_sf") * (1 - pl.col("window_door_pct"))).alias("wall_area_excl_windows_sf"),
            # Row 18: window_door_area = wall_surface_area * window_pct
            (pl.col("wall_surface_area_sf") * pl.col("window_door_pct")).alias("window_door_area_sf"),
            # Row 21: above-grade basement wall area = 4 * above_grade_height * wall_length
            (4 * pl.col("above_grade_basement_wall_height_ft") * pl.col("wall_length_ft")).alias(
                "above_grade_basement_wall_area_sf"
            ),
            # Row 22: below-grade basement wall area = 4 * below_grade_height * wall_length
            (4 * pl.col("below_grade_basement_wall_height_ft") * pl.col("wall_length_ft")).alias(
                "below_grade_basement_wall_area_sf"
            ),
            # Row 23: basement floor perimeter = wall_length * 4
            (pl.col("wall_length_ft") * 4).alias("basement_floor_perimeter_ft"),
            # Row 24: volume = floor_area*wall_height + (above+below)*floor_area/stories
            # Excel: =E10*E13+(E19+E20)*E10/2  (where /2 is /stories for 2-story)
            (
                pl.col("floor_area_sf") * pl.col("wall_height_ft")
                + (pl.col("above_grade_basement_wall_height_ft") + pl.col("below_grade_basement_wall_height_ft"))
                * pl.col("floor_area_sf")
                / pl.col("stories")
            ).alias("volume_cf"),
        )
    )


# ---------------------------------------------------------------------------
# Computation stage 3: heat loss rates (Model rows 33-40)
# ---------------------------------------------------------------------------


def compute_heat_loss_rates(overrides: Overrides = None) -> pl.DataFrame:
    """Compute per-component heat loss rates matching Excel rows 33-40.

    All rates are in BTU/hr/degF.

    Formulas (E column reference):
      Row 33: attic = attic_area / R_attic
      Row 34: walls = wall_area_excl_windows / R_walls
      Row 35: windows_doors = window_door_area / R_windows_doors
      Row 36: above_grade_basement = above_grade_area / R_basement_wall
      Row 37: air_changes = 0.018 * (ACH50/20) * volume
      Row 38: below_grade_basement = below_grade_area / R_basement_wall
      Row 39: slab = perimeter * slab_f_factor
      Row 40: total = sum of all components
    """
    scenarios = compute_building_geometry(overrides)

    return scenarios.with_columns(
        # Row 33: attic heat loss
        (pl.col("attic_floor_area_sf") / pl.col("r_attic")).alias("heat_loss_attic"),
        # Row 34: exterior wall heat loss
        (pl.col("wall_area_excl_windows_sf") / pl.col("r_walls")).alias("heat_loss_walls"),
        # Row 35: windows and doors heat loss
        (pl.col("window_door_area_sf") / pl.col("r_windows_doors")).alias("heat_loss_windows_doors"),
        # Row 36: above-grade basement wall heat loss
        (pl.col("above_grade_basement_wall_area_sf") / pl.col("r_basement_wall")).alias(
            "heat_loss_above_grade_basement"
        ),
        # Row 37: infiltration (air changes) heat loss
        # Excel: =0.018*(ACH50/20)*volume
        (0.018 * (pl.col("ach50") / 20) * pl.col("volume_cf")).alias("heat_loss_air_changes"),
        # Row 38: below-grade basement wall heat loss
        (pl.col("below_grade_basement_wall_area_sf") / pl.col("r_basement_wall")).alias(
            "heat_loss_below_grade_basement"
        ),
        # Row 39: slab heat loss = perimeter * F-factor
        (pl.col("basement_floor_perimeter_ft") * pl.col("slab_f_factor")).alias("heat_loss_slab"),
    ).with_columns(
        # Row 40: total heat loss rate = sum of all components
        (
            pl.col("heat_loss_attic")
            + pl.col("heat_loss_walls")
            + pl.col("heat_loss_windows_doors")
            + pl.col("heat_loss_above_grade_basement")
            + pl.col("heat_loss_air_changes")
            + pl.col("heat_loss_below_grade_basement")
            + pl.col("heat_loss_slab")
        ).alias("total_heat_loss_rate"),
    )


# ---------------------------------------------------------------------------
# Computation stage 4: yearly BTU (Model rows 43-46)
# ---------------------------------------------------------------------------


def compute_yearly_btu(overrides: Overrides = None) -> pl.DataFrame:
    """Compute adjusted HDD and yearly BTU matching Excel rows 43-46.

    Formulas:
      Row 45: adjusted_hdd = hdd - epa_hdd_adjustment
      Row 46: yearly_btu = total_heat_loss_rate * adjusted_hdd * 24
    """
    scenarios = compute_heat_loss_rates(overrides)

    return scenarios.with_columns(
        # Row 45: adjusted HDD = raw HDD minus EPA climate adjustment
        (pl.col("hdd") - pl.col("epa_hdd_adjustment")).alias("adjusted_hdd"),
    ).with_columns(
        # Row 46: yearly BTU = total_heat_loss_rate * adjusted_hdd * 24 hours/day
        (pl.col("total_heat_loss_rate") * pl.col("adjusted_hdd") * 24).alias("yearly_btu"),
    )


# ---------------------------------------------------------------------------
# Computation stage 5: system sizing (Model rows 49-55)
# ---------------------------------------------------------------------------


def compute_system_sizing(overrides: Overrides = None) -> pl.DataFrame:
    """Compute system sizing columns matching Excel rows 49-55.

    Formulas:
      Row 49: coldest_day_temp = weighted avg of county design temps by zone
      Row 52: degree_diff = indoor_design_temp - coldest_day_temp
      Row 53: btu_hr = total_heat_loss_rate * degree_diff + internal_heat_gains
      Row 55: system_capacity = btu_hr * sizing_scale_up_factor
    """
    scenarios = compute_yearly_btu(overrides)

    # Join zone-level weighted-average design temperatures
    zone_temps = _compute_zone_design_temps()
    scenarios = scenarios.join(zone_temps, on="zone")

    return (
        scenarios.with_columns(
            # Row 52: degree difference on coldest day
            # Excel: =E51-E49 (indoor_design_temp - coldest_day_temp)
            (pl.col("indoor_design_temp_f") - pl.col("coldest_day_temp_f")).alias("degree_diff_coldest_day"),
        )
        .with_columns(
            # Row 53: BTU/hr on coldest day
            # Excel: =(E40*E52+E50)
            (
                pl.col("total_heat_loss_rate") * pl.col("degree_diff_coldest_day") + pl.col("internal_heat_gains_btu")
            ).alias("btu_hr_coldest_day"),
        )
        .with_columns(
            # Row 55: heating system BTU estimate = BTU/hr * scale-up factor
            (pl.col("btu_hr_coldest_day") * pl.col("sizing_scale_up_factor")).alias("system_capacity_btu_hr"),
        )
    )


# ---------------------------------------------------------------------------
# Helpers: blended averages by zone (service line costs, rebates)
# ---------------------------------------------------------------------------


def _compute_zone_service_line_costs() -> pl.DataFrame:
    """Compute blended average gas service line cost per zone.

    Joins counties to service_line_costs by gas_utility, then computes
    a weighted average of avg_service_line_cost within each zone using
    new_construction_share as weight.

    Counties with no gas service (gas_utility = null) are excluded.

    Returns a DataFrame with columns: zone, service_line_cost.
    """
    counties = load_counties()
    service_lines = load_service_line_costs()

    return (
        counties.filter(pl.col("gas_utility").is_not_null())
        .join(service_lines, on="gas_utility", how="left")
        .with_columns(
            zone_total=pl.col("new_construction_share").sum().over("zone"),
        )
        .with_columns(
            zone_weight=pl.col("new_construction_share") / pl.col("zone_total"),
        )
        .group_by("zone")
        .agg(
            (pl.col("avg_service_line_cost") * pl.col("zone_weight")).sum().alias("service_line_cost"),
        )
    )


def _compute_zone_hpwh_rebates() -> pl.DataFrame:
    """Compute blended average HPWH rebate per zone.

    Joins counties to utility_rebates (technology = 'HPWH') by electric_utility,
    then computes a weighted average of rebate amount within each zone using
    new_construction_share as weight.

    Returns a DataFrame with columns: zone, hpwh_rebate.
    """
    counties = load_counties()
    rebates = load_utility_rebates()

    # Filter to HPWH rebates only and rename for join
    hpwh_rebates = rebates.filter(pl.col("technology") == "HPWH").select(
        pl.col("utility").alias("electric_utility"),
        pl.col("amount").alias("hpwh_rebate_amount"),
    )

    return (
        counties.join(hpwh_rebates, on="electric_utility", how="left")
        .with_columns(
            # Counties without a matching rebate get 0
            pl.col("hpwh_rebate_amount").fill_null(0),
        )
        .with_columns(
            zone_total=pl.col("new_construction_share").sum().over("zone"),
        )
        .with_columns(
            zone_weight=pl.col("new_construction_share") / pl.col("zone_total"),
        )
        .group_by("zone")
        .agg(
            (pl.col("hpwh_rebate_amount") * pl.col("zone_weight")).sum().alias("hpwh_rebate"),
        )
    )


# ---------------------------------------------------------------------------
# Computation stage 6: baseline costs (Model rows 59-96)
# ---------------------------------------------------------------------------


def compute_baseline_costs(overrides: Overrides = None) -> pl.DataFrame:
    """Compute baseline fossil fuel system costs matching Excel rows 59-96.

    Furnace (rows 59-71):
      - equipment cost: average of vendor quotes from equipment.yaml
      - gas tank cost: propane only (from model_params), 0 for natural gas
      - installed cost: equipment + gas tank
      - yearly fuel usage: yearly_btu / (AFUE * fuel_energy_content)
      - yearly fuel cost: usage * fuel_price
      - yearly electrical usage: yearly_btu / 1e6 * kWh_per_MMBTU (blower fans)
      - yearly electrical cost: electrical_kwh * electricity_price
      - yearly maintenance: flat annual cost
      - yearly operating: fuel + electrical + maintenance

    Central AC (rows 74-78):
      - equipment cost: average of vendor quotes
      - yearly operating: maintenance only (cooling costs not modeled)

    Gas Water Heater (rows 81-88):
      - equipment cost: average of vendor quotes
      - yearly fuel usage: fuel_rate * daily_hours * 365
      - yearly fuel cost: usage * fuel_price
      - yearly operating: fuel + maintenance

    Service line (row 91):
      - blended average cost by zone for natural gas; 0 for propane

    Totals (rows 94-96):
      - baseline_equipment_total: furnace_installed + AC + GWH
      - baseline_equipment_with_service_line: above + service line
      - baseline_yearly_operating: furnace_op + AC_op + GWH_op
    """
    scenarios = compute_system_sizing(overrides)

    # Load equipment prices (scalars)
    equipment = load_equipment()
    furnace_cost = equipment.filter(pl.col("device") == "furnace")["avg_price"][0]
    ac_cost = equipment.filter(pl.col("device") == "ac")["avg_price"][0]
    gwh_cost = equipment.filter(pl.col("device") == "gas_water_heater")["avg_price"][0]

    # Propane tank cost from model params
    model_params = load_model_params()
    propane_tank_cost = model_params["propane_tank_cost"]

    # --- Furnace costs ---
    scenarios = scenarios.with_columns(
        # Row 59: furnace equipment cost (same for all scenarios)
        pl.lit(furnace_cost).alias("furnace_equipment_cost"),
        # Row 61: gas tank cost (propane only)
        pl.when(pl.col("fuel") == "propane")
        .then(pl.lit(propane_tank_cost))
        .otherwise(pl.lit(0.0))
        .alias("gas_tank_cost"),
    )

    scenarios = scenarios.with_columns(
        # Row 62: installed cost = equipment + gas tank
        (pl.col("furnace_equipment_cost") + pl.col("gas_tank_cost")).alias("furnace_installed_cost"),
    )

    # Row 65: yearly fuel usage = yearly_btu / (AFUE * energy_content_per_unit)
    scenarios = scenarios.with_columns(
        pl.when(pl.col("fuel") == "natural_gas")
        .then(pl.col("yearly_btu") / (pl.col("furnace_afue") * pl.col("natural_gas_btu_per_mcf")))
        .otherwise(pl.col("yearly_btu") / (pl.col("furnace_afue") * pl.col("propane_btu_per_gallon")))
        .alias("furnace_yearly_fuel_usage"),
    )

    scenarios = scenarios.with_columns(
        # Row 66: yearly fuel cost = usage * price
        (pl.col("furnace_yearly_fuel_usage") * pl.col("fuel_price")).alias("furnace_yearly_fuel_cost"),
        # Row 68: yearly electrical usage (kWh) = yearly_btu / 1e6 * kWh_per_MMBTU
        # The blower runs proportional to heat delivered (yearly_btu is demand, not input)
        (pl.col("yearly_btu") / 1_000_000 * pl.col("furnace_electrical_usage_kwh_per_mmbtu")).alias(
            "furnace_yearly_electrical_kwh"
        ),
    )

    scenarios = scenarios.with_columns(
        # Row 69: yearly electrical cost = kWh * electricity_price
        (pl.col("furnace_yearly_electrical_kwh") * pl.col("electricity_price")).alias("furnace_yearly_electrical_cost"),
    )

    scenarios = scenarios.with_columns(
        # Row 71: yearly operating = fuel + electrical + maintenance
        (
            pl.col("furnace_yearly_fuel_cost")
            + pl.col("furnace_yearly_electrical_cost")
            + pl.col("furnace_maintenance_cost")
        ).alias("furnace_yearly_operating_cost"),
    )

    # --- Central AC costs ---
    scenarios = scenarios.with_columns(
        # Row 74: AC equipment cost
        pl.lit(ac_cost).alias("ac_equipment_cost"),
        # Row 78: AC yearly operating = maintenance only
        pl.col("ac_maintenance_cost").alias("ac_yearly_operating_cost"),
    )

    # --- Gas Water Heater costs ---
    scenarios = scenarios.with_columns(
        # Row 81: GWH equipment cost
        pl.lit(gwh_cost).alias("gwh_equipment_cost"),
        # Row 85: yearly fuel usage = fuel_rate * daily_hours * 365
        (pl.col("gwh_fuel_usage_rate") * pl.col("gwh_daily_operating_hours") * 365).alias("gwh_yearly_fuel_usage"),
    )

    scenarios = scenarios.with_columns(
        # Row 86: yearly fuel cost = usage * price
        (pl.col("gwh_yearly_fuel_usage") * pl.col("fuel_price")).alias("gwh_yearly_fuel_cost"),
    )

    scenarios = scenarios.with_columns(
        # Row 88: yearly operating = fuel + maintenance
        (pl.col("gwh_yearly_fuel_cost") + pl.col("gwh_maintenance_cost")).alias("gwh_yearly_operating_cost"),
    )

    # --- Service line costs (natural gas only) ---
    zone_service_line = _compute_zone_service_line_costs()
    scenarios = scenarios.join(zone_service_line, on="zone", how="left")

    # Set service line cost to 0 for propane (no gas service line needed)
    scenarios = scenarios.with_columns(
        pl.when(pl.col("fuel") == "propane")
        .then(pl.lit(0.0))
        .otherwise(pl.col("service_line_cost"))
        .alias("service_line_cost"),
    )

    # --- Totals ---
    scenarios = scenarios.with_columns(
        # Row 94: equipment total = furnace_installed + AC + GWH
        (pl.col("furnace_installed_cost") + pl.col("ac_equipment_cost") + pl.col("gwh_equipment_cost")).alias(
            "baseline_equipment_total"
        ),
    )

    scenarios = scenarios.with_columns(
        # Row 95: equipment + service line
        (pl.col("baseline_equipment_total") + pl.col("service_line_cost")).alias(
            "baseline_equipment_with_service_line"
        ),
        # Row 96: yearly operating total
        (
            pl.col("furnace_yearly_operating_cost")
            + pl.col("ac_yearly_operating_cost")
            + pl.col("gwh_yearly_operating_cost")
        ).alias("baseline_yearly_operating"),
    )

    return scenarios


# ---------------------------------------------------------------------------
# Computation stage 7: heat pump costs (Model rows 100-123)
# ---------------------------------------------------------------------------


def compute_heat_pump_costs(overrides: Overrides = None) -> pl.DataFrame:
    """Compute heat pump system costs matching Excel rows 100-123.

    ccASHP (rows 100-109):
      - equipment cost: zone-dependent from equipment.yaml
      - Clean Heat rebate: $0 (zeroed in the current model)
      - federal tax credit: $0 (zeroed in the current model)
      - net cost: equipment - rebate - tax_credit
      - yearly kWh: yearly_btu / (HSPF2 * 1000) where HSPF2 is BTU/Wh
      - yearly electrical cost: kWh * electricity_price
      - yearly maintenance: flat annual cost
      - yearly operating: electrical + maintenance

    HPWH (rows 112-120):
      - device cost: from equipment.yaml
      - rebate: blended average by zone, weighted by new_construction_share
      - net cost: device - rebate
      - yearly kWh: daily_kwh * 365
      - yearly electrical cost: kWh * electricity_price
      - yearly maintenance: flat annual cost
      - yearly operating: electrical + maintenance

    Totals (rows 122-123):
      - hp_equipment_total: ccASHP_net + HPWH_net
      - hp_yearly_operating_total: ccASHP_operating + HPWH_operating
    """
    scenarios = compute_baseline_costs(overrides)

    # Load equipment prices
    equipment = load_equipment()

    # ccASHP: zone-dependent pricing
    ccashp_zone4 = equipment.filter((pl.col("device") == "ccASHP") & (pl.col("zones").list.contains("4")))["avg_price"][
        0
    ]
    ccashp_zone56 = equipment.filter((pl.col("device") == "ccASHP") & (pl.col("zones").list.contains("5")))[
        "avg_price"
    ][0]

    hpwh_cost = equipment.filter(pl.col("device") == "hpwh")["avg_price"][0]

    # --- ccASHP costs ---
    scenarios = scenarios.with_columns(
        # Row 100: ccASHP equipment cost (zone-dependent)
        pl.when(pl.col("zone") == "4")
        .then(pl.lit(ccashp_zone4))
        .otherwise(pl.lit(ccashp_zone56))
        .alias("ccashp_equipment_cost"),
        # Row 101: Clean Heat rebate (currently $0 for ccASHP)
        pl.lit(0.0).alias("ccashp_rebate"),
        # Row 102: Federal tax credit (currently $0)
        pl.lit(0.0).alias("ccashp_federal_tax_credit"),
    )

    scenarios = scenarios.with_columns(
        # Row 103: net cost = equipment - rebate - tax_credit
        (pl.col("ccashp_equipment_cost") - pl.col("ccashp_rebate") - pl.col("ccashp_federal_tax_credit")).alias(
            "ccashp_net_cost"
        ),
    )

    scenarios = scenarios.with_columns(
        # Row 106: yearly kWh = yearly_btu / (HSPF2 * 1000)
        # HSPF2 is in BTU/Wh; multiply by 1000 to convert to BTU/kWh
        (pl.col("yearly_btu") / (pl.col("ccashp_hspf2") * 1000)).alias("ccashp_yearly_kwh"),
    )

    scenarios = scenarios.with_columns(
        # Row 107: yearly electrical cost = kWh * price
        (pl.col("ccashp_yearly_kwh") * pl.col("electricity_price")).alias("ccashp_yearly_electrical_cost"),
    )

    scenarios = scenarios.with_columns(
        # Row 109: yearly operating = electrical + maintenance
        (pl.col("ccashp_yearly_electrical_cost") + pl.col("ccashp_maintenance_cost")).alias(
            "ccashp_yearly_operating_cost"
        ),
    )

    # --- HPWH costs ---
    # Join zone-level blended HPWH rebates
    zone_hpwh_rebates = _compute_zone_hpwh_rebates()
    scenarios = scenarios.join(zone_hpwh_rebates, on="zone", how="left")

    scenarios = scenarios.with_columns(
        # Row 112: HPWH device cost
        pl.lit(hpwh_cost).alias("hpwh_device_cost"),
    )

    scenarios = scenarios.with_columns(
        # Row 114: net cost = device - rebate
        (pl.col("hpwh_device_cost") - pl.col("hpwh_rebate")).alias("hpwh_net_cost"),
        # Row 117: yearly kWh = daily_kwh * 365
        (pl.col("hpwh_daily_kwh") * 365).alias("hpwh_yearly_kwh"),
    )

    scenarios = scenarios.with_columns(
        # Row 118: yearly electrical cost = kWh * price
        (pl.col("hpwh_yearly_kwh") * pl.col("electricity_price")).alias("hpwh_yearly_electrical_cost"),
    )

    scenarios = scenarios.with_columns(
        # Row 120: yearly operating = electrical + maintenance
        (pl.col("hpwh_yearly_electrical_cost") + pl.col("hpwh_maintenance_cost")).alias("hpwh_yearly_operating_cost"),
    )

    # --- HP Totals ---
    scenarios = scenarios.with_columns(
        # Row 122: equipment total = ccASHP_net + HPWH_net
        (pl.col("ccashp_net_cost") + pl.col("hpwh_net_cost")).alias("hp_equipment_total"),
        # Row 123: yearly operating total
        (pl.col("ccashp_yearly_operating_cost") + pl.col("hpwh_yearly_operating_cost")).alias(
            "hp_yearly_operating_total"
        ),
    )

    return scenarios


def compute_savings(overrides: Overrides = None) -> pl.DataFrame:
    """Compute savings comparison matching Excel rows 126-134.

    Adds columns:
      - construction_savings: baseline_equipment_total - hp_equipment_total
      - construction_savings_with_service_line: baseline_equipment_with_service_line - hp_equipment_total
      - mortgage_savings: annual difference in mortgage payments (no service line)
      - mortgage_savings_with_service_line: annual difference in mortgage payments (with service line)
      - operating_savings: baseline_yearly_operating - hp_yearly_operating_total
      - total_yearly_savings: mortgage_savings + operating_savings
      - total_yearly_savings_with_service_line: mortgage_savings_with_sl + operating_savings
      - present_value_15yr: total_yearly_savings_with_service_line * PV annuity factor

    The PMT formula computes annual mortgage payments using annual compounding:
      pmt = (annual_rate * principal) / (1 - (1 + annual_rate)^(-n_years))

    Mortgage savings = PMT_baseline - PMT_hp, i.e., the annual reduction
    in mortgage payments from choosing HP over baseline. Positive when baseline
    equipment costs more (HP saves money on the mortgage).
    """
    scenarios = compute_heat_pump_costs(overrides)

    # Apply overrides for mortgage_rate (row 126)
    scenarios = _apply_overrides(scenarios, overrides)

    # Annual mortgage rate and term in years. The Excel model uses annual
    # compounding (PMT with annual rate and 30 periods), not monthly.
    annual_rate = pl.col("mortgage_rate")
    n_years = pl.col("mortgage_term_years")

    # PMT helper: annual payment for a given principal (positive outflow)
    # pmt = (rate * pv) / (1 - (1 + rate)^(-n))
    def _pmt(principal: pl.Expr) -> pl.Expr:
        return (annual_rate * principal) / (pl.lit(1.0) - (pl.lit(1.0) + annual_rate).pow(-n_years))

    # Row 127-128: Construction cost savings
    scenarios = scenarios.with_columns(
        # Row 127: construction savings (without service line)
        (pl.col("baseline_equipment_total") - pl.col("hp_equipment_total")).alias("construction_savings"),
        # Row 128: construction savings (with service line)
        (pl.col("baseline_equipment_with_service_line") - pl.col("hp_equipment_total")).alias(
            "construction_savings_with_service_line"
        ),
    )

    # Row 129-130: Mortgage savings (annual difference in mortgage payments)
    # Positive when baseline equipment costs more -> lower HP mortgage
    scenarios = scenarios.with_columns(
        # Row 129: mortgage savings (no service line)
        (_pmt(pl.col("baseline_equipment_total")) - _pmt(pl.col("hp_equipment_total"))).alias("mortgage_savings"),
        # Row 130: mortgage savings (with service line)
        (_pmt(pl.col("baseline_equipment_with_service_line")) - _pmt(pl.col("hp_equipment_total"))).alias(
            "mortgage_savings_with_service_line"
        ),
    )

    # Row 131: Operating cost savings
    scenarios = scenarios.with_columns(
        (pl.col("baseline_yearly_operating") - pl.col("hp_yearly_operating_total")).alias("operating_savings"),
    )

    # Row 132-133: Total yearly savings
    scenarios = scenarios.with_columns(
        # Row 132: total yearly savings (no service line)
        (pl.col("mortgage_savings") + pl.col("operating_savings")).alias("total_yearly_savings"),
        # Row 133: total yearly savings (with service line)
        (pl.col("mortgage_savings_with_service_line") + pl.col("operating_savings")).alias(
            "total_yearly_savings_with_service_line"
        ),
    )

    # Row 134: 15-year present value at discount rate
    # PV of annuity = payment * (1 - (1 + r)^(-n)) / r
    discount_rate = pl.col("discount_rate")
    analysis_years = pl.col("analysis_period_years")
    pv_annuity_factor = (pl.lit(1.0) - (pl.lit(1.0) + discount_rate).pow(-analysis_years)) / discount_rate

    scenarios = scenarios.with_columns(
        (pl.col("total_yearly_savings_with_service_line") * pv_annuity_factor).alias("present_value_15yr"),
    )

    return scenarios


def _compute_survey_weights() -> pl.DataFrame:
    """Compute heating survey weights for weighted average calculations.

    Returns a DataFrame with one row per (fuel, zone) combination containing:
      - survey_count: number of survey respondents using this fuel in this zone
      - total_ff_survey_responses: total fossil fuel respondents in this zone
      - pct_ff_using_fuel: fraction of FF respondents using this fuel
    """
    survey = load_heating_survey()

    # Natural gas = "Furnace + Gas" + "Boiler + Gas"
    # Propane = "Furnace + Propane or Oil" + "Boiler + Propane or Oil"
    gas_types = ["Furnace + Gas", "Boiler + Gas"]
    propane_types = ["Furnace + Propane or Oil", "Boiler + Propane or Oil"]

    rows = []
    for zone in ["4", "5", "6"]:
        count_col = f"zone_{zone}_count"
        gas_count = survey.filter(pl.col("system_type").is_in(gas_types))[count_col].sum()
        propane_count = survey.filter(pl.col("system_type").is_in(propane_types))[count_col].sum()
        total_ff = gas_count + propane_count

        rows.append(
            {"fuel": "natural_gas", "zone": zone, "survey_count": gas_count, "total_ff_survey_responses": total_ff}
        )
        rows.append(
            {"fuel": "propane", "zone": zone, "survey_count": propane_count, "total_ff_survey_responses": total_ff}
        )

    weights = pl.DataFrame(rows)

    # pct_ff_using_fuel = survey_count / total_ff_survey_responses
    return weights.with_columns(
        (pl.col("survey_count") / pl.col("total_ff_survey_responses")).alias("pct_ff_using_fuel"),
    )


def _compute_zone_new_construction_shares() -> pl.DataFrame:
    """Compute the fraction of new construction in each zone.

    Returns a DataFrame with columns: zone, pct_new_construction_in_zone.
    """
    counties = load_counties()
    return counties.group_by("zone").agg(pl.col("new_construction_share").sum().alias("pct_new_construction_in_zone"))


def compute_weighted_averages(overrides: Overrides = None) -> pl.DataFrame:
    """Compute weighted statewide and zonewide savings matching Excel rows 137-149.

    Returns a DataFrame with two groups of rows:

    1. Six scenario rows (fuel x zone) with columns:
       survey_count, total_ff_survey_responses, pct_ff_using_fuel,
       pct_new_construction_in_zone, pct_new_construction_fuel_zone

    2. Aggregate rows keyed by 'key' column:
       - fuel-level: key="natural_gas" or "propane" with weighted_statewide_savings_by_fuel
       - zone-level: key="4","5","6" with weighted_zonewide_savings
       - overall: key="overall" with weighted_statewide_savings and weighted_statewide_pv

    Uses heating survey data (what fraction of new construction uses each fuel
    type by zone) and county data (fraction of new construction in each zone)
    to produce statewide weighted averages.
    """
    # Get the full savings table
    savings = compute_savings(overrides)

    # Compute survey weights and zone new construction shares
    survey_weights = _compute_survey_weights()
    zone_shares = _compute_zone_new_construction_shares()

    # Join survey weights onto the 6-row savings table
    scenarios = savings.join(survey_weights, on=["fuel", "zone"])

    # Join zone new construction shares
    scenarios = scenarios.join(zone_shares, on="zone")

    # Row 141: pct of new construction in zone using this fuel
    scenarios = scenarios.with_columns(
        (pl.col("pct_ff_using_fuel") * pl.col("pct_new_construction_in_zone")).alias("pct_new_construction_fuel_zone"),
    )

    # --- Build aggregate rows ---

    # Row 144: Weighted statewide yearly savings by fuel type
    # For each fuel, weighted average of total_yearly_savings_with_service_line
    # across zones, weighted by pct_new_construction_in_zone (zone share of
    # new construction, regardless of fuel mix within zone)
    fuel_agg = (
        scenarios.group_by("fuel")
        .agg(
            (pl.col("total_yearly_savings_with_service_line") * pl.col("pct_new_construction_in_zone")).sum()
            / pl.col("pct_new_construction_in_zone").sum()
        )
        .rename({"fuel": "key", "total_yearly_savings_with_service_line": "weighted_statewide_savings_by_fuel"})
    )

    # Row 146: Weighted zonewide yearly savings (both fuels combined per zone)
    # For each zone, weighted average across fuel types, weighted by pct_ff_using_fuel
    zone_agg = (
        scenarios.group_by("zone")
        .agg(
            (pl.col("total_yearly_savings_with_service_line") * pl.col("pct_ff_using_fuel")).sum()
            / pl.col("pct_ff_using_fuel").sum()
        )
        .rename({"zone": "key", "total_yearly_savings_with_service_line": "weighted_zonewide_savings"})
    )

    # Row 148-149: Weighted overall statewide savings
    # Sum of (savings * weight) across all 6 scenarios
    overall_savings = scenarios.select(
        (pl.col("total_yearly_savings_with_service_line") * pl.col("pct_new_construction_fuel_zone")).sum()
        / pl.col("pct_new_construction_fuel_zone").sum()
    ).item()

    # PV of overall statewide savings
    discount_rate = scenarios["discount_rate"][0]
    analysis_years = scenarios["analysis_period_years"][0]
    pv_factor = (1 - (1 + discount_rate) ** (-analysis_years)) / discount_rate
    overall_pv = overall_savings * pv_factor

    overall_agg = pl.DataFrame(
        {
            "key": ["overall"],
            "weighted_statewide_savings": [overall_savings],
            "weighted_statewide_pv": [overall_pv],
        }
    )

    # Combine all aggregate rows using diagonal concatenation
    # (each aggregate has different columns — align fills with null)
    aggregates = pl.concat([fuel_agg, zone_agg, overall_agg], how="diagonal")

    # Add a 'key' column to scenarios for compatibility with _get_weighted_avg_value
    scenarios = scenarios.with_columns(pl.lit(None).cast(pl.Utf8).alias("key"))

    # Add missing columns to scenarios and aggregates so they can be concatenated
    # The scenario rows need aggregate columns (null), aggregates need scenario columns (null)
    result = pl.concat([scenarios, aggregates], how="diagonal")

    return result


def run_model() -> pl.DataFrame:
    """Run the full model pipeline and return the 6-row result table.

    Loads all data, builds scenarios, computes building geometry, heat loss,
    yearly BTU, system sizing, baseline costs, heat pump costs, and savings.
    Returns the 6-row result DataFrame (3 zones x 2 fuels, ccASHP only).
    """
    return compute_savings()


def _unit_suffix(unit: str) -> str:
    """Map unit tokens to column-name suffixes."""
    return {"$": "dollars", "$/yr": "dollars_per_year", "$_PV": "dollars_pv"}[unit]


def build_tidy_results(savings: pl.DataFrame) -> pl.DataFrame:
    """Reshape model results into a wide-row DataFrame (12 rows x 23 cols).

    Each row is one scenario (baseline_tech x hp_tech x geography).  Columns
    encode the side, measure, and unit in their names so every metric for a
    scenario is visible in a single row::

        baseline_tech | hp_tech | geography | baseline-equipment_cost-dollars | …

    Weighting is implicit in the identifier columns:

    * **baseline_tech** ``natural_gas_furnace`` / ``propane_furnace`` = single
      fuel; ``all_fossil_fuels`` = weighted across fuels (by heating-survey share).
    * **geography** ``Zone 4/5/6`` = single zone; ``Statewide`` = weighted
      across zones (by new-construction share).

    Positive deltas mean the heat pump is cheaper / saves money.
    """
    # -- Measure definitions ---------------------------------------------------
    # (measure_name, baseline_source_col, hp_source_col, unit)
    paired: list[tuple[str, str, str, str]] = [
        ("equipment_cost", "baseline_equipment_total", "hp_equipment_total", "$"),
        ("equipment_cost_incl_service_line", "baseline_equipment_with_service_line", "hp_equipment_total", "$"),
        ("yearly_operating", "baseline_yearly_operating", "hp_yearly_operating_total", "$/yr"),
        ("yearly_mortgage", "_bl_mortgage", "_hp_mortgage", "$/yr"),
        ("yearly_mortgage_incl_service_line", "_bl_mortgage_sl", "_hp_mortgage", "$/yr"),
    ]
    # (measure_name, source_col, unit) — ordered so headline numbers come first
    delta_only: list[tuple[str, str, str]] = [
        ("yearly_total_savings", "total_yearly_savings_with_service_line", "$/yr"),
        ("present_value_15yr", "present_value_15yr", "$_PV"),
        ("construction_savings", "construction_savings_with_service_line", "$"),
        ("yearly_mortgage_savings", "mortgage_savings_with_service_line", "$/yr"),
        ("yearly_operating_savings", "operating_savings", "$/yr"),
    ]

    # -- Enrich with mortgage payment columns ----------------------------------
    rate = savings["mortgage_rate"][0]
    n = savings["mortgage_term_years"][0]
    pmt_factor = rate / (1 - (1 + rate) ** (-n))

    enriched = savings.with_columns(
        (pl.col("baseline_equipment_total") * pmt_factor).alias("_bl_mortgage"),
        (pl.col("baseline_equipment_with_service_line") * pmt_factor).alias("_bl_mortgage_sl"),
        (pl.col("hp_equipment_total") * pmt_factor).alias("_hp_mortgage"),
    )

    # -- Join weights ----------------------------------------------------------
    survey_weights = _compute_survey_weights()
    zone_shares = _compute_zone_new_construction_shares()
    w = enriched.join(survey_weights, on=["fuel", "zone"]).join(zone_shares, on="zone")
    w = w.with_columns(
        (pl.col("pct_ff_using_fuel") * pl.col("pct_new_construction_in_zone")).alias("_w_overall"),
    )

    # Collect every value column that appears in the output
    val_cols: list[str] = []
    for _, bl, hp, _ in paired:
        val_cols.extend([bl, hp])
    for _, col, _ in delta_only:
        val_cols.append(col)
    val_cols = list(dict.fromkeys(val_cols))  # dedupe, preserve order

    # -- Helpers ---------------------------------------------------------------
    def _wmean(df: pl.DataFrame, weight_col: str) -> dict[str, float]:
        total = df[weight_col].sum()
        return {c: float((df[c] * df[weight_col]).sum() / total) for c in val_cols}

    def _make_row(
        bt: str,
        ht: str,
        geo: str,
        src: dict[str, float] | pl.DataFrame,
        idx: int | None = None,
    ) -> dict[str, Any]:
        row: dict[str, Any] = {"baseline_tech": bt, "hp_tech": ht, "geography": geo}
        # Delta-only (headline) measures first
        for name, col, unit in delta_only:
            sfx = _unit_suffix(unit)
            val = src[col] if isinstance(src, dict) else float(src[col][idx])
            row[f"delta-{name}-{sfx}"] = round(val, 2)
        # Then paired cost breakdowns (baseline / hp / delta)
        for name, bl_col, hp_col, unit in paired:
            sfx = _unit_suffix(unit)
            bl = src[bl_col] if isinstance(src, dict) else float(src[bl_col][idx])
            hp = src[hp_col] if isinstance(src, dict) else float(src[hp_col][idx])
            row[f"baseline-{name}-{sfx}"] = round(bl, 2)
            row[f"hp-{name}-{sfx}"] = round(hp, 2)
            row[f"delta-{name}-{sfx}"] = round(bl - hp, 2)
        return row

    # -- Build rows ------------------------------------------------------------
    rows: list[dict[str, Any]] = []

    # 6 individual scenario rows (fuel x zone)
    for i in range(w.height):
        fuel = w["fuel"][i]
        zone = w["zone"][i]
        rows.append(_make_row(f"{fuel}_furnace", "ccASHP", f"Zone {zone}", w, i))

    # 2 statewide-by-fuel rows (weighted across zones)
    for fuel in ["natural_gas", "propane"]:
        agg = _wmean(w.filter(pl.col("fuel") == fuel), "pct_new_construction_in_zone")
        rows.append(_make_row(f"{fuel}_furnace", "ccASHP", "Statewide", agg))

    # 3 zone-wide rows (weighted across fuels)
    for zone in ["4", "5", "6"]:
        agg = _wmean(w.filter(pl.col("zone") == zone), "pct_ff_using_fuel")
        rows.append(_make_row("all_fossil_fuels", "ccASHP", f"Zone {zone}", agg))

    # 1 overall statewide row
    rows.append(_make_row("all_fossil_fuels", "ccASHP", "Statewide", _wmean(w, "_w_overall")))

    return pl.DataFrame(rows)


def _get_git_commit_hash() -> str:
    """Return the short git commit hash, or 'unknown' if not in a git repo."""
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return "unknown"


def _save_tidy_results(tidy: pl.DataFrame, output_dir: Path) -> Path:
    """Save tidy results to a timestamped CSV with a git metadata header.

    Returns the path to the saved file.
    """
    output_dir.mkdir(exist_ok=True)

    commit_hash = _get_git_commit_hash()
    now = datetime.now(tz=UTC)
    date_label = now.strftime("%Y-%m-%d")
    timestamp_file = now.strftime("%Y%m%d_%H%M%S")

    metadata_header = f"# git commit: {commit_hash} ({date_label})\n"

    out_path = output_dir / f"{timestamp_file}_results.csv"
    csv_bytes = tidy.write_csv()
    with open(out_path, "w") as f:
        f.write(metadata_header)
        f.write(csv_bytes)

    return out_path


def main() -> None:
    """Run the model, print tidy results, and save to CSV."""
    tidy = build_tidy_results(compute_savings())

    with pl.Config(
        tbl_rows=-1,
        tbl_cols=-1,
        fmt_str_lengths=40,
        fmt_float="full",
    ):
        print(tidy)

    # Save to output/
    output_dir = Path(__file__).parent / "output"
    out_path = _save_tidy_results(tidy, output_dir)
    print()
    print(f"Results saved to: {out_path}")


if __name__ == "__main__":
    main()
