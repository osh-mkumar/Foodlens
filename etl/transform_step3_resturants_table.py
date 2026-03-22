import pandas as pd

# Load cleaned data
df = pd.read_csv(
    "D:/data-engineering-lab/datasets/processed/zomato_clean_step1.csv"
)

# Add restaurant_id (must match what we used earlier!)
df['restaurant_id'] = df.index + 1

# Select ONLY columns needed for restaurants table
restaurants_df = df[[
    'restaurant_id',
    'name',
    'price',
    'city',
    'region',
    'timing',
    'rating_type',
    'rating',
    'votes',
    'url'
]]

# Save final version
restaurants_df.to_csv(
    "D:/data-engineering-lab/datasets/processed/restaurants.csv",
    index=False
)

print("Restaurants table file created")
print("Rows:", restaurants_df.shape[0])
print("Columns:", restaurants_df.columns.tolist())