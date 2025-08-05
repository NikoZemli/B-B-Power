# ⚡ BB Power Project: Commercial Power Status Dashboard

A live, interactive Streamlit dashboard to monitor power outages across U.S. provider locations. Built for Brown & Brown Insurance Technology Solutions, this tool helps visualize and log outage events in real time to support operational resilience.

---

## 🚀 Features

### 🗺️ Interactive Outage Map
- View outage and non-outage locations using color-coded pins (✅ / ❌)
- Hover over markers to view:
  - Address
  - Provider
  - Outage status

### 📊 Analytics
- **KPI Summary**: Track total locations, outages, and uptime
- **Outage Rate by Provider**: Visual breakdown of percentage outages
- **Outages Over Time**: Line chart (10-minute intervals) if `Timestamp` column is available

### 🔍 Filter Controls
- **Provider filter**: Limit data to a specific utility company
- **Address search**: Match any part of an address string
- **Time slider**: Focus on outages from the past X hours

### 🌧️ NOAA Radar Overlays
- Live composite radar (CONUS BREF)
- 1-hour NEXRAD radar mosaic

### 📜 Historical Logs
- Outages are logged to an internal SQLite database (`outage_history.db`)
- View full outage history with detected/resolved timestamps

### 🔁 Auto Refresh
- The dashboard auto-refreshes every 60 seconds to update with new data

---

## 📂 Project Structure

```bash
bb_power_project/
├── dashboard.py              # Main Streamlit app
├── batch_outage_checker.py  # Scraper to generate outage_results.csv
├── outage_results.csv        # Input data file (auto-refreshed or static)
├── outage_history.db         # SQLite DB for tracking resolved/unresolved outages
├── Long_Lat Locations.csv    # Address coordinate mapping
├── requirements.txt          # Dependencies
├── scraper_errors.log        # Logs for batch scraper
├── 1n9id6sck0dbekkxihijnwigr2c9.jpg # App banner/logo
