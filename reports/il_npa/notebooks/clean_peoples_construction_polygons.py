#!/usr/bin/env python3
"""
Geo Data Cleaning Script to clean and union Peoples Gas construction polygons
Processes geospatial data for Peoples Gas construction polygons

Script Workflow and Transformations Summary
-------------------------------------------

This script prepares and cleans Peoples Gas construction polygons data for further spatial analysis. Below are the key transformations performed:

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

4. **Diagnostics**
   - Reports counts and summaries to provide transparency about any data removed or modified.

The result is a cleaned and filtered Peoples Gas construction polygon dataset, ready for unioning, further geometric processing, and integration with additional city datasets in downstream workflows.
"""

from datetime import datetime
from pathlib import Path

import geopandas as gpd
import pandas as pd

timestamp = datetime.now().strftime("%Y%m%d")
# Set paths
data_dir = Path("../data")
outputs_dir = data_dir / "outputs"
outputs_dir.mkdir(parents=True, exist_ok=True)  # Ensure outputs directory exists
utils_dir = Path("../utils")


# --- Code Cell 5 ---

# Find the most recent Peoples Gas data file
pg_files = sorted(utils_dir.glob("peoplesgas_projects_*.geojson"))
if pg_files:
    pg_file = pg_files[-1]
    print(f"Loading: {pg_file.name}")
    pg_polygons = gpd.read_file(pg_file)
    print(f"Loaded {len(pg_polygons):,} Peoples Gas construction polygons")

    # Rename TYPE to PRP_TYPE
    if "TYPE" in pg_polygons.columns:
        pg_polygons = pg_polygons.rename(columns={"TYPE": "PRP_TYPE"})

    # How many rows have PRP_TYPE == None (i.e., missing values)?
    n_none_prp_type = pg_polygons["PRP_TYPE"].isna().sum()
    print(f"Rows with PRP_TYPE == None: {n_none_prp_type:,}")

    # How many of these rows have a valid (non-null) C_START value?
    if "C_START" in pg_polygons.columns:
        n_none_and_valid_cstart = pg_polygons[pg_polygons["PRP_TYPE"].isna() & pg_polygons["C_START"].notna()].shape[0]
        print(f"Rows with PRP_TYPE == None and valid C_START: {n_none_and_valid_cstart:,}")

    # Drop Contractor column
    pg_polygons = pg_polygons.drop(columns=["Contractor"])

    # Exclude PRP_TYPE == "PI / SI " (with trailing space) or "PI / SI" (without)
    # Also exclude STATUS == 'Street and landscape restoration'
    filtered = pg_polygons[
        (pg_polygons["PRP_TYPE"] != "PI / SI") & (pg_polygons["STATUS"] != "Street and landscape restoration")
    ].copy()
    print(f"Excluded {len(pg_polygons) - len(filtered):,} polygons (PI / SI or Street and landscape restoration)")

    # Convert datetime columns to datetime objects
    datetime_cols = ["C_START", "C_FINISH", "R_START", "R_FINISH"]
    for col in datetime_cols:
        if col in filtered.columns:
            filtered[col] = pd.to_datetime(filtered[col], unit="ms", errors="coerce")

    # Create status_simple column
    filtered["status_simple"] = filtered["C_FINISH"].apply(
        lambda x: "closed" if pd.notnull(x) and x < pd.Timestamp("2025-06-01") else "planned"
    )

    # Show summary stats for C_START grouped by status_simple
    if "C_START" in filtered.columns and "status_simple" in filtered.columns:
        print("\nSummary statistics for C_START by status_simple:")
        stats = filtered.groupby("status_simple")["C_START"].agg(["min", "max", "median", "count"])
        print(stats)

    # Create a new spatial object that contains a union of overlapping polygons by "status_simple"
    from shapely.ops import unary_union

    # Threshold for unioning overlapping polygons: 1 square meter
    # Note: This is applied in UTM Zone 16N (EPSG:32616) which uses meters, so area is in square meters
    OVERLAP_THRESHOLD_SQM = 1.0  # square meters

    def find_connected_components(graph):
        """Find connected components in an undirected graph using DFS.
        Handles isolated nodes (nodes with no edges) as single-node components.
        """
        visited = set()
        components = []

        def dfs(node, component):
            visited.add(node)
            component.append(node)
            # Get neighbors (empty list if node not in graph or has no neighbors)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, component)

        # Process all nodes in the graph
        for node in graph:
            if node not in visited:
                component = []
                dfs(node, component)
                components.append(component)

        return components

    union_by_status = []
    for status, subset in filtered.groupby("status_simple"):
        # Copy to local crs in meters for area thresholding
        subset_m = subset.to_crs(epsg=32616)  # UTM Zone 16N (units: meters, area: square meters)

        # Filter out null/empty geometries before processing
        subset_m = subset_m[subset_m.geometry.notna() & ~subset_m.geometry.is_empty].copy()

        if len(subset_m) == 0:
            print(f"  Warning: No valid geometries for status '{status}', skipping...")
            continue

        print(f"  Processing {len(subset_m):,} polygons for status '{status}' (CRS: {subset_m.crs}, units: meters)")

        # Build overlap graph: find all polygon pairs with overlap > threshold
        # This handles transitive overlaps by finding connected components
        geom_index = subset_m.reset_index()
        spatial_index = geom_index.sindex

        # Build adjacency list for overlap graph
        overlap_graph = {idx: [] for idx in geom_index.index}
        total_overlaps_found = 0
        total_overlaps_above_threshold = 0

        for idx, row in geom_index.iterrows():
            geom = row.geometry

            # Skip if geometry is None or empty
            if geom is None or geom.is_empty:
                continue

            # Use spatial index to find candidate intersections (much faster)
            possible_matches = list(spatial_index.intersection(geom.bounds))

            # Check overlaps with candidate polygons
            for idx2 in possible_matches:
                if idx2 == idx:
                    continue
                other_geom = geom_index.loc[idx2, "geometry"]
                # Skip if other geometry is None or empty
                if other_geom is None or other_geom.is_empty:
                    continue
                if geom.intersects(other_geom):
                    overlap_area = geom.intersection(other_geom).area  # Area in square meters (UTM)
                    total_overlaps_found += 1
                    if overlap_area > OVERLAP_THRESHOLD_SQM:
                        # Add edge to graph (undirected, so add both directions)
                        if idx2 not in overlap_graph[idx]:
                            overlap_graph[idx].append(idx2)
                        if idx not in overlap_graph[idx2]:
                            overlap_graph[idx2].append(idx)
                        total_overlaps_above_threshold += 1

        # Find connected components (handles transitive overlaps)
        components = find_connected_components(overlap_graph)

        # Union all polygons in each connected component
        unions = []
        c_start_mins = []
        c_start_maxs = []
        for component in components:
            if len(component) == 0:
                continue
            # Get geometries for this component
            component_geoms = [geom_index.loc[idx, "geometry"] for idx in component if idx in geom_index.index]
            # Filter out None/empty geometries
            component_geoms = [g for g in component_geoms if g is not None and not g.is_empty]
            if len(component_geoms) > 0:
                unioned_geom = unary_union(component_geoms)
                unions.append(unioned_geom)

                # Get C_START values for this component
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
    # Project back to WGS84
    unioned_polygons = unioned_polygons.to_crs("EPSG:4326")

    print("\nCreated unioned polygons by status_simple (overlap > 1 sq meter):")
    print(unioned_polygons[["status_simple", "geometry"]].head())

    # Write cleaned file to outputs as peoples_polygons_cleaned.geojson
    output_cleaned = outputs_dir / "peoples_polygons_unioned.geojson"
    unioned_polygons.to_file(output_cleaned, driver="GeoJSON")
    print(f"✅ Exported cleaned, unioned polygons to: {output_cleaned.name}")

    # Clip planned polygons by subtracting overlapping areas from closed polygons
    print("\n🔪 Clipping planned polygons by closed polygons...")

    # Split unioned polygons by status
    planned_polygons = unioned_polygons[unioned_polygons["status_simple"] == "planned"].copy()
    closed_polygons = unioned_polygons[unioned_polygons["status_simple"] == "closed"].copy()

    print(f"  Planned polygons: {len(planned_polygons):,}")
    print(f"  Closed polygons: {len(closed_polygons):,}")

    if len(planned_polygons) > 0 and len(closed_polygons) > 0:
        # Convert to UTM for accurate geometric operations
        planned_utm = planned_polygons.to_crs(epsg=32616)
        closed_utm = closed_polygons.to_crs(epsg=32616)

        # Union all closed polygons into a single geometry
        closed_union_geom = unary_union(list(closed_utm.geometry))

        # Clip planned polygons by subtracting closed union
        print("  Subtracting closed polygon areas from planned polygons...")
        planned_utm["geometry"] = planned_utm.geometry.difference(closed_union_geom)

        # Filter out empty geometries after clipping
        planned_utm = planned_utm[~planned_utm.geometry.is_empty].copy()
        print(f"  Planned polygons after clipping: {len(planned_utm):,}")

        # Combine clipped planned polygons with original closed polygons
        clipped_result = pd.concat([planned_utm, closed_utm], ignore_index=True)

        # Project back to WGS84
        clipped_result = clipped_result.to_crs("EPSG:4326")

        # Save to new file
        output_clipped = outputs_dir / "peoples_polygons_unioned_clipped.geojson"
        clipped_result.to_file(output_clipped, driver="GeoJSON")
        print(f"✅ Exported clipped polygons to: {output_clipped.name}")
    elif len(planned_polygons) > 0:
        # Only planned polygons, no clipping needed but save with clipped name for consistency
        output_clipped = outputs_dir / "peoples_polygons_unioned_clipped.geojson"
        planned_polygons.to_file(output_clipped, driver="GeoJSON")
        print(f"✅ No closed polygons to clip from, exported planned polygons to: {output_clipped.name}")
    else:
        print("  No planned polygons to clip")

else:
    print("No Peoples Gas data found. Run: just fetch-data")
    pg_polygons = None
