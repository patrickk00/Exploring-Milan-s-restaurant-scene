from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import pandas as pd
import string
from rapidfuzz import fuzz
import math


google_df = pd.read_excel('C:/Users/pc/Desktop/progetti data management/data-management-project/google_indirizzo_pulito.xlsx')
trip_df = pd.read_excel('C:/Users/pc/Desktop/progetti data management/data-management-project/trip_indirizzo_pulito_excel.xlsx')


# Define the translation table for removing special characters
trans_table = str.maketrans('', '', string.punctuation)

def format_name_df(df : pd.DataFrame, name_r: string, new_col: string):
    def format_name(row):
        name = row[name_r].replace(" ", "").lower().translate(trans_table)
        name = name.replace("restaurant", "1")
        name = name.replace("ristorante", "2")
        name = name.replace("sushi", "3")
        name = name.replace("kebab", "4")
        name = name.replace("restaurant", "5")
        return name
    df[new_col] = df.apply(format_name, axis=1)
    return df


def format_address_trip(trip_df: pd.DataFrame):
    def format_address(row):
        #remove cap and 'Milano, Italia'
        if  str(row.address_trip) != 'nan':
            address = re.sub(r'\b\d{5}\b.*', '', row['address_trip'])
        else:
            address = 'italy'
        return address.replace(" ", "").lower().translate(trans_table)

    trip_df['formatted_address_trip'] = trip_df.apply(format_address, axis=1)
    return trip_df

def format_address_g(google_df: pd.DataFrame):
    def format_address(row):
        #remove ', Milano'
        string = row['address_g']
        index = string.find(', Milano')
        if index != -1:
            ret = string[:index] + string[index+len(', Milano'):]
            return ret.replace(" ", "").lower().translate(trans_table)
        else:
            return string.replace(" ", "").lower().translate(trans_table)
        
    google_df['formatted_address_g'] = google_df.apply(format_address, axis=1)
    return google_df

def save(results: pd.DataFrame, not_found_trip: pd.DataFrame, not_found_google: pd.DataFrame):
    df = pd.DataFrame(results)
    df.to_csv('../output_integration/integration_definitive.csv', index=False)
    df = pd.DataFrame(not_found_trip)
    df.to_csv('../output_integration/not_found_trip.csv', index=False)
    df = pd.DataFrame(not_found_google)
    df.to_csv('../output_integration/not_found_google.csv', index=False)

def compare_row(row, trip):
        g = row['formatted_name_g']
        t = trip['formatted_name_trip']
        score =  fuzz.token_set_ratio(g, t)

        if score >= 80 or g in t or t in g:
            
            return {'index_g': row['Index'], 'score': score, 'name_g' : row['name_g'], 'formatted_title': row['formatted_name_g'], 'address_g': row['address_g'], 'formatted_address_g': row['formatted_address_g']}

google_df = format_name_df(google_df, 'name_g', 'formatted_name_g')
trip_df = format_name_df(trip_df, 'name_trip', 'formatted_name_trip')

google_df = format_address_g(google_df)
trip_df = format_address_trip(trip_df)
# Use list comprehension to remove spaces, make all characters lowercase, and remove special characters

#google_df.set_index('Index', inplace=True)

results = []
not_found_trip = []
not_found_google = []


#cicliamo su dataset di tripadvisor
for i,t in trip_df.iterrows():
    if i%100 == 0:
        save(results, not_found_trip, not_found_google)
        #break
    #sa ve
    print("ITERATION:", i)

    scores = []
    scores = google_df.apply(compare_row, args=(t,), axis=1)
    scores = [k for k in scores if k is not None]
    if len(scores) != 0:
        mask = google_df.Index == scores[0]['index_g']
        #row_g = google_df[google_df['Index'] == scores[0]['index_g']]
        row_g = google_df[mask].iloc[0]
    #if unique merge
    if len(scores) == 0:

        not_found_trip.append(t)
    elif len(scores) == 1:
        #if scores[0] == 100:
        address_score = 100
        #if not row_g['formatted_address_g'].isin(['italy']).any():
        if not row_g['formatted_address_g']=='italy':
           address_score = fuzz.token_set_ratio(row_g['formatted_address_g'], t['formatted_address_trip'])
        if address_score >= 80:
            results.append({**t, **row_g})
        else:
            not_found_trip.append(t)
        #row_g = google_df.loc[scores[0]['index_g']]
        #google_df = google_df.drop(google_df[google_df['Index'] == row_g['Index']].index)

    elif len(scores) > 1:
        final_score = 0
        final = None
        for sc in scores:
            address_score = 79
            #if not row_g['formatted_address_g'].isin(['italy']).any():
            if not row_g['formatted_address_g']=='italy':

                address_score = fuzz.token_set_ratio(sc['formatted_address_g'], t['formatted_address_trip'])
            if final_score < address_score:
                final_score = address_score
                final = sc
        #row_g = google_df[google_df['Index'] == final['index_g']]
        mask = google_df.Index == final['index_g']
        row_g = google_df[mask].iloc[0]
        #row_g = google_df.loc[final['index_g']]
        google_df = google_df.drop(google_df[google_df['Index'] == final['index_g']].index)
        results.append({**t, **row_g})
    x = 0
df = pd.DataFrame(results)
df.to_excel('integration_definitive.xlsx', index=False)
df = pd.DataFrame(not_found_trip)
df.to_excel('not_found_trip.xlsx', index=False)
df = pd.DataFrame(not_found_google)
df.to_excel('not_found_google.xlsx', index=False)