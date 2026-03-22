import pandas as pd

file_path = "D:/data-engineering-lab/datasets/raw/Zomato_Mumbai_Dataset.csv"

df = pd.read_csv(
    file_path,
    sep='|',
    engine='python',
    quoting=3,
    on_bad_lines='skip'
)

# 1. Clean column names 
df.columns = (
    df.columns
    .str.replace('"', '', regex=False)
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)

print("Cleaned columns:")
print(df.columns.tolist())

print("\nSample data:")
print(df.head(3))

# 2. Remove quotes 
for col in df.columns:
    df[col] = df[col].astype(str).str.replace('"', '', regex=False)

# 3. Convert numeric columns
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['votes'] = pd.to_numeric(df['votes'], errors='coerce')

print("\nData types after cleaning:")
print(df.dtypes)

print("\nNull counts:")
print(df[['price', 'rating', 'votes']].isna().sum())

# 4. Save cleaned data
output_path = "D:/data-engineering-lab/datasets/processed/zomato_clean_step1.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved cleaned data to: {output_path}")
