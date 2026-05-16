import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Insights Module", layout="wide")

selected = option_menu(
    menu_title=None,
    options=["Home", "Price Prediction Module", "Analytics Module", "Insights Module", "Society Recommendation Module"],
    icons=["house", "currency-rupee", "clipboard2-data-fill", "lightbulb", "chat-square-quote-fill"],
    default_index=3,
    orientation="horizontal"
)

if selected == "Home":
    st.switch_page("Home.py")
elif selected == "Analytics Module":
    st.switch_page("pages/Analytics_Module.py")
elif selected == "Price Prediction Module":
    st.switch_page("pages/Price_Prediction_Module.py")
elif selected == "Society Recommendation Module":
    st.switch_page("pages/Society_Recommendation_Module.py")

st.title("💡 Insights Module")
st.markdown("Understand **how each property attribute impacts the price** in Gurgaon's real estate market.")

# Load data
feature_importance = pickle.load(open('datasets/feature_importance.pkl', 'rb'))
numeric_coeffs     = pickle.load(open('datasets/numeric_feature_importance.pkl', 'rb'))

# ==============================
# PLOT 1 — Overall Feature Importance (numeric only)
# ==============================
st.header('📊 Which Features Impact Price the Most?')
st.markdown("""
This chart shows how much each property attribute influences the price.
A **positive bar** means the feature increases price, a **negative bar** means it decreases price.
The longer the bar, the stronger the impact.
""")

numeric_coeffs_sorted = numeric_coeffs.sort_values('Price_Impact_Pct')

# Clean feature names for display
label_map = {
    'property_type'   : 'Property Type (Flat vs House)',
    'luxury_category' : 'Luxury Category',
    'bedRoom'         : 'Bedrooms',
    'bathroom'        : 'Bathrooms',
    'built_up_area'   : 'Built-up Area',
    'servant room'    : 'Servant Room',
    'furnishing_type' : 'Furnishing Type'
}
numeric_coeffs_sorted['Label'] = numeric_coeffs_sorted['Feature'].map(label_map)

fig1 = px.bar(
    numeric_coeffs_sorted,
    x='Price_Impact_Pct',
    y='Label',
    orientation='h',
    color='Price_Impact_Pct',
    color_continuous_scale='RdYlGn',
    labels={'Price_Impact_Pct': '% Price Impact (per 1 std dev change)', 'Label': ''},
    text=numeric_coeffs_sorted['Price_Impact_Pct'].apply(lambda x: f'{x:+.1f}%')
)
fig1.update_traces(textposition='outside')
fig1.update_layout(
    title=dict(text='Feature Impact on Property Price', font=dict(size=20), x=0.5),
    coloraxis_showscale=False,
    height=450,
    margin=dict(l=0, r=0, t=50, b=0)
)
st.plotly_chart(fig1, use_container_width=True)

# ==============================
# PLOT 2 — Sector Price Impact
# ==============================
st.header('🏙️ Sector Price Impact (vs Baseline)')
st.markdown("""
Each sector's coefficient shows how much **more or less expensive** a property in that sector is 
compared to the baseline sector (Sector A Block Sushant Lok Phase 1).
Positive = more expensive, Negative = cheaper.
""")

sector_coeffs = feature_importance[
    feature_importance['Feature'].str.startswith('sector_')
].copy()
sector_coeffs['Sector'] = sector_coeffs['Feature'].str.replace('sector_', '', regex=False).str.title()
sector_coeffs = sector_coeffs.sort_values('Price_Impact_Pct', ascending=False)

top_n_sector = st.slider('Show Top/Bottom N Sectors', min_value=5, max_value=30, value=15)

top_sectors    = sector_coeffs.head(top_n_sector)
bottom_sectors = sector_coeffs.tail(top_n_sector)
display_sectors = pd.concat([top_sectors, bottom_sectors]).drop_duplicates()

fig2 = px.bar(
    display_sectors.sort_values('Price_Impact_Pct'),
    x='Price_Impact_Pct',
    y='Sector',
    orientation='h',
    color='Price_Impact_Pct',
    color_continuous_scale='RdYlGn',
    labels={'Price_Impact_Pct': '% Price Impact vs Baseline', 'Sector': ''},
    text=display_sectors.sort_values('Price_Impact_Pct')['Price_Impact_Pct'].apply(lambda x: f'{x:+.1f}%')
)
fig2.update_traces(textposition='outside')
fig2.update_layout(
    title=dict(text='Sector Price Premium/Discount vs Baseline', font=dict(size=20), x=0.5),
    coloraxis_showscale=False,
    height=600,
    margin=dict(l=0, r=80, t=50, b=0)
)
st.plotly_chart(fig2, use_container_width=True)

# ==============================
# PLOT 3 — What-If Price Simulator
# ==============================
st.header('🔮 Price Impact Simulator')
st.markdown("""
Select a feature and see **how changing its value affects the price**.
This uses the linear regression model coefficients to estimate percentage price change.
""")

feature_options = {
    'Bedrooms'       : ('bedRoom', 1, 10, 3),
    'Bathrooms'      : ('bathroom', 1, 10, 2),
    'Built-up Area'  : ('built_up_area', 500, 5000, 1500),
    'Luxury Category': ('luxury_category', 0, 3, 1),
    'Furnishing Type': ('furnishing_type', 0, 2, 1),
}

selected_feature_label = st.selectbox('Select Feature to Simulate', list(feature_options.keys()))
col_name, min_val, max_val, default_val = feature_options[selected_feature_label]

col1, col2 = st.columns(2)
with col1:
    val_before = st.number_input(f'Current {selected_feature_label}', min_value=float(min_val), max_value=float(max_val), value=float(default_val))
with col2:
    val_after  = st.number_input(f'New {selected_feature_label}', min_value=float(min_val), max_value=float(max_val), value=float(default_val + 1))

# Get coefficient for this feature
coeff_row = numeric_coeffs[numeric_coeffs['Feature'] == col_name]
if not coeff_row.empty:
    coeff     = coeff_row['Coefficient'].values[0]
    std_X     = feature_importance  # we need original std — approximate with raw change

    # Approximate: delta in log(price) = coeff_unscaled * delta_X
    # Get std of feature from scaler (approximate via notebook values)
    feature_std_map = {
        'bedRoom'        : 1.244,
        'bathroom'       : 1.38,
        'built_up_area'  : 786.0,
        'luxury_category': 1.1,
        'furnishing_type': 0.82,
    }
    std_x = feature_std_map.get(col_name, 1.0)

    # Unscaled coefficient = scaled_coeff / std_x * std_y
    std_y = 0.557  # from notebook: y_log.std()
    unscaled_coeff = coeff / std_x * std_y  # approx

    delta = val_after - val_before
    log_price_change = unscaled_coeff * delta
    pct_change = (np.expm1(log_price_change)) * 100

    if pct_change > 0:
        st.success(f"Increasing **{selected_feature_label}** from **{val_before:.0f}** to **{val_after:.0f}** → Price increases by approximately **+{pct_change:.1f}%**")
    elif pct_change < 0:
        st.error(f"Changing **{selected_feature_label}** from **{val_before:.0f}** to **{val_after:.0f}** → Price decreases by approximately **{pct_change:.1f}%**")
    else:
        st.info("No change in price.")

    # Visual gauge
    fig3 = px.bar(
        x=[pct_change],
        y=['Price Change'],
        orientation='h',
        color=[pct_change],
        color_continuous_scale='RdYlGn',
        range_color=[-30, 30],
        labels={'x': '% Price Change', 'y': ''}
    )
    fig3.update_layout(
        coloraxis_showscale=False,
        height=150,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    st.plotly_chart(fig3, use_container_width=True)
    
st.markdown("---")

# ── Tech stack ────────────────────────────────────────────────────────────────
st.caption("Tech stack used &nbsp; Python · Streamlit · scikit-learn · Plotly · GeoPandas · Pandas · NumPy · WordCloud · OSMnx")
st.caption("Data sourced from real Gurgaon property listings. Predictions are estimates and should be used as a reference, not a valuation.")
st.caption(
    "📋 Disclaimer: The property data used in this application was collected from 99acres.com "
    "strictly for educational and academic purposes. This project is not affiliated with, endorsed by, "
    "or intended for any commercial use. No proprietary data has been redistributed or monetised."
)
st.caption("Built with ❤️ for Data Science & Analytics by KESHAV GAIROLA")
