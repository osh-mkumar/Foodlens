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
# SAFE PATH HANDLING (IMPORTANT)
# ---------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_path = os.path.join(BASE_DIR, "data")

restaurants = pd.read_csv(os.path.join(data_path, "restaurants.csv"))
cuisines = pd.read_csv(os.path.join(data_path, "cuisines.csv"))
restaurant_cuisines = pd.read_csv(os.path.join(data_path, "restaurant_cuisines.csv"))

# ---------------------------
# CLEAN + MERGE
# ---------------------------
cuisines.rename(columns={"cusine_list": "cuisine_name"}, inplace=True)

df = restaurant_cuisines.merge(restaurants, on="restaurant_id")
df = df.merge(cuisines, on="cuisine_id")

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.markdown("## 🍽️ FoodLens")
st.sidebar.caption("Mumbai Food Intelligence")

page = st.sidebar.selectbox(
    "Navigate",
    ["Overview", "Insights", "Explorer"]
)

st.sidebar.markdown("---")

# Filters
st.sidebar.markdown("### 🎛 Filters")

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

# ---------------------------
# SEARCH
# ---------------------------
search = st.text_input("🔍 Search Restaurant")

# ---------------------------
# FILTERING (FIXED)
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
        color_continuous_scale="reds",
        title="Top Cuisines"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================
# INSIGHTS
# ==========================
elif page == "Insights":

    st.subheader("🚨 Overhyped Restaurants")

    overhyped = df[
        (df["votes"] > 1000) & (df["rating"] < 3.5)
    ][["name", "rating", "votes", "region"]].drop_duplicates(subset=["restaurant_id"])

    st.dataframe(overhyped, use_container_width=True)

    st.divider()

    st.subheader("💎 Best Value Restaurants")

    best_value = df[
        (df["rating"] >= 4.5) & (df["price"] <= 800)
    ][["name", "price", "rating", "region"]].drop_duplicates(subset=["restaurant_id"])

    st.dataframe(best_value, use_container_width=True)

# ==========================
# EXPLORER
# ==========================
elif page == "Explorer":

    st.subheader("🔍 Explore Restaurants")

    unique_restaurants = filtered.drop_duplicates(subset=["restaurant_id"])

    st.write(f"Showing {len(unique_restaurants)} restaurants")

    st.dataframe(
        unique_restaurants[
            ["name", "cuisine_name", "price", "rating", "region"]
        ]
        .sort_values(by="rating", ascending=False),
        use_container_width=True
    )