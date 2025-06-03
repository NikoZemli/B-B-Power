import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import random

# ==== CONFIG ====
EDGE_DRIVER_PATH = "C:/BB Power Project/drivers/msedgedriver.exe"
CSV_PATH = "C:/BB Power Project/Florida Locations.csv"
OUTPUT_PATH = "C:/BB Power Project/Power Status Results.csv"
HEADLESS = False
WAIT_TIME = 2
RATE_LIMIT_SECONDS = 2

# Logging setup
logging.basicConfig(
    filename="power_status_errors.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s: %(message)s"
)

def find_element_in_all_frames(driver, by, value, wait, max_depth=3, depth=0):
    if depth > max_depth:
        return None
    driver.switch_to.default_content()
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    for frame in frames:
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(frame)
            try:
                el = wait.until(EC.presence_of_element_located((by, value)))
                return el
            except:
                nested = find_element_in_all_frames(driver, by, value, wait, max_depth, depth+1)
                if nested:
                    return nested
        except:
            continue
    driver.switch_to.default_content()
    return None

def check_fpl_status(address):
    options = EdgeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Edge(service=EdgeService(EDGE_DRIVER_PATH), options=options)
    wait = WebDriverWait(driver, WAIT_TIME)

    try:
        print(f"Opening FPL map for: {address}")
        driver.get("https://www.fplmaps.com/")

        time.sleep(1)  # Let it load

        try:
            search_input = wait.until(EC.presence_of_element_located((By.ID, "staddress")))
        except:
            search_input = find_element_in_all_frames(driver, By.XPATH, "//input[@id='staddress']", wait)

        if not search_input:
            raise Exception("Search input not found.")

        search_input.clear()
        search_input.send_keys(address)
        search_input.send_keys(Keys.RETURN)

        popup_text = ""
        try:
            wait.until(EC.any_of(
                EC.presence_of_element_located((By.CLASS_NAME, "incident-popup")),
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "No outages")
            ))
            popups = driver.find_elements(By.CLASS_NAME, "incident-popup")
            if popups:
                popup_text = popups[0].text
        except:
            popup_text = ""

        if popup_text:
            if "No outages" in popup_text or "No reported outages" in popup_text:
                return "Power ON ✅"
            elif "affected" in popup_text or "outage" in popup_text.lower():
                return f"Power OFF ❌ - {popup_text}"
            else:
                return f"Unclear status: {popup_text}"
        else:
            return "No popup — likely Power ON ✅"

    except Exception as e:
        logging.error(f"Error for address '{address}': {str(e)}")
        return f"Error: {str(e)}"
    finally:
        driver.quit()
        time.sleep(1)

def validate_csv_columns(df):
    required = {"Address", "City", "State", "ZIP Code"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing columns: {', '.join(required - set(df.columns))}")

def run_batch_check():
    print("→ Starting batch check...")

    try:
        df = pd.read_csv(CSV_PATH, quotechar='"', on_bad_lines='skip')[['Address', 'City', 'State', 'ZIP Code']]
        print(f"→ Loaded {len(df)} rows.")
        df['State'] = df['State'].replace({'Florida': 'FL'})
    except Exception as e:
        print(f"❌ CSV load/clean error: {e}")
        return

    try:
        validate_csv_columns(df)
    except ValueError as ve:
        print(f"❌ {ve}")
        return

    results = []
    for i, row in df.iterrows():
        address = f"{row['Address']}, {row['City']}, {row['State']} {row['ZIP Code']}"
        print(f"[{i + 1}] Checking: {address}")
        status = check_fpl_status(address)
        print(f" → {status}")
        results.append(status)
        time.sleep(random.uniform(0.6, 1.2))

    df["Power Status"] = results
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✅ Done! Results saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    print("→ Script started.")
    run_batch_check()
