from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def check_fpl_outage():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.fplmaps.com/")
    
    time.sleep(12)  # Wait for map layers to load

    page_text = driver.page_source

    # Basic check: look for visible outage blocks
    likely_outage = "Number of customers affected" in page_text

    driver.quit()

    return "Out" if likely_outage else "On"

# Test
if __name__ == "__main__":
    status = check_fpl_outage()
    print("Florida Power & Light Status:", status)
