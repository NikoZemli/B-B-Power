from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ADDRESS = "300 North Beach Street, Daytona Beach, FL 32114"
EDGE_DRIVER_PATH = "C:/BB Power Project/drivers/msedgedriver.exe"

def check_fpl_status(address):
    options = EdgeOptions()
    # REMOVE headless mode so you can SEE what's happening
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Edge(service=EdgeService(EDGE_DRIVER_PATH), options=options)

    try:
        print("Opening FPL map...")
        driver.get("https://www.fplmaps.com/")
        wait = WebDriverWait(driver, 20)

        print("Waiting for search field...")
        search_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search by address')]"))
        )

        print("Typing address...")
        search_input.clear()
        search_input.send_keys(address)
        search_input.send_keys(Keys.RETURN)

        print("Waiting for search results to load...")
        time.sleep(10)

        print("Looking for power status...")
        popups = driver.find_elements(By.CLASS_NAME, "incident-popup")
        if popups:
            popup_text = popups[0].text
            print(f"Popup found: {popup_text}")
            if "No outages" in popup_text or "No reported outages" in popup_text:
                return "Power ON ✅"
            elif "affected" in popup_text or "outage" in popup_text.lower():
                return f"Power OFF ❌ - {popup_text}"
            else:
                return f"Unclear status: {popup_text}"
        else:
            return "No popup found — likely Power ON ✅"

    except Exception as e:
        print(f"❌ Error encountered: {e}")
        return f"Error: {str(e)}"
    finally:
        print("Closing browser...")
        time.sleep(3)  # Let you see final screen
        driver.quit()


# Run it
result = check_fpl_status(ADDRESS)
print(f"Power status for {ADDRESS}: {result}")
