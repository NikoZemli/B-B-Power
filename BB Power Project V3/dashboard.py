import pandas as pd
import folium
from folium.plugins import MarkerCluster
from datetime import datetime
import time
import os
import webbrowser
from check_arcgis_outages import check_arcgis_outages  # Live status checker

# === STEP 1: Load CSV ===
df = pd.read_csv("Long-Lat Locations.csv")

# === STEP 2: Get live outage status ===
outage_statuses = check_arcgis_outages(df)

# === STEP 3: Update DataFrame ===
status_dict = dict(zip(outage_statuses["location_id"], outage_statuses["arcgis_status"]))
df["power_status"] = df["location_id"].map(status_dict).fillna("Unknown")

# === STEP 4: Create Live Dashboard ===
def create_dashboard(df):
    m = folium.Map(location=[27.994402, -81.760254], zoom_start=7, control_scale=True)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        color = "green" if row["power_status"] == "On" else "red"
        popup = (
            f"<div style='font-family: Arial; font-size: 14px;'>"
            f"<b>Address:</b> {row['address']}<br>"
            f"<b>Status:</b> <span style='color:{color}; font-weight: bold'>{row['power_status']}</span><br>"
            f"<b>Coordinates:</b> ({row['latitude']}, {row['longitude']})"
            f"</div>"
        )
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title_html = f"""
        <h2 style='text-align:center; color:#2E7EBB; font-family: Arial;'>Power Status Dashboard</h2>
        <h4 style='text-align:center; font-family: Arial;'>Updated: {timestamp}</h4>
    """
    m.get_root().html.add_child(folium.Element(title_html))
    m.save("dashboard.html")
    print("[✔] Dashboard updated at", timestamp)
    webbrowser.open("dashboard.html")

# === STEP 5: Auto-update every 5 minutes ===
if __name__ == "__main__":
    while True:
        try:
            # Refresh statuses each cycle
            updated_status = check_arcgis_outages(df)
            status_dict = dict(zip(updated_status["location_id"], updated_status["arcgis_status"]))
            df["power_status"] = df["location_id"].map(status_dict).fillna("Unknown")
            create_dashboard(df)
            time.sleep(300)  # Wait 5 minutes
        except Exception as e:
            print("[!] Error during dashboard update:", e)
            time.sleep(300)
