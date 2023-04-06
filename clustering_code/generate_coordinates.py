import random
import pandas as pd
import folium

# Use to generate random coordinates in pittsburgh

# set values as you wish
teams = 8   # <= 15 teams (only 15 colors currently listed)
coords_per_team = 50
team_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]

# Define the latitude and longitude range (Pittsburgh, PA)
lat_min, lat_max = 40.40, 40.50
lon_min, lon_max = -80.10, -79.90

# generate coordinates
coords = []
for t in range(teams):
    for c in range(coords_per_team):
        lat = round(random.uniform(lat_min, lat_max), 6)
        lon = round(random.uniform(lon_min, lon_max), 6)
        coords.append((lat, lon, team_names[t]))

gps_data = pd.DataFrame(coords, columns=['latitude', 'longitude', 'team'])

gps_data.to_csv('gps_data.csv', index=False, header=False)

