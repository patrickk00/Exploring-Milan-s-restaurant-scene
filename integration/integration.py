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

google_df = pd.read_csv('./output_files/google_dataset_cleaned_2.csv')
trip_df = pd.read_csv('./output_files/trip_advisor_cleaned.csv')


name_google_list = list(google_df['name_google'])
name_trip_list = list(trip_df['name_trip'])

#sort to get a faster search
name_google_list = sorted(name_google_list)
name_trip_list = sorted(name_trip_list)
# Define the translation table for removing special characters
trans_table = str.maketrans('', '', string.punctuation)

## Use list comprehension to remove spaces, make all characters lowercase, and remove special characters from the two lists to compare them without useless things
google_list_cl = [s.replace(" ", "").lower().translate(trans_table) for s in name_google_list]
trip_list_cl = [s.replace(" ", "").lower().translate(trans_table) for s in name_trip_list]

results = []

#Define a function 'match' to perform the record linkage between a restaurant name from the TripAdvisor dataset and all restaurants in the Google dataset
def match (i_t, t):
    found = False
    high_score = []
    for i_g, g in enumerate(google_list_cl):
        score = fuzz.token_set_ratio(t, g)
        if score == 100:
            high_score = []
            high_score.append({'score': score, 'google': name_google_list[i_g], 'formatted_google': g})
            found = True
            break
        else:
            if score >= 80:
                high_score.append({'score': score, 'google': name_google_list[i_g], 'formatted_google': g})
    return {'trip': name_trip_list[i_t], 'similar': high_score}

# for i_t, t in enumerate(trip_list_cl):
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(match, i_t, t) for i_t, t in enumerate(trip_list_cl)]
    for future in as_completed(futures):
        print("complete!", future.result)
        res = future.result()
        if res:
            results.append(res)
# for t in name_trip_list:
#     found = False
#     lev_dist = []
#     for g in name_google_list:
#         if t == g:
#             print("FOUND", g)
#             found = True
#             break
#     if not found:
#         print("NOT FOUND", t)
#         for g in name_google_list:
#             lev_dist.append({'lv': levenshtein_distance(g,t), 'google': g, 'trip': t})
#         min_dist = min(lev_dist, key=lambda x: x['lv'])
#         min_dist_elems = [d for d in lev_dist if d['lv'] == min_dist['lv']]
#         print("LIST OF MIN DISTANCES: ", min_dist_elems)
#         results.append({'link': min_dist_elems, 'google': g, 'trip': t})
#     else:
#         results.append({'link': t, 'google': g, 'trip': t})
       
df = pd.DataFrame(results)
df.to_csv('./output_files/record_linkage_index.csv', index=False)

