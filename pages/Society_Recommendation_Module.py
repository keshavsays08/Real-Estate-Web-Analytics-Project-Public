import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import pandas as pd  

st.set_page_config(page_title="Society Recommendation Module", layout="wide")

selected = option_menu(
    menu_title=None,
    options=["Home", "Price Prediction Module", "Analytics Module", "Insights Module", "Society Recommendation Module"],
    icons=["house", "currency-rupee", "clipboard2-data-fill", "lightbulb", "chat-square-quote-fill"],
    default_index=4,
    orientation="horizontal"
)

if selected == "Home":
    st.switch_page("Home.py")
elif selected == "Analytics Module":
    st.switch_page("pages/Analytics_Module.py")
elif selected == "Price Prediction Module":
    st.switch_page("pages/Price_Prediction_Module.py")
elif selected == "Insights Module":
    st.switch_page("pages/Insights_Module.py")

st.title("🏘️ Society Recommendation Module")

# Load data
location_df  = pickle.load(open('datasets/location_distance.pkl', 'rb'))
cosine_sim1  = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2  = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3  = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))

def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = (1*cosine_sim3 + 0.8*cosine_sim2 + 0.8*cosine_sim1)

    sim_scores   = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices    = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores     = [i[1] for i in sorted_scores[1:top_n+1]]
    top_properties = location_df.index[top_indices].tolist()

    return pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

# ==============================
# SECTION 1 — Location Search
# ==============================
st.header('📍 Search Societies by Location & Radius')

col1, col2 = st.columns(2)
with col1:
    location = st.selectbox('Location', sorted(location_df.columns.to_list()))
with col2:
    radius = st.number_input('Radius in Km', min_value=0.5, max_value=50.0, value=5.0, step=0.5)

if st.button('Search'):
    radius_meters = radius * 1000

    result = location_df[location][
        (location_df[location] <= radius_meters) &
        (location_df[location] < 100000)
    ].sort_values()

    if result.empty:
        st.warning(f"No societies found within {radius} km of **{location}**.")
    else:
        st.success(f"Found **{len(result)}** societies within **{radius} km** of **{location}**")
        for society, distance in result.items():
            dist_km = round(distance / 1000, 1)
            st.markdown(f"- **{society}** — {dist_km} km away")

# ==============================
# SECTION 2 — Society Recommender  ✅ outside the button block
# ==============================
st.header('🏠 Recommend Similar Apartments')
st.markdown("Select an apartment to find similar properties based on location, facilities and pricing.")

selected_apartment = st.selectbox('Select an Apartment', sorted(location_df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_apartment)
    st.dataframe(recommendation_df, use_container_width=True)
    
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
