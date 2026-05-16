import streamlit as st
from streamlit_option_menu import option_menu
import joblib
import pickle
import pandas as pd
import numpy as np
st.set_page_config(page_title="Price Prediction", layout="wide")

# Load files
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

pipeline = joblib.load('pipeline.pkl')

# Same navbar on every page for consistent navigation
selected = option_menu(
    menu_title=None,
    options=["Home", "Price Prediction Module", "Analytics Module", "Insights Module","Society Recommendation Module"],
    icons=["house", "currency-rupee", "clipboard2-data-fill", "lightbulb", "chat-square-quote-fill"],
    default_index=1,  # <-- change this per page (0=Home, 1=Price, 2=Analytics, 3=Insights)
    orientation="horizontal"
)

if selected == "Home":
    st.switch_page("Home.py")
elif selected == "Analytics Module":
    st.switch_page("pages/Analytics_Module.py")
elif selected == "Society Recommendation Module":
    st.switch_page("pages/Society_Recommendation_Module.py")
elif selected == "Insights Module":
    st.switch_page("pages/Insights_Module.py")

st.title("Price Prediction Module")
st.header('Enter your inputs for Property Price Prediction in Gurugram')
col1, col2, col3 = st.columns(3)

with col1:
    property_type   = st.selectbox('Property Type', ['flat', 'ind-house'])
with col2:
    sector          = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
with col3:
    balcony         = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))

col4, col5, col6 = st.columns(3)

with col4:
    property_age    = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))
with col5:
    luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
with col6:
    floor_category  = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

col7, col8, col9 = st.columns(3)

with col7:
    facing          = st.selectbox('Facing', sorted(df['facing'].unique().tolist()))
with col8:
    bedRoom         = float(st.selectbox('Bedrooms', sorted(df['bedRoom'].unique().tolist())))
with col9:
    bathroom        = float(st.selectbox('Bathrooms', sorted(df['bathroom'].unique().tolist())))

col10, col11, col12 = st.columns(3)

with col10:
    built_up_area   = float(st.number_input('Built Up Area (In square feet)', min_value=0.0))
with col11:
    servant_room    = float(st.selectbox('Servant Room', [0.0, 1.0]))
with col12:
    store_room      = float(st.selectbox('Store Room', [0.0, 1.0]))

col13, col14, col15 = st.columns(3)

with col13:
    furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
if st.button('Predict'):
    data = [[property_type, sector, balcony, property_age,
             luxury_category, floor_category, facing, bedRoom, bathroom,
             built_up_area, servant_room, store_room, furnishing_type]]

    columns = ['property_type', 'sector', 'balcony', 'agePossession',
               'luxury_category', 'floor_category', 'facing', 'bedRoom', 'bathroom',
               'built_up_area', 'servant room', 'store room', 'furnishing_type']

    one_df = pd.DataFrame(data, columns=columns)
    st.dataframe(one_df)

    base_price = np.expm1(pipeline.predict(one_df))[0]
    low  = base_price - 0.22
    high = base_price + 0.22

    st.success("The price of the property is between {} Cr and {} Cr".format(round(low, 2), round(high, 2)))
    
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
