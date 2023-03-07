from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import string
from fuzzywuzzy import fuzz
from tqdm import tqdm
from itertools import product
google_df = pd.read_excel('C:/Users/pc/Desktop/progetti data management/data-management-project/google_indirizzo_pulito.xlsx')
trip_df = pd.read_excel('C:/Users/pc/Desktop/progetti data management/data-management-project/trip_indirizzo_pulito_excel.xlsx')


import pandas as pd
from rapidfuzz import fuzz

# Define a function to compare the names and addresses of each restaurant
def compare_restaurants(row):
    name_trip = row['name_trip']
    name_g = row['name_g']
    name_score = fuzz.ratio(name_trip.lower(), name_g.lower())
    
    if name_score >= 75:
        address_trip = row['address_trip']
        address_g = row['address_g']
        if isinstance(address_trip, str) and isinstance(address_g, str):
            address_score = fuzz.partial_ratio(address_trip.lower(), address_g.lower())
            if address_score >= 75:
                return True
    
    return False


# Apply the comparison function to each row in the two datasets
matches = []
for row in tqdm(product(trip_df.itertuples(), google_df.itertuples()), total=trip_df.shape[0]*google_df.shape[0]):
    row = {'name_trip': row[0].name_trip, 'address_trip': row[0].address_trip, 'name_g': row[1].name_g, 'address_g': row[1].address_g}
    if compare_restaurants(row):
        matches.append(row)

matched_df = pd.DataFrame(matches)

# Create two dataframes for matched and unmatched records
unmatched_trip_df = trip_df[~trip_df['name_trip'].isin(matched_df['name_trip'])]
unmatched_google_df = google_df[~google_df['name_g'].isin(matched_df['name_g'])]

# Save the matched and unmatched records to separate CSV files
matched_df.to_excel('matched_data.xlsx', index=False)
unmatched_trip_df.to_excel('unmatched_trip_data.xlsx', index=False)
unmatched_google_df.to_excel('unmatched_google_data.xlsx', index=False)