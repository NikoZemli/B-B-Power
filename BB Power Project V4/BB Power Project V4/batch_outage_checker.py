import pandas as pd
import time
import random
import multiprocessing as mp
from selenium.common.exceptions import WebDriverException
from scrapers import check_outage, setup_driver

# ---------- Process Group ----------
def process_provider_group(group_df):
    driver = None
    output = []

    for _, row in group_df.iterrows():
        location_id = row["location_id"]
        provider = row["provider_name"]
        lat = row["latitude"]
        lon = row["longitude"]

        print(f"[{provider}] Checking location {location_id}")
        try:
            if provider == "Florida Power & Light":
                if driver:
                    try: driver.quit()
                    except: pass
                driver = setup_driver()
                result = check_outage(driver, provider, lat, lon)
                driver.quit()
                driver = None
            else:
                if not driver:
                    driver = setup_driver()
                result = check_outage(driver, provider, lat, lon)

            time.sleep(random.uniform(1.5, 3.5))

        except WebDriverException as e:
            print(f"⚠️ WebDriver error on {location_id}: {e}")
            result = None
        except Exception as e:
            print(f"⚠️ General error on {location_id}: {e}")
            result = None

        output.append({
            "location_id": location_id,
            "provider": provider,
            "latitude": lat,
            "longitude": lon,
            "outage": result
        })

    if driver:
        try: driver.quit()
        except: pass

    return output

# ---------- Main Entry ----------
def main():
    df = pd.read_csv("Long-Lat Locations.csv")

    supported_providers = set([
        "Florida Power & Light", "Tampa Electric", "Duke Energy", "CenterPoint Energy",
        "CPS Energy", "Oncor Electric Delivery", "Eversource", "National Grid", "National Grid NY",
        "NYSEG", "RGE", "PSEG Long Island", "Con Edison", "PSEG NJ", "JCP&L", "PSE", "Seattle City Light",
        "Xcel Energy", "Cleco Power", "Entergy Louisiana", "ComEd", "PECO", "Met-Ed", "Duquesne Light",
        "PPL Electric", "We Energies", "MGE", "Georgia Power", "SCE", "PGE", "Dominion Energy",
        "Duke Energy Ohio", "DTE Energy", "Consumers Energy", "Duke Energy NC", "Evergy MO", "Ameren MO",
        "APS", "SRP", "Arizona Public Service", "Duke Energy IN", "Entergy Arkansas", "EWEB", "PGE OR",
        "Pacific Power OR", "LG&E & KU", "Warren RECC", "CMP", "PSO", "OG&E", "Dominion Energy SC",
        "Duke Energy SC", "MTE", "Eversource CT", "Rhode Island Energy", "PNM", "Northwestern Energy",
        "MDU", "Idaho Power", "MidAmerican Energy", "Evergy KS", "Eversource NH", "Hawaiian Electric",
        "Rocky Mountain Power", "BGE", "Green Mountain Power"
    ])

    filtered_df = df[df["provider_name"].isin(supported_providers)]
    grouped = filtered_df.groupby("provider_name")
    provider_groups = [group for _, group in grouped]

    with mp.Pool(processes=4) as pool:
        results = pool.map(process_provider_group, provider_groups)

    flat_results = [item for sublist in results for item in sublist]
    pd.DataFrame(flat_results).to_csv("outage_status_results.csv", index=False)
    print("✅ All results written to outage_status_results.csv")

if __name__ == "__main__":
    main()

def run_diagnostics():
    df = pd.read_csv("outage_status_results.csv")

    # 1. Show rows where outage value is missing (None/NaN)
    print("\n❗ Locations with missing outage status:")
    print(df[df["outage"].isnull()][["location_id", "provider"]])

    # 2. List unique providers with missing data
    missing_providers = df[df["outage"].isnull()]["provider"].unique()
    print("\n🔎 Providers missing results:")
    for provider in missing_providers:
        print(f" - {provider}")

    # 3. Optionally: show counts
    total = len(df)
    missing = df["outage"].isnull().sum()
    print(f"\n📊 Summary: {missing}/{total} locations returned no outage status ({(missing/total)*100:.1f}%)")

# Add this to the bottom of batch_outage_checker.py
if __name__ == "__main__":
    main()
    run_diagnostics()
