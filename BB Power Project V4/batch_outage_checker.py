import pandas as pd
import time
import random
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
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    return driver

# ---------- FPL Scraper ----------
def scrape_fpl(driver, latitude, longitude):
    driver.get("https://www.fplmaps.com/")
    time.sleep(5)
    try:
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe")
        driver.switch_to.frame(iframe)
    except:
        return False
    time.sleep(5)
    try:
        markers = driver.find_elements(By.CSS_SELECTOR, "g[class*='esri-graphics-layer']")
        return any(m.is_displayed() for m in markers)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Tampa Electric Scraper ----------
def scrape_tampa(driver, latitude, longitude):
    driver.get("https://www.tampaelectric.com/outages/outagemap/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Duke Energy Scraper ----------

def scrape_duke_energy(driver, latitude, longitude):
    driver.get("https://outagemap.duke-energy.com/#/current-outages/fl")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- CenterPoint Energy Scraper ----------

def scrape_centerpoint_energy(driver, latitude, longitude):
    driver.get("https://tracker.centerpointenergy.com/map/texas?_ga=2.233136665.642928028.1749747544-2138853262.1749747544&location=eyJ2aWV3Ijp7ImxhdGl0dWRlIjoyOS41OTYsImxvbmdpdHVkZSI6LTk1LjUzNCwiem9vbSI6OSwiZXZlbnRJZCI6bnVsbH19")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- CPS Energy Scraper ----------

def scrape_cps_energy(driver, latitude, longitude):
    driver.get("https://outagemap.cpsenergy.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Oncor Scraper ----------

def scrape_oncor(driver, latitude, longitude):
    driver.get("https://stormcenter.oncor.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Eversource Scraper ----------

def scrape_eversource(driver, latitude, longitude):
    driver.get("https://outagemap.eversource.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- National Grid Scraper ----------

def scrape_national_grid(driver, latitude, longitude):
    driver.get("https://outagemap.ma.nationalgridus.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- National Grid NY Scraper ---------

def scrape_national_grid_ny(driver, latitude, longitude):
    driver.get("https://outagemap.ny.nationalgridus.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- NYSEG Scraper ----------

def scrape_nyseg(driver, latitude, longitude):
    driver.get("https://outagemap.nyseg.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- RGE Scraper ----------

def scrape_rge(driver, latitude, longitude):
    driver.get("https://outagemap.rge.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- PSEG Long Island Scraper ----------

def scrape_pseg_long_island(driver, latitude, longitude):
    driver.get("https://outagemap.psegliny.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Con Edison Scraper ----------

def scrape_con_edison(driver, latitude, longitude):
    driver.get("https://apps.coned.com/stormcenter/external/default.html")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- PSEG NJ Scraper ----------

def scrape_pseg_nj(driver, latitude, longitude):
    driver.get("https://outagecenter.pseg.com/external/default.html/")  # PSE&G's NJ outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- JCP&L Scraper ----------
def scrape_jcpl(driver, latitude, longitude):
    driver.get("https://outages-nj.firstenergycorp.com/")  # JCP&L StormCenter map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- PSE Scraper ----------
def scrape_pse(driver, latitude, longitude):
    driver.get("https://www.pse.com/en/outage/outage-map")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Seattle City Light Scraper ----------
def scrape_seattle_city_light(driver, latitude, longitude):
    driver.get("https://www.seattle.gov/city-light/outages")  # SCL outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False
    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Xcel Energy Scraper ----------
def scrape_xcel_energy(driver, latitude, longitude):
    driver.get("https://www.outagemap-xcelenergy.com/outagemap/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Cleco Power Scraper ----------
def scrape_cleco_power(driver, latitude, longitude):
    driver.get("https://myaccount.cleco.com/Portal/#/PreOutages")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Entergy Louisiana Scraper ----------
def scrape_entergy_la(driver, latitude, longitude):
    driver.get("https://www.etrviewoutage.com/map?state=LA&_gl=1*4iczh2*_gcl_au*MTM2MjQyNzQ3Mi4xNzQ5NzU0Mjc2*_ga*NDI0OTMxNjgzLjE3NDk3NTQyNzY.*_ga_HK6YSZ6LT0*czE3NDk3NTQyNzYkbzEkZzAkdDE3NDk3NTQyNzYkajYwJGwwJGgw")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- ComEd Scraper ----------
def scrape_comed(driver, latitude, longitude):
    driver.get("https://www.comed.com/outages/experiencing-an-outage/outage-map")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- PSEG NJ Scraper ----------
def scrape_peco(driver, latitude, longitude):
    driver.get("https://www.peco.com/outages/experiencing-an-outage/outage-map?os=i&ref=app")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Met-Ed Scraper ----------
def scrape_met_ed(driver, latitude, longitude):
    driver.get("https://outages-pa.firstenergycorp.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='esri-graphics-layer'], g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Duquesne Light Scraper ----------
def scrape_duquesne_light(driver, latitude, longitude):
    driver.get("https://www.duquesnelight.com/outages-safety/current-outages")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- PPL Electric Scraper ----------
def scrape_ppl_electric(driver, latitude, longitude):
    driver.get("https://omap.prod.pplweb.com/OMAP")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- We Energies Scraper ----------
def scrape_we_energies(driver, latitude, longitude):
    driver.get("https://www.we-energies.com/outagesummary/view/outagegrid")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- MGE Scraper ----------
def scrape_mge(driver, latitude, longitude):
    driver.get("https://mge.smartcmobile.com/Outage/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Georgia Power Scraper ----------
def scrape_georgia_power(driver, latitude, longitude):
    driver.get("https://outagemap.georgiapower.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- SCE Scraper ----------
def scrape_sce(driver, latitude, longitude):
    driver.get("https://www.sce.com/outages-safety/outage-center/check-outage-status")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- PGE Scraper ----------
def scrape_pge(driver, latitude, longitude):
    driver.get("https://pgealerts.alerts.pge.com/outage-tools/outage-map/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Dominion Energy Scraper ----------
def scrape_dominion_energy(driver, latitude, longitude):
    driver.get("https://outagemap.dominionenergy.com/external/default.html")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Duke Energy Ohio Scraper ----------
def scrape_duke_energy_ohio(driver, latitude, longitude):
    driver.get("https://outagemap.duke-energy.com/#/current-outages/ohky")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- DTE Energy Scraper ----------
def scrape_dte_energy(driver, latitude, longitude):
    driver.get("https://outage.dteenergy.com/map/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Consumers Energy Scraper ----------
def scrape_consumers_energy(driver, latitude, longitude):
    driver.get("https://www.consumersenergy.com/Outagemap")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Duke Energy NC Scraper ----------
def scrape_duke_energy_nc(driver, latitude, longitude):
    driver.get("https://outagemap.duke-energy.com/#/current-outages/ncsc")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Evergy MO Scraper ----------
def scrape_evergy_mo(driver, latitude, longitude):
    driver.get("https://outagemap.evergy.com/?_ga=2.204464848.1744668144.1749756981-1360526181.1749756980")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Ameren MO Scraper ----------
def scrape_ameren_mo(driver, latitude, longitude):
    driver.get("https://outagemap.aps.com/outageviewer/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- APS Scraper ----------
def scrape_aps(driver, latitude, longitude):
    driver.get("https://outagemap.aps.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- SRP Scraper ----------
def scrape_srp(driver, latitude, longitude):
    driver.get("https://myaccount.srpnet.com/power/myaccount/outages")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Duke Energy IN Scraper ----------
def scrape_duke_energy_in(driver, latitude, longitude):
    driver.get("https://outagemap.duke-energy.com/#/current-outages/in")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Entergy Arkansas Scraper ----------
def scrape_entergy_ar(driver, latitude, longitude):
    driver.get("https://www.etrviewoutage.com/map?state=AR&_gl=1*wtoivm*_gcl_au*MTg3ODg4OTE1OS4xNzQ5NzU3Nzg2*_ga*MTYyNDQ4NjkzMy4xNzQ5NzU3Nzg2*_ga_DYMNYBY5CD*czE3NDk3NTc3ODUkbzEkZzAkdDE3NDk3NTc3ODYkajU5JGwwJGgw*_ga_8YKL3FLBBC*czE3NDk3NTc3ODYkbzEkZzAkdDE3NDk3NTc3ODYkajYwJGwwJGgw&_ga=2.114924999.1117793517.1749757786-1624486933.1749757786")  # Entergy Arkansas StormCenter
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- EWEB Scraper ----------
def scrape_eweb(driver, latitude, longitude):
    driver.get("https://www.eweb.org/outages-and-safety/power-outages/power-outage-map")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- PGE OR Scraper ----------
def scrape_pge_or(driver, latitude, longitude):
    driver.get("https://portlandgeneral.com/outages")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Pacific Power OR Scraper ----------
def scrape_pacific_power_or(driver, latitude, longitude):
    driver.get("https://www.pacificpower.net/outages-safety.html")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- LG&E & KU Scraper ----------
def scrape_lge(driver, latitude, longitude):
    driver.get("https://stormcenter.lge-ku.com/")  # LG&E & KU map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Warren RECC Scraper ----------
def scrape_warren_rec(driver, latitude, longitude):
    driver.get("https://warrenec.outagemap.coop/")  # WRRECC StormCenter map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

#---------- CMP Scraper ----------
def scrape_cmp(driver, latitude, longitude):
    driver.get("https://outagemap.cmpco.com/")  # CMP StormCenter outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- PSO Scraper ----------
def scrape_pso(driver, latitude, longitude):
    driver.get("https://outagemap.psoklahoma.com/?_gl=1*22l8lq*_ga*MjExMDE0NzMyNS4xNzQ5NzU4OTc2*_ga_8TY18DQCWB*czE3NDk3NTg5NzUkbzEkZzAkdDE3NDk3NTg5NzUkajYwJGwwJGgw*_gcl_au*NDMyNzA4Mjk4LjE3NDk3NTg5NzY.*_ga_NFK8JY5JH3*czE3NDk3NTg5NzUkbzEkZzAkdDE3NDk3NTg5NzUkajYwJGwwJGgw")  # PSO outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- OG&E Scraper ----------
def scrape_oge(driver, latitude, longitude):
    driver.get("https://kubra.io/stormcenter/views/8fe9d356-96bc-41f1-b353-6720eb408936/")  # OG&E outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Dominion Energy SC Scraper ----------
def scrape_dominion_energy_sc(driver, latitude, longitude):
    driver.get("https://outagemap.dominionenergy.com/external/default.html")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Duke Energy SC Scraper ----------
def scrape_duke_energy_sc(driver, latitude, longitude):
    driver.get("https://outagemaps.duke-energy.com/#/current-outages/sc")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- MTE Scraper ----------
def scrape_mtemc(driver, latitude, longitude):
    driver.get("https://www.mte.com/ServiceConcerns")  # MTE StormCenter outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Eversource CT Scraper ----------
def scrape_eversource_ct(driver, latitude, longitude):
    driver.get("https://outagemap.eversource.com/external/default.html")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Rhode Island Energy Scraper ----------
def scrape_rhode_island_energy(driver, latitude, longitude):
    driver.get("https://outagemap.rienergy.com/omap")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- PNM Scraper ----------
def scrape_pnm(driver, latitude, longitude):
    driver.get("https://www.nvenergy.com/outages-and-emergencies/view-current-outages/")  # PNM StormCenter outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Northwestern Energy Scraper ----------
def scrape_northwestern_energy(driver, latitude, longitude):
    driver.get("https://retirees-test.northwesternenergy.com/outages/outage-map")  # NW Energy StormCenter map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- MDU Scraper ----------
def scrape_mdu(driver, latitude, longitude):
    driver.get("https://customer.montana-dakota.com/outage-map")  # MDU StormCenter outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Idaho Power Scraper ----------
def scrape_idaho_power(driver, latitude, longitude):
    driver.get("https://tools.idahopower.com/outage")  # Idaho Power outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- MidAmerican Energy Scraper ----------
def scrape_midamerican_energy(driver, latitude, longitude):
    driver.get("https://www.midamericanenergy.com/OutageWatch/dsk.html")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Evergy KS Scraper ----------
def scrape_evergy_ks(driver, latitude, longitude):
    driver.get("https://outagemap.evergy.com/?_ga=2.208438866.1744668144.1749756981-1360526181.1749756980")  # Covers both KS and MO
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Eversource NH Scraper ----------
def scrape_eversource_nh(driver, latitude, longitude):
    driver.get("https://outagemap.eversource.com/external/default.html")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Hawaiian Electric Scraper ----------
def scrape_hawaiian_electric(driver, latitude, longitude):
    driver.get("https://www.hawaiianelectric.com/safety-and-outages/power-outages/oahu-outage-map")  # Hawaiian Electric StormCenter map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Rocky Mountain Power Scraper ----------
def scrape_rocky_mountain_power(driver, latitude, longitude):
    driver.get("https://www.rockymountainpower.net/outages-safety.html")  # Rocky Mountain Power outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- BGE Scraper ----------
def scrape_bge(driver, latitude, longitude):
    driver.get("https://outagemap.bge.com/")  # BGE outage map
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()

# ---------- Green Mountain Power Scraper ----------
def scrape_green_mountain_power(driver, latitude, longitude):
    driver.get("https://outagemap.greenmountainpower.com/")
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "iframe"))
        )
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
    except:
        return False

    time.sleep(3)
    try:
        shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage']")
        return any(s.is_displayed() for s in shapes)
    except:
        return False
    finally:
        driver.switch_to.default_content()



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
    elif provider == "PSEG NJ":
        return scrape_pseg_nj(driver, lat, lon)
    elif provider == "JCP&L":
        return scrape_jcpl(driver, lat, lon)
    elif provider == "PSE":
        return scrape_pse(driver, lat, lon)
    elif provider == "Seattle City Light":
        return scrape_seattle_city_light(driver, lat, lon)
    elif provider == "Xcel Energy":
        return scrape_xcel_energy(driver, lat, lon)
    elif provider == "Cleco Power":
        return scrape_cleco_power(driver, lat, lon)
    elif provider == "Entergy Louisiana":
        return scrape_entergy_la(driver, lat, lon)
    elif provider == "ComEd":
        return scrape_comed(driver, lat, lon)
    elif provider == "PECO":
        return scrape_peco(driver, lat, lon)
    elif provider == "Met-Ed":
        return scrape_met_ed(driver, lat, lon)
    elif provider == "Duquesne Light":
        return scrape_duquesne_light(driver, lat, lon)
    elif provider == "PPL Electric":
        return scrape_ppl_electric(driver, lat, lon)
    elif provider == "We Energies":
        return scrape_we_energies(driver, lat, lon)
    elif provider == "MGE":
        return scrape_mge(driver, lat, lon)
    elif provider == "Georgia Power":
        return scrape_georgia_power(driver, lat, lon)
    elif provider == "SCE":
        return scrape_sce(driver, lat, lon)
    elif provider == "PGE":
        return scrape_pge(driver, lat, lon)
    elif provider == "Dominion Energy":
        return scrape_dominion_energy(driver, lat, lon)
    elif provider == "Duke Energy Ohio":
        return scrape_duke_energy_ohio(driver, lat, lon)
    elif provider == "DTE Energy":
        return scrape_dte_energy(driver, lat, lon)
    elif provider == "Consumers Energy":
        return scrape_consumers_energy(driver, lat, lon)
    elif provider == "Duke Energy NC":
        return scrape_duke_energy_nc(driver, lat, lon)
    elif provider == "Evergy MO":
        return scrape_evergy_mo(driver, lat, lon)
    elif provider == "Ameren MO":
        return scrape_ameren_mo(driver, lat, lon)
    elif provider == "APS":
        return scrape_aps(driver, lat, lon)
    elif provider == "SRP":
        return scrape_srp(driver, lat, lon)
    elif provider == "Arizona Public Service":
        return scrape_aps(driver, lat, lon)
    elif provider == "Duke Energy IN":
        return scrape_duke_energy_in(driver, lat, lon)
    elif provider == "Entergy Arkansas":
        return scrape_entergy_ar(driver, lat, lon)
    elif provider == "EWEB":
        return scrape_eweb(driver, lat, lon)
    elif provider == "PGE OR":
        return scrape_pge_or(driver, lat, lon)
    elif provider == "Pacific Power OR":
        return scrape_pacific_power_or(driver, lat, lon)
    elif provider == "LG&E & KU":
        return scrape_lge(driver, lat, lon)
    elif provider == "Warren RECC":
        return scrape_warren_rec(driver, lat, lon)
    elif provider == "CMP":
        return scrape_cmp(driver, lat, lon)
    elif provider == "PSO":
        return scrape_pso(driver, lat, lon)
    elif provider == "OG&E":
        return scrape_oge(driver, lat, lon)
    elif provider == "Entergy Louisiana":
        return scrape_entergy_la(driver, lat, lon)
    elif provider == "Entergy Arkansas":
        return scrape_entergy_ar(driver, lat, lon)
    elif provider == "Dominion Energy SC":
        return scrape_dominion_energy_sc(driver, lat, lon)
    elif provider == "Duke Energy SC":
        return scrape_duke_energy_sc(driver, lat, lon)
    elif provider == "MTE":
        return scrape_mtemc(driver, lat, lon)
    elif provider == "Eversource CT":
        return scrape_eversource_ct(driver, lat, lon)
    elif provider == "Rhode Island Energy":
        return scrape_rhode_island_energy(driver, lat, lon)
    elif provider == "PNM":
        return scrape_pnm(driver, lat, lon)
    elif provider == "Northwestern Energy":
        return scrape_northwestern_energy(driver, lat, lon)
    elif provider == "MDU":
        return scrape_mdu(driver, lat, lon)
    elif provider == "Idaho Power":
        return scrape_idaho_power(driver, lat, lon)
    elif provider == "MidAmerican Energy":
        return scrape_midamerican_energy(driver, lat, lon)
    elif provider == "Evergy KS":
        return scrape_evergy_ks(driver, lat, lon)
    elif provider == "Eversource NH":
        return scrape_eversource_nh(driver, lat, lon)
    elif provider == "Hawaiian Electric":
        return scrape_hawaiian_electric(driver, lat, lon)
    elif provider == "Rocky Mountain Power":
        return scrape_rocky_mountain_power(driver, lat, lon)
    elif provider == "BGE":
        return scrape_bge(driver, lat, lon)
    elif provider == "Green Mountain Power":
        return scrape_green_mountain_power(driver, lat, lon)
    else:
        return None
# ---------- Main Batch Processing ----------
def main():
    df = pd.read_csv("Long-Lat Locations.csv")
    output = []

    supported = [
    "Florida Power & Light",
    "Tampa Electric",
    "Duke Energy",
    "CenterPoint Energy",
    "CPS Energy",
    "Oncor Electric Delivery", 
    "Eversource",
    "National Grid", 
    "National Grid NY",
    "NYSEG",
    "RGE",
    "PSEG Long Island",
    "Con Edison",
    "PSEG NJ",
    "JCP&L",
    "PSE",
    "Seattle City Light",
    "Xcel Energy",
    "Cleco Power",
    "Entergy Louisiana",
    "ComEd",
    "PECO",
    "Met-Ed",
    "Duquesne Light",
    "PPL Electric",
    "We Energies",
    "MGE",
    "Georgia Power",
    "SCE",
    "PGE",
    "Dominion Energy",
    "Duke Energy Ohio",
    "DTE Energy",
    "Consumers Energy",
    "Duke Energy NC",
    "Evergy MO",
    "Ameren MO",
    "APS",
    "SRP",
    "Arizona Public Service",
    "Duke Energy IN",
    "Entergy Arkansas",
    "EWEB",
    "PGE OR",
    "Pacific Power OR",
    "LG&E & KU",
    "Warren RECC",
    "CMP",
    "PSO",
    "OG&E",
    "Entergy Louisiana",
    "Entergy Arkansas",
    "Dominion Energy SC",
    "Duke Energy SC",
    "MTE",
    "Eversource CT",
    "Rhode Island Energy",
    "PNM",
    "Northwestern Energy",
    "MDU",
    "Idaho Power",
    "MidAmerican Energy",
    "Evergy KS",
    "Eversource NH",
    "Hawaiian Electric",
    "Rocky Mountain Power",
    "BGE",
    "Green Mountain Power"

]

    filtered_df = df[df["provider_name"].isin(supported)]

    driver = None

    for i, row in filtered_df.iterrows():
        location_id = row["location_id"]
        provider = row["provider_name"]
        lat = row["latitude"]
        lon = row["longitude"]

        print(f"Checking location {location_id} | {provider}")
        try:
            if provider == "Florida Power & Light":
                # Restart driver for FPL to avoid session blocking
                if driver:
                    try: driver.quit()
                    except: pass
                driver = setup_driver()
                result = check_outage(driver, provider, lat, lon)
                driver.quit()
                driver = None
            else:
                # Reuse driver for others like Tampa Electric
                if not driver or not driver.service.is_connectable():
                    driver = setup_driver()
                result = check_outage(driver, provider, lat, lon)


            time.sleep(random.uniform(3, 6))  # Anti-bot delay

        except Exception as e:
            print(f"Error on {location_id}: {e}")
            result = None

        output.append({
            "location_id": location_id,
            "provider": provider,
            "latitude": lat,
            "longitude": lon,
            "outage": result
        })

    # Final driver cleanup
    if driver:
        try:
            driver.quit()
        except:
            pass

    # Save to CSV
    pd.DataFrame(output).to_csv("outage_status_results.csv", index=False)
    print("✅ Results written to outage_status_results.csv")

if __name__ == "__main__":
    main()
