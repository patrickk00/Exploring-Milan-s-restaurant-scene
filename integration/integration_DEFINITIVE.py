from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import pandas as pd
import string
from fuzzywuzzy import fuzz


google_df = pd.read_csv('../definitive_files_integration/google_places_cleaned_DEFINITIVE.csv')
trip_df = pd.read_csv('../definitive_files_integration/trip_advisor_cleaned_DEFINITIVE.csv')

# Define the translation table for removing special characters
trans_table = str.maketrans('', '', string.punctuation)

def format_name_df(df : pd.DataFrame, name: string, new_col: string):
    def format_name(row):
        name = row[name].replace(" ", "").lower().translate(trans_table)
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
        address = re.sub(r'\b\d{5}\b.*', '', row['address_trip'])
        return address.replace(" ", "").lower().translate(trans_table)

    trip_df['formatted_address_trip'] = trip_df.apply(format_address, axis=1)
    return trip_df

def format_address_g(google_df: pd.DataFrame):
    def format_address(row):
        #remove ', Milano'
        string = row['address_g']
        index = string.find(', Milano')
        if index != -1:
            return string[:index] + string[index+len(', Milano'):]
        else:
            return string
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
        return fuzz.token_set_ratio(row['formatted_name_g'], trip['formatted_name_trip'])


google_df = format_name_df(google_df, 'name_g', 'formatted_name_g')
trip_df = format_name_df(trip_df, 'name_trip', 'formatted_name_trip')

google_df = format_address_g(google_df)
trip_df = format_name_df(trip_df)
# Use list comprehension to remove spaces, make all characters lowercase, and remove special characters

#google_df.set_index('Index', inplace=True)

results = []

not_found_trip = []

not_found_google = []
#cicliamo su dataset di tripadvisor
for i,t in trip_df.iterrows():
    if i%100 == 0:
        save(results, not_found_trip, not_found_google)
    #sa ve
    print("ITERATION:", i)

    scores = []
    scores = google_df.apply(compare_row, args=(t), axis=1)
    #TO MODIFY
    for i,g in google_df.iterrows():


        score = fuzz.token_set_ratio(name_trip, name_g)
        if score >= 80:
            scores.append({'index_g': g['Index'], 'score': score, 'name_g' : g['name_g'], 'formatted_title': name_g, 'address_g': g['address_g']})
    #if unique merge
    if len(scores) == 0:
        not_found_trip.append(t)
    elif len(scores) == 1:
        #if scores[0] == 100:
        #fare comunque controllo su indirizzi
        row_g = google_df[google_df['Index'] == scores[0]['index_g']]
        address_score = fuzz.token_set_ratio(row_g['address_g'], t['address_trip'])
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
            address_score = fuzz.token_set_ratio(sc['address_g'], t['address_trip'])
            if final_score < address_score:
                final_score = address_score
                final = sc
        row_g = google_df[google_df['Index'] == final['index_g']]

        #row_g = google_df.loc[final['index_g']]
        google_df = google_df.drop(google_df[google_df['Index'] == final['index_g']].index)
        results.append({**t, **row_g})

df = pd.DataFrame(results)
df.to_csv('../output_integration/integration_definitive.csv', index=False)
df = pd.DataFrame(not_found_trip)
df.to_csv('../output_integration/not_found_trip.csv', index=False)
df = pd.DataFrame(not_found_google)
df.to_csv('../output_integration/not_found_google.csv', index=False)