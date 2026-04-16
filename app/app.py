"""
EV Infrastructure Intelligence System
Advanced Multi-page Dashboard with Forecasting & Analytics

Models Supported:
- Linear Regression
- Polynomial Regression
- ARIMA
"""

# ======================================================
# IMPORTS
# ======================================================
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from config import *
from map_utils import create_map

# ======================================================
# PAGE CONFIGURATION
# ======================================================
st.set_page_config(
    page_title="EV Infrastructure Intelligence",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CUSTOM STYLES
# ======================================================
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
}
.risk-high { background: #ff4444 !important; }
.risk-medium { background: #ffaa00 !important; }
.risk-low { background: #00C851 !important; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR – NAVIGATION
# ======================================================
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "📊 Dashboard",
        "🚗 EV Adoption Analysis",
        "🔌 Infrastructure Readiness",
        "🤖 ML Predictions",
        "🏙️ City Comparison",
        "📂 Data Sources"
    ]
)

# ======================================================
# LOAD MODEL (SINGLE UNIFIED BUNDLE)
# ======================================================
@st.cache_resource
def load_model_bundle():
    with open("../models/ev_forecast_model_v2.pkl", "rb") as f:
        return pickle.load(f)

model_data = load_model_bundle()

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_data():
    df = pd.read_csv("../data/final_master_report.csv")
    year_cols = sorted([c for c in df.columns if c.isdigit()], key=int)

    def categorize(f):
        f = str(f).upper()
        if "EV" in f or "ELECTRIC" in f:
            return "EV"
        if "CNG" in f:
            return "CNG"
        if "HYBRID" in f:
            return "HYBRID"
        if "PETROL" in f or "GASOLINE" in f:
            return "PETROL"
        if "DIESEL" in f:
            return "DIESEL"
        return "OTHER"

    df["Category"] = df["Fuel"].apply(categorize)
    df["Total_Vehicles"] = df[year_cols].sum(axis=1)
    return df, year_cols

df, year_cols = load_data()

# ======================================================
# SIDEBAR – CONTROLS
# ======================================================
st.sidebar.header("⚙️ Controls")

fuel_type = st.sidebar.selectbox(
    "Select Fuel Type",
    list(RATIOS.keys())
)

model_choice = st.sidebar.selectbox(
    "Select Prediction Model",
    ["Linear Regression", "Polynomial Regression", "ARIMA"]
)

rto = st.sidebar.selectbox(
    "Select RTO Office",
    sorted(df["RTO Office"].unique())
)

forecast_years = st.sidebar.slider(
    "Forecast Horizon (Years)",
    3, 10, 5
)

# ======================================================
# GEOCODING (PUNE BUG FIXED)
# ======================================================
@st.cache_data
def get_coordinates(rto_name):
    rto_clean = rto_name.strip().upper()

    if rto_clean in RTO_COORDS:
        return RTO_COORDS[rto_clean]

    try:
        geolocator = Nominatim(user_agent="ev_infra_app")
        location = geolocator.geocode(f"{rto_clean}, Maharashtra, India", timeout=10)
        if location:
            return (location.latitude, location.longitude)
    except GeocoderTimedOut:
        pass

    return (19.7515, 75.7139)  # Maharashtra center fallback

lat, lon = get_coordinates(rto)

# ======================================================
# COMMON DATA PROCESSING
# ======================================================
# Get fuel-specific settings
infra_name = RATIOS[fuel_type]['name']
infra_name_singular = RATIOS[fuel_type]['singular']
infra_ratio = RATIOS[fuel_type]['ratio']

rto_df = df[(df["RTO Office"] == rto) & (df["Category"] == fuel_type)]
all_rto_df = df[df["RTO Office"] == rto]

y_hist = rto_df[year_cols].sum().values
X_hist = np.array([int(y) for y in year_cols]).reshape(-1, 1)

# ======================================================
# STATE-LEVEL FORECAST (MODEL ROUTER)
# ======================================================
last_year = int(year_cols[-1])
future_years_arr = np.array(
    [[last_year + i] for i in range(1, forecast_years + 1)]
)

def predict_state(X):
    if model_choice == "Linear Regression":
        return model_data["linear"].predict(X)

    elif model_choice == "Polynomial Regression":
        poly = model_data["poly"]["transformer"]
        model = model_data["poly"]["model"]
        return model.predict(poly.transform(X))

    elif model_choice == "ARIMA":
        return model_data["arima"].forecast(steps=len(X))

state_pred = predict_state(future_years_arr)

# ======================================================
# RTO SHARE LOGIC
# ======================================================
state_fuel_total = df[df["Category"] == fuel_type]["Total_Vehicles"].sum()
rto_fuel_total = rto_df["Total_Vehicles"].sum()
rto_share = rto_fuel_total / state_fuel_total if state_fuel_total > 0 else 0

rto_pred = state_pred * rto_share

# ======================================================
# INFRASTRUCTURE CALCULATIONS
# ======================================================
# NOTE: National estimates are only available for EVs.
if fuel_type == 'EV':
    estimated_state_infra = NATIONAL_EV_CHARGERS * MAHARASHTRA_EV_SHARE
    estimated_rto_infra = int(estimated_state_infra * rto_share)
else:
    # No reliable national data for other types, so we focus on the gap.
    estimated_rto_infra = 0 

needed_infra = int(rto_pred[-1] / infra_ratio)
gap = needed_infra - estimated_rto_infra

vehicles_per_infra = (
    rto_pred[-1] / estimated_rto_infra
    if estimated_rto_infra > 0 else float('inf') # Use infinity for division by zero
)

# Risk calculation based on vehicles per infrastructure unit
if vehicles_per_infra <= RISK_THRESHOLDS['LOW']:
    risk_level, risk_color = "LOW", "🟢"
elif vehicles_per_infra <= RISK_THRESHOLDS['MODERATE']:
    risk_level, risk_color = "MODERATE", "🟡"
else:
    risk_level, risk_color = "HIGH", "🔴"

# ======================================================
# PAGE 1: DASHBOARD
# ======================================================
if page == "📊 Dashboard":
    st.title(f"🚗 {fuel_type} Infrastructure Intelligence Dashboard")
    # st.markdown(f"**Selected RTO:** {rto} | **Analysis Year:** {last_year}")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(f"Current {fuel_type} Vehicles", f"{int(rto_fuel_total):,}")
    col2.metric(f"Projected {fuel_type} Vehicles", f"{int(rto_pred[-1]):,}")
    col3.metric(f"Existing {infra_name}", f"{estimated_rto_infra:,}" if estimated_rto_infra > 0 else "N/A")
    col4.metric(f"{infra_name} Gap", f"{gap:,}")
    col5.markdown(
        f"<div class='metric-card risk-{risk_level.lower()}'>"
        f"<h3>{risk_color} {risk_level}</h3><p>Infra Risk</p></div>",
        unsafe_allow_html=True
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=X_hist.flatten(),
        y=y_hist,
        name="Historical",
        mode="lines+markers"
    ))
    fig.add_trace(go.Scatter(
        x=future_years_arr.flatten(),
        y=rto_pred,
        name="Forecast",
        mode="lines+markers",
        line=dict(dash="dash")
    ))
    fig.update_layout(
        title=f"{fuel_type} Adoption Trend (RTO Level)",
        xaxis_title="Year",
        yaxis_title=f"{fuel_type} Registrations"
    )
    st.plotly_chart(fig, use_container_width=True)

    popup = f"""
    <b>RTO:</b> {rto}<br>
    <b>Projected {fuel_type}s:</b> {int(rto_pred[-1]):,}<br>
    <b>{infra_name} Needed:</b> {needed_infra:,}<br>
    <b>Gap:</b> {gap:,}<br>
    <b>Risk:</b> {risk_color} {risk_level}
    """
    m = create_map(lat, lon, popup, MAP_COLORS.get(risk_level, "blue"))
    st_folium(m, height=450)

# ======================================================
# PAGE 2–6 (ADAPTED FOR FUEL TYPE)
# ======================================================
elif page == "🚗 EV Adoption Analysis":
    st.header(f"Fuel Mix Analysis for {rto}")
    fuel_mix = all_rto_df.groupby("Category")["Total_Vehicles"].sum().reset_index()
    fig = px.pie(fuel_mix, values="Total_Vehicles", names="Category",
                 title=f"Fuel Mix Distribution in {rto}")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🔌 Infrastructure Readiness":
    st.header(f"Infrastructure Readiness for {fuel_type}s in {rto}")
    st.metric(f"{fuel_type} Vehicles per {infra_name_singular}", f"{vehicles_per_infra:.1f}" if estimated_rto_infra > 0 else "N/A")
    st.metric("Risk Level", f"{risk_color} {risk_level}")
    st.info(f"This is based on a ratio of 1 unit of infrastructure per {infra_ratio} vehicles.")

elif page == "🤖 ML Predictions":
    st.header("Model Performance Metrics")
    st.json(model_data["metrics"])
    st.info("These metrics are for the underlying state-level vehicle forecast model, which is independent of RTO or fuel type.")

elif page == "🏙️ City Comparison":
    st.header(f"Compare {fuel_type} Vehicle Counts Across Cities")
    selected_rtos = st.multiselect("Select RTOs", sorted(df["RTO Office"].unique()), default=([rto] if rto else None))
    if len(selected_rtos) >= 1:
        comp_df = pd.DataFrame([
            {"RTO": r, f"{fuel_type} Vehicles": df[(df["RTO Office"] == r) &
                                 (df["Category"] == fuel_type)]["Total_Vehicles"].sum()}
            for r in selected_rtos
        ])
        fig = px.bar(comp_df, x="RTO", y=f"{fuel_type} Vehicles", title=f"{fuel_type} Vehicle Comparison")
        st.plotly_chart(fig, use_container_width=True)

elif page == "📂 Data Sources":
    st.markdown("""
    **Primary Sources**
    - Ministry of Road Transport & Highways – Vahan Dashboard
    - Bureau of Energy Efficiency – EV Charging Infrastructure
    - International Energy Agency – EV Benchmarks
    """)
    st.code(f"""
# Configuration used for this analysis
RATIOS = {RATIOS}
    """, language="python")
