#TENTATIVO PULIZIA
import re
import pandas as pd
trip_advisor_cleaned_definitive=pd.read_csv("C:/Users/pc/Desktop/progetti data management/data-management-project/definitive_files_integration/trip_advisor_cleaned_DEFINITIVE.csv")
google_places_cleaned_DEFINITIVE=pd.read_csv("C:/Users/pc/Desktop/progetti data management/data-management-project/definitive_files_integration/google_places_cleaned_DEFINITIVE.csv")
# Function to clean addresses
def clean_address(address):
    # Remove commas followed by whitespace
    address = re.sub(r',\s+', ' ', address)
    # Remove leading/trailing whitespace
    address = address.strip()
    # Convert multiple whitespace to single whitespace
    address = re.sub(r'\s+', ' ', address)
    # Convert to lowercase
    address = address.lower()
    # Remove Italian words that are commonly used in addresses
    address = re.sub(r'\bitalia\b|\bitalian\b', '', address)
    # Remove parentheses and their contents
    address = re.sub(r'\([^)]*\)', '', address)
    # Remove leading numbers and their separators
    address = re.sub(r'^\d+[\s\.,-]*', '', address)
    # Remove trailing postal codes
    address = re.sub(r'\b\d{5}\b', '', address)
    # Remove leading/trailing whitespace again
    address = address.strip()
    return address

# Clean the addresses in google_places_cleaned_DEFINITIVE
google_places_cleaned_DEFINITIVE['address_g'] = google_places_cleaned_DEFINITIVE['address_g'].apply(clean_address)

# Clean the addresses in trip_advisor_cleaned_definitive
trip_advisor_cleaned_definitive['address_trip'] = trip_advisor_cleaned_definitive['address_trip'].apply(clean_address)
