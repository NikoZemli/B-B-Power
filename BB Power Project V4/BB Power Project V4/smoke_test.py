import csv, logging, time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager  # ✅ Added

from batch_outage_checker import known_scrapers  # ✅ Your existing import

def quick_edge():
    o = Options()
    o.add_argument("--headless=new")
    o.add_argument("--disable-gpu")
    o.add_argument("--window-size=1400,1000")

    # ✅ Use webdriver-manager to auto-download the correct Edge driver
    return webdriver.Edge(
        service=EdgeService(EdgeChromiumDriverManager().install()),
        options=o
    )

def smoke():
    results = []
    driver = quick_edge()
    for provider, url in known_scrapers.items():
        row = {"provider": provider, "url": url}
        try:
            driver.get(url)
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            row["title"] = driver.title
            shapes = driver.find_elements(By.CSS_SELECTOR, "g[class*='outage'], g[class*='esri']")
            row["visible_shapes"] = sum(s.is_displayed() for s in shapes)
            row["status"] = "OK"
        except Exception as e:
            row["status"] = f"ERROR: {e}"
        finally:
            results.append(row)
    driver.quit()

    with open("scraper_smoke_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    smoke()
    print("✅ Done – open scraper_smoke_results.csv for the verdict.")
