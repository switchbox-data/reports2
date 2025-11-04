# How to download PGL Construction Map Geodata

## FeatureServer URL:
```
https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0
```

---

## ⚡ FASTEST WAY TO GET THE DATA (3 Options)

### Option 1: pyesridump (EASIEST - Recommended)
```bash
# Install once
pip install pyesridump

# Download everything
esri2geojson "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0" peoplesgas_projects.geojson
```

**Done!** Open `peoplesgas_projects.geojson` in QGIS or any GIS software.

---

### Option 2: Custom Python Script (Most Control)
```bash
# Run the provided script
python download_peoplesgas_data.py
```

This script will:
- Show you service metadata
- Display available fields
- Download all features with progress
- Save to `peoplesgas_projects.geojson`

---

### Option 3: Direct Curl (No Installation)
```bash
# Download all data in one command
curl "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&f=geojson" -o peoplesgas_projects.geojson
```

⚠️ **Note:** This might hit record limits. Use Option 1 or 2 for best results.

---

## 🔍 VERIFY THE ENDPOINT FIRST

Before downloading, check what's available:

**View metadata in browser:**
```
https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0?f=pjson
```

**Test query (first 10 features):**
```
https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0/query?where=1=1&outFields=*&returnGeometry=true&resultRecordCount=10&f=geojson
```

---

## 📊 WHAT YOU'LL GET

Based on your screenshot, each feature will have:

```json
{
  "type": "Feature",
  "properties": {
    "Phase": "PH25",
    "Contractor": "NPL",
    "Status": "Preconstruction",
    "Construction_Start": "9/25/2030",
    "Construction_End": "9/23/2031",
    "Restoration_Start": "3/16/2031",
    ... more fields
  },
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[-87.xxx, 41.xxx], ...]]
  }
}
```

---

## 🚀 COMPLETE WORKFLOW

```bash
# Step 1: Install pyesridump (one time only)
pip install pyesridump

# Step 2: Download all data
esri2geojson "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0" peoplesgas_projects.geojson

# Step 3: Verify
python -c "import json; d=json.load(open('peoplesgas_projects.geojson')); print(f'Features: {len(d[\"features\"])}'); print('Sample:', d['features'][0]['properties'])"

# Step 4: Use it!
# - Open in QGIS
# - Load with geopandas
# - Convert to shapefile
# - Analyze in Python
```

---

## 🛠️ PROVIDED FILES

- **download_peoplesgas_data.py** - Ready-to-run Python script
- **extract_peoplesgas.sh** - All extraction commands
- **esri_scraper.py** - Generic ESRI downloader (works with any endpoint)

---

## 💡 ADVANCED QUERIES

### Filter by Status
```bash
# Only get projects in "Preconstruction" status
esri2geojson "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0" preconstruction.geojson --where "Status='Preconstruction'"
```

### Filter by Phase
```bash
# Only get PH25 projects
curl "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0/query?where=Phase%3D%27PH25%27&outFields=*&f=geojson" -o ph25_projects.geojson
```

### Filter by Date Range
```bash
# Projects starting after Jan 1, 2025
curl "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0/query?where=Construction_Start%3E%27Jan+1%2C+2025%27&outFields=*&f=geojson" -o future_projects.geojson
```

---

## 📈 ANALYZE THE DATA

Once downloaded, you can:

```python
import geopandas as gpd
import matplotlib.pyplot as plt

# Load data
gdf = gpd.read_file('peoplesgas_projects.geojson')

# Summary statistics
print(f"Total projects: {len(gdf)}")
print("\nProjects by Status:")
print(gdf['Status'].value_counts())
print("\nProjects by Phase:")
print(gdf['Phase'].value_counts())

# Create a map
gdf.plot(column='Status', legend=True, figsize=(12, 12))
plt.title('Peoples Gas Construction Projects by Status')
plt.show()

# Export to different formats
gdf.to_file('peoplesgas_projects.shp')  # Shapefile
gdf.to_file('peoplesgas_projects.gpkg', driver='GPKG')  # GeoPackage
```

---

## ✅ VERIFICATION CHECKLIST

After downloading:
- [ ] File exists and is not empty
- [ ] GeoJSON is valid (test with geojson.io)
- [ ] Features match what you see on the map
- [ ] All expected fields are present
- [ ] Geometries are polygons
- [ ] Coordinate system is correct (usually EPSG:4326 or EPSG:3857)

---

## 🎯 RECOMMENDED: Start Here

```bash
# This is all you need!
pip install pyesridump
esri2geojson "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0" peoplesgas_projects.geojson
```

**That's it!** You now have all the Peoples Gas pipe retirement project polygons with complete attribute data.
