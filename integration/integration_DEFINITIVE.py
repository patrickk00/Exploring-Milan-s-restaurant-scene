from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import string
from fuzzywuzzy import fuzz


google_df = pd.read_excel('C:/Users/pc/Desktop/progetti data management/data-management-project/google_indirizzo_pulito.xlsx')
trip_df = pd.read_excel('C:/Users/pc/Desktop/progetti data management/data-management-project/trip_indirizzo_pulito_excel.xlsx')


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
        df.to_excel('integration_definitive.xlsx', index=False)
        df = pd.DataFrame(not_found_trip)
        df.to_excel('not_found_trip.xlsx', index=False)
        df = pd.DataFrame(not_found_google)
        df.to_excel('not_found_google.xlsx', index=False)
    print("ITERATION:", i)
    name_trip = t['name_trip'].replace(" ", "").lower().translate(trans_table)
    name_trip = name_trip.replace("restaurant", "1")
    name_trip = name_trip.replace("ristorante", "2")
    name_trip = name_trip.replace("sushi", "3")
    name_trip = name_trip.replace("kebab", "4")
    name_trip = name_trip.replace("restaurant", "5")
    # Create a new column with just the street address
    #trip_df['address_trip'] = trip_df['address_trip'].str.split(',').str[0]
    #trip_df['address_trip'] = trip_df['address_trip'].str.strip()

    scores = []
    for i,g in google_df.iterrows():
        name_g = g['name_g'].replace(" ", "").lower().translate(trans_table)
        name_g = name_g.replace("restaurant", "1")
        name_g = name_g.replace("ristorante", "2")
        name_g = name_g.replace("sushi", "3")
        name_g = name_g.replace("kebab", "4")
        name_g = name_g.replace("restaurant", "5")
        #google_df['address_g'] = google_df['address_g'].str.split(',').str[0]
        #google_df['address_g'] = google_df['address_g'].str.strip()

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
df.to_excel('integration_definitive.xlsx', index=False)
df = pd.DataFrame(not_found_trip)
df.to_excel('not_found_trip.xlsx', index=False)
df = pd.DataFrame(not_found_google)
df.to_excel('not_found_google.xlsx', index=False)