#!/usr/bin/env python3
"""
Parcel-Building Matching Script
Matches parcels with buildings to assign unit counts.
This script runs separately to reduce memory load on the main geo_data_cleaning script.
Works on the full datasets (not filtered by construction polygons).

Workflow Description:
---------------------
This script executes a spatial join between Cook County parcels and Chicago building footprints to match parcels with their corresponding buildings citywide, intended primarily to assign building unit counts from assessor data to parcels.

**Key workflow steps:**
1. Load the most recent parcels and building footprints from the geo_data directory, as GeoDataFrames.
2. Load the Cook County Assessor lookup table for unit counts and building class information.
3. Ensure all spatial datasets use a projected CRS suitable for accurate spatial operations.
4. Clean and validate geometries to avoid spatial errors.
5. Perform a spatial join between parcels and buildings to determine which buildings are located within which parcels.
6. For buildings that fall within a parcel, the script aims to establish a 1:1 correspondence between buildings and parcels:
    - If a parcel matches to multiple buildings (a common situation for multi-building lots or complex footprints), the script identifies the building that has the greatest area overlap with the parcel and uses only this building for that parcel.
    - This "area of overlap" is computed via intersection of building and parcel geometries.
    - Thus, each parcel is matched to at most one building—the one physically covering the largest area within that parcel.
7. Assign unit counts and other attributes as appropriate via joins with the assessor lookup.
8. Save the resulting matched data, including per-parcel assigned unit counts, to the outputs directory for downstream use.
9. The script outputs diagnostics such as number of matched parcels, distribution of overlap areas, and how many parcels/buildings had 1:1 or many:1 relationships.

**Notes:**
- The workflow is designed to ensure a deterministic 1:1 mapping: each parcel is associated with at most one building, chosen by maximum area of overlap.
- Unmatched parcels (no buildings within) or buildings not contained in any parcel are reported separately.

This script is intended to be run independently from the main geo_data_cleaning notebook to avoid excessive memory consumption and to operate on the complete datasets.
"""

import gc
import os
import tempfile
from datetime import datetime
from pathlib import Path

import boto3
import geopandas as gpd
import pandas as pd
from botocore.exceptions import ClientError, NoCredentialsError

# Set paths
data_dir = Path("../data")
geo_data_dir = data_dir / "geo_data"
outputs_dir = data_dir / "outputs"
outputs_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d")


def read_geojson_with_s3_fallback(local_path: Path, s3_bucket: str, s3_key: str):
    """
    Read GeoJSON file, checking local path first, then falling back to S3.

    Args:
        local_path: Local file path to check first
        s3_bucket: S3 bucket name
        s3_key: S3 object key (path within bucket)

    Returns:
        GeoDataFrame loaded from local file or S3
    """
    local_path = Path(local_path)

    # Check if local file exists
    if local_path.exists():
        print(f"  Reading from local file: {local_path.name}")
        return gpd.read_file(local_path)

    # Local file doesn't exist, try reading from S3
    print(f"  Local file not found, reading from S3: s3://{s3_bucket}/{s3_key}")
    try:
        # Create S3 client
        s3_client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))

        # Download to temporary file
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".geojson", delete=False) as tmp_file:
            tmp_path = tmp_file.name
            s3_client.download_fileobj(s3_bucket, s3_key, tmp_file)

        # Read from temporary file
        gdf = gpd.read_file(tmp_path)

        # Clean up temporary file
        os.unlink(tmp_path)

        print("  ✅ Successfully loaded from S3")
        return gdf

    except NoCredentialsError:
        print("  ❌ Error: AWS credentials not found. Cannot read from S3.")
        raise
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        if error_code == "NoSuchKey":
            print(f"  ❌ Error: File not found in S3: s3://{s3_bucket}/{s3_key}")
        else:
            print(f"  ❌ AWS Error ({error_code}): {e}")
        raise
    except Exception as e:
        print(f"  ❌ Unexpected error reading from S3: {e}")
        raise


print("🔍 Parcel-Building Matching Script")
print("=" * 60)

# Find the most recent parcels file (full dataset)
parcel_files = sorted(geo_data_dir.glob("cook_county_parcels_*.geojson"))
if parcel_files:
    parcels_file = parcel_files[-1]
    local_path = parcels_file
    # Extract date from filename for S3 key (e.g., cook_county_parcels_20251117.geojson)
    s3_key = f"gis/pgl/{parcels_file.name}"
    print(f"Loading parcels: {parcels_file.name}")
else:
    # No local file found, try to find most recent in S3
    print("⚠️  No local parcels file found, attempting to find most recent in S3...")
    try:
        s3_client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))
        # List objects with prefix
        response = s3_client.list_objects_v2(
            Bucket="data.sb.east",
            Prefix="gis/pgl/cook_county_parcels_",
        )
        if "Contents" in response:
            # Sort by last modified, get most recent
            objects = sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True)
            s3_key = objects[0]["Key"]
            print(f"  Found most recent in S3: {s3_key}")
        else:
            raise FileNotFoundError("No parcels files found in S3")
    except Exception as e:
        print(f"❌ Error finding parcels in S3: {e}")
        print("Please run: just fetch-parcels")
        exit(1)
    local_path = geo_data_dir / "cook_county_parcels_NOT_FOUND.geojson"  # Won't exist, triggers S3 read

parcels = read_geojson_with_s3_fallback(
    local_path=local_path,
    s3_bucket="data.sb.east",
    s3_key=s3_key,
)
print(f"  Loaded {len(parcels):,} parcels")

# Find the most recent buildings file (full dataset)
building_files = sorted(geo_data_dir.glob("chicago_buildings_*.geojson"))
if building_files:
    buildings_file = building_files[-1]
    local_path = buildings_file
    # Extract date from filename for S3 key
    s3_key = f"gis/pgl/{buildings_file.name}"
    print(f"Loading buildings: {buildings_file.name}")
else:
    # No local file found, try to find most recent in S3
    print("⚠️  No local buildings file found, attempting to find most recent in S3...")
    try:
        s3_client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))
        # List objects with prefix
        response = s3_client.list_objects_v2(
            Bucket="data.sb.east",
            Prefix="gis/pgl/chicago_buildings_",
        )
        if "Contents" in response:
            # Sort by last modified, get most recent
            objects = sorted(response["Contents"], key=lambda x: x["LastModified"], reverse=True)
            s3_key = objects[0]["Key"]
            print(f"  Found most recent in S3: {s3_key}")
        else:
            raise FileNotFoundError("No buildings files found in S3")
    except Exception as e:
        print(f"❌ Error finding buildings in S3: {e}")
        print("Please run: just fetch-buildings")
        exit(1)
    local_path = geo_data_dir / "chicago_buildings_NOT_FOUND.geojson"  # Won't exist, triggers S3 read

buildings = read_geojson_with_s3_fallback(
    local_path=local_path,
    s3_bucket="data.sb.east",
    s3_key=s3_key,
)
print(f"  Loaded {len(buildings):,} buildings")

# Load assessor lookup
lookup_file = data_dir / "cook_county_assessor_lookup.csv"
if not lookup_file.exists():
    print(f"ERROR: Assessor lookup file not found: {lookup_file}")
    exit(1)

print(f"Loading assessor lookup: {lookup_file.name}")
assessor_lookup = pd.read_csv(lookup_file, dtype={"assessor_class": str})

# Classify parcels
print("\n📋 Classifying parcels...")
parcels_classified = parcels.merge(assessor_lookup, left_on="assessorbldgclass", right_on="assessor_class", how="left")

classified_count = parcels_classified["type"].notna().sum()
print(f"  Classified {classified_count:,} of {len(parcels_classified):,} parcels")

# Show distribution
type_dist = parcels_classified["type"].value_counts()
residential = parcels_classified[parcels_classified["type"] == "residential"]
if len(residential) > 0:
    sf_mf_dist = residential["sf_mf"].value_counts()
    print(
        f"  Residential: {len(residential):,} ({sf_mf_dist.get('single-family', 0):,} SF, {sf_mf_dist.get('multi-family', 0):,} MF)"
    )

# Free memory
del parcels
gc.collect()

# Perform parcel-building matching
if len(buildings) > 0:
    # Project to UTM for accurate spatial operations
    buildings_utm = buildings.to_crs("EPSG:32616")

    # Project parcels to UTM for accurate spatial operations
    parcels_classified_utm = parcels_classified.to_crs("EPSG:32616")

    # Add unique parcel identifier for tracking
    parcels_classified_utm["parcel_idx"] = range(len(parcels_classified_utm))

    # Add building identifier if not present
    if "bldg_id" not in buildings_utm.columns:
        buildings_utm = buildings_utm.copy()
        buildings_utm["bldg_id"] = buildings_utm.index.astype(str)

    # Make geometries valid to prevent crashes
    parcels_classified_utm["geometry"] = parcels_classified_utm["geometry"].make_valid()
    buildings_utm["geometry"] = buildings_utm["geometry"].make_valid()

    print("\n🔍 Starting parcel-building matching...")
    print(f"  Parcels: {len(parcels_classified_utm):,}")
    print(f"  Buildings: {len(buildings_utm):,}")

    # Find all parcel-building intersections using only relevant columns
    overlay = gpd.overlay(
        parcels_classified_utm[["geometry", "parcel_idx"]],
        buildings_utm[["geometry", "no_of_unit", "bldg_id"]],
        how="intersection",
        keep_geom_type=False,
    )

    print(f"  Intersections found: {len(overlay):,}")

    # Calculate overlap area for each intersection
    overlay["overlap_area"] = overlay.geometry.area

    # Group by parcel_idx and find building with maximum overlap
    overlap_by_parcel = (
        overlay.groupby("parcel_idx").apply(lambda x: x.loc[x["overlap_area"].idxmax()]).reset_index(drop=True)
    )

    print(f"  Parcels with building matches: {len(overlap_by_parcel):,}")

    # Free memory from large intermediate dataset
    del overlay
    gc.collect()

    # Create enriched parcels dataset
    parcels_with_units = parcels_classified.copy()
    parcels_with_units["parcel_idx"] = range(len(parcels_with_units))

    # Merge the best matches back to parcels
    parcels_with_units = parcels_with_units.merge(
        overlap_by_parcel[["parcel_idx", "no_of_unit", "bldg_id", "overlap_area"]], on="parcel_idx", how="left"
    )

    # Keep original building data in separate column for auditing
    parcels_with_units["matched_building_id"] = parcels_with_units["bldg_id"]
    parcels_with_units["overlap_area_sqm"] = parcels_with_units["overlap_area"]
    parcels_with_units["building_units_raw"] = pd.to_numeric(parcels_with_units["no_of_unit"], errors="coerce")

    # Drop temporary columns
    parcels_with_units = parcels_with_units.drop(columns=["parcel_idx", "no_of_unit", "bldg_id", "overlap_area"])

    # Validate specific example: parcel at -87.57623748, 41.74593814 should match building 631646
    test_parcel = parcels_with_units[
        (parcels_with_units["longitude"].astype(float).round(8) == round(-87.57623748, 8))
        & (parcels_with_units["latitude"].astype(float).round(8) == round(41.74593814, 8))
    ]
    if len(test_parcel) > 0:
        print("\n✅ Validation check for test parcel (-87.57623748, 41.74593814):")
        print(f"   Matched building_id: {test_parcel['matched_building_id'].values[0]}")
        print(f"   Building units: {test_parcel['building_units_raw'].values[0]}")
        print("   Expected building_id: 631646")
        if test_parcel["matched_building_id"].values[0] == "631646":
            print("   ✓ Match is correct!")
        else:
            print("   ⚠️  Match differs from expected")

    # Create working column starting with raw data
    parcels_with_units["building_units"] = parcels_with_units["building_units_raw"].copy()

    # Apply fallback logic for missing/zero unit data
    # 1. Single-family with missing/zero units: set to 1 unit
    sf_mask = (parcels_with_units["sf_mf"] == "single-family") & (
        parcels_with_units["building_units"].isna() | (parcels_with_units["building_units"] == 0)
    )
    parcels_with_units.loc[sf_mask, "building_units"] = 1

    # 2. Multi-family with missing units: use average of units_min and units_max
    mf_mask = (
        (parcels_with_units["sf_mf"] == "multi-family")
        & (parcels_with_units["building_units"].isna() | (parcels_with_units["building_units"] == 0))
        & (parcels_with_units["units_min"].notna())
        & (parcels_with_units["units_max"].notna())
    )

    parcels_with_units.loc[mf_mask, "building_units"] = (
        (parcels_with_units.loc[mf_mask, "units_min"] + parcels_with_units.loc[mf_mask, "units_max"]) / 2
    ).round()

    # 3. Multi-family with no data: use units_min if available, otherwise 2 as conservative estimate
    mf_no_data_mask = (parcels_with_units["sf_mf"] == "multi-family") & (
        parcels_with_units["building_units"].isna() | (parcels_with_units["building_units"] == 0)
    )

    # Use units_min where available
    mf_with_min = mf_no_data_mask & parcels_with_units["units_min"].notna()
    parcels_with_units.loc[mf_with_min, "building_units"] = parcels_with_units.loc[mf_with_min, "units_min"]

    # Use 2 as absolute fallback where units_min is not available
    mf_no_min = mf_no_data_mask & parcels_with_units["units_min"].isna()
    parcels_with_units.loc[mf_no_min, "building_units"] = 2

    # Report statistics
    matched_count = parcels_with_units["building_units"].notna().sum()
    total_parcels = len(parcels_classified)
    units_with_data = parcels_with_units["building_units"].dropna()
    units_with_data = units_with_data[units_with_data > 0]

    # Count how many were from raw data vs interpolated
    raw_data_count = parcels_with_units["building_units_raw"].notna().sum()
    interpolated_count = matched_count - raw_data_count

    print("\n📊 Building Unit Data Summary:")
    print(f"  Total parcels: {total_parcels:,}")
    print(f"  From building footprint data: {raw_data_count:,} ({raw_data_count / total_parcels * 100:.1f}%)")
    print(
        f"  Interpolated from fallback logic: {interpolated_count:,} ({interpolated_count / total_parcels * 100:.1f}%)"
    )
    print(f"  Total with unit data: {matched_count:,} ({matched_count / total_parcels * 100:.1f}%)")
    if len(units_with_data) > 0:
        print(f"  Total residential units: {units_with_data.sum():,.0f} (mean: {units_with_data.mean():.1f})")

else:
    print("Cannot create parcel-building mapping: no buildings available")
    parcels_with_units = parcels_classified.copy()
    parcels_with_units["building_units"] = None
    parcels_with_units["matched_building_id"] = None
    parcels_with_units["overlap_area_sqm"] = None
    parcels_with_units["building_units_raw"] = None

# Export parcels_with_units as GeoJSON
print("\n💾 Exporting parcels_with_units...")
output_file = outputs_dir / f"parcels_with_units_{timestamp}.geojson"

# Ensure geometry is in WGS84 for export (parcels_classified_utm was in UTM, but parcels_with_units may be in original CRS)
if parcels_with_units.crs != "EPSG:4326":
    parcels_with_units = parcels_with_units.to_crs("EPSG:4326")

parcels_with_units.to_file(output_file, driver="GeoJSON")
print(f"✅ Exported {len(parcels_with_units):,} parcels with units to {output_file.name}")
print(f"📁 File: {output_file}")

print("\n✅ Parcel-building matching complete!")
