"""Build the supporting workbook for the revenue-neutrality claim (page 56).

Pre-Filed Direct Testimony of Juan-Pablo Velez, Page 56, Lines 8-14:

    Q. Is the heat pump rate revenue-neutral?
    A. Yes, at the residential class level.

This script produces an ``.xlsx`` with live formulas that prove the claim.
The proof has three parts:

1. The total residential delivery RR is partitioned into HP and non-HP
   subclass RRs such that ``HP_RR + nonHP_RR = Total_RR``.
2. Each subclass's volumetric rate is calibrated to collect exactly its
   RR minus unchanged fixed charges.
3. Since each subclass rate collects exactly its subclass RR, and the
   subclass RRs sum to the total, total residential revenue is unchanged.

Run from the report directory::

    uv run python -m testimony_response.build_RIE_1_12_workbook \\
        --output cache/revenue_neutrality.xlsx
    uv run python -m testimony_response.build_RIE_1_12_workbook --upload

See ``cost_of_service_by_subclass.qmd`` for the published-side analysis
logic that this workbook reproduces with formulas.
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
from openpyxl.workbook.defined_name import DefinedName

from lib.rdp import fetch_rdp_file, parse_urdb_json

# ---------------------------------------------------------------------------
# Cross-sheet A1 references (Google Sheets compatible; see build_RIE_1_11_DIV_7_workbook).
# ---------------------------------------------------------------------------
REF_TOTAL_RR = "inputs_revenue_requirement!$B$2"
REF_N_CUSTOMERS = "inputs_revenue_requirement!$B$3"
REF_TY_KWH = "inputs_revenue_requirement!$B$4"
REF_CUSTOMER_CHARGE = "inputs_revenue_requirement!$B$5"
REF_CORE_DELIVERY = "inputs_revenue_requirement!$B$6"
REF_ANNUAL_FIXED = "inputs_revenue_requirement!$B$7"

REF_DEFAULT_VOL = "inputs_tariffs!$B$2"
REF_HP_VOL = "inputs_tariffs!$B$3"
REF_NONHP_VOL = "inputs_tariffs!$B$4"

# ---------------------------------------------------------------------------
# Constants aligned with cost_of_service_by_subclass.qmd & build_RIE_1_11_DIV_7_workbook.
# ---------------------------------------------------------------------------
UTILITY = "rie"
BATCH = "ri_20260331_r1-20_rate_case_test_year"
STATE_LOWER = "ri"
S3_BASE = "s3://data.sb/switchbox/cairo/outputs/hp_rates"
PATH_MASTER_BAT_12 = f"{S3_BASE}/{STATE_LOWER}/all_utilities/{BATCH}/run_1+2/cross_subsidization_BAT_values/"
RDP_REF = "e9e5088"
RDP_REV_YAML_PATH = "rate_design/hp_rates/ri/config/rev_requirement/rie_rate_case_test_year.yaml"
RDP_HPVS_YAML_PATH = "rate_design/hp_rates/ri/config/rev_requirement/rie_hp_vs_nonhp_rate_case_test_year.yaml"
RDP_TARIFF_DIR = "rate_design/hp_rates/ri/config/tariffs/electric"
RDP_GITHUB_BASE = "https://github.com/switchbox-data/rate-design-platform/blob"
REPORTS2_GITHUB_BASE = "https://github.com/switchbox-data/reports2/blob"

# Default upload target: RIE 1-12 discovery response Sheet (revenue neutrality).
DEFAULT_SPREADSHEET_ID = "1JlSDvgS6H70OCIJ4Q8LRQGNFS6AJcaeh7ccNxaab08A"

# Only the two delivery allocation methods reported in the testimony:
# EPMC = cost-of-service allocation (what each subclass should pay)
# Passthrough = current revenue (what each subclass does pay today)
DELIVERY_METHODS_REPORTED = ("epmc", "passthrough")
METHOD_LABELS: dict[str, str] = {
    "epmc": "EPMC (cost of service)",
    "passthrough": "Passthrough (current revenue)",
}


# ---------------------------------------------------------------------------
# Permalink helpers (identical to build_RIE_1_11_DIV_7_workbook).
# ---------------------------------------------------------------------------
def _rdp_permalink(rel_path: str) -> str:
    return f"{RDP_GITHUB_BASE}/{RDP_REF}/{rel_path}"


def _reports2_head_sha() -> str:
    if not hasattr(_reports2_head_sha, "_cached"):
        repo_root = Path(__file__).resolve().parents[3]
        sha = subprocess.check_output(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        _reports2_head_sha._cached = sha  # type: ignore[attr-defined]
    return _reports2_head_sha._cached  # type: ignore[attr-defined]


def _reports2_permalink(rel_path: str, *, line_range: tuple[int, int] | None = None) -> str:
    url = f"{REPORTS2_GITHUB_BASE}/{_reports2_head_sha()}/{rel_path}"
    if line_range is not None:
        start, end = line_range
        url += f"#L{start}-L{end}"
    return url


# ---------------------------------------------------------------------------
# Data loading.
# ---------------------------------------------------------------------------
def load_master_bat() -> pl.DataFrame:
    """Load per-building BAT data, adding has_hp flag."""
    df = (
        pl.scan_parquet(PATH_MASTER_BAT_12, hive_partitioning=True)
        .filter(pl.col("sb.electric_utility") == UTILITY)
        .select(
            "bldg_id",
            "weight",
            "postprocess_group.has_hp",
            "postprocess_group.heating_type_v2",
            "annual_bill_delivery",
        )
        .collect()
    )
    assert isinstance(df, pl.DataFrame)
    return df


def load_inputs() -> dict:
    """Pull scalar inputs from both YAMLs and three calibrated tariff JSONs."""
    raw_rev = fetch_rdp_file(RDP_REV_YAML_PATH, RDP_REF)
    rev = yaml.safe_load(raw_rev)

    raw_hpvs = fetch_rdp_file(RDP_HPVS_YAML_PATH, RDP_REF)
    hpvs = yaml.safe_load(raw_hpvs)

    total_rr = float(rev["total_delivery_revenue_requirement"])
    n_customers = float(rev["test_year_customer_count"])
    ty_kwh = float(rev["test_year_residential_kwh"])

    drr = rev["delivery_revenue_requirement"]
    customer_charge_total = float(drr["customer_charge"]["total_budget"])
    core_delivery_total = float(drr["core_delivery_rate"]["total_budget"])

    def vol_rate(rel_filename: str) -> float:
        path = f"{RDP_TARIFF_DIR}/{rel_filename}"
        doc = parse_urdb_json(fetch_rdp_file(path, RDP_REF))
        return float(doc["items"][0]["energyratestructure"][0][0]["rate"])

    default_vol = vol_rate("rie_default_calibrated.json")
    hp_vol = vol_rate("rie_hp_flat_calibrated.json")
    nonhp_vol = vol_rate("rie_nonhp_default_calibrated.json")

    annual_fixed = (total_rr - default_vol * ty_kwh) / n_customers

    return {
        "total_delivery_revenue_requirement": total_rr,
        "test_year_customer_count": n_customers,
        "test_year_residential_kwh": ty_kwh,
        "customer_charge_total": customer_charge_total,
        "core_delivery_rate_total": core_delivery_total,
        "annual_fixed_per_customer": annual_fixed,
        "default_vol_usd_per_kwh": default_vol,
        "hp_flat_vol_usd_per_kwh": hp_vol,
        "nonhp_default_vol_usd_per_kwh": nonhp_vol,
        "subclass_revenue_requirements": hpvs["subclass_revenue_requirements"],
    }


# ---------------------------------------------------------------------------
# Shared formatting helpers (identical to build_RIE_1_11_DIV_7_workbook).
# ---------------------------------------------------------------------------
def _bold(ws, cell: str) -> None:  # type: ignore[no-untyped-def]
    ws[cell].font = Font(bold=True)


def _header_fill(ws, row: int, n_cols: int) -> None:  # type: ignore[no-untyped-def]
    fill = PatternFill("solid", fgColor="E8E8E8")
    for c in range(1, n_cols + 1):
        ws.cell(row=row, column=c).font = Font(bold=True)
        ws.cell(row=row, column=c).fill = fill


def _autosize(ws, widths: dict[str, int]) -> None:  # type: ignore[no-untyped-def]
    for col, w in widths.items():
        ws.column_dimensions[col].width = w


# ---------------------------------------------------------------------------
# Sheet writers.
# ---------------------------------------------------------------------------
def _write_readme(wb: Workbook, inputs: dict) -> None:
    ws = wb.create_sheet("README", 0)
    rows: list[list] = [
        [
            "Revenue-neutrality supporting workbook (RIE residential HP rate, Docket 2545GE)",
            "",
            "",
        ],
        ["", "", ""],
        ["Item", "Source", "Notes"],
        [
            "Pre-Filed Direct Testimony",
            "JPV, Page 56, Lines 8-14",
            'Q. "Is the heat pump rate revenue-neutral?" A. "Yes, at the residential class level."',
        ],
        [
            "Revenue-requirement YAML (rate case)",
            _rdp_permalink(RDP_REV_YAML_PATH),
            "Total delivery RR, customer count, kWh, customer charge, "
            "core delivery rate — sourced from PRB-1-ELEC exhibit.",
        ],
        [
            "Subclass revenue-requirement YAML (HP vs non-HP)",
            _rdp_permalink(RDP_HPVS_YAML_PATH),
            "Per-subclass RR splits by allocation method (EPMC, passthrough, etc.). Computed from BAT decomposition.",
        ],
        [
            "Calibrated default tariff JSON",
            _rdp_permalink(f"{RDP_TARIFF_DIR}/rie_default_calibrated.json"),
            "Status-quo uniform default delivery $/kWh.",
        ],
        [
            "Calibrated HP flat tariff JSON",
            _rdp_permalink(f"{RDP_TARIFF_DIR}/rie_hp_flat_calibrated.json"),
            "Proposed HP flat delivery $/kWh.",
        ],
        [
            "Calibrated adjusted-default tariff JSON",
            _rdp_permalink(f"{RDP_TARIFF_DIR}/rie_nonhp_default_calibrated.json"),
            "Revenue-neutral adjusted non-HP delivery $/kWh.",
        ],
        [
            "Per-building BAT outputs",
            f"{S3_BASE}/{STATE_LOWER}/all_utilities/{BATCH}/run_1+2/cross_subsidization_BAT_values/",
            "CAIRO batch outputs (one row per RIE residential building).",
        ],
        [
            "Cost-of-service notebook",
            _reports2_permalink("reports/ri_hp_rates/notebooks/cost_of_service_by_subclass.qmd"),
            "Derives HP rate, adjusted default rate, and revenue "
            "neutrality in polars. This workbook reproduces that "
            "logic as live formulas.",
        ],
        ["", "", ""],
        ["Sheet", "What it contains", ""],
        [
            "inputs_revenue_requirement",
            "Test-year scalars from the rate-case revenue-requirement YAML.",
            "",
        ],
        [
            "inputs_tariffs",
            "Calibrated volumetric delivery rates: default, HP flat, adjusted non-HP default.",
            "",
        ],
        [
            "inputs_subclass_rr",
            "HP vs non-HP delivery RR by the two allocation methods "
            "reported in testimony (EPMC and passthrough), "
            "with formula sum-checks proving HP + non-HP = Total.",
            "",
        ],
        [
            "bat_per_building",
            (
                "One row per building: weight, has_hp, delivery bill, annual_kwh back-derived from delivery bill "
                "(= (annual_bill_delivery - annual_fixed_per_customer) / vol_rate), annual_bill_delivery_check formula "
                "(= annual_kwh * vol_rate + annual_fixed_per_customer), weighted products. "
                "weight is uniform: test_year_customer_count / n_buildings (each building represents the same number of customers)."
            ),
            "",
        ],
        [
            "hp_nonhp_aggregates",
            "HP/non-HP/total aggregate customers, kWh, revenue, "
            "fixed charges, volumetric revenue, implied vol rate — "
            "all via SUMIFS over bat_per_building.",
            "",
        ],
        [
            "revenue_neutrality_proof",
            "The proof: revenue under current uniform rate vs. proposed split rates. Total is unchanged.",
            "",
        ],
        [
            "validation",
            "Formula-level checks: weights, revenue, kWh, implied rates vs. calibrated rates.",
            "",
        ],
        ["", "", ""],
        ["Non-goal", "", ""],
        [
            "Per-building BAT / EPMC reconstruction",
            (
                "Out of scope. Per-building cost-of-service is produced "
                "upstream by CAIRO from ResStock hourly loads x marginal "
                "cost shapes. The revenue neutrality proof operates on "
                "the aggregate subclass RR splits, not per-building COS."
            ),
            "",
        ],
    ]
    for r in rows:
        ws.append(r)
    ws["A1"].font = Font(bold=True, size=14)
    for header_row in (3, 12):
        _header_fill(ws, header_row, 3)
    _header_fill(ws, 22, 3)
    _autosize(ws, {"A": 42, "B": 70, "C": 80})
    ws.sheet_view.showGridLines = False


def _write_inputs_revenue_requirement(wb: Workbook, inputs: dict) -> None:
    ws = wb.create_sheet("inputs_revenue_requirement")
    yaml_ref = _rdp_permalink(RDP_REV_YAML_PATH)
    rows = [
        ["key", "value", "source", "notes"],
        [
            "total_delivery_revenue_requirement",
            inputs["total_delivery_revenue_requirement"],
            yaml_ref,
            "PRB-1-ELEC exhibit, p. 14, lines 8-9, columns f & m.",
        ],
        [
            "test_year_customer_count",
            inputs["test_year_customer_count"],
            yaml_ref,
            "5,032,174 bills / 12 = 419,347.83 customers.",
        ],
        [
            "test_year_residential_kwh",
            inputs["test_year_residential_kwh"],
            yaml_ref,
            "PRB-1-ELEC exhibit, p. 14, lines 8-9, column k.",
        ],
        [
            "customer_charge_total",
            inputs["customer_charge_total"],
            yaml_ref,
            "Portion of RR recovered via fixed customer charges.",
        ],
        [
            "core_delivery_rate_total",
            inputs["core_delivery_rate_total"],
            yaml_ref,
            "Portion of RR recovered via core delivery volumetric rate.",
        ],
        [
            "annual_fixed_per_customer",
            f"=({REF_TOTAL_RR} - {REF_DEFAULT_VOL} * {REF_TY_KWH}) / {REF_N_CUSTOMERS}",
            "Derived in this workbook",
            "Annual non-volumetric delivery charges per customer "
            "(customer charge + fixed top-ups). "
            "Validated: annual_kwh * vol_rate + this value ≈ annual_bill_delivery.",
        ],
    ]
    for r in rows:
        ws.append(r)
    _header_fill(ws, 1, 4)
    _autosize(ws, {"A": 42, "B": 22, "C": 70, "D": 70})
    for row_idx, name in [
        (2, "total_delivery_revenue_requirement"),
        (3, "test_year_customer_count"),
        (4, "test_year_residential_kwh"),
        (5, "customer_charge_total"),
        (6, "core_delivery_rate_total"),
        (7, "annual_fixed_per_customer"),
    ]:
        wb.defined_names[name] = DefinedName(
            name=name,
            attr_text=f"inputs_revenue_requirement!$B${row_idx}",
        )
    ws.sheet_view.showGridLines = False


def _write_inputs_tariffs(wb: Workbook, inputs: dict) -> None:
    ws = wb.create_sheet("inputs_tariffs")
    rows = [
        ["key", "value", "source", "notes"],
        [
            "default_vol_usd_per_kwh",
            inputs["default_vol_usd_per_kwh"],
            _rdp_permalink(f"{RDP_TARIFF_DIR}/rie_default_calibrated.json"),
            "Status-quo uniform default delivery $/kWh.",
        ],
        [
            "hp_flat_vol_usd_per_kwh",
            inputs["hp_flat_vol_usd_per_kwh"],
            _rdp_permalink(f"{RDP_TARIFF_DIR}/rie_hp_flat_calibrated.json"),
            "Proposed HP flat delivery $/kWh.",
        ],
        [
            "nonhp_default_vol_usd_per_kwh",
            inputs["nonhp_default_vol_usd_per_kwh"],
            _rdp_permalink(f"{RDP_TARIFF_DIR}/rie_nonhp_default_calibrated.json"),
            "Adjusted non-HP default delivery $/kWh (revenue-neutral).",
        ],
    ]
    for r in rows:
        ws.append(r)
    _header_fill(ws, 1, 4)
    _autosize(ws, {"A": 32, "B": 18, "C": 80, "D": 60})
    for row_idx, name in [
        (2, "default_vol_usd_per_kwh"),
        (3, "hp_flat_vol_usd_per_kwh"),
        (4, "nonhp_default_vol_usd_per_kwh"),
    ]:
        wb.defined_names[name] = DefinedName(name=name, attr_text=f"inputs_tariffs!$B${row_idx}")
    ws.sheet_view.showGridLines = False


def _write_inputs_subclass_rr(wb: Workbook, inputs: dict) -> None:
    """Delivery-only subclass RR splits for the two methods in the testimony."""
    ws = wb.create_sheet("inputs_subclass_rr")
    subs = inputs["subclass_revenue_requirements"]
    yaml_ref = _rdp_permalink(RDP_HPVS_YAML_PATH)
    total_rr = inputs["total_delivery_revenue_requirement"]

    headers = [
        "method",
        "hp_rr",
        "nonhp_rr",
        "sum_formula",
        "total_rr",
        "delta",
    ]
    ws.append(headers)
    _header_fill(ws, 1, len(headers))

    row_idx = 2
    for method in DELIVERY_METHODS_REPORTED:
        vals = subs["delivery"][method]
        ws.cell(row=row_idx, column=1, value=METHOD_LABELS.get(method, method))
        ws.cell(row=row_idx, column=2, value=float(vals["hp"]))
        ws.cell(row=row_idx, column=3, value=float(vals["non-hp"]))
        ws.cell(row=row_idx, column=4, value=f"=B{row_idx}+C{row_idx}")
        ws.cell(row=row_idx, column=5, value=total_rr)
        ws.cell(row=row_idx, column=6, value=f"=D{row_idx}-E{row_idx}")
        row_idx += 1

    for r in range(2, row_idx):
        ws[f"B{r}"].number_format = '"$"#,##0.00'
        ws[f"C{r}"].number_format = '"$"#,##0.00'
        ws[f"D{r}"].number_format = '"$"#,##0.00'
        ws[f"E{r}"].number_format = '"$"#,##0.00'
        ws[f"F{r}"].number_format = '"$"#,##0.00'

    _autosize(
        ws,
        {"A": 30, "B": 20, "C": 20, "D": 20, "E": 20, "F": 14},
    )

    ws.cell(row=row_idx + 1, column=1, value="Source")
    ws.cell(row=row_idx + 1, column=2, value=yaml_ref)

    ws.cell(row=row_idx + 3, column=1, value="Note")
    ws.cell(
        row=row_idx + 3,
        column=2,
        value=(
            "EPMC = equi-proportional marginal cost allocation "
            "(cost of service). Passthrough = current revenue under "
            "today's uniform default rate. The revenue-neutrality "
            "proof uses EPMC for the proposed subclass RRs."
        ),
    )

    # EPMC is the first delivery row (row 2).
    epmc_row = 2
    wb.defined_names["hp_delivery_rr_epmc"] = DefinedName(
        name="hp_delivery_rr_epmc",
        attr_text=f"inputs_subclass_rr!$B${epmc_row}",
    )
    wb.defined_names["nonhp_delivery_rr_epmc"] = DefinedName(
        name="nonhp_delivery_rr_epmc",
        attr_text=f"inputs_subclass_rr!$C${epmc_row}",
    )

    ws.sheet_view.showGridLines = False


REF_HP_EPMC = "inputs_subclass_rr!$B$2"
REF_NONHP_EPMC = "inputs_subclass_rr!$C$2"


def _write_bat_per_building(wb: Workbook, bat: pl.DataFrame) -> int:
    """One row per building with formula columns. Returns last data row."""
    ws = wb.create_sheet("bat_per_building")
    headers = [
        "bldg_id",
        "weight",
        "has_hp",
        "heating_type_v2",
        "annual_bill_delivery",
        "annual_kwh",
        "annual_bill_delivery_check",
        "w_bill",
        "w_kwh",
    ]
    ws.append(headers)
    _header_fill(ws, 1, len(headers))
    ws.freeze_panes = "A2"

    n = bat.height
    rows_data = list(
        bat.select(
            "bldg_id",
            "weight",
            "postprocess_group.has_hp",
            "postprocess_group.heating_type_v2",
            "annual_bill_delivery",
            "annual_kwh",
        ).iter_rows()
    )
    for i, row in enumerate(rows_data, start=2):
        ws.cell(row=i, column=1, value=row[0])
        ws.cell(row=i, column=2, value=float(row[1]))
        ws.cell(row=i, column=3, value=str(row[2]).lower())
        ws.cell(row=i, column=4, value=row[3])
        ws.cell(row=i, column=5, value=float(row[4]))
        ws.cell(row=i, column=6, value=float(row[5]))
        ws.cell(row=i, column=7, value=f"=F{i}*{REF_DEFAULT_VOL}+{REF_ANNUAL_FIXED}")
        ws.cell(row=i, column=8, value=f"=B{i}*E{i}")
        ws.cell(row=i, column=9, value=f"=B{i}*F{i}")

    last_row = 1 + n
    _autosize(
        ws,
        {
            "A": 10,
            "B": 10,
            "C": 10,
            "D": 22,
            "E": 18,
            "F": 14,
            "G": 24,
            "H": 16,
            "I": 16,
        },
    )

    col_to_name = {
        "B": "ws_weight",
        "C": "ws_has_hp",
        "E": "ws_annual_bill",
        "F": "ws_annual_kwh",
        "G": "ws_bill_check",
        "H": "ws_w_bill",
        "I": "ws_w_kwh",
    }
    for col, name in col_to_name.items():
        wb.defined_names[name] = DefinedName(
            name=name,
            attr_text=f"bat_per_building!${col}$2:${col}${last_row}",
        )
    return last_row


def _write_hp_nonhp_aggregates(wb: Workbook, last_bat_row: int) -> None:
    """HP / non-HP / total aggregates via SUMIFS over bat_per_building."""
    ws = wb.create_sheet("hp_nonhp_aggregates")
    headers = [
        "subclass",
        "has_hp_value",
        "n_customers",
        "total_delivery_revenue",
        "total_kwh",
        "annual_fixed_total",
        "volumetric_revenue",
        "implied_vol_rate",
        "calibrated_vol_rate",
        "rate_delta",
    ]
    ws.append(headers)
    _header_fill(ws, 1, len(headers))

    last = last_bat_row
    rng_weight = f"bat_per_building!$B$2:$B${last}"
    rng_has_hp = f"bat_per_building!$C$2:$C${last}"
    rng_w_bill = f"bat_per_building!$H$2:$H${last}"
    rng_w_kwh = f"bat_per_building!$I$2:$I${last}"

    # Row 2: HP
    ws.cell(row=2, column=1, value="Heat pump")
    ws.cell(row=2, column=2, value="true")
    ws.cell(
        row=2,
        column=3,
        value=f'=SUMIFS({rng_weight},{rng_has_hp},"true")',
    )
    ws.cell(
        row=2,
        column=4,
        value=f'=SUMIFS({rng_w_bill},{rng_has_hp},"true")',
    )
    ws.cell(
        row=2,
        column=5,
        value=f'=SUMIFS({rng_w_kwh},{rng_has_hp},"true")',
    )
    ws.cell(row=2, column=6, value=f"=C2*{REF_ANNUAL_FIXED}")
    ws.cell(row=2, column=7, value="=D2-F2")
    ws.cell(row=2, column=8, value="=G2/E2")
    ws.cell(row=2, column=9, value=f"={REF_HP_VOL}")
    ws.cell(row=2, column=10, value="=H2-I2")

    # Row 3: Non-HP
    ws.cell(row=3, column=1, value="Non-heat pump")
    ws.cell(row=3, column=2, value="false")
    ws.cell(
        row=3,
        column=3,
        value=f'=SUMIFS({rng_weight},{rng_has_hp},"false")',
    )
    ws.cell(
        row=3,
        column=4,
        value=f'=SUMIFS({rng_w_bill},{rng_has_hp},"false")',
    )
    ws.cell(
        row=3,
        column=5,
        value=f'=SUMIFS({rng_w_kwh},{rng_has_hp},"false")',
    )
    ws.cell(row=3, column=6, value=f"=C3*{REF_ANNUAL_FIXED}")
    ws.cell(row=3, column=7, value="=D3-F3")
    ws.cell(row=3, column=8, value="=G3/E3")
    ws.cell(row=3, column=9, value=f"={REF_NONHP_VOL}")
    ws.cell(row=3, column=10, value="=H3-I3")

    # Row 4: Total
    ws.cell(row=4, column=1, value="All customers")
    ws.cell(row=4, column=2, value="")
    ws.cell(row=4, column=3, value=f"=SUM({rng_weight})")
    ws.cell(row=4, column=4, value=f"=SUM({rng_w_bill})")
    ws.cell(row=4, column=5, value=f"=SUM({rng_w_kwh})")
    ws.cell(row=4, column=6, value=f"=C4*{REF_ANNUAL_FIXED}")
    ws.cell(row=4, column=7, value="=D4-F4")
    ws.cell(row=4, column=8, value="=G4/E4")
    ws.cell(row=4, column=9, value=f"={REF_DEFAULT_VOL}")
    ws.cell(row=4, column=10, value="=H4-I4")

    for c in ("A", "B"):
        _bold(ws, f"{c}4")

    for r in range(2, 5):
        ws[f"C{r}"].number_format = "#,##0.00"
        ws[f"D{r}"].number_format = '"$"#,##0.00'
        ws[f"E{r}"].number_format = "#,##0"
        ws[f"F{r}"].number_format = '"$"#,##0.00'
        ws[f"G{r}"].number_format = '"$"#,##0.00'
        ws[f"H{r}"].number_format = "0.000000"
        ws[f"I{r}"].number_format = "0.000000"
        ws[f"J{r}"].number_format = "0.000000"

    _autosize(
        ws,
        {
            "A": 18,
            "B": 14,
            "C": 16,
            "D": 22,
            "E": 18,
            "F": 20,
            "G": 22,
            "H": 16,
            "I": 16,
            "J": 14,
        },
    )

    # Named ranges for the proof sheet.
    wb.defined_names["agg_hp_customers"] = DefinedName(
        name="agg_hp_customers",
        attr_text="hp_nonhp_aggregates!$C$2",
    )
    wb.defined_names["agg_nonhp_customers"] = DefinedName(
        name="agg_nonhp_customers",
        attr_text="hp_nonhp_aggregates!$C$3",
    )
    wb.defined_names["agg_hp_kwh"] = DefinedName(
        name="agg_hp_kwh",
        attr_text="hp_nonhp_aggregates!$E$2",
    )
    wb.defined_names["agg_nonhp_kwh"] = DefinedName(
        name="agg_nonhp_kwh",
        attr_text="hp_nonhp_aggregates!$E$3",
    )

    ws.sheet_view.showGridLines = False


# A1 references into hp_nonhp_aggregates used by the proof sheet.
REF_AGG_HP_N = "hp_nonhp_aggregates!$C$2"
REF_AGG_NONHP_N = "hp_nonhp_aggregates!$C$3"
REF_AGG_TOTAL_N = "hp_nonhp_aggregates!$C$4"
REF_AGG_HP_KWH = "hp_nonhp_aggregates!$E$2"
REF_AGG_NONHP_KWH = "hp_nonhp_aggregates!$E$3"
REF_AGG_TOTAL_KWH = "hp_nonhp_aggregates!$E$4"


def _write_revenue_neutrality_proof(wb: Workbook) -> None:
    """The publishable proof: current vs. proposed revenue are equal."""
    ws = wb.create_sheet("revenue_neutrality_proof")

    title = "Revenue-neutrality proof: current uniform rate vs. proposed split rates"
    subtitle = (
        "The proposed heat pump rate reallocates delivery revenue within "
        "the residential class. Total residential delivery revenue is "
        "unchanged. All cells are live formulas referencing input sheets."
    )
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=14)
    ws.merge_cells("A1:D1")
    ws["A2"] = subtitle
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 30

    # --- Section A: Current uniform rate ---
    sec_a_row = 4
    ws.cell(row=sec_a_row, column=1, value="A. Revenue under current uniform rate")
    ws[f"A{sec_a_row}"].font = Font(bold=True, size=12)
    ws.merge_cells(f"A{sec_a_row}:D{sec_a_row}")

    hdr_a = sec_a_row + 1
    for ci, h in enumerate(["Item", "Value", "Formula", ""], start=1):
        ws.cell(row=hdr_a, column=ci, value=h)
    _header_fill(ws, hdr_a, 4)

    r = hdr_a + 1
    items_a = [
        (
            "Total residential customers",
            f"={REF_N_CUSTOMERS}",
            "From rate-case YAML",
        ),
        (
            "Total residential kWh",
            f"={REF_TY_KWH}",
            "From rate-case YAML",
        ),
        (
            "Default volumetric rate ($/kWh)",
            f"={REF_DEFAULT_VOL}",
            "From calibrated default tariff JSON",
        ),
        (
            "Annual fixed per customer ($)",
            f"={REF_ANNUAL_FIXED}",
            "(Total_RR - default_vol * kWh) / customers",
        ),
        (
            "Volumetric revenue ($)",
            f"={REF_DEFAULT_VOL}*{REF_TY_KWH}",
            "default_vol * total_kWh",
        ),
        (
            "Fixed revenue ($)",
            f"={REF_ANNUAL_FIXED}*{REF_N_CUSTOMERS}",
            "annual_fixed * total_customers",
        ),
        (
            "TOTAL CURRENT REVENUE ($)",
            f"=B{r + 4}+B{r + 5}",
            "vol_revenue + fixed_revenue",
        ),
        (
            "Total Delivery RR ($)",
            f"={REF_TOTAL_RR}",
            "From rate-case YAML",
        ),
        (
            "Check: current revenue = Total RR?",
            f"=ABS(B{r + 6}-B{r + 7})",
            "Should be < $1 (float rounding)",
        ),
    ]
    for item, formula, note in items_a:
        ws.cell(row=r, column=1, value=item)
        ws.cell(row=r, column=2, value=formula)
        ws.cell(row=r, column=3, value=note)
        r += 1

    total_current_rev_row = hdr_a + 7
    _bold(ws, f"A{total_current_rev_row}")
    _bold(ws, f"B{total_current_rev_row}")

    # --- Section B: Proposed split rates ---
    sec_b_row = r + 1
    ws.cell(row=sec_b_row, column=1, value="B. Revenue under proposed split rates")
    ws[f"A{sec_b_row}"].font = Font(bold=True, size=12)
    ws.merge_cells(f"A{sec_b_row}:D{sec_b_row}")

    hdr_b = sec_b_row + 1
    for ci, h in enumerate(["Item", "Value", "Formula", ""], start=1):
        ws.cell(row=hdr_b, column=ci, value=h)
    _header_fill(ws, hdr_b, 4)

    r = hdr_b + 1
    items_b = [
        (
            "HP customers",
            f"={REF_AGG_HP_N}",
            "sum(weight) for has_hp = true",
        ),
        (
            "Non-HP customers",
            f"={REF_AGG_NONHP_N}",
            "sum(weight) for has_hp = false",
        ),
        (
            "HP kWh",
            f"={REF_AGG_HP_KWH}",
            "sum(weight * annual_kwh) for HP",
        ),
        (
            "Non-HP kWh",
            f"={REF_AGG_NONHP_KWH}",
            "sum(weight * annual_kwh) for non-HP",
        ),
        (
            "HP volumetric rate ($/kWh)",
            f"={REF_HP_VOL}",
            "From calibrated HP flat tariff JSON",
        ),
        (
            "Non-HP volumetric rate ($/kWh)",
            f"={REF_NONHP_VOL}",
            "From calibrated adjusted-default tariff JSON",
        ),
        (
            "HP volumetric revenue ($)",
            f"=B{r + 4}*B{r + 2}",
            "hp_vol * hp_kWh",
        ),
        (
            "HP fixed revenue ($)",
            f"={REF_ANNUAL_FIXED}*B{r}",
            "annual_fixed * hp_customers",
        ),
        (
            "HP TOTAL REVENUE ($)",
            f"=B{r + 6}+B{r + 7}",
            "HP vol + HP fixed",
        ),
        (
            "Non-HP volumetric revenue ($)",
            f"=B{r + 5}*B{r + 3}",
            "nonhp_vol * nonhp_kWh",
        ),
        (
            "Non-HP fixed revenue ($)",
            f"={REF_ANNUAL_FIXED}*B{r + 1}",
            "annual_fixed * nonhp_customers",
        ),
        (
            "Non-HP TOTAL REVENUE ($)",
            f"=B{r + 9}+B{r + 10}",
            "Non-HP vol + Non-HP fixed",
        ),
        (
            "TOTAL PROPOSED REVENUE ($)",
            f"=B{r + 8}+B{r + 11}",
            "HP_total + nonHP_total",
        ),
    ]
    for item, formula, note in items_b:
        ws.cell(row=r, column=1, value=item)
        ws.cell(row=r, column=2, value=formula)
        ws.cell(row=r, column=3, value=note)
        r += 1

    hp_total_row = hdr_b + 9
    nonhp_total_row = hdr_b + 12
    proposed_total_row = hdr_b + 13
    for tr in (hp_total_row, nonhp_total_row, proposed_total_row):
        _bold(ws, f"A{tr}")
        _bold(ws, f"B{tr}")

    # --- Section C: The identity ---
    sec_c_row = r + 1
    ws.cell(
        row=sec_c_row,
        column=1,
        value="C. Revenue neutrality: proposed = current",
    )
    ws[f"A{sec_c_row}"].font = Font(bold=True, size=12)
    ws.merge_cells(f"A{sec_c_row}:D{sec_c_row}")

    hdr_c = sec_c_row + 1
    for ci, h in enumerate(["Item", "Value", "Formula", ""], start=1):
        ws.cell(row=hdr_c, column=ci, value=h)
    _header_fill(ws, hdr_c, 4)

    r = hdr_c + 1
    items_c = [
        (
            "Total current revenue ($)",
            f"=B{total_current_rev_row}",
            "From Section A",
        ),
        (
            "Total proposed revenue ($)",
            f"=B{proposed_total_row}",
            "From Section B",
        ),
        (
            "Difference ($)",
            f"=B{r + 1}-B{r}",
            "Should be ~$0 (float rounding)",
        ),
        (
            "HP subclass RR (EPMC, $)",
            f"={REF_HP_EPMC}",
            "From inputs_subclass_rr",
        ),
        (
            "Non-HP subclass RR (EPMC, $)",
            f"={REF_NONHP_EPMC}",
            "From inputs_subclass_rr",
        ),
        (
            "HP_RR + nonHP_RR ($)",
            f"=B{r + 3}+B{r + 4}",
            "Sum of subclass RRs",
        ),
        (
            "Total Delivery RR ($)",
            f"={REF_TOTAL_RR}",
            "From rate-case YAML",
        ),
        (
            "Check: HP_RR + nonHP_RR = Total_RR?",
            f"=ABS(B{r + 5}-B{r + 6})",
            "Should be < $1 (float rounding)",
        ),
    ]
    for item, formula, note in items_c:
        ws.cell(row=r, column=1, value=item)
        ws.cell(row=r, column=2, value=formula)
        ws.cell(row=r, column=3, value=note)
        r += 1

    # Number formats — dollar for most value cells.
    for row_i in range(hdr_a + 1, r):
        ws[f"B{row_i}"].number_format = "#,##0.00"

    _autosize(ws, {"A": 40, "B": 24, "C": 44, "D": 10})
    ws.sheet_view.showGridLines = False


def _write_validation(wb: Workbook, last_bat_row: int) -> None:
    ws = wb.create_sheet("validation")
    headers = ["check", "actual", "expected", "abs_error", "tolerance", "ok"]
    ws.append(headers)
    _header_fill(ws, 1, len(headers))

    last = last_bat_row
    rng_weight = f"bat_per_building!$B$2:$B${last}"
    rng_bill = f"bat_per_building!$E$2:$E${last}"
    rng_kwh = f"bat_per_building!$F$2:$F${last}"

    checks = [
        (
            "sum(weight) approx test_year_customer_count",
            f"=SUM({rng_weight})",
            f"={REF_N_CUSTOMERS}",
            0.05,
        ),
        (
            "sum(weight * bill) approx total_delivery_RR",
            f"=SUMPRODUCT({rng_weight},{rng_bill})",
            f"={REF_TOTAL_RR}",
            2000.0,
        ),
        (
            "sum(weight * kwh) approx test_year_residential_kwh",
            f"=SUMPRODUCT({rng_weight},{rng_kwh})",
            f"={REF_TY_KWH}",
            1.0,
        ),
        (
            "n_hp + n_nonhp approx test_year_customer_count",
            f"={REF_AGG_HP_N}+{REF_AGG_NONHP_N}",
            f"={REF_N_CUSTOMERS}",
            0.05,
        ),
        (
            "hp_kWh + nonhp_kWh approx test_year_residential_kwh",
            f"={REF_AGG_HP_KWH}+{REF_AGG_NONHP_KWH}",
            f"={REF_TY_KWH}",
            1.0,
        ),
        (
            "HP implied vol rate approx calibrated HP vol rate",
            "=hp_nonhp_aggregates!$H$2",
            f"={REF_HP_VOL}",
            0.0001,
        ),
        (
            "Non-HP implied vol rate approx calibrated non-HP vol rate",
            "=hp_nonhp_aggregates!$H$3",
            f"={REF_NONHP_VOL}",
            0.0001,
        ),
        (
            "HP_RR_epmc + nonHP_RR_epmc = total_delivery_RR",
            f"={REF_HP_EPMC}+{REF_NONHP_EPMC}",
            f"={REF_TOTAL_RR}",
            1.0,
        ),
    ]
    for i, (name, actual, expected, tol) in enumerate(checks, start=2):
        ws.cell(row=i, column=1, value=name)
        ws.cell(row=i, column=2, value=actual)
        ws.cell(row=i, column=3, value=expected)
        ws.cell(row=i, column=4, value=f"=ABS(B{i}-C{i})")
        ws.cell(row=i, column=5, value=tol)
        ws.cell(row=i, column=6, value=f'=IF(D{i}<=E{i},"OK","FAIL")')

    _autosize(ws, {"A": 60, "B": 22, "C": 22, "D": 16, "E": 14, "F": 8})
    for r in range(2, 2 + len(checks)):
        ws[f"B{r}"].number_format = "#,##0.000000"
        ws[f"C{r}"].number_format = "#,##0.000000"
        ws[f"D{r}"].number_format = "#,##0.000000"
    ws.sheet_view.showGridLines = False


# ---------------------------------------------------------------------------
# Orchestration.
# ---------------------------------------------------------------------------
def build_workbook(output_path: Path) -> Path:
    print(
        f"Loading per-building BAT from {PATH_MASTER_BAT_12} ...",
        flush=True,
    )
    bat = load_master_bat()
    print(f"  {bat.height:,} rows", flush=True)

    print(
        "Loading revenue-requirement YAMLs and tariff JSONs ...",
        flush=True,
    )
    inputs = load_inputs()
    print(
        f"  total_delivery_RR = ${inputs['total_delivery_revenue_requirement']:,.0f}",
        flush=True,
    )
    print(
        f"  default_vol = {inputs['default_vol_usd_per_kwh']:.6f} $/kWh",
        flush=True,
    )
    print(
        f"  hp_flat_vol = {inputs['hp_flat_vol_usd_per_kwh']:.6f} $/kWh",
        flush=True,
    )
    print(
        f"  nonhp_vol   = {inputs['nonhp_default_vol_usd_per_kwh']:.6f} $/kWh",
        flush=True,
    )
    print(
        f"  annual_fixed_per_customer = ${inputs['annual_fixed_per_customer']:,.2f}",
        flush=True,
    )

    bat = bat.with_columns(
        (
            (pl.col("annual_bill_delivery") - inputs["annual_fixed_per_customer"]) / inputs["default_vol_usd_per_kwh"]
        ).alias("annual_kwh")
    )

    _weighted_kwh = float((bat["weight"] * bat["annual_kwh"]).sum())
    _kwh_err = abs(_weighted_kwh - inputs["test_year_residential_kwh"])
    assert _kwh_err < 1.0, (
        f"sum(weight * annual_kwh) = {_weighted_kwh:,.0f} vs test_year_residential_kwh "
        f"= {inputs['test_year_residential_kwh']:,.0f}; error = {_kwh_err:,.2f}"
    )
    print(f"  annual_kwh derived from bills (aggregate kWh error = {_kwh_err:.4f})", flush=True)

    wb = Workbook()
    default = wb.active
    if default is not None:
        wb.remove(default)

    # inputs_tariffs first so annual_fixed formula resolves (same as RIE 1-11 / DIV-7 workbook).
    _write_readme(wb, inputs)
    _write_inputs_tariffs(wb, inputs)
    _write_inputs_revenue_requirement(wb, inputs)
    _write_inputs_subclass_rr(wb, inputs)
    last_bat_row = _write_bat_per_building(wb, bat)
    _write_hp_nonhp_aggregates(wb, last_bat_row)
    _write_revenue_neutrality_proof(wb)
    _write_validation(wb, last_bat_row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(output_path))
    print(
        f"Wrote {output_path} ({output_path.stat().st_size / 1024:.1f} KB)",
        flush=True,
    )
    return output_path


# ---------------------------------------------------------------------------
# Google Sheets upload formatting.
# ---------------------------------------------------------------------------
_TAB_FORMATTING: dict[str, dict] = {
    "README": {
        "wrap_columns": ["A:C"],
        "column_widths_px": {"A": 280, "B": 480, "C": 480},
        "freeze_rows": 1,
        "bold_header": True,
        "bold_rows": [3, 12, 22],
    },
    "inputs_revenue_requirement": {
        "column_number_formats": {"B": "#,##0.00"},
        "wrap_columns": ["C:D"],
        "column_widths_px": {"A": 280, "B": 140, "C": 480, "D": 480},
        "freeze_rows": 1,
        "bold_header": True,
    },
    "inputs_tariffs": {
        "column_number_formats": {"B": "0.000000"},
        "wrap_columns": ["C:D"],
        "column_widths_px": {"A": 240, "B": 130, "C": 520, "D": 400},
        "freeze_rows": 1,
        "bold_header": True,
    },
    "inputs_subclass_rr": {
        "column_number_formats": {
            "B": '"$"#,##0.00',
            "C": '"$"#,##0.00',
            "D": '"$"#,##0.00',
            "E": '"$"#,##0.00',
            "F": '"$"#,##0.00',
        },
        "auto_resize_columns": ["A:F"],
        "freeze_rows": 1,
        "bold_header": True,
    },
    "bat_per_building": {
        "column_number_formats": {
            "B": "#,##0.00",
            "E": '"$"#,##0.00',
            "F": "#,##0.00",
            "G": '"$"#,##0.00',
            "H": "#,##0.00",
            "I": "#,##0.00",
        },
        "auto_resize_columns": ["A:I"],
        "freeze_rows": 1,
        "bold_header": True,
    },
    "hp_nonhp_aggregates": {
        "column_number_formats": {
            "C": "#,##0.00",
            "D": '"$"#,##0.00',
            "E": "#,##0",
            "F": '"$"#,##0.00',
            "G": '"$"#,##0.00',
            "H": "0.000000",
            "I": "0.000000",
            "J": "0.000000",
        },
        "auto_resize_columns": ["A:J"],
        "freeze_rows": 1,
        "bold_header": True,
    },
    "revenue_neutrality_proof": {
        "column_number_formats": {"B": "#,##0.00"},
        "auto_resize_columns": ["A:D"],
        "freeze_rows": 0,
        "bold_header": True,
    },
    "validation": {
        "column_number_formats": {
            "B": "#,##0.000000",
            "C": "#,##0.000000",
            "D": "#,##0.000000",
        },
        "auto_resize_columns": ["A:F"],
        "freeze_rows": 1,
        "bold_header": True,
    },
}


def upload_to_sheet(xlsx_path: Path, spreadsheet_id: str) -> None:
    from lib.data.gsheets import apply_sheet_formatting, xlsx_to_gsheet

    print(
        f"Uploading {xlsx_path} -> Google Sheet {spreadsheet_id} ...",
        flush=True,
    )
    spreadsheet = xlsx_to_gsheet(xlsx_path, spreadsheet_id, delete_other_tabs=True)
    print("Applying number / wrap / width formatting ...", flush=True)
    for ws in spreadsheet.worksheets():
        spec = _TAB_FORMATTING.get(ws.title)
        if spec:
            apply_sheet_formatting(ws, **spec)
    print(
        f"Done. View at https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit",
        flush=True,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("cache/revenue_neutrality.xlsx"),
        help="Output .xlsx path. Default: cache/revenue_neutrality.xlsx",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload to Google Sheet after building.",
    )
    parser.add_argument(
        "--spreadsheet-id",
        default=DEFAULT_SPREADSHEET_ID,
        help=f"Override upload target. Default: {DEFAULT_SPREADSHEET_ID}",
    )
    args = parser.parse_args(argv)

    out = build_workbook(args.output)
    if args.upload:
        upload_to_sheet(out, args.spreadsheet_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
