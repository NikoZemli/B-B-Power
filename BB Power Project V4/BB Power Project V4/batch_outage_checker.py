import time
import logging
import os
import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# ---------- Setup ----------
def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--headless=new")
    try:
        return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    except Exception as e:
        logging.error(f"Driver setup failed: {e}")
        raise

# ---------- Normalize Provider Names ----------
def normalize_provider_name(provider):
    mapping = {
        "duke energy": "Duke Energy (FL)",
        "oncor electric delivery": "Oncor Electric Delivery",
        "grayson-collin electric coop": "Grayson-Collin Electric Coop",
        "jcp&l (jersey central power & light)": "Jersey Central Power and Light",
        "green mountain power": "Green Mountain Power",
        "pse&g": "Jersey Central Power and Light",
        "peco (exelon)": "PECO",
        "met-ed (firstenergy)": "Met-Ed",
        "atlantic city electric": "Atlantic City Electric",
        "madison gas and electric (mge)": "Madison Gas and Electric",
        "georgia power": "Georgia Power",
        "southern california edison (sce)": "Southern California Edison",
        "pacific gas & electric (pg&e)": "Pacific Gas and Electric",
        "entergy arkansas": "Entergy Arkansas",
        "entergy louisiana": "Entergy Louisiana",
        "dominion energy south carolina": "Dominion Energy South Carolina",
        "dominion energy": "Dominion Energy",
        "evergy": "Evergy",
        "eversource": "Eversource",
        "eversource energy": "Eversource",
        "national grid": "National Grid",
        "nyseg (new york state electric & gas)": "NYSEG",
        "rg&e (rochester gas & electric)": "RG&E",
        "pseg long island": "PSEG Long Island",
        "seattle city light": "Seattle City Light",
        "tacoma power": "Tacoma Power",
        "xcel energy": "Xcel Energy",
        "comed": "ComEd",
        "we energies": "We Energies",
        "public service company of oklahoma (pso)": "Public Service Company of Oklahoma",
        "portland general electric (pge)": "Portland General Electric",
        "rocky mountain power": "Rocky Mountain Power",
        "idaho power": "Idaho Power",
        "cps energy": "CPS Energy",
        "austin energy": "Austin Energy",
        "salt river project (srp)": "Salt River Project",
        "arizona public service (aps)": "Arizona Public Service",
        "indiana michigan power (aep)": "Indiana Michigan Power",
        "central maine power (cmp)": "Central Maine Power",
        "rhode island energy (formerly national grid rhode island)": "Rhode Island Energy",
        "public service company of new mexico (pnm)": "Public Service Company of New Mexico",
        "nv energy": "NV Energy",
        "northwestern energy": "Northwestern Energy",
        "montana-dakota utilities co. (mdu)": "Montana-Dakota Utilities Co.",
        "midamerican energy": "MidAmerican Energy",
        "hawaiian electric": "Hawaiian Electric",
        "baltimore gas and electric": "Baltimore Gas and Electric",
        "florida power & light": "Florida Power and Light"  # ADD THIS FOR YOUR CSV!
    }
    return mapping.get(provider.strip().lower(), provider.strip())


# ---------- Known Scraper URLs ----------
known_scrapers = {
    "Tampa Electric": "https://www.tampaelectric.com/outages/outagemap/",
    "Duke Energy (FL)": "https://outagemap.duke-energy.com/#/current-outages/fl",
    "CenterPoint Energy": "https://tracker.centerpointenergy.com/map/texas",
    "CPS Energy": "https://outagemap.cpsenergy.com/",
    "Austin Energy": "https://outagemap.austinenergy.com/",
    "Oncor Electric Delivery": "https://stormcenter.oncor.com/",
    "Grayson-Collin Electric Coop": "https://outage.ghcoop.com/",
    "Eversource": "https://outagemap.eversource.com/",
    "National Grid": "https://outagemap.ma.nationalgridus.com/",
    "NYSEG": "https://outagemap.nyseg.com/",
    "RG&E": "https://outagemap.rge.com/",
    "PSEG Long Island": "https://outagemap.psegliny.com/",
    "Con Edison": "https://apps.coned.com/stormcenter/external/default.html",
    "Jersey Central Power and Light": "https://outages-nj.firstenergycorp.com/",
    "Atlantic City Electric": "https://www.atlanticcityelectric.com/",
    "Puget Sound Energy": "https://www.pse.com/en/outage/outage-map",
    "Seattle City Light": "https://www.seattle.gov/city-light/outages",
    "Tacoma Power": "https://www.mytpu.org/outages/",
    "Xcel Energy": "https://www.outagemap-xcelenergy.com/outagemap/",
    "Cleco Power": "https://myaccount.cleco.com/Portal/#/PreOutages",
    "Entergy Louisiana": "https://www.etrviewoutage.com/map?state=LA",
    "ComEd": "https://www.comed.com/outages/experiencing-an-outage/outage-map",
    "Met-Ed": "https://outages.firstenergycorp.com/",
    "PECO": "https://www.peco.com/outages/experiencing-an-outage/outage-map",
    "PPL Electric Utilities": "https://omap.prod.pplweb.com/OMAP",
    "We Energies": "https://www.we-energies.com/outagesummary/view/outagegrid",
    "Madison Gas and Electric": "https://mge.smartcmobile.com/Outage/",
    "Georgia Power": "https://outagemap.georgiapower.com/",
    "Southern California Edison": "https://www.sce.com/outages-safety/outage-center/check-outage-status",
    "Pacific Gas and Electric": "https://pgealerts.alerts.pge.com/outage-tools/outage-map/",
    "Dominion Energy": "https://outagemap.dominionenergy.com/external/default.html",
    "Toledo Edison": "https://outages.firstenergycorp.com/",
    "Duke Energy (Ohio)": "https://outagemap.duke-energy.com/#/current-outages/ohky",
    "DTE Energy": "https://outage.dteenergy.com/map/",
    "Consumers Energy": "https://www.consumersenergy.com/Outagemap",
    "Duke Energy (NC)": "https://outagemap.duke-energy.com/#/current-outages/ncsc",
    "Evergy": "https://outagemap.evergy.com/",
    "Ameren Missouri": "https://outagemap.ameren.com/",
    "Salt River Project": "https://myaccount.srpnet.com/power/myaccount/outages",
    "Arizona Public Service": "https://outagemap.aps.com/",
    "Duke Energy (IN)": "https://outagemap.duke-energy.com/#/current-outages/in",
    "Indiana Michigan Power": "https://www.indianamichiganpower.com/outages/",
    "Entergy Arkansas": "https://www.etrviewoutage.com/map?state=AR",
    "Portland General Electric": "https://portlandgeneral.com/outages",
    "Pacific Power": "https://www.pacificpower.net/outages-safety.html",
    "Louisville Gas and Electric": "https://stormcenter.lge-ku.com/",
    "Kentucky Utilities": "https://stormcenter.lge-ku.com/",
    "Central Maine Power": "https://outagemap.cmpco.com/",
    "Public Service Company of Oklahoma": "https://outagemap.psoklahoma.com/",
    "Oklahoma Gas and Electric": "https://kubra.io/stormcenter/views/8fe9d356-96bc-41f1-b353-6720eb408936/",
    "Dominion Energy South Carolina": "https://outagemap.dominionenergy.com/external/default.html",
    "Duke Energy (SC)": "https://outagemap.duke-energy.com/#/current-outages/sc",
    "Middle Tennesee Electric": "https://www.mte.com/ServiceConcerns",
    "Eversource Energy": "https://outagemap.eversource.com/external/default.html",
    "Rhode Island Energy": "https://outagemap.rienergy.com/omap",
    "Public Service Company of New Mexico": "https://www.pnm.com/outages",
    "NV Energy": "https://www.nvenergy.com/outages-and-emergencies/view-current-outages/",
    "Northwestern Energy": "https://retirees-test.northwesternenergy.com/outages/outage-map",
    "Montana-Dakota Utilities Co.": "https://customer.montana-dakota.com/outage-map",
    "Idaho Power": "https://tools.idahopower.com/outage",
    "MidAmerican Energy": "https://www.midamericanenergy.com/OutageWatch/dsk.html",
    "Hawaiian Electric": "https://www.hawaiianelectric.com/safety-and-outages/power-outages/oahu-outage-map",
    "Rocky Mountain Power": "https://www.rockymountainpower.net/outages-safety.html",
    "Baltimore Gas and Electric": "https://outagemap.bge.com/",
    "Green Mountain Power": "https://outagemap.greenmountainpower.com/"
}

# ---------- Scrapers ----------
def generic_scraper(driver, url, provider=None):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(2)
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            driver.switch_to.frame(iframes[-1])
            time.sleep(2)
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage'], g[class*='esri']")
        return any(s.is_displayed() for s in shapes)
    except Exception as e:
        logging.warning(f"Generic scraper failed for {provider or url}: {e}")
        return False
    finally:
        try:
            driver.switch_to.default_content()
        except Exception:
            pass

def scrape_fpl(driver, lat, lon):
    try:
        driver.get("https://www.fplmaps.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        time.sleep(4)
        markers = driver.find_elements(By.CSS_SELECTOR, "g[class*='esri']")
        return any(m.is_displayed() for m in markers)
    except Exception as e:
        logging.warning(f"FPL scraper failed: {e}")
        return False
    finally:
        try:
            driver.switch_to.default_content()
        except Exception:
            pass

def check_outage(driver, provider, lat, lon):
    normalized = normalize_provider_name(provider)
    if normalized == "Florida Power and Light":
        return scrape_fpl(driver, lat, lon), ""
    elif normalized in known_scrapers:
        return generic_scraper(driver, known_scrapers[normalized], provider), ""
    else:
        return None, "No scraper implemented"

# ---------- Run ----------
if __name__ == "__main__":
    logging.basicConfig(filename="scraper_errors.log", level=logging.WARNING)
    driver = setup_driver()

    output_rows = []

    with open("Long_Lat Locations.csv", newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        print("DEBUG CSV HEADERS:", reader.fieldnames)
        if "provider" not in reader.fieldnames or "latitude" not in reader.fieldnames or "longitude" not in reader.fieldnames:
            raise KeyError(f"Expected headers missing. Found: {reader.fieldnames}")

        for row in reader:
            provider = row["provider"].strip()
            try:
                lat = float(row["latitude"])
                lon = float(row["longitude"])
                result, note = check_outage(driver, provider, lat, lon)
                address = f"{row.get('address', '')}, {row.get('city', '')}, {row.get('state', '')}"
                print(f"{provider} | {address} | Outage: {result} | Note: {note}")
                output_rows.append({
                    "Address": address,
                    "Provider": provider,
                    "Latitude": lat,
                    "Longitude": lon,
                    "Outage Detected": result,
                    "Notes": note
                })
            except Exception as e:
                err_msg = f"Error: {e}"
                address = f"{row.get('address', '')}, {row.get('city', '')}, {row.get('state', '')}"
                print(f"{address} | Failed | {err_msg}")
                output_rows.append({
                    "Address": address,
                    "Provider": provider,
                    "Latitude": row.get("latitude"),
                    "Longitude": row.get("longitude"),
                    "Outage Detected": None,
                    "Notes": err_msg
                })

    driver.quit()

    with open("outage_results.csv", mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["Address", "Provider", "Latitude", "Longitude", "Outage Detected", "Notes"])
        writer.writeheader()
        writer.writerows(output_rows)

    print("✅ Results saved to outage_results.csv")


    with open("outage_results.csv", mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=["Provider", "Latitude", "Longitude", "Outage Detected", "Notes"])
        writer.writeheader()
        writer.writerows(output_rows)

    print("✅ Results saved to outage_results.csv")
