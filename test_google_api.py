import requests

api_key = "AIzaSyC1Dbv0y0cXEeXwVTzxnIf3d7i4cVf6zJ0"
query = "restaurants in milan"

url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"

response = requests.get(url)
data = response.json()
print(response.headers)
print(data)
for result in data["results"]:
    print(result["name"])