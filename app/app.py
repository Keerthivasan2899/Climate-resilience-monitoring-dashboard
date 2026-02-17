import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

# --------------------
# Load Data
# --------------------


@st.cache_data
def load_ndvi():
    df = pd.read_csv("data/ndvi_with_anomaly.csv")
    df["date"] = pd.to_datetime(
        df["year"].astype(int).astype(str) + "-" +
        df["month"].astype(int).astype(str) + "-01"
    )
    return df


ndvi_df = load_ndvi()


@st.cache_data
def load_rainfall():
    df = pd.read_csv("data/rainfall_with_anomaly.csv")
    df["date"] = pd.to_datetime(
        df["year"].astype(int).astype(str) + "-" +
        df["month"].astype(int).astype(str) + "-01"
    )
    return df


rain_df = load_rainfall()


@st.cache_data
def load_flood():
    df = pd.read_csv("data/flood_with_anomaly.csv")
    df["date"] = pd.to_datetime(
        df["year"].astype(int).astype(str) + "-" +
        df["month"].astype(int).astype(str) + "-01"
    )
    return df


flood_df = load_flood()

# --------------------
# Map Helper Function
# --------------------


def build_region_df(latest_value, label):
    data = {
        "Region": ["North America", "Central America", "South America"],
        label: [
            latest_value * 1.05,  # Simulated value for North America
            latest_value * 0.95,  # Simulated value for Central America
            latest_value * 1.10  # Simulated value for South America
        ],
        "iso": ["USA", "MEX", "BRA"]  # ISO codes for mapping
    }
    return pd.DataFrame(data)


# --------------------
# Page Configuration
# --------------------
st.set_page_config(page_title="Climate Resilience Dashboard", layout="wide")

# --------------------
# Header
# --------------------
st.title("🌎 Climate Resilience Monitoring Dashboard")
st.markdown(
    "Monitoring NDVI, Rainfall, and Flood anomalies across the Americas (2021-2025).")
st.divider()

# --------------------
# Sidebar Controls
# --------------------
st.sidebar.header("Controls")

indicator = st.sidebar.selectbox(
    "Select Indicator",
    ["NDVI", "Rainfall", "Flood"]
)

region = st.sidebar.selectbox(
    "Select Region",
    ["Americas", "North America", "Central America", "South America"]
)

time_mode = st.sidebar.radio(
    "Time Selection Mode",
    ["Predefined Time Windows", "Custom Date Range"]
)

if time_mode == "Predefined Time Windows":
    time_window = st.sidebar.selectbox(
        "Time Window",
        [
            "Full Period (2021-2025)",
            "Last 12 Months",
            "Last 24 Months",
            "Last 36 Months"
        ]
    )
else:
    start_date = st.sidebar.date_input(
        "Start Date",
        value=datetime(2021, 1, 1),
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2025, 12, 31)
    )

    end_date = st.sidebar.date_input(
        "End Date",
        value=datetime(2025, 12, 31),
        min_value=datetime(2021, 1, 1),
        max_value=datetime(2025, 12, 31)
    )

# --------------------
# Filter Data
# --------------------

df = None
value_col = None
anomaly_col = None
label = None

if indicator == "NDVI":
    df = ndvi_df.copy()
    value_col = "ndvi"
    anomaly_col = "anomaly"
    label = "NDVI"

elif indicator == "Rainfall":
    df = rain_df.copy()
    value_col = "rainfall_mm"
    anomaly_col = "anomaly"
    label = "Rainfall"
elif indicator == "Flood":
    df = flood_df.copy()
    value_col = "flood_area_km2"
    anomaly_col = "anomaly"
    label = "Flood Area (km²)"
else:
    df = None

if df is not None:

    if time_mode == "Predefined Time Windows":

        latest_date = df["date"].max()

        if time_window == "Last 12 Months":
            start_date = latest_date - pd.DateOffset(months=12)
        elif time_window == "Last 24 Months":
            start_date = latest_date - pd.DateOffset(months=24)
        elif time_window == "Last 36 Months":
            start_date = latest_date - pd.DateOffset(months=36)
        else:
            start_date = df["date"].min()

        end_date = latest_date
    else:
        start_date = df["date"].min()
        end_date = df["date"].max()

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df = df[(df["date"] >= start_date) &
            (df["date"] <= end_date)]


# --------------------
# Main Layout
# --------------------
col1, col2 = st.columns([1, 3])

with col1:
    if df is not None and not df.empty:
        latest = df.iloc[-1]
        anomaly_val = round(latest[anomaly_col], 3)
        st.metric(
            label=f"Latest {label} Anomaly",
            value=anomaly_val,
            delta=anomaly_val
        )
    else:
        st.metric("No Data", "--")
    st.markdown("### Summary")
    st.markdown(f"- **Region:** {region}")
    if time_mode == "Predefined Time Windows":
        st.markdown(f"- **Time Window:** {time_window}")
    else:
        st.markdown(
            f"- **Custom Date Range:** {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    if df is not None and not df.empty:
        st.markdown("---")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Filtered Data",
            csv,
            f"{label}_filtered.csv",
            "text/csv"
        )


with col2:
    st.subheader(f"{label} Trend")

    if df is not None and not df.empty:
        fig = px.line(
            df,
            x="date",
            y=value_col,
            title=f"Monthly {label}"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")

# --------------------
# Map Section
# --------------------
st.divider()
st.subheader("Spatial Overview")

if df is not None and not df.empty:
    latest = df.iloc[-1]
    latest_val = latest[value_col]

    map_df = build_region_df(latest_val, label)

    if indicator == "NDVI":
        scale = "Greens"
    elif indicator == "Rainfall":
        scale = "Blues"
    else:
        scale = "Reds"

    fig_map = px.choropleth(
        map_df,
        locations="iso",
        color=label,
        hover_name="Region",
        projection="natural earth",
        color_continuous_scale=scale,
        title=f"{label} Across the Americas"
    )

    fig_map.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

else:
    st.info("Map will appear once data is available.")
