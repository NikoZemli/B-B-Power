from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from shapely.geometry import Point, Polygon
import pandas as pd
import time

def check_duke_location_status(df):
    # Filter only Duke Energy rows
    duke_df = df[df["provider_name"].str.contains("Duke Energy", case=False)]

    # Setup Selenium
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://outagemap.duke-energy.com/#/current-outages/fl")
    time.sleep(15)

    # TODO: extract real polygons from Leaflet/ArcGIS map here
    # TEMP: manually simulate one outage polygon
    sample_polygon = Polygon([
        (-81.1, 28.0),
        (-81.1, 28.1),
        (-81.0, 28.1),
        (-81.0, 28.0)
    ])
    outage_polygons = [sample_polygon]

    driver.quit()

    # Check each location
    status_dict = {}
    for _, row in duke_df.iterrows():
        point = Point(row["longitude"], row["latitude"])
        status = "On"
        for poly in outage_polygons:
            if poly.contains(point):
                status = "Out"
                break
        status_dict[row["location_id"]] = status

    return status_dict
