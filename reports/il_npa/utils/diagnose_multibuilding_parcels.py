#!/usr/bin/env python3
"""
Diagnostic: how often do multiple buildings intersect a single parcel, and how
much would the reported unit count change if we summed units across all
intersecting buildings instead of taking only the building with the largest
overlap (the current winner-take-all-by-max-overlap rule)?

Read-only. Does not modify any report outputs. Prints to stdout.

Run from reports/il_npa/:
    uv run python utils/diagnose_multibuilding_parcels.py
"""

from __future__ import annotations

import os
import tempfile
import urllib.request
from pathlib import Path

import boto3
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from botocore.exceptions import ClientError, NoCredentialsError
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

S3_BUCKET = "data.sb"
S3_PREFIX = "il_npa/gis/pgl"
OVERLAP_THRESHOLD_SQM = 1.0
UTM_EPSG = 32616

ASSESSOR_LOOKUP_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1xxa47dClvp0rosZhUP1R7790CNXMLSD_0ExrPccR3p0/export?format=csv&gid=770211799"
)


def _repo_root() -> Path:
    for parent in (Path.cwd().resolve(), *Path.cwd().resolve().parents):
        if (parent / ".git").exists() or (parent / ".here").exists():
            return parent
    raise RuntimeError("could not find reports2 repo root")


REPO = _repo_root()
REPORT_DIR = REPO / "reports" / "il_npa"
data_dir = REPORT_DIR / "data"
geo_data_dir = data_dir / "geo_data"
outputs_dir = data_dir / "outputs"


def read_geojson_with_s3_fallback(local_path: Path, s3_bucket: str, s3_key: str) -> gpd.GeoDataFrame:
    local_path = Path(local_path)
    if local_path.exists():
        print(f"  Reading local: {local_path.name}")
        return gpd.read_file(local_path)
    print(f"  Local not found, reading from s3://{s3_bucket}/{s3_key}")
    try:
        s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".geojson", delete=False) as tmp:
            tmp_path = tmp.name
            s3.download_fileobj(s3_bucket, s3_key, tmp)
        gdf = gpd.read_file(tmp_path)
        os.unlink(tmp_path)
        return gdf
    except NoCredentialsError:
        print("  AWS credentials not found.")
        raise
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "Unknown")
        print(f"  S3 ClientError ({code}): {e}")
        raise


def find_latest_dataset(local_glob: str, s3_prefix_stem: str) -> tuple[Path, str]:
    """Mirror match_parcels_buildings.py: prefer a local file in geo_data_dir,
    else list S3 and return a synthetic local path that won't exist so the
    fallback is taken."""
    local_files = sorted(geo_data_dir.glob(local_glob))
    if local_files:
        f = local_files[-1]
        return f, f"{S3_PREFIX}/{f.name}"
    print(f"  No local match for {local_glob}; searching S3...")
    s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-west-2"))
    resp = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=f"{S3_PREFIX}/{s3_prefix_stem}")
    contents = resp.get("Contents", [])
    if not contents:
        raise FileNotFoundError(f"Nothing matching {s3_prefix_stem} in s3://{S3_BUCKET}/{S3_PREFIX}/")
    latest = sorted(contents, key=lambda x: x["LastModified"], reverse=True)[0]
    s3_key = latest["Key"]
    name = s3_key.rsplit("/", 1)[-1]
    return geo_data_dir / name, s3_key


def load_assessor_lookup() -> pd.DataFrame:
    lookup_file = data_dir / "cook_county_assessor_lookup.csv"
    if not lookup_file.exists():
        print(f"  Downloading assessor lookup from Google Sheets to {lookup_file}")
        data_dir.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(ASSESSOR_LOOKUP_URL, lookup_file)
    return pd.read_csv(lookup_file, dtype={"assessor_class": str})


def fmt_pct(num: float, den: float) -> str:
    return f"{num / den:.1%}" if den else "n/a"


def summarize_group(label: str, g: pd.DataFrame) -> None:
    n = len(g)
    if n == 0:
        print(f"\n=== {label}: 0 parcels")
        return
    multi = g[g["n_buildings"] > 1]
    n_multi = len(multi)
    print(f"\n=== {label}: {n:,} parcels")
    print(f"  parcels with >1 intersecting building: {n_multi:,} ({fmt_pct(n_multi, n)})")
    print(
        f"  n_buildings per parcel: "
        f"median={g['n_buildings'].median():.1f}, "
        f"p90={g['n_buildings'].quantile(0.9):.1f}, "
        f"p99={g['n_buildings'].quantile(0.99):.1f}, "
        f"max={int(g['n_buildings'].max())}"
    )
    if n_multi:
        secondary = multi["units_secondary"]
        zero_secondary = (secondary.fillna(0) == 0).sum()
        pos_secondary = (secondary.fillna(0) > 0).sum()
        ge_primary = (secondary.fillna(0) >= multi["units_max"].fillna(0)).sum()
        print(
            f"  Among multi-building parcels:\n"
            f"    units_secondary == 0 (accessory structures): {zero_secondary:,} "
            f"({fmt_pct(zero_secondary, n_multi)})\n"
            f"    units_secondary  > 0: {pos_secondary:,} "
            f"({fmt_pct(pos_secondary, n_multi)})\n"
            f"    units_secondary >= units_max (>=50% discarded): {ge_primary:,} "
            f"({fmt_pct(ge_primary, n_multi)})"
        )
        if pos_secondary:
            pos = multi[secondary.fillna(0) > 0]
            print(
                f"    units_secondary distribution (nonzero only): "
                f"median={pos['units_secondary'].median():.0f}, "
                f"p90={pos['units_secondary'].quantile(0.9):.0f}, "
                f"p99={pos['units_secondary'].quantile(0.99):.0f}, "
                f"max={int(pos['units_secondary'].max())}"
            )
    total_max = g["units_max"].fillna(0).sum()
    total_sum = g["units_sum"].fillna(0).sum()
    delta = total_sum - total_max
    pct = (delta / total_max) if total_max else float("nan")
    print(
        f"  aggregate units (raw, pre-fallback):\n"
        f"    sum(units_max) = {total_max:,.0f}  (this is what the report uses)\n"
        f"    sum(units_sum) = {total_sum:,.0f}  (counterfactual)\n"
        f"    delta          = {delta:+,.0f}  ({pct:+.1%})"
    )


def main() -> None:
    print("=" * 70)
    print("Multi-building parcel diagnostic")
    print("=" * 70)

    # --- load published parcels_with_units for sf_mf / post-fallback columns ---
    pwu_files = sorted(outputs_dir.glob("parcels_with_units_*.geojson"))
    if not pwu_files:
        raise FileNotFoundError(f"No parcels_with_units_*.geojson in {outputs_dir}. Run `just prep-data` first.")
    pwu_file = pwu_files[-1]
    print(f"\nLoading published parcels_with_units: {pwu_file.name}")
    parcels_with_units = gpd.read_file(pwu_file)
    print(f"  {len(parcels_with_units):,} parcels")

    # --- load raw parcels + buildings (same source of truth as the live script) ---
    print("\nLoading raw parcels...")
    parcels_local, parcels_s3 = find_latest_dataset("cook_county_parcels_*.geojson", "cook_county_parcels_")
    parcels = read_geojson_with_s3_fallback(parcels_local, S3_BUCKET, parcels_s3)
    print(f"  {len(parcels):,} parcels")

    print("\nLoading raw buildings...")
    buildings_local, buildings_s3 = find_latest_dataset("chicago_buildings_*.geojson", "chicago_buildings_")
    buildings = read_geojson_with_s3_fallback(buildings_local, S3_BUCKET, buildings_s3)
    print(f"  {len(buildings):,} buildings")

    # --- classify parcels exactly like the match script ---
    assessor_lookup = load_assessor_lookup()
    parcels_classified = parcels.merge(
        assessor_lookup, left_on="assessorbldgclass", right_on="assessor_class", how="left"
    )
    parcels_classified["parcel_idx"] = range(len(parcels_classified))

    # --- UTM for accurate area calc; make_valid for robustness ---
    print("\nReprojecting to UTM 16N and validating geometries...")
    parcels_utm = parcels_classified.to_crs(f"EPSG:{UTM_EPSG}").copy()
    parcels_utm["geometry"] = parcels_utm["geometry"].make_valid()

    buildings_utm = buildings.to_crs(f"EPSG:{UTM_EPSG}").copy()
    if "bldg_id" not in buildings_utm.columns:
        buildings_utm["bldg_id"] = buildings_utm.index.astype(str)
    buildings_utm["geometry"] = buildings_utm["geometry"].make_valid()
    buildings_utm["bldg_area_sqm"] = buildings_utm.geometry.area

    # --- sjoin: one row per (parcel, intersecting building) pair, no fragmentation ---
    print("\nSpatial join (intersects)...")
    pairs = gpd.sjoin(
        parcels_utm[["parcel_idx", "geometry"]],
        buildings_utm[["bldg_id", "no_of_unit", "bldg_area_sqm", "geometry"]],
        predicate="intersects",
        how="inner",
    )
    print(f"  {len(pairs):,} (parcel, building) pairs")

    # --- compute true pairwise overlap area (sjoin result doesn't include it) ---
    print("  computing per-pair overlap area...")
    # attach building geometries back onto pairs (they drop out of sjoin output)
    pairs = pairs.reset_index(drop=True).merge(
        buildings_utm[["bldg_id", "geometry"]].rename(columns={"geometry": "bldg_geom"}),
        on="bldg_id",
        how="left",
    )
    # pairs.geometry is the parcel geometry (left side of sjoin)
    pairs["overlap_area_sqm"] = pairs.geometry.intersection(gpd.GeoSeries(pairs["bldg_geom"], crs=parcels_utm.crs)).area

    before = len(pairs)
    pairs = pairs[pairs["overlap_area_sqm"] > OVERLAP_THRESHOLD_SQM].copy()
    dropped = before - len(pairs)
    print(f"  dropped {dropped:,} pairs with overlap <= {OVERLAP_THRESHOLD_SQM} sqm")
    print(f"  {len(pairs):,} substantive pairs remain")

    pairs["no_of_unit_num"] = pd.to_numeric(pairs["no_of_unit"], errors="coerce")

    # --- per-pair overlap ratio (fraction of the BUILDING inside the parcel) ---
    # A building "belongs" to a parcel only if a majority of its footprint is
    # inside that parcel. Buildings that merely graze a parcel's edge due to
    # survey precision errors will have tiny overlap_ratio here and are
    # correctly attributed to a neighboring parcel via that parcel's own
    # max-overlap winner. Without this filter, naive `units_sum` systematically
    # double-counts neighbors' buildings.
    pairs["overlap_ratio"] = (pairs["overlap_area_sqm"] / pairs["bldg_area_sqm"].replace(0, np.nan)).fillna(0)
    DOMINANT_RATIO = 0.5
    pairs["is_dominant"] = pairs["overlap_ratio"] >= DOMINANT_RATIO
    print(
        f"  flagged {int(pairs['is_dominant'].sum()):,} / {len(pairs):,} pairs "
        f"({fmt_pct(int(pairs['is_dominant'].sum()), len(pairs))}) as dominant "
        f"(building footprint >= {DOMINANT_RATIO:.0%} inside the parcel)"
    )

    # --- per-parcel aggregations ---
    print("\nAggregating per parcel...")
    grp = pairs.groupby("parcel_idx", sort=False)
    dominant_pairs = pairs[pairs["is_dominant"]]
    grp_dom = dominant_pairs.groupby("parcel_idx", sort=False)
    # Note: "n_buildings" here means buildings whose footprint is majority-inside
    # the parcel — the real set of buildings belonging to this parcel.
    # "n_buildings_intersecting" is the raw sjoin count (includes edge-bleed
    # neighbors) and is kept for reference only.
    per_parcel = pd.DataFrame(
        {
            "n_buildings_intersecting": grp.size(),
            "n_buildings": grp_dom.size(),
            "units_sum_all_intersecting": grp["no_of_unit_num"].sum(min_count=1),
            "units_sum": grp_dom["no_of_unit_num"].sum(min_count=1),
        }
    )
    per_parcel["n_buildings"] = per_parcel["n_buildings"].fillna(0).astype(int)
    idx_max = grp["overlap_area_sqm"].idxmax()
    max_rows = pairs.loc[
        idx_max,
        ["parcel_idx", "no_of_unit_num", "bldg_id", "overlap_area_sqm", "bldg_area_sqm"],
    ]
    max_rows = max_rows.rename(
        columns={
            "no_of_unit_num": "units_max",
            "bldg_id": "bldg_id_max",
            "overlap_area_sqm": "max_overlap_sqm",
            "bldg_area_sqm": "max_overlap_bldg_area_sqm",
        }
    ).set_index("parcel_idx")
    per_parcel = per_parcel.join(max_rows)

    # --- alternative winner: largest building by footprint area ---
    idx_largest = grp["bldg_area_sqm"].idxmax()
    largest_rows = pairs.loc[
        idx_largest,
        ["parcel_idx", "no_of_unit_num", "bldg_id", "bldg_area_sqm"],
    ]
    largest_rows = largest_rows.rename(
        columns={
            "no_of_unit_num": "units_largest",
            "bldg_id": "bldg_id_largest",
            "bldg_area_sqm": "largest_bldg_area_sqm",
        }
    ).set_index("parcel_idx")
    per_parcel = per_parcel.join(largest_rows)
    per_parcel["winner_is_largest"] = per_parcel["bldg_id_max"] == per_parcel["bldg_id_largest"]

    per_parcel["units_secondary"] = per_parcel["units_sum"].fillna(0) - per_parcel["units_max"].fillna(0)
    per_parcel = per_parcel.reset_index()

    # --- integrity check vs published building_units_raw ---
    print("\nIntegrity check: does diagnostic units_max match published building_units_raw?")
    pub_cols_needed = {
        "longitude",
        "latitude",
        "sf_mf",
        "building_units_raw",
        "building_units",
        "matched_building_id",
        "assessorbldgclass",
    }
    missing = pub_cols_needed - set(parcels_with_units.columns)
    if missing:
        print(f"  WARN: published output missing columns: {missing}")
    pub = parcels_with_units.copy()
    pub["parcel_idx"] = range(len(pub))
    joined = per_parcel.merge(
        pub[
            [
                "parcel_idx",
                "longitude",
                "latitude",
                "sf_mf",
                "building_units_raw",
                "building_units",
                "matched_building_id",
                "assessorbldgclass",
            ]
        ],
        on="parcel_idx",
        how="left",
    )
    both = joined.dropna(subset=["units_max", "building_units_raw"])
    agree = np.isclose(
        both["units_max"].astype(float),
        both["building_units_raw"].astype(float),
        equal_nan=True,
    ).sum()
    print(
        f"  diagnostic max overlap agrees with published building_units_raw on "
        f"{agree:,} / {len(both):,} non-null rows "
        f"({fmt_pct(agree, len(both))})"
    )
    if agree != len(both):
        disagree_ct = len(both) - agree
        print(f"  WARN: {disagree_ct:,} disagreements — diagnostic not a perfect re-derivation.")
        print("  Proceed with caution; the delta numbers below are indicative, not exact.")

    # --- stratified summary ---
    joined["sf_mf_stratum"] = joined["sf_mf"].fillna("(unclassified/other)")
    print("\n" + "=" * 70)
    print("Summary by classification")
    print("=" * 70)
    for stratum in ["single-family", "multi-family", "(unclassified/other)"]:
        summarize_group(stratum, joined[joined["sf_mf_stratum"] == stratum])
    summarize_group("ALL parcels", joined)

    # --- fallback incidence (addresses mshron comment #2) ---
    print("\n" + "=" * 70)
    print("Fallback incidence in published building_units")
    print("=" * 70)
    for stratum in ["single-family", "multi-family"]:
        g = parcels_with_units[parcels_with_units["sf_mf"] == stratum]
        n = len(g)
        if n == 0:
            continue
        raw = pd.to_numeric(g["building_units_raw"], errors="coerce")
        final = pd.to_numeric(g["building_units"], errors="coerce")
        raw_present = raw.notna() & (raw != 0)
        raw_absent = ~raw_present
        fallback_applied = raw_absent & final.notna()
        no_data = raw_absent & final.isna()
        print(f"\n  {stratum}: {n:,} parcels")
        print(f"    raw data present (no fallback): {raw_present.sum():,} ({fmt_pct(raw_present.sum(), n)})")
        print(f"    fallback applied:                {fallback_applied.sum():,} ({fmt_pct(fallback_applied.sum(), n)})")
        print(f"    no building_units at all:        {no_data.sum():,} ({fmt_pct(no_data.sum(), n)})")

    # --- top divergent MF parcels for satellite spot-check ---
    print("\n" + "=" * 70)
    print("Top 20 multi-family parcels by units_secondary (for satellite spot-check)")
    print("=" * 70)
    mf = joined[joined["sf_mf"] == "multi-family"].copy()
    top = mf.nlargest(20, "units_secondary")
    cols = [
        "parcel_idx",
        "latitude",
        "longitude",
        "n_buildings",
        "units_max",
        "units_sum",
        "units_secondary",
        "units_largest",
        "winner_is_largest",
        "assessorbldgclass",
    ]
    with pd.option_context("display.max_columns", None, "display.width", 200):
        print(top[cols].to_string(index=False))

    # --- scope to the subset that actually lands in the report ---
    # The report only keeps parcels that intersect buffered Peoples Gas "planned"
    # construction polygons AND are residential/mixed-use (where units are summed).
    # Replicate that filter here so we can quantify the undercount IN THE FINAL DATASET.
    print("\n" + "=" * 70)
    print("Scoped analysis: parcels that actually land in the report")
    print("=" * 70)
    pg_file = REPORT_DIR / "data" / "outputs" / "peoples_polygons_unioned.geojson"
    if not pg_file.exists():
        print(f"  SKIP: {pg_file.relative_to(REPO)} not found — run `just prep-data` first.")
    else:
        pg = gpd.read_file(pg_file)
        if "status_simple" in pg.columns:
            pg = pg[pg["status_simple"] == "planned"].copy()
        pg_utm = pg.to_crs(f"EPSG:{UTM_EPSG}")
        pg_utm["geometry"] = pg_utm.geometry.buffer(8).make_valid()
        print(f"  {len(pg_utm):,} planned Peoples Gas polygons (buffered 8m)")

        pg_union = pg_utm.geometry.union_all()
        in_buffered = parcels_utm[parcels_utm.geometry.intersects(pg_union)].copy()
        print(f"  {len(in_buffered):,} parcels intersect buffered PG polygons")

        # join diagnostic per-parcel onto this subset
        scoped_idxs = set(in_buffered["parcel_idx"].tolist())
        scoped = joined[joined["parcel_idx"].isin(scoped_idxs)].copy()

        # also restrict to residential + mixed-use (where building_units gets summed)
        # We rely on assessor_class groupings already joined into parcels_with_units.
        # The report uses parcels_with_units['type'] in ['residential','mixed-use'].
        pub_type = pub.set_index("parcel_idx")["type"] if "type" in pub.columns else None
        if pub_type is not None:
            scoped = scoped.merge(pub_type.rename("type").reset_index(), on="parcel_idx", how="left")
            scoped_res = scoped[scoped["type"].isin(["residential", "mixed-use"])].copy()
            print(
                f"  of those, {len(scoped_res):,} are residential or mixed-use "
                f"(i.e. actually contribute units in the report)"
            )
        else:
            scoped_res = scoped
            print("  (type column missing; skipping res/mixed-use restriction)")

        print("\n  --- Scoped summary by classification ---")
        for stratum in ["single-family", "multi-family", "(unclassified/other)"]:
            g = scoped_res[scoped_res["sf_mf"].fillna("(unclassified/other)") == stratum]
            n = len(g)
            if n == 0:
                continue
            multi_g = g[g["n_buildings"] > 1]
            pos_sec = multi_g[multi_g["units_secondary"].fillna(0) > 0]
            u_max = pd.to_numeric(g["units_max"], errors="coerce").fillna(0).sum()
            u_sum = pd.to_numeric(g["units_sum"], errors="coerce").fillna(0).sum()
            delta = u_sum - u_max
            pct = (delta / u_max * 100) if u_max else float("nan")
            print(f"\n    {stratum}: {n:,} parcels in scope")
            print(f"      multi-building parcels: {len(multi_g):,} ({fmt_pct(len(multi_g), n)})")
            print(f"      multi-bldg w/ units_secondary>0: {len(pos_sec):,} ({fmt_pct(len(pos_sec), n)} of all scoped)")
            print(f"      sum(units_max)  [report]:       {int(u_max):,}")
            print(f"      sum(units_sum)  [counterfactual]:{int(u_sum):,}")
            print(f"      delta: +{int(delta):,} ({pct:+.1f}%)")

    # --- block-level distribution of error (final unit of analysis) ---
    if pg_file.exists() and len(scoped_res):
        print("\n" + "=" * 70)
        print("Block-level distribution of undercount (scoped + residential/mixed-use)")
        print("=" * 70)
        blocks_local = REPORT_DIR / "data" / "geo_data" / "city_blocks" / "pgp_blocks.geojson"
        blocks_s3_key = "il_npa/gis/pgl/pgp_blocks.geojson"
        try:
            blocks = read_geojson_with_s3_fallback(blocks_local, S3_BUCKET, blocks_s3_key)
        except Exception as e:
            print(f"  SKIP: could not load blocks ({e})")
            blocks = None

        if blocks is not None:
            if "blockid10" in blocks.columns and "geoid10" not in blocks.columns:
                blocks = blocks.rename(columns={"blockid10": "geoid10"})
            blocks = blocks[["geoid10", "geometry"]].to_crs(f"EPSG:{UTM_EPSG}")
            blocks["geometry"] = blocks.geometry.make_valid()

            # best-overlap join: each parcel -> one block (max overlap, matches report)
            scoped_parcels_utm = parcels_utm[parcels_utm["parcel_idx"].isin(scoped_res["parcel_idx"])][
                ["parcel_idx", "geometry"]
            ].copy()
            scoped_parcels_utm["geometry"] = scoped_parcels_utm.geometry.make_valid()

            pb = gpd.sjoin(scoped_parcels_utm, blocks, predicate="intersects", how="inner")
            pb = pb.reset_index(drop=True).merge(
                blocks[["geoid10", "geometry"]].rename(columns={"geometry": "b_geom"}),
                on="geoid10",
                how="left",
            )
            pb["overlap_sqm"] = pb.geometry.intersection(gpd.GeoSeries(pb["b_geom"], crs=scoped_parcels_utm.crs)).area
            pb = pb.sort_values("overlap_sqm", ascending=False).drop_duplicates("parcel_idx", keep="first")[
                ["parcel_idx", "geoid10"]
            ]

            # attach units_max / units_sum + sf_mf
            b = scoped_res.merge(pb, on="parcel_idx", how="inner")
            b["units_max_n"] = pd.to_numeric(b["units_max"], errors="coerce").fillna(0)
            b["units_sum_n"] = pd.to_numeric(b["units_sum"], errors="coerce").fillna(0)

            per_block = b.groupby("geoid10").agg(
                n_parcels=("parcel_idx", "size"),
                units_reported=("units_max_n", "sum"),
                units_counterfactual=("units_sum_n", "sum"),
                n_mf=("sf_mf", lambda s: (s == "multi-family").sum()),
            )
            per_block["delta_units"] = per_block["units_counterfactual"] - per_block["units_reported"]
            per_block["delta_pct"] = np.where(
                per_block["units_reported"] > 0,
                per_block["delta_units"] / per_block["units_reported"] * 100,
                np.nan,
            )

            # --- restrict further to the blocks that survive the fully-residential
            #     filter in analysis.qmd (the *actual* final unit of analysis) ---
            final_geojson = sorted(
                (REPORT_DIR / "data" / "outputs").glob("final_peoplesgas_with_buildings_streets_block_all_*.geojson")
            )
            final_ids: set[str] | None = None
            if final_geojson:
                try:
                    import json

                    with open(final_geojson[-1]) as f:
                        gj = json.load(f)
                    # analysis.qmd keeps everything but tags fully_res; reconstruct the
                    # fully_res filter from pg_summary columns
                    fr_ids = []
                    for feat in gj.get("features", []):
                        p = feat.get("properties", {})
                        non_vac = p.get("non_vacant_parcels") or 0
                        sf = p.get("sf_parcels") or 0
                        mf = p.get("mf_parcels") or 0
                        comm = p.get("commercial_parcels") or 0
                        ind = p.get("industrial_parcels") or 0
                        tru = p.get("total_residential_units") or 0
                        res_sum = sf + mf
                        pct_res = res_sum / non_vac if non_vac else 0
                        res_diff = non_vac - res_sum
                        res_filter = (pct_res > 0.9) or (res_diff <= 1)
                        comm_ind = (comm + ind) > 0
                        fully_res = (not comm_ind) and tru > 0 and res_filter
                        if fully_res:
                            fr_ids.append(str(p.get("geoid10")))
                    final_ids = set(fr_ids)
                    print(
                        f"  [final filter] {len(final_ids):,} blocks are fully_res "
                        f"per analysis.qmd rule (from {final_geojson[-1].name})"
                    )
                except Exception as e:
                    print(f"  WARN: could not reconstruct fully_res filter: {e}")
                    final_ids = None
            else:
                print(
                    "  NOTE: no final_peoplesgas_*.geojson yet; run `just render` "
                    "to produce it. Skipping fully_res filter."
                )

            if final_ids is not None:
                per_block = per_block[per_block.index.astype(str).isin(final_ids)]
                print(f"  per_block restricted to {len(per_block):,} fully-residential blocks")

            n_blocks = len(per_block)
            n_clean = (per_block["delta_units"] == 0).sum()
            n_affected = (per_block["delta_units"] > 0).sum()
            print(f"\n  blocks in scope: {n_blocks:,}")
            print(f"    no undercount (delta == 0): {n_clean:,} ({fmt_pct(n_clean, n_blocks)})")
            print(f"    with undercount:            {n_affected:,} ({fmt_pct(n_affected, n_blocks)})")

            print("\n  delta_units per block (affected blocks only):")
            aff = per_block[per_block["delta_units"] > 0]["delta_units"]
            if len(aff):
                print(
                    f"    median={aff.median():.0f}, p75={aff.quantile(0.75):.0f}, "
                    f"p90={aff.quantile(0.9):.0f}, p99={aff.quantile(0.99):.0f}, "
                    f"max={int(aff.max())}"
                )

            print("\n  delta_pct per block (affected blocks only):")
            affp = per_block.loc[per_block["delta_units"] > 0, "delta_pct"].dropna()
            if len(affp):
                print(
                    f"    median={affp.median():.1f}%, p75={affp.quantile(0.75):.1f}%, "
                    f"p90={affp.quantile(0.9):.1f}%, p99={affp.quantile(0.99):.1f}%, "
                    f"max={affp.max():.1f}%"
                )

            # how concentrated is the total undercount?
            total_delta = per_block["delta_units"].sum()
            ranked = per_block.sort_values("delta_units", ascending=False)
            for k in [10, 25, 50, 100]:
                top_k = ranked.head(k)["delta_units"].sum()
                print(
                    f"    top {k:>3d} blocks account for "
                    f"{int(top_k):,} / {int(total_delta):,} units "
                    f"({fmt_pct(top_k, total_delta)}) of the total undercount"
                )

            print("\n  Top 15 blocks by delta_units:")
            top = ranked.head(15).reset_index()
            top["delta_pct"] = top["delta_pct"].round(1)
            with pd.option_context("display.max_columns", None, "display.width", 200):
                print(
                    top[
                        [
                            "geoid10",
                            "n_parcels",
                            "n_mf",
                            "units_reported",
                            "units_counterfactual",
                            "delta_units",
                            "delta_pct",
                        ]
                    ].to_string(index=False)
                )

    # --- hypothesis test: max-overlap vs max-footprint-area ---
    print("\n" + "=" * 70)
    print("Winner rule comparison: max-overlap vs max-footprint-area")
    print("=" * 70)
    multi = joined[joined["n_buildings"] > 1].copy()
    n_multi = len(multi)
    if n_multi:
        same = multi["winner_is_largest"].fillna(False)
        print(f"  multi-building parcels: {n_multi:,}")
        print(f"    winner == largest:  {same.sum():,} ({fmt_pct(same.sum(), n_multi)})")
        print(f"    winner != largest:  {(~same).sum():,} ({fmt_pct((~same).sum(), n_multi)})")
        u_max = pd.to_numeric(multi["units_max"], errors="coerce").fillna(0)
        u_largest = pd.to_numeric(multi["units_largest"], errors="coerce").fillna(0)
        u_sum = pd.to_numeric(multi["units_sum"], errors="coerce").fillna(0)
        print("  aggregate units (multi-building parcels only):")
        print(f"    sum of units_sum     (naive all-buildings): {int(u_sum.sum()):,}")
        print(f"    sum of units_max     (current rule):         {int(u_max.sum()):,}")
        print(f"    sum of units_largest (max-footprint rule):   {int(u_largest.sum()):,}")
        diff = u_largest - u_max
        print(
            f"    delta (largest - max-overlap): total={int(diff.sum()):,}, "
            f"mean={diff.mean():.3f}, median={diff.median():.3f}"
        )
        # when winner != largest, how often does the largest building have MORE units?
        diff_when = multi.loc[~same]
        if len(diff_when):
            ul = pd.to_numeric(diff_when["units_largest"], errors="coerce").fillna(0)
            um = pd.to_numeric(diff_when["units_max"], errors="coerce").fillna(0)
            print(f"  among {len(diff_when):,} 'winner != largest' parcels:")
            print(
                f"    largest has MORE units than max-overlap: "
                f"{(ul > um).sum():,} ({fmt_pct((ul > um).sum(), len(diff_when))})"
            )
            print(
                f"    largest has FEWER units:                "
                f"{(ul < um).sum():,} ({fmt_pct((ul < um).sum(), len(diff_when))})"
            )
            print(
                f"    equal:                                  "
                f"{(ul == um).sum():,} ({fmt_pct((ul == um).sum(), len(diff_when))})"
            )
        # data-quality cut: winner has zero units while sibling has > 0
        zero_winner = multi[(u_max == 0) & (u_sum > 0)]
        print(
            f"  parcels where max-overlap winner reports 0 units "
            f"but other buildings report >0: {len(zero_winner):,} "
            f"({fmt_pct(len(zero_winner), n_multi)})"
        )

    # --- sample maps ---
    print("\n" + "=" * 70)
    print("Generating sample diagnostic maps")
    print("=" * 70)
    maps_dir = REPO / "reports" / "il_npa" / "data" / "outputs" / "diagnostics" / "maps"
    maps_dir.mkdir(parents=True, exist_ok=True)

    # Build a map-sample frame: attach parcel_idx to pairs for quick geometry lookup
    parcels_geom_by_idx = parcels_utm.set_index("parcel_idx")[["geometry"]]

    def render_parcel_map(parcel_idx_val: int, out_path: Path, title: str) -> None:
        try:
            p_geom = parcels_geom_by_idx.loc[parcel_idx_val, "geometry"]
        except KeyError:
            return
        parcel_gdf = gpd.GeoDataFrame({"geometry": [p_geom]}, geometry="geometry", crs=parcels_utm.crs)
        sub_pairs = pairs[pairs["parcel_idx"] == parcel_idx_val].copy()
        if sub_pairs.empty:
            return
        sub_pairs = sub_pairs.merge(
            buildings_utm[["bldg_id", "geometry"]].rename(columns={"geometry": "b_geom"}),
            on="bldg_id",
            how="left",
        )
        bldgs_gdf = gpd.GeoDataFrame(
            sub_pairs[["bldg_id", "no_of_unit_num", "overlap_area_sqm", "bldg_area_sqm", "b_geom"]].rename(
                columns={"b_geom": "geometry"}
            ),
            geometry="geometry",
            crs=parcels_utm.crs,
        )
        # identify winner (max overlap) and largest (max area)
        winner_id = sub_pairs.loc[sub_pairs["overlap_area_sqm"].idxmax(), "bldg_id"]
        largest_id = sub_pairs.loc[sub_pairs["bldg_area_sqm"].idxmax(), "bldg_id"]

        fig, ax = plt.subplots(figsize=(9, 9))
        parcel_gdf.boundary.plot(ax=ax, color="black", linewidth=2, label="parcel")
        # all buildings light grey
        bldgs_gdf.plot(ax=ax, facecolor="lightgrey", edgecolor="grey", linewidth=0.5, alpha=0.6)
        # largest in blue, winner in red (winner drawn last → on top)
        largest_mask = bldgs_gdf["bldg_id"] == largest_id
        winner_mask = bldgs_gdf["bldg_id"] == winner_id
        if largest_mask.any():
            bldgs_gdf[largest_mask].plot(ax=ax, facecolor="none", edgecolor="tab:blue", linewidth=2.5)
        if winner_mask.any():
            bldgs_gdf[winner_mask].plot(ax=ax, facecolor="none", edgecolor="tab:red", linewidth=2.5, linestyle="--")
        # label every building with its no_of_unit
        for _, row in bldgs_gdf.iterrows():
            c = row.geometry.representative_point()
            units_str = f"{int(row['no_of_unit_num'])}" if pd.notna(row["no_of_unit_num"]) else "NA"
            area_str = f"{row['bldg_area_sqm']:.0f}m²"
            ax.annotate(
                f"{units_str} u\n{area_str}",
                (c.x, c.y),
                ha="center",
                va="center",
                fontsize=8,
                color="black",
            )
        legend_handles = [
            Line2D([0], [0], color="black", lw=2, label="parcel"),
            Patch(facecolor="lightgrey", edgecolor="grey", label="building"),
            Line2D([0], [0], color="tab:red", lw=2.5, ls="--", label="winner (max overlap)"),
            Line2D([0], [0], color="tab:blue", lw=2.5, label="largest footprint"),
        ]
        ax.legend(handles=legend_handles, loc="upper left", fontsize=9)
        ax.set_title(title, fontsize=11)
        ax.set_axis_off()
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        print(f"  wrote {out_path.relative_to(REPO)}")

    # category A: pathological (winner_id has 0 units, but siblings have units)
    cat_a = joined[
        (joined["n_buildings"] > 1) & (joined["units_max"].fillna(0) == 0) & (joined["units_sum"].fillna(0) > 0)
    ].nlargest(5, "units_secondary")

    # category B: winner != largest footprint (and multi-building)
    cat_b = joined[(joined["n_buildings"] > 1) & (~joined["winner_is_largest"].fillna(True))].nlargest(
        5, "units_secondary"
    )

    # category C: MF working correctly (single-building parcels, units_max == units_sum, > 0)
    cat_c = joined[
        (joined["sf_mf"] == "multi-family") & (joined["n_buildings"] == 1) & (joined["units_max"].fillna(0) > 0)
    ].head(3)

    # category D: many buildings (n >= 4)
    cat_d = joined[joined["n_buildings"] >= 4].nlargest(5, "n_buildings")

    categories = [
        ("pathological_zero_winner", cat_a, "Pathological: winner has 0 units, siblings have units"),
        ("winner_not_largest", cat_b, "Winner (max overlap) != largest footprint"),
        ("single_building_mf", cat_c, "Multi-family w/ single building (method working)"),
        ("many_buildings", cat_d, "Parcels with 4+ intersecting buildings"),
    ]
    for cat_slug, df_cat, label in categories:
        print(f"\n  [{cat_slug}] candidates: {len(df_cat)}")
        for i, (_, row) in enumerate(df_cat.iterrows(), start=1):
            title = (
                f"{label}\n"
                f"parcel_idx={int(row['parcel_idx'])} "
                f"sf_mf={row.get('sf_mf', 'NA')} "
                f"n_bldgs={int(row['n_buildings'])} "
                f"units_max={row.get('units_max', 'NA')} "
                f"units_sum={row.get('units_sum', 'NA')} "
                f"units_largest={row.get('units_largest', 'NA')}"
            )
            out_path = maps_dir / f"{cat_slug}_{i:02d}_parcel_{int(row['parcel_idx'])}.png"
            render_parcel_map(int(row["parcel_idx"]), out_path, title)

    print(f"\nMaps written to: {maps_dir.relative_to(REPO)}")
    print("\nDone.")


if __name__ == "__main__":
    main()
