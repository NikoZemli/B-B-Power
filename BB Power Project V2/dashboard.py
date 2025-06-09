import pandas as pd
import folium
from folium.plugins import MarkerCluster
from datetime import datetime
from check_teco import check_teco_outage
from check_fpl import check_fpl_outage
from check_duke import check_duke_outage
from check_duke_locations import check_duke_location_status
from check_tallahassee_locations import check_tallahassee_location_status



# Load location data
df = pd.read_csv("Long-Lat Locations.csv")

# Placeholder: Simulated power status (you'll replace this later with real scraping)
# Set default status
df["power_status"] = "Unknown"

# Check TECO power status once
teco_status = check_teco_outage()

# Apply to all TECO locations
df.loc[df["provider_name"].str.contains("Tampa Electric", case=False), "power_status"] = teco_status

# Florida Power & Light
fpl_status = check_fpl_outage()
df.loc[df["provider_name"].str.contains("Florida Power & Light", case=False), "power_status"] = fpl_status

# Duke Energy
duke_status = check_duke_outage()
df.loc[df["provider_name"].str.contains("Duke Energy", case=False), "power_status"] = duke_status

# Tallahassee (location-specific)
tlh_statuses = check_tallahassee_location_status(df)

for loc_id, status in tlh_statuses.items():
    df.loc[df["location_id"] == loc_id, "power_status"] = status


# Duke Energy (location-specific)
duke_statuses = check_duke_location_status(df)

for loc_id, status in duke_statuses.items():
    df.loc[df["location_id"] == loc_id, "power_status"] = status

# Create map centered on Florida
m = folium.Map(location=[27.994402, -81.760254], zoom_start=7)
marker_cluster = MarkerCluster().add_to(m)

# Add markers
for _, row in df.iterrows():
    color = "green" if row["power_status"] == "On" else "red"
    popup = (
        f"<b>Address:</b> {row['address']}<br>"
        f"<b>Provider:</b> {row['provider_name']}<br>"
        f"<b>Status:</b> {row['power_status']}"
    )
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=popup,
        icon=folium.Icon(color=color)
    ).add_to(marker_cluster)

# Save map with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
title_html = f"""
    <h3 align="center" style="font-size:20px">
        Power Status Dashboard (Updated: {timestamp})
    </h3>
"""
m.get_root().html.add_child(folium.Element(title_html))
m.save("dashboard.html")
print("Map saved to dashboard.html")

import time
import os

while True:
    os.system("py dashboard.py")
    time.sleep(300)  # 5 minutes
