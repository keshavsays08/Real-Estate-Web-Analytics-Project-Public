import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import osmnx as ox
import json
from streamlit_option_menu import option_menu
import ast
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analytics Module", layout="wide")
# Same navbar on every page for consistent navigation
selected = option_menu(
    menu_title=None,
    options=["Home", "Price Prediction Module", "Analytics Module", "Insights Module","Society Recommendation Module"],
    icons=["house", "currency-rupee", "clipboard2-data-fill", "lightbulb", "chat-square-quote-fill"],
    default_index=2,  # <-- change this per page (0=Home, 1=Price, 2=Analytics, 3=Insights)
    orientation="horizontal"
)

if selected == "Home":
    st.switch_page("Home.py")
elif selected == "Price Prediction Module":
    st.switch_page("pages/Price_Prediction_Module.py")
elif selected == "Society Recommendation Module":
    st.switch_page("pages/Society_Recommendation_Module.py")
elif selected == "Insights Module":
    st.switch_page("pages/Insights_Module.py")

st.title("Analytics Module")

# --- Load Data ---
new_df = pd.read_csv('datasets/data_viz1.csv')
normal_plots_df = pd.read_csv('datasets/gurgaon_properties_post_feature_selection_v2.csv')
group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()
group_df_clean = group_df.dropna(subset=['latitude', 'longitude', 'built_up_area'])

# ==============================
# PLOT 1 — Bubble Map
# ==============================
st.header('📍 Sector Price Map (Bubble View)')
st.markdown("""
The bubble map plots each Gurgaon sector as a circle on an interactive map. The **size** of each bubble 
represents the average built-up area of properties in that sector, while the **color** (blue → green → yellow → red) 
indicates the price per sqft — cooler colors mean affordable, warmer colors mean premium pricing. 
Central sectors near **IFFCO Chowk, Sector 43, and Sector 42** show warmer colors, reflecting higher demand. 
This view is great for **comparing individual sectors** at a glance.
""")

fig1 = px.scatter_mapbox(
    group_df_clean,
    lat='latitude',
    lon='longitude',
    color='price_per_sqft',
    size='built_up_area',
    color_continuous_scale='Turbo',
    size_max=35,
    zoom=11,
    mapbox_style="open-street-map",
    hover_name=group_df_clean.index,
    hover_data={
        'price_per_sqft': ':.0f',
        'built_up_area': ':.0f',
        'price': ':.2f',
        'latitude': False,
        'longitude': False
    },
    labels={'price_per_sqft': '₹/sqft', 'price': 'Avg Price (Cr)', 'built_up_area': 'Avg Area (sqft)'}
)
fig1.update_traces(marker=dict(opacity=0.75))
fig1.update_layout(
    title=dict(text='🏙️ Gurgaon Sector - Price per Sqft Map', font=dict(size=20), x=0.5),
    coloraxis_colorbar=dict(title='₹/sqft', thickness=15, len=0.6, tickformat=',.0f'),
    margin=dict(l=0, r=0, t=50, b=0),
    height=600
)
st.plotly_chart(fig1, use_container_width=True)

# ==============================
# PLOT 2 — Choropleth Map
# ==============================
# ✅ Load pre-saved GeoJSON — instant, no OSM fetching!
sectors_gdf = gpd.read_file('datasets/sectors_geo.geojson')

# Drop duplicate columns from geojson before merging
cols_to_drop = [c for c in sectors_gdf.columns if c in ['price_per_sqft', 'price', 'built_up_area']]
sectors_gdf = sectors_gdf.drop(columns=cols_to_drop)

# Now merge cleanly — no _x/_y suffixes
sectors_gdf = sectors_gdf.merge(
    group_df_clean.reset_index()[['sector', 'price_per_sqft', 'price', 'built_up_area']],
    on='sector'
)
geojson = json.loads(sectors_gdf.to_json())

# --- Choropleth ---
st.header('🗺️ Sector Price Heatmap')
st.markdown("""
The choropleth map fills each sector's actual geographic boundary with a color representing its average 
price per sqft. Premium zones are clearly visible as warm-colored patches concentrated in **central Gurgaon 
and Golf Course Road corridors**, while outer sectors appear in cooler shades. This view communicates 
**which areas of the city are expensive vs affordable** by showing actual sector boundaries.
""")

fig = px.choropleth_mapbox(
    sectors_gdf,
    geojson=geojson,
    locations=sectors_gdf.index,
    color='price_per_sqft',
    color_continuous_scale='Turbo',
    range_color=[5000, 40000],
    mapbox_style='open-street-map',
    zoom=11,
    center={"lat": 28.4595, "lon": 77.0266},
    opacity=0.65,
    hover_name='sector',
    hover_data={
        'price_per_sqft': ':.0f',
        'price':          ':.2f',
        'built_up_area':  ':.0f'
    },
    labels={
        'price_per_sqft': '₹/sqft',
        'price':          'Avg Price (Cr)',
        'built_up_area':  'Avg Area (sqft)'
    }
)
fig.update_layout(
    title=dict(text='🏙️ Gurgaon Sector Price Choropleth', font=dict(size=20), x=0.5),
    coloraxis_colorbar=dict(
        title='₹/sqft', thickness=15, len=0.6, tickformat=',.0f',
        tickvals=[5000, 10000, 20000, 30000, 40000],
        ticktext=['5k', '10k', '20k', '30k', '40k+']
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    height=650
)
st.plotly_chart(fig, use_container_width=True)

# ==============================
# PLOT 7 — Top 10 Most Expensive Sectors (Bar Chart)
# ==============================
st.header('📊 Top 10 Most Expensive Sectors')
st.markdown("""
This bar chart highlights the **10 most expensive sectors in Gurgaon** ranked by average 
price per sqft. The color gradient (cool → warm) further reinforces the pricing hierarchy — 
sectors at the top with warmer shades command the highest premiums. Use this to quickly 
identify **premium micro-markets** and benchmark a sector's standing in the city's 
pricing landscape.
""")

col1, col2 = st.columns(2)

with col1:
    top_n = st.slider('Number of Top Sectors', min_value=5, max_value=20, value=10, step=1)

with col2:
    sort_by = st.selectbox('Sort By', ['price_per_sqft', 'price', 'built_up_area'],
                           format_func=lambda x: {
                               'price_per_sqft': 'Price per Sqft (₹)',
                               'price': 'Average Price (Cr)',
                               'built_up_area': 'Average Built-up Area (sqft)'
                           }[x])

top_sectors_df = group_df.nlargest(top_n, sort_by).reset_index()

fig7 = px.bar(
    top_sectors_df,
    x='sector',
    y=sort_by,
    color=sort_by,
    color_continuous_scale='Turbo',
    labels={
        'sector': 'Sector',
        'price_per_sqft': '₹ / sqft',
        'price': 'Avg Price (Cr)',
        'built_up_area': 'Avg Area (sqft)'
    },
    text=top_sectors_df[sort_by].apply(
        lambda v: f'₹{v:,.0f}' if sort_by == 'price_per_sqft'
        else (f'{v:.2f} Cr' if sort_by == 'price' else f'{v:,.0f} sqft')
    )
)

fig7.update_traces(
    textposition='outside',
    marker=dict(opacity=0.85, line=dict(width=0))
)

fig7.update_layout(
    title=dict(
        text=f'🏙️ Top {top_n} Sectors by {sort_by.replace("_", " ").title()}',
        font=dict(size=22),
        x=0.5
    ),
    xaxis=dict(tickangle=-35, title='Sector'),
    yaxis=dict(title=sort_by.replace('_', ' ').title()),
    coloraxis_colorbar=dict(
        title='₹/sqft' if sort_by == 'price_per_sqft' else sort_by,
        thickness=15,
        len=0.6,
        tickformat=',.0f'
    ),
    margin=dict(l=0, r=0, t=60, b=80),
    height=600,
    showlegend=False
)

st.plotly_chart(fig7, use_container_width=True)

# ==============================
# PLOT 3 — WordCloud Map
# ==============================

st.header('🏠 Property Features Word Cloud')
st.markdown("""
The word cloud shows the most commonly listed features and amenities across Gurgaon properties. 
Larger words appear more frequently in property listings — giving a quick snapshot of what features 
are most common in the market.
""")

# Load parquet
init_df = pd.read_parquet('datasets/wordcloud_df.parquet')

# Normalize
init_df['sector'] = init_df['sector'].str.strip().str.lower()
new_df['sector']  = new_df['sector'].str.strip().str.lower()

# 🎯 Dropdown for sector selection
sector_list = sorted(init_df['sector'].dropna().unique())
selected_sectors = st.multiselect("Select Sector(s)", sector_list)

# If nothing selected → use all sectors
if selected_sectors:
    filtered_df = init_df[init_df['sector'].isin(selected_sectors)]
else:
    filtered_df = init_df

# Build word frequency dict
feature_text = {}
for item in filtered_df['features'].dropna().apply(lambda x: x.split(',')):
    for feature in item:
        feature = feature.strip()
        if feature:
            feature_text[feature] = feature_text.get(feature, 0) + 1

# Generate wordcloud
wordcloud = WordCloud(
    width=800, height=400,
    background_color='white',
    colormap='turbo',
    max_words=100
).generate_from_frequencies(feature_text)

# Display
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig)

# ==============================
# PLOT 4 - Price Vs. Area
# ==============================
st.header('💰 Price Vs. Built-up Area')
st.markdown("""
This scatter plot shows the relationship between **built-up area (sqft)** and **price (Cr)** 
for individual properties across Gurgaon. Each point represents a property, colored by the 
number of **bedrooms** — helping identify how size, price, and bedroom count relate to each other. 
Larger properties with more bedrooms generally command higher prices, though location plays a 
significant role too.
""")

property_type = st.selectbox('Select Property Type', ['All', 'flat', 'ind-house'])

# Filter based on selection
if property_type == 'All':
    filtered_df = normal_plots_df
else:
    filtered_df = normal_plots_df[normal_plots_df['property_type'] == property_type]

fig4 = px.scatter(
    filtered_df,
    x='built_up_area',
    y='price',
    color='bedRoom',
    color_continuous_scale='Turbo',
    labels={
        'built_up_area': 'Built-up Area (sqft)',
        'price': 'Price (Cr)',
        'bedRoom': 'Bedrooms'
    },
    hover_data=['bedRoom', 'price', 'built_up_area']
)
fig4.update_traces(marker=dict(opacity=0.5, size=5))
fig4.update_layout(
    title=dict(
        text=f'🏙️ Built-up Area vs Price — {property_type}',
        font=dict(size=22),
        x=0.5
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    height=600
)
st.plotly_chart(fig4, use_container_width=True)

# ==============================
# PLOT 5 - BHK Pie Chart
# ==============================
st.header('🛏️ BHK Distribution')
st.markdown("""
This pie chart shows the distribution of properties by number of **bedrooms (BHK)** across Gurgaon. 
It gives a quick snapshot of what bedroom configurations are most common in the market — 
helping buyers understand supply and developers understand demand.
""")

col1, col2 = st.columns(2)

with col1:
    property_type_pie = st.selectbox('Select Property Type ', ['All', 'flat', 'ind-house'])

with col2:
    sector_list_pie = ['All'] + sorted(normal_plots_df['sector'].dropna().unique().tolist())
    selected_sector_pie = st.selectbox('Select Sector', sector_list_pie)

# Filter
pie_df = normal_plots_df.copy()

if property_type_pie != 'All':
    pie_df = pie_df[pie_df['property_type'] == property_type_pie]

if selected_sector_pie != 'All':
    pie_df = pie_df[pie_df['sector'] == selected_sector_pie]

fig5 = px.pie(
    pie_df,
    names='bedRoom',
    color_discrete_sequence=px.colors.sequential.Turbo,
    hole=0.3,
)
fig5.update_traces(textposition='inside', textinfo='percent+label')
fig5.update_layout(
    title=dict(
        text=f'🏙️ BHK Distribution — {property_type_pie} | {selected_sector_pie}',
        font=dict(size=22),
        x=0.5
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    height=600
)
st.plotly_chart(fig5, use_container_width=True)

# ==============================
# PLOT 6 - BHK Price Box Plot
# ==============================
st.header('📦 Price Distribution by BHK')
st.markdown("""
This box plot shows how **property prices vary across different bedroom configurations (BHK)** in Gurgaon.
The box represents the interquartile range (middle 50% of prices), the line inside is the median price,
and the whiskers show the overall spread. Outliers appear as individual dots.
This helps understand the typical price range you can expect for each BHK type.
""")

col1, col2 = st.columns(2)

with col1:
    property_type_box = st.selectbox('Select Property Type  ', ['All', 'flat', 'ind-house'])

with col2:
    max_bhk = st.slider('Max Bedrooms', min_value=2, max_value=10, value=4)

# Filter
box_df = normal_plots_df.copy()

if property_type_box != 'All':
    box_df = box_df[box_df['property_type'] == property_type_box]

box_df = box_df[box_df['bedRoom'] <= max_bhk]

fig6 = px.box(
    box_df,
    x='bedRoom',
    y='price',
    color='bedRoom',
    color_discrete_sequence=px.colors.sequential.Turbo,
    labels={
        'bedRoom': 'Bedrooms (BHK)',
        'price': 'Price (Cr)'
    },
    points='outliers'  # ✅ show outlier dots
)
fig6.update_layout(
    title=dict(
        text=f'🏙️ Price Distribution by BHK — {property_type_box}',
        font=dict(size=22),
        x=0.5
    ),
    showlegend=False,
    margin=dict(l=0, r=0, t=50, b=0),
    height=600
)
st.plotly_chart(fig6, use_container_width=True)

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

