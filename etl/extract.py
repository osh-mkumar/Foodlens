import pandas as pd

file_path = "D:/data-engineering-lab/datasets/raw/Zomato_Mumbai_Dataset.csv"

df = pd.read_csv(
    file_path,
    sep='|',
    engine='python',
    quoting=3,        # ignore quotes
    on_bad_lines='skip'  # skip broken rows
)

print("Rows:", df.shape[0])
print("Columns:", df.columns.tolist())
print(df.head(3))
