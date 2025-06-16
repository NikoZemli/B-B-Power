import time
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
    return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

# ---------- Generic Scraper Template ----------
def generic_scraper(driver, url):
    try:
        driver.get(url)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
        time.sleep(3)
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Specific Scrapers ----------
def scrape_fpl(driver, lat, lon):
    driver.get("https://www.fplmaps.com/")
    time.sleep(5)
    try:
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe")
        driver.switch_to.frame(iframe)
        time.sleep(5)
        markers = driver.find_elements(By.CSS_SELECTOR, "g[class*='esri-graphics-layer']")
        return any(m.is_displayed() for m in markers)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Dispatcher ----------
def check_outage(driver, provider, lat, lon):
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
        "Baltimore gas and Electric": "https://outagemap.bge.com/",
        "Green Mountain Power": "https://outagemap.greenmountainpower.com/"
    }

    if provider == "Florida Power and Light":
        return scrape_fpl(driver, lat, lon)
    elif provider in known_scrapers:
        return generic_scraper(driver, known_scrapers[provider])
    else:
        print(f"[WARN] No scraper implemented for provider: {provider}")
        return None
