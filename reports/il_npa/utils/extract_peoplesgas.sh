#!/bin/bash
# Peoples Gas Pipe Retirement Data Extraction
# =============================================
# FeatureServer URL: https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0

echo "🎯 Peoples Gas Data Extraction Commands"
echo "========================================="
echo ""

# The endpoint you found
ENDPOINT="https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0"

echo "📍 FeatureServer Endpoint:"
echo "$ENDPOINT"
echo ""

echo "1️⃣ METHOD 1: Using pyesridump (RECOMMENDED - Easiest)"
echo "----------------------------------------"
echo "# Install (one time only):"
echo "pip install pyesridump"
echo ""
echo "# Download all data:"
echo "esri2geojson \"$ENDPOINT\" peoplesgas_projects.geojson"
echo ""

echo "2️⃣ METHOD 2: Using the custom Python script"
echo "----------------------------------------"
echo "python esri_scraper.py \"$ENDPOINT\""
echo ""

echo "3️⃣ METHOD 3: Using ogr2ogr (GDAL)"
echo "----------------------------------------"
echo "ogr2ogr -f GeoJSON peoplesgas_projects.geojson \\"
echo "  \"ESRIJSON:${ENDPOINT}/query?where=1=1&outFields=*&f=json\""
echo ""

echo "4️⃣ METHOD 4: Direct API queries (Manual)"
echo "----------------------------------------"
echo "# Step 1: Get metadata"
echo "curl \"${ENDPOINT}?f=pjson\" > service_info.json"
echo ""
echo "# Step 2: Get all Object IDs"
echo "curl \"${ENDPOINT}/query?where=1=1&returnIdsOnly=true&f=json\" > object_ids.json"
echo ""
echo "# Step 3: Query all features"
echo "curl \"${ENDPOINT}/query?where=1=1&outFields=*&returnGeometry=true&f=geojson\" > peoplesgas_projects.geojson"
echo ""

echo "✅ VERIFICATION"
echo "----------------------------------------"
echo "# View the metadata in browser:"
echo "${ENDPOINT}?f=pjson"
echo ""
echo "# Test query (get first 10 features):"
echo "${ENDPOINT}/query?where=1=1&outFields=*&returnGeometry=true&resultRecordCount=10&f=geojson"
echo ""

echo "📊 EXPECTED DATA"
echo "----------------------------------------"
echo "Based on your screenshot, you should get:"
echo "- Polygon geometries for each construction project"
echo "- Phase (e.g., 'PH25')"
echo "- Contractor (e.g., 'NPL')"
echo "- Status (e.g., 'Preconstruction', 'Installation', 'Restoration', 'Complete')"
echo "- Construction_Start, Construction_End dates"
echo "- Restoration_Start date"
echo "- And any other project attributes"
echo ""

echo "🚀 QUICK START (Copy/Paste)"
echo "----------------------------------------"
cat <<'COMMANDS'
# Install pyesridump
pip install pyesridump

# Download all Peoples Gas project data
esri2geojson "https://services.arcgis.com/7AlGmBBkiOr2Pn8A/arcgis/rest/services/PGL_Projects_PROD/FeatureServer/0" peoplesgas_projects.geojson

# Verify the download
python -c "import json; data=json.load(open('peoplesgas_projects.geojson')); print(f'Downloaded {len(data[\"features\"])} features'); print('Sample:', data['features'][0]['properties'])"
COMMANDS
