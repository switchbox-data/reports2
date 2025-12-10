#!/usr/bin/env python3
"""
Chicago Building Footprints Downloader
=======================================
Downloads all building footprint polygons from Chicago Data Portal.

Dataset: Building Footprints (current)
Dataset ID: syp8-uezg
API Documentation: https://dev.socrata.com/foundry/data.cityofchicago.org/syp8-uezg

Usage:
    python download_chicago_buildings.py
"""

import json
import os
import time
from pathlib import Path

import requests

# Chicago Data Portal GeoJSON endpoint
API_ENDPOINT = "https://data.cityofchicago.org/resource/syp8-uezg.geojson"


def get_headers():
    """Get request headers with API token if available"""
    headers = {}
    app_token = os.getenv("SOCRATA_APP_TOKEN")
    if app_token:
        headers["X-App-Token"] = app_token
        print(f"✅ Using API token: {app_token[:8]}...")
    else:
        print("⚠️  No SOCRATA_APP_TOKEN found, using unauthenticated requests (rate limited)")
    return headers


def get_total_count(headers):
    """Get total count of building footprints"""
    print("🔍 Getting total count of building footprints...")

    # Use JSON endpoint for count query
    count_endpoint = API_ENDPOINT.replace(".geojson", ".json")
    params = {"$select": "COUNT(*)"}

    response = requests.get(count_endpoint, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if data and len(data) > 0:
        return int(data[0].get("COUNT", 0))
    return 0


def download_buildings_batch(headers, limit, offset):
    """Download a batch of building footprints"""
    params = {
        "$limit": limit,
        "$offset": offset,
        "$order": ":id",
        "$select": "*",  # Explicitly request all fields
    }

    response = requests.get(API_ENDPOINT, headers=headers, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


def main():
    print("=" * 60)
    print("🏢 Chicago Building Footprints Downloader")
    print("=" * 60)
    print()

    try:
        headers = get_headers()

        # Get total count
        total_count = get_total_count(headers)
        print(f"✅ Found {total_count:,} building footprints")

        if total_count == 0:
            print("⚠️  No buildings found!")
            return 1

        # Download in batches
        batch_size = 50000  # Socrata's typical max
        print(f"\n📥 Downloading buildings in batches of {batch_size:,}...")
        all_features = []

        offset = 0
        batch_num = 1

        while offset < total_count:
            total_batches = (total_count + batch_size - 1) // batch_size
            print(f"   Batch {batch_num}/{total_batches}: offset {offset:,}...", end=" ")

            try:
                batch_data = download_buildings_batch(headers, batch_size, offset)

                if batch_data and "features" in batch_data:
                    features = batch_data["features"]
                    all_features.extend(features)
                    print(f"✓ Got {len(features):,} features ({len(all_features):,}/{total_count:,} total)")
                else:
                    print("✗ No features returned")
                    break

                # Be nice to the server
                time.sleep(0.5)

                offset += batch_size
                batch_num += 1

            except Exception as e:
                print(f"✗ Error: {e}")
                break

        # Create final GeoJSON
        geojson = {
            "type": "FeatureCollection",
            "features": all_features,
            "metadata": {
                "source": "Chicago Data Portal",
                "dataset": "Building Footprints (current)",
                "dataset_id": "syp8-uezg",
                "api_endpoint": API_ENDPOINT,
                "downloadDate": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_features": len(all_features),
            },
        }

        # Save to file with date
        download_date = time.strftime("%Y%m%d")
        output_dir = Path(__file__).parent.parent / "data" / "geo_data"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"chicago_buildings_{download_date}.geojson"

        print(f"\n💾 Saving to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(geojson, f, indent=2)

        # Statistics
        print("\n" + "=" * 60)
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"📊 Downloaded: {len(all_features):,} features")
        print(f"📁 Saved to: {output_file}")

        if all_features:
            print("\n📋 Sample Feature Properties:")
            sample_props = all_features[0]["properties"]
            for i, (key, value) in enumerate(sample_props.items()):
                if i >= 10:
                    print(f"   ... and {len(sample_props) - 10} more fields")
                    break
                print(f"   {key}: {value}")

        print("\n🎯 Next Steps:")
        print("   - Open in QGIS: Layer → Add Vector Layer")
        print("   - Use in Python: geopandas.read_file('chicago_buildings.geojson')")
        print("   - View in browser: geojson.io")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
