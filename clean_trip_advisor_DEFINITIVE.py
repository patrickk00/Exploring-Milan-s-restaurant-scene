from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

from fuzzywuzzy import fuzz
import string

name1 = "Sauris & borc da bria"
name2 = "Hosteria Sauris & Borc - da BRIA"

score = fuzz.token_set_ratio(name1, name2)

if score >= 80: 
    print("The names are similar.")
else:
    print("The names are not similar.")

google_df = pd.read_csv('./output/google_places_cleaned_DEFINITIVE.csv')
trip_df = pd.read_csv('./output/trip_advisor_DEFINITIVE.csv')


#TRIP ADVISOR
#remove count in trip advisor restaurant's names:
trip_df['title'] = trip_df['title'].str.replace('^\d+, ', '')
#change euro symbols
trip_df['expensive'] = trip_df['expensive'].replace({'€': 1, '€€': 2,'€ - €€': 1.5,'€€€': 3, '€€ - €€€': 2.5, '€€€€':4 , '€€€ - €€€€':3.5, '€€€€ - €€€€€':4.5,'€€€€€':5 })
#rename columns
new_col_names = { 
                  'id':'id_trip',
                  'title':'name_trip',
                  'r_bubbles':'rating_trip',
                  'r_number':'total_reviews_trip',
                  'cook_type':'cook_type_trip',
                  'expensive': 'price_level_trip', 
                  'address_trip':'address_trip',
                  'revews': 'reviews_trip'}

# Rename the columns in the DataFrame
trip_df= trip_df.rename(columns=new_col_names)

trip_df['rating_trip'] = trip_df['rating_trip'].str.extract(r'(\d\.\d|\d)', expand=False)
trip_df['total_reviews_trip'] = trip_df['total_reviews_trip'].str.extract(r'(\d+)', expand=False)
trip_df = trip_df.iloc[:, 1:]
trip_df.drop_duplicates('id_trip')
print(trip_df.columns.to_list())

trip_df.to_csv('./output/trip_advisor_cleaned_DEFINITIVE.csv', index=False)


