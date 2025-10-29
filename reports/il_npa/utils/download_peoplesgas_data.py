#!/usr/bin/env python3
"""
Peoples Gas Pipe Retirement Projects Downloader
================================================
Downloads all construction project polygons with full attributes.

FeatureServer: https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0

Usage:
    python download_peoplesgas_data.py
"""

import json
import time

import requests

# The endpoint you found
FEATURE_SERVER = "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0"


def get_service_info():
    """Get service metadata"""
    print("📡 Fetching service information...")
    params = {"f": "json"}
    response = requests.get(FEATURE_SERVER, params=params)
    response.raise_for_status()
    return response.json()


def get_all_object_ids():
    """Get all object IDs (no pagination limit)"""
    print("🔍 Getting all Object IDs...")
    url = f"{FEATURE_SERVER}/query"
    params = {"where": "1=1", "returnIdsOnly": "true", "f": "json"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("objectIds", [])


def download_features_batch(object_ids):
    """Download features by object IDs"""
    url = f"{FEATURE_SERVER}/query"
    ids_str = ",".join(map(str, object_ids))

    params = {"objectIds": ids_str, "outFields": "*", "returnGeometry": "true", "f": "geojson"}

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def main():
    print("=" * 60)
    print("🗺️  Peoples Gas Pipe Retirement Projects Downloader")
    print("=" * 60)
    print()

    try:
        # Get service info
        info = get_service_info()
        print(f"✅ Service: {info.get('name', 'Unknown')}")
        print(f"   Geometry Type: {info.get('geometryType', 'Unknown')}")
        max_record_count = info.get("maxRecordCount", 1000)
        print(f"   Max Record Count: {max_record_count}")

        # Show available fields
        if "fields" in info:
            print(f"\n📋 Available Fields ({len(info['fields'])}):")
            for field in info["fields"][:10]:  # Show first 10
                print(f"   - {field['name']} ({field['type']})")
            if len(info["fields"]) > 10:
                print(f"   ... and {len(info['fields']) - 10} more")

        # Get all object IDs
        print()
        object_ids = get_all_object_ids()
        total_features = len(object_ids)
        print(f"✅ Found {total_features} features")

        if total_features == 0:
            print("⚠️  No features found!")
            return

        # Download in batches
        print(f"\n📥 Downloading features in batches of {max_record_count}...")
        all_features = []

        for i in range(0, total_features, max_record_count):
            batch_ids = object_ids[i : i + max_record_count]
            batch_num = (i // max_record_count) + 1
            total_batches = (total_features + max_record_count - 1) // max_record_count

            print(f"   Batch {batch_num}/{total_batches}: {len(batch_ids)} features...", end=" ")

            try:
                batch_data = download_features_batch(batch_ids)
                if "features" in batch_data:
                    all_features.extend(batch_data["features"])
                    print(f"✓ ({len(all_features)}/{total_features} total)")
                else:
                    print("✗ No features returned")

                # Be nice to the server
                if i + max_record_count < total_features:
                    time.sleep(0.5)

            except Exception as e:
                print(f"✗ Error: {e}")
                continue

        # Create final GeoJSON
        geojson = {
            "type": "FeatureCollection",
            "features": all_features,
            "metadata": {
                "source": "Peoples Gas Pipe Retirement Program",
                "featureServer": FEATURE_SERVER,
                "downloadDate": time.strftime("%Y-%m-%d %H:%M:%S"),
            },
        }

        # Save to file
        output_file = "peoplesgas_projects.geojson"
        print(f"\n💾 Saving to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(geojson, f, indent=2)

        # Statistics
        print("\n" + "=" * 60)
        print("✅ SUCCESS!")
        print("=" * 60)
        print(f"📊 Downloaded: {len(all_features)} features")
        print(f"📁 Saved to: {output_file}")

        if all_features:
            print("\n📋 Sample Feature Properties:")
            sample_props = all_features[0]["properties"]
            for key, value in list(sample_props.items())[:10]:
                print(f"   {key}: {value}")
            if len(sample_props) > 10:
                print(f"   ... and {len(sample_props) - 10} more fields")

        print("\n🎯 Next Steps:")
        print("   - Open in QGIS: Layer → Add Vector Layer")
        print("   - Use in Python: geopandas.read_file('peoplesgas_projects.geojson')")
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
