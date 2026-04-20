#!/usr/bin/env python3
"""
Geo Data Cleaning Script to clean and union Peoples Gas construction polygons
Processes geospatial data for Peoples Gas construction polygons

Script Workflow and Transformations Summary
-------------------------------------------

This script prepares and cleans Peoples Gas construction polygons data for further spatial analysis. Below are the key transformations performed:
Data was sourced from the Peoples Gas Construction Polygons dataset using reports/il_npa/utils/download_peoplesgas_data.py
1. **File Loading and Setup**
   - Sets up directories for input (`../data/geo_data`, `../utils`) and output (`../data/outputs`).
   - Locates and reads the most recent available Peoples Gas construction polygons file.

2. **Column Standardization and Basic Cleaning**
   - Renames columns (e.g., `TYPE` to `PRP_TYPE`) for schema consistency.
   - Reports and analyzes missing values in key fields such as `PRP_TYPE` and `C_START`.
   - Drops columns that are not needed (e.g., removes `Contractor` column).

3. **Filtering Records**
   - Removes polygons classified as `"PI / SI"` in the `PRP_TYPE` column (with or without trailing space).
   - Removes polygons with `STATUS` set to `"Street and landscape restoration"`.

4. **Unioning Overlapping Polygons**
   - Uses a threshold of 1 square meter to union overlapping polygons.
   - Uses a connected components algorithm to find overlapping polygons.
   - Uses a union operation to combine overlapping polygons.

5. **Status assignment**
   - Assigns a status to each polygon based on the `C_START` column.
   - If the `C_START` date is before the `MIN_START` date, the polygon is assigned the status "closed".
   - If the `C_START` date is after the `MIN_START` date, the polygon is assigned the status "planned".

6. **Diagnostics**
   - Reports counts and summaries to provide transparency about any data removed or modified.

The result is 2 versions of the cleaned and filtered Peoples Gas construction polygon dataset, ready for integration with additional city datasets in downstream workflows.

1. `peoples_polygons_unioned.geojson` - Unioned polygons by status_simple (overlap > 1 sq meter)
    - This file is used for further geometric processing and integration with additional city datasets in downstream workflows.
    - Planned and closed polygons are unioned separately. No clipping is performed where closed polygons overlap with planned polygons.
2. `peoples_polygons_unioned_clipped.geojson` - Unioned polygons by status_simple (overlap > 1 sq meter) clipped by closed polygons
    - This file was not used in the analysis.
    - Planned and closed polygons are unioned separately. Planned polygons are clipped by the union of all closed polygons.
"""

import os
import tempfile
from datetime import datetime
from pathlib import Path

import boto3
import geopandas as gpd
import pandas as pd
from botocore.exceptions import ClientError, NoCredentialsError
from shapely.ops import unary_union

timestamp = datetime.now().strftime("%Y%m%d")


def _repo_root() -> Path:
    for parent in (Path.cwd().resolve(), *Path.cwd().resolve().parents):
        if (parent / ".git").exists() or (parent / ".here").exists():
            return parent
    raise RuntimeError("could not find reports2 repo root")


REPO = _repo_root()
data_dir = REPO / "reports" / "il_npa" / "data"
outputs_dir = data_dir / "outputs"
outputs_dir.mkdir(parents=True, exist_ok=True)
utils_dir = REPO / "reports" / "il_npa" / "utils"

MIN_START = "2026-01-01"
S3_BUCKET = "data.sb"
S3_PREFIX = "il_npa/gis/pgl"


def read_geojson_with_s3_fallback(local_path: Path, s3_bucket: str, s3_key: str) -> gpd.GeoDataFrame:
    """Read GeoJSON from local path, falling back to S3 if not present locally."""
    local_path = Path(local_path)
    if local_path.exists():
        print(f"  Reading from local file: {local_path.name}")
        return gpd.read_file(local_path)

    print(f"  Local file not found, reading from S3: s3://{s3_bucket}/{s3_key}")
    try:
        s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".geojson", delete=False) as tmp:
            tmp_path = tmp.name
            s3.download_fileobj(s3_bucket, s3_key, tmp)
        gdf = gpd.read_file(tmp_path)
        os.unlink(tmp_path)
        print("  Successfully loaded from S3")
        return gdf
    except NoCredentialsError:
        print("  Error: AWS credentials not found; cannot read from S3.")
        raise
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "Unknown")
        print(f"  AWS Error ({code}): {e}")
        raise


def find_latest_pg_file() -> tuple[Path, str]:
    """Locate the most recent peoplesgas_projects_*.geojson.

    Prefers a local file in utils/; otherwise lists S3 and returns a synthetic
    local path (that won't exist on disk) alongside the S3 key so the S3
    fallback path in read_geojson_with_s3_fallback is taken.
    """
    local_files = sorted(utils_dir.glob("peoplesgas_projects_*.geojson"))
    if local_files:
        f = local_files[-1]
        return f, f"{S3_PREFIX}/{f.name}"

    print("No local Peoples Gas file found, looking for most recent in S3...")
    s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))
    resp = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=f"{S3_PREFIX}/peoplesgas_projects_")
    contents = resp.get("Contents", [])
    if not contents:
        raise FileNotFoundError(
            f"No peoplesgas_projects_*.geojson found locally in {utils_dir} "
            f"or in s3://{S3_BUCKET}/{S3_PREFIX}/. "
            "Run `just fetch-data` (and `just upload-data`) to populate it."
        )
    latest = sorted(contents, key=lambda x: x["LastModified"], reverse=True)[0]
    s3_key = latest["Key"]
    name = s3_key.rsplit("/", 1)[-1]
    print(f"  Found most recent in S3: {s3_key}")
    return utils_dir / name, s3_key


pg_local, pg_s3_key = find_latest_pg_file()
print(f"Loading: {pg_local.name}")
pg_polygons = read_geojson_with_s3_fallback(pg_local, S3_BUCKET, pg_s3_key)
print(f"Loaded {len(pg_polygons):,} Peoples Gas construction polygons")

if "TYPE" in pg_polygons.columns:
    pg_polygons = pg_polygons.rename(columns={"TYPE": "PRP_TYPE"})

n_none_prp_type = pg_polygons["PRP_TYPE"].isna().sum()
print(f"Rows with PRP_TYPE == None: {n_none_prp_type:,}")

if "C_START" in pg_polygons.columns:
    n_none_and_valid_cstart = pg_polygons[pg_polygons["PRP_TYPE"].isna() & pg_polygons["C_START"].notna()].shape[0]
    print(f"Rows with PRP_TYPE == None and valid C_START: {n_none_and_valid_cstart:,}")

pg_polygons = pg_polygons.drop(columns=["Contractor"])

# Exclude PRP_TYPE == "PI / SI " (with trailing space) or "PI / SI" (without)
# Also exclude STATUS == 'Street and landscape restoration'
filtered = pg_polygons[
    (pg_polygons["PRP_TYPE"] != "PI / SI") & (pg_polygons["STATUS"] != "Street and landscape restoration")
].copy()
print(f"Excluded {len(pg_polygons) - len(filtered):,} polygons (PI / SI or Street and landscape restoration)")

datetime_cols = ["C_START", "C_FINISH", "R_START", "R_FINISH"]
for col in datetime_cols:
    if col in filtered.columns:
        filtered[col] = pd.to_datetime(filtered[col], unit="ms", errors="coerce")

filtered["status_simple"] = filtered["C_START"].apply(
    lambda x: "closed" if pd.notnull(x) and x < pd.Timestamp(MIN_START) else "planned"
)

if "C_START" in filtered.columns and "status_simple" in filtered.columns:
    print("\nSummary statistics for C_START by status_simple:")
    stats = filtered.groupby("status_simple")["C_START"].agg(["min", "max", "median", "count"])
    print(stats)

# Threshold for unioning overlapping polygons: 1 square meter
# Applied in UTM Zone 16N (EPSG:32616) which uses meters.
OVERLAP_THRESHOLD_SQM = 1.0


def find_connected_components(graph):
    """Find connected components in an undirected graph using DFS.
    Handles isolated nodes (nodes with no edges) as single-node components.
    """
    visited = set()
    components = []

    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)

    return components


union_by_status = []
for status, subset in filtered.groupby("status_simple"):
    subset_m = subset.to_crs(epsg=32616)
    subset_m = subset_m[subset_m.geometry.notna() & ~subset_m.geometry.is_empty].copy()

    if len(subset_m) == 0:
        print(f"  Warning: No valid geometries for status '{status}', skipping...")
        continue

    print(f"  Processing {len(subset_m):,} polygons for status '{status}' (CRS: {subset_m.crs}, units: meters)")

    geom_index = subset_m.reset_index()
    spatial_index = geom_index.sindex

    overlap_graph = {idx: [] for idx in geom_index.index}
    total_overlaps_found = 0
    total_overlaps_above_threshold = 0

    for idx, row in geom_index.iterrows():
        geom = row.geometry
        if geom is None or geom.is_empty:
            continue

        possible_matches = list(spatial_index.intersection(geom.bounds))

        for idx2 in possible_matches:
            if idx2 == idx:
                continue
            other_geom = geom_index.loc[idx2, "geometry"]
            if other_geom is None or other_geom.is_empty:
                continue
            if geom.intersects(other_geom):
                overlap_area = geom.intersection(other_geom).area
                total_overlaps_found += 1
                if overlap_area > OVERLAP_THRESHOLD_SQM:
                    if idx2 not in overlap_graph[idx]:
                        overlap_graph[idx].append(idx2)
                    if idx not in overlap_graph[idx2]:
                        overlap_graph[idx2].append(idx)
                    total_overlaps_above_threshold += 1

    components = find_connected_components(overlap_graph)

    unions = []
    c_start_mins = []
    c_start_maxs = []
    for component in components:
        if len(component) == 0:
            continue
        component_geoms = [geom_index.loc[idx, "geometry"] for idx in component if idx in geom_index.index]
        component_geoms = [g for g in component_geoms if g is not None and not g.is_empty]
        if len(component_geoms) > 0:
            unioned_geom = unary_union(component_geoms)
            unions.append(unioned_geom)

            if "C_START" in geom_index.columns:
                component_c_starts = [
                    geom_index.loc[idx, "C_START"]
                    for idx in component
                    if idx in geom_index.index and pd.notna(geom_index.loc[idx, "C_START"])
                ]
                if len(component_c_starts) > 0:
                    c_start_mins.append(min(component_c_starts))
                    c_start_maxs.append(max(component_c_starts))
                else:
                    c_start_mins.append(None)
                    c_start_maxs.append(None)
            else:
                c_start_mins.append(None)
                c_start_maxs.append(None)

    print(
        f"    Found {total_overlaps_found:,} overlaps, {total_overlaps_above_threshold:,} above {OVERLAP_THRESHOLD_SQM} sqm threshold"
    )
    print(f"    Found {len(components):,} connected components")
    print(f"    Created {len(unions):,} unioned polygons")

    gdf = gpd.GeoDataFrame(
        {
            "status_simple": [status] * len(unions),
            "geometry": unions,
            "C_START_min": c_start_mins,
            "C_START_max": c_start_maxs,
        },
        crs=subset_m.crs,
    )
    union_by_status.append(gdf)

unioned_polygons = pd.concat(union_by_status, ignore_index=True)
unioned_polygons = unioned_polygons.to_crs("EPSG:4326")

print("\nCreated unioned polygons by status_simple (overlap > 1 sq meter):")
print(unioned_polygons[["status_simple", "geometry"]].head())

output_cleaned = outputs_dir / "peoples_polygons_unioned.geojson"
unioned_polygons.to_file(output_cleaned, driver="GeoJSON")
print(f"✅ Exported cleaned, unioned polygons to: {output_cleaned.name}")

print("\n🔪 Clipping planned polygons by closed polygons...")

planned_polygons = unioned_polygons[unioned_polygons["status_simple"] == "planned"].copy()
closed_polygons = unioned_polygons[unioned_polygons["status_simple"] == "closed"].copy()

print(f"  Planned polygons: {len(planned_polygons):,}")
print(f"  Closed polygons: {len(closed_polygons):,}")

if len(planned_polygons) > 0 and len(closed_polygons) > 0:
    planned_utm = planned_polygons.to_crs(epsg=32616)
    closed_utm = closed_polygons.to_crs(epsg=32616)

    closed_union_geom = unary_union(list(closed_utm.geometry))

    print("  Subtracting closed polygon areas from planned polygons...")
    planned_utm["geometry"] = planned_utm.geometry.difference(closed_union_geom)

    planned_utm = planned_utm[~planned_utm.geometry.is_empty].copy()
    print(f"  Planned polygons after clipping: {len(planned_utm):,}")

    clipped_result = pd.concat([planned_utm, closed_utm], ignore_index=True)
    clipped_result = clipped_result.to_crs("EPSG:4326")

    output_clipped = outputs_dir / "peoples_polygons_unioned_clipped.geojson"
    clipped_result.to_file(output_clipped, driver="GeoJSON")
    print(f"✅ Exported clipped polygons to: {output_clipped.name}")
elif len(planned_polygons) > 0:
    output_clipped = outputs_dir / "peoples_polygons_unioned_clipped.geojson"
    planned_polygons.to_file(output_clipped, driver="GeoJSON")
    print(f"✅ No closed polygons to clip from, exported planned polygons to: {output_clipped.name}")
else:
    print("  No planned polygons to clip")
