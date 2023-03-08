import pandas as pd
#import jellyfish
#from itertools import product
#from tqdm import tqdm

# Load the two datasets into pandas dataframes
google_df = pd.read_excel('C:/Users/pc/Desktop/progetti data management/data-management-project/google_indirizzo_pulito.xlsx')
trip_df = pd.read_excel('C:/Users/pc/Desktop/progetti data management/data-management-project/trip_indirizzo_pulito_excel.xlsx')




from geopy.geocoders import Nominatim
# Set up the geocoding client
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='my-app')
location = geolocator.geocode('Via Monte Napoleone 8, 20121 Milano MI, Italy')

street = location.raw['road']
city = location.raw['address']['city']
postal_code = location.raw['address']['postcode']

print(street, city, postal_code)

