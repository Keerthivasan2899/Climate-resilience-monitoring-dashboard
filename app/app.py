import streamlit as st
import pandas as pd
import plotly.express as px

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

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(pd.to_datetime("2021-01-01"), pd.to_datetime("2025-12-31")),
    min_value=pd.to_datetime("2021-01-01"),
    max_value=pd.to_datetime("2025-12-31")
)

# --------------------
# Main Layout
# --------------------
col1, col2 = st.columns([1, 3])

with col1:
    st.metric(label=f"{indicator} Anomaly", value="--", delta="--")
    st.markdown("### Summary")
    st.markdown(f"- **Region:** {region}")
    st.markdown(
        f"- **Date Range:** {date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}")
    st.markdown("### Insights")
    st.markdown("- NDVI anomalies indicate vegetation stress.")
    st.markdown("- Rainfall anomalies can signal drought or flood conditions.")
    st.markdown("- Flood anomalies highlight areas at risk of flooding.")

with col2:
    st.subheader("Time Series Trend")
    st.info("Chart will appear here after data integration.")
    st.subheader("Geospatial Distribution")
    st.info("Map will appear here after data integration.")

st.divider()

st.subheader("Spatial Overview")
st.info("Interactive map will appear here.")
