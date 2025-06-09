from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def check_duke_outage():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://outagemap.duke-energy.com/")

    # Wait for the map to load outages
    time.sleep(15)

    page_text = driver.page_source

    # Heuristic: look for common outage info pattern
    outage_detected = "Customers Affected" in page_text or "outage" in page_text.lower()

    driver.quit()

    return "Out" if outage_detected else "On"

# Test
if __name__ == "__main__":
    status = check_duke_outage()
    print("Duke Energy Status:", status)
