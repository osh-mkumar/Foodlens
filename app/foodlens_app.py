import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="FoodLens", layout="wide")

# ---------------------------
# STYLE
# ---------------------------
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}
h1, h2, h3 {
    color: #e5e7eb;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD DATA (SAFE PATH)
# ---------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data")

restaurants = pd.read_csv(os.path.join(data_path, "restaurants.csv"))
cuisines = pd.read_csv(os.path.join(data_path, "cuisines.csv"))
restaurant_cuisines = pd.read_csv(os.path.join(data_path, "restaurant_cuisines.csv"))

cuisines.rename(columns={"cusine_list": "cuisine_name"}, inplace=True)

df = restaurant_cuisines.merge(restaurants, on="restaurant_id")
df = df.merge(cuisines, on="cuisine_id")

# ---------------------------
# REGION → COORDS
# ---------------------------
region_coords = {
    "Andheri": (19.1136, 72.8697),
    "Bandra": (19.0596, 72.8295),
    "Borivali": (19.2307, 72.8567),
    "Dadar": (19.0183, 72.8424),
    "Goregaon": (19.1550, 72.8490),
    "Juhu": (19.1075, 72.8263),
    "Malad": (19.1860, 72.8480),
    "Powai": (19.1176, 72.9060),
    "Thane": (19.2183, 72.9781),
    "Vashi": (19.0771, 72.9986)
}

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.markdown("## 🍽️ FoodLens")
st.sidebar.caption("Mumbai Food Intelligence")

page = st.sidebar.selectbox(
    "Navigate",
    ["Overview", "Insights", "Explorer", "Recommendations"]
)

st.sidebar.markdown("---")

# Filters
min_rating = st.sidebar.slider("⭐ Rating", 0.0, 5.0, 0.0)
max_price = st.sidebar.slider("💰 Price", 100, 5000, 5000)

selected_region = st.sidebar.selectbox(
    "📍 Region",
    ["All"] + sorted(df["region"].dropna().unique())
)

selected_cuisine = st.sidebar.selectbox(
    "🍜 Cuisine",
    ["All"] + sorted(df["cuisine_name"].dropna().unique())
)

search = st.text_input("🔍 Search Restaurant")

# ---------------------------
# FILTERING
# ---------------------------
filtered = df[
    ((df["rating"].fillna(0)) >= min_rating) &
    ((df["price"].fillna(9999)) <= max_price)
]

if selected_region != "All":
    filtered = filtered[filtered["region"] == selected_region]

if selected_cuisine != "All":
    filtered = filtered[filtered["cuisine_name"] == selected_cuisine]

if search:
    filtered = filtered[filtered["name"].str.contains(search, case=False, na=False)]

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
# 🍽️ FoodLens  
### Mumbai Food Intelligence Dashboard
""")

st.divider()

# ==========================
# OVERVIEW
# ==========================
if page == "Overview":

    col1, col2, col3 = st.columns(3)

    col1.metric("Restaurants", df["restaurant_id"].nunique())
    col2.metric("Cuisines", df["cuisine_name"].nunique())
    col3.metric("Avg Rating", round(df["rating"].mean(), 2))

    st.divider()

    top_cuisines = (
        df.groupby("cuisine_name")
        .size()
        .reset_index(name="count")
        .sort_values(by="count", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_cuisines,
        x="count",
        y="cuisine_name",
        orientation="h",
        color="count",
        color_continuous_scale="reds"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================
# INSIGHTS
# ==========================
elif page == "Insights":

    st.subheader("📊 Advanced Insights")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.scatter(df, x="price", y="rating", opacity=0.6)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.histogram(df, x="rating", nbins=30)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    fig3 = px.scatter(df, x="votes", y="rating", opacity=0.6)
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    st.subheader("📍 Top Areas by Average Rating")

    area_stats = (
        df.groupby("region")
        .agg(avg_rating=("rating", "mean"), count=("restaurant_id", "nunique"))
        .dropna()
        .sort_values(by="avg_rating", ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        area_stats,
        x="avg_rating",
        y="region",
        orientation="h",
        color="avg_rating",
        color_continuous_scale="greens",
        title="Top Rated Areas"
    )

    st.plotly_chart(fig, use_container_width=True)
# ==========================
# EXPLORER
# ==========================
elif page == "Explorer":

    st.subheader("🔍 Explore Restaurants")

    unique = filtered.drop_duplicates(subset=["restaurant_id"])

    st.write(f"Showing {len(unique)} restaurants")

    st.dataframe(
        unique[["name", "cuisine_name", "price", "rating", "region"]]
        .sort_values(by="rating", ascending=False),
        use_container_width=True
    )

# ==========================
# RECOMMENDATIONS
# ==========================
elif page == "Recommendations":

    st.subheader("🎯 Smart Recommendations")

    budget = st.slider("Budget", 100, 5000, 1000)

    cuisine_choice = st.selectbox(
        "Cuisine",
        sorted(df["cuisine_name"].dropna().unique())
    )

    region_choice = st.selectbox(
        "Your Area",
        sorted(df["region"].dropna().unique())
    )

    rec = df[
        (df["price"].fillna(9999) <= budget) &
        (df["cuisine_name"] == cuisine_choice) &
        (df["region"] == region_choice)
    ]

    rec = rec.drop_duplicates(subset=["restaurant_id"])
    rec = rec.sort_values(by="rating", ascending=False).head(5)

    st.write(f"Top Picks in {region_choice}")

    st.dataframe(
        rec[["name", "price", "rating", "region"]],
        use_container_width=True
    )

# ==========================
# MAP
# ==========================
