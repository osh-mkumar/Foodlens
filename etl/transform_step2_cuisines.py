import pandas as pd

# Load cleaned data
df = pd.read_csv(
    "D:/data-engineering-lab/datasets/processed/zomato_clean_step1.csv"
)

# Create restaurant ID
df['restaurant_id'] = df.index + 1

# Split cuisines
df['cusine_category'] = df['cusine_category'].fillna('')
df['cusine_list'] = df['cusine_category'].str.split(',')

# Explode into rows
restaurant_cuisine_df = df[['restaurant_id', 'cusine_list']].explode('cusine_list')

# Clean cuisine names
restaurant_cuisine_df['cusine_list'] = (
    restaurant_cuisine_df['cusine_list']
    .str.strip()
    .str.lower()
)

# Remove empty cuisines
restaurant_cuisine_df = restaurant_cuisine_df[
    restaurant_cuisine_df['cusine_list'] != ''
]

# Create cuisines table
cuisines_df = (
    restaurant_cuisine_df[['cusine_list']]
    .drop_duplicates()
    .reset_index(drop=True)
)
cuisines_df['cuisine_id'] = cuisines_df.index + 1

# Create mapping table
restaurant_cuisine_df = restaurant_cuisine_df.merge(
    cuisines_df,
    left_on='cusine_list',
    right_on='cusine_list',
    how='left'
)

restaurant_cuisine_df = restaurant_cuisine_df[
    ['restaurant_id', 'cuisine_id']
]

# Save outputs
cuisines_df.to_csv(
    "D:/data-engineering-lab/datasets/processed/cuisines.csv",
    index=False
)

restaurant_cuisine_df.to_csv(
    "D:/data-engineering-lab/datasets/processed/restaurant_cuisines.csv",
    index=False
)

print("Cuisine normalization complete")
print("Total cuisines:", cuisines_df.shape[0])
print("Total mappings:", restaurant_cuisine_df.shape[0])
