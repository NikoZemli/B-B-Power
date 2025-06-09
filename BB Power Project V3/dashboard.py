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
outage_statuses = check_arcgis_outages()

# === STEP 3: Update DataFrame ===
status_dict = dict(zip(outage_statuses["location_id"], outage_statuses["arcgis_status"]))
df["power_status"] = df["location_id"].map(status_dict).fillna("Unknown")

# === STEP 4: Create Live Dashboard ===
def create_dashboard(df):
    m = folium.Map(
        location=[39.8283, -98.5795],
        zoom_start=5,
        tiles="CartoDB positron",  # Clean modern map theme
        control_scale=True
    )
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():
        color = "green" if row["power_status"] == "On" else "red"
        popup = (
            f"<div style='font-family: Arial; font-size: 14px;'>"
            f"<b>Address:</b> {row['address']}<br>"
            f"<b>Status:</b> <span style='color:{color}; font-weight: bold'>{row['power_status']}</span><br>"
            f"</div>"
        )
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title_html = f"""
        <div style='position: fixed; top: 10px; left: 50%; transform: translateX(-50%); 
                    background-color: rgba(255, 255, 255, 0.85); color: #1a1a1a; padding: 10px 20px; border-radius: 8px; 
                    font-family: Arial; z-index: 9999; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.15);'>
            <img src='065cb5c9-1400-40d2-8205-87e4159da242.png' alt='Brown & Brown Insurance Logo' style='width: 160px; display: block; margin: 0 auto 8px;'>
            <div style='font-size: 18px; font-weight: bold;'>Brown & Brown Power Dashboard</div>
            <div style='font-size: 12px;'>Updated: {timestamp}</div>
        </div>
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
            updated_status = check_arcgis_outages()
            status_dict = dict(zip(updated_status["location_id"], updated_status["arcgis_status"]))
            df["power_status"] = df["location_id"].map(status_dict).fillna("Unknown")
            create_dashboard(df)
            time.sleep(300)  # Wait 5 minutes
        except Exception as e:
            print("[!] Error during dashboard update:", e)
            time.sleep(300)
