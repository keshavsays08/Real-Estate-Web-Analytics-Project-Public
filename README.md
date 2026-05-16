# 🏙️ Gurgaon Real Estate Analytics Platform

> An end-to-end machine learning platform for property price prediction, market analytics, and society recommendations in Gurgaon, India.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4+-orange?logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Project Overview

This project is a **multi-module real estate intelligence platform** built for the Gurgaon property market. It combines data scraping, feature engineering, machine learning, and an interactive Streamlit dashboard to help buyers, sellers, and investors make data-driven decisions.

The platform covers:
- **Price Prediction** — Predict property prices using a tuned Random Forest model (R² = 0.91)
- **Market Analytics** — Interactive maps, charts, and word clouds for market understanding
- **Insights Module** — Feature importance and price sensitivity analysis via OLS regression
- **Society Recommender** — Content-based filtering to recommend similar properties

---

## 🗂️ Project Structure

```
real_estate_project/
│
├── S0_data_gathering/          # Web scraping scripts (99acres)
├── S1_data_cleaning/           # Raw data cleaning notebooks
├── S2_feature_engineering/     # Feature creation and encoding
├── S3_EDA/                     # Exploratory Data Analysis
├── S4_outliers_treatment/      # Outlier detection and removal
├── S5_feature_selection/       # Feature selection experiments
├── S6_model_building/
│   └── main_model_building.ipynb   # Model training, GridSearchCV, saving
│
└── S7_streamlit_deployment/
    ├── Home.py                          # Main entry point
    ├── utils.py                         # Shared utility classes
    ├── pipeline.pkl                     # Trained ML pipeline
    ├── df.pkl                           # Feature reference dataframe
    ├── datasets/
    │   ├── data_viz1.csv                # Analytics dataset with lat/lon
    │   ├── gurgaon_properties_post_feature_selection_v2.csv
    │   ├── sectors_geo.geojson          # Sector boundary polygons
    │   ├── wordcloud_df.parquet         # Features for word cloud
    │   ├── location_distance.pkl        # Society-to-landmark distances
    │   ├── cosine_sim1.pkl              # Facility similarity matrix
    │   ├── cosine_sim2.pkl              # Price similarity matrix
    │   ├── cosine_sim3.pkl              # Location similarity matrix
    │   └── feature_importance.pkl       # OLS regression coefficients
    └── pages/
        ├── Price_Prediction_Module.py
        ├── Analytics_Module.py
        ├── Insights_Module.py
        └── Society_Recommendation_Module.py
```

---

## 🔧 Tech Stack

| Layer | Tools |
|---|---|
| **Language** | Python 3.12 |
| **ML & Stats** | Scikit-learn, Statsmodels, NumPy, Pandas |
| **Web Scraping** | Requests, BeautifulSoup4 |
| **Geocoding** | GeoPy (Nominatim), OSMnx, GeoPandas |
| **Visualization** | Plotly Express, Matplotlib, WordCloud |
| **Dashboard** | Streamlit, streamlit-option-menu |
| **Serialization** | Joblib, Pickle, Parquet |

---

## 🤖 Machine Learning Pipeline

### Model: Random Forest Regressor

| Metric | Value |
|---|---|
| R² Score (CV) | **0.91** |
| CV Strategy | K-Fold (k=10) |
| Hyperparameter Tuning | GridSearchCV |
| Target Variable | log1p(price) → expm1 for output |

### Preprocessing Pipeline (sklearn Pipeline)

```
ColumnTransformer
├── StandardScaler          → [bedRoom, bathroom, built_up_area, servant room, store room]
├── OrdinalEncoder          → [property_type, balcony, agePossession, luxury_category,
│                              floor_category, facing, furnishing_type]
├── OneHotEncoder           → [agePossession]
└── TargetEncoder           → [sector]
         ↓
RandomForestRegressor(n_estimators=500)
```

### Algorithms Benchmarked

Linear Regression, Ridge, Lasso, SVR, Decision Tree, **Random Forest**, Extra Trees, Gradient Boosting, XGBoost, MLP Neural Network (10+ total)

---

## 📊 Modules

### 1. 💰 Price Prediction Module
- User inputs 13 property attributes
- Pipeline preprocesses and predicts log-price
- Output: price range in Crores (± 0.22 Cr confidence band)

### 2. 📍 Analytics Module
- **Bubble Map** — sector-wise price per sqft with bubble size = avg area
- **Choropleth Map** — filled sector boundaries colored by price (OSMnx GeoJSON)
- **Word Cloud** — most common property features, filterable by sector
- **Scatter Plot** — Built-up area vs Price, colored by BHK
- **Pie Chart** — BHK distribution, filterable by sector and property type
- **Box Plot** — Price distribution by BHK configuration
- **Bar Chart** — Top N most expensive sectors, sortable by multiple metrics

### 3. 💡 Insights Module
- OLS Linear Regression on log-transformed prices
- Standardized coefficients show **relative feature importance**
- Sector premium/discount chart vs baseline sector
- **What-If Simulator** — change any attribute and see % price impact

### 4. 🏘️ Society Recommendation Module
- **Location Search** — find societies within X km of any landmark
- **Similarity Recommender** — cosine similarity across 3 matrices:
  - Location distances (769 landmarks)
  - Property facilities
  - Price characteristics

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install streamlit streamlit-option-menu scikit-learn pandas numpy \
            plotly geopandas osmnx geopy joblib wordcloud \
            category_encoders statsmodels
```

### Run Locally

```bash
git clone https://github.com/yourusername/gurgaon-real-estate
cd gurgaon-real-estate/S7_streamlit_deployment
streamlit run Home.py
```

---

## 📈 Key Results

- **0.91 R²** on 10-fold cross-validation using Random Forest
- **133 sectors** geocoded with latitude/longitude
- **246 societies** in the recommendation engine
- **769 landmarks** used for location-based distance matrix
- **3,274 properties** in the final cleaned dataset

---

## 🗺️ Data Pipeline

```
Web Scraping (99acres)
        ↓
Raw Data Cleaning (nulls, types, deduplication)
        ↓
Feature Engineering (luxury score, floor category, age bucket)
        ↓
EDA + Outlier Treatment (IQR, domain knowledge)
        ↓
Feature Selection (correlation, VIF, importance)
        ↓
Model Training + GridSearchCV (Random Forest)
        ↓
Streamlit Deployment (5-module dashboard)
```

---

## 📁 Dataset

Data was scraped from 99acres.com for Gurgaon properties. The final dataset contains:

| Column | Description |
|---|---|
| property_type | flat / ind-house |
| sector | 133 unique sectors |
| bedRoom | Number of bedrooms |
| bathroom | Number of bathrooms |
| built_up_area | Area in sq ft |
| balcony | Number of balconies |
| agePossession | New / Relatively New / Moderately Old / Old / Under Construction |
| luxury_category | Class A / B / C / D |
| floor_category | Low / Mid / High floor |
| facing | Cardinal direction |
| servant room | 0 or 1 |
| store room | 0 or 1 |
| furnishing_type | Furnished / Semi / Unfurnished |
| price | Target variable in Crores |

---

## 🙏 Acknowledgements

- Property data sourced from 99acres.com
- Geocoding via OpenStreetMap Nominatim
- Sector boundary polygons via OSMnx / OpenStreetMap contributors

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
