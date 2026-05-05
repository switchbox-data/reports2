"""Build workbooks for RIE 1-8 and RIE 1-9 discovery responses.

RIE 1-8: "Under current default rates, 79% of gas-heated households
in Rhode Island would lose money after switching to heat pumps."

RIE 1-9: "With such rates 87% of gas-heated households would save
money after switching to heat pumps."

Both percentages use LMI-adjusted bills (32% enrollment tier).

Run from the report directory::

    uv run python -m testimony_response.build_RIE_1_8_1_9_workbook
    uv run python -m testimony_response.build_RIE_1_8_1_9_workbook --upload
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import polars as pl
import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

from lib.rdp import fetch_rdp_file, parse_urdb_json

# ---------------------------------------------------------------------------
# Constants.
# ---------------------------------------------------------------------------
UTILITY = "rie"
BATCH = "ri_20260331_r1-20_rate_case_test_year"
S3_BASE = "s3://data.sb/switchbox/cairo/outputs/hp_rates"
_state = "ri"

PATH_BILLS_12 = f"{S3_BASE}/{_state}/all_utilities/{BATCH}/run_1+2/comb_bills_year_target/"
PATH_BILLS_34 = f"{S3_BASE}/{_state}/all_utilities/{BATCH}/run_3+4/comb_bills_year_target/"
PATH_BILLS_1920 = f"{S3_BASE}/{_state}/all_utilities/{BATCH}/run_19+20/comb_bills_year_target/"

RDP_REF = "e9e5088"
RDP_REV_YAML_PATH = "rate_design/hp_rates/ri/config/rev_requirement/rie_rate_case_test_year.yaml"
RDP_TARIFF_DIR = "rate_design/hp_rates/ri/config/tariffs/electric"

REPORTS2_GITHUB_BASE = "https://github.com/switchbox-data/reports2/blob"

SPREADSHEET_1_8 = "1TEURpTKhM3ddpPagNxq1bT0oB24RyoorD4y7EVfFeUY"
SPREADSHEET_1_9 = "1wocSf02gT7WS9G_vxs70d1SG1IOwhPLcUZGRuHXDRB8"

BILL_COLS = [
    "elec_total_bill",
    "elec_total_bill_lmi_32",
    "gas_total_bill",
    "gas_total_bill_lmi_32",
    "oil_total_bill",
    "propane_total_bill",
]
KWH_COLS = ["elec_delivery_bill", "elec_fixed_charge"]
LMI_BILL_COLS = [
    "elec_total_bill_lmi_32",
    "gas_total_bill_lmi_32",
    "oil_total_bill",
    "propane_total_bill",
]

# Scenario descriptions for the assumptions sheet.
SCENARIOS: dict[str, dict[str, str]] = {
    "1-8": {
        "request": (
            "RIE 1-8: Under current default rates, 79% of gas-heated "
            "households in Rhode Island would lose money after switching "
            "to heat pumps."
        ),
        "before_desc": "Run 1+2: Current HVAC, default delivery + supply rates",
        "after_desc": "Run 3+4: Heat pump upgrade, same default rates",
        "before_path": PATH_BILLS_12,
        "after_path": PATH_BILLS_34,
        "headline": "Percentage that LOSE money (1 - pct_save)",
    },
    "1-9": {
        "request": (
            "RIE 1-9: With such rates 87% of gas-heated households would save money after switching to heat pumps."
        ),
        "before_desc": "Run 1+2: Current HVAC, default delivery + supply rates",
        "after_desc": "Run 19+20: Heat pump upgrade, proposed HP flat rate",
        "before_path": PATH_BILLS_12,
        "after_path": PATH_BILLS_1920,
        "headline": "Percentage that SAVE money (pct_save)",
    },
}


# ---------------------------------------------------------------------------
# Permalink helpers.
# ---------------------------------------------------------------------------
def _reports2_head_sha() -> str:
    if not hasattr(_reports2_head_sha, "_cached"):
        repo_root = Path(__file__).resolve().parents[3]
        sha = subprocess.check_output(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        _reports2_head_sha._cached = sha  # type: ignore[attr-defined]
    return _reports2_head_sha._cached  # type: ignore[attr-defined]


def _reports2_permalink(rel_path: str) -> str:
    return f"{REPORTS2_GITHUB_BASE}/{_reports2_head_sha()}/{rel_path}"


# ---------------------------------------------------------------------------
# Data loading.
# ---------------------------------------------------------------------------
def _load_annual_bills(path: str) -> pl.DataFrame:
    """Load annual master bills for RIE, selecting only needed columns."""
    lf = pl.scan_parquet(path, hive_partitioning=True)
    result = (
        lf.filter((pl.col("sb.electric_utility") == UTILITY) & (pl.col("month") == "Annual"))
        .select(
            "bldg_id",
            "weight",
            "heats_with_natgas",
            *BILL_COLS,
            *KWH_COLS,
        )
        .collect()
    )
    assert isinstance(result, pl.DataFrame)
    return result


def _load_inputs() -> dict:
    """Pull revenue-requirement YAML, tariff rates, and report tariff-table values."""
    import pickle

    raw_yaml = fetch_rdp_file(RDP_REV_YAML_PATH, RDP_REF)
    rev = yaml.safe_load(raw_yaml)
    total_rr = float(rev["total_delivery_revenue_requirement"])
    n_customers = float(rev["test_year_customer_count"])
    ty_kwh = float(rev["test_year_residential_kwh"])

    def _fetch_tariff(filename: str) -> dict:
        return parse_urdb_json(fetch_rdp_file(f"{RDP_TARIFF_DIR}/{filename}", RDP_REF))

    default_del = _fetch_tariff("rie_default_calibrated.json")
    hp_flat_del = _fetch_tariff("rie_hp_flat_calibrated.json")
    hp_flat_sup = _fetch_tariff("rie_hp_flat_supply_calibrated.json")

    default_vol = float(default_del["items"][0]["energyratestructure"][0][0]["rate"])
    annual_fixed_per_customer = (total_rr - default_vol * ty_kwh) / n_customers

    rv = pickle.loads(Path("cache/report_variables.pkl").read_bytes())

    return {
        "default_vol_usd_per_kwh": default_vol,
        "annual_fixed_per_customer": annual_fixed_per_customer,
        "tariff_table": {
            "elec_customer_charge": rv["elec_customer_charge"],
            "elec_other_fixed_charges": rv["elec_other_fixed_charges"],
            "elec_delivery_avg_cents": rv["elec_delivery_avg_cents"],
            "elec_lrs_winter_cents": rv["elec_lrs_winter_cents"],
            "elec_lrs_summer_cents": rv["elec_lrs_summer_cents"],
            "elec_lrs_fall_cents": rv["elec_lrs_fall_cents"],
            "gas_fixed_charge": rv["gas_fixed_charge"],
            "gas_nonheating_fixed_charge": rv["gas_nonheating_fixed_charge"],
            "gas_avg_per_therm": rv["gas_avg_per_therm"],
            "gas_nonheating_avg_per_therm": rv["gas_nonheating_avg_per_therm"],
            "hp_flat_delivery_cents": float(hp_flat_del["items"][0]["energyratestructure"][0][0]["rate"]) * 100,
            "hp_flat_supply_cents": float(hp_flat_sup["items"][0]["energyratestructure"][0][0]["rate"]) * 100,
        },
    }


def _derive_annual_kwh(bills: pl.DataFrame, inputs: dict) -> pl.DataFrame:
    """Add annual_kwh column derived from the delivery bill components."""
    return bills.with_columns(
        (
            (pl.col("elec_fixed_charge") + pl.col("elec_delivery_bill") - inputs["annual_fixed_per_customer"])
            / inputs["default_vol_usd_per_kwh"]
        ).alias("annual_kwh")
    )


# ---------------------------------------------------------------------------
# Formatting helpers.
# ---------------------------------------------------------------------------
def _header_fill(ws, row: int, n_cols: int) -> None:
    fill = PatternFill("solid", fgColor="E8E8E8")
    for c in range(1, n_cols + 1):
        ws.cell(row=row, column=c).font = Font(bold=True)
        ws.cell(row=row, column=c).fill = fill


def _autosize(ws, widths: dict[str, int]) -> None:
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


# ---------------------------------------------------------------------------
# Sheet writers.
# ---------------------------------------------------------------------------
def _write_assumptions(wb: Workbook, scenario_id: str, inputs: dict) -> None:
    ws = wb.create_sheet("assumptions", 0)
    scen = SCENARIOS[scenario_id]
    tt = inputs["tariff_table"]

    ws["A1"] = f"RIE {scenario_id} — Supporting calculation"
    ws["A1"].font = Font(bold=True, size=14)
    ws.merge_cells("A1:C1")

    row = 3

    # --- Key-value rows (2 columns) ----------------------------------------
    kv_rows: list[tuple[str, str]] = [
        ("Discovery request", scen["request"]),
        ("", ""),
        ("Assumptions", ""),
        (
            "LMI discount tier",
            "32% enrollment (RI's current rate). The _lmi_32 bill columns "
            "apply existing utility LMI discounts to enrolled low-income "
            "households. Non-enrolled households see the undiscounted bill.",
        ),
        (
            "Bill columns used",
            "elec_total_bill_lmi_32 + gas_total_bill_lmi_32 + oil_total_bill + propane_total_bill",
        ),
        (
            "Gas-heated filter",
            "heats_with_natgas == true (ResStock heating fuel assignment)",
        ),
        (
            "Save definition",
            "delta < 0 (annual LMI-adjusted energy bill decreases after HP)",
        ),
        (
            "Lose definition",
            "delta > 0 (annual LMI-adjusted energy bill increases after HP)",
        ),
    ]
    bold_labels = {"Assumptions", "Data sources", "per_building columns"}
    for label, value in kv_rows:
        ws.cell(row=row, column=1, value=label)
        if label in bold_labels:
            ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2, value=value)
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        row += 1

    # --- Tariff table (3 columns) -------------------------------------------
    row += 1
    ws.cell(row=row, column=1, value="Default tariffs (before)")
    ws.cell(row=row, column=1).font = Font(bold=True)
    cite = "Rhode Island Energy, Docket No. 2545-GE (2025). Blazunas Schedules & Workpapers, Book 21, PRB-1-ELEC."
    ws.cell(row=row, column=2, value=cite)
    ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
    row += 1

    _header_fill(ws, row, 3)
    for c, hdr in enumerate(["Tariff", "Fixed charge", "Volumetric rate"], 1):
        ws.cell(row=row, column=c, value=hdr)
    row += 1

    default_tariff_rows: list[tuple[str, str, str]] = [
        (
            "Electricity — customer charge (A-16)",
            f"${tt['elec_customer_charge']:.2f} /mo",
            "—",
        ),
        (
            "Electricity — RE Growth + LIHEAP (A-16)",
            f"${tt['elec_other_fixed_charges']:.2f} /mo",
            "—",
        ),
        (
            "Electricity — delivery (A-16)",
            "—",
            f"{tt['elec_delivery_avg_cents']:.2f} ¢/kWh",
        ),
        (
            "Electricity — supply, winter (LRS, Jan–Mar)",  # noqa: RUF001
            "—",
            f"{tt['elec_lrs_winter_cents']:.2f} ¢/kWh",
        ),
        (
            "Electricity — supply, summer (LRS, Apr–Sep)",  # noqa: RUF001
            "—",
            f"{tt['elec_lrs_summer_cents']:.2f} ¢/kWh",
        ),
        (
            "Electricity — supply, fall (LRS, Oct–Dec)",  # noqa: RUF001
            "—",
            f"{tt['elec_lrs_fall_cents']:.2f} ¢/kWh",
        ),
        (
            "Natural gas — Rate 12 (heating)",
            f"${tt['gas_fixed_charge']:.2f} /mo",
            f"${tt['gas_avg_per_therm']:.3f} /therm",
        ),
        (
            "Natural gas — Rate 10 (non-heating)",
            f"${tt['gas_nonheating_fixed_charge']:.2f} /mo",
            f"${tt['gas_nonheating_avg_per_therm']:.3f} /therm",
        ),
        ("Heating oil (EIA)", "—", "$3.48–$4.10 /gal (monthly prices)"),  # noqa: RUF001
        ("Propane (EIA)", "—", "$3.44–$3.67 /gal (monthly prices)"),  # noqa: RUF001
    ]
    for tariff, fixed, vol in default_tariff_rows:
        ws.cell(row=row, column=1, value=tariff)
        ws.cell(row=row, column=2, value=fixed)
        ws.cell(row=row, column=3, value=vol)
        row += 1

    # --- After tariffs (scenario-specific) ----------------------------------
    if scenario_id == "1-9":
        row += 1
        ws.cell(row=row, column=1, value="HP subclass tariffs (after)")
        ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(
            row=row,
            column=2,
            value=(
                "Delivery: EPMC allocation (revenue target reflects HP subclass cost-of-service). "
                "Supply: per-customer allocation (each customer bears an equal share of supply revenue). "
                "Gas, oil, and propane tariffs unchanged."
            ),
        )
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        row += 1

        _header_fill(ws, row, 3)
        for c, hdr in enumerate(["Tariff", "Fixed charge", "Volumetric rate"], 1):
            ws.cell(row=row, column=c, value=hdr)
        row += 1

        hp_tariff_rows: list[tuple[str, str, str]] = [
            (
                "Electricity — customer charge",
                f"${tt['elec_customer_charge']:.2f} /mo",
                "—",
            ),
            (
                "Electricity — RE Growth + LIHEAP",
                f"${tt['elec_other_fixed_charges']:.2f} /mo",
                "—",
            ),
            (
                "Electricity — HP delivery (EPMC)",
                "—",
                f"{tt['hp_flat_delivery_cents']:.2f} ¢/kWh",
            ),
            (
                "Electricity — HP supply (per-customer)",
                "—",
                f"{tt['hp_flat_supply_cents']:.2f} ¢/kWh",
            ),
        ]
        for tariff, fixed, vol in hp_tariff_rows:
            ws.cell(row=row, column=1, value=tariff)
            ws.cell(row=row, column=2, value=fixed)
            ws.cell(row=row, column=3, value=vol)
            row += 1
    else:
        row += 1
        ws.cell(row=row, column=1, value="After tariffs")
        ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(
            row=row,
            column=2,
            value="Same default tariffs as above (HP upgrade keeps current rates).",
        )
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        row += 1

    # --- Data sources -------------------------------------------------------
    row += 1
    ds_rows: list[tuple[str, str]] = [
        ("Data sources", ""),
        ("Before bills", f"{scen['before_desc']}\n{scen['before_path']}"),
        ("After bills", f"{scen['after_desc']}\n{scen['after_path']}"),
        (
            "Analysis notebook",
            _reports2_permalink("reports/ri_hp_rates/notebooks/analysis.qmd"),
        ),
    ]
    for label, value in ds_rows:
        ws.cell(row=row, column=1, value=label)
        if label in bold_labels:
            ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2, value=value)
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        row += 1

    # --- per_building columns -----------------------------------------------
    row += 1
    col_rows: list[tuple[str, str]] = [
        ("per_building columns", ""),
        ("bldg_id", "ResStock building identifier"),
        ("weight", "CAIRO sample weight (number of real households this building represents)"),
        (
            "annual_kwh_before",
            "Annual grid-consumed electricity (kWh), upgrade 0 (current HVAC). "
            "Derived from delivery bill: (bill_delivery - annual_fixed_per_customer) / vol_rate. "
            "Same derivation as RIE 1-5 workbook.",
        ),
        (
            "annual_kwh_after",
            "Annual grid-consumed electricity (kWh), upgrade 2 (heat pump). "
            "Derived from run 3+4 delivery bills (default rate); "
            "same physical consumption regardless of which tariff is applied.",
        ),
        ("elec_bill_before", "Annual electric bill before HP, undiscounted"),
        (
            "elec_bill_lmi_before",
            "Annual electric bill before HP, with LMI discount applied (32% of eligible households receive discount)",
        ),
        ("gas_bill_before", "Annual gas bill before HP, undiscounted (same as LMI; gas has no LMI discount)"),
        (
            "gas_bill_lmi_before",
            "Annual gas bill before HP, with LMI discount applied (32% of eligible households receive discount)",
        ),
        ("oil_bill_before", "Annual heating oil bill before HP (no LMI discount applies)"),
        ("propane_bill_before", "Annual propane bill before HP (no LMI discount applies)"),
        ("elec_bill_after", "Annual electric bill after HP, undiscounted"),
        ("elec_bill_lmi_after", "Annual electric bill after HP, with LMI discount applied"),
        ("gas_bill_after", "Annual gas bill after HP, undiscounted"),
        ("gas_bill_lmi_after", "Annual gas bill after HP, with LMI discount applied"),
        ("oil_bill_after", "Annual heating oil bill after HP"),
        ("propane_bill_after", "Annual propane bill after HP"),
        ("elec_lmi_discount_before", "Formula: elec_bill_before - elec_bill_lmi_before (discount amount)"),
        ("elec_lmi_discount_after", "Formula: elec_bill_after - elec_bill_lmi_after (discount amount)"),
        (
            "energy_bill_lmi_before",
            "Formula: sum of LMI-adjusted fuel bills before HP (elec_lmi + gas_lmi + oil + propane)",
        ),
        ("energy_bill_lmi_after", "Formula: sum of LMI-adjusted fuel bills after HP"),
        ("delta", "Formula: energy_bill_lmi_after - energy_bill_lmi_before (negative = savings)"),
        ("saves", "Formula: 1 if delta < 0, else 0"),
        ("w_saves", "Formula: weight * saves (weighted savings indicator)"),
    ]
    for label, value in col_rows:
        ws.cell(row=row, column=1, value=label)
        if label in bold_labels:
            ws.cell(row=row, column=1).font = Font(bold=True)
        ws.cell(row=row, column=2, value=value)
        ws.cell(row=row, column=2).alignment = Alignment(wrap_text=True)
        row += 1

    _autosize(ws, {"A": 44, "B": 40, "C": 36})
    ws.sheet_view.showGridLines = False


def _write_per_building(wb: Workbook, gas: pl.DataFrame) -> int:
    """Write per-building bills sheet. Returns the last data row number."""
    ws = wb.create_sheet("per_building")

    headers = [
        "bldg_id",  # A
        "weight",  # B
        "annual_kwh_before",  # C  data (upgrade 0)
        "annual_kwh_after",  # D  data (upgrade 2)
        "elec_bill_before",  # E
        "elec_bill_lmi_before",  # F
        "gas_bill_before",  # G
        "gas_bill_lmi_before",  # H
        "oil_bill_before",  # I
        "propane_bill_before",  # J
        "elec_bill_after",  # K
        "elec_bill_lmi_after",  # L
        "gas_bill_after",  # M
        "gas_bill_lmi_after",  # N
        "oil_bill_after",  # O
        "propane_bill_after",  # P
        "elec_lmi_discount_before",  # Q  formula
        "elec_lmi_discount_after",  # R  formula
        "energy_bill_lmi_before",  # S  formula
        "energy_bill_lmi_after",  # T  formula
        "delta",  # U  formula
        "saves",  # V  formula
        "w_saves",  # W  formula
    ]
    ws.append(headers)
    _header_fill(ws, 1, len(headers))
    ws.freeze_panes = "A2"

    data_cols = [
        "bldg_id",
        "weight",
        "annual_kwh_before",
        "annual_kwh_after",
        "elec_total_bill_before",
        "elec_total_bill_lmi_32_before",
        "gas_total_bill_before",
        "gas_total_bill_lmi_32_before",
        "oil_total_bill_before",
        "propane_total_bill_before",
        "elec_total_bill_after",
        "elec_total_bill_lmi_32_after",
        "gas_total_bill_after",
        "gas_total_bill_lmi_32_after",
        "oil_total_bill_after",
        "propane_total_bill_after",
    ]

    rows = list(gas.select(data_cols).iter_rows())
    for i, row in enumerate(rows, start=2):
        for ci, val in enumerate(row, start=1):
            ws.cell(row=i, column=ci, value=float(val) if ci > 1 else val)
        # Q: elec LMI discount before = E - F
        ws.cell(row=i, column=17, value=f"=E{i}-F{i}")
        # R: elec LMI discount after = K - L
        ws.cell(row=i, column=18, value=f"=K{i}-L{i}")
        # S: energy_bill_lmi_before = F + H + I + J
        ws.cell(row=i, column=19, value=f"=F{i}+H{i}+I{i}+J{i}")
        # T: energy_bill_lmi_after = L + N + O + P
        ws.cell(row=i, column=20, value=f"=L{i}+N{i}+O{i}+P{i}")
        # U: delta = T - S
        ws.cell(row=i, column=21, value=f"=T{i}-S{i}")
        # V: saves = IF(U < 0, 1, 0)
        ws.cell(row=i, column=22, value=f"=IF(U{i}<0,1,0)")
        # W: w_saves = weight * saves
        ws.cell(row=i, column=23, value=f"=B{i}*V{i}")

    last_row = 1 + len(rows)

    for r in range(2, last_row + 1):
        for col in "CD":
            ws[f"{col}{r}"].number_format = "#,##0"
        for col in "EFGHIJKLMNOPQRSTU":
            ws[f"{col}{r}"].number_format = '"$"#,##0.00'

    _autosize(
        ws,
        {
            "A": 10,
            "B": 10,
            "C": 18,
            "D": 18,
            "E": 16,
            "F": 18,
            "G": 16,
            "H": 18,
            "I": 14,
            "J": 16,
            "K": 16,
            "L": 18,
            "M": 16,
            "N": 18,
            "O": 14,
            "P": 16,
            "Q": 22,
            "R": 22,
            "S": 22,
            "T": 22,
            "U": 14,
            "V": 8,
            "W": 12,
        },
    )
    return last_row


def _write_result(wb: Workbook, last_row: int, scenario_id: str) -> None:
    """Summary sheet deriving the headline percentage with formulas."""
    ws = wb.create_sheet("result")
    scen = SCENARIOS[scenario_id]

    ws["A1"] = f"RIE {scenario_id} — Result"
    ws["A1"].font = Font(bold=True, size=14)
    ws.merge_cells("A1:C1")

    hdr_row = 3
    for ci, h in enumerate(["", "Value", "Formula / Notes"], start=1):
        ws.cell(row=hdr_row, column=ci, value=h)
    _header_fill(ws, hdr_row, 3)

    # Row 4: total gas-heated customers (weighted)
    ws.cell(row=4, column=1, value="Gas-heated customers (weighted)")
    ws.cell(row=4, column=2, value=f"=SUM(per_building!B2:B{last_row})")
    ws.cell(row=4, column=3, value="SUM of weights (all rows are gas-heated)")

    # Row 5: gas-heated customers that save
    ws.cell(row=5, column=1, value="Gas-heated customers that save")
    ws.cell(row=5, column=2, value=f"=SUM(per_building!W2:W{last_row})")
    ws.cell(row=5, column=3, value="SUM of weighted saves indicator")

    # Row 6: pct save
    ws.cell(row=6, column=1, value="Percentage that save")
    ws.cell(row=6, column=2, value="=B5/B4")
    ws.cell(row=6, column=3, value="weighted_savers / total_weighted")
    ws.cell(row=6, column=2).number_format = "0.0%"

    # Row 7: pct lose
    ws.cell(row=7, column=1, value="Percentage that lose")
    ws.cell(row=7, column=2, value="=1-B6")
    ws.cell(row=7, column=3, value="1 - pct_save")
    ws.cell(row=7, column=2).number_format = "0.0%"

    ws.cell(row=9, column=1, value="Headline figure")
    ws.cell(row=9, column=1).font = Font(bold=True)
    ws.cell(row=9, column=2, value=scen["headline"])

    for r in (4, 5):
        ws[f"B{r}"].number_format = "#,##0.00"

    # Bold the headline row
    if scenario_id == "1-8":
        ws.cell(row=7, column=1).font = Font(bold=True)
        ws.cell(row=7, column=2).font = Font(bold=True)
    else:
        ws.cell(row=6, column=1).font = Font(bold=True)
        ws.cell(row=6, column=2).font = Font(bold=True)

    _autosize(ws, {"A": 32, "B": 20, "C": 40})
    ws.sheet_view.showGridLines = False


# ---------------------------------------------------------------------------
# Validation.
# ---------------------------------------------------------------------------
def _validate_kwh_consistency(gas_18: pl.DataFrame, gas_19: pl.DataFrame) -> None:
    """Assert kWh values are identical between 1-8 and 1-9 DataFrames."""
    merged = gas_18.select("bldg_id", "annual_kwh_before", "annual_kwh_after").join(
        gas_19.select(
            "bldg_id",
            pl.col("annual_kwh_before").alias("kwh_before_19"),
            pl.col("annual_kwh_after").alias("kwh_after_19"),
        ),
        on="bldg_id",
        how="inner",
    )
    assert merged.height == gas_18.height == gas_19.height, (
        f"Building count mismatch: 1-8={gas_18.height}, 1-9={gas_19.height}, joined={merged.height}"
    )
    before_diff = float((merged["annual_kwh_before"] - merged["kwh_before_19"]).abs().max())  # type: ignore[arg-type]
    after_diff = float((merged["annual_kwh_after"] - merged["kwh_after_19"]).abs().max())  # type: ignore[arg-type]
    assert before_diff < 0.01, f"kWh_before differs: max diff = {before_diff}"
    assert after_diff < 0.01, f"kWh_after differs: max diff = {after_diff}"
    print(
        f"  kWh consistency: {merged.height} buildings, "
        f"before max_diff={before_diff:.2e}, after max_diff={after_diff:.2e}",
        flush=True,
    )


# ---------------------------------------------------------------------------
# Orchestration.
# ---------------------------------------------------------------------------
def build_workbook(
    output_path: Path,
    scenario_id: str,
    gas: pl.DataFrame,
    inputs: dict,
) -> Path:
    """Build one workbook for the given scenario."""
    total_w = float(gas["weight"].sum())
    save_w = float(gas.filter(pl.col("delta") < 0)["weight"].sum())
    pct_save = save_w / total_w

    print(f"\n  RIE {scenario_id}:", flush=True)
    print(f"    gas-heated buildings: {gas.height:,}", flush=True)
    print(f"    weighted customers: {total_w:,.1f}", flush=True)
    print(f"    pct save: {pct_save:.4f} ({pct_save * 100:.1f}%)", flush=True)
    print(f"    pct lose: {1 - pct_save:.4f} ({(1 - pct_save) * 100:.1f}%)", flush=True)

    if scenario_id == "1-8":
        expected_lose = 0.79
        actual_lose = 1 - pct_save
        assert abs(actual_lose - expected_lose) < 0.02, (
            f"RIE 1-8: expected ~{expected_lose:.0%} lose, got {actual_lose:.1%}"
        )
    else:
        expected_save = 0.87
        assert abs(pct_save - expected_save) < 0.02, f"RIE 1-9: expected ~{expected_save:.0%} save, got {pct_save:.1%}"

    wb = Workbook()
    default_ws = wb.active
    if default_ws is not None:
        wb.remove(default_ws)

    _write_assumptions(wb, scenario_id, inputs)
    last_row = _write_per_building(wb, gas)
    _write_result(wb, last_row, scenario_id)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    print(
        f"    Wrote {output_path} ({output_path.stat().st_size / 1024:.1f} KB)",
        flush=True,
    )
    return output_path


# ---------------------------------------------------------------------------
# Google Sheets upload.
# ---------------------------------------------------------------------------
_TAB_FORMATTING: dict[str, dict] = {
    "assumptions": {
        "wrap_columns": ["B:B"],
        "column_widths_px": {"A": 180, "B": 640},
        "freeze_rows": 0,
        "bold_header": False,
    },
    "per_building": {
        "column_number_formats": {
            "C": "#,##0",
            "D": "#,##0",
            "E": '"$"#,##0.00',
            "F": '"$"#,##0.00',
            "G": '"$"#,##0.00',
            "H": '"$"#,##0.00',
            "I": '"$"#,##0.00',
            "J": '"$"#,##0.00',
            "K": '"$"#,##0.00',
            "L": '"$"#,##0.00',
            "M": '"$"#,##0.00',
            "N": '"$"#,##0.00',
            "O": '"$"#,##0.00',
            "P": '"$"#,##0.00',
            "Q": '"$"#,##0.00',
            "R": '"$"#,##0.00',
            "S": '"$"#,##0.00',
            "T": '"$"#,##0.00',
            "U": '"$"#,##0.00',
        },
        "auto_resize_columns": ["A:W"],
        "freeze_rows": 1,
        "bold_header": True,
    },
    "result": {
        "auto_resize_columns": ["A:C"],
        "freeze_rows": 0,
        "bold_header": True,
    },
}


def upload_to_sheet(xlsx_path: Path, spreadsheet_id: str) -> None:
    from lib.data.gsheets import apply_sheet_formatting, xlsx_to_gsheet

    print(f"  Uploading {xlsx_path} -> {spreadsheet_id} ...", flush=True)
    spreadsheet = xlsx_to_gsheet(xlsx_path, spreadsheet_id, delete_other_tabs=True)
    for ws in spreadsheet.worksheets():
        spec = _TAB_FORMATTING.get(ws.title)
        if spec:
            apply_sheet_formatting(ws, **spec)
    print(
        f"  Done. https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit",
        flush=True,
    )


# ---------------------------------------------------------------------------
# CLI.
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload to Google Sheets after building.",
    )
    args = parser.parse_args(argv)

    print("Loading tariff inputs ...", flush=True)
    inputs = _load_inputs()
    print(
        f"  vol_rate = {inputs['default_vol_usd_per_kwh']:.5f}, "
        f"annual_fixed = ${inputs['annual_fixed_per_customer']:,.2f}",
        flush=True,
    )

    print("Loading master bills (run 1+2) ...", flush=True)
    before = _load_annual_bills(PATH_BILLS_12)
    print(f"  {before.height:,} annual rows for {UTILITY}", flush=True)

    print("Loading master bills (run 3+4) ...", flush=True)
    after_default = _load_annual_bills(PATH_BILLS_34)
    print(f"  {after_default.height:,} rows", flush=True)

    print("Loading master bills (run 19+20) ...", flush=True)
    after_hprate = _load_annual_bills(PATH_BILLS_1920)
    print(f"  {after_hprate.height:,} rows", flush=True)

    print("Deriving annual kWh (upgrade 0 from run 1+2, upgrade 2 from run 3+4) ...", flush=True)
    kwh_before = _derive_annual_kwh(before, inputs)
    kwh_after = _derive_annual_kwh(after_default, inputs)
    print(
        f"  upgrade 0 median: {kwh_before['annual_kwh'].median():,.0f} kWh, "
        f"upgrade 2 median: {kwh_after['annual_kwh'].median():,.0f} kWh",
        flush=True,
    )

    gas_default = _join_and_filter(before, after_default, kwh_before, kwh_after)
    gas_hprate = _join_and_filter(before, after_hprate, kwh_before, kwh_after)

    _validate_kwh_consistency(gas_default, gas_hprate)

    out_1_8 = build_workbook(Path("cache/rie_1_8.xlsx"), "1-8", gas_default, inputs)
    out_1_9 = build_workbook(Path("cache/rie_1_9.xlsx"), "1-9", gas_hprate, inputs)

    if args.upload:
        print("\nUploading ...", flush=True)
        upload_to_sheet(out_1_8, SPREADSHEET_1_8)
        upload_to_sheet(out_1_9, SPREADSHEET_1_9)

    return 0


def _join_and_filter(
    before: pl.DataFrame,
    after: pl.DataFrame,
    kwh_before: pl.DataFrame,
    kwh_after: pl.DataFrame,
) -> pl.DataFrame:
    """Join before/after on bldg_id, filter to gas-heated, add kWh + LMI totals + delta."""
    before_r = before.rename({c: f"{c}_before" for c in BILL_COLS}).select(
        "bldg_id",
        "weight",
        "heats_with_natgas",
        *[f"{c}_before" for c in BILL_COLS],
    )
    after_r = after.select(
        "bldg_id",
        *[pl.col(c).alias(f"{c}_after") for c in BILL_COLS],
    )
    joined = before_r.join(after_r, on="bldg_id", how="inner")
    joined = joined.join(
        kwh_before.select("bldg_id", pl.col("annual_kwh").alias("annual_kwh_before")),
        on="bldg_id",
        how="left",
    )
    joined = joined.join(
        kwh_after.select("bldg_id", pl.col("annual_kwh").alias("annual_kwh_after")),
        on="bldg_id",
        how="left",
    )
    gas = joined.filter(pl.col("heats_with_natgas"))

    return gas.with_columns(
        pl.sum_horizontal([f"{c}_before" for c in LMI_BILL_COLS]).alias("energy_bill_lmi_before"),
        pl.sum_horizontal([f"{c}_after" for c in LMI_BILL_COLS]).alias("energy_bill_lmi_after"),
    ).with_columns(
        (pl.col("energy_bill_lmi_after") - pl.col("energy_bill_lmi_before")).alias("delta"),
    )


if __name__ == "__main__":
    sys.exit(main())
