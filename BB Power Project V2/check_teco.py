from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def check_teco_outage():
    options = Options()
    options.add_argument("--headless")  # Comment this out if you want to see the browser
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.tampaelectric.com/outages/outagemap/")

    time.sleep(10)  # Wait for the map to load (can be optimized later)

    page_text = driver.page_source
    power_out = "There are currently no outages reported" not in page_text

    driver.quit()

    return "Out" if power_out else "On"

# Test
if __name__ == "__main__":
    status = check_teco_outage()
    print("Tampa Electric Power Status:", status)
