import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
import requests

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
            <h1>Brown and Brown Power Status Dashboard</h1>
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
m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

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

# ----- Weather on Map Click -----
api_key = "6883338242361e86c568e8755255bdb2"

if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
    try:
        weather_response = requests.get(weather_url).json()
        if weather_response.get("cod") == 200:
            temp = weather_response["main"]["temp"]
            desc = weather_response["weather"][0]["description"].capitalize()
            city = weather_response["name"]
            icon = weather_response["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon}.png"

            st.markdown(f"""
                <div class="weather-box">
                    <strong>🌤️ Weather at clicked location ({city}):</strong><br>
                    <img src="{icon_url}" style="vertical-align:middle"> {desc}, {temp} °F
                </div>
            """, unsafe_allow_html=True)
    except:
        st.warning("⚠️ Could not retrieve weather data for clicked location.")


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
