from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import string
from fuzzywuzzy import fuzz


google_df = pd.read_csv('../definitive_files_integration/google_places_cleaned_DEFINITIVE.csv')
trip_df = pd.read_csv('../definitive_files_integration/trip_advisor_cleaned_DEFINITIVE.csv')


# Define the translation table for removing special characters
trans_table = str.maketrans('', '', string.punctuation)

# Use list comprehension to remove spaces, make all characters lowercase, and remove special characters

#google_df.set_index('Index', inplace=True)

results = []

not_found_trip = []

not_found_google = []
#cicliamo su dataset di tripadvisor
for i,t in trip_df.iterrows():
    if i%100 == 0:
        df = pd.DataFrame(results)
        df.to_csv('../output_integration/integration_definitive.csv', index=False)
        df = pd.DataFrame(not_found_trip)
        df.to_csv('../output_integration/not_found_trip.csv', index=False)
        df = pd.DataFrame(not_found_google)
        df.to_csv('../output_integration/not_found_google.csv', index=False)
    print("ITERATION:", i)
    name_trip = t['name_trip'].replace(" ", "").lower().translate(trans_table)
    name_trip = name_trip.replace("restaurant", "1")
    name_trip = name_trip.replace("ristorante", "2")
    name_trip = name_trip.replace("sushi", "3")
    name_trip = name_trip.replace("kebab", "4")
    name_trip = name_trip.replace("restaurant", "5")
    scores = []
    for i,g in google_df.iterrows():
        name_g = g['name_g'].replace(" ", "").lower().translate(trans_table)
        name_g = name_g.replace("restaurant", "1")
        name_g = name_g.replace("ristorante", "2")
        name_g = name_g.replace("sushi", "3")
        name_g = name_g.replace("kebab", "4")
        name_g = name_g.replace("restaurant", "5")

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