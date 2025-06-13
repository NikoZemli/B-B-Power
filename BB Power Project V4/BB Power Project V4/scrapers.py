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

# ---------- Example Specific Scrapers ----------
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

def scrape_tampa(driver, lat, lon):
    return generic_scraper(driver, "https://www.tampaelectric.com/outages/outagemap/")

def scrape_duke_energy(driver, lat, lon):
    return generic_scraper(driver, "https://outagemap.duke-energy.com/#/current-outages/fl")

def scrape_centerpoint_energy(driver, lat, lon):
    return generic_scraper(driver, "https://tracker.centerpointenergy.com/map/texas")

def scrape_cps_energy(driver, lat, lon):
    return generic_scraper(driver, "https://outagemap.cpsenergy.com/")

def scrape_oncor(driver, lat, lon):
    return generic_scraper(driver, "https://stormcenter.oncor.com/")

def scrape_eversource(driver, lat, lon):
    return generic_scraper(driver, "https://outagemap.eversource.com/")

def scrape_national_grid(driver, lat, lon):
    return generic_scraper(driver, "https://outagemap.ma.nationalgridus.com/")

def scrape_national_grid_ny(driver, lat, lon):
    return generic_scraper(driver, "https://outagemap.ny.nationalgridus.com/")

def scrape_nyseg(driver, lat, lon):
    return generic_scraper(driver, "https://outagemap.nyseg.com/")

def scrape_rge(driver, lat, lon):
    return generic_scraper(driver, "https://outagemap.rge.com/")

def scrape_pseg_long_island(driver, lat, lon):
    return generic_scraper(driver, "https://outagemap.psegliny.com/")

def scrape_con_edison(driver, lat, lon):
    return generic_scraper(driver, "https://apps.coned.com/stormcenter/external/default.html")

# ---------- Dispatcher ----------
def check_outage(driver, provider, lat, lon):
    if provider == "Florida Power & Light":
        return scrape_fpl(driver, lat, lon)
    elif provider == "Tampa Electric":
        return scrape_tampa(driver, lat, lon)
    elif provider == "Duke Energy":
        return scrape_duke_energy(driver, lat, lon)
    elif provider == "CenterPoint Energy":
        return scrape_centerpoint_energy(driver, lat, lon)
    elif provider == "CPS Energy":
        return scrape_cps_energy(driver, lat, lon)
    elif provider == "Oncor Electric Delivery":
        return scrape_oncor(driver, lat, lon)
    elif provider == "Eversource":
        return scrape_eversource(driver, lat, lon)
    elif provider == "National Grid":
        return scrape_national_grid(driver, lat, lon)
    elif provider == "National Grid NY":
        return scrape_national_grid_ny(driver, lat, lon)
    elif provider == "NYSEG":
        return scrape_nyseg(driver, lat, lon)
    elif provider == "RGE":
        return scrape_rge(driver, lat, lon)
    elif provider == "PSEG Long Island":
        return scrape_pseg_long_island(driver, lat, lon)
    elif provider == "Con Edison":
        return scrape_con_edison(driver, lat, lon)
    else:
        return None
