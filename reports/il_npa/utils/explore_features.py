#!/usr/bin/env python3
"""
Explore what types of features are available in the People's Gas dataset.
Shows unique values for categorical fields to help refine queries.
"""

import json

import requests

FEATURE_SERVER = "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0"


def get_unique_values(field_name):
    """Get unique values for a field using the statistics query."""
    url = f"{FEATURE_SERVER}/query"
    params = {
        "where": "1=1",
        "returnGeometry": "false",
        "outFields": field_name,
        "returnDistinctValues": "true",
        "f": "json",
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if "features" in data:
        values = [f["attributes"][field_name] for f in data["features"]]
        return sorted([v for v in values if v is not None])
    return []


def get_field_stats(field_name):
    """Get statistics for a field."""
    url = f"{FEATURE_SERVER}/query"
    params = {
        "where": "1=1",
        "outStatistics": json.dumps(
            [{"statisticType": "count", "onStatisticField": field_name, "outStatisticFieldName": "count"}]
        ),
        "groupByFieldsForStatistics": field_name,
        "f": "json",
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    if "features" in data:
        stats = {}
        for f in data["features"]:
            value = f["attributes"].get(field_name, "NULL")
            count = f["attributes"].get("count", 0)
            stats[value] = count
        return stats
    return {}


def main():
    print("=" * 70)
    print("🔍 Exploring People's Gas Feature Categories")
    print("=" * 70)
    print()

    # Get service info
    print("📡 Fetching service information...")
    response = requests.get(f"{FEATURE_SERVER}?f=json", timeout=30)
    info = response.json()

    fields = info.get("fields", [])
    print(f"✅ Found {len(fields)} fields\n")

    # Key categorical fields to explore
    categorical_fields = ["TYPE", "STATUS", "Phase", "Contractor", "Shop"]

    for field_name in categorical_fields:
        # Check if field exists
        field_info = next((f for f in fields if f["name"] == field_name), None)
        if not field_info:
            print(f"⚠️  Field '{field_name}' not found")
            continue

        print(f"📊 {field_name} ({field_info['type']})")
        print("-" * 70)

        try:
            # Get statistics with counts
            stats = get_field_stats(field_name)

            if stats:
                total = sum(stats.values())
                print(f"   Total records: {total}\n")

                # Sort by count descending
                for value, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / total * 100) if total > 0 else 0
                    value_display = value if value != "NULL" else "(NULL/Empty)"
                    print(f"   • {value_display:30} {count:4} ({percentage:5.1f}%)")
            else:
                print("   No data available")

            print()

        except Exception as e:
            print(f"   ✗ Error: {e}\n")

    # Show date fields
    print("=" * 70)
    print("📅 DATE FIELDS")
    print("-" * 70)
    date_fields = [f for f in fields if f["type"] == "esriFieldTypeDate"]
    for field in date_fields:
        print(f"   • {field['name']:25} {field.get('alias', '')}")

    print("\n" + "=" * 70)
    print("💡 EXAMPLE QUERIES")
    print("=" * 70)
    print("""
To download only specific categories, modify the download script's query:

1. By STATUS (e.g., only 'In Progress' projects):
   where = "STATUS = 'In Progress'"

2. By Phase (e.g., only 'PH25'):
   where = "Phase = 'PH25'"

3. By multiple conditions (e.g., In Progress AND PH25):
   where = "STATUS = 'In Progress' AND Phase = 'PH25'"

4. By date range (e.g., starting after Jan 1, 2025):
   where = "C_START > timestamp '2025-01-01 00:00:00'"

5. Exclude completed (e.g., not Complete):
   where = "STATUS <> 'Complete'"
""")

    print("=" * 70)


if __name__ == "__main__":
    exit(main())
