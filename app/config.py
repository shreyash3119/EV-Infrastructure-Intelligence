"""
Configuration file for EV Infrastructure Intelligence System
Contains all constants, parameters, and mappings
"""

import os

# ==============================
# APPLICATION SETTINGS
# ==============================
APP_TITLE = "EV Infrastructure Intelligence"
APP_ICON = "🚗"
VERSION = "2.0.0"
LAST_UPDATED = "2026-02-04"

# ==============================
# MODEL PARAMETERS
# ==============================
RATIOS = {
    'EV': {'name': 'Charging Stations', 'singular': 'Charging Station', 'ratio': 10},
    'CNG': {'name': 'CNG Pumps', 'singular': 'CNG Pump', 'ratio': 800},
    'HYBRID': {'name': 'Specialized Garages', 'singular': 'Specialized Garage', 'ratio': 500}
}
DEFAULT_FORECAST_YEARS = 5
MIN_FORECAST_YEARS = 3
MAX_FORECAST_YEARS = 10

# ==============================
# INFRASTRUCTURE ESTIMATES
# ==============================
NATIONAL_EV_CHARGERS = 12000  # Approximate public chargers in India (2024)
MAHARASHTRA_EV_SHARE = 0.18   # Maharashtra's share of national EV fleet (~18%)

# Charger installation costs (in INR)
CHARGER_COST_PER_UNIT = 500000  # ₹5 Lakh per charging station
TECHNICIAN_TRAINING_COST = 50000  # ₹50K per technician
TECHNICIANS_PER_CHARGER = 2

# ==============================
# RISK THRESHOLDS
# ==============================
RISK_THRESHOLDS = {
    'LOW': 10,       # EVs per charger <= 10
    'MODERATE': 20,  # EVs per charger <= 20
    'HIGH': 999      # EVs per charger > 20
}

# ==============================
# RTO COORDINATES (MAHARASHTRA)
# ==============================
RTO_COORDS = {
    # Mumbai Metropolitan Region
    'MUMBAI SOUTH': (18.9388, 72.8354),
    'MUMBAI WEST': (19.0596, 72.8295),
    'MUMBAI CENTRAL': (19.0176, 72.8562),
    'MUMBAI EAST': (19.1136, 72.8697),
    'THANE': (19.2183, 72.9781),
    'NAVI MUMBAI': (19.0330, 73.0297),
    'KALYAN': (19.2403, 73.1305),
    'MIRA ROAD': (19.2806, 72.8692),
    'VASAI': (19.4612, 72.8081),
    
    # Pune Region
    'PUNE': (18.5204, 73.8567),
    'PIMPRI CHINCHWAD': (18.6298, 73.7997),
    'KOTHRUD PUNE': (18.5074, 73.8077),
    'SHIVAJINAGAR PUNE': (18.5304, 73.8567),
    'HADAPSAR PUNE': (18.5089, 73.9260),
    'NIGDI': (18.6555, 73.7702),
    
    # Nashik Division
    'NASHIK': (19.9975, 73.7898),
    'NASHIK ROAD': (20.0478, 73.7791),
    'MALEGAON': (20.5579, 74.5287),
    'SINNAR': (19.8453, 73.9973),
    
    # Nagpur Division
    'NAGPUR': (21.1458, 79.0882),
    'NAGPUR EAST': (21.1619, 79.1039),
    'NAGPUR WEST': (21.1255, 79.0677),
    'KAMPTEE': (21.2225, 79.1973),
    
    # Aurangabad Division
    'AURANGABAD': (19.8762, 75.3433),
    'JALNA': (19.8344, 75.8814),
    'BEED': (18.9894, 75.7607),
    'PARBHANI': (19.2608, 76.7713),
    
    # Kolhapur Division
    'KOLHAPUR': (16.7050, 74.2433),
    'SANGLI': (16.8524, 74.5641),
    'SATARA': (17.6805, 73.9903),
    'SOLAPUR': (17.6599, 75.9064),
    
    # Amravati Division
    'AMRAVATI': (20.9374, 77.7796),
    'AKOLA': (20.7002, 77.0082),
    'YAVATMAL': (20.3974, 78.1307),
    'BULDHANA': (20.5311, 76.1844),
    'WASHIM': (20.1109, 77.1331),
    
    # Konkan Division
    'RATNAGIRI': (16.9944, 73.3000),
    'SINDHUDURG': (16.0244, 73.6697),
    'RAIGAD': (18.5196, 73.0169),
    
    # Other Major RTOs
    'AHMEDNAGAR': (19.0948, 74.7480),
    'DHULE': (20.9042, 74.7749),
    'JALGAON': (21.0077, 75.5626),
    'NANDURBAR': (21.3676, 74.2403),
    'CHANDRAPUR': (19.9615, 79.2961),
    'GONDIA': (21.4535, 80.1939),
    'WARDHA': (20.7453, 78.5974),
    'HINGOLI': (19.7157, 77.1447),
    'NANDED': (19.1383, 77.3210),
    'LATUR': (18.4088, 76.5604),
    'OSMANABAD': (18.1773, 76.0407),
}

# ==============================
# MAP SETTINGS
# ==============================
MAP_CONFIG = {
    'default_zoom': 12,
    'min_zoom': 8,
    'max_zoom': 18,
    'tile_layer': 'OpenStreetMap',
}

MAP_COLORS = {
    'LOW': '#00C851',      # Green
    'MODERATE': '#ffaa00', # Orange
    'HIGH': '#ff4444',     # Red
}

# ==============================
# UI THEME
# ==============================
THEME = {
    'primary_color': '#667eea',
    'secondary_color': '#764ba2',
    'success_color': '#00C851',
    'warning_color': '#ffaa00',
    'danger_color': '#ff4444',
}

# ==============================
# DATA SOURCES
# ==============================
DATA_SOURCES = {
    'VAHAN': {
        'name': 'Ministry of Road Transport & Highways - Vahan Dashboard',
        'url': 'https://vahan.parivahan.gov.in/vahan4dashboard/',
        'description': 'Official vehicle registration data',
        'update_frequency': 'Daily'
    },
    'BEE': {
        'name': 'Bureau of Energy Efficiency',
        'url': 'https://beeindia.gov.in/',
        'description': 'Charging infrastructure data',
        'update_frequency': 'Quarterly'
    },
    'IEA': {
        'name': 'International Energy Agency',
        'url': 'https://www.iea.org/reports/global-ev-outlook-2024',
        'description': 'Global EV benchmarks and standards',
        'update_frequency': 'Annual'
    }
}

# ==============================
# FILE PATHS
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

DATA_FILE = os.path.join(DATA_DIR, 'final_master_report.csv')
MODEL_FILE = os.path.join(MODEL_DIR, 'ev_forecast_model.pkl')
METRICS_FILE = os.path.join(MODEL_DIR, 'model_metrics.json')
