import folium

#create map object

lat = 50.721802
long = -3.533620
location = [lat, long]
m = folium.Map(location=location, zoom_start=15)

#tooltip
tooltip = 'Click for more info'

#create markers:
folium.Marker(location, popup="<strong>Location One</strong>", tooltip=tooltip).add_to(m)

#generate map
m.save('map.html')