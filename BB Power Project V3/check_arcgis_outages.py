import requests
import pandas as pd
from shapely.geometry import Point, Polygon

def check_arcgis_outages():
    # Load locations
    df = pd.read_csv("Long-Lat Locations.csv")

    # Query ArcGIS live outage polygons
    url = "https://services.arcgis.com/BLN4oKB0N1YSgvY8/arcgis/rest/services/Power_Outages_(View)/FeatureServer/1/query"
    params = {
        "where": "1=1",
        "outFields": "*",
        "outSR": "4326",
        "f": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Parse polygons
        polygons = []
        for feature in data["features"]:
            geom = feature.get("geometry", {})
            if "rings" in geom:
                for ring in geom["rings"]:
                    polygons.append(Polygon(ring))

    except Exception as e:
        print(f"[!] Failed to load ArcGIS data: {e}")
        polygons = []

    # Match location status
    status_list = []
    for _, row in df.iterrows():
        point = Point(row["longitude"], row["latitude"])
        status = "On"
        for poly in polygons:
            if poly.contains(point):
                status = "Out"
                break
        status_list.append({"location_id": row["location_id"], "arcgis_status": status})

    return pd.DataFrame(status_list)
