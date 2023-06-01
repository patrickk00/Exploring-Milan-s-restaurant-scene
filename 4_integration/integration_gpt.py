import pandas as pd
from rapidfuzz import fuzz
from rapidfuzz import process

# carica i due dataset come dataframe
google_df = pd.read_csv(
    "../definitive_files_integration/google_places_cleaned_DEFINITIVE.csv"
)
trip_df = pd.read_csv(
    "../definitive_files_integration/trip_advisor_cleaned_DEFINITIVE.csv"
)

# crea una nuova colonna 'match' nel dataframe 1
google_df["match"] = ""

# itera attraverso le righe del dataframe 1 e cerca corrispondenze nel dataframe 2
for index1, row1 in google_df.iterrows():
    best_match = None
    best_ratio = -1
    print("chacha", index1)
    # itera attraverso le righe del dataframe 2 e confronta la stringa dell'indirizzo e del nome
    for index2, row2 in trip_df.iterrows():
        ratio = fuzz.token_sort_ratio(row1["address_g"], row2["address_trip"])
        ratio += fuzz.token_sort_ratio(row1["name_g"], row2["name_trip"])
        # se la corrispondenza è migliore rispetto alle precedenti trovate
        # salva la riga del dataframe 2 e l'indice di ratio corrispondente
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = index2
    # se è stata trovata una corrispondenza, salva l'indice del dataframe 2 nella colonna 'match'
    if best_match is not None:
        google_df.at[index1, "match"] = best_match

# unisci i due dataframe usando la colonna 'match'
df_merged = pd.merge(
    google_df,
    trip_df,
    how="left",
    left_on="match",
    right_index=True,
    suffixes=("_1", "_2"),
)

df_merged.to_csv("integration_gpt.csv", index=False)
