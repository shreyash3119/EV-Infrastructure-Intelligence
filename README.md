# EV Infrastructure Intelligence

Machine learning powered Streamlit dashboard for forecasting vehicle adoption and estimating infrastructure readiness across Maharashtra RTO regions.

The project combines historical registration data, pre-trained forecasting models, and geospatial visualization to help planners understand where EV charging and related support infrastructure may fall short over the next few years.

## Overview

This application focuses on:

- Forecasting state-level vehicle growth using multiple ML/time-series approaches
- Translating that forecast into RTO-level demand using each RTO's observed share
- Estimating infrastructure needs for EV, CNG, and hybrid categories
- Highlighting infrastructure gaps and risk levels for selected RTO offices
- Presenting the results through an interactive Streamlit dashboard

## Key Features

- Interactive KPI dashboard for current fleet, projected fleet, existing infrastructure, and infrastructure gap
- Multiple forecasting options: Linear Regression, Polynomial Regression, and ARIMA
- RTO-level analysis for 62 Maharashtra transport office regions
- Fuel-mix exploration for each selected RTO
- Infrastructure readiness view with risk classification
- City comparison charts across multiple RTOs
- Interactive Folium map with location-based infrastructure insight
- Built-in data source and configuration summary inside the app

## Screenshots

### Dashboard Overview

![Dashboard overview](projectImages/Screenshot%20%28357%29.png)

### Fuel Mix Analysis

![Fuel mix analysis](projectImages/Screenshot%20%28358%29.png)

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Folium
- scikit-learn
- geopy

## Project Structure

```text
EV-Infrastructure-Intelligence/
|-- app/
|   |-- app.py
|   |-- config.py
|   |-- map_utils.py
|   `-- utils.py
|-- data/
|   `-- final_master_report.csv
|-- models/
|   |-- ev_forecast_model.pkl
|   |-- ev_forecast_model_v2.pkl
|   `-- model_metrics.json
|-- notebooks/
|   |-- train_model.ipynb
|   `-- train_model1.ipynb
|-- projectImages/
|   |-- Screenshot (357).png
|   `-- Screenshot (358).png
|-- requirements.txt
`-- README.md
```

## Data Snapshot

- Main dataset: `data/final_master_report.csv`
- Records: 970
- RTO offices covered: 62
- Historical year range used by the app: 2022 to 2025
- Geographic scope: Maharashtra, India

The app derives a simplified `Category` field from raw fuel values and uses that mapping to power the dashboard views.

## Forecasting Approach

The dashboard loads a pre-trained model bundle from `models/ev_forecast_model_v2.pkl` and supports three forecasting modes:

1. Linear Regression
2. Polynomial Regression
3. ARIMA

The forecast is generated at the state level and then apportioned to the selected RTO using that RTO's share of total vehicles for the selected category.

### Stored Model Metrics

Metrics available in `models/model_metrics.json`:

- R2 score: 0.9847
- MAE: 7299.5
- RMSE: 7590.74
- MAPE: 3.03%
- Trained on: 2026-02-05
- Training year range: 2022-2025

## Infrastructure Logic

The app estimates required infrastructure using category-specific ratios defined in `app/config.py`:

- EV: 1 charging station per 10 vehicles
- CNG: 1 CNG pump per 800 vehicles
- HYBRID: 1 specialized garage per 500 vehicles

Risk is classified from the projected vehicles-per-infrastructure ratio:

- Low
- Moderate
- High

Note: Existing infrastructure estimation is currently grounded in the EV public charger baseline. For non-EV categories, the app focuses primarily on gap-based planning rather than a national installed-base estimate.

## App Pages

- `Dashboard`: headline KPIs, forecast trend, and RTO map
- `EV Adoption Analysis`: fuel mix pie chart for the selected RTO
- `Infrastructure Readiness`: projected load per infrastructure unit and risk level
- `ML Predictions`: stored model metrics
- `City Comparison`: compare selected RTOs side by side
- `Data Sources`: source references and active configuration

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd EV-Infrastructure-Intelligence
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the App

Run Streamlit from inside the `app` directory because the current code uses relative paths for the data and model files:

```bash
cd app
streamlit run app.py
```

The app will open locally at:

```text
http://localhost:8501
```

## Configuration

Important application settings live in `app/config.py`, including:

- infrastructure ratios
- Maharashtra RTO coordinate mappings
- EV infrastructure baseline assumptions
- UI theme constants
- data source references

## Notes and Limitations

- The dashboard is designed around Maharashtra RTO data only.
- Forecasting is based on historical registration patterns from 2022-2025.
- Existing installed infrastructure is explicitly estimated only for EV charging.
- Geocoding falls back to predefined coordinates or a Maharashtra center point when lookup fails.

## Data Sources

Configured project sources include:

- Ministry of Road Transport and Highways - Vahan Dashboard
- Bureau of Energy Efficiency
- International Energy Agency - Global EV Outlook 2024

## Future Improvements

- Add scenario planning for policy or incentive changes
- Include more detailed charger type breakdowns
- Add exportable reports for planning teams
- Expand beyond Maharashtra with state-wise configuration packs
- Add automated data refresh and retraining workflows

## License

Add your preferred license here if this repository will be shared publicly.
