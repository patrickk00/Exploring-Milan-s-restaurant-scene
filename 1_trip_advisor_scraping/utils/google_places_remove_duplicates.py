import csv
import pandas as pd

df1 = pd.read_csv('../output/google_places.csv')

cleaned_list = []

for row in df1.itertuples():
    print(row)
    place_id = row.place_id
    found = any(d.place_id == place_id for d in cleaned_list)
    if not found:
        cleaned_list.append(row)

df = pd.DataFrame(cleaned_list)
df.to_csv('../output/google_places_no_duplicates.csv', index=False)