from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import folium
import random
import sys
import math

# This should NOT run from the "add-location" option.  This should be a separate option
#   wherein you are searching for other clusters (NOT adding your own, because you are not at 
#   the bar, or elsewhere, yet)

# Your submitted, current location is input as your_lat, your_long, your_team

# "weighted_data" is the data thats being presented on the weighted, clustered map
#   assumed weighted_data has 4 columns: lat, long, weight, team (in that order)

def find_centerpoint(your_lat, your_long, your_team):
    weighted_data = pd.read_csv('weighted_gps_data.csv', header=None)
    weighted_data.columns = ['latitude', 'longitude', 'weight', 'team']

    team_subset = weighted_data[weighted_data['team'] == your_team]

    found = False
    closest_lat = 0
    closest_long = 0
    closest_dist = sys.maxsize

    for _, coord in team_subset.iterrows():
        dist = math.hypot(coord['latitude']-your_lat, coord['longitude']-your_long)
        if (dist < closest_dist):
            found = True
            closest_lat = coord['latitude']
            closest_long = coord['longitude']
            closest_dist = dist

    if not found:
        return (None, None)
    else:   
        return (closest_lat, closest_long)


print(find_centerpoint(40.46413233333333,-79.913525,'B'))