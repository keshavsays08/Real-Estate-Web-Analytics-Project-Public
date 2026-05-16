import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Gurgaon Real Estate Intelligence", layout="wide")

selected = option_menu(
    menu_title=None,
    options=["Home", "Price Prediction Module", "Analytics Module", "Insights Module", "Society Recommendation Module"],
    icons=["house", "currency-rupee", "clipboard2-data-fill", "lightbulb", "chat-square-quote-fill"],
    default_index=0,
    orientation="horizontal"
)

if selected == "Price Prediction Module":
    st.switch_page("pages/Price_Prediction_Module.py")
elif selected == "Analytics Module":
    st.switch_page("pages/Analytics_Module.py")
elif selected == "Insights Module":
    st.switch_page("pages/Insights_Module.py")
elif selected == "Society Recommendation Module":
    st.switch_page("pages/Society_Recommendation_Module.py")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("🗺️ &nbsp; **Gurgaon, Haryana**")
st.title("Real-Estate Analytics Web-App for **Gurgaon**")
st.markdown("""
An end-to-end data science application covering price prediction, sector analytics, 
market insights, and society recommendations — built on real property listing data 
from across Gurgaon.
""")

# ── Stats ─────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Property listings", "3,500+")
col2.metric("Sectors covered", "60+")
col3.metric("Modules", "4")

st.markdown("---")

# ── Module cards ──────────────────────────────────────────────────────────────
st.subheader("Explore modules")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### 💰 Price Prediction")
        st.markdown("Enter property details and get an estimated price range using a trained regression pipeline.")
        st.caption("13 input features &nbsp;·&nbsp; Flat & ind-house &nbsp;·&nbsp; ±0.22 Cr range")
        if st.button("Open →", key="btn_price"):
            st.switch_page("pages/Price_Prediction_Module.py")

    with st.container(border=True):
        st.markdown("#### 💡 Insights")
        st.markdown("Understand which features drive property prices and simulate how changes affect valuation.")
        st.caption("Feature importance &nbsp;·&nbsp; Sector premiums &nbsp;·&nbsp; What-if simulator")
        if st.button("Open →", key="btn_insights"):
            st.switch_page("pages/Insights_Module.py")

with col2:
    with st.container(border=True):
        st.markdown("#### 📊 Analytics")
        st.markdown("Explore sector-level price maps, BHK distributions, area vs price trends, and amenity word clouds.")
        st.caption("Bubble & choropleth maps &nbsp;·&nbsp; 7 interactive charts")
        if st.button("Open →", key="btn_analytics"):
            st.switch_page("pages/Analytics_Module.py")

    with st.container(border=True):
        st.markdown("#### 🏘️ Society Recommendations")
        st.markdown("Find societies within a radius of any landmark, or get similar apartment recommendations.")
        st.caption("Location search &nbsp;·&nbsp; Cosine similarity")
        if st.button("Open →", key="btn_society"):
            st.switch_page("pages/Society_Recommendation_Module.py")

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
