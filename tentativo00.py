import pandas as pd
import re
trip_advisor_cleaned_definitive = pd.read_csv("C:/Users/pc/Desktop/progetti data management/data-management-project/definitive_files_integration/trip_advisor_cleaned_DEFINITIVE.csv")
google_places_cleaned_DEFINITIVE = pd.read_csv("C:/Users/pc/Desktop/progetti data management/data-management-project/definitive_files_integration/google_places_cleaned_DEFINITIVE.csv")

# Function to clean addresses

def clean_address(address):
    try:
        if pd.isna(address) or address is None:
            return ''
        if not isinstance(address, str):
            address = str(address)
        # Remove commas followed by whitespace
        address = re.sub(r',\s+', ' ', address)
        address = address.replace('/', ',')
        # Remove leading/trailing whitespace
        address = address.strip()
        address = re.sub(r'\s+', ' ', address)
        address= address.lower()
        address = re.sub(r'\bitalia\b|\bitalian\b|\bvia\b|\bMilano\b|\bmilano\b|\bcentro commerciale\b|\bcorso\b|\bviale\b|\bpiazza\b|\bcarrefour\b|\buniversità\b|\barco della pace\b|\bpzza\b|\banfiteatro\b', ' ', address)
        address = re.sub(r'\([^)]*\)', ' ', address)
        address = re.sub(r'^\d+[\s\.,-]*', ' ', address)
        address = re.sub(r'\b\d{5}\b', ' ', address)
        address = re.sub(r'[^\w\s]', '', address)
        address = re.sub(r'[^\w\s]', '', address)
        address = re.sub(r'\s+', ' ', address)
       
        address = re.sub(r'\broad\b|\bstreet\b|\bavenue\b|\bdrive\b|\blane\b|\bway\b|\bplaza\b|\bparkway\b|\bboulevard\b|\bcourt\b', ' ', address)
        address = re.sub(r'\b(n|s|e|w|nw|ne|sw|se)\b', ' ', address)
        # Remove building/room numbers
        address = re.sub(r'\b\d{1,4}[- ]\d{1,4}\b|\b\d{1,4}[a-z]?\b', ' ', address)
        address = address.strip()
        return address
    except:
        print(f'Error processing address: {address}')
 #print(type(address))

trip_advisor_cleaned_definitive['address_trip'] = trip_advisor_cleaned_definitive['address_trip'].fillna('')
google_places_cleaned_DEFINITIVE['address_g'] = google_places_cleaned_DEFINITIVE['address_g'].fillna('')

# Convert all non-NaN values to string
trip_advisor_cleaned_definitive['address_trip'] = trip_advisor_cleaned_definitive['address_trip'].astype(str)
google_places_cleaned_DEFINITIVE['address_g'] = google_places_cleaned_DEFINITIVE['address_g'].astype(str)

# Clean the addresses in google_places_cleaned_DEFINITIVE
#google_places_cleaned_DEFINITIVE['address_g'] = google_places_cleaned_DEFINITIVE['address_g'].fillna('').apply(clean_address)

# Clean the addresses in trip_advisor_cleaned_definitive
#trip_advisor_cleaned_definitive['address_trip'] = trip_advisor_cleaned_definitive['address_trip'].fillna('').apply(lambda x: clean_address(x))
# Create backup columns
trip_advisor_cleaned_definitive = trip_advisor_cleaned_definitive.assign(address_trip_backup=trip_advisor_cleaned_definitive['address_trip'])
google_places_cleaned_DEFINITIVE = google_places_cleaned_DEFINITIVE.assign(address_g_backup=google_places_cleaned_DEFINITIVE['address_g'])


try:
    google_places_cleaned_DEFINITIVE['address_g']=google_places_cleaned_DEFINITIVE['address_g'].apply(clean_address)
    trip_advisor_cleaned_definitive['address_trip'] = trip_advisor_cleaned_definitive['address_trip'].apply(clean_address)
except TypeError:
    trip_advisor_cleaned_definitive['address_trip'] = trip_advisor_cleaned_definitive['address_trip'].apply(lambda x: x if isinstance(x, str) else None)
    trip_advisor_cleaned_definitive['address_trip'] = trip_advisor_cleaned_definitive['address_trip'].apply(clean_address)
    google_places_cleaned_DEFINITIVE['address_g'] = google_places_cleaned_DEFINITIVE['address_g'].apply(lambda x: x if isinstance(x, str) else None)
    google_places_cleaned_DEFINITIVE['address_g'] = google_places_cleaned_DEFINITIVE['address_g'].apply(clean_address)
    
    
    
    
    
print(trip_advisor_cleaned_definitive['address_trip'], google_places_cleaned_DEFINITIVE['address_g'])
trip_advisor_cleaned_definitive.to_excel('trip_indirizzo_pulito_excel.xlsx', index=False)
google_places_cleaned_DEFINITIVE.to_excel('google_indirizzo_pulito.xlsx', index=False)