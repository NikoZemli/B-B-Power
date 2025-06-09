from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from shapely.geometry import Point, Polygon
import pandas as pd
import time

def check_tallahassee_location_status(df):
    # Filter Tallahassee utility locations
    tlh_df = df[df["provider_name"].str.contains("City of Tallahassee", case=False)]

    # Setup Selenium
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://talgov.com/you/outage")
    time.sleep(15)  # Wait for map and JS to render

    # TODO: Replace this with actual polygon scrape
    sample_polygon = Polygon([
        (-84.3, 30.4),
        (-84.3, 30.5),
        (-84.2, 30.5),
        (-84.2, 30.4)
    ])
    outage_polygons = [sample_polygon]

    driver.quit()

    # Check each location against polygon(s)
    status_dict = {}
    for _, row in tlh_df.iterrows():
        point = Point(row["longitude"], row["latitude"])
        status = "On"
        for poly in outage_polygons:
            if poly.contains(point):
                status = "Out"
                break
        status_dict[row["location_id"]] = status

    return status_dict
