#!/usr/bin/env python3
"""Allocate project-level PRP costs to census blocks by perimeter share.

For each raw ArcGIS construction polygon matched to a project in
pgl_project_costs.csv, compute how much of each overlapping block's
perimeter falls within the (8 m buffered) project polygon.  Allocate
the project's Total Project Forecast to blocks proportionally so that
100 % of each project's cost is distributed.  A block touching multiple
projects receives the sum of its pro-rated shares.

Blocks with no overlapping matched project get est_prp = NaN.

Output: the same block-level geojson with one additional column,
``est_prp``.
"""

import os
import tempfile
from pathlib import Path

import boto3
import geopandas as gpd
import pandas as pd

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------

POLYGON_BUFFER_M = 8
UTM_CRS = "EPSG:32616"
MIN_START = "2026-01-01"
S3_BUCKET = "data.sb"
S3_PREFIX = "il_npa/gis/pgl"


def _repo_root() -> Path:
    for parent in (Path.cwd().resolve(), *Path.cwd().resolve().parents):
        if (parent / ".git").exists() or (parent / ".here").exists():
            return parent
    raise RuntimeError("could not find reports2 repo root")


REPO = _repo_root()
DATA_DIR = REPO / "reports" / "il_npa" / "data"
OUTPUTS_DIR = DATA_DIR / "outputs"
UTILS_DIR = REPO / "reports" / "il_npa" / "utils"
COSTS_CSV = DATA_DIR / "pgl_project_costs.csv"

# ---------------------------------------------------------------------------
# I/O helpers (reused from project_level_check / clean script)
# ---------------------------------------------------------------------------


def read_geojson_with_s3_fallback(local_path: Path, s3_key: str) -> gpd.GeoDataFrame:
    if local_path.exists():
        print(f"  Reading from local: {local_path.name}")
        return gpd.read_file(local_path)
    print(f"  Downloading from S3: s3://{S3_BUCKET}/{s3_key}")
    s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))
    with tempfile.NamedTemporaryFile(suffix=".geojson", delete=False) as tmp:
        s3.download_fileobj(S3_BUCKET, s3_key, tmp)
        tmp_path = tmp.name
    gdf = gpd.read_file(tmp_path)
    os.unlink(tmp_path)
    return gdf


def _find_latest(directory: Path, pattern: str) -> Path | None:
    files = sorted(directory.glob(pattern))
    return files[-1] if files else None


# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------


def load_blocks() -> tuple[gpd.GeoDataFrame, str]:
    """Load the latest block-level geojson from data/outputs/."""
    candidates = sorted(
        f
        for f in OUTPUTS_DIR.glob("peoplesgas_with_buildings_streets_block_*.geojson")
        if "_with_est_prp" not in f.name
    )
    latest = candidates[-1] if candidates else None
    if latest is None:
        raise FileNotFoundError(f"No block geojson found in {OUTPUTS_DIR}. Run geo_data_cleaning.qmd first.")
    print(f"Blocks: {latest.name}")
    gdf = gpd.read_file(latest)
    print(f"  {len(gdf)} blocks loaded")
    return gdf, latest.name


def load_raw_polygons() -> gpd.GeoDataFrame:
    """Load raw ArcGIS construction polygons (pre-union)."""
    local_files = sorted(UTILS_DIR.glob("peoplesgas_projects_*.geojson"))
    if local_files:
        raw_path = local_files[-1]
        raw_s3_key = f"{S3_PREFIX}/{raw_path.name}"
    else:
        raw_path = UTILS_DIR / "peoplesgas_projects_20251117.geojson"
        raw_s3_key = f"{S3_PREFIX}/peoplesgas_projects_20251117.geojson"

    raw = read_geojson_with_s3_fallback(raw_path, raw_s3_key)
    print(f"  {len(raw)} raw polygons loaded")
    return raw


def load_costs() -> pd.DataFrame:
    """Load and clean pgl_project_costs.csv."""
    costs = pd.read_csv(COSTS_CSV)
    costs["total_forecast"] = pd.to_numeric(
        costs["Total Project Forecast"].astype(str).str.replace(",", ""),
        errors="coerce",
    )
    costs = costs.rename(
        columns={
            "Project Identifier": "mx_id",
            "Project Name": "project_name",
            "Total Project CI/DI main retirement mileage": "mileage",
        }
    )
    costs["name_upper"] = costs["project_name"].str.upper()
    print(f"Costs: {len(costs)} rows, {costs['total_forecast'].notna().sum()} with forecast")
    return costs


# ---------------------------------------------------------------------------
# 2. Match raw polygons → cost data (replicating project_level_check logic)
# ---------------------------------------------------------------------------


def match_polygons_to_costs(raw: gpd.GeoDataFrame, costs: pd.DataFrame) -> gpd.GeoDataFrame:
    """Filter raw polygons, build combined_name, join to cost CSV."""

    # Build combined project name from PR_NAME + Phase
    raw = raw.copy()
    raw["phase_clean"] = raw["Phase"].fillna("").astype(str).str.replace("-", "", regex=False).str.strip()
    raw["combined_name"] = (raw["PR_NAME"].fillna("") + " " + raw["phase_clean"]).str.strip().str.upper()

    # Filter: exclude PI/SI and street restoration
    mask = (
        (raw["TYPE"] != "PI / SI") & (raw["TYPE"] != "PI / SI ") & (raw["STATUS"] != "Street and landscape restoration")
    )
    raw = raw[mask].copy()

    # Classify status using C_START date
    if "C_START" in raw.columns:
        raw["C_START_dt"] = pd.to_datetime(raw["C_START"], unit="ms", errors="coerce")
        raw["status_simple"] = raw["C_START_dt"].apply(
            lambda x: "closed" if pd.notnull(x) and x < pd.Timestamp(MIN_START) else "planned"
        )
    else:
        raw["status_simple"] = "planned"

    raw = raw[raw["status_simple"] == "planned"].copy()
    print(f"  After filtering: {len(raw)} planned polygons")

    # Join to costs on combined_name
    cost_cols = ["mx_id", "project_name", "total_forecast", "name_upper"]
    costs_valid = costs[costs["total_forecast"].notna()][cost_cols].copy()

    matched = raw.merge(costs_valid, left_on="combined_name", right_on="name_upper", how="inner")
    print(f"  Matched to cost data: {len(matched)} polygon rows")
    print(f"  Unique projects: {matched['mx_id'].nunique()}")
    return matched


# ---------------------------------------------------------------------------
# 3. Allocate costs by perimeter share
# ---------------------------------------------------------------------------


def allocate_costs(
    blocks: gpd.GeoDataFrame,
    matched_projects: gpd.GeoDataFrame,
) -> pd.DataFrame:
    """For each project, allocate total_forecast to blocks by perimeter share.

    Returns a DataFrame with columns [geoid10, est_prp].
    """
    blocks_utm = blocks[["geoid10", "geometry"]].to_crs(UTM_CRS)
    proj_utm = matched_projects[["mx_id", "total_forecast", "geometry"]].to_crs(UTM_CRS)

    # Buffer project polygons
    proj_utm = proj_utm.copy()
    proj_utm["geometry"] = proj_utm.geometry.buffer(POLYGON_BUFFER_M)

    # Precompute block boundaries (LineString/MultiLineString)
    blocks_utm = blocks_utm.copy()
    blocks_utm["boundary"] = blocks_utm.geometry.boundary

    # At least one project (ROSEMOOR PH03) has two polygon pieces with the
    # same PR_NAME + Phase.  Dissolve to one geometry per mx_id so each
    # project's total_forecast is allocated exactly once.
    proj_dissolved = proj_utm.dissolve(by="mx_id", aggfunc="first").reset_index()

    allocations: list[pd.DataFrame] = []
    project_qc: list[dict] = []

    for _, proj_row in proj_dissolved.iterrows():
        mx_id = proj_row["mx_id"]
        proj_geom = proj_row["geometry"]
        total_forecast = proj_row["total_forecast"]

        if proj_geom is None or proj_geom.is_empty or pd.isna(total_forecast):
            continue

        # Compute perimeter of each block's boundary inside this project polygon
        perim_in_project = blocks_utm["boundary"].intersection(proj_geom).length

        # Keep blocks with nonzero overlap
        overlap_mask = perim_in_project > 0
        if not overlap_mask.any():
            project_qc.append(
                {
                    "mx_id": mx_id,
                    "total_forecast": total_forecast,
                    "n_blocks": 0,
                    "total_allocated": 0,
                }
            )
            continue

        overlapping = blocks_utm.loc[overlap_mask, ["geoid10"]].copy()
        overlapping["perim_in_project"] = perim_in_project[overlap_mask].values
        total_perim = overlapping["perim_in_project"].sum()
        overlapping["share"] = overlapping["perim_in_project"] / total_perim
        overlapping["est_prp_contribution"] = total_forecast * overlapping["share"]
        overlapping["mx_id"] = mx_id

        allocations.append(overlapping[["geoid10", "mx_id", "est_prp_contribution"]])

        project_qc.append(
            {
                "mx_id": mx_id,
                "total_forecast": total_forecast,
                "n_blocks": len(overlapping),
                "total_allocated": overlapping["est_prp_contribution"].sum(),
            }
        )

    # QC summary
    qc = pd.DataFrame(project_qc)
    _print_qc(qc)

    if not allocations:
        print("WARNING: No allocations produced!")
        return pd.DataFrame({"geoid10": pd.Series(dtype=str), "est_prp": pd.Series(dtype=float)})

    all_alloc = pd.concat(allocations, ignore_index=True)

    # Sum across projects for blocks that touch >1 project
    block_est = all_alloc.groupby("geoid10")["est_prp_contribution"].sum().reset_index()
    block_est = block_est.rename(columns={"est_prp_contribution": "est_prp"})

    return block_est


def _print_qc(qc: pd.DataFrame) -> None:
    """Print allocation QC diagnostics."""
    print("\n" + "=" * 70)
    print("QC: Per-project allocation summary")
    print("=" * 70)

    if qc.empty:
        print("  No projects to report.")
        return

    qc["diff"] = qc["total_allocated"] - qc["total_forecast"]
    qc["pct_diff"] = (qc["diff"] / qc["total_forecast"] * 100).round(4)

    n_matched = (qc["n_blocks"] > 0).sum()
    n_zero = (qc["n_blocks"] == 0).sum()
    print(f"  Projects with block overlaps: {n_matched}")
    print(f"  Projects with NO block overlaps: {n_zero}")
    if n_zero > 0:
        print("    (these projects' costs are unallocated)")
        zero_projects = qc[qc["n_blocks"] == 0]["mx_id"].tolist()
        for mx in zero_projects[:10]:
            print(f"      {mx}")
        if len(zero_projects) > 10:
            print(f"      ... and {len(zero_projects) - 10} more")

    print(f"\n  Total forecast (matched projects): ${qc['total_forecast'].sum():>14,.0f}")
    print(f"  Total allocated to blocks:         ${qc['total_allocated'].sum():>14,.0f}")

    # Flag any large deviations (should be ~0 by construction)
    big_diff = qc[qc["pct_diff"].abs() > 0.01]
    if len(big_diff) > 0:
        print(f"\n  WARNING: {len(big_diff)} projects with allocation error > 0.01%:")
        for _, row in big_diff.head(5).iterrows():
            print(
                f"    {row['mx_id']}: forecast=${row['total_forecast']:,.0f}  "
                f"allocated=${row['total_allocated']:,.0f}  diff={row['pct_diff']:.4f}%"
            )


# ---------------------------------------------------------------------------
# 4. Main
# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 70)
    print("Allocating PRP project costs to census blocks")
    print("=" * 70)

    blocks, block_filename = load_blocks()
    raw = load_raw_polygons()
    costs = load_costs()

    matched = match_polygons_to_costs(raw, costs)
    block_est = allocate_costs(blocks, matched)

    # Left-join est_prp onto original blocks
    blocks = blocks.merge(block_est, on="geoid10", how="left")

    n_with = blocks["est_prp"].notna().sum()
    n_without = blocks["est_prp"].isna().sum()
    print(f"\n  Blocks with est_prp:    {n_with}")
    print(f"  Blocks without (NaN):   {n_without}")
    print(f"  Total est_prp:          ${blocks['est_prp'].sum():>14,.0f}")

    # Comparison with system-average approach
    SYS_AVG_CPM = 4_233_333.333
    if "street_miles" in blocks.columns:
        blocks["prp_sys_avg"] = blocks["street_miles"] * SYS_AVG_CPM
        both = blocks[blocks["est_prp"].notna()].copy()
        if len(both) > 0:
            print("\n  Comparison (blocks with est_prp):")
            print(f"    Sum est_prp:        ${both['est_prp'].sum():>14,.0f}")
            print(f"    Sum sys-avg prp:    ${both['prp_sys_avg'].sum():>14,.0f}")
            ratio = both["est_prp"].sum() / both["prp_sys_avg"].sum()
            print(f"    Ratio (est/sys):    {ratio:.3f}")
        blocks = blocks.drop(columns=["prp_sys_avg"])

    # Export
    out_name = block_filename.replace(".geojson", "_with_est_prp.geojson")
    out_path = OUTPUTS_DIR / out_name
    blocks.to_file(out_path, driver="GeoJSON")
    print(f"\n✅ Exported: {out_path.name}")
    print(f"   {len(blocks)} blocks, schema: {list(blocks.columns)}")


if __name__ == "__main__":
    main()
