import math

def move_coordinate(lat, lon, lat_distance, lon_distance):
    # Earth's radius in meters
    R = 6371000

    # Convert coordinates to radians
    lat, lon = map(math.radians, [lat, lon])

    # Calculate new latitude and longitude
    new_lat = lat + lat_distance / R
    new_lon = lon + (lon_distance / R) # * math.cos(lat)

    # Convert coordinates back to degrees
    new_lat, new_lon = map(math.degrees, [new_lat, new_lon])

    return (new_lat, new_lon)


