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
            margin-top: 0px !important; /* Reduced top margin */
            color: #333;
        }
        iframe {
            margin-bottom: -10px; /* Reduce spacing after map */
        }
        section.main > div {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
        }
    </style>
""", unsafe_allow_html=True)


# ----- Load Data -----
df = pd.read_csv("outage_results.csv")

# ----- Sidebar Filters -----
with st.sidebar:
    st.image("1n9id6sck0dbekkxihijnwigr2c9.jpg", width=120)
    st.markdown("## ⚙️ Filter Options")
    provider_filter = st.selectbox("🔌 Select Provider", options=["All"] + sorted(df["Provider"].dropna().unique()))

if provider_filter != "All":
    df = df[df["Provider"] == provider_filter]

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

# ----- Map -----
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

st_folium(m, width=1250, height=600)  # Full-width large map


# ----- Last Updated Timestamp -----
if "Timestamp" in df.columns:
    last_update = pd.to_datetime(df["Timestamp"]).max()
    st.markdown(
        f"<div style='text-align:left; font-size:16px; color:gray; margin-top:-10px;'>🕒 Last updated: {last_update.strftime('%Y-%m-%d %H:%M:%S')}</div>",
        unsafe_allow_html=True
    )

st.markdown("""<hr style='margin:10px 0;'>""", unsafe_allow_html=True)

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
