import json
import folium

# Function which adds a location to the map
def add_location(map, location, popup):
    #tooltip
    tooltip = 'Click for more info'
    folium.Marker(location, popup, tooltip=tooltip).add_to(map)
    return map

# Function to open and return a json file 
def open_json_file(file_name):
    file = open(file_name)
    return json.load(file)

# Open and load json file containing locations 
locations = open_json_file('latLong.json')

# Map is centred at this location
center = [50.735805, -3.533051]

# Map that is bounded to Exeter Uni
map = folium.Map(location = center,
                 min_lon=-3.520532,
                 max_lon=-3.548116,
                 min_lat=50.729748,
                 max_lat=50.741780,
                 max_bounds=True,
                 zoom_start = 16,
                 min_zoom = 15)

# Create markers for locations in the json file:
for location in locations:
    coords = [location['lat'], location['long']]
    popup = location['locationName']
    map = add_location(map, coords, popup)

# Generate map
map.save('map.html')