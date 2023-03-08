import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# load the two datasets into pandas dataframes

df1 = pd.read_csv('../definitive_files_integration/google_places_cleaned_DEFINITIVE.csv')
df2 = pd.read_csv('../definitive_files_integration/trip_advisor_cleaned_DEFINITIVE.csv')

# create a function to perform fuzzy matching on restaurant names and addresses
def fuzzy_match(row, choices, scorer, cutoff):
    name = row['name_g']
    address = row['address_g']
    matches = process.extractBests(name, choices=choices, scorer=scorer, score_cutoff=cutoff)
    for match in matches:
        if fuzz.partial_ratio(match[0], address) > cutoff:
            return match[1]
    return None

# perform fuzzy matching on restaurant names and addresses in df1
df1['match'] = df1.apply(fuzzy_match, choices=df2['name_trip'], scorer=fuzz.token_sort_ratio, cutoff=80, axis=1)

# merge the two datasets on the matched restaurant names
merged_df = pd.merge(df1, df2, left_on='match', right_on='name_g', how='inner')

# save the merged dataframe to a csv file
merged_df.to_csv('merged_dataset.csv', index=False)