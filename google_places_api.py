import time
import requests
import pandas as pd
import utils.coordinate_distances as coordinate_distances
import configparser
config = configparser.ConfigParser()
config.read('credentials.txt')
sapi_key = config['API_KEY']['key']
location = "Milan"
query = "restaurant"

url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}+in+{location}&key={api_key}"
response = requests.get(url)
data = response.json()
coordinates=[[45.532720, 9.065930],
[45.532720, 9.283597],
[45.403184, 9.283597],
[45.403184, 9.065930]]


radius = "100" # radius in meters
types = "restaurant"
results = []

starting_lat = coordinates[3][0]
starting_lon = coordinates[3][1]
ending_lat = coordinates[1][0]
ending_lon = coordinates[1][1] 
coordinates_array = [[starting_lat,starting_lon]]

while starting_lat < ending_lat:
    starting_lon = coordinates[3][1]
    while starting_lon < ending_lon:
      print("hello", starting_lon)
      new_lat, new_lon =  coordinate_distances.move_coordinate(starting_lat, starting_lon, 0, 100)
      coordinates_array.append([new_lat,new_lon])  
      starting_lon = new_lon 
    new_lat, new_lon =  coordinate_distances.move_coordinate(starting_lat, starting_lon, 100, 0)
    coordinates_array.append([new_lat,new_lon])
    starting_lat = new_lat
print(len(coordinates_array))
with open("coordinates.txt", "w") as f:
    for element in coordinates_array:
        f.write(str(element[0]) + ',' + str(element[1]) + "\n")
i = 0
for c in coordinates_array:
    i+=1
    if i > 100:
        #time.sleep(5)
        i=0
        df = pd.DataFrame(results)
        df.to_csv('google_places.csv', index=False)
    print("for", c)
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={c[0]},{c[1]}&radius={radius}&types={types}&page_size=60&key={api_key}"
    response = requests.get(url)
    print(response.headers)
    data = response.json()
    print(data)
    results.extend(data["results"])   

    #print(response.request.headers)
    #print(response.headers)
    #next_page_token = data.get("next_page_token")
    # while next_page_token:
    #     try:

    #         url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={api_key}"
    #         response = requests.get(url)
    #         data = response.json()
    #         results += data["results"]
    #     except KeyError:
    #         break
    #     if "INVALID_REQUEST" in data['status']:
    #         time.sleep(5)
    #     else:
    #         next_page_token = data.get("next_page_token")
# Print the name and address of each restaurant
#print(results)
df = pd.DataFrame(results)
df.to_csv('google_places.csv', index=False)
df.to_excel('google_placess.xlsx')
# for result in data["results"]:
#     print(result["name"])
#     print(result["formatted_address"])
#     print("---")



#45.532720, 9.065930
#45.532720, 9.283597
#45.403184, 9.283597
#45.403184, 9.065930
