import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
import requests
import threading
import subprocess

# ── Outage history storage (standard-lib only) ────────────────────────────────
import sqlite3, pathlib, datetime as dt

DB_PATH = pathlib.Path("outage_history.db")

def init_db() -> None:
    """Create the SQLite file the first time the app runs."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS outages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                address     TEXT,
                provider    TEXT,
                detected_at TIMESTAMP,
                resolved_at TIMESTAMP
            )
        """)
init_db()
def log_outage(address: str, provider: str) -> None:
    """Insert a row only if this outage isn’t already open."""
    now = dt.datetime.utcnow()
    with sqlite3.connect(DB_PATH) as conn:
        open_outage = conn.execute("""
            SELECT 1 FROM outages
            WHERE address=? AND provider=? AND resolved_at IS NULL
        """, (address, provider)).fetchone()

        if not open_outage:
            conn.execute("""
                INSERT INTO outages (address, provider, detected_at)
                VALUES (?,?,?)
            """, (address, provider, now))

def resolve_outage(address: str, provider: str) -> None:
    """Stamp resolved_at when power returns."""
    now = dt.datetime.utcnow()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            UPDATE outages
            SET resolved_at=?
            WHERE address=? AND provider=? AND resolved_at IS NULL
        """, (now, address, provider))

# ----- Auto-Refresh -----
st_autorefresh(interval=60000, key="refresh")  # Refresh every 60 seconds

# ----- Page Config -----
st.set_page_config(page_title="Power Dashboard", layout="wide")

# ----- Custom Styling -----
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .stMarkdown {
            margin-bottom: 0.5rem;
        }
        .bb-header {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .bb-header h1 {
            color: #ffffff;
        }
        .bb-banner {
            background-color: #1C2D57;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .weather-box {
            background-color: #f0f4f8;
            padding: 16px;
            border-radius: 10px;
            margin-top: 0px !important;
            color: #333;
        }
        iframe {
            margin-bottom: -10px;
        }
        section.main > div {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
        }

        /* Sidebar enhancements */
        .sidebar-content h2,
        .sidebar-content h3 {
            font-size: 18px !important;
            font-weight: 600 !important;
            margin-top: 15px;
            margin-bottom: 10px;
        }

        /* Expander background and text color */
        .streamlit-expanderHeader {
            background-color: #1C2D57 !important;
            color: white !important;
            font-weight: 600;
        }
        .streamlit-expanderContent {
            background-color: #1C2D57 !important;
            color: white !important;
        }

        /* Optional: remove focus outline */
        .streamlit-expanderHeader:focus {
            outline: none !important;
            box-shadow: none !important;
        }

        /* Optional: tighten spacing between expanders */
        .streamlit-expander {
            margin-bottom: 8px;
        }
    </style>
            
""", unsafe_allow_html=True)

# ----- Custom Styling -----
st.markdown("""
    <style>
    /* tighten the global block padding (you already had this) */
    .block-container {padding-top:0rem!important;padding-bottom:0rem!important;}

    /* NEW – remove Streamlit’s default 1.5 rem gap between blocks */
    [data-testid="stVerticalBlock"] {gap:0.25rem!important;}

    /* optional: also collapse gaps inside columns */
    [data-testid="column"] > [data-testid="stVerticalBlock"] {gap:0.25rem!important;}

    /* keep headings tight so they don’t re-introduce white space */
    h1,h2,h3,h4,h5,h6 {margin-top:0.6rem!important;margin-bottom:0.2rem!important;}
    </style>
""", unsafe_allow_html=True)

# ----- Load Data -----
df = pd.read_csv("outage_results.csv")

# ── Persist today’s status into the history DB ────────────────────────────────
if {"Address", "Provider", "Outage Detected"}.issubset(df.columns):
    for _, row in df.iterrows():
        if row["Outage Detected"]:
            log_outage(row["Address"], row["Provider"])
        else:
            resolve_outage(row["Address"], row["Provider"])

# Convert 'Timestamp' column to datetime if it exists
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")


# ----- Sidebar Filters -----
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)

    st.image("1n9id6sck0dbekkxihijnwigr2c9.jpg", width=120)
    st.markdown("## ⚙️ Filter Options")

    # Provider filter
    provider_filter = st.selectbox("🔌 Select Provider", options=["All"] + sorted(df["Provider"].dropna().unique()))
    if provider_filter != "All":
        df = df[df["Provider"] == provider_filter]

    # Address search filter
    address_filter = st.text_input("📍 Search by Address")
    if address_filter:
        df = df[df["Address"].str.contains(address_filter, case=False, na=False)]

    # Optional time filter
    if "Timestamp" in df.columns:
        st.markdown("### ⏱️ Time Filter")
        hours = st.slider("Show data from past X hours", min_value=1, max_value=72, value=24)
        cutoff_time = pd.Timestamp.now() - pd.Timedelta(hours=hours)
        df = df[df["Timestamp"] >= cutoff_time]

    # Outage rate bar chart
    if "Outage Detected" in df.columns and not df["Outage Detected"].isna().all():
        outage_ratio = df.groupby("Provider")["Outage Detected"].mean().sort_values(ascending=False)
        st.markdown("### ⚠️ Outage Rate")
        st.bar_chart(outage_ratio)

    # Help section
    with st.expander("ℹ️ What do these filters do?"):
        st.write("""
        - **Provider**: Limits the map and table to one utility company.
        - **Address Search**: Find locations containing a specific keyword.
        - **Time Filter**: Focus on recent outage events only.
        """)

    st.markdown('</div>', unsafe_allow_html=True)
# ----- Header -----
st.markdown(f"""
    <div class="bb-banner">
        <div class="bb-header">
            <h1>Brown and Brown Commercial Power Status Dashboard</h1>
        </div>
    </div>
""", unsafe_allow_html=True)
st.markdown("Track and visualize power outages across provider locations.")

# ----- KPIs -----
col1, col2, col3 = st.columns(3)
col1.metric("🔍 Locations Monitored", len(df))
col2.metric("❌ Outages Detected", df["Outage Detected"].sum())
col3.metric("✅ No Outage", len(df) - df["Outage Detected"].sum())

# ----- Map and Click-Based Weather Info -----
st.markdown("### 🌍 Outage Locations Map", unsafe_allow_html=True)

center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()
m = folium.Map(
    location=[39.8283, -98.5795],   # “centroid” of the contiguous US
    zoom_start=4,                   # 4 → shows the full country
    tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
    attr='&copy; <a href="https://carto.com/">CARTO</a>',
    name="CartoDB Positron"
)

for _, row in df.iterrows():
    status = "❌ Outage" if row["Outage Detected"] else "✅ No Outage"
    color = "red" if row["Outage Detected"] else "green"
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"""
        <b>Address:</b> {row['Address']}<br>
        <b>Provider:</b> {row['Provider']}<br>
        <b>Status:</b> {status}
        """,
        icon=folium.Icon(color=color)
    ).add_to(m)

# ── LIVE RADAR OVERLAYS ─────────────────────────────────────────────────────────
# 1) CONUS-wide composite (MRMS BREF reflectivity mosaic) served by NOAA GeoServer
folium.raster_layers.WmsTileLayer(
    url="https://opengeo.ncep.noaa.gov/geoserver/conus/conus_bref_qcd/ows?",
    name="NOAA Radar (CONUS BREF)",
    layers="conus_bref_qcd",
    fmt="image/png",
    transparent=True,
    attr="NOAA/NWS MRMS",    # ← use **attr**, not attribution
    overlay=True,
    control=True,
    opacity=0.65
).add_to(m)

# 2) Re-centred NEXRAD-time mosaic from nowCOAST (ArcGIS tiled service, XYZ)
folium.TileLayer(
    tiles=("https://nowcoast.noaa.gov/arcgis/rest/services/"
           "nowcoast/radar_meteo_imagery_nexrad_time/MapServer/tile/{z}/{y}/{x}"),
    name="NEXRAD (latest 1 hr)",
    attr="NOAA/NWS nowCOAST",
    overlay=True,
    control=True,
    opacity=0.6
).add_to(m)

# Optional: give the user a layer switcher
folium.LayerControl(
    position="topright",
    collapsed=True              # shows only a small layers button
).add_to(m)

# ────────────────────────────────────────────────────────────────────────────────

# Render map and capture user interaction
map_data = st_folium(m, width=1250, height=600)
# ----- Last Updated Timestamp (under map) -----
import os
from datetime import datetime

last_updated = None

if "Timestamp" in df.columns and not df["Timestamp"].isna().all():
    last_updated = pd.to_datetime(df["Timestamp"]).max()
else:
    try:
        mod_time = os.path.getmtime("outage_results.csv")
        last_updated = datetime.fromtimestamp(mod_time)
    except:
        last_updated = None

if last_updated:
    st.markdown(f"<p style='margin-top: -10px; color: gray;'>🕒 Last Updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)

# ----- Time-Series Chart -----
st.markdown("### 📈 Outages Over Time")
if "Timestamp" in df.columns:
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    time_summary = df.resample("10min", on="Timestamp")["Outage Detected"].sum().rename("Outages")
    st.line_chart(time_summary)
else:
    st.info("ℹ️ Add a 'Timestamp' column in your CSV to enable outage trend analysis.")

# ----- Table -----
st.markdown("### 📋 Full Outage Table")
st.data_editor(df, use_container_width=True, hide_index=True, disabled=True)

# ── Historical outage log ─────────────────────────────────────────────────────
def load_history() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return (
            pd.read_sql(
                "SELECT * FROM outages ORDER BY detected_at DESC", conn,
                parse_dates=["detected_at", "resolved_at"]
            )
            .rename(columns={
                "address": "Address",
                "provider": "Provider",
                "detected_at": "Detected At",
                "resolved_at": "Resolved At"
            })
        )

# BIG header, no dropdown
st.markdown("### 📜 Historical Outage Table")

hist_df = load_history()

# hide the internal SQLite id so it matches the live table look
if "id" in hist_df.columns:
    hist_df = hist_df.drop(columns=["id"])

st.data_editor(
    hist_df,
    use_container_width=True,
    hide_index=True,
    disabled=True      # read-only, just like the live table
)
